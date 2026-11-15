import pytest

from convex_deepstack import models
from experiments import comparison_models


def test_windows_deepstack_search_uses_scnn_only(monkeypatch):
    class Trial:
        def suggest_categorical(self, name, choices):
            if name == "block_type":
                pytest.fail("Windows should not sample a WaDiRo block type")
            return choices[0]

        def suggest_float(self, *args, **kwargs):
            return 0.01

    monkeypatch.setattr(models.sys, "platform", "win32")
    assert models._suggest_params_optuna(Trial())["block_type"] == "scnn"


def test_windows_direct_wadiro_fails_before_native_solver(monkeypatch):
    monkeypatch.setattr(comparison_models.sys, "platform", "win32")
    with pytest.raises(RuntimeError, match="disabled on Windows"):
        comparison_models.train_wadiro_or_scnn(
            "wadiro", None, None, cfg={}, device="cpu"
        )
