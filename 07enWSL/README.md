# Week 7: Packet Interception, Filtering and Defensive Port Probing

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
> 
> by Revolvix

---

## ⚠️ Environment Notice

This laboratory kit is designed for the **WSL2 + Ubuntu 22.04 + Docker + Portainer** environment.

**Repository:** https://github.com/antonioclim/netENwsl
**This Week's Folder:** `7enWSL`

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

# Clone Week 7
git clone https://github.com/antonioclim/netENwsl.git WEEK7
cd WEEK7
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
git clone https://github.com/antonioclim/netENwsl.git WEEK7
cd WEEK7
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
cd /mnt/d/NETWORKING/WEEK7/7enWSL
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

### Week 7 Network Configuration

Navigate: **Networks → week7net**

Current configuration:
- Subnet: 10.0.7.0/24
- Gateway: 10.0.7.1
- TCP Server: 10.0.7.100
- UDP Receiver: 10.0.7.200

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

### Essential Wireshark Filters for Week 7

| Filter | Purpose |
|--------|---------|
| `tcp.port == 9090` | TCP Echo server traffic |
| `udp.port == 9091` | UDP Receiver traffic |
| `tcp.flags.syn == 1 && tcp.flags.ack == 0` | TCP connection attempts |
| `tcp.flags.reset == 1` | Reset packets (REJECT) |
| `icmp.type == 3` | ICMP unreachable messages |
| `ip.addr == 10.0.7.11 && ip.addr == 10.0.7.200` | Traffic between specific hosts |

### Analysing Filtering Effects

1. **REJECT action**: Look for TCP RST or ICMP Type 3 packets
2. **DROP action**: Look for missing responses, client timeouts
3. **Permitted traffic**: Complete TCP handshake or UDP exchange

### Saving Captures

1. **File → Save As**
2. Navigate to: `D:\NETWORKING\WEEK7\pcap\`
3. Filename: `capture_exercise_N.pcap`

---

## Overview

This laboratory session explores the practical foundations of network traffic observation and policy enforcement at the packet level. The week builds upon your understanding of TCP/IP fundamentals and socket programming, introducing the critical skill of capturing and analysing real network traffic as forensic evidence. You will learn to distinguish between application-layer behaviour and network-layer phenomena, a distinction that proves essential when debugging distributed systems in production environments.

If this is your first time working with packet captures, expect some initial confusion about interface selection and filter syntax. That's normal — by the end of the session, these tools become second nature.

The seminar component focuses on packet filtering and defensive port probing techniques. Filtering rules transform abstract security policies into concrete, enforceable decisions at the network boundary. Rather than treating firewalls as opaque infrastructure, you will construct and verify filtering rules programmatically, understanding exactly why a connection succeeds or fails. This approach prepares you for container networking, reverse proxies and incident response scenarios covered in subsequent weeks.

All exercises operate within an isolated laboratory network created by Docker containers or Mininet topologies. The kit emphasises reproducibility: every observation you make should be backed by packet captures and logs that another engineer could verify independently.

## Learning Objectives

By the end of this laboratory session, you will be able to:

1. **Identify** TCP and UDP packet fields in captured traffic using tcpdump and Wireshark filters
2. **Explain** the difference between application-layer failures and network-layer filtering effects using concrete packet evidence
3. **Implement** IP-based allow and block filtering rules using iptables profiles and verify their effect with repeatable tests
4. **Analyse** packet captures to determine root causes of connection timeouts, resets and drops
5. **Design** custom firewall profiles that enforce specific traffic policies whilst maintaining baseline connectivity
6. **Evaluate** the trade-offs between DROP and REJECT filtering actions for debugging and security purposes

## Prerequisites

### Knowledge Requirements

- TCP three-way handshake mechanics (SYN, SYN-ACK, ACK)
- UDP connectionless transmission model
- IPv4 addressing and basic subnetting (covered in Week 5)
- Socket programming fundamentals from Weeks 2-4
- Basic command-line proficiency

### Software Requirements

- Windows 10/11 with WSL2 enabled
- Docker Engine (in WSL)
- Portainer CE (running globally on port 9000)
- Wireshark (native Windows installation)
- Python 3.11 or later
- Git (recommended)

### Hardware Requirements

- Minimum 8GB RAM (16GB recommended)
- 10GB free disk space
- Network connectivity for initial setup

## Quick Start

### First-Time Setup (Run Once)

```bash
# Open Ubuntu terminal (WSL)
wsl

