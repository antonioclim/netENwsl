#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# MODULE_DOCSTRING
# ═══════════════════════════════════════════════════════════════════════════════
"""Validate Week 12 anti-AI evidence.

This is a convenience wrapper around :mod:`anti_ai.validator`.
"""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from anti_ai.validator import main


if __name__ == "__main__":
    raise SystemExit(main())
