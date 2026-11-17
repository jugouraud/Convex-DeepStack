"""UCI experiment configuration and final orchestration."""

import argparse
import hashlib
import json
import math
import sys
import warnings
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10
    import tomli as tomllib

from .config import make_default_config
from .uci_reporting import run_uci_reporting
from .uci_sweep import run_uci_sweep
from .utils import initialize_environment

PROGRESS_PREFIX = "@@CDS_STATUS@@"
MODELS = {"Convex DeepStack", "SCNN", "WaDiRo-SCNN", "ResNet"}
EXPERIMENT_KEYS = {
    "sweep_seeds", "models_to_run", "train_fraction", "val_fraction", "test_fraction",
    "objective_metric", "wide_neurons", "resnet_width", "resnet_epochs", "resnet_patience",
    "convex_min_blocks", "convex_block_patience", "convex_improvement_tol", "convex_alpha_stop",
    "checkpoint_after_each_study",
}


def load_uci_config(path: str | Path, output: Path) -> dict:
    """Parse and validate the bounded TOML interface to the existing study configuration."""
    with Path(path).open("rb") as handle:
        supplied = tomllib.load(handle)
    if set(supplied) != {"experiment", "trials", "datasets", "search_space", "colab"}:
        raise ValueError("Expected [experiment], [trials], [[datasets]], [search_space], [colab]")
    if set(supplied["experiment"]) - EXPERIMENT_KEYS:
        raise ValueError("Unknown UCI experiment configuration key")
    config = make_default_config()
    config.update(supplied["experiment"])
    config["uci_datasets"] = supplied["datasets"]
    config["n_trials"].update(supplied["trials"])
    config["search_space"].update(supplied["search_space"])
    config["results_csv"] = str(output / "uci_control_sweep_results.csv")
    config["best_csv"] = str(output / "uci_control_sweep_best_by_validation.csv")
    config["group_columns"] = ["dataset", "uci_id", "target", "seed", "Model"]

    seeds = config["sweep_seeds"]
    models = config["models_to_run"]
    if not seeds or len(seeds) > 20 or any(type(s) is not int or s < 0 for s in seeds):
        raise ValueError("sweep_seeds must contain 1-20 nonnegative integer seeds")
    if not models or len(set(models)) != len(models) or not set(models) <= MODELS:
        raise ValueError("Unknown or duplicate model in models_to_run")
    fractions = [config[key] for key in ("train_fraction", "val_fraction", "test_fraction")]
    if (not all(type(value) in (int, float) and 0 < value < 1 for value in fractions)
            or not math.isclose(sum(fractions), 1.0, rel_tol=1e-8, abs_tol=1e-8)):
        raise ValueError("Split fractions must each be positive and sum to 1")
    if config["objective_metric"] != "val_MinMax_normalised_MSE":
        raise ValueError("Only validation MinMax-normalised MSE is supported")
    if not isinstance(config["uci_datasets"], list) or not 1 <= len(config["uci_datasets"]) <= 20:
        raise ValueError("Configure between 1 and 20 UCI datasets")
    for dataset in config["uci_datasets"]:
        if (not isinstance(dataset, dict) or set(dataset) - {"key", "id", "target_column", "max_rows"}
                or not isinstance(dataset.get("key"), str)
                or not dataset["key"].replace("_", "").isalnum()
                or type(dataset.get("id")) is not int or dataset["id"] < 1
                or ("max_rows" in dataset and
                    (type(dataset["max_rows"]) is not int
                     or not 10 <= dataset["max_rows"] <= 50000))
                or ("target_column" in dataset and
                    not isinstance(dataset["target_column"], str))):
            raise ValueError("Invalid UCI dataset specification")
    if len({d["key"] for d in config["uci_datasets"]}) != len(config["uci_datasets"]):
        raise ValueError("UCI dataset keys must be unique")
    for model in models:
        count = config["n_trials"].get(model)
        if type(count) is not int or not 1 <= count <= 1000:
            raise ValueError(f"Invalid trial count for {model}")
    if (type(config["wide_neurons"]) is not int or not 1 <= config["wide_neurons"] <= 4096
            or type(config["resnet_width"]) is not int or not 1 <= config["resnet_width"] <= 1024
            or type(config["resnet_epochs"]) is not int or not 1 <= config["resnet_epochs"] <= 20000
            or type(config["resnet_patience"]) is not int
            or not 1 <= config["resnet_patience"] <= config["resnet_epochs"]
            or type(config["convex_min_blocks"]) is not int
            or not 1 <= config["convex_min_blocks"] <= 1000
            or type(config["convex_block_patience"]) is not int
            or not 1 <= config["convex_block_patience"] <= 1000):
        raise ValueError("Invalid model capacity or stopping configuration")
    if set(supplied["trials"]) - MODELS:
        raise ValueError("Unknown trial model")
    if set(supplied["search_space"]) - set(make_default_config()["search_space"]):
        raise ValueError("Unknown search-space key")
    for name, spec in config["search_space"].items():
        if isinstance(spec, dict):
            low, high = spec.get("low"), spec.get("high")
            if (set(spec) - {"low", "high", "log"}
                    or type(spec.get("log", False)) is not bool
                    or type(low) not in (int, float) or type(high) not in (int, float)
                    or not math.isfinite(low) or not math.isfinite(high)
                    or low > high or (spec.get("log", False) and low <= 0)):
                raise ValueError(f"Invalid search-space range: {name}")
            is_integer_space = name.startswith((
                "convex_max_", "convex_warmup", "resnet_layers"
            ))
            if is_integer_space and (type(low) is not int or type(high) is not int
                                     or low < 1 or high > 1000):
                raise ValueError(f"Invalid integer search-space range: {name}")
            if name == "resnet_dropout" and (low < 0 or high >= 1):
                raise ValueError("ResNet dropout must be in [0, 1)")
        elif not isinstance(spec, list) or not 1 <= len(spec) <= 20:
            raise ValueError(f"Invalid search-space choices: {name}")
        elif name == "resnet_batch_size" and not all(
            type(v) is int and 1 <= v <= 4096 for v in spec
        ):
            raise ValueError("Invalid ResNet batch-size choices")
    trial_total = (len(config["uci_datasets"]) * len(seeds) *
                   sum(config["n_trials"][model] for model in models))
    if trial_total > 50000:
        raise ValueError("UCI sweep exceeds the 50,000-trial safety limit")
    return config


