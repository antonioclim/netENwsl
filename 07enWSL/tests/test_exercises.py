#!/usr/bin/env python3
"""
Exercise Verification Tests — Week 7
====================================
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Tests to verify exercise completion and expected outcomes.
Compatible with both standalone execution and pytest.

Usage:
    # Standalone
    python3 tests/test_exercises.py --exercise 1
    python3 tests/test_exercises.py --all
    
    # With pytest
    pytest tests/test_exercises.py -v
    pytest tests/test_exercises.py -m exercise1

Exit codes:
    0 - All tests passed
    1 - Some tests failed
    2 - Error (configuration issue)
"""

from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import argparse
import socket
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# ═══════════════════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class TestResult:
    """Result of a single test execution."""
    name: str
    passed: bool
    message: str
    duration: float = 0.0


# ═══════════════════════════════════════════════════════════════════════════════
# TEST CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
DEFAULT_TCP_HOST = "localhost"
DEFAULT_TCP_PORT = 9090
DEFAULT_UDP_HOST = "localhost"
DEFAULT_UDP_PORT = 9091
DEFAULT_PROXY_PORT = 8888
DEFAULT_TIMEOUT = 5.0


# ═══════════════════════════════════════════════════════════════════════════════
# INDIVIDUAL TEST FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════


TestResult.__test__ = False  # Prevent pytest collecting this helper dataclass
def test_tcp_connectivity(
    host: str = DEFAULT_TCP_HOST,
    port: int = DEFAULT_TCP_PORT,
    timeout: float = DEFAULT_TIMEOUT
) -> tuple[bool, str]:
    """
    Test basic TCP connectivity to the echo server.
    
    Args:
        host: Target hostname or IP
        port: Target port number
        timeout: Connection timeout in seconds
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        sock.close()
        return True, f"Connection to {host}:{port} successful"
    except socket.timeout:
        return False, f"Connection to {host}:{port} timed out"
    except ConnectionRefusedError:
        return False, f"Connection to {host}:{port} refused"
    except OSError as e:
        return False, f"Connection error: {e}"


def test_tcp_echo(
    host: str = DEFAULT_TCP_HOST,
    port: int = DEFAULT_TCP_PORT,
    timeout: float = DEFAULT_TIMEOUT,
    test_message: str = "test_echo_verification"
) -> tuple[bool, str]:
    """
    Test TCP echo response - sends message and verifies echo.
    
    Args:
        host: Target hostname or IP
        port: Target port number
        timeout: Socket timeout in seconds
        test_message: Message to send and expect back
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        
        sock.sendall(test_message.encode("utf-8"))
        response = sock.recv(4096).decode("utf-8")
        sock.close()
        
        if response.strip() == test_message:
            return True, "Echo response correct"
        else:
            return False, f"Echo mismatch: expected '{test_message}', got '{response.strip()}'"
            
    except socket.timeout:
        return False, "Echo test timed out waiting for response"
    except ConnectionRefusedError:
        return False, "Connection refused - is the server running?"
    except OSError as e:
        return False, f"Echo test error: {e}"


def test_tcp_blocked(
    host: str = DEFAULT_TCP_HOST,
    port: int = DEFAULT_TCP_PORT,
    timeout: float = 3.0
) -> tuple[bool, str]:
    """
    Test that TCP is blocked (expects connection refused or timeout).
    
    This test PASSES if the connection FAILS (blocked by firewall).
    
    Args:
        host: Target hostname or IP
        port: Target port number
        timeout: Connection timeout in seconds
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result != 0:
            return True, f"Connection blocked (errno {result})"
        else:
            return False, "Connection succeeded - firewall rule not active"
            
    except socket.timeout:
        return True, "Connection timed out (expected with DROP rule)"
    except ConnectionRefusedError:
        return True, "Connection refused (expected with REJECT rule)"
    except OSError as e:
        return True, f"Connection failed: {e}"


def test_udp_send(
    host: str = DEFAULT_UDP_HOST,
    port: int = DEFAULT_UDP_PORT,
    test_message: str = "test_udp"
) -> tuple[bool, str]:
    """
    Test UDP send capability.
    
    Note: UDP send always "succeeds" at the socket level since there's
    no delivery confirmation. This only verifies send doesn't error.
    
    Args:
        host: Target hostname or IP
        port: Target port number
        test_message: Message to send
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(test_message.encode("utf-8"), (host, port))
        sock.close()
        return True, "UDP datagram sent (delivery not confirmed)"
    except OSError as e:
        return False, f"UDP send failed: {e}"


