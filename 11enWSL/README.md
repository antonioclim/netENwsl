# Week 11: Application Protocols – FTP, DNS, SSH & Load Balancing

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
> 
> by Revolvix

---

## ⚠️ Environment Notice

This laboratory kit is designed for the **WSL2 + Ubuntu 22.04 + Docker + Portainer** environment.

**Repository:** https://github.com/antonioclim/netENwsl
**This Week's Folder:** `11enWSL`

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

# Clone Week 11
git clone https://github.com/antonioclim/netENwsl.git WEEK11
cd WEEK11
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
git clone https://github.com/antonioclim/netENwsl.git WEEK11
cd WEEK11
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
cd /mnt/d/NETWORKING/WEEK11/11enWSL
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

### Week 11 Network Configuration

Navigate: **Networks → s11_network**

Current configuration:
- Subnet: 172.28.0.0/16
- Nginx Load Balancer: s11_nginx_lb
- Backend 1: s11_backend_1
- Backend 2: s11_backend_2
- Backend 3: s11_backend_3

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

### Essential Wireshark Filters for Week 11

| Filter | Purpose |
|--------|---------|
| `tcp.port == 8080 && http` | HTTP traffic to load balancer |
| `http.request` | HTTP requests only |
| `http.response` | HTTP responses only |
| `udp.port == 53 && dns` | DNS queries |
| `tcp.port == 21 && ftp` | FTP control channel |
| `http contains "X-Served-By"` | Load balancer routing |
| `ip.addr == 172.28.0.0/16` | All lab network traffic |

### Analysing Load Balancer Traffic

1. Start capture on vEthernet (WSL)
2. Run: `for i in {1..10}; do curl -s http://localhost:8080/; done`
3. Filter: `http`
4. Observe the X-Served-By header alternating between backends

### Saving Captures

1. **File → Save As**
2. Navigate to: `D:\NETWORKING\WEEK11\pcap\`
3. Filename: `capture_loadbalancer.pcap`

---

## Overview

This laboratory session explores three fundamental application layer protocols that underpin the modern Internet infrastructure: FTP (File Transfer Protocol), DNS (Domain Name System), and SSH (Secure Shell). These protocols exemplify distinct communication paradigms—FTP employs a dual-connection architecture separating control and data channels, DNS operates predominantly over UDP with hierarchically structured query mechanisms, and SSH establishes multiplexed encrypted channels for secure remote access.

The practical component focuses on distributed application architectures, specifically reverse proxy configurations and load balancing strategies using both custom Python implementations and industrial-strength Nginx deployments. Students will orchestrate multi-container environments using Docker Compose, implementing various distribution algorithms (round-robin, least connections, IP hash) and observing failover behaviour in real-time.

The convergence of theoretical protocol knowledge with practical load balancing implementation provides essential competencies for debugging network issues, configuring production infrastructure, and developing scalable distributed applications.

## Learning Objectives

By the end of this laboratory session, you will be able to:

1. **Identify** the architectural components of FTP, DNS, and SSH protocols, including their port assignments, message formats, and operational modes
2. **Explain** the differences between FTP active and passive modes, the DNS resolution hierarchy, and SSH key exchange mechanisms
3. **Implement** a functional Python load balancer supporting multiple distribution algorithms and passive health checking
4. **Demonstrate** Nginx reverse proxy configuration with upstream pools, weighted backends, and automatic failover
5. **Analyse** network traffic patterns using packet capture tools to verify load distribution and protocol behaviour
6. **Design** containerised multi-tier architectures using Docker Compose with proper networking isolation and service dependencies
7. **Evaluate** the performance characteristics of different load balancing algorithms through systematic benchmarking

## Prerequisites

### Knowledge Requirements
- OSI/TCP-IP architectural models (Week 2)
- TCP/UDP socket programming fundamentals (Weeks 3-4)
- IP addressing, subnetting, and routing concepts (Weeks 5-6)
- Transport layer protocols: TCP, UDP, TLS (Week 8)
- HTTP protocol and web services (Week 10)

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
- Network connectivity

## Quick Start

### First-Time Setup (Run Once)

```bash
# Open Ubuntu terminal (WSL)
wsl

# Navigate to the kit directory
cd /mnt/d/NETWORKING/WEEK11/11enWSL

# Start Docker if not running
sudo service docker start

# Verify prerequisites
python3 setup/verify_environment.py

# If any issues, run the installer helper
python3 setup/install_prerequisites.py

# Install Python dependencies
pip install -r setup/requirements.txt --break-system-packages
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
| Nginx Load Balancer | http://localhost:8080 | None |
| Backend 1 | http://localhost:8081 | None |
| Backend 2 | http://localhost:8082 | None |
| Backend 3 | http://localhost:8083 | None |
| Nginx Health Check | http://localhost:8080/health | None |

