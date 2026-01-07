# Week 1: Fundamentals of Computer Networks

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
>
> by Revolvix

---

## ⚠️ Environment Notice

This laboratory kit is designed for the **WSL2 + Ubuntu 22.04 + Docker + Portainer** environment.

**Repository:** https://github.com/antonioclim/netENwsl

---

## Environment Verification

Before starting this lab, verify your environment is properly configured.

### From Windows PowerShell:

```powershell
# Check WSL status - Ubuntu-22.04 should be default
wsl --status
# Expected: Default Distribution: Ubuntu-22.04

# Check Docker is accessible via WSL
wsl docker ps
# Expected: At minimum, "portainer" container running

# Check Portainer is accessible
curl http://localhost:9000
# Expected: HTML response (Portainer UI)
```

### From Ubuntu Terminal (WSL):

```bash
# Start Docker service if not running
sudo service docker start

# Verify Portainer is running
docker ps --filter name=portainer
# Expected: portainer container with status "Up"

# Verify Docker version
docker --version
# Expected: Docker version 28.x or higher
```

### Access Points

| Service | URL/Port | Credentials |
|---------|----------|-------------|
| **Portainer** | http://localhost:9000 | `stud` / `studstudstud` |
| Network Lab Container | Shell via Docker | N/A |
| TCP Test Server | localhost:9090 | N/A |
| UDP Test Server | localhost:9091 | N/A |

> **Note:** Portainer runs as a global service (not per-lab). It's always available at port 9000.

---

## Overview

This laboratory introduces the foundational concepts of computer networking through hands-on experimentation with essential diagnostic tools. The session establishes the critical skills required for network troubleshooting and analysis that will serve as the cornerstone for all subsequent laboratory work.

Computer networks permeate every aspect of modern computing infrastructure. Understanding how to diagnose connectivity issues, inspect network configurations, and analyse traffic flows represents essential competencies for any computing professional. This week focuses on developing practical intuition about network behaviour through direct observation and measurement.

The exercises progress from basic interface inspection through connectivity validation to traffic capture and protocol analysis. Students will work with industry-standard tools including `ip`, `ss`, `ping`, `netcat`, `tcpdump`, and `tshark`, developing the diagnostic vocabulary necessary for effective network administration.

---

## Learning Objectives

By the end of this laboratory session, you will be able to:

1. **Recall** the essential Linux networking commands and their primary functions, including `ip addr`, `ip route`, `ss`, `ping`, and `netcat`
2. **Explain** the purpose of network interfaces, routing tables, and socket states in a Linux environment
3. **Demonstrate** connectivity testing using ICMP echo requests and interpret latency measurements
4. **Implement** basic TCP and UDP communication channels using netcat and Python sockets
5. **Analyse** network traffic captures to identify protocol behaviour and connection states
6. **Compare** TCP and UDP communication patterns through packet capture examination
7. **Evaluate** network configurations to diagnose common connectivity problems

---

## Prerequisites

### Knowledge Requirements

- Basic Linux command-line proficiency (navigation, file operations, pipe redirection)
- Understanding of IP addressing concepts (IPv4, subnet notation)
- Familiarity with client-server communication model
- Elementary Python programming (variables, functions, basic I/O)

### Software Requirements (Pre-installed)

Your environment should already have:

- ✅ Windows 10/11 with WSL2 enabled
- ✅ Ubuntu 22.04 LTS (default WSL distribution)
- ✅ Docker Engine in WSL (NOT Docker Desktop)
- ✅ Portainer CE running on port 9000
- ✅ Wireshark (native Windows application)
- ✅ Python 3.11+ with packages: docker, scapy, dpkt

If any of these are missing, see the [Prerequisites Documentation](../PREREQUISITES_EN.md).

### Standard Credentials

| Service | Username | Password |
|---------|----------|----------|
| Ubuntu WSL | `stud` | `stud` |
| Portainer | `stud` | `studstudstud` |

---

## Quick Start

### Step 1: Open Ubuntu Terminal

From Windows, either:
- Click "Ubuntu" in Start menu, or
- In PowerShell, type: `wsl`

### Step 2: Navigate to Lab Directory

```bash
# If you cloned to D:/NETWORKING/
cd /mnt/d/NETWORKING/WEEK1
```

### Step 3: Verify Prerequisites

