#!/usr/bin/env python3
"""
Homework 6.1: NAT Translation Analysis
======================================
Computer Networks - Week 6 (WSL Environment)
ASE Bucharest, CSIE | by ing. dr. Antonio Clim

Objectives:
- Analyse NAT translation tables and understand connection tracking
- Identify port forwarding rules and their effects
- Trace packet flow through NAT devices

Level: Intermediate (⭐⭐)
Estimated time: 45-60 minutes

Learning Objectives Covered:
- LO2: Explain PAT translation tables
- LO3: Implement NAT/MASQUERADE

Usage:
    python homework/exercises/hw_6_01_nat_analysis.py
    python homework/exercises/hw_6_01_nat_analysis.py --verbose
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

# ═══════════════════════════════════════════════════════════════════════════════
# LOGGING_CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMERATIONS
# ═══════════════════════════════════════════════════════════════════════════════

class ConnectionState(Enum):
    """TCP connection states in conntrack."""
    NONE = "NONE"
    SYN_SENT = "SYN_SENT"
    SYN_RECV = "SYN_RECV"
    ESTABLISHED = "ESTABLISHED"
    FIN_WAIT = "FIN_WAIT"
    CLOSE_WAIT = "CLOSE_WAIT"
    LAST_ACK = "LAST_ACK"
    TIME_WAIT = "TIME_WAIT"
    CLOSE = "CLOSE"
    
    @classmethod
    def from_string(cls, value: str) -> "ConnectionState":
        """Parse state from string, with fallback."""
        try:
            return cls(value.upper())
        except ValueError:
            return cls.NONE


class Protocol(Enum):
    """IP protocol types."""
    TCP = "tcp"
    UDP = "udp"
    ICMP = "icmp"
    OTHER = "other"
    
    @classmethod
    def from_string(cls, value: str) -> "Protocol":
        """Parse protocol from string."""
        mapping = {"tcp": cls.TCP, "udp": cls.UDP, "icmp": cls.ICMP}
        return mapping.get(value.lower(), cls.OTHER)


# ═══════════════════════════════════════════════════════════════════════════════
# DATA_STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class NATEntry:
    """
    Represents a NAT translation table entry (conntrack).
    
    Attributes:
        protocol: Network protocol (TCP/UDP/ICMP)
        internal_ip: Original source IP (private network)
        internal_port: Original source port
        external_ip: Translated source IP (NAT public IP)
        external_port: Translated source port (assigned by NAT)
        destination_ip: Remote server IP
        destination_port: Remote server port
        state: TCP connection state (if applicable)
        timeout: Seconds until entry expires
    """
    protocol: Protocol
    internal_ip: str
    internal_port: int
    external_ip: str
    external_port: int
    destination_ip: str
    destination_port: int
    state: ConnectionState
    timeout: int
    
    def __post_init__(self) -> None:
        """Validate entry after initialisation."""
        if not self._is_valid_ip(self.internal_ip):
            logger.warning(f"Invalid internal IP: {self.internal_ip}")
        if not self._is_valid_ip(self.destination_ip):
            logger.warning(f"Invalid destination IP: {self.destination_ip}")
    
    @staticmethod
    def _is_valid_ip(ip: str) -> bool:
        """Validate IPv4 address format."""
        if not ip:
            return False
        parts = ip.split(".")
        if len(parts) != 4:
            return False
        try:
            return all(0 <= int(p) <= 255 for p in parts)
        except ValueError:
            return False
    
    def is_established(self) -> bool:
        """Check if connection is established."""
        return self.state == ConnectionState.ESTABLISHED
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert entry to dictionary for JSON export."""
        return {
            "protocol": self.protocol.value,
            "internal": f"{self.internal_ip}:{self.internal_port}",
            "external": f"{self.external_ip}:{self.external_port}",
            "destination": f"{self.destination_ip}:{self.destination_port}",
            "state": self.state.value,
            "timeout": self.timeout,
        }


