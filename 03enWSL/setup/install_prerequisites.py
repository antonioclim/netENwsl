#!/usr/bin/env python3
"""
Prerequisites Installation Helper
NETWORKING class - ASE, Informatics | by Revolvix

Assists with installing and configuring prerequisites for the Week 3 laboratory.
This script provides guidance and automation for Windows/WSL2 environments.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import subprocess
import sys
import platform
import webbrowser
from pathlib import Path
from typing import Optional



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class PrerequisiteInstaller:
    """Guides installation of laboratory prerequisites."""


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
    def __init__(self):
        self.is_windows = platform.system() == "Windows"
        self.is_admin = self._check_admin()


# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
    def _check_admin(self) -> bool:
        """Check if running with administrator privileges."""
        if not self.is_windows:
            return False
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False


# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
    def print_header(self, title: str) -> None:
        """Print a formatted section header."""
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60)


# ═══════════════════════════════════════════════════════════════════════════════
# PREDICTION_PROMPT
# ═══════════════════════════════════════════════════════════════════════════════
    def prompt_continue(self, message: str = "Press Enter to continue...") -> None:
        """Pause and wait for user input."""
        input(f"\n{message}")


# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
    def run_command(self, cmd: list, shell: bool = False) -> bool:
        """Run a command and return success status."""
        try:
            result = subprocess.run(cmd, shell=shell)
            return result.returncode == 0
        except Exception as e:
            print(f"Error: {e}")
            return False


# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def install_python_packages(self) -> bool:
        """Install required Python packages."""
        self.print_header("Installing Python Packages")
        
        packages = ["pyyaml", "requests"]
        
        print("Installing required Python packages...")
        for pkg in packages:
            print(f"  Installing {pkg}...")
            success = self.run_command([
                sys.executable, "-m", "pip", "install", "--quiet", pkg
            ])
            if not success:
                print(f"  Failed to install {pkg}")
                return False
            print(f"  ✓ {pkg} installed")
        
        return True


# ═══════════════════════════════════════════════════════════════════════════════
# CONTAINER_MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════
    def guide_docker_installation(self) -> None:
        """Guide user through Docker Desktop installation."""
        self.print_header("Docker Desktop Installation")
        
        print("""
Docker Desktop is required for running the laboratory containers.

Installation steps:
1. Download Docker Desktop from: https://docker.com/products/docker-desktop
2. Run the installer (requires administrator privileges)
3. During installation, ensure "Use WSL 2 instead of Hyper-V" is selected
4. Restart your computer when prompted
5. After restart, open Docker Desktop and complete the initial setup
6. Accept the Docker Desktop Service Agreement

Important settings after installation:
- Settings → General → "Use the WSL 2 based engine" should be enabled
- Settings → Resources → WSL Integration → Enable integration with your distro
""")
        
        if input("Open Docker Desktop download page? (y/n): ").lower() == 'y':
            webbrowser.open("https://www.docker.com/products/docker-desktop")
        
        self.prompt_continue()


# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def guide_wsl2_installation(self) -> None:
        """Guide user through WSL2 installation."""
        self.print_header("WSL2 Installation")
        
        print("""
WSL2 (Windows Subsystem for Linux 2) provides a Linux environment on Windows.

For Windows 10 (version 2004+) or Windows 11:

Option 1: Automatic installation (recommended)
  Open PowerShell as Administrator and run:
    wsl --install

  This installs WSL2 with Ubuntu by default. Restart when prompted.

Option 2: Manual installation
  If automatic installation fails, follow these steps:

  1. Enable Windows features:
     dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
     dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

  2. Restart your computer

  3. Download and install the WSL2 kernel update:
     https://aka.ms/wsl2kernel

  4. Set WSL2 as default:
     wsl --set-default-version 2

  5. Install Ubuntu from Microsoft Store or using:
     wsl --install -d Ubuntu-22.04
