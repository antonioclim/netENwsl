# 📖 Glossary — Week 1: Network Fundamentals
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## Core Networking Terms

| Term | Definition | Example |
|------|------------|---------|
| **Bandwidth** | Maximum data transfer rate of a network link | 100 Mbps Ethernet |
| **Latency** | Time delay for data to travel from source to destination | 12ms ping time |
| **RTT (Round-Trip Time)** | Time for a packet to go to destination and back | `ping` reports RTT |
| **Packet** | Unit of data transmitted over a network | TCP segment, UDP datagram |
| **Protocol** | Set of rules governing data communication | TCP, UDP, ICMP, HTTP |
| **Port** | Logical endpoint for network communication (0-65535) | Port 80 (HTTP), 443 (HTTPS) |
| **Socket** | Combination of IP address + port + protocol | `192.168.1.10:8080/TCP` |
| **Interface** | Network connection point (physical or virtual) | `eth0`, `lo`, `wlan0` |
| **Loopback** | Virtual interface for local communication | `127.0.0.1`, `lo` |
| **Gateway** | Device that routes traffic between networks | Your router at home |
| **Subnet** | Logical division of an IP network | `192.168.1.0/24` |
| **CIDR** | Notation for IP addresses and subnet masks | `/24` = 255.255.255.0 |

---

## TCP/IP Terms

| Term | Definition | Example |
|------|------------|---------|
| **TCP** | Connection-oriented, reliable transport protocol | Web browsing, email |
| **UDP** | Connectionless, fast transport protocol | DNS, streaming, gaming |
| **ICMP** | Protocol for network diagnostics and errors | `ping`, `traceroute` |
| **IP Address** | Unique identifier for a device on a network | `192.168.1.100` |
| **MAC Address** | Hardware address of network interface | `00:1A:2B:3C:4D:5E` |
| **Three-way Handshake** | TCP connection establishment: SYN→SYN-ACK→ACK | Every TCP connection start |
| **SYN** | Synchronise flag — initiates TCP connection | First handshake packet |
| **ACK** | Acknowledgement flag — confirms receipt | Response packets |
| **FIN** | Finish flag — closes TCP connection | Connection termination |

---

## Socket States

| State | Meaning | When It Occurs |
|-------|---------|----------------|
| **CLOSED** | No connection exists | Initial/final state |
| **LISTEN** | Server waiting for connections | After `bind()` and `listen()` |
| **SYN_SENT** | Client sent SYN, waiting for response | During connection attempt |
| **SYN_RECEIVED** | Server received SYN, sent SYN-ACK | During handshake |
| **ESTABLISHED** | Connection active, data can flow | Normal operation |
| **FIN_WAIT_1** | Sent FIN, waiting for ACK | Initiating close |
| **FIN_WAIT_2** | Received ACK for FIN, waiting for peer's FIN | Closing |
| **TIME_WAIT** | Waiting for delayed packets to expire | After close (2×MSL) |
| **CLOSE_WAIT** | Received FIN, waiting for application to close | Peer initiated close |
| **LAST_ACK** | Sent FIN, waiting for final ACK | Final closing step |

---

## Docker Terms

| Term | Definition | Example |
|------|------------|---------|
| **Container** | Lightweight, isolated runtime environment | `week1_lab` |
| **Image** | Read-only template for creating containers | `ubuntu:22.04` |
| **Volume** | Persistent storage for container data | `-v /host:/container` |
| **Network** | Virtual network connecting containers | `week1_network` |
| **Bridge** | Default Docker network driver | Containers on same host |
| **Port Mapping** | Connecting host port to container port | `-p 8080:80` |
| **Compose** | Tool for defining multi-container apps | `docker-compose.yml` |
| **Dockerfile** | Script to build Docker images | `FROM`, `RUN`, `COPY` |

---

## WSL Terms

