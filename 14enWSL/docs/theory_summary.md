# Week 14: Theoretical Background Summary

> NETWORKING class — ASE, CSIE | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

This document summarises the key theoretical concepts relevant to Week 14's integrated laboratory session.

---

💭 **PREDICTION:** Before reading this document, estimate: How many OSI layers can you name from memory? Write down your answer, then check against Section 1.

---

## 1. TCP/IP Protocol Stack Review

### Layer Model Comparison

| OSI Layer | TCP/IP Layer | Protocols | PDU |
|-----------|--------------|-----------|-----|
| Application (7) | Application | HTTP, FTP, DNS, SMTP | Data |
| Presentation (6) | Application | SSL/TLS, compression | Data |
| Session (5) | Application | Sockets, sessions | Data |
| Transport (4) | Transport | TCP, UDP | Segment/Datagram |
| Network (3) | Internet | IP, ICMP, OSPF | Packet |
| Data Link (2) | Network Access | Ethernet, ARP | Frame |
| Physical (1) | Network Access | Cables, signals | Bits |

### Encapsulation Process

When application data travels down the stack:

1. **Application Layer:** Data is prepared (e.g., HTTP request)
2. **Transport Layer:** TCP header added (ports, sequence numbers) → Segment
3. **Network Layer:** IP header added (source/destination IPs) → Packet
4. **Data Link Layer:** Ethernet header/trailer added (MAC addresses) → Frame
5. **Physical Layer:** Converted to electrical/optical signals

## 2. TCP Connection Management

💭 **PREDICTION:** How many packets are exchanged in a TCP three-way handshake? Write down your answer before reading further.

### Three-Way Handshake

Connection establishment uses the SYN, SYN-ACK, ACK sequence:

```
Client                          Server
  |                                |
  |-------- SYN (seq=x) --------->|
  |                                |
  |<---- SYN-ACK (seq=y, ack=x+1) -|
  |                                |
  |-------- ACK (ack=y+1) -------->|
  |                                |
  |===== Connection Established ===|
```

### Connection Termination

Graceful termination uses the FIN sequence:

```
Client                          Server
  |                                |
  |-------- FIN ----------------->|
  |<------- ACK ------------------|
  |<------- FIN ------------------|
  |-------- ACK ----------------->|
  |                                |
  |===== Connection Closed ========|
```

### TCP Flags

| Flag | Purpose |
|------|---------|
| SYN | Synchronise sequence numbers (connection initiation) |
| ACK | Acknowledgement field is significant |
| FIN | No more data from sender (connection termination) |
| RST | Reset the connection (abort) |
| PSH | Push buffered data to application |
| URG | Urgent pointer field is significant |

## 3. HTTP Protocol

### Request-Response Model

HTTP follows a simple request-response pattern:

```
Client                                Server
  |                                      |
  |-- TCP connect to port 80/443 ------->|
  |                                      |
  |-- GET /index.html HTTP/1.1 --------->|
  |-- Host: example.com                  |
  |-- Accept: text/html                  |
  |                                      |
  |<-- HTTP/1.1 200 OK ------------------|
  |<-- Content-Type: text/html           |
  |<-- Content-Length: 1234              |
  |<-- <html>...</html>                  |
  |                                      |
```

### Common Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request succeeded |
| 301 | Moved Permanently | Resource relocated |
| 400 | Bad Request | Malformed request |
| 404 | Not Found | Resource doesn't exist |
| 500 | Internal Server Error | Server-side error |
| 502 | Bad Gateway | Upstream server error |
| 503 | Service Unavailable | Server temporarily unavailable |

## 4. Load Balancing and Reverse Proxies

### Reverse Proxy Architecture

A reverse proxy sits between clients and backend servers:

```
                        ┌─────────────┐
                        │  Backend A  │
Client ───► Proxy ──────┼─────────────┤
                        │  Backend B  │
                        └─────────────┘
```

### Benefits of Reverse Proxies

1. **Load Distribution:** Spreads requests across multiple backends
2. **High Availability:** Continues serving if one backend fails
3. **SSL Termination:** Handles encryption at the proxy
4. **Caching:** Stores frequently requested content
5. **Security:** Hides internal infrastructure

