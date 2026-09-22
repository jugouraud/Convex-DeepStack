"""Compatibility tests for constructors provided by the upstream dependency."""

import wadiroscnn

from convex_deepstack.models import scnn, wadiro_scnn


def test_scnn_wrapper_uses_upstream_constructor(monkeypatch):
    """Forward SCNN construction arguments to the upstream package."""
    sentinel = object()

    def fake_scnn(*args, **kwargs):
        assert args == ("arg",)
        assert kwargs == {"option": 1}
        return sentinel

    monkeypatch.setattr(wadiroscnn, "scnn", fake_scnn)
    assert scnn("arg", option=1) is sentinel


def test_wadiro_wrapper_uses_upstream_constructor(monkeypatch):
    """Forward WaDiRo-SCNN construction arguments to the upstream package."""
    sentinel = object()

    def fake_wadiro_scnn(*args, **kwargs):
        assert args == ("arg",)
        assert kwargs == {"option": 1}
        return sentinel

    monkeypatch.setattr(wadiroscnn, "wadiro_scnn", fake_wadiro_scnn)
    assert wadiro_scnn("arg", option=1) is sentinel
