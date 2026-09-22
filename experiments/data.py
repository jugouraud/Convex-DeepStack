import math

import numpy as np
from sklearn.preprocessing import StandardScaler

from .utils import as_2d_column

# Synthetic benchmark functions used by the controlled experiments.
def ackley(X, a=20.0, b=0.2, c=2.0 * np.pi):
    """Vectorised d-dimensional Ackley function."""
    X = np.asarray(X, dtype=np.float64)
    d = X.shape[1]
    sum_sq = np.sum(X ** 2, axis=1)
    cos_sum = np.sum(np.cos(c * X), axis=1)
    return (-a * np.exp(-b * np.sqrt(sum_sq / d))
            - np.exp(cos_sum / d)
            + a + np.e).reshape(-1, 1)

def rastrigin(X):
    """Vectorised d-dimensional Rastrigin function."""
    X = np.asarray(X, dtype=np.float64)
    d = X.shape[1]
    return (10.0 * d + np.sum(X ** 2 - 10.0 * np.cos(2.0 * np.pi * X), axis=1)).reshape(-1, 1)

def rosenbrock(X):
    """Vectorised d-dimensional Rosenbrock function."""
    X = np.asarray(X, dtype=np.float64)
    if X.shape[1] < 2:
        return ((1.0 - X[:, 0]) ** 2).reshape(-1, 1)
    return np.sum(
        100.0 * (X[:, 1:] - X[:, :-1] ** 2) ** 2 + (1.0 - X[:, :-1]) ** 2,
        axis=1,
    ).reshape(-1, 1)

BENCHMARKS = {
    "ackley": {
        "fn": ackley,
        "low": -5.0,
        "high": 5.0,
        "why": "smooth but nonconvex; default benchmark used in this notebook",
    },
    "rastrigin": {
        "fn": rastrigin,
        "low": -5.12,
        "high": 5.12,
        "why": "highly multimodal; stress-tests oscillatory robustness",
    },
    "rosenbrock": {
        "fn": rosenbrock,
        "low": -2.0,
        "high": 2.0,
        "why": "curved valley; stress-tests sparse interpolation and conditioning",
    },
}

from .corruption import (
    corrupt_training_set,
    sliced_wasserstein_outlier_introducer,
)
from .data_config import (
    SignedShiftCorruptionConfig,
    SyntheticSplitConfig,
    WassersteinOutlierConfig,
)


def exact_split_counts(
    n_dim,
    samples_per_dim,
    train_fraction=0.60,
    val_fraction=0.20,
    test_fraction=0.20,
):
    """Return train/validation/test counts with ``n_train = n_dim * samples_per_dim``."""
    if n_dim <= 0 or samples_per_dim <= 0:
        raise ValueError("n_dim and samples_per_dim must both be positive.")
    fractions = (train_fraction, val_fraction, test_fraction)
    if any(fraction <= 0 for fraction in fractions):
        raise ValueError("train_fraction, val_fraction, and test_fraction must be positive.")
    if not math.isclose(sum(fractions), 1.0, rel_tol=1e-8, abs_tol=1e-8):
        raise ValueError("train_fraction + val_fraction + test_fraction must sum to 1.")

    n_train = int(n_dim * samples_per_dim)
    n_val = max(1, int(round(n_train * val_fraction / train_fraction)))
    n_test = max(1, int(round(n_train * test_fraction / train_fraction)))
    return n_train, n_val, n_test


def _resolve_config(
    config: SyntheticSplitConfig | None,
    legacy_options: dict,
) -> SyntheticSplitConfig:
    if config is not None and legacy_options:
        raise TypeError("Pass either config or legacy keyword options, not both.")
    return SyntheticSplitConfig(**legacy_options) if config is None else config


def _validate_config(config: SyntheticSplitConfig) -> tuple[str, dict]:
    if not 0.0 <= float(config.corruption_fraction) <= 1.0:
        raise ValueError("corruption_fraction must be between 0 and 1.")

    function_name = config.function_name.lower()
    if function_name not in BENCHMARKS:
        choices = sorted(BENCHMARKS)
        raise ValueError(f"Unknown function_name={function_name!r}; choose from {choices}")
    return function_name, BENCHMARKS[function_name]