| Term | Definition | Example |
|------|------------|---------|
| **WSL** | Windows Subsystem for Linux | Running Ubuntu on Windows |
| **WSL2** | WSL with full Linux kernel | Better Docker support |
| **Distro** | Linux distribution in WSL | Ubuntu-22.04 |
| **vEthernet** | Virtual network adapter for WSL | Capture in Wireshark |
| **/mnt/c/** | Windows C: drive mounted in WSL | Access Windows files |

---

## Commands Reference

### Network Inspection

| Command | Purpose | Example |
|---------|---------|---------|
| `ip addr` | Show IP addresses and interfaces | `ip addr show eth0` |
| `ip route` | Show routing table | `ip route show` |
| `ip link` | Show/modify network interfaces | `ip link set eth0 up` |
| `ss` | Show socket statistics | `ss -tlnp` |
| `netstat` | Legacy socket statistics (deprecated) | `netstat -an` |

### Connectivity Testing

| Command | Purpose | Example |
|---------|---------|---------|
| `ping` | Test connectivity with ICMP | `ping -c 4 8.8.8.8` |
| `traceroute` | Show path to destination | `traceroute google.com` |
| `nc` (netcat) | TCP/UDP networking utility | `nc -l -p 9090` |
| `curl` | HTTP client | `curl http://localhost:9000` |
| `wget` | Download files | `wget http://example.com/file` |

### Packet Capture

| Command | Purpose | Example |
|---------|---------|---------|
| `tcpdump` | Capture packets (CLI) | `tcpdump -i eth0 port 80` |
| `tshark` | Wireshark CLI version | `tshark -r capture.pcap` |

### Docker Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `docker ps` | List running containers | `docker ps -a` (all) |
| `docker exec` | Run command in container | `docker exec -it lab bash` |
| `docker logs` | View container logs | `docker logs week1_lab` |
| `docker compose up` | Start services from compose file | `docker compose up -d` |
| `docker compose down` | Stop and remove services | `docker compose down` |

---

## Command Flags Explained

### ss flags

| Flag | Meaning |
|------|---------|
| `-t` | TCP sockets only |
| `-u` | UDP sockets only |
| `-l` | Listening sockets only |
| `-n` | Numeric output (no DNS resolution) |
| `-p` | Show process using socket |
| `-a` | All sockets (listening + non-listening) |

**Common combinations:**
- `ss -tlnp` — TCP listening sockets with processes
- `ss -tunap` — All TCP/UDP sockets with processes

### ping flags

| Flag | Meaning |
|------|---------|
| `-c N` | Send N packets then stop |
| `-i N` | Wait N seconds between packets |
| `-W N` | Timeout after N seconds |
| `-n` | Numeric output only |

### tcpdump flags

| Flag | Meaning |
|------|---------|
| `-i IFACE` | Capture on interface |
| `-w FILE` | Write to pcap file |
| `-r FILE` | Read from pcap file |
| `-n` | Don't resolve hostnames |
| `-c N` | Capture N packets then stop |
| `port N` | Filter by port number |
| `host IP` | Filter by IP address |

---

## Acronyms

| Acronym | Full Form | Context |
|---------|-----------|---------|
| TCP | Transmission Control Protocol | Reliable transport |
| UDP | User Datagram Protocol | Fast transport |
| IP | Internet Protocol | Network layer addressing |
| ICMP | Internet Control Message Protocol | Diagnostics (ping) |
| ARP | Address Resolution Protocol | IP → MAC mapping |
| DNS | Domain Name System | Name → IP resolution |
| HTTP | HyperText Transfer Protocol | Web communication |
| HTTPS | HTTP Secure | Encrypted web |
| SSH | Secure Shell | Remote access |
| FTP | File Transfer Protocol | File transfer |
| NIC | Network Interface Card | Physical network hardware |
| MAC | Media Access Control | Hardware address |
| LAN | Local Area Network | Local network |
| WAN | Wide Area Network | Internet-scale network |
| NAT | Network Address Translation | IP address sharing |
| DHCP | Dynamic Host Configuration Protocol | Automatic IP assignment |
| MTU | Maximum Transmission Unit | Largest packet size |
| TTL | Time To Live | Packet hop limit |
| RTT | Round-Trip Time | Latency measurement |
| MSS | Maximum Segment Size | TCP payload limit |

---

## Relationships Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           NETWORK STACK                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  APPLICATION    ┌─────────┐  ┌─────────┐  ┌─────────┐                      │
│  LAYER          │  HTTP   │  │   DNS   │  │   SSH   │  ... (uses ports)    │
│                 └────┬────┘  └────┬────┘  └────┬────┘                      │
│                      │            │            │                            │
│  ────────────────────┴────────────┴────────────┴────────────────────────── │
│                                                                              │
│  TRANSPORT      ┌─────────────────────┐  ┌─────────────────────┐           │
│  LAYER          │        TCP          │  │        UDP          │           │
│                 │ (reliable, ordered) │  │ (fast, unordered)   │           │
│                 └──────────┬──────────┘  └──────────┬──────────┘           │
│                            │                        │                       │
│  ──────────────────────────┴────────────────────────┴────────────────────── │
│                                                                              │
│  NETWORK        ┌─────────────────────────────────────────────┐             │
│  LAYER          │                    IP                        │             │
│                 │         (addressing, routing)                │             │
│                 └──────────────────────┬──────────────────────┘             │
│                                        │                                     │
│  ──────────────────────────────────────┴──────────────────────────────────── │
│                                                                              │
│  LINK           ┌─────────────────────────────────────────────┐             │
│  LAYER          │              Ethernet / Wi-Fi                │             │
│                 │           (MAC addresses, frames)            │             │
│                 └─────────────────────────────────────────────┘             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

PORT NUMBERS (0-65535):
┌──────────────┬────────────────────────────────────────────────────────────┐
│  0 - 1023    │  Well-known ports (require root): HTTP(80), SSH(22), etc. │
├──────────────┼────────────────────────────────────────────────────────────┤
│ 1024 - 49151 │  Registered ports: MySQL(3306), PostgreSQL(5432), etc.    │
├──────────────┼────────────────────────────────────────────────────────────┤
│ 49152 - 65535│  Dynamic/ephemeral ports (client-side)                    │
└──────────────┴────────────────────────────────────────────────────────────┘
```

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  WEEK 1 QUICK REFERENCE                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  CHECK NETWORK CONFIG          TEST CONNECTIVITY                            │
│  ──────────────────           ──────────────────                            │
│  ip addr show                  ping -c 4 HOST                               │
│  ip route show                 traceroute HOST                              │
│  ss -tlnp                      nc -l -p PORT (server)                       │
│                                nc HOST PORT (client)                        │
│                                                                              │
│  DOCKER COMMANDS               CAPTURE TRAFFIC                              │
│  ────────────────              ───────────────                              │
│  docker ps -a                  tcpdump -i IFACE -w FILE                     │
│  docker exec -it NAME bash     tshark -r FILE                               │
│  docker compose up -d                                                       │
│  docker compose down                                                        │
│                                                                              │
│  KEY PORTS THIS WEEK           CREDENTIALS                                  │
│  ───────────────────           ───────────                                  │
│  9000 - Portainer (RESERVED)   WSL: stud / stud                            │
│  9090 - TCP test               Portainer: stud / studstudstud              │
│  9091 - UDP test                                                            │
│  9092 - Alternative                                                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Cross-References

Use this section to understand how concepts relate to each other.

### Socket → Related Concepts

| Term | Relationship | See Also |
|------|--------------|----------|
| **Port** | Socket includes port number | Ports section above |
| **TCP/UDP** | Socket specifies protocol | TCP/IP Terms section |
| **IP Address** | Socket includes IP | Core Networking Terms |
| **LISTEN state** | Server socket waiting | Socket States section |
| **ESTABLISHED** | Active socket connection | Socket States section |

### Container → Related Concepts

| Term | Relationship | See Also |
|------|--------------|----------|
| **Image** | Container created from image | Docker Terms section |
| **Volume** | Persistent storage for container | Docker Terms section |
| **Network** | Container communication | Docker Terms section |
| **Port Mapping** | Container external access | Docker Terms section |

### Capture → Related Concepts

| Term | Relationship | See Also |
|------|--------------|----------|
| **tcpdump** | CLI packet capture | Commands Reference |
| **Wireshark** | GUI packet capture | README.md §Wireshark |
| **PCAP** | Capture file format | Acronyms section |
| **tshark** | Wireshark CLI | Commands Reference |

### Common Confusion Pairs

| Often Confused | Key Difference |
|----------------|----------------|
| Latency vs Bandwidth | Time vs Volume per second |
| TCP vs UDP | Reliable vs Fast |
| Image vs Container | Template vs Running instance |
| Port vs Socket | Number vs Full endpoint (IP+Port+Protocol) |
| LISTEN vs ESTABLISHED | Waiting vs Active |
| localhost vs 127.0.0.1 | Same (hostname vs IP) |

---

*NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim*
*Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment*
