"""Run Convex DeepStack across the complete configured synthetic benchmark grid."""

import argparse
import json
import math
import os
import tempfile
import time
import warnings
from copy import deepcopy
from pathlib import Path
from typing import Any

import numpy as np

from .config import make_default_config
from .sweep import _grid_points, make_dataset_for_grid_point
from .tuning import ModelStudyContext, run_model_study
from .utils import initialize_environment


def _json_value(value: Any) -> Any:
    """Convert NumPy values and non-finite floats into portable JSON values."""
    if isinstance(value, np.generic):
        value = value.item()
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if isinstance(value, dict):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_value(item) for item in value]
    return value


def _write_json(path: Path, payload: Any) -> None:
    """Write one complete JSON document atomically."""
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.stem}-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(_json_value(payload), handle, indent=2, sort_keys=True)
            handle.write("\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _summary_record(row: dict) -> dict:
    """Select the result and timing fields intended for experiment reporting."""
    fields = (
        "function", "dimension", "samples_per_dim", "seed", "corruption_mode",
        "corruption_fraction", "n_train", "n_train_base", "n_inserted_outliers",
        "n_val", "n_test", "status", "error", "training_seconds", "objective_metric",
        "objective_value", "val_MSE", "val_MinMax_normalised_MSE",
        "test_MSE", "test_MinMax_normalised_MSE",
    )
    return {field: row.get(field) for field in fields}


def _composition_record(row: dict) -> dict:
    """Extract final stack structure, selected hyperparameters, and block history."""
    history_text = row.get("convex_block_history_json")
    try:
        block_history = json.loads(history_text) if history_text else []
    except json.JSONDecodeError:
        block_history = []
    fields = (
        "function", "dimension", "samples_per_dim", "seed", "corruption_mode",
        "corruption_fraction", "status", "error", "trial_seed", "optuna_params_json",
        "convex_n_blocks", "convex_n_block_attempts", "convex_stop_reason",
        "convex_min_blocks", "convex_block_patience",
        "convex_low_improvement_streak_at_stop", "convex_baseline_val_mse_scaled",
        "convex_final_val_mse_scaled",
    )
    record = {field: row.get(field) for field in fields}
    record["block_history"] = block_history
    return record


def make_cds_synthetic_config() -> dict:
    """Return the default full synthetic grid restricted to one CDS trial per point."""
    config = deepcopy(make_default_config())
    config["models_to_run"] = ["Convex DeepStack"]
    config["n_trials"] = {"Convex DeepStack": 1}
    return config


def run_cds_synthetic_experiment(
    output_dir: str | Path = "outputs/cds_synthetic",
    *,
    config: dict | None = None,
) -> tuple[list[dict], list[dict]]:
    """Run CDS on every configured synthetic point and checkpoint two JSON artifacts.

    The summary artifact stores final evaluation metrics and training duration. The
    composition artifact records each final stack's selected trial configuration,
    accepted block weights, block types, and stopping history.
    """
    config = make_cds_synthetic_config() if config is None else deepcopy(config)
    if config.get("models_to_run") != ["Convex DeepStack"]:
        raise ValueError("The CDS synthetic runner requires models_to_run=['Convex DeepStack'].")
    if int(config["n_trials"].get("Convex DeepStack", 0)) != 1:
        raise ValueError("The CDS synthetic runner requires exactly one CDS trial per grid point.")

    output = Path(output_dir)
    results_path = output / "cds_synthetic_results.json"
    compositions_path = output / "cds_synthetic_model_compositions.json"
    points = _grid_points(config)
    summaries: list[dict] = []
    compositions: list[dict] = []
    initialize_environment(seed=int(config["sweep_seeds"][0]))

    print(f"CDS synthetic grid: {len(points)} studies; output={output}", flush=True)
    for index, point in enumerate(points, start=1):
        data, corruption_mode = make_dataset_for_grid_point(point, config)
        print(
            f"[{index}/{len(points)}] start function={point.function_name} d={point.dimension} "
            f"samples_per_dim={point.samples_per_dim} seed={point.seed} "
            f"corruption={corruption_mode}:{point.corruption_fraction}",
            flush=True,
        )
        rows: list[dict] = []
        started = time.perf_counter()
        study = run_model_study(ModelStudyContext(
            data=data,
            model_name="Convex DeepStack",
            base_config=config,
            corruption_fraction=float(point.corruption_fraction),
            corruption_mode=corruption_mode,
            result_rows=rows,
        ))
        row = study.trials[0].user_attrs["result_row"]
        summary = _summary_record(row)
        summaries.append(summary)
        compositions.append(_composition_record(row))
        _write_json(results_path, summaries)
        _write_json(compositions_path, compositions)
        print(
            f"[{index}/{len(points)}] {summary['status']} "
            f"training_seconds={summary['training_seconds']:.2f} "
            f"wall_seconds={time.perf_counter() - started:.2f} "
            f"test_minmax_mse={summary['test_MinMax_normalised_MSE']}",
            flush=True,
        )
    return summaries, compositions


def main() -> None:
    parser = argparse.ArgumentParser(description="Run CDS on the full synthetic benchmark grid")
    parser.add_argument("--output-dir", default="outputs/cds_synthetic")
    arguments = parser.parse_args()
    # The full grid can emit thousands of repetitive upstream solver and Optuna
    # warnings. Keep terminal output focused on progress and real exceptions.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        run_cds_synthetic_experiment(arguments.output_dir)


if __name__ == "__main__":
    main()
