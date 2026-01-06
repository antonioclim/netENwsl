#!/usr/bin/env python3
"""
Homework 2.2: Protocol Analyser
NETWORKING class - ASE, Informatics | by Revolvix

Analyse PCAP files to extract TCP and UDP statistics.

Requirements:
- Parse PCAP files (using scapy or raw parsing)
- Identify TCP connections and handshakes
- Calculate connection statistics
- Analyse UDP flows

Usage:
    python hw_2_02.py <pcap_file>     # Analyse a capture file
    python hw_2_02.py --test          # Run self-tests

Dependencies:
    pip install scapy
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

# Attempt to import scapy
try:
    from scapy.all import rdpcap, TCP, UDP, IP
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False
    print("Warning: scapy not installed. Install with: pip install scapy")


# =============================================================================
# Data structures for tracking connections
# =============================================================================

@dataclass
class TCPConnection:
    """Represents a TCP connection for analysis."""
    src_ip: str
    src_port: int
    dst_ip: str
    dst_port: int
    
    # TODO: Add fields to track
    syn_seen: bool = False
    syn_ack_seen: bool = False
    ack_seen: bool = False
    fin_seen: bool = False
    
    bytes_sent: int = 0
    bytes_received: int = 0
    
    start_time: float | None = None
    end_time: float | None = None
    
    @property
    def handshake_complete(self) -> bool:
        """Check if three-way handshake was observed."""
        # TODO: Implement
        return self.syn_seen and self.syn_ack_seen and self.ack_seen
    
    @property
    def duration(self) -> float | None:
        """Calculate connection duration in seconds."""
        # TODO: Implement
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None
    
    def connection_key(self) -> tuple:
        """Generate unique key for this connection (bidirectional)."""
        # TODO: Ensure same key for both directions
        endpoints = sorted([
            (self.src_ip, self.src_port),
            (self.dst_ip, self.dst_port)
        ])
        return tuple(endpoints)


@dataclass
class UDPFlow:
    """Represents a UDP flow for analysis."""
    src_ip: str
    src_port: int
    dst_ip: str
    dst_port: int
    
    datagram_count: int = 0
    total_bytes: int = 0
    
    @property
    def avg_datagram_size(self) -> float:
        """Calculate average datagram size."""
        if self.datagram_count == 0:
            return 0.0
        return self.total_bytes / self.datagram_count
    
    def flow_key(self) -> tuple:
        """Generate unique key for this flow (bidirectional)."""
        endpoints = sorted([
            (self.src_ip, self.src_port),
            (self.dst_ip, self.dst_port)
        ])
        return tuple(endpoints)


@dataclass
class AnalysisResult:
    """Container for analysis results."""
    tcp_connections: dict[tuple, TCPConnection] = field(default_factory=dict)
    udp_flows: dict[tuple, UDPFlow] = field(default_factory=dict)
    
    @property
    def total_tcp_connections(self) -> int:
        return len(self.tcp_connections)
    
    @property
    def complete_handshakes(self) -> int:
        return sum(1 for c in self.tcp_connections.values() if c.handshake_complete)
    
    @property
    def total_udp_flows(self) -> int:
        return len(self.udp_flows)


# =============================================================================
# TODO: Implement PCAP analysis
# =============================================================================

def analyse_pcap(filepath: Path) -> AnalysisResult:
    """
    Analyse a PCAP file and extract TCP/UDP statistics.
    
    Args:
        filepath: Path to the PCAP file
    
    Returns:
        AnalysisResult containing all statistics
    """
    if not SCAPY_AVAILABLE:
        raise RuntimeError("scapy is required for PCAP analysis")
    
    result = AnalysisResult()
    
    # TODO: Read PCAP file
    # packets = rdpcap(str(filepath))
    
    # TODO: Process each packet
    # for packet in packets:
    #     if TCP in packet:
    #         process_tcp_packet(packet, result)
    #     elif UDP in packet:
    #         process_udp_packet(packet, result)
    
    raise NotImplementedError("Implement analyse_pcap()")


def process_tcp_packet(packet: Any, result: AnalysisResult) -> None:
    """
    Process a TCP packet and update connection tracking.
    
    Args:
        packet: Scapy packet with TCP layer
        result: AnalysisResult to update
    """
    # TODO: Extract connection info
    # src_ip = packet[IP].src
    # dst_ip = packet[IP].dst
    # src_port = packet[TCP].sport
    # dst_port = packet[TCP].dport
    
    # TODO: Track TCP flags
    # flags = packet[TCP].flags
    # SYN = 0x02, ACK = 0x10, FIN = 0x01, SYN-ACK = 0x12
    
    # TODO: Update connection state
    # - Create new connection if not seen
    # - Update flags seen
    # - Track bytes transferred
    # - Update timestamps
    
    raise NotImplementedError("Implement process_tcp_packet()")


def process_udp_packet(packet: Any, result: AnalysisResult) -> None:
    """
    Process a UDP packet and update flow tracking.
    
    Args:
        packet: Scapy packet with UDP layer
        result: AnalysisResult to update
    """
    # TODO: Extract flow info
    # src_ip = packet[IP].src
    # dst_ip = packet[IP].dst
    # src_port = packet[UDP].sport
    # dst_port = packet[UDP].dport
    # length = len(packet[UDP].payload)
    
    # TODO: Update flow statistics
    # - Create new flow if not seen
    # - Increment datagram count
    # - Add to total bytes
    
    raise NotImplementedError("Implement process_udp_packet()")


# =============================================================================
# TODO: Implement output formatting
# =============================================================================

def format_results(result: AnalysisResult) -> str:
    """
    Format analysis results for display.
    
    Args:
        result: AnalysisResult to format
    
    Returns:
        Formatted string for printing
    """
    lines = []
    
    # TODO: Format TCP section
    lines.append("=" * 50)
    lines.append("TCP Analysis")
    lines.append("=" * 50)
    lines.append(f"Total connections: {result.total_tcp_connections}")
    lines.append(f"Complete handshakes: {result.complete_handshakes}")
    lines.append("")
    
    # TODO: Add per-connection details
    # for i, (key, conn) in enumerate(result.tcp_connections.items(), 1):
    #     lines.append(f"Connection {i}: {conn.src_ip}:{conn.src_port} → {conn.dst_ip}:{conn.dst_port}")
    #     if conn.duration:
    #         lines.append(f"  Duration: {conn.duration:.3f}s")
    #     lines.append(f"  Bytes sent: {conn.bytes_sent}")
    #     lines.append(f"  Bytes received: {conn.bytes_received}")
    #     lines.append("")
    
    # TODO: Format UDP section
    lines.append("=" * 50)
    lines.append("UDP Analysis")
    lines.append("=" * 50)
    lines.append(f"Total unique flows: {result.total_udp_flows}")
    lines.append("")
    
    # TODO: Add per-flow details
    # for i, (key, flow) in enumerate(result.udp_flows.items(), 1):
    #     lines.append(f"Flow {i}: {flow.src_ip}:{flow.src_port} ↔ {flow.dst_ip}:{flow.dst_port}")
    #     lines.append(f"  Datagrams: {flow.datagram_count}")
    #     lines.append(f"  Avg size: {flow.avg_datagram_size:.0f} bytes")
    #     lines.append("")
    
    return "\n".join(lines)


# =============================================================================
# Self-tests
# =============================================================================

def run_tests() -> None:
    """Run basic self-tests."""
    print("Running self-tests...")
    
    # Test TCP connection tracking
    conn = TCPConnection(
        src_ip="192.168.1.1",
        src_port=12345,
        dst_ip="192.168.1.2",
        dst_port=80
    )
    
    # Initially no handshake
    assert not conn.handshake_complete, "Handshake should not be complete initially"
    print("✓ Initial handshake state correct")
    
    # Simulate handshake
    conn.syn_seen = True
    conn.syn_ack_seen = True
    conn.ack_seen = True
    assert conn.handshake_complete, "Handshake should be complete after all flags"
    print("✓ Handshake completion detection works")
    
    # Test duration calculation
    conn.start_time = 1000.0
    conn.end_time = 1001.5
    assert conn.duration == 1.5, f"Duration should be 1.5, got {conn.duration}"
    print("✓ Duration calculation works")
    
    # Test UDP flow
    flow = UDPFlow(
        src_ip="192.168.1.1",
        src_port=53421,
        dst_ip="8.8.8.8",
        dst_port=53
    )
    flow.datagram_count = 4
    flow.total_bytes = 256
    assert flow.avg_datagram_size == 64.0, f"Avg should be 64, got {flow.avg_datagram_size}"
    print("✓ UDP average size calculation works")
    
    # Test connection key bidirectionality
    conn2 = TCPConnection(
        src_ip="192.168.1.2",
        src_port=80,
        dst_ip="192.168.1.1",
        dst_port=12345
    )
    assert conn.connection_key() == conn2.connection_key(), "Keys should match for reverse direction"
    print("✓ Bidirectional key generation works")
    
    print("\n✓ All tests passed!")
    print("\nNow implement the PCAP analysis functions and test with real captures.")


# =============================================================================
# Main entry point
# =============================================================================

def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Protocol Analyser - PCAP statistics"
    )
    parser.add_argument(
        "pcap_file",
        nargs="?",
        help="PCAP file to analyse"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run self-tests"
    )
    
    args = parser.parse_args()
    
    if args.test:
        run_tests()
        return 0
    
    if not args.pcap_file:
        parser.print_help()
        return 1
    
    filepath = Path(args.pcap_file)
    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        return 1
    
    try:
        print(f"Analysing: {filepath}")
        print()
        result = analyse_pcap(filepath)
        print(format_results(result))
        return 0
    
    except NotImplementedError as e:
        print(f"Not implemented: {e}")
        print("\nComplete the TODO sections to enable analysis.")
        return 1
    
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