@dataclass
class PortForwardRule:
    """
    Represents a port forwarding rule (DNAT).
    
    Attributes:
        external_port: Port exposed on NAT public IP
        internal_ip: Target internal server IP
        internal_port: Target internal server port
        protocol: Network protocol
        description: Human-readable description
        enabled: Whether rule is active
    """
    external_port: int
    internal_ip: str
    internal_port: int
    protocol: Protocol
    description: str
    enabled: bool = True
    
    def matches(self, port: int, proto: Optional[Protocol] = None) -> bool:
        """Check if this rule matches the given port and protocol."""
        if self.external_port != port:
            return False
        if proto and self.protocol != proto:
            return False
        return self.enabled


@dataclass
class AnalysisResult:
    """Container for analysis results."""
    total_entries: int = 0
    by_protocol: Dict[str, int] = field(default_factory=dict)
    by_state: Dict[str, int] = field(default_factory=dict)
    by_host: Dict[str, int] = field(default_factory=dict)
    by_destination: Dict[str, int] = field(default_factory=dict)
    established_count: int = 0
    warnings: List[str] = field(default_factory=list)


# ═══════════════════════════════════════════════════════════════════════════════
# SAMPLE_DATA
# ═══════════════════════════════════════════════════════════════════════════════

SAMPLE_CONNTRACK = """
tcp      6 431999 ESTABLISHED src=192.168.1.10 dst=8.8.8.8 sport=45678 dport=443 src=8.8.8.8 dst=203.0.113.1 sport=443 dport=50001 [ASSURED] mark=0 use=1
tcp      6 117 TIME_WAIT src=192.168.1.10 dst=93.184.216.34 sport=45679 dport=80 src=93.184.216.34 dst=203.0.113.1 sport=80 dport=50002 [ASSURED] mark=0 use=1
udp      17 28 src=192.168.1.20 dst=8.8.8.8 sport=53421 dport=53 src=8.8.8.8 dst=203.0.113.1 sport=53 dport=50003 mark=0 use=1
tcp      6 431800 ESTABLISHED src=192.168.1.10 dst=142.250.185.46 sport=45680 dport=443 src=142.250.185.46 dst=203.0.113.1 sport=443 dport=50004 [ASSURED] mark=0 use=1
tcp      6 431700 ESTABLISHED src=192.168.1.20 dst=8.8.8.8 sport=45681 dport=443 src=8.8.8.8 dst=203.0.113.1 sport=443 dport=50005 [ASSURED] mark=0 use=1
icmp     1 29 src=192.168.1.10 dst=203.0.113.2 type=8 code=0 id=1234 src=203.0.113.2 dst=203.0.113.1 type=0 code=0 id=1234 mark=0 use=1
"""

PORT_FORWARD_RULES: List[PortForwardRule] = [
    PortForwardRule(8080, "192.168.1.100", 80, Protocol.TCP, "Web server"),
    PortForwardRule(2222, "192.168.1.50", 22, Protocol.TCP, "SSH bastion"),
    PortForwardRule(3389, "192.168.1.60", 3389, Protocol.TCP, "Remote desktop"),
    PortForwardRule(5000, "192.168.1.70", 5000, Protocol.TCP, "Application server"),
    PortForwardRule(53, "192.168.1.2", 53, Protocol.UDP, "Internal DNS", enabled=False),
]


# ═══════════════════════════════════════════════════════════════════════════════
# CONNTRACK_PARSING
# ═══════════════════════════════════════════════════════════════════════════════

