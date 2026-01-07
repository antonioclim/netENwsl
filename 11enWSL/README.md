# Week 11: Application Protocols – FTP, DNS, SSH & Load Balancing

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
> 
> by Revolvix

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
- Docker Desktop (WSL2 backend)
- Wireshark (native Windows application)
- Python 3.11 or later
- Git (recommended)

### Hardware Requirements
- Minimum 8GB RAM (16GB recommended)
- 10GB free disk space
- Network connectivity

## Quick Start

### First-Time Setup (Run Once)

```powershell
# Open PowerShell as Administrator
cd WEEK11_WSLkit

# Verify prerequisites
python setup/verify_environment.py

# If any issues, run the installer helper
python setup/install_prerequisites.py

# Install Python dependencies
pip install -r setup/requirements.txt --break-system-packages
```

### Starting the Laboratory

```powershell
# Start all services
python scripts/start_lab.py

# Verify everything is running
python scripts/start_lab.py --status
```

### Accessing Services

| Service | URL/Port | Credentials |
|---------|----------|-------------|
| Portainer | https://localhost:9443 | Set on first access |
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
   ```powershell
   python src/exercises/ex_11_01_backend.py --id 1 --port 8081 -v
   ```

3. Start Backend 2 with artificial delay:
   ```powershell
   python src/exercises/ex_11_01_backend.py --id 2 --port 8082 --delay 0.1 -v
   ```

4. Start Backend 3 with longer delay:
   ```powershell
   python src/exercises/ex_11_03_backend.py --id 3 --port 8083 --delay 0.2 -v
   ```

5. Verify each backend responds:
   ```powershell
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
```powershell
python tests/test_exercises.py --exercise 1
```

---

### Exercise 2: Python Load Balancer with Round-Robin

**Objective:** Implement and test a Python-based load balancer using round-robin distribution

**Duration:** 20 minutes

**Steps:**

1. Ensure all three backends are running (from Exercise 1)

2. Start the load balancer with round-robin algorithm:
   ```powershell
   python src/exercises/ex_11_02_loadbalancer.py ^
       --backends localhost:8081,localhost:8082,localhost:8083 ^
       --listen 0.0.0.0:8080 ^
       --algo rr
   ```

3. Test round-robin distribution:
   ```powershell
   for /L %i in (1,1,6) do @curl -s http://localhost:8080/
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
```powershell
python tests/test_exercises.py --exercise 2
```

---

### Exercise 3: Sticky Sessions with IP Hash

**Objective:** Configure session affinity using IP-based hashing

**Duration:** 15 minutes

**Steps:**

1. Stop the current load balancer (Ctrl+C)

2. Restart with IP hash algorithm:
   ```powershell
   python src/exercises/ex_11_02_loadbalancer.py ^
       --backends localhost:8081,localhost:8082,localhost:8083 ^
       --listen 0.0.0.0:8080 ^
       --algo ip_hash
   ```

3. Send multiple requests:
   ```powershell
   for /L %i in (1,1,5) do @curl -s http://localhost:8080/
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
```powershell
python tests/test_exercises.py --exercise 3
```

---

### Exercise 4: Failover Simulation

**Objective:** Observe automatic failover when a backend becomes unavailable

**Duration:** 15 minutes

**Steps:**

1. With load balancer running in round-robin mode, stop Backend 2 (Ctrl+C in its terminal)

2. Send requests and observe redistribution:
   ```powershell
   for /L %i in (1,1,6) do @curl -s http://localhost:8080/ 2>nul || echo ERROR
   ```

3. The first request to Backend 2 will fail; subsequent requests go to 1 and 3

4. Restart Backend 2 and observe recovery:
   ```powershell
   python src/exercises/ex_11_01_backend.py --id 2 --port 8082 -v
   ```

**What to Observe:**
- Initial failure triggers passive health marking
- Traffic redistributes to healthy backends
- Recovery occurs after fail_timeout expires

**Verification:**
```powershell
python tests/test_exercises.py --exercise 4
```

---

### Exercise 5: Nginx Docker Load Balancer

**Objective:** Deploy an industrial-strength Nginx load balancer using Docker Compose

**Duration:** 20 minutes

**Steps:**

1. Stop any Python backends and load balancer

2. Start the Nginx stack:
   ```powershell
   python scripts/start_lab.py --nginx-only
   ```
   Or manually:
   ```powershell
   cd docker
   docker compose up -d
   ```

3. Test round-robin distribution:
   ```powershell
   for /L %i in (1,1,6) do @curl -s http://localhost:8080/
   ```

4. Observe the X-Served-By header:
   ```powershell
   curl -v http://localhost:8080/ 2>&1 | findstr "X-Served-By"
   ```

5. Check Nginx status:
   ```powershell
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
```powershell
python tests/test_exercises.py --exercise 5
```

---

### Exercise 6: DNS Protocol Analysis

**Objective:** Construct and analyse DNS queries using a manual client implementation

**Duration:** 20 minutes

**Steps:**

1. Query an A record:
   ```powershell
   python src/exercises/ex_11_03_dns_client.py google.com A --verbose
   ```

2. Query MX records for mail servers:
   ```powershell
   python src/exercises/ex_11_03_dns_client.py google.com MX
   ```

3. Query NS records:
   ```powershell
   python src/exercises/ex_11_03_dns_client.py ase.ro NS
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
```powershell
python tests/test_exercises.py --exercise 6
```

---

### Exercise 7: Performance Benchmarking

**Objective:** Compare performance characteristics of Python vs Nginx load balancers

**Duration:** 15 minutes

**Steps:**

1. Benchmark Python load balancer:
   ```powershell
   python src/exercises/ex_11_02_loadbalancer.py loadgen ^
       --url http://localhost:8080/ ^
       --n 500 --c 20
   ```

2. Start Nginx stack and benchmark:
   ```powershell
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
```powershell
python tests/test_exercises.py --exercise 7
```

## Demonstrations

### Demo 1: Complete Load Balancing Workflow

Automated demonstration showcasing the full laboratory environment:

```powershell
python scripts/run_demo.py --demo 1
```

**What to observe:**
- Docker stack initialisation
- Round-robin distribution across backends
- Traffic capture in Wireshark-compatible format
- Validation report generation

### Demo 2: Failover and Recovery

Demonstrates automatic failover behaviour:

```powershell
python scripts/run_demo.py --demo 2
```

**What to observe:**
- Backend failure detection
- Traffic redistribution
- Health check recovery

## Packet Capture and Analysis

### Capturing Traffic

```powershell
# Start capture
python scripts/capture_traffic.py --interface eth0 --output pcap/week11_capture.pcap

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

```powershell
# Stop all containers (preserves data)
python scripts/stop_lab.py

# Verify shutdown
docker ps
```

### Full Cleanup (Before Next Week)

```powershell
# Remove all containers, networks, and volumes for this week
python scripts/cleanup.py --full

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
```powershell
netstat -ano | findstr :8080
taskkill /PID <pid> /F
```

#### Issue: Docker containers won't start
**Solution:**
```powershell
docker compose down -v
docker system prune -f
docker compose up -d
```

#### Issue: Permission denied for packet capture
**Solution:** Run PowerShell as Administrator or use elevated WSL terminal.

#### Issue: Python module not found
**Solution:**
```powershell
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
│ │Backend│   │Backend│   │Backend│    Docker Network: s11_net                │
│ │   1   │   │   2   │   │   3   │                                           │
│ │ :8081 │   │ :8082 │   │ :8083 │                                           │
│ └───────┘   └───────┘   └───────┘                                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

*NETWORKING class - ASE, Informatics | by Revolvix*
