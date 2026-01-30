#!/usr/bin/env python3
"""Submission validator for the Week 1 anti-AI workflow.

This validator is designed to be used by instructors or CI to verify that a
Week 1 homework submission contains evidence of real laboratory interaction.

It validates:
- challenge validity window
- basic challenge integrity hash
- presence and hashes of required artefacts
- presence of the report token in the report
- presence of the PCAP payload token in the submitted TCP and UDP PCAP files
- a minimal TCP three-way handshake pattern in the TCP PCAP

Important
This validator does not attempt to detect whether a student used AI tools for
explanations. It enforces that a valid submission must include artefacts that
AI alone cannot produce.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc

from anti_ai.pcap_tools import inspect_pcap


@dataclass
class ValidationResult:
    name: str
    passed: bool
    message: str
    details: Optional[Dict[str, Any]] = None


@dataclass
class ValidationReport:
    student_id: str
    session_token: str
    generated_at_utc: str
    validated_at_utc: str
    results: List[ValidationResult] = field(default_factory=list)

    @property
    def passed_count(self) -> int:
        return sum(1 for r in self.results if r.passed)

    @property
    def failed_count(self) -> int:
        return sum(1 for r in self.results if not r.passed)

    @property
    def all_passed(self) -> bool:
        return self.failed_count == 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "student_id": self.student_id,
            "session_token": self.session_token[:16] + "...",
            "generated_at_utc": self.generated_at_utc,
            "validated_at_utc": self.validated_at_utc,
            "summary": {
                "passed": self.passed_count,
                "failed": self.failed_count,
                "total": len(self.results),
                "status": "PASS" if self.all_passed else "FAIL",
            },
            "results": [
                {
                    "name": r.name,
                    "passed": r.passed,
                    "message": r.message,
                    "details": r.details,
                }
                for r in self.results
            ],
        }


def _load_structured_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with open(path, encoding="utf-8") as f:
        if path.suffix.lower() in {".yaml", ".yml"}:
            return yaml.safe_load(f)
        if path.suffix.lower() == ".json":
            return json.load(f)

    raise ValueError("Unsupported file type. Use .yaml, .yml or .json")


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _verification_hash(student_id: str, session_token: str, generated_at_utc: str) -> str:
    data = f"{student_id}:{session_token}:{generated_at_utc}:week1"
    return hashlib.sha256(data.encode("utf-8")).hexdigest()[:16]


class SubmissionValidator:
    def __init__(
        self,
        *,
        challenge_file: Path,
        evidence_file: Path,
        base_dir: Path,
        verbose: bool = False,
    ) -> None:
        self.challenge_file = challenge_file
        self.evidence_file = evidence_file
        self.base_dir = base_dir
        self.verbose = verbose

        self.challenge: dict[str, Any] = _load_structured_file(challenge_file)
        self.evidence: dict[str, Any] = _load_structured_file(evidence_file)

        meta = self.challenge.get("metadata", {})
        self.student_id = str(meta.get("student_id") or "")
        self.session_token = str(meta.get("session_token") or "")
        self.generated_at_utc = str(meta.get("generated_at_utc") or "")

        self.report_token = str(self.challenge.get("challenges", {}).get("report", {}).get("token") or "")
        self.payload_token = str(self.challenge.get("challenges", {}).get("pcap", {}).get("payload_token") or "")

    def _log(self, msg: str) -> None:
        if self.verbose:
            print(msg)

    def validate_all(self) -> ValidationReport:
        report = ValidationReport(
            student_id=self.student_id,
            session_token=self.session_token,
            generated_at_utc=self.generated_at_utc,
            validated_at_utc=datetime.now(timezone.utc).isoformat(),
        )

        checks = [
            self._validate_challenge_window,
            self._validate_challenge_integrity,
            self._validate_evidence_metadata,
            self._validate_artefact_hashes,
            self._validate_report_token,
            self._validate_pcap_tokens,
        ]

        for fn in checks:
            try:
                result = fn()
            except Exception as exc:  # pragma: no cover
                result = ValidationResult(name=fn.__name__, passed=False, message=f"Validation error: {exc}")
            report.results.append(result)

            status = "✅" if result.passed else "❌"
            self._log(f"{status} {result.name}: {result.message}")

        return report

    def _validate_challenge_window(self) -> ValidationResult:
        meta = self.challenge.get("metadata", {})
        try:
            expires = datetime.fromisoformat(str(meta.get("expires_at_utc")))
            now = datetime.now(timezone.utc)
            if expires.tzinfo is None:
                expires = expires.replace(tzinfo=timezone.utc)
            if now > expires:
                return ValidationResult(
                    name="challenge_window",
                    passed=False,
                    message=f"Challenge expired at {expires.isoformat()}",
                )
            return ValidationResult(
                name="challenge_window",
                passed=True,
                message=f"Challenge valid until {expires.isoformat()}",
            )
        except Exception as exc:
            return ValidationResult(name="challenge_window", passed=False, message=f"Invalid expiry: {exc}")

    def _validate_challenge_integrity(self) -> ValidationResult:
        meta = self.challenge.get("metadata", {})
        stored = str(meta.get("verification_hash") or "")
        computed = _verification_hash(self.student_id, self.session_token, self.generated_at_utc)
        if stored != computed:
            return ValidationResult(
                name="challenge_integrity",
                passed=False,
                message="Challenge metadata mismatch (verification hash)",
                details={"stored": stored, "computed": computed},
            )
        return ValidationResult(name="challenge_integrity", passed=True, message="Challenge metadata consistent")

    def _validate_evidence_metadata(self) -> ValidationResult:
        meta = self.evidence.get("meta", {})
        if str(meta.get("student_id") or "") != self.student_id:
            return ValidationResult(
                name="evidence_metadata",
                passed=False,
                message="Student id mismatch between challenge and evidence",
            )
        if str(meta.get("session_token") or "") != self.session_token:
            return ValidationResult(
                name="evidence_metadata",
                passed=False,
                message="Session token mismatch between challenge and evidence",
            )
        if str(meta.get("challenge_verification_hash") or "") != str(self.challenge.get("metadata", {}).get("verification_hash") or ""):
            return ValidationResult(
                name="evidence_metadata",
                passed=False,
                message="Challenge verification hash mismatch",
            )
        return ValidationResult(name="evidence_metadata", passed=True, message="Evidence metadata matches challenge")

    def _resolve_path(self, rel_or_abs: str) -> Path:
        p = Path(rel_or_abs)
        if p.is_absolute():
            return p
        return self.base_dir / p

    def _validate_artefact_hashes(self) -> ValidationResult:
        artefacts = self.evidence.get("artefacts")
        if not isinstance(artefacts, list) or not artefacts:
            return ValidationResult(name="artefact_hashes", passed=False, message="No artefacts listed in evidence")

        missing: list[str] = []
        mismatched: list[dict[str, str]] = []

        for item in artefacts:
            if not isinstance(item, dict):
                continue
            path = self._resolve_path(str(item.get("path") or ""))
            expected = str(item.get("sha256") or "")

            if not path.exists():
                missing.append(str(path))
                continue

            actual = _sha256_file(path)
            if expected and actual != expected:
                mismatched.append({"path": str(path), "expected": expected, "actual": actual})

        if missing:
            return ValidationResult(
                name="artefact_hashes",
                passed=False,
                message=f"Missing artefacts: {len(missing)}",
                details={"missing": missing},
            )
        if mismatched:
            return ValidationResult(
                name="artefact_hashes",
                passed=False,
                message=f"Artefact hash mismatch: {len(mismatched)}",
                details={"mismatched": mismatched[:5]},
            )

        return ValidationResult(name="artefact_hashes", passed=True, message="Artefact files and hashes verified")

    def _validate_report_token(self) -> ValidationResult:
        report_path: Optional[Path] = None
        for item in self.evidence.get("artefacts", []):
            if isinstance(item, dict) and str(item.get("path") or "").endswith("network_report.md"):
                report_path = self._resolve_path(str(item.get("path") or ""))
                break

        if report_path is None:
            return ValidationResult(name="report_token", passed=False, message="network_report.md not listed in evidence")

        try:
            text = report_path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            return ValidationResult(name="report_token", passed=False, message=f"Failed to read report: {exc}")

        if not self.report_token:
            return ValidationResult(name="report_token", passed=False, message="Challenge does not define a report token")

        if self.report_token not in text:
            return ValidationResult(
                name="report_token",
                passed=False,
                message="Report token not found in network_report.md",
                details={"expected_token": self.report_token},
            )

        return ValidationResult(name="report_token", passed=True, message="Report token found")

    def _validate_pcap_tokens(self) -> ValidationResult:
        if not self.payload_token:
            return ValidationResult(name="pcap_tokens", passed=False, message="Challenge does not define a PCAP payload token")

        pcaps: list[Path] = []
        for item in self.evidence.get("artefacts", []):
            if not isinstance(item, dict):
                continue
            p = str(item.get("path") or "")
            if p.endswith(".pcap"):
                pcaps.append(self._resolve_path(p))

        if not pcaps:
            return ValidationResult(name="pcap_tokens", passed=False, message="No PCAP artefacts listed in evidence")

        failures: list[dict[str, Any]] = []

        for pcap in pcaps:
            inspection = inspect_pcap(pcap, expected_payload=self.payload_token)
            ok_payload = inspection.payload_found
            ok_handshake = True

            # Require handshake only for TCP capture (heuristic: name contains 'tcp')
            if "tcp" in pcap.name.lower():
                ok_handshake = inspection.handshake_ok

            if not ok_payload or not ok_handshake:
                failures.append(
                    {
                        "pcap": str(pcap),
                        "payload_found": inspection.payload_found,
                        "handshake_ok": inspection.handshake_ok,
                        "details": inspection.to_dict(),
                    }
                )

        if failures:
            return ValidationResult(
                name="pcap_tokens",
                passed=False,
                message=f"PCAP proof checks failed: {len(failures)}",
                details={"failures": failures[:3]},
            )

        return ValidationResult(name="pcap_tokens", passed=True, message="PCAP proof tokens verified")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Week 1 anti-AI submission")
    parser.add_argument("--challenge", type=Path, required=True, help="Challenge file")
    parser.add_argument("--evidence", type=Path, required=True, help="Evidence JSON file")
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=Path.cwd(),
        help="Base directory for relative artefact paths (default: current directory)",
    )
    parser.add_argument("--report", type=Path, default=None, help="Write JSON report to file")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    validator = SubmissionValidator(
        challenge_file=args.challenge,
        evidence_file=args.evidence,
        base_dir=args.base_dir,
        verbose=args.verbose,
    )
    report = validator.validate_all()

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
        print(f"[OK] Report written: {args.report}")

    status = "PASS" if report.all_passed else "FAIL"
    print(f"\n=== Week 1 Anti-AI Validation: {status} ===")
    print(f"Checks passed: {report.passed_count}/{len(report.results)}")

    if not report.all_passed:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
