
from __future__ import annotations

import math
import warnings
from contextlib import contextmanager
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Mapping

import numpy as np
import optuna
import torch
import torch.nn as nn
import wadiroscnn
from optuna.samplers import TPESampler

try:
    from tqdm.auto import tqdm
except ImportError:
    tqdm = None


@contextmanager
def suppress_cvxpy_vec_futurewarning():
    """Suppress the CVXPY vectorization FutureWarning during convex training calls.

    Args:
        None.

    Returns:
        ContextManager[None]: A context manager that temporarily suppresses the warning.
    """
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message=r".*You didn't specify the order of the vec expression.*",
            category=FutureWarning,
            module=r"cvxpy.*",
        )
        yield


def scnn(*args: Any, **kwargs: Any):
    """Instantiate an SCNN model from the upstream WaDiRo-SCNN package.

    Args:
        *args (Any): Positional arguments forwarded to the SCNN constructor.
        **kwargs (Any): Keyword arguments forwarded to the SCNN constructor.

    Returns:
        Any: An initialized upstream SCNN model instance.
    """
    return wadiroscnn.scnn(*args, **kwargs)


def wadiro_scnn(*args: Any, **kwargs: Any):
    """Instantiate a WaDiRo-SCNN model from the upstream package.

    Args:
        *args (Any): Positional arguments forwarded to the WaDiRo-SCNN constructor.
        **kwargs (Any): Keyword arguments forwarded to the WaDiRo-SCNN constructor.

    Returns:
        Any: An initialized upstream WaDiRo-SCNN model instance.
    """
    return wadiroscnn.wadiro_scnn(*args, **kwargs)


@dataclass(frozen=True)
class ResidualSearchData:

    x_train: np.ndarray
    y_train: np.ndarray
    x_val: np.ndarray
    y_val: np.ndarray
    y_train_previous: np.ndarray
    y_val_previous: np.ndarray


@dataclass(frozen=True)
class EarlyExitConfig:

    max_evals: int
    warmup: int
    alpha: float
    alpha_consistency: float
    alpha_rarity: float
    gamma: float
    eps_stab: float
    stability_window: int
    recent_window: int
    k_stop: int
    seed: int
    verbose: bool
    optuna_multivariate: bool
    optuna_group: bool
    optuna_n_startup_trials: int | None
    optuna_min_startup_trials: int
    optuna_warn_independent_sampling: bool
    optuna_sampler_kwargs: Mapping[str, Any] | None


@dataclass(frozen=True)
class DeepStackConfig:

    nu: float = 0.1
    improvement_tol: float = 1e-3
    min_blocks: int = 2
    block_patience: int = 2
    max_blocks: int | None = None
    max_evals: int = 100
    alpha: float = 0.1
    alpha_consistency: float = 0.8
    alpha_rarity: float = 0.1
    gamma: float = 0.01
    eps_stab: float = 5e-3
    stability_window: int = 10
    recent_window: int = 10
    k_stop: int = 3
    warmup: int = 10
    verbose: bool = True
    seed: int = 0
    optuna_multivariate: bool = True
    optuna_group: bool = True
    optuna_n_startup_trials: int | None = None
    optuna_min_startup_trials: int = 20
    optuna_warn_independent_sampling: bool = True
    optuna_sampler_kwargs: Mapping[str, Any] | None = None

    def early_exit_for_block(self, block_index: int) -> EarlyExitConfig:
        """Create deterministic early-exit search settings for a residual block.

        Args:
            block_index (int): One-based index of the residual block.

        Returns:
            EarlyExitConfig: Configuration for the block.
        """
        return EarlyExitConfig(
            max_evals=self.max_evals,
            warmup=self.warmup,
            alpha=self.alpha,
            alpha_consistency=self.alpha_consistency,
            alpha_rarity=self.alpha_rarity,
            gamma=self.gamma,
            eps_stab=self.eps_stab,
            stability_window=self.stability_window,
            recent_window=self.recent_window,
            k_stop=self.k_stop,
            seed=int(self.seed) + block_index - 1,
            verbose=self.verbose,
            optuna_multivariate=self.optuna_multivariate,
            optuna_group=self.optuna_group,
            optuna_n_startup_trials=self.optuna_n_startup_trials,
            optuna_min_startup_trials=self.optuna_min_startup_trials,
            optuna_warn_independent_sampling=self.optuna_warn_independent_sampling,
            optuna_sampler_kwargs=self.optuna_sampler_kwargs,
        )


