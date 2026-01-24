# Week 3: Introduction to Network Programming

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
> 
> by ing. dr. Antonio Clim

---

## ⚠️ Environment Notice

This laboratory kit is designed for the **WSL2 + Ubuntu 22.04 + Docker + Portainer** environment.

**Repository:** https://github.com/antonioclim/netENwsl
**This Week's Folder:** `3enWSL`

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

### Step 2: Go to Directory and Clone

```powershell
# Create networking folder if it doesn't exist
mkdir D:\NETWORKING -ErrorAction SilentlyContinue
cd D:\NETWORKING

# Clone Week 3
git clone https://github.com/antonioclim/netENwsl.git WEEK3
cd WEEK3
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
git clone https://github.com/antonioclim/netENwsl.git WEEK3
cd WEEK3
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
cd /mnt/d/NETWORKING/WEEK3/3enWSL
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

1. Go to: **Networks → week3_network**
2. View current IPAM configuration (172.20.0.0/24)
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

### Essential Wireshark Filters for Week 3

| Filter | Purpose |
|--------|---------|
| `udp.port >= 5000 and udp.port <= 5100` | Broadcast/multicast traffic |
| `eth.dst == ff:ff:ff:ff:ff:ff` | Broadcast frames |
| `ip.dst == 239.1.1.1` | Multicast group traffic |
| `igmp` | IGMP membership messages |
| `tcp.port == 9090 or tcp.port == 8080` | TCP tunnel traffic |

### Following a TCP Conversation

1. Find any packet in the conversation
2. Right-click → **Follow → TCP Stream**
3. View complete conversation in readable text

### Saving Captures

1. **File → Save As**
2. Go to: `D:\NETWORKING\WEEK3\pcap\`
3. Filename: `capture_exercise_N.pcap`

---

## Overview

This laboratory introduces the fundamental concepts and practical techniques of network programming using Python sockets. The session focuses on three essential communication approachs that form the backbone of distributed systems: UDP broadcast, UDP multicast and TCP tunnelling.

UDP broadcast represents the simplest form of one-to-many communication, where a single transmission reaches all hosts within a Layer 2 broadcast domain. While straightforward to implement, broadcast communication is inherently limited to local network segments and generates traffic that all hosts must process, making it suitable primarily for service discovery and local announcements.

UDP multicast provides a more sophisticated approach to group communication, allowing selective delivery to hosts that have explicitly joined a multicast group. This mechanism reduces network overhead compared to broadcast while enabling efficient one-to-many delivery across routed networks when IGMP (Internet Group Management Protocol) is properly configured.

TCP tunnelling (port forwarding) demonstrates how to create a relay point that bridges connections between network segments. This technique is foundational for understanding proxy servers, NAT traversal and the construction of overlay networks. The tunnel accepts incoming TCP connections and establishes corresponding outbound connections to a target server, forwarding data bidirectionally.

## Learning Objectives

By the end of this laboratory session, you will be able to:

1. **Recall** the fundamental differences between unicast, broadcast and multicast addressing at the IP layer and identify the socket options required for each communication mode
2. **Explain** why broadcast is constrained to Layer 2 domains while multicast can traverse routers when IGMP is enabled and describe the role of TTL in multicast propagation
3. **Implement** functional UDP broadcast and multicast senders and receivers using Python's socket library, correctly configuring SO_BROADCAST and multicast group membership
4. **Construct** a TCP tunnel that accepts connections on one port and forwards traffic bidirectionally to a target server, using threading for full-duplex communication
5. **Analyse** captured network traffic using tcpdump and Wireshark, identifying UDP datagrams, IGMP membership reports and TCP three-way handshakes
6. **Evaluate** the appropriateness of broadcast, multicast and unicast for different application scenarios, considering factors such as network topology, scalability and reliability requirements

## Prerequisites

### Knowledge Requirements

Before beginning this laboratory, you should be familiar with:
- OSI and TCP/IP reference models (covered in Week 2)
- Fundamental differences between TCP and UDP transport protocols
- Basic Python programming including functions, classes and exception handling
- Command-line navigation in Linux environments
- IP addressing and subnetting concepts

### Software Requirements

The following software must be installed and configured:
- Windows 10/11 with WSL2 enabled (Ubuntu 22.04 recommended)
- Docker Engine (in WSL)
- Portainer CE (running globally on port 9000)
- Wireshark for Windows (native application)
- Python 3.11 or later
- Git for version control

### Hardware Requirements

Minimum specifications for comfortable operation:
- 8GB RAM (16GB recommended for concurrent containers)
- 10GB free disk space for Docker images and captures
- Dual-core processor (quad-core recommended)
- Stable network connectivity for package installation

## Quick Start

### First-Time Setup (Run Once)

Open Ubuntu terminal (WSL) and execute:

```bash
# Go to the kit directory
cd /mnt/d/NETWORKING/WEEK3/3enWSL

