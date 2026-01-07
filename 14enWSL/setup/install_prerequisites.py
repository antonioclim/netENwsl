#!/usr/bin/env python3
"""
Prerequisites Installation Helper
NETWORKING class - ASE, Informatics | by Revolvix

Assists with installing and configuring prerequisites for the Week 14
laboratory environment on Windows with WSL2.

This script provides guidance and automated checks for:
- Python packages
- Docker Desktop verification
- WSL2 configuration
- Network analysis tools

Note: Some installations require administrator privileges and manual steps.
"""

import subprocess
import sys
import shutil
import platform
from pathlib import Path
from typing import Tuple, List, Optional

# Colour codes for terminal output
class Colours:
    """ANSI colour codes for terminal output."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str) -> None:
    """Print a formatted header."""
    print(f"\n{Colours.HEADER}{Colours.BOLD}{'=' * 60}{Colours.ENDC}")
    print(f"{Colours.HEADER}{Colours.BOLD}{text}{Colours.ENDC}")
    print(f"{Colours.HEADER}{Colours.BOLD}{'=' * 60}{Colours.ENDC}\n")

def print_success(text: str) -> None:
    """Print success message."""
    print(f"{Colours.GREEN}[✓] {text}{Colours.ENDC}")

def print_warning(text: str) -> None:
    """Print warning message."""
    print(f"{Colours.YELLOW}[!] {text}{Colours.ENDC}")

def print_error(text: str) -> None:
    """Print error message."""
    print(f"{Colours.RED}[✗] {text}{Colours.ENDC}")

def print_info(text: str) -> None:
    """Print info message."""
    print(f"{Colours.CYAN}[i] {text}{Colours.ENDC}")

def run_command(cmd: List[str], timeout: int = 30) -> Tuple[bool, str, str]:
    """
    Execute a command and return results.
    
    Returns:
        Tuple of (success, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return (result.returncode == 0, result.stdout, result.stderr)
    except subprocess.TimeoutExpired:
        return (False, "", "Command timed out")
    except FileNotFoundError:
        return (False, "", f"Command not found: {cmd[0]}")
    except Exception as e:
        return (False, "", str(e))

def check_python_version() -> bool:
    """Verify Python version meets requirements."""
    version = sys.version_info
    if version >= (3, 11):
        print_success(f"Python {version.major}.{version.minor}.{version.micro} installed")
        return True
    elif version >= (3, 10):
        print_warning(f"Python {version.major}.{version.minor} works but 3.11+ recommended")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor} too old (need 3.10+)")
        return False

def install_python_packages() -> bool:
    """Install required Python packages."""
    print_info("Installing required Python packages...")
    
    # Get the requirements file path
    script_dir = Path(__file__).parent
    requirements_file = script_dir / "requirements.txt"
    
    if not requirements_file.exists():
        print_error("requirements.txt not found")
        return False
    
    # Read required packages
    with open(requirements_file, 'r') as f:
        packages = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    # Check and install each package
    all_installed = True
    for package in packages:
        package_name = package.split('>=')[0].split('==')[0].strip()
        
        try:
            __import__(package_name.replace('-', '_'))
            print_success(f"Package '{package_name}' already installed")
        except ImportError:
            print_info(f"Installing '{package_name}'...")
            success, stdout, stderr = run_command([
                sys.executable, '-m', 'pip', 'install', package, '--quiet'
            ])
            
            if success:
                print_success(f"Installed '{package_name}'")
            else:
                print_error(f"Failed to install '{package_name}': {stderr}")
                all_installed = False
    
    return all_installed

def check_docker() -> bool:
    """Check if Docker is installed and running."""
    # Check Docker installed
    if not shutil.which('docker'):
        print_error("Docker not found")
        print_info("Install Docker Desktop from: https://www.docker.com/products/docker-desktop/")
        return False
    
    print_success("Docker CLI installed")
    
    # Check Docker running
    success, _, _ = run_command(['docker', 'info'], timeout=15)
    if not success:
        print_error("Docker daemon not running")
        print_info("Start Docker Desktop application")
        return False
    
    print_success("Docker daemon running")
    
    # Check Docker Compose
    success, stdout, _ = run_command(['docker', 'compose', 'version'])
    if success:
        version = stdout.strip().split()[-1] if stdout else "unknown"
        print_success(f"Docker Compose {version} available")
        return True
    else:
        print_error("Docker Compose not available")
        return False

def check_wsl2() -> bool:
    """Check WSL2 configuration on Windows."""
    if platform.system() != 'Windows':
        print_info("Not on Windows - skipping WSL2 check")
        return True
    
    success, stdout, stderr = run_command(['wsl', '--status'], timeout=10)
    output = stdout + stderr
    
    if 'WSL 2' in output or 'Default Version: 2' in output:
        print_success("WSL2 enabled and configured")
        return True
    else:
        print_warning("WSL2 status unclear")
        print_info("Enable WSL2: wsl --install")
        print_info("Set default: wsl --set-default-version 2")
        return False

def check_wireshark() -> bool:
    """Check if Wireshark is installed."""
    # Check common Windows paths
    wireshark_paths = [
        Path(r"C:\Program Files\Wireshark\Wireshark.exe"),
        Path(r"C:\Program Files (x86)\Wireshark\Wireshark.exe"),
    ]
    
    for path in wireshark_paths:
        if path.exists():
            print_success(f"Wireshark found at {path}")
            return True
    
    # Check if in PATH
    if shutil.which('wireshark'):
        print_success("Wireshark available in PATH")
        return True
    
    print_warning("Wireshark not found")
    print_info("Install from: https://www.wireshark.org/download.html")
    return False

