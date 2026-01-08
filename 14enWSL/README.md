# Week 14: Integrated Recap and Project Evaluation

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
>
> by Revolvix

---

## ⚠️ Environment Notice

This laboratory kit is designed for the **WSL2 + Ubuntu 22.04 + Docker + Portainer** environment.

**Repository:** https://github.com/antonioclim/netENwsl
**This Week's Folder:** `14enWSL`

| Component | Details |
|-----------|---------|
| Windows | Windows 10/11 with WSL2 enabled |
| Linux Distribution | Ubuntu 22.04 LTS (default WSL distro) |
| Container Runtime | Docker Engine (in WSL) |
| Management Interface | Portainer CE on port 9000 (global) |
| Packet Analysis | Wireshark (native Windows application) |

**Note:** This is the final laboratory session of the semester, integrating concepts from all previous weeks.

---

## 📥 Cloning This Week's Laboratory

### Step 1: Open PowerShell (Windows)

Press `Win + X` → Select "Windows Terminal" or "PowerShell"

### Step 2: Navigate and Clone

```powershell
# Create networking folder if it doesn't exist
mkdir D:\NETWORKING -ErrorAction SilentlyContinue
cd D:\NETWORKING

# Clone Week 14
git clone https://github.com/antonioclim/netENwsl.git WEEK14
cd WEEK14
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
git clone https://github.com/antonioclim/netENwsl.git WEEK14
cd WEEK14
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
cd /mnt/d/NETWORKING/WEEK14/14enWSL
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

### Week 14 Network Configuration

Navigate: **Networks**

This week uses two networks:
- **week14_backend_net**: 172.20.0.0/24 (servers, load balancer internal)
- **week14_frontend_net**: 172.21.0.0/24 (client, load balancer external)

Services:
- Load Balancer (lb): 172.21.0.10 / 172.20.0.10
- Backend 1 (app1): 172.20.0.2
- Backend 2 (app2): 172.20.0.3
- TCP Echo: 172.20.0.20
- Client: 172.21.0.2

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

### Essential Wireshark Filters for Week 14

| Filter | Purpose |
|--------|---------|
| `http.request.method == "GET"` | HTTP GET requests |
| `http.response.code == 200` | Successful HTTP responses |
| `http contains "X-Backend"` | Load balancer headers |
| `tcp.port == 8080` | Load balancer traffic |
| `tcp.port == 9090` | TCP echo traffic |
| `ip.addr == 172.20.0.2 \|\| ip.addr == 172.20.0.3` | Backend traffic |
| `ip.addr == 172.21.0.10` | Load balancer traffic |
| `tcp.flags.syn == 1 && tcp.flags.ack == 0` | TCP connection initiations |

### Analysing Load Balancer Traffic

1. Filter by `http` to see all HTTP traffic
2. Look for `X-Backend` header to see which backend handled each request
3. Follow TCP streams to trace complete request/response cycles
4. Compare timing between requests to different backends

### Saving Captures

1. **File → Save As**
2. Navigate to: `D:\NETWORKING\WEEK14\pcap\`
3. Filename: `capture_week14.pcap`

---

## Overview

This laboratory session serves as a comprehensive review and integration of concepts covered throughout the Computer Networks course. The practical focus centres on building and validating a complete network topology that incorporates multiple services communicating across a containerised environment.

The topology demonstrates fundamental networking principles through a load-balanced web application architecture: a client generates HTTP traffic directed at a reverse proxy, which distributes requests across multiple backend servers using round-robin scheduling. Additionally, a TCP echo service validates basic socket communication patterns. All traffic can be captured and analysed using standard packet analysis tools.

This kit is designed for Windows 10/11 with WSL2 (Windows Subsystem for Linux) and Docker Engine (in WSL), providing a portable environment that students can deploy on their personal machines without requiring dedicated virtual machines or native Linux installations.

## Learning Objectives

By the end of this laboratory session, you will be able to:

1. **Recall** the OSI and TCP/IP layered architectures, identifying which protocols operate at each layer and their respective PDUs (segments, packets, frames)
2. **Explain** the purpose of reverse proxies and load balancers in distributed system architectures, describing how round-robin scheduling achieves request distribution
3. **Implement** a multi-container Docker environment with custom networking, demonstrating understanding of IP addressing, port mapping and inter-container communication
4. **Analyse** packet captures to trace HTTP request flows through multiple network hops, identifying TCP handshakes, HTTP headers and response patterns
5. **Design** verification strategies for network services, creating test harnesses that validate connectivity, port availability and HTTP endpoint behaviour
6. **Evaluate** system behaviour under various conditions, assessing load balancer failover mechanisms and interpreting error scenarios

## Prerequisites

### Knowledge Requirements

- TCP/IP fundamentals: IP addressing, subnetting (CIDR notation), port numbers
- HTTP protocol basics: methods, status codes, headers
- Docker concepts: containers, images, networks, volumes, docker-compose
- Python programming: socket operations, HTTP libraries, subprocess management
- Command-line proficiency: PowerShell/Bash navigation, file operations

### Software Requirements

| Software | Version | Purpose |
|----------|---------|---------|
| Windows 10/11 | 21H2+ | Host operating system with WSL2 support |
| WSL2 | Latest | Linux subsystem for Docker backend |
| Docker Engine | Latest | Container runtime (in WSL) |
| Portainer CE | Latest | Docker management (global on port 9000) |
| Python | 3.11+ | Script execution and automation |
| Wireshark | 4.0+ | Packet capture analysis (native Windows) |
| Git | 2.30+ | Version control (optional) |

### Hardware Requirements

- **Minimum:** 8 GB RAM, 10 GB free disk space, dual-core processor
- **Recommended:** 16 GB RAM, SSD storage, quad-core processor
- Network connectivity for pulling Docker images

## Quick Start

### First-Time Setup (Run Once)

```bash
# Open Ubuntu terminal (WSL)
wsl

