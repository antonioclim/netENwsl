# Week 5: Network Layer – IP Addressing, Subnetting, VLSM

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

---

## ⚠️ Environment Notice

This laboratory kit is designed for the **WSL2 + Ubuntu 22.04 + Docker + Portainer** environment.

**Repository:** https://github.com/antonioclim/netENwsl
**This Week's Folder:** `5enWSL`

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

# Clone Week 5
git clone https://github.com/antonioclim/netENwsl.git WEEK5
cd WEEK5
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
git clone https://github.com/antonioclim/netENwsl.git WEEK5
cd WEEK5
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

Open browser and go to: **http://localhost:9000**

**Login credentials:**
- Username: `stud`
- Password: `studstudstud`

### Step 4: Go to Laboratory Directory

```bash
cd /mnt/d/NETWORKING/WEEK5/5enWSL
ls -la
```

---

## 🖥️ Understanding Portainer Interface

### Dashboard Overview

After login at http://localhost:9000, you will see:
1. **Home** - List of Docker environments
2. **local** - Click to manage local Docker

### Viewing Containers

Go to: **Home → local → Containers**

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

1. Go to: **Networks → week5_labnet**
2. View current IPAM configuration (10.5.0.0/24)
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

### Essential Wireshark Filters for Week 5

| Filter | Purpose |
|--------|---------|
| `ip.addr == 10.5.0.0/24` | Week 5 labnet traffic |
| `udp.port == 9999` | UDP Echo server traffic |
| `icmp` | ICMP (ping) traffic |
| `ipv6` | IPv6 traffic only |
| `icmpv6` | ICMPv6 including Neighbour Discovery |

### Following a UDP Conversation

1. Find any UDP packet
2. Right-click → **Follow → UDP Stream**
3. View the complete exchange

### Saving Captures

1. **File → Save As**
2. Go to: `D:\NETWORKING\WEEK5\pcap\`
3. Filename: `capture_exercise_N.pcap`

---

## Overview

The network layer (Layer 3) forms the foundation of internetworking, providing logical addressing and routing that allow communication across different physical networks. This lab examines IPv4 and IPv6 addressing, covering how addresses are assigned, calculated and organised for scalable network designs.

Students will work through the mathematics of subnetting using both Fixed Length Subnet Mask (FLSM) and Variable Length Subnet Mask (VLSM) techniques. The practical exercises use Docker containers and Python tools to test addressing scenarios, calculate network parameters and verify configurations.

After this lab, students will have the background needed to understand routing protocols, network address translation and the broader structure of the global Internet.

## Learning Objectives

By the end of this laboratory session, you will be able to:

1. **Identify** the role and functions of the network layer within the OSI and TCP/IP reference models
2. **Explain** the structural differences between IPv4 and IPv6 header formats and addressing schemes
3. **Calculate** network addresses, broadcast addresses and usable host ranges from CIDR notation
4. **Apply** FLSM subnetting to partition networks into equal-sized segments
5. **Design** VLSM allocation schemes that optimise address space utilisation for varied requirements
6. **Evaluate** the efficiency and correctness of addressing schemes through programmatic validation

## Prerequisites

### Knowledge Requirements
- Understanding of OSI model layers and their functions
- Familiarity with binary number systems and bitwise operations
- Basic Python programming skills (functions, CLI arguments)
- Previous experience with Docker containers

### Software Requirements
- Windows 10/11 with WSL2 enabled
- Docker Engine (in WSL)
- Portainer CE (running globally on port 9000)
- Wireshark (native Windows)
- Python 3.11 or later
- Git

### Hardware Requirements
- Minimum 8GB RAM (16GB recommended)
- 10GB free disk space
- Network connectivity

---

## 📚 Pedagogical Resources

This week includes evidence-based teaching materials to support your learning:

| Resource | Purpose | Location |
|----------|---------|----------|
| Peer Instruction Questions | MCQ for class voting and discussion | `docs/peer_instruction.md` |
| Pair Programming Guide | Structured collaborative exercises | `docs/pair_programming_guide.md` |
| Common Misconceptions | Frequent errors and how to avoid them | `docs/misconceptions.md` |
| Glossary | Technical terms and definitions | `docs/glossary.md` |
| Code Tracing | Mental execution practice | `docs/code_tracing.md` |
| Parsons Problems | Code block reordering exercises | `docs/parsons_problems.md` |

**Recommended approach:**
1. Read `docs/misconceptions.md` before starting exercises
2. Use `docs/glossary.md` as a reference during work
3. Complete `docs/code_tracing.md` to verify understanding
4. Work through exercises with a partner using `docs/pair_programming_guide.md`

---

## Quick Start

### First-Time Setup (Run Once)

```bash
# Open Ubuntu terminal (WSL)
wsl

