#!/usr/bin/env python3
"""
Exercise 1: TCP Port Scanner
============================
Week 13 - IoT and Security in Computer Networks
ASE Bucharest, CSIE | by ing. dr. Antonio Clim

LEARNING OBJECTIVES (Anderson-Bloom Taxonomy):
1. UNDERSTAND TCP socket operation and the three-way handshake
2. DIFFERENTIATE between port states: open, closed, filtered
3. APPLY concurrent programming with ThreadPoolExecutor
4. ANALYSE scan results to identify running services
5. CREATE structured JSON reports for security assessment

PAIR PROGRAMMING NOTES:
- Driver: Implement scanning logic, handle socket operations
- Navigator: Verify error handling, research service ports
- Swap after: Completing the single-port scan function

ETHICAL WARNING:
- This tool is intended EXCLUSIVELY for the controlled laboratory
- DO NOT use on systems without explicit authorisation
- Violation of this rule constitutes a criminal offence under the law

USAGE:
    # Basic scan
    python3 ex_13_01_port_scanner.py --target 10.0.13.11 --ports 1-1024
    
    # Specific scan with JSON export
    python3 ex_13_01_port_scanner.py --target 10.0.13.11 --ports 22,80,443,8080 --json-out scan.json
    
    # Host discovery in network
    python3 ex_13_01_port_scanner.py --target 10.0.13.1-15 --mode discovery
    
    # Scan with high parallelism
    python3 ex_13_01_port_scanner.py --target 10.0.13.11 --ports 1-65535 --workers 200 --timeout 0.1
"""

from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORT_DEPENDENCIES
# ═══════════════════════════════════════════════════════════════════════════════
import argparse
import ipaddress
import json
import socket
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional, Tuple


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION_AND_CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

# Known ports and associated services (relevant subset for Week 13)
KNOWN_PORTS = {
    20: "FTP-Data",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    993: "IMAPS",
    995: "POP3S",
    1883: "MQTT",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    6379: "Redis",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
    8883: "MQTT-TLS",
    27017: "MongoDB",
}


class Colors:
    """ANSI colour codes for terminal output."""
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


# Disable colours when output is not a TTY
try:
    if not sys.stdout.isatty():
        Colors.RED = Colours.GREEN = Colours.YELLOW = ""
        Colours.BLUE = Colours.CYAN = Colours.RESET = Colours.BOLD = ""
except Exception:
    pass


# ═══════════════════════════════════════════════════════════════════════════════
# DATA_STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ScanResult:
    """Result of scanning a single port."""
    port: int
    state: str  # "open", "closed", "filtered"
    service: Optional[str] = None
    banner: Optional[str] = None
    response_time_ms: Optional[float] = None


@dataclass
class HostScanResult:
    """Complete scan results for a single host."""
    target: str
    scan_time: str
    total_ports: int
    open_ports: List[ScanResult]
    closed_ports: int
    filtered_ports: int
    duration_seconds: float


# ═══════════════════════════════════════════════════════════════════════════════
# CORE_SCANNING_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════

