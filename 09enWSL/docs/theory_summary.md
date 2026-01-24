# Theoretical Summary: Week 9

> Session Layer (L5) and Presentation Layer (L6)
> NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

## Overview

Week 9 explores the intermediate layers of the OSI model that bridge the reliable
transport layer (L4) with application-specific protocols (L7). These layers handle
**dialogue management** (session) and **data representation** (presentation).

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         OSI Model Context                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   Layer 7: Application    │ HTTP, FTP, SMTP, DNS                           │
│   ─────────────────────────────────────────────────────────────────────────│
│   Layer 6: PRESENTATION   │ Encoding, Serialisation, Encryption ◄── Week 9 │
│   ─────────────────────────────────────────────────────────────────────────│
│   Layer 5: SESSION        │ Authentication, Checkpoints, Dialogue ◄── Week 9│
│   ─────────────────────────────────────────────────────────────────────────│
│   Layer 4: Transport      │ TCP, UDP (reliable delivery)                   │
│   Layer 3: Network        │ IP (routing)                                   │
│   Layer 2: Data Link      │ Ethernet, MAC addresses                        │
│   Layer 1: Physical       │ Cables, signals                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Session Layer (L5)

### Purpose

The session layer manages the **logical dialogue** between applications, providing:

- **Session establishment**: Initiating communication with authentication
- **Synchronisation**: Checkpoints for resumption after failures
- **Dialogue control**: Managing turn-taking in half-duplex communication
- **Termination**: Graceful closure with state preservation

### Key Distinction: Connection vs Session

| Aspect           | TCP Connection (L4)      | Session (L5)              |
|------------------|--------------------------|---------------------------|
| Endpoints        | IP:port ↔ IP:port        | User ↔ Service            |
| State            | Sequence numbers         | Authentication, context   |
| Persistence      | Single socket lifetime   | May span reconnections    |
| Failure handling | Retransmission           | Checkpoint/resume         |
| Identity         | Anonymous                | Authenticated user        |

### Session Layer in Practice

In modern networking, the session layer is often implemented within applications rather than as a distinct protocol. Key patterns include:

**State Management:**
- Cookies and tokens maintain identity across requests
- Session IDs link multiple operations to a single user context
- Keepalive mechanisms prevent premature session termination

**Checkpoint and Recovery:**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Session Checkpoint Example                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   Large File Transfer (100 MB):                                             │
│                                                                             │
│   [████████████████░░░░░░░░░░░░░░░░] 35% complete                          │
│                    ↑                                                        │
│                Checkpoint saved at 35 MB                                    │
│                                                                             │
│   Network drops → TCP reconnects → Session resumes at 35 MB                │
│   (Without session layer, would restart from 0%)                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Real-World Examples

- **HTTP Sessions**: Cookies maintain user state across multiple TCP connections
- **FTP Sessions**: Authentication persists while data connections open/close
- **Database Connections**: Transaction state maintained across queries
- **SSH Sessions**: Terminal state, environment variables, working directory preserved

---

## Presentation Layer (L6)

### Purpose

The presentation layer handles **data syntax** transformations:

- **Serialisation**: Converting data structures to byte streams
- **Encoding**: Character set conversions (ASCII, UTF-8, etc.)
- **Compression**: Reducing data size for transmission
- **Encryption**: Protecting data confidentiality (though often at L4 with TLS)

### Endianness (Byte Order)

Multi-byte numbers can be stored in two ways:

```
Value: 0x12345678 (305,419,896 in decimal)

Big-Endian (Network Order):
┌────┬────┬────┬────┐
│ 12 │ 34 │ 56 │ 78 │  ← Most significant byte first
└────┴────┴────┴────┘
  addr 0   1   2   3

Little-Endian (Intel/AMD x86):
┌────┬────┬────┬────┐
│ 78 │ 56 │ 34 │ 12 │  ← Least significant byte first
└────┴────┴────┴────┘
  addr 0   1   2   3
```

**Golden Rule**: Network protocols use **big-endian** (network byte order).

### Presentation Layer Data Formats

The presentation layer defines how complex data types are represented in bytes:

**Primitive Types:**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Type           │ Size    │ Range                    │ struct code         │
├─────────────────────────────────────────────────────────────────────────────┤
│  uint8          │ 1 byte  │ 0 to 255                │ B                   │
│  int8           │ 1 byte  │ -128 to 127             │ b                   │
│  uint16         │ 2 bytes │ 0 to 65,535             │ H                   │
│  int16          │ 2 bytes │ -32,768 to 32,767       │ h                   │
│  uint32         │ 4 bytes │ 0 to 4,294,967,295      │ I                   │
│  int32          │ 4 bytes │ -2^31 to 2^31-1         │ i                   │
│  float32        │ 4 bytes │ IEEE 754 single         │ f                   │
│  float64        │ 8 bytes │ IEEE 754 double         │ d                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Variable-Length Data:**
- Length-prefixed strings: `[4-byte length][UTF-8 bytes]`
- Null-terminated strings: `[bytes]\x00`
- TLV (Type-Length-Value) encoding for flexible structures

### Python `struct` Format Characters

| Character | Meaning                    | Size    |
|-----------|----------------------------|---------|
| `>`       | Big-endian (network)       | -       |
| `<`       | Little-endian              | -       |
| `!`       | Network byte order (= `>`) | -       |
| `B`       | Unsigned byte              | 1 byte  |
| `H`       | Unsigned short             | 2 bytes |
| `I`       | Unsigned int               | 4 bytes |
| `Q`       | Unsigned long long         | 8 bytes |
| `s`       | String (bytes)             | n bytes |

