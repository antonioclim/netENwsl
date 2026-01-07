#!/usr/bin/env python3
"""
Environment Verification Script
NETWORKING class - ASE, Informatics | by Revolvix

Checks that all prerequisites are installed and configured correctly
for the Week 13 IoT and Security laboratory.
"""

import subprocess
import sys
import shutil
import platform
from pathlib import Path
from typing import Optional


class Checker:
    """Environment verification checker with pass/fail/warning tracking."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
    
    def check(self, name: str, condition: bool, fix_hint: str = "") -> None:
        """Record a check result."""
        if condition:
            print(f"  [PASS] {name}")
            self.passed += 1
        else:
            print(f"  [FAIL] {name}")
            if fix_hint:
                print(f"         Fix: {fix_hint}")
            self.failed += 1
    
    def warn(self, name: str, message: str) -> None:
        """Record a warning (non-critical)."""
        print(f"  [WARN] {name}: {message}")
        self.warnings += 1
    
    def summary(self) -> int:
        """Print summary and return exit code."""
        print("\n" + "=" * 60)
        print(f"Results: {self.passed} passed, {self.failed} failed, {self.warnings} warnings")
        if self.failed == 0:
            print("Environment is ready!")
            return 0
        else:
            print("Please fix the issues above before proceeding.")
            return 1


def check_command(cmd: str) -> bool:
    """Check if a command exists in PATH."""
    return shutil.which(cmd) is not None


def check_docker_running() -> bool:
    """Check if Docker daemon is running and accessible."""
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
    """Check if docker compose command works."""
    try:
        result = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except Exception:
        return False


def check_wsl2() -> bool:
    """Check if WSL2 is available and default."""
    if platform.system() != "Windows":
        return True  # Not on Windows, skip WSL check
    try:
        result = subprocess.run(
            ["wsl", "--status"],
            capture_output=True,
            timeout=10
        )
        output = result.stdout.decode() + result.stderr.decode()
        return "WSL 2" in output or "Default Version: 2" in output
    except Exception:
        return False


def get_python_version() -> tuple:
    """Get Python version as tuple."""
    return sys.version_info[:3]


def check_python_package(package_name: str) -> bool:
    """Check if a Python package is importable."""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False


def check_wireshark() -> bool:
    """Check if Wireshark is installed."""
    # Check common Windows installation paths
    wireshark_paths = [
        Path(r"C:\Program Files\Wireshark\Wireshark.exe"),
        Path(r"C:\Program Files (x86)\Wireshark\Wireshark.exe"),
    ]
    for path in wireshark_paths:
        if path.exists():
            return True
    # Also check PATH
    return check_command("wireshark")


def get_docker_version() -> Optional[str]:
    """Get Docker version string."""
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            timeout=10
        )
        if result.returncode == 0:
            return result.stdout.decode().strip()
    except Exception:
        pass
    return None


def main() -> int:
    """Run all environment checks."""
    print("=" * 60)
    print("Environment Verification for Week 13 Laboratory")
    print("IoT and Security in Computer Networks")
    print("NETWORKING class - ASE, Informatics")
    print("=" * 60)
    print()
    
    c = Checker()
    
    # Python Environment
    print("Python Environment:")
    py_version = get_python_version()
    c.check(
        f"Python {py_version[0]}.{py_version[1]}.{py_version[2]}",
        py_version >= (3, 11),
        "Install Python 3.11 or later from python.org"
    )
    
    # Required Python packages
    required_packages = [
        ("docker", "pip install docker"),
        ("requests", "pip install requests"),
        ("yaml", "pip install pyyaml"),
    ]
    for pkg, install_cmd in required_packages:
        c.check(
            f"Python package: {pkg}",
            check_python_package(pkg),
            install_cmd
        )
    
    # Optional but recommended packages
    optional_packages = [
        ("paho.mqtt.client", "paho-mqtt", "pip install paho-mqtt"),
        ("scapy", "scapy", "pip install scapy"),
    ]
    for import_name, display_name, install_cmd in optional_packages:
        try:
            parts = import_name.split(".")
            pkg = __import__(parts[0])
            for part in parts[1:]:
                pkg = getattr(pkg, part)
            c.check(f"Python package: {display_name}", True)
        except (ImportError, AttributeError):
            c.warn(f"Python package: {display_name}", f"Optional. Install with: {install_cmd}")
    
    print("\nDocker Environment:")
    c.check(
        "Docker installed",
        check_command("docker"),
        "Install Docker Desktop from docker.com"
    )
    
    docker_version = get_docker_version()
    if docker_version:
        print(f"         Version: {docker_version}")
    
    c.check(
        "Docker Compose available",
        check_docker_compose(),
        "Docker Compose should come with Docker Desktop"
    )
    
    c.check(
        "Docker daemon running",
        check_docker_running(),
        "Start Docker Desktop application"
    )
    
    print("\nWSL2 Environment:")
    if platform.system() == "Windows":
        c.check(
            "WSL2 available",
            check_wsl2(),
            "Enable WSL2: wsl --install"
        )
    else:
        print("  [INFO] Not running on Windows, skipping WSL2 check")
    
    print("\nNetwork Tools:")
    c.check(
        "Wireshark available",
        check_wireshark(),
        "Install Wireshark from wireshark.org"
    )
    
    if check_command("tcpdump"):
        c.check("tcpdump available", True)
    else:
        c.warn("tcpdump", "Optional. Useful for command-line captures")
    
    if check_command("netcat") or check_command("nc"):
        c.check("netcat available", True)
    else:
        c.warn("netcat", "Optional. Useful for network testing")
    
    print("\nOptional Tools:")
    if check_command("git"):
        c.check("Git installed", True)
    else:
        c.warn("Git", "Recommended for version control")
    
    if check_command("curl"):
        c.check("curl installed", True)
    else:
        c.warn("curl", "Useful for HTTP testing")
    
    # Check project structure
    print("\nProject Structure:")
    project_root = Path(__file__).parent.parent
    required_dirs = ["docker", "scripts", "src", "tests", "docs"]
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        c.check(f"Directory: {dir_name}/", dir_path.is_dir())
    
    # Check Docker configuration
    compose_file = project_root / "docker" / "docker-compose.yml"
    c.check(
        "docker-compose.yml present",
        compose_file.is_file(),
        "Docker configuration file is missing"
    )
    
    return c.summary()


if __name__ == "__main__":
    sys.exit(main())
