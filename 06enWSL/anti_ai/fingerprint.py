#!/usr/bin/env python3
"""Privacy-aware environment fingerprinting.

This module intentionally avoids collecting raw identifiers in evidence.
It produces a short hash derived from a small set of properties.

Rationale
- The goal is to reduce naive replay between students and attempts.
- It is not a device identifier and it must not be treated as such.
"""

from __future__ import annotations

import getpass
import hashlib
import platform
import socket
from typing import Optional


def compute_fingerprint_hash(salt: Optional[str] = None) -> str:
    items = [
        platform.system(),
        platform.release(),
        platform.machine(),
        platform.python_version(),
        socket.gethostname(),
        getpass.getuser(),
    ]
    base = "|".join(items)
    if salt:
        base = f"{salt}|{base}"
    return hashlib.sha256(base.encode("utf-8")).hexdigest()[:16]
