#!/usr/bin/env python3
"""
Homework 1.01: Network Configuration Report Generator
=====================================================
Computer Networks - Week 1 (WSL Environment)
ASE Bucharest | by ing. dr. Antonio Clim

Objectives:
- Recall core Linux networking commands and their output formats
- Demonstrate ability to gather and interpret network configuration data
- Apply report generation techniques to summarise system state

Prerequisites:
- Linux environment (WSL2 Ubuntu or container)
- Basic understanding of IP addresses and routing

Level: Beginner
Estimated time: 30-45 minutes

Pair Programming Notes:
- Driver: Execute commands and observe output structure
- Navigator: Predict output format before each command runs
- Swap after: Completing each major section of the report

Usage:
    python hw_1_01_network_report.py --output network_report.md
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import subprocess
import socket
from datetime import datetime
from pathlib import Path
from typing import List, Dict


# ═══════════════════════════════════════════════════════════════════════════════
# PREDICTION_PROMPT
# ═══════════════════════════════════════════════════════════════════════════════
def prompt_prediction() -> None:
    """
    Ask student to predict report contents before generation.
    
    This implements Brown & Wilson Principle 4: Predictions help build
    mental models of system behaviour.
    """
    print("\n" + "=" * 60)
    print("💭 PREDICTION TIME")
    print("=" * 60)
    print("Before generating the report, predict:")
    print("  1. How many network interfaces will be listed?")
    print("  2. What IP address ranges do you expect to see?")
    print("  3. Will there be any active network connections?")
    print("=" * 60)
    input("Press Enter to continue and verify your predictions...")
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# COMMAND_EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════
def run_command(cmd: List[str]) -> str:
    """
    Execute a shell command and return its output.
    
    Args:
        cmd: Command and arguments as a list of strings
        
    Returns:
        Command stdout on success, error message on failure
        
    Example:
        >>> run_command(["ip", "addr", "show"])
        '1: lo: <LOOPBACK,UP,LOWER_UP>...'
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds"
    except FileNotFoundError:
        return f"Error: Command not found: {cmd[0]}"
    except Exception as e:
        return f"Error: {e}"


# ═══════════════════════════════════════════════════════════════════════════════
# DATA_GATHERING
# ═══════════════════════════════════════════════════════════════════════════════
def get_interfaces() -> str:
    """Get brief network interface information using ip command."""
    return run_command(["ip", "-br", "addr", "show"])


def get_detailed_interfaces() -> str:
    """Get detailed network interface information including MTU and flags."""
    return run_command(["ip", "addr", "show"])


def get_routing_table() -> str:
    """Get the IP routing table showing default gateway and local routes."""
    return run_command(["ip", "route", "show"])


def get_active_connections() -> str:
    """
    Get active network connections and listening sockets.
    
    Uses ss (socket statistics) which is the modern replacement for netstat.
    Flags: -t (TCP), -u (UDP), -n (numeric), -a (all), -p (process)
    """
    return run_command(["ss", "-tunap"])


def get_dns_config() -> str:
    """
    Get DNS resolver configuration from /etc/resolv.conf.
    
    This file specifies which DNS servers the system uses for name resolution.
    """
    try:
        with open("/etc/resolv.conf", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "DNS configuration file not found"
    except PermissionError:
        return "Permission denied reading DNS configuration"


def get_hostname_info() -> Dict[str, str]:
    """
    Get hostname and attempt to resolve it to an IP address.
    
    Returns:
        Dictionary with 'hostname' and 'ip' keys
    """
    hostname = socket.gethostname()
    try:
        ip = socket.gethostbyname(hostname)
    except socket.error:
        ip = "Unable to resolve"
    
    return {
        "hostname": hostname,
        "ip": ip
    }


# ═══════════════════════════════════════════════════════════════════════════════
# REPORT_GENERATION
# ═══════════════════════════════════════════════════════════════════════════════
def generate_report(output_path: Path) -> None:
    """
    Generate a complete network configuration report in Markdown format.
    
    The report includes sections for interfaces, routing, connections, DNS
    and analysis prompts for the student to complete.
    
    Args:
        output_path: Where to save the generated report
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hostname_info = get_hostname_info()
    
    report = f"""# Network Configuration Report

> Generated: {timestamp}
> Hostname: {hostname_info['hostname']}

## 1. Network Interfaces

### Brief Overview

```
{get_interfaces()}
```

### Detailed Configuration

```
{get_detailed_interfaces()}
```

**Analysis:**
<!-- TODO: Add your analysis of the interfaces here -->
<!-- - What interfaces are present? -->
<!-- - What are their IP addresses and subnet masks? -->
<!-- - Which interfaces are active? -->


## 2. Routing Table

```
{get_routing_table()}
```

**Analysis:**
<!-- TODO: Explain each route -->
<!-- - What is the default gateway? -->
<!-- - What local networks are directly reachable? -->


## 3. Active Network Connections

```
{get_active_connections()}
```

**Analysis:**
<!-- TODO: Analyse the connections -->
<!-- - What services are listening? -->
<!-- - Are there any established connections? -->


## 4. DNS Configuration

```
{get_dns_config()}
```

**Analysis:**
<!-- TODO: Explain the DNS configuration -->
<!-- - What DNS servers are configured? -->
<!-- - Are they public or private DNS? -->


## 5. Interesting Findings

<!-- TODO: Document at least one interesting or unusual finding -->
<!-- - Did you find anything unexpected? -->
<!-- - Any security considerations? -->


## 6. Conclusions

<!-- TODO: Summarise your findings -->


---

*Report generated for NETWORKING class - ASE, Informatics*
"""
    
    output_path.write_text(report, encoding="utf-8")
    print(f"✅ Report generated: {output_path}")


# ═══════════════════════════════════════════════════════════════════════════════
# PARSE_ARGUMENTS
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for report configuration."""
    parser = argparse.ArgumentParser(
        description="Generate network configuration report",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python hw_1_01_network_report.py
  python hw_1_01_network_report.py --output my_report.md
  python hw_1_01_network_report.py --no-predict
        """
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=Path("network_report.md"),
        help="Output file path (default: network_report.md)"
    )
    parser.add_argument(
        "--no-predict",
        action="store_true",
        help="Skip the prediction prompt"
    )
    return parser.parse_args()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """
    Main entry point for the homework assignment.
    
    Returns:
        Exit code (0 for success)
    """
    args = parse_args()
    
    # Prediction prompt for learning
    if not args.no_predict:
        prompt_prediction()
    
    # Generate report
    generate_report(args.output)
    
    # Next steps guidance
    print("\n📋 Next steps:")
    print("1. Open the generated report in a text editor")
    print("2. Complete the TODO sections with your analysis")
    print("3. Add any additional observations")
    print("4. Submit according to homework guidelines")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
