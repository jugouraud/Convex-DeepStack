import json
import time
from copy import deepcopy
from dataclasses import dataclass

import numpy as np
import optuna
from optuna.samplers import TPESampler

try:
    from tqdm.auto import tqdm
except ImportError:  # pragma: no cover - progress bars are optional
    tqdm = None

from .utils import DEVICE, set_global_seed
from .metrics import evaluate_model_on_splits
from convex_deepstack import ConvexDeepStack, DeepStackConfig
from convex_deepstack.models import suppress_cvxpy_vec_futurewarning
from .comparison_models import (
    ResNetRegressor,
    ResNetTrainingConfig,
    ResNetTrainingData,
    train_resnet_best_epoch,
    train_wadiro_or_scnn,
)


@dataclass
class ModelStudyContext:
    """State shared by all trials in one model/configuration study."""

    data: dict
    model_name: str
    base_config: dict
    corruption_fraction: float
    corruption_mode: str
    result_rows: list[dict]


@dataclass(frozen=True)
class TrialOutcome:
    """Training/evaluation outcome used to construct a normalized result row."""

    status: str
    training_seconds: float
    metrics: dict | None = None
    extra: dict | None = None
    error: str = ""


def set_trial_seed(seed: int) -> None:
    """Seed all RNGs for a single hyperparameter trial."""
    set_global_seed(int(seed))


def _space_float(trial, name, spec):
    return trial.suggest_float(
        name,
        float(spec["low"]),
        float(spec["high"]),
        log=bool(spec.get("log", False)),
    )


def _space_int(trial, name, spec):
    return trial.suggest_int(name, int(spec["low"]), int(spec["high"]))


def suggest_trial_config(trial, model_name, base_config):
    """Return a copy of the experiment config populated from one Optuna trial."""
    config = deepcopy(base_config)
    space = base_config["search_space"]

    if model_name in ("WaDiRo", "WaDiRo-SCNN"):
        config["wadiro_radius"] = _space_float(
            trial,
            "wadiro_radius",
            space["wadiro_radius"],
        )
    elif model_name == "SCNN":
        config["scnn_lamb_reg"] = _space_float(
            trial,
            "scnn_lamb_reg",
            space["scnn_lamb_reg"],
        )
        config["scnn_regularizer"] = trial.suggest_categorical(
            "scnn_regularizer",
            list(space["scnn_regularizer"]),
        )
    elif model_name == "ResNet":
        config["resnet_layers"] = _space_int(trial, "resnet_layers", space["resnet_layers"])
        config["resnet_dropout"] = _space_float(
            trial,
            "resnet_dropout",
            space["resnet_dropout"],
        )
        config["learning_rate"] = _space_float(
            trial,
            "learning_rate",
            space["resnet_learning_rate"],
        )
        config["weight_decay"] = _space_float(
            trial,
            "weight_decay",
            space["resnet_weight_decay"],
        )
        config["batch_size"] = trial.suggest_categorical(
            "batch_size",
            list(space["resnet_batch_size"]),
        )
    elif model_name == "Convex DeepStack":
        config["convex_nu"] = _space_float(trial, "convex_nu", space["convex_nu"])
        config["convex_max_blocks"] = _space_int(
            trial,
            "convex_max_blocks",
            space["convex_max_blocks"],
        )
        config["convex_max_evals"] = _space_int(
            trial,
            "convex_max_evals",
            space["convex_max_evals"],
        )
        config["convex_warmup"] = _space_int(
            trial,
            "convex_warmup",
            space["convex_warmup"],
        )
        config["convex_k_stop"] = _space_int(
            trial,
            "convex_k_stop",
            space["convex_k_stop"],
        )
    else:
        raise ValueError(f"Unknown model_name={model_name!r}")

    return config


def dataset_metadata(context: ModelStudyContext) -> dict:
    """Return the dataset columns repeated on each trial record."""
    data = context.data
    return {
        "function": data["function_name"],
        "dimension": data["n_dim"],
        "samples_per_dim": data["samples_per_dim"],
        "seed": data["seed"],
        "corruption_mode": context.corruption_mode,
        "corruption_fraction": float(context.corruption_fraction),
        "n_train": data["n_train"],
        "n_train_base": data["n_train_base"],
        "n_inserted_outliers": data["n_inserted_outliers"],
        "n_val": data["n_val"],
        "n_test": data["n_test"],
    }


