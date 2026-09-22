from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats

from .utils import ensure_output_folder

MODEL_COLORS = {
    "Convex DeepStack": "#0072B2",
    "SCNN": "#E69F00",
    "WaDiRo-SCNN": "#009E73",
    "ResNet": "#CC79A7",
}
CONTROL_MODELS = ["SCNN", "WaDiRo-SCNN", "ResNet"]
ALL_MODELS = ["Convex DeepStack", *CONTROL_MODELS]
METRIC = "test_MinMax_normalised_MSE"
MODEL_NAME_MAP = {
    "WaDiRo": "WaDiRo-SCNN",
    "WADIDRO": "WaDiRo-SCNN",
    "WaDiRoSCNN": "WaDiRo-SCNN",
    "ConvexDeepStack": "Convex DeepStack",
}
KEY_COLS = [
    "function",
    "dimension",
    "samples_per_dim",
    "seed",
    "corruption_fraction",
    "corruption_mode",
]


def _prepare_results_for_summary(
    results_df: pd.DataFrame,
    best_df: pd.DataFrame | None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if results_df.empty:
        empty_best = pd.DataFrame() if best_df is None else best_df.copy()
        return results_df.copy(), empty_best

    successful = results_df[results_df["status"].eq("ok")].copy()
    successful["Model"] = successful["Model"].replace(MODEL_NAME_MAP)
    successful[METRIC] = pd.to_numeric(successful[METRIC], errors="coerce")
    successful["training_seconds"] = pd.to_numeric(
        successful["training_seconds"], errors="coerce"
    )

    if best_df is None or best_df.empty:
        best = (
            successful.sort_values(KEY_COLS + ["Model", "objective_value"])
            .groupby(KEY_COLS + ["Model"], as_index=False)
            .first()
        )
    else:
        best = best_df.copy()
        best["Model"] = best["Model"].replace(MODEL_NAME_MAP)
        best[METRIC] = pd.to_numeric(best[METRIC], errors="coerce")
        best["training_seconds"] = pd.to_numeric(best["training_seconds"], errors="coerce")

    return successful, best


def _configuration_mask(frame: pd.DataFrame, configuration: dict) -> np.ndarray:
    comparisons = [frame[column].eq(configuration[column]) for column in KEY_COLS]
    return np.logical_and.reduce(comparisons)


def build_control_summary(results_df: pd.DataFrame, best_df: pd.DataFrame) -> pd.DataFrame:
    """Summarize control-model distributions against the best DeepStack result."""
    successful, best = _prepare_results_for_summary(results_df, best_df)
    if successful.empty:
        return pd.DataFrame()

    runtime_by_model = (
        successful.groupby("Model", as_index=True)["training_seconds"]
        .sum(min_count=1)
        .to_dict()
    )

    rows: list[dict] = []
    for key, group in successful.groupby(KEY_COLS, dropna=False):
        key_values = key if isinstance(key, tuple) else (key,)
        configuration = dict(zip(KEY_COLS, key_values))
        configuration_mask = _configuration_mask(best, configuration)
        convex_best = best[
            configuration_mask & best["Model"].eq("Convex DeepStack")
        ]
        convex_error = (
            float(convex_best[METRIC].iloc[0])
            if not convex_best.empty and pd.notna(convex_best[METRIC].iloc[0])
            else np.nan
        )

        for model_name in ALL_MODELS:
            model_trials = group[group["Model"].eq(model_name)].copy()
            if model_trials.empty:
                continue

            values = model_trials[METRIC].dropna().astype(float).to_numpy()
            mean_error = float(np.mean(values)) if len(values) else np.nan
            std_error = float(np.std(values, ddof=1)) if len(values) > 1 else 0.0
            percentile = np.nan
            if model_name in CONTROL_MODELS and len(values) and np.isfinite(convex_error):
                percentile = float(
                    scipy.stats.percentileofscore(values, convex_error, kind="rank")
                )

            model_best = best[
                configuration_mask & best["Model"].eq(model_name)
            ]
            if model_best.empty:
                best_row = model_trials.sort_values("objective_value").iloc[0]
            else:
                best_row = model_best.iloc[0]

            rows.append(
                {
                    **configuration,
                    "Model": model_name,
                    "gaussian_mean_test_MinMax_normalised_MSE": mean_error,
                    "gaussian_std_test_MinMax_normalised_MSE": std_error,
                    "best_test_MinMax_normalised_MSE": best_row.get(METRIC, np.nan),
                    "convex_percentile_in_model_overall_mse": percentile,
                    "training_seconds_total_all_configs": float(
                        runtime_by_model.get(model_name, np.nan)
                    ),
                }
            )

    return pd.DataFrame(rows).sort_values(KEY_COLS + ["Model"]).reset_index(drop=True)


def plot_gaussian_comparator(
    results_df: pd.DataFrame,
    best_df: pd.DataFrame,
    config_index: int = 0,
    *,
    output_dir: str | Path | None = None,
):
    """Plot each control-model error distribution against the DeepStack result."""
    successful, best = _prepare_results_for_summary(results_df, best_df)
    if successful.empty:
        raise RuntimeError("No successful trials available for plotting.")

    configurations = (
        successful[KEY_COLS].drop_duplicates().sort_values(KEY_COLS).reset_index(drop=True)
    )
    if configurations.empty:
        raise RuntimeError("No dataset configurations available for plotting.")

    configuration = configurations.iloc[int(config_index)]
    configuration_dict = configuration.to_dict()
    successful_mask = _configuration_mask(successful, configuration_dict)
    best_mask = _configuration_mask(best, configuration_dict)
    subset = successful[successful_mask].copy()
    convex_rows = best[best_mask & best["Model"].eq("Convex DeepStack")]
    if convex_rows.empty:
        return None
    convex_error = float(convex_rows[METRIC].iloc[0])

    control_values = {
        model_name: subset.loc[subset["Model"].eq(model_name), METRIC]
        .dropna()
        .astype(float)
        .to_numpy()
        for model_name in CONTROL_MODELS
    }
    control_values = {
        model_name: values for model_name, values in control_values.items() if len(values)
    }
    if not control_values:
        return None

    destination = Path(output_dir) if output_dir is not None else ensure_output_folder()
    destination.mkdir(parents=True, exist_ok=True)

    for model_name, values in control_values.items():
        plot_values = np.concatenate([values, np.asarray([convex_error])])
        data_min = float(np.min(plot_values))
        data_max = float(np.max(plot_values))
        if data_max - data_min < 1e-6:
            center = (data_min + data_max) / 2.0
            width = max(0.1, 0.1 * (data_max - data_min + 1e-12))
            data_min = max(0.0, center - width / 2)
            data_max = center + width / 2
        buffer = 0.05 * (data_max - data_min + 1e-12)
        x_min = data_min - buffer
        x_max = data_max + buffer

        plt.figure(figsize=(10, 5.5))
        counts, _, _ = plt.hist(
            values,
            bins=100,
            range=(x_min, x_max),
            color=MODEL_COLORS[model_name],
            alpha=0.7,
            label=f"{model_name} Histogram",
            edgecolor="black",
        )
        max_frequency = counts.max() if len(counts) else 0
        plt.axvline(
            convex_error,
            color=MODEL_COLORS["Convex DeepStack"],
            linewidth=1.75,
            linestyle="--",
            label=f"Convex DeepStack = {convex_error:.6g}",
        )
        plt.title(
            f"{model_name} vs Convex DeepStack comparator\n"
            f"{configuration['function']} | d={configuration['dimension']} | "
            f"samples/dim={configuration['samples_per_dim']} | "
            f"corruption={configuration['corruption_fraction']}"
        )
        plt.xlabel("Test MinMax-normalised MSE")
        plt.ylabel("Frequency")
        plt.ylim(bottom=0, top=max_frequency * 1.15 if max_frequency > 0 else None)
        plt.xlim(x_min, x_max)
        plt.grid(True, alpha=0.25)
        plt.legend()
        plt.tight_layout()

        plot_filename = (
            f"{model_name.replace(' ', '_')}_vs_ConvexDeepStack_comparator_histogram_"
            f"{configuration['function']}_{configuration['dimension']}_"
            f"{configuration['samples_per_dim']}_"
            f"corruption_{configuration['corruption_fraction']}.png"
        )
        plt.savefig(destination / plot_filename, bbox_inches="tight")
        plt.show()

    return configuration_dict


def run_summary_export_and_plot(
    results_df: pd.DataFrame,
    best_df: pd.DataFrame,
    *,
    output_dir: str | Path | None = None,
    summary_csv: str = "control_sweep_summary.csv",
    results_csv: str = "control_sweep_results.csv",
) -> pd.DataFrame:
    """Write result tables and generate the comparator figure."""
    folder = Path(output_dir) if output_dir is not None else ensure_output_folder()
    folder.mkdir(parents=True, exist_ok=True)

    results_df.to_csv(folder / results_csv, index=False)
    summary = build_control_summary(results_df, best_df)
    summary.to_csv(folder / summary_csv, index=False)
    plot_gaussian_comparator(results_df, best_df, output_dir=folder)
    return summary
