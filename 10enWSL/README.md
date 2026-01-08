# Week 10: Application Layer Protocols — HTTP/HTTPS, REST and Network Services

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
>
> by Revolvix

---

## ⚠️ Environment Notice

This laboratory kit is designed for the **WSL2 + Ubuntu 22.04 + Docker + Portainer** environment.

**Repository:** https://github.com/antonioclim/netENwsl
**This Week's Folder:** `10enWSL`

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

# Clone Week 10
git clone https://github.com/antonioclim/netENwsl.git WEEK10
cd WEEK10
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
git clone https://github.com/antonioclim/netENwsl.git WEEK10
cd WEEK10
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
cd /mnt/d/NETWORKING/WEEK10/10enWSL
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

### Week 10 Network Configuration

Navigate: **Networks → week10_labnet**

Current configuration:
- Subnet: 172.20.0.0/24
- Web server: 172.20.0.10
- DNS server: 172.20.0.53
- SSH server: 172.20.0.22
- FTP server: 172.20.0.21
- Debug container: 172.20.0.200

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

### Essential Wireshark Filters for Week 10

| Filter | Purpose |
|--------|---------|
| `tcp.port == 8000 && http` | HTTP traffic to web server |
| `udp.port == 5353` | DNS queries to custom server |
| `tcp.port == 2222` | SSH connections |
| `tcp.port == 2121` | FTP control channel |
| `tcp.portrange == 30000-30009` | FTP passive data channels |
| `ssl.handshake` | TLS handshakes (HTTPS) |
| `ip.addr == 172.20.0.0/24` | All lab network traffic |
| `http.request` | HTTP requests only |
| `dns` | DNS protocol traffic |

### Analysing Application Layer Protocols

1. **HTTP Analysis**: Filter `http`, examine request methods, status codes
2. **DNS Analysis**: Filter `dns`, check query names and response IPs
3. **SSH Analysis**: Filter `tcp.port == 2222`, observe encrypted payloads
4. **TLS Analysis**: Filter `ssl`, examine certificate exchange

### Saving Captures

1. **File → Save As**
2. Navigate to: `D:\NETWORKING\WEEK10\pcap\`
3. Filename: `capture_week10.pcap`

---

## Overview

This laboratory explores the application layer of the TCP/IP protocol stack, focusing on HTTP/HTTPS communication, RESTful API design patterns, and fundamental network services including DNS, SSH and FTP. The session bridges theoretical protocol specifications with practical implementation through Docker-orchestrated service environments and Python-based exercises.

The HTTP protocol forms the backbone of modern web communication, operating as a stateless request-response mechanism over TCP. Its secure variant, HTTPS, encapsulates HTTP within TLS (Transport Layer Security), providing authentication, confidentiality and data integrity. Understanding the architectural distinctions between these protocols—and the cryptographic handshake that precedes encrypted communication—is essential for any network practitioner.

REST (Representational State Transfer) represents an architectural style for distributed hypermedia systems. The Richardson Maturity Model provides a structured progression from RPC-style interactions (Level 0) through resource-oriented URIs (Level 1), proper HTTP verb semantics (Level 2), to full HATEOAS compliance (Level 3). This laboratory provides working implementations at each maturity level, enabling comparative analysis of API design patterns.

## Learning Objectives

By the end of this laboratory session, you will be able to:

1. **Recall** the structure of HTTP request and response messages, including methods, status codes, headers and body formats
2. **Explain** the role of TLS in HTTPS communication and describe the certificate validation process
3. **Implement** a minimal HTTPS server with CRUD endpoints and interact with it using standard tools
4. **Analyse** network traffic captures to distinguish between plaintext HTTP, encrypted HTTPS and other application protocols
5. **Compare** API implementations across REST maturity levels and justify design decisions
6. **Evaluate** the trade-offs between different network service protocols (DNS over UDP, SSH encryption, FTP multi-channel architecture)

## Prerequisites

### Knowledge Requirements
- Familiarity with TCP/IP fundamentals (Weeks 1-5)
- Understanding of socket programming concepts (Week 3)
- Basic experience with Docker containers (Week 6+)
- Python programming proficiency

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
cd /mnt/d/NETWORKING/WEEK10/10enWSL

# Start Docker if not running
sudo service docker start

# Verify prerequisites are installed
python3 setup/verify_environment.py

# If any issues arise, run the installer helper
python3 setup/install_prerequisites.py
```

