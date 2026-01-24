#!/usr/bin/env python3
"""
Week 10 Traffic Capture Helper
NETWORKING class - ASE, Informatics | by Revolvix

Assists with packet capture for laboratory exercises.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import subprocess
import sys
import argparse
import time
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.logger import setup_logger

logger = setup_logger("capture_traffic")



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def list_interfaces() -> None:
    """List available network interfaces."""
    logger.info("Available network interfaces:")
    
    try:
        # Try tshark first
        result = subprocess.run(
            ["tshark", "-D"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print(result.stdout)
            return
    except FileNotFoundError:
        pass
    
    # Try tcpdump
    try:
        result = subprocess.run(
            ["tcpdump", "--list-interfaces"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print(result.stdout)
            return
    except FileNotFoundError:
        pass
    
    logger.error("Neither tshark nor tcpdump found.")
    logger.info("Install Wireshark (includes tshark) from wireshark.org")



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def capture_with_tcpdump(
    interface: str,
    output: Path,
    duration: int,
    filter_expr: str
) -> bool:
    """Capture traffic using tcpdump."""
    cmd = [
        "tcpdump",
        "-i", interface,
        "-w", str(output),
        "-G", str(duration),
        "-W", "1"
    ]
    
    if filter_expr:
        cmd.extend(filter_expr.split())
    
    logger.info(f"Starting tcpdump on {interface}...")
    logger.info(f"Output: {output}")
    logger.info(f"Duration: {duration}s")
    logger.info("Press Ctrl+C to stop early")
    
    try:
        result = subprocess.run(cmd, timeout=duration + 10)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return True
    except KeyboardInterrupt:
        logger.info("Capture stopped by user")
        return True
    except Exception as e:
        logger.error(f"Capture failed: {e}")
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# CONTAINER_MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════
def capture_in_container(
    container: str,
    interface: str,
    output: Path,
    duration: int
) -> bool:
    """Capture traffic inside a Docker container."""
    # Copy the capture command
    capture_cmd = f"tcpdump -i {interface} -w /tmp/capture.pcap -G {duration} -W 1"
    
    logger.info(f"Starting capture in container {container}...")
    
    try:
        # Run capture
        result = subprocess.run(
            ["docker", "exec", container, "sh", "-c", capture_cmd],
            timeout=duration + 10
        )
        
        # Copy file out
        subprocess.run([
            "docker", "cp",
            f"{container}:/tmp/capture.pcap",
            str(output)
        ])
        
        logger.info(f"Capture saved to: {output}")
        return True
        
    except Exception as e:
        logger.error(f"Container capture failed: {e}")
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    parser = argparse.ArgumentParser(description="Capture network traffic")
    parser.add_argument("--interface", "-i", default="any",
                        help="Network interface to capture on")
    parser.add_argument("--output", "-o", type=Path,
                        help="Output pcap file path")
    parser.add_argument("--duration", "-d", type=int, default=60,
                        help="Capture duration in seconds (default: 60)")
    parser.add_argument("--filter", "-f", default="",
                        help="BPF filter expression")
    parser.add_argument("--list", "-l", action="store_true",
                        help="List available interfaces")
    parser.add_argument("--container", "-c",
                        help="Capture inside Docker container")
    args = parser.parse_args()
    
    if args.list:
        list_interfaces()
        return 0
    
    # Generate output filename if not provided
    if args.output is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pcap_dir = PROJECT_ROOT / "pcap"
        pcap_dir.mkdir(exist_ok=True)
        args.output = pcap_dir / f"week10_capture_{timestamp}.pcap"
    
    logger.info("=" * 50)
    logger.info("Week 10 Traffic Capture")
    logger.info("=" * 50)
    
    if args.container:
        success = capture_in_container(
            args.container,
            args.interface,
            args.output,
            args.duration
        )
    else:
        success = capture_with_tcpdump(
            args.interface,
            args.output,
            args.duration,
            args.filter
        )
    
    if success and args.output.exists():
        size = args.output.stat().st_size
        logger.info(f"Capture complete: {args.output} ({size} bytes)")
        logger.info("")
        logger.info("Analyse with:")
        logger.info(f"  wireshark {args.output}")
        logger.info(f"  tshark -r {args.output}")
        return 0
    else:
        logger.error("Capture failed or file not created")
        return 1


if __name__ == "__main__":
    sys.exit(main())
