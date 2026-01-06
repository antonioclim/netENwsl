# Week 2: Architectural Models and Socket Programming

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
> 
> by Revolvix

## Overview

This laboratory session bridges the theoretical foundations of network architecture with practical implementation through socket programming. The session explores the two fundamental architectural models that underpin modern computer networking: the **OSI reference model** (a theoretical seven-layer framework developed by ISO for standardised communication) and the **TCP/IP model** (the pragmatic four-layer architecture that powers the Internet).

The practical component introduces the Berkeley Sockets API, the de facto standard interface for network programming across operating systems. Students will implement concurrent TCP servers capable of handling multiple simultaneous connections through threading, as well as connectionless UDP servers suitable for low-latency applications. These implementations directly correlate with the transport layer concepts discussed in the theoretical portion.

Throughout the exercises, students will capture network traffic to observe protocol behaviour at the packet level, correlating application code with the encapsulation process described in architectural models. This approach reinforces understanding of how data traverses the protocol stack, with headers added at each layer during transmission and removed during reception.

## Learning Objectives

By the end of this laboratory session, you will be able to:

1. **Recall** the seven layers of the OSI model and four layers of the TCP/IP model, identifying their respective PDUs and primary functions
2. **Explain** the encapsulation process and how data units transform as they traverse the protocol stack from application to physical layer
3. **Implement** concurrent TCP servers using Python's socket module with threading for simultaneous client handling
4. **Implement** UDP servers and clients demonstrating connectionless communication patterns
5. **Analyse** network captures to identify TCP three-way handshake (SYN, SYN-ACK, ACK) and compare with UDP's connectionless behaviour
6. **Evaluate** the trade-offs between TCP (reliability, ordering, flow control) and UDP (minimal overhead, low latency) for different application requirements

## Prerequisites

### Knowledge Requirements

- Understanding of basic networking concepts from Week 1 (protocols, addressing, protocol stacks)
- Familiarity with Python programming (functions, classes, basic I/O)
- Basic command-line proficiency in Windows PowerShell or WSL2 terminal

### Software Requirements

- Windows 10/11 with WSL2 enabled
- Docker Desktop (WSL2 backend) version 4.0 or later
- Wireshark (native Windows installation)
- Python 3.11 or later
- Git (optional, for version control)

### Hardware Requirements

- Minimum 8GB RAM (16GB recommended for smooth Docker operation)
- 10GB free disk space
- Network connectivity (for initial setup only; exercises run locally)

## Quick Start

### First-Time Setup (Run Once)

```powershell
# Open PowerShell as Administrator
cd WEEK2_WSLkit

# Verify prerequisites are installed
python setup/verify_environment.py

# If any issues detected, run the installer helper
python setup/install_prerequisites.py
```

### Starting the Laboratory

```powershell
# Start all services
python scripts/start_lab.py

# Verify everything is running
python scripts/start_lab.py --status

# For a quick demonstration
python scripts/run_demo.py
```

### Accessing Services

| Service | URL/Port | Credentials |
|---------|----------|-------------|
| Portainer | https://localhost:9443 | Set on first access |
| TCP Server | localhost:9090 | N/A |
| UDP Server | localhost:9091 | N/A |

## Laboratory Exercises

### Exercise 1: TCP Concurrent Server Implementation

**Objective:** Implement and operate a multi-threaded TCP server that transforms received messages, demonstrating connection-oriented communication patterns.

**Duration:** 25 minutes

**Theoretical Context:** TCP (Transmission Control Protocol) operates at the Transport Layer (L4), providing reliable, ordered, and error-checked delivery of bytes between applications. The three-way handshake establishes a connection before data transfer, ensuring both endpoints are ready to communicate.

**Steps:**

1. **Start the laboratory environment:**
   ```powershell
   python scripts/start_lab.py
   ```

2. **Launch the TCP server in threaded mode:**
   ```powershell
   python src/exercises/ex_2_01_tcp.py server --port 9090 --mode threaded
   ```
   
   Observe the server output indicating it is listening for connections.

3. **In a separate terminal, send a message:**
   ```powershell
   python src/exercises/ex_2_01_tcp.py client --host 127.0.0.1 --port 9090 --message "Hello from client"
   ```
   
   **Expected output:**
   ```
   [HH:MM:SS.mmm][CLIENT] RX 20B in X.Xms: b'OK: HELLO FROM CLIENT'
   ```