def check_tshark() -> bool:
    """Check if tshark is available."""
    # Check common paths
    tshark_paths = [
        Path(r"C:\Program Files\Wireshark\tshark.exe"),
        Path(r"C:\Program Files (x86)\Wireshark\tshark.exe"),
    ]
    
    for path in tshark_paths:
        if path.exists():
            print_success(f"tshark found at {path}")
            return True
    
    if shutil.which('tshark'):
        print_success("tshark available in PATH")
        return True
    
    print_warning("tshark not found (installed with Wireshark)")
    return False

def check_ports_available() -> bool:
    """Check if required ports are available."""
    import socket
    
    required_ports = [
        (8080, "Load Balancer"),
        (8001, "Backend App 1"),
        (8002, "Backend App 2"),
        (9000, "TCP Echo Server"),
        (9443, "Portainer (optional)"),
    ]
    
    all_available = True
    for port, service in required_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            result = sock.connect_ex(('localhost', port))
            if result == 0:
                print_warning(f"Port {port} ({service}) is in use")
                all_available = False
            else:
                print_success(f"Port {port} ({service}) available")
        except Exception:
            print_success(f"Port {port} ({service}) available")
        finally:
            sock.close()
    
    return all_available

def configure_docker_for_wsl2() -> None:
    """Provide guidance for Docker Desktop WSL2 configuration."""
    print_header("Docker Desktop Configuration Guide")
    
    print(f"""
{Colours.CYAN}To configure Docker Desktop for optimal WSL2 performance:{Colours.ENDC}

1. {Colours.BOLD}Open Docker Desktop Settings{Colours.ENDC}
   - Click the Docker icon in the system tray
   - Select 'Settings' (gear icon)

2. {Colours.BOLD}General Settings{Colours.ENDC}
   - Enable: "Use the WSL 2 based engine"
   - Enable: "Start Docker Desktop when you log in" (optional)

3. {Colours.BOLD}Resources > WSL Integration{Colours.ENDC}
   - Enable: "Enable integration with my default WSL distro"
   - Select your preferred distro (e.g., Ubuntu)

4. {Colours.BOLD}Resources > Advanced{Colours.ENDC}
   - Memory: At least 4GB (8GB recommended)
   - CPUs: At least 2 cores
   - Disk image size: At least 20GB

5. {Colours.BOLD}Click "Apply & Restart"{Colours.ENDC}

{Colours.YELLOW}Note: Docker Desktop requires a restart after configuration changes.{Colours.ENDC}
""")

def show_manual_installation_guide() -> None:
    """Display manual installation instructions."""
    print_header("Manual Installation Guide")
    
    print(f"""
{Colours.BOLD}1. Python 3.11+{Colours.ENDC}
   Download: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"
   - Check "Install pip"

{Colours.BOLD}2. Docker Desktop{Colours.ENDC}
   Download: https://www.docker.com/products/docker-desktop/
   - Requires Windows 10/11 Pro, Enterprise, or Education
   - Or Windows 10/11 Home with WSL2
   - Enable WSL2 backend during installation

{Colours.BOLD}3. WSL2 (Windows Subsystem for Linux){Colours.ENDC}
   Open PowerShell as Administrator:
   {Colours.CYAN}wsl --install{Colours.ENDC}
   {Colours.CYAN}wsl --set-default-version 2{Colours.ENDC}

{Colours.BOLD}4. Wireshark{Colours.ENDC}
   Download: https://www.wireshark.org/download.html
   - Include "TShark" during installation
   - Install "Npcap" when prompted

{Colours.BOLD}5. Git (Optional but Recommended){Colours.ENDC}
   Download: https://git-scm.com/download/win

{Colours.YELLOW}After installation, restart your computer and run this script again.{Colours.ENDC}
""")

def main() -> int:
    """
    Main entry point for prerequisites installation.
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    print_header("Week 14 Prerequisites Installer")
    print("NETWORKING class - ASE, Informatics | by Revolvix")
    print()
    
    # Track overall status
    issues_found = False
    
    # Check Python
    print(f"\n{Colours.BOLD}Python Environment{Colours.ENDC}")
    if not check_python_version():
        issues_found = True
    
    # Install Python packages
    print(f"\n{Colours.BOLD}Python Packages{Colours.ENDC}")
    if not install_python_packages():
        issues_found = True
    
    # Check Docker
    print(f"\n{Colours.BOLD}Docker Environment{Colours.ENDC}")
    if not check_docker():
        issues_found = True
    
    # Check WSL2 (Windows only)
    print(f"\n{Colours.BOLD}WSL2 Configuration{Colours.ENDC}")
    if not check_wsl2():
        issues_found = True
    
    # Check Wireshark
    print(f"\n{Colours.BOLD}Network Analysis Tools{Colours.ENDC}")
    wireshark_ok = check_wireshark()
    tshark_ok = check_tshark()
    if not (wireshark_ok or tshark_ok):
        print_warning("Network capture tools not found")
        issues_found = True
    
    # Check ports
    print(f"\n{Colours.BOLD}Port Availability{Colours.ENDC}")
    if not check_ports_available():
        print_warning("Some ports are in use - may need to stop other services")
    
    # Summary
    print_header("Summary")
    
    if not issues_found:
        print_success("All prerequisites are installed and configured!")
        print_info("You can now run: python scripts/start_lab.py")
        return 0
    else:
        print_warning("Some prerequisites need attention")
        print()
        
        response = input("Would you like to see the manual installation guide? [Y/n]: ")
        if response.lower() != 'n':
            show_manual_installation_guide()
        
        response = input("Would you like to see Docker configuration tips? [Y/n]: ")
        if response.lower() != 'n':
            configure_docker_for_wsl2()
        
        return 1

if __name__ == "__main__":
    sys.exit(main())
