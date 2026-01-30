#!/usr/bin/env python3
"""Issue a Week 13 anti-AI challenge.

This is a thin wrapper around :mod:`anti_ai.challenge_generator` so students can use a single,
consistent entry point from the scripts directory.
"""

from __future__ import annotations

from anti_ai.challenge_generator import main


if __name__ == "__main__":
    raise SystemExit(main())
