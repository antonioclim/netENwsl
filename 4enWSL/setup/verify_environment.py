#!/usr/bin/env python3
"""
Environment Verification Script
NETWORKING class - ASE, Informatics | by Revolvix

Checks that all prerequisites are installed and configured correctly
for the Week 4 laboratory session.
"""

import subprocess
import sys
import shutil
import os
from pathlib import Path


class Checker:
    """Verification results collector."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0

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
        print()
        print("=" * 60)
        print(f"Results: {self.passed} passed, {self.failed} failed, {self.warnings} warnings")
        
        if self.failed == 0:
            print("\033[92mEnvironment is ready for Week 4 laboratory!\033[0m")
            return 0
        else:
            print("\033[91mPlease fix the issues above before proceeding.\033[0m")
            return 1


def check_command(cmd: str) -> bool:
    """Check if a command is available in PATH."""
    return shutil.which(cmd) is not None


def get_command_version(cmd: str, version_flag: str = "--version") -> str:
    """Get version string from a command."""
    try:
        result = subprocess.run(
            [cmd, version_flag],
            capture_output=True,
            timeout=10,
            text=True
        )
        return result.stdout.strip() or result.stderr.strip()
    except Exception:
        return ""


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
    """Check if running in WSL2 or if WSL2 is available."""
    # Check if we're inside WSL
    if os.path.exists("/proc/version"):
        try:
            with open("/proc/version", "r") as f:
                content = f.read().lower()
                if "microsoft" in content or "wsl" in content:
                    return True
        except Exception:
            pass
    
    # Check if WSL command is available (Windows)
    try:
        result = subprocess.run(
            ["wsl", "--status"],
            capture_output=True,
            timeout=10
        )
        output = result.stdout.decode(errors='ignore') + result.stderr.decode(errors='ignore')
        return "WSL 2" in output or "Default Version: 2" in output
    except Exception:
        return False


def check_port_available(port: int) -> bool:
    """Check if a port is available for binding."""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        sock.bind(('127.0.0.1', port))
        sock.close()
        return True
    except OSError:
        return False


def check_wireshark() -> bool:
    """Check if Wireshark is installed."""
    # Windows paths
    windows_paths = [
        Path(r"C:\Program Files\Wireshark\Wireshark.exe"),
        Path(r"C:\Program Files (x86)\Wireshark\Wireshark.exe"),
    ]
    
    for path in windows_paths:
        if path.exists():
            return True
    
    # Linux/WSL
    return check_command("wireshark") or check_command("tshark")


def main():
    """Main verification routine."""
    print("=" * 60)
    print("Environment Verification for Week 4 Laboratory")
    print("NETWORKING class - ASE, Informatics | by Revolvix")
    print("=" * 60)
    print()

    c = Checker()

    # Python Environment
    print("\033[1mPython Environment:\033[0m")
    py_version = sys.version_info
    c.check(
        f"Python {py_version.major}.{py_version.minor}.{py_version.micro}",
        py_version >= (3, 8),
        "Install Python 3.8 or later from python.org"
    )

    # Required Python standard library modules
    required_modules = [
        ("socket", "Standard library - should be present"),
        ("struct", "Standard library - should be present"),
        ("threading", "Standard library - should be present"),
        ("zlib", "Standard library - should be present"),
        ("json", "Standard library - should be present"),
    ]
    
    for module, hint in required_modules:
        try:
            __import__(module)
            c.check(f"Python module: {module}", True)
        except ImportError:
            c.check(f"Python module: {module}", False, hint)

    # Optional Python packages
    print()
    print("\033[1mOptional Python Packages:\033[0m")
    optional_packages = [
        ("docker", "pip install docker"),
        ("requests", "pip install requests"),
        ("pyyaml", "pip install pyyaml"),
    ]
    
    for pkg, install_cmd in optional_packages:
        try:
            __import__(pkg)
            c.check(f"Python package: {pkg}", True)
        except ImportError:
            c.warn(pkg, f"Not installed. Install with: {install_cmd}")

    # Docker Environment
    print()
    print("\033[1mDocker Environment:\033[0m")
    docker_installed = check_command("docker")
    c.check(
        "Docker installed",
        docker_installed,
        "Install Docker Desktop from docker.com"
    )
    
    if docker_installed:
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

    # WSL2 Environment
    print()
    print("\033[1mWSL2 Environment:\033[0m")
    wsl_available = check_wsl2()
    if wsl_available:
        c.check("WSL2 available/detected", True)
    else:
        c.warn("WSL2", "Not detected. Required for Docker Desktop WSL2 backend")

    # Network Tools
    print()
    print("\033[1mNetwork Tools:\033[0m")
    c.check(
        "Wireshark/tshark available",
        check_wireshark(),
        "Install Wireshark from wireshark.org"
    )
    
    if check_command("tcpdump"):
        c.check("tcpdump available", True)
    else:
        c.warn("tcpdump", "Not installed. Install with: sudo apt install tcpdump")
    
    if check_command("nc") or check_command("netcat"):
        c.check("netcat available", True)
    else:
        c.warn("netcat", "Not installed. Install with: sudo apt install netcat-openbsd")

    # Port Availability
    print()
    print("\033[1mPort Availability:\033[0m")
    ports_to_check = [
        (5400, "TEXT protocol server"),
        (5401, "BINARY protocol server"),
        (5402, "UDP sensor server"),
        (9443, "Portainer"),
    ]
    
    for port, service in ports_to_check:
        available = check_port_available(port)
        if available:
            c.check(f"Port {port} ({service})", True)
        else:
            c.check(
                f"Port {port} ({service})",
                False,
                f"Port in use. Find process: netstat -ano | findstr :{port}"
            )

    # Optional Tools
    print()
    print("\033[1mOptional Tools:\033[0m")
    if check_command("git"):
        version = get_command_version("git")
        c.check(f"Git installed ({version.split()[2] if len(version.split()) > 2 else 'unknown version'})", True)
    else:
        c.warn("Git", "Recommended for version control")

    return c.summary()


if __name__ == "__main__":
    sys.exit(main())