# Start Docker if not running
sudo service docker start

# Verify all prerequisites are installed
python3 setup/verify_environment.py

# If any checks fail, run the installer helper
python3 setup/install_prerequisites.py
```

### Starting the Laboratory

```bash
# Start all Docker containers
python3 scripts/start_lab.py

# Verify services are running correctly
python3 scripts/start_lab.py --status

# View container logs (optional)
docker compose -f docker/docker-compose.yml logs -f
```

### Accessing Services

| Service | Address | Purpose |
|---------|---------|---------|
| Portainer | http://localhost:9000 | Container management (stud/studstudstud) |
| Echo Server | localhost:8080 | TCP echo service on server container |
| TCP Tunnel | localhost:9090 | Forwards to server:8080 via router |
| Client Shell | docker exec -it week3_client bash | Interactive testing environment |

## Laboratory Exercises

### Exercise 1: UDP Broadcast Communication

**Objective:** Implement and observe UDP broadcast transmission within a Layer 2 domain, understanding the SO_BROADCAST socket option and the behaviour of limited broadcast addresses.

**Duration:** 30 minutes

**Theory:** UDP broadcast sends datagrams to all hosts on a network segment. The address 255.255.255.255 represents a "limited broadcast" that never crosses routers, while directed broadcasts (e.g., 172.20.0.255) target specific subnets. The operating system kernel requires explicit permission via the SO_BROADCAST socket option before allowing broadcast transmissions.

**Steps:**

1. Access the client container:
```bash
docker exec -it week3_client bash
```

2. In a separate terminal, start a broadcast receiver:
```bash
docker exec -it week3_client python3 /app/src/exercises/ex_3_01_udp_broadcast.py recv --port 5007 --count 5
```

3. In another terminal, start a second receiver on the receiver container:
```bash
docker exec -it week3_receiver python3 /app/src/exercises/ex_3_01_udp_broadcast.py recv --port 5007 --count 5
```

4. Send broadcast datagrams from the client:
```bash
docker exec -it week3_client python3 /app/src/exercises/ex_3_01_udp_broadcast.py send --dst 255.255.255.255 --port 5007 --count 5 --interval 1
```

5. Observe that both receivers display the same messages

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 1
```

**Expected Observations:**
- Both receivers display incoming datagrams with identical content
- The source port varies (ephemeral port selection)
- The destination address in the receiver output shows the sender's IP

### Exercise 2: UDP Multicast Communication

**Objective:** Configure multicast group membership using IGMP and observe selective delivery to subscribed receivers only.

**Duration:** 35 minutes

**Theory:** Multicast addresses in the range 224.0.0.0 to 239.255.255.255 identify groups rather than individual hosts. A host joins a multicast group by sending an IGMP Membership Report, instructing network equipment to forward group traffic to its interface. The IP_ADD_MEMBERSHIP socket option triggers this process.

**Steps:**

1. Start a multicast receiver on the client container:
```bash
docker exec -it week3_client python3 /app/src/exercises/ex_3_02_udp_multicast.py recv --group 239.1.1.1 --port 5008 --count 5
```

2. Start a second receiver on the receiver container:
```bash
docker exec -it week3_receiver python3 /app/src/exercises/ex_3_02_udp_multicast.py recv --group 239.1.1.1 --port 5008 --count 5
```

3. Send multicast datagrams from the server:
```bash
docker exec -it week3_server python3 /app/src/exercises/ex_3_02_udp_multicast.py send --group 239.1.1.1 --port 5008 --count 5 --ttl 4
```