### Example: Protocol Header

```python
import struct
import zlib

# Define header format: magic(4), length(4), crc(4), flags(4)
HEADER_FORMAT = ">4sIII"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)  # 16 bytes

def pack_message(payload: bytes, flags: int = 0) -> bytes:
    """Pack a message with header for transmission."""
    magic = b"FTPC"
    length = len(payload)
    crc = zlib.crc32(payload) & 0xFFFFFFFF
    
    header = struct.pack(HEADER_FORMAT, magic, length, crc, flags)
    return header + payload

def unpack_message(data: bytes) -> tuple:
    """Unpack a message and verify integrity."""
    magic, length, crc, flags = struct.unpack(HEADER_FORMAT, data[:HEADER_SIZE])
    payload = data[HEADER_SIZE:HEADER_SIZE + length]
    
    # Verify CRC
    actual_crc = zlib.crc32(payload) & 0xFFFFFFFF
    if actual_crc != crc:
        raise ValueError("CRC mismatch - data corrupted")
    
    return payload, flags
```

---

## FTP Protocol Analysis

### Architecture

FTP uses **two separate connections**:

1. **Control Connection** (port 21): Text commands, session management
2. **Data Connection** (port 20 or dynamic): File transfers

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        FTP Dual-Channel Architecture                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   Client                                                  Server            │
│   ┌────────────┐                                        ┌────────────┐     │
│   │            │ ══════ Control (port 21) ════════════► │            │     │
│   │            │         USER, PASS, LIST, RETR         │            │     │
│   │            │ ◄══════════════════════════════════════ │            │     │
│   │            │         220, 230, 150, 226             │            │     │
│   │            │                                        │            │     │
│   │            │ ═══════ Data (dynamic) ═══════════════►│            │     │
│   │            │         File bytes                     │            │     │
│   └────────────┘                                        └────────────┘     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Session Lifecycle

```
1. TCP Connect (SYN/SYN-ACK/ACK)
2. Server: "220 Welcome to FTP server"
3. Client: "USER alice"
4. Server: "331 Password required for alice"
5. Client: "PASS secret"
6. Server: "230 User alice logged in"      ← Session established
7. Client: "PWD" / "LIST" / "RETR" / etc.  ← Session operations
8. Client: "QUIT"
9. Server: "221 Goodbye"                   ← Session closed
```

### Transfer Modes

| Mode   | Command   | Usage                              |
|--------|-----------|------------------------------------| 
| ASCII  | `TYPE A`  | Text files (line ending conversion)|
| Binary | `TYPE I`  | Executables, images, archives      |

### Active vs Passive Mode

| Mode    | Command | Data Connection Initiator | NAT-friendly |
|---------|---------|---------------------------|--------------|
| Active  | PORT    | Server → Client:20        | ✗ No         |
| Passive | PASV    | Client → Server:dynamic   | ✓ Yes        |

**PASV Response Decoding:**
```
227 Entering Passive Mode (192,168,1,5,234,100)
                          └─────────┘ └──┬──┘
                          IP address   Port = 234×256 + 100 = 60004
```

---

## Practical Applications

### Binary Protocol Design Checklist

1. **Magic bytes**: Identify protocol, aid resynchronisation
2. **Version field**: Allow protocol evolution
3. **Length field**: Enable message framing (TCP has no boundaries!)
4. **Checksum**: Verify integrity (CRC-32, MD5, SHA-256)
5. **Flags**: Optional features (compression, encryption)
6. **Reserved fields**: Space for future extensions

### Common Serialisation Formats

| Format           | Type   | Use Case                    |
|------------------|--------|-----------------------------|
| JSON             | Text   | Web APIs, human-readable    |
| Protocol Buffers | Binary | High-performance, typed     |
| MessagePack      | Binary | Compact JSON alternative    |
| CBOR             | Binary | IoT, constrained devices    |
| XDR              | Binary | RPC, NFS                    |

---

## Linking Theory to Exercises

| Concept | Exercise | What You Learn |
|---------|----------|----------------|
| Endianness | ex_9_01 | struct.pack/unpack, network byte order |
| Session state | ex_9_02 | FTP authentication, session lifecycle |
| Dual-channel | ex_9_03/04 | Control vs data connection |
| Binary framing | hw_9_01 | Length-prefixed messages |
| Checkpoints | hw_9_02 | Session recovery after failure |

---

## Key Takeaways

1. **Session ≠ Connection**: Sessions add application-level state beyond TCP
2. **Always use network byte order** (`>` or `!` in struct) for portability
3. **Framing is essential**: TCP doesn't preserve message boundaries
4. **Checksums detect errors**: Include them in every protocol
5. **FTP separates concerns**: Control and data on different channels
6. **Passive mode**: Necessary for NAT traversal (client initiates data connection)

---

## Further Reading

- RFC 959: File Transfer Protocol (FTP)
- RFC 4217: Securing FTP with TLS
- Stevens, W.R. *TCP/IP Illustrated, Volume 1*
- Kurose, J. & Ross, K. *Computer Networking: A Top-Down Approach*
- Cohen, D. "On Holy Wars and a Plea for Peace" (origin of endianness terms)

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
*Week 9: Session Layer and Presentation Layer*
