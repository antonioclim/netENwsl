#!/usr/bin/env python3
"""
Traffic Capture Helper for Week 11 Laboratory
NETWORKING class - ASE, Informatics | by Revolvix

This script assists with capturing network traffic for analysis in Wireshark.
"""
from __future__ import annotations

import subprocess
import sys
import time
import argparse
import signal
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.logger import setup_logger, print_banner

logger = setup_logger("capture_traffic")

# Global process reference for signal handling
capture_process = None


def signal_handler(signum, frame):
    """Handle interrupt signal."""
    global capture_process
    if capture_process:
        logger.info("\nStopping capture...")
        capture_process.terminate()
        capture_process.wait()
    sys.exit(0)


def find_capture_tool() -> str:
    """Find available packet capture tool."""
    import shutil
    
    # Prefer tshark, then tcpdump
    if shutil.which('tshark'):
        return 'tshark'
    if shutil.which('tcpdump'):
        return 'tcpdump'
    
    return ''


def start_tshark_capture(interface: str, 
                         output_file: str,
                         capture_filter: str,
                         duration: int) -> subprocess.Popen:
    """Start tshark capture."""
    cmd = [
        'tshark',
        '-i', interface,
        '-w', output_file,
    ]
    
    if capture_filter:
        cmd.extend(['-f', capture_filter])
    
    if duration > 0:
        cmd.extend(['-a', f'duration:{duration}'])
    
    logger.info(f"Starting tshark capture on {interface}")
    logger.info(f"Command: {' '.join(cmd)}")
    
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def start_tcpdump_capture(interface: str,
                          output_file: str,
                          capture_filter: str,
                          duration: int) -> subprocess.Popen:
    """Start tcpdump capture."""
    cmd = [
        'tcpdump',
        '-i', interface,
        '-w', output_file,
    ]
    
    if capture_filter:
        cmd.extend([capture_filter])
    
    logger.info(f"Starting tcpdump capture on {interface}")
    logger.info(f"Command: {' '.join(cmd)}")
    
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def analyse_capture(pcap_file: str) -> None:
    """Analyse a capture file and print summary."""
    import shutil
    
    if not Path(pcap_file).exists():
        logger.error(f"Capture file not found: {pcap_file}")
        return
    
    if shutil.which('tshark'):
        # Count packets by protocol
        logger.info("\nCapture Analysis:")
        logger.info("-" * 40)
        
        # HTTP packets
        result = subprocess.run(
            ['tshark', '-r', pcap_file, '-Y', 'http', '-T', 'fields', '-e', 'frame.number'],
            capture_output=True, text=True
        )
        http_count = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
        logger.info(f"HTTP packets: {http_count}")
        
        # DNS packets
        result = subprocess.run(
            ['tshark', '-r', pcap_file, '-Y', 'dns', '-T', 'fields', '-e', 'frame.number'],
            capture_output=True, text=True
        )
        dns_count = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
        logger.info(f"DNS packets: {dns_count}")
        
        # Total packets
        result = subprocess.run(
            ['tshark', '-r', pcap_file, '-T', 'fields', '-e', 'frame.number'],
            capture_output=True, text=True
        )
        total_count = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
        logger.info(f"Total packets: {total_count}")
        
        logger.info("-" * 40)
        logger.info(f"\nCapture file: {pcap_file}")
        logger.info("Open in Wireshark for detailed analysis")
    else:
        logger.info(f"\nCapture saved to: {pcap_file}")
        logger.info("Install tshark for automatic analysis")


def main() -> int:
    global capture_process
    
    parser = argparse.ArgumentParser(
        description="Capture network traffic for Week 11 Laboratory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                              # Capture on default interface
  %(prog)s -i eth0 -o myfile.pcap       # Custom interface and output
  %(prog)s --filter "tcp port 8080"     # Capture only LB traffic
  %(prog)s --duration 30                # Capture for 30 seconds
  %(prog)s --analyse pcap/capture.pcap  # Analyse existing capture
        """
    )
    parser.add_argument("-i", "--interface", default="any",
                        help="Network interface (default: any)")
    parser.add_argument("-o", "--output", default=None,
                        help="Output file (default: pcap/week11_TIMESTAMP.pcap)")
    parser.add_argument("-f", "--filter", default="tcp port 8080",
                        help="Capture filter (default: tcp port 8080)")
    parser.add_argument("-d", "--duration", type=int, default=0,
                        help="Capture duration in seconds (default: until Ctrl+C)")
    parser.add_argument("--analyse", metavar="FILE",
                        help="Analyse existing capture file instead of capturing")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Verbose output")
    
    args = parser.parse_args()
    
    # Analysis mode
    if args.analyse:
        analyse_capture(args.analyse)
        return 0
    
    print_banner("Traffic Capture - Week 11")
    
    # Find capture tool
    tool = find_capture_tool()
    if not tool:
        logger.error("No packet capture tool found!")
        logger.error("Install tshark (Wireshark) or tcpdump")
        return 1
    
    # Generate output filename if not specified
    if args.output:
        output_file = args.output
    else:
        pcap_dir = PROJECT_ROOT / "pcap"
        pcap_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = str(pcap_dir / f"week11_{timestamp}.pcap")
    
    # Setup signal handler
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Start capture
        if tool == 'tshark':
            capture_process = start_tshark_capture(
                args.interface, output_file, args.filter, args.duration
            )
        else:
            capture_process = start_tcpdump_capture(
                args.interface, output_file, args.filter, args.duration
            )
        
        logger.info(f"Output file: {output_file}")
        logger.info("Press Ctrl+C to stop capture")
        logger.info("")
        
        # Wait for capture to complete
        if args.duration > 0:
            logger.info(f"Capturing for {args.duration} seconds...")
            capture_process.wait()
        else:
            # Wait indefinitely until interrupted
            while capture_process.poll() is None:
                time.sleep(1)
        
        # Analyse capture
        analyse_capture(output_file)
        
        return 0
    
    except Exception as e:
        logger.error(f"Capture failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())


# Revolvix&Hypotheticalandrei
