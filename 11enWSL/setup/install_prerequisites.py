#!/usr/bin/env python3
"""
Prerequisites Installation Helper for Week 11 Laboratory
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Assists with installing required dependencies.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import subprocess
import sys
import platform
import shutil
from pathlib import Path



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def print_header(text: str) -> None:
    """Print a formatted header."""
    print("")
    print("=" * 60)
    print(f" {text}")
    print("=" * 60)



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def print_step(text: str) -> None:
    """Print a step message."""
    print(f"\n>>> {text}")



# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
def run_command(cmd: list, check: bool = True) -> bool:
    """Run a command and return success status."""
    try:
        print(f"    Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=check)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        print(f"    Command not found: {cmd[0]}")
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def install_python_packages() -> bool:
    """Install required Python packages."""
    print_step("Installing Python packages...")
    
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("    Creating requirements.txt...")
        requirements_file.write_text("""# Week 11 Laboratory Dependencies
# NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

# Core dependencies
requests>=2.28.0
pyyaml>=6.0

# DNS client exercise
dnspython>=2.4.0

# SSH demo (optional)
paramiko>=3.3.0

# FTP server demo (optional)
pyftpdlib>=1.5.0
""")
    
    # Try pip install
    cmd = [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)]
    
    # Add --break-system-packages for system Python
    if platform.system() == "Linux":
        cmd.append("--break-system-packages")
    
    return run_command(cmd, check=False)



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_docker_desktop() -> bool:
    """Check and provide instructions for Docker Desktop."""
    print_step("Checking Docker Desktop...")
    
    if shutil.which("docker"):
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True
        )
        if result.returncode == 0:
            print("    Docker Desktop is installed and running")
            return True
        else:
            print("    Docker is installed but not running")
            print("    Please start Docker Desktop")
            return False
    else:
        print("    Docker Desktop is not installed")
        print("")
        print("    Installation instructions:")
        print("    1. Download Docker Desktop from: https://www.docker.com/products/docker-desktop/")
        print("    2. Run the installer")
        print("    3. Enable WSL2 backend during installation")
        print("    4. Restart your computer if prompted")
        print("    5. Start Docker Desktop")
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
def setup_wsl2() -> bool:
    """Provide WSL2 setup instructions (Windows only)."""
    if platform.system() != "Windows":
        return True
    
    print_step("Checking WSL2...")
    
    try:
        result = subprocess.run(
            ["wsl", "--status"],
            capture_output=True,
            text=True
        )
        output = result.stdout + result.stderr
        
        if "WSL 2" in output or "Default Version: 2" in output:
            print("    WSL2 is enabled")
            return True
        else:
            print("    WSL2 may not be properly configured")
    except FileNotFoundError:
        print("    WSL is not available")
    
    print("")
    print("    To enable WSL2, run in PowerShell (Admin):")
    print("    wsl --install")
    print("    ")
    print("    Then restart your computer")
    
    return False



# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
def setup_wireshark() -> bool:
    """Check Wireshark installation."""
    print_step("Checking Wireshark...")
    
    wireshark_paths = [
        Path(r"C:\Program Files\Wireshark\Wireshark.exe"),
        Path(r"C:\Program Files (x86)\Wireshark\Wireshark.exe"),
    ]
    
    for path in wireshark_paths:
        if path.exists():
            print(f"    Wireshark found: {path}")
            return True
    
    if shutil.which("wireshark"):
        print("    Wireshark found in PATH")
        return True
    
    print("    Wireshark not found")
    print("")
    print("    Installation instructions:")
    print("    1. Download from: https://www.wireshark.org/download.html")
    print("    2. Run the installer")
    print("    3. Install Npcap when prompted (required for packet capture)")
    
    return False



# ═══════════════════════════════════════════════════════════════════════════════
# RESOURCE_CREATION
# ═══════════════════════════════════════════════════════════════════════════════
def create_directory_structure() -> None:
    """Create required directory structure."""
    print_step("Creating directory structure...")
    
    project_root = Path(__file__).parent.parent
    
    directories = [
        "docker/configs",
        "docker/volumes",
        "scripts/utils",
        "src/exercises",
        "src/apps",
        "src/utils",
        "tests",
        "docs",
        "homework/exercises",
        "homework/solutions",
        "pcap",
        "artifacts",
    ]
    
    for dir_name in directories:
        dir_path = project_root / dir_name
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"    Created: {dir_name}/")
        else:
            print(f"    Exists:  {dir_name}/")
    
    # Create .gitkeep files
    gitkeep_dirs = ["docker/volumes", "homework/solutions", "pcap", "artifacts"]
    for dir_name in gitkeep_dirs:
        gitkeep = project_root / dir_name / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    print_header("Week 11 Laboratory - Prerequisites Installation")
    print("NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim")
    
    print(f"\nOperating System: {platform.system()} {platform.release()}")
    print(f"Python Version: {sys.version}")
    
    results = {}
    
    # Create directories
    create_directory_structure()
    
    # Install Python packages
    results['python_packages'] = install_python_packages()
    
    # Check Docker
    results['docker'] = check_docker_desktop()
    
    # Check WSL2 (Windows)
    if platform.system() == "Windows":
        results['wsl2'] = setup_wsl2()
    
    # Check Wireshark
    results['wireshark'] = setup_wireshark()
    
    # Summary
    print_header("Installation Summary")
    
    all_passed = True
    for name, passed in results.items():
        status = "\033[32mOK\033[0m" if passed else "\033[31mNEEDS ATTENTION\033[0m"
        print(f"  {name:20} {status}")
        if not passed:
            all_passed = False
    
    print("")
    
    if all_passed:
        print("\033[32mAll prerequisites are installed!\033[0m")
        print("\nNext steps:")
        print("  1. Run: python setup/verify_environment.py")
        print("  2. Start the lab: python scripts/start_lab.py")
        return 0
    else:
        print("\033[33mSome prerequisites need attention.\033[0m")
        print("Follow the instructions above to complete setup.")
        return 1


if __name__ == "__main__":
    sys.exit(main())


# ing. dr. Antonio Clim
