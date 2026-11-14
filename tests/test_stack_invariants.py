import numpy as np
import pytest
import torch
from torch import nn

from convex_deepstack import ConvexDeepStack, DeepStackConfig


class FixedResidual(nn.Module):
    def forward(self, x):
        return x[:, :1] + 1


def test_invalid_search_budgets_are_rejected():
    for overrides in (
        {"max_blocks": None}, {"max_blocks": 1}, {"max_evals": 0},
        {"nu": 0}, {"nu": 1.1}, {"recent_window": 0},
        {"optuna_group": True, "optuna_multivariate": False},
    ):
        with pytest.raises(ValueError):
            DeepStackConfig(**overrides)


def test_training_rejects_invalid_shape_before_search(monkeypatch):
    model = ConvexDeepStack(2, 1)
    monkeypatch.setattr(model, "_tpe_search_early_exit", lambda *args: pytest.fail("search ran"))
    with pytest.raises(ValueError, match="aligned"):
        model.build_optimal_model(np.ones((3, 2)), np.ones(2), np.ones((2, 2)),
                                  np.ones(2), DeepStackConfig(verbose=False))
    with pytest.raises(ValueError, match="finite"):
        model.build_optimal_model(np.array([[np.inf, 1.0]]), np.ones(1),
                                  np.ones((2, 2)), np.ones(2), DeepStackConfig(verbose=False))


def test_block_weight_and_inference_contracts():
    model = ConvexDeepStack(2, 1)
    with pytest.raises(ValueError, match="finite"):
        model.add_block(FixedResidual(), float("nan"))
    assert len(model.blocks) == 0
    model.add_block(FixedResidual(), 0.25)
    result = model(torch.ones((3, 2), dtype=torch.float64))
    assert result.shape == (3, 1)
    torch.testing.assert_close(result, torch.full((3, 1), 0.5, dtype=torch.float64))
    with pytest.raises(ValueError, match="shape"):
        model(torch.ones((3, 3), dtype=torch.float64))
    with pytest.raises(ValueError, match="finite"):
        model.set_block_weight(0, float("inf"))
    assert float(model.get_block_weight(0)) == 0.25


def test_training_cannot_silently_restart_a_fitted_stack():
    model = ConvexDeepStack(2, 1)
    model.add_block(FixedResidual())
    with pytest.raises(RuntimeError, match="empty stack"):
        model.build_optimal_model(None, None, None, None, DeepStackConfig(verbose=False))


def test_residual_line_search_rejects_broadcasting():
    with pytest.raises(ValueError, match="match"):
        ConvexDeepStack._compute_boosting_weight(
            np.ones((3, 2)), np.ones((3, 1)), np.zeros((3, 1)), 0.5
        )


def test_repeated_candidates_preserve_residual_predictions(monkeypatch):
    from convex_deepstack import models as module
    from convex_deepstack.models import ResidualSearchData

    observed = []

    class LastPrediction(nn.Module):
        def forward(self, features):
            return features[:, -1:]

    class FakeSCNN:
        def train(self, X_train, Y_train, **kwargs):
            observed.append((X_train.copy(), Y_train.copy()))

        def get_torch_model(self):
            return LastPrediction()

    monkeypatch.setattr(module, "scnn", FakeSCNN)
    features = np.array([[1.0, 0.0], [2.0, 1.0]])
    targets = np.array([[2.0], [3.0]])
    previous = np.array([[0.5], [1.0]])
    data = ResidualSearchData(features, targets, features, targets, previous, previous)
    model = ConvexDeepStack(2, 1)
    evaluate, best = model._objective_building_full(data)
    params = {"block_type": "scnn", "max_neurons_scnn": 2, "bias_scnn": True,
              "loss_scnn": "l2", "lamb_reg_scnn": 0.01, "regularizer_scnn": "RIDGE"}
    first = evaluate(params)
    second = evaluate(params)
    expected = float(np.mean((targets - 2.0 * previous) ** 2))
    assert first["status"] == second["status"] == "ok"
    assert first["loss"] == second["loss"] == expected
    assert best["search_loss"] == expected
    for x_observed, y_observed in observed:
        np.testing.assert_array_equal(x_observed, np.column_stack((features, previous)))
        np.testing.assert_array_equal(y_observed, targets - previous)
    np.testing.assert_array_equal(features, np.array([[1.0, 0.0], [2.0, 1.0]]))
