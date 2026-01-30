#!/usr/bin/env python3
"""Validate Week 8 anti-AI submission.

This is a thin wrapper around `anti_ai.submission_validator`.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure repository root is on sys.path when running as a script
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from anti_ai.submission_validator import main


if __name__ == "__main__":
    raise SystemExit(main())
