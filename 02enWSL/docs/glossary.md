# 📖 Glossary — Week 2: Architectural Models and Socket Programming

> NETWORKING class — ASE, CSIE Bucharest  
> Computer Networks Laboratory | by ing. dr. Antonio Clim

---

## Core Socket Terms

| Term | Definition | Example |
|------|------------|---------|
| **Socket** | An endpoint for network communication; combines IP address and port number | `sock = socket.socket(AF_INET, SOCK_STREAM)` |
| **File descriptor** | Integer handle the OS uses to track open sockets/files | Socket fd might be 3, 4, 5... |
| **Address family** | Protocol family for the socket (IPv4, IPv6, Unix) | `AF_INET` (IPv4), `AF_INET6` (IPv6) |
| **Socket type** | Communication semantics (stream vs datagram) | `SOCK_STREAM` (TCP), `SOCK_DGRAM` (UDP) |
| **Backlog** | Queue size for pending connections on a listening socket | `sock.listen(32)` — up to 32 waiting |

---

## Socket Operations

| Operation | Purpose | TCP | UDP |
|-----------|---------|-----|-----|
| **bind()** | Assign local address (IP:port) to socket | Required for server | Optional |
| **listen()** | Mark socket as passive (accepting connections) | Required for server | N/A |
| **accept()** | Extract first connection from queue, create new socket | Returns (conn, addr) | N/A |
| **connect()** | Initiate connection to remote address | Triggers handshake | Sets default destination |
| **send()** / **sendall()** | Transmit data on connected socket | Byte stream | N/A (use sendto) |
| **recv()** | Receive data from connected socket | Returns bytes | N/A (use recvfrom) |
| **sendto()** | Send datagram to specific address | Unusual | Standard method |
| **recvfrom()** | Receive datagram and sender address | Unusual | Returns (data, addr) |
| **close()** | Release socket resources | Triggers FIN | Immediate |
| **shutdown()** | Disable send/receive on socket | SHUT_RD, SHUT_WR, SHUT_RDWR | Same |

---

## Protocol Terms

| Term | Definition | Context |
|------|------------|---------|
| **Segment** | TCP Protocol Data Unit (PDU) at Transport Layer | TCP header + data |
| **Datagram** | UDP Protocol Data Unit; also IP-level PDU | UDP header + data; self-contained |
| **Packet** | Network Layer PDU | IP header + segment/datagram |
| **Frame** | Data Link Layer PDU | Ethernet header + packet + trailer |
| **Three-way handshake** | TCP connection establishment: SYN → SYN-ACK → ACK | `connect()` triggers this |
| **Four-way termination** | TCP connection close: FIN → ACK → FIN → ACK | `close()` triggers this |
| **ACK** | Acknowledgement; confirms receipt of data | TCP reliability mechanism |
| **SYN** | Synchronise; initiates connection | First handshake packet |
| **FIN** | Finish; initiates connection termination | Graceful close |
| **RST** | Reset; aborts connection immediately | Error or rejection |

---

## Addressing Terms

| Term | Definition | Example |
|------|------------|---------|
| **Port** | 16-bit number identifying application endpoint | 80 (HTTP), 443 (HTTPS), 9090 (our lab) |
| **Well-known ports** | 0–1023; reserved for standard services | 22 (SSH), 53 (DNS), 80 (HTTP) |
| **Registered ports** | 1024–49151; for applications | 3306 (MySQL), 5432 (PostgreSQL) |
| **Ephemeral ports** | 49152–65535; assigned dynamically to clients | OS picks automatically |
| **Loopback** | Address for same-machine communication | 127.0.0.1 (IPv4), ::1 (IPv6) |
| **Wildcard address** | Accept on all interfaces | 0.0.0.0 (IPv4), :: (IPv6) |

---

## Concurrency Terms

