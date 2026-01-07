#!/usr/bin/env python3
"""
Environment Verification Script
NETWORKING class - ASE, Informatics | by Revolvix

Checks that all prerequisites are installed and configured correctly
for the Week 1 Computer Networks laboratory.

ADAPTED FOR: WSL2 + Ubuntu 22.04 + Docker (in WSL) + Portainer Global
"""

from __future__ import annotations

import subprocess
import sys
import shutil
import os
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

    def info(self, message: str) -> None:
        """Print informational message."""
        print(f"         {message}")

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


def is_running_in_wsl() -> bool:
    """Check if we're running inside WSL."""
    try:
        with open("/proc/version", "r") as f:
            return "microsoft" in f.read().lower()
    except:
        return False


def check_command_exists(cmd: str) -> bool:
    """Check if a command is available in PATH."""
    return shutil.which(cmd) is not None


def check_docker_running_wsl() -> bool:
    """Verify Docker daemon is responsive (WSL environment)."""
    try:
        # In WSL, check docker directly
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=15
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def check_docker_running_windows() -> bool:
    """Verify Docker is accessible from Windows via WSL."""
    try:
        result = subprocess.run(
            ["wsl", "docker", "info"],
            capture_output=True,
            timeout=15
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def check_docker_compose_wsl() -> bool:
    """Verify Docker Compose is available in WSL."""
    try:
        # Try docker-compose (v1 style, common in WSL)
        result = subprocess.run(
            ["docker-compose", "--version"],
            capture_output=True,
            timeout=10
        )
        if result.returncode == 0:
            return True
        
        # Try docker compose (v2 style)
        result = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def check_portainer_running() -> bool:
    """Check if Portainer container is running on port 9000."""
    try:
        if is_running_in_wsl():
            # In WSL, check docker directly
            result = subprocess.run(
                ["docker", "ps", "--filter", "name=portainer", "--format", "{{.Names}}"],
                capture_output=True,
                text=True,
                timeout=10
            )
        else:
            # On Windows, use wsl docker
            result = subprocess.run(
                ["wsl", "docker", "ps", "--filter", "name=portainer", "--format", "{{.Names}}"],
                capture_output=True,
                text=True,
                timeout=10
            )
        
        return "portainer" in result.stdout.lower()
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def check_wsl2_default_ubuntu() -> bool:
    """Check if Ubuntu-22.04 is the default WSL distribution."""
    if sys.platform != "win32":
        # We're in WSL, check if it's Ubuntu
        try:
            result = subprocess.run(
                ["lsb_release", "-d"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return "22.04" in result.stdout
        except:
            return False
    
    try:
        result = subprocess.run(
            ["wsl", "--status"],
            capture_output=True,
            timeout=10
        )
        output = (result.stdout.decode(errors="ignore") + 
                  result.stderr.decode(errors="ignore"))
        return "Ubuntu-22.04" in output or "Ubuntu" in output
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def check_wsl2_available() -> bool:
    """Check if WSL2 is configured."""
    if sys.platform != "win32":
        # We're already in WSL, so it's available
        return is_running_in_wsl()
    
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
    
    # If in WSL, check Windows paths via /mnt/c
    wsl_paths = [
        Path("/mnt/c/Program Files/Wireshark/Wireshark.exe"),
        Path("/mnt/c/Program Files (x86)/Wireshark/Wireshark.exe"),
    ]
    
    for p in wsl_paths:
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
        if is_running_in_wsl():
            result = subprocess.run(
                ["docker", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
        else:
            result = subprocess.run(
                ["wsl", "docker", "--version"],
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
    print("\nEnvironment: WSL2 + Ubuntu 22.04 + Docker + Portainer")
    
    in_wsl = is_running_in_wsl()
    if in_wsl:
        print("Detected: Running inside WSL")
    else:
        print("Detected: Running on Windows")

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

    # WSL2 Environment
    checker.section("WSL2 Environment")
    
    checker.check(
        "WSL2 available and configured",
        check_wsl2_available(),
        "Enable WSL2: wsl --install (requires restart)"
    )
    
    checker.check(
        "Ubuntu 22.04 is default distribution",
        check_wsl2_default_ubuntu(),
        "Set default: wsl --set-default Ubuntu-22.04"
    )

    # Docker Environment (in WSL)
    checker.section("Docker Environment (in WSL)")
    
    if in_wsl:
        docker_installed = check_command_exists("docker")
    else:
        # On Windows, check if wsl docker works
        try:
            result = subprocess.run(["wsl", "which", "docker"], capture_output=True, timeout=5)
            docker_installed = result.returncode == 0
        except:
            docker_installed = False
    
    checker.check(
        "Docker CLI available in WSL",
        docker_installed,
        "Install Docker in WSL: sudo apt install docker.io"
    )

    if docker_installed:
        docker_ver = get_docker_version()
        if docker_ver:
            checker.info(f"Version: {docker_ver}")

    if in_wsl:
        docker_running = check_docker_running_wsl()
    else:
        docker_running = check_docker_running_windows()
    
    checker.check(
        "Docker daemon running",
        docker_running,
        "Start Docker: sudo service docker start (in WSL Ubuntu)"
    )

    if in_wsl:
        compose_ok = check_docker_compose_wsl()
    else:
        try:
            result = subprocess.run(["wsl", "docker-compose", "--version"], capture_output=True, timeout=10)
            compose_ok = result.returncode == 0
        except:
            compose_ok = False
    
    checker.check(
        "Docker Compose available",
        compose_ok,
        "Install: sudo apt install docker-compose"
    )

    # Portainer (Global Service)
    checker.section("Portainer (Global Service)")
    
    portainer_ok = check_portainer_running()
    checker.check(
        "Portainer running on port 9000",
        portainer_ok,
        "Start Portainer: docker start portainer"
    )
    
    if portainer_ok:
        checker.info("Access: http://localhost:9000")
        checker.info("Credentials: stud / studstudstud")

    # Network Tools
    checker.section("Network Analysis Tools")
    
    checker.check(
        "Wireshark installed",
        check_wireshark_installed(),
        "Install Wireshark from wireshark.org (on Windows)"
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
