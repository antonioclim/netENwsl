"""Submission validator for Week 13 anti-AI workflow."""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

from .challenge import verify_integrity
from .pcap_tools import (
    pcap_contains_tls_handshake,
    pcap_contains_token_on_port,
    pcap_has_basic_tcp_handshake,
)


def _parse_utc(value: str) -> _dt.datetime:
    return _dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=_dt.timezone.utc)


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _read_text(path: Path, max_bytes: int = 2_000_000) -> str:
    data = path.read_bytes()[:max_bytes]
    return data.decode("utf-8", errors="replace")


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Validate Week 13 anti-AI submission")
    p.add_argument("--challenge", required=True, help="Challenge YAML path")
    p.add_argument("--evidence", required=True, help="Evidence JSON path")
    p.add_argument("--base-dir", default=".", help="Base directory for artefact paths")
    p.add_argument("--secret-env", default="ANTI_AI_SECRET", help="Environment variable name for HMAC secret")
    p.add_argument("--require-tls", action="store_true", help="Require a TLS handshake capture on 8883")
    p.add_argument("--verbose", action="store_true", help="Verbose output")
    return p


def _check_ttl(challenge: Dict[str, Any], evidence: Dict[str, Any]) -> Tuple[bool, str]:
    try:
        issued = _parse_utc(str(challenge["issued_at_utc"]))
        collected = _parse_utc(str(evidence["meta"]["collected_at_utc"]))
        ttl = int(challenge["ttl_seconds"])
    except Exception as exc:
        return False, f"TTL check failed: {exc}"

    expires = issued + _dt.timedelta(seconds=ttl)
    if collected > expires:
        return False, f"Evidence collected after expiry ({collected.isoformat()} > {expires.isoformat()})"
    return True, "TTL ok"


def main() -> int:
    args = build_arg_parser().parse_args()
    base_dir = Path(args.base_dir).resolve()

    secret = None
    if args.secret_env:
        import os
        secret = os.environ.get(args.secret_env)

    challenge_path = Path(args.challenge)
    challenge = yaml.safe_load(challenge_path.read_text(encoding="utf-8"))
    if not isinstance(challenge, dict):
        raise SystemExit("[ERROR] Invalid challenge format")

    if not verify_integrity(challenge, secret):
        raise SystemExit("[ERROR] Challenge integrity tag does not verify")

    evidence_path = Path(args.evidence)
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    if not isinstance(evidence, dict):
        raise SystemExit("[ERROR] Invalid evidence format")

    ok, msg = _check_ttl(challenge, evidence)
    if not ok:
        raise SystemExit(f"[ERROR] {msg}")
    if args.verbose:
        print(f"[OK] {msg}")

    artefacts: List[Dict[str, Any]] = list(evidence.get("artefacts", []))
    if not artefacts:
        raise SystemExit("[ERROR] No artefacts listed in evidence")

    # Verify hashes
    for item in artefacts:
        rel = Path(str(item.get("path", "")))
        expected = str(item.get("sha256", ""))
        ap = (base_dir / rel).resolve()
        if not ap.exists():
            raise SystemExit(f"[ERROR] Missing artefact: {rel}")
        actual = _sha256_file(ap)
        if actual != expected:
            raise SystemExit(f"[ERROR] SHA256 mismatch for {rel}")

    # Token must appear in at least one text artefact
    report_token = str(challenge.get("report_token", ""))
    if not report_token:
        raise SystemExit("[ERROR] Challenge report token missing")

    token_found = False
    for item in artefacts:
        rel = Path(str(item.get("path", "")))
        if rel.suffix.lower() not in {".json", ".md", ".txt", ".log"}:
            continue
        txt = _read_text((base_dir / rel).resolve())
        if report_token in txt:
            token_found = True
            break
    if not token_found:
        raise SystemExit("[ERROR] Report token not found in submitted text artefacts")

    # Payload token in plaintext MQTT capture
    payload_token = str(challenge.get("payload_token", ""))
    mqtt_plain_port = int(challenge.get("mqtt_plain_port", 1883))
    mqtt_tls_port = int(challenge.get("mqtt_tls_port", 8883))

    pcap_paths = [Path(str(a.get("path", ""))) for a in artefacts if str(a.get("path", "")).lower().endswith(".pcap")]
    if not pcap_paths:
        raise SystemExit("[ERROR] No PCAP artefacts listed in evidence")

    mqtt_token_ok = False
    handshake_ok = False
    tls_ok = False

    for rel in pcap_paths:
        ap = (base_dir / rel).resolve()
        if pcap_contains_token_on_port(ap, payload_token, mqtt_plain_port):
            mqtt_token_ok = True
        if pcap_has_basic_tcp_handshake(ap, mqtt_plain_port):
            handshake_ok = True
        if pcap_contains_tls_handshake(ap, mqtt_tls_port):
            tls_ok = True

    if not mqtt_token_ok:
        raise SystemExit("[ERROR] Payload token not found in MQTT plaintext capture (port 1883)")
    if not handshake_ok:
        raise SystemExit("[ERROR] No basic TCP handshake observed for MQTT plaintext port (1883)")
    if args.require_tls and not tls_ok:
        raise SystemExit("[ERROR] No TLS handshake observed on port 8883")

    if args.verbose:
        print("[OK] Payload token observed in MQTT plaintext capture")
        print("[OK] TCP handshake observed for MQTT plaintext capture")
        if args.require_tls:
            print("[OK] TLS handshake observed on 8883")

    print("[PASS] Submission validates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
