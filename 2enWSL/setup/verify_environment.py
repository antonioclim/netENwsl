#!/usr/bin/env python3
"""
Environment Verification Script
NETWORKING class - ASE, Informatics | by Revolvix

Checks that all prerequisites are installed and configured correctly
for the Week 2 Socket Programming laboratory.
"""

import subprocess
import sys
import shutil
import platform
from pathlib import Path
from typing import Tuple, Optional


class Checker:
    """Verification result collector with formatted output."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
    
    def check(self, name: str, condition: bool, fix_hint: str = "") -> bool:
        """Record a check result."""
        if condition:
            print(f"  [\033[92mPASS\033[0m] {name}")
            self.passed += 1
        else:
            print(f"  [\033[91mFAIL\033[0m] {name}")
            if fix_hint:
                print(f"         \033[93mFix:\033[0m {fix_hint}")
            self.failed += 1
        return condition
    
    def warn(self, name: str, message: str) -> None:
        """Record a warning."""
        print(f"  [\033[93mWARN\033[0m] {name}: {message}")
        self.warnings += 1
    
    def info(self, message: str) -> None:
        """Display informational message."""
        print(f"  [\033[94mINFO\033[0m] {message}")
    
    def summary(self) -> int:
        """Print summary and return exit code."""
        print()
        print("=" * 60)
        total = self.passed + self.failed
        print(f"Results: {self.passed}/{total} passed, {self.failed} failed, {self.warnings} warnings")
        print()
        
        if self.failed == 0:
            print("\033[92m✓ Environment is ready for Week 2 laboratory!\033[0m")
            print()
            print("Next steps:")
            print("  1. Start the lab: python scripts/start_lab.py")
            print("  2. Run the demo:  python scripts/run_demo.py")
            return 0
        else:
            print("\033[91m✗ Please fix the issues above before proceeding.\033[0m")
            print()
            print("For automated fixes, try: python setup/install_prerequisites.py")
            return 1


def get_command_output(cmd: list[str], timeout: int = 10) -> Tuple[bool, str]:
    """Execute command and return success status with output."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=timeout,
            text=True
        )
        output = result.stdout.strip() or result.stderr.strip()
        return result.returncode == 0, output
    except FileNotFoundError:
        return False, "Command not found"
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except Exception as e:
        return False, str(e)


def check_command_exists(cmd: str) -> bool:
    """Check if command is available in PATH."""
    return shutil.which(cmd) is not None


def check_python_version() -> Tuple[bool, str]:
    """Verify Python version meets requirements."""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    meets_req = version >= (3, 11)
    return meets_req, version_str


def check_python_package(package: str) -> bool:
    """Check if Python package is installed."""
    try:
        __import__(package.replace("-", "_"))
        return True
    except ImportError:
        return False


def check_docker_running() -> Tuple[bool, str]:
    """Verify Docker daemon is running."""
    success, output = get_command_output(["docker", "info"])
    if success:
        return True, "Docker daemon is running"
    return False, output


def check_docker_compose() -> Tuple[bool, str]:
    """Verify Docker Compose is available."""
    success, output = get_command_output(["docker", "compose", "version"])
    if success:
        return True, output.split('\n')[0] if output else "Available"
    return False, "Docker Compose not found"


def check_wsl2_windows() -> Tuple[bool, str]:
    """Verify WSL2 is enabled on Windows."""
    if platform.system() != "Windows":
        return True, "Not on Windows (WSL check skipped)"
    
    success, output = get_command_output(["wsl", "--status"])
    if success and ("WSL 2" in output or "Default Version: 2" in output):
        return True, "WSL2 is enabled"
    return False, "WSL2 may not be enabled"


def check_wireshark() -> Tuple[bool, str]:
    """Check for Wireshark installation."""
    # Check common Windows paths
    windows_paths = [
        Path(r"C:\Program Files\Wireshark\Wireshark.exe"),
        Path(r"C:\Program Files (x86)\Wireshark\Wireshark.exe"),
    ]
    
    for path in windows_paths:
        if path.exists():
            return True, str(path)
    
    # Check if available in PATH (Linux/WSL)
    if check_command_exists("wireshark"):
        return True, "Available in PATH"
    
    # Check for tshark as alternative
    if check_command_exists("tshark"):
        return True, "tshark available (CLI mode)"
    
    return False, "Not found"