def run_uci_experiment(config_path: str | Path, output_dir: str | Path) -> None:
    """Compose the UCI data/study and reporting steps; emit machine-readable progress."""
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    config = load_uci_config(config_path, output)
    initialize_environment(seed=int(config["sweep_seeds"][0]))

    def progress(event):
        """Emit both launcher-readable and concise human progress output."""
        print(PROGRESS_PREFIX + json.dumps(event, separators=(",", ":")), flush=True)
        if event.get("state") == "completed":
            print("UCI experiment complete.", flush=True)
        elif event.get("event") == "study_started":
            print(
                f"[{event['completed_trials']}/{event['total_trials']}] start "
                f"dataset={event['dataset']} model={event['model']}",
                flush=True,
            )
        elif "trial" in event:
            print(
                f"[{event['completed_trials']}/{event['total_trials']}] "
                f"{event['outcome']} dataset={event['dataset']} model={event['model']} "
                f"trial={event['trial']} training_seconds={event.get('training_seconds'):.2f} "
                f"objective={event.get('objective_value')}",
                flush=True,
            )

    progress({"state": "running", "completed_trials": 0,
              "total_trials": len(config["uci_datasets"]) * len(config["sweep_seeds"]) *
              sum(config["n_trials"][m] for m in config["models_to_run"])})
    results, best = run_uci_sweep(config, progress)
    run_uci_reporting(results, best, output)
    revision = Path(__file__).resolve().parent.parent / "source_revision.txt"
    snapshot = Path(__file__).resolve().parent.parent / "source_snapshot_sha256.txt"
    manifest = {
        "source_snapshot_sha256": snapshot.read_text().strip() if snapshot.exists() else "unavailable",
        "source_revision": revision.read_text().strip() if revision.exists() else "unavailable",
        "config_sha256": hashlib.sha256(Path(config_path).read_bytes()).hexdigest(),
        "datasets": config["uci_datasets"],
        "seeds": config["sweep_seeds"],
        "split_fractions": [config[k] for k in
                            ("train_fraction", "val_fraction", "test_fraction")],
        "objective_metric": config["objective_metric"],
        "python": sys.version.split()[0],
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    progress({"state": "completed"})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run UCI studies locally (no Colab)")
    parser.add_argument("--config", default="experiments/config.toml")
    parser.add_argument(
        "--output-dir",
        help="Override the config output directory; use a new directory to avoid overwrites.",
    )
    arguments = parser.parse_args()
    if arguments.output_dir is None:
        with Path(arguments.config).open("rb") as handle:
            arguments.output_dir = tomllib.load(handle)["colab"]["output_dir"]
    # Solvers and Optuna can emit thousands of repeated warnings during a sweep.
    # Exceptions and tracebacks remain visible to the terminal.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        run_uci_experiment(arguments.config, arguments.output_dir)