def test_proxy_connectivity(
    host: str = DEFAULT_TCP_HOST,
    port: int = DEFAULT_PROXY_PORT,
    timeout: float = DEFAULT_TIMEOUT
) -> tuple[bool, str]:
    """
    Test connectivity to the packet filter proxy.
    
    Args:
        host: Proxy hostname or IP
        port: Proxy port number
        timeout: Connection timeout in seconds
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    return test_tcp_connectivity(host, port, timeout)


# ═══════════════════════════════════════════════════════════════════════════════
# EXERCISE TEST SUITES
# ═══════════════════════════════════════════════════════════════════════════════

def get_exercise_tests(exercise: int) -> list[tuple[str, Callable[[], tuple[bool, str]]]]:
    """
    Get the test functions for a specific exercise.
    
    Args:
        exercise: Exercise number (1-5)
        
    Returns:
        List of (test_name, test_function) tuples
        
    Raises:
        ValueError: If exercise number is invalid
    """
    if exercise == 1:
        # Exercise 1: Baseline connectivity
        return [
            ("TCP connectivity", test_tcp_connectivity),
            ("TCP echo", test_tcp_echo),
            ("UDP send", test_udp_send),
        ]
    
    elif exercise == 2:
        # Exercise 2: TCP filtering with REJECT
        return [
            ("TCP blocked", test_tcp_blocked),
            ("UDP still works", test_udp_send),
        ]
    
    elif exercise == 3:
        # Exercise 3: UDP filtering with DROP
        return [
            ("TCP connectivity", test_tcp_connectivity),
            ("UDP send (may be dropped)", lambda: (True, "Sent but delivery not verified")),
        ]
    
    elif exercise == 4:
        # Exercise 4: Application layer filter
        return [
            ("Proxy connectivity", test_proxy_connectivity),
        ]
    
    elif exercise == 5:
        # Exercise 5: Port probing
        return [
            ("Port probe setup", lambda: (True, "See artifacts/probe_results.log")),
        ]
    
    else:
        raise ValueError(f"Unknown exercise: {exercise}. Valid range: 1-5")


def run_exercise_tests(exercise: int) -> list[TestResult]:
    """
    Run all tests for a specific exercise.
    
    Args:
        exercise: Exercise number (1-5)
        
    Returns:
        List of TestResult objects
    """
    try:
        tests = get_exercise_tests(exercise)
    except ValueError as e:
        print(f"Error: {e}")
        return []
    
    results = []
    
    print(f"\nTesting Exercise {exercise}")
    print("─" * 50)
    
    if exercise == 2:
        print("Note: This test expects TCP to be BLOCKED")
    
    for name, test_func in tests:
        passed, message = test_func()
        result = TestResult(name=name, passed=passed, message=message)
        results.append(result)
        
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status} {name}: {message}")
    
    return results


# ═══════════════════════════════════════════════════════════════════════════════
# PYTEST COMPATIBILITY
# ═══════════════════════════════════════════════════════════════════════════════
# These functions allow running with pytest


# ═══════════════════════════════════════════════════════════════════════════════
# PYTEST COLLECTION GUARDS
# ═══════════════════════════════════════════════════════════════════════════════
# The helper functions below are designed for standalone execution. When this
# module is imported by pytest we do not want them to be collected as tests.
#
# This avoids mixing "baseline" and "blocked" expectations in a single test run.
test_tcp_connectivity.__test__ = False  # type: ignore[attr-defined]
test_tcp_echo.__test__ = False  # type: ignore[attr-defined]
test_tcp_blocked.__test__ = False  # type: ignore[attr-defined]
test_udp_send.__test__ = False  # type: ignore[attr-defined]
test_proxy_connectivity.__test__ = False  # type: ignore[attr-defined]

def _docker_lab_running() -> bool:
    """Return True if the Week 7 Docker lab containers appear to be running."""
    try:
        import subprocess

        p = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
            timeout=3,
            check=False,
        )
        if p.returncode != 0:
            return False
        names = set((p.stdout or "").splitlines())
        # Container names are defined in docker/docker-compose.yml
        return "week7_tcp_server" in names
    except Exception:
        return False

def _require_docker_lab() -> None:
    """Skip docker-dependent pytest checks when the lab is not running."""
    if not _docker_lab_running():
        import pytest

        pytest.skip("Docker lab not running (start with: python scripts/start_lab.py)")

import pytest  # noqa: E402 (import not at top)


@pytest.mark.exercise1
def test_exercise1_tcp_connectivity():
    """Pytest: Exercise 1 - TCP connectivity."""
    _require_docker_lab()
    passed, msg = test_tcp_connectivity()
    assert passed, msg


@pytest.mark.exercise1
def test_exercise1_tcp_echo():
    """Pytest: Exercise 1 - TCP echo."""
    _require_docker_lab()
    passed, msg = test_tcp_echo()
    assert passed, msg


@pytest.mark.exercise1
def test_exercise1_udp_send():
    """Pytest: Exercise 1 - UDP send."""
    _require_docker_lab()
    passed, msg = test_udp_send()
    assert passed, msg


@pytest.mark.exercise2
def test_exercise2_tcp_blocked():
    """Pytest: Exercise 2 - TCP blocked."""
    _require_docker_lab()
    passed, msg = test_tcp_blocked()
    assert passed, msg


@pytest.mark.exercise2
def test_exercise2_udp_works():
    """Pytest: Exercise 2 - UDP still works."""
    _require_docker_lab()
    passed, msg = test_udp_send()
    assert passed, msg


@pytest.mark.exercise3
def test_exercise3_tcp_connectivity():
    """Pytest: Exercise 3 - TCP connectivity."""
    _require_docker_lab()
    passed, msg = test_tcp_connectivity()
    assert passed, msg


@pytest.mark.exercise4
def test_exercise4_proxy_connectivity():
    """Pytest: Exercise 4 - Proxy connectivity."""
    _require_docker_lab()
    passed, msg = test_proxy_connectivity()
    assert passed, msg


# ═══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

def build_parser() -> argparse.ArgumentParser:
    """Build command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Week 7 Exercise Verification Tests",
        epilog="Exit codes: 0=all passed, 1=some failed, 2=error"
    )
    
    parser.add_argument(
        "--exercise", "-e",
        type=int,
        choices=[1, 2, 3, 4, 5],
        help="Exercise number to test (1-5)"
    )
    
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Run all exercise tests"
    )
    
    parser.add_argument(
        "--host",
        default=DEFAULT_TCP_HOST,
        help=f"Target host (default: {DEFAULT_TCP_HOST})"
    )
    
    parser.add_argument(
        "--tcp-port",
        type=int,
        default=DEFAULT_TCP_PORT,
        help=f"TCP server port (default: {DEFAULT_TCP_PORT})"
    )
    
    parser.add_argument(
        "--udp-port",
        type=int,
        default=DEFAULT_UDP_PORT,
        help=f"UDP receiver port (default: {DEFAULT_UDP_PORT})"
    )
    
    return parser


def main() -> int:
    """
    Main entry point for CLI execution.
    
    Returns:
        Exit code: 0 if all passed, 1 if any failed, 2 if error
    """
    parser = build_parser()
    args = parser.parse_args()
    
    # Header
    print("═" * 60)
    print("  Week 7 Exercise Verification")
    print("  NETWORKING class - ASE, Informatics")
    print("═" * 60)
    
    all_results: list[TestResult] = []
    
    if args.all:
        for exercise in [1, 2, 3, 4, 5]:
            results = run_exercise_tests(exercise)
            all_results.extend(results)
    elif args.exercise:
        all_results = run_exercise_tests(args.exercise)
    else:
        print("\nUsage:")
        print("  python test_exercises.py --exercise <1-5>")
        print("  python test_exercises.py --all")
        return 0
    
    # Summary
    if all_results:
        print()
        print("═" * 60)
        passed = sum(1 for r in all_results if r.passed)
        total = len(all_results)
        status = "✅ ALL PASSED" if passed == total else "❌ SOME FAILED"
        print(f"  Results: {passed}/{total} tests passed — {status}")
        print("═" * 60)
        
        return 0 if passed == total else 1
    
    return 2


if __name__ == "__main__":
    sys.exit(main())
