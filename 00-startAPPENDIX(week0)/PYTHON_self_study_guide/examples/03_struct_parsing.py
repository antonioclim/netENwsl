#!/usr/bin/env python3
"""
Example 3: Binary parsing with struct
=====================================
Demonstrates data extraction from protocol headers.

Course: Computer Networks - ASE Bucharest, CSIE
Author: ing. dr. Antonio Clim
Version: 2.1 — with subgoal labels and extended comments

💡 ANALOGY: Network Packets as Postal Letters
---------------------------------------------
| Packet Element   | Letter Element                       |
|------------------|--------------------------------------|
| IP Header        | Envelope with addresses (from, to)   |
| TCP Header       | Stamp and regilayerion number        |
| Payload          | Letter contents inside envelope      |
| Checksum         | Wax seal (verifies integrity)        |
| TTL              | "Return after 30 days if..."         |

struct.unpack() = you open the envelope and read addresses in standard format

Learning objectives:
- Understanding binary format of protocol headers
- Bit and byte manipulation in Python
- Interpreting fields of an IP header
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import struct
import socket
import logging
from typing import Optional
from dataclasses import dataclass

__all__ = ['IPHeader', 'TCPHeader', 'parse_ip_header', 'parse_tcp_header']

# ═══════════════════════════════════════════════════════════════════════════════
# LOGGING_CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
# NOTE: Logging is essential for debugging in network applications
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datafmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# DATA_STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class IPHeader:
    """Structured representation of an IPv4 header.
    
    NOTE: Dataclass automatically generates __init__, __repr__, __eq__ etc.
    Much cleaner than a dict or manual class.
    
    Attributes:
        version: IP version (4 for IPv4)
        header_length: Header length in bytes
        tos: Type of Service / DSCP
        total_length: Total packet length
        identification: ID for fragmentation
        flags: Fragmentation flags (DF, MF)
        fragment_offset: Fragment offset
        ttl: Time To Live
        protocol: Encapsulated protocol (6=TCP, 17=UDP, 1=ICMP)
        checksum: Header checksum (hex)
        src_ip: Source IP address
        dst_ip: Destination IP address
    """
    version: int
    header_length: int
    tos: int
    total_length: int
    identification: int
    flags: int
    fragment_offset: int
    ttl: int
    protocol: int
    checksum: str
    src_ip: str
    dst_ip: str


# ═══════════════════════════════════════════════════════════════════════════════
# PROTOCOL_CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

# NOTE: Protocol numbers from IP header (RFC 790)
PROTOCOL_NAMES: dict[int, str] = {
    1: "ICMP",
    6: "TCP",
    17: "UDP",
    47: "GRE",
    50: "ESP",
    51: "AH",
    89: "OSPF",
}

# struct format for IP header
# HACK: !BBHHHBBHII = network byte order, 20 bytes total
# B=1byte, H=2bytes, I=4bytes
IP_HEADER_FORMAT: str = '!BBHHHBBHII'
IP_HEADER_SIZE: int = 20


# ═══════════════════════════════════════════════════════════════════════════════
# PARSING_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def parse_ip_header(data: bytes) -> IPHeader:
    """Parse an IPv4 header from binary data.
    
    Extracts all standard fields from a 20-byte IPv4 header.
    
    Args:
        data: Minimum 20 bytes representing the IP header
        
    Returns:
        IPHeader with all fields populated
        
    Raises:
        TypeError: If data is not of type bytes
        ValueError: If data has less than 20 bytes or invalid format
        
    Example:
        >>> header = parse_ip_header(raw_packet[:20])
        >>> print(header.src_ip)
        '192.168.1.1'
        
    Note:
        struct format: !BBHHHBBHII
        - ! = network byte order (big-endian)
        - B = unsigned char (1 byte)
        - H = unsigned short (2 bytes)
        - I = unsigned int (4 bytes)
    """
    # ─────────────────────────────────────────────────────────────
    # INPUT_VALIDATION
    # ─────────────────────────────────────────────────────────────
    if not isinstance(data, bytes):
        raise TypeError(
            f"Expected bytes, got {type(data).__name__}. "
            f"If you have a string, try data.encode()."
        )
    
    if len(data) < IP_HEADER_SIZE:
        raise ValueError(
            f"Insufficient data: {len(data)} bytes (minimum {IP_HEADER_SIZE} for IP header). "
            f"Verify you have captured the complete header."
        )
    
    # ─────────────────────────────────────────────────────────────
    # PARSING_WITH_STRUCT
    # ─────────────────────────────────────────────────────────────
    try:
        # NOTE: Format = Version+IHL, TOS, TotalLen, ID, Flags+FragOff, TTL, Proto, Checksum, SrcIP, DstIP
        fields = struct.unpack(IP_HEADER_FORMAT, data[:IP_HEADER_SIZE])
        logger.debug(f"Raw fields: {fields}")
        
    except struct.error as e:
        raise ValueError(
            f"Invalid binary format: {e}. "
            f"Bytes do not match IP header format."
        ) from e
    
    # ─────────────────────────────────────────────────────────────
    # EXTRACT_VERSION_IHL
    # ─────────────────────────────────────────────────────────────
    # NOTE: First byte contains 2 fields of 4 bits each
    # HACK: We use bit operations to separate them
    version_ihl: int = fields[0]
    version: int = version_ihl >> 4  # First 4 bits (shift right)
    ihl: int = (version_ihl & 0x0F)  # Last 4 bits (mask)
    header_length: int = ihl * 4     # IHL is in units of 4 bytes
    
    # WARNING: Version check — alert if not IPv4
    if version != 4:
        logger.warning(f"Aexpected IP version: {version} (expected 4)")
    
    # ─────────────────────────────────────────────────────────────
    # EXTRACT_FLAGS_FRAGMENT
    # ─────────────────────────────────────────────────────────────
    # NOTE: Bytes 6-7 contain flags (3 bits) and fragment offset (13 bits)
    flags_frag: int = fields[4]
    flags: int = flags_frag >> 13           # First 3 bits
    fragment_offset: int = flags_frag & 0x1FFF  # Last 13 bits
    
    # ─────────────────────────────────────────────────────────────
    # CONVERT_IP_ADDRESSES
    # ─────────────────────────────────────────────────────────────
    # NOTE: IP addresses are stored as unsigned int (4 bytes)
    # inet_ntoa converts them to string format (dotted decimal)
    try:
        src_ip: str = socket.inet_ntoa(struct.pack('!I', fields[8]))
        dst_ip: str = socket.inet_ntoa(struct.pack('!I', fields[9]))
    except (socket.error, struct.error) as e:
        logger.error(f"Error converting IP addresses: {e}")
        src_ip = f"invalid:{fields[8]:08x}"
        dst_ip = f"invalid:{fields[9]:08x}"
    
    # ─────────────────────────────────────────────────────────────
    # BUILD_RESULT
    # ─────────────────────────────────────────────────────────────
    return IPHeader(
        version=version,
        header_length=header_length,
        tos=fields[1],
        total_length=fields[2],
        identification=fields[3],
        flags=flags,
        fragment_offset=fragment_offset,
        ttl=fields[5],
        protocol=fields[6],
        checksum=f"0x{fields[7]:04x}",
        src_ip=src_ip,
        dst_ip=dst_ip,
    )


def get_protocol_name(protocol_num: int) -> str:
    """Returns the protocol name for a given number.
    
    Args:
        protocol_num: Protocol number from IP header
        
    Returns:
        Protocol name or "Aknown (N)" if not known
        
    Example:
        >>> get_protocol_name(6)
        'TCP'
    """
    return PROTOCOL_NAMES.get(protocol_num, f"Aknown ({protocol_num})")


# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def display_header(header: IPHeader) -> None:
    """Displays an IP header in a readable format.
    
    Args:
        header: IPHeader object to display
        
    Returns:
        None. Prints to console.
    """
    protocol_name: str = get_protocol_name(header.protocol)
    
    # NOTE: Interpret flags — bits have specific meanings
    flags_str: list[str] = []
    if header.flags & 0x4:
        flags_str.append("Reserved")
    if header.flags & 0x2:
        flags_str.append("DF (Don't Fragment)")
    if header.flags & 0x1:
        flags_str.append("MF (More Fragments)")
    flags_display: str = ", ".join(flags_str) if flags_str else "None"
    
    print(f"""
