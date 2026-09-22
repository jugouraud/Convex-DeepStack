from dataclasses import dataclass


@dataclass(frozen=True)
class SyntheticSplitConfig:
    """Configuration for one deterministic synthetic benchmark split."""

    function_name: str
    n_dim: int
    samples_per_dim: int
    seed: int
    train_fraction: float = 0.60
    val_fraction: float = 0.20
    test_fraction: float = 0.20
    corruption_mode: str = "none"
    corruption_fraction: float = 0.0
    target_noise_multiplier: float = 4.0
    input_noise_multiplier: float = 4.0
    shared_noise_multiplier: float | None = None
    wasserstein_min_distance: float = 0.2
    wasserstein_n_projections: int = 100
    wasserstein_k_multiplier: float = 1.1
    wasserstein_max_output_scale: float = 2.0


@dataclass(frozen=True)
class SignedShiftCorruptionConfig:
    """Configuration for signed standard-deviation corruption."""

    corruption_mode: str = "output_signed_std_shift"
    corruption_fraction: float = 0.20
    target_noise_multiplier: float = 4.0
    input_noise_multiplier: float = 4.0
    random_state: int = 42


@dataclass(frozen=True)
class WassersteinOutlierConfig:
    """Configuration for sliced-Wasserstein outlier insertion."""

    domain_dimensions: int
    n_points: int
    distance_min: float
    n_projections: int
    k_multiplier: float
    max_output_scale: float
    seed: int
    verbose: bool = False
