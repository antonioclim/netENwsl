#!/usr/bin/env python3
"""
Docker Desktop Configuration Helper
NETWORKING class - ASE, Informatics | by Revolvix

Provides guidance and automation for Docker Desktop configuration
with WSL2 backend for the Week 10 laboratory.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import subprocess
import sys
import json
import platform
from pathlib import Path



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def print_header(title: str) -> None:
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_wsl_distros() -> list:
    """List installed WSL distributions."""
    try:
        result = subprocess.run(
            ["wsl", "-l", "-v"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            distros = []
            for line in lines[1:]:  # Skip header
                parts = line.strip().split()
                if parts:
                    name = parts[0].replace('*', '').strip()
                    if name and not name.startswith('-'):
                        distros.append(name)
            return distros
    except Exception:
        pass
    return []



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_docker_desktop_settings() -> None:
    """Check Docker Desktop settings and provide recommendations."""
    print_header("Docker Desktop Configuration Check")
    
    # Check if Docker is using WSL2 backend
    try:
        result = subprocess.run(
            ["docker", "info", "--format", "{{.OperatingSystem}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            os_info = result.stdout.strip()
            print(f"Docker OS: {os_info}")
            
            if "wsl" in os_info.lower() or "linux" in os_info.lower():
                print("  ✓ Docker is using WSL2/Linux backend")
            else:
                print("  ⚠ Docker may not be using WSL2 backend")
                print("    Configure in Docker Desktop: Settings > General > Use WSL 2 based engine")
    except Exception as e:
        print(f"  ✗ Could not check Docker backend: {e}")
    
    # Check memory allocation
    try:
        result = subprocess.run(
            ["docker", "info", "--format", "{{.MemTotal}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            mem_bytes = int(result.stdout.strip())
            mem_gb = mem_bytes / (1024 ** 3)
            print(f"Docker memory: {mem_gb:.1f} GB")
            
            if mem_gb >= 4:
                print("  ✓ Sufficient memory allocated")
            else:
                print("  ⚠ Consider allocating more memory for Docker")
                print("    Configure in Docker Desktop: Settings > Resources > Memory")
    except Exception:
        pass
    
    # List WSL distributions
    distros = check_wsl_distros()
    if distros:
        print(f"\nWSL distributions: {', '.join(distros)}")
        print("  Ensure Docker Desktop WSL integration is enabled for your distro")
        print("  Configure in: Docker Desktop > Settings > Resources > WSL Integration")



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def print_network_configuration() -> None:
    """Print network configuration for the laboratory."""
    print_header("Laboratory Network Configuration")
    
    print("""
The Week 10 laboratory uses the following network configuration:

Docker Network: labnet (172.20.0.0/24)
  • 172.20.0.10  - web (HTTP server)
  • 172.20.0.53  - dns-server (custom DNS)
  • 172.20.0.22  - ssh-server (OpenSSH)
  • 172.20.0.21  - ftp-server (pyftpdlib)
  • 172.20.0.100 - ssh-client (Paramiko)
  • 172.20.0.200 - debug (network tools)

Host Port Mappings:
  • 8000  → web:8000        (HTTP)
  • 5353  → dns-server:5353 (DNS/UDP)
  • 2222  → ssh-server:22   (SSH)
  • 2121  → ftp-server:2121 (FTP control)
  • 30000-30009 → ftp-server (FTP passive)

To capture traffic in Wireshark:
  1. Use the "vEthernet (WSL)" adapter on Windows
  2. Or capture inside containers using tcpdump
  3. Filter by the labnet subnet: ip.addr == 172.20.0.0/24
""")



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def print_wsl2_tips() -> None:
    """Print WSL2 configuration tips."""
    print_header("WSL2 Configuration Tips")
    
    print("""
For best performance:

1. Ensure WSL2 is your default version:
   wsl --set-default-version 2

2. Limit WSL2 memory usage (create .wslconfig in %USERPROFILE%):
   [wsl2]
   memory=4GB
   processors=2
   localhostForwarding=true

3. Restart WSL after configuration changes:
   wsl --shutdown

4. Access Windows files from WSL:
   /mnt/c/Users/<username>/

5. Access WSL files from Windows:
   \\\\wsl$\\<distro-name>\\

Common issues:
  • Slow file access: Store project files in WSL filesystem (/home/...)
  • Network issues: Ensure localhostForwarding=true in .wslconfig
  • Docker not starting: Check Docker Desktop is running on Windows
""")



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    print("Docker Desktop Configuration Helper")
    print("NETWORKING class - ASE, Informatics | by Revolvix")
    
    if platform.system() != "Windows":
        print("\nNote: This script is designed for Windows with Docker Desktop.")
        print("On Linux, Docker can be installed directly without Docker Desktop.")
    
    check_docker_desktop_settings()
    print_network_configuration()
    print_wsl2_tips()
    
    print_header("Ready to Start")
    print("""
To start the laboratory:
  python scripts/start_lab.py

To verify services:
  python scripts/start_lab.py --status
""")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