# Navigate to the kit directory
cd /mnt/d/NETWORKING/WEEK7/7enWSL

# Start Docker if not running
sudo service docker start

# Verify prerequisites
python3 setup/verify_environment.py

# If any issues, run the installer helper
python3 setup/install_prerequisites.py

# Configure Docker for this week's requirements
python3 setup/configure_docker.py
```

### Starting the Laboratory

```bash
# Start all services
python3 scripts/start_lab.py

# Verify everything is running
python3 scripts/start_lab.py --status
```

### Accessing Services

| Service | URL/Port | Credentials |
|---------|----------|-------------|
| Portainer | http://localhost:9000 | stud / studstudstud |
| TCP Echo Server | localhost:9090 | None |
| UDP Echo Receiver | localhost:9091 | None |
| Packet Filter Proxy | localhost:8888 | None (when enabled) |

## Laboratory Exercises

### Exercise 1: Baseline Traffic Capture

**Objective:** Establish baseline TCP and UDP connectivity and capture evidence of successful communication.

**Duration:** 20 minutes

**Steps:**

1. Start the laboratory environment:
   ```bash
   python3 scripts/start_lab.py
   ```

2. In a separate terminal, begin traffic capture:
   ```bash
   python3 scripts/capture_traffic.py --interface any --output pcap/ex1_baseline.pcap --duration 60
   ```

3. Run the baseline demonstration:
   ```bash
   python3 scripts/run_demo.py --demo baseline
   ```

4. Examine the captured traffic using Wireshark:
   - Open `pcap/ex1_baseline.pcap`
   - Apply filter: `tcp.port == 9090`
   - Identify the three-way handshake (SYN, SYN-ACK, ACK)
   - Locate the echo request and response payloads

5. Repeat for UDP traffic:
   - Apply filter: `udp.port == 9091`
   - Note the absence of connection establishment overhead

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 1
```

**Expected Observations:**
- TCP stream shows complete handshake before data transfer
- UDP packets appear immediately without setup phase
- Both protocols successfully echo the test message

### Exercise 2: TCP Filtering with REJECT

**Objective:** Apply a filtering rule that blocks TCP connections to port 9090 and observe the client-side failure mode.

**Duration:** 25 minutes

**Steps:**

1. Ensure the baseline is working:
   ```bash
   python3 scripts/run_demo.py --demo baseline
   ```

2. Apply the TCP blocking profile:
   ```bash
   python3 src/apps/firewallctl.py --profile block_tcp_9090 --dry-run
   python3 src/apps/firewallctl.py --profile block_tcp_9090
   ```

3. Capture traffic whilst testing the blocked connection:
   ```bash
   python3 scripts/capture_traffic.py --output pcap/ex2_tcp_blocked.pcap --duration 30
   ```

4. In another terminal, attempt the TCP connection:
   ```bash
   python3 src/apps/tcp_client.py --host localhost --port 9090 --message "blocked_test" --timeout 5
   ```

5. Stop the capture and analyse in Wireshark:
   - Look for ICMP "Destination Unreachable" or TCP RST packets
   - Compare the timing to the baseline capture

