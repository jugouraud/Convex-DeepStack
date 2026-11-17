## 5. GPU acceleration playbook (only after passing the remote gate)

### 5.1 Start with the computational graph / libraries

1. Transfer/generate inputs **once**, and keep them in device memory across as much of the calculation as possible.
2. Ensure bulk work uses cuBLAS/cuDNN/efficient sparse and FFT kernels, and appropriate existing PyTorch/Numba/CuPy functionality. Avoid Python loops launching tiny GPU ops; vectorize, batch, or fuse.
3. Use `torch.inference_mode()` for inference where appropriate; compare efficient memory formats and batching. Do not disable gradient computation when required for training or differentiation.
4. Test `torch.compile` (when supported) after profiling graph breaks and tensor shapes. Account for **first-call compile time, recompilation from shape changes, steady-state throughput, and cache reuse**. A function that runs once may lose after compilation.
5. For sufficiently static shapes and host launch bottlenecks, investigate CUDA Graphs / compiler modes that reduce launch overhead; respect supported graph semantics, mutation constraints, extra memory requirements, and debugging complexity.
6. Test AMP/bfloat16/FP16/TF32 or reduced storage precision **only when hardware supports it and the end-to-end numerical-error contract passes**. Check underflow, accumulation type, determinism, and data-transfer representation.
7. Remove hidden synchronization (`.item()`, `.cpu()`, printed tensors, implicit device transfers, data-dependent Python control). Use an explicitly synchronized timer for full GPU computation when needed.
8. For training/data pipelines, compare prefetch, pinned buffers, worker count, persistent workers and batch size while measuring CPU decode, H2D, GPU utilization, and memory pressure. More workers can hurt.

### 5.2 When custom kernels are justified

Write Triton, TileLang, Helion, CuTe DSL, or CUDA kernels **only** after a profiler shows that existing operations dominate and optimized libraries/compilers are insufficient. Choose a DSL supported by the actual GPU and project environment; maintain a reference implementation and differential tests. Benchmark **compilation/autotuning cost as well as runtime**.

Check the following, as supported by hardware and profiling:

- Global-memory coalescing, alignment, useful bytes per transaction, and avoidable HBM round trips.
- Tiling, register and shared-memory reuse, arithmetic intensity, and fusion of compatible operations; check occupancy reductions caused by large tiles / register pressure.
- Launch geometry, occupancy, warp divergence, bank conflicts, synchronization and atomics; do not maximize occupancy at the expense of useful throughput.
- For tensor-core-friendly operations: actual precision, tile constraints, math mode, and correct accumulation/error.
- Pipelined/asynchronous copies and warp specialization on architectures where available; protect against race conditions and unnecessary synchronizations.
- Shape families: irregular tails, tiny inputs, large/sparse inputs, and non-contiguous strides. Autotune across **representative** shapes, not one benchmark shape.
- Memory safety: bounds, races, aliasing, out-of-range masks; output initialization where needed. Compare against high-precision reference including edge cases.

### 5.3 Classify GPU bottlenecks accurately

| Evidence | First actions |
|---|---|
| CPU timeline full of tiny launches | Batch, fuse, compiled graph, CUDA Graphs if compatible |
| H2D/D2H dominates | Reduce crossings, keep state on device, pinned async transfers if beneficial |
| HBM bandwidth ceiling | Eliminate intermediates, tile/reuse, fuse and compact data |
| Poor memory coalescing | Fix layout / access pattern; profile transactions |
| Tensor core underuse in GEMM-heavy case | Check shapes/dtypes/layout/library path/precision contract |
| Register spills/shared-memory pressure | Smaller tiles, different kernel schedule, check occupancy |
| Low utilization on tiny jobs | CPU may win; batch independent jobs |
| Network upload/download dominates | Redesign remote data flow or **choose CPU** |

**GPU profile is not the objective.** A kernel can be 3× faster while the complete Colab job is slower after upload or compilation. Always retime the full job after each optimization.

---