# Navigate to the kit directory
cd /mnt/d/NETWORKING/WEEK14/14enWSL

# Start Docker if not running
sudo service docker start

# Verify all prerequisites are installed
python3 setup/verify_environment.py

# If any checks fail, run the prerequisite installer
python3 setup/install_prerequisites.py

# Configure Docker for the lab
python3 setup/configure_docker.py
```

### Starting the Laboratory

```bash
# Start all services (builds images if needed)
python3 scripts/start_lab.py

# Check service status
python3 scripts/start_lab.py --status

# View real-time logs
docker compose -f docker/docker-compose.yml logs -f
```

### Accessing Services

| Service | URL/Port | Description | Credentials |
|---------|----------|-------------|-------------|
| Portainer | http://localhost:9000 | Container management UI | stud / studstudstud |
| Load Balancer | http://localhost:8080 | Reverse proxy frontend | None |
| LB Status | http://localhost:8080/lb-status | Backend statistics | None |
| Backend 1 | http://localhost:8001 | Direct backend access | None |
| Backend 2 | http://localhost:8002 | Direct backend access | None |
| TCP Echo | localhost:9090 | Echo protocol server | None |

## Laboratory Exercises

### Exercise 1: Environment Verification and Service Discovery

**Objective:** Confirm the laboratory environment is correctly configured and understand the service topology.

**Duration:** 15 minutes

**Steps:**

1. Run the environment verification script:
   ```bash
   python3 setup/verify_environment.py
   ```

2. Start the laboratory environment:
   ```bash
   python3 scripts/start_lab.py
   ```

3. Verify all containers are running:
   ```bash
   docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
   ```

4. Test connectivity to each service:
   ```bash
   # Load balancer
   curl http://localhost:8080/
   
   # Backend 1 directly
   curl http://localhost:8001/info
   
   # Backend 2 directly
   curl http://localhost:8002/info
   
   # LB status endpoint
   curl http://localhost:8080/lb-status
   ```

5. Examine the Docker network configuration:
   ```bash
   docker network ls
   docker network inspect week14_backend_net
   docker network inspect week14_frontend_net
   ```

**Verification:**
```bash
python3 tests/test_environment.py
```

**Expected Outcome:**
- All containers report "healthy" status
- Each curl request returns HTTP 200
- Network inspection shows correct IP assignments

---

### Exercise 2: Load Balancer Behaviour Analysis

**Objective:** Observe and verify round-robin request distribution across backend servers.

**Duration:** 20 minutes

**Steps:**

1. Send multiple sequential requests and observe the `X-Backend` header:
   ```bash
   for i in {1..10}; do
       curl -s -D - http://localhost:8080/ -o /dev/null 2>&1 | grep "X-Backend"
   done
   ```

2. Access the load balancer statistics endpoint:
   ```bash
   curl http://localhost:8080/lb-status | python3 -m json.tool
   ```

3. Run the automated HTTP client from within a container:
   ```bash
   docker compose -f docker/docker-compose.yml exec client python3 /app/src/apps/http_client.py --url http://lb:8080/ --count 20
   ```

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 2
```

