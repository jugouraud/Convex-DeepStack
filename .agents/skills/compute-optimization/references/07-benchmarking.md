## 7. Practical benchmark and correctness guardrails

### 7.1 Minimal benchmark discipline

- Use a high-resolution monotonic wall clock for end-to-end (`time.perf_counter()`); synchronize GPU before recording completion. CUDA APIs are usually asynchronous.
- Use `torch.utils.benchmark.Timer` / `blocked_autorange` where applicable to amortize timer overhead; avoid claiming microsecond differences from one run.
- Fix seeds where possible; verify actual input distribution, dtype, shapes, memory layout, NaN/Inf handling, duplicates, zero-length cases, overflow and boundary conditions.
- Separate cold-start from steady-state; document caches, compilation, disk-cache warming, setup and input staging.
- On contested machines, benchmark at multiple times or isolate cores if authorized; report contention/noise. In Colab, shared hardware, GPU temperature, quota and runtime availability can change.
- Record peak memory/VRAM and allocation failures; improvements with OOM on target sizes are not wins.
- Validate **per-element and aggregate** results. An `allclose` check with a loose absolute tolerance can accept nonsense for near-zero outputs. Also compare norms, maximum errors, invariants, conserved totals, ranking/order if required, and representative hard cases.
- For stochastic algorithms, report distributional/statistical fidelity over repeated seeds, not equality of one output.
- Do not test only a warmed preloaded GPU tensor and silently call the result “end-to-end.”

### 7.2 Experiment ledger

For each candidate:

```text
ID / date / revision:
Hardware / software / precision / thread and GPU settings:
Input source / shapes / bytes / repetitions:
Baseline total (cold/warm, median+spread):
Measured bottleneck and expected Amdahl bound:
Change and mechanism:
Correctness test + error statistics:
CPU compute / GPU compute / network transfer / H2D-D2H / other phases:
Total end-to-end (cold/warm, median+spread):
Memory and resource use:
Result: KEEP / REVERT / RETEST; reason:
```

**Evidence rule:** A reported whole-program speedup must be `T_baseline_total / T_candidate_total`, same data and same inclusion of setup and transfer. Label device-only wins separately. Distinguish *speedup relative to unoptimized CPU* and *speedup relative to the best optimized CPU*.

---
