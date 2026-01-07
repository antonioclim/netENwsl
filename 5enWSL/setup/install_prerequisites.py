#!/usr/bin/env python3
"""
Prerequisites Installation Helper
NETWORKING class - ASE, Informatics | by Revolvix

Guides the user through installing required software.
"""

import subprocess
import sys
import shutil
from pathlib import Path


def print_header(title: str):
    """Print a formatted section header."""
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)
    print()


def print_step(step: int, description: str):
    """Print a numbered step."""
    print(f"  Step {step}: {description}")


def check_command(cmd: str) -> bool:
    """Check if a command is available."""
    return shutil.which(cmd) is not None


def install_python_packages():
    """Install required Python packages."""
    print_header("Python Package Installation")
    
    packages = ["docker", "requests", "pyyaml"]
    
    print("  Installing optional packages for enhanced functionality:")
    for pkg in packages:
        print(f"    - {pkg}")
    
    print()
    response = input("  Install these packages? [Y/n]: ").strip().lower()
    
    if response in ("", "y", "yes"):
        for pkg in packages:
            print(f"  Installing {pkg}...")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", pkg],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"    ✓ {pkg} installed successfully")
            else:
                print(f"    ✗ Failed to install {pkg}: {result.stderr}")
    else:
        print("  Skipped package installation")


def guide_docker_installation():
    """Guide Docker Desktop installation."""
    print_header("Docker Desktop Installation")
    
    if check_command("docker"):
        print("  ✓ Docker is already installed")
        
        # Check if it's running
        result = subprocess.run(["docker", "info"], capture_output=True)
        if result.returncode == 0:
            print("  ✓ Docker daemon is running")
        else:
            print("  ✗ Docker is installed but not running")
            print()
            print("  Please start Docker Desktop:")
            if sys.platform == "win32":
                print("    1. Open Start menu")
                print("    2. Search for 'Docker Desktop'")
                print("    3. Launch and wait for it to start")
            else:
                print("    Run: sudo systemctl start docker")
        return
    
    print("  Docker Desktop is not installed.")
    print()
    
    if sys.platform == "win32":
        print("  Windows Installation Instructions:")
        print_step(1, "Download Docker Desktop from:")
        print("         https://www.docker.com/products/docker-desktop/")
        print()
        print_step(2, "Run the installer")
        print()
        print_step(3, "During installation, ensure 'Use WSL 2 instead of Hyper-V' is selected")
        print()
        print_step(4, "Restart your computer when prompted")
        print()
        print_step(5, "After restart, launch Docker Desktop and complete setup")
    elif sys.platform == "darwin":
        print("  macOS Installation Instructions:")
        print_step(1, "Download Docker Desktop from:")
        print("         https://www.docker.com/products/docker-desktop/")
        print()
        print_step(2, "Open the .dmg file and drag Docker to Applications")
        print()
        print_step(3, "Launch Docker from Applications folder")
    else:
        print("  Linux Installation Instructions:")
        print_step(1, "Install Docker Engine:")
        print("         curl -fsSL https://get.docker.com | sh")
        print()
        print_step(2, "Add your user to the docker group:")
        print("         sudo usermod -aG docker $USER")
        print()
        print_step(3, "Log out and back in for group changes to take effect")


def guide_wsl2_installation():
    """Guide WSL2 installation (Windows only)."""
    if sys.platform != "win32":
        return
    
    print_header("WSL2 Installation")
    
    # Check if WSL is available
    try:
        result = subprocess.run(["wsl", "--status"], capture_output=True, timeout=10)
        output = result.stdout.decode() + result.stderr.decode()
        
        if "WSL 2" in output or "Default Version: 2" in output:
            print("  ✓ WSL2 is already installed and configured")
            return
    except Exception:
        pass
    
    print("  WSL2 setup instructions:")
    print()
    print_step(1, "Open PowerShell as Administrator")
    print()
    print_step(2, "Run the following command:")
    print("         wsl --install")
    print()
    print_step(3, "Restart your computer when prompted")
    print()
    print_step(4, "After restart, WSL2 with Ubuntu will be configured")
    print()
    print("  Note: WSL2 is required for Docker Desktop on Windows")


def guide_wireshark_installation():
    """Guide Wireshark installation."""
    print_header("Wireshark Installation (Optional)")
    
    # Check if already installed
    wireshark_paths = [
        Path(r"C:\Program Files\Wireshark\Wireshark.exe"),
        Path(r"C:\Program Files (x86)\Wireshark\Wireshark.exe"),
    ]
    
    for path in wireshark_paths:
        if path.exists():
            print("  ✓ Wireshark is already installed")
            return
    
    if check_command("wireshark") or check_command("tshark"):
        print("  ✓ Wireshark is already installed")
        return
    
    print("  Wireshark is useful for packet analysis but not required.")
    print("  (tcpdump is available inside Docker containers)")
    print()
    print("  Installation:")
    print("    1. Download from: https://www.wireshark.org/download.html")
    print("    2. Run the installer")
    print("    3. During installation, enable 'Install Npcap' when prompted")


def main():
    print()
    print("=" * 60)
    print("  Week 5 Laboratory - Prerequisites Installation Helper")
    print("  NETWORKING class - ASE, Informatics")
    print("=" * 60)
    print()
    print("  This script will guide you through installing required software.")
    print("  It will NOT make any changes without your confirmation.")
    print()
    
    # Check current status first
    print("  Current Status:")
    print(f"    Python: {sys.version.split()[0]}")
    print(f"    Docker: {'✓ Installed' if check_command('docker') else '✗ Not found'}")
    print(f"    Git:    {'✓ Installed' if check_command('git') else '✗ Not found'}")
    
    print()
    input("  Press Enter to continue...")
    
    # Python packages
    install_python_packages()
    
    # Docker
    guide_docker_installation()
    
    # WSL2 (Windows)
    guide_wsl2_installation()
    
    # Wireshark
    guide_wireshark_installation()
    
    # Summary
    print_header("Next Steps")
    
    print("  1. Complete any pending installations above")
    print("  2. Restart your computer if Docker or WSL2 was installed")
    print("  3. Run the verification script:")
    print("       python setup/verify_environment.py")
    print("  4. Start the laboratory:")
    print("       python scripts/start_lab.py")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
