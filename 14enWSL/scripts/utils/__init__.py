"""Utility modules for Week 14 laboratory scripts.

NETWORKING class — ASE, CSIE | Computer Networks Laboratory
by ing. dr. Antonio Clim

This package provides shared utilities for Docker management,
network operations and logging.
"""

__all__ = ["DockerManager", "setup_logger", "check_port_open", "get_container_ip", "wait_for_port"]
__version__ = "2.0.0"
__author__ = "ing. dr. Antonio Clim"

# Lazy imports to avoid circular dependencies
def __getattr__(name):
    if name == "DockerManager":
        from scripts.utils.docker_utils import DockerManager
        return DockerManager
    elif name == "setup_logger":
        from scripts.utils.logger import setup_logger
        return setup_logger
    elif name in ("check_port_open", "get_container_ip", "wait_for_port"):
        from scripts.utils import network_utils
        return getattr(network_utils, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
