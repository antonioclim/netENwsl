#!/usr/bin/env python3
"""
Traffic Capture Helper
NETWORKING class - ASE, CSIE Bucharest | by ing. dr. Antonio Clim

Wrapper for tcpdump/tshark to simplify packet capture for laboratory exercises.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import argparse
import subprocess
import sys
import signal
import os
from pathlib import Path
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.logger import setup_logger

logger = setup_logger("capture")



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def find_capture_tool() -> tuple:
    """Find available capture tool."""
    tools = [
        ("tcpdump", ["tcpdump", "--version"]),
        ("tshark", ["tshark", "--version"]),
    ]
    
    for name, cmd in tools:
        try:
            result = subprocess.run(cmd, capture_output=True)
            if result.returncode == 0:
                return name, name
        except FileNotFoundError:
            continue
    
    # Try in WSL
    try:
        result = subprocess.run(["wsl", "tcpdump", "--version"], capture_output=True)
        if result.returncode == 0:
            return "tcpdump", "wsl tcpdump"
    except FileNotFoundError:
        pass
    
    return None, None



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def generate_output_filename(prefix: str = "capture") -> str:
    """Generate timestamped output filename."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.pcap"



# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
def run_capture(
    tool: str,
    interface: str,
    output: str,
    filter_expr: str = "",
    packet_count: int = 0,
    duration: int = 0
) -> int:
    """
    Run packet capture.
    
    Args:
        tool: Capture tool command
        interface: Network interface
        output: Output file path
        filter_expr: BPF filter expression
        packet_count: Stop after N packets (0 = unlimited)
        duration: Stop after N seconds (0 = unlimited)
    
    Returns:
        Exit code
    """
    # Build command
    if "tcpdump" in tool:
        cmd = tool.split() + ["-i", interface, "-w", output]
        if packet_count > 0:
            cmd.extend(["-c", str(packet_count)])
        if filter_expr:
            cmd.append(filter_expr)
    else:  # tshark
        cmd = tool.split() + ["-i", interface, "-w", output]
        if packet_count > 0:
            cmd.extend(["-c", str(packet_count)])
        if duration > 0:
            cmd.extend(["-a", f"duration:{duration}"])
        if filter_expr:
            cmd.extend(["-f", filter_expr])
    
    logger.info(f"Starting capture: {' '.join(cmd)}")
    logger.info(f"Output file: {output}")
    logger.info("Press Ctrl+C to stop capture")
    print()
    
    try:
        # Run capture
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # Handle duration timeout
        if duration > 0 and "tcpdump" in tool:
            try:
                proc.wait(timeout=duration)
            except subprocess.TimeoutExpired:
                proc.send_signal(signal.SIGINT)
                proc.wait(timeout=2)
        else:
            # Wait for Ctrl+C
            proc.wait()
        
        return proc.returncode
        
    except KeyboardInterrupt:
        logger.info("Capture stopped by user")
        if proc:
            proc.send_signal(signal.SIGINT)
            proc.wait(timeout=2)
        return 0



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def analyse_capture(filepath: str, display_filter: str = "") -> None:
    """Analyse captured packets."""
    print()
    print("=" * 60)
    print("  Capture Analysis")
    print("=" * 60)
    print()
    
    # Try tshark for analysis
    cmd = ["tshark", "-r", filepath]
    if display_filter:
        cmd.extend(["-Y", display_filter])
    cmd.extend(["-T", "fields",
                "-e", "frame.number",
                "-e", "ip.src",
                "-e", "ip.dst",
                "-e", "tcp.srcport",
                "-e", "tcp.dstport",
                "-e", "tcp.flags.str",
                "-E", "header=y"])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(result.stdout)
        else:
            logger.warning("Could not analyse with tshark")
            print(result.stderr)
    except FileNotFoundError:
        logger.warning("tshark not found - install Wireshark for analysis")



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Network Traffic Capture Helper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Capture TCP traffic on loopback
  python scripts/capture_traffic.py -i lo -f "tcp port 9090" -o pcap/tcp.pcap
  
  # Capture with packet limit
  python scripts/capture_traffic.py -i lo -c 100 -o pcap/sample.pcap
  
  # Capture for 30 seconds
  python scripts/capture_traffic.py -i lo -d 30 -o pcap/timed.pcap
  
  # List available interfaces
  python scripts/capture_traffic.py --list-interfaces

Common BPF filters:
  tcp port 9090       - TCP traffic on port 9090
  udp port 9091       - UDP traffic on port 9091
  host 127.0.0.1      - Traffic to/from localhost
  tcp and port 9090   - TCP only on port 9090
        """
    )
    parser.add_argument(
        "--interface", "-i",
        default="lo",
        help="Network interface to capture from (default: lo)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output PCAP file (default: auto-generated)"
    )
    parser.add_argument(
        "--filter", "-f",
        default="",
        help="BPF filter expression"
    )
    parser.add_argument(
        "--count", "-c",
        type=int,
        default=0,
        help="Stop after N packets (0 = unlimited)"
    )
    parser.add_argument(
        "--duration", "-d",
        type=int,
        default=0,
        help="Stop after N seconds (0 = unlimited)"
    )
    parser.add_argument(
        "--analyse", "-a",
        action="store_true",
        help="Analyse capture after stopping"
    )
    parser.add_argument(
        "--list-interfaces",
        action="store_true",
        help="List available network interfaces"
    )
    
    args = parser.parse_args()
    
    # List interfaces
    if args.list_interfaces:
        print("Available interfaces:")
        try:
            result = subprocess.run(["ip", "link", "show"], 
                                  capture_output=True, text=True)
            print(result.stdout)
        except FileNotFoundError:
            # Windows
            result = subprocess.run(["ipconfig"], capture_output=True, text=True)
            print(result.stdout)
        return 0
    
    # Find capture tool
    tool_name, tool_cmd = find_capture_tool()
    if not tool_name:
        logger.error("No capture tool found (tcpdump or tshark)")
        logger.error("Install Wireshark or run in WSL/Docker")
        return 1
    
    logger.info(f"Using capture tool: {tool_name}")
    
    # Generate output filename if not specified
    output = args.output or str(PROJECT_ROOT / "pcap" / generate_output_filename())
    
    # Ensure output directory exists
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    
    # Run capture
    result = run_capture(
        tool_cmd,
        args.interface,
        output,
        args.filter,
        args.count,
        args.duration
    )
    
    # Analyse if requested
    if args.analyse and Path(output).exists():
        analyse_capture(output, args.filter.replace("port", "tcp.port or udp.port"))
    
    print()
    logger.info(f"Capture saved to: {output}")
    logger.info("Open with Wireshark for detailed analysis")
    
    return result


if __name__ == "__main__":
    sys.exit(main())
