#!/usr/bin/env python3
"""
Environment Validation Tests
NETWORKING class - ASE, Informatics | by Revolvix

Tests to verify the laboratory environment is correctly configured.
"""

from __future__ import annotations

import socket
import subprocess
import sys
import shutil
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestResult:
    """Simple test result tracker."""
    
    def __init__(self) -> None:
        self.passed = 0
        self.failed = 0
        self.tests: list[tuple[str, bool, str]] = []
    
    def add(self, name: str, passed: bool, message: str = "") -> None:
        self.tests.append((name, passed, message))
        if passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def summary(self) -> int:
        print()
        print("=" * 60)
        print(f"Results: {self.passed} passed, {self.failed} failed")
        print("=" * 60)
        return 0 if self.failed == 0 else 1


def check_docker_available() -> tuple[bool, str]:
    """Check if Docker is available and running."""
    if not shutil.which("docker"):
        return False, "Docker not in PATH"
    
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        if result.returncode == 0:
            return True, "Docker daemon running"
        else:
            return False, "Docker daemon not responding"
    except Exception as e:
        return False, str(e)


def check_port_available(host: str, port: int, timeout: float = 2.0) -> tuple[bool, str]:
    """Check if a port is available (can connect)."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            return True, f"Port {port} is open"
        else:
            return False, f"Port {port} is closed (errno {result})"
    except Exception as e:
        return False, str(e)


def check_tcp_echo(host: str, port: int, timeout: float = 5.0) -> tuple[bool, str]:
    """Test TCP echo functionality."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        
        test_msg = "env_test_message"
        sock.sendall(test_msg.encode("utf-8"))
        response = sock.recv(4096).decode("utf-8")
        sock.close()
        
        if response.strip() == test_msg:
            return True, "Echo response correct"
        else:
            return False, f"Unexpected response: {response}"
    except Exception as e:
        return False, str(e)


def check_file_exists(path: Path) -> tuple[bool, str]:
    """Check if a file exists."""
    if path.exists():
        return True, f"Found: {path.name}"
    else:
        return False, f"Missing: {path}"


def main() -> int:
    print("=" * 60)
    print("Week 7 Environment Validation Tests")
    print("NETWORKING class - ASE, Informatics")
    print("=" * 60)
    print()

    results = TestResult()

    # Docker tests
    print("[Docker Environment]")
    passed, msg = check_docker_available()
    results.add("Docker available", passed, msg)
    print(f"  {'[PASS]' if passed else '[FAIL]'} Docker available: {msg}")

    # Network tests
    print()
    print("[Network Services]")
    
    # TCP server
    passed, msg = check_port_available("localhost", 9090)
    results.add("TCP server port", passed, msg)
    print(f"  {'[PASS]' if passed else '[FAIL]'} TCP server (9090): {msg}")
    
    if passed:
        passed, msg = check_tcp_echo("localhost", 9090)
        results.add("TCP echo functionality", passed, msg)
        print(f"  {'[PASS]' if passed else '[FAIL]'} TCP echo: {msg}")
    
    # UDP receiver (port check only)
    passed, msg = check_port_available("localhost", 9091)
    # UDP doesn't respond to TCP connect, so just note it
    print(f"  [INFO] UDP receiver (9091): Port check not applicable for UDP")
    results.add("UDP receiver assumed", True, "Cannot verify UDP without sending")

    # File structure tests
    print()
    print("[File Structure]")
    
    required_files = [
        PROJECT_ROOT / "docker" / "docker-compose.yml",
        PROJECT_ROOT / "docker" / "configs" / "firewall_profiles.json",
        PROJECT_ROOT / "src" / "apps" / "tcp_server.py",
        PROJECT_ROOT / "src" / "apps" / "tcp_client.py",
        PROJECT_ROOT / "src" / "apps" / "port_probe.py",
    ]
    
    for path in required_files:
        passed, msg = check_file_exists(path)
        results.add(f"File: {path.name}", passed, msg)
        print(f"  {'[PASS]' if passed else '[FAIL]'} {msg}")

    # Directory tests
    print()
    print("[Directories]")
    
    required_dirs = [
        PROJECT_ROOT / "artifacts",
        PROJECT_ROOT / "pcap",
    ]
    
    for path in required_dirs:
        passed = path.exists() and path.is_dir()
        results.add(f"Directory: {path.name}", passed)
        print(f"  {'[PASS]' if passed else '[FAIL]'} {path.name}/")

    return results.summary()


if __name__ == "__main__":
    sys.exit(main())
