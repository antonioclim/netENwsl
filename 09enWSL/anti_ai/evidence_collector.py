#!/usr/bin/env python3
"""
Evidence collector for Week 9 anti-AI workflow.

This script records:
- environment fingerprint (basic provenance)
- artefact hashes (PCAP and report)

It does not attempt to grade content. It only packages verifiable evidence
that a validator can later check.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from anti_ai.challenge import load_challenge
from anti_ai.fingerprint import EnvironmentFingerprint, resolve_project_root


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


@dataclass(frozen=True)
class ArtefactRecord:
    path: str
    sha256: str
    size_bytes: int

    @classmethod
    def from_path(cls, path: Path) -> "ArtefactRecord":
        return cls(path=str(path.as_posix()), sha256=sha256_file(path), size_bytes=path.stat().st_size)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect Week 9 anti-AI evidence")
    parser.add_argument("--challenge", type=Path, required=True, help="Path to challenge JSON")
    parser.add_argument("--pcap", type=Path, action="append", required=True, help="PCAP/PCAPNG capture path (repeatable)")
    parser.add_argument("--report", type=Path, required=True, help="Written report path (txt/md)")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("artifacts/anti_ai"),
        help="Output directory (default: artifacts/anti_ai)",
    )

    args = parser.parse_args()

    project_root = resolve_project_root()
    challenge_path = (project_root / args.challenge).resolve() if not args.challenge.is_absolute() else args.challenge
    challenge = load_challenge(challenge_path)

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    artefacts: list[ArtefactRecord] = []

    report_path = (project_root / args.report).resolve() if not args.report.is_absolute() else args.report
    artefacts.append(ArtefactRecord.from_path(report_path))

    for p in args.pcap:
        pcap_path = (project_root / p).resolve() if not p.is_absolute() else p
        artefacts.append(ArtefactRecord.from_path(pcap_path))

    evidence = {
        "schema_version": 1,
        "course": challenge.course,
        "week": challenge.week,
        "student_id": challenge.student_id,
        "created_at_utc": now,
        "challenge_sha256": challenge.integrity_sha256,
        "environment": EnvironmentFingerprint.collect().to_dict(),
        "artefacts": [a.to_dict() for a in artefacts],
    }

    out_dir: Path = args.out
    out_path = out_dir / f"evidence_week09_{challenge.student_id}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