def _suggest_params_optuna(trial):
    """Sample one conditional residual-block configuration with Optuna.

    Args:
        trial (optuna.trial.Trial): Optuna trial used to sample hyperparameters.

    Returns:
        dict[str, Any]: Sampled block type and associated hyperparameters.
    """
    block_type = trial.suggest_categorical("block_type", ["wadiro", "scnn"])

    if block_type == "wadiro":
        return {
            "block_type": "wadiro",
            "radius": trial.suggest_float("radius", 1e-5, 1e2, log=True),
            "max_neurons_wadiro": trial.suggest_categorical(
                "max_neurons_wadiro", [2, 4, 8, 16, 32, 64, 128, 256, 512]
            ),
            "bias_wadiro": True,
            "wasserstein": trial.suggest_categorical("wasserstein", ["l1", "l2"]),
        }

    return {
        "block_type": "scnn",
        "lamb_reg_scnn": trial.suggest_float("lamb_reg_scnn", 1e-6, 1e3, log=True),
        "max_neurons_scnn": trial.suggest_categorical(
            "max_neurons_scnn", [2, 4, 8, 16, 32, 64, 128, 256, 512]
        ),

        "bias_scnn": True,
        "loss_scnn": trial.suggest_categorical("loss_scnn", ["l1", "l2"]),
        "regularizer_scnn": trial.suggest_categorical(
            "regularizer_scnn", ["RIDGE", "LASSO"]
        ),
    }


def _objective_building_full(
    self,
    data: ResidualSearchData,
    *,
    use_aug: bool = True,
    verbose: bool = False,
):
    """Create the candidate evaluator used during residual-block hyperparameter search.

    Args:
        self (ConvexDeepStack): Model receiving the candidate block.
        data (ResidualSearchData): Training and validation data for the residual search.
        use_aug (bool): Whether to augment inputs with the current ensemble prediction.
        verbose (bool): Whether to enable candidate-level diagnostic output.

    Returns:
        tuple[Callable, dict[str, Any]]: Candidate-evaluation callable and mutable
        best-candidate record.
    """
    X_tr = data.x_train
    y_tr = data.y_train
    X_val = data.x_val
    y_val = data.y_val
    y_tr_prev = data.y_train_previous
    y_val_prev = data.y_val_previous

    best_holder = {
        "search_loss": np.inf,
        "params": None,
        "model": None,
    }

    FAIL_LOSS = 1e12

    def _failure(reason, exception=None):
        """Create a standardized failed-candidate result.

        Args:
            reason (str): Identifier describing the failure.
            exception (Exception | None): Optional exception associated with the failure.

        Returns:
            dict[str, Any]: Standardized failed-candidate result.
        """
        out = {
            "loss": FAIL_LOSS,
            "status": "fail",
            "reason": reason,
        }
        if exception is not None:
            out["exception"] = repr(exception)
        return out

    def _success(search_loss):
        """Create a standardized successful-candidate result.

        Args:
            search_loss (float): Residual validation loss of the candidate.

        Returns:
            dict[str, Any]: Standardized successful-candidate result.
        """
        return {
            "loss": float(search_loss),
            "status": "ok",
            "reason": None,
        }

    def _residual_loss(rhat_val):
        """Compute the mean squared error between validation residuals and residual predictions.

        Args:
            rhat_val (numpy.ndarray): Predicted validation residuals.

        Returns:
            float: Residual validation mean squared error.
        """
        r_val = self._ensure_2d(y_val - y_val_prev)
        rhat_val = self._ensure_2d(rhat_val)
        return float(np.mean((r_val - rhat_val) ** 2))

    def _update_best(search_loss, model, params):
        """Update the stored best candidate when a lower search loss is observed.

        Args:
            search_loss (float): Residual validation loss of the candidate.
            model (Any): Trained candidate model.
            params (dict[str, Any]): Hyperparameters of the candidate.

        Returns:
            None: The best-candidate record is updated in place.
        """
        if search_loss < best_holder["search_loss"]:
            best_holder.update(
                search_loss=float(search_loss),
                model=deepcopy(model),
                params=params,
            )

    print_trial_types = False

    def evaluate_candidate(params):
        """Train and evaluate one sampled residual-block candidate.

        Args:
            params (dict[str, Any]): Sampled block type and hyperparameters.

        Returns:
            dict[str, Any]: Standardized candidate-evaluation result.
        """
        block_type = params["block_type"]
        X_tr_aug, X_val_aug = self._augment_inputs(
            X_tr, X_val, y_tr_prev, y_val_prev, use_aug
        )
        r_tr = self._ensure_2d(y_tr - y_tr_prev)



        if block_type == "scnn":
            if verbose and print_trial_types:
                print("Block type: SCNN")
            max_neurons = int(params["max_neurons_scnn"])
            bias = bool(params["bias_scnn"])
            loss = params["loss_scnn"]
            lamb_reg = float(params["lamb_reg_scnn"])
            regularizer = params["regularizer_scnn"]

            try:
                mdl = scnn()
                with suppress_cvxpy_vec_futurewarning():
                    mdl.train(
                        X_train=X_tr_aug,
                        Y_train=r_tr,
                        bias=bias,
                        max_neurons=max_neurons,
                        loss=loss,
                        lamb_reg=lamb_reg,
                        regularizer=regularizer,
                    )
                torch_model = mdl.get_torch_model()
                torch_model.eval()
                dtype, device_t = self._get_torch_dtype_device(torch_model)
                rhat_val = self._ensure_2d(
                    self._predict_torch_on_numpy(torch_model, X_val_aug, dtype, device_t)
                )

                if not np.isfinite(rhat_val).all():
                    return _failure("nonfinite_rhat_val")

                search_loss = _residual_loss(rhat_val)
                if not np.isfinite(search_loss):
                    return _failure("nonfinite_search_loss")
            except Exception as e:
                return _failure("exception", e)

            _update_best(search_loss, mdl, {
                "block_type": block_type,
                "max_neurons": max_neurons,
                "bias": bias,
                "loss": loss,
                "lamb_reg": lamb_reg,
                "regularizer": regularizer,
            })
            return _success(search_loss)


        if block_type == "wadiro":
            if verbose and print_trial_types:
                print("Block type: Wadiro")
            radius = float(params["radius"])
            max_neurons = int(params["max_neurons_wadiro"])
            bias = bool(params["bias_wadiro"])
            wasserstein = params["wasserstein"]

            try:
                mdl = wadiro_scnn()
                with suppress_cvxpy_vec_futurewarning():
                    mdl.train(
                        X_train=X_tr_aug,
                        Y_train=r_tr,
                        radius=radius,
                        bias=bias,
                        max_neurons=max_neurons,
                        verbose=False,
                        wasserstein=wasserstein,
                        solver="CLARABEL",
                    )
                torch_model = mdl.get_torch_model()
                torch_model.eval()
                dtype, device_t = self._get_torch_dtype_device(torch_model)
                rhat_val = self._ensure_2d(
                    self._predict_torch_on_numpy(torch_model, X_val_aug, dtype, device_t)
                )

                if not np.isfinite(rhat_val).all():
                    return _failure("nonfinite_rhat_val")

                search_loss = _residual_loss(rhat_val)
                if not np.isfinite(search_loss):
                    return _failure("nonfinite_search_loss")
            except Exception as e:
                return _failure("exception", e)

            _update_best(search_loss, mdl, {
                "block_type": block_type,
                "radius": radius,
                "max_neurons": max_neurons,
                "bias": bias,
                "wasserstein": wasserstein,
            })
            return _success(search_loss)

        return _failure(f"unknown_block_type:{block_type}")

    return evaluate_candidate, best_holder


