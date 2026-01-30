#!/usr/bin/env python3
"""Submission validation for Week 6 anti-AI workflow.

Validation checks
- Challenge integrity and optional signature
- TTL expiry (with a small grace window)
- Evidence schema basics and artefact hashes
- Report token present in at least one text artefact
- Payload token present in at least one PCAP artefact
- Basic TCP handshake evidence if a TCP token is present

The validator is intentionally strict about hashes and tokens and tolerant about probe outputs.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from anti_ai.challenge import AntiAIChallenge
from anti_ai.pcap_tools import find_payload_token, has_tcp_handshake, parse_pcap


TEXT_EXTENSIONS = {".md", ".txt", ".log", ".json", ".yaml", ".yml"}


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def sha256_file(path: Path) -> str:
    import hashlib

    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    errors: List[str]
    warnings: List[str]


def _load_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("Evidence JSON must be a mapping")
    return data


def _iter_text_files(base_dir: Path, artefacts: List[Dict[str, Any]]) -> Iterable[Path]:
    for a in artefacts:
        p = base_dir / Path(a["path"])
        if p.suffix.lower() in TEXT_EXTENSIONS:
            yield p


def _iter_pcap_files(base_dir: Path, artefacts: List[Dict[str, Any]]) -> Iterable[Path]:
    for a in artefacts:
        p = base_dir / Path(a["path"])
        if p.suffix.lower() == ".pcap":
            yield p


def validate_submission(
    challenge_path: Path,
    evidence_path: Path,
    base_dir: Path,
    secret: Optional[str] = None,
    require_signature: bool = False,
    ignore_expiry: bool = False,
    verbose: bool = False,
) -> ValidationResult:
    errors: List[str] = []
    warnings: List[str] = []

    try:
        challenge = AntiAIChallenge.load_yaml(str(challenge_path))
    except Exception as e:
        return ValidationResult(False, [f"Failed to load challenge: {e}"], [])

    # Integrity and signature checks.
    try:
        challenge.verify_integrity(secret if require_signature else None)
    except Exception as e:
        errors.append(str(e))

    if require_signature and secret is None:
        errors.append("Signature is required but no secret was provided")

    if not ignore_expiry and challenge.is_expired(_utc_now()):
        errors.append("Challenge has expired")

    try:
        evidence = _load_json(evidence_path)
    except Exception as e:
        return ValidationResult(False, errors + [f"Failed to load evidence JSON: {e}"], warnings)

    meta = evidence.get("meta", {})
    if not isinstance(meta, dict):
        errors.append("Evidence meta section is missing or invalid")
        meta = {}

    if int(meta.get("week_id", -1)) != int(challenge.week_id):
        errors.append("Evidence week_id does not match challenge")
    if str(meta.get("student_id", "")) != challenge.student_id:
        errors.append("Evidence student_id does not match challenge")
    if str(meta.get("challenge_id", "")) != challenge.challenge_id:
        errors.append("Evidence challenge_id does not match challenge")

    artefacts = evidence.get("artefacts", [])
    if not isinstance(artefacts, list) or not artefacts:
        errors.append("No artefacts listed in evidence")

    # Hash validation.
    for a in artefacts if isinstance(artefacts, list) else []:
        if not isinstance(a, dict):
            errors.append("Artefact entry is not a mapping")
            continue
        if "path" not in a or "sha256" not in a:
            errors.append("Artefact entry missing path or sha256")
            continue
        rel = Path(str(a["path"]))
        full = (base_dir / rel).resolve()
        if not full.exists():
            errors.append(f"Artefact not found: {rel}")
            continue
        actual = sha256_file(full)
        if str(a["sha256"]) != actual:
            errors.append(f"SHA256 mismatch for artefact: {rel}")

    # Report token check in any text artefact.
    token_found = False
    for p in _iter_text_files(base_dir, artefacts if isinstance(artefacts, list) else []):
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        if challenge.report_token in text:
            token_found = True
            break
    if not token_found:
        errors.append("Report token not found in any text artefact")

    # PCAP payload token check.
    pcap_files = list(_iter_pcap_files(base_dir, artefacts if isinstance(artefacts, list) else []))
    if not pcap_files:
        errors.append("No PCAP artefact provided")
    else:
        any_token = False
        any_tcp = False
        any_udp = False
        any_tcp_handshake = False

        for pcap in pcap_files:
            try:
                packets = parse_pcap(pcap)
            except Exception as e:
                errors.append(f"Failed to parse PCAP {pcap}: {e}")
                continue
            found = find_payload_token(
                packets,
                challenge.payload_token,
                expected_tcp_port=challenge.tcp_port,
                expected_udp_port=challenge.udp_port,
            )
            if found["tcp"] or found["udp"]:
                any_token = True
            if found["tcp"]:
                any_tcp = True
                if has_tcp_handshake(packets, expected_port=challenge.tcp_port):
                    any_tcp_handshake = True
            if found["udp"]:
                any_udp = True

        if not any_token:
            errors.append("Payload token not found in any PCAP payload")
        if any_tcp and not any_tcp_handshake:
            errors.append("TCP payload token found but no TCP handshake was detected")
        if not any_tcp and not any_udp:
            errors.append("No matching TCP or UDP payload token found on expected ports")

    # Probe outputs are warnings only, but we sanity check for obviously empty content.
    probes = evidence.get("probes", {})
    if isinstance(probes, dict) and probes.get("status") != "not_run":
        nat_probe = probes.get("nat_probe", {})
        if isinstance(nat_probe, dict):
            out = str(nat_probe.get("stdout", ""))
            if out and "MASQ" not in out.upper() and "MASQUERADE" not in out.upper():
                warnings.append("NAT probe output does not appear to include MASQUERADE")
        sdn_probe = probes.get("sdn_probe", {})
        if isinstance(sdn_probe, dict):
            out = str(sdn_probe.get("stdout", "")).strip()
            if out and not re.fullmatch(r"\d+", out):
                warnings.append("SDN probe output is not a simple integer")

    return ValidationResult(ok=len(errors) == 0, errors=errors, warnings=warnings)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Validate Week 6 anti-AI submission")
    p.add_argument("--challenge", required=True, help="Challenge YAML path")
    p.add_argument("--evidence", required=True, help="Evidence JSON path")
    p.add_argument("--base-dir", default=".", help="Base directory for artefact paths")
    p.add_argument(
        "--require-signature",
        action="store_true",
        help="Require a signed challenge and verify it using a secret",
    )
    p.add_argument(
        "--secret-env",
        default="ANTI_AI_SECRET",
        help="Environment variable name that holds the signing secret",
    )
    p.add_argument(
        "--ignore-expiry",
        action="store_true",
        help="Ignore TTL expiry (instructor use only)",
    )
    p.add_argument("--verbose", action="store_true", help="Verbose output")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    secret = os.environ.get(args.secret_env)

    result = validate_submission(
        challenge_path=Path(args.challenge),
        evidence_path=Path(args.evidence),
        base_dir=Path(args.base_dir),
        secret=secret,
        require_signature=bool(args.require_signature),
        ignore_expiry=bool(args.ignore_expiry),
        verbose=bool(args.verbose),
    )

    if result.ok:
        print("PASS")
    else:
        print("FAIL")

    if result.warnings:
        print("Warnings:")
        for w in result.warnings:
            print(f"- {w}")

    if result.errors:
        print("Errors:")
        for e in result.errors:
            print(f"- {e}")

    return 0 if result.ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
