#!/usr/bin/env python3
"""Submission validator for Week 3.

The validator checks that a submission contains evidence that cannot plausibly be
produced by a language model alone. It does not aim to prohibit AI usage. It
aims to enforce that the student must execute real networking tasks.

Inputs:
- a challenge YAML file (generated per student)
- an evidence JSON file (hashes and metadata)
- the referenced artefacts on disk (PCAP files and a short report)

Checks:
- challenge integrity (SHA-256 and optionally HMAC)
- challenge expiry window
- evidence structure and artefact hashes
- presence of the report token in the report
- presence of the payload token in the three required PCAPs:
    * UDP broadcast capture
    * UDP multicast capture
    * TCP tunnel capture (token in payload and basic handshake observed)

Exit codes:
- 0: PASS
- 1: FAIL (validation error)
- 2: FAIL (missing inputs)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from anti_ai.challenge import load_challenge, verify_integrity
from anti_ai.pcap_tools import pcap_contains_token


@dataclass(frozen=True, slots=True)
class ValidationResult:
    ok: bool
    messages: list[str]
    details: dict[str, Any]


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _load_evidence(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Evidence JSON is not a mapping")
    return data


def _hash_file(path: Path) -> str:
    import hashlib

    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _find_artefact(evidence: dict[str, Any], rel_path: str) -> dict[str, Any] | None:
    for a in evidence.get("artefacts", []):
        if isinstance(a, dict) and a.get("path") == rel_path:
            return a
    return None


def validate(
    *,
    challenge_path: Path,
    evidence_path: Path,
    base_dir: Path,
    verbose: bool,
    ignore_expiry: bool,
    require_hmac: bool,
) -> ValidationResult:
    messages: list[str] = []
    details: dict[str, Any] = {"pcap": {}}

    if not challenge_path.exists():
        return ValidationResult(False, [f"Missing challenge file: {challenge_path}"], details)
    if not evidence_path.exists():
        return ValidationResult(False, [f"Missing evidence file: {evidence_path}"], details)

    challenge = load_challenge(challenge_path)
    hmac_key = os.environ.get("ANTI_AI_HMAC_KEY")

    ok, msg = verify_integrity(challenge, hmac_key)
    if not ok:
        messages.append("FAIL: " + msg)
        return ValidationResult(False, messages, details)
    messages.append("OK: " + msg)

    if require_hmac and not hmac_key:
        messages.append("FAIL: HMAC is required but ANTI_AI_HMAC_KEY is not set")
        return ValidationResult(False, messages, details)

    # Expiry check
    if not ignore_expiry:
        now = _utc_now()
        expires = challenge.expires_at()
        if now > expires:
            messages.append(
                f"FAIL: Challenge expired (now={now.isoformat()}, expires={expires.isoformat()})"
            )
            return ValidationResult(False, messages, details)
        messages.append(f"OK: Challenge is within validity window (expires at {expires.isoformat()})")
    else:
        messages.append("WARN: Expiry check is disabled (--ignore-expiry)")

    evidence = _load_evidence(evidence_path)
    meta = evidence.get("meta") or {}
    if str(meta.get("student_id", "")) != challenge.student_id:
        messages.append("FAIL: Evidence student_id does not match the challenge")
        return ValidationResult(False, messages, details)
    if int(meta.get("week", -1)) != challenge.week:
        messages.append("FAIL: Evidence week does not match the challenge")
        return ValidationResult(False, messages, details)

    # Required artefacts (paths relative to base_dir)
    sid = challenge.student_id
    required = {
        "report": f"artifacts/anti_ai/w03_report_{sid}.md",
        "broadcast": f"artifacts/anti_ai/w03_broadcast_{sid}.pcap",
        "multicast": f"artifacts/anti_ai/w03_multicast_{sid}.pcap",
        "tunnel": f"artifacts/anti_ai/w03_tunnel_{sid}.pcap",
    }

    missing_refs = [k for k, p in required.items() if _find_artefact(evidence, p) is None]
    if missing_refs:
        messages.append("FAIL: Evidence is missing required artefact references: " + ", ".join(missing_refs))
        messages.append("Expected paths:")
        for k, p in required.items():
            messages.append(f"  - {k}: {p}")
        return ValidationResult(False, messages, details)

    # Hash verification
    for key, rel in required.items():
        art = _find_artefact(evidence, rel)
        assert art is not None
        file_path = (base_dir / rel).resolve()
        if not file_path.exists():
            messages.append(f"FAIL: Artefact file is missing on disk: {rel}")
            return ValidationResult(False, messages, details)

        expected = str(art.get("sha256", ""))
        actual = _hash_file(file_path)
        if expected != actual:
            messages.append(f"FAIL: SHA-256 mismatch for {rel}")
            if verbose:
                messages.append(f"  expected: {expected}")
                messages.append(f"  actual:   {actual}")
            return ValidationResult(False, messages, details)
        messages.append(f"OK: SHA-256 verified for {rel}")

    # Report token check
    report_path = (base_dir / required["report"]).resolve()
    report_text = _read_text(report_path)
    if challenge.report_token not in report_text:
        messages.append("FAIL: Report token was not found in the report file")
        messages.append(f"Expected token: {challenge.report_token}")
        return ValidationResult(False, messages, details)
    messages.append("OK: Report token found in report")

    # PCAP checks
    # Broadcast: UDP token on broadcast_port
    bc_path = (base_dir / required["broadcast"]).resolve()
    found, bc_details = pcap_contains_token(
        bc_path,
        challenge.payload_token,
        proto="udp",
        port=challenge.broadcast_port,
    )
    details["pcap"]["broadcast"] = bc_details
    if not found:
        messages.append("FAIL: Payload token not found in broadcast PCAP")
        messages.append(f"Expected UDP port: {challenge.broadcast_port}")
        return ValidationResult(False, messages, details)
    messages.append("OK: Payload token found in broadcast PCAP")

    # Multicast: UDP token on multicast_port and destination group if parsed
    mc_path = (base_dir / required["multicast"]).resolve()
    found, mc_details = pcap_contains_token(
        mc_path,
        challenge.payload_token,
        proto="udp",
        port=challenge.multicast_port,
        dst_ip=challenge.multicast_group,
    )
    details["pcap"]["multicast"] = mc_details
    if not found:
        # Fallback: do not require destination IP if capture did not preserve it as expected
        found2, mc_details2 = pcap_contains_token(
            mc_path,
            challenge.payload_token,
            proto="udp",
            port=challenge.multicast_port,
        )
        details["pcap"]["multicast_fallback"] = mc_details2
        if not found2:
            messages.append("FAIL: Payload token not found in multicast PCAP")
            messages.append(f"Expected UDP port: {challenge.multicast_port}")
            messages.append(f"Expected group:    {challenge.multicast_group} (best effort)")
            return ValidationResult(False, messages, details)
    messages.append("OK: Payload token found in multicast PCAP")

    # Tunnel: TCP token and basic handshake
    tn_path = (base_dir / required["tunnel"]).resolve()
    found, tn_details = pcap_contains_token(
        tn_path,
        challenge.payload_token,
        proto="tcp",
        port=challenge.tunnel_listen_port,
        require_handshake=True,
    )
    details["pcap"]["tunnel"] = tn_details
    if not found:
        # Fallback to common echo server port, in case capture was done on the target side
        found2, tn_details2 = pcap_contains_token(
            tn_path,
            challenge.payload_token,
            proto="tcp",
            port=8080,
            require_handshake=True,
        )
        details["pcap"]["tunnel_fallback"] = tn_details2
        if not found2:
            messages.append("FAIL: Payload token not found in tunnel PCAP")
            messages.append(f"Expected TCP port: {challenge.tunnel_listen_port} (or 8080 fallback)")
            return ValidationResult(False, messages, details)

    handshake_ok = bool(tn_details.get("handshake_ok")) or bool(details.get("pcap", {}).get("tunnel_fallback", {}).get("handshake_ok"))
    if not handshake_ok:
        messages.append("FAIL: TCP handshake was not detected in tunnel PCAP")
        messages.append("Capture might have started too late. Re-capture including connection setup.")
        return ValidationResult(False, messages, details)

    messages.append("OK: Payload token and TCP handshake found in tunnel PCAP")

    return ValidationResult(True, messages, details)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Validate a Week 3 submission (anti-AI)")
    p.add_argument("--challenge", required=True, help="Challenge YAML file")
    p.add_argument("--evidence", required=True, help="Evidence JSON file")
    p.add_argument("--base-dir", default=".", help="Base directory for relative paths (default: .)")
    p.add_argument("--verbose", action="store_true", help="Print extra details on failures")
    p.add_argument(
        "--ignore-expiry",
        action="store_true",
        help="Ignore the challenge expiry window (intended for staff re-grading)",
    )
    p.add_argument(
        "--require-hmac",
        action="store_true",
        help="Require ANTI_AI_HMAC_KEY and verify the HMAC tag",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    result = validate(
        challenge_path=Path(args.challenge),
        evidence_path=Path(args.evidence),
        base_dir=Path(args.base_dir),
        verbose=bool(args.verbose),
        ignore_expiry=bool(args.ignore_expiry),
        require_hmac=bool(args.require_hmac),
    )

    for m in result.messages:
        print(m)

    if args.verbose:
        # Do not dump tokens, but details are safe (paths and counts)
        print("")
        print("Details (debug):")
        print(json.dumps(result.details, indent=2, sort_keys=True))

    return 0 if result.ok else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