**Expected Outcome:**
- Requests alternate between backend addresses (round-robin pattern)
- The `/lb-status` endpoint shows increasing request counts for both backends
- Backend selection follows A, B, A, B pattern

---

### Exercise 3: TCP Echo Protocol Testing

**Objective:** Validate TCP socket communication using the echo server.

**Duration:** 15 minutes

**Steps:**

1. Test basic echo functionality using netcat:
   ```bash
   # Test connectivity
   nc -zv localhost 9090
   
   # Interactive echo test
   echo "Hello Week 14" | nc localhost 9090
   ```

2. Run the Python TCP echo client:
   ```bash
   python3 src/apps/tcp_echo_client.py --host localhost --port 9090 --message "Testing echo" --repeat 5
   ```

3. Observe the echo server logs:
   ```bash
   docker compose -f docker/docker-compose.yml logs echo
   ```

4. Test with varying message sizes:
   ```bash
   python3 src/apps/tcp_echo_client.py --host localhost --port 9090 --message "A" --repeat 10
   python3 src/apps/tcp_echo_client.py --host localhost --port 9090 --message "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" --repeat 5
   ```

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 3
```

**Expected Outcome:**
- All echoed messages match the original input
- Server logs show received and sent byte counts
- Connection establishment and teardown complete successfully

---

### Exercise 4: Packet Capture and Analysis

**Objective:** Capture and analyse network traffic to understand protocol interactions.

**Duration:** 30 minutes

**Steps:**

1. Start packet capture on the Docker network:
   ```bash
   python3 scripts/capture_traffic.py --duration 60 --output pcap/week14_capture.pcap
   ```

2. While capture is running, generate traffic:
   ```bash
   # In a new terminal
   for i in {1..20}; do
       curl -s http://localhost:8080/ > /dev/null
       sleep 0.2
   done
   ```

3. Open the capture in Wireshark (Windows):
   - Navigate to `D:\NETWORKING\WEEK14\14enWSL\pcap\`
   - Double-click `week14_capture.pcap`

4. Apply these Wireshark filters to analyse traffic:
   ```
   # All HTTP traffic
   http
   
   # TCP handshakes (SYN packets)
   tcp.flags.syn == 1 && tcp.flags.ack == 0
   
   # HTTP requests only
   http.request
   
   # Traffic to/from load balancer
   ip.addr == 172.21.0.10
   
   # Specific backend traffic
   ip.addr == 172.20.0.2 || ip.addr == 172.20.0.3
   ```

5. Use tshark for command-line analysis:
   ```bash
   # Conversation statistics
   tshark -r pcap/week14_capture.pcap -q -z conv,tcp
   
   # HTTP request summary
   tshark -r pcap/week14_capture.pcap -Y http.request -T fields -e frame.number -e ip.src -e ip.dst -e http.host
   ```

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 4
```

**Expected Outcome:**
- PCAP file contains captured packets
- HTTP conversations visible between client, load balancer and backends
- TCP three-way handshakes identifiable for each connection

## Demonstrations

### Demo 1: Complete System Walkthrough

This automated demonstration exercises all system components and generates a comprehensive report.

```bash
python3 scripts/run_demo.py --demo full
```

**What to observe:**
- Container startup sequence and health checks
- HTTP request distribution across backends
- TCP echo validation
- Traffic capture and summary generation
- Artefact generation in the `artifacts/` directory

### Demo 2: Failover Behaviour

This demonstration shows how the load balancer handles backend failures.

```bash
python3 scripts/run_demo.py --demo failover
```

**What to observe:**
- Initial requests distributed across both backends
- One backend is stopped mid-test
- Load balancer marks the backend as unhealthy
- All subsequent requests route to the remaining backend
- Backend restart and recovery to healthy state

## Packet Capture and Analysis

### Capturing Traffic

```bash
# Basic capture (30 seconds)
python3 scripts/capture_traffic.py --duration 30 --output pcap/demo.pcap

# Extended capture with filter
python3 scripts/capture_traffic.py --duration 120 --filter "port 8080" --output pcap/http_only.pcap

# Capture from specific interface
python3 scripts/capture_traffic.py --interface "eth0" --duration 60 --output pcap/eth_capture.pcap
```

