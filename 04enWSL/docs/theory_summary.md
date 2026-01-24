# Week 4: Theory Summary

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

## Overview

Week 4 focuses on the **Physical Layer** and **Data Link Layer** of the OSI model, along with practical implementation of custom protocols over TCP and UDP. This document summarises the key theoretical concepts that underpin the laboratory exercises.

---

## The Physical Layer (Layer 1)

### Function and Purpose

The Physical Layer constitutes the lowest stratum of the OSI model, responsible for the raw transmission of unstructured bit streams across a physical medium. It defines the electrical, optical, or radio specifications required to establish, maintain and terminate physical connections between network devices.

### Transmission Media

Physical Layer implementations employ three principal categories of transmission media:

**Guided Media (Wired)**
- **Twisted Pair Cable**: Copper conductors twisted helically to reduce electromagnetic interference. Categories range from Cat5e (1 Gbps) to Cat8 (25–40 Gbps)
- **Coaxial Cable**: Central conductor surrounded by insulating layer and metallic shield. Used in cable television and legacy Ethernet
- **Optical Fibre**: Glass or plastic fibres transmitting modulated light pulses. Supports distances exceeding 100 km at speeds above 100 Gbps

**Unguided Media (Wireless)**
- **Radio Waves**: IEEE 802.11 (Wi-Fi), operating in 2.4 GHz and 5 GHz bands
- **Microwaves**: Point-to-point links for backhaul connectivity
- **Infrared**: Short-range, line-of-sight communication

### Signal Encoding

The conversion of digital data to physical signals employs several encoding schemes:

| Scheme | Description | Application |
|--------|-------------|-------------|
| NRZ (Non-Return to Zero) | Binary 1 = high voltage, 0 = low voltage | Simple serial links |
| Manchester | Transition in middle of bit period encodes data | Ethernet (10BASE-T) |
| 4B/5B | Four data bits encoded as five-bit symbols | Fast Ethernet |
| 8B/10B | Eight data bits encoded as ten-bit symbols | Gigabit Ethernet |
| PAM-4 | Four amplitude levels encode two bits per symbol | 400G Ethernet |

### Synchronisation

Maintaining temporal alignment between transmitter and receiver requires either:

- **Asynchronous Transmission**: Start and stop bits frame each character
- **Synchronous Transmission**: Clock signal embedded in data stream or transmitted separately

---

## The Data Link Layer (Layer 2)

### Function and Purpose

The Data Link Layer provides reliable node-to-node data transfer by converting the raw Physical Layer bit stream into discrete data frames. It handles error detection, flow control and media access in shared communication channels.

### Sublayer Architecture

The IEEE 802 standards divide the Data Link Layer into two sublayers:

**LLC (Logical Link Control)** — IEEE 802.2
- Provides interface to Network Layer
- Implements flow control and error recovery
- Supports multiple network protocols simultaneously

**MAC (Media Access Control)** — IEEE 802.3, 802.11, etc.
- Controls access to shared transmission medium
- Defines physical addressing (MAC addresses)
- Implements specific protocol standards (Ethernet, Wi-Fi)

### Framing

Framing delineates the boundaries of data units within the continuous bit stream. Several techniques exist:

**Character Count**
A length field in the header specifies the number of bytes in the frame.

```
+--------+-------------------+
| Length | Payload (N bytes) |
+--------+-------------------+
```

**Character Stuffing**
Special delimiter characters mark frame boundaries. Escape sequences handle delimiter occurrence in data.

```
+-------+---------+-------+
| START | Payload | END   |
+-------+---------+-------+
```

**Bit Stuffing**
A fixed pattern (e.g., 01111110) marks frame boundaries. Five consecutive 1s in data trigger insertion of a 0 bit.

**Physical Layer Coding Violations**
Invalid signal patterns in the encoding scheme indicate frame boundaries.

### Error Detection

Data Link protocols employ several error detection mechanisms:

**Parity Check**
Single bit appended to make total number of 1s even (even parity) or odd (odd parity). Detects single-bit errors only.

**Checksum**
Arithmetic sum of data segments, typically with one's complement. Used in IP, TCP and UDP headers.

**Cyclic Redundancy Check (CRC)**
Polynomial division produces fixed-length remainder appended to data. Common polynomials:

| Standard | Polynomial | Length | Detection Capability |
|----------|-----------|--------|---------------------|
| CRC-8 | x⁸ + x² + x + 1 | 8 bits | Burst errors ≤ 8 bits |
| CRC-16 | x¹⁶ + x¹⁵ + x² + 1 | 16 bits | Burst errors ≤ 16 bits |
| CRC-32 | x³² + x²⁶ + x²³ + ... + 1 | 32 bits | Burst errors ≤ 32 bits |