def _train_convex_backend(model_name: str, data: dict, trial_config: dict):
    backend_name = "scnn" if model_name == "SCNN" else "wadiro"
    _, torch_model = train_wadiro_or_scnn(
        backend_name,
        data["X_train_s"],
        data["y_train_s"],
        cfg=trial_config,
        device=DEVICE,
    )
    return torch_model, {}


def _train_resnet(data: dict, trial_config: dict):
    model = ResNetRegressor(
        in_dim=data["n_dim"],
        width=trial_config["resnet_width"],
        n_layers=trial_config["resnet_layers"],
        dropout=trial_config["resnet_dropout"],
        out_dim=1,
    )
    training_data = ResNetTrainingData(
        x_train=data["X_train_s"].astype(np.float32),
        y_train=data["y_train_s"].astype(np.float32),
        x_val=data["X_val_s"].astype(np.float32),
        y_val=data["y_val_s"].astype(np.float32),
    )
    training_config = ResNetTrainingConfig(
        epochs=int(trial_config["resnet_epochs"]),
        patience=int(trial_config["resnet_patience"]),
        batch_size=int(trial_config["batch_size"]),
        learning_rate=float(trial_config["learning_rate"]),
        weight_decay=float(trial_config["weight_decay"]),
        device=DEVICE,
    )
    model, best = train_resnet_best_epoch(model, training_data, training_config)
    return model, {
        "resnet_best_epoch": best.get("epoch", np.nan),
        "resnet_best_val_mse_scaled": best.get("val_mse_scaled", np.nan),
    }


def _compact_block_history(history: dict) -> list[dict]:
    fields = (
        "block_idx",
        "best_params",
        "best_val",
        "model_val_mse_after",
        "absolute_improvement",
        "relative_improvement",
        "meets_improvement_tol",
        "consecutive_low_improvement",
        "block_patience",
        "best_weight",
        "added",
        "stop_reason",
    )
    return [
        {field: block.get(field) for field in fields}
        for block in history.get("blocks", [])
    ]


def _deepstack_extra(history: dict, trial_config: dict) -> dict:
    blocks = history.get("blocks", [])
    accepted_blocks = [block for block in blocks if bool(block.get("added"))]
    final_val_mse = (
        accepted_blocks[-1].get("model_val_mse_after", np.nan)
        if accepted_blocks
        else history.get("baseline_val_mse", np.nan)
    )
    return {
        "convex_n_blocks": int(history.get("n_blocks_accepted", len(accepted_blocks))),
        "convex_n_block_attempts": int(history.get("n_block_attempts", len(blocks))),
        "convex_stop_reason": history.get("stop_reason"),
        "convex_min_blocks": int(
            history.get("min_blocks", trial_config.get("convex_min_blocks", 2))
        ),
        "convex_block_patience": int(
            history.get("block_patience", trial_config.get("convex_block_patience", 2))
        ),
        "convex_low_improvement_streak_at_stop": int(
            history.get("consecutive_low_improvement_at_stop", 0)
        ),
        "convex_baseline_val_mse_scaled": history.get("baseline_val_mse", np.nan),
        "convex_final_val_mse_scaled": final_val_mse,
        "convex_block_history_json": json.dumps(_compact_block_history(history), default=str),
    }


def _train_deepstack(data: dict, trial_config: dict, trial_seed: int):
    model = ConvexDeepStack(in_dim_x=data["n_dim"], out_dim=1)
    search_config = DeepStackConfig(
        nu=float(trial_config["convex_nu"]),
        improvement_tol=float(trial_config["convex_improvement_tol"]),
        min_blocks=int(trial_config.get("convex_min_blocks", 5)),
        block_patience=int(trial_config.get("convex_block_patience", 2)),
        max_blocks=int(trial_config["convex_max_blocks"]),
        max_evals=int(trial_config["convex_max_evals"]),
        warmup=int(trial_config["convex_warmup"]),
        k_stop=int(trial_config["convex_k_stop"]),
        verbose=False,
        seed=int(trial_seed),
        optuna_multivariate=bool(trial_config.get("convex_optuna_multivariate", True)),
        optuna_group=bool(trial_config.get("convex_optuna_group", True)),
    )
    history = model.build_optimal_model(
        data["X_train_s"].astype(np.float64),
        data["y_train_s"].astype(np.float64),
        data["X_val_s"].astype(np.float64),
        data["y_val_s"].astype(np.float64),
        config=search_config,
    )
    model.to(DEVICE)
    model.eval()
    return model, _deepstack_extra(history, trial_config)


