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
"""

from __future__ import annotations
import re
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

# ═══════════════════════════════════════════════════════════════════════════════
# DATA_STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class NATEntry:
    """Represents a NAT translation table entry."""
    protocol: str
    internal_ip: str
    internal_port: int
    external_ip: str
    external_port: int
    destination_ip: str
    destination_port: int
    state: str
    timeout: int

@dataclass
class PortForwardRule:
    """Represents a port forwarding rule."""
    external_port: int
    internal_ip: str
    internal_port: int
    protocol: str
    description: str

# ═══════════════════════════════════════════════════════════════════════════════
# SAMPLE_DATA
# ═══════════════════════════════════════════════════════════════════════════════
SAMPLE_CONNTRACK = """
tcp      6 431999 ESTABLISHED src=192.168.1.10 dst=8.8.8.8 sport=45678 dport=443 src=8.8.8.8 dst=203.0.113.1 sport=443 dport=50001 [ASSURED] mark=0 use=1
tcp      6 117 TIME_WAIT src=192.168.1.10 dst=93.184.216.34 sport=45679 dport=80 src=93.184.216.34 dst=203.0.113.1 sport=80 dport=50002 [ASSURED] mark=0 use=1
udp      17 28 src=192.168.1.20 dst=8.8.8.8 sport=53421 dport=53 src=8.8.8.8 dst=203.0.113.1 sport=53 dport=50003 mark=0 use=1
"""

PORT_FORWARD_RULES = [
    PortForwardRule(8080, "192.168.1.100", 80, "tcp", "Web server"),
    PortForwardRule(2222, "192.168.1.50", 22, "tcp", "SSH bastion"),
    PortForwardRule(3389, "192.168.1.60", 3389, "tcp", "Remote desktop"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# CONNTRACK_PARSING
# ═══════════════════════════════════════════════════════════════════════════════
def parse_conntrack_entry(line: str) -> Optional[NATEntry]:
    """Parse a single conntrack entry line."""
    line = line.strip()
    if not line:
        return None
    
    # TODO: Implement conntrack parsing
    # ─── YOUR CODE HERE ───
    try:
        parts = line.split()
        if len(parts) < 10:
            return None
        
        protocol = parts[0]
        timeout = int(parts[2])
        
        state = "NONE"
        if parts[3] in ["ESTABLISHED", "TIME_WAIT", "SYN_SENT"]:
            state = parts[3]
            start_idx = 4
        else:
            start_idx = 3
        
        original = {}
        translated = {}
        
        for part in parts[start_idx:]:
            if '=' in part:
                key, value = part.split('=', 1)
                if key in ['src', 'dst', 'sport', 'dport']:
                    if key not in original:
                        original[key] = value
                    else:
                        translated[key] = value
        
        return NATEntry(
            protocol=protocol,
            internal_ip=original.get('src', ''),
            internal_port=int(original.get('sport', 0)),
            external_ip=translated.get('dst', ''),
            external_port=int(translated.get('dport', 0)),
            destination_ip=original.get('dst', ''),
            destination_port=int(original.get('dport', 0)),
            state=state,
            timeout=timeout
        )
    except (ValueError, KeyError, IndexError):
        return None
    # ─── END YOUR CODE ───

def parse_all_conntrack(conntrack_output: str) -> List[NATEntry]:
    """Parse all entries from conntrack output."""
    entries = []
    for line in conntrack_output.strip().split('\n'):
        entry = parse_conntrack_entry(line)
        if entry:
            entries.append(entry)
    return entries

# ═══════════════════════════════════════════════════════════════════════════════
# ANALYSIS_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def analyse_connections_by_host(entries: List[NATEntry]) -> Dict[str, int]:
    """Count connections per internal host."""
    counts = {}
    for entry in entries:
        ip = entry.internal_ip
        counts[ip] = counts.get(ip, 0) + 1
    return counts

def trace_inbound_packet(external_port: int, rules: List[PortForwardRule]) -> Optional[Tuple[str, int, str]]:
    """Trace where an inbound packet would be forwarded."""
    for rule in rules:
        if rule.external_port == external_port:
            return (rule.internal_ip, rule.internal_port, rule.description)
    return None

# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def display_conntrack_table(entries: List[NATEntry]) -> None:
    """Display parsed conntrack entries in a table."""
    print("\n" + "=" * 100)
    print("CONNECTION TRACKING TABLE (conntrack)")
    print("=" * 100)
    print(f"{'Proto':<6} {'Internal':<22} {'External Port':<14} {'Destination':<22} {'State':<12}")
    print("-" * 100)
    
    for e in entries:
        internal = f"{e.internal_ip}:{e.internal_port}"
        dest = f"{e.destination_ip}:{e.destination_port}"
        print(f"{e.protocol:<6} {internal:<22} {e.external_port:<14} {dest:<22} {e.state:<12}")
    print("=" * 100)

def display_port_forward_rules(rules: List[PortForwardRule]) -> None:
    """Display port forwarding rules."""
    print("\n" + "=" * 80)
    print("PORT FORWARDING RULES (DNAT)")
    print("=" * 80)
    print(f"{'External Port':<15} {'Protocol':<10} {'Internal Target':<25} {'Description':<25}")
    print("-" * 80)
    
    for rule in rules:
        target = f"{rule.internal_ip}:{rule.internal_port}"
        print(f"{rule.external_port:<15} {rule.protocol:<10} {target:<25} {rule.description:<25}")
    print("=" * 80)

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point."""
    print("=" * 70)
    print("Homework 6.1: NAT Translation Analysis")
    print("Computer Networks - Week 6 | ASE Bucharest, CSIE")
    print("=" * 70)
    
    entries = parse_all_conntrack(SAMPLE_CONNTRACK)
    print(f"\nParsed {len(entries)} NAT entries")
    
    display_conntrack_table(entries)
    display_port_forward_rules(PORT_FORWARD_RULES)
    
    # Trace packets
    print("\n🔍 Packet Tracing:")
    for port in [8080, 2222, 443]:
        result = trace_inbound_packet(port, PORT_FORWARD_RULES)
        if result:
            ip, p, desc = result
            print(f"   External :{port} → {ip}:{p} ({desc})")
        else:
            print(f"   External :{port} → No forwarding rule")
    
    print("\n✅ Analysis Complete")
    return 0

if __name__ == "__main__":
    sys.exit(main())
