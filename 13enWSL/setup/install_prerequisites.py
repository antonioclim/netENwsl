#!/usr/bin/env python3
"""
Prerequisites Installation Helper
NETWORKING class - ASE, Informatics | by Revolvix

This script helps verify and guide installation of prerequisites
for the Week 13 IoT and Security laboratory.
"""

import subprocess
import sys
import shutil
import platform
from pathlib import Path
from typing import List, Tuple


def print_banner():
    """Display script banner."""
    print("=" * 70)
    print("  Week 13 - Prerequisites Installation Helper")
    print("  IoT and Security in Computer Networks")
    print("  NETWORKING class - ASE, Informatics")
    print("=" * 70)
    print()


def check_admin() -> bool:
    """Check if running with administrator/root privileges."""
    if platform.system() == "Windows":
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False
    else:
        import os
        return os.geteuid() == 0


def run_command(cmd: List[str], capture: bool = True) -> Tuple[int, str, str]:
    """Run a command and return (returncode, stdout, stderr)."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture,
            text=True,
            timeout=120
        )
        return result.returncode, result.stdout or "", result.stderr or ""
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)


def install_python_packages():
    """Install required Python packages."""
    print("\n--- Installing Python Packages ---\n")
    
    packages = [
        "docker",
        "requests",
        "pyyaml",
        "paho-mqtt",
        "scapy",
    ]
    
    for pkg in packages:
        print(f"Installing {pkg}...", end=" ", flush=True)
        code, out, err = run_command([
            sys.executable, "-m", "pip", "install", "--quiet", pkg
        ])
        if code == 0:
            print("OK")
        else:
            print(f"FAILED\n  Error: {err.strip()}")


def check_docker_desktop():
    """Check and provide guidance for Docker Desktop."""
    print("\n--- Docker Desktop ---\n")
    
    if shutil.which("docker"):
        code, out, err = run_command(["docker", "info"])
        if code == 0:
            print("[OK] Docker is installed and running")
            return True
        else:
            print("[!] Docker is installed but daemon is not running")
            print("    Please start Docker Desktop")
            return False
    else:
        print("[!] Docker is not installed")
        print()
        print("Installation instructions:")
        print("  1. Download Docker Desktop from https://www.docker.com/products/docker-desktop/")
        print("  2. Run the installer")
        print("  3. During setup, ensure WSL2 backend is selected")
        print("  4. Restart your computer if prompted")
        print("  5. Start Docker Desktop")
        return False


def check_wsl2():
    """Check and provide guidance for WSL2."""
    print("\n--- WSL2 Configuration ---\n")
    
    if platform.system() != "Windows":
        print("[INFO] Not running on Windows, skipping WSL2 check")
        return True
    
    code, out, err = run_command(["wsl", "--status"])
    output = out + err
    
    if "WSL 2" in output or "Default Version: 2" in output:
        print("[OK] WSL2 is configured correctly")
        return True
    else:
        print("[!] WSL2 may not be properly configured")
        print()
        print("To enable WSL2, run these commands in PowerShell (as Administrator):")
        print()
        print("  wsl --install")
        print("  wsl --set-default-version 2")
        print()
        print("Then restart your computer.")
        return False


def check_wireshark():
    """Check and provide guidance for Wireshark."""
    print("\n--- Wireshark ---\n")
    
    wireshark_paths = [
        Path(r"C:\Program Files\Wireshark\Wireshark.exe"),
        Path(r"C:\Program Files (x86)\Wireshark\Wireshark.exe"),
    ]
    
    for path in wireshark_paths:
        if path.exists():
            print(f"[OK] Wireshark found at {path}")
            return True
    
    if shutil.which("wireshark"):
        print("[OK] Wireshark is available in PATH")
        return True
    
    print("[!] Wireshark is not installed")
    print()
    print("Installation instructions:")
    print("  1. Download Wireshark from https://www.wireshark.org/download.html")
    print("  2. Run the installer (choose Windows x64 Installer)")
    print("  3. During installation, install Npcap when prompted")
    print("  4. Complete the installation")
    return False


def setup_project_structure():
    """Ensure project directories exist."""
    print("\n--- Project Structure ---\n")
    
    project_root = Path(__file__).parent.parent
    
    directories = [
        "artifacts",
        "pcap",
        "docker/configs/certs",
        "docker/volumes",
    ]
    
    for dir_name in directories:
        dir_path = project_root / dir_name
        if not dir_path.exists():
            dir_path.mkdir(parents=True)
            print(f"  Created: {dir_name}/")
        else:
            print(f"  Exists:  {dir_name}/")


def generate_certificates():
    """Generate TLS certificates for MQTT."""
    print("\n--- TLS Certificates ---\n")
    
    project_root = Path(__file__).parent.parent
    certs_dir = project_root / "docker" / "configs" / "certs"
    
    ca_key = certs_dir / "ca.key"
    ca_crt = certs_dir / "ca.crt"
    server_key = certs_dir / "server.key"
    server_crt = certs_dir / "server.crt"
    
    if ca_crt.exists() and server_crt.exists():
        print("[OK] Certificates already exist")
        return True
    
    if not shutil.which("openssl"):
        print("[!] OpenSSL not found in PATH")
        print("    On Windows, OpenSSL is typically installed with Git")
        print("    Alternatively, install from https://slproweb.com/products/Win32OpenSSL.html")
        return False
    
    certs_dir.mkdir(parents=True, exist_ok=True)
    
    print("Generating CA certificate...")
    code, out, err = run_command([
        "openssl", "req", "-x509", "-newkey", "rsa:2048",
        "-days", "365", "-nodes",
        "-subj", "/CN=Week13-CA",
        "-keyout", str(ca_key),
        "-out", str(ca_crt)
    ])
    
    if code != 0:
        print(f"[!] Failed to generate CA certificate: {err}")
        return False
    
    print("Generating server certificate...")
    csr_path = certs_dir / "server.csr"
    
    code, out, err = run_command([
        "openssl", "req", "-newkey", "rsa:2048", "-nodes",
        "-subj", "/CN=week13-mqtt",
        "-keyout", str(server_key),
        "-out", str(csr_path)
    ])
    
    if code != 0:
        print(f"[!] Failed to generate server CSR: {err}")
        return False
    
    code, out, err = run_command([
        "openssl", "x509", "-req", "-days", "365",
        "-in", str(csr_path),
        "-CA", str(ca_crt),
        "-CAkey", str(ca_key),
        "-CAcreateserial",
        "-out", str(server_crt)
    ])
    
    if code != 0:
        print(f"[!] Failed to sign server certificate: {err}")
        return False
    
    # Cleanup temporary files
    csr_path.unlink(missing_ok=True)
    (certs_dir / "ca.srl").unlink(missing_ok=True)
    
    print("[OK] Certificates generated successfully")
    return True


def main():
    """Main installation helper routine."""
    print_banner()
    
    if not check_admin():
        print("[INFO] Running without administrator privileges")
        print("       Some operations may require elevated permissions")
        print()
    
    # Check prerequisites
    all_ok = True
    
    all_ok &= check_wsl2()
    all_ok &= check_docker_desktop()
    all_ok &= check_wireshark()
    
    # Install Python packages
    print("\nProceed with Python package installation? [Y/n]: ", end="")
    try:
        response = input().strip().lower()
        if response in ("", "y", "yes"):
            install_python_packages()
    except EOFError:
        install_python_packages()
    
    # Setup project structure
    setup_project_structure()
    
    # Generate certificates
    generate_certificates()
    
    # Summary
    print("\n" + "=" * 70)
    print("  Setup Summary")
    print("=" * 70)
    print()
    
    if all_ok:
        print("[OK] All prerequisites appear to be met")
    else:
        print("[!] Some prerequisites need attention (see above)")
    
    print()
    print("Next steps:")
    print("  1. Run: python setup/verify_environment.py")
    print("  2. Run: python scripts/start_lab.py")
    print()
    
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