def tcp_connect_scan(
    host: str,
    port: int,
    timeout: float = 0.5,
    grab_banner: bool = True
) -> ScanResult:
    """
    Perform a TCP connect scan on a single port.
    
    💭 PREDICTION: Before calling this function, predict:
       - What will connect_ex() return for an open port? (Answer: 0)
       - What causes a "filtered" result? (Answer: timeout, firewall DROP)
    
    Technical explanation:
    - Creates a TCP socket and attempts a full three-way handshake
    - Result depends on target response:
        * Successful connection → port OPEN (service listening)
        * Connection refused (RST) → port CLOSED (no service)
        * Timeout (no response) → port FILTERED (firewall DROP)
    
    Args:
        host: IP address or hostname to scan
        port: Port number (1-65535)
        timeout: Connection timeout in seconds
        grab_banner: Whether to attempt reading service banner
    
    Returns:
        ScanResult with port state and optional service information
    """
    start_time = time.perf_counter()
    result = ScanResult(port=port, state="unknown")
    
    # Create TCP socket (SOCK_STREAM = TCP)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    
    try:
        # ─────────────────────────────────────────────────────────────────────
        # TCP CONNECT: Attempt three-way handshake
        # connect_ex() returns 0 for success, error code otherwise
        # ─────────────────────────────────────────────────────────────────────
        error_code = sock.connect_ex((host, port))
        
        if error_code == 0:
            # Connection successful - port is OPEN
            result.state = "open"
            result.service = KNOWN_PORTS.get(port, "unknown")
            
            # Optional: attempt to read service banner
            if grab_banner:
                try:
                    sock.settimeout(0.5)
                    sock.sendall(b"\r\n")
                    banner = sock.recv(1024).decode("utf-8", errors="replace").strip()
                    if banner:
                        result.banner = banner[:100]  # Limit length
                except Exception:
                    pass  # Banner grab failed - not critical
        else:
            # Connection refused - port is CLOSED
            result.state = "closed"
    
    except socket.timeout:
        # No response within timeout - port is FILTERED
        result.state = "filtered"
    
    except ConnectionRefusedError:
        # Explicit refusal - port is CLOSED
        result.state = "closed"
    
    except OSError as e:
        # Other network errors
        result.state = f"error:{e.__class__.__name__}"
    
    finally:
        sock.close()
    
    # Calculate response time
    result.response_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
    
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# INPUT_PARSING
# ═══════════════════════════════════════════════════════════════════════════════

def parse_ports(ports_str: str) -> List[int]:
    """
    Parse port specification into a list of port numbers.
    
    Supports formats:
    - "80" → [80]
    - "80,443,8080" → [80, 443, 8080]
    - "1-1024" → [1, 2, ..., 1024]
    - "22,80,443,1000-2000" → combined list
    
    Args:
        ports_str: Port specification string
    
    Returns:
        List of integer port numbers
    
    Raises:
        SystemExit: If port specification is invalid
    """
    ports: List[int] = []
    
    for part in ports_str.split(","):
        part = part.strip()
        if not part:
            continue
        
        if "-" in part:
            # Port range (e.g., "1-1024")
            try:
                start, end = part.split("-", 1)
                start_port, end_port = int(start), int(end)
                
                if not (1 <= start_port <= 65535 and 1 <= end_port <= 65535):
                    raise ValueError(f"Invalid port in range: {part}")
                if start_port > end_port:
                    raise ValueError(f"Invalid range: {part}")
                
                ports.extend(range(start_port, end_port + 1))
            except ValueError as e:
                print(f"[!] Range parsing error: {e}")
                sys.exit(1)
        else:
            # Single port
            try:
                port = int(part)
                if not (1 <= port <= 65535):
                    raise ValueError(f"Invalid port: {port}")
                ports.append(port)
            except ValueError as e:
                print(f"[!] Port parsing error: {e}")
                sys.exit(1)
    
    return sorted(set(ports))  # Remove duplicates and sort


def parse_targets(target_str: str) -> List[str]:
    """
    Parse target specification into list of IP addresses.
    
    Supports:
    - Single IP: "192.168.1.1"
    - CIDR notation: "192.168.1.0/24"
    - Simple range: "192.168.1.1-10"
    
    Args:
        target_str: Target specification string
    
    Returns:
        List of IP address strings
    """
    targets: List[str] = []
    
    if "/" in target_str:
        # CIDR notation
        try:
            network = ipaddress.ip_network(target_str, strict=False)
            targets = [str(ip) for ip in network.hosts()]
        except ValueError as e:
            print(f"[!] Invalid CIDR: {e}")
            sys.exit(1)
    
    elif "-" in target_str and target_str.count(".") == 3:
        # Simple range (e.g., 192.168.1.1-10)
        try:
            base, range_part = target_str.rsplit(".", 1)
            if "-" in range_part:
                start, end = range_part.split("-")
                for i in range(int(start), int(end) + 1):
                    targets.append(f"{base}.{i}")
            else:
                targets.append(target_str)
        except ValueError:
            targets.append(target_str)
    else:
        targets.append(target_str)
    
    return targets


