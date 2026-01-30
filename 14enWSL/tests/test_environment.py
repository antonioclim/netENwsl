#!/usr/bin/env python3
"""
test_environment.py - Environment Validation Tests
Week 14 - Integrated Recap
NETWORKING class - ASE, Informatics | by Revolvix

Verifies that the laboratory environment is correctly configured.

Usage:
    python tests/test_environment.py
    pytest tests/test_environment.py -v
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import subprocess
import socket
import sys
import json
import os
from pathlib import Path
from typing import Optional

import pytest
from urllib.request import urlopen, Request
from urllib.error import URLError

# Integration tests in this module require a running Week 14 Docker lab.
# They are disabled by default to keep CI and local development fast and reliable.
RUN_DOCKER_TESTS = os.getenv("RUN_DOCKER_TESTS", "").strip().lower() in {"1", "true", "yes"}

def _docker_available() -> bool:
    try:
        completed = subprocess.run(["docker", "info"], capture_output=True, timeout=5)
        return completed.returncode == 0
    except Exception:
        return False

DOCKER_AVAILABLE = _docker_available()



PROJECT_ROOT = Path(__file__).parent.parent



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class Colours:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_port_open(host: str, port: int, timeout: float = 2.0) -> bool:
    """Check if a TCP port is open."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_http_endpoint(url: str, timeout: float = 5.0) -> tuple:
    """Check HTTP endpoint. Returns (success, status_code)."""
    try:
        req = Request(url, method="GET")
        with urlopen(req, timeout=timeout) as response:
            return True, response.status
    except Exception as e:
        return False, str(e)



# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
def run_command(cmd: list, timeout: int = 10) -> tuple:
    """Run command and return (success, stdout, stderr)."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class TestDockerEnvironment:
    pytestmark = pytest.mark.skipif(
        not (RUN_DOCKER_TESTS and DOCKER_AVAILABLE),
        reason="Set RUN_DOCKER_TESTS=1 and start the Week 14 Docker lab to enable integration tests",
    )
    """Test Docker environment is properly configured."""


# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_docker_running(self):
        """Docker daemon should be running."""
        success, _, _ = run_command(["docker", "info"])
        assert success, "Docker daemon is not running"


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_docker_compose_available(self):
        """Docker Compose should be available."""
        success, _, _ = run_command(["docker", "compose", "version"])
        assert success, "Docker Compose is not available"


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_compose_file_exists(self):
        """docker-compose.yml should exist."""
        compose_file = PROJECT_ROOT / "docker" / "docker-compose.yml"
        assert compose_file.exists(), f"Compose file not found: {compose_file}"



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class TestNetworkConnectivity:
    pytestmark = pytest.mark.skipif(
        not (RUN_DOCKER_TESTS and DOCKER_AVAILABLE),
        reason="Set RUN_DOCKER_TESTS=1 and start the Week 14 Docker lab to enable integration tests",
    )
    """Test network services are accessible."""


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_load_balancer_port(self):
        """Load balancer port 8080 should be accessible."""
        assert check_port_open("localhost", 8080), \
            "Load balancer port 8080 is not accessible"


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_backend1_port(self):
        """Backend 1 port 8001 should be accessible."""
        assert check_port_open("localhost", 8001), \
            "Backend 1 port 8001 is not accessible"


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_backend2_port(self):
        """Backend 2 port 8002 should be accessible."""
        assert check_port_open("localhost", 8002), \
            "Backend 2 port 8002 is not accessible"


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_echo_server_port(self):
        """TCP echo server port 9090 should be accessible."""
        assert check_port_open("localhost", 9090), \
            "TCP echo server port 9090 is not accessible"



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class TestHTTPEndpoints:
    pytestmark = pytest.mark.skipif(
        not (RUN_DOCKER_TESTS and DOCKER_AVAILABLE),
        reason="Set RUN_DOCKER_TESTS=1 and start the Week 14 Docker lab to enable integration tests",
    )
    """Test HTTP endpoints respond correctly."""


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_load_balancer_root(self):
        """Load balancer root endpoint should return 200."""
        success, status = check_http_endpoint("http://localhost:8080/")
        assert success and status == 200, \
            f"Load balancer root failed: {status}"


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_load_balancer_status(self):
        """Load balancer status endpoint should return 200."""
        success, status = check_http_endpoint("http://localhost:8080/lb-status")
        assert success and status == 200, \
            f"LB status endpoint failed: {status}"


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_backend1_health(self):
        """Backend 1 health endpoint should return 200."""
        success, status = check_http_endpoint("http://localhost:8001/health")
        assert success and status == 200, \
            f"Backend 1 health failed: {status}"


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_backend2_health(self):
        """Backend 2 health endpoint should return 200."""
        success, status = check_http_endpoint("http://localhost:8002/health")
        assert success and status == 200, \
            f"Backend 2 health failed: {status}"


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_backend_info_json(self):
        """Backend info endpoint should return valid JSON."""
        try:
            with urlopen("http://localhost:8001/info", timeout=5) as response:
                data = json.loads(response.read())
                assert "id" in data, "Missing 'id' in backend info"
        except Exception as e:
            assert False, f"Backend info test failed: {e}"



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class TestTCPEcho:
    pytestmark = pytest.mark.skipif(
        not (RUN_DOCKER_TESTS and DOCKER_AVAILABLE),
        reason="Set RUN_DOCKER_TESTS=1 and start the Week 14 Docker lab to enable integration tests",
    )
    """Test TCP echo server functionality."""


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_echo_connection(self):
        """Should be able to connect to echo server."""
        assert check_port_open("localhost", 9090), \
            "Cannot connect to echo server"


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_echo_response(self):
        """Echo server should echo back messages."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(("localhost", 9090))

            test_message = b"hello_week14_test\n"
            sock.sendall(test_message)

            response = sock.recv(1024)
            sock.close()

            assert test_message.strip() in response, \
                f"Echo mismatch: sent {test_message}, got {response}"

        except Exception as e:
            assert False, f"Echo test failed: {e}"



# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
def run_standalone_tests():
    """Run tests in standalone mode (without pytest)."""
    print()
    print("=" * 60)
    print("  Environment Validation Tests - Week 14")
    print("=" * 60)
    print()

    test_classes = [
        TestDockerEnvironment,
        TestNetworkConnectivity,
        TestHTTPEndpoints,
        TestTCPEcho,
    ]

    passed = 0
    failed = 0
    errors = []

    for test_class in test_classes:
        print(f"\n{test_class.__name__}:")
        instance = test_class()

        for method_name in dir(instance):
            if not method_name.startswith("test_"):
                continue

            method = getattr(instance, method_name)
            test_name = method_name.replace("test_", "").replace("_", " ")

            try:
                method()
                print(f"  {Colours.GREEN}✓{Colours.RESET} {test_name}")
                passed += 1
            except AssertionError as e:
                print(f"  {Colours.RED}✗{Colours.RESET} {test_name}")
                print(f"    {Colours.YELLOW}{e}{Colours.RESET}")
                failed += 1
                errors.append((test_name, str(e)))
            except Exception as e:
                print(f"  {Colours.RED}✗{Colours.RESET} {test_name} (error)")
                print(f"    {Colours.YELLOW}{e}{Colours.RESET}")
                failed += 1
                errors.append((test_name, str(e)))

    print()
    print("=" * 60)
    print(f"  Results: {Colours.GREEN}{passed} passed{Colours.RESET}, "
          f"{Colours.RED}{failed} failed{Colours.RESET}")
    print("=" * 60)

    if failed > 0:
        print(f"\n{Colours.YELLOW}Tip: Make sure the lab is running:{Colours.RESET}")
        print("  python scripts/start_lab.py")
        print()

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run_standalone_tests())
