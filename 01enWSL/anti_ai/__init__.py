"""Week 1 anti-AI utilities.

This package implements a small challenge–evidence–validator workflow that:

- creates per-student challenges (tokens, payloads, parameters)
- collects evidence and hashes submitted artefacts
- validates that submitted artefacts contain the required proofs

The goal is not to prohibit AI tools. The goal is to ensure that AI alone is
insufficient for a valid submission.
"""

from __future__ import annotations

__all__ = [
    "challenge_generator",
    "evidence_collector",
    "fingerprint",
    "pcap_tools",
    "submission_validator",
]
