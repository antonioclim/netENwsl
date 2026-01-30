"""Week 13 anti-AI tooling.

This package provides a small challenge–evidence–validator workflow designed to make
submissions depend on real execution artefacts rather than purely textual answers.

It is intentionally lightweight so it can run in WSL, Linux and CI.
"""

from __future__ import annotations

__all__ = [
    "challenge_generator",
    "evidence_collector",
    "submission_validator",
]
