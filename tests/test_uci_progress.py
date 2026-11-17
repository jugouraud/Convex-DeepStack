from experiments.uci_runner import run_uci_experiment


def test_uci_runner_prints_human_readable_progress(monkeypatch, tmp_path, capsys):
    import experiments.uci_runner as runner

    monkeypatch.setattr(runner, "load_uci_config", lambda *args: {
        "sweep_seeds": [1], "uci_datasets": [{"key": "example"}],
        "models_to_run": ["Convex DeepStack"], "n_trials": {"Convex DeepStack": 1},
    })
    monkeypatch.setattr(runner, "initialize_environment", lambda **kwargs: None)
    monkeypatch.setattr(runner, "run_uci_sweep", lambda config, report: (
        report({"state": "running", "event": "study_started", "dataset": "example",
                "model": "Convex DeepStack", "completed_trials": 0, "total_trials": 1}),
        report({"state": "running", "dataset": "example", "model": "Convex DeepStack",
                "trial": 1, "outcome": "ok", "training_seconds": 1.25,
                "objective_value": 0.1, "completed_trials": 1, "total_trials": 1}),
        (None, None),
    )[-1])
    monkeypatch.setattr(runner, "run_uci_reporting", lambda *args: None)

    config_path = tmp_path / "config.toml"
    config_path.write_text("[placeholder]\n")
    runner.run_uci_experiment(config_path, tmp_path)

    output = capsys.readouterr().out
    assert "[0/1] start dataset=example model=Convex DeepStack" in output
    assert "[1/1] ok dataset=example model=Convex DeepStack" in output
    assert "UCI experiment complete." in output
