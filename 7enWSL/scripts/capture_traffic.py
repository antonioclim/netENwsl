#!/usr/bin/env python3
"""
Traffic Capture Helper
NETWORKING class - ASE, Informatics | by Revolvix

Helper script for capturing network traffic using tcpdump or tshark.
Provides a consistent interface for laboratory exercises.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import shutil
import signal
import time
from pathlib import Path
from typing import Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.logger import setup_logger

logger = setup_logger("capture")


def find_capture_tool() -> tuple[str, list[str]]:
    """
    Find an available packet capture tool.
    
    Returns:
        Tuple of (tool_name, base_arguments)
    """
    # Prefer tcpdump
    if shutil.which("tcpdump"):
        return "tcpdump", ["tcpdump", "-nn", "-U"]
    
    # Fall back to tshark
    if shutil.which("tshark"):
        return "tshark", ["tshark", "-n"]
    
    # Check Windows paths
    wireshark_paths = [
        Path(r"C:\Program Files\Wireshark\tshark.exe"),
        Path(r"C:\Program Files (x86)\Wireshark\tshark.exe"),
    ]
    for p in wireshark_paths:
        if p.exists():
            return "tshark", [str(p), "-n"]
    
    raise RuntimeError("No packet capture tool found. Install tcpdump or Wireshark.")


def list_interfaces(tool: str, base_args: list[str]) -> None:
    """List available network interfaces."""
    if tool == "tcpdump":
        subprocess.run(["tcpdump", "-D"], check=False)
    else:
        subprocess.run(base_args[:1] + ["-D"], check=False)


def start_capture(
    tool: str,
    base_args: list[str],
    interface: str,
    output: Path,
    filter_expr: str,
    duration: Optional[int] = None
) -> subprocess.Popen:
    """
    Start a packet capture.
    
    Args:
        tool: Capture tool name
        base_args: Base command arguments
        interface: Network interface
        output: Output file path
        filter_expr: BPF filter expression
        duration: Capture duration in seconds (None for indefinite)
        
    Returns:
        Popen process handle
    """
    args = base_args.copy()
    
    # Add interface
    args.extend(["-i", interface])
    
    # Add output file
    args.extend(["-w", str(output)])
    
    # Add duration if specified (tcpdump specific)
    if duration and tool == "tcpdump":
        args.extend(["-G", str(duration), "-W", "1"])
    
    # Add filter if specified
    if filter_expr:
        args.append(filter_expr)
    
    logger.info(f"Starting capture: {' '.join(args)}")
    
    output.parent.mkdir(parents=True, exist_ok=True)
    
    return subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Capture network traffic for Week 7 laboratory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Capture all TCP/UDP traffic for 60 seconds
  python capture_traffic.py --output pcap/demo.pcap --duration 60

  # Capture only TCP port 9090
  python capture_traffic.py --output pcap/tcp.pcap --filter "tcp port 9090"

  # List available interfaces
  python capture_traffic.py --list-interfaces
"""
    )
    parser.add_argument(
        "--interface", "-i",
        default="any",
        help="Network interface to capture (default: any)"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=PROJECT_ROOT / "pcap" / "capture.pcap",
        help="Output file path"
    )
    parser.add_argument(
        "--filter", "-f",
        default="tcp or udp",
        help="BPF filter expression (default: 'tcp or udp')"
    )
    parser.add_argument(
        "--duration", "-d",
        type=int,
        help="Capture duration in seconds (default: indefinite)"
    )
    parser.add_argument(
        "--list-interfaces",
        action="store_true",
        help="List available network interfaces and exit"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    args = parser.parse_args()

    try:
        tool, base_args = find_capture_tool()
        logger.info(f"Using capture tool: {tool}")
    except RuntimeError as e:
        logger.error(str(e))
        return 1

    if args.list_interfaces:
        list_interfaces(tool, base_args)
        return 0

    logger.info("=" * 60)
    logger.info("Week 7 Traffic Capture")
    logger.info("=" * 60)
    logger.info(f"Interface: {args.interface}")
    logger.info(f"Output: {args.output}")
    logger.info(f"Filter: {args.filter}")
    if args.duration:
        logger.info(f"Duration: {args.duration} seconds")
    else:
        logger.info("Duration: Press Ctrl+C to stop")
    logger.info("")

    try:
        proc = start_capture(
            tool,
            base_args,
            args.interface,
            args.output,
            args.filter,
            args.duration
        )

        if args.duration:
            # Wait for duration
            logger.info(f"Capturing for {args.duration} seconds...")
            time.sleep(args.duration)
            proc.terminate()
        else:
            # Wait for Ctrl+C
            logger.info("Capturing... Press Ctrl+C to stop")
            proc.wait()

        # Check output
        if args.output.exists():
            size = args.output.stat().st_size
            logger.info(f"Capture saved: {args.output} ({size} bytes)")
            
            # Show packet count if tshark available
            if shutil.which("tshark"):
                result = subprocess.run(
                    ["tshark", "-r", str(args.output), "-T", "fields", "-e", "frame.number"],
                    capture_output=True,
                    text=True
                )
                packet_count = len(result.stdout.strip().split("\n")) if result.stdout.strip() else 0
                logger.info(f"Packets captured: {packet_count}")
        else:
            logger.warning("No output file created - check permissions and filter")

        return 0

    except KeyboardInterrupt:
        logger.info("")
        logger.info("Capture stopped by user")
        if proc and proc.poll() is None:
            proc.terminate()
            proc.wait()
        return 0
    except Exception as e:
        logger.error(f"Capture failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