4. Capture IGMP traffic to observe group membership:
```bash
docker exec -it week3_client tcpdump -i eth0 igmp -c 5
```

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 2
```

**Expected Observations:**
- IGMP Membership Report messages when receivers join the group
- Only containers that joined the group receive the multicast datagrams
- TTL value determines how many router hops the multicast can traverse

### Exercise 3: TCP Tunnel (Port Forwarding)

**Objective:** Construct and analyse a TCP tunnel that relays connections between endpoints, understanding bidirectional forwarding and the proxy pattern.

**Duration:** 35 minutes

**Theory:** TCP tunnelling creates a relay point that accepts incoming connections on one port and forwards data to a target server on another port (possibly on a different host). This pattern is fundamental to proxy servers, load balancers and NAT traversal techniques.

**Steps:**

1. Verify the tunnel is running on the router:
```bash
docker exec -it week3_router ps aux | grep tcp_tunnel
```

2. Test direct connection to the echo server:
```bash
docker exec -it week3_client bash -c "echo 'DIRECT TEST' | nc server 8080"
```

3. Test connection through the tunnel:
```bash
docker exec -it week3_client bash -c "echo 'TUNNEL TEST' | nc router 9090"
```

4. Start Wireshark and capture on vEthernet (WSL)

5. Run multiple test messages and observe the traffic flow:
```bash
docker exec -it week3_client bash -c "for i in 1 2 3; do echo MESSAGE_\$i | nc -q 1 router 9090; done"
```

6. In Wireshark, filter for `tcp.port == 9090 or tcp.port == 8080` and analyse the connection patterns

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 3
```

**Expected Observations:**
- Each tunnel connection creates two TCP streams: client→router and router→server
- Data is forwarded bidirectionally with minimal latency
- Connection termination on either side triggers cleanup of the other connection

## Demonstrations

### Demo 1: Broadcast vs Multicast Comparison

This demonstration highlights the fundamental difference between broadcast (all hosts receive) and multicast (only group members receive).

```bash
python3 scripts/run_demo.py --demo broadcast_vs_multicast
```

### Demo 2: TCP Tunnel Visualisation

Watch data flow through the tunnel with detailed logging:

```bash
python3 scripts/run_demo.py --demo tunnel_flow
```

### Demo 3: IGMP Snooping

Observe IGMP messages as hosts join and leave multicast groups:

```bash
python3 scripts/run_demo.py --demo igmp
```

## Packet Capture Guide

### Starting Capture

Using the capture script:
```bash
python3 scripts/capture_traffic.py --interface eth0 --output pcap/week3_capture.pcap --duration 60
```

Using tcpdump directly in containers:
```bash
docker exec -it week3_client tcpdump -i eth0 -w /app/pcap/capture.pcap -c 100
```

### Suggested Wireshark Filters

```
# All UDP traffic on demo ports
udp.port >= 5000 and udp.port <= 5100

# Broadcast traffic only
eth.dst == ff:ff:ff:ff:ff:ff

# Multicast group 239.1.1.1
ip.dst == 239.1.1.1

# IGMP protocol messages
igmp

# TCP tunnel traffic
tcp.port == 9090 or tcp.port == 8080

# TCP SYN packets (connection attempts)
tcp.flags.syn == 1 and tcp.flags.ack == 0

# Retransmissions (useful for debugging)
tcp.analysis.retransmission
```

## Shutdown and Cleanup

### End of Session

Graceful shutdown preserving data:
```bash
# Stop all containers (Portainer stays running!)
python3 scripts/stop_lab.py

# Verify shutdown
docker ps

# View logs before stopping (optional)
docker compose -f docker/docker-compose.yml logs --tail=50
```

### Full Cleanup (Before Next Week)

Complete removal for fresh start:
```bash
# Remove containers, networks and volumes
python3 scripts/cleanup.py --full

# Verify cleanup
docker system df

# Prune unused Docker resources (optional)
python3 scripts/cleanup.py --full --prune
```

## Homework Assignments

See the `homework/` directory for detailed instructions.

### Assignment 1: Enhanced Broadcast Receiver

Extend the broadcast receiver to log statistics including packet count, bytes received and source distribution. Implement a timeout mechanism that terminates reception after a configurable period of inactivity.

### Assignment 2: Multicast Chat Application