6. Verify UDP still works:
   ```bash
   python3 scripts/run_demo.py --demo udp_only
   ```

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 2
```

**Expected Observations:**
- Client receives immediate feedback (connection refused)
- ICMP or RST packets visible in the capture
- UDP traffic unaffected by the TCP rule

### Exercise 3: UDP Filtering with DROP

**Objective:** Apply a DROP rule to UDP port 9091 and contrast the failure mode with REJECT.

**Duration:** 25 minutes

**Steps:**

1. Restore baseline first:
   ```bash
   python3 src/apps/firewallctl.py --profile baseline
   ```

2. Apply the UDP drop profile:
   ```bash
   python3 src/apps/firewallctl.py --profile block_udp_9091
   ```

3. Capture and test:
   ```bash
   python3 scripts/capture_traffic.py --output pcap/ex3_udp_dropped.pcap --duration 30
   ```

4. Attempt UDP communication:
   ```bash
   python3 src/apps/udp_sender.py --host localhost --port 9091 --message "dropped_test" --count 3
   ```

5. Observe the receiver timeout behaviour and capture contents

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 3
```

**Key Questions:**
- How does the client behave differently with DROP vs REJECT?
- What packet evidence distinguishes a dropped packet from a lost packet?
- Which approach is better for debugging? For security?

### Exercise 4: Application-Layer Packet Filter

**Objective:** Use the user-space packet filter proxy to implement allow/block lists at the application layer.

**Duration:** 30 minutes

**Steps:**

1. Start the TCP server on port 9090:
   ```bash
   python3 src/apps/tcp_server.py --host 0.0.0.0 --port 9090 --log artifacts/tcp_server.log
   ```

2. Start the packet filter proxy:
   ```bash
   python3 src/apps/packet_filter.py --listen-port 8888 --upstream-host localhost --upstream-port 9090 --log artifacts/proxy.log
   ```

3. Test connectivity through the proxy:
   ```bash
   python3 src/apps/tcp_client.py --host localhost --port 8888 --message "via_proxy"
   ```

4. Add an allow list (blocks all other sources):
   ```bash
   python3 src/apps/packet_filter.py --listen-port 8888 --upstream-host localhost --upstream-port 9090 --allow 127.0.0.1 --log artifacts/proxy_filtered.log
   ```

5. Test from different source addresses (if available) and observe the proxy logs

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 4
```

### Exercise 5: Defensive Port Probing

**Objective:** Use controlled port probing to verify which services are accessible and which are filtered.

**Duration:** 20 minutes

**Steps:**

1. Configure a mixed filtering profile:
   ```bash
   python3 src/apps/firewallctl.py --profile mixed_filtering
   ```

2. Run the port probe:
   ```bash
   python3 src/apps/port_probe.py --host localhost --ports 22,80,443,8080,9090,9091 --timeout 1 --log artifacts/probe_results.log
   ```

3. Compare probe results against the applied profile
4. Document which ports appear open, closed, or filtered

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 5
```

## Demonstrations

### Demo 1: Complete Traffic Flow

Automated demonstration showing baseline connectivity, TCP filtering and UDP filtering in sequence.

```bash
python3 scripts/run_demo.py --demo full
```

**What to observe:**
- Console output indicating success/failure at each stage
- Log files generated in `artifacts/`
- Packet capture showing all traffic types

### Demo 2: REJECT vs DROP Comparison

Side-by-side comparison of client behaviour under different filtering actions.

```bash
python3 scripts/run_demo.py --demo reject_vs_drop
```

**What to observe:**
- Timing differences in client failure responses
- Packet evidence of each filtering mode

## Packet Capture and Analysis

### Capturing Traffic

```bash
# Start capture with automatic duration
python3 scripts/capture_traffic.py --interface any --output pcap/week7_capture.pcap --duration 120

# Or use Wireshark directly on Windows
# Open Wireshark > Select vEthernet (WSL) interface > Start capture
```

### Suggested Wireshark Filters

```
# TCP traffic to echo server
tcp.port == 9090

# UDP traffic to receiver
udp.port == 9091

# TCP connection attempts (SYN packets)
tcp.flags.syn == 1 && tcp.flags.ack == 0

# Reset packets (indicating rejection)
tcp.flags.reset == 1

# ICMP unreachable messages
icmp.type == 3

# All traffic between specific hosts
ip.addr == 10.0.7.11 && ip.addr == 10.0.7.200
```

### tshark Command-Line Analysis

