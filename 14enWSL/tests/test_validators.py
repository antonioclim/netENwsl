#!/usr/bin/env python3
"""Unit tests for validation utilities.

NETWORKING class — ASE, CSIE | Computer Networks Laboratory
by ing. dr. Antonio Clim

Tests for IP address, port range and container name validation functions.
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path
from typing import Optional, Tuple

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATION_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def validate_ip_address(ip: str) -> Tuple[bool, Optional[str]]:
    """Validate an IPv4 address."""
    if not ip or not isinstance(ip, str):
        return False, "IP address cannot be empty"

    parts = ip.split(".")
    if len(parts) != 4:
        return False, f"Expected 4 octets, got {len(parts)}"

    for i, part in enumerate(parts):
        try:
            value = int(part)
            if value < 0 or value > 255:
                return False, f"Octet {i+1} out of range: {value}"
            if part != str(value):
                return False, f"Invalid octet format: {part}"
        except ValueError:
            return False, f"Non-numeric octet: {part}"
    return True, None


def validate_port_range(port: int, allow_privileged: bool = False) -> Tuple[bool, Optional[str]]:
    """Validate a port number."""
    if not isinstance(port, int):
        return False, "Port must be an integer"
    if port < 1 or port > 65535:
        return False, f"Port {port} out of valid range (1-65535)"
    if not allow_privileged and port < 1024:
        return False, f"Port {port} is privileged (use allow_privileged=True)"
    if port == 9000:
        return False, f"Port {port} is reserved for system services"
    return True, None


def validate_container_name(name: str) -> Tuple[bool, Optional[str]]:
    """Validate a Docker container name."""
    if not name or not isinstance(name, str):
        return False, "Container name cannot be empty"
    if len(name) > 128:
        return False, f"Name too long: {len(name)} chars (max 128)"
    pattern = r"^[a-zA-Z0-9][a-zA-Z0-9_.-]*$"
    if not re.match(pattern, name):
        return False, "Name must start with alphanumeric"
    return True, None


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_CASES
# ═══════════════════════════════════════════════════════════════════════════════
class TestIPAddressValidation(unittest.TestCase):
    """Tests for IP address validation."""

    def test_valid_ip_addresses(self) -> None:
        valid_ips = ["192.168.1.1", "10.0.0.1", "172.20.0.2", "0.0.0.0", "255.255.255.255", "127.0.0.1"]
        for ip in valid_ips:
            is_valid, error = validate_ip_address(ip)
            self.assertTrue(is_valid, f"{ip} should be valid, got: {error}")

    def test_invalid_ip_addresses(self) -> None:
        invalid_ips = [("", "empty"), ("192.168.1", "few octets"), ("256.1.1.1", "octet > 255")]
        for ip, reason in invalid_ips:
            is_valid, _ = validate_ip_address(ip)
            self.assertFalse(is_valid, f"{ip} ({reason}) should be invalid")


class TestPortValidation(unittest.TestCase):
    """Tests for port number validation."""

    def test_valid_ports(self) -> None:
        valid_ports = [1024, 8080, 8001, 65535, 3000]
        for port in valid_ports:
            is_valid, error = validate_port_range(port)
            self.assertTrue(is_valid, f"Port {port} should be valid, got: {error}")

    def test_invalid_ports(self) -> None:
        for port in [0, -1, 65536, 100000]:
            is_valid, _ = validate_port_range(port)
            self.assertFalse(is_valid, f"Port {port} should be invalid")

    def test_reserved_port(self) -> None:
        is_valid, error = validate_port_range(9000)
        self.assertFalse(is_valid)
        self.assertIn("reserved", error.lower())


class TestContainerNameValidation(unittest.TestCase):
    """Tests for container name validation."""

    def test_valid_names(self) -> None:
        for name in ["week14_app1", "my-container", "A1"]:
            is_valid, error = validate_container_name(name)
            self.assertTrue(is_valid, f"'{name}' should be valid, got: {error}")

    def test_invalid_names(self) -> None:
        for name, reason in [("", "empty"), ("_container", "starts with underscore")]:
            is_valid, _ = validate_container_name(name)
            self.assertFalse(is_valid, f"'{name}' ({reason}) should be invalid")


if __name__ == "__main__":
    unittest.main(verbosity=2)
