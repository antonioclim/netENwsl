#!/usr/bin/env python3
"""
Environment Verification Script
NETWORKING class - ASE, Informatics | by Revolvix

Checks that all prerequisites are installed and configured correctly
for the Week 8 laboratory session.
"""

import subprocess
import sys
import shutil
import platform
from pathlib import Path
from typing import Callable, Optional


class EnvironmentChecker:
    """Comprehensive environment verification utility."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.is_windows = platform.system() == "Windows"
    
    def check(self, name: str, condition: bool, fix_hint: str = "") -> bool:
        """Record a check result."""
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
    
    def warn(self, name: str, message: str):
        """Record a warning."""
        print(f"  [\033[93mWARN\033[0m] {name}: {message}")
        self.warnings += 1
    
    def info(self, message: str):
        """Print informational message."""
        print(f"  [\033[94mINFO\033[0m] {message}")
    
    def summary(self) -> int:
        """Print summary and return exit code."""
        print()
        print("=" * 60)
        print(f"Results: \033[92m{self.passed} passed\033[0m, "
              f"\033[91m{self.failed} failed\033[0m, "
              f"\033[93m{self.warnings} warnings\033[0m")
        
        if self.failed == 0:
            print("\n\033[92m✓ Environment is ready for Week 8!\033[0m")
            return 0
        else:
            print("\n\033[91m✗ Please fix the issues above before proceeding.\033[0m")
            return 1


def check_command_exists(cmd: str) -> bool:
    """Check if a command is available in PATH."""
    return shutil.which(cmd) is not None


def get_command_version(cmd: str, version_flag: str = "--version") -> Optional[str]:
    """Get version string from a command."""
    try:
        result = subprocess.run(
            [cmd, version_flag],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout.strip() or result.stderr.strip()
    except Exception:
        return None


def check_docker_running() -> bool:
    """Check if Docker daemon is running."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=15
        )
        return result.returncode == 0
    except Exception:
        return False


def check_docker_compose() -> bool:
    """Check if Docker Compose V2 is available."""
    try:
        result = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except Exception:
        return False


def check_wsl2_available() -> bool:
    """Check if WSL2 is available (Windows only)."""
    if platform.system() != "Windows":
        return True  # Not applicable
    
    try:
        result = subprocess.run(
            ["wsl", "--status"],
            capture_output=True,
            timeout=10
        )
        output = (result.stdout.decode("utf-8", errors="ignore") + 
                  result.stderr.decode("utf-8", errors="ignore"))
        return "WSL 2" in output or "Default Version: 2" in output
    except Exception:
        return False


def check_python_package(package: str) -> bool:
    """Check if a Python package is installed."""
    try:
        __import__(package)
        return True
    except ImportError:
        return False


def check_port_available(port: int) -> bool:
    """Check if a port is available for binding."""
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", port))
            return True
    except OSError:
        return False


