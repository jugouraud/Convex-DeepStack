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
    max_blocks: int = 20
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

    def __post_init__(self) -> None:
        """Reject unsafe search budgets and inconsistent stopping parameters before training."""
        if not (0.0 < self.nu <= 1.0):
            raise ValueError("nu must be in (0, 1].")
        if not math.isfinite(self.improvement_tol) or self.improvement_tol < 0:
            raise ValueError("improvement_tol must be finite and nonnegative.")
        if self.min_blocks < 1 or self.block_patience < 1:
            raise ValueError("min_blocks and block_patience must be positive.")
        if self.max_blocks is None or self.max_blocks < self.min_blocks:
            raise ValueError("max_blocks must be finite and >= min_blocks.")
        if self.max_evals < 1 or self.warmup < 1:
            raise ValueError("max_evals and warmup must be positive.")
        if self.stability_window < 1 or self.recent_window < 1 or self.k_stop < 1:
            raise ValueError("early-exit window sizes and k_stop must be positive.")
        if self.optuna_min_startup_trials < 1 or (
            self.optuna_n_startup_trials is not None
            and self.optuna_n_startup_trials < 1
        ):
            raise ValueError("Optuna startup trial counts must be positive.")
        if self.optuna_group and not self.optuna_multivariate:
            raise ValueError("Optuna grouped TPE requires multivariate sampling.")
        if not math.isfinite(self.alpha) or not 0.0 < self.alpha < 1.0:
            raise ValueError("alpha must be in (0, 1).")
        for name in ("alpha_consistency", "alpha_rarity"):
            value = getattr(self, name)
            if not math.isfinite(value) or not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be in [0, 1].")
        if not math.isfinite(self.gamma) or self.gamma <= 0:
            raise ValueError("gamma must be positive and finite.")
        if not math.isfinite(self.eps_stab) or self.eps_stab < 0:
            raise ValueError("eps_stab must be finite and nonnegative.")

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

    X_tr_aug, X_val_aug = self._augment_inputs(
        X_tr, X_val, y_tr_prev, y_val_prev, use_aug
    )
    r_tr = self._ensure_2d(y_tr - y_tr_prev)
    r_val = self._ensure_2d(y_val - y_val_prev)

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

    def conformal_upper_quantile(values, alpha_level):
        """Compute the finite-sample conformal upper quantile of observed losses.

        Args:
            values (Iterable[float]): Observed loss values.
            alpha_level (float): Miscoverage level used to select the upper quantile.

        Returns:
            float: Selected conformal upper quantile.
        """
        vals = sorted(float(v) for v in values)
        n = len(vals)
        if n == 0:
            return np.inf
        idx = int(math.ceil((n + 1) * (1.0 - alpha_level))) - 1
        idx = max(0, min(idx, n - 1))
        return vals[idx]

    losses_valid = []
    new_best_flags = []
    incumbent_loss = None

    U_warm = None
    alpha_t = float(alpha)
    alpha_changes = []

    exploitation_mode = False
    stop_counter = 0
    early_exit_trace = []
    trial_records = []

    progress = (
        tqdm(total=max_evals, desc="Optuna TPE trials", unit="trial", leave=True)
        if (tqdm is not None and verbose)
        else None
    )


    for t in range(1, max_evals + 1):
        trial = study.ask()
        params = self._suggest_params_optuna(trial)
        result = evaluate_candidate(params)

        loss_t = float(result.get("loss", np.inf))
        if not np.isfinite(loss_t):
            loss_t = 1e12


        study.tell(trial, loss_t)

        trial_records.append({
            "trial": t,
            "number": trial.number,
            "params": params,
            "loss": loss_t,
            "status": result.get("status"),
            "reason": result.get("reason"),
            "exception": result.get("exception"),
        })

        if progress is not None:
            progress.update(1)
            if np.isfinite(best_holder["search_loss"]):
                progress.set_postfix(best=f"{best_holder['search_loss']:.6g}")

        is_valid = np.isfinite(loss_t) and loss_t < FAIL_THRESHOLD
        if not is_valid:
            continue


        if incumbent_loss is None:
            is_new_best = 1
            incumbent_loss = loss_t
        else:
            is_new_best = int(loss_t < incumbent_loss)
            incumbent_loss = min(incumbent_loss, loss_t)

        losses_valid.append(loss_t)
        new_best_flags.append(is_new_best)

        if len(losses_valid) < warmup:
            early_exit_trace.append({
                "trial": t,
                "loss": loss_t,
                "phase": "warmup",
                "U_warm": U_warm,
                "q_hat": None,
                "alpha_t": alpha_t,
                "e_t": None,
                "d_t": None,
                "p_good": None,
                "p_newbest": None,
                "exploitation_mode": False,
                "stop_counter": stop_counter,
            })
            continue

        if U_warm is None:
            U_warm = conformal_upper_quantile(losses_valid[:warmup], alpha)
            early_exit_trace.append({
                "trial": t,
                "loss": loss_t,
                "phase": "warmup_complete",
                "U_warm": U_warm,
                "q_hat": None,
                "alpha_t": alpha_t,
                "e_t": None,
                "d_t": None,
                "p_good": None,
                "p_newbest": None,
                "exploitation_mode": False,
                "stop_counter": stop_counter,
            })
            continue

        e_t = int(loss_t > U_warm)

        alpha_old = alpha_t
        alpha_t = alpha_t + gamma * (alpha - e_t)
        alpha_t = float(np.clip(alpha_t, 1e-6, 1.0 - 1e-6))


        d_t = abs(alpha_t - alpha_old)
        alpha_changes.append(d_t)


        if len(alpha_changes) >= stability_window:
            recent_deltas = alpha_changes[-stability_window:]
            exploitation_mode = all(d <= eps_stab for d in recent_deltas)
        else:
            exploitation_mode = False

        q_hat = None
        p_good = None
        p_newbest = None
        phase = "exploitation" if exploitation_mode else "exploration"

        if exploitation_mode:
            post_warmup_losses = losses_valid[warmup:]
            post_warmup_flags = new_best_flags[warmup:]

            if recent_window is not None:
                window_losses = post_warmup_losses[-recent_window:]
                window_flags = post_warmup_flags[-recent_window:]
            else:
                window_losses = post_warmup_losses
                window_flags = post_warmup_flags

            if len(window_losses) > 0:

                q_hat = conformal_upper_quantile(window_losses, alpha)

                p_good = float(np.mean([L <= U_warm for L in window_losses]))
                p_newbest = float(np.mean(window_flags))

                cond_good = p_good >= alpha_consistency
                cond_rare = p_newbest <= alpha_rarity

                if cond_good and cond_rare:
                    stop_counter += 1
                else:
                    stop_counter = 0

                if stop_counter >= k_stop:
                    early_exit_trace.append({
                        "trial": t,
                        "loss": loss_t,
                        "phase": phase,
                        "U_warm": U_warm,
                        "q_hat": q_hat,
                        "alpha_t": alpha_t,
                        "e_t": e_t,
                        "d_t": d_t,
                        "p_good": p_good,
                        "p_newbest": p_newbest,
                        "exploitation_mode": exploitation_mode,
                        "stop_counter": stop_counter,
                        "stopped": True,
                    })
                    break

        early_exit_trace.append({
            "trial": t,
            "loss": loss_t,
            "phase": phase,
            "U_warm": U_warm,
            "q_hat": q_hat,
            "alpha_t": alpha_t,
            "e_t": e_t,
            "d_t": d_t,
            "p_good": p_good,
            "p_newbest": p_newbest,
            "exploitation_mode": exploitation_mode,
            "stop_counter": stop_counter,
            "stopped": False,
        })

    if progress is not None:
        progress.close()

    sampler_settings = {
        "sampler": "Optuna TPESampler",
        "multivariate": bool(optuna_multivariate),
        "group": bool(optuna_group),
        "n_startup_trials": n_startup_trials,
        "conformal_warmup": warmup,
        "warn_independent_sampling": bool(optuna_warn_independent_sampling),
        "seed": seed,
    }

    return {
        "best_model": best_holder["model"],
        "best_search_loss": best_holder["search_loss"],
        "best_params": best_holder["params"],
        "study": study,
        "trials": study,
        "trial_records": trial_records,
        "early_exit_trace": early_exit_trace,
        "sampler_settings": sampler_settings,
    }


