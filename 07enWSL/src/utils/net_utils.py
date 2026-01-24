"""Utility helpers for Week 7 scripts.

This module aims to keep dependencies minimal and behaviour predictable.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import os
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional


@dataclass(frozen=True)


# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class CmdResult:
    argv: list[str]
    returncode: int
    stdout: str
    stderr: str



# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
def run_cmd(argv: Iterable[str], timeout: Optional[int] = None, check: bool = False, cwd: Optional[Path] = None) -> CmdResult:
    argv_list = list(argv)
    proc = subprocess.run(
        argv_list,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
        cwd=str(cwd) if cwd else None,
    )
    res = CmdResult(argv=argv_list, returncode=proc.returncode, stdout=proc.stdout, stderr=proc.stderr)
    if check and res.returncode != 0:
        raise RuntimeError(f"Command failed: {shlex.join(argv_list)}\nstdout:\n{res.stdout}\nstderr:\n{res.stderr}")
    return res



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def is_root() -> bool:
    return os.geteuid() == 0

if __name__ == "__main__":
    # Module loaded directly - display module info
    print(f"Module {__name__} loaded successfully.")
    print(f"This module provides utility functions for the networking laboratory.")
