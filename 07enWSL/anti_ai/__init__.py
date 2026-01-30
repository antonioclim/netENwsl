"""Anti-AI utilities for Week 7.

This package provides a lightweight challenge–evidence–validation workflow.
It is designed to make generative AI insufficient on its own by requiring
environment-derived artefacts such as packet captures and reproducible hashes.
"""

from __future__ import annotations

__all__ = [
    "challenge_generator",
    "evidence_collector",
    "submission_validator",
]