def build_optimal_model(
    self,
    X_tr,
    y_tr,
    X_val,
    y_val,
    config: DeepStackConfig | None = None,
):
    """Construct the residual stack by searching, weighting, and accepting candidate blocks.

    Args:
        self (ConvexDeepStack): Model whose residual stack is constructed.
        X_tr (numpy.ndarray): Training feature matrix.
        y_tr (numpy.ndarray): Training targets.
        X_val (numpy.ndarray): Validation feature matrix.
        y_val (numpy.ndarray): Validation targets.
        config (DeepStackConfig | None): Stack-construction configuration, or None for defaults.

    Returns:
        dict[str, Any]: Training history and stopping information for the constructed stack.
    """
    config = DeepStackConfig() if config is None else config
    if self.blocks:
        raise RuntimeError("build_optimal_model requires an empty stack; create a new model.")
    nu = config.nu
    improvement_tol = config.improvement_tol
    min_blocks = config.min_blocks
    block_patience = config.block_patience
    max_blocks = config.max_blocks
    verbose = config.verbose
    optuna_multivariate = config.optuna_multivariate
    optuna_group = config.optuna_group
    optuna_n_startup_trials = config.optuna_n_startup_trials
    optuna_min_startup_trials = config.optuna_min_startup_trials

    X_tr = np.asarray(X_tr, dtype=np.float64)
    X_val = np.asarray(X_val, dtype=np.float64)
    y_tr = self._ensure_2d(y_tr).astype(np.float64)
    y_val = self._ensure_2d(y_val).astype(np.float64)
    if (X_tr.ndim != 2 or X_val.ndim != 2
            or X_tr.shape[1] != self.in_dim_x or X_val.shape[1] != self.in_dim_x):
        raise ValueError("Training and validation features must be 2D with in_dim_x columns.")
    if (y_tr.ndim != 2 or y_val.ndim != 2
            or y_tr.shape[1] != self.out_dim or y_val.shape[1] != self.out_dim):
        raise ValueError("Targets must have out_dim columns.")
    if min(X_tr.shape[0], X_val.shape[0]) < 1 or (
        X_tr.shape[0] != y_tr.shape[0] or X_val.shape[0] != y_val.shape[0]
    ):
        raise ValueError("Train/validation samples must be nonempty and aligned with targets.")
    if not all(np.isfinite(array).all() for array in (X_tr, y_tr, X_val, y_val)):
        raise ValueError("Train/validation arrays must contain only finite values.")

    min_blocks = max(1, int(min_blocks))
    block_patience = max(1, int(block_patience))
    improvement_tol = max(0.0, float(improvement_tol))
    if max_blocks is not None:
        max_blocks = int(max_blocks)
        if max_blocks < min_blocks:
            raise ValueError(
                f"max_blocks={max_blocks} must be >= min_blocks={min_blocks}."
            )

    y_tr_prev = np.zeros((X_tr.shape[0], self.out_dim), dtype=np.float64)
    y_val_prev = np.zeros((X_val.shape[0], self.out_dim), dtype=np.float64)

    prediction_log = []
    block_idx = 0
    consecutive_low_improvement = 0

    baseline_val = float(np.mean((y_val - y_val_prev) ** 2))
    best_val_so_far = baseline_val

    if verbose:
        print(f"[Start] cumulative_loss={baseline_val:.6f}")

    history = {
        "baseline_val_mse": baseline_val,
        "blocks": [],
        "prediction_log": prediction_log,
        "block_patience": block_patience,
        "sampler": {
            "name": "Optuna TPESampler",
            "multivariate": bool(optuna_multivariate),
            "group": bool(optuna_group),
            "n_startup_trials": optuna_n_startup_trials,
            "min_startup_trials": optuna_min_startup_trials,
        },
    }

    while True:
        if max_blocks is not None and len(prediction_log) >= max_blocks:
            if verbose:
                print(f"[Stop] reached max_blocks={max_blocks} accepted blocks.")
            break

        block_idx += 1
        if verbose:
            print(f"\n\n======== Evaluating block {block_idx} ========\n")

        residual_data = ResidualSearchData(
            x_train=X_tr,
            y_train=y_tr,
            x_val=X_val,
            y_val=y_val,
            y_train_previous=y_tr_prev,
            y_val_previous=y_val_prev,
        )
        tpe_result = self._tpe_search_early_exit(
            residual_data,
            config.early_exit_for_block(block_idx),
        )

        best_params = tpe_result["best_params"]
        best_search_loss = float(tpe_result["best_search_loss"])
        best_model = tpe_result["best_model"]

        if best_model is None or best_params is None or not np.isfinite(best_search_loss):
            if verbose:
                print("[Stop] no finite residual-search result from TPE.")
            history["blocks"].append({
                **self._make_history_entry(
                    block_idx, best_params, best_search_loss, None, None,
                    val_mse_after=None, added=False,
                    stop_reason="non_finite_or_missing_search_result",
                ),
                "best_search_loss": best_search_loss,
                "weighted_val_mse": None,
                "early_exit_trace": tpe_result.get("early_exit_trace", []),
                "trial_records": tpe_result.get("trial_records", []),
                "sampler_settings": tpe_result.get("sampler_settings", {}),
            })
            break

        block_type = best_params.get("block_type", None)


        if block_type in ("wadiro", "scnn"):
            torch_block = best_model.get_torch_model()
            torch_block.eval()
            model_dtype, model_device = self._get_torch_dtype_device(torch_block)

            X_tr_aug, X_val_aug = self._augment_inputs(
                X_tr, X_val, y_tr_prev, y_val_prev, use_aug=True
            )
            rhat_tr = self._ensure_2d(
                self._predict_torch_on_numpy(torch_block, X_tr_aug, model_dtype, model_device)
            )
            rhat_val = self._ensure_2d(
                self._predict_torch_on_numpy(torch_block, X_val_aug, model_dtype, model_device)
            )

        else:
            if verbose:
                print(f"[Stop] unknown block_type={block_type}.")
            history["blocks"].append({
                **self._make_history_entry(
                    block_idx, best_params, best_search_loss, None, None,
                    val_mse_after=None, added=False,
                    stop_reason="unknown_block_type",
                ),
                "best_search_loss": best_search_loss,
                "weighted_val_mse": None,
                "early_exit_trace": tpe_result.get("early_exit_trace", []),
                "trial_records": tpe_result.get("trial_records", []),
                "sampler_settings": tpe_result.get("sampler_settings", {}),
            })
            break

        if not (np.isfinite(rhat_tr).all() and np.isfinite(rhat_val).all()):
            if verbose:
                print("[Stop] non-finite predictions from selected block.")
            history["blocks"].append({
                **self._make_history_entry(
                    block_idx, best_params, best_search_loss, None, None,
                    val_mse_after=None, added=False,
                    stop_reason="non_finite_predictions",
                ),
                "best_search_loss": best_search_loss,
                "weighted_val_mse": None,
                "early_exit_trace": tpe_result.get("early_exit_trace", []),
                "trial_records": tpe_result.get("trial_records", []),
                "sampler_settings": tpe_result.get("sampler_settings", {}),
            })
            break


        best_gamma, best_weight, y_val_new, weighted_val_mse = self._compute_boosting_weight(
            rhat_val=rhat_val,
            y_val=y_val,
            y_val_prev=y_val_prev,
            nu=nu,
        )
        weighted_val_mse = float(weighted_val_mse)

        if not np.isfinite(weighted_val_mse):
            if verbose:
                print("[Stop] non-finite cumulative validation MSE.")
            history["blocks"].append({
                **self._make_history_entry(
                    block_idx, best_params, best_search_loss, best_weight, best_gamma,
                    val_mse_after=None, added=False,
                    stop_reason="non_finite_weighted_val_mse",
                ),
                "best_search_loss": best_search_loss,
                "weighted_val_mse": weighted_val_mse,
                "early_exit_trace": tpe_result.get("early_exit_trace", []),
                "trial_records": tpe_result.get("trial_records", []),
                "sampler_settings": tpe_result.get("sampler_settings", {}),
            })
            break

        model_val_before = float(best_val_so_far)
        delta = model_val_before - weighted_val_mse
        relative_delta = delta / max(abs(model_val_before), 1e-12)
        accepted_before = len(prediction_log)
        if verbose:
            print(
                f"[Block {block_idx}] finished | "
                f"residual_loss={best_search_loss:.6f} | "
                f"weight={best_weight:.6g} | "
                f"new_ensemble_loss={weighted_val_mse:.6f} | "
                f"relative_improvement={relative_delta:.6g}"
            )

        if weighted_val_mse > model_val_before + 1e-10:
            if verbose:
                print("[Stop] candidate would increase cumulative loss.")
            history["blocks"].append({
                "block_idx": block_idx,
                "best_params": best_params,
                "best_val": model_val_before,
                "residual_search_loss": best_search_loss,
                "best_search_loss": best_search_loss,
                "model_val_mse_before": model_val_before,
                "model_val_mse_after_candidate": weighted_val_mse,
                "model_val_mse_after": model_val_before,
                "weighted_val_mse": weighted_val_mse,
                "absolute_improvement": delta,
                "relative_improvement": relative_delta,
                "improvement_tol": improvement_tol,
                "accepted_blocks_before_candidate": accepted_before,
                "best_weight": best_weight,
                "best_gamma": best_gamma,
                "added": False,
                "stop_reason": "would_increase_model_val_mse",
                "early_exit_trace": tpe_result.get("early_exit_trace", []),
                "trial_records": tpe_result.get("trial_records", []),
                "sampler_settings": tpe_result.get("sampler_settings", {}),
            })
            break




        meets_improvement_tol = bool(relative_delta > improvement_tol)


        self.add_block(torch_block, weight=best_weight)

        y_tr_prev = y_tr_prev + best_weight * rhat_tr
        y_val_prev = y_val_new
        cur_val_mse = float(np.mean((y_val - y_val_prev) ** 2))
        best_val_so_far = cur_val_mse
        prediction_log.append(y_val_prev.copy())

        accepted_after = len(prediction_log)
        if accepted_after >= min_blocks:
            if meets_improvement_tol:
                consecutive_low_improvement = 0
            else:
                consecutive_low_improvement += 1
        else:
            consecutive_low_improvement = 0

        patience_exhausted = (
            accepted_after >= min_blocks
            and consecutive_low_improvement >= block_patience
        )
        block_stop_reason = (
            "block_patience_exhausted" if patience_exhausted else None
        )

        history["blocks"].append({
            "block_idx": block_idx,
            "best_params": best_params,
            "best_val": cur_val_mse,
            "residual_search_loss": best_search_loss,
            "best_search_loss": best_search_loss,
            "model_val_mse_before": model_val_before,
            "model_val_mse_after": cur_val_mse,
            "weighted_val_mse": weighted_val_mse,
            "absolute_improvement": delta,
            "relative_improvement": relative_delta,
            "improvement_tol": improvement_tol,
            "meets_improvement_tol": meets_improvement_tol,
            "accepted_blocks_before_candidate": accepted_before,
            "accepted_blocks_after_candidate": accepted_after,
            "consecutive_low_improvement": consecutive_low_improvement,
            "block_patience": block_patience,
            "best_weight": best_weight,
            "best_gamma": best_gamma,
            "added": True,
            "stop_reason": block_stop_reason,
            "early_exit_trace": tpe_result.get("early_exit_trace", []),
            "trial_records": tpe_result.get("trial_records", []),
            "sampler_settings": tpe_result.get("sampler_settings", {}),
        })

        if verbose:
            quality = "meaningful" if meets_improvement_tol else "below tolerance"
            print(
                f"[Block {block_idx}] accepted ({quality}) | "
                f"low_improvement_streak={consecutive_low_improvement}/"
                f"{block_patience}"
            )

        if patience_exhausted:
            if verbose:
                print(
                    "[Stop] block patience exhausted after "
                    f"{consecutive_low_improvement} consecutive accepted blocks "
                    "below the relative-improvement threshold."
                )
            break

    history["n_blocks_accepted"] = len(prediction_log)
    history["n_block_attempts"] = len(history["blocks"])
    history["min_blocks"] = min_blocks
    history["block_patience"] = block_patience
    history["consecutive_low_improvement_at_stop"] = consecutive_low_improvement
    history["improvement_tol"] = improvement_tol
    history["stop_reason"] = next(
        (
            block.get("stop_reason")
            for block in reversed(history["blocks"])
            if block.get("stop_reason")
        ),
        "max_blocks"
        if max_blocks is not None and len(prediction_log) >= max_blocks
        else None,
    )

    if verbose:
        print(
            f"[Done] accepted_blocks={history['n_blocks_accepted']} | "
            f"attempts={history['n_block_attempts']} | "
            f"stop_reason={history['stop_reason']}"
        )

    self.train_history = history
    return history


