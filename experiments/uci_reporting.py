"""UCI validation-selected results and test-error comparison figures."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .reporting import METRIC, MODEL_COLORS

plt.switch_backend("Agg")
KEYS = ["dataset", "uci_id", "target", "seed"]


def run_uci_reporting(results: pd.DataFrame, best: pd.DataFrame, output: Path) -> pd.DataFrame:
    """Summarize test error and plot each control distribution vs selected CDS."""
    successful = results.loc[results["status"].eq("ok")].copy()
    rows = []
    figures = output / "plots"
    figures.mkdir(parents=True, exist_ok=True)

    for key, group in successful.groupby(KEYS, sort=True):
        selected = best.loc[(best[KEYS] == pd.Series(key, index=KEYS)).all(axis=1)]
        cds = selected.loc[selected["Model"].eq("Convex DeepStack")]
        cds_error = float(cds[METRIC].iloc[0]) if not cds.empty else None
        for model_name, model_trials in group.groupby("Model", sort=True):
            errors = model_trials[METRIC].to_numpy(dtype=float)
            chosen = selected.loc[selected["Model"].eq(model_name)]
            rows.append({
                **dict(zip(KEYS, key)),
                "Model": model_name,
                "mean_test_MinMax_normalised_MSE": float(np.mean(errors)),
                "std_test_MinMax_normalised_MSE": float(np.std(errors, ddof=1))
                if len(errors) > 1 else 0.0,
                "best_test_MinMax_normalised_MSE": float(chosen[METRIC].iloc[0]),
                "training_seconds_total": float(model_trials["training_seconds"].sum()),
                "cds_percentile_in_model": float(100 * np.mean(errors <= cds_error))
                if cds_error is not None and model_name != "Convex DeepStack" else np.nan,
            })
            if cds_error is None or model_name == "Convex DeepStack":
                continue
            fig, ax = plt.subplots(figsize=(9, 5))
            ax.hist(errors, bins=min(30, max(1, len(errors) // 2)),
                    color=MODEL_COLORS[model_name], alpha=0.7)
            ax.axvline(cds_error, color=MODEL_COLORS["Convex DeepStack"],
                       linestyle="--", label=f"Convex DeepStack: {cds_error:.5g}")
            ax.set(title=f"{key[0]} / seed {key[3]}: {model_name} vs Convex DeepStack",
                   xlabel="Test MinMax-normalised MSE", ylabel="Frequency")
            ax.grid(alpha=0.25)
            ax.legend()
            fig.tight_layout()
            fig.savefig(figures / f"{key[0]}_seed{key[3]}_{model_name.replace(' ', '_')}.png")
            plt.close(fig)

    summary = pd.DataFrame(rows)
    summary.to_csv(output / "uci_control_sweep_summary.csv", index=False)
    return summary
