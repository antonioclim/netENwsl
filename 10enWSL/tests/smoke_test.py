#!/usr/bin/env python3
"""
Week 10 — Smoke Tests
=====================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

This script performs basic connectivity tests for all lab services.
Run this after starting the lab to verify everything is working.

Usage:
    python3 tests/smoke_test.py
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import socket
import subprocess
import sys
from dataclasses import dataclass
from typing import Callable, Tuple


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class ServiceTest:
    """Configuration for a single service test."""
    name: str
    host: str
    port: int
    protocol: str  # "tcp" or "udp"


SERVICES = [
    ServiceTest("Web Server (HTTP)", "localhost", 8000, "tcp"),
    ServiceTest("DNS Server", "localhost", 5353, "udp"),
    ServiceTest("SSH Server", "localhost", 2222, "tcp"),
    ServiceTest("FTP Server", "localhost", 2121, "tcp"),
]


# ═══════════════════════════════════════════════════════════════════════════════
# TCP_TESTS
# ═══════════════════════════════════════════════════════════════════════════════
def test_tcp_port(host: str, port: int, timeout: float = 5.0) -> Tuple[bool, str]:
    """
    Test if a TCP port is reachable.

    💭 PREDICTION: What error will we get if the service is not running?
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect((host, port))
            return True, "Connected"
    except socket.timeout:
        return False, "Timeout"
    except ConnectionRefusedError:
        return False, "Connection refused"
    except OSError as exc:
        return False, str(exc)


# ═══════════════════════════════════════════════════════════════════════════════
# UDP_TESTS
# ═══════════════════════════════════════════════════════════════════════════════
def build_minimal_dns_query() -> bytes:
    """Build a minimal DNS query packet for connectivity testing."""
    return bytes([
        0x00, 0x01,  # Transaction ID
        0x01, 0x00,  # Flags: standard query
        0x00, 0x01,  # Questions: 1
        0x00, 0x00,  # Answer RRs: 0
        0x00, 0x00,  # Authority RRs: 0
        0x00, 0x00,  # Additional RRs: 0
        0x04, 0x74, 0x65, 0x73, 0x74,  # "test"
        0x00,        # Root
        0x00, 0x01,  # Type: A
        0x00, 0x01,  # Class: IN
    ])


def test_udp_port(host: str, port: int, timeout: float = 5.0) -> Tuple[bool, str]:
    """
    Test if a UDP port is responsive (sends a minimal DNS query).

    💭 PREDICTION: Why might UDP tests be less reliable than TCP tests?
    """
    dns_query = build_minimal_dns_query()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(timeout)
            sock.sendto(dns_query, (host, port))
            data, _ = sock.recvfrom(512)
            return True, f"Received {len(data)} bytes"
    except socket.timeout:
        return False, "Timeout (no response)"
    except OSError as exc:
        return False, str(exc)


# ═══════════════════════════════════════════════════════════════════════════════
# HTTP_TESTS
# ═══════════════════════════════════════════════════════════════════════════════
def test_http_endpoint(url: str, timeout: float = 5.0) -> Tuple[bool, str]:
    """Test if an HTTP endpoint is responsive."""
    try:
        import urllib.request
        import urllib.error

        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return True, f"HTTP {response.status}"
    except urllib.error.HTTPError as exc:
        return True, f"HTTP {exc.code}"  # Server responded
    except urllib.error.URLError as exc:
        return False, str(exc.reason)
    except Exception as exc:
        return False, str(exc)


# ═══════════════════════════════════════════════════════════════════════════════
# DNS_TESTS
# ═══════════════════════════════════════════════════════════════════════════════
def test_dns_query(
    server: str, port: int, domain: str = "web.lab.local"
) -> Tuple[bool, str]:
    """
    Test DNS resolution using dig.

    💭 PREDICTION: What IP address will web.lab.local resolve to?
    """
    try:
        result = subprocess.run(
            ["dig", f"@{server}", "-p", str(port), domain, "+short", "+time=2"],
            capture_output=True,
            text=True,
            timeout=5,
        )

        if result.returncode == 0 and result.stdout.strip():
            return True, f"Resolved to {result.stdout.strip()}"
        return False, "No answer"
    except FileNotFoundError:
        return False, "dig not installed"
    except subprocess.TimeoutExpired:
        return False, "Timeout"


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_RUNNER
# ═══════════════════════════════════════════════════════════════════════════════
def run_service_test(service: ServiceTest) -> Tuple[bool, str]:
    """Run a single service test based on protocol."""
    if service.protocol == "tcp":
        return test_tcp_port(service.host, service.port)
    elif service.protocol == "udp":
        return test_udp_port(service.host, service.port)
    return False, f"Unknown protocol: {service.protocol}"


def print_test_result(name: str, success: bool, message: str) -> None:
    """Print formatted test result."""
    status = "✓ PASS" if success else "✗ FAIL"
    print(f"  [{status}] {name} — {message}")


def run_basic_tests() -> Tuple[int, int]:
    """Run basic connectivity tests for all services."""
    passed = 0
    failed = 0

    for service in SERVICES:
        success, message = run_service_test(service)
        label = f"{service.name} ({service.host}:{service.port})"
        print_test_result(label, success, message)

        if success:
            passed += 1
        else:
            failed += 1

    return passed, failed


def run_additional_tests() -> Tuple[int, int]:
    """Run additional application-level tests."""
    passed = 0
    failed = 0

    print("\n" + "-" * 60)
    print("Additional Tests:")
    print("-" * 60)

    # HTTP endpoint test
    success, message = test_http_endpoint("http://localhost:8000/")
    print_test_result("HTTP GET /", success, message)
    passed += 1 if success else 0
    failed += 0 if success else 1

    # DNS resolution test
    success, message = test_dns_query("127.0.0.1", 5353)
    print_test_result("DNS web.lab.local", success, message)
    passed += 1 if success else 0
    failed += 0 if success else 1

    return passed, failed


def print_summary(passed: int, failed: int) -> None:
    """Print test summary with guidance."""
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed > 0:
        print("\n[HINT] Some services are not running. Try:")
        print("  python3 scripts/start_lab.py")
        print("\nFor troubleshooting, see:")
        print("  docs/troubleshooting.md")
    else:
        print("\n[OK] All services are running!")
        print("\nYou can now start the exercises:")
        print("  python3 src/exercises/ex_10_01_tls_rest_crud.py serve")


def run_tests() -> int:
    """
    Run all smoke tests.

    Returns:
        Number of failed tests
    """
    print("=" * 60)
    print("Week 10 Smoke Tests")
    print("=" * 60)

    basic_passed, basic_failed = run_basic_tests()
    additional_passed, additional_failed = run_additional_tests()

    total_passed = basic_passed + additional_passed
    total_failed = basic_failed + additional_failed

    print_summary(total_passed, total_failed)
    return total_failed


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point."""
    return run_tests()


if __name__ == "__main__":
    raise SystemExit(main())
