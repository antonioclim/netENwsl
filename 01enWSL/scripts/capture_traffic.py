#!/usr/bin/env python3
"""
Traffic Capture Helper
NETWORKING class - ASE, Informatics | by Revolvix

This script provides a convenient interface for capturing network traffic
using tcpdump within the Docker container.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import subprocess
import sys
import argparse
import signal
import time
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.logger import setup_logger

logger = setup_logger("capture_traffic")

# Global flag for signal handling
capture_running = True



# ═══════════════════════════════════════════════════════════════════════════════
# DATA_PROCESSING
# ═══════════════════════════════════════════════════════════════════════════════
def signal_handler(signum, frame):
    """Handle interrupt signals gracefully."""
    global capture_running
    capture_running = False
    logger.info("\nCapture interrupted. Stopping...")



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_container_running(container: str) -> bool:
    """Check if the specified container is running."""
    try:
        result = subprocess.run(
            ["docker", "inspect", "--format", "{{.State.Running}}", container],
            capture_output=True,
            text=True
        )
        return result.stdout.strip() == "true"
    except Exception:
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Capture network traffic in the lab container",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/capture_traffic.py --interface lo --port 9090
  python scripts/capture_traffic.py --output pcap/mytest.pcap --count 100
  python scripts/capture_traffic.py --filter "tcp port 9090" --duration 60
        """
    )
    parser.add_argument(
        "--interface", "-i",
        default="any",
        help="Network interface to capture on (default: any)"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output file path (default: pcap/capture_TIMESTAMP.pcap)"
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        help="Filter by port number"
    )
    parser.add_argument(
        "--host",
        help="Filter by host IP address"
    )
    parser.add_argument(
        "--filter", "-f",
        help="Custom BPF filter expression"
    )
    parser.add_argument(
        "--count", "-c",
        type=int,
        help="Stop after capturing N packets"
    )
    parser.add_argument(
        "--duration",
        type=int,
        help="Stop after N seconds"
    )
    parser.add_argument(
        "--container",
        default="week1_lab",
        help="Docker container to run capture in (default: week1_lab)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show packet summaries during capture"
    )
    args = parser.parse_args()

    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Check container is running
    if not check_container_running(args.container):
        logger.error(f"Container '{args.container}' is not running.")
        logger.info("Start the lab first: python scripts/start_lab.py")
        return 1

    # Determine output file
    if args.output:
        output_file = args.output
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = PROJECT_ROOT / "pcap" / f"capture_{timestamp}.pcap"
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Build filter expression
    filter_parts = []
    if args.port:
        filter_parts.append(f"port {args.port}")
    if args.host:
        filter_parts.append(f"host {args.host}")
    if args.filter:
        filter_parts.append(args.filter)
    
    filter_expr = " and ".join(filter_parts) if filter_parts else ""

    # Build tcpdump command
    tcpdump_cmd = ["tcpdump", "-i", args.interface]
    
    # Output file (mapped path in container)
    container_output = f"/work/pcap/{output_file.name}"
    tcpdump_cmd.extend(["-w", container_output])
    
    if args.count:
        tcpdump_cmd.extend(["-c", str(args.count)])
    
    if args.verbose:
        tcpdump_cmd.append("-v")
    
    if filter_expr:
        tcpdump_cmd.append(filter_expr)

    # Full docker exec command
    docker_cmd = ["docker", "exec", args.container] + tcpdump_cmd

    logger.info("=" * 60)
    logger.info("Starting Traffic Capture")
    logger.info("=" * 60)
    logger.info(f"  Interface: {args.interface}")
    logger.info(f"  Filter: {filter_expr or '(none)'}")
    logger.info(f"  Output: {output_file}")
    if args.count:
        logger.info(f"  Max packets: {args.count}")
    if args.duration:
        logger.info(f"  Duration: {args.duration}s")
    logger.info("")
    logger.info("Press Ctrl+C to stop capture")
    logger.info("-" * 60)

    try:
        # Start capture process
        process = subprocess.Popen(
            docker_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        start_time = time.time()
        
        # Monitor capture
        while capture_running:
            # Check if process has finished
            ret = process.poll()
            if ret is not None:
                break
            
            # Check duration limit
            if args.duration:
                elapsed = time.time() - start_time
                if elapsed >= args.duration:
                    logger.info(f"\nDuration limit ({args.duration}s) reached.")
                    process.terminate()
                    break
            
            # Read and display output
            try:
                line = process.stdout.readline()
                if line:
                    print(line.rstrip())
            except Exception:
                pass
            
            time.sleep(0.1)

        # Ensure process is terminated
        if process.poll() is None:
            process.terminate()
            process.wait(timeout=5)

    except Exception as e:
        logger.error(f"Capture failed: {e}")
        return 1

    # Check output file
    if output_file.exists():
        size = output_file.stat().st_size
        logger.info("")
        logger.info("=" * 60)
        logger.info(f"\033[92mCapture saved:\033[0m {output_file}")
        logger.info(f"  Size: {size:,} bytes")
        logger.info("")
        logger.info("To analyse:")
        logger.info(f"  tshark -r {output_file}")
        logger.info(f"  wireshark {output_file}")
        logger.info("=" * 60)
    else:
        logger.warning(f"Output file not found: {output_file}")
        logger.info("The file may be at a different location in the container.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
