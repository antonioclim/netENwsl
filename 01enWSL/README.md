# Week 1: Fundamentals of Computer Networks

[![CI Status](https://github.com/antonioclim/netENwsl/actions/workflows/ci.yml/badge.svg)](https://github.com/antonioclim/netENwsl/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

---

## ⚠️ Environment Notice

This laboratory kit is designed for the **WSL2 + Ubuntu 22.04 + Docker + Portainer** environment.

**Repository:** https://github.com/antonioclim/netENwsl
**This Week's Folder:** `1enWSL`

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

# Clone Week 1
git clone https://github.com/antonioclim/netENwsl.git WEEK1
cd WEEK1
```

### Step 3: Verify Clone
```powershell
dir
# You should see: docker/, scripts/, src/, README.md, etc.
```

### Alternative: Clone Inside WSL

If you prefer to work entirely within WSL:

```bash
# In Ubuntu terminal
mkdir -p /mnt/d/NETWORKING
cd /mnt/d/NETWORKING
git clone https://github.com/antonioclim/netENwsl.git WEEK1
cd WEEK1
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
# From WSL, navigate to the cloned repository
cd /mnt/d/NETWORKING/WEEK1/1enWSL

# Verify you're in the correct directory
ls -la
# You should see: docker/, scripts/, src/, README.md, etc.
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
- **Start/Stop/Restart**: Use the action buttons on the right
- **Logs**: Click container name → "Logs" tab
- **Console**: Click container name → "Console" tab → "Connect"
- **Inspect**: View detailed JSON configuration
- **Stats**: Real-time CPU/Memory/Network usage

### Modifying Container IP Address

1. Navigate: **Networks → week1_network**
2. View current IPAM configuration (e.g., 172.20.1.0/24)
3. To change:
   - Stop containers using the network
   - Edit `docker-compose.yml`:
     ```yaml
     networks:
       week1_network:
         ipam:
           config:
             - subnet: 172.20.1.0/24  # Change subnet here
               gateway: 172.20.1.1    # Change gateway here
     ```
   - Recreate: `docker compose down && docker compose up -d`
   - Verify in Portainer: Networks → check new configuration

### Modifying Container Ports

1. In Portainer: View container → "Inspect" → scroll to "HostConfig.PortBindings"
2. To change permanently, edit `docker-compose.yml`:
   ```yaml
   ports:
     - "9090:9090"   # Format: "host_port:container_port"
     - "9095:9091"   # Example: map container 9091 to host 9095
   ```
3. Recreate container: `docker compose down && docker compose up -d`
4. Verify: New ports appear in Portainer container list

**⚠️ NEVER use port 9000** - reserved for Portainer!

---

## 🦈 Wireshark Setup and Usage

### When to Open Wireshark

Open Wireshark:
- **BEFORE** generating network traffic you want to capture
- When exercises mention "capture", "analyse packets", or "observe traffic"
- For demonstrations requiring traffic visualisation

### Step 1: Launch Wireshark

From Windows Start Menu: Search "Wireshark" → Click to open

### Step 2: Select Capture Interface

**CRITICAL:** Select the correct interface for WSL traffic:

| Interface Name | When to Use |
|----------------|-------------|
| **vEthernet (WSL)** | ✅ Most common - captures WSL Docker traffic |
| **vEthernet (WSL) (Hyper-V firewall)** | Alternative if above doesn't work |
| **Loopback Adapter** | Only for localhost traffic (127.0.0.1) |
| **Ethernet/Wi-Fi** | Physical network traffic (not Docker) |

**How to select:** Double-click the interface name OR select it and click the blue shark fin icon.

### Step 3: Generate Traffic

With Wireshark capturing (you'll see packets appearing), run your lab exercises:
```bash
# In Ubuntu terminal
docker exec -it week1_lab bash

# Run network commands inside container
ping 172.20.1.1
nc -l -p 9090  # etc.
```

### Step 4: Stop Capture

Click the red square button (Stop) when finished generating traffic.

### Key Wireshark Filters

Type in the display filter bar (green when valid) and press Enter:

| Filter | Purpose | Example Use |
|--------|---------|-------------|
| `tcp` | All TCP traffic | General TCP analysis |
| `udp` | All UDP traffic | DNS, DHCP analysis |
| `tcp.port == 9090` | Specific port | Lab exercise traffic |
| `ip.addr == 172.20.1.2` | Specific IP | Container traffic |
| `tcp.flags.syn == 1` | TCP SYN packets | Connection initiations |
| `tcp.flags.syn == 1 && tcp.flags.ack == 0` | Only initial SYN | New connections only |
| `tcp.flags.fin == 1` | TCP FIN packets | Connection terminations |
| `http` | HTTP traffic | Web traffic |
| `icmp` | ICMP (ping) | Connectivity tests |
| `tcp.analysis.retransmission` | Retransmissions | Network problems |
| `frame.len > 100` | Large packets | Data transfer |
| `tcp.stream eq 0` | First TCP stream | Follow single conversation |

**Combining filters:**
- AND: `tcp.port == 9090 && ip.addr == 172.20.1.2`
- OR: `tcp.port == 9090 || tcp.port == 9091`
- NOT: `!arp && !dns`

### Understanding Wireshark Columns

| Column | Meaning | What to Look For |
|--------|---------|------------------|
| No. | Packet sequence number | Order of capture |
| Time | Seconds since capture start | Timing analysis |
| Source | Sender IP address | Who sent it |
| Destination | Receiver IP address | Who receives it |
| Protocol | Protocol name | TCP, UDP, HTTP, etc. |
| Length | Packet size (bytes) | Data amount |
| Info | Protocol details | Flags, sequence numbers, etc. |

### Wireshark Colour Coding

| Colour | Meaning |
|--------|---------|
| Light purple | TCP traffic |
| Light blue | UDP traffic |
| Light green | HTTP traffic |
| Black text, red background | Errors, bad checksums |
| Black text, yellow background | Warnings, retransmissions |
| Grey background | TCP SYN/FIN (connection events) |

### Following a TCP Conversation

1. Find any packet in the conversation you want to examine
2. Right-click → **Follow → TCP Stream**
3. A window shows the complete conversation in readable text
   - Red text: Data sent by client
   - Blue text: Data sent by server
4. Use dropdown to switch between ASCII/Hex/Raw views
5. Close window to return to packet list (filter auto-applied)

### Analysing the TCP Three-Way Handshake

Look for this sequence:
1. **SYN**: Client → Server (Flags: SYN)
2. **SYN-ACK**: Server → Client (Flags: SYN, ACK)
3. **ACK**: Client → Server (Flags: ACK)

Filter to see only handshakes: `tcp.flags.syn == 1`

### Saving Captures

1. **File → Save As** (or Ctrl+Shift+S)
2. Navigate to: `D:\NETWORKING\WEEK1\pcap\`
3. Filename: `capture_exercise_N.pcap`
4. Format: Wireshark/pcap or pcapng (default)

### Exporting Data for Analysis

1. **File → Export Packet Dissections → As CSV**
2. Select fields to export
3. Save to `artifacts/` folder for Python processing

---

## Overview

This laboratory introduces the foundational concepts of computer networking through hands-on experimentation with core diagnostic tools. The session establishes the critical skills required for network troubleshooting and analysis that will serve as the foundation for all subsequent laboratory work.

Computer networks permeate every aspect of modern computing infrastructure. Understanding how to diagnose connectivity issues, inspect network configurations and analyse traffic flows represents key competencies for any computing professional. This week focuses on developing practical intuition about network behaviour through direct observation and measurement.

The exercises progress from basic interface inspection through connectivity validation to traffic capture and protocol analysis. Students will work with industry-standard tools including `ip`, `ss`, `ping`, `netcat`, `tcpdump` and `tshark`, developing the diagnostic vocabulary necessary for effective network administration.

## Learning Objectives

By the end of this laboratory session, you will be able to:

1. **Recall** the core Linux networking commands and their primary functions, including `ip addr`, `ip route`, `ss`, `ping` and `netcat`
2. **Explain** the purpose of network interfaces, routing tables and socket states in a Linux environment
3. **Demonstrate** connectivity testing using ICMP echo requests and interpret latency measurements
4. **Implement** basic TCP and UDP communication channels using netcat and Python sockets
5. **Analyse** network traffic captures to identify protocol behaviour and connection states
6. **Compare** TCP and UDP communication patterns through packet capture examination
7. **Evaluate** network configurations to diagnose common connectivity problems

## Prerequisites

### Knowledge Requirements

- Basic Linux command-line proficiency (navigation, file operations, pipe redirection)
- Understanding of IP addressing concepts (IPv4, subnet notation)
- Familiarity with client-server communication model
- Elementary Python programming (variables, functions, basic I/O)

### Software Requirements

- Windows 10/11 with WSL2 enabled
- Docker Engine (in WSL)
- Portainer CE (running globally on port 9000)
- Wireshark (native Windows application)
- Python 3.11 or later
- Git (recommended)

### Hardware Requirements

- Minimum 8GB RAM (16GB recommended)
- 10GB free disk space
- Network connectivity (for initial setup only; exercises run offline)

## Quick Start

### First-Time Setup (Run Once)

```bash
# Open Ubuntu terminal (WSL)
wsl

# Navigate to the laboratory directory
cd /mnt/d/NETWORKING/WEEK1/1enWSL

# Start Docker if not running
sudo service docker start

# Verify prerequisites
python3 setup/verify_environment.py

# If any issues, run the installer helper
python3 setup/install_prerequisites.py
```

### Starting the Laboratory

```bash
# From WSL, in the 1enWSL directory
python3 scripts/start_lab.py

# Verify everything is running
python3 scripts/start_lab.py --status
```

### Accessing Services

| Service | URL/Port | Credentials |
|---------|----------|-------------|
| Portainer | http://localhost:9000 | stud / studstudstud |
| Network Lab Container | Shell via Docker | N/A |
| TCP Test Server | localhost:9090 | N/A |
| UDP Test Server | localhost:9091 | N/A |

## Laboratory Exercises

### Exercise 1: Network Interface Inspection

**Objective:** Examine local network configuration and understand interface states

**Duration:** 15 minutes

**Steps:**

1. Open a terminal in the lab container:
   ```bash
   docker exec -it week1_lab bash
   ```

2. Display all network interfaces:
   ```bash
   ip addr show
   ip -br a  # brief format
   ```

3. Examine the routing table:
   ```bash
   ip route show
   ip r  # short form
   ```

4. Document your findings:
   - Primary interface name and IP address
   - Default gateway address
   - Subnet mask in CIDR notation

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 1
```

### Exercise 2: Connectivity Testing with Ping

**Objective:** Validate network connectivity at multiple levels and measure latency

**Duration:** 20 minutes

**Steps:**

1. Test loopback connectivity (TCP/IP stack verification):
   ```bash
   ping -c 4 127.0.0.1
   ```

2. Test gateway connectivity:
   ```bash
   ping -c 4 $(ip route | grep default | awk '{print $3}')
   ```

3. Run the Python latency measurement exercise:
   ```bash
   python3 src/exercises/ex_1_01_ping_latency.py --host 127.0.0.1 --count 5
   ```

4. Record the average RTT (Round-Trip Time) for each target

**Expected Output:**
```
PING host=127.0.0.1 tx=5 rx=5 avg_rtt=0.045 ms
```

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 2
```

### Exercise 3: TCP Communication with Netcat

**Objective:** Establish bidirectional TCP communication and observe connection states

**Duration:** 25 minutes

**Steps:**

1. Open two terminal sessions in the lab container

2. In Terminal 1, start a TCP server:
   ```bash
   nc -l -p 9090
   ```

3. In Terminal 2, connect as a client:
   ```bash
   nc localhost 9090
   ```

4. Exchange messages between terminals and observe bidirectional flow

5. In a third terminal, examine the connection state:
   ```bash
   ss -tnp | grep 9090
   ```

6. Run the Python TCP exercise:
   ```bash
   python3 src/exercises/ex_1_02_tcp_server_client.py --port 9095
   ```

**Expected Observations:**
- Two ESTABLISHED connections visible in `ss` output
- Messages appear in both terminals
- Connection terminates cleanly with Ctrl+C

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 3
```

### Exercise 4: Traffic Capture and Analysis

**Objective:** Capture network packets and analyse TCP handshake

**Duration:** 30 minutes

**Steps:**

1. Start packet capture:
   ```bash
   python3 scripts/capture_traffic.py --interface lo --port 9090 --output pcap/ex4_capture.pcap &
   ```

2. Generate TCP traffic:
   ```bash
   # Terminal 1
   nc -l -p 9090
   
   # Terminal 2
   echo "Test message for capture" | nc localhost 9090
   ```

3. Stop capture (Ctrl+C) and analyse:
   ```bash
   tshark -r pcap/ex4_capture.pcap
   ```

4. Identify the TCP three-way handshake packets:
   ```bash
   tshark -r pcap/ex4_capture.pcap -Y "tcp.flags.syn==1"
   ```

5. Export to CSV for processing:
   ```bash
   tshark -r pcap/ex4_capture.pcap -T fields \
       -e frame.number -e frame.time_relative \
       -e ip.src -e ip.dst \
       -e tcp.srcport -e tcp.dstport \
       -e tcp.flags.str \
       -E header=y -E separator=, > artifacts/capture_analysis.csv
   ```

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 4
```

### Exercise 5: PCAP Statistical Analysis

**Objective:** Process captured traffic programmatically using Python

**Duration:** 20 minutes

**Steps:**

1. Ensure you have a capture file from Exercise 4

2. Run the PCAP statistics exercise:
   ```bash
   python3 src/exercises/ex_1_04_pcap_stats.py --input pcap/ex4_capture.pcap
   ```

3. Parse the CSV export:
   ```bash
   python3 src/exercises/ex_1_03_parse_csv.py --input artifacts/capture_analysis.csv
   ```

4. Document the following metrics:
   - Total packet count
   - Conversation duration
   - Bytes transmitted

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 5
```

## Demonstrations

### Demo 1: Complete Network Diagnostic Sequence

This automated demonstration shows a professional diagnostic workflow:

```bash
python3 scripts/run_demo.py --demo 1
```

**What to observe:**
- Interface enumeration and state verification
- Routing table interpretation
- Progressive connectivity testing (loopback → gateway → external)
- Socket state inspection

### Demo 2: TCP vs UDP Comparison

Demonstrates the fundamental differences between connection-oriented and connectionless transport:

```bash
python3 scripts/run_demo.py --demo 2
```

**What to observe:**
- TCP requires three-way handshake before data transfer
- UDP sends data immediately without connection establishment
- TCP provides delivery confirmation; UDP does not
- Packet overhead differences between protocols

## Packet Capture and Analysis

### Capturing Traffic

```bash
# Start capture with Python helper
python3 scripts/capture_traffic.py --interface eth0 --output pcap/week1_capture.pcap

# Or use tcpdump directly in container
docker exec week1_lab tcpdump -i any -w /work/pcap/capture.pcap
```

### Opening Captures in Wireshark (Windows)

1. Navigate to the `pcap/` directory
2. Double-click any `.pcap` file to open in Wireshark
3. Apply display filters as needed

### Suggested Wireshark Filters

```
# TCP traffic only
tcp

# Specific port
tcp.port == 9090

# TCP handshake packets (SYN flag set)
tcp.flags.syn == 1

# Packets with payload data
tcp.len > 0

# ICMP (ping) traffic
icmp

# Filter by IP address
ip.addr == 127.0.0.1
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
# Remove all containers, networks and volumes for this week
python3 scripts/cleanup.py --full

# Verify cleanup
docker system df
```

## 📚 Pedagogical Resources

This laboratory kit includes evidence-based teaching materials to support your learning:

### For Self-Study

| Resource | Purpose | Location |
|----------|---------|----------|
| [Glossary](docs/glossary.md) | Technical terms and definitions | `docs/glossary.md` |
| [Concept Analogies](docs/concept_analogies.md) | Real-world analogies for networking concepts | `docs/concept_analogies.md` |
| [Common Misconceptions](docs/misconceptions.md) | Frequent errors and how to avoid them | `docs/misconceptions.md` |
| [Code Tracing](docs/code_tracing.md) | Practice tracing through code mentally | `docs/code_tracing.md` |

### For Classroom Activities

| Resource | Purpose | Location |
|----------|---------|----------|
| [Peer Instruction Questions](docs/peer_instruction.md) | MCQ questions for class voting and discussion | `docs/peer_instruction.md` |
| [Pair Programming Guide](docs/pair_programming_guide.md) | Structured collaborative exercises | `docs/pair_programming_guide.md` |

### Recommended Study Sequence

1. **Before lab:** Read `docs/theory_summary.md` and `docs/glossary.md`
2. **During lab:** Use prediction prompts in exercises; work in pairs when possible
3. **After lab:** Review `docs/misconceptions.md` to check your understanding
4. **For practice:** Try the exercises in `docs/code_tracing.md`

---

## Homework Assignments

See the `homework/` directory for take-home exercises.

### Assignment 1: Network Documentation

Create a detailed network configuration report for your home or university network. Document interfaces, routes and connectivity test results using the techniques from Exercise 1 and 2.

### Assignment 2: Protocol Analysis

Capture and analyse a complete HTTP transaction (use `curl` or a web browser). Identify all TCP connection phases: establishment, data transfer and termination. Submit annotated screenshots and the PCAP file.

## Troubleshooting

### Common Issues

#### Issue: Docker containers fail to start
**Solution:** Ensure Docker is running in WSL. Run `sudo service docker start` and verify with `docker info`.

#### Issue: Permission denied when running scripts
**Solution:** Run `chmod +x scripts/*.py` or execute with `python3 scripts/script_name.py` explicitly.

#### Issue: Netcat connection refused
**Solution:** Verify the server is running with `ss -tlnp | grep PORT`. Ensure no firewall is blocking local connections.

#### Issue: No packets captured
**Solution:** Verify the correct interface with `ip link show`. Use `-i any` to capture on all interfaces. Ensure traffic is being generated during capture.

#### Issue: tshark permission denied
**Solution:** Either run as root in the container or add user to the `wireshark` group: `sudo usermod -aG wireshark $USER`

#### Issue: Python import errors
**Solution:** Ensure you have installed requirements: `pip install -r setup/requirements.txt --break-system-packages`

See `docs/troubleshooting.md` for additional solutions.

## Theoretical Background

### The TCP/IP Network Model

Modern networks operate according to a layered architecture where each layer provides services to the layer above. This laboratory focuses primarily on the Transport Layer (TCP/UDP) and Network Layer (IP), with observation of their interactions.

### The Three-Way Handshake

TCP connection establishment follows a precise sequence:
1. **SYN** - Client initiates connection request
2. **SYN-ACK** - Server acknowledges and responds
3. **ACK** - Client confirms, connection established

This mechanism ensures both parties are ready to communicate before data transfer begins.

### Socket States

Network sockets transition through defined states:
- **LISTEN** - Server awaiting connections
- **ESTABLISHED** - Active bidirectional communication
- **TIME_WAIT** - Connection closed, awaiting timeout
- **CLOSE_WAIT** - Remote side initiated close

Understanding these states is key to diagnosing connection problems.

## References

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (7th ed.). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress.
- Stevens, W. R. (1994). *TCP/IP Illustrated, Volume 1*. Addison-Wesley.
- Fall, K. & Stevens, W. R. (2011). *TCP/IP Illustrated, Volume 1* (2nd ed.). Addison-Wesley.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    Windows 10/11 Host                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                 WSL2 + Ubuntu 22.04                       │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │              Docker Engine                          │  │  │
│  │  │  ┌────────────────────────────────────────────┐    │  │  │
│  │  │  │          week1_lab Container               │    │  │  │
│  │  │  │                                            │    │  │  │
│  │  │  │  ┌─────────┐  ┌─────────┐  ┌─────────┐   │    │  │  │
│  │  │  │  │  ping   │  │ netcat  │  │ tcpdump │   │    │  │  │
│  │  │  │  └────┬────┘  └────┬────┘  └────┬────┘   │    │  │  │
│  │  │  │       │            │            │        │    │  │  │
│  │  │  │  ┌────┴────────────┴────────────┴────┐   │    │  │  │
│  │  │  │  │      Network Stack (lo/eth0)      │   │    │  │  │
│  │  │  │  └───────────────────────────────────┘   │    │  │  │
│  │  │  │                                            │    │  │  │
│  │  │  │  Ports: 9090 (TCP), 9091 (UDP)           │    │  │  │
│  │  │  └────────────────────────────────────────────┘    │  │  │
│  │  │                                                     │  │  │
│  │  │  Network: week1_network (bridge, 172.20.1.0/24)    │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  │                                                           │  │
│  │  ┌────────────────┐                                      │  │
│  │  │   Portainer    │ (Global service, port 9000)          │  │
│  │  └────────────────┘                                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌────────────────┐                                           │
│  │   Wireshark    │ (native Windows - captures vEthernet WSL) │
│  └────────────────┘                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Extended Troubleshooting

### Docker Issues

**Problem:** "Cannot connect to Docker daemon"
```bash
sudo service docker start
docker ps  # Verify it works
```

**Problem:** Permission denied when running docker
```bash
sudo usermod -aG docker $USER
newgrp docker
# Or logout and login again
```

**Problem:** Docker service won't start
```bash
sudo service docker status  # Check status
sudo dockerd  # Run manually to see errors
```

**Problem:** Docker commands work but containers can't access network
```bash
# Check Docker network configuration
docker network ls
docker network inspect week1_network

# Verify WSL network adapter
ip addr show eth0
```

### Portainer Issues

**Problem:** Cannot access http://localhost:9000
```bash
# Check if Portainer container exists and is running
docker ps -a | grep portainer

# If stopped, start it
docker start portainer

# If doesn't exist, create it
docker run -d -p 9000:9000 --name portainer --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data portainer/portainer-ce:latest
```

**Problem:** Forgot Portainer password
```bash
# Reset Portainer (loses settings but not containers)
docker stop portainer
docker rm portainer
docker volume rm portainer_data
# Recreate with command above, set new password
```

**Problem:** Portainer shows "Unable to connect to Docker"
```bash
# Verify Docker socket permissions
ls -la /var/run/docker.sock

# Restart Portainer with correct socket
docker stop portainer
docker rm portainer
docker run -d -p 9000:9000 --name portainer --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data portainer/portainer-ce:latest
```

### WSL Issues

**Problem:** WSL not starting or Ubuntu not available
```powershell
# In PowerShell (Administrator)
wsl --status
wsl --list --verbose

# If Ubuntu not installed
wsl --install -d Ubuntu-22.04
```

**Problem:** WSL2 shows as version 1
```powershell
# Convert to WSL2
wsl --set-version Ubuntu-22.04 2
```

**Problem:** Cannot access Windows files from WSL
```bash
# Verify mount points
ls /mnt/
# Should show: c, d, etc.

# If missing, restart WSL
wsl --shutdown  # From PowerShell
# Then reopen Ubuntu
```

### Wireshark Issues

**Problem:** No packets captured
- ✅ Verify correct interface selected (vEthernet WSL)
- ✅ Ensure traffic is being generated DURING capture
- ✅ Check display filter isn't hiding packets (clear filter)
- ✅ Try "Capture → Options" and enable promiscuous mode

**Problem:** "No interfaces found" or permission error
- Run Wireshark as Administrator (right-click → Run as administrator)
- Reinstall Npcap with "WinPcap API-compatible Mode" option checked

**Problem:** Can't see Docker container traffic
- Select `vEthernet (WSL)` interface, not `Ethernet` or `Wi-Fi`
- Ensure containers are on bridge network, not host network

**Problem:** vEthernet (WSL) not visible
```powershell
# Restart Hyper-V networking (PowerShell Administrator)
Get-NetAdapter | Where-Object {$_.Name -like "*WSL*"}

# If missing, restart WSL completely
wsl --shutdown
# Wait 10 seconds, then start Ubuntu again
```

### Network Issues

**Problem:** Container can't reach internet
```bash
# Check Docker network
docker network ls
docker network inspect week1_network

# Check DNS in container
docker exec week1_lab cat /etc/resolv.conf

# Test DNS resolution
docker exec week1_lab nslookup google.com
```

**Problem:** Port already in use
```bash
# Find what's using the port
sudo netstat -tlnp | grep 9090
# Or
sudo ss -tlnp | grep 9090

# Kill the process or use different port
sudo kill <PID>
```

**Problem:** Cannot connect to container ports from Windows
```bash
# Verify container is running and ports are mapped
docker ps

# Check port binding
docker inspect week1_lab | grep -A 20 "PortBindings"

# Test from WSL
curl -v localhost:9090
```

### Python Issues

**Problem:** ModuleNotFoundError for docker/scapy/etc.
```bash
# Install with break-system-packages flag (required on Ubuntu 22.04+)
pip install docker scapy dpkt pyyaml --break-system-packages

# Or use pip3 explicitly
pip3 install -r setup/requirements.txt --break-system-packages
```

**Problem:** Python version mismatch
```bash
# Check installed Python version
python3 --version

# If < 3.11, install newer version
sudo apt update
sudo apt install python3.11 python3.11-venv

# Use python3.11 explicitly
python3.11 scripts/start_lab.py
```

---

## 🧹 Complete Cleanup Procedure

### End of Session (Quick)

```bash
# Stop lab containers (Portainer stays running!)
cd /mnt/d/NETWORKING/WEEK1/1enWSL
docker compose -f docker/docker-compose.yml down

# Verify - should still show portainer
docker ps
```

### End of Week (Thorough)

```bash
# Remove this week's containers and networks
docker compose -f docker/docker-compose.yml down --volumes

# Remove unused images
docker image prune -f

# Remove unused networks
docker network prune -f

# Check disk usage
docker system df
```

### Full Reset (Before New Semester)

```bash
# WARNING: This removes EVERYTHING except Portainer
docker stop $(docker ps -q | grep -v $(docker ps -q --filter name=portainer)) 2>/dev/null
docker rm $(docker ps -aq | grep -v $(docker ps -aq --filter name=portainer)) 2>/dev/null
docker image prune -a -f
docker network prune -f
docker volume prune -f

# Verify Portainer still running
docker ps
```

**⚠️ NEVER run `docker system prune -a` without excluding Portainer!**

### Selective Cleanup Commands

```bash
# Remove only week1 resources
docker stop week1_lab 2>/dev/null
docker rm week1_lab 2>/dev/null
docker network rm week1_network 2>/dev/null

# Remove dangling images only
docker image prune -f

# View what would be removed (dry run)
docker system prune --dry-run
```

---

## 📊 Week 1 Network Configuration Summary

| Resource | Value | Notes |
|----------|-------|-------|
| Subnet | 172.20.1.0/24 | Week 1 dedicated subnet |
| Gateway | 172.20.1.1 | Docker bridge gateway |
| Lab Container IP | Assigned by DHCP | Check with `ip addr` |
| TCP Port | 9090 | Test server |
| UDP Port | 9091 | Test server |
| Alternative Port | 9092 | Additional testing |
| Portainer | 9000 | **RESERVED - Global service** |

---

*NETWORKING class - ASE, Informatics | by Revolvix*
*Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment*
