#!/usr/bin/env python3
"""
Homework 1.02: PCAP Traffic Analyser
====================================
Computer Networks - Week 1 (WSL Environment)
ASE Bucharest | by ing. dr. Antonio Clim

Assignment: Complete this script to analyse network traffic from a PCAP file.

Objectives:
- Apply packet parsing techniques using the dpkt library
- Analyse protocol distribution across captured traffic
- Identify communication patterns between network hosts
- Generate summary statistics from raw packet data

Prerequisites:
- dpkt library installed: pip install dpkt --break-system-packages
- Understanding of IP packet structure
- Familiarity with TCP/UDP protocols

Level: Intermediate
Estimated time: 60-90 minutes

Pair Programming Notes:
- Driver: Implement the parsing logic
- Navigator: Verify packet structure assumptions against RFC
- Swap after: Completing each function

Due: Next laboratory session

Grading Criteria:
- Correct packet parsing: 2 points
- Protocol identification: 2 points
- Traffic statistics: 3 points
- Report formatting: 2 points
- Code quality: 1 point
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import dpkt
import socket
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field


# ═══════════════════════════════════════════════════════════════════════════════
# DATA_STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class TrafficStatistics:
    """
    Container for traffic analysis results.
    
    Attributes:
        total_packets: Count of all packets processed
        total_bytes: Sum of all packet sizes
        protocols: Mapping of protocol name to packet count
        source_ips: Mapping of source IP to packet count
        dest_ips: Mapping of destination IP to packet count
        conversations: Mapping of (src, dst) tuple to packet count
        packets_per_second: Mapping of timestamp (seconds) to packet count
        start_time: Timestamp of first packet
        end_time: Timestamp of last packet
    """
    total_packets: int = 0
    total_bytes: int = 0
    protocols: Dict[str, int] = field(default_factory=dict)
    source_ips: Dict[str, int] = field(default_factory=dict)
    dest_ips: Dict[str, int] = field(default_factory=dict)
    conversations: Dict[Tuple[str, str], int] = field(default_factory=dict)
    packets_per_second: Dict[int, int] = field(default_factory=dict)
    start_time: Optional[float] = None
    end_time: Optional[float] = None


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def ip_to_string(packed_ip: bytes) -> str:
    """
    Convert packed IP address to human-readable string.
    
    Args:
        packed_ip: 4-byte packed IP address (network byte order)
        
    Returns:
        Dotted decimal string representation
        
    Example:
        >>> ip_to_string(b'\\xc0\\xa8\\x01\\x01')
        '192.168.1.1'
    """
    return socket.inet_ntoa(packed_ip)


# ═══════════════════════════════════════════════════════════════════════════════
# PROTOCOL_IDENTIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def identify_transport_protocol(ip_packet) -> str:
    """
    Identify the transport layer protocol from an IP packet.
    
    Args:
        ip_packet: dpkt IP packet object with .p attribute
        
    Returns:
        Protocol name: "TCP", "UDP", "ICMP", or "OTHER"
        
    TODO: Complete this function
    Hint: Compare ip_packet.p against dpkt.ip.IP_PROTO_* constants
    
    Example:
        >>> # If ip_packet.p == 6 (TCP)
        >>> identify_transport_protocol(ip_packet)
        'TCP'
    """
    # TODO: Implement protocol identification
    # Protocol numbers: TCP=6, UDP=17, ICMP=1
    #
    # if ip_packet.p == dpkt.ip.IP_PROTO_TCP:
    #     return "TCP"
    # elif ip_packet.p == dpkt.ip.IP_PROTO_UDP:
    #     return "UDP"
    # elif ip_packet.p == dpkt.ip.IP_PROTO_ICMP:
    #     return "ICMP"
    # else:
    #     return "OTHER"
    pass


# ═══════════════════════════════════════════════════════════════════════════════
# PACKET_PARSING
# ═══════════════════════════════════════════════════════════════════════════════
def parse_pcap(filepath: str) -> TrafficStatistics:
    """
    Parse a PCAP file and extract detailed traffic statistics.
    
    This function iterates through all packets in the capture file,
    extracting IP-level information and aggregating statistics.
    
    Args:
        filepath: Path to PCAP file
        
    Returns:
        TrafficStatistics object with analysis results
        
    TODO: Complete this function following the steps below
    """
    stats = TrafficStatistics()
    
    with open(filepath, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        
        for timestamp, buf in pcap:
            # ─────────────────────────────────────────────────────────────────
            # STEP 1: Parse Ethernet frame
            # ─────────────────────────────────────────────────────────────────
            # TODO: Uncomment and use:
            # eth = dpkt.ethernet.Ethernet(buf)
            
            # ─────────────────────────────────────────────────────────────────
            # STEP 2: Check if payload is IP packet
            # ─────────────────────────────────────────────────────────────────
            # TODO: Check isinstance(eth.data, dpkt.ip.IP)
            # If not IP, skip this packet with 'continue'
            
            # ─────────────────────────────────────────────────────────────────
            # STEP 3: Extract IP information
            # ─────────────────────────────────────────────────────────────────
            # TODO: Get the IP packet: ip = eth.data
            # Extract: source IP, destination IP, packet length
            
            # ─────────────────────────────────────────────────────────────────
            # STEP 4: Update counters
            # ─────────────────────────────────────────────────────────────────
            # TODO: Increment:
            # - stats.total_packets
            # - stats.total_bytes (use len(buf))
            # - stats.source_ips[src_ip]
            # - stats.dest_ips[dst_ip]
            # - stats.protocols[protocol_name]
            
            # ─────────────────────────────────────────────────────────────────
            # STEP 5: Track timestamps
            # ─────────────────────────────────────────────────────────────────
            # TODO: Update start_time (first packet) and end_time (last packet)
            # Also update packets_per_second[int(timestamp)]
            
            pass
    
    return stats


# ═══════════════════════════════════════════════════════════════════════════════
# STATISTICS_CALCULATION
# ═══════════════════════════════════════════════════════════════════════════════
def calculate_top_talkers(stats: TrafficStatistics, n: int = 5) -> List[Tuple[str, int]]:
    """
    Find the top N source IP addresses by packet count.
    
    Args:
        stats: TrafficStatistics object with source_ips populated
        n: Number of top talkers to return (default: 5)
        
    Returns:
        List of (ip_address, packet_count) tuples, sorted descending
        
    TODO: Complete this function
    Hint: Use sorted() with a key function, or Counter.most_common()
    """
    # TODO: Sort source_ips by count and return top N
    # return sorted(stats.source_ips.items(), key=lambda x: x[1], reverse=True)[:n]
    pass


def calculate_conversation_pairs(stats: TrafficStatistics) -> List[Tuple[str, str, int]]:
    """
    Get unique conversation pairs (source-dest) and their packet counts.
    
    Args:
        stats: TrafficStatistics object with conversations populated
        
    Returns:
        List of (source_ip, dest_ip, packet_count) tuples
        
    TODO: Complete this function
    """
    # TODO: Return sorted conversation pairs
    # return [(src, dst, count) for (src, dst), count in 
    #         sorted(stats.conversations.items(), key=lambda x: x[1], reverse=True)]
    pass


def calculate_duration(stats: TrafficStatistics) -> float:
    """
    Calculate capture duration in seconds.
    
    Args:
        stats: TrafficStatistics object with start_time and end_time
        
    Returns:
        Duration in seconds, or 0.0 if timestamps not available
        
    TODO: Complete this function
    """
    # TODO: Return end_time - start_time (handle None case)
    pass


def calculate_throughput(stats: TrafficStatistics) -> float:
    """
    Calculate average throughput in bits per second.
    
    Args:
        stats: TrafficStatistics object
        
    Returns:
        Throughput in bps, or 0.0 if duration is zero
        
    TODO: Complete this function
    """
    # TODO: Calculate (total_bytes * 8) / duration
    # Remember to handle division by zero
    pass


# ═══════════════════════════════════════════════════════════════════════════════
# REPORT_GENERATION
# ═══════════════════════════════════════════════════════════════════════════════
def generate_report(stats: TrafficStatistics) -> str:
    """
    Generate a formatted text report of traffic statistics.
    
    Args:
        stats: TrafficStatistics object with all fields populated
        
    Returns:
        Formatted multi-line report string
        
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
        # TODO: Add duration using calculate_duration()
        # TODO: Add average throughput using calculate_throughput()
        "",
        "PROTOCOL DISTRIBUTION",
        "-" * 40,
        # TODO: Add protocol counts and percentages
        # for protocol, count in sorted(stats.protocols.items()):
        #     pct = 100 * count / stats.total_packets if stats.total_packets else 0
        #     report_lines.append(f"  {protocol}: {count} ({pct:.1f}%)")
        "",
        "TOP SOURCE ADDRESSES",
        "-" * 40,
        # TODO: Add top 5 source IPs using calculate_top_talkers()
        "",
        "TOP DESTINATION ADDRESSES",
        "-" * 40,
        # TODO: Add top 5 destination IPs
        "",
        "=" * 60,
    ]
    
    return "\n".join(report_lines)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point for the homework assignment."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Analyse network traffic from PCAP file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python hw_1_02_pcap_analyser.py capture.pcap
  python hw_1_02_pcap_analyser.py capture.pcap --output report.txt
  python hw_1_02_pcap_analyser.py capture.pcap --json
        """
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
