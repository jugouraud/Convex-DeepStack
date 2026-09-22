import itertools
from dataclasses import dataclass

import pandas as pd

try:
    from tqdm.auto import tqdm
except ImportError:  # pragma: no cover - progress bars are optional
    tqdm = None

from .data import make_synthetic_split
from .data_config import SyntheticSplitConfig
from .tuning import ModelStudyContext, run_model_study


@dataclass(frozen=True)
class DatasetGridPoint:
    """One synthetic-dataset configuration in the outer control sweep."""

    function_name: str
    dimension: int
    samples_per_dim: int
    seed: int
    corruption_fraction: float

    @property
    def study_key_prefix(self) -> tuple[str, int, int, int, float]:
        """Return the immutable dataset portion of a study lookup key."""
        return (
            self.function_name,
            self.dimension,
            self.samples_per_dim,
            self.seed,
            float(self.corruption_fraction),
        )


def save_results(all_rows, config):
    """Persist all trial rows and the best successful trial per model/dataset."""
    results_df = pd.DataFrame(all_rows)
    results_df.to_csv(config["results_csv"], index=False)

    if results_df.empty or "status" not in results_df:
        best_df = pd.DataFrame()
    else:
        successful = results_df[results_df["status"].eq("ok")].copy()
        if successful.empty:
            best_df = pd.DataFrame()
        else:
            group_columns = [
                "function",
                "dimension",
                "samples_per_dim",
                "seed",
                "corruption_fraction",
                "corruption_mode",
                "Model",
            ]
            best_df = (
                successful.sort_values(group_columns + ["objective_value"])
                .groupby(group_columns, as_index=False)
                .first()
            )

    best_df.to_csv(config["best_csv"], index=False)
    return results_df, best_df


def make_dataset_for_grid_point(point: DatasetGridPoint, config):
    """Build one dataset and return its effective corruption mode."""
    corruption_mode = (
        "none" if point.corruption_fraction <= 0 else config["corruption_mode"]
    )
    split_config = SyntheticSplitConfig(
        function_name=point.function_name,
        n_dim=point.dimension,
        samples_per_dim=point.samples_per_dim,
        seed=point.seed,
        train_fraction=config["train_fraction"],
        val_fraction=config["val_fraction"],
        test_fraction=config["test_fraction"],
        corruption_mode=corruption_mode,
        corruption_fraction=float(point.corruption_fraction),
        target_noise_multiplier=config["target_noise_multiplier"],
        input_noise_multiplier=config["input_noise_multiplier"],
        shared_noise_multiplier=config.get("shared_noise_multiplier"),
        wasserstein_min_distance=config.get("wasserstein_min_distance", 0.2),
        wasserstein_n_projections=config.get("wasserstein_n_projections", 100),
        wasserstein_k_multiplier=config.get("wasserstein_k_multiplier", 1.1),
        wasserstein_max_output_scale=config.get("wasserstein_max_output_scale", 2),
    )
    return make_synthetic_split(split_config), corruption_mode


def _grid_points(config) -> list[DatasetGridPoint]:
    selected_setups = config.get("sweep_setups")
    if selected_setups is None:
        selected_setups = itertools.product(
            config["function_names"],
            config["sweep_dimensions"],
            config["sweep_samples_per_dim"],
        )

    points = [
        DatasetGridPoint(
            function_name=function_name,
            dimension=int(dimension),
            samples_per_dim=int(samples_per_dim),
            seed=int(seed),
            corruption_fraction=float(corruption_fraction),
        )
        for (function_name, dimension, samples_per_dim), seed, corruption_fraction
        in itertools.product(
            selected_setups,
            config["sweep_seeds"],
            config["corruption_fractions"],
        )
    ]
    debug_limit = config.get("sweep_debug_limit")
    return points if debug_limit is None else points[: int(debug_limit)]



def run_control_sweep(config):
    """Run every configured model study across the synthetic-data grid."""
    points = _grid_points(config)
    result_rows: list[dict] = []
    studies = {}

    iterator = tqdm(points, desc="dataset grid") if tqdm is not None else points
    for grid_index, point in enumerate(iterator, start=1):
        data, corruption_mode = make_dataset_for_grid_point(point, config)
        print(
            f"\n=== grid {grid_index}/{len(points)} | {point.function_name} | "
            f"d={point.dimension} | samples/dim={point.samples_per_dim} | "
            f"seed={point.seed} | "
            f"corruption={corruption_mode}:{point.corruption_fraction} ==="
        )

        for model_name in config["models_to_run"]:
            print(
                f"  Optuna/TPE study: {model_name} "
                f"({config['n_trials'][model_name]} trials)"
            )
            context = ModelStudyContext(
                data=data,
                model_name=model_name,
                base_config=config,
                corruption_fraction=float(point.corruption_fraction),
                corruption_mode=corruption_mode,
                result_rows=result_rows,
            )
            study = run_model_study(context)
            studies[point.study_key_prefix + (model_name,)] = study

            if config.get("checkpoint_after_each_study", True):
                save_results(result_rows, config)

    results_df, best_df = save_results(result_rows, config)
    return results_df, best_df, studies
