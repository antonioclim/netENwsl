#!/usr/bin/env python3
"""
Traffic Capture Helper
======================
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

This script assists with packet capture from Docker containers.

Learning Objectives:
    - Capture network traffic for analysis in Wireshark
    - Understand container networking interfaces
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import subprocess
import sys
import argparse
import signal
from pathlib import Path
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURE_MODULE_PATH
# ═══════════════════════════════════════════════════════════════════════════════
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORT_UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════
from scripts.utils.logger import setup_logger

logger = setup_logger("capture_traffic")


# ═══════════════════════════════════════════════════════════════════════════════
# CONTAINER_HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def get_docker_container_pid(container_name: str) -> int:
    """
    Get the PID of a Docker container's main process.
    
    Args:
        container_name: Name of the container
        
    Returns:
        Process ID of the container
        
    Raises:
        RuntimeError: If container not found
    """
    result = subprocess.run(
        ["docker", "inspect", "-f", "{{.State.Pid}}", container_name],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"Container {container_name} not found")
    return int(result.stdout.strip())


def list_container_interfaces(container: str) -> None:
    """
    List network interfaces in a container.
    
    Args:
        container: Container name
    """
    result = subprocess.run(
        ["docker", "exec", container, "ip", "link", "show"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"Interfaces in {container}:")
        print(result.stdout)
    else:
        logger.error(f"Could not list interfaces: {result.stderr}")


# ═══════════════════════════════════════════════════════════════════════════════
# CAPTURE_TRAFFIC
# ═══════════════════════════════════════════════════════════════════════════════
def capture_in_container(container: str, interface: str, output: Path, 
                         duration: int = 60, filter_expr: str = "") -> int:
    """
    Start a packet capture inside a Docker container.
    
    Args:
        container: Container name
        interface: Network interface (e.g., eth0)
        output: Output pcap file path
        duration: Capture duration in seconds
        filter_expr: Optional tcpdump filter expression
    
    Returns:
        Exit code (0 for success)
    """
    # ─────────────────────────────────────────────────────────────────────────
    # PREPARE_OUTPUT_DIRECTORY
    # ─────────────────────────────────────────────────────────────────────────
    output.parent.mkdir(parents=True, exist_ok=True)
    
    # ─────────────────────────────────────────────────────────────────────────
    # BUILD_TCPDUMP_COMMAND
    # ─────────────────────────────────────────────────────────────────────────
    cmd = ["docker", "exec", container, "tcpdump", "-i", interface, "-w", "/tmp/capture.pcap"]
    
    if filter_expr:
        cmd.extend(filter_expr.split())
    
    if duration > 0:
        cmd.extend(["-G", str(duration), "-W", "1"])
    
    # ─────────────────────────────────────────────────────────────────────────
    # START_CAPTURE
    # ─────────────────────────────────────────────────────────────────────────
    logger.info(f"Starting capture in {container} on {interface}...")
    logger.info(f"Duration: {duration} seconds")
    logger.info(f"Output: {output}")
    logger.info("Press Ctrl+C to stop capture early")
    
    try:
        proc = subprocess.Popen(cmd)
        proc.wait(timeout=duration + 5)
    except KeyboardInterrupt:
        logger.info("Capture interrupted by user")
        proc.terminate()
    except subprocess.TimeoutExpired:
        proc.terminate()
    
    # ─────────────────────────────────────────────────────────────────────────
    # COPY_CAPTURE_FILE
    # ─────────────────────────────────────────────────────────────────────────
    copy_cmd = ["docker", "cp", f"{container}:/tmp/capture.pcap", str(output)]
    subprocess.run(copy_cmd)
    
    # ─────────────────────────────────────────────────────────────────────────
    # CLEANUP_TEMPORARY_FILE
    # ─────────────────────────────────────────────────────────────────────────
    subprocess.run(["docker", "exec", container, "rm", "-f", "/tmp/capture.pcap"])
    
    # ─────────────────────────────────────────────────────────────────────────
    # VERIFY_OUTPUT
    # ─────────────────────────────────────────────────────────────────────────
    if output.exists():
        size = output.stat().st_size
        logger.info(f"Capture saved: {output} ({size} bytes)")
        return 0
    else:
        logger.error("Failed to save capture file")
        return 1


# ═══════════════════════════════════════════════════════════════════════════════
# BUILD_ARGUMENT_PARSER
# ═══════════════════════════════════════════════════════════════════════════════
def build_parser() -> argparse.ArgumentParser:
    """
    Build the command-line argument parser.
    
    Returns:
        Configured ArgumentParser
    """
    parser = argparse.ArgumentParser(
        description="Capture network traffic from Docker containers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python capture_traffic.py --container week5_python --interface eth0
  python capture_traffic.py --container week5_udp-server --duration 30
  python capture_traffic.py --container week5_python --filter "udp port 9999"
  python capture_traffic.py --list week5_python
"""
    )
    parser.add_argument("--container", "-c", default="week5_python",
                        help="Container name (default: week5_python)")
    parser.add_argument("--interface", "-i", default="eth0",
                        help="Network interface (default: eth0)")
    parser.add_argument("--output", "-o", type=Path,
                        help="Output pcap file (default: pcap/capture_TIMESTAMP.pcap)")
    parser.add_argument("--duration", "-d", type=int, default=60,
                        help="Capture duration in seconds (default: 60)")
    parser.add_argument("--filter", "-f", default="",
                        help="tcpdump filter expression")
    parser.add_argument("--list", "-l", metavar="CONTAINER",
                        help="List interfaces in a container")
    return parser


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """
    Main entry point for the traffic capture script.
    
    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    parser = build_parser()
    args = parser.parse_args()
    
    # ─────────────────────────────────────────────────────────────────────────
    # HANDLE_LIST_MODE
    # ─────────────────────────────────────────────────────────────────────────
    if args.list:
        list_container_interfaces(args.list)
        return 0
    
    # ─────────────────────────────────────────────────────────────────────────
    # GENERATE_OUTPUT_FILENAME
    # ─────────────────────────────────────────────────────────────────────────
    if args.output is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = PROJECT_ROOT / "pcap" / f"capture_{timestamp}.pcap"
    
    # ─────────────────────────────────────────────────────────────────────────
    # START_CAPTURE
    # ─────────────────────────────────────────────────────────────────────────
    return capture_in_container(
        container=args.container,
        interface=args.interface,
        output=args.output,
        duration=args.duration,
        filter_expr=args.filter
    )


if __name__ == "__main__":
    sys.exit(main())
