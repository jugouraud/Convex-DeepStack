## 1. Required workflow: Diagnose → Model → Experiment → Validate → Report

### Phase A — Establish the task and performance contract

Before touching hot code, record:

- **Workload:** algorithm, input sizes/shapes, distribution/sparsity, number of calls, dependencies, data origin, output size, whether data already lives remotely, and whether calls are independent or stateful.
- **Metric:** e.g. cold one-shot completion time, warm batch throughput, p50/p95 latency, peak resident RAM/VRAM, cost per solved problem, energy, or a weighted objective. Use the user's real metric as the primary one.
- **Accuracy contract:** bitwise identity vs numerical tolerance; deterministic vs stochastic; precision range and overflow/underflow behavior; full expected output; allowed approximations.
- **Hardware/runtime:** model, core/SM count if available, RAM/VRAM, OS, library versions, thread settings, accelerator quota, transfer path, and target deployment machine. Record local and remote environments separately.
- **Constraints:** deadline, monetary/compute-unit budget, allowed dependencies, CPU/GPU permissions, acceptable complexity/maintenance, upload authorization.

**Baseline artifacts:** command, commit/hash or source fingerprint, inputs/hash, environment, timings, correctness check, and memory use. Record `N` or `n_samples`; never compare a debug build with optimized release code.

### Phase B — Profile the actual critical path

1. Measure **whole-program wall clock** (including input, parse, compute, output); identify the top 2–3 phases.
2. Separate one-time costs from per-batch/per-call costs; measure cold and warm operation.
3. For CPU, use wall-clock tracing plus `cProfile` / `py-spy` for Python stacks, `perf` / VTune for native code when permitted, and allocation/memory profilers as needed. `cProfile` alone cannot diagnose CPU cache stalls inside native kernels.
4. For GPU, profile host scheduling, CUDA launch, H2D/D2H copies, device kernel time, synchronization, and memory. Use `torch.profiler`, Nsight Systems, and Nsight Compute when available; otherwise use CUDA events and synchronized wall-clock timing.
5. Identify one primary limit: **algorithmic, I/O/network, memory capacity, memory bandwidth, cache/NUMA, serialization, interpreter/launch overhead, compute throughput, synchronization, or underutilization.** A workload may change regimes with size.

**Mandatory hypothesis template:**

> “On representative case X, phase Y occupies ~Z% of whole-job time. Technique A should reduce Y by mechanism M, at extra cost C. Predicted upper bound on total speedup is S; I will validate with benchmark B and correctness check K.”

If no measured hotspot exists, do not optimize a random loop.

### Phase C — Build a simple bound before implementing

- **Amdahl's law:** if fraction `f` of the original end-to-end time is accelerated by factor `s`, `S_total = 1 / ((1-f) + f/s)`. When `f = 0.10`, even infinite acceleration of that fraction yields at most `1.11×` overall.
- **Roofline:** `attainable_compute ≲ min(peak_compute, arithmetic_intensity × sustainable_memory_bandwidth)`. Use a **measured, architecture- and precision-specific** bandwidth / throughput ceiling where possible. Arithmetic intensity = useful operations per byte moved at the relevant memory level, not merely bytes in the source file.
- **Little's law / parallelism:** look for sufficient independent in-flight work, but avoid oversubscription, synchronization, and memory-thrashing. Added threads are not automatically faster.
- **Bandwidth lower bound:** if the algorithm must move `B` bytes through a boundary with sustained bandwidth `b`, then time is at least `B / b` before protocol overheads. Apply separately to network, host RAM/PCIe, and GPU HBM rather than using one imagined bandwidth.
- **Size regime:** chart time vs input size; measure crossover points. A simpler CPU implementation can be optimal for small jobs, GPU for large or repeated ones.

### Phase D — Controlled experimentation

Use at least 3–5 representative repetitions per candidate when practical; increase repetitions for noisy/short runs. Warm up JIT, caches, CUDA contexts, and memory allocators **only when reporting steady-state throughput**. Randomize or alternate candidate order to reduce drift, pin thread settings, and record median plus spread (e.g. p10–p90/IQR); also record tail latency when relevant. Never compare timings from unequal inputs or unsynchronized CUDA operations.

Change a single factor, check correctness, measure total wall clock, then decide whether to keep or revert. Preserve profiler traces / results sufficient to explain the decision.

### Phase E — Required final performance report

| Metric | Baseline CPU | Optimized CPU | Colab GPU (if tested) |
|---|---:|---:|---:|
| End-to-end cold time (s) | measured | measured | measured, **including provisioning/transfer** |
| End-to-end warm time (s) | measured | measured | measured, **including per-call transfer** |
| Compute-only time (s) | measured | measured | **device or remote compute, distinctly labeled** |
| Input upload / output download (s) | N/A | N/A | measured |
| Host↔device copies (s) | N/A | N/A | measured |
| Memory peak | measured | measured | remote RAM + VRAM |
| Output validation | pass/fail | pass/fail | pass/fail |
| Reproducible environment | specified | specified | specified |

Include measured speedup on the same end-to-end basis, accuracy deltas, setup costs amortized over expected repeated use, limitations, confidence/noise, and a precise recommendation. If Colab was unavailable, state **not tested** and provide a CPU result; do not fabricate a GPU timing.

---
