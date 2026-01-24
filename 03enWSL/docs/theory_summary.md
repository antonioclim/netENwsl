# Theory Summary: Network Programming Fundamentals

> NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

## Overview

This document provides a condensed theoretical framework for Week 3 laboratory concepts, covering the essential principles of broadcast, multicast and tunnelling mechanisms within the TCP/IP protocol suite.

---

## 1. Communication Approaches

### Unicast Transmission

Unicast represents the fundamental one-to-one communication model where a single source transmits data to a single destination. The network layer routes packets through intermediate nodes using destination IP addresses, with each packet independently addressed. This approach dominates conventional client-server architectures and constitutes the baseline for understanding more sophisticated transmission modes.

**Characteristics:**
- Point-to-point addressing (single source → single destination)
- Full TCP reliability available (acknowledgements, retransmission, flow control)
- Scalability challenges when distributing identical content to multiple receivers
- Network bandwidth consumption proportional to receiver count

### Broadcast Transmission

Broadcasting enables a single source to transmit data to all hosts within a defined network segment simultaneously. The network layer interprets specific destination addresses as broadcast indicators, prompting switches to flood frames to all ports (except the source) and hosts to process the incoming data regardless of application interest.

**IPv4 Broadcast Addresses:**
- **Limited broadcast** (`255.255.255.255`): Never forwarded by routers; confined to local segment
- **Directed broadcast** (e.g., `192.168.1.255` for /24 subnet): Targets specific subnet; router forwarding behaviour configurable

**Socket Programming Implications:**
```python
# Enable broadcast capability on socket
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
```

The `SO_BROADCAST` option must be explicitly enabled, serving as an intentional safeguard against accidental broadcast transmission.

**Limitations:**
- Layer 2 flooding consumes bandwidth on all network segments
- All hosts must process broadcast frames at NIC level (CPU overhead)
- Routers typically block broadcasts at subnet boundaries (broadcast storm prevention)
- No receiver selectivity—all hosts receive regardless of interest

### Multicast Transmission

Multicasting provides an elegant middle ground between unicast inefficiency and broadcast indiscrimination. A single source transmits to a group address and only hosts that have expressed interest (through IGMP group membership) receive and process the data. Network infrastructure (switches, routers) optimises delivery paths to avoid unnecessary duplication.

**IPv4 Multicast Address Range:**
- Class D addresses: `224.0.0.0` to `239.255.255.255`
- Well-known groups: `224.0.0.0/24` (link-local, not forwarded)
- Administratively scoped: `239.0.0.0/8` (organisation-local)
- Source-specific multicast (SSM): `232.0.0.0/8`

**Group Membership Protocol (IGMP):**
- **IGMPv1** (RFC 1112): Basic join/leave with querier election
- **IGMPv2** (RFC 2236): Explicit leave messages, reduced leave latency
- **IGMPv3** (RFC 3376): Source filtering (include/exclude source lists)

**Socket Programming for Multicast:**
```python
# Join multicast group
mreq = struct.pack("4sl", socket.inet_aton("239.1.1.1"), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Set outgoing interface (optional)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, 
                socket.inet_aton("192.168.1.100"))

# Configure TTL for multicast scope control
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
```

---

## 2. Socket Options Reference

### SOL_SOCKET Level Options

| Option | Purpose | Type |
|--------|---------|------|
| `SO_BROADCAST` | Enable broadcast transmission | Boolean |
| `SO_REUSEADDR` | Allow address reuse (multiple listeners) | Boolean |
| `SO_REUSEPORT` | Load balance across multiple processes | Boolean |
| `SO_RCVBUF` | Receive buffer size | Integer |
| `SO_SNDBUF` | Send buffer size | Integer |
| `SO_KEEPALIVE` | Enable TCP keep-alive probes | Boolean |
| `SO_LINGER` | Control close() behaviour | struct |

### IPPROTO_IP Level Options (Multicast)

| Option | Purpose |
|--------|---------|
| `IP_ADD_MEMBERSHIP` | Join multicast group |
| `IP_DROP_MEMBERSHIP` | Leave multicast group |
| `IP_MULTICAST_IF` | Set outgoing interface for multicast |
| `IP_MULTICAST_TTL` | Set TTL for multicast packets |
| `IP_MULTICAST_LOOP` | Enable/disable local loopback |