# ═══════════════════════════════════════════════════════════════════════════════
# CONCURRENT_SCANNING
# ═══════════════════════════════════════════════════════════════════════════════

def scan_host(
    target: str,
    ports: List[int],
    timeout: float = 0.5,
    max_workers: int = 100,
    grab_banner: bool = True,
    verbose: bool = True
) -> HostScanResult:
    """
    Scan all specified ports on a host using concurrent threads.
    
    💭 PREDICTION: If scanning 1000 ports with 100 workers and 0.5s timeout,
       what's the minimum time this will take? (Answer: ~5 seconds)
    
    Uses ThreadPoolExecutor for parallel scanning, significantly reducing
    total scan time compared to sequential scanning.
    
    Args:
        target: Target IP address or hostname
        ports: List of ports to scan
        timeout: Per-port connection timeout
        max_workers: Maximum concurrent scanning threads
        grab_banner: Whether to attempt banner grabbing
        verbose: Whether to print progress
    
    Returns:
        HostScanResult containing all scan findings
    """
    start_time = time.perf_counter()
    scan_timestamp = datetime.now().isoformat()
    
    open_ports: List[ScanResult] = []
    closed_count = 0
    filtered_count = 0
    
    if verbose:
        print(f"\n{Colours.BOLD}[*] Scanning {target} - {len(ports)} ports{Colours.RESET}")
        print(f"    Timeout: {timeout}s | Workers: {max_workers}")
    
    # ─────────────────────────────────────────────────────────────────────────
    # PARALLEL EXECUTION: Submit all scan tasks to thread pool
    # ─────────────────────────────────────────────────────────────────────────
    with ThreadPoolExecutor(max_workers=min(max_workers, len(ports))) as executor:
        futures = {
            executor.submit(tcp_connect_scan, target, port, timeout, grab_banner): port
            for port in ports
        }
        
        for future in as_completed(futures):
            result = future.result()
            
            if result.state == "open":
                open_ports.append(result)
                if verbose:
                    banner_info = f" | {result.banner[:50]}" if result.banner else ""
                    print(f"    {Colours.GREEN}[OPEN]{Colours.RESET} {result.port:5d}/tcp"
                          f"  {result.service or 'unknown':15s}{banner_info}")
            
            elif result.state == "closed":
                closed_count += 1
            
            elif result.state == "filtered":
                filtered_count += 1
    
    duration = time.perf_counter() - start_time
    
    # Sort open ports by port number
    open_ports.sort(key=lambda x: x.port)
    
    if verbose:
        print(f"\n{Colours.BOLD}[+] Results for {target}:{Colours.RESET}")
        print(f"    Open: {Colours.GREEN}{len(open_ports)}{Colours.RESET} | "
              f"Closed: {closed_count} | Filtered: {filtered_count}")
        print(f"    Duration: {duration:.2f}s")
    
    return HostScanResult(
        target=target,
        scan_time=scan_timestamp,
        total_ports=len(ports),
        open_ports=open_ports,
        closed_ports=closed_count,
        filtered_ports=filtered_count,
        duration_seconds=round(duration, 2)
    )


def discover_hosts(
    targets: List[str],
    timeout: float = 0.5,
    max_workers: int = 50
) -> List[str]:
    """
    Discover active hosts by checking common ports.
    
    Args:
        targets: List of IP addresses to check
        timeout: Connection timeout per port
        max_workers: Maximum concurrent threads
    
    Returns:
        List of IP addresses that responded on at least one port
    """
    DISCOVERY_PORTS = [22, 80, 443, 445, 3389, 8080]
    alive_hosts: List[str] = []
    
    print(f"\n{Colours.BOLD}[*] Host discovery in network...{Colours.RESET}")
    print(f"    Targets: {len(targets)} | Test ports: {DISCOVERY_PORTS}")
    
    def check_host(host: str) -> Optional[str]:
        for port in DISCOVERY_PORTS:
            result = tcp_connect_scan(host, port, timeout, grab_banner=False)
            if result.state == "open":
                return host
        return None
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(check_host, host): host for host in targets}
        
        for future in as_completed(futures):
            host = future.result()
            if host:
                alive_hosts.append(host)
                print(f"    {Colours.GREEN}[ALIVE]{Colours.RESET} {host}")
    
    print(f"\n{Colours.BOLD}[+] Active hosts: {len(alive_hosts)}/{len(targets)}{Colours.RESET}")
    return alive_hosts


