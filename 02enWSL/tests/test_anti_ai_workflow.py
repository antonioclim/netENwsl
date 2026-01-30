"""Anti‑AI workflow tests for Week 2.

These tests are designed to run without Docker. They exercise the core workflow:
- challenge generation (signed)
- proof runner (TCP and UDP reference exercises)
- evidence collection
- submission validation

The aim is to ensure the anti‑AI tooling remains functional as the kit evolves.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.smoke
def test_end_to_end_signed_challenge(tmp_path: Path) -> None:
    env = os.environ.copy()
    env["ANTI_AI_MASTER_KEY"] = "unit-test-master-key"

    challenge_path = tmp_path / "challenge.yaml"
    proof_dir = tmp_path / "proof"
    evidence_path = tmp_path / "evidence.json"

    # 1) Generate challenge
    gen = subprocess.run(
        [sys.executable, "-m", "anti_ai.challenge_generator",
         "--student-id", "TEST123",
         "--out", str(challenge_path),
         "--ttl-seconds", "3600"],
        cwd=str(PROJECT_ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert gen.returncode == 0, gen.stdout + gen.stderr
    assert challenge_path.exists()

    # 2) Run proof runner (uses reference exercises)
    proof = subprocess.run(
        [sys.executable, "-m", "anti_ai.proof_runner",
         "--challenge", str(challenge_path),
         "--out-dir", str(proof_dir),
         "--timeout", "8"],
        cwd=str(PROJECT_ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert proof.returncode == 0, proof.stdout + proof.stderr
    assert (proof_dir / "tcp_client.txt").exists()
    assert (proof_dir / "udp_client.txt").exists()

    # 3) Collect evidence
    ev = subprocess.run(
        [sys.executable, "-m", "anti_ai.evidence_collector",
         "--challenge", str(challenge_path),
         "--base-dir", str(tmp_path),
         "--artefact", "proof/tcp_client.txt",
         "--artefact", "proof/udp_client.txt",
         "--artefact", "proof/tcp_server.txt",
         "--artefact", "proof/udp_server.txt",
         "--artefact", "proof/proof_summary.json",
         "--output", str(evidence_path)],
        cwd=str(PROJECT_ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert ev.returncode == 0, ev.stdout + ev.stderr
    assert evidence_path.exists()

    # 4) Validate
    val = subprocess.run(
        [sys.executable, "-m", "anti_ai.submission_validator",
         "--challenge", str(challenge_path),
         "--evidence", str(evidence_path),
         "--base-dir", str(tmp_path),
         "--verbose"],
        cwd=str(PROJECT_ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert val.returncode == 0, val.stdout + val.stderr
    assert "PASS" in val.stdout


@pytest.mark.slow
def test_validator_rejects_tampered_log(tmp_path: Path) -> None:
    env = os.environ.copy()
    env["ANTI_AI_MASTER_KEY"] = "unit-test-master-key"

    challenge_path = tmp_path / "challenge.yaml"
    proof_dir = tmp_path / "proof"
    evidence_path = tmp_path / "evidence.json"

    # Generate challenge and proof.
    subprocess.check_call(
        [sys.executable, "-m", "anti_ai.challenge_generator",
         "--student-id", "TEST999",
         "--out", str(challenge_path),
         "--ttl-seconds", "3600"],
        cwd=str(PROJECT_ROOT),
        env=env,
    )

    subprocess.check_call(
        [sys.executable, "-m", "anti_ai.proof_runner",
         "--challenge", str(challenge_path),
         "--out-dir", str(proof_dir),
         "--timeout", "8"],
        cwd=str(PROJECT_ROOT),
        env=env,
    )

    # Tamper with the TCP client log.
    tcp_log = proof_dir / "tcp_client.txt"
    tcp_log.write_text("OK: NOTHING TO SEE HERE\n", encoding="utf-8")

    # Collect evidence (hashes now match the tampered file).
    subprocess.check_call(
        [sys.executable, "-m", "anti_ai.evidence_collector",
         "--challenge", str(challenge_path),
         "--base-dir", str(tmp_path),
         "--artefact", "proof/tcp_client.txt",
         "--artefact", "proof/udp_client.txt",
         "--artefact", "proof/tcp_server.txt",
         "--artefact", "proof/udp_server.txt",
         "--artefact", "proof/proof_summary.json",
         "--output", str(evidence_path)],
        cwd=str(PROJECT_ROOT),
        env=env,
    )

    # Validation should fail because the payload token is missing.
    val = subprocess.run(
        [sys.executable, "-m", "anti_ai.submission_validator",
         "--challenge", str(challenge_path),
         "--evidence", str(evidence_path),
         "--base-dir", str(tmp_path)],
        cwd=str(PROJECT_ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert val.returncode != 0
    assert "payload token" in (val.stdout + val.stderr).lower()
