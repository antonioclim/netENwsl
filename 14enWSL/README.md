# Week 14: Integrated Recap and Project Evaluation

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
>
> by Revolvix

## Overview

This laboratory session serves as a comprehensive review and integration of concepts covered throughout the Computer Networks course. The practical focus centres on building and validating a complete network topology that incorporates multiple services communicating across a containerised environment.

The topology demonstrates fundamental networking principles through a load-balanced web application architecture: a client generates HTTP traffic directed at a reverse proxy, which distributes requests across multiple backend servers using round-robin scheduling. Additionally, a TCP echo service validates basic socket communication patterns. All traffic can be captured and analysed using standard packet analysis tools.

This kit is designed for Windows 10/11 with WSL2 (Windows Subsystem for Linux) and Docker Desktop, providing a portable environment that students can deploy on their personal machines without requiring dedicated virtual machines or native Linux installations.

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
| Docker Desktop | 4.0+ | Container runtime with WSL2 integration |
| Python | 3.11+ | Script execution and automation |
| Wireshark | 4.0+ | Packet capture analysis (native Windows) |
| Git | 2.30+ | Version control (optional) |

### Hardware Requirements

- **Minimum:** 8 GB RAM, 10 GB free disk space, dual-core processor
- **Recommended:** 16 GB RAM, SSD storage, quad-core processor
- Network connectivity for pulling Docker images

## Quick Start

### First-Time Setup (Run Once)

```powershell
# Open PowerShell as Administrator
cd WEEK14_WSLkit

# Verify all prerequisites are installed
python setup/verify_environment.py

# If any checks fail, run the prerequisite installer
python setup/install_prerequisites.py

# Configure Docker for the lab
python setup/configure_docker.py
```

### Starting the Laboratory

```powershell
# Start all services (builds images if needed)
python scripts/start_lab.py

# Check service status
python scripts/start_lab.py --status

# View real-time logs
docker compose -f docker/docker-compose.yml logs -f
```

### Accessing Services

| Service | URL/Port | Description | Credentials |
|---------|----------|-------------|-------------|
| Portainer | https://localhost:9443 | Container management UI | Set on first access |
| Load Balancer | http://localhost:8080 | Reverse proxy frontend | None |
| LB Status | http://localhost:8080/lb-status | Backend statistics | None |
| Backend 1 | http://localhost:8001 | Direct backend access | None |
| Backend 2 | http://localhost:8002 | Direct backend access | None |
| TCP Echo | localhost:9000 | Echo protocol server | None |

## Laboratory Exercises

### Exercise 1: Environment Verification and Service Discovery

**Objective:** Confirm the laboratory environment is correctly configured and understand the service topology.

**Duration:** 15 minutes

**Steps:**

1. Run the environment verification script:
   ```powershell
   python setup/verify_environment.py
   ```

2. Start the laboratory environment:
   ```powershell
   python scripts/start_lab.py
   ```

3. Verify all containers are running:
   ```powershell
   docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
   ```

4. Test connectivity to each service:
   ```powershell
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
   ```powershell
   docker network ls
   docker network inspect week14_backend_net
   docker network inspect week14_frontend_net
   ```

**Verification:**
```powershell
python tests/test_environment.py
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
   ```powershell
   for ($i=1; $i -le 10; $i++) {
       $response = Invoke-WebRequest -Uri "http://localhost:8080/" -UseBasicParsing
       Write-Host "Request $i : $($response.Headers['X-Backend'])"
   }
   ```

2. Alternatively, use curl to inspect headers:
   ```powershell
   for ($i=1; $i -le 10; $i++) {
       curl -s -D - http://localhost:8080/ -o $null 2>&1 | Select-String "X-Backend"
   }
   ```

3. Access the load balancer statistics endpoint:
   ```powershell
   curl http://localhost:8080/lb-status | python -m json.tool
   ```

4. Run the automated HTTP client from within a container:
   ```powershell
   docker compose -f docker/docker-compose.yml exec client python3 /app/src/apps/http_client.py --url http://lb:8080/ --count 20
   ```

**Verification:**
```powershell
python tests/test_exercises.py --exercise 2
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
   ```powershell
   # In PowerShell, use Test-NetConnection for basic check
   Test-NetConnection -ComputerName localhost -Port 9000
   
   # For interactive echo, use WSL
   wsl echo "Hello Week 14" | nc localhost 9000
   ```

2. Run the Python TCP echo client:
   ```powershell
   python src/apps/tcp_echo_client.py --host localhost --port 9000 --message "Testing echo" --repeat 5
   ```

3. Observe the echo server logs:
   ```powershell
   docker compose -f docker/docker-compose.yml logs echo
   ```

4. Test with varying message sizes:
   ```powershell
   python src/apps/tcp_echo_client.py --host localhost --port 9000 --message "A" --repeat 10
   python src/apps/tcp_echo_client.py --host localhost --port 9000 --message "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" --repeat 5
   ```

**Verification:**
```powershell
python tests/test_exercises.py --exercise 3
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
   ```powershell
   python scripts/capture_traffic.py --duration 60 --output pcap/week14_capture.pcap
   ```

