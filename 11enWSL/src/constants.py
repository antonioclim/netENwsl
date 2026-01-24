#!/usr/bin/env python3
"""
constants.py — Centralised Constants for Week 11 Lab Kit
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim
"""
from __future__ import annotations
import os
from pathlib import Path
from typing import Tuple, Final

# PROJECT PATHS
PROJECT_ROOT: Final[Path] = Path(__file__).parent.parent
DOCKER_DIR: Final[Path] = PROJECT_ROOT / "docker"
DOCS_DIR: Final[Path] = PROJECT_ROOT / "docs"
FORMATIVE_DIR: Final[Path] = PROJECT_ROOT / "formative"

# NETWORK DEFAULTS
DEFAULT_LISTEN_HOST: Final[str] = "0.0.0.0"
LOCALHOST: Final[str] = "127.0.0.1"
DEFAULT_LISTEN_PORT: Final[int] = 8080
BACKEND_PORT_1: Final[int] = 8081
BACKEND_PORT_2: Final[int] = 8082
BACKEND_PORT_3: Final[int] = 8083
DEFAULT_BACKEND_PORTS: Final[Tuple[int, ...]] = (BACKEND_PORT_1, BACKEND_PORT_2, BACKEND_PORT_3)
PORTAINER_PORT: Final[int] = 9000

# PROTOCOL PORTS (Standard)
FTP_CONTROL_PORT: Final[int] = 21
FTP_DATA_PORT: Final[int] = 20
SSH_PORT: Final[int] = 22
DNS_PORT: Final[int] = 53
HTTP_PORT: Final[int] = 80
HTTPS_PORT: Final[int] = 443

# TIMEOUTS (seconds)
SOCKET_TIMEOUT: Final[float] = 2.5
HEALTH_CHECK_INTERVAL: Final[float] = 10.0
FAIL_TIMEOUT: Final[float] = 10.0
DOCKER_STARTUP_TIMEOUT: Final[float] = 30.0

# LOAD BALANCER SETTINGS
ALGORITHM_ROUND_ROBIN: Final[str] = "rr"
ALGORITHM_LEAST_CONN: Final[str] = "least_conn"
ALGORITHM_IP_HASH: Final[str] = "ip_hash"
DEFAULT_ALGORITHM: Final[str] = ALGORITHM_ROUND_ROBIN
VALID_ALGORITHMS: Final[Tuple[str, ...]] = (ALGORITHM_ROUND_ROBIN, ALGORITHM_LEAST_CONN, ALGORITHM_IP_HASH)
MAX_FAILS_DEFAULT: Final[int] = 1

# DOCKER CONFIGURATION
DOCKER_NETWORK_NAME: Final[str] = "s11_network"
CONTAINER_NGINX: Final[str] = "s11_nginx_lb"
ALL_LAB_CONTAINERS: Final[Tuple[str, ...]] = (
    CONTAINER_NGINX, "s11_backend_1", "s11_backend_2", "s11_backend_3"
)

# BUFFER SIZES (bytes)
BUFFER_SIZE: Final[int] = 4096
CRLF: Final[bytes] = b"\r\n"
HEADER_END: Final[bytes] = b"\r\n\r\n"

# VALIDATION LIMITS
MIN_USER_PORT: Final[int] = 1024
MAX_PORT: Final[int] = 65535
QUIZ_MIN_PASSING_SCORE: Final[int] = 70


def get_env_or_default(var_name: str, default: str) -> str:
    """Get environment variable or return default."""
    return os.getenv(var_name, default)


def get_backend_url(port: int, host: str = LOCALHOST) -> str:
    """Construct backend URL from host and port."""
    return f"http://{host}:{port}"


__all__ = [
    "PROJECT_ROOT", "DEFAULT_LISTEN_HOST", "DEFAULT_LISTEN_PORT",
    "DEFAULT_BACKEND_PORTS", "LOCALHOST", "FTP_CONTROL_PORT", "DNS_PORT",
    "SSH_PORT", "SOCKET_TIMEOUT", "HEALTH_CHECK_INTERVAL", "FAIL_TIMEOUT",
    "DEFAULT_ALGORITHM", "VALID_ALGORITHMS", "MAX_FAILS_DEFAULT",
    "DOCKER_NETWORK_NAME", "ALL_LAB_CONTAINERS", "BUFFER_SIZE", "CRLF",
    "MIN_USER_PORT", "MAX_PORT", "get_env_or_default", "get_backend_url",
]
