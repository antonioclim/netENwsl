#!/usr/bin/env python3
"""
Environment Verification Script for Week 11 Laboratory
NETWORKING class - ASE, Informatics | by Revolvix

Checks that all prerequisites are installed and configured correctly.
"""
from __future__ import annotations

import subprocess
import sys
import shutil
import platform
from pathlib import Path


class Checker:
    """Verification checker with pass/fail tracking."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
    
    def check(self, name: str, condition: bool, fix_hint: str = "") -> bool:
        """Check a condition and report result."""
        if condition:
            print(f"  [\033[32mPASS\033[0m] {name}")
            self.passed += 1
            return True
        else:
            print(f"  [\033[31mFAIL\033[0m] {name}")
            if fix_hint:
                print(f"         Fix: {fix_hint}")
            self.failed += 1
            return False
    
    def warn(self, name: str, message: str) -> None:
        """Issue a warning."""
        print(f"  [\033[33mWARN\033[0m] {name}: {message}")
        self.warnings += 1
    
    def info(self, message: str) -> None:
        """Print info message."""
        print(f"  [\033[36mINFO\033[0m] {message}")
    
    def summary(self) -> int:
        """Print summary and return exit code."""
        print("")
        print("=" * 50)
        print(f"Results: {self.passed} passed, {self.failed} failed, {self.warnings} warnings")
        
        if self.failed == 0:
            print("\n\033[32mEnvironment is ready for Week 11 Laboratory!\033[0m")
            return 0
        else:
            print("\n\033[31mPlease fix the issues above before proceeding.\033[0m")
            return 1


def check_command(cmd: str) -> bool:
    """Check if a command is available."""
    return shutil.which(cmd) is not None


def get_command_version(cmd: str, version_arg: str = "--version") -> str:
    """Get version string from a command."""
    try:
        result = subprocess.run(
            [cmd, version_arg],
            capture_output=True,
            text=True,
            timeout=5
        )
        output = result.stdout + result.stderr
        return output.split('\n')[0].strip()
    except Exception:
        return "unknown"


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
    """Check if Docker Compose v2 is available."""
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
    if platform.system() != "Windows":
        return True  # Not applicable on non-Windows
    
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


def main() -> int:
    print("=" * 50)
    print("Environment Verification for Week 11 Laboratory")
    print("NETWORKING class - ASE, Informatics | by Revolvix")
    print("=" * 50)
    print("")
    
    c = Checker()
    
    # ─────────────────────────────────────────────────
    # Python Environment
    # ─────────────────────────────────────────────────
    print("Python Environment:")
    
    py_version = sys.version_info
    c.check(
        f"Python {py_version.major}.{py_version.minor}.{py_version.micro}",
        py_version >= (3, 11),
        "Install Python 3.11 or later from python.org"
    )
    
    # Required Python packages
    required_packages = [
        ("urllib.request", "urllib3", "Built-in - should be available"),
        ("socket", None, "Built-in - should be available"),
        ("concurrent.futures", None, "Built-in - should be available"),
    ]
    
    for pkg, pip_name, hint in required_packages:
        try:
            __import__(pkg.split('.')[0])
            c.check(f"Python module: {pkg}", True)
        except ImportError:
            fix = f"pip install {pip_name}" if pip_name else hint
            c.check(f"Python module: {pkg}", False, fix)
    
    # Optional packages for exercises
    print("\nOptional Python Packages (for exercises):")
    
    optional_packages = [
        ("dnspython", "dnspython>=2.4.0"),
        ("paramiko", "paramiko>=3.3.0"),
        ("pyftpdlib", "pyftpdlib>=1.5.0"),
    ]
    
    for pkg, pip_spec in optional_packages:
        if check_python_package(pkg):
            c.check(f"Python package: {pkg}", True)
        else:
            c.warn(pkg, f"Not installed. Run: pip install {pip_spec}")
    
    # ─────────────────────────────────────────────────
    # Docker Environment
    # ─────────────────────────────────────────────────
    print("\nDocker Environment:")
    
    c.check(
        "Docker installed",
        check_command("docker"),
        "Install Docker Desktop from docker.com"
    )
    
    c.check(
        "Docker Compose v2",
        check_docker_compose(),
        "Docker Compose should come with Docker Desktop"
    )
    
    c.check(
        "Docker daemon running",
        check_docker_running(),
        "Start Docker Desktop application"
    )
    
    if check_command("docker"):
        c.info(f"Docker version: {get_command_version('docker', '--version')}")
    
    # ─────────────────────────────────────────────────
    # WSL2 Environment (Windows only)
    # ─────────────────────────────────────────────────
    if platform.system() == "Windows":
        print("\nWSL2 Environment:")
        c.check(
            "WSL2 available",
            check_wsl2(),
            "Enable WSL2: wsl --install"
        )
    
    # ─────────────────────────────────────────────────
    # Network Tools
    # ─────────────────────────────────────────────────
    print("\nNetwork Tools:")
    
    # Check for Wireshark on Windows
    wireshark_paths = [
        Path(r"C:\Program Files\Wireshark\Wireshark.exe"),
        Path(r"C:\Program Files (x86)\Wireshark\Wireshark.exe"),
    ]
    wireshark_found = any(p.exists() for p in wireshark_paths) or check_command("wireshark")
    
    c.check(
        "Wireshark available",
        wireshark_found,
        "Install Wireshark from wireshark.org"
    )
    
    if check_command("tshark"):
        c.check("tshark (CLI)", True)
    else:
        c.warn("tshark", "Recommended for command-line packet analysis")
    
    # Check curl
    c.check(
        "curl available",
        check_command("curl"),
        "Install curl (usually pre-installed on Windows 10+)"
    )
    
    # ─────────────────────────────────────────────────
    # Optional Tools
    # ─────────────────────────────────────────────────
    print("\nOptional Tools:")
    
    if check_command("git"):
        c.check("Git installed", True)
        c.info(f"Git version: {get_command_version('git', '--version')}")
    else:
        c.warn("Git", "Recommended for version control")
    
    if check_command("ab"):
        c.check("Apache Bench (ab)", True)
    else:
        c.warn("Apache Bench", "Optional for benchmarking. Install Apache httpd or use built-in load generator")
    
    # ─────────────────────────────────────────────────
    # Directory Structure
    # ─────────────────────────────────────────────────
    print("\nDirectory Structure:")
    
    project_root = Path(__file__).parent.parent
    required_dirs = [
        "docker",
        "scripts",
        "src/exercises",
        "tests",
        "pcap",
        "artifacts",
    ]
    
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists():
            c.check(f"Directory: {dir_name}/", True)
        else:
            c.warn(dir_name, f"Creating {dir_name}/...")
            dir_path.mkdir(parents=True, exist_ok=True)
    
    # Check for docker-compose.yml
    compose_file = project_root / "docker" / "docker-compose.yml"
    c.check(
        "docker-compose.yml exists",
        compose_file.exists(),
        "Ensure the Docker configuration is present"
    )
    
    return c.summary()


if __name__ == "__main__":
    sys.exit(main())


# Revolvix&Hypotheticalandrei
