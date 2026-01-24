# Week 8: Transport Layer — HTTP Server Implementation and Reverse Proxies

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
> 
> by ing. dr. Antonio Clim

---

## ⚠️ Environment Notice

This laboratory kit is designed for the **WSL2 + Ubuntu 22.04 + Docker + Portainer** environment.

**Repository:** https://github.com/antonioclim/netENwsl
**This Week's Folder:** `8enWSL`

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

### Step 2: Clone the Repository

```powershell
# Create networking folder if it doesn't exist
mkdir D:\NETWORKING -ErrorAction SilentlyContinue
cd D:\NETWORKING

# Clone Week 8
git clone https://github.com/antonioclim/netENwsl.git WEEK8
cd WEEK8
```

### Step 3: Verify Clone
```powershell
dir
# You should see: docker/, scripts/, src/, README.md, www/, etc.
```

### Alternative: Clone Inside WSL

```bash
# In Ubuntu terminal
mkdir -p /mnt/d/NETWORKING
cd /mnt/d/NETWORKING
git clone https://github.com/antonioclim/netENwsl.git WEEK8
cd WEEK8
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
cd /mnt/d/NETWORKING/WEEK8/8enWSL
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

### Week 8 Network Configuration

Go to: **Networks → week8-laboratory-network**

Current configuration:
- Subnet: 172.28.8.0/24
- Gateway: 172.28.8.1
- nginx proxy: 172.28.8.10
- Backend servers: 172.28.8.21-23

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

### Essential Wireshark Filters for Week 8

| Filter | Purpose |
|--------|---------|
| `http` | All HTTP traffic |
| `tcp.port == 8080` | nginx proxy traffic |
| `tcp.port == 8443` | HTTPS traffic |
| `tcp.flags.syn == 1 && tcp.flags.ack == 0` | TCP SYN packets |
| `http.request` | HTTP requests only |
| `http.response.code == 200` | Successful responses |
| `http.response.code >= 400` | Error responses |
| `http.response.header matches "X-Backend"` | Backend identification |

### Analysing HTTP Request-Response

1. Filter: `http`
2. Find request packet (e.g., GET / HTTP/1.1)
3. Right-click → **Follow → TCP Stream**
4. View complete HTTP conversation with headers

### Saving Captures

1. **File → Save As**
2. Go to: `D:\NETWORKING\WEEK8\pcap\`
3. Filename: `capture_http.pcap`

---

## Overview

The transport layer sits between applications and the network, handling process-to-process communication through ports. It provides multiplexing (many applications sharing one network connection) and, with TCP, reliable data transfer with ordering guarantees.

This session covers TCP, UDP and TLS through practical work: building HTTP servers and reverse proxies from scratch. You will implement request parsers, static file servers and round-robin load balancers using Python sockets.

By building these components yourself, you will see exactly how TCP reliability supports HTTP — how the three-way handshake establishes connections, how sequence numbers maintain order and how the protocol recovers from packet loss. The exercises progress from basic socket operations to proxy implementations with security features like path validation and rate limiting.

The Docker infrastructure mirrors production patterns: nginx serves as reference reverse proxy while your Python servers demonstrate the underlying mechanics. Wireshark captures throughout illuminate connection establishment, data transfer and teardown.

## Learning Objectives

By the end of this laboratory session, you will be able to:

1. **Identify** the components of TCP and UDP headers and explain port numbers in process demultiplexing
2. **Describe** the three-way handshake mechanism and articulate why connection establishment requires exactly three messages
3. **Implement** a functional HTTP/1.1 server capable of parsing requests, serving static files and generating properly formatted responses
4. **Construct** a reverse proxy with round-robin load balancing that distributes requests across multiple backend servers
5. **Analyse** packet captures to distinguish TCP flags, correlate request-response pairs and identify connection state transitions
6. **Evaluate** security vulnerabilities in HTTP servers (directory traversal, resource exhaustion) and implement appropriate mitigations

## Prerequisites

### Knowledge Requirements
- Socket programming fundamentals from Week 3 (TCP client-server model)
- HTTP message format and status codes (application layer concepts)
- Basic understanding of process multiplexing and port allocation
- Familiarity with Docker container orchestration

### Software Requirements
- Windows 10/11 with WSL2 enabled
- Docker Engine (in WSL)
- Portainer CE (running globally on port 9000)
- Wireshark (native Windows) for packet analysis
- Python 3.11 or later
- Git (recommended for version control)
- curl or httpie for HTTP testing

### Hardware Requirements
- Minimum 8GB RAM (16GB recommended for comfortable Docker operation)
- 10GB free disk space
- Network connectivity for initial image pulls

## Quick Start

### First-Time Setup (Run Once)

```bash
# Open Ubuntu terminal (WSL)
wsl

