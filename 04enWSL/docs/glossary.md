# 📖 Glossary — Week 4: Physical Layer, Data Link & Custom Protocols

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

---

## Physical Layer Terms

| Term | Definition | Example |
|------|------------|---------|
| **Attenuation** | Signal strength loss over distance | Ethernet signal weakens after 100m |
| **Bandwidth** | Maximum data transfer rate of a channel | 1 Gbps for Cat6 cable |
| **Bit rate** | Number of bits transmitted per second | 100 Mbps |
| **Baud rate** | Number of signal changes per second | 1000 baud (may carry multiple bits) |
| **Crosstalk** | Interference between adjacent wires | Twisted pairs reduce crosstalk |
| **Dispersion** | Signal spreading over distance (fibre) | Limits fibre optic distance |
| **Encoding** | Converting bits to physical signals | Manchester, NRZ, 4B/5B |
| **Full-duplex** | Simultaneous two-way communication | Modern Ethernet |
| **Half-duplex** | One direction at a time | Legacy hubs, walkie-talkies |
| **Guided media** | Physical cables (copper, fibre) | UTP, coaxial, optical fibre |
| **Unguided media** | Wireless transmission | Wi-Fi, Bluetooth, infrared |

---

## Data Link Layer Terms

| Term | Definition | Example |
|------|------------|---------|
| **Frame** | Data Link layer data unit | Ethernet frame (64-1518 bytes) |
| **Framing** | Marking boundaries of data units | Length prefix, delimiters |
| **MAC address** | 48-bit hardware address | `00:1A:2B:3C:4D:5E` |
| **LLC** | Logical Link Control sublayer | IEEE 802.2 |
| **MAC** | Media Access Control sublayer | IEEE 802.3 (Ethernet) |
| **CSMA/CD** | Carrier Sense Multiple Access with Collision Detection | Wired Ethernet |
| **CSMA/CA** | Carrier Sense Multiple Access with Collision Avoidance | Wi-Fi |
| **CRC** | Cyclic Redundancy Check | CRC32 in Ethernet frames |
| **Checksum** | Sum-based error detection | IP header checksum |
| **Flow control** | Preventing receiver buffer overflow | Sliding window |
| **MTU** | Maximum Transmission Unit | 1500 bytes for Ethernet |

---

## Protocol Design Terms

| Term | Definition | Example |
|------|------------|---------|
| **Binary protocol** | Uses raw bytes for efficiency | DNS, HTTP/2 |
| **Text protocol** | Human-readable ASCII/UTF-8 | HTTP/1.1, SMTP |
| **Header** | Metadata preceding payload | 14-byte binary header |
| **Payload** | Actual data being transmitted | Message content |
| **Magic number** | Fixed bytes identifying protocol | `b'NP'` for our protocol |
| **Version field** | Protocol version for compatibility | Version = 1 |
| **Sequence number** | Ordering and duplicate detection | 4-byte incrementing counter |
| **Length prefix** | Payload size before data | 2-byte length field |
| **Delimiter** | Special character marking boundaries | `\r\n` in HTTP |
| **Overhead** | Non-payload bytes in transmission | Header size / total size |

---

## Python struct Module

| Format | Meaning | Size | Example |
|--------|---------|------|---------|
| `>` | Big-endian (network order) | — | `struct.pack('>H', 1000)` |
| `<` | Little-endian (x86 native) | — | `struct.pack('<H', 1000)` |
| `!` | Network order (same as `>`) | — | `struct.pack('!H', 1000)` |
| `B` | Unsigned byte | 1 byte | Values 0-255 |
| `b` | Signed byte | 1 byte | Values -128 to 127 |
| `H` | Unsigned short | 2 bytes | Values 0-65535 |
| `h` | Signed short | 2 bytes | Values -32768 to 32767 |
| `I` | Unsigned int | 4 bytes | Values 0 to 4294967295 |
| `i` | Signed int | 4 bytes | ±2147483647 |
| `Q` | Unsigned long long | 8 bytes | Very large values |
| `f` | Float | 4 bytes | IEEE 754 single precision |
| `d` | Double | 8 bytes | IEEE 754 double precision |
| `Ns` | String of N bytes | N bytes | `4s` = 4-byte string |

**Example:**

```python
import struct

# Pack: Magic(2s) + Version(B) + Type(B) + Length(H) + Seq(I) + CRC(I)
header = struct.pack('>2sBBHII', b'NP', 1, 3, 100, 12345, 0xDEADBEEF)
# Result: 14 bytes

# Unpack
magic, ver, typ, length, seq, crc = struct.unpack('>2sBBHII', header)
```

---

## Error Detection Terms

| Term | Definition | Example |
|------|------------|---------|
| **CRC32** | 32-bit Cyclic Redundancy Check | `zlib.crc32(data)` |
| **Polynomial** | Mathematical basis for CRC | CRC32 uses specific polynomial |
| **Burst error** | Multiple consecutive bit errors | Common in network transmission |
| **Hamming distance** | Minimum bit flips to change valid to valid | CRC32 has distance 5 |
| **Parity bit** | Simple single-bit error detection | Even or odd parity |
| **FEC** | Forward Error Correction | Reed-Solomon codes |

---

## Socket Programming Terms

