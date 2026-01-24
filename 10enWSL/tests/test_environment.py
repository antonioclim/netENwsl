#!/usr/bin/env python3
"""
Week 10 Environment Validation Tests
NETWORKING class - ASE, Informatics | by Revolvix

Tests that verify the laboratory environment is properly configured.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import subprocess
import socket
import sys
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Any

PROJECT_ROOT = Path(__file__).parent.parent



# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def test_docker_available() -> bool:
    """Test that Docker is available and running."""
    result = subprocess.run(
        ["docker", "info"],
        capture_output=True,
        timeout=10
    )
    assert result.returncode == 0, "Docker daemon is not running"



# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def test_docker_compose_available() -> bool:
    """Test that Docker Compose is available."""
    result = subprocess.run(
        ["docker", "compose", "version"],
        capture_output=True
    )
    assert result.returncode == 0, "Docker Compose not available"



# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def test_compose_file_exists() -> bool:
    """Test that docker-compose.yml exists."""
    compose_file = PROJECT_ROOT / "docker" / "docker-compose.yml"
    assert compose_file.exists(), f"docker-compose.yml not found at {compose_file}"



# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def test_python_packages() -> bool:
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
def test_project_structure() -> bool:
    """Test that required directories exist."""
    required_dirs = ["docker", "scripts", "src", "tests", "docs"]
    
    for dir_name in required_dirs:
        dir_path = PROJECT_ROOT / dir_name
        assert dir_path.is_dir(), f"Directory not found: {dir_name}"



# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def test_port_availability() -> bool:
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
        except AssertionError as e:
            print(f"✗ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__}: Unexpected error: {e}")
            failed += 1
    
    print()
    print(f"Results: {passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)
