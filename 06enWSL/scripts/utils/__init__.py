#!/usr/bin/env python3
"""
Utility Package — Week 6: NAT/PAT & SDN Laboratory
==================================================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

This package provides common utilities for laboratory scripts:
- Logging configuration and progress tracking
- Docker/container management
- File and path utilities

Usage:
    from scripts.utils import setup_logger, DockerManager
    from scripts.utils.logger import ProgressLogger
"""

from __future__ import annotations

from typing import TYPE_CHECKING

# Explicit exports for type checkers and IDE support
if TYPE_CHECKING:
    from .docker_utils import DockerManager
    from .logger import ProgressLogger, setup_logger, set_verbose

# Runtime imports
from .logger import ProgressLogger, setup_logger, set_verbose
from .docker_utils import DockerManager

__all__ = [
    # Logging utilities
    "setup_logger",
    "set_verbose", 
    "ProgressLogger",
    # Docker utilities
    "DockerManager",
]

__version__ = "1.0.2"
__author__ = "ing. dr. Antonio Clim"