### Starting the Laboratory

```bash
# Start all Docker services
python3 scripts/start_lab.py

# Verify services are healthy
python3 scripts/start_lab.py --status
```

### Accessing Services

| Service | URL/Port | Credentials |
|---------|----------|-------------|
| Portainer | http://localhost:9000 | stud / studstudstud |
| HTTP Web Server | http://localhost:8000 | None required |
| Custom DNS Server | localhost:5353/udp | N/A |
| SSH Server | localhost:2222 | labuser / labpass |
| FTP Server | localhost:2121 | labftp / labftp |
| HTTPS API (Exercise) | https://localhost:8443 | None required |
| REST Levels (Exercise) | http://localhost:5000 | None required |

## Laboratory Exercises

### Exercise 1: HTTP Service Exploration

**Objective:** Observe HTTP request-response cycles and correlate with TCP segment behaviour.

**Duration:** 20 minutes

**Steps:**

1. Ensure the Docker stack is running:
   ```bash
   python3 scripts/start_lab.py --status
   ```

2. Query the HTTP service from the terminal:
   ```bash
   curl -v http://localhost:8000/
   curl -v http://localhost:8000/hello.txt
   ```

3. Observe the following in the verbose output:
   - HTTP version in the response line (HTTP/1.0 or HTTP/1.1)
   - Response headers: Content-Type, Content-Length, Server
   - Connection behaviour (Keep-Alive vs close)

4. Open Wireshark and capture on the Docker network interface.

5. Re-run the curl commands and correlate HTTP requests with TCP segments.

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 1
```

**Expected Observations:**
- HTTP operates over TCP port 80 (or 8000 in our configuration)
- Request and response are plaintext, visible in packet captures
- TCP three-way handshake precedes any HTTP data

### Exercise 2: DNS Resolution with Custom Server

**Objective:** Understand DNS message structure and UDP request-response patterns.

**Duration:** 15 minutes

**Steps:**

1. Query the custom DNS server using dig (from WSL or debug container):
   ```bash
   # From WSL
   dig @127.0.0.1 -p 5353 myservice.lab.local +short
   dig @127.0.0.1 -p 5353 api.lab.local +short
   dig @127.0.0.1 -p 5353 nonexistent.lab.local +short
   ```

2. Alternatively, enter the debug container:
   ```bash
   docker exec -it week10_debug bash
   dig @dns-server -p 5353 web.lab.local +short
   ```

3. Observe the difference between successful resolution and NXDOMAIN responses.

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 2
```

**Expected Observations:**
- DNS typically uses UDP (connectionless)
- Single request yields single response
- NXDOMAIN (RCODE 3) indicates non-existent domain

### Exercise 3: SSH Encrypted Communication

**Objective:** Observe SSH handshake and understand why payload is not visible in captures.

**Duration:** 15 minutes

**Steps:**

1. Connect to the SSH server from the terminal:
   ```bash
   ssh -p 2222 labuser@localhost
   # Password: labpass
   ```

2. Execute a simple command in the SSH session:
   ```bash
   hostname
   whoami
   exit
   ```

3. Run the automated Paramiko demo:
   ```bash
   python3 src/apps/ssh_demo.py
   ```

4. Capture the SSH traffic in Wireshark and examine the handshake packets.

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 3
```

**Expected Observations:**
- SSH banner exchange visible in initial packets
- Key exchange packets contain algorithm negotiation
- After handshake completion, all payload is encrypted

### Exercise 4: FTP Multi-Channel Protocol

**Objective:** Understand FTP control and data channel separation.

**Duration:** 15 minutes

**Steps:**

1. Connect to the FTP server using Python ftplib:
   ```bash
   python3 src/apps/ftp_demo.py
   ```

2. Alternatively, use an interactive client from WSL:
   ```bash
   lftp -u labftp,labftp -p 2121 localhost
   ls
   get welcome.txt
   bye
   ```

3. Observe multiple TCP connections in Wireshark during file listing and transfer.

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 4
```

**Expected Observations:**
- Control connection on port 2121 carries commands (LIST, RETR, STOR)
- Data connections use passive ports (30000-30009 range)
- NAT and firewall traversal requires passive mode configuration

