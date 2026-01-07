#!/usr/bin/env python3
"""
verify_environment.py - Environment Verification Script
Week 14 - Integrated Recap
NETWORKING class - ASE, Informatics | by Revolvix

Checks that all prerequisites are installed and configured correctly
for the Week 14 laboratory session.

Usage:
    python setup/verify_environment.py
    python setup/verify_environment.py --verbose
"""

from __future__ import annotations

import subprocess
import sys
import shutil
import platform
import socket
from pathlib import Path
from typing import Optional, Tuple


class Colours:
    """ANSI colour codes for terminal output."""
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


class Checker:
    """Verification result tracker."""

    def __init__(self, verbose: bool = False):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.verbose = verbose

    def check(self, name: str, condition: bool, fix_hint: str = "") -> bool:
        """Record a check result."""
        if condition:
            print(f"  {Colours.GREEN}[PASS]{Colours.RESET} {name}")
            self.passed += 1
        else:
            print(f"  {Colours.RED}[FAIL]{Colours.RESET} {name}")
            if fix_hint:
                print(f"         {Colours.YELLOW}Fix:{Colours.RESET} {fix_hint}")
            self.failed += 1
        return condition

    def warn(self, name: str, message: str) -> None:
        """Record a warning."""
        print(f"  {Colours.YELLOW}[WARN]{Colours.RESET} {name}: {message}")
        self.warnings += 1

    def info(self, message: str) -> None:
        """Print informational message."""
        if self.verbose:
            print(f"  {Colours.BLUE}[INFO]{Colours.RESET} {message}")

    def summary(self) -> int:
        """Print summary and return exit code."""
        print()
        print("=" * 60)
        total = self.passed + self.failed
        print(f"  Results: {Colours.GREEN}{self.passed} passed{Colours.RESET}, "
              f"{Colours.RED}{self.failed} failed{Colours.RESET}, "
              f"{Colours.YELLOW}{self.warnings} warnings{Colours.RESET}")
        print("=" * 60)

        if self.failed == 0:
            print(f"\n{Colours.GREEN}{Colours.BOLD}Environment is ready for Week 14!{Colours.RESET}\n")
            return 0
        else:
            print(f"\n{Colours.RED}Please fix the issues above before proceeding.{Colours.RESET}\n")
            return 1


def check_command_exists(cmd: str) -> bool:
    """Check if a command exists in PATH."""
    return shutil.which(cmd) is not None


def run_command(cmd: list, timeout: int = 10) -> Tuple[int, str, str]:
    """Run a command and return (returncode, stdout, stderr)."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except FileNotFoundError:
        return -1, "", f"Command not found: {cmd[0]}"
    except Exception as e:
        return -1, "", str(e)


def check_docker_running() -> bool:
    """Check if Docker daemon is running."""
    code, _, _ = run_command(["docker", "info"], timeout=15)
    return code == 0


def check_docker_compose() -> bool:
    """Check if Docker Compose is available."""
    code, _, _ = run_command(["docker", "compose", "version"], timeout=10)
    return code == 0


def check_wsl2() -> bool:
    """Check if WSL2 is available (Windows only)."""
    if platform.system() != "Windows":
        return True  # Not applicable on Linux/Mac

    try:
        code, stdout, stderr = run_command(["wsl", "--status"], timeout=10)
        output = stdout + stderr
        return "WSL 2" in output or "Default Version: 2" in output
    except Exception:
        return False


def check_port_available(port: int) -> bool:
    """Check if a port is available for binding."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(("127.0.0.1", port))
        sock.close()
        # If connect fails (result != 0), port is available
        return result != 0
    except Exception:
        return True  # Assume available on error


def check_python_package(package: str) -> bool:
    """Check if a Python package is installed."""
    try:
        __import__(package)
        return True
    except ImportError:
        return False


def get_wireshark_path() -> Optional[Path]:
    """Get Wireshark installation path."""
    common_paths = [
        Path(r"C:\Program Files\Wireshark\Wireshark.exe"),
        Path(r"C:\Program Files (x86)\Wireshark\Wireshark.exe"),
    ]
    for path in common_paths:
        if path.exists():
            return path

    # Check if wireshark is in PATH
    if check_command_exists("wireshark"):
        return Path(shutil.which("wireshark"))

    return None


