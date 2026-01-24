#!/usr/bin/env python3
"""
Packet Capture Helper
NETWORKING class - ASE, Informatics | by Revolvix

Assists with capturing network traffic for protocol analysis.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import subprocess
import sys
import signal
import os
import argparse
from pathlib import Path
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.logger import setup_logger, get_timestamp

logger = setup_logger("capture")



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def find_capture_tool() -> tuple:
    """
    Find an available packet capture tool.
    
    Returns:
        Tuple of (tool_name, tool_path) or (None, None)
    """
    import shutil
    
    tools = [
        ("tcpdump", "tcpdump"),
        ("tshark", "tshark"),
        ("dumpcap", "dumpcap"),
    ]
    
    for name, cmd in tools:
        path = shutil.which(cmd)
        if path:
            return name, path
    
    return None, None



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def list_interfaces(tool: str, tool_path: str) -> list:
    """List available network interfaces."""
    try:
        if tool == "tcpdump":
            result = subprocess.run(
                [tool_path, "-D"],
                capture_output=True,
                text=True
            )
        elif tool in ("tshark", "dumpcap"):
            result = subprocess.run(
                [tool_path, "-D"],
                capture_output=True,
                text=True
            )
        else:
            return []
        
        return result.stdout.strip().split("\n")
    except Exception as e:
        logger.error(f"Failed to list interfaces: {e}")
        return []



# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
def start_capture(tool: str, tool_path: str, interface: str, 
                  output_file: Path, port: int = None,
                  duration: int = None) -> subprocess.Popen:
    """
    Start packet capture.
    
    Args:
        tool: Capture tool name
        tool_path: Path to capture tool
        interface: Network interface
        output_file: Output pcap file path
        port: Optional port filter
        duration: Optional capture duration in seconds
    
    Returns:
        Popen object for the capture process
    """
    cmd = [tool_path]
    
    if tool == "tcpdump":
        cmd.extend(["-i", interface, "-w", str(output_file)])
        if port:
            cmd.extend(["port", str(port)])
        if duration:
            cmd.extend(["-G", str(duration), "-W", "1"])
    
    elif tool in ("tshark", "dumpcap"):
        cmd.extend(["-i", interface, "-w", str(output_file)])
        if port:
            cmd.extend(["-f", f"port {port}"])
        if duration:
            cmd.extend(["-a", f"duration:{duration}"])
    
    logger.info(f"Starting capture: {' '.join(cmd)}")
    
    return subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(
        description="Capture network traffic for protocol analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python capture_traffic.py --list                    # List interfaces
  python capture_traffic.py -i any                    # Capture on all interfaces
  python capture_traffic.py -i lo --port 5400         # Capture TEXT protocol
  python capture_traffic.py -i any --duration 60      # Capture for 60 seconds

Default output: pcap/week4_<timestamp>.pcap
        """
    )
    
    parser.add_argument("--list", "-l", action="store_true",
                        help="List available network interfaces")
    parser.add_argument("--interface", "-i", type=str, default="any",
                        help="Network interface to capture on (default: any)")
    parser.add_argument("--output", "-o", type=str,
                        help="Output pcap file path")
    parser.add_argument("--port", "-p", type=int,
                        help="Filter by port number")
    parser.add_argument("--duration", "-d", type=int,
                        help="Capture duration in seconds")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Verbose output")
    
    args = parser.parse_args()
    
    # Find capture tool
    tool, tool_path = find_capture_tool()
    
    if not tool:
        logger.error("No packet capture tool found!")
        logger.info("Install one of: tcpdump, tshark, or Wireshark")
        logger.info("  Ubuntu/WSL: sudo apt install tcpdump tshark")
        logger.info("  Windows: Install Wireshark from wireshark.org")
        return 1
    
    logger.info(f"Using capture tool: {tool} ({tool_path})")
    
    # List interfaces mode
    if args.list:
        logger.info("")
        logger.info("Available network interfaces:")
        for iface in list_interfaces(tool, tool_path):
            print(f"  {iface}")
        return 0
    
    # Determine output file
    pcap_dir = PROJECT_ROOT / "pcap"
    pcap_dir.mkdir(exist_ok=True)
    
    if args.output:
        output_file = Path(args.output)
    else:
        timestamp = get_timestamp()
        output_file = pcap_dir / f"week4_{timestamp}.pcap"
    
    # Check for root/admin (required for packet capture)
    if os.geteuid() != 0 and tool == "tcpdump":
        logger.warning("Packet capture usually requires root privileges")
        logger.info("Try: sudo python scripts/capture_traffic.py ...")
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("Starting Packet Capture")
    logger.info("=" * 60)
    logger.info(f"  Interface: {args.interface}")
    logger.info(f"  Output:    {output_file}")
    if args.port:
        logger.info(f"  Port:      {args.port}")
    if args.duration:
        logger.info(f"  Duration:  {args.duration} seconds")
    logger.info("")
    logger.info("Press Ctrl+C to stop capture")
    logger.info("=" * 60)
    
    # Start capture
    process = start_capture(
        tool, tool_path, args.interface, output_file,
        port=args.port, duration=args.duration
    )
    
    # Handle interrupt


# ═══════════════════════════════════════════════════════════════════════════════
# DATA_PROCESSING
# ═══════════════════════════════════════════════════════════════════════════════
    def signal_handler(signum, frame):
        logger.info("")
        logger.info("Stopping capture...")
        process.terminate()
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Wait for capture to complete
    try:
        process.wait()
    except Exception:
        process.terminate()
    
    # Report results
    if output_file.exists():
        size = output_file.stat().st_size
        logger.info("")
        logger.info("=" * 60)
        logger.info("Capture complete!")
        logger.info(f"  File: {output_file}")
        logger.info(f"  Size: {size:,} bytes")
        logger.info("")
        logger.info("To analyse with Wireshark:")
        logger.info(f"  wireshark {output_file}")
        logger.info("")
        logger.info("To view with tshark:")
        logger.info(f"  tshark -r {output_file} -V")
        logger.info("=" * 60)
    else:
        logger.error("Capture file was not created")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
