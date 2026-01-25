#!/usr/bin/env python3
"""
Exercise 13.04: IoT Vulnerability Checker
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

LEARNING OBJECTIVES:
- LO5: Identify OWASP IoT vulnerabilities
- LO6: Design defence-in-depth strategies
- LO7: Evaluate security posture

USAGE:
    python ex_13_04_vuln_checker.py --target localhost
    python ex_13_04_vuln_checker.py --target 192.168.1.100 --ports 1883,8883
    python ex_13_04_vuln_checker.py --target localhost --output report.json
"""

from __future__ import annotations

import argparse
import json
import socket
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


# ═══════════════════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Vulnerability:
    """Represents a discovered vulnerability."""
    owasp_id: str
    title: str
    severity: str
    description: str
    remediation: str
    port: Optional[int] = None
    service: Optional[str] = None


@dataclass
class ScanResult:
    """Complete scan result for a target."""
    target: str
    timestamp: str
    duration_seconds: float
    ports_scanned: List[int]
    open_ports: List[int]
    vulnerabilities: List[Vulnerability]
    risk_score: float
    summary: str


# ═══════════════════════════════════════════════════════════════════════════════
# TERMINAL OUTPUT
# ═══════════════════════════════════════════════════════════════════════════════

class Clr:
    """ANSI colour codes for terminal output."""
    G = "\033[92m"   # Green
    R = "\033[91m"   # Red
    Y = "\033[93m"   # Yellow
    B = "\033[94m"   # Blue
    C = "\033[96m"   # Cyan
    BD = "\033[1m"   # Bold
    RS = "\033[0m"   # Reset


if not sys.stdout.isatty():
    Clr.G = Clr.R = Clr.Y = Clr.B = Clr.C = Clr.BD = Clr.RS = ""


# ═══════════════════════════════════════════════════════════════════════════════
# SEVERITY HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def severity_colour(severity: str) -> str:
    """Return ANSI colour code for severity level."""
    mapping = {
        "critical": Clr.R,
        "high": Clr.R,
        "medium": Clr.Y,
        "low": Clr.G,
        "info": Clr.B
    }
    return mapping.get(severity.lower(), Clr.RS)


def severity_score(severity: str) -> float:
    """Return numeric score for severity level."""
    mapping = {
        "critical": 10.0,
        "high": 7.5,
        "medium": 5.0,
        "low": 2.5,
        "info": 0.5
    }
    return mapping.get(severity.lower(), 0.0)


def format_severity(severity: str) -> str:
    """Format severity with colour for display."""
    clr = severity_colour(severity)
    return f"{clr}{severity.upper()}{Clr.RS}"


# ═══════════════════════════════════════════════════════════════════════════════
# PORT SCANNING
# ═══════════════════════════════════════════════════════════════════════════════

