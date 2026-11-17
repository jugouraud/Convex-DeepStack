import json

from experiments.cds_synthetic_runner import run_cds_synthetic_experiment
from experiments.config import make_default_config


def test_cds_synthetic_runner_writes_summary_and_composition_json(monkeypatch, tmp_path):
    import experiments.cds_synthetic_runner as runner

    config = make_default_config()
    config.update({
        "models_to_run": ["Convex DeepStack"],
        "n_trials": {"Convex DeepStack": 1},
        "function_names": ["ackley"],
        "sweep_dimensions": [2],
        "sweep_samples_per_dim": [5],
        "sweep_seeds": [1],
        "corruption_fractions": [0.0],
    })

    class Trial:
        user_attrs = {
            "result_row": {
                "function": "ackley", "dimension": 2, "samples_per_dim": 5,
                "seed": 1, "corruption_mode": "none", "corruption_fraction": 0.0,
                "n_train": 10, "n_train_base": 10, "n_inserted_outliers": 0,
                "n_val": 3, "n_test": 3, "status": "ok", "error": None,
                "training_seconds": 1.25, "objective_metric": "val_MinMax_normalised_MSE",
                "objective_value": 0.1, "val_MSE": 1.0,
                "val_MinMax_normalised_MSE": 0.1, "test_MSE": 2.0,
                "test_MinMax_normalised_MSE": 0.2, "trial_seed": 10,
                "optuna_params_json": "{}", "convex_n_blocks": 1,
                "convex_n_block_attempts": 1, "convex_stop_reason": "max_blocks",
                "convex_min_blocks": 1, "convex_block_patience": 1,
                "convex_low_improvement_streak_at_stop": 0,
                "convex_baseline_val_mse_scaled": 1.0,
                "convex_final_val_mse_scaled": 0.5,
                "convex_block_history_json": '[{"best_weight": 0.5}]',
            }
        }

    class Study:
        trials = [Trial()]

    monkeypatch.setattr(runner, "run_model_study", lambda context: Study())
    summaries, compositions = run_cds_synthetic_experiment(tmp_path, config=config)
    assert summaries[0]["training_seconds"] == 1.25
    assert compositions[0]["block_history"] == [{"best_weight": 0.5}]
    assert json.loads((tmp_path / "cds_synthetic_results.json").read_text()) == summaries
    assert json.loads((tmp_path / "cds_synthetic_model_compositions.json").read_text()) == compositions
