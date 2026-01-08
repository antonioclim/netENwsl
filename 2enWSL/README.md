# Week 2: Architectural Models and Socket Programming

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
> 
> by Revolvix

---

## ⚠️ Environment Notice

This laboratory kit is designed for the **WSL2 + Ubuntu 22.04 + Docker + Portainer** environment.

**Repository:** https://github.com/antonioclim/netENwsl
**This Week's Folder:** `2enWSL`

| Component | Details |
|-----------|---------|
| Windows | Windows 10/11 with WSL2 enabled |
| Linux Distribution | Ubuntu 22.04 LTS (default WSL distro) |
| Container Runtime | Docker Engine (in WSL) |
| Management Interface | Portainer CE on port 9000 (global) |
| Packet Analysis | Wireshark (native Windows application) |

---

## 📥 Cloning This Week's Laboratory

### Step 1: Open PowerShell (Windows)

Press `Win + X` → Select "Windows Terminal" or "PowerShell"

### Step 2: Navigate and Clone

```powershell
# Create networking folder if it doesn't exist
mkdir D:\NETWORKING -ErrorAction SilentlyContinue
cd D:\NETWORKING

# Clone Week 2
git clone https://github.com/antonioclim/netENwsl.git WEEK2
cd WEEK2
```

### Step 3: Verify Clone
```powershell
dir
# You should see: docker/, scripts/, src/, README.md, etc.
```

### Alternative: Clone Inside WSL

```bash
# In Ubuntu terminal
mkdir -p /mnt/d/NETWORKING
cd /mnt/d/NETWORKING
git clone https://github.com/antonioclim/netENwsl.git WEEK2
cd WEEK2
```

---

## 🔧 Initial Environment Setup (First Time Only)

### Step 1: Open Ubuntu Terminal

From Windows:
- Click "Ubuntu" in Start menu, OR
- In PowerShell type: `wsl`

You will see the Ubuntu prompt:
```
stud@YOURPC:~$
```

### Step 2: Start Docker Service

```bash
# Start Docker (required after each Windows restart)
sudo service docker start
# Password: stud

# Verify Docker is running
docker ps
```

**Expected output:**
```
CONTAINER ID   IMAGE                    STATUS          NAMES
abc123...      portainer/portainer-ce   Up 2 hours      portainer
```

### Step 3: Verify Portainer Access

Open browser and navigate to: **http://localhost:9000**

**Login credentials:**
- Username: `stud`
- Password: `studstudstud`

### Step 4: Navigate to Laboratory Directory

```bash
cd /mnt/d/NETWORKING/WEEK2/2enWSL
ls -la
```

---

## 🖥️ Understanding Portainer Interface

### Dashboard Overview

After login at http://localhost:9000, you will see:
1. **Home** - List of Docker environments
2. **local** - Click to manage local Docker

### Viewing Containers

Navigate: **Home → local → Containers**

You will see a table showing all containers with:
- Name, State, Image, Created, IP Address, Ports

### Container Actions in Portainer

For any container, you can:
- **Start/Stop/Restart**: Use the action buttons
- **Logs**: Click container name → "Logs" tab
- **Console**: Click container name → "Console" tab → "Connect"
- **Inspect**: View detailed JSON configuration
- **Stats**: Real-time CPU/Memory/Network usage

### Modifying Container IP Address

1. Navigate: **Networks → week2_network**
2. View current IPAM configuration (10.0.2.0/24)
3. To change:
   - Stop containers using the network
   - Edit `docker-compose.yml`
   - Recreate: `docker compose down && docker compose up -d`

**⚠️ NEVER use port 9000** - reserved for Portainer!

---

## 🦈 Wireshark Setup and Usage

### When to Open Wireshark

Open Wireshark:
- **BEFORE** generating network traffic you want to capture
- When exercises mention "capture", "analyse packets", or "observe traffic"

### Step 1: Launch Wireshark

From Windows Start Menu: Search "Wireshark" → Click to open

### Step 2: Select Capture Interface

**CRITICAL:** Select the correct interface for WSL traffic:

| Interface Name | When to Use |
|----------------|-------------|
| **vEthernet (WSL)** | ✅ Most common - captures WSL Docker traffic |
| **Loopback Adapter** | Only for localhost traffic (127.0.0.1) |
| **Ethernet/Wi-Fi** | Physical network traffic (not Docker) |

### Essential Wireshark Filters for Week 2

| Filter | Purpose |
|--------|---------|
| `tcp.port == 9090` | TCP server traffic |
| `udp.port == 9091` | UDP server traffic |
| `tcp.flags.syn == 1` | TCP SYN packets (handshake) |
| `ip.addr == 10.0.2.10` | Container traffic |

### Following a TCP Conversation