```bash
python setup/verify_environment.py
```

All checks should pass. If any fail, resolve them before proceeding.

### Step 4: Start the Laboratory

```bash
# Ensure Docker is running
sudo service docker start

# Start lab containers
python scripts/start_lab.py
```

### Step 5: Verify Everything is Running

```bash
# Check lab containers
docker ps

# Expected output should show:
# - week1_lab (the laboratory container)
# - portainer (global management interface)
```

---

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
python tests/test_exercises.py --exercise 1
```

---

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
   python src/exercises/ex_1_01_ping_latency.py --host 127.0.0.1 --count 5
   ```

4. Record the average RTT (Round-Trip Time) for each target

**Expected Output:**
```
PING host=127.0.0.1 tx=5 rx=5 avg_rtt=0.045 ms
```

**Verification:**
```bash
python tests/test_exercises.py --exercise 2
```

---

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
   python src/exercises/ex_1_02_tcp_server_client.py --port 9095
   ```

**Expected Observations:**
- Two ESTABLISHED connections visible in `ss` output
- Messages appear in both terminals
- Connection terminates cleanly with Ctrl+C

**Verification:**
```bash
python tests/test_exercises.py --exercise 3
```

---

### Exercise 4: Traffic Capture and Analysis

**Objective:** Capture network packets and analyse TCP handshake

**Duration:** 30 minutes

**Steps:**

1. Start packet capture:
   ```bash
   python scripts/capture_traffic.py --interface lo --port 9090 --output pcap/ex4_capture.pcap &
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

**Wireshark Analysis (Windows):**

Open Wireshark, start capture on `vEthernet (WSL)` interface, then generate traffic as above. Use filter: `tcp.port == 9090`

**Verification:**
```bash
python tests/test_exercises.py --exercise 4
```

---

### Exercise 5: PCAP Statistical Analysis

**Objective:** Process captured traffic programmatically using Python

**Duration:** 20 minutes

**Steps:**

1. Ensure you have a capture file from Exercise 4

2. Run the PCAP statistics exercise:
   ```bash
   python src/exercises/ex_1_04_pcap_stats.py --input pcap/ex4_capture.pcap
   ```

3. Parse the CSV export:
   ```bash
   python src/exercises/ex_1_03_parse_csv.py --input artifacts/capture_analysis.csv
   ```

4. Document the following metrics:
   - Total packet count
   - Conversation duration
   - Bytes transmitted

**Verification:**
```bash
python tests/test_exercises.py --exercise 5
```

---

## Demonstrations

### Demo 1: Complete Network Diagnostic Sequence

This automated demonstration shows a professional diagnostic workflow:

```bash
python scripts/run_demo.py --demo 1
```

**What to observe:**
- Interface enumeration and state verification
- Routing table interpretation
- Progressive connectivity testing (loopback → gateway → external)
- Socket state inspection

### Demo 2: TCP vs UDP Comparison

Demonstrates the fundamental differences between connection-oriented and connectionless transport:

```bash
python scripts/run_demo.py --demo 2
```

**What to observe:**
- TCP requires three-way handshake before data transfer
- UDP sends data immediately without connection establishment
- TCP provides delivery confirmation; UDP does not
- Packet overhead differences between protocols

---

## Packet Capture and Analysis

### Capturing Traffic Inside Container

```bash
# Start capture with Python helper
python scripts/capture_traffic.py --interface eth0 --output pcap/week1_capture.pcap

# Or use tcpdump directly in container
docker exec week1_lab tcpdump -i any -w /work/pcap/capture.pcap
```

### Capturing Traffic with Wireshark (Windows)

1. Open Wireshark from Start menu
2. Select interface: **vEthernet (WSL)** or **vEthernet (WSL) (Hyper-V firewall)**
3. Start capture
4. Generate traffic in lab container
5. Stop capture and analyse

### Opening Captures in Wireshark

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

---

## Cleanup

After completing the lab, clean up resources:

```bash
# Stop lab containers (Portainer keeps running!)
docker-compose -f docker/docker-compose.yml down

# Remove lab networks (if created)
docker network prune -f

# Remove lab images (optional, saves space)
docker image prune -f
```

**⚠️ Important:** Always keep Portainer running for other labs!