| Term | Definition | Example |
|------|------------|---------|
| **Socket** | Endpoint for network communication | `socket.socket()` |
| **Bind** | Associate socket with address/port | `sock.bind(('', 5400))` |
| **Listen** | Mark socket as server | `sock.listen(5)` |
| **Accept** | Wait for incoming connection | `conn, addr = sock.accept()` |
| **Connect** | Initiate connection to server | `sock.connect(('host', port))` |
| **Send** | Transmit data (TCP) | `sock.send(data)` |
| **Recv** | Receive data | `data = sock.recv(1024)` |
| **Sendto** | Transmit data (UDP) | `sock.sendto(data, addr)` |
| **Recvfrom** | Receive data with address (UDP) | `data, addr = sock.recvfrom(1024)` |
| **Blocking** | Operation waits until complete | Default socket behaviour |
| **Non-blocking** | Operation returns immediately | `sock.setblocking(False)` |
| **Timeout** | Maximum wait time | `sock.settimeout(5.0)` |

---

## Network Byte Order

| Concept | Description |
|---------|-------------|
| **Big-endian** | Most significant byte first (network standard) |
| **Little-endian** | Least significant byte first (x86/x64) |
| **Network byte order** | Always big-endian for protocols |
| **Host byte order** | Depends on CPU architecture |

**Visual example:**

```
Value: 1000 decimal = 0x03E8 hexadecimal

Big-endian (network):    [03] [E8]  (MSB first)
Little-endian (x86):     [E8] [03]  (LSB first)
```

---

## Week 4 Protocol Specifics

### TEXT Protocol (TCP port 5400)

| Component | Description |
|-----------|-------------|
| Framing | Length prefix (space-separated ASCII) |
| Format | `<LENGTH> <PAYLOAD>` |
| Example | `5 hello` (length 5, payload "hello") |
| Commands | GET, SET, DEL, KEYS |

### BINARY Protocol (TCP port 5401)

| Field | Size | Description |
|-------|------|-------------|
| Magic | 2 bytes | `b'NP'` (Network Protocol) |
| Version | 1 byte | Protocol version (currently 1) |
| Type | 1 byte | Message type (ECHO=1, PUT=3, GET=5, etc.) |
| PayloadLen | 2 bytes | Payload length in bytes |
| Seq | 4 bytes | Sequence number |
| CRC32 | 4 bytes | Checksum of header + payload |
| Payload | Variable | Actual message data |

### UDP Sensor Protocol (UDP port 5402)

| Field | Size | Description |
|-------|------|-------------|
| Version | 1 byte | Protocol version |
| SensorID | 4 bytes | Unique sensor identifier |
| Temperature | 4 bytes | Float, big-endian |
| Humidity | 4 bytes | Float, big-endian |
| Timestamp | 8 bytes | Unix timestamp |
| CRC16 | 2 bytes | Checksum |

---

## Acronyms

| Acronym | Full Form | Context |
|---------|-----------|---------|
| ASCII | American Standard Code for Information Interchange | Text encoding |
| CRC | Cyclic Redundancy Check | Error detection |
| CSMA | Carrier Sense Multiple Access | Media access control |
| FCS | Frame Check Sequence | Error detection in frames |
| FEC | Forward Error Correction | Error correction |
| LLC | Logical Link Control | Data link sublayer |
| MAC | Media Access Control | Data link sublayer / Hardware address |
| MSB | Most Significant Byte | Big-endian first byte |
| LSB | Least Significant Byte | Little-endian first byte |
| MTU | Maximum Transmission Unit | Max frame payload |
| NRZ | Non-Return to Zero | Line encoding |
| OSI | Open Systems Interconnection | 7-layer reference model |
| PDU | Protocol Data Unit | Data at each layer |
| SDU | Service Data Unit | Data from upper layer |
| TCP | Transmission Control Protocol | Reliable byte stream |
| UDP | User Datagram Protocol | Unreliable datagrams |
| UTP | Unshielded Twisted Pair | Ethernet cabling |

---

## Relationships Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PROTOCOL LAYERS                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   Application Layer                                                         │
│   └── TEXT/BINARY Protocol (our custom protocols)                          │
│       ├── Framing (length-prefix)                                          │
│       ├── Commands (GET, SET, ECHO)                                        │
│       └── Serialisation (struct.pack/unpack)                               │
│                          │                                                  │
│                          ▼                                                  │
│   Transport Layer                                                           │
│   ├── TCP (port 5400, 5401) ──► Reliable byte stream                       │
│   └── UDP (port 5402) ────────► Unreliable datagrams                       │
│                          │                                                  │
│                          ▼                                                  │
│   Network Layer                                                             │
│   └── IP ─────────────────────► Addressing, routing                        │
│                          │                                                  │
│                          ▼                                                  │
│   Data Link Layer                                                           │
│   ├── LLC ────────────────────► Flow control, multiplexing                 │
│   └── MAC ────────────────────► Framing, addressing, error detection       │
│       └── CRC32 ──────────────► Frame Check Sequence                       │
│                          │                                                  │
│                          ▼                                                  │
│   Physical Layer                                                            │
│   └── Encoding, signalling, transmission medium                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  STRUCT FORMAT CHEATSHEET                                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  struct.pack('>2sBBHII', magic, ver, typ, len, seq, crc)                   │
│              │ │ │││││                                                      │
│              │ │ ││││└── I = unsigned int (4B) - CRC                       │
│              │ │ │││└─── I = unsigned int (4B) - Sequence                  │
│              │ │ ││└──── H = unsigned short (2B) - Length                  │
│              │ │ │└───── B = unsigned byte (1B) - Type                     │
│              │ │ └────── B = unsigned byte (1B) - Version                  │
│              │ └──────── 2s = 2-byte string - Magic                        │
│              └────────── > = big-endian (network order)                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  TOTAL: 2 + 1 + 1 + 2 + 4 + 4 = 14 bytes                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
*Week 4: Physical Layer, Data Link Layer & Custom Protocols*
