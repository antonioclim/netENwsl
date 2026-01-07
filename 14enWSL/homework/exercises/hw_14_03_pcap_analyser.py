#!/usr/bin/env python3
"""
Homework Assignment 3: Automated Packet Capture Analysis
NETWORKING class - ASE, Informatics | by Revolvix

Week 14 - Computer Networks Laboratory

OBJECTIVE:
Develop a Python tool that analyses PCAP files and generates
comprehensive network traffic reports.

REQUIREMENTS:
1. Parse PCAP files using scapy or pyshark
2. Extract and summarise protocol statistics
3. Identify TCP conversations and their characteristics
4. Detect potential anomalies (retransmissions, resets, etc.)
5. Generate JSON and Markdown reports

ANALYSIS TO IMPLEMENT:

1. PROTOCOL DISTRIBUTION
   - Count packets by protocol (TCP, UDP, ICMP, etc.)
   - Calculate bytes transferred per protocol
   - Show protocol hierarchy (Ethernet -> IP -> TCP -> HTTP)

2. ENDPOINT ANALYSIS
   - List all unique IP addresses
   - Count packets sent/received per endpoint
   - Identify top talkers (by packets and bytes)

3. TCP CONVERSATION ANALYSIS
   - Track TCP streams (SYN -> data -> FIN)
   - Calculate connection durations
   - Count retransmissions per stream
   - Identify incomplete handshakes

4. HTTP ANALYSIS (if applicable)
   - Extract HTTP requests/responses
   - List requested URLs
   - Analyse response codes
   - Calculate response times

5. ANOMALY DETECTION
   - Flag TCP retransmissions (> threshold)
   - Detect RST packets
   - Identify potential port scans
   - Flag unusual packet sizes

REPORT FORMAT:

{
    "summary": {
        "file": "capture.pcap",
        "duration_seconds": 120.5,
        "total_packets": 15000,
        "total_bytes": 1234567
    },
    "protocols": {
        "TCP": {"packets": 12000, "bytes": 1000000},
        "UDP": {"packets": 2500, "bytes": 200000},
        "ICMP": {"packets": 500, "bytes": 34567}
    },
    "endpoints": [
        {"ip": "192.168.1.1", "packets_sent": 5000, "packets_recv": 4500},
        ...
    ],
    "tcp_conversations": [
        {
            "src": "192.168.1.1:54321",
            "dst": "10.0.0.1:80",
            "packets": 150,
            "bytes": 25000,
            "duration_ms": 500,
            "retransmissions": 2,
            "state": "complete"
        },
        ...
    ],
    "http_requests": [
        {"method": "GET", "url": "/api/data", "status": 200, "latency_ms": 45},
        ...
    ],
    "anomalies": [
        {"type": "high_retransmission", "stream": "...", "count": 15},
        {"type": "rst_flood", "target": "10.0.0.1", "count": 100}
    ]
}

DELIVERABLES:
1. hw_14_03_analyser.py - Main analysis tool
2. hw_14_03_report.py - Report generation module
3. hw_14_03_test.py - Test suite with sample PCAPs
4. hw_14_03_sample_report.md - Example generated report

EVALUATION CRITERIA:
- Analysis accuracy (30%)
- Anomaly detection quality (25%)
- Report clarity and completeness (20%)
- Code quality and documentation (15%)
- Performance on large captures (10%)

HINTS:
- Use scapy for packet parsing: pip install scapy
- Consider using pyshark for complex dissection
- Handle large files with iterative processing
- Test with Week 14 lab captures
"""

import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Iterator
from datetime import datetime
import hashlib

# Try to import scapy
try:
    from scapy.all import rdpcap, PcapReader, Ether, IP, TCP, UDP, ICMP, Raw
    from scapy.layers.http import HTTPRequest, HTTPResponse
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False
    print("[WARNING] scapy not installed. Install with: pip install scapy")

# Configuration
DEFAULT_RETRANSMISSION_THRESHOLD = 5
DEFAULT_RST_FLOOD_THRESHOLD = 10


@dataclass
class PacketInfo:
    """Parsed packet information."""
    timestamp: float
    src_ip: str
    dst_ip: str
    src_port: Optional[int]
    dst_port: Optional[int]
    protocol: str
    size: int
    flags: Optional[str] = None
    payload_size: int = 0