# Go to the kit directory
cd /mnt/d/NETWORKING/WEEK5/5enWSL

# Start Docker if not running
sudo service docker start

# Verify prerequisites
python3 setup/verify_environment.py

# If any issues, run the installer helper
python3 setup/install_prerequisites.py
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
| Python Container | Interactive shell | N/A |
| UDP Echo Server | localhost:9999/udp | N/A |

## Laboratory Exercises

### Exercise 1: CIDR Analysis and Binary Representation

**Objective:** Analyse IPv4 addresses with CIDR notation, calculating all network parameters and understanding binary representations.

**Duration:** 25 minutes

💭 **PREDICTION:** Before running each command, write down what you expect for: network address, broadcast address, number of usable hosts.

**Steps:**

1. Open Ubuntu terminal and go to the kit directory
2. Start the Docker environment:
   ```bash
   python3 scripts/start_lab.py
   ```
3. Execute the CIDR analysis tool:
   ```bash
   docker exec -it week5_python python /app/src/exercises/ex_5_01_cidr_flsm.py analyse 192.168.10.14/26 --verbose
   ```
4. Compare the output with your predictions. Note the network address, broadcast address and host range
5. Experiment with different prefix lengths:
   ```bash
   docker exec -it week5_python python /app/src/exercises/ex_5_01_cidr_flsm.py analyse 10.0.0.100/24
   docker exec -it week5_python python /app/src/exercises/ex_5_01_cidr_flsm.py analyse 172.16.50.1/28
   ```
6. Examine the binary conversion:
   ```bash
   docker exec -it week5_python python /app/src/exercises/ex_5_01_cidr_flsm.py binary 192.168.10.14
   ```

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 1
```

### Exercise 2: FLSM Subnetting

**Objective:** Partition a network into equal-sized subnets using Fixed Length Subnet Mask technique.

**Duration:** 20 minutes

💭 **PREDICTION:** For a /24 split into 4 subnets: How many bits must be borrowed? What will the new prefix be? How many hosts per subnet?

**Steps:**

1. Understand the scenario: Your organisation has been allocated 192.168.100.0/24 and requires 4 equal subnets
2. Calculate manually how many bits must be borrowed from the host portion
3. Verify your calculation using the FLSM tool:
   ```bash
   docker exec -it week5_python python /app/src/exercises/ex_5_01_cidr_flsm.py flsm 192.168.100.0/24 4
   ```
4. Observe the subnet boundaries, broadcast addresses and usable host counts
5. Try different scenarios:
   ```bash
   docker exec -it week5_python python /app/src/exercises/ex_5_01_cidr_flsm.py flsm 10.0.0.0/24 8
   docker exec -it week5_python python /app/src/exercises/ex_5_01_cidr_flsm.py flsm 172.16.0.0/16 16
   ```

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 2
```

### Exercise 3: VLSM Allocation

**Objective:** Design an efficient addressing scheme using Variable Length Subnet Mask for varied requirements.

**Duration:** 30 minutes

💭 **PREDICTION:** Given requirements of 60, 20, 10 and 2 hosts: Which requirement gets allocated first? What prefix will the largest subnet have?

**Steps:**

1. Consider the scenario: A company needs networks for 60 employees, 20 contractors, 10 servers and 2 point-to-point links
2. Available address space: 172.16.0.0/24
3. Understand why VLSM is more efficient than FLSM for this scenario
4. Execute the VLSM allocation:
   ```bash
   docker exec -it week5_python python /app/src/exercises/ex_5_02_vlsm_ipv6.py vlsm 172.16.0.0/24 60 20 10 2
   ```
