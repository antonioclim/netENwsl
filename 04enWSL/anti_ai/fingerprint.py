#!/usr/bin/env python3
"""anti_ai.fingerprint

Collects a privacy-aware environment fingerprint.

This is not a device identifier in the legal sense. It is a coarse hash designed to:
- give the marker a way to spot obvious artefact reuse
- avoid collecting sensitive personal data

The output is a SHA-256 hash of a small set of environment facts.
"""

from __future__ import annotations

import hashlib
import platform
import socket
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Optional


@dataclass(frozen=True)
class Fingerprint:
    created_at_utc: str
    python_version: str
    platform: str
    hostname_hash: str
    fingerprint_sha256: str


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def collect_fingerprint(extra_salt: str = "") -> Fingerprint:
    created = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    pyver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    plat = platform.platform()

    hostname = socket.gethostname().encode("utf-8", errors="replace")
    hostname_hash = _sha256_hex(hostname)[:16]  # short hash, enough for correlation without disclosure

    # Fingerprint hash is stable for the environment and independent of exact time.
    raw = (pyver + "\n" + plat + "\n" + hostname_hash + "\n" + extra_salt).encode("utf-8")
    fp = _sha256_hex(raw)

    return Fingerprint(
        created_at_utc=created,
        python_version=pyver,
        platform=plat,
        hostname_hash=hostname_hash,
        fingerprint_sha256=fp,
    )


def as_dict(fp: Fingerprint) -> Dict[str, str]:
    return {
        "created_at_utc": fp.created_at_utc,
        "python_version": fp.python_version,
        "platform": fp.platform,
        "hostname_hash": fp.hostname_hash,
        "fingerprint_sha256": fp.fingerprint_sha256,
    }
