# 📖 Glossary — Week 9: Session and Presentation Layers
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## Session Layer (L5) Terms

| Term | Definition | Example |
|------|------------|---------|
| **Session** | A logical dialogue between two application processes, including authentication state and context that persists across interactions | FTP login session with authenticated user "test" |
| **Session establishment** | The process of initiating a session, typically involving authentication and parameter negotiation | FTP USER/PASS handshake |
| **Session termination** | Graceful closure of a session with state cleanup | FTP QUIT command → 221 response |
| **Dialogue control** | Management of turn-taking in communication (simplex, half-duplex, full-duplex) | FTP control channel: client sends command → server responds |
| **Checkpoint** | A synchronisation point in a data transfer allowing resumption after failure | FTP REST command to resume at byte offset |
| **Synchronisation** | Coordinating state between communicating parties | FTP transfer completion confirmation (226) |
| **Authentication** | Verification of identity before granting access | USER test → 331 → PASS 12345 → 230 |
| **Control channel** | Persistent connection for commands and responses | FTP port 21 connection |
| **Data channel** | Temporary connection for bulk data transfer | FTP port 20 or dynamic passive port |
| **Active mode** | Server initiates data connection to client | PORT command, server connects outbound |
| **Passive mode** | Client initiates data connection to server | PASV command, client connects to server port |

---

## Presentation Layer (L6) Terms

| Term | Definition | Example |
|------|------------|---------|
| **Endianness** | Byte ordering convention for multi-byte data types | Big-endian: 0x1234 stored as [0x12, 0x34] |
| **Big-endian** | Most significant byte stored at lowest memory address (network byte order) | `struct.pack(">I", 0x12345678)` → `\x12\x34\x56\x78` |
| **Little-endian** | Least significant byte stored at lowest memory address (x86 native) | `struct.pack("<I", 0x12345678)` → `\x78\x56\x34\x12` |
| **Network byte order** | Standard byte order for network protocols (big-endian) | `!` or `>` in Python struct format |
| **Serialisation** | Converting data structures to byte sequences for transmission | `struct.pack("!IH", length, flags)` |
| **Deserialisation** | Reconstructing data structures from byte sequences | `struct.unpack("!IH", data)` |
| **Framing** | Delimiting message boundaries in a byte stream | Length-prefixed messages |
| **Magic number** | Fixed byte sequence identifying protocol or file format | `b"PF"` for Pseudo-FTP, `b"\x89PNG"` for PNG |
| **CRC-32** | 32-bit Cyclic Redundancy Check for error detection | `zlib.crc32(data) & 0xFFFFFFFF` |
| **Checksum** | Value computed from data for integrity verification | CRC-32, Adler-32, MD5 |
| **Compression** | Reducing data size for transmission efficiency | gzip, zlib, brotli |
| **Encoding** | Representing data in a specific format | UTF-8, Base64, hexadecimal |

---

## FTP Protocol Terms

| Term | Definition | Example |
|------|------------|---------|
| **FTP** | File Transfer Protocol — dual-channel protocol for file operations | RFC 959 |
| **Control connection** | Persistent TCP connection for FTP commands (default port 21) | `tcp.port == 21` |
| **Data connection** | Temporary TCP connection for file/listing transfer | Port 20 (active) or dynamic (passive) |
| **PASV** | Passive mode command — server provides port for client to connect | `227 Entering Passive Mode (h1,h2,h3,h4,p1,p2)` |
| **PORT** | Active mode command — client provides address for server to connect | `PORT 192,168,1,100,19,136` |
| **RETR** | Retrieve (download) a file from server | `RETR document.pdf` |
| **STOR** | Store (upload) a file to server | `STOR report.txt` |
| **LIST** | List directory contents | `LIST /home/test` |
| **PWD** | Print working directory | `257 "/home/test" is current directory` |
| **CWD** | Change working directory | `CWD documents` → `250 Directory changed` |
| **TYPE** | Set transfer mode (ASCII or Binary) | `TYPE I` for binary, `TYPE A` for ASCII |

---

## Python struct Module

| Format | Meaning | Size | Example |
|--------|---------|------|---------|
| `>` | Big-endian (network) | - | `struct.pack(">I", 1000)` |
| `<` | Little-endian | - | `struct.pack("<I", 1000)` |
| `!` | Network byte order (= big-endian) | - | `struct.pack("!I", 1000)` |
| `=` | Native byte order | - | `struct.pack("=I", 1000)` |
| `B` | Unsigned byte | 1 byte | `struct.pack("B", 255)` |
| `H` | Unsigned short | 2 bytes | `struct.pack(">H", 65535)` |
| `I` | Unsigned int | 4 bytes | `struct.pack(">I", 2**32-1)` |
| `Q` | Unsigned long long | 8 bytes | `struct.pack(">Q", 2**64-1)` |
| `s` | Char array (bytes) | n bytes | `struct.pack("4s", b"TEST")` |
| `f` | Float | 4 bytes | `struct.pack(">f", 3.14)` |
| `d` | Double | 8 bytes | `struct.pack(">d", 3.14159)` |

---

## FTP Response Codes

| Code | Category | Meaning | Example context |
|------|----------|---------|-----------------|
| **1xx** | Positive Preliminary | Action started, expect another reply | `150 Opening data connection` |
| **2xx** | Positive Completion | Action completed successfully | `226 Transfer complete` |
| **3xx** | Positive Intermediate | Need more information | `331 Username OK, need password` |
| **4xx** | Transient Negative | Temporary failure, retry may succeed | `425 Can't open data connection` |
| **5xx** | Permanent Negative | Command failed, don't retry | `530 Not logged in` |

