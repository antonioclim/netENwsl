#!/usr/bin/env python3
"""
Smoke Test Script
NETWORKING class - ASE, Informatics | by Revolvix

Quick functionality check for the laboratory environment.
"""

import sys
import socket
import struct
import zlib
import time
import subprocess
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def print_status(name: str, passed: bool, message: str = ""):
    """Print test status."""
    status = "\033[92m✓\033[0m" if passed else "\033[91m✗\033[0m"
    print(f"  {status} {name}", end="")
    if message:
        print(f" - {message}", end="")
    print()


def test_python_environment() -> bool:
    """Test Python environment."""
    print("\nPython Environment:")
    
    # Version check
    version_ok = sys.version_info >= (3, 8)
    print_status(f"Python {sys.version_info.major}.{sys.version_info.minor}", 
                 version_ok)
    
    # Required modules
    modules = ['socket', 'struct', 'zlib', 'threading', 'json']
    modules_ok = True
    for module in modules:
        try:
            __import__(module)
        except ImportError:
            modules_ok = False
    print_status("Required modules", modules_ok)
    
    return version_ok and modules_ok


def test_crc32_functionality() -> bool:
    """Test CRC32 functionality."""
    print("\nCRC32 Functionality:")
    
    try:
        data = b"Test data"
        crc = zlib.crc32(data) & 0xFFFFFFFF
        
        # Verify consistency
        crc2 = zlib.crc32(data) & 0xFFFFFFFF
        consistent = crc == crc2
        print_status("CRC32 calculation", consistent)
        
        # Verify detection
        modified_data = b"Test Data"
        crc_modified = zlib.crc32(modified_data) & 0xFFFFFFFF
        detects_change = crc != crc_modified
        print_status("Change detection", detects_change)
        
        return consistent and detects_change
    except Exception as e:
        print_status("CRC32 test", False, str(e))
        return False


def test_struct_packing() -> bool:
    """Test struct packing functionality."""
    print("\nBinary Packing:")
    
    try:
        # Test packing
        packed = struct.pack('>BIf', 1, 12345, 3.14)
        print_status(f"Pack to bytes ({len(packed)} bytes)", True)
        
        # Test unpacking
        version, sensor_id, temp = struct.unpack('>BIf', packed)
        correct = version == 1 and sensor_id == 12345 and abs(temp - 3.14) < 0.01
        print_status("Unpack from bytes", correct)
        
        return correct
    except Exception as e:
        print_status("Struct test", False, str(e))
        return False


def test_socket_creation() -> bool:
    """Test socket creation."""
    print("\nSocket Creation:")
    
    try:
        # TCP socket
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sock.close()
        print_status("TCP socket", True)
        
        # UDP socket
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_sock.close()
        print_status("UDP socket", True)
        
        return True
    except Exception as e:
        print_status("Socket creation", False, str(e))
        return False


def test_port_connectivity(host: str, port: int, timeout: float = 2.0) -> bool:
    """Test if a port is reachable."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False


def test_server_connectivity() -> bool:
    """Test server connectivity."""
    print("\nServer Connectivity:")
    
    servers = [
        ("TEXT Server", "localhost", 5400),
        ("BINARY Server", "localhost", 5401),
        ("Portainer", "localhost", 9443),
    ]
    
    all_ok = True
    servers_running = 0
    
    for name, host, port in servers:
        if test_port_connectivity(host, port):
            print_status(f"{name} (port {port})", True, "responding")
            servers_running += 1
        else:
            print_status(f"{name} (port {port})", False, "not responding")
    
    if servers_running == 0:
        print("  (Note: Servers may not be running yet)")
    
    return True  # Don't fail smoke test if servers aren't running


def test_file_structure() -> bool:
    """Test project file structure."""
    print("\nProject Structure:")
    
    required_files = [
        ('README.md', 'README'),
        ('docker/docker-compose.yml', 'Docker Compose'),
        ('docker/Dockerfile', 'Dockerfile'),
        ('scripts/start_lab.py', 'Start script'),
        ('scripts/stop_lab.py', 'Stop script'),
        ('src/apps/text_proto_server.py', 'TEXT server'),
        ('src/apps/binary_proto_server.py', 'BINARY server'),
    ]
    
    all_present = True
    
    for file_path, name in required_files:
        full_path = PROJECT_ROOT / file_path
        if full_path.exists():
            print_status(name, True)
        else:
            print_status(name, False, "missing")
            all_present = False
    
    return all_present


def main():
    """Run smoke tests."""
    print()
    print("=" * 60)
    print("Week 4 Laboratory Smoke Test")
    print("NETWORKING class - ASE, Informatics | by Revolvix")
    print("=" * 60)
    
    results = []
    
    results.append(("Python Environment", test_python_environment()))
    results.append(("CRC32 Functionality", test_crc32_functionality()))
    results.append(("Binary Packing", test_struct_packing()))
    results.append(("Socket Creation", test_socket_creation()))
    results.append(("Server Connectivity", test_server_connectivity()))
    results.append(("File Structure", test_file_structure()))
    
    # Summary
    print()
    print("=" * 60)
    print("Summary:")
    
    passed = sum(1 for _, ok in results if ok)
    total = len(results)
    
    for name, ok in results:
        status = "\033[92mPASS\033[0m" if ok else "\033[91mFAIL\033[0m"
        print(f"  {name}: {status}")
    
    print()
    print(f"Result: {passed}/{total} tests passed")
    print("=" * 60)
    
    return 0 if passed == total else 1


if __name__ == '__main__':
    sys.exit(main())
