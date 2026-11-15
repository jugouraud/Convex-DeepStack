"""Executed with `colab exec -f`: stage an uploaded source snapshot, then run UCI studies."""

import hashlib
import subprocess
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

PROJECT = Path("/content/cds_uci_job")
OUTPUT = PROJECT / "outputs" / "uci"

with ZipFile("/content/cds_uci_source.zip") as bundle:
    bundle.extractall(PROJECT)
(PROJECT / "source_snapshot_sha256.txt").write_text(
    hashlib.sha256(Path("/content/cds_uci_source.zip").read_bytes()).hexdigest()
)

subprocess.run(
    [sys.executable, "-m", "pip", "install", "-q", "-e", f"{PROJECT}[experiments]"],
    check=True,
    timeout=900,
)
sys.path.insert(0, str(PROJECT))

from experiments.uci_runner import run_uci_experiment  # noqa: E402

run_uci_experiment(PROJECT / "config.toml", OUTPUT)
with ZipFile("/content/cds_uci_results.zip", "w", ZIP_DEFLATED) as archive:
    for file in sorted(OUTPUT.rglob("*")):
        if file.is_file():
            archive.write(file, arcname=file.relative_to(OUTPUT))