╔═══════════════════════════════════════════════════════════════════════╗
║                         PARSED IPv4 HEADER                            ║
╠═══════════════════════════════════════════════════════════════════════╣
║  Version:          {header.version:<10} (IPv{header.version})                          ║
║  Header Length:    {header.header_length:<10} bytes                                ║
║  Type of Service:  {header.tos:<10} (0x{header.tos:02x})                            ║
║  Total Length:     {header.total_length:<10} bytes                                ║
║  Identification:   {header.identification:<10} (0x{header.identification:04x})                          ║
║  Flags:            {flags_display:<45}║
║  Fragment Offset:  {header.fragment_offset:<10}                                    ║
║  TTL:              {header.ttl:<10} hops                                ║
║  Protocol:         {header.protocol:<10} ({protocol_name})                          ║
║  Header Checksum:  {header.checksum:<10}                                    ║
╠═══════════════════════════════════════════════════════════════════════╣
║  Source IP:        {header.src_ip:<20}                         ║
║  Destination IP:   {header.dst_ip:<20}                         ║
╚═══════════════════════════════════════════════════════════════════════╝
""")


# ═══════════════════════════════════════════════════════════════════════════════
# DEMONSTRATION
# ═══════════════════════════════════════════════════════════════════════════════

def demo() -> None:
    """Complete demonstration of IP header parsing.
    
    Generates a valid IP header, parses it and displays the result.
    Also includes error handling demonstrations.
    
    Returns:
        None. Displays output to console.
    """
    print("=" * 70)
    print("DEMONSTRATION: IP Header Parsing with struct")
    print("=" * 70)
    
    # ─────────────────────────────────────────────────────────────
    # PART_1_GENERATE_HEADER
    # ─────────────────────────────────────────────────────────────
    print("\n📦 PART 1: Generate test IP header")
    print("-" * 50)
    
    # NOTE: We build a valid IP header manually
    # This simulates what you would receive from a packet capture
    header_bytes: bytes = struct.pack(IP_HEADER_FORMAT,
        0x45,           # Version (4) + IHL (5) = 20 bytes header
        0x00,           # TOS (0 = normal)
        40,             # Total length (20 header + 20 TCP)
        0x1234,         # Identification
        0x4000,         # Flags (Don't Fragment) + Frag offset (0)
        64,             # TTL (64 hops - standard Linux)
        6,              # Protocol (6 = TCP)
        0x0000,         # Checksum (0 = not calculated)
        0xC0A80101,     # Source: 192.168.1.1
        0x08080808,     # Dest: 8.8.8.8 (Google DNS)
    )
    
    print(f"Generated header ({len(header_bytes)} bytes):")
    print(f"  Raw bytes: {header_bytes}")
    print(f"  Hex: {header_bytes.hex()}")
    
    # HACK: Formatted hex display (like in Wireshark)
    print(f"  Wireshark view:")
    hex_str: str = header_bytes.hex()
    for i in range(0, len(hex_str), 4):
        chunk: str = hex_str[i:i+4]
        if i > 0 and i % 32 == 0:
            print()
        print(f"  {chunk}", end=" ")
    print()
    
    # ─────────────────────────────────────────────────────────────
    # PART_2_PARSING
    # ─────────────────────────────────────────────────────────────
    print("\n🔍 PART 2: Parse header")
    print("-" * 50)
    
    try:
        header: IPHeader = parse_ip_header(header_bytes)
        display_header(header)
        logger.info(f"Header parsed successfully: {header.src_ip} → {header.dst_ip}")
        
    except (TypeError, ValueError) as e:
        logger.error(f"Parsing error: {e}")
        print(f"❌ Error: {e}")
        return
    
    # ─────────────────────────────────────────────────────────────
    # PART_3_ERROR_HANDLING
    # ─────────────────────────────────────────────────────────────
    print("\n⚠️  PART 3: Error handling")
    print("-" * 50)
    
    # Test 1: Insufficient data
    print("\nTest 1: Insufficient data (10 bytes instead of 20)")
    try:
        parse_ip_header(b'\x45\x00\x00\x28\x12\x34\x40\x00\x40\x06')
    except ValueError as e:
        print(f"  ✅ Expected error: {e}")
    
    # Test 2: Wrong type
    print("\nTest 2: Wrong type (string instead of bytes)")
    try:
        parse_ip_header("not bytes")  # type: ignore
    except TypeError as e:
        print(f"  ✅ Expected error: {e}")
    
    print("\n✅ Demonstration completed!")


# ═══════════════════════════════════════════════════════════════════════════════
# INTERACTIVE_QUIZ
# ═══════════════════════════════════════════════════════════════════════════════

def quiz_struct() -> None:
    """Quiz to verify understanding of struct."""
    print("""
╔═══════════════════════════════════════════════════════════════════════╗
║  🗳️  QUIZ: struct.unpack                                              ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  🔮 PREDICTION: What does this code return?                           ║
║                                                                       ║
║      data = b'\\x00\\x50'  # 2 bytes                                    ║
║      port, = struct.unpack('!H', data)                                ║
║      print(port)                                                      ║
║                                                                       ║
║  Options:                                                             ║
║    A) 80                                                              ║
║    B) 20480                                                           ║
║    C) "\\x00\\x50"                                                      ║
║    D) (80,)                                                           ║
║                                                                       ║
║  Answer: A                                                            ║
║                                                                       ║
║  Explanation:                                                         ║
║  - '!H' = network byte order, unsigned short (2 bytes)                ║
║  - 0x0050 in big-endian = 80 in decimal                               ║
║  - The comma after 'port' extracts the value from the tuple           ║
║  - B would be correct if it was '<H' (little-endian)                  ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
""")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        demo()
        quiz_struct()
        
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
    except Exception as e:
        logger.exception(f"Aexpected error: {e}")
        print(f"\n❌ Aexpected error: {e}")
