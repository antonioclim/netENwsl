#!/usr/bin/env python3
"""
Week 10 - Smoke Tests
=====================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

This script performs basic connectivity tests for all lab services.
Run this after starting the lab to verify everything is working.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import socket
import subprocess
import sys
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
TESTS = [
    {
        "name": "Web Server (HTTP)",
        "type": "tcp",
        "host": "localhost",
        "port": 8000,
    },
    {
        "name": "DNS Server",
        "type": "udp",
        "host": "localhost",
        "port": 5353,
    },
    {
        "name": "SSH Server",
        "type": "tcp",
        "host": "localhost",
        "port": 2222,
    },
    {
        "name": "FTP Server",
        "type": "tcp",
        "host": "localhost",
        "port": 2121,
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def check_tcp_port(host: str, port: int, timeout: float = 5.0) -> tuple[bool, str]:
    """
    Test if a TCP port is reachable.
    
    💭 PREDICTION: What error will we get if the service is not running?
    
    Returns:
        Tuple of (success, message)
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


def check_udp_port(host: str, port: int, timeout: float = 5.0) -> tuple[bool, str]:
    """
    Test if a UDP port is responsive (sends a minimal DNS query).
    
    Returns:
        Tuple of (success, message)
    """
    # Minimal DNS query for "test" (won't get valid response but tests connectivity)
    dns_query = bytes([
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
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(timeout)
            sock.sendto(dns_query, (host, port))
            data, addr = sock.recvfrom(512)
            return True, f"Received {len(data)} bytes"
    except socket.timeout:
        return False, "Timeout (no response)"
    except OSError as exc:
        return False, str(exc)


def check_http_endpoint(url: str, timeout: float = 5.0) -> tuple[bool, str]:
    """
    Test if an HTTP endpoint is responsive.
    
    Returns:
        Tuple of (success, message)
    """
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


def check_dns_query(server: str, port: int, domain: str = "web.lab.local") -> tuple[bool, str]:
    """
    Test DNS resolution using dig.
    
    💭 PREDICTION: What IP address will web.lab.local resolve to?
    
    Returns:
        Tuple of (success, message)
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
        else:
            return False, "No answer"
    except FileNotFoundError:
        return False, "dig not installed"
    except subprocess.TimeoutExpired:
        return False, "Timeout"


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_TEST_RUNNER
# ═══════════════════════════════════════════════════════════════════════════════
def run_tests() -> int:
    """
    Run all smoke tests.
    
    Returns:
        Number of failed tests
    """
    print("=" * 60)
    print("Week 10 Smoke Tests")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test in TESTS:
        name = test["name"]
        host = test["host"]
        port = test["port"]
        test_type = test["type"]
        
        if test_type == "tcp":
            success, message = check_tcp_port(host, port)
        elif test_type == "udp":
            success, message = check_udp_port(host, port)
        else:
            success, message = False, f"Unknown test type: {test_type}"
        
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"  [{status}] {name} ({host}:{port}) — {message}")
        
        if success:
            passed += 1
        else:
            failed += 1
    
    # Additional tests
    print("\n" + "-" * 60)
    print("Additional Tests:")
    print("-" * 60)
    
    # HTTP endpoint test
    success, message = check_http_endpoint("http://localhost:8000/")
    status = "✓ PASS" if success else "✗ FAIL"
    print(f"  [{status}] HTTP GET / — {message}")
    if success:
        passed += 1
    else:
        failed += 1
    
    # DNS resolution test
    success, message = check_dns_query("127.0.0.1", 5353)
    status = "✓ PASS" if success else "✗ FAIL"
    print(f"  [{status}] DNS web.lab.local — {message}")
    if success:
        passed += 1
    else:
        failed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed > 0:
        print("\n[HINT] Some services are not running. Try:")
        print("  python3 scripts/start_lab.py")
        print("\nFor detailed troubleshooting, see:")
        print("  docs/troubleshooting.md")
    else:
        print("\n[OK] All services are running!")
        print("\nYou can now start the exercises:")
        print("  python3 src/exercises/ex_10_01_tls_rest_crud.py serve")
    
    return failed


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point."""
    return run_tests()


if __name__ == "__main__":
    raise SystemExit(main())