1. Find any packet in the conversation
2. Right-click → **Follow → TCP Stream**
3. View complete conversation in readable text

### Saving Captures

1. **File → Save As**
2. Navigate to: `D:\NETWORKING\WEEK2\pcap\`
3. Filename: `capture_exercise_N.pcap`

---

## Overview

This laboratory session bridges the theoretical foundations of network architecture with practical implementation through socket programming. The session explores the two fundamental architectural models that underpin modern computer networking: the **OSI reference model** (a theoretical seven-layer framework developed by ISO for standardised communication) and the **TCP/IP model** (the pragmatic four-layer architecture that powers the Internet).

The practical component introduces the Berkeley Sockets API, the de facto standard interface for network programming across operating systems. Students will implement concurrent TCP servers capable of handling multiple simultaneous connections through threading, as well as connectionless UDP servers suitable for low-latency applications.

Throughout the exercises, students will capture network traffic to observe protocol behaviour at the packet level, correlating application code with the encapsulation process described in architectural models.

## Learning Objectives

By the end of this laboratory session, you will be able to:

1. **Recall** the seven layers of the OSI model and four layers of the TCP/IP model, identifying their respective PDUs and primary functions
2. **Explain** the encapsulation process and how data units transform as they traverse the protocol stack
3. **Implement** concurrent TCP servers using Python's socket module with threading
4. **Implement** UDP servers and clients demonstrating connectionless communication patterns
5. **Analyse** network captures to identify TCP three-way handshake and compare with UDP's connectionless behaviour
6. **Evaluate** the trade-offs between TCP and UDP for different application requirements

## Prerequisites

### Knowledge Requirements

- Understanding of basic networking concepts from Week 1
- Familiarity with Python programming (functions, classes, basic I/O)
- Basic command-line proficiency in WSL2 terminal

### Software Requirements

- Windows 10/11 with WSL2 enabled
- Docker Engine (in WSL)
- Portainer CE (running globally on port 9000)
- Wireshark (native Windows installation)
- Python 3.11 or later

### Hardware Requirements

- Minimum 8GB RAM (16GB recommended)
- 10GB free disk space
- Network connectivity (for initial setup only)

## Quick Start

### First-Time Setup (Run Once)

```bash
# Open Ubuntu terminal (WSL)
wsl

# Navigate to the laboratory directory
cd /mnt/d/NETWORKING/WEEK2/2enWSL

# Start Docker if not running
sudo service docker start

# Verify prerequisites
python3 setup/verify_environment.py
```

### Starting the Laboratory

```bash
# Start all services
python3 scripts/start_lab.py

# Verify everything is running
python3 scripts/start_lab.py --status

# For a quick demonstration
python3 scripts/run_demo.py
```

### Accessing Services

| Service | URL/Port | Credentials |
|---------|----------|-------------|
| Portainer | http://localhost:9000 | stud / studstudstud |
| TCP Server | localhost:9090 | N/A |
| UDP Server | localhost:9091 | N/A |

## Laboratory Exercises

### Exercise 1: TCP Concurrent Server Implementation

**Objective:** Implement and operate a multi-threaded TCP server that transforms received messages, demonstrating connection-oriented communication patterns.

**Duration:** 25 minutes

**Theoretical Context:** TCP operates at the Transport Layer (L4), providing reliable, ordered, and error-checked delivery. The three-way handshake establishes a connection before data transfer.

**Steps:**

1. **Start the laboratory environment:**
   ```bash
   python3 scripts/start_lab.py
   ```

2. **Launch the TCP server in threaded mode:**
   ```bash
   python3 src/exercises/ex_2_01_tcp.py server --port 9090 --mode threaded
   ```

3. **In a separate terminal, send a message:**
   ```bash
   python3 src/exercises/ex_2_01_tcp.py client --host 127.0.0.1 --port 9090 --message "Hello from client"
   ```
   
   **Expected output:**
   ```
   [HH:MM:SS.mmm][CLIENT] RX 20B in X.Xms: b'OK: HELLO FROM CLIENT'
   ```

4. **Test concurrent connections:**
   ```bash
   python3 src/exercises/ex_2_01_tcp.py load --host 127.0.0.1 --port 9090 --clients 10
   ```

5. **Compare with iterative mode:**
   ```bash
   python3 src/exercises/ex_2_01_tcp.py server --port 9090 --mode iterative
   ```

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 1
```

### Exercise 2: UDP Server with Application Protocol

**Objective:** Implement a connectionless UDP server with a custom application-layer protocol.

**Duration:** 20 minutes

**Theoretical Context:** UDP provides minimal transport service with no connection establishment, no acknowledgements, and no guaranteed delivery.

**Steps:**

