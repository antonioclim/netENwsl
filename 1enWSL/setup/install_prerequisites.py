#!/usr/bin/env python3
"""
Prerequisites Installation Helper
NETWORKING class - ASE, Informatics | by Revolvix

Guides users through installing missing prerequisites for the Week 1 laboratory.
This script does not automatically install system software but provides
clear instructions for manual installation.
"""

from __future__ import annotations

import subprocess
import sys
import shutil
from pathlib import Path


def print_header(title: str) -> None:
    """Print a formatted section header."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}\n")


def print_step(number: int, description: str) -> None:
    """Print a numbered installation step."""
    print(f"\033[1m{number}.\033[0m {description}")


def check_command(cmd: str) -> bool:
    """Check if a command exists in PATH."""
    return shutil.which(cmd) is not None


def install_python_packages() -> bool:
    """Install required Python packages."""
    packages = ["docker", "requests", "pyyaml", "scapy", "dpkt"]
    
    print("Installing Python packages...")
    
    try:
        # Determine pip command
        pip_cmd = [sys.executable, "-m", "pip", "install", "--upgrade"]
        
        # Check if we need --break-system-packages (Python 3.11+ on some systems)
        result = subprocess.run(
            pip_cmd + ["--help"],
            capture_output=True,
            text=True
        )
        
        if "--break-system-packages" in result.stdout:
            pip_cmd.append("--break-system-packages")
        
        # Install packages
        for pkg in packages:
            print(f"  Installing {pkg}...", end=" ", flush=True)
            result = subprocess.run(
                pip_cmd + [pkg],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("\033[92mOK\033[0m")
            else:
                print(f"\033[91mFAILED\033[0m")
                print(f"    Error: {result.stderr[:200]}")
        
        return True
        
    except Exception as e:
        print(f"\033[91mError installing packages: {e}\033[0m")
        return False


def provide_docker_instructions() -> None:
    """Display Docker Desktop installation instructions."""
    print_header("Docker Desktop Installation")
    
    if sys.platform == "win32":
        print("""Docker Desktop is required for this laboratory.

\033[1mInstallation Steps:\033[0m

1. Visit: https://www.docker.com/products/docker-desktop

2. Download Docker Desktop for Windows

3. Run the installer and follow the prompts

4. During installation, ensure these options are selected:
   - Use WSL 2 instead of Hyper-V
   - Add shortcut to desktop

5. Restart your computer when prompted

6. After restart, launch Docker Desktop

7. Complete the initial setup wizard

8. Verify installation:
   Open PowerShell and run: docker --version

\033[93mNote:\033[0m Docker Desktop requires Windows 10 version 2004 or higher,
or Windows 11. WSL2 must be enabled.
""")
    else:
        print("""Docker is required for this laboratory.

\033[1mFor Ubuntu/Debian:\033[0m
  curl -fsSL https://get.docker.com | sh
  sudo usermod -aG docker $USER
  newgrp docker

\033[1mFor other distributions:\033[0m
  Visit: https://docs.docker.com/engine/install/

After installation, verify with: docker --version
""")


def provide_wsl2_instructions() -> None:
    """Display WSL2 installation instructions."""
    if sys.platform != "win32":
        return
    
    print_header("WSL2 Installation")
    
    print("""WSL2 (Windows Subsystem for Linux 2) is required.

\033[1mInstallation Steps:\033[0m

1. Open PowerShell as Administrator

2. Run the following command:
   wsl --install

3. Restart your computer

4. After restart, complete the Ubuntu setup when prompted

5. Verify WSL2 is the default:
   wsl --status

\033[1mIf WSL is already installed but using version 1:\033[0m
   wsl --set-default-version 2

\033[93mNote:\033[0m This requires Windows 10 version 2004+ or Windows 11.
""")


def provide_wireshark_instructions() -> None:
    """Display Wireshark installation instructions."""
    print_header("Wireshark Installation")
    
    if sys.platform == "win32":
        print("""Wireshark is recommended for packet analysis.

\033[1mInstallation Steps:\033[0m

1. Visit: https://www.wireshark.org/download.html

2. Download the Windows x64 Installer

3. Run the installer with default options

4. When prompted, install Npcap (required for capture)

5. Verify installation by launching Wireshark from Start menu

\033[93mNote:\033[0m You can also use tshark (command-line) from within
the Docker container if you prefer CLI analysis.
""")
    else:
        print("""Wireshark is recommended for packet analysis.

\033[1mFor Ubuntu/Debian:\033[0m
  sudo apt update
  sudo apt install wireshark tshark
  sudo usermod -aG wireshark $USER

\033[1mFor other distributions:\033[0m
  Visit: https://www.wireshark.org/download.html
""")


def main() -> int:
    """Main installation helper flow."""
    print("=" * 60)
    print("Prerequisites Installation Helper")
    print("NETWORKING class - ASE, Informatics | by Revolvix")
    print("=" * 60)
    
    print("\nThis script will help you install missing prerequisites.")
    print("Some installations require manual steps.\n")

    # Check what's missing
    missing_docker = not check_command("docker")
    missing_wireshark = not (
        Path(r"C:\Program Files\Wireshark\Wireshark.exe").exists() or
        check_command("wireshark") or
        check_command("tshark")
    )
    
    # Always try to install/upgrade Python packages
    print_header("Python Packages")
    install_python_packages()
    
    # Provide instructions for missing system software
    if missing_docker:
        provide_docker_instructions()
    else:
        print("\n\033[92mDocker is already installed.\033[0m")
    
    if sys.platform == "win32":
        # Check WSL2
        try:
            result = subprocess.run(
                ["wsl", "--status"],
                capture_output=True,
                timeout=10
            )
            output = result.stdout.decode(errors="ignore") + result.stderr.decode(errors="ignore")
            if "WSL 2" not in output and "Default Version: 2" not in output:
                provide_wsl2_instructions()
            else:
                print("\n\033[92mWSL2 is already configured.\033[0m")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            provide_wsl2_instructions()
    
    if missing_wireshark:
        provide_wireshark_instructions()
    else:
        print("\n\033[92mWireshark is already installed.\033[0m")
    
    # Final verification prompt
    print_header("Next Steps")
    print("""After completing any manual installations:

1. Restart your terminal/PowerShell

2. Run the environment verification again:
   python setup/verify_environment.py

3. If all checks pass, start the laboratory:
   python scripts/start_lab.py

For additional help, see docs/troubleshooting.md
""")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
