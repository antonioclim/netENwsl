"""Submission validation for Week 8.

This validator is designed to run:
  - locally (student self-check)
  - in CI (instructor grading)

The validator checks:
  1) challenge expiry
  2) evidence file integrity (hashes)
  3) minimum protocol signals in required PCAPs

It does not aim to replace a viva, it provides a strong baseline.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .challenge import Challenge, load_challenge
from .evidence_collector import SCHEMA_VERSION as EVIDENCE_SCHEMA
from .files import sha256_file
from .pcap_tools import (
    capture_contains_ascii,
    capture_mentions_port,
    count_http_header_values,
    has_basic_tcp_handshake,
)
from .signing import verify_signature


@dataclass
class ValidationResult:
    ok: bool
    issues: List[str]
    details: Dict[str, Any]


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _evidence_index(evidence: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    idx: Dict[str, Dict[str, Any]] = {}
    for entry in evidence.get("artefacts") or []:
        p = str(entry.get("path") or "")
        if p:
            idx[p] = entry
    return idx


def validate_submission(
    *,
    project_root: Path,
    challenge_path: Path,
    evidence_path: Path,
    secret: Optional[str] = None,
    strict_signature: bool = False,
) -> ValidationResult:
    issues: List[str] = []
    details: Dict[str, Any] = {}

    if not challenge_path.exists():
        return ValidationResult(False, [f"Missing challenge file: {challenge_path}"], {})

    if not evidence_path.exists():
        return ValidationResult(False, [f"Missing evidence file: {evidence_path}"], {})

    challenge: Challenge = load_challenge(challenge_path)
    evidence = _load_json(evidence_path)

    if challenge.schema != "networking.anti_ai.challenge.v1":
        issues.append("Challenge schema is not recognised")

    if evidence.get("schema") != EVIDENCE_SCHEMA:
        issues.append("Evidence schema is not recognised")

    # Expiry check
    if challenge.is_expired(datetime.now(timezone.utc)):
        issues.append("Challenge is expired")

    # Optional signature check
    if strict_signature:
        if not secret:
            issues.append("Strict signature validation requested but no secret provided")
        else:
            unsigned = dict(challenge.as_dict())
            sig = unsigned.pop("signature", None)
            if not verify_signature(unsigned, secret, sig):
                issues.append("Challenge signature is invalid")
    else:
        if secret and challenge.signature:
            unsigned = dict(challenge.as_dict())
            sig = unsigned.pop("signature", None)
            details["signature_valid"] = verify_signature(unsigned, secret, sig)

    # Evidence hashes check
    idx = _evidence_index(evidence)
    details["missing"] = list(evidence.get("missing") or [])

    # Context must exist
    context_rel = "artifacts/student_context.json"
    if context_rel not in idx:
        issues.append("Evidence does not include artifacts/student_context.json")
    else:
        ctx_path = project_root / context_rel
        if not ctx_path.exists():
            issues.append("Context file is missing from working tree")
        else:
            actual_ctx = sha256_file(ctx_path)
            if actual_ctx != challenge.context_sha256:
                issues.append("Context file hash does not match the challenge")

    # Required captures checks
    required = challenge.required_captures or {}
    port = int(challenge.http_port)
    secret_value = challenge.secret_header_value

    capture_results: Dict[str, Any] = {}
    for name, info in required.items():
        filename = str((info or {}).get("filename") or "")
        if not filename:
            continue

        rel = filename
        cap_path = project_root / rel
        entry = idx.get(rel)
        cap_ok = True
        cap_issues: List[str] = []

        if not cap_path.exists():
            cap_ok = False
            cap_issues.append(f"Missing capture file: {rel}")
        else:
            if entry:
                actual = sha256_file(cap_path)
                if actual != entry.get("sha256"):
                    cap_ok = False
                    cap_issues.append("Capture hash does not match evidence.json")
            else:
                cap_ok = False
                cap_issues.append("Capture not listed in evidence.json")

        # Protocol-level checks (best effort)
        if cap_ok:
            if not capture_mentions_port(cap_path, port):
                cap_ok = False
                cap_issues.append(f"No packets on expected port {port}")

            # Additional checks per capture type
            if name == "handshake":
                if not has_basic_tcp_handshake(cap_path, port):
                    cap_ok = False
                    cap_issues.append("TCP handshake not detected")

            if name == "http_exchange":
                if secret_value and not capture_contains_ascii(cap_path, secret_value, port=port):
                    cap_ok = False
                    cap_issues.append("Student token not detected in HTTP payload")

            if name == "load_balance":
                backend_counts = count_http_header_values(cap_path, "X-Backend-ID", port=None)
                capture_results.setdefault("load_balance", {})["backend_counts"] = backend_counts
                if len(backend_counts) < 2:
                    cap_ok = False
                    cap_issues.append("Did not detect responses from multiple backends")

        capture_results[name] = {
            "ok": cap_ok,
            "issues": cap_issues,
            "path": rel,
        }

        if not cap_ok:
            issues.extend([f"{name}: {m}" for m in cap_issues])

    details["captures"] = capture_results
    details["student_hash"] = challenge.student_hash
    details["port"] = port

    return ValidationResult(ok=(len(issues) == 0), issues=issues, details=details)


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Validate Week 8 anti-AI submission")
    parser.add_argument(
        "--challenge",
        default="artifacts/anti_ai/challenge_week08.json",
        help="Path to challenge JSON",
    )
    parser.add_argument(
        "--evidence",
        default="artifacts/anti_ai/evidence.json",
        help="Path to evidence JSON",
    )
    parser.add_argument(
        "--secret",
        default=None,
        help="Optional CI secret for signature validation",
    )
    parser.add_argument(
        "--strict-signature",
        action="store_true",
        help="Fail if the challenge is not correctly signed",
    )

    args = parser.parse_args()
    root = Path(".").resolve()

    result = validate_submission(
        project_root=root,
        challenge_path=root / args.challenge,
        evidence_path=root / args.evidence,
        secret=args.secret,
        strict_signature=bool(args.strict_signature),
    )

    if result.ok:
        print("PASS")
        return 0

    print("FAIL")
    for issue in result.issues:
        print(f"- {issue}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
