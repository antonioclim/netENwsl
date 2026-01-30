#!/usr/bin/env python3
"""Homework 1.01: Network Configuration Report Generator

Computer Networks - Week 1 (WSL Environment)
ASE Bucharest | by ing. dr. Antonio Clim

Objectives
- Recall core Linux networking commands and their output formats
- Demonstrate ability to gather and interpret network configuration data
- Apply report generation techniques to summarise system state

Anti-AI note
This script can embed an Anti-AI verification token (from a Week 1 challenge
file) directly into the generated report. The intent is not to prohibit AI
tools. It is to ensure that a valid submission includes evidence produced by a
real environment.

Prerequisites
- Linux environment (WSL2 Ubuntu or container)
- Basic understanding of IP addresses and routing

Level: Beginner
Estimated time: 30-45 minutes

Pair Programming Notes
- Driver: Execute commands and observe output structure
- Navigator: Predict output format before each command runs
- Swap after: Completing each major section of the report

Usage
    python hw_1_01_network_report.py --output network_report.md
    python hw_1_01_network_report.py --challenge artifacts/anti_ai/challenge_ABC123.yaml
"""

from __future__ import annotations

import argparse
import json
import socket
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml
except ImportError:
    yaml = None

# Ensure repo root is importable when the script is run from subdirectories
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from anti_ai.fingerprint import build_fingerprint


def prompt_prediction() -> None:
    """Ask the student to predict before generating the report."""
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


def run_command(cmd: List[str]) -> str:
    """Execute a shell command and return stdout (or a readable error)."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.stdout if result.returncode == 0 else f"Error: {result.stderr}".strip()
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds"
    except FileNotFoundError:
        return f"Error: Command not found: {cmd[0]}"
    except Exception as exc:
        return f"Error: {exc}"


def get_interfaces() -> str:
    """Get brief network interface information."""
    return run_command(["ip", "-br", "addr", "show"])


def get_detailed_interfaces() -> str:
    """Get detailed interface information."""
    return run_command(["ip", "addr", "show"])


def get_routing_table() -> str:
    """Get the routing table."""
    return run_command(["ip", "route", "show"])


def get_active_connections() -> str:
    """Get active connections and listening sockets."""
    return run_command(["ss", "-tunap"])


def get_dns_config() -> str:
    """Get DNS resolver configuration from /etc/resolv.conf."""
    try:
        return Path("/etc/resolv.conf").read_text(encoding="utf-8")
    except FileNotFoundError:
        return "DNS configuration file not found"
    except PermissionError:
        return "Permission denied reading DNS configuration"


def get_hostname_info() -> Dict[str, str]:
    """Get hostname and attempt to resolve it."""
    hostname = socket.gethostname()
    try:
        ip = socket.gethostbyname(hostname)
    except socket.error:
        ip = "Unable to resolve"

    return {"hostname": hostname, "ip": ip}


def load_challenge(path: Path) -> dict[str, Any]:
    """Load a Week 1 challenge file (YAML or JSON)."""
    if not path.exists():
        raise FileNotFoundError(f"Challenge file not found: {path}")

    if path.suffix.lower() in {".yaml", ".yml"}:
        if yaml is None:
            raise RuntimeError("PyYAML is required for YAML challenge files")
        return yaml.safe_load(path.read_text(encoding="utf-8"))

    if path.suffix.lower() == ".json":
        return json.loads(path.read_text(encoding="utf-8"))

    raise ValueError("Unsupported challenge type. Use .yaml, .yml or .json")


def generate_report(
    *,
    output_path: Path,
    report_token: Optional[str] = None,
    pcap_payload_token: Optional[str] = None,
    fingerprint_hash: Optional[str] = None,
) -> None:
    """Generate a complete network configuration report in Markdown."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hostname_info = get_hostname_info()

    anti_ai_block = ""
    if report_token or pcap_payload_token or fingerprint_hash:
        anti_ai_block = f"""
## Anti-AI Verification (Required)

- Report token: `{report_token or 'N/A'}`
- PCAP payload token: `{pcap_payload_token or 'N/A'}`
- Fingerprint hash: `{fingerprint_hash or 'N/A'}`

> Keep this section unchanged. The validator checks that the tokens match the
> submitted evidence and PCAP artefacts.
"""

    report = f"""# Network Configuration Report

> Generated: {timestamp}
> Hostname: {hostname_info['hostname']}

{anti_ai_block}

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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate network configuration report",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python hw_1_01_network_report.py
  python hw_1_01_network_report.py --output my_report.md
  python hw_1_01_network_report.py --challenge artifacts/anti_ai/challenge_ABC123.yaml
  python hw_1_01_network_report.py --no-predict
""",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("network_report.md"),
        help="Output file path (default: network_report.md)",
    )
    parser.add_argument(
        "--challenge",
        type=Path,
        default=None,
        help="Week 1 challenge file (.yaml/.json) for Anti-AI tokens",
    )
    parser.add_argument(
        "--no-predict",
        action="store_true",
        help="Skip the prediction prompt",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not args.no_predict:
        prompt_prediction()

    report_token: Optional[str] = None
    pcap_payload_token: Optional[str] = None
    fp_hash: Optional[str] = None

    if args.challenge:
        challenge = load_challenge(args.challenge)
        report_token = str(challenge.get("challenges", {}).get("report", {}).get("token") or "")
        pcap_payload_token = str(challenge.get("challenges", {}).get("pcap", {}).get("payload_token") or "")
        fp_hash = str(build_fingerprint(include_features=False)["fingerprint_hash"])

    generate_report(
        output_path=args.output,
        report_token=report_token,
        pcap_payload_token=pcap_payload_token,
        fingerprint_hash=fp_hash,
    )

    print("\n📋 Next steps:")
    print("1. Open the generated report in a text editor")
    print("2. Complete the TODO sections with your analysis")
    print("3. Generate your TCP and UDP PCAPs for Homework 1.02")
    if args.challenge:
        print("4. Collect evidence: python -m anti_ai.evidence_collector --challenge <challenge> --artefact network_report.md --artefact tcp_analysis.pcap --artefact udp_analysis.pcap")
        print("5. Validate locally: python -m anti_ai.submission_validator --challenge <challenge> --evidence evidence.json --base-dir .")
    else:
        print("4. Submit according to homework guidelines")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