Design a simple chat application where multiple clients join a multicast group and exchange messages. Each client should display messages from others with sender identification. Consider how to handle the "loopback" problem where a sender receives its own messages.

### Assignment 3: TCP Tunnel with Logging

Modify the TCP tunnel to write a detailed log file containing timestamps, connection IDs, direction and byte counts. Add support for multiple concurrent tunnels to different targets.

## Troubleshooting

### Common Issues

#### Issue: "Permission denied" when sending broadcast
**Solution:** Ensure SO_BROADCAST is set on the socket before calling sendto(). On some systems, elevated privileges may be required. Verify with:
```python
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
```

#### Issue: Multicast not received by other containers
**Solution:** Check that all receivers have joined the same multicast group and that the interface binding is correct. Verify IGMP is not blocked by firewall rules. Increase TTL if crossing network segments:
```bash
docker exec -it week3_client sysctl net.ipv4.icmp_echo_ignore_broadcasts
```

#### Issue: TCP tunnel connection refused
**Solution:** Confirm the target server is running and listening on the expected port. Check that the tunnel has network connectivity to the target. Verify with:
```bash
docker exec -it week3_router nc -zv server 8080
```

#### Issue: Docker containers cannot communicate
**Solution:** Ensure all containers are on the same Docker network. Check with:
```bash
docker network inspect week3_network
```

#### Issue: Wireshark cannot see Docker traffic
**Solution:** On Windows, capture on the "vEthernet (WSL)" adapter or use tcpdump inside containers and copy the pcap file out for analysis.

See `docs/troubleshooting.md` for additional solutions.

## Theoretical Background

### UDP Socket Programming

UDP (User Datagram Protocol) provides connectionless, unreliable delivery of datagrams. Key characteristics relevant to this laboratory:

The absence of connection state means each datagram is independent. The sendto() function specifies the destination for each transmission, while recvfrom() returns the source address along with the received data. There is no built-in mechanism for ordering, duplicate detection, or acknowledgement.

Socket options modify behaviour: SO_BROADCAST enables transmission to broadcast addresses, SO_REUSEADDR permits immediate reuse of a local address after socket closure and IP_ADD_MEMBERSHIP subscribes to a multicast group.

### TCP Connection Forwarding

TCP tunnelling involves maintaining two simultaneous connections and forwarding data between them. The pattern requires:

A listening socket that accepts incoming client connections. For each accepted connection, a new outbound connection to the target server. Two concurrent data flows: client-to-target and target-to-client. Proper shutdown handling when either side closes the connection.

Threading or asynchronous I/O enables full-duplex operation where data can flow in both directions simultaneously.

### Broadcast vs Multicast

Broadcast transmissions reach all hosts on a Layer 2 segment regardless of interest. The address 255.255.255.255 is a "limited broadcast" confined to the local network, while directed broadcasts (subnet.255) are typically blocked by routers.

Multicast delivers only to hosts that have explicitly joined the group via IGMP. This selective delivery reduces wasted bandwidth and processing on uninterested hosts. Multicast can traverse routers when multicast routing protocols (DVMRP, PIM) are configured.


## 📚 Pedagogical Resources

This laboratory kit includes additional pedagogical materials to support active learning:

| Resource | Purpose |
|----------|---------|
| [docs/peer_instruction.md](docs/peer_instruction.md) | MCQ questions for class discussion (vote-discuss-revote) |
| [docs/pair_programming_guide.md](docs/pair_programming_guide.md) | Structured collaboration exercises |
| [docs/misconceptions.md](docs/misconceptions.md) | Common errors and corrections |
| [docs/glossary.md](docs/glossary.md) | Technical terms and definitions |
| [docs/code_tracing.md](docs/code_tracing.md) | Trace-through exercises for understanding |
| [docs/parsons_problems.md](docs/parsons_problems.md) | Code reordering exercises for active learning |
| [docs/concept_analogies.md](docs/concept_analogies.md) | Real-world analogies for network concepts |

### Prediction Checkpoints

Exercises include **prediction prompts** (💭) that ask you to predict outcomes before running code. This technique improves learning retention significantly. Use the `--no-predict` flag to skip prompts during automated testing.

---

## References

