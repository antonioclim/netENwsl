"""Anti-AI support utilities for Week 8.

This package provides a small, dependency-free workflow that makes it difficult
to submit fabricated artefacts without running the laboratory activities.

Design goals:
  - Student-specific parameters (seeded context)
  - Evidence capture (hashes and timestamps)
  - Offline validation (no Wireshark or tshark required)

The tooling is intentionally lightweight so it can run in WSL and in CI.
"""

from __future__ import annotations

__all__ = [
    "__version__",
]

__version__ = "1.0.0"