# Go to the kit directory
cd /mnt/d/NETWORKING/WEEK8/8enWSL

# Start Docker if not running
sudo service docker start

# Verify prerequisites
python3 setup/verify_environment.py

# If any issues, run the installer helper
python3 setup/install_prerequisites.py

# Configure Docker for best performance
python3 setup/configure_docker.py
```

### Starting the Laboratory

```bash
# Start all services (nginx + 3 backend servers)
python3 scripts/start_lab.py

# Verify everything is running
python3 scripts/start_lab.py --status

# View real-time logs
docker compose -f docker/docker-compose.yml logs -f
```

### Accessing Services

| Service | URL/Port | Description |
|---------|----------|-------------|
| Portainer | http://localhost:9000 | Container management (stud / studstudstud) |
| nginx Proxy | http://localhost:8080 | Load-balanced entry point |
| nginx HTTPS | https://localhost:8443 | TLS-enabled proxy (self-signed) |
| Backend 1 | Internal only (8080) | Python HTTP server (BACKEND_ID=1) |
| Backend 2 | Internal only (8080) | Python HTTP server (BACKEND_ID=2) |
| Backend 3 | Internal only (8080) | Python HTTP server (BACKEND_ID=3) |

---

## 📚 Pedagogical Resources

Before starting the exercises, review these materials:

| Resource | Purpose |
|----------|---------|
| [docs/glossary.md](docs/glossary.md) | Key terms and definitions for Week 8 |
| [docs/misconceptions.md](docs/misconceptions.md) | Common mistakes and how to avoid them |
| [docs/concept_analogies.md](docs/concept_analogies.md) | Real-world analogies for abstract concepts |
| [docs/peer_instruction.md](docs/peer_instruction.md) | Discussion questions for deeper understanding |
| [docs/pair_programming_guide.md](docs/pair_programming_guide.md) | How to work effectively in pairs |
| [docs/code_tracing.md](docs/code_tracing.md) | Practice tracing code execution |
| [docs/parsons_problems.md](docs/parsons_problems.md) | Code reordering exercises |

---

## Laboratory Exercises

### Exercise 1: Minimal HTTP Server Implementation

**Objective:** Implement core HTTP request parsing and static file serving with security considerations

**Duration:** 45–60 minutes

**Conceptual Foundation:**

HTTP/1.1 transmits requests as plaintext over TCP with a defined structure: a request line (`METHOD SP REQUEST-TARGET SP HTTP-VERSION CRLF`), followed by header fields (`field-name ":" OWS field-value CRLF`), an empty line marking header termination and an optional message body. Your implementation must parse this format correctly, map request targets to filesystem paths and construct valid responses.

> 💭 **PREDICTION CHECKPOINT:** Before you begin, predict: What HTTP status code should your server return when a client requests a file that exists? What about a file that does not exist? What about an attempt to access `/../../../etc/passwd`?

**Steps:**

1. Go to the exercise file and examine the provided skeleton:
   ```bash
   cd /mnt/d/NETWORKING/WEEK8/8enWSL
   # View the exercise template
   python3 -c "print(open('src/exercises/ex_8_01_http_server.py').read())"
   ```

2. Implement the `parse_request()` function:
   - Decode raw bytes using ISO-8859-1 (the canonical HTTP header encoding)
   - Split on CRLF to separate request line from headers
   - Extract method, target and HTTP version from the request line
   - Normalise header names to lowercase for case-insensitive matching

3. Implement the `is_safe_path()` function:
   - Use `os.path.normpath()` to collapse `..` sequences
   - Verify the resolved path remains within the document root
   - This prevents directory traversal attacks (e.g., `/../../../etc/passwd`)

4. Implement `serve_file()` and `build_response()`:
   - Map extensions to MIME types
   - Handle index.html for directory requests
   - Return appropriate status codes (200, 403, 404, 405)

5. Test your implementation:
   ```bash
   # Start your server
   python3 src/exercises/ex_8_01_http_server.py --port 8081 --docroot www
   
   # In another terminal, test with curl
   curl -v http://localhost:8081/
   curl -v http://localhost:8081/hello.txt
   curl -v http://localhost:8081/../../etc/passwd
   curl -I http://localhost:8081/  # HEAD request
   ```

> 💭 **VERIFICATION CHECKPOINT:** Did the status codes match your predictions? If not, review the HTTP specification for status code meanings.

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 1
```