def main() -> int:
    """Run all environment checks."""
    import argparse

    parser = argparse.ArgumentParser(description="Verify Week 14 environment")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    print()
    print("=" * 60)
    print(f"  {Colours.BOLD}Environment Verification - Week 14 Laboratory{Colours.RESET}")
    print("  NETWORKING class - ASE, Informatics")
    print("=" * 60)
    print()

    c = Checker(verbose=args.verbose)

    # =========================================================================
    # Python Environment
    # =========================================================================
    print(f"{Colours.BOLD}Python Environment:{Colours.RESET}")

    py_version = sys.version_info
    c.check(
        f"Python {py_version.major}.{py_version.minor}.{py_version.micro}",
        py_version >= (3, 10),
        "Install Python 3.10 or later from python.org"
    )

    # Check required packages
    required_packages = ["requests", "pyyaml"]
    for pkg in required_packages:
        c.check(
            f"Python package: {pkg}",
            check_python_package(pkg),
            f"pip install {pkg}"
        )

    # Optional packages
    optional_packages = ["docker"]
    for pkg in optional_packages:
        if not check_python_package(pkg):
            c.warn(f"Python package: {pkg}", f"Optional but recommended. Install with: pip install {pkg}")

    print()

    # =========================================================================
    # Docker Environment
    # =========================================================================
    print(f"{Colours.BOLD}Docker Environment:{Colours.RESET}")

    c.check(
        "Docker CLI installed",
        check_command_exists("docker"),
        "Install Docker Desktop from https://www.docker.com/products/docker-desktop"
    )

    c.check(
        "Docker Compose available",
        check_docker_compose(),
        "Docker Compose should be included with Docker Desktop"
    )

    docker_running = check_docker_running()
    c.check(
        "Docker daemon running",
        docker_running,
        "Start Docker Desktop application"
    )

    if docker_running:
        # Check Docker version
        code, stdout, _ = run_command(["docker", "version", "--format", "{{.Server.Version}}"])
        if code == 0:
            c.info(f"Docker version: {stdout.strip()}")

    print()

    # =========================================================================
    # WSL2 Environment (Windows only)
    # =========================================================================
    if platform.system() == "Windows":
        print(f"{Colours.BOLD}WSL2 Environment:{Colours.RESET}")

        c.check(
            "WSL2 available",
            check_wsl2(),
            "Enable WSL2: wsl --install (requires restart)"
        )

        print()

    # =========================================================================
    # Network Tools
    # =========================================================================
    print(f"{Colours.BOLD}Network Analysis Tools:{Colours.RESET}")

    wireshark_path = get_wireshark_path()
    c.check(
        "Wireshark installed",
        wireshark_path is not None,
        "Install from https://www.wireshark.org/download.html"
    )
    if wireshark_path:
        c.info(f"Wireshark path: {wireshark_path}")

    # Check tshark
    if check_command_exists("tshark"):
        c.check("tshark available", True)
    else:
        c.warn("tshark", "Install Wireshark with command-line tools for tshark")

    print()

    # =========================================================================
    # Port Availability
    # =========================================================================
    print(f"{Colours.BOLD}Port Availability:{Colours.RESET}")

    ports_to_check = [
        (8080, "Load Balancer"),
        (8001, "Backend 1"),
        (8002, "Backend 2"),
        (9000, "TCP Echo Server"),
        (9443, "Portainer (optional)"),
    ]

    for port, service in ports_to_check:
        available = check_port_available(port)
        if not available:
            c.warn(f"Port {port} ({service})", "Port may be in use by another application")
        else:
            c.check(f"Port {port} ({service}) available", True)

    print()

    # =========================================================================
    # Optional Tools
    # =========================================================================
    print(f"{Colours.BOLD}Optional Tools:{Colours.RESET}")

    if check_command_exists("git"):
        c.check("Git installed", True)
    else:
        c.warn("Git", "Recommended for version control")

    if check_command_exists("curl"):
        c.check("curl installed", True)
    else:
        c.warn("curl", "Recommended for HTTP testing")

    print()

    # =========================================================================
    # Summary
    # =========================================================================
    return c.summary()


if __name__ == "__main__":
    sys.exit(main())
