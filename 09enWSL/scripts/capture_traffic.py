#!/usr/bin/env python3
"""
Traffic Capture Helper for Week 9 Laboratory
NETWORKING class - ASE, Informatics | by Revolvix

This script supports packet capture for FTP traffic analysis.
It can use either tcpdump (in Docker/WSL) or guide Wireshark usage.

Usage:
    python scripts/capture_traffic.py                    # Interactive mode
    python scripts/capture_traffic.py --interface eth0  # Specify interface
    python scripts/capture_traffic.py --output my.pcap  # Custom output
    python scripts/capture_traffic.py --duration 30     # Capture for 30s
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.logger import setup_logger, print_banner

logger = setup_logger("capture_traffic")

DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "pcap"
DEFAULT_INTERFACE = "any"
FTP_PORT = 2121



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def get_timestamp() -> str:
    """Get timestamp string for filename."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_tcpdump() -> bool:
    """Check if tcpdump is available."""
    try:
        result = subprocess.run(
            ["tcpdump", "--version"],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError):
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_tshark() -> bool:
    """Check if tshark is available."""
    try:
        result = subprocess.run(
            ["tshark", "--version"],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError):
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def list_interfaces() -> list:
    """List available network interfaces."""
    interfaces = []
    
    # Try tcpdump -D
    try:
        result = subprocess.run(
            ["tcpdump", "-D"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                if line:
                    interfaces.append(line)
    except subprocess.SubprocessError:
        pass
    
    return interfaces



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def capture_with_tcpdump(
    interface: str,
    output_file: Path,
    port: int = FTP_PORT,
    duration: int = 0
) -> bool:
    """
    Capture traffic using tcpdump.
    
    Args:
        interface: Network interface to capture on
        output_file: Output pcap file path
        port: Port to filter on
        duration: Capture duration (0 = until Ctrl+C)
    
    Returns:
        True if capture was successful
    """
    cmd = [
        "tcpdump",
        "-i", interface,
        "-w", str(output_file),
        f"port {port}"
    ]
    
    if duration > 0:
        cmd.extend(["-G", str(duration), "-W", "1"])
    
    logger.info(f"Starting capture on {interface}...")
    logger.info(f"Filter: port {port}")
    logger.info(f"Output: {output_file}")
    
    if duration == 0:
        logger.info("Press Ctrl+C to stop capture")
    else:
        logger.info(f"Capturing for {duration} seconds...")
    
    print()
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        if duration > 0:
            process.wait(timeout=duration + 5)
        else:
            process.wait()
        
        return True
        
    except KeyboardInterrupt:
        logger.info("\nCapture stopped by user")
        return True
        
    except subprocess.SubprocessError as e:
        logger.error(f"Capture failed: {e}")
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def capture_with_tshark(
    interface: str,
    output_file: Path,
    port: int = FTP_PORT,
    duration: int = 0
) -> bool:
    """
    Capture traffic using tshark.
    
    Args:
        interface: Network interface to capture on
        output_file: Output pcap file path
        port: Port to filter on
        duration: Capture duration (0 = until Ctrl+C)
    
    Returns:
        True if capture was successful
    """
    cmd = [
        "tshark",
        "-i", interface,
        "-w", str(output_file),
        "-f", f"tcp port {port}"
    ]
    
    if duration > 0:
        cmd.extend(["-a", f"duration:{duration}"])
    
    logger.info(f"Starting capture on {interface}...")
    logger.info(f"Filter: tcp port {port}")
    logger.info(f"Output: {output_file}")
    
    if duration == 0:
        logger.info("Press Ctrl+C to stop capture")
    else:
        logger.info(f"Capturing for {duration} seconds...")
    
    print()
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        if duration > 0:
            process.wait(timeout=duration + 5)
        else:
            process.wait()
        
        return True
        
    except KeyboardInterrupt:
        logger.info("\nCapture stopped by user")
        return True
        
    except subprocess.SubprocessError as e:
        logger.error(f"Capture failed: {e}")
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def print_wireshark_instructions() -> None:
    """Print instructions for using Wireshark on Windows."""
    print()
    print("=" * 60)
    print("Wireshark Capture Instructions (Windows)")
    print("=" * 60)
    print()
    print("1. Open Wireshark")
    print()
    print("2. Select the appropriate interface:")
    print("   - For Docker Desktop: 'vEthernet (WSL)' or similar")
    print("   - For localhost: 'Loopback: lo' or 'Adapter for loopback'")
    print("   - For WSL2: May need to use 'any' in WSL terminal")
    print()
    print("3. Apply capture filter:")
    print(f"   tcp port {FTP_PORT}")
    print()
    print("4. Start capture (green shark fin button)")
    print()
    print("5. Run your FTP commands in another terminal")
    print()
    print("6. Stop capture and save as .pcap file to:")
    print(f"   {DEFAULT_OUTPUT_DIR}")
    print()
    print("Useful display filters:")
    print(f"   tcp.port == {FTP_PORT}")
    print("   tcp.flags.syn == 1")
    print("   tcp.len > 0")
    print("   frame contains \"FTPC\"")
    print()
    print("=" * 60)



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def analyse_capture(pcap_file: Path) -> None:
    """Analyse a captured pcap file."""
    if not pcap_file.exists():
        logger.error(f"File not found: {pcap_file}")
        return
    
    logger.info(f"Analysing: {pcap_file}")
    print()
    
    # Try tshark for analysis
    if check_tshark():
        # Packet count
        result = subprocess.run(
            ["tshark", "-r", str(pcap_file), "-T", "fields", "-e", "frame.number"],
            capture_output=True,
            text=True
        )
        packet_count = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
        
        print(f"Total packets: {packet_count}")
        print()
        
        # Summary
        print("First 20 packets:")
        print("-" * 60)
        subprocess.run(
            ["tshark", "-r", str(pcap_file), "-c", "20"],
            text=True
        )
        print("-" * 60)
        
        # Statistics
        print()
        print("Protocol hierarchy:")
        subprocess.run(
            ["tshark", "-r", str(pcap_file), "-z", "io,phs", "-q"],
            text=True
        )
    else:
        logger.warning("tshark not found, basic analysis only")
        print(f"File size: {pcap_file.stat().st_size} bytes")



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Traffic Capture Helper for Week 9",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/capture_traffic.py                    # Interactive mode
  python scripts/capture_traffic.py --list             # List interfaces
  python scripts/capture_traffic.py -i eth0 -d 30     # Capture for 30s
  python scripts/capture_traffic.py --analyse my.pcap # Analyse capture
  python scripts/capture_traffic.py --wireshark       # Show Wireshark guide
        """
    )
    parser.add_argument(
        "-i", "--interface",
        default=DEFAULT_INTERFACE,
        help=f"Network interface (default: {DEFAULT_INTERFACE})"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output file path (default: pcap/week9_TIMESTAMP.pcap)"
    )
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=FTP_PORT,
        help=f"Port to capture (default: {FTP_PORT})"
    )
    parser.add_argument(
        "-d", "--duration",
        type=int,
        default=0,
        help="Capture duration in seconds (0 = until Ctrl+C)"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available interfaces"
    )
    parser.add_argument(
        "--analyse",
        type=Path,
        metavar="FILE",
        help="Analyse an existing pcap file"
    )
    parser.add_argument(
        "--wireshark",
        action="store_true",
        help="Show Wireshark instructions (for Windows)"
    )
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Show Wireshark instructions
    if args.wireshark:
        print_wireshark_instructions()
        return 0
    
    # List interfaces
    if args.list:
        print_banner("Available Interfaces")
        interfaces = list_interfaces()
        if interfaces:
            for iface in interfaces:
                print(f"  {iface}")
        else:
            print("  Could not list interfaces (try with sudo)")
        return 0
    
    # Analyse existing capture
    if args.analyse:
        print_banner("Capture Analysis")
        analyse_capture(args.analyse)
        return 0
    
    # Start capture
    print_banner("Traffic Capture")
    
    # Check tools
    has_tcpdump = check_tcpdump()
    has_tshark = check_tshark()
    
    if not has_tcpdump and not has_tshark:
        logger.warning("Neither tcpdump nor tshark found")
        print_wireshark_instructions()
        return 1
    
    # Set output file
    if args.output:
        output_file = args.output
    else:
        output_file = DEFAULT_OUTPUT_DIR / f"week9_{get_timestamp()}.pcap"
    
    # Capture
    if has_tshark:
        success = capture_with_tshark(
            args.interface,
            output_file,
            args.port,
            args.duration
        )
    else:
        success = capture_with_tcpdump(
            args.interface,
            output_file,
            args.port,
            args.duration
        )
    
    if success and output_file.exists():
        print()
        logger.info(f"Capture saved to: {output_file}")
        logger.info(f"File size: {output_file.stat().st_size} bytes")
        print()
        logger.info("To analyse: python scripts/capture_traffic.py --analyse " + str(output_file))
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