## Laboratory Exercises

### Exercise 1: HTTP Backend Servers

**Objective:** Deploy and test multiple HTTP backend servers that will serve as targets for load balancing

**Duration:** 10 minutes

**Steps:**

1. Open three separate terminal windows

2. Start Backend 1:
   ```bash
   python3 src/exercises/ex_11_01_backend.py --id 1 --port 8081 -v
   ```

3. Start Backend 2 with artificial delay:
   ```bash
   python3 src/exercises/ex_11_01_backend.py --id 2 --port 8082 --delay 0.1 -v
   ```

4. Start Backend 3 with longer delay:
   ```bash
   python3 src/exercises/ex_11_01_backend.py --id 3 --port 8083 --delay 0.2 -v
   ```

5. Verify each backend responds:
   ```bash
   curl http://localhost:8081/
   curl http://localhost:8082/
   curl http://localhost:8083/
   ```

**Expected Output:**
```
Backend 1 | Host: YOUR-PC | Time: 2025-01-06T14:30:00 | Request #1
Backend 2 | Host: YOUR-PC | Time: 2025-01-06T14:30:01 | Request #1
Backend 3 | Host: YOUR-PC | Time: 2025-01-06T14:30:02 | Request #1
```

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 1
```

---

### Exercise 2: Python Load Balancer with Round-Robin

**Objective:** Implement and test a Python-based load balancer using round-robin distribution

**Duration:** 20 minutes

**Steps:**

1. Ensure all three backends are running (from Exercise 1)

2. Start the load balancer with round-robin algorithm:
   ```bash
   python3 src/exercises/ex_11_02_loadbalancer.py \
       --backends localhost:8081,localhost:8082,localhost:8083 \
       --listen 0.0.0.0:8080 \
       --algo rr
   ```

3. Test round-robin distribution:
   ```bash
   for i in {1..6}; do curl -s http://localhost:8080/; done
   ```

4. Observe the rotation pattern: Backend 1 → 2 → 3 → 1 → 2 → 3

**Expected Output:**
```
Backend 1 | Host: ... | Time: ... | Request #1
Backend 2 | Host: ... | Time: ... | Request #1
Backend 3 | Host: ... | Time: ... | Request #1
Backend 1 | Host: ... | Time: ... | Request #2
Backend 2 | Host: ... | Time: ... | Request #2
Backend 3 | Host: ... | Time: ... | Request #2
```

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 2
```

---

### Exercise 3: Sticky Sessions with IP Hash

**Objective:** Configure session affinity using IP-based hashing

**Duration:** 15 minutes

**Steps:**

1. Stop the current load balancer (Ctrl+C)

2. Restart with IP hash algorithm:
   ```bash
   python3 src/exercises/ex_11_02_loadbalancer.py \
       --backends localhost:8081,localhost:8082,localhost:8083 \
       --listen 0.0.0.0:8080 \
       --algo ip_hash
   ```

3. Send multiple requests:
   ```bash
   for i in {1..5}; do curl -s http://localhost:8080/; done
   ```

4. All requests should route to the same backend (sticky session)

**Expected Output:**
```
Backend 2 | Host: ... | Request #1
Backend 2 | Host: ... | Request #2
Backend 2 | Host: ... | Request #3
Backend 2 | Host: ... | Request #4
Backend 2 | Host: ... | Request #5
```

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 3
```

---

### Exercise 4: Failover Simulation

**Objective:** Observe automatic failover when a backend becomes unavailable

**Duration:** 15 minutes

**Steps:**

1. With load balancer running in round-robin mode, stop Backend 2 (Ctrl+C in its terminal)

2. Send requests and observe redistribution:
   ```bash
   for i in {1..6}; do curl -s http://localhost:8080/ 2>/dev/null || echo "ERROR"; done
   ```

3. The first request to Backend 2 will fail; subsequent requests go to 1 and 3

4. Restart Backend 2 and observe recovery:
   ```bash
   python3 src/exercises/ex_11_01_backend.py --id 2 --port 8082 -v
   ```

**What to Observe:**
- Initial failure triggers passive health marking
- Traffic redistributes to healthy backends
- Recovery occurs after fail_timeout expires

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 4
```

---

### Exercise 5: Nginx Docker Load Balancer

**Objective:** Deploy an industrial-strength Nginx load balancer using Docker Compose

**Duration:** 20 minutes

**Steps:**

1. Stop any Python backends and load balancer

2. Start the Nginx stack:
   ```bash
   python3 scripts/start_lab.py --nginx-only
   ```
   Or manually:
   ```bash
   cd docker
   docker compose up -d
   ```