### Exercise 5: HTTPS with TLS Certificate

**Objective:** Implement and test a secure HTTPS endpoint with self-signed certificates.

**Duration:** 25 minutes

**Steps:**

1. Generate a self-signed TLS certificate:
   ```bash
   python3 src/exercises/ex_10_01_https.py generate-cert
   ```

2. Start the HTTPS server:
   ```bash
   python3 src/exercises/ex_10_01_https.py serve --host 0.0.0.0 --port 8443
   ```

3. In another terminal, interact with the API:
   ```bash
   # List resources (initially empty)
   curl -k https://localhost:8443/api/resources

   # Create a resource
   curl -k -X POST https://localhost:8443/api/resources -H "Content-Type: application/json" -d '{"name":"sensor1","value":42}'

   # Get the created resource
   curl -k https://localhost:8443/api/resources/1

   # Update the resource
   curl -k -X PUT https://localhost:8443/api/resources/1 -H "Content-Type: application/json" -d '{"name":"sensor1-updated","value":100}'

   # Delete the resource
   curl -k -X DELETE https://localhost:8443/api/resources/1
   ```

4. Run the automated selftest:
   ```bash
   python3 src/exercises/ex_10_01_https.py selftest
   ```

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 5
```

**Expected Observations:**
- TLS handshake occurs before any HTTP data
- Certificate warning (-k flag bypasses validation)
- HTTP status codes: 200 OK, 201 Created, 204 No Content, 404 Not Found

### Exercise 6: REST Maturity Levels (Richardson Model)

**Objective:** Compare API design across all four REST maturity levels.

**Duration:** 30 minutes

**Steps:**

1. Start the Flask application:
   ```bash
   python3 src/exercises/ex_10_02_rest_levels.py serve --host 127.0.0.1 --port 5000
   ```

2. Test Level 0 (RPC style):
   ```bash
   curl -X POST http://localhost:5000/level0/service -H "Content-Type: application/json" -d '{"action":"list_users"}'
   curl -X POST http://localhost:5000/level0/service -H "Content-Type: application/json" -d '{"action":"get_user","id":1}'
   ```

3. Test Level 1 (Resource URIs with action endpoints):
   ```bash
   curl http://localhost:5000/level1/users
   curl http://localhost:5000/level1/users/1
   curl -X POST http://localhost:5000/level1/users/1/update -H "Content-Type: application/json" -d '{"name":"Updated"}'
   ```

4. Test Level 2 (Proper HTTP verbs):
   ```bash
   curl http://localhost:5000/level2/users
   curl -X POST http://localhost:5000/level2/users -H "Content-Type: application/json" -d '{"name":"New User","email":"new@example.test"}'
   curl -X PUT http://localhost:5000/level2/users/3 -H "Content-Type: application/json" -d '{"name":"Modified"}'
   curl -X DELETE http://localhost:5000/level2/users/3
   ```

5. Test Level 3 (HATEOAS):
   ```bash
   curl http://localhost:5000/level3/users
   ```
   Note the `_links` section in responses.

6. Run the selftest:
   ```bash
   python3 src/exercises/ex_10_02_rest_levels.py selftest
   ```

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 6
```

**Expected Observations:**
- Level 0: Single endpoint, action parameter distinguishes operations
- Level 1: Resources have distinct URIs, but verbs are inconsistent
- Level 2: GET, POST, PUT, DELETE semantics respected
- Level 3: Hypermedia links enable client navigation

## Demonstrations

### Demo 1: Complete Service Stack

Automated demonstration of all Docker services.

```bash
python3 scripts/run_demo.py --demo 1
```

**What to observe:**
- HTTP fetch returns HTML content
- DNS queries resolve to configured IP addresses
- SSH connection executes remote command
- FTP lists directory contents

### Demo 2: Protocol Comparison

Side-by-side comparison of HTTP vs HTTPS traffic visibility.

```bash
python3 scripts/run_demo.py --demo 2
```

**What to observe:**
- HTTP request/response visible in plaintext
- HTTPS shows TLS handshake, encrypted application data
- Certificate information extractable from handshake

## Packet Capture and Analysis

### Capturing Traffic

