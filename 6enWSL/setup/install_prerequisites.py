#!/usr/bin/env python3
"""
Prerequisites Installation Helper
NETWORKING class - ASE, Informatics | by Revolvix

Assists with installing required software for the Week 6 laboratory.
"""

from __future__ import annotations

import subprocess
import sys
import platform
from pathlib import Path


def print_section(title: str) -> None:
    """Print a section header."""
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)
    print()


def run_command(cmd: list[str], check: bool = True) -> bool:
    """Run a command and return success status."""
    try:
        result = subprocess.run(cmd, check=check)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False


def install_python_packages() -> bool:
    """Install required Python packages."""
    print("Installing Python packages...")
    
    packages = [
        "docker",
        "requests",
        "pyyaml",
    ]
    
    cmd = [sys.executable, "-m", "pip", "install", "--break-system-packages"] + packages
    
    try:
        subprocess.run(cmd, check=True)
        print("✓ Python packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install Python packages: {e}")
        return False


def check_docker_installation() -> bool:
    """Check if Docker is installed and provide guidance."""
    try:
        result = subprocess.run(["docker", "--version"], capture_output=True)
        if result.returncode == 0:
            print("✓ Docker is already installed")
            return True
    except FileNotFoundError:
        pass
    
    print("✗ Docker is not installed")
    print()
    print("To install Docker Desktop:")
    print("  1. Download from: https://www.docker.com/products/docker-desktop")
    print("  2. Run the installer")
    print("  3. Enable WSL2 integration in Docker Desktop settings")
    print()
    return False


def check_wsl2() -> bool:
    """Check WSL2 availability on Windows."""
    if platform.system() != "Windows":
        return True  # Not applicable
    
    try:
        result = subprocess.run(["wsl", "--status"], capture_output=True, text=True)
        if "WSL 2" in result.stdout or "Default Version: 2" in result.stdout:
            print("✓ WSL2 is available")
            return True
    except FileNotFoundError:
        pass
    
    print("✗ WSL2 is not available or not the default")
    print()
    print("To enable WSL2:")
    print("  1. Open PowerShell as Administrator")
    print("  2. Run: wsl --install")
    print("  3. Restart your computer")
    print("  4. Run: wsl --set-default-version 2")
    print()
    return False


def provide_wsl_instructions() -> None:
    """Provide instructions for WSL-specific tools."""
    print_section("WSL/Linux Tools (Optional)")
    
    print("The following tools provide additional functionality in WSL/Linux:")
    print()
    print("Install in WSL Ubuntu:")
    print("  sudo apt-get update")
    print("  sudo apt-get install -y mininet openvswitch-switch tcpdump tshark")
    print("  pip3 install --break-system-packages os-ken scapy")
    print()
    print("These are optional if using Docker containers.")


def main() -> int:
    """Main entry point."""
    print_section("Week 6 Prerequisites Installation")
    print("NETWORKING class - ASE, Informatics | by Revolvix")
    
    success = True
    
    # Check WSL2 (Windows only)
    if platform.system() == "Windows":
        print_section("WSL2 Configuration")
        if not check_wsl2():
            success = False
    
    # Check Docker
    print_section("Docker Installation")
    if not check_docker_installation():
        success = False
    
    # Install Python packages
    print_section("Python Packages")
    if not install_python_packages():
        success = False
    
    # Provide WSL instructions
    provide_wsl_instructions()
    
    # Summary
    print_section("Summary")
    
    if success:
        print("✓ Core prerequisites are ready!")
        print()
        print("Next steps:")
        print("  1. Start Docker Desktop")
        print("  2. Run: python setup/verify_environment.py")
        print("  3. Run: python scripts/start_lab.py")
    else:
        print("✗ Some prerequisites need attention")
        print()
        print("Please address the issues above and run this script again.")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
