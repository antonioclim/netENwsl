#!/usr/bin/env python3
"""
Homework 3.1: Enhanced Broadcast Receiver with Statistics
NETWORKING class - ASE, Informatics

Student: <Your Name>
Student ID: <Your ID>
Date: <Submission Date>

Description:
Extend the basic UDP broadcast receiver to collect and display comprehensive
statistics about received traffic, including packet counts, timing analysis,
and sender breakdown.

Requirements:
- Count total packets and unique senders
- Calculate packets per second (moving average)
- Track payload size statistics (min, max, avg)
- Detect inter-arrival time gaps
- Display real-time statistics every 5 seconds
- Generate summary report on Ctrl+C
- Optionally save statistics to JSON file

Usage:
    python hw_3_01.py [--port PORT] [--output FILE]
"""

import socket
import signal
import sys
import time
import json
import argparse
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict

# Configuration
DEFAULT_PORT = 5007
STATS_INTERVAL = 5.0  # seconds
GAP_THRESHOLD = 1.0   # seconds


@dataclass
class PacketInfo:
    """Information about a single received packet."""
    timestamp: float
    sender_ip: str
    sender_port: int
    payload_size: int


@dataclass 
class ReceiverStatistics:
    """Aggregated statistics for the broadcast receiver."""
    start_time: float = field(default_factory=time.time)
    last_packet_time: Optional[float] = None
    total_packets: int = 0
    senders: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    payload_sizes: List[int] = field(default_factory=list)
    inter_arrival_times: List[float] = field(default_factory=list)
    gaps_detected: int = 0
    
    def record_packet(self, packet: PacketInfo) -> None:
        """Record statistics for a received packet.
        
        TODO: Implement this method
        - Increment total_packets
        - Update senders dictionary
        - Add payload_size to list
        - Calculate inter-arrival time if not first packet
        - Detect gaps (> GAP_THRESHOLD)
        - Update last_packet_time
        """
        # YOUR CODE HERE
        pass
    
    def get_runtime(self) -> float:
        """Calculate total runtime in seconds."""
        return time.time() - self.start_time
    
    def get_packets_per_second(self) -> float:
        """Calculate average packets per second.
        
        TODO: Implement this method
        """
        # YOUR CODE HERE
        return 0.0
    
    def get_payload_stats(self) -> Dict[str, float]:
        """Calculate payload size statistics.
        
        TODO: Implement this method
        Returns dict with 'min', 'max', 'avg' keys
        """
        # YOUR CODE HERE
        return {'min': 0, 'max': 0, 'avg': 0.0}
    
    def get_unique_senders(self) -> int:
        """Return count of unique sender IPs."""
        return len(self.senders)
    
    def format_summary(self) -> str:
        """Format a complete summary report.
        
        TODO: Implement this method
        See homework README for expected output format
        """
        # YOUR CODE HERE
        return "Summary not implemented"
    
    def to_json(self) -> dict:
        """Convert statistics to JSON-serializable dictionary.
        
        TODO: Implement this method
        """
        # YOUR CODE HERE
        return {}


class BroadcastReceiverStats:
    """Enhanced UDP Broadcast Receiver with Statistics Collection."""
    
    def __init__(self, port: int = DEFAULT_PORT, output_file: Optional[str] = None):
        self.port = port
        self.output_file = output_file
        self.stats = ReceiverStatistics()
        self.socket: Optional[socket.socket] = None
        self.running = False
        
        # Register signal handlers
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)
    
    def _handle_shutdown(self, signum, frame):
        """Handle graceful shutdown on Ctrl+C.
        
        TODO: Implement this method
        - Set running to False
        - Print summary report
        - Optionally save to JSON file
        - Close socket
        """
        # YOUR CODE HERE
        print("\nShutting down...")
        self.running = False
    
    def _create_socket(self) -> socket.socket:
        """Create and configure UDP socket for broadcast reception.
        
        TODO: Implement this method
        - Create UDP socket
        - Set SO_REUSEADDR option
        - Bind to all interfaces on self.port
        - Set socket timeout for periodic stats display
        """
        # YOUR CODE HERE
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Configure socket...
        return sock
    
    def _display_realtime_stats(self) -> None:
        """Display current statistics to console.
        
        TODO: Implement this method
        - Show packets received, unique senders, rate
        - Use carriage return for updating display
        """
        # YOUR CODE HERE
        pass
    
    def run(self) -> None:
        """Main receiver loop.
        
        TODO: Implement this method
        - Create socket
        - Loop while running
        - Receive packets with timeout
        - Record statistics
        - Display stats periodically
        """
        print(f"=== Enhanced Broadcast Receiver ===")
        print(f"Listening on port {self.port}")
        print(f"Press Ctrl+C to stop and see summary\n")
        
        self.socket = self._create_socket()
        self.running = True
        last_stats_time = time.time()
        
        # YOUR CODE HERE - Main receive loop
        
        print("\nReceiver stopped.")


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Enhanced UDP Broadcast Receiver with Statistics"
    )
    parser.add_argument(
        '--port', '-p',
        type=int,
        default=DEFAULT_PORT,
        help=f"Port to listen on (default: {DEFAULT_PORT})"
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default=None,
        help="Output file for JSON statistics (optional)"
    )
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_arguments()
    
    receiver = BroadcastReceiverStats(
        port=args.port,
        output_file=args.output
    )
    receiver.run()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
