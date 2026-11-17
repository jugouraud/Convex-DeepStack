## 2. CPU acceleration playbook (ordered by expected payoff)

### 2.1 Algorithmic and system-level wins first

1. Remove duplicate calculation, redundant scans, unnecessary sorting/serialization, recomputation, repeated allocations, and reformatting of huge intermediates.
2. Use the appropriate algorithm/data structure: better asymptotics, chunked/streaming computation, efficient sparse representations, incremental updates, index-based lookups, blocking and divide-and-conquer, exact pruning where valid.
3. Consider precomputation/memoization **only** when storage, cache invalidation, and repeated-use patterns justify it.
4. Push filtering/projection/aggregation toward the data source; avoid loading whole tables if the answer needs a small slice. For dataframes, compare lazy scans, predicate pushdown, columnar formats, and vectorized group-bys.
5. Batch small operations to amortize Python call overhead, syscalls, library dispatch, locking, and IPC.
6. Minimize copies and intermediate arrays: in-place operations where safe, views/strides, contiguous layout, and preallocated output. Verify aliasing semantics.

### 2.2 Find the actual CPU bottleneck

| Evidence | Likely limit | Candidate action |
|---|---|---|
| High Python self-time, many tiny calls | Interpreter/dispatch | Vectorize, Numba/Cython, batch, compiled library |
| High LLC/DRAM misses, low arithmetic intensity | Memory-bound | SoA, compact dtype, blocking, better traversal, fewer passes |
| Bad branch speculation, irregular control flow | Branch-bound | Restructure hot loops / branch layout; PGO if stable |
| Retiring/compute-bound and little SIMD | Compute-bound | Compiler vectorization, SIMD-friendly loops, BLAS, dtype choice |
| Few cores busy; lots of independent work | Parallelism limit | Multiprocessing or multithreading (when GIL released), chunking |
| Many cores busy yet slow; contention | Overparallelized | Fewer threads, affinity, reduce locks/false sharing |
| Slower across sockets | NUMA/remote memory | First-touch placement, localize worker/data, bind as justified |
| Allocation/GC/parse dominates | Data plumbing | Reuse buffers, compact representation, faster ingest |

**Top-Down microarchitecture interpretation:** when hardware counters are available, inspect Frontend Bound, Bad Speculation, Backend Bound (memory/core), and Retiring, drilling down only for dominating hotspots. Counter names and thresholds vary by CPU. Measure; do not infer from a single counter.

### 2.3 Memory hierarchy and data layout

- Prefer sequential accesses, contiguous hot columns, Structure-of-Arrays over Array-of-Structures **when measurements and access patterns favor it**; shrink bytes/value only if the precision/range contract allows it.
- Use loop tiling / cache blocking to reuse small working sets in L1/L2/L3 before fetching new data. Tune tiles empirically and watch conflict misses.
- Avoid pointer chasing, unpredictable gathers, and excessive temporary matrices in bandwidth-limited work.
- Prevent false sharing and contention for shared counters; use per-thread local partials followed by reduction where semantics permit.
- NUMA pinning/first touch matters for multi-socket hosts; it should not be applied blindly on single-socket machines or managed runtimes.
- Memory-mapped files and streaming may save RAM but need I/O benchmarks; mmap is not a universal speed boost.

### 2.4 Vectorization, compilation, and native libraries

- Start with tuned libraries: NumPy/SciPy linked to optimized BLAS, oneMKL/OpenBLAS, FFT libraries, Polars/Arrow, domain-specific native routines. Check BLAS backend and thread count.
- For Python loops that dominate, compare NumPy broadcasting (watch temporaries), Numba `@njit` (after warmup), Cython, compiled extensions, or appropriate JIT/compiler. Do **not** rewrite the whole project in C++ as a first move.
- For C/C++/Rust, use optimized production builds and inspect compiler vectorization reports / disassembly before writing intrinsics. Benchmark `-O3` vs `-O2`, ISA-target flags, LTO and PGO; `-march=native` sacrifices portable binaries.
- Use `-ffast-math`, approximate transcendental functions, reduced precision, reassociation, flush-to-zero, and mixed precision **only under an explicitly tested numerical contract**.
- Where branch/layout locality dominates stable native binaries, consider PGO and post-link layout optimization (LLVM BOLT / Propeller-style techniques), with representative profiles and rollback. Such optimizers have no guaranteed win for every application.
- Prefer coarse, independent tasks over fine-grained threading for Python-bound code. Beware BLAS/OpenMP nested-thread oversubscription (`OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS`, `torch.set_num_threads`, etc.). Tune on actual hardware.
- Evaluate thread counts from 1 through physical-core and potentially SMT limits; record the best setting **for the workload**, not a universal number.

### 2.5 CPU stop conditions

Stop local optimization when the remaining runtime is irreducible I/O or memory traffic, the profiler no longer supports a high-impact hypothesis, speedup is within noise, compiler tuning breaks portability, or changes violate the correctness/maintenance budget. At that point evaluate a remote GPU **with the whole-pipeline model below**.

---
