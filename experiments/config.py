from copy import deepcopy

from .utils import SEED

CONFIG = {
    # Synthetic benchmarks
    "function_names": ["ackley", "rastrigin", "rosenbrock"],
    "sweep_dimensions": [3,5,10],
    "sweep_samples_per_dim": [20,50,100],
    "sweep_seeds": [SEED],
    "sweep_setups": None,

    # Exact split ratios. N_train is fixed to dimension * samples_per_dim.
    "train_fraction": 0.60,
    "val_fraction": 0.20,
    "test_fraction": 0.20,

    # Training-set corruption. Clean runs are obtained by setting corruption_fraction=0.
    "corruption_mode": "sliced_wasserstein_outliers",
    "corruption_fractions": [0.0, 0.2, 0.4],
    "shared_noise_multiplier": 4.0,
    "target_noise_multiplier": 4.0,
    "input_noise_multiplier": 4.0,

    # Used only for "sliced_wasserstein_outliers".
    "wasserstein_min_distance": 0.2,
    "wasserstein_n_projections": 100,
    "wasserstein_k_multiplier": 1.1,
    "wasserstein_max_output_scale": 2,

    # Models to run.
    "models_to_run": ["WaDiRo-SCNN", "Convex DeepStack", "SCNN", "ResNet"],

    # Convex model constants.
    "wide_neurons": 512,
    "wadiro_wasserstein": "l2",
    "scnn_loss": "l2",
    "solver": "CLARABEL",

    # Fixed ResNet width; the TPE search does not sweep width.
    "resnet_width": 64,
    "resnet_epochs": 400,
    "resnet_patience": 60,

    # Convex DeepStack constants. Each outer Optuna trial chooses stack-level
    # hyperparameters; each accepted block is itself chosen by the internal TPE
    # search in ConvexDeepStack.build_optimal_model().
    # Relative validation-MSE improvement threshold after the minimum depth.
    "convex_improvement_tol": 1e-3,
    "convex_min_blocks": 2,
    # Weak blocks are still added; stop after this many consecutive weak blocks.
    "convex_block_patience": 2,
    "convex_alpha_stop": 0.05,
    "convex_optuna_multivariate": True,
    "convex_optuna_group": True,

    # TPE trial counts by model.
    "n_trials": {
        "SCNN": 100,
        "WaDiRo-SCNN": 100,
        "ResNet": 100,
        "Convex DeepStack": 1,
    },

    # Objective used by Optuna. The test score is recorded but never optimized.
    "objective_metric": "val_MinMax_normalised_MSE",

    # Search spaces.
    "search_space": {
        "wadiro_radius": {"low": 1e-4, "high": 10.0, "log": True},
        "scnn_lamb_reg": {"low": 1e-6, "high": 1e-1, "log": True},
        "scnn_regularizer": ["LASSO", "RIDGE"],
        "resnet_layers": {"low": 50, "high": 50},
        "resnet_dropout": {"low": 0.0, "high": 0.40},
        "resnet_learning_rate": {"low": 1e-4, "high": 3e-3, "log": True},
        "resnet_weight_decay": {"low": 1e-6, "high": 1e-2, "log": True},
        "resnet_batch_size": [32, 64, 128],
        "convex_nu": {"low": 1, "high": 1, "log": True},
        "convex_max_blocks": {"low": 100, "high": 100},
        "convex_max_evals": {"low": 100, "high": 100},
        "convex_warmup": {"low": 4, "high": 4},
    },

    # Leave as None for the full grid. Set to e.g. 1 or 2 for a smoke test.
    "sweep_debug_limit": None,

    # Output files.
    "results_csv": "control_sweep_results.csv",
    "best_csv": "control_sweep_best_by_validation.csv",
    "summary_csv": "control_sweep_summary.csv",

    # Periodic checkpointing after every completed model-study.
    "checkpoint_after_each_study": True,
}


def make_default_config() -> dict:
    """Return an independent mutable copy of the experiment defaults."""
    return deepcopy(CONFIG)
