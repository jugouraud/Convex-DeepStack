import numpy as np
import pytest

from experiments.config import make_default_config
from experiments.corruption import corrupt_training_set, sliced_wasserstein_outlier_introducer
from experiments.data import make_synthetic_split
from experiments.data_config import SyntheticSplitConfig, WassersteinOutlierConfig


def test_experiment_grid_lists_distinct_benchmarks():
    assert make_default_config()["function_names"] == ["ackley", "rastrigin", "rosenbrock"]


def test_unknown_corruption_mode_is_rejected_even_for_clean_run():
    with pytest.raises(ValueError, match="Unknown corruption_mode"):
        make_synthetic_split(SyntheticSplitConfig("ackley", 2, 5, 1, corruption_mode="typo"))
    with pytest.raises(ValueError, match="Unknown corruption_mode"):
        corrupt_training_set(np.zeros((3, 2)), np.zeros((3, 1)),
                             corruption_mode="typo", corruption_fraction=0)


def test_zero_fraction_is_clean_even_with_outlier_mode():
    data = make_synthetic_split(SyntheticSplitConfig(
        "ackley", 2, 5, 5, corruption_mode="sliced_wasserstein_outliers", corruption_fraction=0.0,
    ))
    np.testing.assert_array_equal(data["X_train_s"], data["X_train"])
    np.testing.assert_array_equal(data["y_train_s"], data["y_train_clean"])
    assert data["n_inserted_outliers"] == 0


def test_validation_and_test_remain_clean_during_outlier_insertion(monkeypatch):
    import experiments.data as module

    def append_points(signal, domain, function, rng, config):
        return np.vstack((signal, np.zeros((config.n_points, signal.shape[1]))))

    monkeypatch.setattr(module, "sliced_wasserstein_outlier_introducer", append_points)
    data = make_synthetic_split(SyntheticSplitConfig(
        "ackley", 2, 5, 5, corruption_mode="sliced_wasserstein_outliers", corruption_fraction=0.2,
    ))
    np.testing.assert_array_equal(data["X_val_s"], data["X_val"])
    np.testing.assert_array_equal(data["y_val_s"], data["y_val"])
    np.testing.assert_array_equal(data["X_test_s"], data["X_test"])
    assert data["n_inserted_outliers"] == 2


def test_outlier_generation_has_bounded_failure(monkeypatch):
    import experiments.corruption as module

    class Transport:
        @staticmethod
        def sliced_wasserstein_distance(*args, **kwargs):
            return 0.0

    monkeypatch.setattr(module, "_load_optimal_transport", lambda: Transport)
    config = WassersteinOutlierConfig(2, 1, 1.0, 2, 1.1, 2.0, 0)
    with pytest.raises(RuntimeError, match="1000 attempts"):
        sliced_wasserstein_outlier_introducer(
            np.zeros((4, 3)), [np.full(2, -1.0), np.ones(2)],
            lambda x: np.zeros((len(x), 1)), np.random.default_rng(1), config,
        )
