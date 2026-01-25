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
  |<----- SYN-ACK (seq=y, ack=x+1)|
  |                                |
  |-------- ACK (ack=y+1) ------->|
  |                                |
  |     Connection Established     |
```

### Four-Way Termination

Connection termination uses FIN and ACK:

```
Client                          Server
  |                                |
  |-------- FIN (seq=u) --------->|
  |                                |
  |<-------- ACK (ack=u+1) -------|
  |                                |
  |<-------- FIN (seq=v) ---------|
  |                                |
  |-------- ACK (ack=v+1) ------->|
  |                                |
  |     Connection Terminated      |
```

## 3. HTTP Protocol Fundamentals

### Request Structure

```
GET /path HTTP/1.1
Host: example.com
User-Agent: curl/7.68.0
Accept: */*

[optional body]
```

### Response Structure

```
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 1234

[response body]
```

### Common Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful request |
| 301 | Moved Permanently | Resource relocated |
| 400 | Bad Request | Malformed request |
| 404 | Not Found | Resource does not exist |
| 500 | Internal Server Error | Server-side failure |
| 502 | Bad Gateway | Upstream server error |
| 503 | Service Unavailable | Server overloaded |

## 4. Load Balancing Concepts

### Round-Robin Algorithm

Requests are distributed sequentially across backends:

```
Request 1 → Backend A
Request 2 → Backend B
Request 3 → Backend A
Request 4 → Backend B
...
```

This is deterministic, not random. Given N backends, request K goes to backend (K mod N).

### Weighted Round-Robin

Backends receive requests proportional to their weights:

```
Weights: A=3, B=1
Sequence: A, A, A, B, A, A, A, B, ...
```

### Health Checks

Load balancers periodically verify backend health:

- **Active:** LB sends probe requests
- **Passive:** LB monitors response codes

## 5. Docker Networking

### Network Types

| Type | Description | Use Case |
|------|-------------|----------|
| bridge | Default isolated network | Container-to-container |
| host | Share host network stack | Performance-critical |
| none | No networking | Security isolation |
| overlay | Multi-host networking | Docker Swarm |

### Port Mapping

```
-p HOST_PORT:CONTAINER_PORT
```

Example: `-p 8080:80` maps host port 8080 to container port 80.

### Container DNS

Docker provides automatic DNS resolution within user-defined networks:

1. **Container name:** `curl http://app1:8080/`
2. **Service name:** `curl http://backend:8080/` (Compose)
3. **IP address:** `curl http://172.20.0.2:8080/`

## 6. Wireshark Filters

### Capture Filters (BPF)

Applied during capture to reduce file size:

```
port 8080
host 192.168.1.1
tcp port 80
```

### Display Filters

Applied after capture for analysis:

```
http.request.method == "GET"
tcp.flags.syn == 1
ip.addr == 172.20.0.2
tcp.stream eq 0
```

## 7. Troubleshooting Methodology

### Systematic Approach

1. **Identify symptoms:** What exactly is failing?
2. **Isolate layer:** Network, transport or application?
3. **Test components:** Verify each service independently
4. **Check logs:** Container and application logs
5. **Capture traffic:** Use Wireshark for deep analysis

### Common Issues

| Symptom | Likely Cause | Verification |
|---------|--------------|--------------|
| Connection refused | Service not running | `docker ps` |
| Connection timeout | Firewall or routing | `ping`, `traceroute` |
| 502 Bad Gateway | Backend down | Check backend logs |
| 503 Service Unavailable | All backends down | Check all containers |

## References

- Kurose, J. & Ross, K. (2021). *Computer Networking: A Top-Down Approach* (8th ed.). Pearson.
- Stevens, W. R. (1994). *TCP/IP Illustrated, Volume 1: The Protocols*. Addison-Wesley.
- RFC 793: Transmission Control Protocol (TCP)
- RFC 7230-7235: HTTP/1.1 Specification

---

*NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim*

*Document version: 2.0 | Week 14: Integrated Recap | January 2025*
