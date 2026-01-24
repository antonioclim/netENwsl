#!/usr/bin/env python3
"""
PCAP Demo File Generator
========================
Computer Networks - Week 1 (WSL Environment)
ASE Bucharest | by ing. dr. Antonio Clim

This script generates synthetic PCAP files for educational purposes.
The generated captures demonstrate common network protocols and patterns
that students will encounter during laboratory exercises.

Prerequisites:
    pip install scapy --break-system-packages

Usage:
    python generate_demo_pcaps.py --all           # Generate all demos
    python generate_demo_pcaps.py --icmp          # Generate ICMP only
    python generate_demo_pcaps.py --tcp           # Generate TCP only
    python generate_demo_pcaps.py --dns           # Generate DNS only
    python generate_demo_pcaps.py --http          # Generate HTTP only
    python generate_demo_pcaps.py --list          # List available demos

Output files are created in the current directory (pcap/).

Note: These are SYNTHETIC captures for educational demonstration.
      For real traffic analysis, capture actual network traffic.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Callable

# Scapy imports with graceful fallback
try:
    from scapy.all import (
        DNS,
        DNSQR,
        DNSRR,
        ICMP,
        IP,
        TCP,
        UDP,
        Ether,
        Raw,
        wrpcap,
    )

    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

# Default MAC addresses (synthetic)
SRC_MAC = "02:00:00:00:00:01"
DST_MAC = "02:00:00:00:00:02"

# Default IP addresses (from lab subnet)
CLIENT_IP = "172.20.1.10"
SERVER_IP = "172.20.1.1"
DNS_SERVER = "8.8.8.8"

# Default ports
HTTP_PORT = 80
DNS_PORT = 53
LAB_PORT = 9090


# ═══════════════════════════════════════════════════════════════════════════════
# PCAP GENERATORS
# ═══════════════════════════════════════════════════════════════════════════════


def generate_icmp_ping(output_path: Path, count: int = 4) -> int:
    """
    Generate ICMP echo request/reply pairs.

    Demonstrates:
    - ICMP protocol structure
    - Request/Reply pattern
    - Sequence numbers
    - Round-trip concept

    Args:
        output_path: Where to save the PCAP file
        count: Number of ping pairs to generate

    Returns:
        Number of packets written
    """
    packets = []

    for seq in range(1, count + 1):
        # Echo Request (Type 8, Code 0)
        request = (
            Ether(src=SRC_MAC, dst=DST_MAC)
            / IP(src=CLIENT_IP, dst=SERVER_IP, ttl=64)
            / ICMP(type=8, code=0, id=0x0001, seq=seq)
            / Raw(load=b"PingData" + bytes([seq]) * 48)
        )
        packets.append(request)

        # Echo Reply (Type 0, Code 0)
        reply = (
            Ether(src=DST_MAC, dst=SRC_MAC)
            / IP(src=SERVER_IP, dst=CLIENT_IP, ttl=64)
            / ICMP(type=0, code=0, id=0x0001, seq=seq)
            / Raw(load=b"PingData" + bytes([seq]) * 48)
        )
        packets.append(reply)

    wrpcap(str(output_path), packets)
    return len(packets)


def generate_tcp_handshake(output_path: Path) -> int:
    """
    Generate TCP three-way handshake with data exchange and termination.

    Demonstrates:
    - SYN -> SYN-ACK -> ACK (connection establishment)
    - Data transfer with ACKs
    - FIN -> FIN-ACK -> ACK (connection termination)
    - Sequence and acknowledgment numbers

    Args:
        output_path: Where to save the PCAP file

    Returns:
        Number of packets written
    """
    packets = []

    client_port = 54321
    server_port = LAB_PORT

    # Initial sequence numbers
    client_seq = 1000
    server_seq = 2000

    # === THREE-WAY HANDSHAKE ===

    # 1. SYN (Client -> Server)
    syn = (
        Ether(src=SRC_MAC, dst=DST_MAC)
        / IP(src=CLIENT_IP, dst=SERVER_IP)
        / TCP(
            sport=client_port,
            dport=server_port,
            flags="S",
            seq=client_seq,
            ack=0,
            options=[("MSS", 1460), ("SAckOK", b"")],
        )
    )
    packets.append(syn)

    # 2. SYN-ACK (Server -> Client)
    syn_ack = (
        Ether(src=DST_MAC, dst=SRC_MAC)
        / IP(src=SERVER_IP, dst=CLIENT_IP)
        / TCP(
            sport=server_port,
            dport=client_port,
            flags="SA",
            seq=server_seq,
            ack=client_seq + 1,
            options=[("MSS", 1460), ("SAckOK", b"")],
        )
    )
    packets.append(syn_ack)

    # 3. ACK (Client -> Server)
    ack = (
        Ether(src=SRC_MAC, dst=DST_MAC)
        / IP(src=CLIENT_IP, dst=SERVER_IP)
        / TCP(
            sport=client_port,
            dport=server_port,
            flags="A",
            seq=client_seq + 1,
            ack=server_seq + 1,
        )
    )
    packets.append(ack)

    # === DATA TRANSFER ===

    # Client sends "Hello, Server!\n"
    client_data = b"Hello, Server!\n"
    data_pkt = (
        Ether(src=SRC_MAC, dst=DST_MAC)
        / IP(src=CLIENT_IP, dst=SERVER_IP)
        / TCP(
            sport=client_port,
            dport=server_port,
            flags="PA",
            seq=client_seq + 1,
            ack=server_seq + 1,
        )
        / Raw(load=client_data)
    )
    packets.append(data_pkt)

    # Server ACKs the data
    data_ack = (
        Ether(src=DST_MAC, dst=SRC_MAC)
        / IP(src=SERVER_IP, dst=CLIENT_IP)
        / TCP(
            sport=server_port,
            dport=client_port,
            flags="A",
            seq=server_seq + 1,
            ack=client_seq + 1 + len(client_data),
        )
    )
    packets.append(data_ack)

    # Server responds "ACK:Hello, Server!\n"
    server_data = b"ACK:Hello, Server!\n"
    response_pkt = (
        Ether(src=DST_MAC, dst=SRC_MAC)
        / IP(src=SERVER_IP, dst=CLIENT_IP)
        / TCP(
            sport=server_port,
            dport=client_port,
            flags="PA",
            seq=server_seq + 1,
            ack=client_seq + 1 + len(client_data),
        )
        / Raw(load=server_data)
    )
    packets.append(response_pkt)

    # Client ACKs the response
    response_ack = (
        Ether(src=SRC_MAC, dst=DST_MAC)
        / IP(src=CLIENT_IP, dst=SERVER_IP)
        / TCP(
            sport=client_port,
            dport=server_port,
            flags="A",
            seq=client_seq + 1 + len(client_data),
            ack=server_seq + 1 + len(server_data),
        )
    )
    packets.append(response_ack)

    # === CONNECTION TERMINATION ===

    # Client sends FIN
    fin_client = (
        Ether(src=SRC_MAC, dst=DST_MAC)
        / IP(src=CLIENT_IP, dst=SERVER_IP)
        / TCP(
            sport=client_port,
            dport=server_port,
            flags="FA",
            seq=client_seq + 1 + len(client_data),
            ack=server_seq + 1 + len(server_data),
        )
    )
    packets.append(fin_client)

    # Server ACKs and sends FIN
    fin_server = (
        Ether(src=DST_MAC, dst=SRC_MAC)
        / IP(src=SERVER_IP, dst=CLIENT_IP)
        / TCP(
            sport=server_port,
            dport=client_port,
            flags="FA",
            seq=server_seq + 1 + len(server_data),
            ack=client_seq + 2 + len(client_data),
        )
    )
    packets.append(fin_server)

    # Client final ACK
    final_ack = (
        Ether(src=SRC_MAC, dst=DST_MAC)
        / IP(src=CLIENT_IP, dst=SERVER_IP)
        / TCP(
            sport=client_port,
            dport=server_port,
            flags="A",
            seq=client_seq + 2 + len(client_data),
            ack=server_seq + 2 + len(server_data),
        )
    )
    packets.append(final_ack)

    wrpcap(str(output_path), packets)
    return len(packets)


def generate_dns_query(output_path: Path) -> int:
    """
    Generate DNS query and response for example.com.

    Demonstrates:
    - DNS query structure (QTYPE A)
    - DNS response with answer
    - UDP transport for DNS
    - Transaction ID matching

    Args:
        output_path: Where to save the PCAP file

    Returns:
        Number of packets written
    """
    packets = []

    dns_txid = 0x1234

    # DNS Query (Client -> DNS Server)
    query = (
        Ether(src=SRC_MAC, dst=DST_MAC)
        / IP(src=CLIENT_IP, dst=DNS_SERVER)
        / UDP(sport=53421, dport=DNS_PORT)
        / DNS(id=dns_txid, rd=1, qd=DNSQR(qname="example.com", qtype="A"))
    )
    packets.append(query)

    # DNS Response (DNS Server -> Client)
    response = (
        Ether(src=DST_MAC, dst=SRC_MAC)
        / IP(src=DNS_SERVER, dst=CLIENT_IP)
        / UDP(sport=DNS_PORT, dport=53421)
        / DNS(
            id=dns_txid,
            qr=1,  # Response
            rd=1,  # Recursion desired
            ra=1,  # Recursion available
            qd=DNSQR(qname="example.com", qtype="A"),
            an=DNSRR(rrname="example.com", type="A", ttl=300, rdata="93.184.216.34"),
        )
    )
    packets.append(response)

    wrpcap(str(output_path), packets)
    return len(packets)


def generate_http_get(output_path: Path) -> int:
    """
    Generate HTTP GET request and response.

    Demonstrates:
    - HTTP request structure
    - HTTP headers
    - HTTP response with body
    - Application layer over TCP

    Args:
        output_path: Where to save the PCAP file

    Returns:
        Number of packets written
    """
    packets = []

    client_port = 54322

    client_seq = 3000
    server_seq = 4000

    # HTTP GET Request
    http_request = (
        b"GET / HTTP/1.1\r\n"
        b"Host: example.com\r\n"
        b"User-Agent: NetworkLab/1.0\r\n"
        b"Accept: text/html\r\n"
        b"Connection: close\r\n"
        b"\r\n"
    )

    request_pkt = (
        Ether(src=SRC_MAC, dst=DST_MAC)
        / IP(src=CLIENT_IP, dst=SERVER_IP)
        / TCP(
            sport=client_port,
            dport=HTTP_PORT,
            flags="PA",
            seq=client_seq,
            ack=server_seq,
        )
        / Raw(load=http_request)
    )
    packets.append(request_pkt)

    # Server ACK
    ack_pkt = (
        Ether(src=DST_MAC, dst=SRC_MAC)
        / IP(src=SERVER_IP, dst=CLIENT_IP)
        / TCP(
            sport=HTTP_PORT,
            dport=client_port,
            flags="A",
            seq=server_seq,
            ack=client_seq + len(http_request),
        )
    )
    packets.append(ack_pkt)

    # HTTP Response
    http_response = (
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: text/html; charset=UTF-8\r\n"
        b"Content-Length: 48\r\n"
        b"Connection: close\r\n"
        b"\r\n"
        b"<html><body><h1>Hello, World!</h1></body></html>"
    )

    response_pkt = (
        Ether(src=DST_MAC, dst=SRC_MAC)
        / IP(src=SERVER_IP, dst=CLIENT_IP)
        / TCP(
            sport=HTTP_PORT,
            dport=client_port,
            flags="PA",
            seq=server_seq,
            ack=client_seq + len(http_request),
        )
        / Raw(load=http_response)
    )
    packets.append(response_pkt)

    # Client ACK
    final_ack = (
        Ether(src=SRC_MAC, dst=DST_MAC)
        / IP(src=CLIENT_IP, dst=SERVER_IP)
        / TCP(
            sport=client_port,
            dport=HTTP_PORT,
            flags="A",
            seq=client_seq + len(http_request),
            ack=server_seq + len(http_response),
        )
    )
    packets.append(final_ack)

    wrpcap(str(output_path), packets)
    return len(packets)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ORCHESTRATION
# ═══════════════════════════════════════════════════════════════════════════════

GENERATORS: dict[str, tuple[str, Callable]] = {
    "icmp": ("demo_icmp_ping.pcap", generate_icmp_ping),
    "tcp": ("demo_tcp_handshake.pcap", generate_tcp_handshake),
    "dns": ("demo_dns_query.pcap", generate_dns_query),
    "http": ("demo_http_get.pcap", generate_http_get),
}


def list_demos() -> None:
    """Print available demo generators."""
    print("\nAvailable PCAP demo generators:")
    print("=" * 50)
    for key, (filename, _) in GENERATORS.items():
        print(f"  --{key:8s} -> {filename}")
    print("  --all      -> Generate all of the above")
    print()


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate synthetic PCAP files for educational purposes.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python generate_demo_pcaps.py --all
    python generate_demo_pcaps.py --icmp --tcp
    python generate_demo_pcaps.py --list
        """,
    )

    parser.add_argument("--list", action="store_true", help="List available demos")
    parser.add_argument("--all", action="store_true", help="Generate all demos")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("."),
        help="Output directory (default: current)",
    )

    for key in GENERATORS:
        parser.add_argument(
            f"--{key}", action="store_true", help=f"Generate {key.upper()} demo"
        )

    args = parser.parse_args()

    if args.list:
        list_demos()
        return 0

    if not SCAPY_AVAILABLE:
        print("ERROR: Scapy is not installed.")
        print("Install with: pip install scapy --break-system-packages")
        return 1

    # Determine which demos to generate
    to_generate = []
    if args.all:
        to_generate = list(GENERATORS.keys())
    else:
        for key in GENERATORS:
            if getattr(args, key, False):
                to_generate.append(key)

    if not to_generate:
        print("No demos specified. Use --list to see options or --all to generate all.")
        return 1

    # Generate selected demos
    print(f"\nGenerating PCAP demos in: {args.output_dir.absolute()}")
    print("=" * 50)

    args.output_dir.mkdir(parents=True, exist_ok=True)

    total_packets = 0
    for key in to_generate:
        filename, generator = GENERATORS[key]
        output_path = args.output_dir / filename

        try:
            packet_count = generator(output_path)
            total_packets += packet_count
            print(f"  {filename:30s} ({packet_count} packets)")
        except Exception as e:
            print(f"  {filename:30s} FAILED: {e}")
            return 1

    print("=" * 50)
    print(f"Total: {len(to_generate)} files, {total_packets} packets")
    print(f"\nGenerated: {datetime.now().isoformat()}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
