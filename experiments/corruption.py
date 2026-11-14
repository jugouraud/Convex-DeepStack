import numpy as np

from .data_config import SignedShiftCorruptionConfig, WassersteinOutlierConfig
from .utils import as_2d_column


def _load_optimal_transport():
    try:
        import ot
    except ImportError as exc:
        raise ImportError(
            "The sliced-Wasserstein outlier mode requires POT. "
            "Install the project dependencies before using this corruption mode."
        ) from exc
    return ot


def _evaluate_one(benchmark, point) -> float:
    point = np.asarray(point, dtype=np.float64).reshape(1, -1)
    return float(np.asarray(benchmark(point), dtype=np.float64).reshape(-1)[0])


def sliced_wasserstein_outlier_introducer(
    signal,
    domain,
    in_sample_function,
    rng,
    config: WassersteinOutlierConfig,
):
    """Append outliers to a joint ``[X, y]`` training signal."""
    domain_dimensions = config.domain_dimensions
    n_points = config.n_points
    distance_min = config.distance_min
    n_projections = config.n_projections
    k_multiplier = config.k_multiplier
    max_output_scale = config.max_output_scale
    seed = config.seed
    if config.n_points < 0 or config.n_projections < 1:
        raise ValueError("n_points must be nonnegative and n_projections positive.")
    if (not np.isfinite(config.distance_min) or config.distance_min <= 0
            or not np.isfinite(config.k_multiplier) or config.k_multiplier <= 1
            or not np.isfinite(config.max_output_scale) or config.max_output_scale <= 0):
        raise ValueError("Outlier distance/scale must be positive and k_multiplier > 1.")
    verbose = config.verbose
    domain_min, domain_max = (np.asarray(v, dtype=np.float64) for v in domain)
    corrupted_signal = np.asarray(signal, dtype=np.float64).copy()
    if (corrupted_signal.ndim != 2
            or corrupted_signal.shape[1] != config.domain_dimensions + 1
            or domain_min.shape != (config.domain_dimensions,)
            or domain_max.shape != (config.domain_dimensions,)
            or not np.isfinite(corrupted_signal).all()
            or not np.isfinite(domain_min).all()
            or not np.isfinite(domain_max).all()
            or np.any(domain_min >= domain_max)):
        raise ValueError("Invalid joint signal or outlier domain.")
    if config.n_points == 0:
        return corrupted_signal
    optimal_transport = _load_optimal_transport()

    for _ in range(int(n_points)):
        original_x = rng.uniform(domain_min, domain_max, size=domain_dimensions)
        original_y = _evaluate_one(in_sample_function, original_x)
        reference_signal = np.vstack((corrupted_signal, np.hstack((original_x, original_y))))
        if verbose:
            print(reference_signal.shape)

        distance = 0.0
        multiplier = 1.0
        for _ in range(1_000):
            random_x = rng.uniform(domain_min, domain_max, size=(1, domain_dimensions))
            random_y = rng.uniform(
                -max_output_scale * multiplier,
                max_output_scale * multiplier,
                size=(1, 1),
            )
            candidate_signal = np.vstack(
                (corrupted_signal, np.hstack((random_x, random_y)))
            )
            n_samples = candidate_signal.shape[0]
            weights = np.ones(n_samples) / n_samples
            distance = float(
                np.mean(
                    optimal_transport.sliced_wasserstein_distance(
                        candidate_signal,
                        reference_signal,
                        weights,
                        weights,
                        n_projections=n_projections,
                        seed=seed,
                    )
                )
            )
            if not np.isfinite(distance):
                raise ValueError("Sliced-Wasserstein distance must be finite.")
            if distance >= distance_min:
                break
            multiplier *= k_multiplier
            if not np.isfinite(multiplier):
                raise RuntimeError("Outlier scale overflowed before meeting distance target.")
        else:
            raise RuntimeError("Could not generate a qualifying outlier in 1000 attempts.")

        corrupted_signal = candidate_signal.copy()

    return corrupted_signal


def corrupt_training_set(
    x_train,
    y_train,
    config: SignedShiftCorruptionConfig | None = None,
    *,
    x_reference_for_std=None,
    y_reference_for_std=None,
    **legacy_options,
):
    """Apply signed standard-deviation shifts to training samples."""
    if config is not None and legacy_options:
        raise TypeError("Pass either config or legacy keyword options, not both.")
    if config is None:
        config = SignedShiftCorruptionConfig(**legacy_options)

    corruption_mode = config.corruption_mode
    corruption_fraction = config.corruption_fraction
    target_noise_multiplier = config.target_noise_multiplier
    input_noise_multiplier = config.input_noise_multiplier
    random_state = config.random_state
    if not 0.0 <= float(corruption_fraction) <= 1.0:
        raise ValueError("corruption_fraction must be between 0 and 1.")
    if not np.isfinite(target_noise_multiplier) or not np.isfinite(input_noise_multiplier):
        raise ValueError("Noise multipliers must be finite.")

    aliases = {
        "signed_std_shift": "output_signed_std_shift",
        "input_and_label_signed_std_shift": "input_and_output_signed_std_shift",
    }
    corruption_mode = aliases.get(corruption_mode, corruption_mode)
    valid_modes = {
        "none", "input_signed_std_shift", "output_signed_std_shift",
        "input_and_output_signed_std_shift",
    }
    if corruption_mode not in valid_modes:
        raise ValueError(f"Unknown corruption_mode={corruption_mode!r}.")

    rng = np.random.default_rng(random_state)
    x_corrupted = np.asarray(x_train, dtype=np.float64).copy()
    y_corrupted = as_2d_column(y_train).copy()

    n_samples = x_corrupted.shape[0]
    row_mask = np.zeros(n_samples, dtype=bool)
    input_mask = np.zeros_like(x_corrupted, dtype=bool)
    output_mask = np.zeros_like(y_corrupted, dtype=bool)

    if corruption_mode == "none" or corruption_fraction <= 0:
        return x_corrupted, y_corrupted, row_mask, input_mask, output_mask

    x_reference = x_train if x_reference_for_std is None else x_reference_for_std
    y_reference = y_train if y_reference_for_std is None else y_reference_for_std
    x_std = np.std(np.asarray(x_reference, dtype=np.float64), axis=0)
    y_std = float(np.std(as_2d_column(y_reference)))

    input_modes = {
        "input_signed_std_shift",
        "input_and_output_signed_std_shift",
    }
    if corruption_mode in input_modes:
        for feature_index in range(x_corrupted.shape[1]):
            mask = rng.uniform(0, 1, size=x_corrupted[:, feature_index].shape) >= (
                1 - corruption_fraction
            )
            input_mask[:, feature_index] = mask
            signed_shift = input_noise_multiplier * rng.choice(
                [-x_std[feature_index], x_std[feature_index]],
                size=x_corrupted[:, feature_index][mask].shape,
            )
            x_corrupted[:, feature_index][mask] += signed_shift

    output_modes = {
        "output_signed_std_shift",
        "input_and_output_signed_std_shift",
    }
    if corruption_mode in output_modes:
        output_mask = rng.uniform(0, 1, size=y_corrupted.shape) >= (1 - corruption_fraction)
        signed_shift = target_noise_multiplier * rng.choice(
            [-y_std, y_std],
            size=y_corrupted[output_mask].shape,
        )
        y_corrupted[output_mask] += signed_shift

    row_mask = np.any(input_mask, axis=1) | output_mask.reshape(-1)
    return x_corrupted, y_corrupted, row_mask, input_mask, output_mask
