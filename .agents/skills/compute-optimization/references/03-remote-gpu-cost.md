## 3. Remote Colab GPU: mandatory end-to-end cost model

**There are two distinct data-transfer boundaries.**

```text
LOCAL MACHINE                     REMOTE COLAB VM                    GPU
input -> encode/pack -> [network upload] -> decode -> [H2D] -> kernels
  ^                                   |                      |        |
  +<- decode <- [network download] <- encode <- [D2H] <- result     |
            setup/auth/provision/install/compile are additional costs
```

For a **single cold job**, first use the additive model as a safe approximation:

```text
T_colab_total = T_auth/provision + T_env_install + T_code_transfer
              + T_local_pack + T_network_upload + T_remote_unpack
              + T_preprocess + T_H2D + T_GPU_compute + T_D2H
              + T_remote_pack + T_network_download + T_local_unpack
              + T_result_validation + T_cleanup + T_failure_expected
```

- `T_failure_expected` is an explicitly estimated/reported retry cost when quotas, resets, or disconnections materially affect real usage. Do not silently assume 100% uptime.
- If transfers and computation truly overlap, substitute **measured pipeline critical-path time** for the affected additive terms; never subtract hypothetical overlap.
- Do not count network upload as H2D; the CLI sends data to the **Colab host**, not directly to VRAM.
- Note the *source of every large dataset*. If it already resides in GCS/Drive/remote storage, measure its **remote fetch** rather than pretending a local upload occurs. Conversely, a local-only dataset has an unavoidable transfer unless remote regeneration/compression changes the contract.
- Cold one-shot and persistent-session estimates are different. Reusing a runtime can amortize provisioning/install/JIT, but compute units and idle-session consumption are costs too.
- Report actual wire bytes, raw bytes, serialization time, upload/download wall time, and achieved network throughput. Network bandwidth/RTT is variable; never use peak GPU memory bandwidth for network estimates.

### 3.1 Break-even decision

Suppose `N` same-size jobs run on one persistent session. Let:

- `F` = measured one-time Colab startup + dependency setup + initial compile (s)
- `C` = measured local CPU end-to-end time **per job** (s)
- `G` = measured recurring remote path **per job**, including network, copies, compute, and return (s)

Then the remote GPU can win **only if** `F + N·G < N·C` (ignoring non-time costs). If `C <= G`, reuse cannot break even; if `C > G`, need `N > F/(C-G)`.

**Illustrative numbers, not measurements:** `F=60 s`, `C=80 s`, `G=75 s` imply **more than 12 jobs** are needed; one job is much slower remotely despite fast GPU kernels. Note that uploads/results may not be necessary on every iteration if the workload allows state reuse; measure that alternate design separately.

**Mandatory gate before a substantial remote upload:** estimate transfer bytes and benchmark a **small representative upload + download**. If optimistic bounds already exceed the user's CPU time target, do not provision a larger GPU just to test a kernel. If workload size or reuse changes materially, rerun the gate.

### 3.2 High-payoff data-movement strategies (ranked)

1. **Do less remote transfer.** Keep reusable input/parameters/model and intermediate tensors in Colab RAM/VRAM across operations; return a compact result, not full intermediate arrays. Aggregate/filter/reduce remotely when semantics permit.
2. **Move compute to the data.** If the dataset is already in accessible cloud storage, compare staging it directly inside Colab vs a local→Colab detour. For local data, compare sending code/parameters and regenerating data remotely only if regeneration is equivalent and allowed.
3. **Measure compression end to end.** Compression helps only if saved transfer time exceeds CPU compression/decompression and changed runtime costs. Test zstd/lz4/columnar compression, FP16/int packing only when lossless or accuracy-compliant.
4. **Batch and coalesce.** One large upload is often better than thousands of tiny transfers; package small files only when archive packing/unpacking is worth it. Use explicit integrity checks.
5. **Avoid repeated host↔device round trips.** Create tensors directly on the GPU; keep the computational graph on GPU; fuse intermediates; copy back only final output; avoid `.item()`, `.cpu()`, Python branching on CUDA tensor values, and logging full tensors in inner loops.
6. **Overlap when supported and measured.** Pinned memory plus async H2D/D2H and appropriately independent streams can overlap copies and compute for chunked pipelines. Pinned memory consumes constrained host resources; use bounded staging buffers. No presumed overlap for a dependent single kernel.
7. **Streaming/chunking for oversized data.** Pipeline disk/network→CPU→GPU→CPU→output with bounded buffers, while preserving ordering/correctness. Measure pipeline throughput and peak RAM/VRAM; beware chunk boundary conditions.
8. **Keep results small.** Download only needed metrics/artifacts; compress them if justified. Avoid printing multi-MB tensors to CLI stdout (this is another return channel).
9. **Do not mistake Drive mounting for high-throughput local storage.** Benchmark read/write performance; stage hot data on the VM's local disk if permitted and practical. Colab VM files are ephemeral; save irreplaceable outputs before stopping.

### 3.3 GPU hardware-selection rule

Colab CLI's documented GPU request values include `T4`, `L4`, `G4`, `A100`, `H100`; **availability and entitlement vary**. Confirm the device actually assigned, compute capability, VRAM, and library support after provisioning. Compare candidates by *end-to-end effective rate* for real shapes, not theoretical TFLOPs alone. A faster GPU can be useless if the transfer path dominates or is ineligible.

Never assume Blackwell-specific FP4, TMA, or FlashAttention-4 features are available on the GPUs above. Apply research by principle and by **supported architecture**, not by paper speedup headline.

---
