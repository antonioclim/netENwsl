# Week 8: Transport Layer - Theoretical Summary

> NETWORKING class - ASE, Informatics | by Revolvix

## Overview

The Transport Layer (Layer 4 in the OSI model, Layer 3 in TCP/IP) provides end-to-end communication services for applications. It manages the reliability, flow control, and multiplexing of data between hosts on a network.

## Key Protocols

### TCP (Transmission Control Protocol)

TCP is a connection-oriented protocol that provides reliable, ordered, and error-checked delivery of data between applications.

**Key Characteristics:**
- Connection establishment via three-way handshake (SYN → SYN-ACK → ACK)
- Full-duplex communication
- Flow control using sliding window mechanism
- Congestion control (slow start, congestion avoidance, fast retransmit)
- In-order delivery guarantee
- Checksum verification for data integrity

**Header Structure:**
- Source Port (16 bits)
- Destination Port (16 bits)
- Sequence Number (32 bits)
- Acknowledgement Number (32 bits)
- Data Offset (4 bits)
- Control Flags: URG, ACK, PSH, RST, SYN, FIN (6 bits)
- Window Size (16 bits)
- Checksum (16 bits)
- Urgent Pointer (16 bits)
- Options (variable)

**Connection States:**
1. CLOSED
2. LISTEN
3. SYN_SENT
4. SYN_RECEIVED
5. ESTABLISHED
6. FIN_WAIT_1
7. FIN_WAIT_2
8. CLOSE_WAIT
9. CLOSING
10. LAST_ACK
11. TIME_WAIT

### UDP (User Datagram Protocol)

UDP is a connectionless protocol that provides a simple, unreliable datagram service for applications that require speed over reliability.

**Key Characteristics:**
- No connection establishment overhead
- No delivery guarantee
- No ordering guarantee
- No flow control
- Minimal header overhead (8 bytes)
- Suitable for real-time applications (VoIP, video streaming, gaming)

**Header Structure:**
- Source Port (16 bits)
- Destination Port (16 bits)
- Length (16 bits)
- Checksum (16 bits)

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

### QUIC (Quick UDP Internet Connections)

QUIC is a modern transport protocol built on UDP, designed to reduce connection establishment latency and improve performance.

**Key Features:**
- Integrated TLS 1.3 encryption
- Multiplexed streams without head-of-line blocking
- Connection migration (handles IP address changes)
- 0-RTT connection resumption
- Improved congestion control

## HTTP over TCP

HTTP/1.1 and HTTP/2 operate over TCP connections, utilising the transport layer's reliability guarantees.

**HTTP/1.1:**
- Persistent connections (Connection: keep-alive)
- Pipelining (limited browser support)
- One request at a time per connection (head-of-line blocking)

**HTTP/2:**
- Binary framing
- Multiplexed streams on single connection
- Header compression (HPACK)
- Server push capability
- Stream prioritisation

**HTTP/3:**
- Built on QUIC
- Native stream multiplexing
- Reduced latency
- Better mobile performance

## Reverse Proxy and Load Balancing

A reverse proxy sits between clients and servers, forwarding client requests to appropriate backend servers.

### Load Balancing Algorithms

**Round-Robin:**
- Requests distributed sequentially across servers
- Simple and fair for homogeneous backends
- No consideration of server load

**Weighted Round-Robin:**
- Servers assigned weights based on capacity
- Higher-weight servers receive more requests
- Suitable for heterogeneous backend infrastructure

**Least Connections:**
- Routes to server with fewest active connections
- Adapts to varying request processing times
- Better load distribution under uneven workloads

**IP Hash:**
- Client IP determines backend server
- Provides session persistence
- Useful for stateful applications

### nginx Configuration

nginx implements reverse proxy and load balancing through upstream blocks:

```nginx
upstream backend_pool {
    server backend1:8080 weight=5;
    server backend2:8080 weight=3;
    server backend3:8080 weight=1;
}
```

## Port Concepts

**Well-Known Ports (0-1023):**
- HTTP: 80
- HTTPS: 443
- SSH: 22
- FTP: 21
- DNS: 53

**Registered Ports (1024-49151):**
- MySQL: 3306
- PostgreSQL: 5432
- Redis: 6379

**Dynamic/Ephemeral Ports (49152-65535):**
- Used for client-side connections
- Assigned dynamically by the operating system

## Socket Programming Considerations

When implementing HTTP servers:
- Use non-blocking I/O for scalability
- Handle partial reads/writes
- Implement proper connection timeout
- Consider thread pools for concurrent requests
- Parse HTTP headers carefully (CRLF delimiters)

## References

- RFC 793: Transmission Control Protocol
- RFC 768: User Datagram Protocol
- RFC 9110: HTTP Semantics
- RFC 8446: TLS 1.3
- RFC 9000: QUIC Transport Protocol
- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (7th ed.)

---

*NETWORKING class - ASE, Informatics | by Revolvix*
