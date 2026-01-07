#!/usr/bin/env python3
"""
Environment Verification Script
NETWORKING class - ASE, Informatics | by Revolvix

Checks that all prerequisites are installed and configured correctly
for the Week 6 laboratory (NAT/PAT & SDN).
"""

from __future__ import annotations

import subprocess
import sys
import shutil
import platform
from pathlib import Path
from typing import Callable, Optional


class Checker:
    """Environment verification helper with pass/fail/warning tracking."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        
    def check(self, name: str, condition: bool, fix_hint: str = "") -> bool:
        """Record a check result."""
        if condition:
            print(f"  [PASS] {name}")
            self.passed += 1
        else:
            print(f"  [FAIL] {name}")
            if fix_hint:
                print(f"         Fix: {fix_hint}")
            self.failed += 1
        return condition
    
    def warn(self, name: str, message: str) -> None:
        """Record a warning."""
        print(f"  [WARN] {name}: {message}")
        self.warnings += 1
        
    def info(self, message: str) -> None:
        """Display informational message."""
        print(f"  [INFO] {message}")
        
    def summary(self) -> int:
        """Print summary and return exit code."""
        print()
        print("=" * 60)
        print(f"Results: {self.passed} passed, {self.failed} failed, {self.warnings} warnings")
        
        if self.failed == 0:
            print("\n✓ Environment is ready for Week 6 laboratory!")
            return 0
        else:
            print("\n✗ Please fix the issues above before proceeding.")
            print("  Run: python setup/install_prerequisites.py")
            return 1


def check_command(cmd: str) -> bool:
    """Check if a command is available in PATH."""
    return shutil.which(cmd) is not None


def run_command(cmd: list[str], timeout: int = 10) -> tuple[bool, str]:
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


def check_python_version() -> tuple[bool, str]:
    """Check Python version meets requirements."""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    meets_requirement = version >= (3, 11)
    return meets_requirement, version_str


def check_python_package(package: str) -> bool:
    """Check if a Python package is importable."""
    try:
        __import__(package)
        return True
    except ImportError:
        return False


def check_docker_running() -> bool:
    """Check if Docker daemon is running."""
    success, _ = run_command(["docker", "info"])
    return success


def check_docker_compose() -> bool:
    """Check if Docker Compose is available."""
    success, _ = run_command(["docker", "compose", "version"])
    return success


def check_wsl2() -> tuple[bool, str]:
    """Check if running in WSL2 or if WSL2 is available."""
    # Check if we're running inside WSL
    if Path("/proc/version").exists():
        try:
            with open("/proc/version", "r") as f:
                content = f.read().lower()
                if "microsoft" in content or "wsl" in content:
                    # Check WSL version
                    if "wsl2" in content:
                        return True, "Running in WSL2"
                    # Try to determine version another way
                    success, output = run_command(["uname", "-r"])
                    if success and "microsoft" in output.lower():
                        return True, "Running in WSL"
        except Exception:
            pass
    
    # Check if WSL is available from Windows
    if platform.system() == "Windows":
        success, output = run_command(["wsl", "--status"])
        if success:
            if "WSL 2" in output or "Default Version: 2" in output:
                return True, "WSL2 available"
        return False, "WSL2 not configured"
    
    # Native Linux
    if platform.system() == "Linux":
        return True, "Native Linux"
    
    return False, "Unknown platform"


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
    
    # Check in PATH (Linux/WSL)
    return check_command("wireshark") or check_command("tshark")


def check_mininet() -> bool:
    """Check if Mininet is installed (for WSL/Linux)."""
    return check_command("mn")


def check_ovs() -> bool:
    """Check if Open vSwitch is installed."""
    return check_command("ovs-vsctl")


def main() -> int:
    """Main verification routine."""
    print()
    print("=" * 60)
    print("Environment Verification for Week 6 Laboratory")
    print("NETWORKING class - ASE, Informatics | by Revolvix")
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
    
    # Optional Python packages (for Mininet mode)
    optional_packages = ["scapy"]
    for pkg in optional_packages:
        if check_python_package(pkg):
            c.check(f"Python package: {pkg}", True)
        else:
            c.warn(pkg, "Optional package not installed (needed for WSL mode)")
    
    # Docker Environment
    print("\nDocker Environment:")
    c.check(
        "Docker installed",
        check_command("docker"),
        "Install Docker Desktop from docker.com"
    )
    
    c.check(
        "Docker Compose (v2)",
        check_docker_compose(),
        "Docker Compose should come with Docker Desktop"
    )
    
    docker_running = check_docker_running()
    c.check(
        "Docker daemon running",
        docker_running,
        "Start Docker Desktop application"
    )
    
    if docker_running:
        # Check Docker can run privileged containers
        success, output = run_command([
            "docker", "run", "--rm", "--privileged",
            "alpine", "echo", "privileged_ok"
        ], timeout=30)
        c.check(
            "Docker privileged mode",
            success and "privileged_ok" in output,
            "Enable privileged containers in Docker Desktop settings"
        )
    
    # WSL2 Environment
    print("\nPlatform Environment:")
    wsl_ok, wsl_status = check_wsl2()
    c.check(f"WSL2/Linux: {wsl_status}", wsl_ok, "Enable WSL2: wsl --install")
    
    # Network Tools
    print("\nNetwork Tools:")
    
    wireshark_ok = check_wireshark()
    c.check(
        "Wireshark available",
        wireshark_ok,
        "Install Wireshark from wireshark.org"
    )
    
    # Check for tshark (CLI Wireshark)
    if check_command("tshark"):
        c.check("tshark (CLI)", True)
    else:
        c.warn("tshark", "CLI packet analysis not available")
    
    # WSL-specific tools (optional but recommended)
    print("\nWSL/Linux Tools (optional for Docker mode):")
    
    mininet_ok = check_mininet()
    if mininet_ok:
        c.check("Mininet", True)
    else:
        c.warn("Mininet", "Not installed (optional - Docker mode available)")
    
    ovs_ok = check_ovs()
    if ovs_ok:
        c.check("Open vSwitch", True)
    else:
        c.warn("Open vSwitch", "Not installed (optional - Docker mode available)")
    
    # Check for tcpdump
    if check_command("tcpdump"):
        c.check("tcpdump", True)
    else:
        c.warn("tcpdump", "Not installed (optional)")
    
    # Check for iptables
    if check_command("iptables"):
        c.check("iptables", True)
    else:
        c.warn("iptables", "Not installed (optional - needed for NAT in WSL)")
    
    # Optional Tools
    print("\nOptional Tools:")
    
    if check_command("git"):
        c.check("Git", True)
    else:
        c.warn("Git", "Recommended for version control")
    
    if check_command("curl"):
        c.check("curl", True)
    else:
        c.warn("curl", "Useful for testing HTTP connections")
    
    if check_command("netcat") or check_command("nc"):
        c.check("netcat", True)
    else:
        c.warn("netcat", "Useful for testing TCP/UDP connections")
    
    return c.summary()


if __name__ == "__main__":
    sys.exit(main())
