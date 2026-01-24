#!/usr/bin/env python3
"""
Homework 5.2: IPv6 Analysis and Transition Planning
====================================================
Computer Networks - Week 5 (WSL Environment)
ASE Bucharest, CSIE | by ing. dr. Antonio Clim

Objectives:
- Analyse IPv6 addresses and identify their components (prefix, interface ID)
- Compare IPv6 addressing with equivalent IPv4 scenarios
- Understand dual-stack deployment concepts
- Document a transition plan for an organisation

Prerequisites:
- Understanding of IPv6 address structure and notation
- Familiarity with IPv6 address types (link-local, global, ULA)
- Week 5 exercises completed

Level: Intermediate (⭐⭐)
Estimated time: 45-60 minutes

Pair Programming Notes:
- Driver: Implement IPv6 parsing and validation functions
- Navigator: Verify address formats, research transition mechanisms
- Swap after: Completing the address analysis section
"""

from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import ipaddress
import sys
from dataclasses import dataclass
from typing import List, Optional, Tuple


# ═══════════════════════════════════════════════════════════════════════════════
# DATA_STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class IPv6Analysis:
    """Analysis results for an IPv6 address."""
    address: str
    full_form: str
    compressed_form: str
    address_type: str
    prefix: str
    interface_id: str
    scope: str
    is_valid: bool


@dataclass
class DualStackHost:
    """Represents a host with both IPv4 and IPv6 addresses."""
    hostname: str
    ipv4_address: str
    ipv6_global: str
    ipv6_link_local: str
    description: str


# ═══════════════════════════════════════════════════════════════════════════════
# SAMPLE_DATA
# ═══════════════════════════════════════════════════════════════════════════════
SAMPLE_ADDRESSES = [
    "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
    "fe80::1",
    "::1",
    "2001:db8::1/64",
    "fd00:1234:5678::10",
    "ff02::1",
    "2001:db8:cafe::",
    "::ffff:192.168.1.1",  # IPv4-mapped IPv6
]

ORGANISATION_HOSTS = [
    DualStackHost(
        "web-server-01",
        "192.168.1.10",
        "2001:db8:1::10",
        "fe80::1",
        "Primary web server"
    ),
    DualStackHost(
        "db-server-01", 
        "192.168.1.20",
        "2001:db8:1::20",
        "fe80::2",
        "PostgreSQL database server"
    ),
    DualStackHost(
        "app-server-01",
        "192.168.1.30",
        "2001:db8:1::30",
        "fe80::3",
        "Application backend"
    ),
]


# ═══════════════════════════════════════════════════════════════════════════════
# PREDICTION_PROMPT
# ═══════════════════════════════════════════════════════════════════════════════
def prompt_prediction(question: str) -> str:
    """Ask student to predict outcome before execution."""
    print(f"\n💭 PREDICTION: {question}")
    print("   (Think about your answer before pressing Enter)")
    prediction = input("   Your prediction: ")
    return prediction


# ═══════════════════════════════════════════════════════════════════════════════
# IPV6_ANALYSIS_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def expand_ipv6(address: str) -> str:
    """
    Expand an IPv6 address to its full 32-character hexadecimal form.
    
    Args:
        address: IPv6 address (may be compressed)
        
    Returns:
        Full form with all 8 groups of 4 hex digits
        
    Example:
        >>> expand_ipv6("2001:db8::1")
        "2001:0db8:0000:0000:0000:0000:0000:0001"
    """
    # Remove prefix length if present
    addr_only = address.split('/')[0]
    
    try:
        ipv6 = ipaddress.IPv6Address(addr_only)
        return ipv6.exploded
    except ipaddress.AddressValueError:
        return "INVALID"


def compress_ipv6(address: str) -> str:
    """
    Compress an IPv6 address using :: notation.
    
    Args:
        address: IPv6 address (may be expanded)
        
    Returns:
        Compressed form using :: for consecutive zeros
    """
    addr_only = address.split('/')[0]
    
    try:
        ipv6 = ipaddress.IPv6Address(addr_only)
        return ipv6.compressed
    except ipaddress.AddressValueError:
        return "INVALID"


