## 10. Verified references and further reading

**Official operational and profiling documentation**

- **[D0] Colab CLI** (official Google Colab repository, checked 2026-11-13): https://github.com/googlecolab/google-colab-cli — commands, supported accelerators, session lifecycle, data file upload/download, platform constraints. Announcement: https://developers.googleblog.com/en/introducing-the-google-colab-cli/ (2026-06-05).
- **[D1] Roofline model** — Lawrence Berkeley National Laboratory: https://amcr.lbl.gov/departments/computer-science-department/ppan/roofline-performance-model/ ; NERSC: https://docs.nersc.gov/tools/performance/roofline/
- **[D2] CUDA C++ Best Practices Guide** — NVIDIA, chapter on minimizing H2D/D2H transfers, pinned memory and asynchronous overlap: https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/
- **[D3] PyTorch `torch.compile` compile-time guidance** (updated 2026-07-27): https://docs.pytorch.org/docs/main/user_guide/torch_compiler/compile/programming_model.reducing_compile_time.html ; profiler: https://docs.pytorch.org/docs/main/user_guide/torch_compiler/torch.compiler_profiling_torch_compile.html
- **[D4] PyTorch Performance Tuning Guide** — GPU synchronization, tensor cores, CUDA Graphs, CPU NUMA, OpenMP: https://docs.pytorch.org/tutorials/recipes/recipes/tuning_guide.html
- **[D5] Intel Top-Down Microarchitecture Analysis Method** — VTune 2024 cookbook: https://www.intel.com/content/www/us/en/docs/vtune-profiler/cookbook/2024-2/top-down-microarchitecture-analysis-method.html
- **[D6] PyTorch benchmark utilities** — careful microbenchmark blocking / accelerator timing: https://docs.pytorch.org/docs/main/utils/benchmark.html
- **[D7] Triton language and tutorials:** https://triton-lang.org/
- **[D8] LLVM BOLT background:** https://github.com/llvm/llvm-project/tree/main/bolt

**Research / recent implementations**

- **[R1]** Shah et al., *FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision*, NeurIPS 2024: https://papers.nips.cc/paper_files/paper/2024/hash/7ede97c3e082c6df10a8d6103a2eebd2-Abstract-Conference.html
- **[R2]** Wang et al., *TileLang: A Composable Tiled Programming Model for AI Systems*, arXiv preprint (2025): https://arxiv.org/abs/2504.17577
- **[R3]** *ProSpec: Profile-guided Specialization for GPU Kernels*, Information and Software Technology 188, 2025: https://doi.org/10.1016/j.infsof.2025.107901
- **[R4]** Zadouri et al., *FlashAttention-4: Algorithm and Kernel Pipelining Co-Design for Asymmetric Hardware Scaling*, arXiv preprint (2026-03): https://arxiv.org/abs/2603.05451
- **[R5]** Soi et al., *Optimal Software Pipelining and Warp Specialization for Tensor Core GPUs*, OSDI 2026: https://research.nvidia.com/publication/2026-07_optimal-software-pipelining-and-warp-specialization-tensor-core-gpus
- **[R6]** PyTorch engineering report, *From Minutes to Seconds: LLM-Guided Autotuning for Helion Kernels* (2026-06): https://pytorch.org/blog/from-minutes-to-seconds-llm-guided-autotuning-for-helion-kernels/
- **[R7]** PyTorch engineering report, *Fast by Default: Compile-Time Heuristics for Helion Kernels* (2026-11-12): https://pytorch.org/blog/fast-by-default-compile-time-heuristics-for-helion-kernels/
- **[R8]** Agarwal et al., *How Much of a Real Workload Can LLM-Generated GPU Kernels Actually Reach?*, arXiv preprint (2026-09): https://arxiv.org/abs/2609.21058
- **[R9]** Muscas, *CPU Optimization Techniques for Compiled Languages in Scientific Computing*, INAF technical report (2026-03): https://doi.org/10.20371/INAF/TechRep/376

**Recency rule:** Before using a new compiler/library feature, check its documentation and the installed versions. These sources capture the literature/implementations known on **2026-11-13**; new research may supersede their quantitative claims. Treat preprints, engineering blogs, and production tool documentation according to their evidence status, not as interchangeable peer-reviewed evidence.

---

### Final operating maxim

**The optimal accelerator is the one that delivers the fastest *correct answer at the point of use*.** For Colab CLI, the computation is only one term in that answer. Start with the CPU, reduce work and movement, measure both transfer boundaries, and choose a remote GPU only when the whole-job evidence supports it.
