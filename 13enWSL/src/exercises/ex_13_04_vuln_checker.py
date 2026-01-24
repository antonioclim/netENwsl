#!/usr/bin/env python3
"""
Exercise 4: Vulnerability Checker (Defensive and Educational)
=============================================================
Week 13 - IoT and Security in Computer Networks
ASE Bucharest, CSIE | by ing. dr. Antonio Clim

LEARNING OBJECTIVES (Anderson-Bloom Taxonomy):
1. UNDERSTAND defensive security assessment methodology
2. APPLY banner grabbing and service fingerprinting techniques
3. ANALYSE service responses to identify potential vulnerabilities
4. EVALUATE findings based on severity and context
5. CREATE structured security reports in JSON format

PAIR PROGRAMMING NOTES:
- Driver: Implement service probing, parse responses
- Navigator: Research CVEs, verify finding severity classifications
- Swap after: Completing HTTP service checks

ETHICAL NOTICE:
This script performs light-weight, DEFENSIVE checks only:
- Service reachability verification
- Basic fingerprinting (banners and HTTP headers)
- Identification of *intentionally vulnerable* lab services

It does NOT exploit vulnerabilities and does NOT attempt privilege escalation.
Only use against systems you own or have explicit permission to test.

SUPPORTED SERVICES:
- http   - GET /, header inspection, DVWA fingerprint
- ftp    - Banner inspection, vsftpd version check
- mqtt   - Broker reachability via TCP connect

USAGE:
    python3 ex_13_04_vuln_checker.py --target 127.0.0.1 --port 8080 --service http
    python3 ex_13_04_vuln_checker.py --target 127.0.0.1 --port 2121 --service ftp
    python3 ex_13_04_vuln_checker.py --target 127.0.0.1 --port 1883 --service mqtt
    python3 ex_13_04_vuln_checker.py --target 127.0.0.1 --port 8080 --service http --json-out report.json
"""

from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORT_DEPENDENCIES
# ═══════════════════════════════════════════════════════════════════════════════
import argparse
import json
import socket
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional, Tuple


# ═══════════════════════════════════════════════════════════════════════════════
# DATA_STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Finding:
    """A single security finding from the assessment."""
    title: str
    severity: str  # informational, low, medium, high
    evidence: str


@dataclass
class Report:
    """Complete vulnerability assessment report."""
    target: str
    port: int
    service: str
    timestamp_utc: str
    reachable: bool
    banner: Optional[str]
    http_headers: Optional[Dict[str, str]]
    findings: List[Finding]


# ═══════════════════════════════════════════════════════════════════════════════
# SERVICE_PROBING_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def tcp_banner(host: str, port: int, timeout: float = 2.0) -> Optional[str]:
    """
    Attempt to read a service banner via TCP connection.
    
    💭 PREDICTION: What will vsftpd 2.3.4 send as its banner?
       (Answer: "220 (vsFTPd 2.3.4)" or similar version string)
    
    Many services send identification banners upon connection.
    This is useful for fingerprinting but also a security consideration.
    
    Args:
        host: Target hostname or IP
        port: Target port
        timeout: Connection timeout in seconds
    
    Returns:
        Banner string if received, None otherwise
    """
    try:
        with socket.create_connection((host, port), timeout=timeout) as s:
            s.settimeout(timeout)
            # Send stimulus to trigger response from some services
            try:
                s.sendall(b"\r\n")
            except Exception:
                pass
            data = s.recv(1024)
        text = data.decode(errors="replace").strip()
        return text or None
    except Exception:
        return None