1. **Start the UDP server:**
   ```bash
   python3 src/exercises/ex_2_02_udp.py server --port 9091
   ```

2. **Use the interactive client:**
   ```bash
   python3 src/exercises/ex_2_02_udp.py client --host 127.0.0.1 --port 9091 --interactive
   ```
   
   **Try these commands:**
   ```
   > ping
   > upper:hello world
   > reverse:networking
   > time
   > help
   > exit
   ```

3. **Test single-command mode:**
   ```bash
   python3 src/exercises/ex_2_02_udp.py client --host 127.0.0.1 --port 9091 --once "upper:protocol"
   ```

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 2
```

### Exercise 3: Traffic Capture and Analysis

**Objective:** Capture and analyse network traffic to correlate application-level communication with transport-layer protocol behaviour.

**Duration:** 25 minutes

**Steps:**

1. **Start traffic capture:**
   ```bash
   python3 scripts/capture_traffic.py --interface lo --filter "tcp port 9090" --output pcap/tcp_session.pcap &
   ```

2. **Generate TCP traffic:**
   ```bash
   python3 src/exercises/ex_2_01_tcp.py client --host 127.0.0.1 --port 9090 --message "capture test"
   ```

3. **Analyse with tshark:**
   ```bash
   tshark -r pcap/tcp_session.pcap -Y "tcp.port==9090"
   ```

4. **Identify the TCP handshake packets:**
   - SYN (client → server)
   - SYN-ACK (server → client)
   - ACK (client → server)

5. **Compare with UDP capture:**
   ```bash
   python3 scripts/capture_traffic.py --interface lo --filter "udp port 9091" --output pcap/udp_session.pcap &
   python3 src/exercises/ex_2_02_udp.py client --host 127.0.0.1 --port 9091 --once "ping"
   ```

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 3
```

## Demonstrations

### Demo 1: TCP vs UDP Comparison

```bash
python3 scripts/run_demo.py --demo tcp_vs_udp
```

### Demo 2: Concurrent Connections

```bash
python3 scripts/run_demo.py --demo concurrent
```

## Packet Capture Guide

### Wireshark Filters for This Week

```
tcp.port == 9090
tcp.port == 9090 and tcp.len > 0
udp.port == 9091
tcp.stream eq 0
```

### Analysis Commands

```bash
# Show TCP conversation summary
tshark -r pcap/week2_tcp.pcap -z conv,tcp

# Extract payload data
tshark -r pcap/week2_tcp.pcap -Y "tcp.port==9090 and data" -T fields -e tcp.payload
```

## Shutdown and Cleanup

### End of Session

```bash
# Stop lab containers (Portainer stays running!)
python3 scripts/stop_lab.py

# Verify shutdown
docker ps
```

### Full Cleanup (Before Next Week)

```bash
python3 scripts/cleanup.py --full
docker system df
```

## Homework Assignments

See the `homework/` directory for take-home exercises.

### Assignment 1: Protocol Extension

Extend the UDP server to support arithmetic operations (`add:5:3` → `8`, `mul:4:7` → `28`).

### Assignment 2: Connection Statistics

Modify the TCP server to track connection statistics accessible via a `stats` command.

## Troubleshooting

### Common Issues

#### Issue: `Address already in use`

```bash
lsof -i :9090
kill <pid>
```

#### Issue: Connection refused

```bash
python3 src/exercises/ex_2_01_tcp.py server --bind 0.0.0.0 --port 9090
```

#### Issue: Docker containers fail to start

```bash
sudo service docker start
docker ps
```

## Theoretical Background

### The OSI Model

| Layer | Name | PDU | Function |
|-------|------|-----|----------|
| 7 | Application | Data | User interface, application services |
| 6 | Presentation | Data | Data formatting, encryption |
| 5 | Session | Data | Connection management |
| 4 | Transport | Segment/Datagram | End-to-end delivery |
| 3 | Network | Packet | Logical addressing, routing |
| 2 | Data Link | Frame | Physical addressing |
| 1 | Physical | Bit | Signal transmission |

### The TCP/IP Model

| Layer | Equivalent OSI Layers | Protocols |
|-------|----------------------|-----------|
| Application | 5, 6, 7 | HTTP, FTP, DNS, SSH |
| Transport | 4 | TCP, UDP |
| Internet | 3 | IP, ICMP, ARP |
| Network Access | 1, 2 | Ethernet, WiFi |

### TCP vs UDP Comparison

| Characteristic | TCP | UDP |
|----------------|-----|-----|
| Connection | Connection-oriented | Connectionless |
| Reliability | Guaranteed delivery | Best effort |
| Ordering | In-order delivery | No ordering |
| Header Size | 20-60 bytes | 8 bytes |
| Use Cases | Web, email, file transfer | Streaming, DNS, gaming |