```bash
# Conversation summary
tshark -r pcap/week7_capture.pcap -q -z conv,tcp

# Field extraction
tshark -r pcap/week7_capture.pcap -Y "tcp.port==9090" -T fields -e frame.time -e ip.src -e ip.dst -e tcp.flags -e tcp.len

# Packet count
tshark -r pcap/week7_capture.pcap -Y "udp.port==9091" | wc -l
```

## Shutdown and Cleanup

### End of Session

```bash
# Stop all containers (Portainer stays running!)
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

## 📚 Documentation

The `docs/` directory contains supplementary learning materials:

| Document | Purpose |
|----------|---------|
| `theory_summary.md` | Theoretical background on packet capture and filtering |
| `commands_cheatsheet.md` | Quick reference for tcpdump, tshark and iptables |
| `troubleshooting.md` | Solutions to common issues |
| `further_reading.md` | Books, RFCs and online resources |
| `peer_instruction.md` | MCQ questions for classroom discussion |
| `pair_programming_guide.md` | Collaborative exercise structure |
| `misconceptions.md` | Common errors and how to avoid them |
| `glossary.md` | Technical terms and command reference |
| `code_tracing.md` | Step-through exercises for understanding code flow |
| `parsons_problems.md` | Code reordering exercises (no syntax required) |
| `concept_analogies.md` | Real-world analogies for networking concepts |

---

## Homework Assignments

See the `homework/exercises/` directory for take-home exercises:

| File | Description |
|------|-------------|
| `hw_7_01_validate_firewall_profile.py` | Custom firewall profile design and validation |
| `hw_7_02_troubleshoot_scenarios.py` | Network failure analysis with PCAP evidence |

### Assignment 1: Custom Filtering Profile

**Script:** `python3 homework/exercises/hw_7_01_validate_firewall_profile.py`

Create a new firewall profile that blocks TCP port 9090 only from a specific source IP whilst allowing all other sources. Document your approach and provide packet capture evidence.

**Deliverables:** Modified `firewall_profiles.json`, capture file, short explanation (half page)

### Assignment 2: Failure Analysis Report

**Script:** `python3 homework/exercises/hw_7_02_troubleshoot_scenarios.py --all`

Take one filtering scenario (TCP blocked or UDP dropped) and write a structured analysis including: expected behaviour, observed packets (5-10 tshark lines), root cause explanation and recommendations for automated verification.

**Deliverables:** Markdown report, supporting capture file

## Troubleshooting

### Common Issues

#### Issue: Docker containers fail to start
**Solution:** Ensure Docker is running in WSL. Run `sudo service docker start` then `docker info` to verify.

#### Issue: Wireshark cannot capture Docker traffic
**Solution:** On Windows, capture on the `vEthernet (WSL)` interface or use tcpdump inside WSL2 and copy captures out.

#### Issue: TCP client hangs instead of failing quickly
**Solution:** Verify you are using REJECT (not DROP) in your filtering profile. Use `--timeout` flag on the client.

#### Issue: Permission denied when applying iptables rules
**Solution:** Run inside a privileged container or use `sudo` in WSL2. The Docker-based exercises handle this automatically.

#### Issue: UDP receiver shows nothing
**Solution:** Ensure the receiver starts before the sender. Check destination IP and port match exactly.

See `docs/troubleshooting.md` for additional solutions.

## Theoretical Background

### Packet Capture as Evidence

When distributed systems misbehave, application logs may be incomplete or misleading. Packet captures provide ground truth: they show exactly what crossed the wire, including retransmissions, resets and ICMP errors that applications might not log. This week's exercises establish the habit of capturing evidence before concluding that code is at fault.

### Filtering Semantics

Network filtering transforms security policies into concrete decisions at packet boundaries. The key distinction is between:

- **REJECT:** Send an explicit refusal (TCP RST or ICMP Unreachable), providing fast feedback
- **DROP:** Silently discard the packet, forcing timeouts that can mask the true cause

For debugging, REJECT is preferable. For security (concealing service existence), DROP may be appropriate.

### Reproducibility

A firewall rule should be readable (what does it do), testable (how do we verify it) and reversible (how do we undo it safely). This week's profile-based approach demonstrates declarative policy management suitable for automation.

## References

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (7th ed.). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress.
- Bejtlich, R. (2013). *The Practice of Network Security Monitoring*. No Starch Press.
- *iptables(8)* - Linux Netfilter administration manual page
- *tcpdump(1)* - Network packet analyser manual page

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        WEEK 7 Laboratory Topology                           │
│              (WSL2 + Ubuntu 22.04 + Docker + Portainer)                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────┐                           ┌─────────────────┐        │
│   │   TCP Client    │                           │   TCP Server    │        │
│   │   (src/apps/)   │                           │   Port 9090     │        │
│   └────────┬────────┘                           └────────┬────────┘        │
│            │                                             │                  │
│            │         ┌───────────────────┐              │                  │
│            │         │  Packet Filter    │              │                  │
│            ├────────▶│  Proxy (8888)     │─────────────▶│                  │
│            │         │  (Optional)       │              │                  │
│            │         └───────────────────┘              │                  │
│            │                                             │                  │
│   ┌────────┴────────────────────────────────────────────┴────────┐        │
│   │                     Docker Network (week7net)                 │        │
│   │                         10.0.7.0/24                           │        │
│   └───────────────────────────────────────────────────────────────┘        │
│            │                                             │                  │
│   ┌────────┴────────┐                           ┌────────┴────────┐        │
│   │   UDP Sender    │                           │   UDP Receiver  │        │
│   │   (src/apps/)   │──────────────────────────▶│   Port 9091     │        │
│   └─────────────────┘                           └─────────────────┘        │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────┐      │
│   │                     Filtering Layer                              │      │
│   │   iptables FORWARD chain (applied on router/firewall host)      │      │
│   │   Profiles: baseline | block_tcp_9090 | block_udp_9091          │      │
│   └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│   Portainer: http://localhost:9000 (global service)                        │
│   Credentials: stud / studstudstud                                         │
└─────────────────────────────────────────────────────────────────────────────┘
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

### WSL Issues

**Problem:** WSL not starting
```powershell
# In PowerShell (Administrator)
wsl --status
wsl --list --verbose
```

**Problem:** Cannot access Windows files from WSL
```bash
ls /mnt/
# Should show: c, d, etc.
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