### Round-Robin Scheduling

The simplest load balancing algorithm:

```
Request 1 → Backend A
Request 2 → Backend B
Request 3 → Backend A
Request 4 → Backend B
...
```

Each backend receives requests in rotation, ensuring equal distribution.

### Forwarding Headers

Proxies add headers to preserve client information:

| Header | Purpose |
|--------|---------|
| X-Forwarded-For | Original client IP address |
| X-Real-IP | Client IP (alternative to XFF) |
| X-Forwarded-Host | Original Host header |
| X-Forwarded-Proto | Original protocol (http/https) |

## 5. Network Address Translation (NAT)

### NAT in Docker

Docker uses NAT to enable container networking:

```
Host Network (192.168.x.x)
        │
        ▼
┌───────────────────────────────────┐
│      Docker Bridge (172.20.0.1)   │
│                                    │
│  ┌─────────┐      ┌─────────┐    │
│  │Container│      │Container│    │
│  │172.20.0.2│      │172.20.0.3│   │
│  └─────────┘      └─────────┘    │
└───────────────────────────────────┘
```

Port mapping (`-p 8080:80`) translates:
- External: `host_ip:8080` → Internal: `container_ip:80`

## 6. Packet Analysis Concepts

### Capture Points

Different capture locations reveal different traffic:

1. **Client interface:** Sees all traffic from client perspective
2. **Proxy interface:** Sees both client-proxy and proxy-backend traffic
3. **Backend interface:** Sees only proxy-backend traffic

### Key Analysis Filters (Wireshark)

```
# TCP connection analysis
tcp.flags.syn == 1 && tcp.flags.ack == 0    # SYN packets (new connections)
tcp.flags.fin == 1                           # FIN packets (closing)
tcp.flags.rst == 1                           # RST packets (aborts)

# HTTP analysis
http.request                                 # HTTP requests only
http.response                                # HTTP responses only
http.response.code == 200                    # Successful responses
http.request.method == "GET"                 # GET requests

# IP address filtering
ip.addr == 172.20.0.2                        # Traffic to/from IP
ip.src == 172.21.0.2                         # Traffic from IP
ip.dst == 172.20.0.10                        # Traffic to IP

# Port filtering
tcp.port == 8080                             # Traffic on port 8080
tcp.srcport == 8080 || tcp.dstport == 8080   # Explicit source/destination
```

## 7. Socket Programming Fundamentals

### TCP Server Pattern

```python
# 1. Create socket
server = socket.socket(AF_INET, SOCK_STREAM)

# 2. Bind to address
server.bind(("0.0.0.0", 8080))

# 3. Listen for connections
server.listen(5)

# 4. Accept connections
while True:
    client, address = server.accept()
    # Handle client in new thread/process
    handle_client(client)
```

### TCP Client Pattern

```python
# 1. Create socket
client = socket.socket(AF_INET, SOCK_STREAM)

# 2. Connect to server
client.connect(("server_ip", 8080))

# 3. Send/receive data
client.send(b"Hello")
response = client.recv(1024)

# 4. Close connection
client.close()
```

## 8. Docker Networking

### Network Types

| Type | Description | Use Case |
|------|-------------|----------|
| bridge | Default isolated network | Container-to-container communication |
| host | Shares host network namespace | Performance-critical applications |
| none | No networking | Isolated processing |
| overlay | Multi-host networking | Docker Swarm clusters |

### Service Discovery

Within a Docker network, containers can reach each other by:
1. **Container name:** `curl http://app1:8080/`
2. **Service name:** `curl http://backend:8080/` (Compose)
3. **IP address:** `curl http://172.20.0.2:8080/`

## References

- Kurose, J. & Ross, K. (2021). *Computer Networking: A Top-Down Approach* (8th ed.). Pearson.
- Stevens, W. R. (1994). *TCP/IP Illustrated, Volume 1: The Protocols*. Addison-Wesley.
- RFC 793: Transmission Control Protocol (TCP)
- RFC 7230-7235: HTTP/1.1 Specification

---

*NETWORKING class - ASE, Informatics | by Revolvix*
