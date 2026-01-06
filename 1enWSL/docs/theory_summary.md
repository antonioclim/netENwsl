# Theoretical Summary: Network Fundamentals

> NETWORKING class - ASE, Informatics | by Revolvix

## Introduction to Computer Networks

A computer network is an interconnected collection of autonomous computing devices that exchange data using a shared communication medium. Networks enable resource sharing, distributed processing and communication services that form the foundation of modern digital infrastructure.

## Network Classification

### By Geographic Scope

**Personal Area Network (PAN)**
- Range: ~10 metres
- Examples: Bluetooth devices, USB connections
- Typical use: Connecting peripherals to a computer

**Local Area Network (LAN)**
- Range: Building or campus
- Technology: Ethernet (IEEE 802.3), Wi-Fi (IEEE 802.11)
- Typical use: Office networks, home networks

**Metropolitan Area Network (MAN)**
- Range: City or metropolitan area
- Technology: FDDI, DQDB, Metro Ethernet
- Typical use: Connecting multiple LANs within a city

**Wide Area Network (WAN)**
- Range: Countries, continents
- Technology: MPLS, leased lines, satellite
- Typical use: Internet backbone, corporate networks

### By Topology

| Topology | Advantages | Disadvantages |
|----------|------------|---------------|
| Bus | Simple, inexpensive | Single point of failure |
| Star | Easy to manage, isolate faults | Central hub is critical |
| Ring | Equal access, predictable | Difficult to expand |
| Mesh | Redundant, reliable | Complex, expensive |

## The TCP/IP Model

The Internet Protocol Suite (TCP/IP) is the foundational protocol stack for the Internet and most modern networks.

### Layer Architecture

```
┌─────────────────────────────────────┐
│        Application Layer            │  HTTP, FTP, DNS, SMTP
├─────────────────────────────────────┤
│         Transport Layer             │  TCP, UDP
├─────────────────────────────────────┤
│          Network Layer              │  IP, ICMP, ARP
├─────────────────────────────────────┤
│      Network Interface Layer        │  Ethernet, Wi-Fi
└─────────────────────────────────────┘
```

### Layer Functions

**Application Layer**
- Provides network services directly to applications
- Handles high-level protocols for data representation
- Examples: HTTP (web), SMTP (email), FTP (file transfer)

**Transport Layer**
- End-to-end communication between processes
- Segmentation and reassembly of data
- Flow control and error recovery (TCP)
- Examples: TCP (reliable), UDP (fast)

**Network Layer**
- Logical addressing (IP addresses)
- Routing packets across networks
- Fragmentation and reassembly
- Examples: IPv4, IPv6, ICMP

**Network Interface Layer**
- Physical transmission of bits
- MAC addressing
- Media access control
- Examples: Ethernet, Wi-Fi, PPP

## IP Addressing

### IPv4 Address Structure

An IPv4 address is a 32-bit number, typically written in dotted-decimal notation.

```
192.168.1.100
│   │   │ │
│   │   │ └── Host portion
│   │   └──── Network portion (depends on subnet mask)
│   └──────── 
└──────────── 
```

### CIDR Notation

Classless Inter-Domain Routing (CIDR) notation combines the IP address with the subnet mask.

| CIDR | Subnet Mask | Hosts |
|------|-------------|-------|
| /8 | 255.0.0.0 | 16,777,214 |
| /16 | 255.255.0.0 | 65,534 |
| /24 | 255.255.255.0 | 254 |
| /30 | 255.255.255.252 | 2 |

### Private Address Ranges (RFC 1918)

| Class | Range | CIDR |
|-------|-------|------|
| A | 10.0.0.0 - 10.255.255.255 | 10.0.0.0/8 |
| B | 172.16.0.0 - 172.31.255.255 | 172.16.0.0/12 |
| C | 192.168.0.0 - 192.168.255.255 | 192.168.0.0/16 |

## Transport Protocols

### TCP (Transmission Control Protocol)

**Characteristics:**
- Connection-oriented (three-way handshake)
- Reliable delivery (acknowledgements, retransmission)
- Ordered data transfer (sequence numbers)
- Flow control (sliding window)
- Congestion control

**Three-Way Handshake:**
```
Client                    Server
   │                         │
   │   ──── SYN ────>        │  Step 1: Client initiates
   │                         │
   │   <─── SYN-ACK ───      │  Step 2: Server responds
   │                         │
   │   ──── ACK ────>        │  Step 3: Client confirms
   │                         │
   │    Connection Open      │
```

**Use Cases:** HTTP, FTP, SSH, SMTP (where reliability matters)

### UDP (User Datagram Protocol)

**Characteristics:**
- Connectionless (no handshake)
- Unreliable (no acknowledgements)
- Unordered (no sequence numbers)
- Low overhead
- Fast

**Use Cases:** DNS, VoIP, video streaming, online gaming (where speed matters)

### TCP vs UDP Comparison

| Aspect | TCP | UDP |
|--------|-----|-----|
| Connection | Required | None |
| Reliability | Guaranteed | Best effort |
| Ordering | Preserved | Not guaranteed |
| Header size | 20+ bytes | 8 bytes |
| Speed | Slower | Faster |

## Socket Programming Concepts

A socket is an endpoint for network communication, identified by:
- IP address
- Port number
- Protocol (TCP/UDP)

### Socket States (TCP)

```
CLOSED ─────────────────────────────────────────────┐
   │                                                │
   ▼ (bind, listen)                                 │
LISTEN                                              │
   │                                                │
   ▼ (accept)                                       │
SYN_RECEIVED                                        │
   │                                                │
   ▼                                                │
ESTABLISHED ◄─────────────────────────────────┐     │
   │                                          │     │
   ▼ (close)                                  │     │
FIN_WAIT_1                                    │     │
   │                                          │     │
   ▼                                          │     │
FIN_WAIT_2                                    │     │
   │                                          │     │
   ▼                                          │     │
TIME_WAIT ────────────────────────────────────┴─────┘
```

### Well-Known Ports

| Port | Protocol | Service |
|------|----------|---------|
| 20-21 | TCP | FTP |
| 22 | TCP | SSH |
| 23 | TCP | Telnet |
| 25 | TCP | SMTP |
| 53 | TCP/UDP | DNS |
| 80 | TCP | HTTP |
| 443 | TCP | HTTPS |

## Essential Linux Commands

### Interface Management

```bash
ip addr show          # Display all interfaces
ip link set eth0 up   # Enable interface
ip addr add 10.0.0.1/24 dev eth0  # Assign IP
```

### Routing

```bash
ip route show         # Display routing table
ip route add default via 192.168.1.1  # Add default route
```

### Socket Inspection

```bash
ss -tlnp              # TCP listening sockets
ss -tunap             # All sockets with processes
netstat -an           # Legacy alternative
```

### Connectivity Testing

```bash
ping -c 4 8.8.8.8     # ICMP echo test
traceroute google.com # Path discovery
```

## References

1. Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (7th ed.). Pearson.
2. Tanenbaum, A. S. & Wetherall, D. J. (2011). *Computer Networks* (5th ed.). Pearson.
3. Stevens, W. R. (1994). *TCP/IP Illustrated, Volume 1: The Protocols*. Addison-Wesley.
4. RFC 791 - Internet Protocol (IPv4)
5. RFC 793 - Transmission Control Protocol (TCP)
6. RFC 768 - User Datagram Protocol (UDP)

---

*NETWORKING class - ASE, Informatics | by Revolvix*
