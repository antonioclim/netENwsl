#!/usr/bin/env python3
"""
Homework 1.01: Network Configuration Report Generator
NETWORKING class - ASE, Informatics | by Revolvix

This starter script helps you gather network configuration information.
Complete the TODO sections to generate your report.

Usage:
    python hw_1_01_network_report.py --output network_report.md
"""

from __future__ import annotations

import argparse
import subprocess
import socket
from datetime import datetime
from pathlib import Path
from typing import List, Dict


def run_command(cmd: List[str]) -> str:
    """Execute a command and return its output."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
    except Exception as e:
        return f"Error: {e}"


def get_interfaces() -> str:
    """Get network interface information."""
    return run_command(["ip", "-br", "addr", "show"])


def get_detailed_interfaces() -> str:
    """Get detailed network interface information."""
    return run_command(["ip", "addr", "show"])


def get_routing_table() -> str:
    """Get the routing table."""
    return run_command(["ip", "route", "show"])


def get_active_connections() -> str:
    """Get active network connections."""
    return run_command(["ss", "-tunap"])


def get_dns_config() -> str:
    """Get DNS configuration."""
    try:
        with open("/etc/resolv.conf", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "DNS configuration file not found"


def get_hostname_info() -> Dict[str, str]:
    """Get hostname and related information."""
    hostname = socket.gethostname()
    try:
        ip = socket.gethostbyname(hostname)
    except socket.error:
        ip = "Unable to resolve"
    
    return {
        "hostname": hostname,
        "ip": ip
    }


def generate_report(output_path: Path) -> None:
    """Generate the network configuration report."""
    
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
    print(f"Report generated: {output_path}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate network configuration report"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=Path("network_report.md"),
        help="Output file path (default: network_report.md)"
    )
    args = parser.parse_args()
    
    generate_report(args.output)
    
    print("\nNext steps:")
    print("1. Open the generated report in a text editor")
    print("2. Complete the TODO sections with your analysis")
    print("3. Add any additional observations")
    print("4. Submit according to homework guidelines")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