### Common Response Codes

| Code | Meaning |
|------|---------|
| 125 | Data connection already open |
| 150 | Opening data connection |
| 200 | Command OK |
| 220 | Service ready (welcome banner) |
| 221 | Service closing (goodbye) |
| 226 | Transfer complete |
| 227 | Entering Passive Mode |
| 230 | User logged in |
| 250 | File action OK |
| 257 | Pathname created/displayed |
| 331 | Username OK, need password |
| 425 | Can't open data connection |
| 426 | Connection closed, transfer aborted |
| 450 | File unavailable (busy) |
| 500 | Syntax error |
| 530 | Not logged in |
| 550 | File unavailable (not found) |

---

## Binary Protocol Design Terms

| Term | Definition | Example |
|------|------------|---------|
| **Header** | Fixed-size metadata preceding payload | Magic + Length + CRC + Flags |
| **Payload** | Variable-size application data | File contents, message body |
| **Length prefix** | Field indicating payload size | 4-byte unsigned int before data |
| **Magic bytes** | Protocol identifier at message start | `b"S9"`, `b"HTTP"`, `b"\x89PNG"` |
| **Version field** | Protocol version for compatibility | 1-byte version number |
| **Flags field** | Bitfield for optional features | Bit 0: compression, Bit 1: encryption |
| **Wire format** | Exact byte layout for transmission | `">4sIII"` = magic(4) + type(4) + length(4) + crc(4) |

---

## Relationships Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              OSI Model Context                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   L7 Application    │  FTP Client/Server, Commands (USER, RETR, LIST)       │
│   ─────────────────────────────────────────────────────────────────────────  │
│   L6 Presentation   │  Endianness, Encoding, Compression, CRC-32            │
│                     │  struct.pack/unpack, gzip, zlib                       │
│   ─────────────────────────────────────────────────────────────────────────  │
│   L5 Session        │  Authentication, State, Control/Data Channels         │
│                     │  Login session, PASV/PORT mode negotiation            │
│   ─────────────────────────────────────────────────────────────────────────  │
│   L4 Transport      │  TCP connections (reliable byte stream)               │
│                     │  Port 21 (control), Port 20/dynamic (data)            │
│   ─────────────────────────────────────────────────────────────────────────  │
│   L3 Network        │  IP addressing, routing                               │
│                     │  192.168.1.x, NAT traversal                           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           Binary Message Structure                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌─────────┬──────────┬───────┬────────────┬──────────┬────────────────┐   │
│   │ Magic   │ Version  │ Flags │ Length     │ CRC-32   │ Payload        │   │
│   │ 2 bytes │ 1 byte   │ 1 B   │ 4 bytes    │ 4 bytes  │ N bytes        │   │
│   └─────────┴──────────┴───────┴────────────┴──────────┴────────────────┘   │
│   │◄─────────────── HEADER (12 bytes) ──────────────►│◄─── PAYLOAD ───►│   │
│                                                                              │
│   Format string: ">2sBBII" + payload                                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           FTP Dual-Channel Model                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   Client                              Server                                 │
│   ┌──────────┐                       ┌──────────┐                           │
│   │          │═══ Control (21) ═════►│          │                           │
│   │          │    USER, PASS, LIST   │          │                           │
│   │          │◄═══════════════════   │          │                           │
│   │          │    220, 230, 227      │          │                           │
│   │          │                       │          │                           │
│   │          │═══ Data (dynamic) ═══►│          │  (Passive mode)           │
│   │          │    File contents      │          │                           │
│   └──────────┘                       └──────────┘                           │
│                                                                              │
│   Passive: Client → Server (NAT-friendly)                                    │
│   Active:  Server → Client (blocked by NAT)                                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Quick Reference: Python Code Patterns

### Pack/Unpack Network Data

```python
import struct

# Pack header (network byte order)
header = struct.pack("!2sBBII", 
    b"S9",           # Magic (2 bytes)
    1,               # Version (1 byte)
    0x01,            # Flags (1 byte)
    len(payload),    # Length (4 bytes)
    crc32            # CRC-32 (4 bytes)
)

# Unpack header
magic, version, flags, length, crc = struct.unpack("!2sBBII", header)
```

### CRC-32 Calculation

```python
import zlib

data = b"Hello, World!"
crc = zlib.crc32(data) & 0xFFFFFFFF  # Ensure unsigned 32-bit
print(f"CRC-32: 0x{crc:08X}")
```

### FTP Passive Mode Port Parsing

```python
def parse_pasv(response: str) -> tuple[str, int]:
    """Parse '227 Entering Passive Mode (h1,h2,h3,h4,p1,p2)'"""
    parts = response.split("(")[1].split(")")[0].split(",")
    ip = ".".join(parts[:4])
    port = int(parts[4]) * 256 + int(parts[5])
    return ip, port
```

### Receive Exactly N Bytes

```python
def recv_exactly(sock, n: int) -> bytes:
    """Receive exactly n bytes from socket."""
    data = b""
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError("Connection closed")
        data += chunk
    return data
```

---

## See Also

- [RFC 959](https://tools.ietf.org/html/rfc959) — File Transfer Protocol specification
- [Python struct documentation](https://docs.python.org/3/library/struct.html)
- [Python zlib documentation](https://docs.python.org/3/library/zlib.html)
- `docs/theory_summary.md` — Theoretical background
- `docs/misconceptions.md` — Common mistakes to avoid
- `docs/commands_cheatsheet.md` — Quick command reference

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
*Week 9: Session Layer and Presentation Layer*
