#!/usr/bin/env python3
"""
Environment Validation Tests
NETWORKING class - ASE, Informatics | by Revolvix

Validates the laboratory environment is correctly configured.
"""

from __future__ import annotations

import subprocess
import sys
import socket
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def test_python_version():
    """Verify Python version meets requirements."""
    version = sys.version_info
    assert version >= (3, 11), f"Python 3.11+ required, got {version.major}.{version.minor}"
    print(f"  [PASS] Python {version.major}.{version.minor}.{version.micro}")


def test_required_packages():
    """Verify required Python packages are installed."""
    packages = ["socket", "subprocess", "argparse", "pathlib"]
    
    for pkg in packages:
        try:
            __import__(pkg)
            print(f"  [PASS] Package: {pkg}")
        except ImportError:
            print(f"  [FAIL] Package: {pkg}")
            raise AssertionError(f"Required package not available: {pkg}")


def test_docker_available():
    """Verify Docker is accessible."""
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode == 0, "Docker command failed"
        print(f"  [PASS] Docker: {result.stdout.strip()}")
    except FileNotFoundError:
        print("  [FAIL] Docker not found")
        raise AssertionError("Docker is not installed")
    except subprocess.TimeoutExpired:
        print("  [FAIL] Docker command timed out")
        raise AssertionError("Docker not responding")


def test_docker_running():
    """Verify Docker daemon is running."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=15
        )
        assert result.returncode == 0, "Docker daemon not running"
        print("  [PASS] Docker daemon running")
    except Exception as e:
        print(f"  [FAIL] Docker daemon: {e}")
        raise


def test_project_structure():
    """Verify required directories exist."""
    required_dirs = [
        "docker",
        "scripts",
        "src",
        "tests",
        "pcap",
        "artifacts",
        "docs",
        "homework"
    ]
    
    for dir_name in required_dirs:
        dir_path = PROJECT_ROOT / dir_name
        assert dir_path.exists(), f"Missing directory: {dir_name}"
        print(f"  [PASS] Directory: {dir_name}/")


def test_docker_compose_valid():
    """Verify docker-compose.yml is valid YAML."""
    compose_file = PROJECT_ROOT / "docker" / "docker-compose.yml"
    
    assert compose_file.exists(), "docker-compose.yml not found"
    
    try:
        result = subprocess.run(
            ["docker", "compose", "-f", str(compose_file), "config", "-q"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Invalid compose file: {result.stderr}"
        print("  [PASS] docker-compose.yml valid")
    except Exception as e:
        print(f"  [FAIL] docker-compose.yml: {e}")
        raise


def test_loopback_connectivity():
    """Verify loopback interface is working."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
        sock.listen(1)
        
        # Try to connect
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(2)
        client.connect(("127.0.0.1", port))
        
        client.close()
        sock.close()
        
        print("  [PASS] Loopback connectivity")
    except Exception as e:
        print(f"  [FAIL] Loopback: {e}")
        raise AssertionError(f"Loopback failed: {e}")


def main() -> int:
    """Run all environment tests."""
    print("=" * 60)
    print("Environment Validation Tests")
    print("NETWORKING class - ASE, Informatics | by Revolvix")
    print("=" * 60)
    
    tests = [
        ("Python Version", test_python_version),
        ("Required Packages", test_required_packages),
        ("Docker Available", test_docker_available),
        ("Docker Running", test_docker_running),
        ("Project Structure", test_project_structure),
        ("Docker Compose Valid", test_docker_compose_valid),
        ("Loopback Connectivity", test_loopback_connectivity),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        print(f"\n{name}:")
        try:
            test_func()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"  Error: {e}")
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("\033[92mAll tests passed!\033[0m")
        return 0
    else:
        print("\033[91mSome tests failed.\033[0m")
        return 1


if __name__ == "__main__":
    sys.exit(main())