4. **Test concurrent connections with load testing:**
   ```powershell
   python src/exercises/ex_2_01_tcp.py load --host 127.0.0.1 --port 9090 --clients 10
   ```
   
   Observe that all 10 clients complete successfully, demonstrating the threaded server's ability to handle concurrent connections.

5. **Compare with iterative mode:**
   Stop the server (Ctrl+C) and restart in iterative mode:
   ```powershell
   python src/exercises/ex_2_01_tcp.py server --port 9090 --mode iterative
   ```
   
   Run the load test again and observe the performance difference.

**Verification:**
```powershell
python tests/test_exercises.py --exercise 1
```

### Exercise 2: UDP Server with Application Protocol

**Objective:** Implement a connectionless UDP server with a custom application-layer protocol, contrasting with TCP's connection-oriented approach.

**Duration:** 20 minutes

**Theoretical Context:** UDP (User Datagram Protocol) provides a minimal transport service with no connection establishment, no acknowledgements, and no guaranteed delivery. This makes it suitable for applications where low latency is more important than reliability, such as real-time video streaming, DNS queries, and online gaming.

**Steps:**

1. **Start the UDP server:**
   ```powershell
   python src/exercises/ex_2_02_udp.py server --port 9091
   ```

2. **Use the interactive client to explore the protocol:**
   ```powershell
   python src/exercises/ex_2_02_udp.py client --host 127.0.0.1 --port 9091 --interactive
   ```
   
   **Try these commands:**
   ```
   > ping
     ← PONG (X.Xms)
   
   > upper:hello world
     ← HELLO WORLD (X.Xms)
   
   > reverse:networking
     ← gnikrowten (X.Xms)
   
   > time
     ← HH:MM:SS (X.Xms)
   
   > help
     ← Commands: ping, upper:<text>, lower:<text>, reverse:<text>, time, help, exit
   
   > exit
   ```

3. **Test single-command mode:**
   ```powershell
   python src/exercises/ex_2_02_udp.py client --host 127.0.0.1 --port 9091 --once "upper:protocol"
   ```

**Verification:**
```powershell
python tests/test_exercises.py --exercise 2
```

### Exercise 3: Traffic Capture and Analysis

**Objective:** Capture and analyse network traffic to correlate application-level communication with transport-layer protocol behaviour.

**Duration:** 25 minutes

**Steps:**

1. **Start traffic capture:**
   ```powershell
   python scripts/capture_traffic.py --interface lo --filter "tcp port 9090" --output pcap/tcp_session.pcap &
   ```

2. **Generate TCP traffic:**
   ```powershell
   # Ensure TCP server is running
   python src/exercises/ex_2_01_tcp.py client --host 127.0.0.1 --port 9090 --message "capture test"
   ```

3. **Stop capture and analyse:**
   ```powershell
   # Stop capture (Ctrl+C in capture terminal)
   
   # Analyse with tshark (from WSL)
   wsl tshark -r pcap/tcp_session.pcap -Y "tcp.port==9090" -T fields -e frame.number -e ip.src -e tcp.srcport -e ip.dst -e tcp.dstport -e tcp.flags.str
   ```

4. **Identify the TCP handshake in the output:**
   - Frame 1: `··········S·` (SYN) - Client initiates connection
   - Frame 2: `·······A··S·` (SYN-ACK) - Server acknowledges and accepts
   - Frame 3: `·······A····` (ACK) - Client confirms, connection established

5. **Repeat for UDP and compare:**
   ```powershell
   python scripts/capture_traffic.py --interface lo --filter "udp port 9091" --output pcap/udp_session.pcap &
   python src/exercises/ex_2_02_udp.py client --host 127.0.0.1 --port 9091 --once "ping"
   ```
   
   Note the absence of handshake packets—UDP sends data immediately.

**Verification:**
```powershell
python tests/test_exercises.py --exercise 3
```

## Demonstrations

### Demo 1: Complete TCP/UDP Comparison

This automated demonstration showcases the fundamental differences between TCP and UDP at the packet level.

```powershell
python scripts/run_demo.py --demo 1
```

