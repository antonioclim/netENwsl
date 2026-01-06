#!/usr/bin/env python3
"""
Environment Verification Script
NETWORKING class - ASE, Informatics | by Revolvix

Checks that all prerequisites are installed and configured correctly
for the Week 1 Computer Networks laboratory.
"""

from __future__ import annotations

import subprocess
import sys
import shutil
from pathlib import Path
from typing import Callable


class EnvironmentChecker:
    """Systematic environment verification with detailed reporting."""

    def __init__(self) -> None:
        self.passed: int = 0
        self.failed: int = 0
        self.warnings: int = 0

    def check(self, name: str, condition: bool, fix_hint: str = "") -> bool:
        """Record a check result with optional remediation guidance."""
        if condition:
            print(f"  [\033[92mPASS\033[0m] {name}")
            self.passed += 1
            return True
        else:
            print(f"  [\033[91mFAIL\033[0m] {name}")
            if fix_hint:
                print(f"         \033[93mFix:\033[0m {fix_hint}")
            self.failed += 1
            return False

    def warn(self, name: str, message: str) -> None:
        """Record a non-critical warning."""
        print(f"  [\033[93mWARN\033[0m] {name}: {message}")
        self.warnings += 1

    def section(self, title: str) -> None:
        """Print a section header."""
        print(f"\n\033[1m{title}:\033[0m")

    def summary(self) -> int:
        """Print final summary and return exit code."""
        print("\n" + "=" * 60)
        status_parts = [
            f"\033[92m{self.passed} passed\033[0m",
            f"\033[91m{self.failed} failed\033[0m",
            f"\033[93m{self.warnings} warnings\033[0m"
        ]
        print(f"Results: {', '.join(status_parts)}")
        
        if self.failed == 0:
            print("\n\033[92mEnvironment is ready for Week 1 laboratory!\033[0m")
            return 0
        else:
            print("\n\033[91mPlease fix the issues above before proceeding.\033[0m")
            return 1


def check_command_exists(cmd: str) -> bool:
    """Check if a command is available in PATH."""
    return shutil.which(cmd) is not None


def check_docker_running() -> bool:
    """Verify Docker daemon is responsive."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=15
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def check_docker_compose() -> bool:
    """Verify Docker Compose is available (v2 syntax)."""
    try:
        result = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def check_wsl2_available() -> bool:
    """Check if WSL2 is configured (Windows only)."""
    if sys.platform != "win32":
        return True  # Not applicable on non-Windows
    
    try:
        result = subprocess.run(
            ["wsl", "--status"],
            capture_output=True,
            timeout=10
        )
        output = (result.stdout.decode(errors="ignore") + 
                  result.stderr.decode(errors="ignore"))
        return "WSL 2" in output or "Default Version: 2" in output
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def check_wireshark_installed() -> bool:
    """Check for Wireshark installation."""
    # Windows paths
    win_paths = [
        Path(r"C:\Program Files\Wireshark\Wireshark.exe"),
        Path(r"C:\Program Files (x86)\Wireshark\Wireshark.exe"),
    ]
    
    for p in win_paths:
        if p.exists():
            return True
    
    # Linux/WSL fallback
    return check_command_exists("wireshark") or check_command_exists("tshark")


def check_python_package(package: str) -> bool:
    """Check if a Python package is importable."""
    try:
        __import__(package)
        return True
    except ImportError:
        return False


def get_docker_version() -> str | None:
    """Retrieve Docker version string."""
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    return None


def main() -> int:
    """Execute all environment checks."""
    print("=" * 60)
    print("Environment Verification for Week 1 Laboratory")
    print("NETWORKING class - ASE, Informatics | by Revolvix")
    print("=" * 60)

    checker = EnvironmentChecker()

    # Python Environment
    checker.section("Python Environment")
    py_version = sys.version_info
    checker.check(
        f"Python {py_version.major}.{py_version.minor}.{py_version.micro}",
        py_version >= (3, 11),
        "Install Python 3.11 or later from python.org"
    )

    # Required Python packages
    required_packages = {
        "docker": "pip install docker",
        "requests": "pip install requests",
        "yaml": "pip install pyyaml",
    }
    
    for pkg, install_cmd in required_packages.items():
        pkg_name = "pyyaml" if pkg == "yaml" else pkg
        checker.check(
            f"Python package: {pkg_name}",
            check_python_package(pkg),
            install_cmd
        )

    # Optional packages for advanced exercises
    optional_packages = ["scapy", "dpkt"]
    for pkg in optional_packages:
        if check_python_package(pkg):
            checker.check(f"Python package: {pkg} (optional)", True)
        else:
            checker.warn(pkg, f"Optional package not installed (pip install {pkg})")

    # Docker Environment
    checker.section("Docker Environment")
    
    docker_installed = check_command_exists("docker")
    checker.check(
        "Docker CLI installed",
        docker_installed,
        "Install Docker Desktop from docker.com"
    )

    if docker_installed:
        docker_ver = get_docker_version()
        if docker_ver:
            print(f"         Version: {docker_ver}")

    checker.check(
        "Docker Compose available",
        check_docker_compose(),
        "Docker Compose v2 should come with Docker Desktop"
    )

    checker.check(
        "Docker daemon running",
        check_docker_running(),
        "Start Docker Desktop application"
    )

    # WSL2 Environment (Windows only)
    if sys.platform == "win32":
        checker.section("WSL2 Environment")
        checker.check(
            "WSL2 available and configured",
            check_wsl2_available(),
            "Enable WSL2: wsl --install (requires restart)"
        )

    # Network Tools
    checker.section("Network Analysis Tools")
    
    checker.check(
        "Wireshark installed",
        check_wireshark_installed(),
        "Install Wireshark from wireshark.org"
    )

    if check_command_exists("tshark"):
        checker.check("tshark (CLI) available", True)
    else:
        checker.warn("tshark", "CLI packet analysis will use Docker container")

    # Optional Tools
    checker.section("Optional Tools")
    
    if check_command_exists("git"):
        checker.check("Git installed", True)
    else:
        checker.warn("Git", "Recommended for version control")

    if check_command_exists("curl"):
        checker.check("curl installed", True)
    else:
        checker.warn("curl", "Useful for HTTP testing")

    # Directory Structure
    checker.section("Project Structure")
    
    project_root = Path(__file__).parent.parent
    required_dirs = ["docker", "scripts", "src", "tests", "pcap", "artifacts"]
    
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        checker.check(
            f"Directory: {dir_name}/",
            dir_path.exists(),
            f"Missing directory: {dir_path}"
        )

    # Check docker-compose.yml exists
    compose_file = project_root / "docker" / "docker-compose.yml"
    checker.check(
        "docker-compose.yml present",
        compose_file.exists(),
        "Docker configuration file missing"
    )

    return checker.summary()


if __name__ == "__main__":
    sys.exit(main())
