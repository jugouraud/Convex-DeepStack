## 0. Non-negotiable operating contract

1. **Correctness is a hard constraint.** Preserve semantics, numerical-error limits, data coverage, reproducibility requirements, and production behavior. Never make a benchmark faster by skipping work, shrinking outputs, dropping cases, exploiting an overly permissive tolerance, changing the random problem, or comparing unlike conditions.
2. **Measure before rewriting.** Determine the end-to-end critical path, locate the dominant bottleneck, write a falsifiable speed hypothesis, and compare with a reproducible baseline.
3. **Optimize in this order unless evidence contradicts it:** eliminate work / improve complexity → reduce data movement → improve data layout and memory locality → batch/fuse → use efficient libraries / compilers → tune concurrency and hardware → write custom low-level kernels.
4. **CPU is the default challenger.** A remote GPU is eligible only after an end-to-end cost model indicates a plausible net win for the user's problem sizes and reuse pattern. A GPU microbenchmark never proves a remote-GPU win.
5. **No invented benchmarks.** Never claim a speedup, GPU availability, transfer bandwidth, kernel support, tool installation, or reproducibility without an actual measurement. Label estimates and paper results as estimates / paper results.
6. **Do not assume the hardware.** Detect CPU ISA, core count, sockets/NUMA, RAM, GPU model/compute capability, VRAM, driver, CUDA, package versions, Colab quota, and accessible storage before choosing a path. T4 ≠ A100 ≠ H100; a research result on B200/GB200 is not evidence of a T4 speedup.
7. **Account for optimization overhead.** Include cold start, compilation, tuning, provisioning, upload, download, and reruns whenever they occur in the user's usage mode. Report both cold and warm latency if relevant.
8. **Work on representative inputs.** Include small, typical, large, and adversarial/edge shapes; consider irregular/sparse data and shape variability. Analyze latency and throughput separately.
9. **Change one material factor at a time.** Maintain a correctness-preserving reference implementation, short reversible patches, and a benchmark log. Retain only changes supported by repeatable end-to-end measurements.
10. **Respect privacy and cost.** Never upload private, confidential, licensed, regulated, or user-sensitive data to Colab without authorization. Avoid expensive provisioning, uncontrolled autotune sweeps, huge data uploads, or unattended running sessions.
11. **Prefer available optimized primitives.** BLAS/LAPACK, FFT, specialized sparse libraries, vectorized databases, PyTorch/Inductor, cuBLAS/cuDNN, existing attention kernels, etc. generally precede bespoke CUDA/Triton.
12. **Stop when marginal gain is unconvincing.** Reject optimizations whose realistic improvement is smaller than measurement noise, risk, maintenance cost, or remote overhead. Prefer a verified 1.2× whole-job gain over a speculative 10× kernel gain affecting 2% of runtime.

### Priority when this document is combined with a general AGENTS.md

Apply existing repository rules for safe edits, reviews, tests, API compatibility, and minimal diffs. This supplement controls the **performance diagnosis, measurement, CPU/GPU selection, and evidence**. If a conflict affects correctness, safety, or data handling, follow the stricter constraint. Do not rewrite a project merely to follow a performance fashion.

---
