#!/usr/bin/env python3
"""
Example 3: Binary parsing with struct
Demonstrates extracting data from protocol headers.
"""
import struct
import socket

def parse_ip_header(data: bytes) -> dict:
    """Parse an IP header (first 20 bytes)."""
    if len(data) < 20:
        raise ValueError("Insufficient data for IP header")
    
    # Format: !BBHHHBBHII
    # B = unsigned char (1 byte)
    # H = unsigned short (2 bytes)
    # I = unsigned int (4 bytes)
    fields = struct.unpack('!BBHHHBBHII', data[:20])
    
    version_ihl = fields[0]
    version = version_ihl >> 4
    ihl = (version_ihl & 0x0F) * 4
    
    return {
        'version': version,
        'header_length': ihl,
        'tos': fields[1],
        'total_length': fields[2],
        'identification': fields[3],
        'ttl': fields[5],
        'protocol': fields[6],
        'checksum': hex(fields[7]),
        'src_ip': socket.inet_ntoa(struct.pack('!I', fields[8])),
        'dst_ip': socket.inet_ntoa(struct.pack('!I', fields[9])),
    }

def demo():
    # Simulate an IP header
    header = struct.pack('!BBHHHBBHII',
        0x45,           # Version (4) + IHL (5) = 20 bytes
        0x00,           # TOS
        40,             # Total length
        0x1234,         # Identification
        0x4000,         # Flags + Fragment offset
        64,             # TTL
        6,              # Protocol (TCP)
        0x0000,         # Checksum
        0xC0A80101,     # Source: 192.168.1.1
        0x08080808,     # Dest: 8.8.8.8
    )
    
    print("Generated IP header:")
    print(f"Hex: {header.hex()}")
    print(f"\nParsed:")
    
    result = parse_ip_header(header)
    for key, value in result.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    demo()