def main():
    print("=" * 60)
    print("Environment Verification for Week 8 Laboratory")
    print("Transport Layer: HTTP Server and Reverse Proxies")
    print("NETWORKING class - ASE, Informatics")
    print("=" * 60)
    print()
    
    c = EnvironmentChecker()
    
    # =========================================================================
    # Python Environment
    # =========================================================================
    print("\033[1mPython Environment:\033[0m")
    
    py_version = sys.version_info
    c.check(
        f"Python {py_version.major}.{py_version.minor}.{py_version.micro}",
        py_version >= (3, 11),
        "Install Python 3.11 or later from https://python.org"
    )
    
    # Required packages
    required_packages = {
        "docker": "pip install docker",
        "requests": "pip install requests",
        "yaml": "pip install pyyaml",
    }
    
    for pkg, install_cmd in required_packages.items():
        pkg_name = "pyyaml" if pkg == "yaml" else pkg
        c.check(
            f"Python package: {pkg_name}",
            check_python_package(pkg),
            install_cmd
        )
    
    # Optional packages
    optional_packages = ["pytest", "httpx", "rich"]
    for pkg in optional_packages:
        if check_python_package(pkg):
            c.check(f"Python package: {pkg} (optional)", True)
        else:
            c.warn(pkg, f"Optional package not installed (pip install {pkg})")
    
    # =========================================================================
    # Docker Environment
    # =========================================================================
    print("\n\033[1mDocker Environment:\033[0m")
    
    docker_installed = check_command_exists("docker")
    c.check(
        "Docker installed",
        docker_installed,
        "Install Docker Desktop from https://docker.com"
    )
    
    if docker_installed:
        c.check(
            "Docker Compose V2 available",
            check_docker_compose(),
            "Docker Compose should come with Docker Desktop"
        )
        
        docker_running = check_docker_running()
        c.check(
            "Docker daemon running",
            docker_running,
            "Start Docker Desktop application"
        )
        
        if docker_running:
            # Check Docker version
            version = get_command_version("docker")
            if version:
                c.info(f"Docker version: {version.split(chr(10))[0]}")
    
    # =========================================================================
    # WSL2 Environment (Windows only)
    # =========================================================================
    if platform.system() == "Windows":
        print("\n\033[1mWSL2 Environment:\033[0m")
        c.check(
            "WSL2 available",
            check_wsl2_available(),
            "Enable WSL2: wsl --install"
        )
    
    # =========================================================================
    # Network Tools
    # =========================================================================
    print("\n\033[1mNetwork Tools:\033[0m")
    
    # Wireshark
    wireshark_paths = [
        Path(r"C:\Program Files\Wireshark\Wireshark.exe"),
        Path(r"C:\Program Files (x86)\Wireshark\Wireshark.exe"),
    ]
    wireshark_installed = (
        any(p.exists() for p in wireshark_paths) or 
        check_command_exists("wireshark")
    )
    c.check(
        "Wireshark installed",
        wireshark_installed,
        "Install Wireshark from https://wireshark.org"
    )
    
    # curl
    curl_installed = check_command_exists("curl")
    c.check(
        "curl installed",
        curl_installed,
        "curl should be available on modern Windows/Linux"
    )
    
    # netcat (optional)
    if check_command_exists("nc") or check_command_exists("netcat"):
        c.check("netcat available (optional)", True)
    else:
        c.warn("netcat", "Not installed (useful for raw socket testing)")
    
    # =========================================================================
    # Port Availability
    # =========================================================================
    print("\n\033[1mPort Availability:\033[0m")
    
    critical_ports = [8080, 8443, 9443]
    for port in critical_ports:
        available = check_port_available(port)
        c.check(
            f"Port {port} available",
            available,
            f"Another process is using port {port}. Stop it or use alternative ports."
        )
    
    # =========================================================================
    # Directory Structure
    # =========================================================================
    print("\n\033[1mDirectory Structure:\033[0m")
    
    script_dir = Path(__file__).parent.parent
    required_dirs = ["docker", "scripts", "src", "tests", "www", "pcap"]
    
    for dir_name in required_dirs:
        dir_path = script_dir / dir_name
        c.check(
            f"Directory exists: {dir_name}/",
            dir_path.exists(),
            f"Missing directory: {dir_path}"
        )
    
    # =========================================================================
    # Optional Tools
    # =========================================================================
    print("\n\033[1mOptional Tools:\033[0m")
    
    if check_command_exists("git"):
        c.check("Git installed", True)
        version = get_command_version("git")
        if version:
            c.info(f"Git version: {version.split(chr(10))[0]}")
    else:
        c.warn("Git", "Recommended for version control")
    
    if check_command_exists("code"):
        c.check("VS Code available", True)
    else:
        c.warn("VS Code", "Recommended IDE for development")
    
    # =========================================================================
    # Summary
    # =========================================================================
    return c.summary()


if __name__ == "__main__":
    sys.exit(main())
