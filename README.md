# ConvexDeepStack

A Python implementation of **ConvexDeepStack**, a greedy residual stack built from convex SCNN and WaDiRo-SCNN blocks.

---

## Introduction

ConvexDeepStack constructs a deeper predictor by fitting shallow convex neural-network blocks sequentially to the current residuals. At each stage, candidate SCNN and WaDiRo-SCNN blocks are explored with Optuna/TPE, converted to PyTorch through the upstream `wadiroscnn` package, and added to the residual stack when they improve validation performance.

## How it is made

The implementation relies on the public `wadiroscnn` package for the convex SCNN and WaDiRo-SCNN subproblems. ConvexDeepStack adds the residual-stacking, block-search, weighting, and stopping procedure around those models, while keeping the final stacked predictor as a PyTorch `nn.Module`.

The per-block TPE search uses an ACI quantile-stability trigger. After triggering, it stops following `ceil(1 / alpha_stop) - 1` further valid trials, unless `max_evals` is reached first. The new-best rank bound relies on a separate, unverified post-trigger exchangeability assumption; quantile stability alone is not a coverage or optimality guarantee.


```

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
    alpha_stop=0.05,
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

### UCI regression experiments

The UCI sweep follows the project's existing Optuna/TPE training pipeline and the
Drive notebooks: a deterministic 60/20/20 train/validation/test split, preprocessing
fitted only on training data, selection by validation MinMax-normalised MSE, and
original-unit validation/test metrics. The default TOML config includes Appliances
Energy (UCI 374, capped at 5,000 rows) and Bike Sharing (275, capped at 10,000 rows),
with seed 42 and one trial each for Convex DeepStack, SCNN, WaDiRo-SCNN, and ResNet
(eight outer trials total; CDS performs additional internal block searches). Edit
`experiments/config.toml` to select datasets, models, trial counts, search
spaces, and Colab hardware. Results are saved to the configured `colab.output_dir`.

Run without Colab:

```bash
python -m experiments.uci_runner --config experiments/config.toml
```

Use Linux or Colab for this full sweep: a native CVXPY extension abort was
observed with WaDiRo-SCNN on Windows. ConvexDeepStack searches SCNN residual
blocks only on Windows.

For remote execution, install and authenticate Google's official CLI on Linux or
macOS (`pip install google-colab-cli`, then follow `colab` authentication prompts).
The launcher provisions a Colab session, uploads a source snapshot, executes the
sweep, downloads CSVs/figures/manifest, and stops the session:

```bash
python scripts/run_uci_colab.py --config experiments/config.toml
```

The default `high_mem = true` requests high system RAM with `colab new --high-mem`;
`gpu = ""` keeps the convex solver workload on CPU. Set `gpu = "T4"` if desired
for ResNet. High RAM requires an eligible Colab account and available capacity;
it does not guarantee that a solver will fit. WSL only drives the CLI: training
and dependency installation happen remotely.

To package without authentication, training dependencies, or allocating a runtime
(Python 3.10+), run:

```bash
python scripts/run_uci_colab.py --package-only outputs/uci_colab_package
```

This snapshots current working-tree sources and the selected config, excluding
local data, outputs, environments, and credentials. Dependencies are declared in
`pyproject.toml` and installed remotely; versions are not locked by this package.
From the generated package directory on a Linux/macOS CLI host:

```bash
colab new --help  # Verify this installed version supports --high-mem.
colab new -s cds-uci --high-mem
colab status -s cds-uci
colab upload -s cds-uci source.zip /content/cds_uci_source.zip
colab exec -s cds-uci -f uci_colab_remote.py
colab download -s cds-uci /content/cds_uci_results.zip results.zip
python -m zipfile -t results.zip
colab stop -s cds-uci
```

Download and inspect results before stopping. If execution fails, inspect the
session and retrieve any partial files from `/content/cds_uci_job/outputs/uci/`
before stopping it; the result ZIP is created only after successful completion.

While using the automatic launcher, `<colab.output_dir>/status.json` is updated after each trial;
it is removed after a successful download and retained with failure status on
errors. Remote runs require network access to UCI datasets and Python packages.
Run `pytest -q tests/test_uci_pipeline.py tests/test_uci_colab.py` for the
focused offline checks. If cleanup fails, status remains `cleanup_required` and
the named Colab session must be stopped manually.

### Full synthetic CDS experiment

Run Convex DeepStack only over every configured synthetic function, dimension,
samples-per-dimension setting, seed, and corruption level:

```bash
python -m experiments.cds_synthetic_runner --output-dir outputs/cds_synthetic
```

The terminal prints one start/completion line per grid point. The output directory
contains `cds_synthetic_results.json` (final metrics and training time) and
`cds_synthetic_model_compositions.json` (selected trial settings, accepted-block
weights/types, and stopping history). Both files are atomically checkpointed after
each completed grid point.

## Upstream dependency

ConvexDeepStack uses the SCNN and WaDiRo-SCNN implementations from the `wadiroscnn` package. Their public GitHub implementation is maintained in `jupall/WaDiRo-SCNN`.

## Development and release checks

Run the same checks used by GitHub Actions with:

```bash
make check
```

The CI workflow tests Python 3.10, 3.11, and 3.12 and verifies that a wheel can be built.
The model/training/experiment boundaries and numerical contracts are documented in
[`docs/architecture.md`](docs/architecture.md). The default search is bounded to 20
accepted blocks; set `max_blocks` explicitly for a different finite budget.
The release workflow is configured for PyPI Trusted Publishing when a GitHub Release is published.
Before the first PyPI release, configure this GitHub repository as a Trusted Publisher for the
`convex-deepstack` project on PyPI and create a GitHub environment named `pypi`.

## License

ConvexDeepStack is released under the MIT License. See `LICENSE`.