### Network Issues

**Problem:** Container can't reach internet
```bash
# Check Docker network
docker network ls
docker network inspect week7net

# Check DNS in container
docker exec week7_tcp_server cat /etc/resolv.conf
```

**Problem:** Port already in use
```bash
# Find what's using the port
sudo netstat -tlnp | grep 9090
# Or
sudo ss -tlnp | grep 9090

# Kill the process or use different port
```

### Filtering-Specific Issues

**Problem:** iptables rules not applying
```bash
# Verify iptables is installed
which iptables
# Check current rules
sudo iptables -L -n -v
```

**Problem:** DROP vs REJECT confusion
- REJECT: Client sees immediate "Connection refused"
- DROP: Client experiences timeout (no response)

---

## 🧹 Complete Cleanup Procedure

### End of Session (Quick)

```bash
# Stop lab containers (Portainer stays running!)
cd /mnt/d/NETWORKING/WEEK7/7enWSL
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

---

## 📊 Week 7 Network Configuration Summary

| Resource | Value | Notes |
|----------|-------|-------|
| Network Subnet | 10.0.7.0/24 | week7net |
| Gateway | 10.0.7.1 | Docker bridge gateway |
| TCP Server IP | 10.0.7.100 | Echo server |
| TCP Client IP | 10.0.7.11 | Demo client |
| UDP Receiver IP | 10.0.7.200 | Echo receiver |
| UDP Sender IP | 10.0.7.12 | Demo sender |
| Packet Filter IP | 10.0.7.50 | Proxy (optional) |
| TCP Echo Port | 9090 | TCP |
| UDP Echo Port | 9091 | UDP |
| Proxy Port | 8888 | TCP (optional) |
| Portainer | 9000 | **RESERVED - Global service** |

---

*NETWORKING class - ASE, Informatics | by Revolvix*
*Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment*
