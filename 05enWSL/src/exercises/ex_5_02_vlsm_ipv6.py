#!/usr/bin/env python3
"""
Exercise 5.02 – VLSM and IPv6 Utilities
=======================================
CLI for VLSM allocation and IPv6 address operations.

Usage:
    python ex_5_02_vlsm_ipv6.py vlsm 172.16.0.0/24 60 20 10 2
    python ex_5_02_vlsm_ipv6.py ipv6 2001:0db8:0000:0000:0000:0000:0000:0001
    python ex_5_02_vlsm_ipv6.py ipv6-expand 2001:db8::1
    python ex_5_02_vlsm_ipv6.py ipv6-subnets 2001:db8:10::/48 64 5

Learning Objectives:
    - Apply VLSM for efficient address allocation
    - Understand IPv6 address representation and compression
    - Generate IPv6 subnet plans

Pair Programming Notes:
    - Driver: Run VLSM commands with different requirements
    - Navigator: Verify allocations are largest-first, check efficiency
    - Swap after completing IPv4 section, before IPv6

Author: ing. dr. Antonio Clim, ASE-CSIE Bucharest
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURE_MODULE_PATH
# ═══════════════════════════════════════════════════════════════════════════════
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORT_UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════
from src.utils.net_utils import (
    vlsm_allocate,
    ipv6_compress,
    ipv6_expand,
    ipv6_info,
    ipv6_subnets_from_prefix,
    prefix_for_hosts,
)


# ═══════════════════════════════════════════════════════════════════════════════
# DEFINE_COLOUR_CODES
# ═══════════════════════════════════════════════════════════════════════════════
class Colours:
    """ANSI colour codes for terminal output."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'


def colourise(text: str, colour: str) -> str:
    """
    Apply colour formatting if stdout is a terminal.
    
    Args:
        text: The text to colourise
        colour: ANSI colour code from Colours class
        
    Returns:
        Coloured text if terminal, plain text otherwise
    """
    if sys.stdout.isatty():
        return f"{colour}{text}{Colours.END}"
    return text


# ═══════════════════════════════════════════════════════════════════════════════
# PREDICTION_PROMPTS
# ═══════════════════════════════════════════════════════════════════════════════
def prompt_prediction_vlsm(base: str, requirements: List[int]) -> None:
    """
    Display prediction prompt before VLSM allocation.
    
    Implements Brown & Wilson Principle 4: Predictions before execution.
    """
    sorted_reqs = sorted(requirements, reverse=True)
    print()
    print(colourise("💭 PREDICTION TIME", Colours.YELLOW))
    print(colourise("─" * 50, Colours.YELLOW))
    print(f"  Base network: {colourise(base, Colours.GREEN)}")
    print(f"  Requirements: {requirements}")
    print(f"  Sorted (largest first): {sorted_reqs}")
    print()
    print("  Questions:")
    print(f"  1. What prefix will {sorted_reqs[0]} hosts need?")
    print(f"  2. What will be the first subnet allocated?")
    print("  3. Will all requirements fit in the available space?")
    print()
    input(colourise("  Press Enter when ready to check your answers...", Colours.CYAN))


def prompt_prediction_ipv6(address: str) -> None:
    """Display prediction prompt before IPv6 compression."""
    print()
    print(colourise("💭 PREDICTION TIME", Colours.YELLOW))
    print(colourise("─" * 50, Colours.YELLOW))
    print(f"  Full address: {colourise(address, Colours.GREEN)}")
    print()
    print("  Questions:")
    print("  1. How will this compress using :: notation?")
    print("  2. Where is the longest run of zero groups?")
    print("  3. What address type is this (global, link-local, etc.)?")
    print()
    input(colourise("  Press Enter when ready to check your answers...", Colours.CYAN))


