"""Environment fingerprinting.

The purpose of a fingerprint is not to uniquely identify a person but to
capture enough run-time context to make replay attacks less convenient.

All data collected here is local to the student's machine and can be removed
by deleting the produced evidence file.
"""

from __future__ import annotations

import hashlib
import os
import platform
import socket
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict


@dataclass(frozen=True)
class EnvironmentFingerprint:
    """A minimal run-time fingerprint."""

    created_at_utc: str
    python_version: str
    platform: str
    machine: str
    hostname: str
    user: str

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


def collect_environment_fingerprint() -> EnvironmentFingerprint:
    """Collect a small amount of environment metadata."""
    now = datetime.now(timezone.utc).isoformat()
    return EnvironmentFingerprint(
        created_at_utc=now,
        python_version=sys.version.split()[0],
        platform=platform.platform(),
        machine=platform.machine(),
        hostname=socket.gethostname(),
        user=os.environ.get("USER") or os.environ.get("USERNAME") or "unknown",
    )


def stable_fingerprint_id(fp: EnvironmentFingerprint) -> str:
    """Return a stable identifier for a collected fingerprint.

    This is a hash of the fingerprint contents so we do not need to store
    anything more sensitive than the metadata itself.
    """

    payload = "|".join(
        [
            fp.python_version,
            fp.platform,
            fp.machine,
            fp.hostname,
            fp.user,
        ]
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:16]