@dataclass
class TCPConversation:
    """Represents a TCP conversation/stream."""
    src: str  # ip:port
    dst: str  # ip:port
    packets: int = 0
    bytes: int = 0
    start_time: float = 0
    end_time: float = 0
    syn_count: int = 0
    fin_count: int = 0
    rst_count: int = 0
    retransmissions: int = 0
    
    @property
    def stream_id(self) -> str:
        """Generate unique stream identifier."""
        parts = sorted([self.src, self.dst])
        return f"{parts[0]}<->{parts[1]}"
    
    @property
    def duration_ms(self) -> float:
        if self.end_time > self.start_time:
            return (self.end_time - self.start_time) * 1000
        return 0
    
    @property
    def state(self) -> str:
        """Determine conversation state."""
        if self.rst_count > 0:
            return "reset"
        elif self.syn_count >= 2 and self.fin_count >= 2:
            return "complete"
        elif self.syn_count >= 2:
            return "established"
        elif self.syn_count == 1:
            return "incomplete_handshake"
        return "unknown"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'src': self.src,
            'dst': self.dst,
            'packets': self.packets,
            'bytes': self.bytes,
            'duration_ms': round(self.duration_ms, 2),
            'retransmissions': self.retransmissions,
            'state': self.state
        }


@dataclass
class HTTPTransaction:
    """Represents an HTTP request/response pair."""
    method: str
    url: str
    status: Optional[int] = None
    request_time: float = 0
    response_time: float = 0
    
    @property
    def latency_ms(self) -> float:
        if self.response_time > self.request_time:
            return (self.response_time - self.request_time) * 1000
        return 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'method': self.method,
            'url': self.url,
            'status': self.status,
            'latency_ms': round(self.latency_ms, 2)
        }


@dataclass
class Anomaly:
    """Represents a detected anomaly."""
    anomaly_type: str
    description: str
    severity: str  # low, medium, high
    details: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': self.anomaly_type,
            'description': self.description,
            'severity': self.severity,
            'details': self.details
        }


