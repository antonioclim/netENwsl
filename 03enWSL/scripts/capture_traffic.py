#!/usr/bin/env python3
"""
Traffic Capture Helper
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Assists with capturing network traffic from Docker containers.
"""

# ════════════════════════════════════════════════════════════════════════════════
# IMPORTS AND CONFIGURATION
# ════════════════════════════════════════════════════════════════════════════════

import subprocess
import sys
import argparse
import signal
from pathlib import Path
from datetime import datetime
from typing import Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.logger import setup_logger

logger = setup_logger("capture")


# ════════════════════════════════════════════════════════════════════════════════
# CAPTURE FUNCTIONS
# ════════════════════════════════════════════════════════════════════════════════

def capture_in_container(
    container: str,
    interface: str,
    output: Path,
    duration: int,
    filter_expr: str
) -> int:
    """
    Run tcpdump capture inside a container.
    
    Args:
        container: Docker container name
        interface: Network interface to capture on
        output: Output file path for pcap
        duration: Capture duration in seconds (0 = until interrupted)
        filter_expr: tcpdump filter expression
        
    Returns:
        0 on success, 1 on failure
    """
    
    # ─────────────────────────────────────────────────────────────────────────
    # Step 1: Build tcpdump command
    # ─────────────────────────────────────────────────────────────────────────
    tcpdump_cmd = ["tcpdump", "-i", interface, "-w", "/tmp/capture.pcap"]
    
    if filter_expr:
        tcpdump_cmd.append(filter_expr)
    
    if duration > 0:
        tcpdump_cmd.extend(["-G", str(duration), "-W", "1"])
    
    docker_cmd = ["docker", "exec", container] + tcpdump_cmd
    
    logger.info(f"Starting capture in {container} on {interface}...")
    logger.info(f"Duration: {duration}s, Filter: {filter_expr or 'none'}")
    
    try:
        # ─────────────────────────────────────────────────────────────────────
        # Step 2: Run tcpdump
        # ─────────────────────────────────────────────────────────────────────
        if duration > 0:
            subprocess.run(docker_cmd, timeout=duration + 10)
        else:
            # Run until interrupted
            process = subprocess.Popen(docker_cmd)
            logger.info("Capturing... Press Ctrl+C to stop")
            
            try:
                process.wait()
            except KeyboardInterrupt:
                process.send_signal(signal.SIGINT)
                process.wait()
        
        # ─────────────────────────────────────────────────────────────────────
        # Step 3: Copy capture file out
        # ─────────────────────────────────────────────────────────────────────
        logger.info(f"Copying capture to {output}...")
        subprocess.run([
            "docker", "cp",
            f"{container}:/tmp/capture.pcap",
            str(output)
        ], check=True)
        
        # ─────────────────────────────────────────────────────────────────────
        # Step 4: Cleanup temporary file
        # ─────────────────────────────────────────────────────────────────────
        subprocess.run([
            "docker", "exec", container,
            "rm", "-f", "/tmp/capture.pcap"
        ], capture_output=True)
        
        logger.info(f"Capture saved to: {output}")
        return 0
        
    except subprocess.TimeoutExpired:
        logger.info("Capture duration completed")
        # Still try to copy the file
        subprocess.run([
            "docker", "cp",
            f"{container}:/tmp/capture.pcap",
            str(output)
        ], capture_output=True)
        return 0
        
    except Exception as e:
        logger.error(f"Capture failed: {e}")
        return 1


def list_interfaces(container: str) -> int:
    """List available network interfaces in a container."""
    logger.info(f"Interfaces in {container}:")
    result = subprocess.run([
        "docker", "exec", container,
        "ip", "link", "show"
    ])
    return result.returncode


# ════════════════════════════════════════════════════════════════════════════════
# ARGUMENT PARSER
# ════════════════════════════════════════════════════════════════════════════════

def build_argument_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser."""
    parser = argparse.ArgumentParser(
        description="Capture network traffic from Week 3 laboratory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Capture from client container for 60 seconds
  python capture_traffic.py --container week3_client --duration 60

  # Capture with filter
  python capture_traffic.py --container week3_router --filter "tcp port 9090"

  # Capture to specific file
  python capture_traffic.py -c week3_server -o pcap/server_traffic.pcap

Suggested filters for Week 3:
  "udp port 5007"           # Broadcast traffic
  "udp port 5008"           # Multicast traffic  
  "tcp port 8080"           # Echo server
  "tcp port 9090"           # TCP tunnel
  "igmp"                    # IGMP membership
        """
    )
    parser.add_argument(
        "-c", "--container", default="week3_client",
        help="Container to capture from (default: week3_client)"
    )
    parser.add_argument(
        "-i", "--interface", default="eth0",
        help="Interface to capture on (default: eth0)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output pcap file (default: pcap/week3_<timestamp>.pcap)"
    )
    parser.add_argument(
        "-d", "--duration", type=int, default=0,
        help="Capture duration in seconds (0 = until Ctrl+C)"
    )
    parser.add_argument(
        "-f", "--filter", default="",
        help="tcpdump filter expression"
    )
    parser.add_argument(
        "--list-interfaces", action="store_true",
        help="List available interfaces in container"
    )
    return parser


# ════════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ════════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Main entry point."""
    parser = build_argument_parser()
    args = parser.parse_args()

    # ─────────────────────────────────────────────────────────────────────────
    # Handle list-interfaces request
    # ─────────────────────────────────────────────────────────────────────────
    if args.list_interfaces:
        return list_interfaces(args.container)

    # ─────────────────────────────────────────────────────────────────────────
    # Determine output file
    # ─────────────────────────────────────────────────────────────────────────
    if args.output:
        output = Path(args.output)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = PROJECT_ROOT / "pcap" / f"week3_{timestamp}.pcap"
    
    # ─────────────────────────────────────────────────────────────────────────
    # Ensure output directory exists
    # ─────────────────────────────────────────────────────────────────────────
    output.parent.mkdir(parents=True, exist_ok=True)

    # ─────────────────────────────────────────────────────────────────────────
    # Run capture
    # ─────────────────────────────────────────────────────────────────────────
    return capture_in_container(
        args.container,
        args.interface,
        output,
        args.duration,
        args.filter
    )


if __name__ == "__main__":
    sys.exit(main())