class ConvexDeepStack(nn.Module):

    def __init__(self, in_dim_x: int, out_dim: int):
        """Initialize an empty ConvexDeepStack model.

        Args:
            in_dim_x (int): Number of input features.
            out_dim (int): Number of output dimensions.

        Returns:
            None: Initializes the model in place.
        """
        if in_dim_x < 1 or out_dim < 1:
            raise ValueError("in_dim_x and out_dim must be positive.")
        super().__init__()
        self.in_dim_x = in_dim_x
        self.out_dim = out_dim
        self.blocks = nn.ModuleList()
        self.weights = nn.ParameterList()

    @staticmethod
    def _ensure_2d(array) -> np.ndarray:
        """Convert an array-like object to an array with an explicit output dimension.

        Args:
            array (ArrayLike): Input values to reshape when one-dimensional.

        Returns:
            numpy.ndarray: Array with at least two dimensions.
        """
        array = np.asarray(array)
        if array.ndim == 1:
            return array.reshape(-1, 1)
        if array.ndim != 2:
            raise ValueError("Expected a one- or two-dimensional target/prediction array.")
        return array

    @staticmethod
    def _get_torch_dtype_device(torch_model: nn.Module):
        """Determine the dtype and device used by a PyTorch module.

        Args:
            torch_model (torch.nn.Module): PyTorch module to inspect.

        Returns:
            tuple[torch.dtype, torch.device]: Module dtype and device, with CPU defaults
            when parameterless.
        """
        try:
            parameter = next(torch_model.parameters())
        except StopIteration:
            return torch.get_default_dtype(), torch.device("cpu")
        return parameter.dtype, parameter.device

    @staticmethod
    def _predict_torch_on_numpy(torch_model, x_numpy, dtype, device) -> np.ndarray:
        """Evaluate a PyTorch model on NumPy inputs and return NumPy predictions.

        Args:
            torch_model (torch.nn.Module): PyTorch model to evaluate.
            x_numpy (numpy.ndarray): Input feature matrix.
            dtype (torch.dtype): Tensor dtype used for evaluation.
            device (torch.device): Device used for evaluation.

        Returns:
            numpy.ndarray: Model predictions converted to NumPy.
        """
        with torch.no_grad():
            x_tensor = torch.from_numpy(x_numpy).to(dtype=dtype, device=device)
            return torch_model(x_tensor).cpu().numpy()

    @staticmethod
    def _compute_boosting_weight(rhat_val, y_val, y_val_prev, nu):
        """Compute the residual line-search coefficient and updated validation prediction.

        Args:
            rhat_val (numpy.ndarray): Candidate residual predictions on validation data.
            y_val (numpy.ndarray): Validation targets.
            y_val_prev (numpy.ndarray): Current ensemble predictions on validation data.
            nu (float): Shrinkage factor applied to the line-search coefficient.

        Returns:
            tuple[float, float, numpy.ndarray, float]: Line-search coefficient, block weight,
            updated predictions, and validation MSE.
        """
        validation_residual = ConvexDeepStack._ensure_2d(y_val - y_val_prev)
        residual_prediction = ConvexDeepStack._ensure_2d(rhat_val)
        if validation_residual.shape != residual_prediction.shape:
            raise ValueError("Residual predictions must match validation target shape.")
        numerator = float(np.sum(validation_residual * residual_prediction))
        denominator = float(np.sum(residual_prediction * residual_prediction) + 1e-12)
        gamma = numerator / denominator
        weight = nu * gamma
        y_val_new = ConvexDeepStack._ensure_2d(y_val_prev) + weight * residual_prediction
        validation_loss = float(np.mean((y_val - y_val_new) ** 2))
        return gamma, weight, y_val_new, validation_loss

    @staticmethod
    def _make_history_entry(
        block_idx,
        best_params,
        best_val,
        best_weight,
        best_gamma,
        val_mse_after,
        added,
        stop_reason,
    ) -> dict:
        """Create a normalized history record for one candidate block.

        Args:
            block_idx (int): One-based candidate block index.
            best_params (dict[str, Any] | None): Selected hyperparameters.
            best_val (float | None): Recorded validation value.
            best_weight (float | None): Selected block weight.
            best_gamma (float | None): Unshrunk line-search coefficient.
            val_mse_after (float | None): Validation MSE after the candidate.
            added (bool): Whether the candidate was added to the stack.
            stop_reason (str | None): Reason for stopping, when applicable.

        Returns:
            dict[str, Any]: Normalized block-history record.
        """
        return {
            "block_idx": block_idx,
            "best_params": best_params,
            "best_val": best_val,
            "best_weight": best_weight,
            "best_gamma": best_gamma,
            "val_mse_after": val_mse_after,
            "added": added,
            "stop_reason": stop_reason,
        }

    def _augment_inputs(self, x_train, x_val, y_train_prev, y_val_prev, use_aug):
        """Optionally append current ensemble predictions to training and validation features.

        Args:
            x_train (numpy.ndarray): Training feature matrix.
            x_val (numpy.ndarray): Validation feature matrix.
            y_train_prev (numpy.ndarray): Current ensemble predictions on training data.
            y_val_prev (numpy.ndarray): Current ensemble predictions on validation data.
            use_aug (bool): Whether to append current predictions to the features.

        Returns:
            tuple[numpy.ndarray, numpy.ndarray]: Training and validation feature matrices
            after optional augmentation.
        """
        if not use_aug:
            return x_train, x_val
        return (
            self._data_augmenter(x_train, y_train_prev),
            self._data_augmenter(x_val, y_val_prev),
        )

    @staticmethod
    def _data_augmenter(x, y):
        """Append prediction values while preserving the feature array representation.

        Args:
            x (numpy.ndarray | torch.Tensor): Feature matrix.
            y (numpy.ndarray | torch.Tensor): Prediction values to append.

        Returns:
            numpy.ndarray | torch.Tensor: Feature matrix with appended prediction values.
        """
        if isinstance(x, np.ndarray):
            if isinstance(y, torch.Tensor):
                y = y.detach().cpu().numpy()
            return np.concatenate([x, y], axis=1)
        if isinstance(x, torch.Tensor):
            if isinstance(y, np.ndarray):
                y = torch.from_numpy(y).to(device=x.device, dtype=x.dtype)
            return torch.cat([x, y], dim=1)
        raise TypeError("x must be a torch.Tensor or numpy.ndarray")

    def add_block(
        self,
        pretrained_block: nn.Module,
        weight: float | torch.Tensor = 1.0,
    ) -> None:
        """Append a pretrained residual block with a fixed ensemble weight.

        Args:
            pretrained_block (torch.nn.Module): Residual-prediction block to append.
            weight (float | torch.Tensor): Fixed additive weight assigned to the block.

        Returns:
            None: Updates the model in place.
        """
        if not isinstance(pretrained_block, nn.Module):
            raise TypeError("pretrained_block must be a torch.nn.Module.")
        weight = torch.as_tensor(weight, dtype=torch.float64)
        if weight.numel() != 1 or not torch.isfinite(weight).all():
            raise ValueError("Block weight must be a finite scalar.")
        self.blocks.append(pretrained_block)
        self.weights.append(nn.Parameter(weight.reshape(()), requires_grad=False))

    def set_block_weight(self, idx: int, new_weight: float | torch.Tensor) -> None:
        """Replace the fixed additive weight of one residual block.

        Args:
            idx (int): Index of the block weight to replace.
            new_weight (float | torch.Tensor): New fixed additive weight.

        Returns:
            None: Updates the selected weight in place.
        """
        weight = self.weights[idx]
        new_weight = torch.as_tensor(new_weight, device=weight.device, dtype=weight.dtype)
        if new_weight.numel() != 1 or not torch.isfinite(new_weight).all():
            raise ValueError("Block weight must be a finite scalar.")
        with torch.no_grad():
            weight.copy_(new_weight.reshape(()))

    def get_block_weight(self, idx: int) -> torch.Tensor:
        """Return a detached copy of one residual-block weight.

        Args:
            idx (int): Index of the block weight to retrieve.

        Returns:
            torch.Tensor: Detached scalar block weight.
        """
        return self.weights[idx].detach()

    def forward(self, x: torch.Tensor, return_all: bool = False):
        """Evaluate the additive residual stack on an input batch.

        Args:
            x (torch.Tensor): Input feature batch.
            return_all (bool): Whether to return predictions after every accepted block.

        Returns:
            torch.Tensor | list[torch.Tensor]: Final prediction or intermediate predictions
            for all blocks.
        """
        if x.ndim != 2 or x.shape[1] != self.in_dim_x:
            raise ValueError("Input must have shape (batch, in_dim_x).")
        batch_size = x.size(0)
        device, dtype = x.device, x.dtype
        ensemble_prediction = torch.zeros(
            batch_size,
            self.out_dim,
            dtype=dtype,
            device=device,
        )
        intermediate_predictions = []

        for block_index, block in enumerate(self.blocks):
            augmented_input = torch.cat([x, ensemble_prediction], dim=1)
            residual_prediction = block(augmented_input)

            if residual_prediction.dim() == 1 and self.out_dim == 1:
                residual_prediction = residual_prediction.reshape(batch_size, 1)
            if residual_prediction.shape != (batch_size, self.out_dim):
                raise RuntimeError(
                    f"Block {block_index} returned {tuple(residual_prediction.shape)}; "
                    f"expected {(batch_size, self.out_dim)}"
                )

            weight = self.weights[block_index].to(device=device, dtype=dtype)
            ensemble_prediction = ensemble_prediction + weight * residual_prediction
            if return_all:
                intermediate_predictions.append(ensemble_prediction.clone())

        return intermediate_predictions if return_all else ensemble_prediction


ConvexDeepStack._suggest_params_optuna = staticmethod(_suggest_params_optuna)
ConvexDeepStack._objective_building_full = _objective_building_full
ConvexDeepStack._tpe_search_early_exit = _tpe_search_early_exit
ConvexDeepStack.build_optimal_model = build_optimal_model
