"""Submit UCI studies to the official Colab CLI and mirror progress to local status.json."""

import argparse
import json
import os
import queue
import re
import shutil
import subprocess
import tempfile
import threading
import time
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from zipfile import ZIP_DEFLATED, ZipFile

REPO = Path(__file__).resolve().parents[1]
PROGRESS_PREFIX = "@@CDS_STATUS@@"
REMOTE_ARCHIVE = "/content/cds_uci_source.zip"
REMOTE_RESULTS = "/content/cds_uci_results.zip"


def _write_status(path: Path, state: dict) -> None:
    """Replace one complete status document atomically for readers on this machine."""
    path.parent.mkdir(parents=True, exist_ok=True)
    state = {**state, "updated_at": datetime.now(timezone.utc).isoformat()}
    descriptor, temporary = tempfile.mkstemp(prefix=".status-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(state, handle, sort_keys=True)
            handle.write("\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _call(args: list[str], *, timeout: int = 600) -> None:
    subprocess.run(args, check=True, timeout=timeout, cwd=REPO)


def _execute_and_monitor(args: list[str], status: Path, *, session: str, timeout: int) -> None:
    """Keep reading CLI output even when no progress has occurred recently."""
    proc = subprocess.Popen(
        args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=REPO,
        text=True, encoding="utf-8", errors="replace", bufsize=1,
    )
    events: queue.Queue[str | None] = queue.Queue(maxsize=1000)

    def read_output():
        assert proc.stdout is not None
        for line in proc.stdout:
            events.put(line)
        events.put(None)

    reader = threading.Thread(target=read_output, daemon=True)
    reader.start()
    deadline = time.monotonic() + timeout
    try:
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("Colab experiment exceeded execution_timeout_seconds")
            try:
                line = events.get(timeout=min(1.0, remaining))
            except queue.Empty:
                continue
            if line is None:
                break
            if PROGRESS_PREFIX in line:
                payload = line.split(PROGRESS_PREFIX, 1)[1].strip()
                if len(payload) <= 4096:
                    try:
                        event = json.loads(payload)
                    except json.JSONDecodeError:
                        continue
                    if (isinstance(event, dict) and event.get("state") in
                            {"running", "completed"}):
                        _write_status(status, {"session": session, **event})
                continue
            print(line, end="", flush=True)
        if proc.wait(timeout=10) != 0:
            raise subprocess.CalledProcessError(proc.returncode, args)
    finally:
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=10)
        reader.join(timeout=1)


def _build_archive(archive: Path, config_path: Path) -> None:
    """Stage current source files needed for the remote run (never credentials)."""
    paths = [REPO / "README.md", REPO / "LICENSE", REPO / "pyproject.toml"]
    paths.extend((REPO / "src" / "convex_deepstack").glob("*.py"))
    paths.extend((REPO / "experiments").glob("*.py"))
    with ZipFile(archive, "w", ZIP_DEFLATED) as bundle:
        for file in paths:
            bundle.write(file, arcname=file.relative_to(REPO))
        bundle.write(config_path, arcname="config.toml")
        revision = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True, text=True,
            timeout=10, check=False,
        )
        bundle.writestr("source_revision.txt", revision.stdout.strip() or "unavailable")


def _unpack_results(archive: Path, destination: Path) -> None:
    with ZipFile(archive) as bundle:
        members = bundle.infolist()
        if len(members) > 500 or sum(item.file_size for item in members) > 250_000_000:
            raise ValueError("Colab result archive exceeds size/entry limits")
        for member in members:
            path = PurePosixPath(member.filename)
            if path.is_absolute() or ".." in path.parts or member.is_dir():
                raise ValueError("Invalid Colab result archive path")
            if not member.filename.startswith("plots/") and member.filename not in {
                "manifest.json", "uci_control_sweep_results.csv",
                "uci_control_sweep_best_by_validation.csv", "uci_control_sweep_summary.csv",
            }:
                raise ValueError("Unexpected Colab artifact")
        required = {
            "manifest.json", "uci_control_sweep_results.csv",
            "uci_control_sweep_best_by_validation.csv", "uci_control_sweep_summary.csv",
        }
        if not required <= {item.filename for item in members}:
            raise ValueError("Colab results are missing required output files")
        bundle.extractall(destination)