3. Test round-robin distribution:
   ```bash
   for i in {1..6}; do curl -s http://localhost:8080/; done
   ```

4. Observe the X-Served-By header:
   ```bash
   curl -v http://localhost:8080/ 2>&1 | grep "X-Served-By"
   ```

5. Check Nginx status:
   ```bash
   curl http://localhost:8080/nginx_status
   ```

**Expected Output:**
```
web1
web2
web3
web1
web2
web3
```

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 5
```

---

### Exercise 6: DNS Protocol Analysis

**Objective:** Construct and analyse DNS queries using a manual client implementation

**Duration:** 20 minutes

**Steps:**

1. Query an A record:
   ```bash
   python3 src/exercises/ex_11_03_dns_client.py google.com A --verbose
   ```

2. Query MX records for mail servers:
   ```bash
   python3 src/exercises/ex_11_03_dns_client.py google.com MX
   ```

3. Query NS records:
   ```bash
   python3 src/exercises/ex_11_03_dns_client.py ase.ro NS
   ```

4. Compare with system dig tool:
   ```bash
   dig google.com A +short
   dig google.com MX +short
   ```

**Expected Output:**
```
[DNS Query] google.com A
[Packet Hex] 00 01 01 00 00 01 00 00 ...
[Response] google.com -> 142.250.185.78
           TTL: 300 seconds
```

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 6
```

---

### Exercise 7: Performance Benchmarking

**Objective:** Compare performance characteristics of Python vs Nginx load balancers

**Duration:** 15 minutes

**Steps:**

1. Benchmark Python load balancer:
   ```bash
   python3 src/exercises/ex_11_02_loadbalancer.py loadgen \
       --url http://localhost:8080/ \
       --n 500 --c 20
   ```

2. Start Nginx stack and benchmark:
   ```bash
   ab -n 1000 -c 10 http://localhost:8080/
   ```

3. Record and compare metrics:
   - Requests per second
   - Mean latency
   - 95th percentile latency

**Expected Results:**
- Python LB: ~500-1000 requests/second
- Nginx LB: ~10,000+ requests/second

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 7
```

## Demonstrations

### Demo 1: Complete Load Balancing Workflow

Automated demonstration showcasing the full laboratory environment:

```bash
python3 scripts/run_demo.py --demo 1
```

**What to observe:**
- Docker stack initialisation
- Round-robin distribution across backends
- Traffic capture in Wireshark-compatible format
- Validation report generation

### Demo 2: Failover and Recovery

Demonstrates automatic failover behaviour:

```bash
python3 scripts/run_demo.py --demo 2
```

**What to observe:**
- Backend failure detection
- Traffic redistribution
- Health check recovery

## Packet Capture and Analysis

### Capturing Traffic

```bash
# Start capture
python3 scripts/capture_traffic.py --interface eth0 --output pcap/week11_capture.pcap

# Alternative: use tcpdump directly
docker exec -it s11_nginx_lb tcpdump -i eth0 -w /tmp/capture.pcap
```

### Suggested Wireshark Filters

```
# HTTP traffic to load balancer
tcp.port == 8080 and http

# DNS queries
udp.port == 53 and dns

# FTP control channel
tcp.port == 21 and ftp

# Show only HTTP requests
http.request

# Filter by backend
http.host contains "web1" or http.host contains "web2"
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
# Remove all containers, networks, and volumes for this week
python3 scripts/cleanup.py --full

