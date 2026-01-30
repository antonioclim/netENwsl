"""
Environment fingerprinting helpers.

The goal is not surveillance. The goal is practical provenance:
record enough context to help an instructor verify that artefacts were
generated in the intended environment and time window.
"""

from __future__ import annotations

import os
import platform
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class EnvironmentFingerprint:
    created_at_utc: str
    python_version: str
    python_executable: str
    platform: str
    machine: str
    processor: str
    hostname: str
    user: str

    @classmethod
    def collect(cls) -> "EnvironmentFingerprint":
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        return cls(
            created_at_utc=now,
            python_version=sys.version.replace("\n", " "),
            python_executable=sys.executable,
            platform=platform.platform(),
            machine=platform.machine(),
            processor=platform.processor(),
            hostname=platform.node(),
            user=os.environ.get("USER") or os.environ.get("USERNAME") or "",
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def resolve_project_root(start: Path | None = None) -> Path:
    """Locate the repository root by walking upwards until pyproject.toml is found."""
    cur = (start or Path.cwd()).resolve()
    for _ in range(12):
        if (cur / "pyproject.toml").exists():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return (start or Path.cwd()).resolve()
