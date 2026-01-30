#!/usr/bin/env python3
"""Privacy-aware environment fingerprint.

The goal is not device tracking. The goal is a lightweight binding between the
produced artefacts and the execution environment so that submissions are harder
to swap between students.

The fingerprint is deliberately *minimised*:
- we hash the collected fields
- we do not store raw host identifiers in the evidence file
"""

from __future__ import annotations

import getpass
import platform
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from anti_ai.challenge import sha256_hex


@dataclass(frozen=True, slots=True)
class Fingerprint:
    """A minimal hashed fingerprint."""

    hash_hex: str
    fields: dict[str, Any]


def compute_fingerprint(extra: dict[str, Any] | None = None) -> Fingerprint:
    """Compute a privacy-aware fingerprint.

    The returned object includes the raw fields in memory for debugging, but
    callers should write only the hash to disk unless they have a very strong
    justification.
    """
    extra = extra or {}

    fields: dict[str, Any] = {
        "user": getpass.getuser(),
        "node": platform.node(),
        "system": platform.system(),
        "release": platform.release(),
        "python": platform.python_version(),
    }

    # Include path-based variation if provided (useful in CI and WSL setups)
    if "cwd" not in extra:
        fields["cwd"] = str(Path.cwd())

    fields.update(extra)

    # Hash the canonical representation
    # We deliberately avoid storing the raw fields in evidence by default.
    import json

    canon = json.dumps(fields, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return Fingerprint(hash_hex=sha256_hex(canon), fields=fields)
