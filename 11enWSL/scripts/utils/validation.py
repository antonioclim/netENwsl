#!/usr/bin/env python3
"""
validation.py — Input Validation Utilities for Week 11 Lab Kit
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim
"""
from __future__ import annotations

import re
import ipaddress
from pathlib import Path
from typing import List, Optional, Union, Any

MIN_USER_PORT = 1024
MAX_PORT = 65535
MAX_HOSTNAME_LENGTH = 253
MAX_PATH_LENGTH = 4096
MAX_INPUT_LENGTH = 256

_HOSTNAME_PATTERN = re.compile(
    r'^(?=.{1,253}$)(?!-)[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?'
    r'(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
)

_DANGEROUS_PATH_PATTERNS = ['..', '~', '$', '`', ';', '|', '&', '>', '<', '\x00']


def validate_port(port: Any, allow_privileged: bool = False) -> bool:
    """Validate that a value is a valid port number."""
    try:
        port_int = int(port)
    except (TypeError, ValueError):
        return False
    min_port = 1 if allow_privileged else MIN_USER_PORT
    return min_port <= port_int <= MAX_PORT


def validate_port_range(port: Any) -> bool:
    """Validate port is in user range (1024-65535)."""
    return validate_port(port, allow_privileged=False)


def validate_hostname(hostname: str) -> bool:
    """Validate that a string is a valid hostname or IP address."""
    if not hostname or not isinstance(hostname, str):
        return False
    if len(hostname) > MAX_HOSTNAME_LENGTH:
        return False
    if validate_ip_address(hostname):
        return True
    return bool(_HOSTNAME_PATTERN.match(hostname))


def validate_ip_address(ip: str) -> bool:
    """Validate that a string is a valid IP address (v4 or v6)."""
    if not ip or not isinstance(ip, str):
        return False
    if ip.startswith('[') and ip.endswith(']'):
        ip = ip[1:-1]
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def validate_path_safe(path: str) -> bool:
    """Validate that a path is safe (no traversal attacks)."""
    if not path or not isinstance(path, str):
        return False
    if len(path) > MAX_PATH_LENGTH:
        return False
    for pattern in _DANGEROUS_PATH_PATTERNS:
        if pattern in path:
            return False
    return True


def validate_path_exists(path: Union[str, Path]) -> bool:
    """Validate that a path exists and is accessible."""
    try:
        return Path(path).exists()
    except (OSError, ValueError):
        return False


def sanitize_user_input(text: str, max_length: int = MAX_INPUT_LENGTH,
                        allow_newlines: bool = False) -> str:
    """Sanitise user text input by removing control characters."""
    if not text or not isinstance(text, str):
        return ""
    allowed_whitespace = {'\t'}
    if allow_newlines:
        allowed_whitespace.add('\n')
    sanitised = ''.join(c for c in text if c.isprintable() or c in allowed_whitespace)
    return sanitised[:max_length]


def validate_algorithm(algo: str, valid_algorithms: Optional[List[str]] = None) -> bool:
    """Validate load balancing algorithm name."""
    if valid_algorithms is None:
        valid_algorithms = ["rr", "least_conn", "ip_hash"]
    return algo in valid_algorithms


def validate_backend_spec(spec: str) -> bool:
    """Validate backend specification (host:port format)."""
    if not spec or ':' not in spec:
        return False
    parts = spec.rsplit(':', 1)
    if len(parts) != 2:
        return False
    host, port_str = parts
    if not validate_hostname(host):
        return False
    try:
        return validate_port(int(port_str))
    except ValueError:
        return False


__all__ = [
    "validate_port", "validate_port_range", "validate_hostname",
    "validate_ip_address", "validate_path_safe", "validate_path_exists",
    "sanitize_user_input", "validate_algorithm", "validate_backend_spec",
]


if __name__ == "__main__":
    print("Running validation self-tests...")
    assert validate_port(8080) is True
    assert validate_port(80, allow_privileged=True) is True
    assert validate_port(80, allow_privileged=False) is False
    assert validate_hostname("localhost") is True
    assert validate_hostname("192.168.1.1") is True
    assert validate_path_safe("/home/user/file.txt") is True
    assert validate_path_safe("../../etc/passwd") is False
    assert validate_backend_spec("localhost:8081") is True
    print("✅ All validation tests passed!")
