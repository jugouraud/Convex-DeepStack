"""Colab CLI invocation, recoverable failure, and atomic local progress contracts."""

import io
import json
from zipfile import ZipFile

import pytest

from scripts import run_uci_colab as launcher


def test_progress_events_are_reflected_locally(monkeypatch, tmp_path):
    class FakeProcess:
        stdout = io.StringIO(
            'startup\n'
            '@@CDS_STATUS@@{"state":"running","completed_trials":1,"total_trials":2}\n'
            '@@CDS_STATUS@@{"state":"running","completed_trials":2,"total_trials":2}\n'
        )
        returncode = 0

        def poll(self):
            return 0

        def wait(self, timeout):
            return 0

    monkeypatch.setattr(launcher.subprocess, "Popen", lambda *a, **kw: FakeProcess())
    status = tmp_path / "status.json"
    launcher._execute_and_monitor(["colab", "exec"], status, session="test", timeout=5)
    assert json.loads(status.read_text())["completed_trials"] == 2
    assert list(tmp_path.glob(".status-*")) == []


def test_archive_rejects_parent_directory_escape(tmp_path):
    archive = tmp_path / "results.zip"
    with ZipFile(archive, "w") as bundle:
        bundle.writestr("../outside.txt", "unsafe")
    with pytest.raises(ValueError, match="archive path"):
        launcher._unpack_results(archive, tmp_path)
    assert not (tmp_path.parent / "outside.txt").exists()


def test_submit_download_and_stop_even_on_remote_error(monkeypatch, tmp_path):
    monkeypatch.setattr(launcher, "REPO", tmp_path)
    monkeypatch.setattr(launcher.shutil, "which", lambda name: "/usr/bin/colab")
    config = tmp_path / "config.toml"
    config.write_text('[colab]\nsession="test-uci"\noutput_dir="outputs/uci"\n')
    commands = []

    def fake_call(command, *, timeout=600):
        commands.append(command)
        if command[1] == "download":
            with ZipFile(command[-1], "w") as bundle:
                for name in (
                    "manifest.json", "uci_control_sweep_results.csv",
                    "uci_control_sweep_best_by_validation.csv", "uci_control_sweep_summary.csv",
                ):
                    bundle.writestr(name, "{}")

    def fake_archive(archive, config_path):
        with ZipFile(archive, "w") as bundle:
            bundle.writestr("config.toml", config_path.read_bytes())

    monkeypatch.setattr(launcher, "_call", fake_call)
    monkeypatch.setattr(launcher, "_build_archive", fake_archive)
    monkeypatch.setattr(launcher, "_execute_and_monitor", lambda *a, **kw: None)
    launcher.run_colab(config)
    assert [cmd[1] for cmd in commands] == ["new", "upload", "download", "stop"]
    assert (tmp_path / "outputs/uci/manifest.json").exists()
    assert not (tmp_path / "outputs/uci/status.json").exists()

    commands.clear()

    def fail_exec(*args, **kwargs):
        raise TimeoutError("out of time")

    monkeypatch.setattr(launcher, "_execute_and_monitor", fail_exec)
    with pytest.raises(TimeoutError):
        launcher.run_colab(config)
    assert [cmd[1] for cmd in commands] == ["new", "upload", "stop"]
    status = json.loads((tmp_path / "outputs/uci/status.json").read_text())
    assert status["state"] == "failed"
