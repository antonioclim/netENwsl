#!/usr/bin/env python3
"""
Prerequisites Installation Helper
NETWORKING class - ASE, Informatics | by Revolvix

Assists with installing and configuring prerequisites for the
Week 9 laboratory environment on Windows with WSL2.

Usage:
    python setup/install_prerequisites.py
    python setup/install_prerequisites.py --check-only
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import subprocess
import sys
import webbrowser
from pathlib import Path



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def print_header(title: str) -> None:
    """Print a section header."""
    print()
    print("=" * 60)
    print(f" {title}")
    print("=" * 60)
    print()



# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
def run_command(cmd: list, check: bool = True) -> bool:
    """Run a command and return success status."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError):
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def install_python_packages() -> bool:
    """Install required Python packages."""
    print_header("Installing Python Packages")
    
    packages = [
        "docker",
        "requests",
        "pyyaml",
        "pyftpdlib"  # For FTP server exercises
    ]
    
    print("Required packages:", ", ".join(packages))
    print()
    
    for pkg in packages:
        print(f"Installing {pkg}...", end=" ", flush=True)
        
        if run_command([sys.executable, "-m", "pip", "install", pkg]):
            print("✓")
        else:
            print("✗")
            print(f"  Try manually: pip install {pkg}")
    
    return True



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_docker_desktop() -> bool:
    """Check and guide Docker Desktop installation."""
    print_header("Docker Desktop")
    
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print(f"Docker is installed: {result.stdout.strip()}")
            
            # Check if running
            info_result = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                timeout=10
            )
            
            if info_result.returncode == 0:
                print("Docker daemon is running ✓")
                return True
            else:
                print("Docker daemon is NOT running")
                print()
                print("Please start Docker Desktop:")
                print("  1. Open Docker Desktop from Start menu")
                print("  2. Wait for it to start (whale icon in system tray)")
                print("  3. Run this script again")
                return False
        else:
            raise FileNotFoundError()
            
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Docker Desktop is not installed")
        print()
        print("Installation instructions:")
        print("  1. Download from: https://www.docker.com/products/docker-desktop/")
        print("  2. Run the installer")
        print("  3. Enable WSL2 backend when prompted")
        print("  4. Restart your computer if required")
        print("  5. Run this script again")
        print()
        
        response = input("Open Docker download page? [y/N]: ")
        if response.lower() == 'y':
            webbrowser.open("https://www.docker.com/products/docker-desktop/")
        
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_wsl2() -> bool:
    """Check and guide WSL2 installation."""
    print_header("WSL2")
    
    try:
        result = subprocess.run(
            ["wsl", "--status"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        output = result.stdout + result.stderr
        
        if "WSL 2" in output or "Default Version: 2" in output:
            print("WSL2 is available ✓")
            return True
        else:
            print("WSL2 may not be the default version")
            
    except (subprocess.SubprocessError, FileNotFoundError):
        print("WSL does not appear to be installed")
    
    print()
    print("To install/configure WSL2:")
    print("  1. Open PowerShell as Administrator")
    print("  2. Run: wsl --install")
    print("  3. Restart your computer")
    print("  4. Set WSL2 as default: wsl --set-default-version 2")
    print()
    print("For more information:")
    print("  https://docs.microsoft.com/en-us/windows/wsl/install")
    
    return False



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_wireshark() -> bool:
    """Check and guide Wireshark installation."""
    print_header("Wireshark")
    
    wireshark_paths = [
        Path(r"C:\Program Files\Wireshark\Wireshark.exe"),
        Path(r"C:\Program Files (x86)\Wireshark\Wireshark.exe")
    ]
    
    for path in wireshark_paths:
        if path.exists():
            print(f"Wireshark found: {path}")
            return True
    
    # Check in PATH
    try:
        result = subprocess.run(
            ["wireshark", "--version"],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            print("Wireshark is available in PATH ✓")
            return True
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    
    print("Wireshark is not installed")
    print()
    print("Installation instructions:")
    print("  1. Download from: https://www.wireshark.org/download.html")
    print("  2. Run the installer")
    print("  3. Include Npcap when prompted (for packet capture)")
    print()
    
    response = input("Open Wireshark download page? [y/N]: ")
    if response.lower() == 'y':
        webbrowser.open("https://www.wireshark.org/download.html")
    
    return False



# ═══════════════════════════════════════════════════════════════════════════════
# RESOURCE_CREATION
# ═══════════════════════════════════════════════════════════════════════════════
def create_project_structure() -> None:
    """Create necessary project directories."""
    print_header("Project Structure")
    
    project_root = Path(__file__).parent.parent
    
    directories = [
        project_root / "docker" / "server-files",
        project_root / "docker" / "client1-files",
        project_root / "docker" / "client2-files",
        project_root / "docker" / "volumes",
        project_root / "pcap",
        project_root / "artifacts"
    ]
    
    for d in directories:
        d.mkdir(parents=True, exist_ok=True)
        print(f"  Created: {d.relative_to(project_root)}")
    
    # Create .gitkeep files
    for d in directories:
        gitkeep = d / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()
    
    print()
    print("Project structure ready ✓")



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install prerequisites for Week 9 Laboratory"
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Only check prerequisites, don't install"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print(" Week 9 Laboratory - Prerequisites Installation")
    print(" NETWORKING class - ASE, Informatics")
    print("=" * 60)
    
    all_ok = True
    
    # Check/install each component
    if not check_wsl2():
        all_ok = False
    
    if not check_docker_desktop():
        all_ok = False
    
    if not check_wireshark():
        all_ok = False
    
    if not args.check_only:
        install_python_packages()
        create_project_structure()
    
    # Summary
    print_header("Summary")
    
    if all_ok:
        print("All prerequisites are installed! ✓")
        print()
        print("Next steps:")
        print("  1. python setup/verify_environment.py")
        print("  2. python scripts/start_lab.py")
    else:
        print("Some prerequisites need attention.")
        print("Please follow the instructions above and run this script again.")
    
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