2. While capture is running, generate traffic:
   ```powershell
   # In a new PowerShell window
   for ($i=1; $i -le 20; $i++) {
       curl -s http://localhost:8080/ | Out-Null
       Start-Sleep -Milliseconds 200
   }
   ```

3. Open the capture in Wireshark:
   ```powershell
   & "C:\Program Files\Wireshark\Wireshark.exe" pcap/week14_capture.pcap
   ```

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
   ```powershell
   # Conversation statistics
   tshark -r pcap/week14_capture.pcap -q -z conv,tcp
   
   # HTTP request summary
   tshark -r pcap/week14_capture.pcap -Y http.request -T fields -e frame.number -e ip.src -e ip.dst -e http.host
   ```

**Verification:**
```powershell
python tests/test_exercises.py --exercise 4
```

**Expected Outcome:**
- PCAP file contains captured packets
- HTTP conversations visible between client, load balancer and backends
- TCP three-way handshakes identifiable for each connection

## Demonstrations

### Demo 1: Complete System Walkthrough

This automated demonstration exercises all system components and generates a comprehensive report.

```powershell
python scripts/run_demo.py --demo full
```

**What to observe:**
- Container startup sequence and health checks
- HTTP request distribution across backends
- TCP echo validation
- Traffic capture and summary generation
- Artefact generation in the `artifacts/` directory

### Demo 2: Failover Behaviour

This demonstration shows how the load balancer handles backend failures.

```powershell
python scripts/run_demo.py --demo failover
```

**What to observe:**
- Initial requests distributed across both backends
- One backend is stopped mid-test
- Load balancer marks the backend as unhealthy
- All subsequent requests route to the remaining backend
- Backend restart and recovery to healthy state

## Packet Capture and Analysis

### Capturing Traffic

```powershell
# Basic capture (30 seconds)
python scripts/capture_traffic.py --duration 30 --output pcap/demo.pcap

# Extended capture with filter
python scripts/capture_traffic.py --duration 120 --filter "port 8080" --output pcap/http_only.pcap

# Capture from specific interface
python scripts/capture_traffic.py --interface "Ethernet" --duration 60 --output pcap/eth_capture.pcap
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
tcp.port == 9000

# IP-based filtering
ip.src == 172.20.0.2
ip.dst == 172.21.0.10
```

### Command-Line Analysis with tshark

```powershell
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

```powershell
# Stop all containers (preserves data)
python scripts/stop_lab.py

# Verify shutdown
docker ps

# View stopped containers
docker ps -a --filter "name=week14"
```

### Full Cleanup (Before Next Week)

```powershell
# Remove all containers, networks and volumes for this week
python scripts/cleanup.py --full

# Verify cleanup
docker system df

# Optional: remove unused Docker resources system-wide
python scripts/cleanup.py --full --prune
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
```powershell
netstat -ano | findstr "8080"
taskkill /PID <process_id> /F
```

#### Issue: WSL2 not running or Docker fails to connect

**Solution:** Restart WSL and Docker Desktop:
```powershell
wsl --shutdown
# Wait 5 seconds, then start Docker Desktop
```

#### Issue: Python packages not found

**Solution:** Install required packages:
```powershell
pip install -r setup/requirements.txt
```

#### Issue: Wireshark cannot capture Docker traffic

**Solution:** Use the npf driver capture or capture from within containers:
```powershell
docker compose -f docker/docker-compose.yml exec client tcpdump -i eth0 -w /app/artifacts/capture.pcap
```

See `docs/troubleshooting.md` for additional solutions.

## Theoretical Background

This laboratory integrates concepts from multiple layers of the network stack:

**Transport Layer (Layer 4):** TCP segments carry HTTP application data and echo protocol messages. The three-way handshake (SYN, SYN-ACK, ACK) establishes connections, while FIN packets terminate them gracefully. Port numbers (8080, 9000) multiplex multiple services on single hosts.

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
    │   │   :9000      │                                                   │
    │   └──────────────┘                                                   │
    │                                                                      │
    └──────────────────────────────────────────────────────────────────────┘

    HOST PORT MAPPINGS:
    ├── localhost:8080  →  lb:8080      (Load Balancer)
    ├── localhost:8001  →  app1:8001    (Backend 1 direct)
    ├── localhost:8002  →  app2:8001    (Backend 2 direct)
    └── localhost:9000  →  echo:9000    (TCP Echo Server)
```

---

*NETWORKING class - ASE, Informatics | by Revolvix*
