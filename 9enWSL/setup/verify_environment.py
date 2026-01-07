#!/usr/bin/env python3
"""
Environment Verification Script
NETWORKING class - ASE, Informatics | by Revolvix

Checks that all prerequisites are installed and configured correctly
for the Week 9 laboratory environment.

Usage:
    python setup/verify_environment.py
    python setup/verify_environment.py --verbose
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


class Checker:
    """Environment verification helper class."""
    
    def __init__(self, verbose: bool = False):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.verbose = verbose
    
    def check(self, name: str, condition: bool, fix_hint: str = "") -> bool:
        """
        Check a condition and report status.
        
        Args:
            name: Description of the check
            condition: True if check passes
            fix_hint: Suggestion for fixing if check fails
        
        Returns:
            The condition value
        """
        if condition:
            print(f"  [\033[32m✓\033[0m] {name}")
            self.passed += 1
        else:
            print(f"  [\033[31m✗\033[0m] {name}")
            if fix_hint:
                print(f"      Fix: {fix_hint}")
            self.failed += 1
        return condition
    
    def warn(self, name: str, message: str) -> None:
        """Print a warning message."""
        print(f"  [\033[33m!\033[0m] {name}: {message}")
        self.warnings += 1
    
    def info(self, message: str) -> None:
        """Print an info message."""
        if self.verbose:
            print(f"      {message}")
    
    def summary(self) -> int:
        """Print summary and return exit code."""
        print()
        print("=" * 50)
        print(f"Results: {self.passed} passed, {self.failed} failed, {self.warnings} warnings")
        
        if self.failed == 0:
            print("\033[32mEnvironment is ready!\033[0m")
            return 0
        else:
            print("\033[31mPlease fix the issues above before proceeding.\033[0m")
            return 1


def check_command(cmd: str) -> bool:
    """Check if a command is available in PATH."""
    return shutil.which(cmd) is not None


def get_command_version(cmd: str, args: list = None) -> str:
    """Get version string from a command."""
    if args is None:
        args = ["--version"]
    
    try:
        result = subprocess.run(
            [cmd] + args,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout.strip().split('\n')[0]
    except (subprocess.SubprocessError, FileNotFoundError):
        return ""


def check_docker_running() -> bool:
    """Check if Docker daemon is running."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def check_wsl2() -> bool:
    """Check if WSL2 is available."""
    try:
        result = subprocess.run(
            ["wsl", "--status"],
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stdout + result.stderr
        return "WSL 2" in output or "Default Version: 2" in output
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def check_python_package(package: str) -> bool:
    """Check if a Python package is installed."""
    try:
        __import__(package)
        return True
    except ImportError:
        return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify Week 9 Laboratory Environment"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show verbose output"
    )
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("Environment Verification for Week 9 Laboratory")
    print("NETWORKING class - ASE, Informatics")
    print("=" * 50)
    print()
    
    c = Checker(verbose=args.verbose)
    
    # Python Environment
    print("Python Environment:")
    py_version = sys.version_info
    c.check(
        f"Python {py_version.major}.{py_version.minor}.{py_version.micro}",
        py_version >= (3, 8),
        "Install Python 3.8 or later from python.org"
    )
    
    # Python packages
    required_packages = {
        "docker": "pip install docker",
        "requests": "pip install requests",
        "yaml": "pip install pyyaml"
    }
    
    for pkg, install_cmd in required_packages.items():
        pkg_name = "pyyaml" if pkg == "yaml" else pkg
        c.check(
            f"Python package: {pkg_name}",
            check_python_package(pkg),
            install_cmd
        )
    
    # Optional packages
    optional_packages = ["colorama", "rich"]
    for pkg in optional_packages:
        if not check_python_package(pkg):
            c.warn(f"Optional package: {pkg}", f"Install with: pip install {pkg}")
    
    # Docker Environment
    print("\nDocker Environment:")
    
    docker_installed = check_command("docker")
    c.check(
        "Docker installed",
        docker_installed,
        "Install Docker Desktop from docker.com"
    )
    
    if docker_installed:
        version = get_command_version("docker")
        c.info(f"Docker version: {version}")
        
        # Check Docker Compose
        compose_v2 = False
        try:
            result = subprocess.run(
                ["docker", "compose", "version"],
                capture_output=True,
                timeout=5
            )
            compose_v2 = result.returncode == 0
        except subprocess.SubprocessError:
            pass
        
        compose_v1 = check_command("docker-compose")
        
        c.check(
            "Docker Compose installed",
            compose_v2 or compose_v1,
            "Docker Compose should come with Docker Desktop"
        )
        
        c.check(
            "Docker daemon running",
            check_docker_running(),
            "Start Docker Desktop application"
        )
    
    # WSL2 Environment (Windows only)
    print("\nWSL2 Environment:")
    
    if sys.platform == "win32":
        c.check(
            "WSL2 available",
            check_wsl2(),
            "Enable WSL2: wsl --install"
        )
    else:
        c.info("Not on Windows, skipping WSL2 check")
        print("  [·] WSL2: Not applicable (not on Windows)")
    
    # Network Tools
    print("\nNetwork Tools:")
    
    # Wireshark
    wireshark_paths = [
        Path(r"C:\Program Files\Wireshark\Wireshark.exe"),
        Path("/usr/bin/wireshark"),
        Path("/Applications/Wireshark.app/Contents/MacOS/Wireshark")
    ]
    wireshark_found = any(p.exists() for p in wireshark_paths) or check_command("wireshark")
    
    c.check(
        "Wireshark available",
        wireshark_found,
        "Install Wireshark from wireshark.org"
    )
    
    # tshark
    tshark_found = check_command("tshark")
    if tshark_found:
        c.check("tshark available", True)
    else:
        c.warn("tshark", "Install for command-line packet analysis")
    
    # tcpdump (Linux/WSL)
    tcpdump_found = check_command("tcpdump")
    if tcpdump_found:
        c.check("tcpdump available", True)
    elif sys.platform != "win32":
        c.warn("tcpdump", "Install with: sudo apt install tcpdump")
    
    # Optional Tools
    print("\nOptional Tools:")
    
    if check_command("git"):
        version = get_command_version("git")
        c.check(f"Git installed ({version.split()[-1] if version else 'unknown'})", True)
    else:
        c.warn("Git", "Recommended for version control")
    
    if check_command("netcat") or check_command("nc"):
        c.check("Netcat available", True)
    else:
        c.warn("Netcat (nc)", "Useful for network debugging")
    
    # Project Files
    print("\nProject Files:")
    
    project_root = Path(__file__).parent.parent
    
    compose_file = project_root / "docker" / "docker-compose.yml"
    c.check(
        "docker-compose.yml exists",
        compose_file.exists(),
        f"Expected at: {compose_file}"
    )
    
    exercises_dir = project_root / "src" / "exercises"
    c.check(
        "Exercise files present",
        exercises_dir.exists() and any(exercises_dir.glob("*.py")),
        "Exercise files should be in src/exercises/"
    )
    
    return c.summary()


if __name__ == "__main__":
    sys.exit(main())
