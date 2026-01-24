"""
Scripts Utilities Package — Week 3 Laboratory
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

This package provides utility modules for the laboratory scripts.

Modules:
    docker_utils: Docker container and compose management
    network_utils: Network testing and verification utilities
    logger: Logging configuration with colour support
"""

from .docker_utils import DockerManager
from .network_utils import NetworkUtils, check_port_open, tcp_echo_test
from .logger import setup_logger, get_logger
from typing import Optional, List, Dict, Tuple, Any

__all__ = [
    'DockerManager',
    'NetworkUtils',
    'check_port_open',
    'tcp_echo_test',
    'setup_logger',
    'get_logger',
]
