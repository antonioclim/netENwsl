#!/usr/bin/env python3
"""
PCAP Sample Generator — Week 7
==============================
NETWORKING class - ASE, Informatics | Computer Networks Laboratory

Generates synthetic PCAP files demonstrating key networking concepts for
packet capture and filtering exercises. These samples serve as reference
materials for students analysing their own captures.

Usage:
    python3 pcap/samples/generate_samples.py
    python3 pcap/samples/generate_samples.py --output-dir ./pcap/samples
    python3 pcap/samples/generate_samples.py --verify

Requirements:
    pip install scapy

Note:
    If scapy is not available, the script creates minimal valid PCAP files
    using raw binary format (libpcap).
"""

from __future__ import annotations

import argparse
import struct
import sys
import time
from pathlib import Path
from typing import Optional

# Try to import scapy for full-featured PCAP generation
try:
    from scapy.all import (
        Ether, IP, TCP, UDP, ICMP, Raw,
        wrpcap, rdpcap, conf
    )
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

# Laboratory network configuration (must match docker-compose.yml)
LAB_CONFIG = {
    "network": "10.0.7.0/24",
    "gateway": "10.0.7.1",
    "tcp_server": "10.0.7.100",
    "tcp_client": "10.0.7.11",
    "udp_receiver": "10.0.7.200",
    "udp_sender": "10.0.7.12",
    "tcp_port": 9090,
    "udp_port": 9091,
}

