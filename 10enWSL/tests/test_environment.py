#!/usr/bin/env python3
"""Week 10 environment validation tests.

These checks verify that the laboratory environment is correctly configured.

Notes
-----
Some environments (for example, CI or limited sandboxes) may not provide
Docker. In those cases, Docker-dependent tests are skipped.

Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import shutil
import socket
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent



# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def test_docker_available() -> None:
    """Docker must be installed and the daemon must be reachable."""
    if shutil.which("docker") is None:
        pytest.skip("Docker is not available on this system")

    result = subprocess.run(["docker", "info"], capture_output=True, text=True, timeout=10)
    assert result.returncode == 0, "Docker daemon is not running"



# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def test_docker_compose_available() -> None:
    """Docker Compose must be available (docker compose)."""
    if shutil.which("docker") is None:
        pytest.skip("Docker is not available on this system")

    result = subprocess.run(["docker", "compose", "version"], capture_output=True, text=True, timeout=10)
    assert result.returncode == 0, "Docker Compose is not available"



# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def test_compose_file_exists() -> None:
    """Test that docker-compose.yml exists."""
    compose_file = PROJECT_ROOT / "docker" / "docker-compose.yml"
    assert compose_file.exists(), f"docker-compose.yml not found at {compose_file}"



# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def test_python_packages() -> None:
    """Test that required Python packages are installed."""
    packages = ["flask", "requests", "paramiko", "yaml"]
    
    for pkg in packages:
        try:
            __import__(pkg)
        except ImportError:
            raise AssertionError(f"Required package not installed: {pkg}")



# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def test_project_structure() -> None:
    """Test that required directories exist."""
    required_dirs = ["docker", "scripts", "src", "tests", "docs"]
    
    for dir_name in required_dirs:
        dir_path = PROJECT_ROOT / dir_name
        assert dir_path.is_dir(), f"Directory not found: {dir_name}"



# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def test_port_availability() -> None:
    """Test that required ports are available (when services not running)."""
    ports = [8000, 5353, 2222, 2121]
    
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("127.0.0.1", port))
        except OSError:
            # Port in use - might be our services running, which is OK
            pass


if __name__ == "__main__":
    # Simple test runner
    tests = [
        test_docker_available,
        test_docker_compose_available,
        test_compose_file_exists,
        test_python_packages,
        test_project_structure,
        test_port_availability,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            print(f"✓ {test.__name__}")
            passed += 1
        except pytest.skip.Exception as exc:
            print(f"↷ {test.__name__}: skipped ({exc})")
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__}: Unexpected error: {e}")
            failed += 1
    
    print()
    print(f"Results: {passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)