def identify_address_type(address: str) -> Tuple[str, str]:
    """
    Identify the type and scope of an IPv6 address.
    
    Args:
        address: IPv6 address to analyse
        
    Returns:
        Tuple of (address_type, scope)
        
    Types:
        - "Loopback" (::1)
        - "Link-local" (fe80::/10)
        - "Global Unicast" (2000::/3)
        - "Unique Local" (fc00::/7)
        - "Multicast" (ff00::/8)
        - "IPv4-mapped" (::ffff:0:0/96)
        - "Unspecified" (::)
    """
    addr_only = address.split('/')[0]
    
    try:
        ipv6 = ipaddress.IPv6Address(addr_only)
        
        # TODO: Implement address type identification
        # Hint: Use ipv6.is_loopback, ipv6.is_link_local, etc.
        
        # ─── YOUR CODE HERE ───
        if ipv6.is_loopback:
            return ("Loopback", "Host")
        elif ipv6.is_link_local:
            return ("Link-local", "Link")
        elif ipv6.is_global:
            return ("Global Unicast", "Global")
        elif ipv6.is_private:
            return ("Unique Local (ULA)", "Organisation")
        elif ipv6.is_multicast:
            return ("Multicast", "Varies")
        elif ipv6.is_unspecified:
            return ("Unspecified", "None")
        elif ipv6.ipv4_mapped:
            return ("IPv4-mapped", "Compatibility")
        else:
            return ("Unknown", "Unknown")
        # ─── END YOUR CODE ───
        
    except ipaddress.AddressValueError:
        return ("Invalid", "N/A")


def extract_prefix_and_iid(address: str, prefix_len: int = 64) -> Tuple[str, str]:
    """
    Extract the network prefix and interface identifier from an IPv6 address.
    
    Standard split is /64 (64-bit prefix, 64-bit interface ID).
    
    Args:
        address: IPv6 address
        prefix_len: Prefix length (default 64)
        
    Returns:
        Tuple of (prefix, interface_id)
    """
    full = expand_ipv6(address)
    if full == "INVALID":
        return ("INVALID", "INVALID")
    
    # Remove colons for bit manipulation
    hex_str = full.replace(":", "")
    
    # Calculate hex characters for prefix
    prefix_hex = prefix_len // 4
    
    prefix_part = hex_str[:prefix_hex]
    iid_part = hex_str[prefix_hex:]
    
    # Format back with colons (every 4 characters)
    def add_colons(s: str) -> str:
        return ":".join(s[i:i+4] for i in range(0, len(s), 4))
    
    return (add_colons(prefix_part), add_colons(iid_part))


def analyse_ipv6_address(address: str) -> IPv6Analysis:
    """
    Perform complete analysis of an IPv6 address.
    
    Args:
        address: IPv6 address to analyse
        
    Returns:
        IPv6Analysis dataclass with all details
    """
    addr_type, scope = identify_address_type(address)
    prefix, iid = extract_prefix_and_iid(address)
    
    return IPv6Analysis(
        address=address,
        full_form=expand_ipv6(address),
        compressed_form=compress_ipv6(address),
        address_type=addr_type,
        prefix=prefix,
        interface_id=iid,
        scope=scope,
        is_valid=addr_type != "Invalid"
    )


# ═══════════════════════════════════════════════════════════════════════════════
# DUAL_STACK_ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
def compare_addressing(hosts: List[DualStackHost]) -> None:
    """
    Compare IPv4 and IPv6 addressing for a list of hosts.
    
    Displays a comparison table showing both address families.
    """
    print("\n" + "=" * 80)
    print("DUAL-STACK HOST COMPARISON")
    print("=" * 80)
    print(f"{'Hostname':<16} {'IPv4':<16} {'IPv6 Global':<25} {'Link-Local':<16}")
    print("-" * 80)
    
    for host in hosts:
        print(f"{host.hostname:<16} {host.ipv4_address:<16} "
              f"{host.ipv6_global:<25} {host.ipv6_link_local:<16}")
    
    print("=" * 80)
    
    # Analysis questions
    print("\n📊 Analysis Questions:")
    print("   1. How many bits are in each IPv4 address vs IPv6?")
    print("   2. Which address type is routable on the Internet?")
    print("   3. What is the purpose of link-local addresses?")


def generate_eui64_iid(mac_address: str) -> str:
    """
    Generate an EUI-64 interface identifier from a MAC address.
    
    Process:
    1. Split MAC into two halves
    2. Insert FF:FE in the middle
    3. Flip the 7th bit (Universal/Local)
    
    Args:
        mac_address: MAC address in format "aa:bb:cc:dd:ee:ff"
        
    Returns:
        EUI-64 interface identifier
    """
    # TODO: Implement EUI-64 generation
    # ─── YOUR CODE HERE ───
    # Remove colons and validate
    mac = mac_address.replace(":", "").replace("-", "").lower()
    if len(mac) != 12:
        return "INVALID_MAC"
    
    # Split into two halves
    first_half = mac[:6]
    second_half = mac[6:]
    
    # Insert fffe in the middle
    eui64 = first_half + "fffe" + second_half
    
    # Flip the 7th bit (Universal/Local bit)
    first_byte = int(eui64[:2], 16)
    first_byte ^= 0x02  # Flip bit 1 (0-indexed from right)
    eui64 = f"{first_byte:02x}" + eui64[2:]
    
    # Format as IPv6 interface ID
    return f"{eui64[0:4]}:{eui64[4:8]}:{eui64[8:12]}:{eui64[12:16]}"
    # ─── END YOUR CODE ───


