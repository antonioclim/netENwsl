#!/usr/bin/env python3
"""
Prerequisites Installation Helper
NETWORKING class - ASE, Informatics | by Revolvix

Assists with installing and configuring prerequisites for Week 8.
This script provides guidance and automates where possible.
"""

import subprocess
import sys
import platform
import shutil
from pathlib import Path
from typing import List, Tuple


def print_header(title: str):
    """Print a formatted section header."""
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_step(step: int, description: str):
    """Print a numbered step."""
    print(f"\n\033[1m[Step {step}]\033[0m {description}")


def run_command(cmd: List[str], check: bool = False) -> Tuple[int, str, str]:
    """Run a command and return (returncode, stdout, stderr)."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)


def check_pip_available() -> bool:
    """Check if pip is available."""
    return shutil.which("pip") is not None or shutil.which("pip3") is not None


def get_pip_command() -> str:
    """Get the appropriate pip command."""
    if shutil.which("pip3"):
        return "pip3"
    return "pip"


def install_python_packages():
    """Install required Python packages."""
    print_header("Installing Python Packages")
    
    packages = [
        "docker>=6.0.0",
        "requests>=2.28.0",
        "pyyaml>=6.0",
        "pytest>=7.0.0",
        "httpx>=0.24.0",
    ]
    
    pip_cmd = get_pip_command()
    
    for package in packages:
        pkg_name = package.split(">=")[0].split("==")[0]
        print(f"\n  Installing {pkg_name}...", end=" ", flush=True)
        
        returncode, stdout, stderr = run_command([
            pip_cmd, "install", package, "--quiet"
        ])
        
        if returncode == 0:
            print("\033[92m✓\033[0m")
        else:
            print(f"\033[91m✗\033[0m")
            print(f"    Error: {stderr}")


def check_docker_installation():
    """Provide Docker installation guidance."""
    print_header("Docker Desktop Installation")
    
    if shutil.which("docker"):
        print("\n  \033[92m✓ Docker is already installed\033[0m")
        
        # Check if running
        returncode, _, _ = run_command(["docker", "info"])
        if returncode == 0:
            print("  \033[92m✓ Docker daemon is running\033[0m")
        else:
            print("  \033[93m! Docker daemon is not running\033[0m")
            print("\n  Please start Docker Desktop:")
            if platform.system() == "Windows":
                print("    1. Open Start Menu")
                print("    2. Search for 'Docker Desktop'")
                print("    3. Click to launch")
            else:
                print("    $ sudo systemctl start docker")
    else:
        print("\n  Docker Desktop is not installed.")
        print("\n  \033[1mInstallation Instructions:\033[0m")
        
        if platform.system() == "Windows":
            print("""
    1. Download Docker Desktop from:
       https://www.docker.com/products/docker-desktop/
    
    2. Run the installer (Docker Desktop Installer.exe)
    
    3. During installation, ensure these options are selected:
       ☑ Use WSL 2 instead of Hyper-V
       ☑ Add shortcut to desktop
    
    4. Restart your computer when prompted
    
    5. After restart, launch Docker Desktop
    
    6. Complete the tutorial or skip it
    
    7. Verify installation:
       Open PowerShell and run: docker --version
            """)
        else:
            print("""
    For Ubuntu/Debian:
    
    $ curl -fsSL https://get.docker.com -o get-docker.sh
    $ sudo sh get-docker.sh
    $ sudo usermod -aG docker $USER
    $ newgrp docker
    
    Verify: docker --version
            """)


def check_wsl2_installation():
    """Provide WSL2 installation guidance (Windows only)."""
    if platform.system() != "Windows":
        return
    
    print_header("WSL2 Configuration")
    
    # Check if WSL is available
    returncode, stdout, stderr = run_command(["wsl", "--status"])
    output = stdout + stderr
    
    if "WSL 2" in output or "Default Version: 2" in output:
        print("\n  \033[92m✓ WSL2 is properly configured\033[0m")
    else:
        print("\n  WSL2 may not be properly configured.")
        print("\n  \033[1mConfiguration Instructions:\033[0m")
        print("""
    1. Open PowerShell as Administrator
    
    2. Enable WSL:
       wsl --install
    
    3. Set WSL2 as default:
       wsl --set-default-version 2
    
    4. Restart your computer
    
    5. Verify:
       wsl --status
       (Should show "Default Version: 2")
        """)


def check_wireshark_installation():
    """Provide Wireshark installation guidance."""
    print_header("Wireshark Installation")
    
    wireshark_paths = [
        Path(r"C:\Program Files\Wireshark\Wireshark.exe"),
        Path(r"C:\Program Files (x86)\Wireshark\Wireshark.exe"),
    ]
    
    if any(p.exists() for p in wireshark_paths) or shutil.which("wireshark"):
        print("\n  \033[92m✓ Wireshark is installed\033[0m")
    else:
        print("\n  Wireshark is not installed.")
        print("\n  \033[1mInstallation Instructions:\033[0m")
        
        if platform.system() == "Windows":
            print("""
    1. Download Wireshark from:
       https://www.wireshark.org/download.html
       
    2. Choose "Windows x64 Installer"
    
    3. Run the installer with default options
    
    4. When prompted about Npcap, select:
       ☑ Install Npcap
       
    5. Complete installation
    
    6. Verify by opening Wireshark from Start Menu
            """)
        else:
            print("""
    For Ubuntu/Debian:
    
    $ sudo apt update
    $ sudo apt install wireshark
    $ sudo usermod -aG wireshark $USER
    
    Answer "Yes" when asked about non-root capture.
            """)


def create_requirements_file():
    """Create requirements.txt if it doesn't exist."""
    print_header("Creating requirements.txt")
    
    requirements = """# Week 8 Laboratory Requirements
# NETWORKING class - ASE, Informatics

# Core dependencies
docker>=6.0.0
requests>=2.28.0
pyyaml>=6.0

# Testing
pytest>=7.0.0
pytest-asyncio>=0.21.0

# HTTP utilities
httpx>=0.24.0

# Optional: Enhanced CLI output
rich>=13.0.0
"""
    
    script_dir = Path(__file__).parent
    req_file = script_dir / "requirements.txt"
    
    with open(req_file, "w") as f:
        f.write(requirements)
    
    print(f"  Created: {req_file}")


