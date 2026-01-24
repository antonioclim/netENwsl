# Week 8: Transport Layer — Theoretical Summary

> NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

## Overview

The Transport Layer (Layer 4 in OSI, Layer 3 in TCP/IP) provides end-to-end communication services for applications. It handles reliability, flow control and multiplexing of data between hosts on a network.

> 💭 **Test yourself:** Before reading further, can you explain why applications need the transport layer? Why can't they just use IP directly?

---

## Key Protocols

### TCP (Transmission Control Protocol)

TCP is a connection-oriented protocol that provides reliable, ordered and error-checked delivery of data between applications.

**Key Characteristics:**
- Connection establishment via three-way handshake (SYN → SYN-ACK → ACK)
- Full-duplex communication
- Flow control using sliding window mechanism
- Congestion control (slow start, congestion avoidance, fast retransmit)
- In-order delivery guarantee
- Checksum verification for data integrity

**Header Structure (20 bytes minimum):**

| Field | Size | Purpose |
|-------|------|---------|
| Source Port | 16 bits | Sender's port number |
| Destination Port | 16 bits | Receiver's port number |
| Sequence Number | 32 bits | Position of first data byte |
| Acknowledgement Number | 32 bits | Next expected byte |
| Data Offset | 4 bits | Header length (in 32-bit words) |
| Control Flags | 6 bits | URG, ACK, PSH, RST, SYN, FIN |
| Window Size | 16 bits | Receiver's buffer space |
| Checksum | 16 bits | Error detection |
| Urgent Pointer | 16 bits | Priority data offset |

> 💭 **Think about it:** Why is the sequence number 32 bits? What would happen with fewer bits?

**Connection States:**

```
CLOSED → LISTEN → SYN_RECEIVED → ESTABLISHED
   ↑                                  ↓
   └──── TIME_WAIT ← FIN_WAIT_2 ← FIN_WAIT_1
```

### UDP (User Datagram Protocol)

UDP is a connectionless protocol providing simple, unreliable datagram service for applications that prioritise speed over reliability.

**Key Characteristics:**
- No connection establishment overhead
- No delivery guarantee
- No ordering guarantee
- No flow control
- Minimal header overhead (8 bytes)
- Suitable for real-time applications (VoIP, video streaming, gaming)

**Header Structure (8 bytes):**

| Field | Size | Purpose |
|-------|------|---------|
| Source Port | 16 bits | Sender's port |
| Destination Port | 16 bits | Receiver's port |
| Length | 16 bits | Header + data length |
| Checksum | 16 bits | Error detection |

> 💭 **Consider:** When would you choose UDP over TCP? Think of three real applications.

### TLS (Transport Layer Security)

TLS provides cryptographic security for communications over TCP. It operates between the Transport and Application layers.

**Key Features:**
- Server authentication (and optional client authentication)
- Data encryption (symmetric encryption after handshake)
- Data integrity (MAC verification)
- Perfect Forward Secrecy (with ephemeral key exchange)

**TLS 1.3 Improvements:**
- Reduced handshake latency (1-RTT, 0-RTT resumption)
- Removed legacy cryptographic algorithms
- Mandatory AEAD encryption
- Simplified cipher suite negotiation

---

## HTTP over TCP

HTTP/1.1 and HTTP/2 operate over TCP connections, using the transport layer's reliability guarantees.

### HTTP/1.1

- Persistent connections (`Connection: keep-alive` by default)
- Pipelining (limited browser support)
- One request at a time per connection (head-of-line blocking)

### HTTP/2

- Binary framing (not text-based)
- Multiplexed streams on single connection
- Header compression (HPACK)
- Server push capability
- Stream prioritisation

### HTTP/3

- Built on QUIC (UDP-based)
- Native stream multiplexing
- Reduced latency
- Better mobile performance

> 💭 **Prediction:** If HTTP/2 already multiplexes streams, why was HTTP/3 needed? What problem does QUIC solve that TCP cannot?

---

## Reverse Proxy and Load Balancing

A reverse proxy sits between clients and servers, forwarding client requests to appropriate backend servers.

### Load Balancing Algorithms

| Algorithm | Description | Best For |
|-----------|-------------|----------|
| **Round-Robin** | Sequential distribution | Homogeneous backends |
| **Weighted Round-Robin** | Proportional distribution | Different server capacities |
| **Least Connections** | Route to least busy server | Varying request durations |
| **IP Hash** | Client IP determines backend | Session persistence |

### nginx Upstream Configuration

```nginx
upstream backend_pool {
    server backend1:8080 weight=5;
    server backend2:8080 weight=3;
    server backend3:8080 weight=1;
}
```

> 💭 **Calculate:** With weights 5:3:1, how many of the first 18 requests go to each backend?

---

## Port Concepts

### Well-Known Ports (0-1023)

| Port | Protocol | Service |
|------|----------|---------|
| 20, 21 | FTP | File Transfer |
| 22 | SSH | Secure Shell |
| 53 | DNS | Domain Name System |
| 80 | HTTP | Web (unencrypted) |
| 443 | HTTPS | Web (encrypted) |

### Registered Ports (1024-49151)

| Port | Service |
|------|---------|
| 3306 | MySQL |
| 5432 | PostgreSQL |
| 6379 | Redis |
| 8080 | HTTP Alternate |
| 9000 | Portainer |

### Dynamic/Ephemeral Ports (49152-65535)

- Used for client-side connections
- Assigned dynamically by the operating system
- Released when connection closes

---

## Socket Programming Considerations

When implementing HTTP servers:

1. **Use non-blocking I/O** for scalability (or threading/async)
2. **Handle partial reads/writes** — TCP is a stream protocol
3. **Implement proper timeouts** — prevent resource exhaustion
4. **Consider thread pools** for concurrent request handling
5. **Parse HTTP carefully** — CRLF delimiters, header case-insensitivity

> 💭 **Think ahead:** What happens if you call `recv(4096)` but the client only sent 100 bytes? What if they sent 10,000 bytes?

---

## Test Your Understanding

Before proceeding to exercises, answer these questions:

1. Why does TCP need a three-way handshake instead of two-way?
2. What is the maximum port number? Why?
3. How does a reverse proxy differ from a forward proxy?
4. What header tells the server how many bytes are in the HTTP body?
5. Why might you use UDP for a video call instead of TCP?

<details>
<summary>Check your answers</summary>

1. **Three-way handshake:** Confirms bidirectional communication. Two-way would only confirm one direction.
2. **Maximum port:** 65535 (16 bits = 2^16 - 1). Historical design decision balancing header size vs port range.
3. **Reverse vs forward:** Reverse proxy is deployed by server (clients unaware); forward proxy is configured by client.
4. **Body length:** `Content-Length` header specifies body size in bytes.
5. **UDP for video:** Late packets are useless; TCP retransmission adds latency. Better to skip frames than wait.
</details>

---

## References

- RFC 793: Transmission Control Protocol
- RFC 768: User Datagram Protocol
- RFC 9110: HTTP Semantics
- RFC 8446: TLS 1.3
- RFC 9000: QUIC Transport Protocol
- Kurose, J. & Ross, K. (2021). *Computer Networking: A Top-Down Approach* (8th ed.)

---

## Related Documents

- [docs/misconceptions.md](misconceptions.md) — Common mistakes about these topics
- [docs/glossary.md](glossary.md) — Term definitions
- [docs/peer_instruction.md](peer_instruction.md) — Discussion questions

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
