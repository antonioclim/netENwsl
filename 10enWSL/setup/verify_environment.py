#!/usr/bin/env python3
"""
Environment Verification Script
NETWORKING class - ASE, Informatics | by Revolvix

Checks that all prerequisites are installed and configured correctly
for the Week 10 laboratory on Windows with WSL2 and Docker Desktop.
"""

import subprocess
import sys
import shutil
import platform
from pathlib import Path


class Checker:
    """Tracks verification results and provides formatted output."""
    
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
        print("\n" + "=" * 60)
        print(f"Results: {self.passed} passed, {self.failed} failed, {self.warnings} warnings")
        if self.failed == 0:
            print("Environment is ready for Week 10 laboratory!")
            return 0
        else:
            print("Please fix the issues above before proceeding.")
            return 1


def check_command(cmd: str) -> bool:
    """Check if a command is available in PATH."""
    return shutil.which(cmd) is not None


def check_docker_running() -> bool:
    """Check if Docker daemon is accessible."""
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
    """Check if a Python package is importable."""
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


def check_openssl() -> bool:
    """Check if OpenSSL is available for certificate generation."""
    try:
        result = subprocess.run(
            ["openssl", "version"],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except Exception:
        return False


def main() -> int:
    print("=" * 60)
    print("Environment Verification for Week 10 Laboratory")
    print("NETWORKING class - ASE, Informatics | by Revolvix")
    print("=" * 60)
    print()

    c = Checker()
    
    # System information
    print(f"System: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print()

    # Python version check
    print("Python Environment:")
    py_version = sys.version_info
    c.check(
        f"Python {py_version.major}.{py_version.minor}.{py_version.micro}",
        py_version >= (3, 11),
        "Install Python 3.11 or later from python.org"
    )

    # Required Python packages
    required_packages = [
        ("docker", "pip install docker"),
        ("requests", "pip install requests"),
        ("yaml", "pip install pyyaml"),
        ("flask", "pip install flask"),
        ("paramiko", "pip install paramiko"),
    ]
    
    for pkg, install_hint in required_packages:
        c.check(
            f"Python package: {pkg}",
            check_python_package(pkg),
            install_hint
        )

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
    if platform.system() == "Windows":
        print("\nWSL2 Environment:")
        c.check(
            "WSL2 available",
            check_wsl2(),
            "Enable WSL2: wsl --install"
        )

    # Network tools
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
    
    c.check(
        "OpenSSL available",
        check_openssl(),
        "Install OpenSSL or use Git Bash which includes it"
    )

    # Optional tools
    print("\nOptional Tools:")
    if check_command("git"):
        c.check("Git installed", True)
    else:
        c.warn("Git", "Recommended for version control")

    if check_command("curl"):
        c.check("curl installed", True)
    else:
        c.warn("curl", "Useful for HTTP testing")

    # Port availability
    print("\nPort Availability:")
    ports = [
        (8000, "HTTP web server"),
        (5353, "DNS server"),
        (2222, "SSH server"),
        (2121, "FTP server"),
        (8443, "HTTPS exercise"),
        (5000, "REST exercise"),
    ]
    
    for port, description in ports:
        available = check_port_available(port)
        if not available:
            c.warn(f"Port {port}", f"In use - {description} may conflict")
        else:
            c.check(f"Port {port} ({description})", True)

    # Directory structure
    print("\nProject Structure:")
    project_root = Path(__file__).parent.parent
    required_dirs = ["docker", "scripts", "src", "tests", "docs"]
    
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        c.check(
            f"Directory: {dir_name}/",
            dir_path.exists() and dir_path.is_dir(),
            f"Missing directory: {dir_name}"
        )

    return c.summary()


if __name__ == "__main__":
    sys.exit(main())
