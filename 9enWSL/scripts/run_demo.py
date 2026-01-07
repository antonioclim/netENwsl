#!/usr/bin/env python3
"""
Demonstration Script for Week 9 Laboratory
NETWORKING class - ASE, Informatics | by Revolvix

This script runs automated demonstrations of the FTP protocol concepts
covered in Week 9: Session Layer (L5) and Presentation Layer (L6).

Available demos:
- endianness: Binary encoding and byte order
- ftp_session: FTP session lifecycle
- multi_client: Concurrent client connections
- binary_protocol: Custom binary protocol headers

Usage:
    python scripts/run_demo.py                    # List available demos
    python scripts/run_demo.py endianness         # Run specific demo
    python scripts/run_demo.py --all              # Run all demos
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.logger import setup_logger, print_banner
from scripts.utils.network_utils import check_port, wait_for_port

logger = setup_logger("run_demo")


# =============================================================================
# Demo Definitions
# =============================================================================

DEMOS = {
    "endianness": {
        "title": "Endianness and Binary Framing",
        "description": "Demonstrates big-endian vs little-endian encoding",
        "requires_server": False
    },
    "ftp_session": {
        "title": "FTP Session Lifecycle",
        "description": "Shows authentication, commands, and session state",
        "requires_server": True
    },
    "multi_client": {
        "title": "Multi-Client Testing",
        "description": "Demonstrates concurrent FTP client connections",
        "requires_server": True
    },
    "binary_protocol": {
        "title": "Binary Protocol Headers",
        "description": "Shows custom protocol header structure",
        "requires_server": False
    }
}


# =============================================================================
# Demo Implementations
# =============================================================================

def demo_endianness() -> bool:
    """
    Demonstrate endianness concepts.
    """
    print_banner("Demo: Endianness and Binary Framing")
    
    exercise_path = PROJECT_ROOT / "src" / "exercises" / "ex_9_01_endianness.py"
    
    if not exercise_path.exists():
        logger.error(f"Exercise not found: {exercise_path}")
        return False
    
    logger.info("Running endianness demonstration...")
    print()
    
    try:
        result = subprocess.run(
            [sys.executable, str(exercise_path), "--demo", "--selftest"],
            cwd=PROJECT_ROOT,
            timeout=30
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        logger.error("Demo timed out")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Demo failed: {e}")
        return False


def demo_ftp_session() -> bool:
    """
    Demonstrate FTP session lifecycle.
    """
    print_banner("Demo: FTP Session Lifecycle")
    
    # Check if server is running
    if not check_port("localhost", 2121):
        logger.warning("FTP server not running on port 2121")
        logger.info("Starting server with Docker...")
        
        # Try to start Docker containers
        subprocess.run(
            ["docker", "compose", "-f", str(PROJECT_ROOT / "docker" / "docker-compose.yml"), "up", "-d"],
            capture_output=True
        )
        
        if not wait_for_port("localhost", 2121, timeout=30):
            logger.error("Could not start FTP server")
            logger.info("Run 'python scripts/start_lab.py' first")
            return False
    
    logger.info("FTP server is available")
    print()
    
    # Run client demo
    client_path = PROJECT_ROOT / "src" / "exercises" / "ftp_demo_client.py"
    
    if not client_path.exists():
        logger.error(f"Client not found: {client_path}")
        return False
    
    commands = ["list"]
    
    for cmd in commands:
        logger.info(f"Executing: {cmd}")
        
        try:
            result = subprocess.run(
                [
                    sys.executable, str(client_path),
                    "--host", "localhost",
                    "--port", "2121",
                    "--user", "test",
                    "--password", "12345",
                    cmd
                ],
                cwd=PROJECT_ROOT,
                timeout=30
            )
            print()
        except subprocess.SubprocessError as e:
            logger.error(f"Command failed: {e}")
            return False
    
    print()
    print("=" * 60)
    print("Session Lifecycle Summary")
    print("=" * 60)
    print()
    print("1. Connection established (TCP handshake)")
    print("2. Server sends welcome banner (220)")
    print("3. Client authenticates (USER/PASS)")
    print("4. Session created (230 Logged in)")
    print("5. Commands executed within session")
    print("6. Session closed (QUIT)")
    print()
    print("This demonstrates L5 (Session Layer) concepts:")
    print("  - Session establishment and termination")
    print("  - Authentication state management")
    print("  - Command-response dialogue")
    print()
    print("=" * 60)
    
    return True


def demo_multi_client() -> bool:
    """
    Demonstrate multi-client testing.
    """
    print_banner("Demo: Multi-Client Testing")
    
    logger.info("This demo uses Docker Compose to orchestrate multiple clients")
    print()
    
    compose_file = PROJECT_ROOT / "docker" / "docker-compose.yml"
    
    # Show the architecture
    print("Architecture:")
    print()
    print("  ┌─────────────────┐")
    print("  │   ftp-server    │  Port 2121")
    print("  │   (pyftpdlib)   │")
    print("  └────────┬────────┘")
    print("           │")
    print("    ┌──────┴──────┐")
    print("    │             │")
    print("┌───┴───┐   ┌───┴───┐")
    print("│client1│   │client2│")
    print("└───────┘   └───────┘")
    print()
    
    # Run docker compose
    logger.info("Starting multi-client test...")
    print()
    
    try:
        # Restart containers to ensure clean state
        subprocess.run(
            ["docker", "compose", "-f", str(compose_file), "down"],
            cwd=PROJECT_ROOT / "docker",
            capture_output=True
        )
        
        result = subprocess.run(
            ["docker", "compose", "-f", str(compose_file), "up", "--abort-on-container-exit"],
            cwd=PROJECT_ROOT / "docker",
            timeout=60
        )
        
        print()
        
        if result.returncode == 0:
            logger.info("Multi-client test completed successfully")
        else:
            logger.warning("Some clients may have exited with errors")
        
        return True
        
    except subprocess.TimeoutExpired:
        logger.error("Demo timed out")
        return False
    except subprocess.SubprocessError as e:
        logger.error(f"Demo failed: {e}")
        return False
    finally:
        # Restart in detached mode
        subprocess.run(
            ["docker", "compose", "-f", str(compose_file), "up", "-d"],
            cwd=PROJECT_ROOT / "docker",
            capture_output=True
        )


def demo_binary_protocol() -> bool:
    """
    Demonstrate binary protocol structure.
    """
    print_banner("Demo: Binary Protocol Headers")
    
    print("Pseudo-FTP Binary Protocol Structure")
    print("=" * 60)
    print()
    print("HEADER (16 bytes):")
    print("┌────────────┬──────────┬──────────┬────────────┐")
    print("│ Magic (4B) │ Len (4B) │ CRC (4B) │ Flags (4B) │")
    print("│ 0x46545043 │ Big End. │ Big End. │ Bit0=Compr │")
    print("└────────────┴──────────┴──────────┴────────────┘")
    print()
    print("Magic bytes: 'FTPC' (0x46 0x54 0x50 0x43)")
    print()
    
    # Demonstrate with Python
    print("Python struct example:")
    print("-" * 40)
    print()
    
    import struct
    import zlib
    
    # Pack a sample header
    magic = b"FTPC"
    payload = b"Hello, FTP!"
    length = len(payload)
    crc = zlib.crc32(payload) & 0xFFFFFFFF
    flags = 0
    
    header = struct.pack(">4sIII", magic, length, crc, flags)
    
    print(f"Payload: {payload!r}")
    print(f"Length:  {length}")
    print(f"CRC-32:  0x{crc:08X}")
    print(f"Flags:   {flags}")
    print()
    print("Header bytes (big-endian):")
    print("  ", " ".join(f"{b:02X}" for b in header))
    print()
    
    # Show interpretation
    print("Interpretation:")
    print(f"  Bytes 0-3:   {' '.join(f'{b:02X}' for b in header[0:4])} -> Magic 'FTPC'")
    print(f"  Bytes 4-7:   {' '.join(f'{b:02X}' for b in header[4:8])} -> Length {length}")
    print(f"  Bytes 8-11:  {' '.join(f'{b:02X}' for b in header[8:12])} -> CRC-32")
    print(f"  Bytes 12-15: {' '.join(f'{b:02X}' for b in header[12:16])} -> Flags")
    print()
    
    # Unpack
    unpacked = struct.unpack(">4sIII", header)
    print("Unpacked values:")
    print(f"  magic  = {unpacked[0]!r}")
    print(f"  length = {unpacked[1]}")
    print(f"  crc32  = 0x{unpacked[2]:08X}")
    print(f"  flags  = {unpacked[3]}")
    print()
    
    print("=" * 60)
    print()
    print("This demonstrates L6 (Presentation Layer) concepts:")
    print("  - Data serialisation (struct.pack)")
    print("  - Network byte order (big-endian)")
    print("  - Integrity verification (CRC-32)")
    print("  - Framing (length field for message boundaries)")
    print()
    
    return True


# =============================================================================
# Demo Runner
# =============================================================================

DEMO_FUNCTIONS = {
    "endianness": demo_endianness,
    "ftp_session": demo_ftp_session,
    "multi_client": demo_multi_client,
    "binary_protocol": demo_binary_protocol
}


def list_demos() -> None:
    """List all available demos."""
    print()
    print("Available Demonstrations:")
    print("=" * 60)
    print()
    
    for name, info in DEMOS.items():
        req = " (requires server)" if info["requires_server"] else ""
        print(f"  {name:20} - {info['title']}{req}")
        print(f"  {' ':20}   {info['description']}")
        print()
    
    print("Usage:")
    print("  python scripts/run_demo.py <demo_name>")
    print("  python scripts/run_demo.py --all")
    print()


def run_demo(name: str) -> bool:
    """Run a specific demo by name."""
    if name not in DEMO_FUNCTIONS:
        logger.error(f"Unknown demo: {name}")
        return False
    
    return DEMO_FUNCTIONS[name]()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run Week 9 Laboratory Demonstrations",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "demo",
        nargs="?",
        choices=list(DEMOS.keys()),
        help="Demo to run"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all demos"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List available demos"
    )
    
    args = parser.parse_args()
    
    if args.list or (not args.demo and not args.all):
        list_demos()
        return 0
    
    if args.all:
        print_banner("Running All Demonstrations")
        
        success = True
        for name in DEMOS:
            print(f"\n{'#' * 60}")
            print(f"# Demo: {name}")
            print(f"{'#' * 60}\n")
            
            if not run_demo(name):
                success = False
            
            print()
            time.sleep(1)
        
        print_banner("All Demonstrations Complete")
        return 0 if success else 1
    
    if args.demo:
        return 0 if run_demo(args.demo) else 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