def check_tcpdump() -> Tuple[bool, str]:
    """Check for tcpdump availability."""
    if check_command_exists("tcpdump"):
        success, output = get_command_output(["tcpdump", "--version"])
        version = output.split('\n')[0] if output else "Available"
        return True, version
    return False, "Not found"


def main() -> int:
    """Main verification routine."""
    print()
    print("=" * 60)
    print("  Environment Verification for Week 2 Laboratory")
    print("  Socket Programming: TCP and UDP")
    print("  NETWORKING class - ASE, Informatics")
    print("=" * 60)
    print()
    
    c = Checker()
    
    # Python Environment
    print("\033[1mPython Environment:\033[0m")
    py_ok, py_version = check_python_version()
    c.check(
        f"Python {py_version}",
        py_ok,
        "Install Python 3.11+ from https://python.org"
    )
    
    # Required Python packages
    required_packages = ["socket", "threading", "argparse"]  # Standard library
    optional_packages = {
        "docker": "pip install docker",
        "requests": "pip install requests",
        "pyyaml": "pip install pyyaml",
    }
    
    for pkg, install_cmd in optional_packages.items():
        if check_python_package(pkg):
            c.check(f"Python package: {pkg}", True)
        else:
            c.check(f"Python package: {pkg}", False, install_cmd)
    
    print()
    
    # Docker Environment
    print("\033[1mDocker Environment:\033[0m")
    c.check(
        "Docker CLI installed",
        check_command_exists("docker"),
        "Install Docker Desktop from https://docker.com"
    )
    
    docker_ok, docker_msg = check_docker_running()
    c.check(
        f"Docker daemon: {docker_msg[:40]}",
        docker_ok,
        "Start Docker Desktop application"
    )
    
    compose_ok, compose_msg = check_docker_compose()
    c.check(
        f"Docker Compose: {compose_msg[:40]}",
        compose_ok,
        "Included with Docker Desktop"
    )
    
    print()
    
    # WSL2 Environment (Windows only)
    if platform.system() == "Windows":
        print("\033[1mWSL2 Environment:\033[0m")
        wsl_ok, wsl_msg = check_wsl2_windows()
        c.check(
            f"WSL2: {wsl_msg}",
            wsl_ok,
            "Enable WSL2: wsl --install"
        )
        print()
    
    # Network Tools
    print("\033[1mNetwork Analysis Tools:\033[0m")
    ws_ok, ws_msg = check_wireshark()
    c.check(
        f"Wireshark: {ws_msg[:40]}",
        ws_ok,
        "Install from https://wireshark.org"
    )
    
    tcpdump_ok, tcpdump_msg = check_tcpdump()
    if tcpdump_ok:
        c.check(f"tcpdump: {tcpdump_msg[:40]}", True)
    else:
        c.warn("tcpdump", "Optional - available inside Docker container")
    
    print()
    
    # Optional Tools
    print("\033[1mOptional Tools:\033[0m")
    if check_command_exists("git"):
        c.check("Git: Available", True)
    else:
        c.warn("Git", "Recommended for version control")
    
    if check_command_exists("nc") or check_command_exists("netcat"):
        c.check("Netcat: Available", True)
    else:
        c.warn("Netcat", "Useful for debugging - available in Docker")
    
    print()
    
    # Project Structure
    print("\033[1mProject Structure:\033[0m")
    project_root = Path(__file__).parent.parent
    
    required_dirs = ["docker", "src", "scripts", "tests"]
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        c.check(f"Directory: {dir_name}/", dir_path.is_dir())
    
    required_files = [
        "docker/docker-compose.yml",
        "src/exercises/ex_2_01_tcp.py",
        "src/exercises/ex_2_02_udp.py",
    ]
    for file_path in required_files:
        full_path = project_root / file_path
        c.check(f"File: {file_path}", full_path.is_file())
    
    return c.summary()


if __name__ == "__main__":
    sys.exit(main())
