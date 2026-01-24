# Week 2: Theory Summary — Architectural Models and Socket Programming

> NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim

---

## 🎯 Learning Path (CPA Method)

This summary follows the **Concrete → Pictorial → Abstract** progression:

| Phase | What You Experience | Examples in This Week |
|-------|--------------------|-----------------------|
| **CONCRETE** | Tangible analogies | Phone calls (TCP), postcards (UDP), hotel reception (ports) |
| **PICTORIAL** | Visual diagrams | Handshake sequence, layer stacks, socket lifecycle |
| **ABSTRACT** | Code and protocols | Python sockets, Wireshark filters, RFC specifications |

**After completing this material, you will be able to:**
- **EXPLAIN** the differences between OSI and TCP/IP models
- **COMPARE** TCP and UDP characteristics and select appropriately
- **IMPLEMENT** basic client-server applications using Python sockets
- **ANALYSE** network traffic using Wireshark filters
- **EVALUATE** when to use iterative vs threaded server designs

---

## Architectural Models Overview

> **Learning Objective:** UNDERSTAND how layered models organise network complexity.

Computer networks employ layered architectural models to manage complexity through abstraction, enable interoperability between vendors and allow independent development of individual layers. The two primary models are the theoretical OSI reference model and the practical TCP/IP model that powers the Internet.

### Concrete Analogy: The Postal System

Think of network layers like sending a parcel internationally:
- **Application layer** = You write the letter content
- **Presentation layer** = You translate it if needed
- **Session layer** = You manage the correspondence thread
- **Transport layer** = You choose tracked (TCP) or standard (UDP) delivery
- **Network layer** = The postal service routes between countries
- **Data Link layer** = Local delivery van handles street-level transport
- **Physical layer** = The actual road the van drives on

---

## The OSI Reference Model

> **Learning Objective:** RECALL the seven layers and their Protocol Data Units.

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

---

## The TCP/IP Model

> **Learning Objective:** MAP OSI layers to the practical TCP/IP model.

The practical four-layer model implemented by the Internet, developed for ARPANET in the 1970s.

### Layer Mapping

| TCP/IP Layer | OSI Equivalent | Key Protocols |
|--------------|----------------|---------------|
| Application | Layers 5, 6, 7 | HTTP, FTP, DNS, SMTP, SSH |
| Transport | Layer 4 | TCP, UDP |
| Internet | Layer 3 | IP, ICMP, ARP |
| Network Access | Layers 1, 2 | Ethernet, WiFi, PPP |

---

## Transport Layer Protocols

> **Learning Objective:** COMPARE TCP and UDP and SELECT the appropriate protocol for given scenarios.

### TCP (Transmission Control Protocol)

#### Concrete Analogy: A Phone Call

TCP works like a phone conversation:
1. You dial and wait for the other person to answer (handshake)
2. You confirm they can hear you ("Hello?") and they confirm back
3. You take turns speaking in order
4. If someone misses something, they ask you to repeat
5. You say goodbye before hanging up (connection teardown)

#### Characteristics

- Connection-oriented (three-way handshake)
- Reliable delivery with acknowledgements
- In-order delivery via sequence numbers
- Flow control (sliding window)
- Congestion control

#### Three-Way Handshake (Pictorial)

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

#### Concrete Analogy: Postcards

UDP works like sending postcards:
1. You write and post immediately (no setup)
2. No confirmation of delivery
3. They might arrive out of order or not at all
4. Very fast and cheap
5. Perfect for "I'm here, wish you were here" messages where losing one is acceptable

#### Characteristics

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

---

## Socket Programming Concepts

> **Learning Objective:** IMPLEMENT client-server communication using Python sockets.

### Concrete Analogy: Telephone Sockets

A socket is like a telephone handset:
- **Creating a socket** = Picking up the phone
- **Binding** = Assigning your phone number
- **Listening** = Turning on the ringer
- **Accepting** = Answering a call
- **Connecting** = Dialling someone
- **Send/Recv** = Speaking and listening
- **Closing** = Hanging up

### Socket Types

**SOCK_STREAM (TCP):**
- Byte stream abstraction
- Connection must be established before data transfer
- Suitable for reliable, ordered communication

**SOCK_DGRAM (UDP):**
- Message (datagram) abstraction
- No connection—each message is independent
- Suitable for low-latency, loss-tolerant communication

### Socket Lifecycle (Pictorial)

```
TCP Server                          TCP Client
──────────                          ──────────
socket()                            socket()
   │                                   │
bind()                                 │
   │                                   │
listen()                               │
   │                                   │
accept() ◄─────── connect() ──────────┘
   │                   │
recv() ◄═══════════ send()
   │                   │
send() ═══════════► recv()
   │                   │
close()              close()
```

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

---

## Server Concurrency Models

> **Learning Objective:** EVALUATE iterative vs concurrent server designs for different workloads.

### Concrete Analogy: Bank Tellers

- **Iterative server** = One teller, long queue. Everyone waits.
- **Threaded server** = Multiple tellers, parallel service. Faster overall.

### Iterative Server

Handles one client at a time, sequentially. Simple but creates bottleneck under load.

```python
while True:
    conn, addr = sock.accept()
    handle_client(conn)  # Blocks next accept
```

**When to use:** Low traffic, simple protocols, resource-constrained systems.

### Concurrent Server (Threading)

Spawns a new thread for each client connection. Enables parallel processing.

```python
while True:
    conn, addr = sock.accept()
    thread = Thread(target=handle_client, args=(conn,))
    thread.start()  # Returns immediately
```

**When to use:** Multiple simultaneous clients, I/O-bound operations.

---

## Packet Analysis with Wireshark

> **Learning Objective:** ANALYSE captured traffic using display filters.

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

---

## Self-Check Questions

Test your understanding before the lab:

1. **RECALL:** What are the four layers of the TCP/IP model?

2. **UNDERSTAND:** Why does TCP require a three-way handshake while UDP does not?

3. **APPLY:** If you need to send 1000 small sensor readings per second where losing a few is acceptable, which protocol would you choose and why?

4. **ANALYSE:** Looking at a Wireshark capture, how can you identify the start of a new TCP connection?

5. **EVALUATE:** Your server handles 50 concurrent clients. Each request takes 100ms of CPU time. Would you use an iterative or threaded design? What trade-offs exist?

<details>
<summary>Quick Answers</summary>

1. Application, Transport, Internet, Network Access
2. TCP needs to establish connection state on both ends; UDP sends immediately without state
3. UDP — low latency, acceptable loss, minimal overhead for small messages
4. Look for SYN flag set, no ACK flag (first packet of handshake)
5. Threaded for parallelism, but watch for thread overhead and resource contention

</details>

---

## References

- Kurose, J. & Ross, K. (2021). *Computer Networking: A Top-Down Approach* (8th ed.)
- Stevens, W. R. et al. (2004). *UNIX Network Programming, Vol. 1*
- RFC 793: Transmission Control Protocol
- RFC 768: User Datagram Protocol

---

*NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim*
