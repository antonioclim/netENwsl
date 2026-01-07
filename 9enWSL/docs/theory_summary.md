# Theoretical Summary: Week 9

> Session Layer (L5) and Presentation Layer (L6)
> NETWORKING class - ASE, Informatics | by Revolvix

## Overview

Week 9 explores the intermediate layers of the OSI model that bridge the reliable
transport layer (L4) with application-specific protocols (L7). These layers handle
**dialogue management** (session) and **data representation** (presentation).

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

### Real-World Examples

- **HTTP Sessions**: Cookies maintain user state across multiple TCP connections
- **FTP Sessions**: Authentication persists while data connections open/close
- **Database Connections**: Transaction state maintained across queries

---

## Presentation Layer (L6)

### Purpose

The presentation layer handles **data syntax** transformations:

- **Serialisation**: Converting data structures to byte streams
- **Encoding**: Character set conversions (ASCII, UTF-8, etc.)
- **Compression**: Reducing data size for transmission
- **Encryption**: Protecting data confidentiality

### Endianness (Byte Order)

Multi-byte numbers can be stored in two ways:

```
Value: 0x12345678

Big-Endian (Network Order):
┌────┬────┬────┬────┐
│ 12 │ 34 │ 56 │ 78 │  ← Most significant byte first
└────┴────┴────┴────┘

Little-Endian (Intel/AMD):
┌────┬────┬────┬────┐
│ 78 │ 56 │ 34 │ 12 │  ← Least significant byte first
└────┴────┴────┴────┘
```

**Golden Rule**: Network protocols use **big-endian** (network byte order).

### Python `struct` Format Characters

| Character | Meaning                    | Size    |
|-----------|----------------------------|---------|
| `>`       | Big-endian (network)       | -       |
| `<`       | Little-endian              | -       |
| `!`       | Network byte order (= `>`) | -       |
| `B`       | Unsigned byte              | 1 byte  |
| `H`       | Unsigned short             | 2 bytes |
| `I`       | Unsigned int               | 4 bytes |
| `s`       | String (bytes)             | n bytes |

### Example: Protocol Header

```python
import struct
import zlib

# Define header format: magic(4), length(4), crc(4), flags(4)
HEADER_FORMAT = ">4sIII"

def pack_message(payload: bytes) -> bytes:
    magic = b"FTPC"
    length = len(payload)
    crc = zlib.crc32(payload) & 0xFFFFFFFF
    flags = 0
    
    header = struct.pack(HEADER_FORMAT, magic, length, crc, flags)
    return header + payload
```

---

## FTP Protocol Analysis

### Architecture

FTP uses **two separate connections**:

1. **Control Connection** (port 21): Text commands, session management
2. **Data Connection** (port 20 or dynamic): File transfers

```
┌─────────────┐                    ┌─────────────┐
│   Client    │──── Control ──────│   Server    │
│             │     (port 21)      │             │
│             │                    │             │
│             │──── Data ─────────│             │
│             │  (port 20/dyn)    │             │
└─────────────┘                    └─────────────┘
```

### Session Lifecycle

```
1. TCP Connect (SYN/SYN-ACK/ACK)
2. Server: "220 Welcome"
3. Client: "USER alice"
4. Server: "331 Password required"
5. Client: "PASS secret"
6. Server: "230 Logged in"      ← Session established
7. Client: "PWD" / "LIST" / "RETR" / etc.
8. Client: "QUIT"
9. Server: "221 Goodbye"        ← Session closed
```

### Transfer Modes

| Mode   | Command   | Usage                    |
|--------|-----------|--------------------------|
| ASCII  | `TYPE A`  | Text files (line ending conversion) |
| Binary | `TYPE I`  | Executables, images, archives |

### Active vs Passive Mode

| Mode    | Initiator | Firewall-friendly |
|---------|-----------|-------------------|
| Active  | Server → Client:20 | ✗ |
| Passive | Client → Server:dyn | ✓ |

---

## Practical Applications

### Binary Protocol Design Checklist

1. **Magic bytes**: Identify protocol, aid resynchronisation
2. **Version field**: Allow protocol evolution
3. **Length field**: Enable message framing
4. **Checksum**: Verify integrity (CRC-32, MD5, SHA-256)
5. **Flags**: Optional features (compression, encryption)

### Common Serialisation Formats

| Format          | Type   | Use Case                    |
|-----------------|--------|-----------------------------|
| JSON            | Text   | Web APIs, human-readable    |
| Protocol Buffers| Binary | High-performance, typed     |
| MessagePack     | Binary | Compact JSON alternative    |
| CBOR            | Binary | IoT, constrained devices    |

---

## Key Takeaways

1. **Session ≠ Connection**: Sessions add application-level state
2. **Always use network byte order** for portability
3. **Framing is essential**: TCP doesn't preserve message boundaries
4. **Checksums detect errors**: Include them in every protocol
5. **FTP separates concerns**: Control and data on different channels

---

## Further Reading

- RFC 959: File Transfer Protocol (FTP)
- RFC 4217: Securing FTP with TLS
- Stevens, W.R. *TCP/IP Illustrated, Volume 1*
- Kurose, J. & Ross, K. *Computer Networking: A Top-Down Approach*

---

*NETWORKING class - ASE, Informatics | by Revolvix*
