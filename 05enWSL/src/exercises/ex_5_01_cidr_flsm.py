#!/usr/bin/env python3
"""
Exercise 5.01 – CIDR Analysis and FLSM Subnetting
=================================================
CLI for calculating network parameters and splitting into equal subnets.

Usage:
    python ex_5_01_cidr_flsm.py analyse 192.168.10.14/26 [--verbose] [--json]
    python ex_5_01_cidr_flsm.py flsm 192.168.100.0/24 4
    python ex_5_01_cidr_flsm.py binary 192.168.10.14

Learning Objectives:
    - Calculate network parameters from CIDR notation
    - Understand binary representation of IP addresses
    - Apply FLSM subnetting to partition networks

Pair Programming Notes:
    - Driver: Execute commands and observe output
    - Navigator: Predict results before execution, verify accuracy
    - Swap after each exercise section

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
    analyze_ipv4_interface,
    flsm_split,
    ipv4_host_range,
    ip_to_binary,
    ip_to_dotted_binary,
    prefix_to_netmask,
    netmask_to_prefix,
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
    UNDERLINE = '\033[4m'
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
def prompt_prediction_analyze(target: str) -> None:
    """
    Display prediction prompt before CIDR analysis.
    
    Implements Brown & Wilson Principle 4: Predictions before execution
    help students engage actively with the material.
    """
    print()
    print(colourise("💭 PREDICTION TIME", Colours.YELLOW))
    print(colourise("─" * 50, Colours.YELLOW))
    print(f"  Before seeing the answer for {colourise(target, Colours.GREEN)}:")
    print("  1. What is the network address?")
    print("  2. What is the broadcast address?")
    print("  3. How many usable hosts?")
    print()
    input(colourise("  Press Enter when ready to check your answers...", Colours.CYAN))


def prompt_prediction_flsm(base: str, n_subnets: int) -> None:
    """Display prediction prompt before FLSM subnetting."""
    print()
    print(colourise("💭 PREDICTION TIME", Colours.YELLOW))
    print(colourise("─" * 50, Colours.YELLOW))
    print(f"  Splitting {colourise(base, Colours.GREEN)} into {n_subnets} subnets:")
    print("  1. How many bits need to be borrowed?")
    print("  2. What will the new prefix length be?")
    print("  3. How many hosts per subnet?")
    print()
    input(colourise("  Press Enter when ready to check your answers...", Colours.CYAN))


# ═══════════════════════════════════════════════════════════════════════════════
# COMMAND_ANALYZE
# ═══════════════════════════════════════════════════════════════════════════════
def cmd_analyze(target: str, verbose: bool = False, as_json: bool = False, 
                predict: bool = False) -> int:
    """
    Analyse an IPv4 address with CIDR prefix.
    
    This command calculates all network parameters from a CIDR notation
    address, including network address, broadcast, usable host range
    and address classification.
    
    Args:
        target: IPv4 address with prefix (e.g., '192.168.10.14/26')
        verbose: If True, show binary representations and explanations
        as_json: If True, output in JSON format
        predict: If True, show prediction prompt first
        
    Returns:
        0 on success, 1 on error
    """
    # ─────────────────────────────────────────────────────────────────────────
    # SHOW_PREDICTION_PROMPT
    # ─────────────────────────────────────────────────────────────────────────
    if predict and not as_json:
        prompt_prediction_analyze(target)
    
    # ─────────────────────────────────────────────────────────────────────────
    # PARSE_AND_VALIDATE_INPUT
    # ─────────────────────────────────────────────────────────────────────────
    try:
        info = analyze_ipv4_interface(target)
    except ValueError as e:
        print(colourise(f"Error: {e}", Colours.RED), file=sys.stderr)
        return 1
    
    # ─────────────────────────────────────────────────────────────────────────
    # BUILD_OUTPUT_PAYLOAD
    # ─────────────────────────────────────────────────────────────────────────
    payload = {
        "input": target,
        "address": str(info.address),
        "address_type": info.address_type,
        "network": str(info.network.network_address),
        "prefix": info.network.prefixlen,
        "netmask": str(info.netmask),
        "wildcard": str(info.wildcard),
        "broadcast": str(info.broadcast),
        "total_addresses": info.total_addresses,
        "usable_hosts": info.usable_hosts,
        "first_host": str(info.first_host) if info.first_host else None,
        "last_host": str(info.last_host) if info.last_host else None,
        "is_private": info.is_private,
    }
    
    # ─────────────────────────────────────────────────────────────────────────
    # OUTPUT_JSON_FORMAT
    # ─────────────────────────────────────────────────────────────────────────
    if as_json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0
    
    # ─────────────────────────────────────────────────────────────────────────
    # OUTPUT_FORMATTED_DISPLAY
    # ─────────────────────────────────────────────────────────────────────────
    print()
    print(colourise("═" * 50, Colours.BLUE))
    print(colourise("  IPv4 CIDR Analysis", Colours.BOLD))
    print(colourise("═" * 50, Colours.BLUE))
    print()
    
    print(f"  {colourise('Input:', Colours.CYAN):30} {target}")
    print(f"  {colourise('IP Address:', Colours.CYAN):30} {info.address}")
    print(f"  {colourise('Address Type:', Colours.CYAN):30} {colourise(info.address_type.upper(), Colours.YELLOW)}")
    print()
    
    print(f"  {colourise('Network Address:', Colours.CYAN):30} {info.network.network_address}/{info.network.prefixlen}")
    print(f"  {colourise('Subnet Mask:', Colours.CYAN):30} {info.netmask}")
    print(f"  {colourise('Wildcard Mask:', Colours.CYAN):30} {info.wildcard}")
    print(f"  {colourise('Broadcast Address:', Colours.CYAN):30} {info.broadcast}")
    print()
    
    print(f"  {colourise('Total Addresses:', Colours.CYAN):30} {info.total_addresses}")
    print(f"  {colourise('Usable Hosts:', Colours.CYAN):30} {colourise(str(info.usable_hosts), Colours.GREEN)}")
    print(f"  {colourise('First Host:', Colours.CYAN):30} {info.first_host or 'N/A'}")
    print(f"  {colourise('Last Host:', Colours.CYAN):30} {info.last_host or 'N/A'}")
    print()
    
    print(f"  {colourise('Private Address:', Colours.CYAN):30} {'Yes' if info.is_private else 'No'}")
    
    # ─────────────────────────────────────────────────────────────────────────
    # OUTPUT_VERBOSE_BINARY_DETAILS
    # ─────────────────────────────────────────────────────────────────────────
    if verbose:
        print()
        print(colourise("─" * 50, Colours.BLUE))
        print(colourise("  Binary Representation", Colours.BOLD))
        print(colourise("─" * 50, Colours.BLUE))
        print()
        
        addr_bin = ip_to_dotted_binary(str(info.address))
        mask_bin = ip_to_dotted_binary(str(info.netmask))
        net_bin = ip_to_dotted_binary(str(info.network.network_address))
        bcast_bin = ip_to_dotted_binary(str(info.broadcast))
        
        prefix = info.network.prefixlen
        
        print(f"  {colourise('IP (binary):', Colours.CYAN):30}")
        print(f"    {colourise(addr_bin[:prefix], Colours.GREEN)}{addr_bin[prefix:]}")
        print(f"    {'─' * prefix}{'^' * (35 - prefix)} host portion")
        print()
        
        print(f"  {colourise('Mask (binary):', Colours.CYAN):30}")
        print(f"    {mask_bin}")
        print()
        
        print(f"  {colourise('Network (binary):', Colours.CYAN):30}")
        print(f"    {net_bin}")
        print()
        
        print(f"  {colourise('Broadcast (binary):', Colours.CYAN):30}")
        print(f"    {bcast_bin}")
        print()
        
        # ─────────────────────────────────────────────────────────────────────
        # OUTPUT_CALCULATION_EXPLANATION
        # ─────────────────────────────────────────────────────────────────────
        print(colourise("─" * 50, Colours.BLUE))
        print(colourise("  Calculation Explanation", Colours.BOLD))
        print(colourise("─" * 50, Colours.BLUE))
        print()
        
        host_bits = 32 - prefix
        print(f"  • Prefix /{prefix} = {prefix} bits for network, {host_bits} bits for host")
        print(f"  • Total addresses = 2^{host_bits} = {2**host_bits}")
        print(f"  • Usable hosts = 2^{host_bits} - 2 = {2**host_bits - 2}")
        print(f"  • Network address: all host bits = 0")
        print(f"  • Broadcast address: all host bits = 1")
    
    print()
    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# COMMAND_FLSM
# ═══════════════════════════════════════════════════════════════════════════════
def cmd_flsm(base: str, n_subnets: int, as_json: bool = False, 
             predict: bool = False) -> int:
    """
    Split a network into N equal subnets using FLSM.
    
    Fixed Length Subnet Mask creates equal-sized subnets by borrowing
    the same number of bits from each subnet's host portion.
    
    Args:
        base: Base network in CIDR format (e.g., '192.168.100.0/24')
        n_subnets: Number of subnets (must be power of 2)
        as_json: If True, output in JSON format
        predict: If True, show prediction prompt first
        
    Returns:
        0 on success, 1 on error
    """
    # ─────────────────────────────────────────────────────────────────────────
    # SHOW_PREDICTION_PROMPT
    # ─────────────────────────────────────────────────────────────────────────
    if predict and not as_json:
        prompt_prediction_flsm(base, n_subnets)
    
    # ─────────────────────────────────────────────────────────────────────────
    # CALCULATE_SUBNETS
    # ─────────────────────────────────────────────────────────────────────────
    try:
        subnets = flsm_split(base, n_subnets)
    except ValueError as e:
        print(colourise(f"Error: {e}", Colours.RED), file=sys.stderr)
        return 1
    
    # ─────────────────────────────────────────────────────────────────────────
    # OUTPUT_JSON_FORMAT
    # ─────────────────────────────────────────────────────────────────────────
    if as_json:
        result = []
        for subnet in subnets:
            first, last, usable = ipv4_host_range(subnet)
            result.append({
                "network": str(subnet.network_address),
                "prefix": subnet.prefixlen,
                "cidr": str(subnet),
                "broadcast": str(subnet.broadcast_address),
                "usable_hosts": usable,
                "first_host": str(first) if first else None,
                "last_host": str(last) if last else None,
            })
        print(json.dumps({"base": base, "num_subnets": n_subnets, "subnets": result}, indent=2))
        return 0
    
    # ─────────────────────────────────────────────────────────────────────────
    # CALCULATE_METADATA
    # ─────────────────────────────────────────────────────────────────────────
    import ipaddress
    base_net = ipaddress.ip_network(base, strict=True)
    bits_added = n_subnets.bit_length() - 1
    new_prefix = base_net.prefixlen + bits_added
    
    # ─────────────────────────────────────────────────────────────────────────
    # OUTPUT_FORMATTED_DISPLAY
    # ─────────────────────────────────────────────────────────────────────────
    print()
    print(colourise("═" * 60, Colours.BLUE))
    print(colourise("  FLSM Subnetting (Fixed Length Subnet Mask)", Colours.BOLD))
    print(colourise("═" * 60, Colours.BLUE))
    print()
    
    print(f"  {colourise('Base Network:', Colours.CYAN):30} {base}")
    print(f"  {colourise('Number of Subnets:', Colours.CYAN):30} {n_subnets}")
    print(f"  {colourise('Borrowed Bits:', Colours.CYAN):30} {bits_added}")
    print(f"  {colourise('New Prefix:', Colours.CYAN):30} /{new_prefix}")
    print(f"  {colourise('Increment:', Colours.CYAN):30} {2**(32-new_prefix)} addresses")
    print()
    
    # ─────────────────────────────────────────────────────────────────────────
    # OUTPUT_SUBNET_TABLE
    # ─────────────────────────────────────────────────────────────────────────
    print(colourise("─" * 60, Colours.BLUE))
    print(f"  {'No.':>4}  {'Subnet':<20} {'Broadcast':<18} {'Hosts':<10} {'Range'}")
    print(colourise("─" * 60, Colours.BLUE))
    
    for i, subnet in enumerate(subnets, 1):
        first, last, usable = ipv4_host_range(subnet)
        interval = f"{first}..{last}" if first and last else "N/A"
        print(f"  {i:>4}. {str(subnet):<20} {str(subnet.broadcast_address):<18} {usable:<10} {interval}")
    
    print(colourise("─" * 60, Colours.BLUE))
    print()
    
    # ─────────────────────────────────────────────────────────────────────────
    # OUTPUT_SUMMARY
    # ─────────────────────────────────────────────────────────────────────────
    total_usable = sum(ipv4_host_range(s)[2] for s in subnets)
    print(f"  {colourise('Total Usable Hosts:', Colours.GREEN)} {total_usable}")
    print()
    
    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# COMMAND_BINARY
# ═══════════════════════════════════════════════════════════════════════════════
def cmd_binary(ip: str) -> int:
    """
    Display the binary representation of an IP address.
    
    Shows the address in both continuous 32-bit format and
    dotted binary format with octet breakdown.
    
    Args:
        ip: IPv4 address (e.g., '192.168.1.1')
        
    Returns:
        0 on success, 1 on error
    """
    # ─────────────────────────────────────────────────────────────────────────
    # VALIDATE_INPUT
    # ─────────────────────────────────────────────────────────────────────────
    try:
        import ipaddress
        addr = ipaddress.IPv4Address(ip)
    except ValueError as e:
        print(colourise(f"Error: {e}", Colours.RED), file=sys.stderr)
        return 1
    
    # ─────────────────────────────────────────────────────────────────────────
    # CONVERT_TO_BINARY
    # ─────────────────────────────────────────────────────────────────────────
    binary = ip_to_binary(ip)
    dotted = ip_to_dotted_binary(ip)
    
    # ─────────────────────────────────────────────────────────────────────────
    # OUTPUT_FORMATTED_DISPLAY
    # ─────────────────────────────────────────────────────────────────────────
    print()
    print(colourise("═" * 50, Colours.BLUE))
    print(colourise("  IP → Binary Conversion", Colours.BOLD))
    print(colourise("═" * 50, Colours.BLUE))
    print()
    
    print(f"  {colourise('Decimal IP:', Colours.CYAN):25} {ip}")
    print(f"  {colourise('Full Binary:', Colours.CYAN):25} {binary}")
    print(f"  {colourise('Dotted Binary:', Colours.CYAN):25} {dotted}")
    print()
    
    # ─────────────────────────────────────────────────────────────────────────
    # OUTPUT_OCTET_BREAKDOWN
    # ─────────────────────────────────────────────────────────────────────────
    octets = ip.split('.')
    print(colourise("  Conversion by Octets:", Colours.CYAN))
    for i, octet in enumerate(octets):
        oct_bin = bin(int(octet))[2:].zfill(8)
        print(f"    Octet {i+1}: {octet:>3} → {oct_bin}")
    print()
    
    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# COMMAND_QUIZ
# ═══════════════════════════════════════════════════════════════════════════════
def cmd_quiz() -> int:
    """
    Generate a random quick quiz question for practice.
    
    Creates a random CIDR address and challenges the student
    to calculate network parameters before revealing the answer.
    
    Returns:
        0 on success
    """
    import random
    
    # ─────────────────────────────────────────────────────────────────────────
    # GENERATE_RANDOM_ADDRESS
    # ─────────────────────────────────────────────────────────────────────────
    octets = [random.randint(1, 254) for _ in range(4)]
    prefix = random.choice([24, 25, 26, 27, 28, 29, 30])
    
    ip = '.'.join(map(str, octets))
    cidr = f"{ip}/{prefix}"
    
    # ─────────────────────────────────────────────────────────────────────────
    # DISPLAY_CHALLENGE
    # ─────────────────────────────────────────────────────────────────────────
    print()
    print(colourise("═" * 50, Colours.YELLOW))
    print(colourise("  Quick Quiz: CIDR Analysis", Colours.BOLD))
    print(colourise("═" * 50, Colours.YELLOW))
    print()
    print(f"  Address: {colourise(cidr, Colours.GREEN)}")
    print()
    print("  Calculate:")
    print("  1. Network address")
    print("  2. Broadcast address")
    print("  3. Number of usable hosts")
    print("  4. First and last usable host")
    print()
    
    input(colourise("  Press Enter to see the answer...", Colours.CYAN))
    
    return cmd_analyze(cidr, verbose=False, as_json=False)


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
        description="Exercise 5.01 – CIDR Analysis and FLSM Subnetting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s analyse 192.168.10.14/26           Analyse the address
  %(prog)s analyse 192.168.10.14/26 --verbose With detailed explanations
  %(prog)s analyse 192.168.10.14/26 --json    JSON output
  %(prog)s analyse 192.168.10.14/26 --predict With prediction prompt
  %(prog)s flsm 192.168.100.0/24 4            Split into 4 subnets
  %(prog)s flsm 10.0.0.0/24 8                 Split into 8 subnets
  %(prog)s binary 192.168.1.1                 Binary conversion
  %(prog)s quiz                               Random quick quiz
"""
    )
    
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # ─────────────────────────────────────────────────────────────────────────
    # SUBPARSER_ANALYZE
    # ─────────────────────────────────────────────────────────────────────────
    p_analyze = subparsers.add_parser(
        "analyse",
        help="Analyse an IPv4 address with CIDR prefix"
    )
    p_analyze.add_argument(
        "target",
        help="IPv4 address with prefix (e.g., 192.168.10.14/26)"
    )
    p_analyze.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Display detailed explanations and binary representation"
    )
    p_analyze.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output in JSON format"
    )
    p_analyze.add_argument(
        "--predict", "-p",
        action="store_true",
        help="Show prediction prompt before results"
    )
    
    # ─────────────────────────────────────────────────────────────────────────
    # SUBPARSER_FLSM
    # ─────────────────────────────────────────────────────────────────────────
    p_flsm = subparsers.add_parser(
        "flsm",
        help="Split a network into N equal subnets (FLSM)"
    )
    p_flsm.add_argument(
        "base",
        help="Base network in CIDR format (e.g., 192.168.100.0/24)"
    )
    p_flsm.add_argument(
        "n",
        type=int,
        help="Number of subnets (power of 2)"
    )
    p_flsm.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output in JSON format"
    )
    p_flsm.add_argument(
        "--predict", "-p",
        action="store_true",
        help="Show prediction prompt before results"
    )
    
    # ─────────────────────────────────────────────────────────────────────────
    # SUBPARSER_BINARY
    # ─────────────────────────────────────────────────────────────────────────
    p_binary = subparsers.add_parser(
        "binary",
        help="Display the binary representation of an IP address"
    )
    p_binary.add_argument(
        "ip",
        help="IPv4 address (e.g., 192.168.1.1)"
    )
    
    # ─────────────────────────────────────────────────────────────────────────
    # SUBPARSER_QUIZ
    # ─────────────────────────────────────────────────────────────────────────
    subparsers.add_parser(
        "quiz",
        help="Generate a random quick quiz question"
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
    
    if args.command == "analyse":
        return cmd_analyze(args.target, args.verbose, args.json, 
                          getattr(args, 'predict', False))
    elif args.command == "flsm":
        return cmd_flsm(args.base, args.n, args.json,
                       getattr(args, 'predict', False))
    elif args.command == "binary":
        return cmd_binary(args.ip)
    elif args.command == "quiz":
        return cmd_quiz()
    
    return 1


if __name__ == "__main__":
    sys.exit(main())
