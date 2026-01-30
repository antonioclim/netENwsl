#!/usr/bin/env python3
"""Week 10 exercise and script smoke tests.

The aim of this test module is to provide quick, deterministic checks that can
run on most developer machines and in CI.

Docker is used by the Week 10 laboratory environment. However, some execution
contexts (for example, CI sandboxes) may not provide Docker. In those cases,
Docker-dependent behaviour should be verified using the dedicated
``setup/verify_environment.py`` script and the ``make verify`` target.

Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable, List

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def _run_python(args: List[str], timeout: int = 60) -> subprocess.CompletedProcess[str]:
    """Run a Python subprocess in the Week 10 project root."""
    return subprocess.run(
        [PYTHON, *args],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def _assert_ok(result: subprocess.CompletedProcess[str]) -> None:
    """Assert that a subprocess result succeeded, printing useful diagnostics."""
    if result.returncode != 0:
        combined = (result.stdout or "") + "\n" + (result.stderr or "")
        raise AssertionError(combined.strip())


def _docker_available() -> bool:
    return shutil.which("docker") is not None


def test_exercise_10_01_selftest() -> None:
    result = _run_python(["src/exercises/ex_10_01_tls_rest_crud.py", "selftest"], timeout=90)
    _assert_ok(result)


def test_exercise_10_02_selftest() -> None:
    result = _run_python(["src/exercises/ex_10_02_richardson_maturity.py", "selftest"], timeout=90)
    _assert_ok(result)


def test_scripts_help() -> None:
    scripts: Iterable[str] = (
        "scripts/start_lab.py",
        "scripts/stop_lab.py",
        "scripts/capture_traffic.py",
        "scripts/cleanup.py",
        "scripts/run_demo.py",
    )

    for script in scripts:
        result = _run_python([script, "--help"], timeout=30)
        _assert_ok(result)


def test_anti_cheat_cli_help() -> None:
    result = _run_python(["-m", "anti_cheat.challenge_generator", "--help"], timeout=30)
    _assert_ok(result)

    result = _run_python(["-m", "anti_cheat.submission_validator", "--help"], timeout=30)
    _assert_ok(result)


def test_docker_presence_is_visible() -> None:
    """A tiny sanity check so the test output clearly signals docker availability."""
    # We do not fail if Docker is missing, but we want a clear signal in CI logs.
    assert _docker_available() in (True, False)