CRC-32 is standard in Ethernet frames and achieves 99.9999998% detection of errors.

### Flow Control

Preventing buffer overflow at the receiver requires flow control mechanisms:

**Stop-and-Wait**
Sender transmits one frame and awaits acknowledgement before sending the next. Simple but inefficient for high bandwidth-delay products.

**Sliding Window**
Sender maintains a window of frames that may be outstanding simultaneously. Window size W determines throughput:

```
Efficiency = W / (1 + 2a)

where a = propagation delay / transmission time
```

### Media Access Control

Shared media require coordination to prevent collisions:

**Random Access**
- ALOHA: Transmit at will, retransmit on collision
- CSMA (Carrier Sense Multiple Access): Listen before transmitting
- CSMA/CD: Collision detection terminates transmission early (Ethernet)
- CSMA/CA: Collision avoidance via acknowledgements (Wi-Fi)

**Controlled Access**
- Token Passing: Transmit only when holding token (Token Ring)
- Polling: Central controller queries stations in turn

**Channelisation**
- TDMA (Time Division): Each station assigned time slots
- FDMA (Frequency Division): Each station assigned frequency band
- CDMA (Code Division): Each station assigned unique spreading code

---

## Custom Protocol Design

### Protocol Structure

Application-level protocols implemented over TCP or UDP require careful structural design:

**Text Protocols**
- Human-readable format (ASCII)
- Self-documenting messages
- Easier debugging with standard tools
- Examples: HTTP/1.1, SMTP, FTP control

**Binary Protocols**
- Compact representation
- Fixed-width fields for efficient parsing
- Reduced bandwidth consumption
- Examples: DNS, HTTP/2, Protocol Buffers

### Framing in TCP Streams

TCP provides a reliable byte stream with no inherent message boundaries. Applications must implement framing:

**Length Prefix**
Message preceded by fixed-width field indicating payload length:

```
+--------+--------+-------------------+
| Length (2 bytes)| Payload (N bytes) |
+--------+--------+-------------------+
```

**Delimiter-Based**
Special character or sequence marks message end:

```
+-------------------+-------+
| Payload           | \r\n  |
+-------------------+-------+
```

Requires escaping or prohibition of delimiter in payload.

**Fixed-Length Messages**
All messages occupy identical byte count. Padding required for shorter content.

### Integrity Verification

Ensuring data integrity beyond TCP's checksum:

**Application-Level CRC**
Computing CRC-32 over payload detects corruption not caught by transport layer (rare but possible in end-to-end scenarios).

**Sequence Numbers**
Monotonically increasing identifiers detect:
- Duplicate messages (same sequence number)
- Lost messages (gap in sequence numbers)
- Reordered messages (out-of-sequence arrival)

---

## Laboratory Relevance

The Week 4 exercises implement these concepts:

| Concept | Exercise Implementation |
|---------|------------------------|
| Length-prefix framing | TEXT protocol over TCP |
| Fixed-width headers | BINARY protocol over TCP |
| CRC-32 integrity | BINARY and UDP protocols |
| Sequence numbers | BINARY protocol |
| Connectionless transport | UDP sensor protocol |

---

## Key Equations

**Transmission Time**
```
T = L / R

where L = frame length (bits), R = data rate (bps)
```

**Propagation Delay**
```
D = d / v

where d = distance (m), v = propagation velocity (m/s)
```

**Bandwidth-Delay Product**
```
BDP = R × RTT

where R = data rate, RTT = round-trip time
```

**CRC Polynomial Division**
```
R(x) = M(x) × xⁿ mod G(x)

where M(x) = message polynomial, G(x) = generator polynomial, n = degree of G(x)
```

---

## Common Misconceptions

Students often hold incorrect assumptions about these topics. See `misconceptions.md` for detailed explanations:

- TCP preserves message boundaries (it does not)
- CRC guarantees data integrity (it only detects errors)
- Big-endian and little-endian are interchangeable (they are not)
- Binary protocols are always better than text (depends on use case)

---

## Further Reading

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (7th ed.), Chapters 4–5
- Tanenbaum, A. & Wetherall, D. (2011). *Computer Networks* (5th ed.), Chapters 3–4
- Peterson, L. & Davie, B. (2021). *Computer Networks: A Systems Approach* (6th ed.)
- RFC 793: Transmission Control Protocol
- RFC 768: User Datagram Protocol
- IEEE 802.3: Ethernet Standard

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