def http_probe(
    host: str,
    port: int,
    timeout: float = 3.0
) -> Tuple[bool, Optional[str], Dict[str, str], Optional[str]]:
    """
    Perform HTTP GET request and analyse response.
    
    💭 PREDICTION: What HTTP header reveals the web server software?
       (Answer: "Server" header, e.g., "Server: Apache/2.4.41")
    
    Args:
        host: Target hostname or IP
        port: Target port
        timeout: Request timeout in seconds
    
    Returns:
        Tuple of (reachable, status_line, headers_dict, body_snippet)
    """
    # ─────────────────────────────────────────────────────────────────────────
    # CONSTRUCT_HTTP_REQUEST
    # ─────────────────────────────────────────────────────────────────────────
    req = (
        f"GET / HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"User-Agent: week13-vuln-checker\r\n"
        f"Connection: close\r\n\r\n"
    ).encode()

    # ─────────────────────────────────────────────────────────────────────────
    # SEND_REQUEST_AND_RECEIVE_RESPONSE
    # ─────────────────────────────────────────────────────────────────────────
    try:
        with socket.create_connection((host, port), timeout=timeout) as s:
            s.sendall(req)
            s.settimeout(timeout)
            raw = b""
            while len(raw) < 65536:
                chunk = s.recv(4096)
                if not chunk:
                    break
                raw += chunk
    except Exception:
        return False, None, {}, None

    # ─────────────────────────────────────────────────────────────────────────
    # PARSE_HTTP_RESPONSE
    # ─────────────────────────────────────────────────────────────────────────
    text = raw.decode(errors="replace")
    head, _, body = text.partition("\r\n\r\n")
    lines = head.split("\r\n")
    status_line = lines[0].strip() if lines else None

    headers: Dict[str, str] = {}
    for line in lines[1:]:
        if ":" in line:
            k, v = line.split(":", 1)
            headers[k.strip()] = v.strip()

    snippet = body[:500].strip() or None
    return True, status_line, headers, snippet


def check_mqtt_reachability(host: str, port: int, timeout: float = 2.0) -> bool:
    """
    Check if MQTT broker is reachable via TCP connect.
    
    💭 PREDICTION: Does a successful TCP connection mean the broker
       allows anonymous access? (Answer: No - only means port is open)
    
    Note: This only checks TCP connectivity, not MQTT protocol or auth.
    
    Args:
        host: Target hostname or IP
        port: Target port
        timeout: Connection timeout
    
    Returns:
        True if connection succeeded, False otherwise
    """
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# SERVICE_SPECIFIC_CHECKS
# ═══════════════════════════════════════════════════════════════════════════════

def check_http_service(host: str, port: int) -> Tuple[bool, Optional[str], Optional[Dict[str, str]], List[Finding]]:
    """
    Perform HTTP service assessment.
    
    Args:
        host: Target host
        port: Target port
    
    Returns:
        Tuple of (reachable, banner, headers, findings)
    """
    findings: List[Finding] = []
    
    reachable, status_line, http_headers, body_snippet = http_probe(host, port)
    
    if not reachable:
        findings.append(Finding(
            title="HTTP service not reachable",
            severity="high",
            evidence=f"Could not connect to {host}:{port}",
        ))
        return False, None, None, findings
    
    # ─────────────────────────────────────────────────────────────────────────
    # CHECK_SERVER_HEADER
    # ─────────────────────────────────────────────────────────────────────────
    server = http_headers.get("Server")
    if server:
        findings.append(Finding(
            title="HTTP Server header observed",
            severity="informational",
            evidence=f"Server: {server}",
        ))

    # ─────────────────────────────────────────────────────────────────────────
    # CHECK_FOR_DVWA (intentionally vulnerable application)
    # ─────────────────────────────────────────────────────────────────────────
    if body_snippet:
        if "Damn Vulnerable Web Application" in body_snippet:
            findings.append(Finding(
                title="DVWA detected (intentionally vulnerable lab target)",
                severity="informational",
                evidence="Page contains 'Damn Vulnerable Web Application'",
            ))
        elif "DVWA" in body_snippet:
            findings.append(Finding(
                title="Possible DVWA instance detected (heuristic)",
                severity="low",
                evidence="Body snippet contains 'DVWA'",
            ))
    
    return True, status_line, http_headers, findings


def check_ftp_service(host: str, port: int) -> Tuple[bool, Optional[str], List[Finding]]:
    """
    Perform FTP service assessment.
    
    Args:
        host: Target host
        port: Target port
    
    Returns:
        Tuple of (reachable, banner, findings)
    """
    findings: List[Finding] = []
    
    banner = tcp_banner(host, port)
    reachable = banner is not None
    
    if not reachable:
        findings.append(Finding(
            title="FTP service not reachable or no banner received",
            severity="medium",
            evidence=f"Could not read banner from {host}:{port}",
        ))
        return False, None, findings
    
    # ─────────────────────────────────────────────────────────────────────────
    # ANALYSE_FTP_BANNER
    # ─────────────────────────────────────────────────────────────────────────
    findings.append(Finding(
        title="FTP banner observed",
        severity="informational",
        evidence=banner,
    ))
    
    # Check for known vulnerable version
    if "vsftpd" in banner.lower() and "2.3.4" in banner:
        findings.append(Finding(
            title="vsftpd 2.3.4 detected",
            severity="high",
            evidence="This version is associated with CVE-2011-2523 (backdoor vulnerability).",
        ))
    
    return True, banner, findings