def _sample_ordered_split(config: SyntheticSplitConfig, spec: dict, rng) -> dict:
    n_train, n_val, n_test = exact_split_counts(
        config.n_dim,
        config.samples_per_dim,
        train_fraction=config.train_fraction,
        val_fraction=config.val_fraction,
        test_fraction=config.test_fraction,
    )
    n_total = n_train + n_val + n_test
    x_all = rng.uniform(
        spec["low"],
        spec["high"],
        size=(n_total, config.n_dim),
    ).astype(np.float64)
    y_all = spec["fn"](x_all).astype(np.float64)

    return {
        "n_train_base": n_train,
        "n_val": n_val,
        "n_test": n_test,
        "n_total": n_total,
        "X_train": x_all[:n_train],
        "y_train_clean": y_all[:n_train],
        "X_val": x_all[n_train : n_train + n_val],
        "y_val": y_all[n_train : n_train + n_val],
        "X_test": x_all[n_train + n_val :],
        "y_test": y_all[n_train + n_val :],
    }


def _scale_split(raw: dict) -> dict:
    x_scaler = StandardScaler(with_mean=False, with_std=False)
    y_scaler = StandardScaler(with_mean=False, with_std=False)

    x_train_scaled = x_scaler.fit_transform(raw["X_train"]).astype(np.float64)
    y_train_clean = as_2d_column(raw["y_train_clean"])
    y_scaler.fit(y_train_clean)

    return {
        "X_train_s": x_train_scaled,
        "X_val_s": x_scaler.transform(raw["X_val"]).astype(np.float64),
        "X_test_s": x_scaler.transform(raw["X_test"]).astype(np.float64),
        "y_train_s_clean": y_scaler.transform(y_train_clean).astype(np.float64),
        "y_val_s": y_scaler.transform(as_2d_column(raw["y_val"])).astype(np.float64),
        "y_test_s": y_scaler.transform(as_2d_column(raw["y_test"])).astype(np.float64),
        "x_scaler": x_scaler,
        "y_scaler": y_scaler,
    }


def _normalise_corruption_mode(mode: str) -> str:
    aliases = {
        "wasserstein_outliers": "sliced_wasserstein_outliers",
    }
    return aliases.get(mode, mode)


def _effective_noise_multipliers(config: SyntheticSplitConfig) -> tuple[float, float]:
    if config.shared_noise_multiplier is None:
        return config.target_noise_multiplier, config.input_noise_multiplier
    multiplier = float(config.shared_noise_multiplier)
    return multiplier, multiplier


def _apply_wasserstein_corruption(
    config: SyntheticSplitConfig,
    spec: dict,
    rng,
    raw: dict,
    scaled: dict,
) -> dict:
    x_train = scaled["X_train_s"] + rng.normal(0, 0.05, raw["X_train"].shape)
    x_val = scaled["X_val_s"] + rng.normal(0, 0.05, raw["X_val"].shape)
    y_train = scaled["y_train_s_clean"] + rng.normal(
        0,
        0.05,
        scaled["y_train_s_clean"].shape,
    )
    y_val = scaled["y_val_s"] + rng.normal(0, 0.05, raw["y_val"].shape)

    n_inserted = max(
        0,
        int(round(config.corruption_fraction * raw["n_train_base"])),
    )
    corruption_mask = np.zeros(x_train.shape[0], dtype=bool)
    input_mask = np.zeros_like(x_train, dtype=bool)
    output_mask = np.zeros_like(y_train, dtype=bool)

    if n_inserted > 0:
        domain = [
            np.full(config.n_dim, spec["low"], dtype=np.float64),
            np.full(config.n_dim, spec["high"], dtype=np.float64),
        ]
        outlier_config = WassersteinOutlierConfig(
            domain_dimensions=config.n_dim,
            n_points=n_inserted,
            distance_min=config.wasserstein_min_distance,
            n_projections=config.wasserstein_n_projections,
            k_multiplier=config.wasserstein_k_multiplier,
            max_output_scale=config.wasserstein_max_output_scale,
            seed=config.seed,
        )
        train_signal = np.hstack((x_train, y_train))
        train_signal = sliced_wasserstein_outlier_introducer(
            train_signal,
            domain,
            spec["fn"],
            rng,
            outlier_config,
        )
        x_train = train_signal[:, :-1].astype(np.float64)
        y_train = train_signal[:, -1].reshape(-1, 1).astype(np.float64)
        corruption_mask = np.zeros(x_train.shape[0], dtype=bool)
        corruption_mask[raw["n_train_base"] :] = True
        input_mask = np.zeros_like(x_train, dtype=bool)
        output_mask = corruption_mask.reshape(-1, 1)

    return {
        "X_train_s": x_train,
        "X_val_s": x_val,
        "y_train_s": y_train,
        "y_val_s": y_val,
        "X_train_corr": x_train.copy(),
        "y_train_corr": y_train.copy(),
        "corruption_mask": corruption_mask,
        "input_mask": input_mask,
        "output_mask": output_mask,
        "n_inserted_outliers": n_inserted,
    }


