#!/usr/bin/env python3
"""
Firewall Rule Helper — Week 7
=============================
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

This tool applies small iptables rule profiles from `configs/firewall_profiles.json`.
It is intended for a lab router namespace created by Mininet or Docker networks.

Usage examples:
    sudo python3 src/apps/firewallctl.py --profile baseline
    sudo python3 src/apps/firewallctl.py --profile block_tcp_9090
    sudo python3 src/apps/firewallctl.py --profile block_tcp_9090 --dry-run

Profiles are defined in JSON format with the following structure:
    {
        "profile_name": {
            "description": "What this profile does",
            "forward_policy": "ACCEPT",
            "rules": [
                {"chain": "FORWARD", "proto": "tcp", "dport": 9090, "action": "DROP"}
            ]
        }
    }
"""

from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORT_DEPENDENCIES
# ═══════════════════════════════════════════════════════════════════════════════
import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Add parent directory to path for utils import
_script_dir = Path(__file__).resolve().parent
_utils_dir = _script_dir.parent / "utils"
if str(_utils_dir.parent) not in sys.path:
    sys.path.insert(0, str(_utils_dir.parent))

from utils.net_utils import run_cmd, is_root


# ═══════════════════════════════════════════════════════════════════════════════
# ARGUMENT_PARSING
# ═══════════════════════════════════════════════════════════════════════════════
def build_parser() -> argparse.ArgumentParser:
    """
    Build and return the command-line argument parser.
    
    Creates an ArgumentParser configured for firewall profile management
    with options for profile selection, configuration path and dry-run mode.
    
    Returns:
        Configured ArgumentParser instance ready for parse_args()
    """
    default_config = str(
        Path(__file__).resolve().parent.parent.parent 
        / "docker" / "configs" / "firewall_profiles.json"
    )
    
    parser = argparse.ArgumentParser(
        description="Apply iptables profiles for Week 7 laboratory.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  sudo python3 firewallctl.py --profile baseline
  sudo python3 firewallctl.py --profile block_tcp_9090 --dry-run
  sudo python3 firewallctl.py --profile block_udp_9091

Available profiles (default config):
  - baseline: Allow all traffic (permissive)
  - block_tcp_9090: Block TCP port 9090 with DROP
  - block_udp_9091: Block UDP port 9091 with DROP
  - reject_tcp_9090: Block TCP port 9090 with REJECT
"""
    )
    parser.add_argument(
        "--profile", 
        required=True, 
        help="Profile name from firewall_profiles.json"
    )
    parser.add_argument(
        "--config", 
        default=default_config, 
        help="Path to profiles JSON file (default: docker/configs/firewall_profiles.json)"
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="Print commands without executing them"
    )
    
    return parser


# ═══════════════════════════════════════════════════════════════════════════════
# IPTABLES_EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════
def execute_iptables(argv: list[str], dry_run: bool) -> None:
    """
    Execute an iptables command or print it in dry-run mode.
    
    Wraps the iptables command execution with dry-run support for
    safe testing of firewall rules before applying them.
    
    Args:
        argv: Complete iptables command as list of arguments
        dry_run: If True, print command instead of executing
        
    Raises:
        subprocess.CalledProcessError: If iptables command fails (not in dry-run)
    """
    if dry_run:
        print(f"[dry-run] {' '.join(argv)}")
        return
    
    run_cmd(argv, timeout=10, check=True)


def apply_profile(profile: dict[str, Any], dry_run: bool) -> None:
    """
    Apply a firewall profile by executing its rules.
    
    Clears the FORWARD chain, sets the default policy, then applies
    each rule from the profile in order.
    
    Args:
        profile: Profile dictionary with 'rules' and 'forward_policy' keys
        dry_run: If True, print commands instead of executing
    """
    rules = profile.get("rules", [])
    forward_policy = profile.get("forward_policy", "ACCEPT")
    
    # Clear FORWARD chain and set policy
    execute_iptables(["iptables", "-F", "FORWARD"], dry_run)
    execute_iptables(["iptables", "-P", "FORWARD", forward_policy], dry_run)
    
    # Apply rules in order
    for rule in rules:
        argv = build_rule_command(rule)
        execute_iptables(argv, dry_run)


def build_rule_command(rule: dict[str, Any]) -> list[str]:
    """
    Build iptables command from a rule dictionary.
    
    Converts a rule specification dictionary into a complete iptables
    command line argument list.
    
    Args:
        rule: Dictionary with keys: chain, proto, dport, action
        
    Returns:
        List of command arguments for iptables
    """
    chain = rule.get("chain", "FORWARD")
    proto = rule.get("proto")
    action = rule.get("action", "ACCEPT")
    dport = rule.get("dport")
    
    argv = ["iptables", "-A", chain]
    
    if proto:
        argv += ["-p", str(proto)]
    if dport is not None:
        argv += ["--dport", str(dport)]
    
    argv += ["-j", str(action)]
    
    return argv


def display_current_rules(dry_run: bool) -> None:
    """
    Display current FORWARD chain rules for verification.
    
    Shows the resulting iptables rules after profile application
    for transparency and debugging.
    
    Args:
        dry_run: If True, skip display (rules not actually applied)
    """
    if dry_run:
        return
    
    result = run_cmd(
        ["iptables", "-L", "FORWARD", "-n", "-v"], 
        timeout=10, 
        check=False
    )
    print(result.stdout)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """
    Main entry point for the firewall control utility.
    
    Parses arguments, loads the specified profile and applies
    the firewall rules. Requires root privileges unless in dry-run mode.
    
    Returns:
        Exit code: 0 for success, 2 for permission error, 3 for unknown profile
    """
    args = build_parser().parse_args()
    
    # Check for root privileges
    if not is_root() and not args.dry_run:
        print("This tool needs root privileges. Use sudo or --dry-run.")
        return 2
    
    # Load configuration
    cfg_path = Path(args.config)
    if not cfg_path.exists():
        print(f"Configuration file not found: {cfg_path}")
        return 3
    
    data: dict[str, Any] = json.loads(cfg_path.read_text(encoding="utf-8"))
    
    # Validate profile exists
    if args.profile not in data:
        print(f"Unknown profile: {args.profile}")
        print(f"Available profiles: {', '.join(sorted(data.keys()))}")
        return 3
    
    profile = data[args.profile]
    
    # Display profile info
    print(f"Applying profile: {args.profile}")
    if "description" in profile:
        print(f"Description: {profile['description']}")
    
    # Apply the profile
    apply_profile(profile, args.dry_run)
    
    # Show resulting rules
    display_current_rules(args.dry_run)
    
    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# SCRIPT_EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    raise SystemExit(main())
