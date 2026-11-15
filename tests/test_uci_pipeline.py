"""UCI contracts: reproducible data, configuration, and validation-selected reports."""

from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

from experiments import uci_data
from experiments.uci_reporting import run_uci_reporting
from experiments.uci_runner import load_uci_config


def test_uci_data_is_deterministic_and_keeps_test_targets_in_original_units(monkeypatch):
    rows = 60
    features = pd.DataFrame({
        "continuous": np.linspace(-3, 5, rows),
        "category": ["a", "b", "c"] * 20,
    })
    targets = pd.DataFrame({"response": np.linspace(100, 1000, rows)})
    monkeypatch.setattr(
        uci_data,
        "fetch_ucirepo",
        lambda id: SimpleNamespace(data=SimpleNamespace(features=features, targets=targets)),
    )
    config = {"train_fraction": 0.6, "val_fraction": 0.2, "test_fraction": 0.2}
    spec = {"key": "example", "id": 123, "max_rows": 50}
    first = uci_data.run_uci_data(spec, 42, config)
    again = uci_data.run_uci_data(spec, 42, config)

    assert (first["n_train"], first["n_val"], first["n_test"]) == (30, 10, 10)
    assert first["n_dim"] == 4  # one numeric and three one-hot columns
    assert np.array_equal(first["X_train_s"], again["X_train_s"])
    assert np.allclose(first["inverse_y"](first["y_test_s"]), first["y_test"].ravel())
    assert np.allclose(first["y_train_s"].mean(axis=0), 0.0, atol=1e-12)


def test_uci_config_rejects_unbounded_trials_and_split_leakage(tmp_path):
    source = Path(__file__).resolve().parents[1] / "experiments/config.toml"
    valid = source.read_text(encoding="utf-8")
    path = tmp_path / "config.toml"
    path.write_text(valid, encoding="utf-8")
    loaded = load_uci_config(path, tmp_path)
    assert loaded["n_trials"]["SCNN"] == 100
    assert loaded["group_columns"] == ["dataset", "uci_id", "target", "seed", "Model"]
    path.write_text(valid.replace('SCNN = 100', 'SCNN = 100001'))
    with pytest.raises(ValueError, match="trial count"):
        load_uci_config(path, tmp_path)
    path.write_text(valid.replace("val_fraction = 0.20", "val_fraction = 0.50"))
    with pytest.raises(ValueError, match="fractions"):
        load_uci_config(path, tmp_path)


def test_uci_report_uses_validation_selected_model_not_best_test(tmp_path):
    rows = []
    for model, scores in {"Convex DeepStack": [0.3], "SCNN": [0.1, 0.9]}.items():
        for index, score in enumerate(scores):
            rows.append({
                "dataset": "example", "uci_id": 111, "target": "y", "seed": 42,
                "Model": model, "trial_number": index, "status": "ok",
                "training_seconds": 1.0, "test_MinMax_normalised_MSE": score,
            })
    results = pd.DataFrame(rows)
    best = results.loc[[0, 2]]  # SCNN's 0.9 test error was validation-selected.
    summary = run_uci_reporting(results, best, tmp_path)
    selected = summary.loc[summary["Model"].eq("SCNN")].iloc[0]
    assert selected["best_test_MinMax_normalised_MSE"] == 0.9
    assert selected["mean_test_MinMax_normalised_MSE"] == 0.5
    assert (tmp_path / "plots" / "example_seed42_SCNN.png").exists()
