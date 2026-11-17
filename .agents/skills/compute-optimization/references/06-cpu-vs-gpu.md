## 6. CPU versus Colab GPU: decision rules

| Workload / conditions | Preferred first experiment | Why / exception |
|---|---|---|
| Tiny or latency-critical interactive task, local data | CPU | Remote provisioning and RTT dominate; test if amortized session exists |
| Branch-heavy, irregular pointer chasing, modest data | CPU | Limited coalescing and irregular control; still profile |
| Large dense GEMM, convolution, large batched transforms | Optimized CPU **and** GPU estimate | High parallelism; GPU only if transfers + setup are amortized |
| Many identical jobs, large reusable model on remote VM | Colab GPU candidate | Reuse amortizes setup and data upload; confirm quota and VRAM |
| Huge local input, tiny compute per byte | CPU / local streaming | Network is often the bottleneck; compress/reduce first |
| Huge dataset already in remote cloud storage, small outputs | Colab GPU candidate | Avoid local upload path; benchmark cloud storage ingress |
| Single giant output that must return locally | Model both | Download may erase kernel speedup |
| Data restricted from uploading | Local CPU | A remote GPU is not a permitted alternative |
| Mixed CPU+GPU stages | Pipeline evaluation | Optimize actual critical path; overlap only if measured |

If the benchmark shows the CPU winning end-to-end, **recommend CPU** even if the GPU is faster in an isolated kernel.

---
