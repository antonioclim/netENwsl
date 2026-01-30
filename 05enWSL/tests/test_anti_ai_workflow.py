#!/usr/bin/env python3
"""
End-to-end tests for the Week 5 anti-AI workflow.

These tests run a small pipeline:
- generate a challenge
- run both homework scripts with the challenge
- collect evidence
- validate the submission

The pipeline is designed to run without Docker and without network access.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _run(cmd: list[str], *, cwd: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )


def test_anti_ai_pipeline(tmp_path: Path) -> None:
    # Prepare environment so the homework scripts can import anti_ai when executed from tmp_path
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT)

    student_id = "TEST123"
    challenge_path = tmp_path / f"challenge_{student_id}.yaml"

    # 1) Generate challenge
    gen = _run(
        [sys.executable, "-m", "anti_ai.challenge_generator", "--student-id", student_id, "--output", str(challenge_path)],
        cwd=tmp_path,
        env=env,
    )
    assert gen.returncode == 0, gen.stderr or gen.stdout
    assert challenge_path.exists()

    # 2) Run homework scripts
    hw1 = PROJECT_ROOT / "homework" / "exercises" / "hw_5_01_subnet_design.py"
    hw2 = PROJECT_ROOT / "homework" / "exercises" / "hw_5_02_ipv6_transition.py"

    r1 = _run([sys.executable, str(hw1), "--challenge", str(challenge_path), "--non-interactive"], cwd=tmp_path, env=env)
    assert r1.returncode == 0, r1.stderr or r1.stdout

    r2 = _run([sys.executable, str(hw2), "--challenge", str(challenge_path), "--non-interactive"], cwd=tmp_path, env=env)
    assert r2.returncode == 0, r2.stderr or r2.stdout

    # Expected outputs (names come from the challenge generator contract)
    subnet_plan = tmp_path / f"subnet_plan_{student_id}.json"
    ipv6_report = tmp_path / f"ipv6_report_{student_id}.json"
    evidence = tmp_path / f"evidence_{student_id}.json"

    assert subnet_plan.exists()
    assert ipv6_report.exists()

    # 3) Collect evidence
    ev = _run(
        [
            sys.executable,
            "-m",
            "anti_ai.evidence_collector",
            "--challenge",
            str(challenge_path),
            "--artefact",
            subnet_plan.name,
            "--artefact",
            ipv6_report.name,
            "--output",
            evidence.name,
            "--base-dir",
            str(tmp_path),
        ],
        cwd=tmp_path,
        env=env,
    )
    assert ev.returncode == 0, ev.stderr or ev.stdout
    assert evidence.exists()

    # 4) Validate
    val = _run(
        [
            sys.executable,
            "-m",
            "anti_ai.submission_validator",
            "--challenge",
            str(challenge_path),
            "--evidence",
            str(evidence),
            "--base-dir",
            str(tmp_path),
            "--ignore-expiry",
        ],
        cwd=tmp_path,
        env=env,
    )
    assert val.returncode == 0, val.stderr or val.stdout
    assert "[PASS]" in val.stdout