---

## 3. TCP Tunnelling Concepts

### Definition and Purpose

A TCP tunnel encapsulates application traffic within a TCP connection, providing a transport mechanism through network boundaries (firewalls, NAT devices) or enabling protocol transformation. The tunnel endpoint accepts connections and forwards traffic bidirectionally to a destination service.

### Architecture Pattern

```
[Client] ──TCP──► [Tunnel Entry] ══tunnel══► [Tunnel Exit] ──TCP──► [Server]
```

**Key Characteristics:**
- Bidirectional data flow through persistent connection
- Transparent to client application (same TCP interface)
- Additional latency from double TCP processing
- Potential TCP-over-TCP performance issues (congestion control interaction)

### Implementation Considerations

**Threading Model:**
- Concurrent handling of multiple client connections
- Separate threads for each direction (client→server, server→client)
- Proper synchronisation for shared resources

**Connection Lifecycle:**
1. Accept incoming client connection
2. Establish outbound connection to target server
3. Create forwarding threads for both directions
4. Handle graceful termination when either side closes
5. Clean up resources (sockets, threads)

**Buffering Strategy:**
- Non-blocking I/O with select/poll for efficiency
- Fixed-size buffers for predictable memory usage
- Handling partial reads/writes

---

## 4. Protocol Analysis Fundamentals

### Wireshark Display Filters

**Broadcast Analysis:**
```
eth.dst == ff:ff:ff:ff:ff:ff
ip.dst == 255.255.255.255
udp.port == 5007
```

**Multicast Analysis:**
```
ip.dst >= 224.0.0.0 and ip.dst <= 239.255.255.255
igmp
udp.port == 5008
```

**TCP Tunnel Analysis:**
```
tcp.port == 9090
tcp.port == 8080
tcp.flags.syn == 1
tcp.analysis.retransmission
```

### tcpdump Equivalents

```bash
# Capture broadcast traffic
tcpdump -i eth0 'broadcast or dst 255.255.255.255'

# Capture multicast traffic
tcpdump -i eth0 'multicast'

# Capture TCP tunnel traffic
tcpdump -i eth0 'port 9090 or port 8080'

# Save to file for Wireshark analysis
tcpdump -i eth0 -w capture.pcap 'port 9090'
```

---

## 5. Performance Considerations

### Broadcast Efficiency

Broadcast efficiency degrades linearly with network size. For N hosts on a segment, each broadcast consumes bandwidth proportional to N and requires processing by all N hosts.

**Equation:** `Total bandwidth = Message size × Switch ports`

### Multicast Efficiency

Multicast achieves sender efficiency independent of receiver count. Network infrastructure handles replication at best points (closest to receivers).

**Comparison:**
- Unicast to 100 receivers: 100× bandwidth at source
- Multicast to 100 receivers: 1× bandwidth at source

### Tunnel Overhead

TCP tunnelling introduces:
- Header overhead (additional TCP/IP headers)
- Processing latency (user-space forwarding)
- Buffer copying (kernel ↔ user space transitions)
- Potential congestion control interaction effects

---

## 6. Security Implications

### Broadcast Vulnerabilities
- No access control—all hosts receive data
- Amplification attacks possible (smurf attack with ICMP)
- Information disclosure to any listener on segment

### Multicast Vulnerabilities
- Group membership spoofing possible
- No built-in authentication or encryption
- Requires IPsec or application-layer security

### Tunnel Security
- Encrypts underlying traffic if using SSL/TLS tunnel
- Can bypass security controls (firewall traversal)
- Man-in-the-middle risk at tunnel endpoints

---

## References

1. RFC 791: Internet Protocol (IP)
2. RFC 1112: Host Extensions for IP Multicasting (IGMPv1)
3. RFC 2236: Internet Group Management Protocol, Version 2
4. RFC 3376: Internet Group Management Protocol, Version 3
5. Stevens, W. R. (1994). *TCP/IP Illustrated, Volume 1*. Addison-Wesley.
6. Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (7th ed.). Pearson.

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
