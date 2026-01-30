#!/usr/bin/env python3
"""
Minimal environment fingerprinting.

This is intentionally privacy-aware: we do not collect usernames, MAC addresses
or raw command output. We hash a small set of platform signals so that
submissions can record that they were produced on a real system.

Important
---------
A fingerprint is not identity proof. It is a lightweight friction mechanism
that supports audit trails and reduces low-effort reuse.
"""

from __future__ import annotations

import hashlib
import os
import platform
import subprocess
import sys
from dataclasses import dataclass
from typing import Dict, Optional


def _safe_run(cmd: list[str], timeout: int = 3) -> str:
    """Run a command and return a trimmed string output or an empty string."""
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if res.returncode != 0:
            return ""
        return (res.stdout or "").strip()
    except Exception:
        return ""


def _is_wsl() -> bool:
    if os.path.exists("/proc/sys/fs/binfmt_misc/WSLInterop"):
        return True
    if "WSL_DISTRO_NAME" in os.environ:
        return True
    try:
        with open("/proc/version", "r", encoding="utf-8") as f:
            return "microsoft" in f.read().lower()
    except OSError:
        return False


@dataclass(frozen=True)
class Fingerprint:
    """Hashed platform fingerprint and the unhashed inputs used to generate it."""

    fingerprint_sha256: str
    inputs: Dict[str, str]


def compute_fingerprint() -> Fingerprint:
    """Compute a minimal, hashed environment fingerprint."""
    inputs: Dict[str, str] = {
        "platform": platform.platform(),
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "wsl": "yes" if _is_wsl() else "no",
    }

    # Optional signals (safe to omit if unavailable)
    uname = _safe_run(["uname", "-a"])
    if uname:
        inputs["uname"] = uname

    docker_ver = _safe_run(["docker", "--version"])
    if docker_ver:
        inputs["docker"] = docker_ver

    payload = "\n".join(f"{k}={v}" for k, v in sorted(inputs.items()))
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return Fingerprint(fingerprint_sha256=digest, inputs=inputs)