```bash
# Start capture with helper script
python3 scripts/capture_traffic.py --interface eth0 --output pcap/week10_capture.pcap

# Or use Wireshark directly on the WSL network interface
```

### Suggested Wireshark Filters

```
# HTTP traffic to the demo web server
tcp.port == 8000 && http

# DNS queries to custom server
udp.port == 5353

# SSH connections
tcp.port == 2222

# FTP control and data channels
tcp.port == 2121 || tcp.portrange == 30000-30009

# TLS handshakes
ssl.handshake

# All traffic on the lab network
ip.addr == 172.20.0.0/24
```

### Traffic Analysis with tshark

```bash
# DNS queries and responses
tshark -r pcap/week10_capture.pcap -Y "udp.port==5353" -T fields -e dns.qry.name -e dns.flags.rcode

# HTTP requests
tshark -r pcap/week10_capture.pcap -Y "http.request" -T fields -e http.request.method -e http.host -e http.request.uri

# TCP connection initiators
tshark -r pcap/week10_capture.pcap -Y "tcp.flags.syn==1 && tcp.flags.ack==0" -T fields -e ip.dst -e tcp.dstport
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

### Assignment 1: SOAP Endpoint Implementation

Implement a minimal SOAP service and compare its message structure with the REST exercises. Document the XML envelope format and error handling patterns.

### Assignment 2: HTTPS Certificate Chain Analysis

Using OpenSSL and Wireshark, analyse the certificate chain of a public HTTPS website. Document the root CA, intermediate certificates and end-entity certificate. Explain the role of each.

### Assignment 3: Multi-Service Docker Composition

Extend the provided Docker Compose configuration to include an additional service (e.g., a reverse proxy with nginx). Document the network topology changes and demonstrate traffic flow.

## Troubleshooting

### Common Issues

#### Issue: Docker permission denied
**Solution:** Ensure Docker is running in WSL and your user is in the docker group. Run `sudo service docker start` and verify with `docker ps`.

#### Issue: Port already in use
**Solution:** Check with `sudo netstat -tlnp | grep <PORT>` and terminate the conflicting process, or modify the port mapping in docker-compose.yml.

#### Issue: Certificate validation errors
**Solution:** Expected for self-signed certificates. Use `curl -k` or configure your client to trust the generated CA. For production, use certificates from a trusted CA.

#### Issue: DNS queries not resolving
**Solution:** Ensure the dns-server container is healthy with `docker ps`. Query explicitly with the correct port: `dig @127.0.0.1 -p 5353 <hostname>`.

See `docs/troubleshooting.md` for additional solutions.

## Theoretical Background

### HTTP/HTTPS Architecture

HTTP operates as a request-response protocol where clients (typically web browsers or API consumers) initiate connections to servers. Each request consists of a method (GET, POST, PUT, DELETE, etc.), URI, headers and optional body. Responses include a status code, headers and body.

HTTPS wraps HTTP within TLS, adding a cryptographic layer that provides:
- **Authentication**: Server identity verified via X.509 certificates
- **Confidentiality**: Symmetric encryption protects data in transit
- **Integrity**: Message authentication codes detect tampering

The TLS handshake negotiates cipher suites, exchanges keys and establishes the secure channel before any HTTP data flows.

### REST Architectural Style

REST (Representational State Transfer) defines constraints for scalable, stateless distributed systems:
- **Client-Server separation**: Concerns are isolated
- **Statelessness**: Each request contains all necessary context
- **Cacheability**: Responses indicate cache directives
- **Uniform Interface**: Resources identified by URIs, manipulated through representations
- **Layered System**: Intermediaries (proxies, gateways) are transparent

The Richardson Maturity Model grades API implementations:
- **Level 0**: HTTP as transport for RPC
- **Level 1**: Resources with distinct URIs
- **Level 2**: HTTP verbs used semantically
- **Level 3**: Hypermedia as the Engine of Application State (HATEOAS)

### Network Services

**DNS (Domain Name System)**: Hierarchical naming system translating domain names to IP addresses. Typically uses UDP port 53, though TCP is used for zone transfers and large responses.

**SSH (Secure Shell)**: Cryptographic network protocol for secure remote access. Provides authentication, encryption and integrity protection. Uses TCP port 22.

**FTP (File Transfer Protocol)**: Multi-channel protocol separating control commands (port 21) from data transfer. Active mode has server connect to client; passive mode has client initiate both connections.

## References

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (7th ed.). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming* (3rd ed.). Apress.
- Fielding, R. T. (2000). *Architectural Styles and the Design of Network-based Software Architectures*. Doctoral dissertation, University of California, Irvine.
- RFC 7230-7235: HTTP/1.1 Specification
- RFC 8446: TLS 1.3
- RFC 1035: Domain Names - Implementation and Specification
- RFC 4251-4254: SSH Protocol Architecture

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    WEEK10 Docker Network (172.20.0.0/24)            │
│              (WSL2 + Ubuntu 22.04 + Docker + Portainer)             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐             │
│  │   web       │    │ dns-server  │    │ ssh-server  │             │
│  │ 172.20.0.10 │    │ 172.20.0.53 │    │ 172.20.0.22 │             │
│  │  :8000/tcp  │    │  :5353/udp  │    │   :22/tcp   │             │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘             │
│         │                  │                  │                     │
│  ┌──────┴──────────────────┴──────────────────┴──────┐             │
│  │                  labnet (bridge)                   │             │
│  └──────┬──────────────────┬──────────────────┬──────┘             │
│         │                  │                  │                     │
│  ┌──────┴──────┐    ┌──────┴──────┐    ┌──────┴──────┐             │
│  │ ftp-server  │    │ ssh-client  │    │   debug     │             │
│  │ 172.20.0.21 │    │ 172.20.0.100│    │ 172.20.0.200│             │
│  │  :2121/tcp  │    │  Paramiko   │    │ curl/dig/   │             │
│  │:30000-30009 │    │             │    │ tcpdump/nmap│             │
│  └─────────────┘    └─────────────┘    └─────────────┘             │
│                                                                     │
│  Portainer: http://localhost:9000 (global service)                  │
│  Credentials: stud / studstudstud                                   │
└─────────────────────────────────────────────────────────────────────┘

Host Port Mappings:
  • 8000  → web:8000        (HTTP)
  • 5353  → dns-server:5353 (DNS/UDP)
  • 2222  → ssh-server:22   (SSH)
  • 2121  → ftp-server:2121 (FTP control)
  • 30000-30009 → ftp-server (FTP passive data)
  • 9000  → Portainer       (RESERVED - Global)
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
docker network inspect week10_labnet

# Check DNS in container
docker exec week10_debug cat /etc/resolv.conf
```

