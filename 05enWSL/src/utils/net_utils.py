#!/usr/bin/env python3
"""
Network Utilities for Week 5 – Network Layer: IP Addressing
============================================================
Reusable functions for CIDR calculations, VLSM, IPv6 and validations.

This module provides the core networking functions used by the exercise scripts.
Each function includes subgoal labels (═══ comments) to help trace algorithm steps.

Learning Notes:
    - Study the VLSM allocation algorithm to understand largest-first ordering
    - Compare FLSM vs VLSM efficiency in your exercises
    - IPv6 functions demonstrate compression rules

Author: ing. dr. Antonio Clim, ASE-CSIE Bucharest
Version: 2.1 (January 2026)
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import ipaddress
import math
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union


# ═══════════════════════════════════════════════════════════════════════════════
# DEFINE_DATA_STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class IPv4NetworkInfo:
    """
    Complete information about an IPv4 network/interface.
    
    Attributes:
        address: The specific IP address being analysed
        network: The network this address belongs to
        netmask: Subnet mask in dotted decimal
        wildcard: Inverse mask (used in ACLs)
        broadcast: Broadcast address for this network
        total_addresses: Total addresses in the block (2^host_bits)
        usable_hosts: Addresses assignable to hosts (total - 2)
        first_host: First usable host address
        last_host: Last usable host address
        is_private: True if RFC 1918 private address
        address_type: Classification as 'network', 'broadcast', or 'host'
    """
    address: ipaddress.IPv4Address
    network: ipaddress.IPv4Network
    netmask: ipaddress.IPv4Address
    wildcard: ipaddress.IPv4Address
    broadcast: ipaddress.IPv4Address
    total_addresses: int
    usable_hosts: int
    first_host: Optional[ipaddress.IPv4Address]
    last_host: Optional[ipaddress.IPv4Address]
    is_private: bool
    address_type: str


@dataclass
class VLSMAllocation:
    """
    Result of a VLSM allocation.
    
    Attributes:
        required_hosts: Number of hosts requested
        allocated_prefix: Prefix length assigned (e.g., 26 for /26)
        network: The allocated network
        gateway: Suggested gateway (first usable host)
        broadcast: Broadcast address
        usable_hosts: Actual usable host count
        efficiency: Percentage of allocated space actually needed
    """
    required_hosts: int
    allocated_prefix: int
    network: ipaddress.IPv4Network
    gateway: ipaddress.IPv4Address
    broadcast: ipaddress.IPv4Address
    usable_hosts: int
    efficiency: float


@dataclass
class IPv6Info:
    """
    Information about an IPv6 address.
    
    Attributes:
        full_form: All 32 hex digits with colons
        compressed: Minimal representation using :: notation
        exploded: Same as full_form (for compatibility)
        network: Network portion if prefix was specified
        address_type: Classification (global-unicast, link-local, etc.)
        scope: Routing scope (global, link-local, etc.)
    """
    full_form: str
    compressed: str
    exploded: str
    network: Optional[ipaddress.IPv6Network]
    address_type: str
    scope: str


# ═══════════════════════════════════════════════════════════════════════════════
# IPV4_ANALYSIS_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def analyze_ipv4_interface(cidr: str) -> IPv4NetworkInfo:
    """
    Completely analyse an IPv4 address with CIDR prefix.
    
    Algorithm Steps:
        1. PARSE_INPUT: Convert CIDR string to interface object
        2. CALCULATE_WILDCARD: Compute inverse mask via XOR
        3. CLASSIFY_ADDRESS: Determine if network, broadcast, or host
        4. COMPUTE_HOST_RANGE: Calculate usable addresses
        5. BUILD_RESULT: Assemble all information into dataclass
    
    Args:
        cidr: Address in format 'x.x.x.x/n' (e.g., '192.168.10.14/26')
    
    Returns:
        IPv4NetworkInfo with all network details
    
    Raises:
        ValueError: For invalid addresses or prefix lengths
    
    Example:
        >>> info = analyze_ipv4_interface("192.168.10.14/26")
        >>> print(info.usable_hosts)
        62
    """
    # ─────────────────────────────────────────────────────────────────────────
    # PARSE_INPUT
    # ─────────────────────────────────────────────────────────────────────────
    interface = ipaddress.IPv4Interface(cidr)
    network = interface.network
    address = interface.ip
    
    # ─────────────────────────────────────────────────────────────────────────
    # CALCULATE_WILDCARD
    # ─────────────────────────────────────────────────────────────────────────
    netmask_int = int(network.netmask)
    wildcard_int = netmask_int ^ 0xFFFFFFFF
    wildcard = ipaddress.IPv4Address(wildcard_int)
    
    # ─────────────────────────────────────────────────────────────────────────
    # CLASSIFY_ADDRESS
    # ─────────────────────────────────────────────────────────────────────────
    if address == network.network_address:
        addr_type = "network"
    elif address == network.broadcast_address:
        addr_type = "broadcast"
    else:
        addr_type = "host"
    
    # ─────────────────────────────────────────────────────────────────────────
    # COMPUTE_HOST_RANGE
    # ─────────────────────────────────────────────────────────────────────────
    total = network.num_addresses
    if network.prefixlen == 32:
        usable = 1
        first_host = last_host = address
    elif network.prefixlen == 31:
        usable = 2
        first_host = network.network_address
        last_host = network.broadcast_address
    else:
        usable = total - 2
        first_host = network.network_address + 1
        last_host = network.broadcast_address - 1
    
    # ─────────────────────────────────────────────────────────────────────────
    # BUILD_RESULT
    # ─────────────────────────────────────────────────────────────────────────
    return IPv4NetworkInfo(
        address=address,
        network=network,
        netmask=network.netmask,
        wildcard=wildcard,
        broadcast=network.broadcast_address,
        total_addresses=total,
        usable_hosts=usable,
        first_host=first_host if usable > 0 else None,
        last_host=last_host if usable > 0 else None,
        is_private=network.is_private,
        address_type=addr_type
    )


def ipv4_host_range(network: ipaddress.IPv4Network) -> Tuple[Optional[ipaddress.IPv4Address], 
                                                              Optional[ipaddress.IPv4Address], 
                                                              int]:
    """Return (first_host, last_host, usable_count) for an IPv4 network."""
    total = network.num_addresses
    if network.prefixlen == 32:
        return network.network_address, network.network_address, 1
    elif network.prefixlen == 31:
        return network.network_address, network.broadcast_address, 2
    elif total <= 2:
        return None, None, 0
    return network.network_address + 1, network.broadcast_address - 1, total - 2


# ═══════════════════════════════════════════════════════════════════════════════
# SUBNETTING_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def prefix_for_hosts(hosts_needed: int) -> int:
    """
    Calculate the minimum prefix required for a number of hosts.
    
    Algorithm:
        1. Add 2 to hosts_needed (for network + broadcast)
        2. Find smallest power of 2 >= total_needed
        3. Convert to prefix: 32 - host_bits
    
    Args:
        hosts_needed: Number of hosts required (must be positive)
    
    Returns:
        Prefix length (e.g., 26 for max 62 hosts)
    
    Example:
        >>> prefix_for_hosts(50)
        26
    """
    # ─────────────────────────────────────────────────────────────────────────
    # VALIDATE_INPUT
    # ─────────────────────────────────────────────────────────────────────────
    if hosts_needed <= 0:
        raise ValueError("Number of hosts must be positive")
    
    # ─────────────────────────────────────────────────────────────────────────
    # CALCULATE_TOTAL_ADDRESSES_NEEDED
    # ─────────────────────────────────────────────────────────────────────────
    total_needed = hosts_needed + 2
    
    # ─────────────────────────────────────────────────────────────────────────
    # FIND_MINIMUM_HOST_BITS
    # ─────────────────────────────────────────────────────────────────────────
    host_bits = math.ceil(math.log2(total_needed))
    host_bits = max(host_bits, 2)
    
    # ─────────────────────────────────────────────────────────────────────────
    # CONVERT_TO_PREFIX
    # ─────────────────────────────────────────────────────────────────────────
    prefix = 32 - host_bits
    
    if prefix < 0:
        raise ValueError(f"No sufficient prefix for {hosts_needed} hosts")
    
    return prefix


def flsm_split(base_network: str, num_subnets: int) -> List[ipaddress.IPv4Network]:
    """
    Split a network into N equal subnets using Fixed Length Subnet Mask.
    
    Args:
        base_network: Base network in strict CIDR format (e.g., '192.168.100.0/24')
        num_subnets: Number of subnets (must be power of 2: 2, 4, 8, 16...)
    
    Returns:
        List of resulting subnets (all same size)
    
    Example:
        >>> subnets = flsm_split("192.168.0.0/24", 4)
        >>> [str(s) for s in subnets]
        ['192.168.0.0/26', '192.168.0.64/26', '192.168.0.128/26', '192.168.0.192/26']
    """
    # ─────────────────────────────────────────────────────────────────────────
    # PARSE_NETWORK
    # ─────────────────────────────────────────────────────────────────────────
    net = ipaddress.ip_network(base_network, strict=True)
    
    if not isinstance(net, ipaddress.IPv4Network):
        raise ValueError("FLSM implemented only for IPv4")
    
    # ─────────────────────────────────────────────────────────────────────────
    # VALIDATE_SUBNET_COUNT
    # ─────────────────────────────────────────────────────────────────────────
    if num_subnets <= 0 or (num_subnets & (num_subnets - 1)) != 0:
        raise ValueError("Number of subnets must be power of 2 (2, 4, 8, 16...)")
    
    # ─────────────────────────────────────────────────────────────────────────
    # CALCULATE_NEW_PREFIX
    # ─────────────────────────────────────────────────────────────────────────
    bits_needed = num_subnets.bit_length() - 1
    new_prefix = net.prefixlen + bits_needed
    
    if new_prefix > 30:
        raise ValueError(f"Resulting prefix /{new_prefix} leaves no usable hosts")
    
    # ─────────────────────────────────────────────────────────────────────────
    # GENERATE_SUBNETS
    # ─────────────────────────────────────────────────────────────────────────
    return list(net.subnets(prefixlen_diff=bits_needed))


def vlsm_allocate(base_network: str, host_requirements: List[int]) -> List[VLSMAllocation]:
    """
    Allocate subnets with VLSM for a list of host requirements.
    
    CRITICAL: Requirements are processed LARGEST-FIRST to ensure proper
    block boundary alignment.
    
    Args:
        base_network: Available network in CIDR format (e.g., '10.0.0.0/24')
        host_requirements: List of host counts (e.g., [60, 30, 10, 2])
    
    Returns:
        List of VLSMAllocation objects in original input order
    
    Example:
        >>> allocs = vlsm_allocate("172.16.0.0/24", [60, 20, 10, 2])
        >>> for a in allocs:
        ...     print(f"{a.required_hosts} hosts -> {a.network}")
    """
    # ─────────────────────────────────────────────────────────────────────────
    # PARSE_NETWORK
    # ─────────────────────────────────────────────────────────────────────────
    net = ipaddress.ip_network(base_network, strict=True)
    
    if not isinstance(net, ipaddress.IPv4Network):
        raise ValueError("VLSM implemented only for IPv4")
    
    # ─────────────────────────────────────────────────────────────────────────
    # SORT_REQUIREMENTS
    # ─────────────────────────────────────────────────────────────────────────
    sorted_reqs = sorted(enumerate(host_requirements), key=lambda x: -x[1])
    
    allocations: List[VLSMAllocation] = []
    current_addr = int(net.network_address)
    end_addr = int(net.broadcast_address)
    
    # ─────────────────────────────────────────────────────────────────────────
    # PROCESS_EACH_REQUIREMENT
    # ─────────────────────────────────────────────────────────────────────────
    for orig_idx, hosts in sorted_reqs:
        # ─────────────────────────────────────────────────────────────────────
        # CALCULATE_PREFIX
        # ─────────────────────────────────────────────────────────────────────
        prefix = prefix_for_hosts(hosts)
        block_size = 2 ** (32 - prefix)
        
        # ─────────────────────────────────────────────────────────────────────
        # ALIGN_TO_BOUNDARY
        # ─────────────────────────────────────────────────────────────────────
        if current_addr % block_size != 0:
            current_addr = ((current_addr // block_size) + 1) * block_size
        
        # ─────────────────────────────────────────────────────────────────────
        # VERIFY_SPACE
        # ─────────────────────────────────────────────────────────────────────
        if current_addr + block_size - 1 > end_addr:
            raise ValueError(
                f"Insufficient space for {hosts} hosts. "
                f"Current address: {ipaddress.IPv4Address(current_addr)}, "
                f"Required: /{prefix} ({block_size} addresses)"
            )
        
        # ─────────────────────────────────────────────────────────────────────
        # ALLOCATE_SUBNET
        # ─────────────────────────────────────────────────────────────────────
        subnet = ipaddress.IPv4Network(f"{ipaddress.IPv4Address(current_addr)}/{prefix}")
        first_host, last_host, usable = ipv4_host_range(subnet)
        
        efficiency = (hosts / usable * 100) if usable > 0 else 0
        
        allocations.append(VLSMAllocation(
            required_hosts=hosts,
            allocated_prefix=prefix,
            network=subnet,
            gateway=first_host if first_host else subnet.network_address,
            broadcast=subnet.broadcast_address,
            usable_hosts=usable,
            efficiency=efficiency
        ))
        
        # ─────────────────────────────────────────────────────────────────────
        # ADVANCE_CURSOR
        # ─────────────────────────────────────────────────────────────────────
        current_addr += block_size
    
    # ─────────────────────────────────────────────────────────────────────────
    # REORDER_RESULTS
    # ─────────────────────────────────────────────────────────────────────────
    result = [None] * len(host_requirements)
    for i, (orig_idx, _) in enumerate(sorted_reqs):
        result[orig_idx] = allocations[i]
    
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# IPV6_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def ipv6_compress(address: str) -> str:
    """Compress an IPv6 address to minimal form."""
    addr = ipaddress.IPv6Address(address)
    return str(addr)


def ipv6_expand(address: str) -> str:
    """Expand an IPv6 address to full form."""
    addr = ipaddress.IPv6Address(address)
    return addr.exploded


def ipv6_info(address_or_network: str) -> IPv6Info:
    """Analyse an IPv6 address or network."""
    # ─────────────────────────────────────────────────────────────────────────
    # PARSE_ADDRESS
    # ─────────────────────────────────────────────────────────────────────────
    network = None
    try:
        if '/' in address_or_network:
            iface = ipaddress.IPv6Interface(address_or_network)
            addr = iface.ip
            network = iface.network
        else:
            addr = ipaddress.IPv6Address(address_or_network)
    except ValueError as e:
        raise ValueError(f"Invalid IPv6 address: {address_or_network}") from e
    
    # ─────────────────────────────────────────────────────────────────────────
    # DETERMINE_TYPE_AND_SCOPE
    # ─────────────────────────────────────────────────────────────────────────
    if addr.is_loopback:
        addr_type = "loopback"
        scope = "node-local"
    elif addr.is_link_local:
        addr_type = "link-local"
        scope = "link-local"
    elif addr.is_site_local:
        addr_type = "site-local (deprecated)"
        scope = "site-local"
    elif addr.is_multicast:
        addr_type = "multicast"
        scope_nibble = (int(addr) >> 112) & 0xF
        scope_map = {1: "interface-local", 2: "link-local", 5: "site-local",
                     8: "organisation-local", 14: "global"}
        scope = scope_map.get(scope_nibble, f"scope-{scope_nibble}")
    elif addr.is_private:
        addr_type = "unique-local"
        scope = "global (private)"
    elif addr.is_global:
        addr_type = "global-unicast"
        scope = "global"
    else:
        addr_type = "other"
        scope = "unknown"
    
    return IPv6Info(
        full_form=addr.exploded, compressed=str(addr), exploded=addr.exploded,
        network=network, address_type=addr_type, scope=scope
    )


def ipv6_subnets_from_prefix(base_prefix: str, target_prefix: int, count: int) -> List[ipaddress.IPv6Network]:
    """Generate IPv6 subnets from a base prefix."""
    net = ipaddress.IPv6Network(base_prefix, strict=True)
    
    if target_prefix <= net.prefixlen:
        raise ValueError(f"Target prefix /{target_prefix} must be longer than /{net.prefixlen}")
    if target_prefix > 128:
        raise ValueError("Maximum IPv6 prefix is /128")
    
    all_subnets = net.subnets(new_prefix=target_prefix)
    result = []
    for i, subnet in enumerate(all_subnets):
        if i >= count:
            break
        result.append(subnet)
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATION_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def validate_ip_in_network(ip: str, network: str) -> bool:
    """Check if an IP address belongs to a network."""
    try:
        addr = ipaddress.ip_address(ip)
        net = ipaddress.ip_network(network, strict=False)
        return addr in net
    except ValueError:
        return False


def is_valid_host_address(cidr: str) -> Tuple[bool, str]:
    """Check if a CIDR address can be used as host address."""
    try:
        info = analyze_ipv4_interface(cidr)
        if info.address_type == "network":
            return False, f"Address {info.address} is the network address for {info.network}"
        elif info.address_type == "broadcast":
            return False, f"Address {info.address} is the broadcast address for {info.network}"
        else:
            return True, f"Valid host address in network {info.network}"
    except ValueError as e:
        return False, str(e)


def summarize_networks(networks: List[str]) -> List[ipaddress.IPv4Network]:
    """Summarise a list of IPv4 networks (supernetting/aggregation)."""
    nets = [ipaddress.ip_network(n, strict=False) for n in networks]
    return list(ipaddress.collapse_addresses(nets))


# ═══════════════════════════════════════════════════════════════════════════════
# CONVERSION_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def netmask_to_prefix(netmask: str) -> int:
    """Convert a network mask to prefix length."""
    mask = ipaddress.IPv4Address(netmask)
    binary = bin(int(mask))[2:].zfill(32)
    return binary.count('1')


def prefix_to_netmask(prefix: int) -> str:
    """Convert a prefix length to network mask."""
    if not 0 <= prefix <= 32:
        raise ValueError("Prefix must be between 0 and 32")
    bits = '1' * prefix + '0' * (32 - prefix)
    octets = [int(bits[i:i+8], 2) for i in range(0, 32, 8)]
    return '.'.join(map(str, octets))


def ip_to_binary(ip: str) -> str:
    """Convert an IP address to binary representation."""
    addr = ipaddress.IPv4Address(ip)
    return bin(int(addr))[2:].zfill(32)


def ip_to_dotted_binary(ip: str) -> str:
    """Convert IP to binary with dots between octets."""
    binary = ip_to_binary(ip)
    return '.'.join([binary[i:i+8] for i in range(0, 32, 8)])


if __name__ == "__main__":
    print("=== Network Utilities Demonstration ===\n")
    info = analyze_ipv4_interface("192.168.10.14/26")
    print(f"Analysis 192.168.10.14/26:")
    print(f"  Network: {info.network}, Usable hosts: {info.usable_hosts}")
    print(f"  Range: {info.first_host} - {info.last_host}")