# ═══════════════════════════════════════════════════════════════════════════════
# TRANSITION_PLANNING
# ═══════════════════════════════════════════════════════════════════════════════
def print_transition_mechanisms() -> None:
    """Print information about IPv6 transition mechanisms."""
    print("\n" + "=" * 70)
    print("IPv6 TRANSITION MECHANISMS")
    print("=" * 70)
    
    mechanisms = [
        {
            "name": "Dual-Stack",
            "description": "Run IPv4 and IPv6 simultaneously on all devices",
            "pros": ["Native performance", "Full compatibility"],
            "cons": ["Requires IPv6 on all devices", "Double the addressing overhead"]
        },
        {
            "name": "Tunnelling (6in4, 6to4)",
            "description": "Encapsulate IPv6 packets within IPv4",
            "pros": ["Works over IPv4-only networks", "Incremental deployment"],
            "cons": ["Added latency", "MTU issues", "Security concerns"]
        },
        {
            "name": "NAT64/DNS64",
            "description": "Translate between IPv6 and IPv4 at network edge",
            "pros": ["IPv6-only internal network", "Reduces IPv4 usage"],
            "cons": ["Stateful translation required", "Some protocols may break"]
        },
    ]
    
    for mech in mechanisms:
        print(f"\n📌 {mech['name']}")
        print(f"   {mech['description']}")
        print(f"   ✅ Pros: {', '.join(mech['pros'])}")
        print(f"   ⚠️ Cons: {', '.join(mech['cons'])}")
    
    print("\n" + "=" * 70)


# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def display_analysis_table(analyses: List[IPv6Analysis]) -> None:
    """Display IPv6 analysis results in a formatted table."""
    print("\n" + "=" * 100)
    print("IPv6 ADDRESS ANALYSIS")
    print("=" * 100)
    print(f"{'Address':<30} {'Type':<18} {'Scope':<12} {'Compressed':<25}")
    print("-" * 100)
    
    for a in analyses:
        status = "✅" if a.is_valid else "❌"
        print(f"{status} {a.address:<28} {a.address_type:<18} {a.scope:<12} {a.compressed_form:<25}")
    
    print("=" * 100)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point for Homework 5.2."""
    print("=" * 70)
    print("Homework 5.2: IPv6 Analysis and Transition Planning")
    print("Computer Networks - Week 5 | ASE Bucharest, CSIE")
    print("=" * 70)
    
    # Part 1: IPv6 Address Analysis
    print("\n📋 PART 1: IPv6 Address Analysis")
    print("-" * 40)
    
    prompt_prediction(
        "How many of the sample addresses are Global Unicast (Internet-routable)?"
    )
    
    analyses = [analyse_ipv6_address(addr) for addr in SAMPLE_ADDRESSES]
    display_analysis_table(analyses)
    
    # Count by type
    type_counts: dict = {}
    for a in analyses:
        type_counts[a.address_type] = type_counts.get(a.address_type, 0) + 1
    
    print("\n📊 Address Type Distribution:")
    for addr_type, count in sorted(type_counts.items()):
        print(f"   {addr_type}: {count}")
    
    # Part 2: Prefix and Interface ID Extraction
    print("\n\n📋 PART 2: Prefix and Interface ID")
    print("-" * 40)
    
    sample = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    prefix, iid = extract_prefix_and_iid(sample)
    print(f"Address: {sample}")
    print(f"Prefix (/64):    {prefix}")
    print(f"Interface ID:    {iid}")
    
    # Part 3: EUI-64 Generation
    print("\n\n📋 PART 3: EUI-64 Interface Identifier")
    print("-" * 40)
    
    mac = "00:1a:2b:3c:4d:5e"
    eui64 = generate_eui64_iid(mac)
    print(f"MAC Address: {mac}")
    print(f"EUI-64 IID:  {eui64}")
    print(f"Full link-local would be: fe80::{eui64}")
    
    # Part 4: Dual-Stack Comparison
    print("\n\n📋 PART 4: Dual-Stack Comparison")
    print("-" * 40)
    compare_addressing(ORGANISATION_HOSTS)
    
    # Part 5: Transition Mechanisms
    print("\n\n📋 PART 5: Transition Mechanisms")
    print("-" * 40)
    print_transition_mechanisms()
    
    # Summary
    print("\n" + "=" * 70)
    print("✅ Analysis Complete")
    print("=" * 70)
    print("\n📝 Reflection Questions:")
    print("   1. Why is IPv6 transition taking so long?")
    print("   2. What are the security implications of tunnelling?")
    print("   3. How does SLAAC differ from DHCPv6?")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