**Problem:** Port already in use
```bash
# Find what's using the port
sudo netstat -tlnp | grep 8000
# Or
sudo ss -tlnp | grep 8000

# Kill the process or use different port
```

### Service-Specific Issues

**Problem:** SSH connection refused
```bash
# Check if SSH server is running
docker ps | grep week10_ssh
docker logs week10_ssh
```

**Problem:** FTP passive mode fails
- Ensure ports 30000-30009 are mapped in docker-compose.yml
- Check Windows Firewall is not blocking these ports

**Problem:** DNS queries timeout
```bash
# Check DNS server is running
docker logs week10_dns
# Query with verbose output
dig @127.0.0.1 -p 5353 web.lab.local +trace
```

---

## 🧹 Complete Cleanup Procedure

### End of Session (Quick)

```bash
# Stop lab containers (Portainer stays running!)
cd /mnt/d/NETWORKING/WEEK10/10enWSL
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

## 📊 Week 10 Network Configuration Summary

| Resource | Value | Notes |
|----------|-------|-------|
| Network Subnet | 172.20.0.0/24 | week10_labnet |
| Web Server IP | 172.20.0.10 | HTTP port 8000 |
| DNS Server IP | 172.20.0.53 | UDP port 5353 |
| SSH Server IP | 172.20.0.22 | TCP port 2222 (mapped) |
| FTP Server IP | 172.20.0.21 | TCP port 2121 |
| FTP Passive Range | 30000-30009 | Data channels |
| Debug Container | 172.20.0.200 | Network tools |
| SSH Credentials | labuser / labpass | SSH server |
| FTP Credentials | labftp / labftp | FTP server |
| Portainer | 9000 | **RESERVED - Global service** |

---

*NETWORKING class - ASE, Informatics | by Revolvix*
*Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment*