def scan_port(host: str, port: int, timeout: float = 1.0) -> bool:
    """Check if a port is open on the target host."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            return result == 0
    except (socket.error, socket.timeout):
        return False


def scan_ports(host: str, ports: List[int]) -> List[int]:
    """Scan multiple ports and return list of open ports."""
    open_ports = []
    for port in ports:
        if scan_port(host, port):
            open_ports.append(port)
    return open_ports


def get_service_name(port: int) -> str:
    """Return service name for common IoT ports."""
    services = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        80: "HTTP",
        443: "HTTPS",
        1883: "MQTT",
        2121: "FTP-alt",
        5683: "CoAP",
        8080: "HTTP-alt",
        8443: "HTTPS-alt",
        8883: "MQTT-TLS",
        9000: "Portainer"
    }
    return services.get(port, "Unknown")


# ═══════════════════════════════════════════════════════════════════════════════
# VULNERABILITY CHECKS
# ═══════════════════════════════════════════════════════════════════════════════

def check_insecure_mqtt(open_ports: List[int]) -> Optional[Vulnerability]:
    """Check for unencrypted MQTT (OWASP I7)."""
    if 1883 in open_ports and 8883 not in open_ports:
        return Vulnerability(
            owasp_id="I7",
            title="Insecure Data Transfer",
            severity="high",
            description="MQTT broker accepts plaintext connections on port 1883 "
                       "without TLS alternative on port 8883.",
            remediation="Enable TLS on port 8883 and disable plaintext port 1883.",
            port=1883,
            service="MQTT"
        )
    return None


def check_telnet_enabled(open_ports: List[int]) -> Optional[Vulnerability]:
    """Check for Telnet service (OWASP I2)."""
    if 23 in open_ports:
        return Vulnerability(
            owasp_id="I2",
            title="Insecure Network Services",
            severity="critical",
            description="Telnet service is running on port 23. Telnet transmits "
                       "credentials in plaintext.",
            remediation="Disable Telnet and use SSH for remote administration.",
            port=23,
            service="Telnet"
        )
    return None


def check_ftp_enabled(open_ports: List[int]) -> Optional[Vulnerability]:
    """Check for FTP service (OWASP I2)."""
    ftp_ports = [p for p in open_ports if p in [21, 2121]]
    if ftp_ports:
        return Vulnerability(
            owasp_id="I2",
            title="Insecure Network Services",
            severity="high",
            description=f"FTP service detected on port {ftp_ports[0]}. FTP transmits "
                       "credentials in plaintext unless FTPS is configured.",
            remediation="Replace FTP with SFTP or configure FTPS with TLS.",
            port=ftp_ports[0],
            service="FTP"
        )
    return None


def check_http_unencrypted(open_ports: List[int]) -> Optional[Vulnerability]:
    """Check for unencrypted HTTP (OWASP I3)."""
    http_ports = [p for p in open_ports if p in [80, 8080]]
    https_ports = [p for p in open_ports if p in [443, 8443]]
    
    if http_ports and not https_ports:
        return Vulnerability(
            owasp_id="I3",
            title="Insecure Ecosystem Interfaces",
            severity="medium",
            description=f"HTTP service on port {http_ports[0]} without HTTPS alternative. "
                       "Web interfaces may transmit sensitive data unencrypted.",
            remediation="Enable HTTPS with valid TLS certificate.",
            port=http_ports[0],
            service="HTTP"
        )
    return None


def check_management_exposed(open_ports: List[int]) -> Optional[Vulnerability]:
    """Check for exposed management interfaces (OWASP I8)."""
    mgmt_ports = [p for p in open_ports if p in [9000]]
    if mgmt_ports:
        return Vulnerability(
            owasp_id="I8",
            title="Lack of Device Management",
            severity="medium",
            description=f"Management interface (Portainer) exposed on port {mgmt_ports[0]}. "
                       "Ensure strong authentication is configured.",
            remediation="Restrict management interface access via firewall rules.",
            port=mgmt_ports[0],
            service="Portainer"
        )
    return None


def run_vulnerability_checks(open_ports: List[int]) -> List[Vulnerability]:
    """Run all vulnerability checks against open ports."""
    checks = [
        check_insecure_mqtt,
        check_telnet_enabled,
        check_ftp_enabled,
        check_http_unencrypted,
        check_management_exposed
    ]
    
    vulnerabilities = []
    for check in checks:
        result = check(open_ports)
        if result:
            vulnerabilities.append(result)
    
    return vulnerabilities


# ═══════════════════════════════════════════════════════════════════════════════
# RISK CALCULATION
# ═══════════════════════════════════════════════════════════════════════════════

def calculate_risk_score(vulnerabilities: List[Vulnerability]) -> float:
    """Calculate overall risk score from vulnerabilities."""
    if not vulnerabilities:
        return 0.0
    
    total = sum(severity_score(v.severity) for v in vulnerabilities)
    normalised = min(10.0, total / len(vulnerabilities) * 1.5)
    return round(normalised, 1)


def risk_rating(score: float) -> str:
    """Return risk rating label for score."""
    if score >= 8.0:
        return "CRITICAL"
    elif score >= 6.0:
        return "HIGH"
    elif score >= 4.0:
        return "MEDIUM"
    elif score >= 2.0:
        return "LOW"
    return "MINIMAL"


# ═══════════════════════════════════════════════════════════════════════════════
# REPORT GENERATION
# ═══════════════════════════════════════════════════════════════════════════════

def print_scan_header(target: str, ports: List[int]) -> None:
    """Print scan header."""
    print(f"\n{Clr.BD}{'═' * 64}{Clr.RS}")
    print(f"{Clr.BD}  🔍 IoT VULNERABILITY SCANNER{Clr.RS}")
    print(f"  Target: {target}")
    print(f"  Ports: {len(ports)} to scan")
    print(f"{Clr.BD}{'═' * 64}{Clr.RS}\n")


def print_port_results(open_ports: List[int]) -> None:
    """Print port scan results."""
    print(f"{Clr.BD}Open Ports:{Clr.RS}")
    if open_ports:
        for port in open_ports:
            service = get_service_name(port)
            print(f"  {Clr.G}●{Clr.RS} {port}/tcp — {service}")
    else:
        print(f"  {Clr.Y}No open ports detected{Clr.RS}")
    print()


def print_vulnerability(vuln: Vulnerability, idx: int) -> None:
    """Print single vulnerability details."""
    sev_fmt = format_severity(vuln.severity)
    print(f"{Clr.BD}[{idx}] {vuln.owasp_id}: {vuln.title}{Clr.RS}")
    print(f"    Severity: {sev_fmt}")
    if vuln.port:
        print(f"    Port: {vuln.port} ({vuln.service})")
    print(f"    {vuln.description}")
    print(f"    {Clr.C}→ {vuln.remediation}{Clr.RS}")
    print()


def print_vulnerabilities(vulnerabilities: List[Vulnerability]) -> None:
    """Print all vulnerabilities."""
    print(f"{Clr.BD}Vulnerabilities Found:{Clr.RS}")
    if vulnerabilities:
        for i, vuln in enumerate(vulnerabilities, 1):
            print_vulnerability(vuln, i)
    else:
        print(f"  {Clr.G}✅ No vulnerabilities detected{Clr.RS}\n")


def print_summary(result: ScanResult) -> None:
    """Print scan summary."""
    rating = risk_rating(result.risk_score)
    clr = severity_colour(rating.lower())
    
    print(f"{Clr.BD}{'─' * 64}{Clr.RS}")
    print(f"{Clr.BD}Summary:{Clr.RS}")
    print(f"  Risk Score: {clr}{result.risk_score}/10.0 ({rating}){Clr.RS}")
    print(f"  Open Ports: {len(result.open_ports)}/{len(result.ports_scanned)}")
    print(f"  Vulnerabilities: {len(result.vulnerabilities)}")
    print(f"  Duration: {result.duration_seconds:.2f}s")
    print(f"{Clr.BD}{'═' * 64}{Clr.RS}\n")


def generate_report(result: ScanResult) -> None:
    """Generate and print complete scan report."""
    print_port_results(result.open_ports)
    print_vulnerabilities(result.vulnerabilities)
    print_summary(result)


# ═══════════════════════════════════════════════════════════════════════════════
# JSON EXPORT
# ═══════════════════════════════════════════════════════════════════════════════

def export_json(result: ScanResult, output_path: Path) -> None:
    """Export scan result to JSON file."""
    data = asdict(result)
    data["vulnerabilities"] = [asdict(v) for v in result.vulnerabilities]
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"{Clr.G}Report exported to: {output_path}{Clr.RS}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN SCANNER
# ═══════════════════════════════════════════════════════════════════════════════

DEFAULT_PORTS = [21, 22, 23, 80, 443, 1883, 2121, 5683, 8080, 8443, 8883, 9000]


def parse_ports(port_str: str) -> List[int]:
    """Parse port specification string."""
    ports = []
    for part in port_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = map(int, part.split("-"))
            ports.extend(range(start, end + 1))
        else:
            ports.append(int(part))
    return sorted(set(ports))


def run_scan(target: str, ports: List[int]) -> ScanResult:
    """Execute vulnerability scan against target."""
    import time
    
    print_scan_header(target, ports)
    
    start_time = time.time()
    print(f"Scanning {len(ports)} ports...")
    
    open_ports = scan_ports(target, ports)
    vulnerabilities = run_vulnerability_checks(open_ports)
    risk_score = calculate_risk_score(vulnerabilities)
    
    duration = time.time() - start_time
    
    return ScanResult(
        target=target,
        timestamp=datetime.now().isoformat(),
        duration_seconds=round(duration, 2),
        ports_scanned=ports,
        open_ports=open_ports,
        vulnerabilities=vulnerabilities,
        risk_score=risk_score,
        summary=f"{len(vulnerabilities)} vulnerabilities, risk score {risk_score}/10"
    )


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="IoT Vulnerability Checker — OWASP IoT Top 10",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --target localhost
  %(prog)s --target 192.168.1.100 --ports 1883,8883,8080
  %(prog)s --target localhost --output report.json
        """
    )
    
    parser.add_argument(
        "--target", "-t",
        required=True,
        help="Target host to scan"
    )
    parser.add_argument(
        "--ports", "-p",
        default=",".join(map(str, DEFAULT_PORTS)),
        help=f"Ports to scan (default: {','.join(map(str, DEFAULT_PORTS))})"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Export report to JSON file"
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=1.0,
        help="Port scan timeout in seconds (default: 1.0)"
    )
    
    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_arguments()
    
    try:
        ports = parse_ports(args.ports)
    except ValueError as e:
        print(f"{Clr.R}ERROR: Invalid port specification: {e}{Clr.RS}")
        return 1
    
    result = run_scan(args.target, ports)
    generate_report(result)
    
    if args.output:
        export_json(result, args.output)
    
    return 0 if result.risk_score < 6.0 else 1


if __name__ == "__main__":
    sys.exit(main())