| Term | Definition | Example |
|------|------------|---------|
| **Thread** | Lightweight execution unit within a process | `threading.Thread(target=handler)` |
| **Daemon thread** | Thread that exits when main programme exits | `thread.daemon = True` |
| **Blocking call** | Function that waits until operation completes | `accept()`, `recv()` without timeout |
| **Non-blocking** | Function returns immediately, may need retry | `sock.setblocking(False)` |
| **Timeout** | Maximum wait time before giving up | `sock.settimeout(5.0)` |
| **Race condition** | Bug from unsynchronised concurrent access | Two threads modifying same variable |
| **Iterative server** | Handles one client at a time, sequentially | Simple but creates bottleneck |
| **Concurrent server** | Handles multiple clients simultaneously | Threading, forking, or async |

---

## Architectural Model Terms

| Term | Definition | Layer(s) |
|------|------------|----------|
| **OSI Model** | 7-layer theoretical reference model by ISO | Physical → Application |
| **TCP/IP Model** | 4-layer practical model powering the Internet | Network Access → Application |
| **PDU** | Protocol Data Unit; data + headers at each layer | Segment, packet, frame |
| **Encapsulation** | Adding headers as data descends the stack | App data → segment → packet → frame |
| **Decapsulation** | Removing headers as data ascends the stack | Frame → packet → segment → App data |
| **SAP** | Service Access Point; interface between layers | Port numbers are Transport SAPs |

---

## Commands Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `netcat` / `nc` | Swiss-army knife for TCP/UDP testing | `nc -v localhost 9090` |
| `ss` | Socket statistics (modern netstat) | `ss -tlnp` (TCP listening) |
| `lsof` | List open files including sockets | `lsof -i :9090` |
| `tcpdump` | Command-line packet capture | `tcpdump -i lo port 9090` |
| `tshark` | Wireshark CLI for scripted analysis | `tshark -i lo -Y "tcp.port==9090"` |
| `nmap` | Network scanner and port checker | `nmap -p 9090 localhost` |

---

## Python Socket Constants

| Constant | Value | Meaning |
|----------|-------|---------|
| `AF_INET` | 2 | IPv4 address family |
| `AF_INET6` | 10 | IPv6 address family |
| `SOCK_STREAM` | 1 | TCP (reliable stream) |
| `SOCK_DGRAM` | 2 | UDP (unreliable datagram) |
| `SOL_SOCKET` | 1 | Socket-level options |
| `SO_REUSEADDR` | 2 | Allow rebind to TIME_WAIT port |
| `SHUT_RD` | 0 | Shutdown reading |
| `SHUT_WR` | 1 | Shutdown writing |
| `SHUT_RDWR` | 2 | Shutdown both |

---

## Relationships Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        APPLICATION                                   │
│                    (your Python code)                               │
└───────────────────────────┬─────────────────────────────────────────┘
                            │ socket API (send, recv, etc.)
┌───────────────────────────▼─────────────────────────────────────────┐
│                     TRANSPORT LAYER                                  │
│        ┌─────────────────┬─────────────────┐                        │
│        │      TCP        │      UDP        │                        │
│        │  (SOCK_STREAM)  │  (SOCK_DGRAM)   │                        │
│        │  - Reliable     │  - Best effort  │                        │
│        │  - Ordered      │  - No order     │                        │
│        │  - Connection   │  - Connectionless│                       │
│        └─────────────────┴─────────────────┘                        │
│                      Segments / Datagrams                            │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────────┐
│                      NETWORK LAYER (IP)                              │
│                         Packets                                      │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────────┐
│                    DATA LINK LAYER                                   │
│                    (Ethernet, WiFi)                                  │
│                         Frames                                       │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────────┐
│                     PHYSICAL LAYER                                   │
│                    (cables, signals)                                 │
│                         Bits                                         │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Quick Reference: TCP vs UDP

```
TCP (SOCK_STREAM)                 UDP (SOCK_DGRAM)
─────────────────                 ─────────────────
socket()                          socket()
bind()                            bind()
listen()                          ─
accept() → new socket             ─
recv() / send()                   recvfrom() / sendto()
close()                           close()

Connection: YES                   Connection: NO
Reliability: YES                  Reliability: NO
Ordering: YES                     Ordering: NO
```

---

*NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim*
