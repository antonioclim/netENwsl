#!/usr/bin/env python3
"""
Environment Verification Script
NETWORKING class - ASE, Informatics | by Revolvix

Checks that all prerequisites are installed and configured correctly
for the Week 3 laboratory environment on Windows/WSL2.
"""

import subprocess
import sys
import shutil
import platform
from pathlib import Path
from typing import Tuple


class EnvironmentChecker:
    """Verifies system prerequisites for the laboratory environment."""

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
                print(f"         Fix: {fix_hint}")
            self.failed += 1
            return False

    def warn(self, name: str, message: str) -> None:
        """Record a warning."""
        print(f"  [\033[93mWARN\033[0m] {name}: {message}")
        self.warnings += 1

    def summary(self) -> int:
        """Print summary and return exit code."""
        print("\n" + "=" * 60)
        print(f"Results: {self.passed} passed, {self.failed} failed, {self.warnings} warnings")
        
        if self.failed == 0:
            print("\033[92mEnvironment is ready for Week 3 laboratory!\033[0m")
            return 0
        else:
            print("\033[91mPlease fix the issues above before proceeding.\033[0m")
            return 1


def check_command_exists(cmd: str) -> bool:
    """Check if a command is available in PATH."""
    return shutil.which(cmd) is not None


def run_command(cmd: list, timeout: int = 10) -> Tuple[bool, str]:
    """Run a command and return success status and output."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=timeout,
            text=True
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except FileNotFoundError:
        return False, "Command not found"
    except Exception as e:
        return False, str(e)


def check_python_version() -> Tuple[bool, str]:
    """Check Python version is 3.11 or later."""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    return version >= (3, 11), version_str


def check_docker_installed() -> bool:
    """Check if Docker is installed."""
    return check_command_exists("docker")


def check_docker_running() -> bool:
    """Check if Docker daemon is running."""
    success, _ = run_command(["docker", "info"])
    return success


def check_docker_compose() -> bool:
    """Check if Docker Compose is available."""
    success, _ = run_command(["docker", "compose", "version"])
    return success


def check_wsl2_available() -> bool:
    """Check if WSL2 is available (Windows only)."""
    if platform.system() != "Windows":
        return True  # Not applicable on non-Windows
    
    success, output = run_command(["wsl", "--status"])
    if not success:
        return False
    return "WSL 2" in output or "Default Version: 2" in output


def check_wireshark_installed() -> bool:
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
    return check_command_exists("wireshark")


def check_python_package(package: str) -> bool:
    """Check if a Python package is installed."""
    try:
        __import__(package)
        return True
    except ImportError:
        return False


def main() -> int:
    """Main verification routine."""
    print("=" * 60)
    print("Environment Verification for Week 3 Laboratory")
    print("NETWORKING class - ASE, Informatics | by Revolvix")
    print("=" * 60)
    print()

    checker = EnvironmentChecker()

    # Python Environment
    print("Python Environment:")
    py_ok, py_version = check_python_version()
    checker.check(
        f"Python {py_version}",
        py_ok,
        "Install Python 3.11 or later from https://python.org"
    )

    # Check required Python packages
    required_packages = {
        "yaml": "pyyaml",
        "requests": "requests",
    }
    
    for import_name, pip_name in required_packages.items():
        checker.check(
            f"Python package: {pip_name}",
            check_python_package(import_name),
            f"pip install {pip_name}"
        )

    # Docker Environment
    print("\nDocker Environment:")
    docker_installed = checker.check(
        "Docker installed",
        check_docker_installed(),
        "Install Docker Desktop from https://docker.com"
    )
    
    if docker_installed:
        checker.check(
            "Docker Compose available",
            check_docker_compose(),
            "Docker Compose should be included with Docker Desktop"
        )
        
        checker.check(
            "Docker daemon running",
            check_docker_running(),
            "Start Docker Desktop application"
        )

    # WSL2 Environment (Windows only)
    if platform.system() == "Windows":
        print("\nWSL2 Environment:")
        checker.check(
            "WSL2 available",
            check_wsl2_available(),
            "Enable WSL2: wsl --install"
        )

    # Network Tools
    print("\nNetwork Tools:")
    wireshark_ok = check_wireshark_installed()
    if wireshark_ok:
        checker.check("Wireshark installed", True)
    else:
        checker.warn(
            "Wireshark",
            "Not found. Install from https://wireshark.org for traffic analysis"
        )

    # Optional Tools
    print("\nOptional Tools:")
    if check_command_exists("git"):
        checker.check("Git installed", True)
    else:
        checker.warn("Git", "Recommended for version control")

    if check_command_exists("code"):
        checker.check("VS Code available", True)
    else:
        checker.warn("VS Code", "Recommended editor for Python development")

    # Verify project structure
    print("\nProject Structure:")
    project_root = Path(__file__).parent.parent
    
    required_dirs = ["docker", "scripts", "src", "tests", "docs"]
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        checker.check(
            f"Directory: {dir_name}/",
            dir_path.is_dir(),
            f"Missing directory: {dir_path}"
        )

    docker_compose = project_root / "docker" / "docker-compose.yml"
    checker.check(
        "docker-compose.yml exists",
        docker_compose.is_file(),
        f"Missing: {docker_compose}"
    )

    return checker.summary()


if __name__ == "__main__":
    sys.exit(main())
