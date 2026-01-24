#!/usr/bin/env python3
"""
Homework 13.2: Network Security Audit Script
============================================
Computer Networks - Week 13 (WSL Environment)
ASE Bucharest, CSIE | by ing. dr. Antonio Clim

Objectives:
- Implement basic port scanning with service detection
- Perform banner grabbing to identify services
- Check for common vulnerabilities

Level: Advanced (⭐⭐⭐)
Estimated time: 75-90 minutes

⚠️ ETHICAL NOTE: Only scan systems you own or have permission to test.
"""

from __future__ import annotations
import json
import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Optional

COMMON_PORTS = {
    22: "SSH", 23: "Telnet", 25: "SMTP", 80: "HTTP", 443: "HTTPS",
    445: "SMB", 1883: "MQTT", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 6379: "Redis", 8080: "HTTP-Proxy", 27017: "MongoDB"
}
TIMEOUT = 2

# ═══════════════════════════════════════════════════════════════════════════════
# DATA_STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class PortResult:
    """Result of scanning a single port."""
    port: int
    state: str
    service: str
    banner: str
    vulnerabilities: List[str] = field(default_factory=list)

@dataclass
class HostResult:
    """Complete audit result for a host."""
    host: str
    scan_time: str
    open_ports: List[PortResult] = field(default_factory=list)
    risk_score: int = 0

# ═══════════════════════════════════════════════════════════════════════════════
# SCANNING_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def scan_port(host: str, port: int) -> PortResult:
    """Scan a single port."""
    service = COMMON_PORTS.get(port, "unknown")
    result = PortResult(port=port, state="closed", service=service, banner="")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        if sock.connect_ex((host, port)) == 0:
            result.state = "open"
            result.vulnerabilities = check_vulnerabilities(port)
        sock.close()
    except socket.timeout:
        result.state = "filtered"
    except socket.error:
        pass
    
    return result

def check_vulnerabilities(port: int) -> List[str]:
    """Check for common vulnerabilities based on port."""
    vulns = []
    if port == 23:
        vulns.append("Telnet transmits credentials in plaintext")
    elif port == 445:
        vulns.append("SMB exposure - check for EternalBlue")
    elif port == 1883:
        vulns.append("MQTT without TLS may expose credentials")
    elif port == 6379:
        vulns.append("Redis often runs without authentication")
    elif port == 27017:
        vulns.append("MongoDB may lack authentication")
    return vulns

def scan_host(host: str, ports: List[int] = None) -> HostResult:
    """Perform complete security audit."""
    if ports is None:
        ports = list(COMMON_PORTS.keys())
    
    result = HostResult(host=host, scan_time=datetime.now().isoformat())
    print(f"\n🔍 Scanning {host} ({len(ports)} ports)...")
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(scan_port, host, p): p for p in ports}
        for future in as_completed(futures):
            port_result = future.result()
            if port_result.state == "open":
                result.open_ports.append(port_result)
                print(f"   ✓ Port {port_result.port} ({port_result.service}): OPEN")
    
    result.open_ports.sort(key=lambda x: x.port)
    result.risk_score = sum(10 + len(p.vulnerabilities) * 10 for p in result.open_ports)
    return result

# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def display_results(result: HostResult) -> None:
    """Display audit results."""
    print("\n" + "=" * 70)
    print(f"SECURITY AUDIT: {result.host}")
    print("=" * 70)
    
    risk_icon = "🟢" if result.risk_score < 30 else "🟡" if result.risk_score < 60 else "🔴"
    print(f"\n{risk_icon} RISK SCORE: {result.risk_score}/100")
    
    print(f"\n📡 OPEN PORTS ({len(result.open_ports)}):")
    print("-" * 70)
    for p in result.open_ports:
        vulns = f"{len(p.vulnerabilities)} issue(s)" if p.vulnerabilities else "OK"
        print(f"   {p.port:<8} {p.service:<15} {vulns}")
        for v in p.vulnerabilities:
            print(f"           ⚠️ {v}")

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point."""
    print("=" * 70)
    print("Homework 13.2: Network Security Audit")
    print("Computer Networks - Week 13 | ASE Bucharest, CSIE")
    print("=" * 70)
    print("\n⚠️ Only scan systems you own or have permission to test.")
    
    print("""
Port States:
  OPEN     - Service accepting connections
  CLOSED   - No service listening
  FILTERED - Firewall dropping packets
    """)
    
    demo_ports = [22, 80, 443, 1883, 8080, 9000]
    result = scan_host("localhost", demo_ports)
    display_results(result)
    
    # Export
    with open("security_audit.json", 'w') as f:
        json.dump(asdict(result), f, indent=2)
    print("\n📁 Report saved to: security_audit.json")
    
    print("\n📝 Defence Recommendations:")
    print("   1. Close unnecessary ports")
    print("   2. Use TLS for all services")
    print("   3. Enable authentication everywhere")
    print("   4. Keep software updated")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