class ConntrackParser:
    """Parser for conntrack output."""
    
    # Regex patterns for extraction
    FIELD_PATTERN = re.compile(r'(\w+)=(\S+)')
    STATE_PATTERN = re.compile(r'\b(ESTABLISHED|TIME_WAIT|SYN_SENT|SYN_RECV|FIN_WAIT|CLOSE)\b')
    
    @classmethod
    def parse_entry(cls, line: str) -> Optional[NATEntry]:
        """
        Parse a single conntrack entry line.
        
        Args:
            line: Raw conntrack output line
            
        Returns:
            NATEntry if parsing succeeds, None otherwise
            
        Example input:
            tcp 6 431999 ESTABLISHED src=192.168.1.10 dst=8.8.8.8 sport=45678 dport=443 ...
        """
        line = line.strip()
        if not line:
            return None
        
        try:
            parts = line.split()
            if len(parts) < 10:
                logger.debug(f"Line too short: {line[:50]}...")
                return None
            
            # Extract protocol
            protocol = Protocol.from_string(parts[0])
            
            # Extract timeout (third field is usually timeout)
            timeout = cls._safe_int(parts[2], default=0)
            
            # Extract state (if present)
            state = ConnectionState.NONE
            state_match = cls.STATE_PATTERN.search(line)
            if state_match:
                state = ConnectionState.from_string(state_match.group(1))
            
            # Extract key-value pairs
            fields = cls.FIELD_PATTERN.findall(line)
            
            # Build dictionaries for original and reply tuples
            original: Dict[str, str] = {}
            reply: Dict[str, str] = {}
            
            seen_keys: set = set()
            for key, value in fields:
                if key in ['src', 'dst', 'sport', 'dport']:
                    if key not in seen_keys:
                        original[key] = value
                        seen_keys.add(key)
                    else:
                        reply[key] = value
            
            # Validate we have required fields
            required = ['src', 'dst', 'sport', 'dport']
            if not all(k in original for k in required):
                logger.debug(f"Missing required fields in original tuple")
                return None
            
            return NATEntry(
                protocol=protocol,
                internal_ip=original.get('src', ''),
                internal_port=cls._safe_int(original.get('sport', '0')),
                external_ip=reply.get('dst', original.get('dst', '')),
                external_port=cls._safe_int(reply.get('dport', '0')),
                destination_ip=original.get('dst', ''),
                destination_port=cls._safe_int(original.get('dport', '0')),
                state=state,
                timeout=timeout
            )
            
        except (ValueError, KeyError, IndexError) as e:
            logger.debug(f"Parse error: {e}")
            return None
    
    @staticmethod
    def _safe_int(value: str, default: int = 0) -> int:
        """Safely convert string to int."""
        try:
            return int(value)
        except (ValueError, TypeError):
            return default
    
    @classmethod
    def parse_all(cls, conntrack_output: str) -> List[NATEntry]:
        """Parse all entries from conntrack output."""
        entries = []
        for line in conntrack_output.strip().split('\n'):
            entry = cls.parse_entry(line)
            if entry:
                entries.append(entry)
            else:
                logger.debug(f"Skipped unparseable line: {line[:50]}...")
        return entries


# ═══════════════════════════════════════════════════════════════════════════════
# ANALYSIS_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def analyse_connections(entries: List[NATEntry]) -> AnalysisResult:
    """
    Perform comprehensive analysis of NAT entries.
    
    Args:
        entries: List of parsed NAT entries
        
    Returns:
        AnalysisResult with statistics and warnings
    """
    result = AnalysisResult(total_entries=len(entries))
    
    for entry in entries:
        # Count by protocol
        proto = entry.protocol.value
        result.by_protocol[proto] = result.by_protocol.get(proto, 0) + 1
        
        # Count by state
        state = entry.state.value
        result.by_state[state] = result.by_state.get(state, 0) + 1
        
        # Count by internal host
        host = entry.internal_ip
        result.by_host[host] = result.by_host.get(host, 0) + 1
        
        # Count by destination
        dest = entry.destination_ip
        result.by_destination[dest] = result.by_destination.get(dest, 0) + 1
        
        # Count established
        if entry.is_established():
            result.established_count += 1
    
    # Generate warnings
    for host, count in result.by_host.items():
        if count > 100:
            result.warnings.append(f"High connection count from {host}: {count}")
    
    return result


def trace_inbound_packet(
    external_port: int,
    rules: List[PortForwardRule],
    protocol: Optional[Protocol] = None
) -> Optional[Tuple[str, int, str]]:
    """
    Trace where an inbound packet would be forwarded.
    
    Args:
        external_port: Port on NAT public interface
        rules: List of port forwarding rules
        protocol: Optional protocol filter
        
    Returns:
        Tuple of (internal_ip, internal_port, description) or None
    """
    for rule in rules:
        if rule.matches(external_port, protocol):
            return (rule.internal_ip, rule.internal_port, rule.description)
    return None


