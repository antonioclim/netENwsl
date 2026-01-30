#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# MODULE_DOCSTRING
# ═══════════════════════════════════════════════════════════════════════════════
"""Issue a Week 12 anti-AI challenge.

This is a small wrapper around :mod:`anti_ai.challenge_generator`.

It exists so that students can run a single script from the project root without
needing to remember module paths.
"""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from anti_ai.challenge_generator import main


if __name__ == "__main__":
    raise SystemExit(main())