**What to observe:**

- TCP requires 7+ packets for a single request-response (handshake + data + acknowledgements + close)
- UDP requires only 2 packets (request + response)
- TCP provides sequence numbers for ordering; UDP has none
- TCP header is 20+ bytes; UDP header is exactly 8 bytes

### Demo 2: Concurrent Connection Handling

Demonstrates how the threaded TCP server handles multiple simultaneous connections.

```powershell
python scripts/run_demo.py --demo 2
```

**What to observe:**

- Each client connection spawns a dedicated worker thread
- Server logs show interleaved processing of concurrent requests
- All clients receive responses despite simultaneous arrival

## Packet Capture and Analysis

### Capturing Traffic

```powershell
# TCP capture on loopback
python scripts/capture_traffic.py --interface lo --filter "tcp port 9090" --output pcap/week2_tcp.pcap

# UDP capture
python scripts/capture_traffic.py --interface lo --filter "udp port 9091" --output pcap/week2_udp.pcap

# Combined capture for comparison
python scripts/capture_traffic.py --interface lo --filter "port 9090 or port 9091" --output pcap/week2_combined.pcap
```

### Suggested Wireshark Filters

```
# TCP traffic on application port
tcp.port == 9090

# TCP handshake packets only
tcp.flags.syn == 1

# TCP data packets (with payload)
tcp.port == 9090 and tcp.len > 0

# UDP traffic
udp.port == 9091

# Follow TCP stream
tcp.stream eq 0
```

### Analysis Commands

```bash
# In WSL terminal

# Show TCP conversation summary
tshark -r pcap/week2_tcp.pcap -z conv,tcp

# Extract payload data
tshark -r pcap/week2_tcp.pcap -Y "tcp.port==9090 and data" -T fields -e tcp.payload

# Detailed packet information
tshark -r pcap/week2_tcp.pcap -V -Y "frame.number <= 10"
```

## Shutdown and Cleanup

### End of Session

```powershell
# Stop all containers (preserves data for next session)
python scripts/stop_lab.py

# Verify shutdown
docker ps
```

### Full Cleanup (Before Next Week)

```powershell
# Remove all containers, networks, and volumes for this week
python scripts/cleanup.py --full

# Verify cleanup
docker system df
```

## Homework Assignments

See the `homework/` directory for take-home exercises.

### Assignment 1: Protocol Extension

Extend the UDP server's application protocol to support arithmetic operations (`add:5:3` → `8`, `mul:4:7` → `28`). Implement proper error handling for invalid operands.

### Assignment 2: Connection Statistics

Modify the TCP server to track and report connection statistics (total connections, bytes transferred, average response time) accessible via a special `stats` command.

## Troubleshooting

### Common Issues

#### Issue: `Address already in use` when starting server

**Solution:** Another process is using the port. Find and terminate it:
```powershell
# On Windows
netstat -ano | findstr :9090
taskkill /PID <pid> /F

# In WSL
lsof -i :9090
kill <pid>
```

#### Issue: Connection refused when testing client

**Solution:** Ensure the server is running and listening on the correct interface:
```powershell
python src/exercises/ex_2_01_tcp.py server --bind 0.0.0.0 --port 9090
```

#### Issue: Empty packet capture

**Solution:** Verify you are capturing on the correct interface. For localhost traffic, use `lo` (loopback). Check available interfaces:
```bash
wsl ip link show
```

#### Issue: Docker containers fail to start

**Solution:** Ensure Docker Desktop is running and WSL2 integration is enabled:
1. Open Docker Desktop
2. Settings → Resources → WSL Integration
3. Enable integration with your WSL2 distribution

See `docs/troubleshooting.md` for additional solutions.

## Theoretical Background

### The OSI Model

The Open Systems Interconnection model provides a seven-layer framework for understanding network communication:

| Layer | Name | PDU | Function |
|-------|------|-----|----------|
| 7 | Application | Data | User interface, application services |
| 6 | Presentation | Data | Data formatting, encryption, compression |
| 5 | Session | Data | Connection management, dialogue control |
| 4 | Transport | Segment/Datagram | End-to-end delivery, flow control |
| 3 | Network | Packet | Logical addressing, routing |
| 2 | Data Link | Frame | Physical addressing, error detection |
| 1 | Physical | Bit | Signal transmission on physical medium |

