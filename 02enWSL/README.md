# Week 2: Architectural Models and Socket Programming

> NETWORKING class — ASE, CSIE Bucharest | Computer Networks Laboratory
> 
> by ing. dr. Antonio Clim

---

## 🧭 Quick Start

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

**⏱️ Estimated time: 5 minutes**

### Step 1: Open PowerShell (Windows)

Press `Win + X` → Select "Windows Terminal" or "PowerShell"

### Step 2: Clone the Repository

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

Open browser and go to: **http://localhost:9000**

**Login credentials:**
- Username: `stud`
- Password: `studstudstud`

### Step 4: Go to Laboratory Directory

```bash
cd /mnt/d/NETWORKING/WEEK2/2enWSL
ls -la
```

---

### ✅ Checkpoint: Environment Ready

Before continuing, verify:
- [ ] Docker is running (`docker ps` shows portainer)
- [ ] Portainer is accessible at http://localhost:9000
- [ ] You can access the lab directory

**If any check fails, see [Troubleshooting](#troubleshooting) section.**

---

## 🖥️ Understanding Portainer Interface

**⏱️ Estimated time: 5 minutes**

### Dashboard Overview

After login at http://localhost:9000, you will see:
1. **Home** — List of Docker environments
2. **local** — Click to manage local Docker

### Viewing Containers

Path: **Home → local → Containers**

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

1. Go to: **Networks → week2_network**
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
2. Go to: `D:\NETWORKING\WEEK2\pcap\`
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

**From previous cohorts:** The most common mistake is binding to `127.0.0.1` and then wondering why Docker containers cannot connect. If this happens to you, check your bind address first — it should be `0.0.0.0` for container access.

## Learning Objectives

By the end of this laboratory session, you will be able to:

1. **Recall** the seven layers of the OSI model and four layers of the TCP/IP model, identifying their respective PDUs and primary functions
2. **Explain** the encapsulation process and how data units transform as they traverse the protocol stack
3. **Implement** concurrent TCP servers using Python's socket module with threading
4. **Implement** UDP servers and clients demonstrating connectionless communication patterns
5. **Capture** network traffic using Wireshark and filter by protocol type
6. **Analyse** TCP handshake sequences and correlate packets with socket API calls
7. **Debug** common socket programming errors including "Address already in use"

See [docs/learning_objectives.md](docs/learning_objectives.md) for the complete traceability matrix linking objectives to exercises and assessments.

---

## 📚 Pedagogical Resources

| Resource | Purpose |
|----------|---------|
| [docs/theory_summary.md](docs/theory_summary.md) | OSI/TCP-IP theory with CPA analogies |
| [docs/peer_instruction.md](docs/peer_instruction.md) | 5 MCQ questions for class voting |
| [docs/pair_programming_guide.md](docs/pair_programming_guide.md) | Collaborative exercise structure |
| [docs/misconceptions.md](docs/misconceptions.md) | 12 common errors with corrections |
| [docs/glossary.md](docs/glossary.md) | Technical terms reference |
| [docs/code_tracing.md](docs/code_tracing.md) | Trace execution exercises |
| [docs/parsons_problems.md](docs/parsons_problems.md) | Code reordering exercises |
| [docs/concept_analogies.md](docs/concept_analogies.md) | Real-world analogies |
| [docs/troubleshooting.md](docs/troubleshooting.md) | Problem-solving guide |
| [docs/reflection_prompts.md](docs/reflection_prompts.md) | Post-lab reflection questions |
| [docs/commands_cheatsheet.md](docs/commands_cheatsheet.md) | Quick reference |

### Formative Assessment

Run the interactive quiz:
```bash
make quiz           # Full quiz
make quiz-quick     # 5 random questions
make quiz-review    # Review mode
```

---

## Quick Start

```bash
# 1. Go to lab directory
cd /mnt/d/NETWORKING/WEEK2/2enWSL

# 2. Start Docker containers
docker compose -f docker/docker-compose.yml up -d

# 3. Verify everything is running
docker ps

# 4. Run the TCP exercise
python3 src/exercises/ex_2_01_tcp.py server --port 9090

# In another terminal:
python3 src/exercises/ex_2_01_tcp.py client --host 127.0.0.1 --port 9090 -m "Hello"
```

---

## Exercise 1: TCP Concurrent Server Implementation

**⏱️ Estimated time: 25 minutes**

### Objectives
- Implement a TCP server using Python sockets
- Compare iterative vs threaded server behaviour
- Observe TCP three-way handshake in Wireshark

### Preparation

1. Open Wireshark and select **vEthernet (WSL)** interface
2. Apply filter: `tcp.port == 9090`
3. Start capture

### Step 1: Start the Server

```bash
# Terminal 1
python3 src/exercises/ex_2_01_tcp.py server --port 9090 --mode threaded
```

**💭 PREDICTION:** What packets will Wireshark show when you start the server?
> Answer: None! `bind()` and `listen()` are local operations.

### Step 2: Connect a Client

```bash
# Terminal 2
python3 src/exercises/ex_2_01_tcp.py client --host 127.0.0.1 --port 9090 -m "Hello World"
```

**💭 PREDICTION:** What packets will appear in Wireshark now?
> Answer: SYN → SYN-ACK → ACK (handshake), then DATA packets with PSH flag.

### Step 3: Compare Iterative Mode

```bash
# Restart server in iterative mode
python3 src/exercises/ex_2_01_tcp.py server --port 9090 --mode iterative

# Run load test
python3 src/exercises/ex_2_01_tcp.py load --host 127.0.0.1 --port 9090 --clients 5
```

**💭 PREDICTION:** With 5 clients and 100ms per request, what's the total time?
> Iterative: ~500ms (sequential). Threaded: ~100ms (parallel).

### Exercise Deliverables

- [ ] Screenshot of Wireshark showing TCP handshake
- [ ] Measured timings: iterative vs threaded (5 clients)
- [ ] Answer: Why does iterative mode take longer?

---

## Exercise 2: UDP Server with Application Protocol

**⏱️ Estimated time: 20 minutes**

### Objectives
- Implement a UDP server processing commands
- Observe connectionless communication
- Compare UDP traffic pattern with TCP

### Preparation

1. Clear Wireshark capture
2. Apply filter: `udp.port == 9091`

### Step 1: Start UDP Server

```bash
python3 src/exercises/ex_2_02_udp.py server --port 9091
```

### Step 2: Interactive Client Session

```bash
python3 src/exercises/ex_2_02_udp.py client --host 127.0.0.1 --port 9091 -i
```

Try these commands:
```
> ping
> upper:hello world
> time
> help
> exit
```

**💭 PREDICTION:** How many packets per command?
> Answer: 2 (request + response). No handshake!

### Exercise Deliverables

- [ ] Screenshot showing UDP request-response pairs
- [ ] Comparison: How does UDP traffic differ from TCP?

---

## Exercise 3: Traffic Capture and Analysis

**⏱️ Estimated time: 25 minutes**

### Objectives
- Capture complete TCP and UDP sessions
- Identify protocol differences visually
- Save captures for later analysis

### Step 1: Capture TCP Session

```bash
# Clear Wireshark, start fresh capture
# Run a complete TCP session:
python3 src/exercises/ex_2_01_tcp.py server --port 9090 &
sleep 1
python3 src/exercises/ex_2_01_tcp.py client --host 127.0.0.1 --port 9090 -m "Capture test"
```

Save as: `pcap/tcp_session.pcap`

### Step 2: Capture UDP Session

```bash
python3 src/exercises/ex_2_02_udp.py server --port 9091 &
sleep 1
python3 src/exercises/ex_2_02_udp.py client --host 127.0.0.1 --port 9091 -o "ping"
```

Save as: `pcap/udp_session.pcap`

### Analysis Questions

1. How many packets in the TCP capture vs UDP capture?
2. What is the total overhead (headers) for TCP vs UDP?
3. Identify the FIN-ACK sequence in the TCP capture.

---

## Homework Assignments

See the `homework/` directory for take-home exercises.

### Assignment 1: Protocol Extension

Extend the UDP server to support arithmetic operations (`add:5:3` → `8`, `mul:4:7` → `28`).

### Assignment 2: Connection Statistics

Modify the TCP server to track connection statistics accessible via a `stats` command.

## Troubleshooting

### Common Issues

#### Issue: `Address already in use`

This happens when a previous server is still running or the socket is in TIME_WAIT state.

```bash
# Find what's using the port
lsof -i :9090

# Kill it
kill <pid>

# Or use SO_REUSEADDR (already in our code)
```

**From experience:** About 70% of "Address already in use" errors come from forgetting to stop the previous server. Check with `ps aux | grep python` first.

#### Issue: Connection refused

The server isn't running or is bound to a different address.

```bash
# Check if server is listening
ss -tlnp | grep 9090

# Start server on all interfaces
python3 src/exercises/ex_2_01_tcp.py server --bind 0.0.0.0 --port 9090
```

#### Issue: Docker containers fail to start

```bash
sudo service docker start
docker ps
```

#### Issue: Cannot reach server from Docker container

If you bound to `127.0.0.1`, containers cannot connect. Use `0.0.0.0` instead.

#### Issue: Wireshark shows no packets

- Verify you selected **vEthernet (WSL)** interface
- Ensure traffic is generated DURING capture
- Clear display filter to see all traffic
- Try: `ip.addr == 127.0.0.1`

**If nothing else works:** Try restarting WSL with `wsl --shutdown` from PowerShell. This fixes about 30% of mysterious Docker and networking issues.

---

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
# Recreate Portainer with initial setup
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

## 📋 Support

Having issues? Follow this order:
1. Check [docs/troubleshooting.md](docs/troubleshooting.md)
2. Review the [docs/misconceptions.md](docs/misconceptions.md)
3. Ask a colleague (pair programming helps!)
4. Issues: Open an issue in GitHub

---

*NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim*  
*Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment*