def _apply_signed_shift_corruption(
    config: SyntheticSplitConfig,
    raw: dict,
    scaled: dict,
    corruption_mode: str,
) -> dict:
    target_multiplier, input_multiplier = _effective_noise_multipliers(config)
    corruption_config = SignedShiftCorruptionConfig(
        corruption_mode=corruption_mode,
        corruption_fraction=config.corruption_fraction,
        target_noise_multiplier=target_multiplier,
        input_noise_multiplier=input_multiplier,
        random_state=config.seed + 10_000,
    )
    x_train, y_train, row_mask, input_mask, output_mask = corrupt_training_set(
        scaled["X_train_s"],
        scaled["y_train_s_clean"],
        corruption_config,
        x_reference_for_std=raw["X_train"],
        y_reference_for_std=raw["y_train_clean"],
    )
    return {
        "X_train_s": x_train,
        "X_val_s": scaled["X_val_s"],
        "y_train_s": y_train,
        "y_val_s": scaled["y_val_s"],
        "X_train_corr": x_train,
        "y_train_corr": y_train,
        "corruption_mask": row_mask,
        "input_mask": input_mask,
        "output_mask": output_mask,
        "n_inserted_outliers": 0,
    }


def _apply_corruption(
    config: SyntheticSplitConfig,
    spec: dict,
    rng,
    raw: dict,
    scaled: dict,
) -> dict:
    mode = _normalise_corruption_mode(config.corruption_mode)
    if mode == "sliced_wasserstein_outliers":
        return _apply_wasserstein_corruption(config, spec, rng, raw, scaled)
    return _apply_signed_shift_corruption(config, raw, scaled, mode)


def _build_payload(
    config: SyntheticSplitConfig,
    function_name: str,
    raw: dict,
    scaled: dict,
    corruption: dict,
) -> dict:
    y_scaler = scaled["y_scaler"]

    def inverse_y(y_scaled):
        values = np.asarray(y_scaled).reshape(-1, 1)
        return y_scaler.inverse_transform(values).reshape(-1)

    return {
        "function_name": function_name,
        "n_dim": config.n_dim,
        "samples_per_dim": config.samples_per_dim,
        "seed": config.seed,
        "n_train": int(corruption["X_train_s"].shape[0]),
        "n_train_base": raw["n_train_base"],
        "n_val": raw["n_val"],
        "n_test": raw["n_test"],
        "n_total": raw["n_total"],
        "n_inserted_outliers": corruption["n_inserted_outliers"],
        "X_train": raw["X_train"],
        "y_train_clean": raw["y_train_clean"],
        "X_train_corr": corruption["X_train_corr"],
        "y_train_corr": corruption["y_train_corr"],
        "corruption_mask": corruption["corruption_mask"],
        "input_corruption_mask": corruption["input_mask"],
        "output_corruption_mask": corruption["output_mask"],
        "X_val": raw["X_val"],
        "y_val": raw["y_val"],
        "X_test": raw["X_test"],
        "y_test": raw["y_test"],
        "X_train_s": corruption["X_train_s"],
        "y_train_s": corruption["y_train_s"],
        "X_val_s": corruption["X_val_s"],
        "y_val_s": corruption["y_val_s"],
        "X_test_s": scaled["X_test_s"],
        "y_test_s": scaled["y_test_s"],
        "x_scaler": scaled["x_scaler"],
        "y_scaler": y_scaler,
        "inverse_y": inverse_y,
        "data_generation_metadata": {
            "split": "shuffle_false_ordered",
            "scaler": "StandardScaler(with_mean=False, with_std=False)",
            "corruption": "Bernoulli masks with signed +/- std shifts",
            "mean_x": np.mean(raw["X_train"], axis=0),
            "std_x": np.std(raw["X_train"], axis=0),
            "mean_y": np.mean(raw["y_train_clean"]),
            "std_y": np.std(raw["y_train_clean"]),
        },
    }


def make_synthetic_split(
    config: SyntheticSplitConfig | None = None,
    **legacy_options,
):
    """Create one reproducible synthetic split with clean validation/test data."""
    resolved_config = _resolve_config(config, legacy_options)
    function_name, spec = _validate_config(resolved_config)
    rng = np.random.default_rng(resolved_config.seed)
    raw = _sample_ordered_split(resolved_config, spec, rng)
    scaled = _scale_split(raw)
    corruption = _apply_corruption(resolved_config, spec, rng, raw, scaled)
    return _build_payload(resolved_config, function_name, raw, scaled, corruption)
