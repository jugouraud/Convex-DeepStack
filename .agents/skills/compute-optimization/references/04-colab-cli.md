## 4. Colab CLI operating procedure (current documented interface)

**Platform note:** The official repository currently documents Linux/macOS support for the CLI, not native Windows support. Verify the installed `colab --help` and version because syntax and quotas evolve. Do not assume credentials are present.

```bash
# One-time, local: choose ONE installer; only if the tool is not already installed
uv tool install google-colab-cli
# or: python -m pip install google-colab-cli

colab --help

# Persistent, named session is preferable for expensive repeated jobs / datasets
colab new -s perfbench --gpu T4
colab status -s perfbench

# Install only the actual project's dependencies, if required
colab install -s perfbench -r requirements.txt

# Source script is sent automatically by 'exec -f': no separate code upload needed
colab exec -s perfbench -f gpu_probe.py

# Upload data explicitly. CLI upload targets remote filesystem, NOT VRAM.
colab upload -s perfbench ./input.bin /content/input.bin
colab exec -s perfbench -f gpu_workload.py
colab download -s perfbench /content/result.json ./result.json

# Verify output exists locally AND passes correctness checks before teardown
colab stop -s perfbench
```

**Do not assume** these illustrative paths exist: create `/content/...` output in the script; use the actual input location in the script. For many input files, verify whether your installed CLI supports directory operations; otherwise package into a validated archive and transfer the archive. Inspect `colab upload --help` and `colab download --help` before transferring large amounts.

The CLI also documents `colab run --gpu T4 script.py` for ephemeral one-shot jobs. Prefer it when setup/data are small, output retrieval works for the selected workflow, and a fresh runtime is appropriate; for large data or repeated jobs, a named persistent session is typically the first candidate to benchmark.

**Operational checks:**

- Before upload: data classification/permissions, free disk, file size/hash, compressed and uncompressed sizes, expected transfer time.
- After provisioning: log `colab status`, `nvidia-smi` if available, `torch.cuda.get_device_name(0)` and VRAM, available package versions.
- After upload: verify remote file size/hash and decode / input count.
- After execution: save output and timing artifact; validate before cleanup.
- Finally: stop unused sessions and retrieve checkpoints. Do not claim Colab GPUs are available solely because the CLI supports requesting them.
- If GPU allocation/quota, permissions, security policy, or tools fail, **fall back to optimized local CPU** and document the obstacle. No bypassing access or authentication controls.

### 4.1 Example remote probe (`gpu_probe.py`)

```python
import json
import platform
import time

import torch

info = {
    "python_platform": platform.platform(),
    "torch": torch.__version__,
    "cuda_available": torch.cuda.is_available(),
}
if torch.cuda.is_available():
    info["gpu"] = torch.cuda.get_device_name(0)
    info["capability"] = list(torch.cuda.get_device_capability(0))
    info["vram_bytes"] = torch.cuda.get_device_properties(0).total_memory
    x = torch.ones((2048, 2048), device="cuda")
    # Warmup excludes one-time context creation from the steady-state sample.
    for _ in range(5):
        y = x @ x
    torch.cuda.synchronize()
    times = []
    for _ in range(10):
        start = torch.cuda.Event(enable_timing=True)
        end = torch.cuda.Event(enable_timing=True)
        start.record()
        y = x @ x
        end.record()
        torch.cuda.synchronize()
        times.append(start.elapsed_time(end))  # GPU elapsed milliseconds
    info["matmul_device_ms_samples"] = times
print(json.dumps(info, indent=2))
```

This probe describes the remote GPU and a **device-only synthetic matmul**, not the user's application speed and not a Colab-versus-local result. The real workload benchmark must separately measure whole-job wall clock and transfer phases.

### 4.2 Benchmark transfer + compute separately

Capture a local monotonic timer around each CLI call (`time.perf_counter()` in a wrapper, or `/usr/bin/time -p` where available). Inside the remote script, record `read/decode`, `H2D`, `GPU kernel`, `D2H`, and `encode/write` using appropriate CUDA synchronization or events. CPU wall clocks are for pipeline phases and CUDA events are for correctly scoped device timings; do not mix event milliseconds with network wall-clock seconds. If profiler support is limited, this decomposition still provides a useful lower bound and identifies the dominant boundary.

**Recommended log schema** (one line per input shape, seed, repetition, hardware and revision):

```json
{
  "case_id": "representative-large",
  "backend": "colab-gpu",
  "gpu": "DETECTED_AT_RUNTIME",
  "cold": true,
  "input_bytes_raw": null,
  "input_bytes_sent": null,
  "result_bytes_downloaded": null,
  "provision_s": null,
  "install_compile_s": null,
  "upload_s": null,
  "remote_decode_s": null,
  "h2d_s": null,
  "gpu_compute_s": null,
  "d2h_s": null,
  "remote_encode_s": null,
  "download_s": null,
  "total_wall_s": null,
  "correct": null
}
```

Use `null` for not measured; never insert invented zeros. Include unit labels. Use a unique case ID and record environment + input fingerprints separately.

---
