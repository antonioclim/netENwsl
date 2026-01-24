#!/usr/bin/env python3
"""
Traffic Capture Helper
======================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

Provides simplified traffic capture for Week 13 laboratory exercises.

USAGE:
    # Capture lab traffic for 60 seconds
    python3 scripts/capture_traffic.py --duration 60

    # Capture with custom filter
    python3 scripts/capture_traffic.py --filter "tcp port 1883"

    # Capture all traffic (no filter)
    python3 scripts/capture_traffic.py --no-filter
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORT_DEPENDENCIES
# ═══════════════════════════════════════════════════════════════════════════════
import subprocess
import sys
import time
import signal
import argparse
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.logger import setup_logger

logger = setup_logger("capture_traffic")


# ═══════════════════════════════════════════════════════════════════════════════
# CAPTURE_MANAGER_CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class CaptureManager:
    """Manages packet capture using tcpdump or tshark."""
    
    def __init__(self, output_dir: Path):
        """
        Initialise capture manager.
        
        Args:
            output_dir: Directory to store capture files
        """
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.process = None
        self.output_file = None
    
    # ─────────────────────────────────────────────────────────────────────────
    # START_CAPTURE
    # ─────────────────────────────────────────────────────────────────────────
    def start_capture(
        self,
        interface: str = "any",
        output: str = None,
        bpf_filter: str = None,
        duration: int = None
    ) -> bool:
        """
        Start packet capture.
        
        Args:
            interface: Network interface to capture on
            output: Output filename (auto-generated if None)
            bpf_filter: BPF filter expression
            duration: Capture duration in seconds (None for manual stop)
        
        Returns:
            True if capture started successfully
        """
        # Generate output filename if not provided
        if output:
            self.output_file = self.output_dir / output
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.output_file = self.output_dir / f"capture_{timestamp}.pcap"
        
        # Build tcpdump command
        cmd = ["tcpdump", "-i", interface, "-w", str(self.output_file)]
        
        if bpf_filter:
            cmd.extend(bpf_filter.split())
        
        if duration:
            cmd.extend(["-G", str(duration), "-W", "1"])
        
        logger.info(f"Starting capture on interface: {interface}")
        logger.info(f"Output file: {self.output_file}")
        if bpf_filter:
            logger.info(f"BPF filter: {bpf_filter}")
        
        try:
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            time.sleep(1)  # Give tcpdump time to start
            
            if self.process.poll() is not None:
                _, stderr = self.process.communicate()
                logger.error(f"Capture failed to start: {stderr.decode()}")
                return False
            
            logger.info("Capture started successfully")
            return True
            
        except FileNotFoundError:
            logger.error("tcpdump not found. Install with: apt-get install tcpdump")
            return False
        except PermissionError:
            logger.error("Permission denied. Run with sudo or as root.")
            return False
        except Exception as e:
            logger.error(f"Failed to start capture: {e}")
            return False
    
    # ─────────────────────────────────────────────────────────────────────────
    # STOP_CAPTURE
    # ─────────────────────────────────────────────────────────────────────────
    def stop_capture(self) -> Path:
        """
        Stop the running capture.
        
        Returns:
            Path to the capture file
        """
        if self.process:
            logger.info("Stopping capture...")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            
            self.process = None
            logger.info(f"Capture saved to: {self.output_file}")
        
        return self.output_file
    
    # ─────────────────────────────────────────────────────────────────────────
    # WAIT_FOR_DURATION
    # ─────────────────────────────────────────────────────────────────────────
    def wait_for_duration(self, duration: int) -> None:
        """Wait for specified duration then stop capture."""
        logger.info(f"Capturing for {duration} seconds...")
        try:
            for remaining in range(duration, 0, -1):
                if remaining % 10 == 0 or remaining <= 5:
                    logger.info(f"  {remaining} seconds remaining...")
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Capture interrupted by user")
        finally:
            self.stop_capture()


# ═══════════════════════════════════════════════════════════════════════════════
# ARGUMENT_PARSING
# ═══════════════════════════════════════════════════════════════════════════════

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Capture network traffic for Week 13 laboratory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --duration 60                    # Capture for 60 seconds
  %(prog)s --filter "tcp port 1883"         # Custom BPF filter
  %(prog)s --no-filter --duration 30        # Capture all traffic
  %(prog)s --output my_capture.pcap         # Custom output filename
        """
    )
    parser.add_argument(
        "--interface", "-i",
        default="any",
        help="Network interface to capture on (default: any)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output filename (default: auto-generated)"
    )
    parser.add_argument(
        "--filter", "-f",
        default="tcp port 1883 or tcp port 8883 or tcp port 8080 or tcp port 2121 or tcp port 6200",
        help="BPF filter expression (default: Week 13 lab ports)"
    )
    parser.add_argument(
        "--duration", "-d",
        type=int,
        default=60,
        help="Capture duration in seconds (default: 60)"
    )
    parser.add_argument(
        "--no-filter",
        action="store_true",
        help="Capture all traffic (no BPF filter)"
    )
    
    return parser.parse_args()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Main entry point."""
    args = parse_arguments()
    
    # ─────────────────────────────────────────────────────────────────────────
    # DISPLAY_BANNER
    # ─────────────────────────────────────────────────────────────────────────
    logger.info("=" * 60)
    logger.info("Week 13 Traffic Capture")
    logger.info("=" * 60)
    
    # ─────────────────────────────────────────────────────────────────────────
    # INITIALISE_CAPTURE
    # ─────────────────────────────────────────────────────────────────────────
    pcap_dir = PROJECT_ROOT / "pcap"
    capture = CaptureManager(pcap_dir)
    
    bpf_filter = None if args.no_filter else args.filter
    
    # ─────────────────────────────────────────────────────────────────────────
    # START_CAPTURE
    # ─────────────────────────────────────────────────────────────────────────
    if not capture.start_capture(
        interface=args.interface,
        output=args.output,
        bpf_filter=bpf_filter,
        duration=None  # We'll handle duration manually
    ):
        return 1
    
    # ─────────────────────────────────────────────────────────────────────────
    # SETUP_SIGNAL_HANDLERS
    # ─────────────────────────────────────────────────────────────────────────
    def signal_handler(sig, frame):
        capture.stop_capture()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # ─────────────────────────────────────────────────────────────────────────
    # WAIT_FOR_CAPTURE_DURATION
    # ─────────────────────────────────────────────────────────────────────────
    capture.wait_for_duration(args.duration)
    
    # ─────────────────────────────────────────────────────────────────────────
    # DISPLAY_RESULTS
    # ─────────────────────────────────────────────────────────────────────────
    logger.info("=" * 60)
    logger.info("Capture complete!")
    logger.info(f"Open in Wireshark: {capture.output_file}")
    logger.info("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
