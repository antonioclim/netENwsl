#!/usr/bin/env python3
"""
Environment Verification Script
NETWORKING class - ASE, Informatics | by Revolvix

Checks that all prerequisites are installed and configured correctly
for the Week 12 laboratory on Email Protocols and RPC.
"""

import subprocess
import sys
import shutil
from pathlib import Path
from typing import Optional


class Checker:
    """Verification result collector with pass/fail/warning tracking."""
    
    def __init__(self) -> None:
        self.passed = 0
        self.failed = 0
        self.warnings = 0

    def check(self, name: str, condition: bool, fix_hint: str = "") -> None:
        """Record a pass/fail check result."""
        if condition:
            print(f"  [\033[92mPASS\033[0m] {name}")
            self.passed += 1
        else:
            print(f"  [\033[91mFAIL\033[0m] {name}")
            if fix_hint:
                print(f"         Fix: {fix_hint}")
            self.failed += 1

    def warn(self, name: str, message: str) -> None:
        """Record a warning (non-blocking issue)."""
        print(f"  [\033[93mWARN\033[0m] {name}: {message}")
        self.warnings += 1

    def summary(self) -> int:
        """Print summary and return exit code."""
        print()
        print("=" * 60)
        print(f"Results: {self.passed} passed, {self.failed} failed, {self.warnings} warnings")
        if self.failed == 0:
            print("\033[92mEnvironment is ready for Week 12!\033[0m")
            return 0
        else:
            print("\033[91mPlease fix the issues above before proceeding.\033[0m")
            return 1


def check_command(cmd: str) -> bool:
    """Check if a command is available in PATH."""
    return shutil.which(cmd) is not None


def check_python_version() -> tuple[bool, str]:
    """Check Python version meets minimum requirements."""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    return version >= (3, 11), version_str


def check_python_package(package: str) -> bool:
    """Check if a Python package can be imported."""
    try:
        __import__(package)
        return True
    except ImportError:
        return False


def check_docker_running() -> bool:
    """Check if Docker daemon is running and accessible."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=15
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def check_docker_compose() -> bool:
    """Check if Docker Compose (v2) is available."""
    try:
        result = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def check_wsl2() -> bool:
    """Check if WSL2 is available (Windows only)."""
    try:
        result = subprocess.run(
            ["wsl", "--status"],
            capture_output=True,
            timeout=10
        )
        output = result.stdout.decode(errors="replace") + result.stderr.decode(errors="replace")
        return "WSL 2" in output or "Default Version: 2" in output
    except (subprocess.TimeoutExpired, FileNotFoundError):
        # Not on Windows or WSL not installed
        return False


def check_port_available(port: int) -> bool:
    """Check if a TCP port appears to be available."""
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex(("127.0.0.1", port))
            # Non-zero means connection failed, i.e. port is not in use
            return result != 0
    except Exception:
        return True  # Assume available if we can't check


def find_wireshark() -> Optional[Path]:
    """Locate Wireshark installation."""
    # Common Windows paths
    windows_paths = [
        Path(r"C:\Program Files\Wireshark\Wireshark.exe"),
        Path(r"C:\Program Files (x86)\Wireshark\Wireshark.exe"),
    ]
    for p in windows_paths:
        if p.exists():
            return p
    
    # Check PATH (Linux/macOS or WSL)
    if check_command("wireshark"):
        return Path(shutil.which("wireshark"))
    
    return None


def main() -> int:
    """Run all environment checks."""
    print("=" * 60)
    print("Environment Verification for Week 12 Laboratory")
    print("Email Protocols (SMTP) and Remote Procedure Call")
    print("NETWORKING class - ASE, Informatics")
    print("=" * 60)
    print()

    c = Checker()

    # Python Environment
    print("Python Environment:")
    py_ok, py_version = check_python_version()
    c.check(
        f"Python {py_version}",
        py_ok,
        "Install Python 3.11 or later from python.org"
    )

    # Required Python packages
    required_packages = [
        ("grpcio", "pip install grpcio"),
        ("grpcio_tools", "pip install grpcio-tools"),
        ("google.protobuf", "pip install protobuf"),
    ]
    
    for pkg, fix in required_packages:
        c.check(
            f"Python package: {pkg}",
            check_python_package(pkg.split(".")[0]),
            fix
        )

    # Optional but recommended packages
    optional_packages = [
        ("colorama", "pip install colorama"),
        ("pytest", "pip install pytest"),
        ("dnspython", "pip install dnspython"),
    ]
    
    print()
    print("Optional Python Packages:")
    for pkg, fix in optional_packages:
        if check_python_package(pkg):
            c.check(f"Python package: {pkg}", True)
        else:
            c.warn(f"Python package: {pkg}", f"Optional. Install with: {fix}")

    # Docker Environment
    print()
    print("Docker Environment:")
    c.check(
        "Docker installed",
        check_command("docker"),
        "Install Docker Desktop from docker.com"
    )
    c.check(
        "Docker Compose v2 installed",
        check_docker_compose(),
        "Docker Compose should come with Docker Desktop"
    )
    c.check(
        "Docker daemon running",
        check_docker_running(),
        "Start Docker Desktop application"
    )

    # WSL2 (Windows)
    print()
    print("WSL2 Environment:")
    if sys.platform == "win32" or check_command("wsl"):
        c.check(
            "WSL2 available",
            check_wsl2(),
            "Enable WSL2: wsl --install"
        )
    else:
        c.warn("WSL2", "Not on Windows - skipping WSL2 check")

    # Network Tools
    print()
    print("Network Tools:")
    wireshark_path = find_wireshark()
    c.check(
        "Wireshark available",
        wireshark_path is not None,
        "Install Wireshark from wireshark.org"
    )
    
    if check_command("nc") or check_command("netcat"):
        c.check("netcat (nc) available", True)
    else:
        c.warn("netcat", "Recommended for manual SMTP testing")

    if check_command("curl"):
        c.check("curl available", True)
    else:
        c.warn("curl", "Recommended for HTTP/RPC testing")

    # Port Availability
    print()
    print("Port Availability (Week 12 defaults):")
    week12_ports = {
        1025: "SMTP",
        6200: "JSON-RPC",
        6201: "XML-RPC",
        6251: "gRPC",
        9443: "Portainer",
    }
    
    for port, service in week12_ports.items():
        if check_port_available(port):
            c.check(f"Port {port} ({service})", True)
        else:
            c.warn(f"Port {port} ({service})", "Port in use - may need alternative")

    # Optional Tools
    print()
    print("Optional Tools:")
    if check_command("git"):
        c.check("Git installed", True)
    else:
        c.warn("Git", "Recommended for version control")

    if check_command("tcpdump"):
        c.check("tcpdump available", True)
    else:
        c.warn("tcpdump", "Optional for packet capture in WSL")

    if check_command("tshark"):
        c.check("tshark available", True)
    else:
        c.warn("tshark", "Optional for command-line packet analysis")

    return c.summary()


if __name__ == "__main__":
    sys.exit(main())