def train_model_from_trial_config(
    model_name: str,
    data: dict,
    trial_config: dict,
    trial_seed: int,
):
    """Dispatch one model training run from its normalized trial configuration."""
    set_trial_seed(trial_seed)
    if model_name in {"SCNN", "WaDiRo", "WaDiRo-SCNN"}:
        return _train_convex_backend(model_name, data, trial_config)
    if model_name == "ResNet":
        return _train_resnet(data, trial_config)
    if model_name == "Convex DeepStack":
        return _train_deepstack(data, trial_config, trial_seed)
    raise ValueError(f"Unknown model_name={model_name!r}")


def _hyperparameter_columns(trial_config: dict) -> dict:
    names = (
        "wadiro_radius",
        "wadiro_wasserstein",
        "scnn_lamb_reg",
        "scnn_regularizer",
        "scnn_loss",
        "wide_neurons",
        "solver",
        "resnet_width",
        "resnet_layers",
        "resnet_dropout",
        "learning_rate",
        "weight_decay",
        "batch_size",
        "convex_nu",
        "convex_max_blocks",
        "convex_max_evals",
        "convex_warmup",
        "convex_k_stop",
        "convex_improvement_tol",
        "convex_min_blocks",
        "convex_block_patience",
    )
    return {name: trial_config.get(name, np.nan) for name in names}


def make_trial_row(
    context: ModelStudyContext,
    trial,
    trial_config: dict,
    outcome: TrialOutcome,
) -> dict:
    """Build one normalized, CSV-ready trial record."""
    row = dataset_metadata(context)
    row.update(
        {
            "Model": context.model_name,
            "trial_number": trial.number,
            "trial_seed": trial_config.get("trial_seed", np.nan),
            "status": outcome.status,
            "training_seconds": float(outcome.training_seconds),
            "error": outcome.error,
        }
    )
    row.update(_hyperparameter_columns(trial_config))

    if outcome.metrics:
        row.update(outcome.metrics)
    else:
        for split in ("val", "test"):
            for metric_name in (
                "MSE",
                "MinMax_normalised_MSE",
                "Variance_normalised_MSE",
            ):
                row[f"{split}_{metric_name}"] = np.nan

    if outcome.extra:
        row.update(outcome.extra)

    row["optuna_params_json"] = json.dumps(trial.params, sort_keys=True)
    row["objective_metric"] = trial_config["objective_metric"]
    row["objective_value"] = row.get(trial_config["objective_metric"], np.nan)
    return row


def _trial_seed(data_seed: int, trial_number: int) -> int:
    return int(data_seed * 10_000 + trial_number)


def run_model_study(context: ModelStudyContext):
    """Run all Optuna trials for one model on one dataset configuration."""
    data = context.data
    model_name = context.model_name
    base_config = context.base_config
    n_trials = int(
        base_config["n_trials"].get(
            model_name,
            base_config["n_trials"].get("WaDiRo", 1),
        )
    )
    sampler = TPESampler(
        seed=int(data["seed"]),
        multivariate=True,
        group=True,
        n_startup_trials=min(5, max(1, n_trials // 4)),
    )
    study = optuna.create_study(direction="minimize", sampler=sampler)

    def objective(trial):
        trial_config = suggest_trial_config(trial, model_name, base_config)
        trial_seed = _trial_seed(int(data["seed"]), trial.number)
        trial_config["trial_seed"] = trial_seed
        start = time.perf_counter()

        try:
            with suppress_cvxpy_vec_futurewarning():
                torch_model, extra = train_model_from_trial_config(
                    model_name,
                    data,
                    trial_config,
                    trial_seed,
                )
            metrics = evaluate_model_on_splits(
                torch_model,
                data,
                batch_size=trial_config.get("batch_size", 128),
            )
            outcome = TrialOutcome(
                status="ok",
                training_seconds=time.perf_counter() - start,
                metrics=metrics,
                extra=extra,
            )
        except Exception as exc:
            outcome = TrialOutcome(
                status="failed",
                training_seconds=time.perf_counter() - start,
                error=repr(exc),
            )

        row = make_trial_row(context, trial, trial_config, outcome)
        context.result_rows.append(row)
        trial.set_user_attr("result_row", row)
        objective_value = row[base_config["objective_metric"]]
        return float(objective_value) if np.isfinite(objective_value) else float("inf")

    study.optimize(
        objective,
        n_trials=n_trials,
        gc_after_trial=True,
        show_progress_bar=False if model_name == "Convex DeepStack" else bool(tqdm),
    )
    return study
