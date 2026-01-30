# Week 2: Architectural Models and Socket Programming

> NETWORKING class — ASE, CSIE Bucharest | Computer Networks Laboratory
> 
> by ing. dr. Antonio Clim

---

## 🧭 Quick Navigation

| Section | Time | Description |
|---------|------|-------------|
| [Environment Notice](#️-environment-notice) | — | WSL2 + Docker requirements |
| [Cloning](#-cloning-this-weeks-laboratory) | 5 min | Get the lab files |
| [Initial Setup](#-initial-environment-setup-first-time-only) | 10 min | First-time configuration |
| [Portainer Interface](#️-understanding-portainer-interface) | 5 min | Container management GUI |
| [Wireshark Setup](#-wireshark-setup-and-usage) | 10 min | Packet capture preparation |
| [Overview](#overview) | 5 min | Session goals and context |
| [Learning Objectives](#learning-objectives) | 5 min | What you will learn |
| [Pedagogical Resources](#-pedagogical-resources) | — | Learning materials index |
| [Quick Start](#quick-start) | 5 min | Get running fast |
| [Exercise 1: TCP](#exercise-1-tcp-concurrent-server-implementation) | 25 min | Connection-oriented server |
| [Exercise 2: UDP](#exercise-2-udp-server-with-application-protocol) | 20 min | Connectionless server |
| [Exercise 3: Capture](#exercise-3-traffic-capture-and-analysis) | 25 min | Protocol analysis |
| [Troubleshooting](#troubleshooting) | — | Common issues reference |
| [Self-Assessment](#-self-assessment-checklist) | 10 min | Verify understanding |

**Total estimated time:** 2-3 hours

---

## ⚠️ Environment Notice

This laboratory kit is designed for the **WSL2 + Ubuntu 22.04 + Docker + Portainer** environment.

**Repository:** https://github.com/antonioclim/netENwsl
**This Week's Folder:** `02enWSL`

| Component | Details |
|-----------|---------|
| Windows | Windows 10/11 with WSL2 enabled |
| Linux Distribution | Ubuntu 22.04 LTS (default WSL distro) |
| Container Runtime | Docker Engine (in WSL) |
| Management Interface | Portainer CE on port 9000 (global) |
| Packet Analysis | Wireshark (native Windows application) |

---

## 📥 Cloning This Week's Laboratory

**⏱️ Estimated time: 5 minutes**

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

**⏱️ Estimated time: 10 minutes**

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
cd /mnt/d/NETWORKING/WEEK2/02enWSL
ls -la
```

---

### ✅ Checkpoint: Environment Ready

Before continuing, verify:
- [ ] Docker is running (`docker ps` shows portainer)
- [ ] Portainer is accessible at http://localhost:9000
- [ ] You can navigate to the lab directory

**If any check fails, see [Troubleshooting](#troubleshooting) section.**

---

## 🖥️ Understanding Portainer Interface

**⏱️ Estimated time: 5 minutes**

### Dashboard Overview

After login at http://localhost:9000, you will see:
1. **Home** — List of Docker environments
2. **local** — Click to manage local Docker

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
- **Stats**: CPU/Memory/Network usage in real time

### Modifying Container IP Address

1. Navigate: **Networks → week2_network**
2. View current IPAM configuration (10.0.2.0/24)
3. To change:
   - Stop containers using the network
   - Edit `docker-compose.yml`
   - Recreate: `docker compose down && docker compose up -d`

**⚠️ NEVER use port 9000** — reserved for Portainer!

---

## 🦈 Wireshark Setup and Usage

**⏱️ Estimated time: 10 minutes**

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
| **vEthernet (WSL)** | ✅ Most common — captures WSL Docker traffic |
| **Loopback Adapter** | Only for localhost traffic (127.0.0.1) |
| **Ethernet/Wi-Fi** | Physical network traffic (not Docker) |

### Filters for Week 2

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

### ✅ Checkpoint: Tools Ready

Before starting exercises, verify:
- [ ] Wireshark can capture on vEthernet (WSL) interface
- [ ] You know how to apply display filters
- [ ] Portainer shows your Docker environment

---

## Overview

This laboratory session bridges the theoretical foundations of network architecture with practical implementation through socket programming. The session explores the two primary architectural models that underpin modern computer networking: the **OSI reference model** (a theoretical seven-layer framework developed by ISO for standardised communication) and the **TCP/IP model** (the pragmatic four-layer architecture that powers the Internet).

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

For detailed Bloom taxonomy mapping, see [docs/learning_objectives.md](docs/learning_objectives.md).

## 📚 Pedagogical Resources

This laboratory includes evidence-based learning materials:

| Resource | Purpose | Location |
|----------|---------|----------|
| **Learning Objectives** | Bloom taxonomy mapping and skills checklist | [docs/learning_objectives.md](docs/learning_objectives.md) |
| **Peer Instruction Questions** | MCQ for think-pair-share activities | [docs/peer_instruction.md](docs/peer_instruction.md) |
| **Pair Programming Guide** | Structured collaborative exercises | [docs/pair_programming_guide.md](docs/pair_programming_guide.md) |
| **Common Misconceptions** | Frequent errors and corrections | [docs/misconceptions.md](docs/misconceptions.md) |
| **Glossary** | Technical terms reference | [docs/glossary.md](docs/glossary.md) |
| **Code Tracing** | Execution prediction exercises | [docs/code_tracing.md](docs/code_tracing.md) |
| **Parsons Problems** | Code reordering challenges | [docs/parsons_problems.md](docs/parsons_problems.md) |
| **Concept Analogies** | Practical analogies for abstract concepts | [docs/concept_analogies.md](docs/concept_analogies.md) |
| **Diagrams** | Visual aids with ASCII and PNG versions | [docs/images/README.md](docs/images/README.md) |


### 🗺️ Recommended Learning Path

Follow this sequence for best learning:

| Order | Resource | Time | Purpose |
|-------|----------|------|---------|
| 1 | [docs/theory_summary.md](docs/theory_summary.md) | 15 min | OSI/TCP-IP model overview |
| 2 | [docs/concept_analogies.md](docs/concept_analogies.md) | 10 min | Build intuition with CPA analogies |
| 3 | [docs/glossary.md](docs/glossary.md) | Reference | Keep open during exercises |
| 4 | **Exercise 1** (TCP) | 25 min | Start with connection-oriented |
| 5 | [docs/code_tracing.md](docs/code_tracing.md) | 15 min | Trace TCP execution |
| 6 | **Exercise 2** (UDP) | 20 min | Compare with connectionless |
| 7 | [docs/misconceptions.md](docs/misconceptions.md) | 10 min | Check your understanding |
| 8 | **Exercise 3** (Capture) | 25 min | Observe protocols in action |
| 9 | [docs/peer_instruction.md](docs/peer_instruction.md) | 35 min | Group discussion (if in class) |

**Total estimated time:** 2.5 hours (self-study) or 3 hours (with peer instruction)

### 💭 Prediction Checkpoints

Before running each exercise, pause and predict the outcome. This builds deeper understanding.

**Exercise 1 (TCP):**
- [ ] How many packets does `listen()` generate? _(Answer: Zero — it's local)_
- [ ] What packets will `connect()` trigger? _(Answer: SYN → SYN-ACK → ACK)_
- [ ] Threaded server with 10 clients: total time? _(Answer: ~100ms parallel)_

**Exercise 2 (UDP):**
- [ ] Does `bind()` send any packets? _(Answer: No — local operation)_
- [ ] Packets for one "ping" exchange? _(Answer: 2 — request + response)_
- [ ] What if server is down when client sends? _(Answer: sendto succeeds, recvfrom times out)_

**Exercise 3 (Capture):**
- [ ] TCP vs UDP: what's missing in UDP capture? _(Answer: No SYN, ACK, FIN packets)_

---

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

**⏱️ Estimated time: 5 minutes**

### First-Time Setup (Run Once)

```bash
# Open Ubuntu terminal (WSL)
wsl

# Navigate to the laboratory directory
cd /mnt/d/NETWORKING/WEEK2/02enWSL

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

---

## Laboratory Exercises

### Exercise 1: TCP Concurrent Server Implementation

**⏱️ Duration:** 25 minutes

**Objective:** Implement and operate a multi-threaded TCP server that transforms received messages, demonstrating connection-oriented communication patterns.

**Theoretical Context:** TCP operates at the Transport Layer (L4), providing reliable, ordered and error-checked delivery. The three-way handshake establishes a connection before data transfer.

> 💭 **PREDICTION CHECKPOINT:** Before starting, predict:
> - What will Wireshark show when the client connects?
> - How will threaded vs iterative mode differ under load?

**Steps:**

1. **Start the laboratory environment:**
   ```bash
   python3 scripts/start_lab.py
   ```

2. **Launch the TCP server in threaded mode:**
   ```bash
   python3 src/exercises/ex_2_01_tcp.py server --port 9090 --mode threaded
   ```
   
   > 💡 **Learning mode:** Add `--interactive` for built-in prediction prompts:
   > ```bash
   > python3 src/exercises/ex_2_01_tcp.py server --port 9090 --interactive
   > ```

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

---

### ✅ Checkpoint: TCP Understanding

After completing Exercise 1, verify:
- [ ] I can explain why the server needs `listen()` and `accept()`
- [ ] I understand why threaded mode is faster under load
- [ ] I can identify the three-way handshake in Wireshark

---

### Exercise 2: UDP Server with Application Protocol

**⏱️ Duration:** 20 minutes

**Objective:** Implement a connectionless UDP server with a custom application-layer protocol.

**Theoretical Context:** UDP provides minimal transport service with no connection establishment, no acknowledgements and no guaranteed delivery.

> 💭 **PREDICTION CHECKPOINT:** Before starting, predict:
> - How will the Wireshark capture differ from TCP?
> - What happens if you send to a server that isn't running?

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

---

### ✅ Checkpoint: UDP Understanding

After completing Exercise 2, verify:
- [ ] I understand why UDP doesn't need `listen()` or `accept()`
- [ ] I can explain why the same socket sends and receives
- [ ] I know why `recvfrom()` returns the sender's address

---

### Exercise 3: Traffic Capture and Analysis

**⏱️ Duration:** 25 minutes

**Objective:** Capture and analyse network traffic to correlate application-level communication with transport-layer protocol behaviour.

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

---

### ✅ Checkpoint: Protocol Analysis

After completing Exercise 3, verify:
- [ ] I can identify TCP handshake packets in a capture
- [ ] I understand why UDP captures have fewer packets
- [ ] I can follow a TCP stream in Wireshark

---

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
cd /mnt/d/NETWORKING/WEEK2/02enWSL
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
| Portainer | 9000 | **RESERVED — Global service** |

---

## ✅ Self-Assessment Checklist

**⏱️ Estimated time: 10 minutes**

Before proceeding to Week 3, verify your understanding:

### Conceptual Understanding

- [ ] I can name all 7 layers of the OSI model and their PDUs
- [ ] I can explain the difference between TCP and UDP
- [ ] I understand why TCP needs a three-way handshake
- [ ] I know when to use TCP vs UDP for different applications

### Practical Skills

- [ ] I can start/stop the laboratory environment
- [ ] I can run TCP and UDP servers in different modes
- [ ] I can capture and analyse network traffic with Wireshark/tcpdump
- [ ] I can identify TCP handshake packets in a capture

### Code Understanding

- [ ] I understand the difference between `bind()` and `connect()`
- [ ] I can explain why threaded servers handle concurrent clients better
- [ ] I know what SO_REUSEADDR does and when to use it
- [ ] I understand the byte-stream nature of TCP

### Troubleshooting

- [ ] I know how to diagnose "Address already in use" errors
- [ ] I can verify if Docker is running
- [ ] I can select the correct Wireshark capture interface

**If you checked all boxes, you're ready for Week 3!**

---

*NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim*
*Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment*


---

## Anti‑AI evidence workflow for assessed work

You may use AI tools to clarify concepts and troubleshoot. Your submission must still include proof of real execution. The anti‑AI workflow in this kit generates per‑student challenges and machine‑checkable evidence.

### Quick start

From inside `02enWSL/`:

```bash
make install
make anti-ai STUDENT_ID=YOUR_ID
```

This will generate:
- a personalised challenge file under `artifacts/anti_ai/`
- proof logs for TCP and UDP traffic under `artifacts/anti_ai/proof_YOUR_ID/`
- an `evidence_YOUR_ID.json` manifest with SHA256 hashes and minimal environment metadata

### What is checked

The validator checks that your proof logs contain the per‑student payload token and that the artefacts match the recorded hashes. This makes it impractical to submit plausible looking results without running the programs.

For strict validation with signed challenges, the instructor sets `ANTI_AI_MASTER_KEY` when generating challenges and when validating submissions.
