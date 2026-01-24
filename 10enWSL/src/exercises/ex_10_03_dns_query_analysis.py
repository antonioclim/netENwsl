#!/usr/bin/env python3
"""
Week 10 - Exercise 3: DNS Query Structure and Analysis
=========================================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

This exercise demonstrates DNS query and response structure using the
dnspython library to build and parse DNS messages.

Objectives:
- Understand DNS message structure (header, question, answer sections)
- Build and send DNS queries programmatically
- Parse and interpret DNS responses
- Compare UDP vs TCP DNS queries

Prerequisites:
- Python 3.11+
- dnspython library (pip install dnspython)

Pair Programming Notes:
- Driver: Execute queries and observe output
- Navigator: Verify response structure against RFC 1035
- Swap after: Completing three different query types
"""

Common Errors
-------------
1. "Connection timed out" → DNS server not running; check docker ps | grep dns
2. "NXDOMAIN" → Domain does not exist; check spelling
3. "dnspython not found" → pip install dnspython --break-system-packages
4. "Truncated response" → Response too large for UDP; use TCP (+tcp flag)
5. "SERVFAIL" → DNS server error; check container logs

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import socket
import sys
from typing import Optional

try:
    import dns.message
    import dns.query
    import dns.rdatatype
    import dns.resolver
except ImportError:
    print("[ERROR] dnspython is required: pip install dnspython")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
DEFAULT_DNS_SERVER = "127.0.0.1"
DEFAULT_DNS_PORT = 5353
DEFAULT_TIMEOUT = 5.0


# ═══════════════════════════════════════════════════════════════════════════════
# DNS_QUERY_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def query_dns_udp(
    domain: str,
    server: str = DEFAULT_DNS_SERVER,
    port: int = DEFAULT_DNS_PORT,
    rdtype: str = "A",
    timeout: float = DEFAULT_TIMEOUT,
) -> Optional[dns.message.Message]:
    """
    Send a DNS query over UDP.
    
    💭 PREDICTION: What happens if the response is larger than 512 bytes?
    
    Args:
        domain: Domain name to query
        server: DNS server IP address
        port: DNS server port
        rdtype: Record type (A, AAAA, MX, NS, TXT, etc.)
        timeout: Query timeout in seconds
    
    Returns:
        DNS response message or None on failure
    """
    try:
        qname = dns.name.from_text(domain)
        request = dns.message.make_query(qname, rdtype)
        
        print(f"[DNS] Querying {domain} ({rdtype}) via UDP to {server}:{port}")
        
        response = dns.query.udp(request, server, port=port, timeout=timeout)
        return response
    except dns.exception.Timeout:
        print(f"[ERROR] DNS query timed out after {timeout}s")
        return None
    except Exception as exc:
        print(f"[ERROR] DNS query failed: {exc}")
        return None


def query_dns_tcp(
    domain: str,
    server: str = DEFAULT_DNS_SERVER,
    port: int = DEFAULT_DNS_PORT,
    rdtype: str = "A",
    timeout: float = DEFAULT_TIMEOUT,
) -> Optional[dns.message.Message]:
    """
    Send a DNS query over TCP.
    
    💭 PREDICTION: When would you prefer TCP over UDP for DNS?
    
    Args:
        domain: Domain name to query
        server: DNS server IP address
        port: DNS server port
        rdtype: Record type
        timeout: Query timeout in seconds
    
    Returns:
        DNS response message or None on failure
    """
    try:
        qname = dns.name.from_text(domain)
        request = dns.message.make_query(qname, rdtype)
        
        print(f"[DNS] Querying {domain} ({rdtype}) via TCP to {server}:{port}")
        
        response = dns.query.tcp(request, server, port=port, timeout=timeout)
        return response
    except dns.exception.Timeout:
        print(f"[ERROR] DNS query timed out after {timeout}s")
        return None
    except Exception as exc:
        print(f"[ERROR] DNS query failed: {exc}")
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# RESPONSE_PARSING
# ═══════════════════════════════════════════════════════════════════════════════
def print_dns_response(response: dns.message.Message, verbose: bool = False) -> None:
    """
    Print a formatted DNS response.
    
    💭 PREDICTION: What sections does a DNS response contain?
    
    Args:
        response: DNS response message
        verbose: If True, print full details
    """
    print("\n" + "=" * 60)
    print("DNS RESPONSE")
    print("=" * 60)
    
    # Header information
    rcode = dns.rcode.to_text(response.rcode())
    print(f"\nStatus: {rcode}")
    print(f"ID: {response.id}")
    print(f"Flags: QR={response.flags & dns.flags.QR != 0}, "
          f"AA={response.flags & dns.flags.AA != 0}, "
          f"TC={response.flags & dns.flags.TC != 0}, "
          f"RD={response.flags & dns.flags.RD != 0}, "
          f"RA={response.flags & dns.flags.RA != 0}")
    
    # Question section
    print(f"\n;; QUESTION SECTION ({len(response.question)} question(s)):")
    for q in response.question:
        print(f"  {q.name} {dns.rdataclass.to_text(q.rdclass)} {dns.rdatatype.to_text(q.rdtype)}")
    
    # Answer section
    print(f"\n;; ANSWER SECTION ({len(response.answer)} answer(s)):")
    for rrset in response.answer:
        for rdata in rrset:
            print(f"  {rrset.name} {rrset.ttl} {dns.rdataclass.to_text(rrset.rdclass)} "
                  f"{dns.rdatatype.to_text(rrset.rdtype)} {rdata}")
    
    # Authority section
    if response.authority:
        print(f"\n;; AUTHORITY SECTION ({len(response.authority)} record(s)):")
        for rrset in response.authority:
            for rdata in rrset:
                print(f"  {rrset.name} {rrset.ttl} {dns.rdataclass.to_text(rrset.rdclass)} "
                      f"{dns.rdatatype.to_text(rrset.rdtype)} {rdata}")
    
    # Additional section
    if response.additional:
        print(f"\n;; ADDITIONAL SECTION ({len(response.additional)} record(s)):")
        for rrset in response.additional:
            for rdata in rrset:
                print(f"  {rrset.name} {rrset.ttl} {dns.rdataclass.to_text(rrset.rdclass)} "
                      f"{dns.rdatatype.to_text(rrset.rdtype)} {rdata}")
    
    print("\n" + "=" * 60)


