#!/usr/bin/env python3
"""
Traffic Capture Helper
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Helper script for capturing network traffic with tcpdump/Wireshark.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import subprocess
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.logger import setup_logger, print_banner

logger = setup_logger("capture_traffic")



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def get_default_interface() -> str:
    """Get the default network interface."""
    try:
        # Try to get Docker bridge interface
        result = subprocess.run(
            ["docker", "network", "inspect", "bridge", "--format", "{{.Options.com.docker.network.bridge.name}}"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass
    
    # Default to lo for loopback
    return "lo"



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_tcpdump_available() -> bool:
    """Check if tcpdump is available."""
    try:
        result = subprocess.run(["which", "tcpdump"], capture_output=True)
        return result.returncode == 0
    except Exception:
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
def start_capture(
    interface: str,
    output_file: Path,
    filter_expr: str,
    duration: int
) -> bool:
    """
    Start packet capture.
    
    Args:
        interface: Network interface to capture from
        output_file: Output pcap file path
        filter_expr: BPF filter expression
        duration: Capture duration in seconds (0 for indefinite)
        
    Returns:
        True if capture succeeded, False otherwise
    """
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    cmd: list[str] = [
        "tcpdump",
        "-i", interface,
        "-w", str(output_file),
        "-nn",  # Don't resolve hostnames or ports
    ]
    
    if filter_expr:
        cmd.extend(filter_expr.split())
    
    logger.info(f"Starting capture on interface: {interface}")
    logger.info(f"Output file: {output_file}")
    logger.info(f"Filter: {filter_expr or '(none)'}")
    
    if duration > 0:
        logger.info(f"Duration: {duration} seconds")
        cmd.extend(["-G", str(duration), "-W", "1"])
    else:
        logger.info("Duration: Until Ctrl+C")
    
    logger.info("\nCapture command:")
    logger.info(f"  {' '.join(cmd)}")
    print()
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        if duration > 0:
            stdout, stderr = process.communicate(timeout=duration + 5)
        else:
            logger.info("Press Ctrl+C to stop capture...")
            stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            logger.info(f"\n✓ Capture saved to: {output_file}")
            
            # Show file size
            if output_file.exists():
                size: int = output_file.stat().st_size
                logger.info(f"  File size: {size:,} bytes")
        else:
            logger.error(f"Capture failed: {stderr.decode()}")
            return False
            
    except subprocess.TimeoutExpired:
        process.terminate()
        logger.info(f"\n✓ Capture complete: {output_file}")
    except KeyboardInterrupt:
        process.terminate()
        logger.info(f"\n✓ Capture stopped: {output_file}")
    except PermissionError:
        logger.error("Permission denied. Try running with sudo or as administrator.")
        return False
    except Exception as e:
        logger.error(f"Capture error: {e}")
        return False
    
    return True



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def print_wireshark_instructions(output_file: Path, filter_expr: str) -> None:
    """Print instructions for viewing capture in Wireshark."""
    print("\n" + "=" * 60)
    print("Viewing in Wireshark")
    print("=" * 60)
    print(f"""
1. Open Wireshark

2. File → Open → Select: {output_file}

3. Useful display filters:
   http                        # HTTP traffic only
   tcp.port == 8080           # Traffic on port 8080
   tcp.flags.syn == 1         # TCP SYN packets
   http.request               # HTTP requests only
   http.response              # HTTP responses only

4. Right-click a packet → Follow → TCP Stream
   (to see the complete HTTP conversation)

5. Statistics → Conversations → TCP
   (to see connection statistics)
""")



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Capture network traffic for Week 8 laboratory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/capture_traffic.py
  python scripts/capture_traffic.py --filter "tcp port 8080"
  python scripts/capture_traffic.py --duration 60 --output mycapture.pcap
  python scripts/capture_traffic.py --interface docker0
        """
    )
    parser.add_argument(
        "--interface", "-i",
        default=None,
        help="Network interface (default: auto-detect)"
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Output file path (default: pcap/week8_<timestamp>.pcap)"
    )
    parser.add_argument(
        "--filter", "-f",
        default="tcp port 8080",
        help="BPF filter expression (default: 'tcp port 8080')"
    )
    parser.add_argument(
        "--duration", "-d",
        type=int,
        default=0,
        help="Capture duration in seconds (0 = until Ctrl+C)"
    )
    parser.add_argument(
        "--list-interfaces", "-l",
        action="store_true",
        help="List available network interfaces"
    )
    
    args = parser.parse_args()
    
    print_banner(
        "Week 8 Traffic Capture",
        "Transport Layer: HTTP Server and Reverse Proxies"
    )
    
    # List interfaces
    if args.list_interfaces:
        logger.info("Available interfaces:")
        try:
            result = subprocess.run(
                ["tcpdump", "-D"],
                capture_output=True,
                text=True
            )
            print(result.stdout)
        except Exception:
            logger.error("Could not list interfaces. Is tcpdump installed?")
        return 0
    
    # Check tcpdump
    if not check_tcpdump_available():
        logger.error("tcpdump is not available.")
        print("""
To install tcpdump:
  Ubuntu/Debian: sudo apt install tcpdump
  Windows WSL:   sudo apt install tcpdump
  
Alternatively, use Wireshark GUI for capture.
        """)
        return 1
    
    # Determine interface
    interface: str = args.interface or get_default_interface()
    
    # Determine output file
    output_file: Path
    if args.output:
        output_file = Path(args.output)
    else:
        timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = PROJECT_ROOT / "pcap" / f"week8_{timestamp}.pcap"
    
    # Start capture
    success: bool = start_capture(
        interface=interface,
        output_file=output_file,
        filter_expr=args.filter,
        duration=args.duration
    )
    
    if success:
        print_wireshark_instructions(output_file, args.filter)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
