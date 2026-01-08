#!/usr/bin/env python3
"""
Environment Verification Script
NETWORKING class - ASE, Informatics | by Revolvix

Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment

Checks that all prerequisites are installed and configured correctly
for the Week 1 Computer Networks laboratory.
"""

from __future__ import annotations

import subprocess
import sys
import shutil
import os
import socket
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional


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

    def info(self, name: str, message: str) -> None:
        """Display informational message."""
        print(f"  [\033[94mINFO\033[0m] {name}: {message}")

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


def check_running_in_wsl() -> bool:
    """Check if we're running inside WSL."""
    # Check for WSL-specific indicators
    if os.path.exists("/proc/sys/fs/binfmt_misc/WSLInterop"):
        return True
    
    # Check for WSL environment variable
    if "WSL_DISTRO_NAME" in os.environ:
        return True
    
    # Check /proc/version for WSL string
    try:
        with open("/proc/version", "r") as f:
            version = f.read().lower()
            return "microsoft" in version or "wsl" in version
    except (FileNotFoundError, IOError):
        pass
    
    return False


def get_wsl_distro_info() -> tuple[Optional[str], Optional[str]]:
    """Get WSL distribution name and version."""
    distro_name = os.environ.get("WSL_DISTRO_NAME")
    
    # Get Ubuntu version
    version = None
    try:
        result = subprocess.run(
            ["lsb_release", "-rs"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        # Try alternative method
        try:
            with open("/etc/os-release", "r") as f:
                for line in f:
                    if line.startswith("VERSION_ID="):
                        version = line.split("=")[1].strip().strip('"')
                        break
        except (FileNotFoundError, IOError):
            pass
    
    return distro_name, version


def check_docker_running() -> bool:
    """Verify Docker daemon is responsive (in WSL, not Docker Desktop)."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=15
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def check_docker_in_wsl() -> bool:
    """Verify Docker is running natively in WSL, not via Docker Desktop."""
    try:
        result = subprocess.run(
            ["docker", "info", "--format", "{{.OperatingSystem}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            os_info = result.stdout.strip().lower()
            # Docker Desktop shows "Docker Desktop" in OperatingSystem
            # Native Docker in WSL shows Ubuntu/Linux
            return "docker desktop" not in os_info
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
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


def check_docker_service_status() -> str:
    """Check Docker service status in WSL."""
    try:
        result = subprocess.run(
            ["service", "docker", "status"],
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stdout + result.stderr
        if "running" in output.lower():
            return "running"
        elif "stopped" in output.lower() or "not running" in output.lower():
            return "stopped"
        return "unknown"
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return "unknown"


def check_portainer_running() -> bool:
    """Check if Portainer container is running on port 9000."""
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=portainer", "--format", "{{.Status}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            return "up" in result.stdout.lower()
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    return False


def check_portainer_accessible() -> bool:
    """Check if Portainer web interface is accessible on port 9000."""
    try:
        # Try to connect to Portainer
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(5)
            result = sock.connect_ex(('localhost', 9000))
            return result == 0
    except (socket.error, OSError):
        return False


def check_wireshark_installed() -> bool:
    """Check for Wireshark installation (Windows native or WSL)."""
    # Check common Windows paths via WSL mount
    win_paths = [
        Path("/mnt/c/Program Files/Wireshark/Wireshark.exe"),
        Path("/mnt/c/Program Files (x86)/Wireshark/Wireshark.exe"),
    ]
    
    for p in win_paths:
        if p.exists():
            return True
    
    # Check in WSL (tshark is the CLI component)
    return check_command_exists("wireshark") or check_command_exists("tshark")


def check_python_package(package: str) -> bool:
    """Check if a Python package is importable."""
    try:
        __import__(package)
        return True
    except ImportError:
        return False


def get_docker_version() -> Optional[str]:
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


def try_start_docker() -> bool:
    """Attempt to start Docker service (requires sudo)."""
    print("         \033[93mAttempting to start Docker...\033[0m")
    try:
        result = subprocess.run(
            ["sudo", "service", "docker", "start"],
            capture_output=True,
            timeout=30
        )
        if result.returncode == 0:
            # Wait a moment for Docker to initialize
            import time
            time.sleep(2)
            return check_docker_running()
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    return False


def main() -> int:
    """Execute all environment checks."""
    print("=" * 60)
    print("Environment Verification for Week 1 Laboratory")
    print("NETWORKING class - ASE, Informatics | by Revolvix")
    print("WSL2 + Ubuntu 22.04 + Docker + Portainer Environment")
    print("=" * 60)

    checker = EnvironmentChecker()

    # WSL2 Environment
    checker.section("WSL2 Environment")
    
    is_wsl = check_running_in_wsl()
    checker.check(
        "Running in WSL",
        is_wsl,
        "This script should be run from within WSL Ubuntu terminal"
    )
    
    if is_wsl:
        distro_name, distro_version = get_wsl_distro_info()
        
        if distro_name:
            checker.info("WSL Distribution", distro_name)
        
        if distro_version:
            is_ubuntu_22 = distro_version.startswith("22.")
            checker.check(
                f"Ubuntu version {distro_version}",
                is_ubuntu_22,
                "Recommended: Ubuntu 22.04 LTS. Install with: wsl --install -d Ubuntu-22.04"
            )
        else:
            checker.warn("Ubuntu version", "Could not determine version")

    # Python Environment
    checker.section("Python Environment")
    py_version = sys.version_info
    checker.check(
        f"Python {py_version.major}.{py_version.minor}.{py_version.micro}",
        py_version >= (3, 11),
        "Install Python 3.11+: sudo apt install python3.11"
    )

    # Required Python packages
    required_packages = {
        "docker": "pip install docker --break-system-packages",
        "requests": "pip install requests --break-system-packages",
        "yaml": "pip install pyyaml --break-system-packages",
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
            checker.warn(pkg, f"Optional package (pip install {pkg} --break-system-packages)")

    # Docker Environment
    checker.section("Docker Environment")
    
    docker_installed = check_command_exists("docker")
    checker.check(
        "Docker CLI installed",
        docker_installed,
        "Install Docker: sudo apt install docker.io"
    )

    if docker_installed:
        docker_ver = get_docker_version()
        if docker_ver:
            print(f"         Version: {docker_ver}")
    
    docker_running = check_docker_running()
    if not docker_running:
        # Try to start Docker
        checker.warn("Docker daemon", "Not running, attempting to start...")
        docker_running = try_start_docker()
    
    checker.check(
        "Docker daemon running",
        docker_running,
        "Start Docker: sudo service docker start"
    )
    
    if docker_running:
        # Check it's native Docker, not Docker Desktop
        is_native = check_docker_in_wsl()
        if is_native:
            checker.check("Docker running natively in WSL", True)
        else:
            checker.warn(
                "Docker Desktop detected",
                "Consider using native Docker in WSL for better performance"
            )

    checker.check(
        "Docker Compose available",
        check_docker_compose(),
        "Docker Compose v2 should be included with docker.io package"
    )

    # Portainer (Global Service)
    checker.section("Portainer (Global Service - Port 9000)")
    
    portainer_running = check_portainer_running()
    portainer_accessible = check_portainer_accessible()
    
    checker.check(
        "Portainer container running",
        portainer_running,
        "Start Portainer: docker start portainer"
    )
    
    checker.check(
        "Portainer accessible on http://localhost:9000",
        portainer_accessible,
        "If container missing, create it (see troubleshooting section)"
    )
    
    if not portainer_running and docker_running:
        print("\n         \033[93mTo create Portainer if it doesn't exist:\033[0m")
        print("         docker run -d -p 9000:9000 --name portainer --restart=always \\")
        print("           -v /var/run/docker.sock:/var/run/docker.sock \\")
        print("           -v portainer_data:/data portainer/portainer-ce:latest")
    
    if portainer_running:
        checker.info("Portainer credentials", "stud / studstudstud")

    # Network Analysis Tools
    checker.section("Network Analysis Tools")
    
    wireshark_installed = check_wireshark_installed()
    checker.check(
        "Wireshark installed",
        wireshark_installed,
        "Install Wireshark on Windows from wireshark.org"
    )

    if check_command_exists("tshark"):
        checker.check("tshark (CLI) available in WSL", True)
    else:
        checker.warn("tshark", "Install: sudo apt install tshark")

    if check_command_exists("tcpdump"):
        checker.check("tcpdump available", True)
    else:
        checker.warn("tcpdump", "Install: sudo apt install tcpdump")

    # Optional Tools
    checker.section("Optional Tools")
    
    if check_command_exists("git"):
        checker.check("Git installed", True)
    else:
        checker.warn("Git", "Recommended: sudo apt install git")

    if check_command_exists("curl"):
        checker.check("curl installed", True)
    else:
        checker.warn("curl", "Install: sudo apt install curl")

    if check_command_exists("nc") or check_command_exists("netcat"):
        checker.check("netcat installed", True)
    else:
        checker.warn("netcat", "Install: sudo apt install netcat-openbsd")

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

    # Final Information
    checker.section("Access Information")
    print("  Portainer:     http://localhost:9000")
    print("  Credentials:   stud / studstudstud")
    print("  Lab Container: docker exec -it week1_lab bash")
    print("  TCP Port:      9090")
    print("  UDP Port:      9091")

    return checker.summary()


if __name__ == "__main__":
    sys.exit(main())