""")
        
        if self.is_admin:
            if input("Run 'wsl --install' now? (y/n): ").lower() == 'y':
                self.run_command(["wsl", "--install"], shell=True)
        else:
            print("\nNote: WSL installation requires administrator privileges.")
            print("Please run PowerShell as Administrator to install WSL.")
        
        self.prompt_continue()


# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def guide_wireshark_installation(self) -> None:
        """Guide user through Wireshark installation."""
        self.print_header("Wireshark Installation")
        
        print("""
Wireshark is used for packet capture and analysis.

Installation steps:
1. Download from: https://www.wireshark.org/download.html
2. Run the installer
3. During installation:
   - Select "Install Npcap" (required for packet capture)
   - When prompted about Npcap, select "Install Npcap in WinPcap API-compatible mode"
4. After installation, you may need to restart your computer

For capturing Docker traffic on Windows:
- Use the interface named "\\Device\\NPF_{...}" or similar
- Alternatively, capture inside containers using tcpdump
""")
        
        if input("Open Wireshark download page? (y/n): ").lower() == 'y':
            webbrowser.open("https://www.wireshark.org/download.html")
        
        self.prompt_continue()


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
    def configure_python_path(self) -> None:
        """Add project to Python path."""
        self.print_header("Python Path Configuration")
        
        project_root = Path(__file__).parent.parent.resolve()
        
        print(f"""
To use the project modules, the project root should be in your Python path.

Project root: {project_root}

Option 1: Set PYTHONPATH environment variable
  PowerShell:
    $env:PYTHONPATH = "{project_root}"
  
  Or permanently via System Properties → Environment Variables

Option 2: Install in development mode
  cd {project_root}
  pip install -e .

Option 3: The scripts handle this automatically by adding the project root
  to sys.path at runtime.
""")
        
        self.prompt_continue()


# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
    def verify_setup(self) -> bool:
        """Run verification to check installation status."""
        self.print_header("Verifying Installation")
        
        print("Running environment verification...\n")
        
        verify_script = Path(__file__).parent / "verify_environment.py"
        if verify_script.exists():
            result = subprocess.run([sys.executable, str(verify_script)])
            return result.returncode == 0
        else:
            print("Verification script not found.")
            return False



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main installation routine."""
    print("=" * 60)
    print("Prerequisites Installation Helper")
    print("Week 3 Laboratory - NETWORKING class")
    print("ASE, Informatics | by Revolvix")
    print("=" * 60)
    
    installer = PrerequisiteInstaller()
    
    if not installer.is_windows:
        print("\nNote: This helper is designed for Windows systems.")
        print("On Linux, use your distribution's package manager.")
    
    print("""
This helper will guide you through installing the prerequisites
for the Week 3 laboratory environment.

Select an option:
  1. Install Python packages only
  2. Guide: Docker Desktop installation
  3. Guide: WSL2 installation
  4. Guide: Wireshark installation
  5. Configure Python path
  6. Verify current setup
  7. Install all Python packages and verify
  0. Exit
""")
    
    while True:
        try:
            choice = input("\nEnter choice (0-7): ").strip()
            
            if choice == "0":
                print("Exiting.")
                return 0
            elif choice == "1":
                installer.install_python_packages()
            elif choice == "2":
                installer.guide_docker_installation()
            elif choice == "3":
                installer.guide_wsl2_installation()
            elif choice == "4":
                installer.guide_wireshark_installation()
            elif choice == "5":
                installer.configure_python_path()
            elif choice == "6":
                installer.verify_setup()
            elif choice == "7":
                if installer.install_python_packages():
                    print("\n✓ Python packages installed successfully.")
                installer.verify_setup()
            else:
                print("Invalid choice. Please enter 0-7.")
                
        except KeyboardInterrupt:
            print("\n\nInterrupted by user.")
            return 1
        except EOFError:
            return 0


if __name__ == "__main__":
    sys.exit(main())
