# Week 2: Theory Summary

> NETWORKING class - ASE, Informatics | by Revolvix

## Architectural Models Overview

Computer networks employ layered architectural models to manage complexity through abstraction, enable interoperability between vendors, and allow independent development of individual layers. The two primary models are the theoretical OSI reference model and the practical TCP/IP model that powers the Internet.

## The OSI Reference Model

The Open Systems Interconnection model, developed by ISO in the 1980s, provides a seven-layer framework for understanding network communication.

### Layer Summary

| Layer | Name | PDU | Primary Function |
|-------|------|-----|------------------|
| 7 | Application | Data | User interface, application protocols |
| 6 | Presentation | Data | Data formatting, encryption, compression |
| 5 | Session | Data | Connection management, dialogue control |
| 4 | Transport | Segment | End-to-end delivery, multiplexing |
| 3 | Network | Packet | Logical addressing, routing |
| 2 | Data Link | Frame | Physical addressing, error detection |
| 1 | Physical | Bit | Signal transmission on medium |

### Key Concepts

**PDU (Protocol Data Unit):** The data unit specific to each layer, containing the payload plus that layer's header.

**Encapsulation:** The process whereby each layer adds its own header (and sometimes trailer) to the data received from the layer above.

**SAP (Service Access Point):** The interface through which adjacent layers communicate, such as TCP/UDP ports.

## The TCP/IP Model

The practical four-layer model implemented by the Internet, developed for ARPANET in the 1970s.

### Layer Mapping

| TCP/IP Layer | OSI Equivalent | Key Protocols |
|--------------|----------------|---------------|
| Application | Layers 5, 6, 7 | HTTP, FTP, DNS, SMTP, SSH |
| Transport | Layer 4 | TCP, UDP |
| Internet | Layer 3 | IP, ICMP, ARP |
| Network Access | Layers 1, 2 | Ethernet, WiFi, PPP |

## Transport Layer Protocols

### TCP (Transmission Control Protocol)

**Characteristics:**
- Connection-oriented (three-way handshake)
- Reliable delivery with acknowledgements
- In-order delivery via sequence numbers
- Flow control (sliding window)
- Congestion control

**Three-Way Handshake:**
```
Client              Server
   │                   │
   │──── SYN ────────▶│  seq=x
   │                   │
   │◀─── SYN-ACK ─────│  seq=y, ack=x+1
   │                   │
   │──── ACK ────────▶│  ack=y+1
   │                   │
   │◀═══ DATA ═══════▶│  connection active
```

**Use Cases:** Web browsing, email, file transfer—applications requiring reliability.

### UDP (User Datagram Protocol)

**Characteristics:**
- Connectionless (no handshake)
- Best-effort delivery (no guarantees)
- No ordering
- Minimal overhead (8-byte header)
- Low latency

**Use Cases:** DNS queries, video streaming, online gaming, IoT—applications prioritising speed over reliability.

### Protocol Comparison

| Characteristic | TCP | UDP |
|----------------|-----|-----|
| Connection | Required | Not required |
| Reliability | Guaranteed | Best effort |
| Ordering | Preserved | Not guaranteed |
| Flow Control | Yes | No |
| Header Size | 20+ bytes | 8 bytes |
| Latency | Higher | Lower |

## Socket Programming Fundamentals

### Socket Types

**SOCK_STREAM (TCP):**
- Byte stream abstraction
- Connection must be established before data transfer
- Suitable for reliable, ordered communication

**SOCK_DGRAM (UDP):**
- Message (datagram) abstraction
- No connection—each message is independent
- Suitable for low-latency, loss-tolerant communication

### Basic Socket Flow

**TCP Server:**
1. Create socket
2. Bind to address and port
3. Listen for connections
4. Accept connection (creates new socket)
5. Receive/send data
6. Close connection

**UDP Server:**
1. Create socket
2. Bind to address and port
3. Receive datagram (includes sender address)
4. Send response
5. (No close—connectionless)

## Server Concurrency Models

### Iterative Server

Handles one client at a time, sequentially. Simple but creates bottleneck under load.

```python
while True:
    conn, addr = sock.accept()
    handle_client(conn)  # Blocks next accept
```

### Concurrent Server (Threading)

Spawns a new thread for each client connection. Enables parallel processing.

```python
while True:
    conn, addr = sock.accept()
    thread = Thread(target=handle_client, args=(conn,))
    thread.start()  # Returns immediately
```

## Packet Analysis

### Wireshark Display Filters

```
# Filter by protocol
tcp
udp

# Filter by port
tcp.port == 9090
udp.port == 9091

# Filter by flags
tcp.flags.syn == 1
tcp.flags.ack == 1

# Filter by IP
ip.addr == 127.0.0.1
```

### Key Fields to Observe

| Protocol | Field | Purpose |
|----------|-------|---------|
| IP | ip.src, ip.dst | Source/destination addresses |
| TCP | tcp.srcport, tcp.dstport | Port numbers |
| TCP | tcp.seq, tcp.ack | Sequence and acknowledgement numbers |
| TCP | tcp.flags | Control flags (SYN, ACK, FIN, etc.) |
| UDP | udp.length | Datagram length |

## References

- Kurose, J. & Ross, K. (2021). *Computer Networking: A Top-Down Approach* (8th ed.)
- Stevens, W. R. et al. (2004). *UNIX Network Programming, Vol. 1*
- RFC 793: Transmission Control Protocol
- RFC 768: User Datagram Protocol

---

*NETWORKING class - ASE, Informatics | by Revolvix*
