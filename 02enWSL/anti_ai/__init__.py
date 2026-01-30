"""Anti‑AI utilities for Week 2.

The goal is not to ban AI tools. The goal is to require evidence of real execution
so that a language model alone is insufficient to produce a valid submission.

This package is designed to be self‑contained and to run on WSL2 without Docker.
"""

from __future__ import annotations

__all__ = [
    "challenge",
    "challenge_generator",
    "evidence_collector",
    "fingerprint",
    "proof_runner",
    "submission_validator",
]
