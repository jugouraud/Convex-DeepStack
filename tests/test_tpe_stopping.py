"""Behavioral checks for the paper's block-level ACI/TPE stopping rule."""

import numpy as np
import pytest

from convex_deepstack.models import ConvexDeepStack, DeepStackConfig


def _search_with_losses(monkeypatch, losses, **settings):
    """Use real Optuna trials while replacing only expensive convex training."""
    scores = iter(losses)
    best = {"search_loss": np.inf, "params": None, "model": None}

    def candidate_factory(self, data, *, verbose=False):
        def evaluate(params):
            loss = next(scores)
            if loss is None:
                return {"loss": 1e12, "status": "fail", "reason": "synthetic_failure"}
            if loss < best["search_loss"]:
                best.update(search_loss=loss, params=params, model=object())
            return {"loss": loss, "status": "ok"}

        return evaluate, best

    monkeypatch.setattr(ConvexDeepStack, "_objective_building_full", candidate_factory)
    monkeypatch.setattr(
        ConvexDeepStack,
        "_suggest_params_optuna",
        staticmethod(lambda trial: {"trial": trial.number}),
    )
    options = dict(
        max_evals=len(losses),
        warmup=2,
        stability_window=2,
        eps_stab=0.0,
        alpha_stop=0.25,
        optuna_multivariate=False,
        optuna_group=False,
        optuna_n_startup_trials=2,
        verbose=False,
    )
    options.update(settings)
    config = DeepStackConfig(**options).early_exit_for_block(1)
    return ConvexDeepStack(in_dim_x=1, out_dim=1)._tpe_search_early_exit(None, config)


def test_fixed_post_trigger_count_and_best_trial(monkeypatch):
    result = _search_with_losses(monkeypatch, [1.0] * 7 + [0.5] + [1.0] * 12)
    trace = result["early_exit_trace"]

    assert result["sampler_settings"]["trigger_trial"] == 5
    assert result["sampler_settings"]["m_stop"] == 3
    assert len(result["trial_records"]) == 8
    assert trace[4]["phase"] == "exploitation_trigger"
    assert trace[-1]["stopped"] is True
    assert result["best_search_loss"] == pytest.approx(0.5)


def test_threshold_uses_only_prior_losses(monkeypatch):
    result = _search_with_losses(monkeypatch, [1.0, 1.0, 2.0] + [3.0] * 5)
    third = result["early_exit_trace"][2]

    assert third["q_hat"] == pytest.approx(1.0)
    assert third["e_t"] == 1
    assert third["alpha_t"] < 0.1


def test_no_false_exchangeability_trigger_or_post_budget_claim(monkeypatch):
    changing = _search_with_losses(monkeypatch, [float(i) for i in range(1, 13)])
    assert changing["sampler_settings"]["trigger_trial"] is None
    assert changing["sampler_settings"]["stop_reason"] == "budget_exhausted"

    short = _search_with_losses(monkeypatch, [1.0] * 7)
    assert short["sampler_settings"]["trigger_trial"] == 5
    assert short["sampler_settings"]["post_trigger_trials"] == 2
    assert short["sampler_settings"]["stop_reason"] == "budget_exhausted"
    assert not any(record["stopped"] for record in short["early_exit_trace"])


def test_failed_fit_does_not_count_as_exchangeable_loss(monkeypatch):
    result = _search_with_losses(monkeypatch, [1.0, 1.0, None] + [1.0] * 15)
    assert result["sampler_settings"]["trigger_trial"] == 6
    assert len(result["trial_records"]) == 9
    assert result["early_exit_trace"][2]["phase"] == "failed"
    assert result["sampler_settings"]["post_trigger_trials"] == 3


@pytest.mark.parametrize("alpha_stop", [0.0, 1.0, -0.1, float("nan")])
def test_invalid_stopping_probability_is_rejected(monkeypatch, alpha_stop):
    with pytest.raises(ValueError, match="alpha_stop"):
        _search_with_losses(monkeypatch, [1.0] * 9, alpha_stop=alpha_stop)