def run_colab(config_path: Path) -> None:
    if config_path.stat().st_size > 1_000_000:
        raise ValueError("UCI config file exceeds 1 MB")
    if shutil.which("colab") is None:
        raise RuntimeError("Install/authenticate the official google-colab-cli first")
    # Import only the parser, not the training dependencies, before the remote run.
    try:
        import tomllib
    except ModuleNotFoundError:  # Python 3.10
        import tomli as tomllib

    with config_path.open("rb") as handle:
        settings = tomllib.load(handle)["colab"]
    if set(settings) - {"session", "gpu", "high_mem", "output_dir", "execution_timeout_seconds"}:
        raise ValueError("Unknown Colab settings")
    high_mem = settings.get("high_mem", False)
    if type(high_mem) is not bool:
        raise ValueError("Colab high_mem must be a boolean")
    session = settings["session"]
    if not isinstance(session, str) or re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,39}", session) is None:
        raise ValueError("Invalid Colab session name")
    gpu = settings.get("gpu", "")
    if gpu not in ("", "T4", "L4", "G4", "H100", "A100"):
        raise ValueError("Unsupported Colab GPU type")
    timeout = settings.get("execution_timeout_seconds", 86400)
    if type(timeout) is not int or not 60 <= timeout <= 172800:
        raise ValueError("Invalid Colab execution timeout")
    if not isinstance(settings.get("output_dir"), str) or not settings["output_dir"]:
        raise ValueError("Invalid Colab output_dir")
    output = (REPO / settings["output_dir"]).resolve()
    if not output.is_relative_to(REPO):
        raise ValueError("Colab output_dir must stay within the repository")
    output.mkdir(parents=True, exist_ok=True)
    status_path = output / "status.json"
    _write_status(status_path, {"state": "preparing", "session": session, "completed_trials": 0})
    session_created = False
    succeeded = False
    try:
        with tempfile.TemporaryDirectory(prefix="cds-uci-") as folder:
            snapshot = Path(folder) / "source.zip"
            results = Path(folder) / "results.zip"
            _build_archive(snapshot, config_path)
            _write_status(status_path, {"state": "provisioning", "session": session, "completed_trials": 0})
            command = ["colab", "new", "-s", session]
            if gpu:
                command.extend(["--gpu", gpu])
            if high_mem:
                command.append("--high-mem")
            try:
                _call(command, timeout=600)
            except subprocess.TimeoutExpired:
                # Provisioning may have succeeded despite the local timeout.
                session_created = True
                raise
            session_created = True
            _call(["colab", "upload", "-s", session, str(snapshot), REMOTE_ARCHIVE])
            _write_status(status_path, {"state": "running", "session": session, "completed_trials": 0})
            _execute_and_monitor(
                ["colab", "exec", "-s", session, "-f",
                 str(REPO / "scripts" / "uci_colab_remote.py")],
                status_path, session=session, timeout=timeout,
            )
            _call(["colab", "download", "-s", session, REMOTE_RESULTS, str(results)])
            _unpack_results(results, output)
            succeeded = True
    except (OSError, ValueError, subprocess.SubprocessError, TimeoutError) as exc:
        _write_status(status_path, {"state": "failed", "session": session, "reason": type(exc).__name__})
        raise
    finally:
        if session_created:
            try:
                _call(["colab", "stop", "-s", session], timeout=180)
            except (OSError, subprocess.SubprocessError):
                succeeded = False
                _write_status(status_path, {"state": "cleanup_required", "session": session})
                print(f"Warning: could not stop Colab session {session}; stop it manually")
        if succeeded:
            status_path.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Submit the UCI sweep to Google Colab")
    parser.add_argument("--config", type=Path, default=REPO / "experiments/config.toml")
    parser.add_argument("--package-only", type=Path, metavar="DIRECTORY",
                        help="Write source.zip and the remote runner without contacting Colab")
    args = parser.parse_args()
    if args.package_only is not None:
        args.package_only.mkdir(parents=True, exist_ok=True)
        _build_archive(args.package_only / "source.zip", args.config.resolve())
        shutil.copy2(REPO / "scripts/uci_colab_remote.py",
                     args.package_only / "uci_colab_remote.py")
        print(f"Colab package written to {args.package_only.resolve()}")
        return
    run_colab(args.config.resolve())


if __name__ == "__main__":
    main()