### The TCP/IP Model

The practical four-layer model implemented by the Internet:

| Layer | Equivalent OSI Layers | Protocols |
|-------|----------------------|-----------|
| Application | 5, 6, 7 | HTTP, FTP, DNS, SSH, SMTP |
| Transport | 4 | TCP, UDP |
| Internet | 3 | IP, ICMP, ARP |
| Network Access | 1, 2 | Ethernet, WiFi, PPP |

### TCP vs UDP Comparison

| Characteristic | TCP | UDP |
|----------------|-----|-----|
| Connection | Connection-oriented | Connectionless |
| Reliability | Guaranteed delivery | Best effort |
| Ordering | In-order delivery | No ordering |
| Flow Control | Yes (sliding window) | None |
| Header Size | 20-60 bytes | 8 bytes |
| Use Cases | Web, email, file transfer | Streaming, DNS, gaming |

## References

- Kurose, J. & Ross, K. (2021). *Computer Networking: A Top-Down Approach* (8th ed.). Pearson. Chapters 1-3.
- Tanenbaum, A. & Wetherall, D. (2011). *Computer Networks* (5th ed.). Pearson. Chapter 1.
- Stevens, W. R., Fenner, B., & Rudoff, A. (2004). *UNIX Network Programming, Vol. 1: The Sockets Networking API* (3rd ed.). Addison-Wesley. Chapters 1-4.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming* (3rd ed.). Apress.
- RFC 793: Transmission Control Protocol (TCP)
- RFC 768: User Datagram Protocol (UDP)
- ISO/IEC 7498-1: Information technology — Open Systems Interconnection — Basic Reference Model

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        WEEK 2 Laboratory Environment                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   Windows Host                                                           │
│   ┌──────────────────────────────────────────────────────────────────┐  │
│   │  Wireshark                                                        │  │
│   │  (Packet Analysis)                                                │  │
│   └──────────────────────────────────────────────────────────────────┘  │
│                                   │                                      │
│                                   │ \\.\pipe\docker_engine               │
│                                   ▼                                      │
│   ┌──────────────────────────────────────────────────────────────────┐  │
│   │  Docker Desktop (WSL2 Backend)                                    │  │
│   │  ┌────────────────────────────────────────────────────────────┐  │  │
│   │  │  week2_lab Container                                        │  │  │
│   │  │  ┌─────────────────┐  ┌─────────────────┐                   │  │  │
│   │  │  │  TCP Server     │  │  UDP Server     │                   │  │  │
│   │  │  │  :9090          │  │  :9091          │                   │  │  │
│   │  │  │  (threaded)     │  │  (datagram)     │                   │  │  │
│   │  │  └─────────────────┘  └─────────────────┘                   │  │  │
│   │  │            │                    │                            │  │  │
│   │  │            └────────┬───────────┘                            │  │  │
│   │  │                     │                                        │  │  │
│   │  │              Docker Network                                  │  │  │
│   │  │              week2_network                                   │  │  │
│   │  │              10.0.2.0/24                                     │  │  │
│   │  └────────────────────────────────────────────────────────────┘  │  │
│   │                                                                   │  │
│   │  ┌────────────────────────────────────────────────────────────┐  │  │
│   │  │  Portainer CE                                               │  │  │
│   │  │  :9443 (HTTPS)                                              │  │  │
│   │  └────────────────────────────────────────────────────────────┘  │  │
│   └──────────────────────────────────────────────────────────────────┘  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘

TCP Three-Way Handshake:
                                                     
    Client                Server                     
       │                     │                       
       │───── SYN ──────────▶│  (seq=x)              
       │                     │                       
       │◀──── SYN-ACK ───────│  (seq=y, ack=x+1)     
       │                     │                       
       │───── ACK ──────────▶│  (ack=y+1)            
       │                     │                       
       │◀═══ DATA ══════════▶│  (connection active)  
       │                     │                       

UDP Connectionless Exchange:

    Client                Server
       │                     │
       │───── Datagram ─────▶│  (request)
       │                     │
       │◀──── Datagram ──────│  (response)
       │                     │
```

---

*NETWORKING class - ASE, Informatics | by Revolvix*
