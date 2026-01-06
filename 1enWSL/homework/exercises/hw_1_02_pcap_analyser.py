#!/usr/bin/env python3
"""
Homework 1.02: PCAP Traffic Analyser
NETWORKING class - ASE, Informatics | by Revolvix

Assignment: Complete this script to analyse network traffic from a PCAP file.

Objectives:
    1. Parse PCAP file using dpkt library
    2. Calculate protocol distribution
    3. Identify unique IP addresses
    4. Measure traffic volume over time
    5. Generate summary report

Due: Next laboratory session

Instructions:
    1. Complete all functions marked with TODO
    2. Run verification: python -m pytest tests/test_homework.py -k hw_1_02
    3. Submit via the course portal

Grading Criteria:
    - Correct packet parsing: 2 points
    - Protocol identification: 2 points
    - Traffic statistics: 3 points
    - Report formatting: 2 points
    - Code quality: 1 point
"""

import dpkt
import socket
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class TrafficStatistics:
    """Container for traffic analysis results."""
    total_packets: int = 0
    total_bytes: int = 0
    protocols: Dict[str, int] = field(default_factory=dict)
    source_ips: Dict[str, int] = field(default_factory=dict)
    dest_ips: Dict[str, int] = field(default_factory=dict)
    conversations: Dict[Tuple[str, str], int] = field(default_factory=dict)
    packets_per_second: Dict[int, int] = field(default_factory=dict)
    start_time: Optional[float] = None
    end_time: Optional[float] = None


def ip_to_string(packed_ip: bytes) -> str:
    """
    Convert packed IP address to string representation.
    
    Args:
        packed_ip: 4-byte packed IP address
        
    Returns:
        Dotted decimal string (e.g., "192.168.1.1")
    """
    return socket.inet_ntoa(packed_ip)


def identify_transport_protocol(ip_packet) -> str:
    """
    Identify the transport layer protocol.
    
    Args:
        ip_packet: dpkt IP packet object
        
    Returns:
        Protocol name: "TCP", "UDP", "ICMP", or "OTHER"
        
    TODO: Complete this function
    Hint: Check ip_packet.p against dpkt.ip.IP_PROTO_* constants
    """
    # TODO: Implement protocol identification
    # if ip_packet.p == dpkt.ip.IP_PROTO_TCP:
    #     return "TCP"
    # ...
    pass


def parse_pcap(filepath: str) -> TrafficStatistics:
    """
    Parse a PCAP file and extract traffic statistics.
    
    Args:
        filepath: Path to PCAP file
        
    Returns:
        TrafficStatistics object with analysis results
        
    TODO: Complete this function
    """
    stats = TrafficStatistics()
    
    with open(filepath, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        
        for timestamp, buf in pcap:
            # TODO: Parse Ethernet frame
            # eth = dpkt.ethernet.Ethernet(buf)
            
            # TODO: Check if it's an IP packet
            # if isinstance(eth.data, dpkt.ip.IP):
            
            # TODO: Extract and count:
            # - Total packets
            # - Total bytes
            # - Source IP addresses
            # - Destination IP addresses
            # - Transport protocol
            # - Timestamp for packets per second
            
            pass
    
    return stats


def calculate_top_talkers(stats: TrafficStatistics, n: int = 5) -> List[Tuple[str, int]]:
    """
    Find the top N source IP addresses by packet count.
    
    Args:
        stats: TrafficStatistics object
        n: Number of top talkers to return
        
    Returns:
        List of (ip_address, packet_count) tuples, sorted descending
        
    TODO: Complete this function
    """
    # TODO: Sort source_ips by count and return top N
    pass


def calculate_conversation_pairs(stats: TrafficStatistics) -> List[Tuple[str, str, int]]:
    """
    Find unique conversation pairs (source-dest) and their packet counts.
    
    Args:
        stats: TrafficStatistics object
        
    Returns:
        List of (source_ip, dest_ip, packet_count) tuples
        
    TODO: Complete this function
    """
    # TODO: Return sorted conversation pairs
    pass


def calculate_duration(stats: TrafficStatistics) -> float:
    """
    Calculate capture duration in seconds.
    
    Args:
        stats: TrafficStatistics object
        
    Returns:
        Duration in seconds
        
    TODO: Complete this function
    """
    # TODO: Return end_time - start_time
    pass


def calculate_throughput(stats: TrafficStatistics) -> float:
    """
    Calculate average throughput in bits per second.
    
    Args:
        stats: TrafficStatistics object
        
    Returns:
        Throughput in bps
        
    TODO: Complete this function
    """
    # TODO: Calculate (total_bytes * 8) / duration
    pass


def generate_report(stats: TrafficStatistics) -> str:
    """
    Generate a formatted text report of traffic statistics.
    
    Args:
        stats: TrafficStatistics object
        
    Returns:
        Formatted report string
        
    TODO: Complete this function with all statistics
    """
    report_lines = [
        "=" * 60,
        "PCAP Traffic Analysis Report",
        "=" * 60,
        "",
        "SUMMARY",
        "-" * 40,
        f"Total Packets: {stats.total_packets}",
        f"Total Bytes: {stats.total_bytes:,}",
        # TODO: Add duration
        # TODO: Add average throughput
        "",
        "PROTOCOL DISTRIBUTION",
        "-" * 40,
        # TODO: Add protocol counts and percentages
        "",
        "TOP SOURCE ADDRESSES",
        "-" * 40,
        # TODO: Add top 5 source IPs
        "",
        "TOP DESTINATION ADDRESSES",
        "-" * 40,
        # TODO: Add top 5 destination IPs
        "",
        "=" * 60,
    ]
    
    return "\n".join(report_lines)


def main():
    """Main entry point for the homework assignment."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Analyse network traffic from PCAP file"
    )
    parser.add_argument(
        "pcap_file",
        help="Path to PCAP file to analyse"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file for report (default: stdout)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format"
    )
    args = parser.parse_args()
    
    # Verify file exists
    pcap_path = Path(args.pcap_file)
    if not pcap_path.exists():
        print(f"Error: File not found: {args.pcap_file}")
        return 1
    
    # Parse and analyse
    print(f"Analysing: {args.pcap_file}")
    stats = parse_pcap(args.pcap_file)
    
    # Generate output
    if args.json:
        import json
        output = json.dumps({
            "total_packets": stats.total_packets,
            "total_bytes": stats.total_bytes,
            "protocols": stats.protocols,
            "unique_sources": len(stats.source_ips),
            "unique_destinations": len(stats.dest_ips),
        }, indent=2)
    else:
        output = generate_report(stats)
    
    # Write output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Report written to: {args.output}")
    else:
        print(output)
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