def extract_answers(response: dns.message.Message) -> list[str]:
    """
    Extract answer data from DNS response.
    
    Args:
        response: DNS response message
    
    Returns:
        List of answer values (IP addresses, hostnames, etc.)
    """
    answers = []
    for rrset in response.answer:
        for rdata in rrset:
            answers.append(str(rdata))
    return answers


# ═══════════════════════════════════════════════════════════════════════════════
# DEMONSTRATION_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def demo_basic_query(server: str, port: int) -> None:
    """
    Demonstrate basic DNS queries.
    
    💭 PREDICTION: What IP addresses will the lab domains resolve to?
    """
    print("\n" + "#" * 60)
    print("# DEMO: Basic DNS Queries")
    print("#" * 60)
    
    domains = [
        ("web.lab.local", "A"),
        ("api.lab.local", "A"),
        ("myservice.lab.local", "A"),
    ]
    
    for domain, rdtype in domains:
        response = query_dns_udp(domain, server, port, rdtype)
        if response:
            answers = extract_answers(response)
            print(f"  {domain} -> {', '.join(answers) if answers else 'NO ANSWER'}")


def demo_compare_transports(server: str, port: int) -> None:
    """
    Compare UDP vs TCP DNS queries.
    
    💭 PREDICTION: Will UDP and TCP give the same results?
    """
    print("\n" + "#" * 60)
    print("# DEMO: UDP vs TCP Transport")
    print("#" * 60)
    
    domain = "web.lab.local"
    
    print("\n[UDP Query]")
    response_udp = query_dns_udp(domain, server, port)
    if response_udp:
        print(f"  Response size: ~{len(response_udp.to_wire())} bytes")
        print(f"  Answers: {extract_answers(response_udp)}")
    
    print("\n[TCP Query]")
    response_tcp = query_dns_tcp(domain, server, port)
    if response_tcp:
        print(f"  Response size: ~{len(response_tcp.to_wire())} bytes")
        print(f"  Answers: {extract_answers(response_tcp)}")


def demo_nonexistent(server: str, port: int) -> None:
    """
    Query a non-existent domain.
    
    💭 PREDICTION: What response code will we get for a non-existent domain?
    """
    print("\n" + "#" * 60)
    print("# DEMO: Non-existent Domain (NXDOMAIN)")
    print("#" * 60)
    
    response = query_dns_udp("nonexistent.lab.local", server, port)
    if response:
        print_dns_response(response)


# ═══════════════════════════════════════════════════════════════════════════════
# INTERACTIVE_QUERY
# ═══════════════════════════════════════════════════════════════════════════════
def interactive_query(server: str, port: int) -> None:
    """Run interactive DNS query session."""
    print("\n" + "#" * 60)
    print("# Interactive DNS Query")
    print(f"# Server: {server}:{port}")
    print("# Type 'quit' to exit")
    print("#" * 60)
    
    while True:
        try:
            line = input("\nEnter domain [type]: ").strip()
            if not line or line.lower() == "quit":
                break
            
            parts = line.split()
            domain = parts[0]
            rdtype = parts[1] if len(parts) > 1 else "A"
            
            response = query_dns_udp(domain, server, port, rdtype)
            if response:
                print_dns_response(response)
        except (EOFError, KeyboardInterrupt):
            break
    
    print("\n[INFO] Goodbye!")


# ═══════════════════════════════════════════════════════════════════════════════
# ARGUMENT_PARSING
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="DNS Query Exercise")
    parser.add_argument("--server", default=DEFAULT_DNS_SERVER, help="DNS server address")
    parser.add_argument("--port", type=int, default=DEFAULT_DNS_PORT, help="DNS server port")
    
    sub = parser.add_subparsers(dest="cmd", required=True)
    
    sub.add_parser("demo", help="Run demonstration queries")
    sub.add_parser("interactive", help="Interactive query mode")
    
    p_query = sub.add_parser("query", help="Query a specific domain")
    p_query.add_argument("domain", help="Domain name to query")
    p_query.add_argument("--type", dest="rdtype", default="A", help="Record type")
    p_query.add_argument("--tcp", action="store_true", help="Use TCP instead of UDP")
    
    return parser.parse_args(argv)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main(argv: list[str]) -> int:
    """Main entry point."""
    args = parse_args(argv)
    
    if args.cmd == "demo":
        demo_basic_query(args.server, args.port)
        demo_compare_transports(args.server, args.port)
        demo_nonexistent(args.server, args.port)
        return 0
    
    if args.cmd == "interactive":
        interactive_query(args.server, args.port)
        return 0
    
    if args.cmd == "query":
        if args.tcp:
            response = query_dns_tcp(args.domain, args.server, args.port, args.rdtype)
        else:
            response = query_dns_udp(args.domain, args.server, args.port, args.rdtype)
        
        if response:
            print_dns_response(response)
            return 0
        return 1
    
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
