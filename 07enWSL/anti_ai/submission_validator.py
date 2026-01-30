"""Submission validator for the Week 7 anti-AI workflow."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .challenge import load_challenge
from .pcap_tools import PcapFormatError, find_payload_token, has_tcp_handshake, iter_packets


def sha256_file(path: Path) -> str:
    import hashlib

    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class ValidationIssue:
    level: str  # "error" or "warning"
    message: str


def _read_text_safely(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Validate a Week 7 anti-AI submission.")
    p.add_argument("--challenge", required=True, type=Path, help="Challenge YAML")
    p.add_argument("--evidence", required=True, type=Path, help="Evidence JSON")
    p.add_argument("--base-dir", default=Path("."), type=Path, help="Base directory for artefacts")
    p.add_argument("--ignore-ttl", action="store_true", help="Ignore TTL expiry (instructor use)")
    p.add_argument("--verbose", action="store_true", help="Verbose output")
    return p


def validate(challenge_path: Path, evidence_path: Path, base_dir: Path, *, ignore_ttl: bool) -> Tuple[bool, List[ValidationIssue]]:
    chal = load_challenge(challenge_path)

    if chal.is_expired() and not ignore_ttl:
        return False, [ValidationIssue("error", "Challenge expired, regenerate and rerun the lab")]

    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    issues: List[ValidationIssue] = []

    artefacts = evidence.get("artefacts", [])
    if not isinstance(artefacts, list) or not artefacts:
        issues.append(ValidationIssue("error", "Evidence contains no artefacts"))

    # Verify hashes and gather candidate files
    base = base_dir.resolve()
    pcap_files: List[Path] = []
    text_files: List[Path] = []

    for a in artefacts:
        if not isinstance(a, dict):
            continue
        rel = a.get("path")
        expected = a.get("sha256")
        if not rel or not expected:
            issues.append(ValidationIssue("error", "Artefact entry missing path or sha256"))
            continue
        ap = (base / rel).resolve() if not Path(rel).is_absolute() else Path(rel)
        if not ap.exists():
            issues.append(ValidationIssue("error", f"Missing artefact: {rel}"))
            continue
        actual = sha256_file(ap)
        if actual != expected:
            issues.append(ValidationIssue("error", f"Hash mismatch for {rel}"))
            continue

        if ap.suffix.lower() in {".pcap", ".pcapng"}:
            pcap_files.append(ap)
        elif ap.suffix.lower() in {".md", ".txt", ".json", ".py"}:
            text_files.append(ap)

    # Report token check
    report_ok = False
    for tf in text_files:
        if chal.report_token in _read_text_safely(tf):
            report_ok = True
            break
    if not report_ok:
        issues.append(
            ValidationIssue(
                "error",
                "Report token not found in any text artefact, include it verbatim in your report",
            )
        )

    # PCAP token check
    if not pcap_files:
        issues.append(ValidationIssue("error", "No PCAP artefact provided"))

    tcp_found = False
    udp_found = False
    handshake_ok = False

    token_bytes = chal.payload_token.encode("utf-8")
    for pf in pcap_files:
        try:
            packets = list(iter_packets(pf))
        except PcapFormatError as e:
            issues.append(ValidationIssue("error", f"{pf.name}: {e}"))

            continue
        t, u = find_payload_token(packets, token_bytes, tcp_port=chal.tcp_port, udp_port=chal.udp_port)
        tcp_found = tcp_found or t
        udp_found = udp_found or u
        handshake_ok = handshake_ok or has_tcp_handshake(packets, port=chal.tcp_port)

    if not tcp_found:
        issues.append(
            ValidationIssue(
                "error",
                f"Payload token not found in TCP payload towards port {chal.tcp_port}",
            )
        )
    if not udp_found:
        issues.append(
            ValidationIssue(
                "error",
                f"Payload token not found in UDP payload towards port {chal.udp_port}",
            )
        )
    if not handshake_ok:
        issues.append(
            ValidationIssue(
                "warning",
                "TCP handshake pattern not detected, ensure you captured the start of the connection",
            )
        )

    ok = not any(i.level == "error" for i in issues)
    return ok, issues


def main() -> int:
    args = build_parser().parse_args()
    ok, issues = validate(args.challenge, args.evidence, args.base_dir, ignore_ttl=args.ignore_ttl)

    if args.verbose:
        print("Validation results:")
    for i in issues:
        prefix = "ERROR" if i.level == "error" else "WARNING"
        print(f"{prefix}: {i.message}")

    if ok:
        print("PASS")
        return 0
    print("FAIL")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
