# ConvexDeepStack

A Python implementation of **ConvexDeepStack**, a greedy residual stack built from convex SCNN and WaDiRo-SCNN blocks.

---

## Introduction

ConvexDeepStack constructs a deeper predictor by fitting shallow convex neural-network blocks sequentially to the current residuals. At each stage, candidate SCNN and WaDiRo-SCNN blocks are explored with Optuna/TPE, converted to PyTorch through the upstream `wadiroscnn` package, and added to the residual stack when they improve validation performance.

## How it is made

The implementation relies on the public `wadiroscnn` package for the convex SCNN and WaDiRo-SCNN subproblems. ConvexDeepStack adds the residual-stacking, block-search, weighting, and stopping procedure around those models, while keeping the final stacked predictor as a PyTorch `nn.Module`.


## How to use it

### Download

Install from a local checkout with:

```bash
python -m pip install .
```

For development, use an editable install:

```bash
python -m pip install -e ".[dev]"
```

Publication experiment dependencies can be installed with:

```bash
python -m pip install -e ".[experiments]"
```

Once a release is published on PyPI, the intended installation command is:

```bash
python -m pip install convex-deepstack
```

### Create and train a model

```python
from convex_deepstack import ConvexDeepStack, DeepStackConfig

model = ConvexDeepStack(in_dim_x=X_train.shape[1], out_dim=1)

config = DeepStackConfig(
    nu=0.1,
    max_blocks=20,
    max_evals=100,
    warmup=20,
)

history = model.build_optimal_model(
    X_train,
    y_train,
    X_validation,
    y_validation,
    config=config,
)
```

### Predict with the stacked PyTorch model

```python
import torch

model.eval()
with torch.no_grad():
    prediction = model(torch.tensor(X_test, dtype=torch.float64))
```

The fitted object remains a standard PyTorch module and can therefore be used with ordinary PyTorch inference tooling.

## Publication experiments

The evaluation code is kept outside the installable package, directly under `experiments/`, in the same spirit as the upstream WaDiRo-SCNN repository.

Run the complete experiment workflow with:

```bash
python -m experiments.runner
```

The main experiment files are:

- `comparison_models.py`: standalone SCNN, WaDiRo-SCNN, and ResNet baselines;
- `corruption.py`: robustness/corruption procedures;
- `tuning.py`: model-level Optuna studies;
- `sweep.py`: experiment orchestration;
- `metrics.py` and `reporting.py`: evaluation metrics and publication summaries.

## Upstream dependency

ConvexDeepStack uses the SCNN and WaDiRo-SCNN implementations from the `wadiroscnn` package. Their public GitHub implementation is maintained in `jupall/WaDiRo-SCNN`.

## Development and release checks

Run the same checks used by GitHub Actions with:

```bash
make check
```

The CI workflow tests Python 3.10, 3.11, and 3.12 and verifies that a wheel can be built.
The release workflow is configured for PyPI Trusted Publishing when a GitHub Release is published.
Before the first PyPI release, configure this GitHub repository as a Trusted Publisher for the
`convex-deepstack` project on PyPI and create a GitHub environment named `pypi`.

## License

ConvexDeepStack is released under the MIT License. See `LICENSE`.
