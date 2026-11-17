<!-- Source: AGENTS_v1.6(1).md / OPT; IDs namespaced CORE.*. Source wording otherwise preserved. -->

## OPT


### Measure and choose work

- CORE.OPT1 M Before performance changes define workload/latency or throughput/cost target; profile whole path incl load/parse/transfer/compute/output; retain comparable hardware/runtime baseline.
- CORE.OPT2 M Benchmark completed work: repeated comparable trials, cold start/miss versus warm hit/steady state, warmup/compile costs, relevant latency spread/throughput/peak memory; GPU events or correct boundary synchronization.
- CORE.OPT3 S Remove unnecessary work/allocations and improve algorithms first; prefer optimized bulk kernels over interpreter loops/custom kernels; distinguish compute-, memory-, I/O-, or launch-bound work.

### Cache and load

- CORE.OPT4 S Cache only measured expensive reusable work; include key/lookup/load/decode/transfer/write/eviction costs. Reuse owned models/resources across calls when lifecycle-safe; do not duplicate datasets per worker blindly.
- CORE.OPT5 M Apply DATA4/AUTH/PRIV to caches; bound retained bytes/lifetime and mutation. Handle misses/corruption/partial entries explicitly; thread-safe cache coherence does not guarantee one computation per key.
- CORE.OPT6 S Tune storage layout/chunked reads/compression/mmap and loader workers/prefetch/persistence from measurements; account for RAM/pinned memory/IPC, lifecycle, dataset sharding/order/seeds.

### CPU behavior

- CORE.OPT7 S CPU: favor contiguous/sequential access, cache-friendly blocking, SIMD/BLAS, and buffer reuse; measure layout conversion and temporaries; test NUMA locality/affinity only when relevant.
- CORE.OPT8 M CPU: bound combined application/loader/BLAS/OpenMP thread+process pools to allocated resources; account for quotas, nested parallelism, IPC, replicated memory; document tuned settings.
- CORE.OPT9 S CPU: choose threads for I/O or native work releasing GIL; for GIL-bound Python consider coarse processes/native kernels. Check actual interpreter build, sharing races, and process-start overhead.

### GPU behavior

- CORE.OPT10 S GPU: offload only when end-to-end wins; batch/vectorize within latency+VRAM budgets, keep reusable data resident, avoid tiny launches/round trips; benchmark fusion/compile incl cold/recompile costs.
- CORE.OPT11 M GPU: budget live tensors/activations/workspaces/allocator-reserved memory and concurrent work; monitor allocated vs reserved peaks. Releasing allocator cache does not free live tensors.
- CORE.OPT12 S GPU: reduce/batch transfers first; try bounded pinned host buffers+nonblocking copies/stream overlap only when supported and measured. Avoid routine item()/CPU reads or allocator-cache flushing in hot loops.
- CORE.OPT13 M GPU: preserve stream/event dependencies and buffer lifetime; no read/reuse/mutation before async completion. Use runtime-supported multiprocessing; never fork an initialized accelerator runtime.

### Inference and numerical correctness

- CORE.OPT14 S CPU/GPU ML: use eval plus appropriate no-grad/inference mode only when gradients are unnecessary; benchmark autocast/precision/layout/compile options on supported hardware, not blanket half conversion.
- CORE.OPT15 M Validate optimizations against reference outputs/domain tolerances, finite/edge cases, gradient/training metrics as applicable; report numerical/determinism changes and actual end-to-end gains, memory/latency regressions.