def main():
    print("\033[1m")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║     Week 8 Laboratory - Prerequisites Installation        ║")
    print("║     Transport Layer: HTTP Server and Reverse Proxies      ║")
    print("║     NETWORKING class - ASE, Informatics                   ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print("\033[0m")
    
    print("\nThis script will help you install and configure prerequisites.")
    print("Follow the instructions for any missing components.")
    
    # Step 1: Python packages
    print_step(1, "Python Packages")
    if check_pip_available():
        response = input("\nInstall Python packages now? [Y/n]: ").strip().lower()
        if response != "n":
            install_python_packages()
    else:
        print("  \033[91mError: pip is not available\033[0m")
        print("  Please install pip first:")
        print("    python -m ensurepip --upgrade")
    
    # Step 2: Docker
    print_step(2, "Docker Desktop")
    check_docker_installation()
    
    # Step 3: WSL2 (Windows only)
    if platform.system() == "Windows":
        print_step(3, "WSL2 Configuration")
        check_wsl2_installation()
        next_step = 4
    else:
        next_step = 3
    
    # Step 4: Wireshark
    print_step(next_step, "Wireshark")
    check_wireshark_installation()
    
    # Step 5: Create requirements.txt
    print_step(next_step + 1, "Requirements File")
    create_requirements_file()
    
    # Summary
    print_header("Next Steps")
    print("""
    1. Install any missing prerequisites listed above
    
    2. Restart your terminal/PowerShell session
    
    3. Run the verification script:
       python setup/verify_environment.py
    
    4. If all checks pass, start the laboratory:
       python scripts/start_lab.py
    """)
    
    print("\n\033[92mSetup assistance complete!\033[0m\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