def find_related_entries(
    entries: List[NATEntry],
    ip: Optional[str] = None,
    port: Optional[int] = None
) -> List[NATEntry]:
    """Find entries matching given criteria."""
    results = []
    for entry in entries:
        if ip and entry.internal_ip != ip and entry.destination_ip != ip:
            continue
        if port and entry.internal_port != port and entry.destination_port != port:
            continue
        results.append(entry)
    return results


# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def display_conntrack_table(entries: List[NATEntry], verbose: bool = False) -> None:
    """Display parsed conntrack entries in a table."""
    print("\n" + "═" * 100)
    print("CONNECTION TRACKING TABLE (conntrack)")
    print("═" * 100)
    print(f"{'Proto':<6} {'Internal':<22} {'Ext Port':<10} {'Destination':<24} {'State':<12} {'Timeout':<8}")
    print("─" * 100)
    
    for e in entries:
        internal = f"{e.internal_ip}:{e.internal_port}"
        dest = f"{e.destination_ip}:{e.destination_port}"
        print(f"{e.protocol.value:<6} {internal:<22} {e.external_port:<10} {dest:<24} {e.state.value:<12} {e.timeout:<8}")
    
    print("═" * 100)
    print(f"Total entries: {len(entries)}")


def display_port_forward_rules(rules: List[PortForwardRule]) -> None:
    """Display port forwarding rules."""
    print("\n" + "═" * 85)
    print("PORT FORWARDING RULES (DNAT)")
    print("═" * 85)
    print(f"{'Ext Port':<10} {'Proto':<8} {'Internal Target':<25} {'Description':<25} {'Status':<10}")
    print("─" * 85)
    
    for rule in rules:
        target = f"{rule.internal_ip}:{rule.internal_port}"
        status = "✓ Active" if rule.enabled else "✗ Disabled"
        print(f"{rule.external_port:<10} {rule.protocol.value:<8} {target:<25} {rule.description:<25} {status:<10}")
    
    print("═" * 85)


def display_analysis(result: AnalysisResult) -> None:
    """Display analysis results."""
    print("\n" + "═" * 60)
    print("ANALYSIS RESULTS")
    print("═" * 60)
    
    print(f"\n📊 Total Connections: {result.total_entries}")
    print(f"   Established: {result.established_count}")
    
    print("\n📈 By Protocol:")
    for proto, count in sorted(result.by_protocol.items()):
        print(f"   {proto}: {count}")
    
    print("\n📈 By State:")
    for state, count in sorted(result.by_state.items()):
        print(f"   {state}: {count}")
    
    print("\n📈 By Internal Host:")
    for host, count in sorted(result.by_host.items(), key=lambda x: -x[1]):
        print(f"   {host}: {count}")
    
    if result.warnings:
        print("\n⚠️ Warnings:")
        for warning in result.warnings:
            print(f"   {warning}")
    
    print("═" * 60)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="NAT Translation Analysis — Week 6 Homework"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    print("═" * 70)
    print("Homework 6.1: NAT Translation Analysis")
    print("Computer Networks - Week 6 | ASE Bucharest, CSIE")
    print("═" * 70)
    
    # Parse conntrack entries
    entries = ConntrackParser.parse_all(SAMPLE_CONNTRACK)
    print(f"\n✓ Parsed {len(entries)} NAT entries")
    
    # Display tables
    display_conntrack_table(entries, verbose=args.verbose)
    display_port_forward_rules(PORT_FORWARD_RULES)
    
    # Analyse
    result = analyse_connections(entries)
    display_analysis(result)
    
    # Trace packets
    print("\n🔍 Packet Tracing:")
    test_ports = [8080, 2222, 443, 5000, 53]
    for port in test_ports:
        trace = trace_inbound_packet(port, PORT_FORWARD_RULES)
        if trace:
            ip, p, desc = trace
            print(f"   External :{port} → {ip}:{p} ({desc})")
        else:
            print(f"   External :{port} → No forwarding rule")
    
    print("\n" + "═" * 70)
    print("✅ Analysis Complete")
    print("═" * 70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
