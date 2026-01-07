#!/usr/bin/env python3
"""
Environment Verification Script
NETWORKING class - ASE, Informatics | by Revolvix

Checks that all prerequisites are installed and configured correctly
for the Week 7 laboratory environment.
"""

from __future__ import annotations

import subprocess
import sys
import shutil
import platform
from pathlib import Path
from typing import Tuple


class Checker:
    """Tracks verification results with pass/fail/warning states."""
    
    def __init__(self) -> None:
        self.passed = 0
        self.failed = 0
        self.warnings = 0

    def check(self, name: str, condition: bool, fix_hint: str = "") -> bool:
        """Record a check result."""
        if condition:
            print(f"  [PASS] {name}")
            self.passed += 1
            return True
        else:
            print(f"  [FAIL] {name}")
            if fix_hint:
                print(f"         Fix: {fix_hint}")
            self.failed += 1
            return False

    def warn(self, name: str, message: str) -> None:
        """Record a warning (non-critical issue)."""
        print(f"  [WARN] {name}: {message}")
        self.warnings += 1

    def summary(self) -> int:
        """Print summary and return exit code."""
        print()
        print("=" * 60)
        print(f"Results: {self.passed} passed, {self.failed} failed, {self.warnings} warnings")
        print("=" * 60)
        if self.failed == 0:
            print("Environment is ready for Week 7 laboratory!")
            return 0
        else:
            print("Please fix the issues above before proceeding.")
            return 1


def check_command(cmd: str) -> bool:
    """Check if a command is available in PATH."""
    return shutil.which(cmd) is not None


def run_silent(args: list[str], timeout: int = 10) -> Tuple[int, str, str]:
    """Run a command silently and return (returncode, stdout, stderr)."""
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "timeout"
    except FileNotFoundError:
        return -1, "", "not found"
    except Exception as e:
        return -1, "", str(e)


def check_docker_running() -> bool:
    """Check if Docker daemon is running and accessible."""
    rc, stdout, stderr = run_silent(["docker", "info"])
    return rc == 0


def check_docker_compose() -> bool:
    """Check if Docker Compose (V2) is available."""
    rc, stdout, stderr = run_silent(["docker", "compose", "version"])
    return rc == 0


def check_wsl2() -> bool:
    """Check if running in WSL2 or if WSL2 is available on Windows."""
    if platform.system() == "Linux":
        # Check if we're inside WSL
        try:
            with open("/proc/version", "r") as f:
                version = f.read().lower()
                return "microsoft" in version or "wsl" in version
        except Exception:
            return False
    elif platform.system() == "Windows":
        rc, stdout, stderr = run_silent(["wsl", "--status"])
        output = stdout + stderr
        return "WSL 2" in output or "Default Version: 2" in output
    return False


def check_python_package(package: str) -> bool:
    """Check if a Python package is importable."""
    try:
        __import__(package)
        return True
    except ImportError:
        return False


def get_wireshark_path() -> Path | None:
    """Find Wireshark installation on Windows."""
    possible_paths = [
        Path(r"C:\Program Files\Wireshark\Wireshark.exe"),
        Path(r"C:\Program Files (x86)\Wireshark\Wireshark.exe"),
    ]
    for p in possible_paths:
        if p.exists():
            return p
    return None


def main() -> int:
    """Run all environment checks."""
    print("=" * 60)
    print("Environment Verification for Week 7 Laboratory")
    print("NETWORKING class - ASE, Informatics | by Revolvix")
    print("=" * 60)
    print()

    c = Checker()
    system = platform.system()

    # Python Environment
    print("Python Environment:")
    py_version = sys.version_info
    c.check(
        f"Python {py_version.major}.{py_version.minor}.{py_version.micro}",
        py_version >= (3, 11),
        "Install Python 3.11 or later from python.org"
    )

    # Required Python packages
    required_packages = [
        ("yaml", "pyyaml"),
        ("requests", "requests"),
    ]
    for import_name, pip_name in required_packages:
        if check_python_package(import_name):
            c.check(f"Python package: {pip_name}", True)
        else:
            c.check(f"Python package: {pip_name}", False, f"pip install {pip_name}")

    # Optional packages
    optional_packages = ["docker", "colorama"]
    for pkg in optional_packages:
        if check_python_package(pkg):
            c.check(f"Optional package: {pkg}", True)
        else:
            c.warn(pkg, f"Not installed. Run: pip install {pkg}")

    print()
    print("Docker Environment:")
    c.check(
        "Docker installed",
        check_command("docker"),
        "Install Docker Desktop from docker.com"
    )
    c.check(
        "Docker Compose V2 installed",
        check_docker_compose(),
        "Docker Compose should come with Docker Desktop"
    )
    c.check(
        "Docker daemon running",
        check_docker_running(),
        "Start Docker Desktop application"
    )

    # Check Docker version
    if check_command("docker"):
        rc, stdout, stderr = run_silent(["docker", "version", "--format", "{{.Server.Version}}"])
        if rc == 0 and stdout.strip():
            print(f"         Docker version: {stdout.strip()}")

    print()
    print("WSL2 Environment:")
    if system == "Windows":
        c.check(
            "WSL2 available",
            check_wsl2(),
            "Enable WSL2: wsl --install"
        )
    elif system == "Linux":
        is_wsl = check_wsl2()
        if is_wsl:
            c.check("Running inside WSL2", True)
        else:
            c.warn("WSL2", "Not running in WSL2 (native Linux detected)")

    print()
    print("Network Tools:")
    
    # Wireshark
    if system == "Windows":
        wireshark_path = get_wireshark_path()
        c.check(
            "Wireshark installed",
            wireshark_path is not None,
            "Install Wireshark from wireshark.org"
        )
        if wireshark_path:
            print(f"         Found at: {wireshark_path}")
    else:
        # In WSL/Linux, check for tshark
        has_wireshark = check_command("wireshark") or check_command("tshark")
        c.check(
            "Wireshark/tshark installed",
            has_wireshark,
            "sudo apt install wireshark tshark"
        )

    # tcpdump (useful in WSL)
    if system == "Linux" or check_wsl2():
        if check_command("tcpdump"):
            c.check("tcpdump installed", True)
        else:
            c.warn("tcpdump", "Not installed. Run: sudo apt install tcpdump")

    print()
    print("Optional Tools:")
    
    # Git
    if check_command("git"):
        c.check("Git installed", True)
        rc, stdout, stderr = run_silent(["git", "--version"])
        if rc == 0:
            print(f"         {stdout.strip()}")
    else:
        c.warn("Git", "Recommended for version control")

    # netcat
    if check_command("nc") or check_command("netcat"):
        c.check("netcat installed", True)
    else:
        c.warn("netcat", "Useful for debugging. Run: sudo apt install netcat-openbsd")

    print()
    print("Directory Structure:")
    script_dir = Path(__file__).resolve().parent.parent
    required_dirs = ["docker", "scripts", "src", "tests", "docs", "pcap", "artifacts"]
    for d in required_dirs:
        dir_path = script_dir / d
        if dir_path.exists():
            c.check(f"Directory: {d}/", True)
        else:
            c.check(f"Directory: {d}/", False, f"Missing directory structure")

    return c.summary()


if __name__ == "__main__":
    sys.exit(main())
