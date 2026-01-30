#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# MODULE_DOCSTRING
# ═══════════════════════════════════════════════════════════════════════════════
"""Generate a Week 12 anti-AI evidence file.

The evidence file is intentionally boring JSON. It records:

 - which capture(s) and report file you intend to submit
 - SHA-256 hashes so the assessor can detect accidental corruption
 - a small environment fingerprint (hashed) for auditability

The validator uses the capture itself for the core check.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    import yaml
except ImportError:  # pragma: no cover
    print("[ERROR] PyYAML is required: pip install pyyaml")
    raise


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _run_cmd(cmd: List[str]) -> str:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
        out = (r.stdout or "") + (r.stderr or "")
        return out.strip()
    except Exception:
        return ""


def _fingerprint() -> str:
    """Return a privacy-preserving environment fingerprint.

We hash the raw strings to avoid leaking detailed host metadata.
"""

    parts = [
        platform.platform(),
        platform.python_version(),
        _run_cmd(["uname", "-a"]),
        _run_cmd(["wslpath", "-m", "/"]) if os.name == "posix" else "",
        _run_cmd(["docker", "ps", "--format", "{{.ID}} {{.Image}} {{.Names}}"]),
    ]
    raw = "\n".join(p for p in parts if p)
    return hashlib.sha256(raw.encode("utf-8", errors="replace")).hexdigest()


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Generate Week 12 anti-AI evidence JSON")
    ap.add_argument("--student-id", required=True, help="Student identifier")
    ap.add_argument(
        "--challenge",
        type=Path,
        default=None,
        help="Challenge YAML path (default: artifacts/anti_ai/challenge_<student-id>.yaml)",
    )
    ap.add_argument(
        "--pcap",
        type=Path,
        action="append",
        default=[],
        help="Capture file path (repeatable)",
    )
    ap.add_argument("--report", type=Path, default=None, help="Optional markdown report path")
    ap.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output evidence JSON (default: artifacts/anti_ai/evidence_<student-id>.json)",
    )
    return ap.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    student_id = str(args.student_id).strip()
    if not student_id:
        print("[ERROR] --student-id cannot be empty")
        return 2

    challenge = args.challenge or (Path("artifacts") / "anti_ai" / f"challenge_{student_id}.yaml")
    if not challenge.exists():
        print(f"[ERROR] Challenge not found: {challenge}")
        return 2

    try:
        ch_obj = yaml.safe_load(challenge.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"[ERROR] Failed to read challenge YAML: {exc}")
        return 2

    pcaps = [Path(p) for p in args.pcap]
    if not pcaps:
        print("[ERROR] Provide at least one capture with --pcap")
        return 2

    missing = [str(p) for p in pcaps if not p.exists()]
    if missing:
        print("[ERROR] The following capture files do not exist:")
        for m in missing:
            print(f"  - {m}")
        return 2

    if args.report and not args.report.exists():
        print(f"[ERROR] Report file does not exist: {args.report}")
        return 2

    output = args.output or (Path("artifacts") / "anti_ai" / f"evidence_{student_id}.json")
    output.parent.mkdir(parents=True, exist_ok=True)

    sha_map: Dict[str, str] = {}
    for p in pcaps:
        sha_map[str(p)] = _sha256_file(p)
    if args.report:
        sha_map[str(args.report)] = _sha256_file(args.report)

    evidence: Dict[str, Any] = {
        "meta": {
            "week": int(ch_obj.get("week", 12)),
            "student_id": student_id,
            "generated_at_utc": _utc_now_iso(),
            "challenge_path": str(challenge),
        },
        "artifacts": {
            "pcaps": [str(p) for p in pcaps],
            "report": str(args.report) if args.report else None,
            "sha256": sha_map,
        },
        "environment": {
            "fingerprint_sha256": _fingerprint(),
        },
    }

    output.write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    print(f"Evidence written to: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
