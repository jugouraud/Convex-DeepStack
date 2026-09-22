"""Smoke tests for the installable ConvexDeepStack public API."""

import torch

import convex_deepstack
from convex_deepstack import ConvexDeepStack, DeepStackConfig


def test_public_exports():
    """Expose only the intended top-level package API through star imports."""
    assert convex_deepstack.__all__ == ["ConvexDeepStack", "DeepStackConfig"]


def test_model_instantiation_and_empty_forward():
    """Instantiate the public model and evaluate its empty-stack prediction."""
    model = ConvexDeepStack(in_dim_x=3, out_dim=1)
    prediction = model(torch.ones((4, 3), dtype=torch.float64))
    assert prediction.shape == (4, 1)
    assert torch.equal(prediction, torch.zeros_like(prediction))


def test_default_config_is_constructible():
    """Construct the published default stack configuration."""
    config = DeepStackConfig()
    assert config.max_evals > 0
    assert config.min_blocks >= 1
