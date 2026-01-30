#!/usr/bin/env python3
"""Compute a minimal environment fingerprint.

This is used as supporting evidence for Week 1 anti-AI checks. It intentionally
avoids collecting personal identifiers. The returned hash is derived from a
small set of platform signals and command outputs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any, Optional


def _run_optional_command(cmd: list[str], timeout: int = 3) -> Optional[str]:
    """Run a command and return stdout if it succeeds.

    The result is intended to be hashed, not stored as raw content.
    """
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if res.returncode == 0:
            out = res.stdout.strip()
            return out or None
        return None
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return None


def _bool_to_str(value: bool) -> str:
    return "yes" if value else "no"


def is_wsl() -> bool:
    """Best-effort check for WSL."""
    try:
        if "WSL_DISTRO_NAME" in dict(**__import__("os").environ):
            return True
    except Exception:
        pass
    try:
        with open("/proc/version", encoding="utf-8") as f:
            v = f.read().lower()
        return "microsoft" in v or "wsl" in v
    except (FileNotFoundError, OSError):
        return False


def collect_features() -> dict[str, Any]:
    """Collect minimal, low-sensitivity features."""
    py = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    docker_ver = _run_optional_command(["docker", "--version"], timeout=3)
    ip_ver = _run_optional_command(["ip", "-V"], timeout=3)

    # NOTE: We do not include hostname, MAC addresses or user names.
    return {
        "python": py,
        "platform": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "wsl": _bool_to_str(is_wsl()),
        "docker": bool(docker_ver),
        "ip_cmd": bool(ip_ver),
    }


def fingerprint_hash(features: dict[str, Any]) -> str:
    """Compute a stable hash from the provided features."""
    raw = json.dumps(features, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def build_fingerprint(include_features: bool = False) -> dict[str, Any]:
    """Build fingerprint payload.

    Args:
        include_features: Whether to include the raw feature dictionary.

    Returns:
        Dictionary containing a short hash, timestamp and optionally features.
    """
    features = collect_features()
    full_hash = fingerprint_hash(features)
    payload: dict[str, Any] = {
        "fingerprint_hash": full_hash[:16],
        "computed_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    if include_features:
        payload["features"] = features
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute a minimal environment fingerprint")
    parser.add_argument("--json", action="store_true", help="Print JSON output")
    parser.add_argument("--features", action="store_true", help="Include feature fields")
    args = parser.parse_args()

    fp = build_fingerprint(include_features=args.features)

    if args.json:
        print(json.dumps(fp, indent=2))
    else:
        print(fp["fingerprint_hash"])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