### Suggested Wireshark Filters

```
# HTTP traffic analysis
http.request.method == "GET"
http.response.code == 200
http contains "X-Backend"

# TCP connection analysis
tcp.flags.syn == 1
tcp.flags.fin == 1
tcp.flags.rst == 1

# Specific port filtering
tcp.port == 8080
tcp.port == 9090

# IP-based filtering
ip.src == 172.20.0.2
ip.dst == 172.21.0.10
```

### Command-Line Analysis with tshark

```bash
# Protocol hierarchy
tshark -r pcap/demo.pcap -q -z io,phs

# HTTP statistics
tshark -r pcap/demo.pcap -q -z http,stat

# TCP conversation list
tshark -r pcap/demo.pcap -q -z conv,tcp

# Extract HTTP headers
tshark -r pcap/demo.pcap -Y http -T fields -e http.host -e http.request.uri -e http.response.code
```

## Shutdown and Cleanup

### End of Session

```bash
# Stop all containers (Portainer stays running!)
python3 scripts/stop_lab.py

# Verify shutdown
docker ps

# View stopped containers
docker ps -a --filter "name=week14"
```

### Full Cleanup (Before Next Week)

```bash
# Remove all containers, networks and volumes for this week
python3 scripts/cleanup.py --full

# Verify cleanup
docker system df

# Optional: remove unused Docker resources system-wide
python3 scripts/cleanup.py --full --prune
```

## Homework Assignments

See the `homework/` directory for take-home exercises.

### Assignment 1: Protocol Extension

Extend the TCP echo server to support the binary protocol defined in `src/exercises/ex_14_03.py`. Implement commands: ECHO, REVERSE, UPPER and INFO.

**Deliverable:** Modified server script and test client demonstrating all commands.

### Assignment 2: Load Balancer Enhancement

Modify the load balancer to implement weighted round-robin scheduling. Configure weights via command-line arguments and verify unequal distribution.

**Deliverable:** Modified proxy script, configuration documentation and test results showing weighted distribution.

### Assignment 3: Packet Analysis Report

Capture traffic during a 5-minute session with mixed HTTP and TCP echo traffic. Produce a report identifying:
- Total packets per protocol
- Unique TCP conversations
- HTTP request/response pairs with latency measurements
- Any anomalies or errors observed

**Deliverable:** PCAP file, analysis script and written report (PDF or Markdown).

## Troubleshooting

### Common Issues

#### Issue: Docker containers fail to start with "port already in use"

**Solution:** Identify and stop the conflicting process:
```bash
sudo netstat -tlnp | grep 8080
# or
sudo ss -tlnp | grep 8080
```

#### Issue: WSL2 not running or Docker fails to connect

**Solution:** Restart WSL and Docker:
```bash
# In PowerShell
wsl --shutdown
# Wait 5 seconds, then restart Ubuntu
wsl
sudo service docker start
```

#### Issue: Python packages not found

**Solution:** Install required packages:
```bash
pip install -r setup/requirements.txt --break-system-packages
```

#### Issue: Wireshark cannot capture Docker traffic

**Solution:** Use vEthernet (WSL) interface or capture from within containers:
```bash
docker compose -f docker/docker-compose.yml exec client tcpdump -i eth0 -w /app/artifacts/capture.pcap
```

See `docs/troubleshooting.md` for additional solutions.

## Theoretical Background

This laboratory integrates concepts from multiple layers of the network stack:

**Transport Layer (Layer 4):** TCP segments carry HTTP application data and echo protocol messages. The three-way handshake (SYN, SYN-ACK, ACK) establishes connections, while FIN packets terminate them gracefully. Port numbers (8080, 9090) multiplex multiple services on single hosts.

**Application Layer (Layer 7):** HTTP/1.1 provides request-response communication with methods (GET, POST), status codes (200, 502) and headers (X-Forwarded-For, X-Backend). The reverse proxy pattern separates client-facing and backend concerns.

**Network Layer (Layer 3):** IPv4 addresses (172.20.0.0/24, 172.21.0.0/24) identify containers. Docker's bridge networks provide isolated subnets with NAT for external connectivity.

**Load Balancing:** Round-robin scheduling distributes requests evenly across backends. Health checks detect failures, enabling automatic failover. The proxy adds headers to preserve client identity through the forwarding chain.

## References

