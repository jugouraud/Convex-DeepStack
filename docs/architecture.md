# Architecture and scientific contracts

## Deployment and ownership

ConvexDeepStack is a **single-process Python library**. It has no service,
queue, database, tenancy, or external request surface. The caller owns input
arrays, the current model, seeds, filesystem permissions, and published outputs.
Convex solvers are invoked synchronously through the upstream `wadiroscnn`
package. Runtime depends on input size, candidate width and solver behavior;
there is no hard wall-clock deadline for a single upstream solve.

## Execution boundaries

```text
User arrays (training, validation)
    -> convex_deepstack.models.ConvexDeepStack.build_optimal_model
        -> validate shapes, finiteness, config, empty-stack invariant
        -> per-block Optuna TPE candidate search
            -> upstream SCNN/WaDiRo-SCNN solver (failure boundary)
            -> PyTorch residual prediction on validation data
        -> validation line search and acceptance/early stopping
        -> nn.ModuleList + fixed registered weights
    -> ConvexDeepStack.forward -> predictions

python -m experiments.runner  [final experiment orchestrator]
    -> experiments.sweep.run_control_sweep
        -> experiments.data.make_synthetic_split
        -> experiments.tuning.run_model_study
            -> experiments.comparison_models / ConvexDeepStack
            -> experiments.metrics.evaluate_model_on_splits
        -> CSV checkpoints in configured working directory
    -> experiments.reporting.run_summary_export_and_plot
```

The installable package (`src/convex_deepstack`) does not import experiment
code. Experiments may import the library; this dependency direction is
intentional. `ConvexDeepStack` and `DeepStackConfig` remain the public API.
The upstream package owns the convex optimization implementation; do not
reimplement its solvers inside this project without a separately reviewed
numerical-equivalence study.

## Contract and failure semantics

- Features: finite CPU-convertible `(n_samples, in_dim_x)` matrices for fitting.
- Targets: finite `(n_samples, out_dim)` matrices (a vector is allowed only for
  `out_dim=1`). Training and validation splits must both be nonempty.
- Score: validation mean squared error, **lower is better**; candidate search
  minimizes residual MSE and stack acceptance evaluates cumulative MSE.
- Inference: `(batch, in_dim_x)` tensor -> `(batch, out_dim)` tensor; accepted
  blocks receive the original features concatenated with current prediction.
- A newly initialized model must be fitted once; attempting to fit an already
  populated model is rejected rather than silently double-counting blocks.
- Scientific splits use their own seed; training outliers never enter test or
  validation targets. TPE is seeded separately per block/trial.
- A failed/infeasible convex candidate records a failure; search exhaustion
  terminates the stack. An infeasible synthetic outlier distance fails after
  a bounded number of draws, not with an infinite loop.
- Checkpoint CSVs contain study observations and may contain exception text;
  use synthetic/non-personal datasets and restrict output-directory access.
  CSV files are diagnostic artifacts, not transactional records or checkpoints
  that can be safely resumed without further validation.

## Prioritized quality scenarios

1. An invalid fit input is rejected **before** launching any optimizer.
2. Clean validation/test splits remain unchanged by train-only corruption.
3. Search work is bounded by block/trial limits and outlier attempt limits;
   single convex-solver runtime is still an upstream dependency.
4. Existing imports, class signatures, and `nn.Module` serialization remain
   compatible with the release's documented public API.
5. A fresh checkout's CI runs public API, numerical-contract, and experiment
   tests without requiring production datasets or Google Drive.

## Decision record: incremental architecture stabilization

**Status:** accepted for this patch; **owner:** repository maintainers.
**Options considered:** rewrite the 1,317-line training module into several
pipeline files now, or stabilize public boundaries and tests first.
**Decision:** retain the current model-training module and its compatibility
surface, while documenting ownership and adding tests at existing seams.
**Reason:** an untested move of search/optimization code would introduce a
numerical-regression risk disproportionate to this safety patch.
**Consequence:** `models.py` still combines model, candidate search, and
orchestration, and does not yet satisfy the one-core-step-per-file form of
PIPE1. The compensating control is contract-oriented coverage and a bounded
training configuration. **Review by:** 2027-02-13 or before the next major
model-training refactor, whichever comes first. Extract search and stack
construction only after establishing upstream-backed integration fixtures.