- Kurose, J. F. & Ross, K. W. (2021). *Computer Networking: A Top-Down Approach* (8th ed.). Pearson. Chapters 3 and 4.
- Rhodes, B. & Goerzen, J. (2014). *Foundations of Python Network Programming* (3rd ed.). Apress. Chapters 2 and 3.
- Stevens, W. R., Fenner, B. & Rudoff, A. M. (2004). *UNIX Network Programming, Volume 1: The Sockets Networking API* (3rd ed.). Addison-Wesley.
- RFC 1112 - Host Extensions for IP Multicasting
- RFC 2236 - Internet Group Management Protocol, Version 2
- Python Documentation: socket — Low-level networking interface

## Architecture Diagram

```
                         WEEK 3 NETWORK TOPOLOGY
    ╔════════════════════════════════════════════════════════════════╗
    ║                     Docker Network: 172.20.0.0/24              ║
    ║                 (WSL2 + Ubuntu 22.04 + Docker)                 ║
    ╠════════════════════════════════════════════════════════════════╣
    ║                                                                ║
    ║   ┌─────────────┐         ┌─────────────┐                      ║
    ║   │   SERVER    │         │   ROUTER    │                      ║
    ║   │ 172.20.0.10 │◄───────►│172.20.0.254 │                      ║
    ║   │             │         │             │                      ║
    ║   │ Echo :8080  │         │ Tunnel :9090│                      ║
    ║   └─────────────┘         └──────┬──────┘                      ║
    ║                                  │                             ║
    ║                                  │                             ║
    ║   ┌─────────────┐         ┌──────┴──────┐                      ║
    ║   │  RECEIVER   │         │   CLIENT    │                      ║
    ║   │172.20.0.101 │◄───────►│ 172.20.0.100│                      ║
    ║   │             │         │             │                      ║
    ║   │ Bcast :5007 │         │  Interactive│                      ║
    ║   └─────────────┘         └─────────────┘                      ║
    ║                                                                ║
    ╠════════════════════════════════════════════════════════════════╣
    ║  Broadcast: 172.20.0.255 or 255.255.255.255                    ║
    ║  Multicast: 239.1.1.1 (example group)                          ║
    ║  Gateway: 172.20.0.1 (Docker bridge)                           ║
    ║  Portainer: http://localhost:9000 (global service)             ║
    ╚════════════════════════════════════════════════════════════════╝
    
    Data Flow (TCP Tunnel):
    
    Client ──TCP:9090──► Router (Tunnel) ──TCP:8080──► Server (Echo)
           ◄────────────────────────────◄────────────────────────
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
docker network inspect week3_network

# Check DNS in container
docker exec week3_client cat /etc/resolv.conf
```

**Problem:** Port already in use
```bash
# Find what's using the port
sudo netstat -tlnp | grep 9090
# Or
sudo ss -tlnp | grep 9090

# Kill the process or use different port
```

### Broadcast/Multicast Issues

**Problem:** Broadcast not received
```bash
# Verify SO_BROADCAST is enabled
docker exec -it week3_client python3 -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
print('Broadcast enabled')
"
```

**Problem:** Multicast not working
```bash
# Check multicast route
docker exec -it week3_client ip route show table all | grep 224
```

---

## 🧹 Complete Cleanup Procedure

### End of Session (Quick)

```bash
# Stop lab containers (Portainer stays running!)
cd /mnt/d/NETWORKING/WEEK3/3enWSL
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

## 📊 Week 3 Network Configuration Summary

| Resource | Value | Notes |
|----------|-------|-------|
| Subnet | 172.20.0.0/24 | Week 3 dedicated subnet |
| Gateway | 172.20.0.1 | Docker bridge gateway |
| Server IP | 172.20.0.10 | Echo server (port 8080) |
| Router IP | 172.20.0.254 | TCP tunnel (port 9090) |
| Client IP | 172.20.0.100 | Interactive container |
| Receiver IP | 172.20.0.101 | Broadcast/multicast receiver |
| Broadcast Demo Port | 5007 | UDP broadcast exercises |
| Multicast Demo Port | 5008 | UDP multicast exercises |
| Echo Server Port | 8080 | TCP echo service |
| Tunnel Port | 9090 | TCP tunnel entry point |
| Portainer | 9000 | **RESERVED - Global service** |

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
*Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment*