# ═══════════════════════════════════════════════════════════════════════════════
# COMMAND_VLSM
# ═══════════════════════════════════════════════════════════════════════════════
def cmd_vlsm(base: str, requirements: List[int], as_json: bool = False,
             predict: bool = False) -> int:
    """
    Allocate subnets using Variable Length Subnet Mask.
    
    VLSM allocates different-sized subnets from a single address block,
    optimising address usage by matching subnet sizes to actual requirements.
    Requirements are automatically sorted largest-first for proper allocation.
    
    Args:
        base: Available network in CIDR format (e.g., '172.16.0.0/24')
        requirements: List of host requirements (e.g., [60, 20, 10, 2])
        as_json: If True, output in JSON format
        predict: If True, show prediction prompt first
        
    Returns:
        0 on success, 1 on error
    """
    # ─────────────────────────────────────────────────────────────────────────
    # SHOW_PREDICTION_PROMPT
    # ─────────────────────────────────────────────────────────────────────────
    if predict and not as_json:
        prompt_prediction_vlsm(base, requirements)
    
    # ─────────────────────────────────────────────────────────────────────────
    # PERFORM_VLSM_ALLOCATION
    # ─────────────────────────────────────────────────────────────────────────
    try:
        allocations = vlsm_allocate(base, requirements)
    except ValueError as e:
        print(colourise(f"Error: {e}", Colours.RED), file=sys.stderr)
        return 1
    
    # ─────────────────────────────────────────────────────────────────────────
    # OUTPUT_JSON_FORMAT
    # ─────────────────────────────────────────────────────────────────────────
    if as_json:
        result = []
        for alloc in allocations:
            result.append({
                "required_hosts": alloc.required_hosts,
                "prefix": alloc.allocated_prefix,
                "network": str(alloc.network),
                "gateway": str(alloc.gateway),
                "broadcast": str(alloc.broadcast),
                "usable_hosts": alloc.usable_hosts,
                "efficiency_percent": round(alloc.efficiency, 2),
            })
        output = {
            "base_network": base,
            "requirements": requirements,
            "allocations": result,
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return 0
    
    # ─────────────────────────────────────────────────────────────────────────
    # CALCULATE_METADATA
    # ─────────────────────────────────────────────────────────────────────────
    import ipaddress
    base_net = ipaddress.ip_network(base, strict=True)
    
    # ─────────────────────────────────────────────────────────────────────────
    # OUTPUT_FORMATTED_HEADER
    # ─────────────────────────────────────────────────────────────────────────
    print()
    print(colourise("═" * 70, Colours.BLUE))
    print(colourise("  VLSM Allocation (Variable Length Subnet Mask)", Colours.BOLD))
    print(colourise("═" * 70, Colours.BLUE))
    print()
    
    print(f"  {colourise('Available Network:', Colours.CYAN):30} {base}")
    print(f"  {colourise('Total Addresses:', Colours.CYAN):30} {base_net.num_addresses}")
    print(f"  {colourise('Host Requirements:', Colours.CYAN):30} {', '.join(map(str, requirements))}")
    print()
    
    # ─────────────────────────────────────────────────────────────────────────
    # OUTPUT_ALGORITHM_EXPLANATION
    # ─────────────────────────────────────────────────────────────────────────
    print(colourise("─" * 70, Colours.BLUE))
    print(colourise("  VLSM Algorithm:", Colours.BOLD))
    print(colourise("─" * 70, Colours.BLUE))
    print("  1. Sort requirements in descending order")
    print("  2. For each requirement, calculate minimum prefix needed")
    print("  3. Align start address to block boundary")
    print("  4. Allocate and advance cursor")
    print()
    
    # ─────────────────────────────────────────────────────────────────────────
    # OUTPUT_ALLOCATION_TABLE
    # ─────────────────────────────────────────────────────────────────────────
    print(colourise("─" * 70, Colours.BLUE))
    print(f"  {'#':>3}  {'Required':>8}  {'Prefix':>7}  {'Subnet':<20} {'Gateway':<16} {'Efficiency'}")
    print(colourise("─" * 70, Colours.BLUE))
    
    total_required = 0
    total_allocated = 0
    
    for i, alloc in enumerate(allocations, 1):
        efficiency_colour = Colours.GREEN if alloc.efficiency > 75 else Colours.YELLOW if alloc.efficiency > 50 else Colours.RED
        eff_str = colourise(f"{alloc.efficiency:5.1f}%", efficiency_colour)
        
        print(f"  {i:>3}  {alloc.required_hosts:>8}  /{alloc.allocated_prefix:<6}  "
              f"{str(alloc.network):<20} {str(alloc.gateway):<16} {eff_str}")
        
        total_required += alloc.required_hosts
        total_allocated += alloc.usable_hosts
    
    print(colourise("─" * 70, Colours.BLUE))
    
    # ─────────────────────────────────────────────────────────────────────────
    # OUTPUT_EFFICIENCY_SUMMARY
    # ─────────────────────────────────────────────────────────────────────────
    print()
    total_used = sum(alloc.network.num_addresses for alloc in allocations)
    remaining = base_net.num_addresses - total_used
    overall_efficiency = (total_required / total_allocated * 100) if total_allocated > 0 else 0
    
    print(f"  {colourise('Summary:', Colours.BOLD)}")
    print(f"    Total hosts required:     {total_required}")
    print(f"    Total hosts allocated:    {total_allocated}")
    print(f"    Overall efficiency:       {colourise(f'{overall_efficiency:.1f}%', Colours.GREEN)}")
    print(f"    Remaining free addresses: {remaining}")
    
    if remaining > 0:
        import ipaddress
        # Find the last allocated address
        last_alloc = max(allocations, key=lambda a: int(a.network.broadcast_address))
        next_addr = int(last_alloc.network.broadcast_address) + 1
        if next_addr <= int(base_net.broadcast_address):
            print(f"    First free address:       {ipaddress.IPv4Address(next_addr)}")
    
    print()
    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# COMMAND_IPV6_COMPRESS
# ═══════════════════════════════════════════════════════════════════════════════
def cmd_ipv6_compress(address: str, predict: bool = False) -> int:
    """
    Analyse and compress an IPv6 address.
    
    Shows the full form, compressed form, address type and scope.
    Demonstrates IPv6 compression rules.
    
    Args:
        address: IPv6 address in any valid format
        predict: If True, show prediction prompt first
        
    Returns:
        0 on success, 1 on error
    """
    # ─────────────────────────────────────────────────────────────────────────
    # SHOW_PREDICTION_PROMPT
    # ─────────────────────────────────────────────────────────────────────────
    if predict:
        prompt_prediction_ipv6(address)
    
    # ─────────────────────────────────────────────────────────────────────────
    # ANALYSE_ADDRESS
    # ─────────────────────────────────────────────────────────────────────────
    try:
        info = ipv6_info(address)
    except ValueError as e:
        print(colourise(f"Error: {e}", Colours.RED), file=sys.stderr)
        return 1
    
    # ─────────────────────────────────────────────────────────────────────────
    # OUTPUT_FORMATTED_DISPLAY
    # ─────────────────────────────────────────────────────────────────────────
    print()
    print(colourise("═" * 60, Colours.BLUE))
    print(colourise("  IPv6 Address Analysis", Colours.BOLD))
    print(colourise("═" * 60, Colours.BLUE))
    print()
    
    print(f"  {colourise('Input:', Colours.CYAN):30} {address}")
    print(f"  {colourise('Full Form:', Colours.CYAN):30} {info.full_form}")
    print(f"  {colourise('Compressed Form:', Colours.CYAN):30} {colourise(info.compressed, Colours.GREEN)}")
    print()
    
    print(f"  {colourise('Address Type:', Colours.CYAN):30} {info.address_type}")
    print(f"  {colourise('Scope:', Colours.CYAN):30} {info.scope}")
    
    if info.network:
        print(f"  {colourise('Network:', Colours.CYAN):30} {info.network}")
    
    print()
    
    # ─────────────────────────────────────────────────────────────────────────
    # OUTPUT_COMPRESSION_RULES
    # ─────────────────────────────────────────────────────────────────────────
    print(colourise("─" * 60, Colours.BLUE))
    print(colourise("  IPv6 Compression Rules:", Colours.BOLD))
    print(colourise("─" * 60, Colours.BLUE))
    print("  1. Remove leading zeros from each group")
    print("  2. Use :: for the longest sequence of zeros")
    print("  3. :: can only be used once")
    print()
    
    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# COMMAND_IPV6_EXPAND
# ═══════════════════════════════════════════════════════════════════════════════
def cmd_ipv6_expand(address: str) -> int:
    """
    Expand an IPv6 address to full form.
    
    Shows the complete 128-bit representation with all zeros included.
    
    Args:
        address: Compressed IPv6 address (e.g., '2001:db8::1')
        
    Returns:
        0 on success, 1 on error
    """
    # ─────────────────────────────────────────────────────────────────────────
    # EXPAND_ADDRESS
    # ─────────────────────────────────────────────────────────────────────────
    try:
        expanded = ipv6_expand(address)
    except ValueError as e:
        print(colourise(f"Error: {e}", Colours.RED), file=sys.stderr)
        return 1
    
    # ─────────────────────────────────────────────────────────────────────────
    # OUTPUT_FORMATTED_DISPLAY
    # ─────────────────────────────────────────────────────────────────────────
    print()
    print(colourise("═" * 60, Colours.BLUE))
    print(colourise("  IPv6 Address Expansion", Colours.BOLD))
    print(colourise("═" * 60, Colours.BLUE))
    print()
    
    print(f"  {colourise('Input (compressed):', Colours.CYAN):30} {address}")
    print(f"  {colourise('Output (expanded):', Colours.CYAN):30} {colourise(expanded, Colours.GREEN)}")
    print()
    
    # ─────────────────────────────────────────────────────────────────────────
    # OUTPUT_GROUP_BREAKDOWN
    # ─────────────────────────────────────────────────────────────────────────
    groups = expanded.split(':')
    print(colourise("  Hexadecimal Groups:", Colours.CYAN))
    for i, group in enumerate(groups):
        decimal_val = int(group, 16)
        print(f"    Group {i+1}: {group} = {decimal_val} (decimal)")
    print()
    
    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# COMMAND_IPV6_SUBNETS
# ═══════════════════════════════════════════════════════════════════════════════
def cmd_ipv6_subnets(base: str, target_prefix: int, count: int) -> int:
    """
    Generate IPv6 subnets from a base prefix.
    
    Creates a specified number of subnets with the target prefix length
    from a larger allocation.
    
    Args:
        base: Base prefix (e.g., '2001:db8:10::/48')
        target_prefix: Target prefix length (e.g., 64)
        count: Number of subnets to generate
        
    Returns:
        0 on success, 1 on error
    """
    # ─────────────────────────────────────────────────────────────────────────
    # GENERATE_SUBNETS
    # ─────────────────────────────────────────────────────────────────────────
    try:
        subnets = ipv6_subnets_from_prefix(base, target_prefix, count)
    except ValueError as e:
        print(colourise(f"Error: {e}", Colours.RED), file=sys.stderr)
        return 1
    
    # ─────────────────────────────────────────────────────────────────────────
    # CALCULATE_METADATA
    # ─────────────────────────────────────────────────────────────────────────
    import ipaddress
    base_net = ipaddress.ip_network(base, strict=True)
    total_possible = 2 ** (target_prefix - base_net.prefixlen)
    
    # ─────────────────────────────────────────────────────────────────────────
    # OUTPUT_FORMATTED_HEADER
    # ─────────────────────────────────────────────────────────────────────────
    print()
    print(colourise("═" * 70, Colours.BLUE))
    print(colourise("  IPv6 Subnetting", Colours.BOLD))
    print(colourise("═" * 70, Colours.BLUE))
    print()
    
    print(f"  {colourise('Base Prefix:', Colours.CYAN):30} {base}")
    print(f"  {colourise('Target Prefix:', Colours.CYAN):30} /{target_prefix}")
    print(f"  {colourise('Requested Subnets:', Colours.CYAN):30} {count}")
    print(f"  {colourise('Total Possible Subnets:', Colours.CYAN):30} {total_possible:,}")
    print()
    
    # ─────────────────────────────────────────────────────────────────────────
    # OUTPUT_SUBNET_TABLE
    # ─────────────────────────────────────────────────────────────────────────
    print(colourise("─" * 70, Colours.BLUE))
    print(f"  {'#':>3}  {'Subnet Prefix':<45} {'Suggested Gateway'}")
    print(colourise("─" * 70, Colours.BLUE))
    
    for i, subnet in enumerate(subnets, 1):
        # Gateway = first address (::1)
        gateway = subnet.network_address + 1
        print(f"  {i:>3}  {str(subnet):<45} {gateway}")
    
    print(colourise("─" * 70, Colours.BLUE))
    print()
    
    # ─────────────────────────────────────────────────────────────────────────
    # OUTPUT_NOTES
    # ─────────────────────────────────────────────────────────────────────────
    if target_prefix == 64:
        print(colourise("  Note:", Colours.YELLOW))
        print("  • /64 is the standard length for LANs (SLAAC)")
        print("  • Interface ID occupies the last 64 bits")
        print("  • Each /64 subnet can have 2^64 addresses")
    
    print()
    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# COMMAND_IPV6_TYPES
# ═══════════════════════════════════════════════════════════════════════════════
def cmd_ipv6_types() -> int:
    """
    Display reference information about IPv6 address types.
    
    Shows common prefixes, their purposes and example usage.
    
    Returns:
        0 (always succeeds)
    """
    # ─────────────────────────────────────────────────────────────────────────
    # OUTPUT_HEADER
    # ─────────────────────────────────────────────────────────────────────────
    print()
    print(colourise("═" * 65, Colours.BLUE))
    print(colourise("  IPv6 Address Types", Colours.BOLD))
    print(colourise("═" * 65, Colours.BLUE))
    print()
    
    # ─────────────────────────────────────────────────────────────────────────
    # OUTPUT_TYPE_TABLE
    # ─────────────────────────────────────────────────────────────────────────
    types = [
        ("::", "Unspecified address", "Used when we have no address"),
        ("::1", "Loopback", "Equivalent to 127.0.0.1"),
        ("fe80::/10", "Link-local", "Local communication, auto-configured"),
        ("fc00::/7", "Unique local", "Equivalent to RFC 1918 (private addresses)"),
        ("2000::/3", "Global unicast", "Internet routable addresses"),
        ("ff00::/8", "Multicast", "Communication to groups"),
    ]
    
    print(f"  {'Prefix':<15} {'Type':<20} {'Description'}")
    print(colourise("─" * 65, Colours.BLUE))
    
    for prefix, typ, desc in types:
        print(f"  {colourise(prefix, Colours.GREEN):<24} {typ:<20} {desc}")
    
    # ─────────────────────────────────────────────────────────────────────────
    # OUTPUT_EXAMPLES
    # ─────────────────────────────────────────────────────────────────────────
    print()
    print(colourise("  Practical Examples:", Colours.YELLOW))
    print("  • fe80::1             Link-local on interface")
    print("  • 2001:db8::1         Global unicast (documentation)")
    print("  • ff02::1             All-nodes multicast")
    print("  • ff02::2             All-routers multicast")
    print()
    
    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# BUILD_ARGUMENT_PARSER
# ═══════════════════════════════════════════════════════════════════════════════
def build_parser() -> argparse.ArgumentParser:
    """
    Build the command-line argument parser.
    
    Returns:
        Configured ArgumentParser with all subcommands
    """
    parser = argparse.ArgumentParser(
        description="Exercise 5.02 – VLSM and IPv6 Utilities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s vlsm 172.16.0.0/24 60 20 10 2       VLSM allocation
  %(prog)s vlsm 10.0.0.0/22 200 100 50 2 2    For large organisation
  %(prog)s vlsm 172.16.0.0/24 60 20 --predict  With prediction prompt
  
  %(prog)s ipv6 2001:0db8:0000:0000:0000:0000:0000:0001   IPv6 compression
  %(prog)s ipv6-expand 2001:db8::1                        IPv6 expansion
  %(prog)s ipv6-subnets 2001:db8:10::/48 64 10            Generate subnets
  %(prog)s ipv6-types                                      Type reference
"""
    )
    
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # ─────────────────────────────────────────────────────────────────────────
    # SUBPARSER_VLSM
    # ─────────────────────────────────────────────────────────────────────────
    p_vlsm = subparsers.add_parser(
        "vlsm",
        help="Allocate subnets with VLSM for a list of requirements"
    )
    p_vlsm.add_argument(
        "base",
        help="Available network in CIDR format (e.g., 172.16.0.0/24)"
    )
    p_vlsm.add_argument(
        "requirements",
        type=int,
        nargs="+",
        help="List of host requirements (e.g., 60 20 10 2)"
    )
    p_vlsm.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output in JSON format"
    )
    p_vlsm.add_argument(
        "--predict", "-p",
        action="store_true",
        help="Show prediction prompt before results"
    )
    
    # ─────────────────────────────────────────────────────────────────────────
    # SUBPARSER_IPV6
    # ─────────────────────────────────────────────────────────────────────────
    p_ipv6 = subparsers.add_parser(
        "ipv6",
        help="Analyse and compress an IPv6 address"
    )
    p_ipv6.add_argument(
        "address",
        help="IPv6 address in any format"
    )
    p_ipv6.add_argument(
        "--predict", "-p",
        action="store_true",
        help="Show prediction prompt before results"
    )
    
    # ─────────────────────────────────────────────────────────────────────────
    # SUBPARSER_IPV6_EXPAND
    # ─────────────────────────────────────────────────────────────────────────
    p_expand = subparsers.add_parser(
        "ipv6-expand",
        help="Expand an IPv6 address to full form"
    )
    p_expand.add_argument(
        "address",
        help="Compressed IPv6 address (e.g., 2001:db8::1)"
    )
    
    # ─────────────────────────────────────────────────────────────────────────
    # SUBPARSER_IPV6_SUBNETS
    # ─────────────────────────────────────────────────────────────────────────
    p_subnets = subparsers.add_parser(
        "ipv6-subnets",
        help="Generate IPv6 subnets from a prefix"
    )
    p_subnets.add_argument(
        "base",
        help="Base prefix (e.g., 2001:db8:10::/48)"
    )
    p_subnets.add_argument(
        "target_prefix",
        type=int,
        help="Target prefix length (e.g., 64)"
    )
    p_subnets.add_argument(
        "count",
        type=int,
        help="Number of subnets to generate"
    )
    
    # ─────────────────────────────────────────────────────────────────────────
    # SUBPARSER_IPV6_TYPES
    # ─────────────────────────────────────────────────────────────────────────
    subparsers.add_parser(
        "ipv6-types",
        help="Display IPv6 address types"
    )
    
    return parser


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main(argv: Optional[List[str]] = None) -> int:
    """
    Main entry point for the exercise.
    
    Args:
        argv: Command-line arguments (defaults to sys.argv)
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    
    if args.command == "vlsm":
        return cmd_vlsm(args.base, args.requirements, args.json,
                       getattr(args, 'predict', False))
    elif args.command == "ipv6":
        return cmd_ipv6_compress(args.address, getattr(args, 'predict', False))
    elif args.command == "ipv6-expand":
        return cmd_ipv6_expand(args.address)
    elif args.command == "ipv6-subnets":
        return cmd_ipv6_subnets(args.base, args.target_prefix, args.count)
    elif args.command == "ipv6-types":
        return cmd_ipv6_types()
    
    return 1


if __name__ == "__main__":
    sys.exit(main())