**Expected Observations:**
- GET requests return file contents with appropriate Content-Type
- HEAD requests return headers only (no body)
- Directory traversal attempts yield 403 Forbidden
- Non-existent files return 404 Not Found

---

### Exercise 2: Reverse Proxy with Round-Robin Load Balancing

**Objective:** Construct a reverse proxy that distributes incoming requests across multiple backend servers

**Duration:** 40–50 minutes

**Conceptual Foundation:**

A reverse proxy operates as an intermediary, accepting client connections and forwarding requests to backend servers. Round-robin load balancing cycles through available backends sequentially, distributing load evenly (assuming similar request costs). The proxy must preserve HTTP semantics, inject appropriate headers (e.g., `X-Forwarded-For`) and maintain connection management across both client-proxy and proxy-backend segments.

> 💭 **PREDICTION CHECKPOINT:** If you have 3 backends and send 9 requests, how many requests will each backend receive with round-robin? What happens if one backend fails?

**Steps:**

1. Examine the exercise template:
   ```bash
   python3 -c "print(open('src/exercises/ex_8_02_reverse_proxy.py').read())"
   ```

2. Implement the `RoundRobinBalancer` class:
   - Maintain a list of backend addresses
   - Track the current index for round-robin selection
   - Use modular arithmetic for cyclic iteration

3. Implement `forward_request()`:
   - Connect to the selected backend
   - Forward the original request (with modified Host header if necessary)
   - Add `X-Forwarded-For` header with the original client IP
   - Relay the backend response to the client

4. Launch three backend servers (in separate terminals):
   ```bash
   # Terminal 1
   python3 src/apps/backend_server.py --port 9001 --id A
   
   # Terminal 2
   python3 src/apps/backend_server.py --port 9002 --id B
   
   # Terminal 3
   python3 src/apps/backend_server.py --port 9003 --id C
   ```

5. Start your proxy:
   ```bash
   # Terminal 4
   python3 src/exercises/ex_8_02_reverse_proxy.py --port 8888 --backends 127.0.0.1:9001,127.0.0.1:9002,127.0.0.1:9003
   ```

6. Generate traffic and observe distribution:
   ```bash
   for i in {1..9}; do curl -sS http://localhost:8888/ 2>/dev/null | grep -o 'Backend [A-C]'; done
   ```

> 💭 **VERIFICATION CHECKPOINT:** Did you see the pattern A → B → C → A → B → C → A → B → C? If not, check your modular arithmetic in `next_backend()`.

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 2
```

**Expected Observations:**
- Requests cycle through backends: A → B → C → A → B → C...
- Response headers include `X-Served-By` indicating the backend
- Proxy adds `X-Forwarded-For` with client address

---

### Exercise 3: POST Request Handling

**Objective:** Extend the HTTP server to process POST requests with body content

**Duration:** 30–40 minutes

> 💭 **PREDICTION CHECKPOINT:** How does a server know how many bytes to read for the request body? What header provides this information?

**Steps:**

1. Implement Content-Length parsing in request headers
2. Read exactly Content-Length bytes for the request body
3. Parse form data (application/x-www-form-urlencoded)
4. Implement a simple endpoint that echoes received data

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 3

# Manual test
curl -X POST -d "name=Student&course=Networks" http://localhost:8081/api/echo
```

---

### Exercise 4: Rate Limiting

**Objective:** Implement token bucket rate limiting to prevent resource exhaustion

**Duration:** 35–45 minutes

**Conceptual Foundation:**

The token bucket algorithm maintains a reservoir of tokens that replenish at a fixed rate. Each request consumes one token; if the bucket is empty, the request is rejected (429 Too Many Requests). This provides burst tolerance while enforcing sustained rate limits.

> 💭 **PREDICTION CHECKPOINT:** With a bucket capacity of 10 tokens and refill rate of 1 token/second, what happens if 15 requests arrive simultaneously? How many succeed? How many fail?

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 4

# Flood test
for i in {1..100}; do curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8081/; done | sort | uniq -c
```

---

### Exercise 5: Caching Proxy

**Objective:** Implement response caching with Cache-Control header interpretation

**Duration:** 45–55 minutes

> 💭 **PREDICTION CHECKPOINT:** If a response has `Cache-Control: max-age=60`, how long should the proxy serve the cached version? What happens after 60 seconds?

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 5
```

---

## Demonstrations

### Demo 1: Docker Infrastructure with nginx Load Balancer

This demonstration showcases the production-grade nginx reverse proxy configuration with three Python backend servers.

```bash
python3 scripts/run_demo.py --demo docker-nginx
```

**What to observe:**
- nginx distributes requests using round-robin by default
- Backend identification via X-Backend-ID header
- Graceful handling of backend failures
- Access logs showing request routing