5. Analyse the efficiency percentages for each subnet
6. Try a more complex scenario:
   ```bash
   docker exec -it week5_python python /app/src/exercises/ex_5_02_vlsm_ipv6.py vlsm 10.10.0.0/22 200 100 50 25 10 2 2 2
   ```

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 3
```

### Exercise 4: IPv6 Address Operations

**Objective:** Understand IPv6 address representation, compression rules and subnetting.

**Duration:** 25 minutes

💭 **PREDICTION:** How will `2001:0db8:0000:0000:0000:0000:0000:0001` look when compressed? How many times can :: appear?

**Steps:**

1. Check IPv6 address types:
   ```bash
   docker exec -it week5_python python /app/src/exercises/ex_5_02_vlsm_ipv6.py ipv6-types
   ```
2. Compress an expanded IPv6 address:
   ```bash
   docker exec -it week5_python python /app/src/exercises/ex_5_02_vlsm_ipv6.py ipv6 2001:0db8:0000:0000:0000:0000:0000:0001
   ```
3. Expand a compressed address:
   ```bash
   docker exec -it week5_python python /app/src/exercises/ex_5_02_vlsm_ipv6.py ipv6-expand 2001:db8::1
   ```
4. Generate IPv6 /64 subnets from a /48 allocation:
   ```bash
   docker exec -it week5_python python /app/src/exercises/ex_5_02_vlsm_ipv6.py ipv6-subnets 2001:db8:10::/48 64 10
   ```

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 4
```

## Demonstrations

### Demo 1: Complete Addressing Workflow

Automated demonstration showcasing CIDR analysis, FLSM partitioning and VLSM allocation.

```bash
python3 scripts/run_demo.py --demo 1
```

**What to observe:**
- How the same /24 network is partitioned differently with FLSM vs VLSM
- Efficiency comparisons between the two approaches
- Binary representation of network boundaries

### Demo 2: UDP Echo with Network Isolation

Demonstrates containerised network communication with explicit IP addressing.

```bash
python3 scripts/run_demo.py --demo 2
```

**What to observe:**
- Container IP assignments within the 10.5.0.0/24 subnet
- UDP packet exchange between client and server containers
- Traffic patterns visible in packet captures

## Packet Capture and Analysis

### Capturing Traffic

```bash
# Start capture in Docker network
python3 scripts/capture_traffic.py --interface eth0 --output pcap/week5_capture.pcap

# Or capture directly from UDP server container
docker exec week5_udp-server tcpdump -i eth0 -w /app/pcap/udp_traffic.pcap &
```

### Suggested Wireshark Filters

```
# Show only ICMP (ping) traffic
icmp

# Filter by specific subnet
ip.addr == 10.5.0.0/24

# UDP traffic on port 9999
udp.port == 9999

# IPv6 only
ipv6

# ICMPv6 (including Neighbour Discovery)
icmpv6
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

## Homework Assignments

See the `homework/` directory for take-home exercises.

### Assignment 1: Corporate Network Design
Design a VLSM addressing scheme for a medium enterprise with headquarters (500 users), two branch offices (150 and 80 users), DMZ servers (25) and point-to-point WAN links.

### Assignment 2: IPv6 Migration Planning
Given an existing IPv4 /22 network with 12 subnets, propose an equivalent IPv6 addressing plan using a /48 allocation, maintaining logical groupings.

## Troubleshooting

### Common Issues

#### Issue: Docker containers fail to start
**Solution:** Ensure Docker is running in WSL. Run `sudo service docker start` then `docker info` to verify.

#### Issue: Python module not found errors
**Solution:** Ensure you're executing commands from the correct directory. The container mounts expect the kit structure.

#### Issue: Cannot access UDP server from host
**Solution:** Check that port 9999/udp is properly mapped. Use `docker ps` to verify port bindings.

#### Issue: Wireshark cannot capture Docker traffic
**Solution:** On Windows, capture on the "vEthernet (WSL)" interface. For container-internal traffic, use tcpdump within containers.

See `docs/troubleshooting.md` for more solutions.

## Theoretical Background

The network layer (Layer 3) provides end-to-end logical addressing and routing capabilities. Unlike data link layer addresses which have only local significance, network layer addresses allow communication across different physical networks.

**IPv4 Addressing**: 32-bit addresses expressed in dotted-decimal notation (e.g., 192.168.1.1). The address space is divided into network and host portions, with the boundary determined by the subnet mask or CIDR prefix.

**Subnetting**: The practice of dividing a network into smaller segments. FLSM creates equal-sized subnets, whilst VLSM allows variable sizes to match actual requirements, improving address utilisation efficiency.

**IPv6 Addressing**: 128-bit addresses expressed in hexadecimal colon notation. The vastly larger address space eliminates the need for NAT and supports hierarchical allocation. Standard subnet size is /64, providing 64 bits for the interface identifier.

## References

- Kurose, J. & Ross, K. (2021). *Computer Networking: A Top-Down Approach* (8th ed.). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress.
- RFC 791 – Internet Protocol (IPv4)
- RFC 8200 – Internet Protocol, Version 6 (IPv6)
- RFC 1918 – Address Allocation for Private Internets
- RFC 4291 – IP Version 6 Addressing Architecture

## Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                    Docker Network: labnet                        │
│                    Subnet: 10.5.0.0/24                          │
│                    Gateway: 10.5.0.1                            │
│            (WSL2 + Ubuntu 22.04 + Docker + Portainer)           │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   python     │    │  udp-server  │    │  udp-client  │       │
│  │  10.5.0.10   │    │  10.5.0.20   │    │  10.5.0.30   │       │
│  │              │    │  :9999/udp   │    │              │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│                             ▲                    │               │
│                             │    UDP Echo        │               │
│                             └────────────────────┘               │
│                                                                  │
│  Portainer: http://localhost:9000 (global service)              │
│  Credentials: stud / studstudstud                               │
└──────────────────────────────────────────────────────────────────┘
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
- ✅ Try "Capture → Options" and turn on promiscuous mode

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
docker network inspect week5_labnet

# Check DNS in container
docker exec week5_python cat /etc/resolv.conf
```

