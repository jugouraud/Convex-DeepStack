---
name: compute-optimization
description: Use for actual CPU/GPU acceleration, numerical/scientific performance, profiling, benchmarking, CUDA/PyTorch kernels, or remote Google Colab CLI compute. Not for routine unrelated code edits or an unmeasured request to add a cache.
---

# Computation-Speed Optimization Specialist

Use together with `AGENTS.md` and `docs/agent-policy/core/OPT.md`; preserving correctness, privacy, numerical contract, and minimal patch scope is mandatory. This specialist only governs optimization diagnosis and evidence. Do not assume GPUs, Colab access, CLI availability, or permission to transfer data.

**Mandatory sequence:** characterize real workload and accuracy → time end-to-end baseline → profile top bottleneck → estimate plausible upper bound → change one factor → verify correctness → compare repeated end-to-end cold/warm results → keep/revert and report. CPU is the default challenger. Do not claim improvements without actual measurements. Do not upload data or provision costly remote resources without authorization.

## Selective references

- `references/00-operating-contract.md` — complete non-negotiable performance contract.
- `references/01-experiment-workflow.md` — hypothesis, reproducibility, profiling, timing, report format; read for all consequential optimization.
- `references/02-cpu-optimization.md` — algorithm, locality, SIMD, threading, compiler, native libraries.
- `references/03-remote-gpu-cost.md` — use only when remote Colab GPU is a candidate; upload/download, H2D/D2H and break-even.
- `references/04-colab-cli.md` — use only for authorized Colab CLI execution; verify installed interface first.
- `references/05-gpu-optimization.md` — use for GPU kernel, CUDA, PyTorch device tuning.
- `references/06-cpu-vs-gpu.md` — use when choosing accelerator/compute environment.
- `references/07-benchmarking.md` — robust repetition, correctness or numerical precision.
- `references/09-report.md` — final optimization deliverable, measured vs unmeasured data.
- `references/08-research-2024-2026.md` and `references/10-references.md` — maintenance/research only; check recency and hardware applicability.

If the task is ordinary API or UI latency optimization, also read the applicable backend `PERF` or frontend `PERF` reference; those encode system-specific correctness and performance concerns.
