"""Privacy‑aware environment fingerprint.

The purpose of the fingerprint is not to uniquely identify a student.
It is a lightweight, low‑risk signal that binds evidence to a runtime environment.

We store a SHA‑256 hash of a small set of non‑sensitive fields.
"""

from __future__ import annotations

import getpass
import hashlib
import os
import platform
import socket
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Fingerprint:
    platform: str
    python_version: str
    user: str
    hostname: str
    kernel_release: str
    hash_sha256: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "platform": self.platform,
            "python_version": self.python_version,
            "user": self.user,
            "hostname": self.hostname,
            "kernel_release": self.kernel_release,
            "hash_sha256": self.hash_sha256,
        }


def _sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def compute_fingerprint() -> Fingerprint:
    plat = platform.platform()
    pyv = platform.python_version()
    user = getpass.getuser()
    host = socket.gethostname()
    kernel = platform.release()

    payload = "\n".join([plat, pyv, user, host, kernel])
    return Fingerprint(
        platform=plat,
        python_version=pyv,
        user=user,
        hostname=host,
        kernel_release=kernel,
        hash_sha256=_sha256_hex(payload),
    )