### Demo 2: HTTP Server Internals

Shows the request-response cycle with detailed logging.

```bash
python3 scripts/run_demo.py --demo http-server
```

**What to observe:**
- Request parsing breakdown (method, path, headers)
- File resolution and MIME type detection
- Response construction with proper headers

### Demo 3: Three-Way Handshake Capture

Captures and analyses TCP connection establishment.

```bash
python3 scripts/run_demo.py --demo handshake
```

**What to observe:**
- SYN packet from client
- SYN-ACK response from server
- ACK completing the handshake
- Sequence number initialisation

## Packet Capture and Analysis

### Capturing Traffic

```bash
# Start capture for HTTP traffic
python3 scripts/capture_traffic.py --interface lo --filter "tcp port 8080" --output pcap/week8_http.pcap

# Capture proxy-to-backend traffic
python3 scripts/capture_traffic.py --interface docker0 --filter "tcp port 8080" --output pcap/week8_proxy.pcap
```

### Suggested Wireshark Filters

```
# HTTP traffic only
http

# TCP handshake (SYN packets)
tcp.flags.syn == 1 && tcp.flags.ack == 0

# All packets to/from port 8080
tcp.port == 8080

# HTTP requests only
http.request

# HTTP responses with specific status
http.response.code == 200
http.response.code >= 400

# Follow TCP stream
tcp.stream eq 0

# Packets with specific backend
http.response.header matches "X-Backend"
```

### Analysis Exercises

1. **Identify the three-way handshake:**
   - Filter: `tcp.flags.syn == 1`
   - Count SYN and SYN-ACK packets

2. **Calculate response times:**
   - Compare request timestamp with response timestamp
   - Use Statistics → Conversations → TCP

3. **Examine keep-alive behaviour:**
   - Observe multiple requests on a single TCP connection
   - Note the Connection: keep-alive header

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

# Also prune unused Docker resources
python3 scripts/cleanup.py --full --prune

# Verify cleanup
docker system df
```

## Homework Assignments

See the `homework/` directory for take-home exercises.

### Assignment 1: HTTPS Server with Self-Signed Certificate
Extend the HTTP server to support TLS using Python's `ssl` module. Generate a self-signed certificate and configure the server to accept HTTPS connections. Document the TLS handshake observed in Wireshark.

**Deliverables:** Python implementation + Wireshark capture + analysis report

### Assignment 2: Weighted Load Balancer
Modify the round-robin proxy to support weighted distribution. Backend servers should be configurable with weights (e.g., 5:3:1) and requests should be distributed proportionally.

**Deliverables:** Python implementation + test demonstrating distribution

## Troubleshooting

### Common Issues

#### Issue: "Address already in use" when starting server
**Solution:** Another process is using the port. Find and terminate it:
```bash
# On WSL/Linux
lsof -i :8080
kill -9 <PID>

# Or use a different port
python3 src/exercises/ex_8_01_http_server.py --port 8082
```

#### Issue: Docker containers fail to start
**Solution:** Ensure Docker is running in WSL:
```bash
sudo service docker start
docker info
```

#### Issue: curl returns "Connection refused"
**Solution:** Verify the server is running and listening:
```bash
netstat -tlnp | grep 8080
python3 scripts/start_lab.py --status
```

#### Issue: Wireshark doesn't show HTTP traffic
**Solution:** Ensure you're capturing on the correct interface. For Docker traffic, use `vEthernet (WSL)`. For localhost, use the loopback interface.

See `docs/troubleshooting.md` for more solutions.

## Theoretical Background

### Transport Layer Fundamentals

The transport layer provides logical communication between application processes running on different hosts. While the network layer (IP) delivers packets between hosts, the transport layer extends this to process-to-process delivery through the port abstraction.

**Key Mechanisms:**
- **Multiplexing/Demultiplexing:** Using port numbers to direct segments to the correct socket
- **Reliability (TCP):** Sequence numbers, acknowledgments, retransmission
- **Flow Control (TCP):** Receiver advertised window prevents buffer overflow
- **Congestion Control (TCP):** Additive increase, multiplicative decrease (AIMD)

### TCP vs UDP Trade-offs

| Characteristic | TCP | UDP |
|---------------|-----|-----|
| Connection | Required (handshake) | Connectionless |
| Reliability | Guaranteed delivery | Best-effort |
| Ordering | Preserved | Not guaranteed |
| Overhead | 20+ byte header | 8 byte header |
| Use Cases | HTTP, FTP, SSH | DNS, VoIP, Gaming |

### HTTP Over TCP

HTTP/1.1 relies on TCP's reliable, ordered byte stream. Each HTTP request-response exchange occurs over a TCP connection (possibly reused with keep-alive). The transport layer handles retransmission of lost segments transparently to the application.

### Reverse Proxy Architecture

```
┌──────────┐     ┌─────────────────┐     ┌──────────────┐
│  Client  │────▶│  Reverse Proxy  │────▶│  Backend 1   │
└──────────┘     │    (nginx)      │────▶│  Backend 2   │
                 └─────────────────┘────▶│  Backend 3   │
                                         └──────────────┘
