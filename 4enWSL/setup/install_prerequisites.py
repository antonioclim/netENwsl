#!/usr/bin/env python3
"""
Prerequisites Installation Helper
NETWORKING class - ASE, Informatics | by Revolvix

Guides users through installing required software for Week 4 laboratory.
This script does not automatically install software but provides clear
instructions and verification steps.
"""

import subprocess
import sys
import os
import platform
from pathlib import Path


def print_header(text: str) -> None:
    """Print a formatted header."""
    print()
    print("=" * 60)
    print(f" {text}")
    print("=" * 60)


def print_step(number: int, text: str) -> None:
    """Print a numbered step."""
    print(f"\n  [{number}] {text}")


def print_command(cmd: str) -> None:
    """Print a command to execute."""
    print(f"\n      \033[96m{cmd}\033[0m")


def print_note(text: str) -> None:
    """Print a note."""
    print(f"\n      \033[93mNote:\033[0m {text}")


def is_windows() -> bool:
    """Check if running on Windows."""
    return platform.system() == "Windows"


def is_wsl() -> bool:
    """Check if running inside WSL."""
    if os.path.exists("/proc/version"):
        try:
            with open("/proc/version", "r") as f:
                content = f.read().lower()
                return "microsoft" in content or "wsl" in content
        except Exception:
            pass
    return False


def check_admin() -> bool:
    """Check if running with administrator/root privileges."""
    if is_windows():
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False
    else:
        return os.geteuid() == 0


def install_wsl2_instructions():
    """Provide WSL2 installation instructions."""
    print_header("WSL2 Installation")
    
    print("""
    WSL2 (Windows Subsystem for Linux version 2) is required for
    Docker Desktop's recommended backend.
    """)
    
    print_step(1, "Open PowerShell as Administrator")
    print_command("Start-Process powershell -Verb RunAs")
    
    print_step(2, "Enable WSL feature")
    print_command("wsl --install")
    
    print_step(3, "Restart your computer when prompted")
    
    print_step(4, "After restart, set WSL2 as default")
    print_command("wsl --set-default-version 2")
    
    print_step(5, "Verify installation")
    print_command("wsl --status")
    
    print_note("The output should show 'Default Version: 2'")


def install_docker_instructions():
    """Provide Docker Desktop installation instructions."""
    print_header("Docker Desktop Installation")
    
    print("""
    Docker Desktop provides container runtime with WSL2 integration.
    """)
    
    print_step(1, "Download Docker Desktop")
    print("      https://www.docker.com/products/docker-desktop/")
    
    print_step(2, "Run the installer")
    print("      - Accept the licence agreement")
    print("      - Select 'Use WSL 2 instead of Hyper-V' option")
    
    print_step(3, "Start Docker Desktop")
    print("      - Wait for the Docker engine to initialise")
    print("      - Look for the whale icon in the system tray")
    
    print_step(4, "Configure WSL2 integration")
    print("      - Open Docker Desktop Settings")
    print("      - Go to Resources > WSL Integration")
    print("      - Enable integration with your default WSL2 distro")
    
    print_step(5, "Verify installation")
    print_command("docker --version")
    print_command("docker compose version")
    print_command("docker run hello-world")


def install_wireshark_instructions():
    """Provide Wireshark installation instructions."""
    print_header("Wireshark Installation")
    
    print("""
    Wireshark is essential for packet capture and protocol analysis.
    """)
    
    print_step(1, "Download Wireshark")
    print("      https://www.wireshark.org/download.html")
    print("      Select 'Windows x64 Installer'")
    
    print_step(2, "Run the installer")
    print("      - Accept default components")
    print("      - Install Npcap when prompted (required for capture)")
    print("      - Select 'Install Npcap in WinPcap API-compatible Mode'")
    
    print_step(3, "Verify installation")
    print("      - Launch Wireshark from Start Menu")
    print("      - Verify network interfaces are visible")
    
    print_note("You may need to run Wireshark as Administrator for some captures")


def install_python_packages_instructions():
    """Provide Python packages installation instructions."""
    print_header("Python Packages Installation")
    
    print("""
    Optional Python packages enhance the laboratory experience.
    """)
    
    print_step(1, "Upgrade pip")
    print_command("python -m pip install --upgrade pip")
    
    print_step(2, "Install recommended packages")
    print_command("pip install docker requests pyyaml")
    
    print_step(3, "Verify installation")
    print_command("python -c \"import docker; import requests; import yaml; print('OK')\"")


def install_linux_tools_instructions():
    """Provide Linux tools installation instructions for WSL."""
    print_header("Linux Network Tools (in WSL)")
    
    print("""
    These tools are useful for network analysis within WSL.
    """)
    
    print_step(1, "Update package lists")
    print_command("sudo apt update")
    
    print_step(2, "Install network tools")
    print_command("sudo apt install -y tcpdump tshark netcat-openbsd iproute2 iputils-ping")
    
    print_step(3, "Configure tshark for non-root capture (optional)")
    print_command("sudo dpkg-reconfigure wireshark-common")
    print("      Select 'Yes' to allow non-root users to capture")
    print_command("sudo usermod -aG wireshark $USER")
    print_note("Log out and back in for group changes to take effect")


def run_verification():
    """Run the verification script."""
    print_header("Running Environment Verification")
    
    script_path = Path(__file__).parent / "verify_environment.py"
    if script_path.exists():
        subprocess.run([sys.executable, str(script_path)])
    else:
        print("    Verification script not found. Run manually:")
        print_command("python setup/verify_environment.py")


def main():
    """Main installation guide."""
    print()
    print("╔════════════════════════════════════════════════════════════╗")
    print("║     Week 4 Laboratory Prerequisites Installation Guide     ║")
    print("║     NETWORKING class - ASE, Informatics | by Revolvix      ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    if is_wsl():
        print("\n    \033[92mDetected: Running inside WSL\033[0m")
    elif is_windows():
        print("\n    \033[92mDetected: Running on Windows\033[0m")
    else:
        print(f"\n    Detected: {platform.system()}")
    
    print("""
    This script provides installation instructions for required software.
    Follow the steps for each component you need to install.
    
    Components needed:
    1. WSL2 (Windows Subsystem for Linux)
    2. Docker Desktop with WSL2 backend
    3. Wireshark (for packet analysis)
    4. Python packages (optional enhancements)
    5. Linux network tools (in WSL)
    """)
    
    while True:
        print("\n" + "-" * 60)
        print("Select a component to view installation instructions:")
        print("  1) WSL2")
        print("  2) Docker Desktop")
        print("  3) Wireshark")
        print("  4) Python packages")
        print("  5) Linux network tools (WSL)")
        print("  6) Run environment verification")
        print("  q) Quit")
        print("-" * 60)
        
        choice = input("\nEnter choice [1-6, q]: ").strip().lower()
        
        if choice == '1':
            install_wsl2_instructions()
        elif choice == '2':
            install_docker_instructions()
        elif choice == '3':
            install_wireshark_instructions()
        elif choice == '4':
            install_python_packages_instructions()
        elif choice == '5':
            install_linux_tools_instructions()
        elif choice == '6':
            run_verification()
        elif choice == 'q':
            print("\nGoodbye! Run verification when ready:")
            print_command("python setup/verify_environment.py")
            break
        else:
            print("\n    Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
