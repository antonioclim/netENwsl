#!/usr/bin/env python3
"""
Environment Verification Script
NETWORKING class - ASE, Informatics | by Revolvix

Checks that all prerequisites are installed and configured correctly.
"""

import subprocess
import sys
import shutil
from pathlib import Path


class Checker:
    """Environment check manager."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0

    def check(self, name: str, condition: bool, fix_hint: str = ""):
        if condition:
            print(f"  [PASS] {name}")
            self.passed += 1
        else:
            print(f"  [FAIL] {name}")
            if fix_hint:
                print(f"         Fix: {fix_hint}")
            self.failed += 1

    def warn(self, name: str, message: str):
        print(f"  [WARN] {name}: {message}")
        self.warnings += 1

    def summary(self) -> int:
        print("\n" + "=" * 50)
        print(f"Results: {self.passed} passed, {self.failed} failed, {self.warnings} warnings")
        if self.failed == 0:
            print("Environment is ready!")
            return 0
        else:
            print("Please fix the issues above before proceeding.")
            return 1


def check_command(cmd: str) -> bool:
    """Check if a command is available."""
    return shutil.which(cmd) is not None


def check_docker_running() -> bool:
    """Check if Docker daemon is running."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except Exception:
        return False


def check_docker_compose() -> bool:
    """Check if Docker Compose is available."""
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
    """Check if WSL2 is available (Windows only)."""
    if sys.platform != "win32":
        return True  # Not applicable on other platforms
    
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


def check_python_package(package: str) -> bool:
    """Check if a Python package is installed."""
    try:
        __import__(package)
        return True
    except ImportError:
        return False


def check_wireshark() -> bool:
    """Check if Wireshark is available."""
    # Windows paths
    windows_paths = [
        Path(r"C:\Program Files\Wireshark\Wireshark.exe"),
        Path(r"C:\Program Files (x86)\Wireshark\Wireshark.exe"),
    ]
    
    for path in windows_paths:
        if path.exists():
            return True
    
    # Linux/Mac
    return check_command("wireshark") or check_command("tshark")


def main():
    print("=" * 50)
    print("Environment Verification for Week 5 Laboratory")
    print("NETWORKING class - ASE, Informatics")
    print("=" * 50)
    print()

    c = Checker()

    # Python version check
    print("Python Environment:")
    py_version = sys.version_info
    c.check(
        f"Python {py_version.major}.{py_version.minor}.{py_version.micro}",
        py_version >= (3, 10),
        "Install Python 3.10 or later from python.org"
    )

    # Python packages
    required_packages = {
        "ipaddress": "Standard library (should be built-in)",
    }
    optional_packages = {
        "docker": "pip install docker",
        "requests": "pip install requests",
        "yaml": "pip install pyyaml",
    }
    
    for pkg, fix in required_packages.items():
        c.check(f"Python package: {pkg}", check_python_package(pkg), fix)
    
    for pkg, fix in optional_packages.items():
        if check_python_package(pkg):
            c.check(f"Python package: {pkg}", True)
        else:
            c.warn(pkg, f"Optional. Install with: {fix}")

    # Docker environment
    print("\nDocker Environment:")
    c.check(
        "Docker installed",
        check_command("docker"),
        "Install Docker Desktop from docker.com"
    )
    c.check(
        "Docker Compose installed",
        check_docker_compose(),
        "Docker Compose should come with Docker Desktop"
    )
    c.check(
        "Docker daemon running",
        check_docker_running(),
        "Start Docker Desktop application"
    )

    # WSL2 (Windows only)
    if sys.platform == "win32":
        print("\nWSL2 Environment:")
        c.check(
            "WSL2 available",
            check_wsl2(),
            "Enable WSL2: wsl --install"
        )

    # Network tools
    print("\nNetwork Tools:")
    if check_wireshark():
        c.check("Wireshark available", True)
    else:
        c.warn("Wireshark", "Install from wireshark.org for packet analysis")

    # Optional tools
    print("\nOptional Tools:")
    if check_command("git"):
        c.check("Git installed", True)
    else:
        c.warn("Git", "Recommended for version control")
    
    if check_command("tcpdump"):
        c.check("tcpdump installed", True)
    else:
        c.warn("tcpdump", "Available inside Docker containers")

    # File system check
    print("\nProject Structure:")
    project_root = Path(__file__).parent.parent
    
    required_dirs = ["docker", "scripts", "src", "tests"]
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        c.check(f"Directory: {dir_name}/", dir_path.exists())
    
    compose_file = project_root / "docker" / "docker-compose.yml"
    c.check("docker-compose.yml exists", compose_file.exists())

    return c.summary()


if __name__ == "__main__":
    sys.exit(main())
