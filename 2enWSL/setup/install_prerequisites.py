#!/usr/bin/env python3
"""
Prerequisites Installation Helper
NETWORKING class - ASE, Informatics | by Revolvix

Helps install missing dependencies for the Week 2 laboratory.
Note: Some installations require manual steps or administrator privileges.
"""

import subprocess
import sys
import platform
from pathlib import Path


def print_header(text: str) -> None:
    """Print formatted section header."""
    print()
    print("=" * 60)
    print(f"  {text}")
    print("=" * 60)
    print()


def print_step(step: int, text: str) -> None:
    """Print numbered step."""
    print(f"  [{step}] {text}")


def run_command(cmd: list[str], check: bool = True) -> bool:
    """Run command and return success status."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"      Error: {e}")
        return False


def install_python_packages() -> None:
    """Install required Python packages."""
    print_header("Installing Python Packages")
    
    packages = ["docker", "requests", "pyyaml"]
    
    for pkg in packages:
        print(f"  Installing {pkg}...")
        success = run_command([sys.executable, "-m", "pip", "install", pkg])
        if success:
            print(f"    ✓ {pkg} installed")
        else:
            print(f"    ✗ Failed to install {pkg}")


def show_docker_instructions() -> None:
    """Display Docker installation instructions."""
    print_header("Docker Desktop Installation")
    
    if platform.system() == "Windows":
        print("  Docker Desktop for Windows:")
        print()
        print_step(1, "Download from: https://www.docker.com/products/docker-desktop/")
        print_step(2, "Run the installer (Docker Desktop Installer.exe)")
        print_step(3, "During installation, ensure 'Use WSL 2 instead of Hyper-V' is selected")
        print_step(4, "Restart your computer if prompted")
        print_step(5, "Start Docker Desktop from the Start Menu")
        print_step(6, "Wait for Docker to finish starting (whale icon becomes stable)")
        print()
        print("  After installation, verify with:")
        print("    docker --version")
        print("    docker compose version")
    else:
        print("  Docker for Linux:")
        print()
        print_step(1, "Follow instructions at: https://docs.docker.com/engine/install/")
        print_step(2, "Add your user to the docker group:")
        print("        sudo usermod -aG docker $USER")
        print_step(3, "Log out and back in for group changes to take effect")


def show_wsl2_instructions() -> None:
    """Display WSL2 installation instructions."""
    if platform.system() != "Windows":
        return
    
    print_header("WSL2 Installation")
    
    print("  Windows Subsystem for Linux 2:")
    print()
    print_step(1, "Open PowerShell as Administrator")
    print_step(2, "Run: wsl --install")
    print_step(3, "Restart your computer")
    print_step(4, "After restart, Ubuntu will finish installing")
    print_step(5, "Create a username and password when prompted")
    print()
    print("  Verify installation:")
    print("    wsl --status")
    print()
    print("  The output should show 'Default Version: 2'")


def show_wireshark_instructions() -> None:
    """Display Wireshark installation instructions."""
    print_header("Wireshark Installation")
    
    if platform.system() == "Windows":
        print("  Wireshark for Windows:")
        print()
        print_step(1, "Download from: https://www.wireshark.org/download.html")
        print_step(2, "Run the installer")
        print_step(3, "When prompted, install Npcap (required for capturing)")
        print_step(4, "Complete the installation with default options")
        print()
        print("  For WSL2/Docker traffic capture:")
        print("  - Wireshark can capture from Docker's network interface")
        print("  - Or use tshark inside WSL/containers")
    else:
        print("  Wireshark for Linux:")
        print()
        print("    sudo apt-get update")
        print("    sudo apt-get install wireshark tshark")
        print()
        print("  Allow non-root capture:")
        print("    sudo dpkg-reconfigure wireshark-common")
        print("    sudo usermod -aG wireshark $USER")


def show_verification_steps() -> None:
    """Show final verification steps."""
    print_header("Verification Steps")
    
    print("  After installing all prerequisites, verify the environment:")
    print()
    print("    python setup/verify_environment.py")
    print()
    print("  All checks should pass before starting the laboratory.")
    print()
    print("  Quick test of Docker:")
    print("    docker run --rm hello-world")


def main() -> int:
    """Main installation helper routine."""
    print()
    print("=" * 60)
    print("  Prerequisites Installation Helper")
    print("  Week 2: Socket Programming Laboratory")
    print("  NETWORKING class - ASE, Informatics")
    print("=" * 60)
    
    print()
    print("This script will help you install missing dependencies.")
    print("Some steps may require administrator/root privileges.")
    print()
    
    # Check what's needed
    options = []
    
    try:
        import docker
    except ImportError:
        options.append(("p", "Install Python packages", install_python_packages))
    
    # Always show Docker instructions as they require manual installation
    options.append(("d", "Show Docker installation instructions", show_docker_instructions))
    
    if platform.system() == "Windows":
        options.append(("w", "Show WSL2 installation instructions", show_wsl2_instructions))
    
    options.append(("s", "Show Wireshark installation instructions", show_wireshark_instructions))
    options.append(("v", "Show verification steps", show_verification_steps))
    options.append(("a", "Show all instructions", None))
    options.append(("q", "Quit", None))
    
    while True:
        print()
        print("Available options:")
        for key, desc, _ in options:
            print(f"  [{key}] {desc}")
        print()
        
        choice = input("Select option: ").strip().lower()
        
        if choice == "q":
            break
        elif choice == "a":
            install_python_packages()
            show_docker_instructions()
            show_wsl2_instructions()
            show_wireshark_instructions()
            show_verification_steps()
        else:
            for key, _, action in options:
                if choice == key and action:
                    action()
                    break
            else:
                print("  Invalid option. Please try again.")
    
    print()
    print("Installation helper complete.")
    print("Run 'python setup/verify_environment.py' to check your setup.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