class PCAPAnalyser:
    """
    PCAP file analyser.
    
    TODO: Implement the analysis methods.
    """
    
    def __init__(self, pcap_path: str):
        """
        Initialise analyser with PCAP file path.
        
        Args:
            pcap_path: Path to PCAP file
        """
        self.pcap_path = Path(pcap_path)
        if not self.pcap_path.exists():
            raise FileNotFoundError(f"PCAP file not found: {pcap_path}")
        
        # Statistics
        self.total_packets = 0
        self.total_bytes = 0
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        
        # Protocol counts
        self.protocols: Dict[str, Dict[str, int]] = defaultdict(
            lambda: {'packets': 0, 'bytes': 0}
        )
        
        # Endpoint statistics
        self.endpoints: Dict[str, Dict[str, int]] = defaultdict(
            lambda: {'packets_sent': 0, 'packets_recv': 0, 'bytes_sent': 0, 'bytes_recv': 0}
        )
        
        # TCP conversations
        self.tcp_conversations: Dict[str, TCPConversation] = {}
        
        # HTTP transactions
        self.http_transactions: List[HTTPTransaction] = []
        
        # Anomalies
        self.anomalies: List[Anomaly] = []
        
        # Sequence tracking for retransmission detection
        self._tcp_sequences: Dict[str, set] = defaultdict(set)
    
    def analyse(self) -> None:
        """
        Perform full analysis of the PCAP file.
        
        This is the main entry point for analysis.
        """
        if not SCAPY_AVAILABLE:
            raise RuntimeError("scapy is required for PCAP analysis")
        
        print(f"Analysing {self.pcap_path}...")
        
        # Process packets
        for packet in self._read_packets():
            self._process_packet(packet)
        
        # Post-processing
        self._detect_anomalies()
        
        print(f"Analysis complete: {self.total_packets} packets processed")
    
    def _read_packets(self) -> Iterator:
        """
        Read packets from PCAP file.
        
        Uses iterator to handle large files efficiently.
        """
        # TODO: Implement packet reading
        # Use PcapReader for large files
        pass
    
    def _process_packet(self, packet) -> None:
        """
        Process a single packet.
        
        Args:
            packet: Scapy packet object
        """
        # TODO: Implement packet processing
        # 1. Update total counts
        # 2. Update protocol statistics
        # 3. Update endpoint statistics
        # 4. If TCP, update conversation tracking
        # 5. If HTTP, track request/response
        pass
    
    def _extract_packet_info(self, packet) -> Optional[PacketInfo]:
        """
        Extract information from packet.
        
        Args:
            packet: Scapy packet object
            
        Returns:
            PacketInfo object or None if packet cannot be parsed
        """
        # TODO: Implement packet info extraction
        # Handle different protocol layers
        pass
    
    def _update_protocol_stats(self, info: PacketInfo) -> None:
        """Update protocol statistics."""
        # TODO: Implement protocol statistics tracking
        pass
    
    def _update_endpoint_stats(self, info: PacketInfo) -> None:
        """Update endpoint statistics."""
        # TODO: Implement endpoint statistics tracking
        pass
    
    def _track_tcp_conversation(self, info: PacketInfo, packet) -> None:
        """
        Track TCP conversation state.
        
        Args:
            info: Extracted packet info
            packet: Original scapy packet
        """
        # TODO: Implement TCP conversation tracking
        # 1. Generate stream ID
        # 2. Create or update conversation
        # 3. Track SYN/FIN/RST flags
        # 4. Detect retransmissions
        pass
    
    def _is_retransmission(self, stream_id: str, seq: int) -> bool:
        """
        Check if packet is a retransmission.
        
        Args:
            stream_id: TCP stream identifier
            seq: TCP sequence number
            
        Returns:
            True if this sequence was already seen
        """
        # TODO: Implement retransmission detection
        # Track seen sequence numbers per stream
        pass
    
    def _detect_anomalies(self) -> None:
        """
        Detect anomalies in the captured traffic.
        
        Called after all packets are processed.
        """
        # TODO: Implement anomaly detection
        # 1. High retransmission rates
        # 2. RST floods
        # 3. Incomplete handshakes
        # 4. Port scan patterns
        # 5. Unusual packet sizes
        pass
    
    def _detect_high_retransmissions(self) -> None:
        """Detect streams with high retransmission rates."""
        for stream_id, conv in self.tcp_conversations.items():
            if conv.retransmissions > DEFAULT_RETRANSMISSION_THRESHOLD:
                rate = conv.retransmissions / max(1, conv.packets) * 100
                self.anomalies.append(Anomaly(
                    anomaly_type="high_retransmission",
                    description=f"Stream {stream_id} has {conv.retransmissions} retransmissions ({rate:.1f}%)",
                    severity="medium" if rate < 10 else "high",
                    details={
                        'stream': stream_id,
                        'retransmissions': conv.retransmissions,
                        'total_packets': conv.packets,
                        'rate_percent': round(rate, 2)
                    }
                ))
    
    def _detect_rst_flood(self) -> None:
        """Detect potential RST flood attacks."""
        rst_by_target: Dict[str, int] = defaultdict(int)
        
        for conv in self.tcp_conversations.values():
            if conv.rst_count > 0:
                # Count RSTs by destination
                rst_by_target[conv.dst.split(':')[0]] += conv.rst_count
        
        for target, count in rst_by_target.items():
            if count > DEFAULT_RST_FLOOD_THRESHOLD:
                self.anomalies.append(Anomaly(
                    anomaly_type="rst_flood",
                    description=f"Potential RST flood targeting {target} ({count} RST packets)",
                    severity="high",
                    details={'target': target, 'rst_count': count}
                ))
    
    def _detect_port_scan(self) -> None:
        """Detect potential port scan patterns."""
        # TODO: Implement port scan detection
        # Look for many connections from same source to different ports
        pass
    
    def get_summary(self) -> Dict[str, Any]:
        """Get analysis summary."""
        duration = 0
        if self.start_time and self.end_time:
            duration = self.end_time - self.start_time
        
        return {
            'file': str(self.pcap_path),
            'duration_seconds': round(duration, 2),
            'total_packets': self.total_packets,
            'total_bytes': self.total_bytes
        }
    
    def get_top_talkers(self, n: int = 10) -> List[Dict[str, Any]]:
        """
        Get top N endpoints by traffic.
        
        Args:
            n: Number of top talkers to return
            
        Returns:
            List of endpoint dictionaries sorted by total bytes
        """
        endpoints = []
        for ip, stats in self.endpoints.items():
            total_bytes = stats['bytes_sent'] + stats['bytes_recv']
            endpoints.append({
                'ip': ip,
                'packets_sent': stats['packets_sent'],
                'packets_recv': stats['packets_recv'],
                'bytes_sent': stats['bytes_sent'],
                'bytes_recv': stats['bytes_recv'],
                'total_bytes': total_bytes
            })
        
        return sorted(endpoints, key=lambda x: x['total_bytes'], reverse=True)[:n]
    
    def generate_report(self) -> Dict[str, Any]:
        """
        Generate complete analysis report.
        
        Returns:
            Dictionary containing full analysis results
        """
        return {
            'summary': self.get_summary(),
            'protocols': dict(self.protocols),
            'endpoints': self.get_top_talkers(20),
            'tcp_conversations': [
                conv.to_dict() for conv in self.tcp_conversations.values()
            ],
            'http_requests': [
                tx.to_dict() for tx in self.http_transactions
            ],
            'anomalies': [
                anomaly.to_dict() for anomaly in self.anomalies
            ]
        }
    
    def save_json_report(self, output_path: str) -> None:
        """Save report as JSON."""
        report = self.generate_report()
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"JSON report saved to {output_path}")
    
    def save_markdown_report(self, output_path: str) -> None:
        """Save report as Markdown."""
        report = self.generate_report()
        
        md = []
        md.append("# PCAP Analysis Report\n")
        md.append(f"Generated: {datetime.now().isoformat()}\n")
        
        # Summary
        md.append("## Summary\n")
        summary = report['summary']
        md.append(f"- **File:** {summary['file']}")
        md.append(f"- **Duration:** {summary['duration_seconds']} seconds")
        md.append(f"- **Total Packets:** {summary['total_packets']:,}")
        md.append(f"- **Total Bytes:** {summary['total_bytes']:,}")
        md.append("")
        
        # Protocols
        md.append("## Protocol Distribution\n")
        md.append("| Protocol | Packets | Bytes |")
        md.append("|----------|---------|-------|")
        for proto, stats in report['protocols'].items():
            md.append(f"| {proto} | {stats['packets']:,} | {stats['bytes']:,} |")
        md.append("")
        
        # Top Talkers
        md.append("## Top Endpoints\n")
        md.append("| IP Address | Packets Sent | Packets Recv | Total Bytes |")
        md.append("|------------|--------------|--------------|-------------|")
        for ep in report['endpoints'][:10]:
            md.append(f"| {ep['ip']} | {ep['packets_sent']:,} | {ep['packets_recv']:,} | {ep['total_bytes']:,} |")
        md.append("")
        
        # TCP Conversations
        md.append("## TCP Conversations\n")
        md.append("| Source | Destination | Packets | Duration (ms) | State |")
        md.append("|--------|-------------|---------|---------------|-------|")
        for conv in report['tcp_conversations'][:20]:
            md.append(f"| {conv['src']} | {conv['dst']} | {conv['packets']} | {conv['duration_ms']} | {conv['state']} |")
        md.append("")
        
        # Anomalies
        if report['anomalies']:
            md.append("## Detected Anomalies\n")
            for anomaly in report['anomalies']:
                md.append(f"### {anomaly['type']} ({anomaly['severity']})\n")
                md.append(f"{anomaly['description']}\n")
        
        # Write file
        with open(output_path, 'w') as f:
            f.write('\n'.join(md))
        print(f"Markdown report saved to {output_path}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="PCAP File Analyser - Homework Assignment 3",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="NETWORKING class - ASE, Informatics | by Revolvix"
    )
    
    parser.add_argument(
        'pcap_file',
        help='Path to PCAP file to analyse'
    )
    parser.add_argument(
        '-o', '--output',
        default='report',
        help='Output file base name (default: report)'
    )
    parser.add_argument(
        '-f', '--format',
        choices=['json', 'markdown', 'both'],
        default='both',
        help='Output format (default: both)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("PCAP Analyser - Homework Assignment 3")
    print("NETWORKING class - ASE, Informatics")
    print("=" * 50)
    print()
    
    if not SCAPY_AVAILABLE:
        print("[ERROR] scapy is required. Install with:")
        print("  pip install scapy")
        return 1
    
    try:
        analyser = PCAPAnalyser(args.pcap_file)
        analyser.analyse()
        
        if args.format in ('json', 'both'):
            analyser.save_json_report(f"{args.output}.json")
        
        if args.format in ('markdown', 'both'):
            analyser.save_markdown_report(f"{args.output}.md")
        
        # Print summary
        summary = analyser.get_summary()
        print()
        print("Analysis Summary:")
        print(f"  Packets: {summary['total_packets']:,}")
        print(f"  Bytes: {summary['total_bytes']:,}")
        print(f"  Duration: {summary['duration_seconds']} seconds")
        print(f"  Protocols: {len(analyser.protocols)}")
        print(f"  Endpoints: {len(analyser.endpoints)}")
        print(f"  TCP Conversations: {len(analyser.tcp_conversations)}")
        print(f"  Anomalies: {len(analyser.anomalies)}")
        
        return 0
        
    except Exception as e:
        print(f"[ERROR] {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
