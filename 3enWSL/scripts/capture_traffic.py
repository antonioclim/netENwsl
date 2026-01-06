#!/usr/bin/env python3
"""
Traffic Capture Helper
NETWORKING class - ASE, Informatics | by Revolvix

Assists with capturing network traffic from Docker containers.
"""

import subprocess
import sys
import argparse
import signal
import time
from pathlib import Path
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.logger import setup_logger

logger = setup_logger("capture")


def capture_in_container(
    container: str,
    interface: str,
    output: Path,
    duration: int,
    filter_expr: str
) -> int:
    """Run tcpdump capture inside a container."""
    
    # Build tcpdump command
    tcpdump_cmd = ["tcpdump", "-i", interface, "-w", f"/tmp/capture.pcap"]
    
    if filter_expr:
        tcpdump_cmd.append(filter_expr)
    
    if duration > 0:
        tcpdump_cmd.extend(["-G", str(duration), "-W", "1"])
    
    docker_cmd = ["docker", "exec", container] + tcpdump_cmd
    
    logger.info(f"Starting capture in {container} on {interface}...")
    logger.info(f"Duration: {duration}s, Filter: {filter_expr or 'none'}")
    
    try:
        # Run tcpdump
        if duration > 0:
            result = subprocess.run(
                docker_cmd,
                timeout=duration + 10
            )
        else:
            # Run until interrupted
            process = subprocess.Popen(docker_cmd)
            logger.info("Capturing... Press Ctrl+C to stop")
            
            try:
                process.wait()
            except KeyboardInterrupt:
                process.send_signal(signal.SIGINT)
                process.wait()
        
        # Copy capture file out
        logger.info(f"Copying capture to {output}...")
        subprocess.run([
            "docker", "cp",
            f"{container}:/tmp/capture.pcap",
            str(output)
        ], check=True)
        
        # Cleanup
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


def main() -> int:
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
    args = parser.parse_args()

    # List interfaces if requested
    if args.list_interfaces:
        logger.info(f"Interfaces in {args.container}:")
        subprocess.run([
            "docker", "exec", args.container,
            "ip", "link", "show"
        ])
        return 0

    # Determine output file
    if args.output:
        output = Path(args.output)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = PROJECT_ROOT / "pcap" / f"week3_{timestamp}.pcap"
    
    # Ensure output directory exists
    output.parent.mkdir(parents=True, exist_ok=True)

    return capture_in_container(
        args.container,
        args.interface,
        output,
        args.duration,
        args.filter
    )


if __name__ == "__main__":
    sys.exit(main())
