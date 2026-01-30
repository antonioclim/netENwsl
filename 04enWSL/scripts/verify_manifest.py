#!/usr/bin/env python3
"""
Manifest Checksum Verification — Week 4

Maintains a SHA-256 checksum manifest for the laboratory kit.

Why this exists:
- to detect accidental or unauthorised modifications in distributed teaching material
- to support CI and pre-commit checks

The manifest intentionally ignores directories that students are expected to modify:
- artifacts/
- pcap/ (captures are typically stored here)
- homework/solutions/

Usage:
  python scripts/verify_manifest.py           # verify against manifest.json
  python scripts/verify_manifest.py --update  # regenerate manifest.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


PROJECT_ROOT = Path(__file__).parent.parent
DEFAULT_MANIFEST = PROJECT_ROOT / "manifest.json"

EXCLUDE_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "artifacts",
    "pcap",
    "homework/solutions",
}


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _is_excluded(rel_path: str) -> bool:
    # Normalise to forward slashes
    rp = rel_path.replace("\\", "/")
    if rp == "manifest.json":
        return True
    for ex in EXCLUDE_DIRS:
        ex_norm = ex.replace("\\", "/").rstrip("/")
        if rp == ex_norm or rp.startswith(ex_norm + "/"):
            return True
    return False


def iter_files() -> List[str]:
    files: List[str] = []
    for p in PROJECT_ROOT.rglob("*"):
        if not p.is_file():
            continue
        rel = str(p.relative_to(PROJECT_ROOT))
        if _is_excluded(rel):
            continue
        files.append(rel)
    return sorted(files)


def build_manifest() -> Dict[str, object]:
    entries: Dict[str, Dict[str, object]] = {}
    for rel in iter_files():
        p = PROJECT_ROOT / rel
        entries[rel] = {
            "sha256": _sha256_file(p),
            "size_bytes": p.stat().st_size,
        }
    return {
        "schema": "week4-manifest-v1",
        "created_at_utc": _utc_now_iso(),
        "entries": entries,
    }


def verify_manifest(manifest: Dict[str, object]) -> Tuple[bool, List[str]]:
    errors: List[str] = []

    if manifest.get("schema") != "week4-manifest-v1":
        errors.append("Unsupported manifest schema")
        return False, errors

    entries = manifest.get("entries")
    if not isinstance(entries, dict):
        errors.append("Manifest entries missing or invalid")
        return False, errors

    # Verify all entries
    for rel, meta in entries.items():
        p = PROJECT_ROOT / rel
        if not p.exists():
            errors.append(f"Missing file: {rel}")
            continue
        if not isinstance(meta, dict) or "sha256" not in meta:
            errors.append(f"Invalid manifest entry: {rel}")
            continue
        expected = meta["sha256"]
        actual = _sha256_file(p)
        if actual != expected:
            errors.append(f"Checksum mismatch: {rel}")

    # Detect new files that should be tracked
    tracked = set(entries.keys())
    current = set(iter_files())
    new = sorted(current - tracked)
    if new:
        errors.append("Untracked files (run --update): " + ", ".join(new[:10]) + (" ..." if len(new) > 10 else ""))

    return not errors, errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify or update the kit checksum manifest")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST), help="Manifest path (default: manifest.json)")
    parser.add_argument("--update", action="store_true", help="Regenerate manifest file")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)

    if args.update:
        manifest = build_manifest()
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
        print(f"Wrote manifest: {manifest_path}")
        print(f"Tracked {len(manifest['entries'])} file(s)")
        return 0

    if not manifest_path.exists():
        print(f"ERROR: manifest not found: {manifest_path}")
        print("Run: python scripts/verify_manifest.py --update")
        return 1

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    ok, errs = verify_manifest(manifest)
    if ok:
        print("✓ manifest verification passed")
        return 0

    print("✗ manifest verification failed:")
    for e in errs:
        print(f"  - {e}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
