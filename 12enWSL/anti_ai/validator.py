#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# MODULE_DOCSTRING
# ═══════════════════════════════════════════════════════════════════════════════
"""Submission validator for Week 12 anti-AI evidence.

The validator checks that a submission contains real protocol interaction
by verifying that challenge tokens appear in packet captures.

Required evidence (default policy):
 - a capture file (PCAP or PCAPNG)
 - the SMTP token must appear on traffic involving the SMTP port (1025)
 - the RPC token must appear on traffic involving both JSON-RPC (6200) and XML-RPC (6201)

Optional evidence:
 - a short report markdown file containing the report token

This does not attempt to be unbreakable. It aims to be *practical*, easy to run and
hard to fake without actually exercising the lab.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:  # pragma: no cover
    print("[ERROR] PyYAML is required: pip install pyyaml")
    raise

from .challenge import Week12Challenge
from .pcap_tools import PcapParseError, find_token_hits, summarise_capture


def _parse_utc(ts: str) -> datetime:
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"
    return datetime.fromisoformat(ts)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _sha256_file(path: Path) -> str:
    import hashlib

    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


@dataclass(frozen=True)
class CheckResult:
    name: str
    passed: bool
    details: str


@dataclass
class ValidationReport:
    ok: bool
    challenge_path: str
    evidence_path: str
    checks: List[CheckResult] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ok": self.ok,
            "challenge_path": self.challenge_path,
            "evidence_path": self.evidence_path,
            "checks": [c.__dict__ for c in self.checks],
            "warnings": list(self.warnings),
        }


class Week12SubmissionValidator:
    """Validate a Week 12 submission against a challenge."""

    def __init__(self, *, strict: bool = False, allowed_clock_skew_minutes: int = 10):
        self.strict = bool(strict)
        self.allowed_clock_skew = timedelta(minutes=int(allowed_clock_skew_minutes))

    def load_challenge(self, path: Path) -> Week12Challenge:
        obj = yaml.safe_load(path.read_text(encoding="utf-8"))
        return Week12Challenge.from_dict(obj)

    def load_evidence(self, path: Path) -> Dict[str, Any]:
        return json.loads(path.read_text(encoding="utf-8"))

    def validate(self, *, challenge_path: Path, evidence_path: Path) -> ValidationReport:
        report = ValidationReport(ok=True, challenge_path=str(challenge_path), evidence_path=str(evidence_path))

        try:
            challenge = self.load_challenge(challenge_path)
        except Exception as exc:
            report.ok = False
            report.checks.append(CheckResult("load_challenge", False, f"Failed to load challenge: {exc}"))
            return report

        try:
            evidence = self.load_evidence(evidence_path)
        except Exception as exc:
            report.ok = False
            report.checks.append(CheckResult("load_evidence", False, f"Failed to load evidence: {exc}"))
            return report

        # Check 1: student ID match
        ev_student = str((evidence.get("meta") or {}).get("student_id", "")).strip()
        if ev_student and ev_student != challenge.student_id:
            report.ok = False
            report.checks.append(
                CheckResult(
                    "student_id_match",
                    False,
                    f"Evidence student_id '{ev_student}' does not match challenge '{challenge.student_id}'",
                )
            )
        else:
            report.checks.append(CheckResult("student_id_match", True, "Student ID consistent"))

        # Check 2: challenge signature (optional)
        if challenge.signature_hmac_sha256:
            # When the signature exists we can verify it if the key is available.
            key = os.getenv("WEEK12_CHALLENGE_HMAC_KEY")
            if not key:
                report.warnings.append(
                    "Challenge is signed but WEEK12_CHALLENGE_HMAC_KEY is not set so the signature was not verified"
                )
                report.checks.append(CheckResult("challenge_signature", True, "Signature present (not verified)"))
            else:
                import hmac
                import hashlib
                import json as _json

                payload = challenge.to_dict()
                payload.pop("signature_hmac_sha256", None)
                canon = _json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
                mac = hmac.new(key.encode("utf-8"), canon, hashlib.sha256).hexdigest()
                ok = hmac.compare_digest(mac, str(challenge.signature_hmac_sha256))
                if not ok:
                    report.ok = False
                report.checks.append(
                    CheckResult(
                        "challenge_signature",
                        ok,
                        "Signature verified" if ok else "Signature mismatch (challenge may be tampered)",
                    )
                )
        else:
            if self.strict:
                report.ok = False
                report.checks.append(
                    CheckResult(
                        "challenge_signature",
                        False,
                        "Unsigned challenge in strict mode",
                    )
                )
            else:
                report.checks.append(CheckResult("challenge_signature", True, "No signature (non-strict mode)"))

        # Locate capture(s)
        capture_paths = (evidence.get("artifacts") or {}).get("pcaps") or []
        capture_paths = [Path(p) for p in capture_paths]
        capture_paths = [p for p in capture_paths if p.exists()]

        if not capture_paths:
            report.ok = False
            report.checks.append(CheckResult("pcap_present", False, "No existing PCAP/PCAPNG files listed in evidence"))
            return report
        report.checks.append(CheckResult("pcap_present", True, f"Found {len(capture_paths)} capture file(s)"))

        # Check 3: capture time window (use packet timestamps when available)
        issued = challenge.issued_at
        expires = challenge.expires_at
        win_start = issued - self.allowed_clock_skew
        win_end = expires + self.allowed_clock_skew

        cap_summaries = []
        time_ok_any = False
        time_details = []
        for p in capture_paths:
            try:
                s = summarise_capture(p)
                cap_summaries.append((p, s))
                if s.packet_count == 0:
                    time_details.append(f"{p}: empty capture")
                    continue
                if s.first_ts is None or s.last_ts is None:
                    time_details.append(f"{p}: no timestamps")
                    continue
                first = datetime.fromtimestamp(s.first_ts, tz=timezone.utc)
                last = datetime.fromtimestamp(s.last_ts, tz=timezone.utc)
                ok = (win_start <= first <= win_end) and (win_start <= last <= win_end)
                time_ok_any = time_ok_any or ok
                time_details.append(
                    f"{p.name}: packets={s.packet_count}, first={first.isoformat(timespec='seconds')}, "
                    f"last={last.isoformat(timespec='seconds')}, linktypes={s.linktypes}, within_window={ok}"
                )
            except PcapParseError as exc:
                time_details.append(f"{p.name}: parse error: {exc}")

        if not time_ok_any:
            report.ok = False
        report.checks.append(
            CheckResult(
                "capture_time_window",
                time_ok_any,
                " | ".join(time_details),
            )
        )

        # Token searches
        smtp_port = int(challenge.smtp_port)
        json_port = int(challenge.jsonrpc_port)
        xml_port = int(challenge.xmlrpc_port)

        smtp_hits = []
        rpc_hits = []

        for p in capture_paths:
            smtp_hits.extend(find_token_hits(p, challenge.smtp_subject_token))
            rpc_hits.extend(find_token_hits(p, challenge.rpc_echo_token))

        def _has_port(hits: List[Any], port: int) -> bool:
            for h in hits:
                if h.src_port == port or h.dst_port == port:
                    return True
            return False

        smtp_ok = bool(smtp_hits) and _has_port(smtp_hits, smtp_port)
        rpc_json_ok = bool(rpc_hits) and _has_port(rpc_hits, json_port)
        rpc_xml_ok = bool(rpc_hits) and _has_port(rpc_hits, xml_port)

        if not smtp_ok:
            report.ok = False
        report.checks.append(
            CheckResult(
                "smtp_token_in_capture",
                smtp_ok,
                f"Hits={len(smtp_hits)}, required_port={smtp_port}",
            )
        )

        if not (rpc_json_ok and rpc_xml_ok):
            report.ok = False
        report.checks.append(
            CheckResult(
                "rpc_token_in_capture",
                bool(rpc_hits),
                f"Hits={len(rpc_hits)}", 
            )
        )
        report.checks.append(
            CheckResult(
                "rpc_token_jsonrpc_port",
                rpc_json_ok,
                f"Token must appear on port {json_port}",
            )
        )
        report.checks.append(
            CheckResult(
                "rpc_token_xmlrpc_port",
                rpc_xml_ok,
                f"Token must appear on port {xml_port}",
            )
        )

        # Optional: report token in markdown file
        report_path = (evidence.get("artifacts") or {}).get("report")
        if report_path:
            rp = Path(str(report_path))
            if not rp.exists():
                report.warnings.append(f"Report file listed in evidence does not exist: {rp}")
            else:
                text = rp.read_text(encoding="utf-8", errors="replace")
                ok = challenge.report_token in text
                if not ok:
                    report.ok = False
                report.checks.append(
                    CheckResult(
                        "report_token_present",
                        ok,
                        f"Expected token '{challenge.report_token}' in {rp}",
                    )
                )
        else:
            report.warnings.append("No report path provided in evidence, report token not checked")

        # Optional: evidence file hashes
        hashes = (evidence.get("artifacts") or {}).get("sha256") or {}
        mismatches = []
        for p in capture_paths:
            expected = hashes.get(str(p)) or hashes.get(p.name)
            if expected:
                actual = _sha256_file(p)
                if str(expected) != actual:
                    mismatches.append(f"{p}: expected {expected}, got {actual}")

        if mismatches:
            report.ok = False
            report.checks.append(CheckResult("artifact_hashes", False, " | ".join(mismatches)))
        else:
            report.checks.append(CheckResult("artifact_hashes", True, "OK"))

        return report


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Validate Week 12 anti-AI evidence")
    ap.add_argument("--challenge", type=Path, required=True, help="Challenge YAML path")
    ap.add_argument("--evidence", type=Path, required=True, help="Evidence JSON path")
    ap.add_argument("--strict", action="store_true", help="Require a signed challenge")
    ap.add_argument("--report", type=Path, default=None, help="Write JSON report to this path")
    return ap.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    v = Week12SubmissionValidator(strict=bool(args.strict))
    rep = v.validate(challenge_path=args.challenge, evidence_path=args.evidence)

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(rep.to_dict(), indent=2), encoding="utf-8")
        print(f"Report written to: {args.report}")

    # Human-readable summary
    status = "PASS" if rep.ok else "FAIL"
    print(f"Week 12 anti-AI validation: {status}")
    for c in rep.checks:
        mark = "✓" if c.passed else "✗"
        print(f"  {mark} {c.name}: {c.details}")
    if rep.warnings:
        print("Warnings:")
        for w in rep.warnings:
            print(f"  - {w}")

    return 0 if rep.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
