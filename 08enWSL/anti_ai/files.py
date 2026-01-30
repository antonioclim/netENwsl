"""File helpers used across anti-AI tooling."""

from __future__ import annotations

import hashlib
from pathlib import Path


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    """Compute SHA-256 of a file without loading it fully into memory."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def safe_relpath(path: Path, base: Path) -> str:
    """Return a POSIX-like relative path, falling back to the name."""
    try:
        return path.relative_to(base).as_posix()
    except Exception:
        return path.name
