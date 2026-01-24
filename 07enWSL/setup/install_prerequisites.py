#!/usr/bin/env python3
"""
Prerequisites Installation Helper
NETWORKING class - ASE, Informatics | by Revolvix

Assists with installing and configuring prerequisites for the Week 7
laboratory environment on Windows with WSL2.
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
from typing import List



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def print_header(text: str) -> None:
    """Print a formatted header."""
    print()
    print("=" * 60)
    print(text)
    print("=" * 60)



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def print_step(step: int, text: str) -> None:
    """Print a numbered step."""
    print(f"\n[Step {step}] {text}")
    print("-" * 40)



# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
def run_command(args: List[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a command with output displayed."""
    print(f"  Running: {' '.join(args)}")
    return subprocess.run(args, check=check)



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_admin() -> bool:
    """Check if running with administrator privileges (Windows)."""
    if platform.system() != "Windows":
        return True
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def install_python_packages() -> None:
    """Install required Python packages."""
    print_step(1, "Installing Python packages")
    
    packages = [
        "pyyaml",
        "requests",
        "docker",
        "colorama",
    ]
    
    for pkg in packages:
        try:
            print(f"  Installing {pkg}...")
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "--quiet", pkg],
                check=True,
                capture_output=True
            )
            print(f"    [OK] {pkg} installed")
        except subprocess.CalledProcessError:
            print(f"    [WARN] Failed to install {pkg}")



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_wsl2_status() -> None:
    """Check and report WSL2 status on Windows."""
    print_step(2, "Checking WSL2 Status")
    
    if platform.system() != "Windows":
        print("  Not running on Windows, skipping WSL2 check")
        return
    
    try:
        result = subprocess.run(
            ["wsl", "--status"],
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stdout + result.stderr
        
        if "WSL 2" in output or "Default Version: 2" in output:
            print("  [OK] WSL2 is enabled")
        else:
            print("  [WARN] WSL2 may not be properly configured")
            print()
            print("  To enable WSL2, run in an Administrator PowerShell:")
            print("    wsl --install")
            print("    # or")
            print("    wsl --set-default-version 2")
            
    except FileNotFoundError:
        print("  [FAIL] WSL is not installed")
        print()
        print("  To install WSL, run in an Administrator PowerShell:")
        print("    wsl --install")
    except Exception as e:
        print(f"  [WARN] Could not check WSL status: {e}")



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_docker_status() -> None:
    """Check Docker Desktop status."""
    print_step(3, "Checking Docker Status")
    
    if not shutil.which("docker"):
        print("  [FAIL] Docker is not installed or not in PATH")
        print()
        print("  Install Docker Desktop from: https://docker.com/products/docker-desktop")
        print()
        print("  After installation:")
        print("    1. Enable WSL2 backend in Docker Desktop settings")
        print("    2. Restart Docker Desktop")
        return
    
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print("  [OK] Docker is running")
            
            # Check for WSL2 backend
            if "WSL" in result.stdout or platform.system() == "Linux":
                print("  [OK] WSL2 backend detected")
        else:
            print("  [WARN] Docker is installed but not running")
            print()
            print("  Please start Docker Desktop and wait for it to initialise")
            
    except subprocess.TimeoutExpired:
        print("  [WARN] Docker is responding slowly")
        print("  Please ensure Docker Desktop is fully started")
    except Exception as e:
        print(f"  [WARN] Could not check Docker status: {e}")



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_wireshark_status() -> None:
    """Check Wireshark installation."""
    print_step(4, "Checking Wireshark Status")
    
    wireshark_paths = [
        Path(r"C:\Program Files\Wireshark\Wireshark.exe"),
        Path(r"C:\Program Files (x86)\Wireshark\Wireshark.exe"),
    ]
    
    found = False
    for p in wireshark_paths:
        if p.exists():
            print(f"  [OK] Wireshark found at: {p}")
            found = True
            break
    
    # Also check tshark in PATH (for WSL)
    if shutil.which("tshark"):
        print("  [OK] tshark found in PATH")
        found = True
    
    if not found:
        print("  [WARN] Wireshark not found")
        print()
        print("  Install Wireshark from: https://wireshark.org/download.html")
        print()
        print("  During installation:")
        print("    - Install Npcap when prompted")
        print("    - Enable 'Install TShark' option")



# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
def setup_directories() -> None:
    """Ensure required directories exist."""
    print_step(5, "Setting up directories")
    
    script_dir = Path(__file__).resolve().parent.parent
    
    directories = [
        "artifacts",
        "pcap",
        "docker/volumes",
    ]
    
    for d in directories:
        dir_path = script_dir / d
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  Created: {d}/")
        else:
            print(f"  Exists:  {d}/")



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def print_next_steps() -> None:
    """Print next steps for the user."""
    print_header("Next Steps")
    
    print("""
1. Ensure Docker Desktop is running with WSL2 backend

2. Verify your environment:
   python setup/verify_environment.py

3. Configure Docker for this week:
   python setup/configure_docker.py

4. Start the laboratory:
   python scripts/start_lab.py

For troubleshooting, see docs/troubleshooting.md
""")



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main installation helper."""
    print_header("Week 7 Prerequisites Installation Helper")
    print("NETWORKING class - ASE, Informatics | by Revolvix")
    
    system = platform.system()
    print(f"\nDetected platform: {system} {platform.release()}")
    print(f"Python version: {sys.version}")
    
    if system == "Windows" and not check_admin():
        print()
        print("[WARN] Not running as Administrator")
        print("Some operations may require elevated privileges.")
        print("Consider running PowerShell as Administrator.")
    
    install_python_packages()
    check_wsl2_status()
    check_docker_status()
    check_wireshark_status()
    setup_directories()
    print_next_steps()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