# ═══════════════════════════════════════════════════════════════════════════════
# OUTPUT_AND_REPORTING
# ═══════════════════════════════════════════════════════════════════════════════

def export_json(results: List[HostScanResult], output_path: str) -> None:
    """
    Export scan results to JSON file.
    
    Args:
        results: List of host scan results
        output_path: Path to output JSON file
    """
    data = {
        "scan_report": {
            "generated_at": datetime.now().isoformat(),
            "tool": "Week 13 Port Scanner",
            "hosts": []
        }
    }
    
    for result in results:
        host_data = {
            "target": result.target,
            "scan_time": result.scan_time,
            "statistics": {
                "total_scanned": result.total_ports,
                "open": len(result.open_ports),
                "closed": result.closed_ports,
                "filtered": result.filtered_ports
            },
            "open_ports": [
                {
                    "port": p.port,
                    "service": p.service,
                    "banner": p.banner,
                    "response_ms": p.response_time_ms
                }
                for p in result.open_ports
            ],
            "duration_seconds": result.duration_seconds
        }
        data["scan_report"]["hosts"].append(host_data)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n{Colours.GREEN}[✓] Results exported: {output_path}{Colours.RESET}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    """Main entry point for the port scanner."""
    parser = argparse.ArgumentParser(
        description="TCP port scanner for Week 13 laboratory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --target 10.0.13.11 --ports 1-1024
  %(prog)s --target 10.0.13.1-15 --mode discovery
  %(prog)s --target 10.0.13.11 --ports 22,80,443 --json-out scan.json
        """
    )
    
    parser.add_argument("--target", required=True,
                        help="Target: IP, range (192.168.1.1-10), or CIDR (/24)")
    parser.add_argument("--ports", default="1-1024",
                        help="Ports: 80, 1-1024, or 22,80,443")
    parser.add_argument("--mode", choices=["scan", "discovery"], default="scan",
                        help="Mode: scan (ports) or discovery (active hosts)")
    parser.add_argument("--timeout", type=float, default=0.5,
                        help="Connection timeout in seconds (default: 0.5)")
    parser.add_argument("--workers", type=int, default=100,
                        help="Number of parallel threads (default: 100)")
    parser.add_argument("--no-banner", action="store_true",
                        help="Do not attempt to read service banner")
    parser.add_argument("--json-out", metavar="FILE",
                        help="Export results to JSON file")
    parser.add_argument("--quiet", action="store_true",
                        help="Minimal output")
    
    args = parser.parse_args()
    
    # Banner
    if not args.quiet:
        print(f"\n{Colours.CYAN}{'='*60}")
        print("  Week 13 - TCP Port Scanner")
        print("  WARNING: For controlled laboratory environment only!")
        print(f"{'='*60}{Colours.RESET}")
    
    # Parse targets
    targets = parse_targets(args.target)
    
    if args.mode == "discovery":
        # Host discovery mode
        alive_hosts = discover_hosts(targets, args.timeout, args.workers)
        
        if args.json_out:
            with open(args.json_out, "w") as f:
                json.dump({"alive_hosts": alive_hosts}, f, indent=2)
    
    else:
        # Port scanning mode
        ports = parse_ports(args.ports)
        results: List[HostScanResult] = []
        
        for target in targets:
            result = scan_host(
                target=target,
                ports=ports,
                timeout=args.timeout,
                max_workers=args.workers,
                grab_banner=not args.no_banner,
                verbose=not args.quiet
            )
            results.append(result)
        
        # JSON export if requested
        if args.json_out:
            export_json(results, args.json_out)
    
    print()


if __name__ == "__main__":
    main()
