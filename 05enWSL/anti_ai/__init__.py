"""
Week 5 anti-AI utilities.

This package provides a small, auditable toolchain:

- challenge generation (individualised input data and tokens)
- evidence collection (hashes and minimal environment fingerprint)
- submission validation (automatic checks that match the challenge)

It is designed to be self-contained and to run on standard Python 3.10+.
"""

from __future__ import annotations

__all__ = [
    "__version__",
]

__version__ = "1.0.0"