**Problem:** Port already in use
```bash
# Find what's using the port
sudo netstat -tlnp | grep 9999
# Or
sudo ss -tlnp | grep 9999

# Kill the process or use different port
```

### Subnetting Calculation Issues

**Problem:** VLSM allocation fails
```bash
# Ensure host requirements are sorted largest-first
# Tool expects requirements in any order but validates total space
```

**Problem:** IPv6 address compression incorrect
```bash
# Remember: only ONE :: allowed per address
# Leading zeros can be removed: 0db8 → db8
# Consecutive all-zero groups become ::
```

---

## 🧹 Complete Cleanup Procedure

### End of Session (Quick)

```bash
# Stop lab containers (Portainer stays running!)
cd /mnt/d/NETWORKING/WEEK5/5enWSL
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

## 📊 Week 5 Network Configuration Summary


---

## ✅ Self-Assessment Checklist

Before completing this week, verify you can:

### CIDR and Subnetting Fundamentals
- [ ] Convert between dotted-decimal and CIDR notation
- [ ] Calculate network address from any IP/prefix combination
- [ ] Calculate broadcast address for any subnet
- [ ] Determine usable host range and count
- [ ] Identify if an address is network, host or broadcast

### FLSM (Fixed Length Subnet Mask)
- [ ] Determine bits to borrow for N equal subnets
- [ ] Calculate new prefix after subnetting
- [ ] List all subnet boundaries for a given split
- [ ] Calculate hosts per subnet after split

### VLSM (Variable Length Subnet Mask)
- [ ] Explain why largest-first allocation is necessary
- [ ] Calculate minimum prefix for a host requirement
- [ ] Perform complete VLSM allocation manually
- [ ] Verify allocation efficiency

### IPv6 Addressing
- [ ] Compress an expanded IPv6 address correctly
- [ ] Expand a compressed IPv6 address
- [ ] Identify address types (global, link-local, multicast)
- [ ] Explain why :: can only appear once

### Practical Skills
- [ ] Use the lab tools to verify calculations
- [ ] Start and stop the Docker environment
- [ ] Capture traffic with Wireshark
- [ ] Navigate Portainer for container management

### Docker Networking
- [ ] Explain how Docker networks isolate containers
- [ ] Understand IP assignment within docker-compose
- [ ] Verify container connectivity using ping/netcat

**Recommended:** Complete `docs/code_tracing.md` exercises to verify understanding.

---

## 📚 Additional Resources

See `docs/further_reading.md` for:
- RFC documents (primary sources)
- Recommended textbooks
- Online practice tools
- Video tutorials

---

## 📊 Week 5 Network Configuration Summary

| Resource | Value | Notes |
|----------|-------|-------|
| Subnet | 10.5.0.0/24 | Week 5 labnet |
| Gateway | 10.5.0.1 | Docker bridge gateway |
| Python Container IP | 10.5.0.10 | Exercise environment |
| UDP Server IP | 10.5.0.20 | Echo server |
| UDP Client IP | 10.5.0.30 | Echo client |
| UDP Echo Port | 9999/udp | Server port |
| Portainer | 9000 | **RESERVED - Global service** |

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
*Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment*