- Kurose, J. & Ross, K. (2021). *Computer Networking: A Top-Down Approach* (8th ed.). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming* (3rd ed.). Apress.
- Stevens, W. R. (1994). *TCP/IP Illustrated, Volume 1: The Protocols*. Addison-Wesley.
- Docker Documentation. *Networking overview*. https://docs.docker.com/network/
- Wireshark Documentation. *User's Guide*. https://www.wireshark.org/docs/

## Architecture Diagram

```
                              WEEK 14 NETWORK TOPOLOGY
              (WSL2 + Ubuntu 22.04 + Docker + Portainer)
    ═══════════════════════════════════════════════════════════════════════

    ┌─────────────────────────────────────────────────────────────────────┐
    │                     FRONTEND NETWORK (172.21.0.0/24)                │
    │                                                                      │
    │   ┌──────────────┐                    ┌──────────────┐              │
    │   │    CLIENT    │                    │ LOAD BALANCER│              │
    │   │  172.21.0.2  │◄──────HTTP────────►│  172.21.0.10 │              │
    │   │              │     :8080          │    (lb)      │              │
    │   └──────────────┘                    └───────┬──────┘              │
    │                                               │                      │
    └───────────────────────────────────────────────┼──────────────────────┘
                                                    │
                                                    │ Internal
                                                    │ Proxy
                                                    │
    ┌───────────────────────────────────────────────┼──────────────────────┐
    │                     BACKEND NETWORK (172.20.0.0/24)                  │
    │                                               │                      │
    │   ┌──────────────┐    ┌──────────────┐   ┌───┴──────┐               │
    │   │  BACKEND 1   │    │  BACKEND 2   │   │    LB    │               │
    │   │  (app1)      │    │  (app2)      │   │172.20.0.10│              │
    │   │ 172.20.0.2   │    │ 172.20.0.3   │   └──────────┘               │
    │   │   :8001      │    │   :8001      │                              │
    │   └──────────────┘    └──────────────┘                              │
    │                                                                      │
    │   ┌──────────────┐                                                   │
    │   │  TCP ECHO    │                                                   │
    │   │  (echo)      │                                                   │
    │   │ 172.20.0.20  │                                                   │
    │   │   :9090      │                                                   │
    │   └──────────────┘                                                   │
    │                                                                      │
    └──────────────────────────────────────────────────────────────────────┘

    HOST PORT MAPPINGS:
    ├── localhost:9000  →  Portainer (GLOBAL - RESERVED)
    ├── localhost:8080  →  lb:8080      (Load Balancer)
    ├── localhost:8001  →  app1:8001    (Backend 1 direct)
    ├── localhost:8002  →  app2:8001    (Backend 2 direct)
    └── localhost:9090  →  echo:9090    (TCP Echo Server)
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
docker network inspect week14_backend_net

# Check DNS in container
docker exec week14_client cat /etc/resolv.conf
```

**Problem:** Port already in use
```bash
# Find what's using the port
sudo netstat -tlnp | grep 8080
# Or
sudo ss -tlnp | grep 8080

# Kill the process or use different port
```

### Load Balancer Issues

**Problem:** All requests going to one backend
```bash
# Check both backends are running
docker ps | grep week14_app
# Restart if needed
docker restart week14_app1 week14_app2
```

**Problem:** 502 Bad Gateway errors
```bash
# Check backend health
curl http://localhost:8001/health
curl http://localhost:8002/health
# Check LB logs
docker logs week14_lb
```

---

## 🧹 Complete Cleanup Procedure

### End of Session (Quick)

```bash
# Stop lab containers (Portainer stays running!)
cd /mnt/d/NETWORKING/WEEK14/14enWSL
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

## 📊 Week 14 Network Configuration Summary

| Resource | Value | Notes |
|----------|-------|-------|
| Frontend Network | 172.21.0.0/24 | week14_frontend_net |
| Backend Network | 172.20.0.0/24 | week14_backend_net |
| Load Balancer | 172.21.0.10 / 172.20.0.10 | Port 8080 |
| Backend 1 | 172.20.0.2 | Port 8001 |
| Backend 2 | 172.20.0.3 | Port 8002 (maps to internal 8001) |
| TCP Echo | 172.20.0.20 | Port 9090 |
| Client | 172.21.0.2 | Interactive container |
| Portainer | 9000 | **RESERVED - Global service** |

---

*NETWORKING class - ASE, Informatics | by Revolvix*
*Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment*