```

Benefits: Load distribution, SSL termination, caching, security isolation

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        WEEK 8 WSL Kit Architecture                  │
│              (WSL2 + Ubuntu 22.04 + Docker + Portainer)            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   Windows Host (PowerShell)                                         │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │  Wireshark          curl/httpie        Browser              │  │
│   │  (Packet Capture)   (HTTP Client)      (localhost:8080)     │  │
│   └─────────────┬───────────────┬──────────────────┬────────────┘  │
│                 │               │                  │                │
├─────────────────┼───────────────┼──────────────────┼────────────────┤
│                 ▼               ▼                  ▼                │
│   WSL2 / Docker Engine                                             │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │                    docker-compose                            │  │
│   │  ┌────────────────────────────────────────────────────────┐ │  │
│   │  │               week8-network (172.28.8.0/24)            │ │  │
│   │  │  ┌─────────────┐                                       │ │  │
│   │  │  │   nginx     │◀─── Port 8080 (HTTP)                  │ │  │
│   │  │  │  (proxy)    │◀─── Port 8443 (HTTPS)                 │ │  │
│   │  │  └──────┬──────┘                                       │ │  │
│   │  │         │ Round-Robin                                  │ │  │
│   │  │    ┌────┼────┬────────────┐                           │ │  │
│   │  │    ▼    ▼    ▼            │                           │ │  │
│   │  │  ┌────┐┌────┐┌────┐       │                           │ │  │
│   │  │  │ B1 ││ B2 ││ B3 │ Python HTTP Servers              │ │  │
│   │  │  │8080││8080││8080│ (backend_server.py)              │ │  │
│   │  │  └────┘└────┘└────┘                                   │ │  │
│   │  └────────────────────────────────────────────────────────┘ │  │
│   │                                                              │  │
│   │  Portainer: http://localhost:9000 (global service)          │  │
│   │  Credentials: stud / studstudstud                           │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## References

- Kurose, J. & Ross, K. (2021). *Computer Networking: A Top-Down Approach* (8th ed.). Pearson. Chapter 3: Transport Layer.
- Rhodes, B. & Goerzen, J. (2014). *Foundations of Python Network Programming* (3rd ed.). Apress.
- RFC 793 – Transmission Control Protocol (TCP)
- RFC 768 – User Datagram Protocol (UDP)
- RFC 9110 – HTTP Semantics
- RFC 9112 – HTTP/1.1
- RFC 8446 – TLS 1.3
- nginx Documentation: https://nginx.org/en/docs/

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
docker network inspect week8-laboratory-network

# Check DNS in container
docker exec week8-nginx-proxy cat /etc/resolv.conf
```

**Problem:** Port already in use
```bash
# Find what's using the port
sudo netstat -tlnp | grep 8080
# Or
sudo ss -tlnp | grep 8080

# Kill the process or use different port
```

### HTTP-Specific Issues

**Problem:** curl shows "Empty reply from server"
- Check server logs: `docker compose logs backend1`
- Verify server is processing requests

**Problem:** nginx returns 502 Bad Gateway
- Check if backend servers are running
- Verify nginx upstream configuration

---

## 🧹 Complete Cleanup Procedure

### End of Session (Quick)

```bash
# Stop lab containers (Portainer stays running!)
cd /mnt/d/NETWORKING/WEEK8/8enWSL
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

## 📊 Week 8 Network Configuration Summary

| Resource | Value | Notes |
|----------|-------|-------|
| Network Subnet | 172.28.8.0/24 | week8-laboratory-network |
| Gateway | 172.28.8.1 | Docker bridge gateway |
| nginx proxy IP | 172.28.8.10 | Load balancer |
| Backend 1 IP | 172.28.8.21 | Alpha |
| Backend 2 IP | 172.28.8.22 | Beta |
| Backend 3 IP | 172.28.8.23 | Gamma |
| nginx HTTP | 8080 | Proxy entry point |
| nginx HTTPS | 8443 | TLS termination |
| Backend Port | 8080 | Internal only |
| Portainer | 9000 | **RESERVED - Global service** |

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
*Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment*
