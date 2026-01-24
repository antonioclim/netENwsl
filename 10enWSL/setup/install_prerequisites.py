#!/usr/bin/env python3
"""
Prerequisites Installation Helper
NETWORKING class - ASE, Informatics | by Revolvix

Assists with installing and configuring prerequisites for Week 10 laboratory.
This script checks for missing components and provides installation guidance.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import subprocess
import sys
import shutil
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
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def print_step(step: int, message: str) -> None:
    """Print a numbered step."""
    print(f"\n[Step {step}] {message}")



# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
def run_command(cmd: list, description: str, check: bool = True) -> bool:
    """Run a command with proper error handling."""
    print(f"  Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  ✓ {description} completed successfully")
            return True
        else:
            print(f"  ✗ {description} failed")
            if result.stderr:
                print(f"    Error: {result.stderr[:200]}")
            return False
    except FileNotFoundError:
        print(f"  ✗ Command not found: {cmd[0]}")
        return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_python_packages() -> None:
    """Install required Python packages."""
    print_step(1, "Installing Python packages")
    
    packages = [
        "docker",
        "requests",
        "pyyaml",
        "flask",
        "paramiko",
        "dnslib",
        "pyftpdlib",
    ]
    
    for pkg in packages:
        try:
            __import__(pkg.replace("-", "_"))
            print(f"  ✓ {pkg} already installed")
        except ImportError:
            print(f"  Installing {pkg}...")
            run_command(
                [sys.executable, "-m", "pip", "install", pkg],
                f"Install {pkg}",
                check=False
            )



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_docker() -> bool:
    """Verify Docker is installed and running."""
    print_step(2, "Checking Docker installation")
    
    if not shutil.which("docker"):
        print("  ✗ Docker not found in PATH")
        print("\n  To install Docker Desktop:")
        print("    1. Download from https://docker.com/products/docker-desktop")
        print("    2. Run the installer")
        print("    3. Enable WSL2 integration in Docker Desktop settings")
        print("    4. Restart this script")
        return False
    
    # Check if Docker daemon is running
    result = subprocess.run(
        ["docker", "info"],
        capture_output=True,
        timeout=15
    )
    
    if result.returncode != 0:
        print("  ✗ Docker daemon is not running")
        print("\n  Please start Docker Desktop and try again")
        return False
    
    print("  ✓ Docker is installed and running")
    
    # Check Docker Compose
    result = subprocess.run(
        ["docker", "compose", "version"],
        capture_output=True
    )
    
    if result.returncode == 0:
        print("  ✓ Docker Compose is available")
    else:
        print("  ✗ Docker Compose not found (should come with Docker Desktop)")
    
    return True



# ═══════════════════════════════════════════════════════════════════════════════
# RESOURCE_CREATION
# ═══════════════════════════════════════════════════════════════════════════════
def create_directories() -> None:
    """Create required directories if they don't exist."""
    print_step(3, "Creating directory structure")
    
    project_root = Path(__file__).parent.parent
    
    directories = [
        "artifacts",
        "pcap",
        "docker/volumes",
        "docker/configs",
    ]
    
    for dir_name in directories:
        dir_path = project_root / dir_name
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  Created: {dir_name}/")
        else:
            print(f"  ✓ {dir_name}/ exists")
    
    # Create .gitkeep files
    for dir_name in ["artifacts", "pcap", "docker/volumes"]:
        gitkeep = project_root / dir_name / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()



# ═══════════════════════════════════════════════════════════════════════════════
# RESOURCE_CREATION
# ═══════════════════════════════════════════════════════════════════════════════
def generate_certificates() -> None:
    """Generate self-signed TLS certificates for HTTPS exercise."""
    print_step(4, "Generating TLS certificates")
    
    project_root = Path(__file__).parent.parent
    tls_dir = project_root / "docker" / "configs" / "tls"
    tls_dir.mkdir(parents=True, exist_ok=True)
    
    cert_path = tls_dir / "server.crt"
    key_path = tls_dir / "server.key"
    
    if cert_path.exists() and key_path.exists():
        print("  ✓ Certificates already exist")
        return
    
    if not shutil.which("openssl"):
        print("  ✗ OpenSSL not found - skipping certificate generation")
        print("    Certificates will be generated on first use")
        return
    
    cmd = [
        "openssl", "req",
        "-x509",
        "-newkey", "rsa:2048",
        "-nodes",
        "-keyout", str(key_path),
        "-out", str(cert_path),
        "-days", "365",
        "-subj", "/C=RO/O=ASE-CSIE/OU=Computer Networks/CN=lab.network.local",
        "-addext", "subjectAltName=DNS:lab.network.local,IP:127.0.0.1"
    ]
    
    if run_command(cmd, "Generate self-signed certificate"):
        print(f"    Certificate: {cert_path}")
        print(f"    Private key: {key_path}")



# ═══════════════════════════════════════════════════════════════════════════════
# CONTAINER_MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════
def build_docker_images() -> None:
    """Pre-build Docker images for the laboratory."""
    print_step(5, "Building Docker images")
    
    project_root = Path(__file__).parent.parent
    docker_dir = project_root / "docker"
    
    if not (docker_dir / "docker-compose.yml").exists():
        print("  ✗ docker-compose.yml not found")
        return
    
    print("  Building images (this may take a few minutes)...")
    
    result = subprocess.run(
        ["docker", "compose", "build"],
        cwd=docker_dir,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("  ✓ Docker images built successfully")
    else:
        print("  ✗ Build failed - images will be built on first run")
        if result.stderr:
            print(f"    Error: {result.stderr[:200]}")



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def print_next_steps() -> None:
    """Print next steps for the user."""
    print_header("Setup Complete - Next Steps")
    
    print("""
1. Verify the environment:
   python setup/verify_environment.py

2. Start the laboratory:
   python scripts/start_lab.py

3. Access services:
   - Web server: http://localhost:8000
   - Portainer:  https://localhost:9443

4. Run exercises:
   See README.md for detailed instructions

For troubleshooting, see docs/troubleshooting.md
""")



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    print_header("Week 10 Laboratory Setup")
    print("NETWORKING class - ASE, Informatics | by Revolvix")
    
    print(f"\nPlatform: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version.split()[0]}")
    
    # Install Python packages
    check_python_packages()
    
    # Check Docker
    docker_ok = check_docker()
    
    # Create directories
    create_directories()
    
    # Generate certificates
    generate_certificates()
    
    # Build Docker images (only if Docker is available)
    if docker_ok:
        build_docker_images()
    
    # Print next steps
    print_next_steps()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
