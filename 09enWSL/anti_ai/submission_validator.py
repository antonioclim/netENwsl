#!/usr/bin/env python3
"""
Submission validator for Week 9 anti-AI workflow.

Validates:
- challenge integrity (SHA-256 and optional HMAC)
- evidence integrity (hashes, file existence, time window)
- token presence:
  - report_token must appear in the report artefact
  - payload_token must appear in TCP payload within the capture (PCAP/PCAPNG),
    filtered to the expected control port from the challenge

Exit codes:
- 0 success
- 1 validation failure
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from anti_ai.challenge import (
    Challenge,
    compute_hmac_sha256,
    compute_integrity_sha256,
    load_challenge,
    parse_utc_iso,
)
from anti_ai.pcap_tools import pcap_contains_token
from anti_ai.evidence_collector import sha256_file
from anti_ai.fingerprint import resolve_project_root


def _fail(msg: str) -> int:
    print(f"FAIL: {msg}")
    return 1


def _ok(msg: str) -> None:
    print(f"OK: {msg}")


def load_json(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("JSON root must be an object")
    return raw


def validate_challenge_integrity(challenge_path: Path, secret_env: str | None) -> tuple[Challenge, int]:
    raw = load_json(challenge_path)

    calc_sha = compute_integrity_sha256(raw)
    stored_sha = ((raw.get("integrity") or {}).get("sha256") or "").strip()

    if not stored_sha:
        return Challenge.from_dict(raw), _fail("Challenge integrity.sha256 missing")
    if calc_sha != stored_sha:
        return Challenge.from_dict(raw), _fail("Challenge integrity.sha256 mismatch")

    # Optional HMAC check
    stored_hmac = ((raw.get("integrity") or {}).get("hmac_sha256") or "").strip()
    if stored_hmac:
        secret = (os.environ.get(secret_env or "ANTI_AI_SECRET") or "").strip()
        if not secret:
            _ok("Challenge HMAC present but secret not provided, skipping HMAC verification")
        else:
            calc_hmac = compute_hmac_sha256(raw, secret)
            if calc_hmac != stored_hmac:
                return Challenge.from_dict(raw), _fail("Challenge integrity.hmac_sha256 mismatch")
            _ok("Challenge HMAC verified")

    _ok("Challenge SHA-256 verified")
    return Challenge.from_dict(raw), 0


def validate_evidence_files(evidence: dict[str, Any], project_root: Path) -> tuple[list[Path], list[Path], int]:
    artefacts = evidence.get("artefacts", []) or []
    if not isinstance(artefacts, list) or not artefacts:
        return [], [], _fail("Evidence artefacts missing or empty")

    report_candidates: list[Path] = []
    pcap_candidates: list[Path] = []

    for a in artefacts:
        if not isinstance(a, dict):
            continue
        p = Path(str(a.get("path", "")))
        sha_expected = str(a.get("sha256", "")).strip()
        if not sha_expected:
            return [], [], _fail(f"Artefact {p} is missing sha256")

        abs_path = p if p.is_absolute() else (project_root / p).resolve()
        if not abs_path.exists():
            return [], [], _fail(f"Missing artefact: {abs_path}")

        sha_actual = sha256_file(abs_path)
        if sha_actual != sha_expected:
            return [], [], _fail(f"SHA mismatch for {abs_path}")

        if abs_path.suffix.lower() in {".pcap", ".pcapng"}:
            pcap_candidates.append(abs_path)
        elif abs_path.suffix.lower() in {".md", ".txt"}:
            report_candidates.append(abs_path)

    if not report_candidates:
        return [], [], _fail("No report artefact (.md or .txt) found in evidence")
    if not pcap_candidates:
        return [], [], _fail("No capture artefact (.pcap or .pcapng) found in evidence")

    _ok(f"Validated hashes for {len(artefacts)} artefacts")
    return report_candidates, pcap_candidates, 0


def report_contains_token(report_path: Path, token: str) -> bool:
    try:
        txt = report_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return False
    return token in txt


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Week 9 anti-AI submission evidence")
    parser.add_argument("--challenge", type=Path, required=True, help="Path to challenge JSON")
    parser.add_argument("--evidence", type=Path, required=True, help="Path to evidence JSON")
    parser.add_argument(
        "--secret-env",
        default="ANTI_AI_SECRET",
        help="Environment variable used for optional HMAC verification",
    )

    args = parser.parse_args()
    project_root = resolve_project_root()

    challenge_path = (project_root / args.challenge).resolve() if not args.challenge.is_absolute() else args.challenge
    evidence_path = (project_root / args.evidence).resolve() if not args.evidence.is_absolute() else args.evidence

    challenge, rc = validate_challenge_integrity(challenge_path, args.secret_env)
    if rc != 0:
        return rc

    evidence = load_json(evidence_path)

    # Ensure evidence matches challenge
    if str(evidence.get("challenge_sha256", "")).strip() != challenge.integrity_sha256:
        return _fail("Evidence challenge_sha256 does not match the challenge file")

    created_at_raw = str(evidence.get("created_at_utc", "")).strip()
    if not created_at_raw:
        return _fail("Evidence created_at_utc missing")

    created_at = parse_utc_iso(created_at_raw)
    if created_at > challenge.expires_at:
        return _fail("Evidence was created after challenge expiry")

    report_paths, pcap_paths, rc = validate_evidence_files(evidence, project_root)
    if rc != 0:
        return rc

    # Report token check (any one report artefact is acceptable)
    if not any(report_contains_token(rp, challenge.report_token) for rp in report_paths):
        return _fail("report_token not found in provided report artefact(s)")
    _ok("Report token found")

    # Payload token check in capture (any one capture is acceptable)
    expected_port = challenge.expected_control_port or None
    if not any(pcap_contains_token(pp, challenge.payload_token, expected_port=expected_port) for pp in pcap_paths):
        port_note = f" on port {expected_port}" if expected_port else ""
        return _fail(f"payload_token not found in capture TCP payload{port_note}")
    _ok("Payload token found in capture")

    print("PASS: Submission evidence validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
