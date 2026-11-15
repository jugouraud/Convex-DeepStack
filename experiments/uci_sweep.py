"""UCI dataset-by-seed-by-model Optuna sweep using the existing model trainers."""

import pandas as pd

from .sweep import save_results
from .tuning import ModelStudyContext, run_model_study
from .uci_data import run_uci_data


def run_uci_sweep(config: dict, report_progress) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Train models, checkpoint per study, and emit completed-trial progress."""
    grid = [(dataset, seed) for dataset in config["uci_datasets"] for seed in config["sweep_seeds"]]
    total_trials = len(grid) * sum(config["n_trials"][m] for m in config["models_to_run"])
    completed = 0
    rows: list[dict] = []

    for dataset, seed in grid:
        data = run_uci_data(dataset, int(seed), config)
        for model_name in config["models_to_run"]:
            def after_trial(row):
                nonlocal completed
                completed += 1
                report_progress({
                    "state": "running",
                    "dataset": data["dataset_key"],
                    "model": model_name,
                    "trial": int(row["trial_number"]) + 1,
                    "outcome": row["status"],
                    "completed_trials": completed,
                    "total_trials": total_trials,
                })

            study = run_model_study(ModelStudyContext(
                data=data,
                model_name=model_name,
                base_config=config,
                corruption_fraction=0.0,
                corruption_mode="none",
                result_rows=rows,
                trial_callback=after_trial,
            ))
            if not any(t.user_attrs.get("result_row", {}).get("status") == "ok"
                       for t in study.trials):
                raise RuntimeError(f"All trials failed for {data['dataset_key']}/{model_name}")
            if config["checkpoint_after_each_study"]:
                save_results(rows, config)

    return save_results(rows, config)
