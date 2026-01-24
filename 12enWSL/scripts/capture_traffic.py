#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# MODULE_DOCSTRING
# ═══════════════════════════════════════════════════════════════════════════════
"""
Traffic Capture Helper
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Assists with packet capture for protocol analysis using tcpdump or tshark.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import subprocess
import sys
import argparse
import time
import os
from pathlib import Path
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.logger import setup_colour_logger

logger = setup_colour_logger("capture")

# Default ports for Week 12
DEFAULT_PORTS = [1025, 6200, 6201, 6251]



# ═══════════════════════════════════════════════════════════════════════════════
# FIND_CAPTURE_TOOL_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def find_capture_tool() -> tuple[str, list[str]]:
    """
    Find available packet capture tool.
    
    Returns:
        Tuple of (tool_name, base_command)
    """
    import shutil
    
    # Try tcpdump first
    if shutil.which("tcpdump"):
        return "tcpdump", ["tcpdump"]
    
    # Try tshark
    if shutil.which("tshark"):
        return "tshark", ["tshark"]
    
    raise RuntimeError("No packet capture tool found. Install tcpdump or tshark.")



# ═══════════════════════════════════════════════════════════════════════════════
# BUILD_FILTER_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def build_filter(ports: list[int]) -> str:
    """
    Build a BPF filter expression for the specified ports.
    
    Args:
        ports: List of port numbers
    
    Returns:
        BPF filter string
    """
    port_filters = [f"port {p}" for p in ports]
    return " or ".join(port_filters)



# ═══════════════════════════════════════════════════════════════════════════════
# START_CAPTURE_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def start_capture(
    output_file: Path,
    interface: str = "any",
    ports: list[int] = None,
    duration: int = None,
) -> subprocess.Popen:
    """
    Start a packet capture.
    
    Args:
        output_file: Path to save the capture
        interface: Network interface to capture on
        ports: List of ports to filter (default: Week 12 ports)
        duration: Capture duration in seconds (None for unlimited)
    
    Returns:
        Subprocess handle for the capture process
    """
    if ports is None:
        ports = DEFAULT_PORTS
    
    tool_name, base_cmd = find_capture_tool()
    filter_expr = build_filter(ports)
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    if tool_name == "tcpdump":
        cmd = base_cmd + [
            "-i", interface,
            "-w", str(output_file),
            "-n",  # Don't resolve hostnames
            filter_expr
        ]
    else:  # tshark
        cmd = base_cmd + [
            "-i", interface,
            "-w", str(output_file),
            "-f", filter_expr
        ]
    
    logger.info(f"Starting capture with {tool_name}")
    logger.info(f"Interface: {interface}")
    logger.info(f"Filter: {filter_expr}")
    logger.info(f"Output: {output_file}")
    
    if duration:
        logger.info(f"Duration: {duration} seconds")
    
    # Start capture process
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    
    return process



# ═══════════════════════════════════════════════════════════════════════════════
# STOP_CAPTURE_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def stop_capture(process: subprocess.Popen) -> None:
    """Stop a running capture process."""
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()



# ═══════════════════════════════════════════════════════════════════════════════
# ANALYSE_CAPTURE_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def analyse_capture(pcap_file: Path, brief: bool = True) -> str:
    """
    Analyse a capture file.
    
    Args:
        pcap_file: Path to the capture file
        brief: If True, show summary. If False, show detailed output.
    
    Returns:
        Analysis output as string
    """
    import shutil
    
    if not pcap_file.exists():
        return f"Capture file not found: {pcap_file}"
    
    if shutil.which("tshark"):
        if brief:
            # Summary statistics
            cmd = ["tshark", "-r", str(pcap_file), "-q", "-z", "io,stat,0"]
        else:
            # Detailed packet list
            cmd = ["tshark", "-r", str(pcap_file)]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout
    
    if shutil.which("tcpdump"):
        cmd = ["tcpdump", "-r", str(pcap_file), "-n"]
        if brief:
            cmd.append("-c")
            cmd.append("50")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout
    
    return "No analysis tool available. Install tshark for analysis."



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Capture network traffic for Week 12 protocols"
    )
    parser.add_argument(
        "--interface", "-i",
        default="any",
        help="Network interface to capture on (default: any)"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output file path (default: pcap/week12_<timestamp>.pcap)"
    )
    parser.add_argument(
        "--ports", "-p",
        type=str,
        default="1025,6200,6201,6251",
        help="Comma-separated list of ports (default: 1025,6200,6201,6251)"
    )
    parser.add_argument(
        "--duration", "-d",
        type=int,
        help="Capture duration in seconds (default: unlimited, Ctrl+C to stop)"
    )
    parser.add_argument(
        "--analyse", "-a",
        type=Path,
        help="Analyse an existing capture file instead of capturing"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed analysis output"
    )
    
    args = parser.parse_args()
    
    # Analysis mode
    if args.analyse:
        logger.info(f"Analysing capture: {args.analyse}")
        output = analyse_capture(args.analyse, brief=not args.verbose)
        print(output)
        return 0
    
    # Capture mode
    ports = [int(p.strip()) for p in args.ports.split(",")]
    
    if args.output:
        output_file = args.output
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = PROJECT_ROOT / "pcap" / f"week12_{timestamp}.pcap"
    
    # Check for root/admin privileges
    if os.geteuid() != 0:
        logger.warning("Packet capture typically requires root privileges")
        logger.info("Try running with: sudo python scripts/capture_traffic.py")
    
    try:
        process = start_capture(
            output_file=output_file,
            interface=args.interface,
            ports=ports,
            duration=args.duration,
        )
        
        if args.duration:
            logger.info(f"Capturing for {args.duration} seconds...")
            time.sleep(args.duration)
            stop_capture(process)
        else:
            logger.info("Capturing... Press Ctrl+C to stop")
            try:
                process.wait()
            except KeyboardInterrupt:
                logger.info("Stopping capture...")
                stop_capture(process)
        
        logger.info(f"Capture saved to: {output_file}")
        
        # Quick analysis
        if output_file.exists() and output_file.stat().st_size > 0:
            logger.info("Quick analysis:")
            print(analyse_capture(output_file, brief=True))
        
        return 0
    
    except RuntimeError as e:
        logger.error(str(e))
        return 1
    except Exception as e:
        logger.error(f"Capture failed: {e}")
        return 1



# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    sys.exit(main())
