"""Evidence collection for Week 8.

The evidence file is intended to be student-generated and committed together
with the required artefacts (pcap files and the student context).

The goal is not secrecy, it is friction: it makes copy and paste submissions
significantly less convenient.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from .files import sha256_file, safe_relpath
from .fingerprint import collect_environment_fingerprint, stable_fingerprint_id


SCHEMA_VERSION = "networking.anti_ai.evidence.v1"


@dataclass
class EvidenceFile:
    path: str
    sha256: str
    size_bytes: int
    mtime_utc: str


def _file_entry(path: Path, base: Path) -> EvidenceFile:
    st = path.stat()
    return EvidenceFile(
        path=safe_relpath(path, base),
        sha256=sha256_file(path),
        size_bytes=int(st.st_size),
        mtime_utc=datetime.fromtimestamp(st.st_mtime, tz=timezone.utc).isoformat(),
    )


def collect_evidence(
    *,
    project_root: Path,
    required_paths: List[Path],
    context_file: Path,
    output_path: Path,
    extra_notes: Optional[str] = None,
) -> Dict[str, Any]:
    """Collect hashes and basic metadata for required artefacts."""

    fp = collect_environment_fingerprint()
    now = datetime.now(timezone.utc).isoformat()

    artefacts: List[EvidenceFile] = []
    missing: List[str] = []

    # Always include student context if present
    if context_file.exists():
        artefacts.append(_file_entry(context_file, project_root))
    else:
        missing.append(safe_relpath(context_file, project_root))

    for p in required_paths:
        if p.exists():
            artefacts.append(_file_entry(p, project_root))
        else:
            missing.append(safe_relpath(p, project_root))

    payload: Dict[str, Any] = {
        "schema": SCHEMA_VERSION,
        "created_at_utc": now,
        "fingerprint": fp.as_dict(),
        "fingerprint_id": stable_fingerprint_id(fp),
        "artefacts": [asdict(a) for a in artefacts],
        "missing": missing,
        "notes": extra_notes or "",
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload