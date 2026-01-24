#!/usr/bin/env python3
"""
PCAP Sample Generator — Week 4
==============================

NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Generates synthetic PCAP sample files for educational purposes.
These files can be opened in Wireshark to demonstrate protocol structures.

Usage:
    python scripts/generate_pcap_samples.py
    python scripts/generate_pcap_samples.py --output pcap/

Generated files:
    - week04_lo3_text_commands.pcap    - TEXT protocol session
    - week04_lo4_binary_header.pcap    - BINARY protocol with CRC
    - week04_lo5_tcp_handshake.pcap    - TCP 3-way handshake
    - week04_lo5_udp_sensor.pcap       - UDP sensor datagrams

Note: These are synthetic captures for educational demonstration.
For real traffic analysis, use scripts/capture_traffic.py with live servers.
"""

import struct
import zlib
import time
import os
from pathlib import Path
from typing import List, Tuple
from datetime import datetime


# ═══════════════════════════════════════════════════════════════════════════════
# PCAP FILE FORMAT CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

# PCAP Global Header (24 bytes)
PCAP_MAGIC = 0xa1b2c3d4  # Microsecond resolution
PCAP_VERSION_MAJOR = 2
PCAP_VERSION_MINOR = 4
PCAP_THISZONE = 0        # GMT
PCAP_SIGFIGS = 0
PCAP_SNAPLEN = 65535
PCAP_LINKTYPE_ETHERNET = 1
PCAP_LINKTYPE_RAW = 101  # Raw IP

# Ethernet constants
ETH_TYPE_IPV4 = 0x0800

# IP constants
IP_PROTO_TCP = 6
IP_PROTO_UDP = 17

# TCP flags
TCP_FIN = 0x01
TCP_SYN = 0x02
TCP_RST = 0x04
TCP_PSH = 0x08
TCP_ACK = 0x10


# ═══════════════════════════════════════════════════════════════════════════════
# PCAP WRITER CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class PCAPWriter:
    """Simple PCAP file writer."""
    
    def __init__(self, filename: str, linktype: int = PCAP_LINKTYPE_ETHERNET):
        """Initialize PCAP writer."""
        self.filename = filename
        self.linktype = linktype
        self.packets: List[Tuple[float, bytes]] = []
    
    def add_packet(self, data: bytes, timestamp: float = None) -> None:
        """Add a packet to the capture."""
        if timestamp is None:
            timestamp = time.time()
        self.packets.append((timestamp, data))
    
    def write(self) -> int:
        """Write PCAP file and return file size."""
        with open(self.filename, 'wb') as f:
            # Global header
            f.write(struct.pack('<I', PCAP_MAGIC))
            f.write(struct.pack('<H', PCAP_VERSION_MAJOR))
            f.write(struct.pack('<H', PCAP_VERSION_MINOR))
            f.write(struct.pack('<i', PCAP_THISZONE))
            f.write(struct.pack('<I', PCAP_SIGFIGS))
            f.write(struct.pack('<I', PCAP_SNAPLEN))
            f.write(struct.pack('<I', self.linktype))
            
            # Packets
            for timestamp, data in self.packets:
                ts_sec = int(timestamp)
                ts_usec = int((timestamp - ts_sec) * 1000000)
                
                # Packet header (16 bytes)
                f.write(struct.pack('<I', ts_sec))
                f.write(struct.pack('<I', ts_usec))
                f.write(struct.pack('<I', len(data)))  # Captured length
                f.write(struct.pack('<I', len(data)))  # Original length
                
                # Packet data
                f.write(data)
        
        return os.path.getsize(self.filename)


# ═══════════════════════════════════════════════════════════════════════════════
# PACKET BUILDERS
# ═══════════════════════════════════════════════════════════════════════════════

def build_ethernet_header(src_mac: bytes, dst_mac: bytes, eth_type: int) -> bytes:
    """Build Ethernet header."""
    return dst_mac + src_mac + struct.pack('>H', eth_type)


def build_ip_header(src_ip: str, dst_ip: str, protocol: int, payload_len: int) -> bytes:
    """Build IPv4 header (20 bytes, no options)."""
    version_ihl = (4 << 4) | 5  # IPv4, 5 words (20 bytes)
    dscp_ecn = 0
    total_length = 20 + payload_len
    identification = 0x1234
    flags_fragment = 0x4000  # Don't fragment
    ttl = 64
    
    # Convert IP addresses
    src_parts = [int(x) for x in src_ip.split('.')]
    dst_parts = [int(x) for x in dst_ip.split('.')]
    
    # Build header without checksum
    header = struct.pack('>BBHHHBBH',
        version_ihl, dscp_ecn, total_length,
        identification, flags_fragment,
        ttl, protocol, 0  # checksum placeholder
    )
    header += bytes(src_parts) + bytes(dst_parts)
    
    # Calculate checksum
    checksum = ip_checksum(header)
    header = header[:10] + struct.pack('>H', checksum) + header[12:]
    
    return header


def ip_checksum(header: bytes) -> int:
    """Calculate IP header checksum."""
    if len(header) % 2:
        header += b'\x00'
    
    total = 0
    for i in range(0, len(header), 2):
        total += (header[i] << 8) + header[i + 1]
    
    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)
    
    return (~total) & 0xFFFF


def build_tcp_header(src_port: int, dst_port: int, seq: int, ack: int, 
                     flags: int, payload: bytes = b'') -> bytes:
    """Build TCP header (20 bytes, no options)."""
    data_offset = 5 << 4  # 5 words (20 bytes)
    window = 65535
    urgent = 0
    
    # Build header without checksum
    header = struct.pack('>HHIIBBHHH',
        src_port, dst_port,
        seq, ack,
        data_offset, flags,
        window, 0, urgent  # checksum placeholder
    )
    
    return header + payload


def build_udp_header(src_port: int, dst_port: int, payload: bytes) -> bytes:
    """Build UDP header (8 bytes)."""
    length = 8 + len(payload)
    return struct.pack('>HHHH', src_port, dst_port, length, 0) + payload


# ═══════════════════════════════════════════════════════════════════════════════
# PCAP GENERATORS
# ═══════════════════════════════════════════════════════════════════════════════

def generate_text_protocol_pcap(output_path: str) -> int:
    """
    Generate TEXT protocol PCAP sample.
    
    Demonstrates:
    - TCP connection establishment
    - Length-prefix framing
    - SET/GET/PING commands
    - Protocol response format
    """
    pcap = PCAPWriter(output_path)
    
    # MAC addresses (fake but valid format)
    client_mac = b'\x00\x11\x22\x33\x44\x55'
    server_mac = b'\x00\xaa\xbb\xcc\xdd\xee'
    
    # IP addresses
    client_ip = '172.28.0.10'
    server_ip = '172.28.0.2'
    
    # Ports
    client_port = 54321
    server_port = 5400
    
    base_time = time.time()
    seq_client = 1000
    seq_server = 2000
    
    def add_tcp_packet(src_mac, dst_mac, src_ip, dst_ip, src_port, dst_port,
                       seq, ack, flags, payload=b'', time_offset=0):
        """Helper to add a TCP packet."""
        tcp = build_tcp_header(src_port, dst_port, seq, ack, flags, payload)
        ip = build_ip_header(src_ip, dst_ip, IP_PROTO_TCP, len(tcp))
        eth = build_ethernet_header(src_mac, dst_mac, ETH_TYPE_IPV4)
        pcap.add_packet(eth + ip + tcp, base_time + time_offset)
    
    # TCP 3-way handshake
    add_tcp_packet(client_mac, server_mac, client_ip, server_ip,
                   client_port, server_port, seq_client, 0, TCP_SYN, time_offset=0.0)
    add_tcp_packet(server_mac, client_mac, server_ip, client_ip,
                   server_port, client_port, seq_server, seq_client + 1, 
                   TCP_SYN | TCP_ACK, time_offset=0.001)
    add_tcp_packet(client_mac, server_mac, client_ip, server_ip,
                   client_port, server_port, seq_client + 1, seq_server + 1, 
                   TCP_ACK, time_offset=0.002)
    
    # TEXT Protocol Commands
    commands = [
        (b"4 PING", b"4 pong"),
        (b"14 SET key1 value1", b"2 OK"),
        (b"8 GET key1", b"6 value1"),
        (b"14 SET key2 hello!", b"2 OK"),
        (b"5 COUNT", b"4 OK 2"),
        (b"8 GET key2", b"6 hello!"),
        (b"4 QUIT", b"3 BYE"),
    ]
    
    time_offset = 0.1
    ack_client = seq_server + 1
    ack_server = seq_client + 1
    
    for cmd, resp in commands:
        # Client sends command
        add_tcp_packet(client_mac, server_mac, client_ip, server_ip,
                       client_port, server_port, ack_server, ack_client,
                       TCP_PSH | TCP_ACK, cmd, time_offset)
        ack_server += len(cmd)
        time_offset += 0.05
        
        # Server acknowledges and responds
        add_tcp_packet(server_mac, client_mac, server_ip, client_ip,
                       server_port, client_port, ack_client, ack_server,
                       TCP_PSH | TCP_ACK, resp, time_offset)
        ack_client += len(resp)
        time_offset += 0.05
    
    # TCP connection close
    add_tcp_packet(client_mac, server_mac, client_ip, server_ip,
                   client_port, server_port, ack_server, ack_client,
                   TCP_FIN | TCP_ACK, time_offset=time_offset)
    add_tcp_packet(server_mac, client_mac, server_ip, client_ip,
                   server_port, client_port, ack_client, ack_server + 1,
                   TCP_FIN | TCP_ACK, time_offset=time_offset + 0.001)
    add_tcp_packet(client_mac, server_mac, client_ip, server_ip,
                   client_port, server_port, ack_server + 1, ack_client + 1,
                   TCP_ACK, time_offset=time_offset + 0.002)
    
    return pcap.write()


def generate_binary_protocol_pcap(output_path: str) -> int:
    """
    Generate BINARY protocol PCAP sample.
    
    Demonstrates:
    - Fixed-size binary header (14 bytes)
    - struct packing with big-endian
    - CRC32 integrity verification
    - Message types (ECHO_REQ, ECHO_RESP, PUT, GET)
    """
    pcap = PCAPWriter(output_path)
    
    client_mac = b'\x00\x11\x22\x33\x44\x55'
    server_mac = b'\x00\xaa\xbb\xcc\xdd\xee'
    client_ip = '172.28.0.10'
    server_ip = '172.28.0.2'
    client_port = 54322
    server_port = 5401
    
    base_time = time.time()
    
    def build_binary_message(msg_type: int, payload: bytes, seq: int) -> bytes:
        """Build binary protocol message with header."""
        magic = b'NP'
        version = 1
        payload_len = len(payload)
        
        # Header without CRC
        header = struct.pack('>2sBBHI', magic, version, msg_type, payload_len, seq)
        
        # Calculate CRC over header + payload
        crc = zlib.crc32(header + payload) & 0xFFFFFFFF
        
        return header + struct.pack('>I', crc) + payload
    
    def add_tcp_packet(src_mac, dst_mac, src_ip, dst_ip, src_port, dst_port,
                       seq, ack, flags, payload=b'', time_offset=0):
        tcp = build_tcp_header(src_port, dst_port, seq, ack, flags, payload)
        ip = build_ip_header(src_ip, dst_ip, IP_PROTO_TCP, len(tcp))
        eth = build_ethernet_header(src_mac, dst_mac, ETH_TYPE_IPV4)
        pcap.add_packet(eth + ip + tcp, base_time + time_offset)
    
    seq_client = 1000
    seq_server = 2000
    
    # TCP handshake
    add_tcp_packet(client_mac, server_mac, client_ip, server_ip,
                   client_port, server_port, seq_client, 0, TCP_SYN, time_offset=0.0)
    add_tcp_packet(server_mac, client_mac, server_ip, client_ip,
                   server_port, client_port, seq_server, seq_client + 1,
                   TCP_SYN | TCP_ACK, time_offset=0.001)
    add_tcp_packet(client_mac, server_mac, client_ip, server_ip,
                   client_port, server_port, seq_client + 1, seq_server + 1,
                   TCP_ACK, time_offset=0.002)
    
    # Binary protocol messages
    # Message types: 1=ECHO_REQ, 2=ECHO_RESP, 3=PUT_REQ, 4=PUT_RESP, 5=GET_REQ, 6=GET_RESP
    messages = [
        (1, b"Hello Binary!", 1),      # ECHO_REQ
        (2, b"Hello Binary!", 1),      # ECHO_RESP
        (3, b"sensor1\x00temp\x00" + struct.pack('>f', 23.5), 2),  # PUT_REQ
        (4, b"OK", 2),                  # PUT_RESP
        (5, b"sensor1\x00temp", 3),     # GET_REQ
        (6, struct.pack('>f', 23.5), 3),  # GET_RESP
    ]
    
    time_offset = 0.1
    ack_client = seq_server + 1
    ack_server = seq_client + 1
    
    for i, (msg_type, payload, seq) in enumerate(messages):
        msg = build_binary_message(msg_type, payload, seq)
        
        if i % 2 == 0:  # Client message
            add_tcp_packet(client_mac, server_mac, client_ip, server_ip,
                           client_port, server_port, ack_server, ack_client,
                           TCP_PSH | TCP_ACK, msg, time_offset)
            ack_server += len(msg)
        else:  # Server message
            add_tcp_packet(server_mac, client_mac, server_ip, client_ip,
                           server_port, client_port, ack_client, ack_server,
                           TCP_PSH | TCP_ACK, msg, time_offset)
            ack_client += len(msg)
        
        time_offset += 0.05
    
    # TCP close
    add_tcp_packet(client_mac, server_mac, client_ip, server_ip,
                   client_port, server_port, ack_server, ack_client,
                   TCP_FIN | TCP_ACK, time_offset=time_offset)
    
    return pcap.write()


def generate_tcp_handshake_pcap(output_path: str) -> int:
    """
    Generate clean TCP 3-way handshake PCAP.
    
    Demonstrates:
    - SYN (seq=1000)
    - SYN-ACK (seq=2000, ack=1001)
    - ACK (seq=1001, ack=2001)
    - Plus some data exchange and graceful close
    """
    pcap = PCAPWriter(output_path)
    
    client_mac = b'\x00\x11\x22\x33\x44\x55'
    server_mac = b'\x00\xaa\xbb\xcc\xdd\xee'
    client_ip = '172.28.0.10'
    server_ip = '172.28.0.2'
    client_port = 54323
    server_port = 80
    
    base_time = time.time()
    
    def add_tcp_packet(src_mac, dst_mac, src_ip, dst_ip, src_port, dst_port,
                       seq, ack, flags, payload=b'', time_offset=0):
        tcp = build_tcp_header(src_port, dst_port, seq, ack, flags, payload)
        ip = build_ip_header(src_ip, dst_ip, IP_PROTO_TCP, len(tcp))
        eth = build_ethernet_header(src_mac, dst_mac, ETH_TYPE_IPV4)
        pcap.add_packet(eth + ip + tcp, base_time + time_offset)
    
    # === TCP 3-WAY HANDSHAKE ===
    # 1. SYN (Client -> Server)
    add_tcp_packet(client_mac, server_mac, client_ip, server_ip,
                   client_port, server_port, 1000, 0, TCP_SYN, time_offset=0.0)
    
    # 2. SYN-ACK (Server -> Client)
    add_tcp_packet(server_mac, client_mac, server_ip, client_ip,
                   server_port, client_port, 2000, 1001, TCP_SYN | TCP_ACK, time_offset=0.010)
    
    # 3. ACK (Client -> Server)
    add_tcp_packet(client_mac, server_mac, client_ip, server_ip,
                   client_port, server_port, 1001, 2001, TCP_ACK, time_offset=0.020)
    
    # === DATA EXCHANGE ===
    # Client sends HTTP-like request
    request = b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n"
    add_tcp_packet(client_mac, server_mac, client_ip, server_ip,
                   client_port, server_port, 1001, 2001, TCP_PSH | TCP_ACK, 
                   request, time_offset=0.100)
    
    # Server ACKs and responds
    response = b"HTTP/1.1 200 OK\r\nContent-Length: 5\r\n\r\nHello"
    add_tcp_packet(server_mac, client_mac, server_ip, client_ip,
                   server_port, client_port, 2001, 1001 + len(request), 
                   TCP_PSH | TCP_ACK, response, time_offset=0.150)
    
    # Client ACKs response
    add_tcp_packet(client_mac, server_mac, client_ip, server_ip,
                   client_port, server_port, 1001 + len(request), 
                   2001 + len(response), TCP_ACK, time_offset=0.160)
    
    # === GRACEFUL CLOSE (4-way) ===
    # Client FIN
    add_tcp_packet(client_mac, server_mac, client_ip, server_ip,
                   client_port, server_port, 1001 + len(request),
                   2001 + len(response), TCP_FIN | TCP_ACK, time_offset=0.200)
    
    # Server FIN-ACK
    add_tcp_packet(server_mac, client_mac, server_ip, client_ip,
                   server_port, client_port, 2001 + len(response),
                   1001 + len(request) + 1, TCP_FIN | TCP_ACK, time_offset=0.210)
    
    # Client final ACK
    add_tcp_packet(client_mac, server_mac, client_ip, server_ip,
                   client_port, server_port, 1001 + len(request) + 1,
                   2001 + len(response) + 1, TCP_ACK, time_offset=0.220)
    
    return pcap.write()


def generate_udp_sensor_pcap(output_path: str) -> int:
    """
    Generate UDP sensor protocol PCAP.
    
    Demonstrates:
    - UDP datagram structure (23 bytes)
    - Binary sensor data format
    - CRC32 integrity field
    - Multiple sensors reporting
    """
    pcap = PCAPWriter(output_path)
    
    server_mac = b'\x00\xaa\xbb\xcc\xdd\xee'
    server_ip = '172.28.0.2'
    server_port = 5402
    
    base_time = time.time()
    
    # Sensor configurations
    sensors = [
        (b'\x00\x11\x22\x33\x44\x01', '172.28.0.11', 1001, "Sala_A1"),
        (b'\x00\x11\x22\x33\x44\x02', '172.28.0.12', 1002, "Sala_B2"),
        (b'\x00\x11\x22\x33\x44\x03', '172.28.0.13', 2001, "Exterior"),
    ]
    
    # Temperature readings (simulated)
    readings = [
        (1001, 22.5, "Sala_A1"),
        (1002, 23.1, "Sala_B2"),
        (2001, 18.7, "Exterior"),
        (1001, 22.7, "Sala_A1"),
        (1002, 23.0, "Sala_B2"),
        (2001, 18.5, "Exterior"),
        (1001, 22.8, "Sala_A1"),
        (1002, 22.9, "Sala_B2"),
        (2001, 18.2, "Exterior"),
        (1001, 22.6, "Sala_A1"),
    ]
    
    def build_sensor_datagram(sensor_id: int, temperature: float, location: str) -> bytes:
        """Build sensor datagram (23 bytes)."""
        version = 1
        location_padded = location[:10].ljust(10).encode('utf-8')
        
        # Payload (19 bytes): version(1) + sensor_id(4) + temp(4) + location(10)
        payload = struct.pack('>BIf10s', version, sensor_id, temperature, location_padded)
        
        # CRC32 (4 bytes)
        crc = zlib.crc32(payload) & 0xFFFFFFFF
        
        return payload + struct.pack('>I', crc)
    
    def add_udp_packet(src_mac, src_ip, src_port, payload, time_offset):
        """Add UDP packet to capture."""
        udp = build_udp_header(src_port, server_port, payload)
        ip = build_ip_header(src_ip, server_ip, IP_PROTO_UDP, len(udp))
        eth = build_ethernet_header(src_mac, server_mac, ETH_TYPE_IPV4)
        pcap.add_packet(eth + ip + udp, base_time + time_offset)
    
    # Generate packets
    for i, (sensor_id, temp, location) in enumerate(readings):
        # Find sensor config
        for mac, ip, sid, _ in sensors:
            if sid == sensor_id:
                sensor_mac = mac
                sensor_ip = ip
                break
        
        datagram = build_sensor_datagram(sensor_id, temp, location)
        add_udp_packet(sensor_mac, sensor_ip, 50000 + sensor_id, datagram, i * 0.5)
    
    # Add one corrupted packet (CRC mismatch) for educational purposes
    bad_datagram = build_sensor_datagram(1001, 99.9, "BadData")
    # Corrupt the CRC
    bad_datagram = bad_datagram[:-4] + b'\xDE\xAD\xBE\xEF'
    add_udp_packet(sensors[0][0], sensors[0][1], 51001, bad_datagram, len(readings) * 0.5)
    
    return pcap.write()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Generate all PCAP sample files."""
    # Determine output directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    output_dir = project_root / 'pcap'
    
    # Ensure output directory exists
    output_dir.mkdir(exist_ok=True)
    
    print()
    print("═" * 60)
    print("  PCAP Sample Generator — Week 4")
    print("  NETWORKING class - ASE, Informatics")
    print("═" * 60)
    print()
    
    generators = [
        ("week04_lo3_text_commands.pcap", generate_text_protocol_pcap,
         "TEXT protocol session with SET/GET/PING commands"),
        ("week04_lo4_binary_header.pcap", generate_binary_protocol_pcap,
         "BINARY protocol with 14-byte header and CRC32"),
        ("week04_lo5_tcp_handshake.pcap", generate_tcp_handshake_pcap,
         "Clean TCP 3-way handshake with data exchange"),
        ("week04_lo5_udp_sensor.pcap", generate_udp_sensor_pcap,
         "UDP sensor datagrams (23 bytes each)"),
    ]
    
    total_size = 0
    
    for filename, generator, description in generators:
        output_path = output_dir / filename
        size = generator(str(output_path))
        total_size += size
        print(f"  ✓ {filename}")
        print(f"    Size: {size} bytes")
        print(f"    Description: {description}")
        print()
    
    print("─" * 60)
    print(f"  Total: {len(generators)} files, {total_size} bytes")
    print()
    print("  Open with Wireshark to inspect packet contents:")
    print(f"    wireshark {output_dir}/week04_lo3_text_commands.pcap")
    print()
    print("═" * 60)


if __name__ == '__main__':
    main()