def check_mqtt_service(host: str, port: int) -> Tuple[bool, List[Finding]]:
    """
    Perform MQTT service assessment.
    
    Args:
        host: Target host
        port: Target port
    
    Returns:
        Tuple of (reachable, findings)
    """
    findings: List[Finding] = []
    
    reachable = check_mqtt_reachability(host, port)
    
    if reachable:
        findings.append(Finding(
            title="MQTT broker reachable (TCP connect)",
            severity="informational",
            evidence=f"Connected to {host}:{port}",
        ))
        # Note: We don't test anonymous auth here as that requires MQTT protocol
    else:
        findings.append(Finding(
            title="MQTT broker not reachable",
            severity="high",
            evidence=f"Could not connect to {host}:{port}",
        ))
    
    return reachable, findings


# ═══════════════════════════════════════════════════════════════════════════════
# REPORT_GENERATION
# ═══════════════════════════════════════════════════════════════════════════════

def print_report(report: Report) -> None:
    """Display report in human-readable format."""
    print("=" * 72)
    print("Week 13 - Vulnerability Checker (Defensive)")
    print("=" * 72)
    print(f"Target:    {report.target}")
    print(f"Service:   {report.service}")
    print(f"Port:      {report.port}")
    print(f"Reachable: {report.reachable}")
    print(f"Timestamp: {report.timestamp_utc}")
    
    if report.banner:
        print(f"Banner:    {report.banner}")
    
    if report.http_headers:
        print("\nHTTP Headers:")
        for k, v in report.http_headers.items():
            print(f"  {k}: {v}")
    
    print("\nFindings:")
    if not report.findings:
        print("  (none)")
    else:
        for f in report.findings:
            severity_color = {
                "high": "\033[91m",      # Red
                "medium": "\033[93m",    # Yellow
                "low": "\033[94m",       # Blue
                "informational": "\033[0m"  # Normal
            }.get(f.severity, "\033[0m")
            reset = "\033[0m"
            print(f"  - {severity_color}[{f.severity.upper()}]{reset} {f.title}")
            print(f"    Evidence: {f.evidence}")
    print()


def save_json_report(report: Report, output_path: str) -> None:
    """Save report as JSON file."""
    out = asdict(report)
    out["findings"] = [asdict(x) for x in report.findings]
    
    with open(output_path, "w", encoding="utf-8") as fp:
        json.dump(out, fp, indent=2)
    
    print(f"[+] JSON report written to: {output_path}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Week 13 - Vulnerability checker (defensive)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --target 127.0.0.1 --port 8080 --service http
  %(prog)s --target 127.0.0.1 --port 2121 --service ftp --json-out ftp_report.json
  %(prog)s --target 127.0.0.1 --port 1883 --service mqtt
        """
    )
    parser.add_argument("--target", required=True,
                        help="Target host, e.g., 127.0.0.1")
    parser.add_argument("--port", type=int, required=True,
                        help="Target port")
    parser.add_argument("--service", choices=["http", "ftp", "mqtt"], required=True,
                        help="Service type to check")
    parser.add_argument("--json-out", default=None,
                        help="Optional JSON output path")
    args = parser.parse_args()

    # ─────────────────────────────────────────────────────────────────────────
    # EXECUTE_SERVICE_SPECIFIC_CHECKS
    # ─────────────────────────────────────────────────────────────────────────
    findings: List[Finding] = []
    banner: Optional[str] = None
    headers: Optional[Dict[str, str]] = None
    reachable = False

    if args.service == "http":
        reachable, banner, headers, findings = check_http_service(args.target, args.port)
    
    elif args.service == "ftp":
        reachable, banner, findings = check_ftp_service(args.target, args.port)
    
    elif args.service == "mqtt":
        reachable, findings = check_mqtt_service(args.target, args.port)

    # ─────────────────────────────────────────────────────────────────────────
    # GENERATE_REPORT
    # ─────────────────────────────────────────────────────────────────────────
    report = Report(
        target=args.target,
        port=args.port,
        service=args.service,
        timestamp_utc=datetime.utcnow().isoformat(timespec="seconds") + "Z",
        reachable=reachable,
        banner=banner,
        http_headers=headers,
        findings=findings,
    )

    # ─────────────────────────────────────────────────────────────────────────
    # OUTPUT_RESULTS
    # ─────────────────────────────────────────────────────────────────────────
    print_report(report)
    
    if args.json_out:
        save_json_report(report, args.json_out)

    return 0


if __name__ == "__main__":
    sys.exit(main())
