# ═══════════════════════════════════════════════════════════════════════════════
# MODULE_DOCSTRING
# ═══════════════════════════════════════════════════════════════════════════════
"""Network utility helpers for Week 12.

The kit uses several local services (SMTP, JSON-RPC, XML-RPC and gRPC). These
helpers provide small, dependency-free building blocks for:

- checking whether a TCP port is listening
- waiting for a service to start
- selecting a free port for ad-hoc experiments

All text is written in British English.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import socket
import time
from contextlib import closing
from dataclasses import dataclass


@dataclass(frozen=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PORTCHECK_CLASS
# ═══════════════════════════════════════════════════════════════════════════════
class PortCheck:
    host: str
    port: int
    is_listening: bool
    error: str | None = None



# ═══════════════════════════════════════════════════════════════════════════════
# IS_PORT_LISTENING_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def is_port_listening(host: str, port: int, timeout_s: float = 0.5) -> PortCheck:
    """Return whether *host:port* accepts TCP connections."""
    try:
        with socket.create_connection((host, port), timeout=timeout_s):
            return PortCheck(host=host, port=port, is_listening=True)
    except OSError as exc:
        return PortCheck(host=host, port=port, is_listening=False, error=str(exc))



# ═══════════════════════════════════════════════════════════════════════════════
# WAIT_FOR_PORT_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def wait_for_port(host: str, port: int, timeout_s: float = 5.0, poll_s: float = 0.1) -> bool:
    """Wait until *host:port* is listening, up to *timeout_s* seconds."""
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        if is_port_listening(host, port).is_listening:
            return True
        time.sleep(poll_s)
    return False



# ═══════════════════════════════════════════════════════════════════════════════
# FIND_FREE_PORT_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def find_free_port(host: str = "127.0.0.1") -> int:
    """Ask the OS for an ephemeral free port and return it."""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind((host, 0))
        return int(s.getsockname()[1])

if __name__ == "__main__":
    # Module loaded directly - display module info
    print(f"Module {__name__} loaded successfully.")
    print(f"This module provides utility functions for the networking laboratory.")