```bash
# NEVER do this (unless you want to stop Portainer):
# docker stop portainer

# Verify Portainer is still running:
docker ps --filter name=portainer
```

### Full Cleanup (Before Next Week)

```bash
# Remove all containers, networks for this week
python scripts/cleanup.py --full

# Verify cleanup
docker system df
```

---

## Homework Assignments

See the `homework/` directory for take-home exercises.

### Assignment 1: Network Documentation

Create a comprehensive network configuration report for your home or university network. Document interfaces, routes, and connectivity test results using the techniques from Exercise 1 and 2.

### Assignment 2: Protocol Analysis

Capture and analyse a complete HTTP transaction (use `curl` or a web browser). Identify all TCP connection phases: establishment, data transfer, and termination. Submit annotated screenshots and the PCAP file.

---

## Troubleshooting

### Common Issues

#### Issue: Docker service not running in WSL
**Solution:**
```bash
sudo service docker start
docker ps  # Verify it works
```

#### Issue: "Cannot connect to Docker daemon"
**Solution:** Docker service isn't running. Start it:
```bash
sudo service docker start
```

#### Issue: Permission denied when running docker
**Solution:** Your user isn't in the docker group:
```bash
sudo usermod -aG docker $USER
newgrp docker
```

#### Issue: Portainer not accessible at localhost:9000
**Solution:** Portainer container might be stopped:
```bash
docker start portainer
# Or redeploy if it doesn't exist:
docker run -d -p 9000:9000 --name portainer --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data portainer/portainer-ce:latest
```

#### Issue: Lab container won't start
**Solution:** Check for port conflicts:
```bash
docker ps -a
netstat -tlnp | grep -E "9090|9091|9092"
```

#### Issue: Netcat connection refused
**Solution:** Verify the server is running with `ss -tlnp | grep PORT`. Ensure no firewall is blocking local connections.

#### Issue: No packets captured in Wireshark
**Solution:**
- Ensure you're capturing on `vEthernet (WSL)` interface
- Generate traffic while capturing
- Check display filter isn't too restrictive

#### Issue: Python import errors
**Solution:** Ensure you have installed requirements:
```bash
pip install -r setup/requirements.txt --break-system-packages
```

See `docs/troubleshooting.md` for additional solutions.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         WINDOWS 11                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   Wireshark     │  │    Browser      │  │   PowerShell    │  │
│  │   (Capture)     │  │  (Portainer)    │  │   (Commands)    │  │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘  │
│           │                    │                    │           │
│           │              localhost:9000             │           │
│           ▼                    ▼                    ▼           │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              vEthernet (WSL) - Virtual Network              ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│  ┌───────────────────────────┴───────────────────────────────┐  │
│  │                        WSL2                                │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │                  Ubuntu 22.04 LTS                    │  │  │
│  │  │  ┌─────────────────────────────────────────────┐    │  │  │
│  │  │  │              Docker Engine                   │    │  │  │
│  │  │  │                                              │    │  │  │
│  │  │  │  ┌──────────────┐    ┌──────────────┐      │    │  │  │
│  │  │  │  │  week1_lab   │    │  portainer   │      │    │  │  │
│  │  │  │  │  Container   │    │  (global)    │      │    │  │  │
│  │  │  │  │              │    │  :9000       │      │    │  │  │
│  │  │  │  │ Ports:       │    └──────────────┘      │    │  │  │
│  │  │  │  │ 9090 (TCP)   │                          │    │  │  │
│  │  │  │  │ 9091 (UDP)   │                          │    │  │  │
│  │  │  │  │ 9092 (alt)   │                          │    │  │  │
│  │  │  │  └──────────────┘                          │    │  │  │
│  │  │  │                                              │    │  │  │
│  │  │  │         Docker Networks                     │    │  │  │
│  │  │  │   week1_network (172.20.1.0/24)            │    │  │  │
│  │  │  └─────────────────────────────────────────────┘    │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

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

Understanding these states is essential for diagnosing connection problems.

---

## References

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (7th ed.). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress.
- Stevens, W. R. (1994). *TCP/IP Illustrated, Volume 1*. Addison-Wesley.
- Fall, K. & Stevens, W. R. (2011). *TCP/IP Illustrated, Volume 1* (2nd ed.). Addison-Wesley.

---

*NETWORKING class - ASE, Informatics | by Revolvix*

*Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment*