def _tpe_search_early_exit(
    self,
    data: ResidualSearchData,
    config: EarlyExitConfig,
):
    """Run Optuna TPE search with conformal adaptive early stopping for one residual block.

    Args:
        self (ConvexDeepStack): Model receiving the selected residual block.
        data (ResidualSearchData): Training and validation data for the residual search.
        config (EarlyExitConfig): Hyperparameter-search and early-exit settings.

    Returns:
        dict[str, Any]: Best candidate, search history, early-exit trace, and sampler settings.
    """
    max_evals = config.max_evals
    warmup = config.warmup
    alpha = config.alpha
    alpha_consistency = config.alpha_consistency
    alpha_rarity = config.alpha_rarity
    gamma = config.gamma
    eps_stab = config.eps_stab
    stability_window = config.stability_window
    recent_window = config.recent_window
    k_stop = config.k_stop
    seed = config.seed
    verbose = config.verbose
    optuna_multivariate = config.optuna_multivariate
    optuna_group = config.optuna_group
    optuna_n_startup_trials = config.optuna_n_startup_trials
    optuna_min_startup_trials = config.optuna_min_startup_trials
    optuna_warn_independent_sampling = config.optuna_warn_independent_sampling
    optuna_sampler_kwargs = config.optuna_sampler_kwargs

    evaluate_candidate, best_holder = self._objective_building_full(
        data,
        verbose=verbose,
    )

    max_evals = int(max_evals)
    if max_evals <= 0:
        return {
            "best_model": None,
            "best_search_loss": np.inf,
            "best_params": None,
            "study": None,
            "trials": None,
            "trial_records": [],
            "early_exit_trace": [],
            "sampler_settings": {},
        }

    requested_warmup = max(1, int(warmup))
    if optuna_n_startup_trials is None:

        n_startup_trials = max(requested_warmup, int(optuna_min_startup_trials))
    else:
        n_startup_trials = max(1, int(optuna_n_startup_trials))

    warmup = max(requested_warmup, n_startup_trials)
    warmup = min(warmup, max_evals)

    if optuna_group and not optuna_multivariate:
        raise ValueError("Optuna TPESampler requires multivariate=True when group=True.")

    sampler_kwargs = dict(optuna_sampler_kwargs or {})
    sampler_kwargs.update({
        "seed": seed,
        "n_startup_trials": n_startup_trials,
        "multivariate": bool(optuna_multivariate),
        "group": bool(optuna_group),
        "warn_independent_sampling": bool(optuna_warn_independent_sampling),
    })

    try:
        sampler = TPESampler(**sampler_kwargs)
    except TypeError as exc:
        raise TypeError(
            "Your installed Optuna version does not appear to support the requested "
            "TPESampler arguments. Upgrade with: pip install -U optuna"
        ) from exc

    study = optuna.create_study(direction="minimize", sampler=sampler)

    FAIL_THRESHOLD = 1e11
