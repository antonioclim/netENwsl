# ═══════════════════════════════════════════════════════════════════════════════
# MODULE_DOCSTRING
# ═══════════════════════════════════════════════════════════════════════════════
"""Common utilities for Week 12.

This package intentionally stays small. The Week 12 kit focuses on SMTP and RPC
protocols and most components are self-contained.

The utilities exported here are used by a handful of scripts and tests to:

- check whether a TCP port is listening
- wait for a local service to start
- obtain an ephemeral free port for local integration tests
"""

from __future__ import annotations

from .net_utils import PortCheck, find_free_port, is_port_listening, wait_for_port


def is_port_open(host: str, port: int, timeout_s: float = 0.5) -> bool:
    """Compatibility alias for older weeks and generic tooling."""

    return is_port_listening(host, port, timeout_s=timeout_s).is_listening


__all__ = [
    "PortCheck",
    "is_port_listening",
    "is_port_open",
    "wait_for_port",
    "find_free_port",
]