# Verify cleanup
docker system df
```

## Homework Assignments

See the `homework/` directory for take-home exercises.

### Assignment 1: Weighted Load Balancing
Modify the Nginx configuration to implement 3:2:1 weighted distribution and document the observed behaviour with evidence.

### Assignment 2: Custom Load Balancing Algorithm
Implement a response-time based load balancing algorithm in the Python load balancer that routes to the backend with lowest recent latency.

## Troubleshooting

### Common Issues

#### Issue: Port already in use
**Solution:**
```bash
sudo netstat -tlnp | grep 8080
sudo kill <pid>
```

#### Issue: Docker containers won't start
**Solution:**
```bash
docker compose down -v
docker system prune -f
docker compose up -d
```

#### Issue: Permission denied for packet capture
**Solution:** Run with sudo or use elevated WSL terminal.

#### Issue: Python module not found
**Solution:**
```bash
pip install -r setup/requirements.txt --break-system-packages
```

See `docs/troubleshooting.md` for more solutions.

## Theoretical Background

### FTP Architecture
FTP operates on a dual-connection model: a persistent control connection on port 21 for commands and a transient data connection (port 20 or dynamic) for file transfers. The protocol supports active mode (server initiates data connection) and passive mode (client initiates both connections, preferred with NAT/firewalls).

### DNS Resolution
DNS employs a hierarchical delegation system with root servers, TLD servers, and authoritative nameservers. Recursive resolvers perform iterative queries on behalf of clients, with multi-level caching (browser, OS, ISP) to reduce latency. TTL values balance freshness against query load.

### SSH Security
SSH provides confidentiality (AES, ChaCha20), integrity (HMAC), and authentication (publickey, password) through a layered architecture. The transport layer handles encryption and key exchange (Diffie-Hellman), whilst the connection layer multiplexes logical channels.

### Load Balancing Algorithms
Round-robin provides equal distribution; least-connections optimises for backend load; IP-hash ensures session affinity. Passive health checks mark backends as unavailable after consecutive failures, with recovery after timeout expiration.

## References

- Kurose, J. & Ross, K. (2021). *Computer Networking: A Top-Down Approach* (8th ed.). Pearson. ISBN: 978-0135928615
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming* (3rd ed.). Apress. DOI: 10.1007/978-1-4302-5855-1
- RFC 959 – File Transfer Protocol (FTP)
- RFC 1035 – Domain Names - Implementation and Specification
- RFC 4251-4254 – The Secure Shell (SSH) Protocol Architecture
- [Nginx Load Balancing Documentation](https://nginx.org/en/docs/http/load_balancing.html)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         WEEK 11 - NETWORK TOPOLOGY                          │
│              (WSL2 + Ubuntu 22.04 + Docker + Portainer)                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│    ┌─────────┐                                                              │
│    │ Client  │                                                              │
│    │ (curl)  │                                                              │
│    └────┬────┘                                                              │
│         │                                                                   │
│         │ HTTP :8080                                                        │
│         ▼                                                                   │
│    ┌─────────────────────────────────┐                                      │
│    │      LOAD BALANCER              │                                      │
│    │  ┌─────────────────────────┐    │                                      │
│    │  │  Python LB  │  Nginx   │    │                                      │
│    │  │  (didactic) │ (prod)   │    │                                      │
│    │  └─────────────────────────┘    │                                      │
│    │                                 │                                      │
│    │  Algorithms:                    │                                      │
│    │  • Round Robin                  │                                      │
│    │  • Least Connections            │                                      │
│    │  • IP Hash                      │                                      │
│    └────────────┬────────────────────┘                                      │
│                 │                                                           │
│     ┌───────────┼───────────┐                                               │
│     │           │           │                                               │
│     ▼           ▼           ▼                                               │
│ ┌───────┐   ┌───────┐   ┌───────┐                                           │
│ │Backend│   │Backend│   │Backend│    Docker Network: s11_network            │
│ │   1   │   │   2   │   │   3   │    Subnet: 172.28.0.0/16                  │
│ │ :8081 │   │ :8082 │   │ :8083 │                                           │
│ └───────┘   └───────┘   └───────┘                                           │
│                                                                             │
│  Portainer: http://localhost:9000 (global service)                          │
│  Credentials: stud / studstudstud                                           │
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
docker network inspect s11_network

# Check DNS in container
docker exec s11_nginx_lb cat /etc/resolv.conf
```

**Problem:** Port already in use
```bash
# Find what's using the port
sudo netstat -tlnp | grep 8080
# Or
sudo ss -tlnp | grep 8080

# Kill the process or use different port
```

### Load Balancer-Specific Issues

**Problem:** All requests go to same backend
- Check algorithm setting (round-robin vs ip_hash)
- Verify all backends are running and healthy

**Problem:** Backend not receiving requests
```bash
# Check if backend is registered
docker exec s11_nginx_lb cat /etc/nginx/nginx.conf | grep upstream -A 10
# Verify backend health
curl http://localhost:8081/
```

---

## 🧹 Complete Cleanup Procedure

### End of Session (Quick)

```bash
# Stop lab containers (Portainer stays running!)
cd /mnt/d/NETWORKING/WEEK11/11enWSL
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

## 📊 Week 11 Network Configuration Summary

| Resource | Value | Notes |
|----------|-------|-------|
| Network Subnet | 172.28.0.0/16 | s11_network |
| Nginx Load Balancer | s11_nginx_lb | Port 8080 |
| Backend 1 | s11_backend_1 | Internal only |
| Backend 2 | s11_backend_2 | Internal only |
| Backend 3 | s11_backend_3 | Internal only |
| Python Backend Ports | 8081, 8082, 8083 | Manual start |
| Portainer | 9000 | **RESERVED - Global service** |

---

*NETWORKING class - ASE, Informatics | by Revolvix*
*Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment*