# Sample files to generate (linked to Learning Objectives)
SAMPLE_DEFINITIONS = [
    {
        "filename": "week07_lo1_tcp_handshake.pcap",
        "lo_ref": "LO1",
        "description": "Complete TCP three-way handshake with data exchange",
        "generator": "generate_tcp_handshake",
    },
    {
        "filename": "week07_lo1_udp_baseline.pcap",
        "lo_ref": "LO1",
        "description": "UDP datagram exchange without connection setup",
        "generator": "generate_udp_baseline",
    },
    {
        "filename": "week07_lo2_tcp_blocked_reject.pcap",
        "lo_ref": "LO2",
        "description": "TCP connection blocked with REJECT (RST response)",
        "generator": "generate_tcp_reject",
    },
    {
        "filename": "week07_lo2_tcp_blocked_drop.pcap",
        "lo_ref": "LO2",
        "description": "TCP connection blocked with DROP (retransmissions only)",
        "generator": "generate_tcp_drop",
    },
    {
        "filename": "week07_lo4_timeout_analysis.pcap",
        "lo_ref": "LO4",
        "description": "Connection timeout scenario for root cause analysis",
        "generator": "generate_timeout_scenario",
    },
    {
        "filename": "week07_lo5_stateful_filter.pcap",
        "lo_ref": "LO5",
        "description": "Stateful filtering with established connection tracking",
        "generator": "generate_stateful_filter",
    },
    {
        "filename": "week07_lo6_drop_vs_reject.pcap",
        "lo_ref": "LO6",
        "description": "Side-by-side comparison of DROP vs REJECT behaviour",
        "generator": "generate_drop_vs_reject",
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# PCAP GENERATION WITH SCAPY
# ═══════════════════════════════════════════════════════════════════════════════

def generate_tcp_handshake(output_path: Path) -> bool:
    """
    Generate PCAP showing complete TCP handshake and data exchange.
    
    Demonstrates:
        - SYN, SYN-ACK, ACK sequence
        - Data transfer with PSH flag
        - Connection teardown with FIN
    
    Args:
        output_path: Path to write the PCAP file
        
    Returns:
        True if generation succeeded
    """
    if not SCAPY_AVAILABLE:
        return generate_minimal_pcap(output_path, "tcp_handshake")
    
    packets = []
    base_time = time.time()
    
    client_ip = LAB_CONFIG["tcp_client"]
    server_ip = LAB_CONFIG["tcp_server"]
    server_port = LAB_CONFIG["tcp_port"]
    client_port = 45678
    
    # Packet 1: SYN (Client → Server)
    syn = (
        IP(src=client_ip, dst=server_ip) /
        TCP(sport=client_port, dport=server_port, flags="S", seq=1000)
    )
    syn.time = base_time
    packets.append(syn)
    
    # Packet 2: SYN-ACK (Server → Client)
    syn_ack = (
        IP(src=server_ip, dst=client_ip) /
        TCP(sport=server_port, dport=client_port, flags="SA", seq=2000, ack=1001)
    )
    syn_ack.time = base_time + 0.001
    packets.append(syn_ack)
    
    # Packet 3: ACK (Client → Server) - Handshake complete
    ack = (
        IP(src=client_ip, dst=server_ip) /
        TCP(sport=client_port, dport=server_port, flags="A", seq=1001, ack=2001)
    )
    ack.time = base_time + 0.002
    packets.append(ack)
    
    # Packet 4: Data (Client → Server) with PSH
    data_out = (
        IP(src=client_ip, dst=server_ip) /
        TCP(sport=client_port, dport=server_port, flags="PA", seq=1001, ack=2001) /
        Raw(load=b"Hello from client")
    )
    data_out.time = base_time + 0.010
    packets.append(data_out)
    
    # Packet 5: ACK for data (Server → Client)
    data_ack = (
        IP(src=server_ip, dst=client_ip) /
        TCP(sport=server_port, dport=client_port, flags="A", seq=2001, ack=1018)
    )
    data_ack.time = base_time + 0.011
    packets.append(data_ack)
    
    # Packet 6: Echo response (Server → Client)
    data_in = (
        IP(src=server_ip, dst=client_ip) /
        TCP(sport=server_port, dport=client_port, flags="PA", seq=2001, ack=1018) /
        Raw(load=b"Hello from client")
    )
    data_in.time = base_time + 0.012
    packets.append(data_in)
    
    # Packet 7: FIN (Client → Server)
    fin = (
        IP(src=client_ip, dst=server_ip) /
        TCP(sport=client_port, dport=server_port, flags="FA", seq=1018, ack=2018)
    )
    fin.time = base_time + 0.100
    packets.append(fin)
    
    # Packet 8: FIN-ACK (Server → Client)
    fin_ack = (
        IP(src=server_ip, dst=client_ip) /
        TCP(sport=server_port, dport=client_port, flags="FA", seq=2018, ack=1019)
    )
    fin_ack.time = base_time + 0.101
    packets.append(fin_ack)
    
    # Packet 9: Final ACK (Client → Server)
    final_ack = (
        IP(src=client_ip, dst=server_ip) /
        TCP(sport=client_port, dport=server_port, flags="A", seq=1019, ack=2019)
    )
    final_ack.time = base_time + 0.102
    packets.append(final_ack)
    
    wrpcap(str(output_path), packets)
    return True


def generate_udp_baseline(output_path: Path) -> bool:
    """
    Generate PCAP showing UDP datagram exchange.
    
    Demonstrates:
        - Connectionless nature of UDP
        - No handshake required
        - Fire-and-forget semantics
    
    Args:
        output_path: Path to write the PCAP file
        
    Returns:
        True if generation succeeded
    """
    if not SCAPY_AVAILABLE:
        return generate_minimal_pcap(output_path, "udp_baseline")
    
    packets = []
    base_time = time.time()
    
    sender_ip = LAB_CONFIG["udp_sender"]
    receiver_ip = LAB_CONFIG["udp_receiver"]
    receiver_port = LAB_CONFIG["udp_port"]
    sender_port = 54321
    
    # Packet 1: UDP datagram (Sender → Receiver)
    udp_out = (
        IP(src=sender_ip, dst=receiver_ip) /
        UDP(sport=sender_port, dport=receiver_port) /
        Raw(load=b"UDP test message")
    )
    udp_out.time = base_time
    packets.append(udp_out)
    
    # Packet 2: UDP response (Receiver → Sender) - echo
    udp_in = (
        IP(src=receiver_ip, dst=sender_ip) /
        UDP(sport=receiver_port, dport=sender_port) /
        Raw(load=b"UDP test message")
    )
    udp_in.time = base_time + 0.005
    packets.append(udp_in)
    
    # Packet 3: Another datagram (no guarantee of delivery)
    udp_out2 = (
        IP(src=sender_ip, dst=receiver_ip) /
        UDP(sport=sender_port, dport=receiver_port) /
        Raw(load=b"Second message")
    )
    udp_out2.time = base_time + 0.100
    packets.append(udp_out2)
    
    wrpcap(str(output_path), packets)
    return True


def generate_tcp_reject(output_path: Path) -> bool:
    """
    Generate PCAP showing TCP blocked with REJECT action.
    
    Demonstrates:
        - Immediate RST response to SYN
        - Fast failure feedback
        - Firewall visibility
    
    Args:
        output_path: Path to write the PCAP file
        
    Returns:
        True if generation succeeded
    """
    if not SCAPY_AVAILABLE:
        return generate_minimal_pcap(output_path, "tcp_reject")
    
    packets = []
    base_time = time.time()
    
    client_ip = LAB_CONFIG["tcp_client"]
    server_ip = LAB_CONFIG["tcp_server"]
    server_port = LAB_CONFIG["tcp_port"]
    client_port = 45680
    
    # Packet 1: SYN attempt (Client → Server)
    syn = (
        IP(src=client_ip, dst=server_ip) /
        TCP(sport=client_port, dport=server_port, flags="S", seq=1000)
    )
    syn.time = base_time
    packets.append(syn)
    
    # Packet 2: RST response (Firewall/Server → Client) - REJECT action
    rst = (
        IP(src=server_ip, dst=client_ip) /
        TCP(sport=server_port, dport=client_port, flags="RA", seq=0, ack=1001)
    )
    rst.time = base_time + 0.001
    packets.append(rst)
    
    wrpcap(str(output_path), packets)
    return True


def generate_tcp_drop(output_path: Path) -> bool:
    """
    Generate PCAP showing TCP blocked with DROP action.
    
    Demonstrates:
        - Multiple SYN retransmissions
        - No response packets
        - Eventual timeout
    
    Args:
        output_path: Path to write the PCAP file
        
    Returns:
        True if generation succeeded
    """
    if not SCAPY_AVAILABLE:
        return generate_minimal_pcap(output_path, "tcp_drop")
    
    packets = []
    base_time = time.time()
    
    client_ip = LAB_CONFIG["tcp_client"]
    server_ip = LAB_CONFIG["tcp_server"]
    server_port = LAB_CONFIG["tcp_port"]
    client_port = 45681
    
    # TCP SYN retransmission pattern: 1s, 2s, 4s, 8s (exponential backoff)
    retransmit_delays = [0, 1.0, 3.0, 7.0, 15.0]
    
    for i, delay in enumerate(retransmit_delays):
        syn = (
            IP(src=client_ip, dst=server_ip, id=1000 + i) /
            TCP(sport=client_port, dport=server_port, flags="S", seq=1000)
        )
        syn.time = base_time + delay
        packets.append(syn)
    
    # No response packets - that's the point of DROP
    
    wrpcap(str(output_path), packets)
    return True


def generate_timeout_scenario(output_path: Path) -> bool:
    """
    Generate PCAP for timeout analysis exercise.
    
    Demonstrates:
        - Partial handshake completion
        - Data sent but no response
        - Retransmission attempts
    
    Args:
        output_path: Path to write the PCAP file
        
    Returns:
        True if generation succeeded
    """
    if not SCAPY_AVAILABLE:
        return generate_minimal_pcap(output_path, "timeout")
    
    packets = []
    base_time = time.time()
    
    client_ip = LAB_CONFIG["tcp_client"]
    server_ip = LAB_CONFIG["tcp_server"]
    server_port = LAB_CONFIG["tcp_port"]
    client_port = 45682
    
    # Successful handshake
    packets.append(IP(src=client_ip, dst=server_ip) /
                   TCP(sport=client_port, dport=server_port, flags="S", seq=1000))
    packets[-1].time = base_time
    
    packets.append(IP(src=server_ip, dst=client_ip) /
                   TCP(sport=server_port, dport=client_port, flags="SA", seq=2000, ack=1001))
    packets[-1].time = base_time + 0.001
    
    packets.append(IP(src=client_ip, dst=server_ip) /
                   TCP(sport=client_port, dport=server_port, flags="A", seq=1001, ack=2001))
    packets[-1].time = base_time + 0.002
    
    # Data sent but server stops responding (simulating crash or DROP rule)
    packets.append(IP(src=client_ip, dst=server_ip) /
                   TCP(sport=client_port, dport=server_port, flags="PA", seq=1001, ack=2001) /
                   Raw(load=b"Request data"))
    packets[-1].time = base_time + 0.010
    
    # Retransmission attempts
    for i, delay in enumerate([0.2, 0.4, 0.8, 1.6]):
        packets.append(IP(src=client_ip, dst=server_ip, id=2000 + i) /
                       TCP(sport=client_port, dport=server_port, flags="PA", seq=1001, ack=2001) /
                       Raw(load=b"Request data"))
        packets[-1].time = base_time + 0.010 + delay
    
    wrpcap(str(output_path), packets)
    return True


def generate_stateful_filter(output_path: Path) -> bool:
    """
    Generate PCAP demonstrating stateful filtering.
    
    Demonstrates:
        - Established connection allowed
        - New connection from same source blocked
        - State tracking importance
    
    Args:
        output_path: Path to write the PCAP file
        
    Returns:
        True if generation succeeded
    """
    if not SCAPY_AVAILABLE:
        return generate_minimal_pcap(output_path, "stateful")
    
    packets = []
    base_time = time.time()
    
    client_ip = LAB_CONFIG["tcp_client"]
    server_ip = LAB_CONFIG["tcp_server"]
    server_port = LAB_CONFIG["tcp_port"]
    
    # Connection 1: Established before filter applied (ALLOWED)
    client_port1 = 45690
    packets.append(IP(src=client_ip, dst=server_ip) /
                   TCP(sport=client_port1, dport=server_port, flags="S", seq=1000))
    packets[-1].time = base_time
    
    packets.append(IP(src=server_ip, dst=client_ip) /
                   TCP(sport=server_port, dport=client_port1, flags="SA", seq=2000, ack=1001))
    packets[-1].time = base_time + 0.001
    
    packets.append(IP(src=client_ip, dst=server_ip) /
                   TCP(sport=client_port1, dport=server_port, flags="A", seq=1001, ack=2001))
    packets[-1].time = base_time + 0.002
    
    # Data exchange on established connection (works)
    packets.append(IP(src=client_ip, dst=server_ip) /
                   TCP(sport=client_port1, dport=server_port, flags="PA", seq=1001, ack=2001) /
                   Raw(load=b"Established conn"))
    packets[-1].time = base_time + 1.0
    
    packets.append(IP(src=server_ip, dst=client_ip) /
                   TCP(sport=server_port, dport=client_port1, flags="PA", seq=2001, ack=1017) /
                   Raw(load=b"Response OK"))
    packets[-1].time = base_time + 1.001
    
    # Connection 2: New connection attempt (BLOCKED by stateful rule)
    client_port2 = 45691
    packets.append(IP(src=client_ip, dst=server_ip) /
                   TCP(sport=client_port2, dport=server_port, flags="S", seq=3000))
    packets[-1].time = base_time + 2.0
    
    # RST from firewall (new connections blocked)
    packets.append(IP(src=server_ip, dst=client_ip) /
                   TCP(sport=server_port, dport=client_port2, flags="RA", seq=0, ack=3001))
    packets[-1].time = base_time + 2.001
    
    wrpcap(str(output_path), packets)
    return True


def generate_drop_vs_reject(output_path: Path) -> bool:
    """
    Generate PCAP comparing DROP and REJECT side by side.
    
    Demonstrates:
        - REJECT: immediate RST
        - DROP: retransmissions then timeout
        - Time difference between behaviours
    
    Args:
        output_path: Path to write the PCAP file
        
    Returns:
        True if generation succeeded
    """
    if not SCAPY_AVAILABLE:
        return generate_minimal_pcap(output_path, "drop_vs_reject")
    
    packets = []
    base_time = time.time()
    
    client_ip = LAB_CONFIG["tcp_client"]
    server_ip = LAB_CONFIG["tcp_server"]
    server_port = LAB_CONFIG["tcp_port"]
    
    # === PART 1: REJECT scenario (port 9090) ===
    client_port1 = 45700
    
    # SYN attempt
    packets.append(IP(src=client_ip, dst=server_ip) /
                   TCP(sport=client_port1, dport=server_port, flags="S", seq=1000))
    packets[-1].time = base_time
    
    # Immediate RST (REJECT)
    packets.append(IP(src=server_ip, dst=client_ip) /
                   TCP(sport=server_port, dport=client_port1, flags="RA", seq=0, ack=1001))
    packets[-1].time = base_time + 0.001
    
    # === PART 2: DROP scenario (port 9090, different client port) ===
    client_port2 = 45701
    drop_start = base_time + 5.0  # 5 seconds later
    
    # Multiple SYN attempts with no response
    retransmit_delays = [0, 1.0, 3.0, 7.0]
    for i, delay in enumerate(retransmit_delays):
        packets.append(IP(src=client_ip, dst=server_ip, id=5000 + i) /
                       TCP(sport=client_port2, dport=server_port, flags="S", seq=2000))
        packets[-1].time = drop_start + delay
    
    # No response packets for DROP
    
    wrpcap(str(output_path), packets)
    return True


# ═══════════════════════════════════════════════════════════════════════════════
# FALLBACK: MINIMAL PCAP WITHOUT SCAPY
# ═══════════════════════════════════════════════════════════════════════════════

def generate_minimal_pcap(output_path: Path, scenario: str) -> bool:
    """
    Generate minimal valid PCAP file without scapy.
    
    Creates a basic PCAP with libpcap format header and placeholder packets.
    This is a fallback when scapy is not installed.
    
    Args:
        output_path: Path to write the PCAP file
        scenario: Scenario name for logging
        
    Returns:
        True if generation succeeded
    """
    # PCAP global header (libpcap format)
    # Magic number, version 2.4, timezone, sigfigs, snaplen, linktype (Ethernet)
    pcap_header = struct.pack(
        "<IHHIIII",
        0xa1b2c3d4,  # Magic number
        2, 4,         # Version 2.4
        0,            # Timezone (GMT)
        0,            # Timestamp accuracy
        65535,        # Snaplen
        1             # Link-layer type (Ethernet)
    )
    
    # Minimal Ethernet + IP + TCP packet (SYN)
    # This is a simplified packet for demonstration
    eth_header = bytes([
        0x00, 0x00, 0x00, 0x00, 0x00, 0x01,  # Dst MAC
        0x00, 0x00, 0x00, 0x00, 0x00, 0x02,  # Src MAC
        0x08, 0x00                            # EtherType: IPv4
    ])
    
    ip_header = bytes([
        0x45, 0x00, 0x00, 0x28,  # Version, IHL, TOS, Total Length
        0x00, 0x01, 0x00, 0x00,  # ID, Flags, Fragment
        0x40, 0x06, 0x00, 0x00,  # TTL, Protocol (TCP), Checksum
        0x0a, 0x00, 0x07, 0x0b,  # Src IP: 10.0.7.11
        0x0a, 0x00, 0x07, 0x64,  # Dst IP: 10.0.7.100
    ])
    
    tcp_header = bytes([
        0xb2, 0x6e, 0x23, 0x82,  # Src Port, Dst Port (45678, 9090)
        0x00, 0x00, 0x03, 0xe8,  # Sequence number
        0x00, 0x00, 0x00, 0x00,  # ACK number
        0x50, 0x02, 0xff, 0xff,  # Data offset, Flags (SYN), Window
        0x00, 0x00, 0x00, 0x00,  # Checksum, Urgent pointer
    ])
    
    packet_data = eth_header + ip_header + tcp_header
    
    # PCAP packet header
    ts_sec = int(time.time())
    ts_usec = 0
    incl_len = len(packet_data)
    orig_len = len(packet_data)
    
    packet_header = struct.pack("<IIII", ts_sec, ts_usec, incl_len, orig_len)
    
    try:
        with open(output_path, "wb") as f:
            f.write(pcap_header)
            f.write(packet_header)
            f.write(packet_data)
        return True
    except IOError as e:
        print(f"Error writing {output_path}: {e}")
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ORCHESTRATION
# ═══════════════════════════════════════════════════════════════════════════════

def generate_all_samples(output_dir: Path, verbose: bool = True) -> dict[str, bool]:
    """
    Generate all PCAP sample files.
    
    Args:
        output_dir: Directory to write PCAP files
        verbose: Print progress messages
        
    Returns:
        Dictionary mapping filename to success status
    """
    results = {}
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if verbose:
        print(f"Generating PCAP samples in {output_dir}")
        print(f"Scapy available: {SCAPY_AVAILABLE}")
        if not SCAPY_AVAILABLE:
            print("Note: Install scapy for full-featured PCAPs: pip install scapy")
        print()
    
    generators = {
        "generate_tcp_handshake": generate_tcp_handshake,
        "generate_udp_baseline": generate_udp_baseline,
        "generate_tcp_reject": generate_tcp_reject,
        "generate_tcp_drop": generate_tcp_drop,
        "generate_timeout_scenario": generate_timeout_scenario,
        "generate_stateful_filter": generate_stateful_filter,
        "generate_drop_vs_reject": generate_drop_vs_reject,
    }
    
    for sample in SAMPLE_DEFINITIONS:
        filename = sample["filename"]
        generator_name = sample["generator"]
        output_path = output_dir / filename
        
        if verbose:
            print(f"  Generating {filename}...", end=" ")
        
        generator_func = generators.get(generator_name)
        if generator_func is None:
            if verbose:
                print(f"SKIP (no generator)")
            results[filename] = False
            continue
        
        try:
            success = generator_func(output_path)
            results[filename] = success
            if verbose:
                status = "OK" if success else "FAIL"
                print(status)
        except Exception as e:
            results[filename] = False
            if verbose:
                print(f"ERROR: {e}")
    
    return results


def verify_samples(sample_dir: Path) -> bool:
    """
    Verify that all expected PCAP samples exist and are valid.
    
    Args:
        sample_dir: Directory containing PCAP files
        
    Returns:
        True if all samples are valid
    """
    all_valid = True
    
    print(f"Verifying PCAP samples in {sample_dir}\n")
    
    for sample in SAMPLE_DEFINITIONS:
        filename = sample["filename"]
        filepath = sample_dir / filename
        
        print(f"  {filename}:", end=" ")
        
        if not filepath.exists():
            print("MISSING")
            all_valid = False
            continue
        
        size = filepath.stat().st_size
        if size < 24:  # Minimum PCAP header size
            print(f"INVALID (too small: {size} bytes)")
            all_valid = False
            continue
        
        # Check magic number
        with open(filepath, "rb") as f:
            magic = f.read(4)
        
        if magic not in (b"\xd4\xc3\xb2\xa1", b"\xa1\xb2\xc3\xd4"):
            print(f"INVALID (bad magic: {magic.hex()})")
            all_valid = False
            continue
        
        print(f"OK ({size} bytes)")
    
    print()
    return all_valid


def build_parser() -> argparse.ArgumentParser:
    """Build command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Generate PCAP sample files for Week 7 laboratory",
        epilog="Run without arguments to generate all samples in ./pcap/samples/"
    )
    
    parser.add_argument(
        "--output-dir", "-o",
        type=Path,
        default=Path(__file__).parent,
        help="Output directory for PCAP files (default: script directory)"
    )
    
    parser.add_argument(
        "--verify", "-v",
        action="store_true",
        help="Verify existing samples instead of generating"
    )
    
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress progress output"
    )
    
    return parser


def main() -> int:
    """
    Main entry point.
    
    Returns:
        Exit code: 0 if successful, 1 if errors occurred
    """
    parser = build_parser()
    args = parser.parse_args()
    
    if args.verify:
        valid = verify_samples(args.output_dir)
        return 0 if valid else 1
    
    results = generate_all_samples(args.output_dir, verbose=not args.quiet)
    
    success_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    
    if not args.quiet:
        print(f"\nGenerated {success_count}/{total_count} samples")
    
    return 0 if success_count == total_count else 1


if __name__ == "__main__":
    sys.exit(main())
