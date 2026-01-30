"""Privacy-aware environment fingerprinting.

The goal is to reduce artefact reuse between students and attempts without
collecting sensitive personal data. The function below hashes a small set of
high-level environment characteristics. It is not a device identifier and it
should not be used for tracking outside the scope of this course.
"""

from __future__ import annotations

import hashlib
import os
import platform
import sys
from typing import Dict


def fingerprint_material() -> Dict[str, str]:
    """Return a small dictionary of non-sensitive environment fields."""
    return {
        "platform": platform.platform(),
        "python": sys.version.split()[0],
        "machine": platform.machine(),
        "wsl": "1" if os.environ.get("WSL_DISTRO_NAME") else "0",
        "kernel": platform.release(),
    }


def fingerprint_hash() -> str:
    """Return a short SHA256 digest of the environment fingerprint material."""
    material = fingerprint_material()
    canonical = "\n".join(f"{k}={material[k]}" for k in sorted(material))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