## References

- Kurose, J. & Ross, K. (2021). *Computer Networking: A Top-Down Approach* (8th ed.). Pearson.
- Stevens, W. R., Fenner, B., & Rudoff, A. (2004). *UNIX Network Programming, Vol. 1*. Addison-Wesley.
- RFC 793: Transmission Control Protocol (TCP)
- RFC 768: User Datagram Protocol (UDP)

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        WEEK 2 Laboratory Environment                     │
│                  (WSL2 + Ubuntu 22.04 + Docker + Portainer)             │
├─────────────────────────────────────────────────────────────────────────┤
│   Windows Host                                                           │
│   ┌──────────────────────────────────────────────────────────────────┐  │
│   │  Wireshark (use vEthernet WSL interface)                         │  │
│   └──────────────────────────────────────────────────────────────────┘  │
│                                   │                                      │
│   ┌──────────────────────────────────────────────────────────────────┐  │
│   │  WSL2 + Ubuntu 22.04                                              │  │
│   │  ┌────────────────────────────────────────────────────────────┐  │  │
│   │  │  Docker Engine                                              │  │  │
│   │  │  ┌────────────────────────────────────────────────────────┐ │  │  │
│   │  │  │  week2_lab Container (10.0.2.10)                       │ │  │  │
│   │  │  │  ┌─────────────────┐  ┌─────────────────┐              │ │  │  │
│   │  │  │  │  TCP Server     │  │  UDP Server     │              │ │  │  │
│   │  │  │  │  :9090          │  │  :9091          │              │ │  │  │
│   │  │  │  └─────────────────┘  └─────────────────┘              │ │  │  │
│   │  │  │              Docker Network: week2_network              │ │  │  │
│   │  │  │              Subnet: 10.0.2.0/24                        │ │  │  │
│   │  │  └────────────────────────────────────────────────────────┘ │  │  │
│   │  │                                                              │  │  │
│   │  │  Portainer CE (Global): http://localhost:9000               │  │  │
│   │  │  Credentials: stud / studstudstud                           │  │  │
│   │  └────────────────────────────────────────────────────────────┘  │  │
│   └──────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘

TCP Three-Way Handshake:              UDP Connectionless:
                                                     
    Client          Server               Client          Server
       │               │                    │               │
       │── SYN ───────▶│                    │── Datagram ──▶│
       │◀── SYN-ACK ───│                    │◀── Datagram ──│
       │── ACK ───────▶│                    │               │
       │◀══ DATA ═════▶│                                    
```

---

## 🔧 Extended Troubleshooting

### Docker Issues

**Problem:** "Cannot connect to Docker daemon"
```bash
sudo service docker start
docker ps
```

**Problem:** Permission denied
```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Portainer Issues

**Problem:** Cannot access http://localhost:9000
```bash
docker ps -a | grep portainer
docker start portainer
```

**Problem:** Forgot Portainer password
```bash
docker stop portainer
docker rm portainer
docker volume rm portainer_data
# Recreate Portainer
```

### Socket Programming Issues

**Problem:** "Address already in use"
```bash
lsof -i :9090
kill <pid>
```

**Problem:** Connection refused
```bash
ss -tlnp | grep 9090
```

### Wireshark Issues

**Problem:** No packets captured
- Verify correct interface (vEthernet WSL)
- Ensure traffic is generated DURING capture
- Clear display filter

---

## 🧹 Complete Cleanup Procedure

### End of Session (Quick)

```bash
cd /mnt/d/NETWORKING/WEEK2/2enWSL
docker compose -f docker/docker-compose.yml down
docker ps  # Should still show portainer
```

### End of Week (Thorough)

```bash
docker compose -f docker/docker-compose.yml down --volumes
docker image prune -f
docker network prune -f
```

### Full Reset

```bash
# WARNING: Preserves Portainer only
docker stop $(docker ps -q | grep -v $(docker ps -q --filter name=portainer)) 2>/dev/null
docker rm $(docker ps -aq | grep -v $(docker ps -aq --filter name=portainer)) 2>/dev/null
```

**⚠️ NEVER run `docker system prune -a` without excluding Portainer!**

---

## 📊 Week 2 Network Configuration Summary

| Resource | Value | Notes |
|----------|-------|-------|
| Subnet | 10.0.2.0/24 | Week 2 dedicated subnet |
| Gateway | 10.0.2.1 | Docker bridge gateway |
| Lab Container IP | 10.0.2.10 | Static assignment |
| TCP Port | 9090 | Socket programming |
| UDP Port | 9091 | Datagram exercises |
| Portainer | 9000 | **RESERVED - Global service** |

---

*NETWORKING class - ASE, Informatics | by Revolvix*
*Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment*
