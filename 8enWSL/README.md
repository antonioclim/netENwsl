# Week 8: Transport Layer — HTTP Server Implementation and Reverse Proxies

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
> 
> by Revolvix

## Overview

The transport layer constitutes the pivotal architectural stratum bridging application-level semantics with network-level packet delivery, providing the fundamental abstractions of process-to-process communication through the port mechanism and enabling multiplexed, reliable data transfer. This laboratory session synthesises theoretical understanding of TCP, UDP, and TLS protocols with practical implementation of HTTP servers and reverse proxy architectures.

Through hands-on construction of HTTP request parsers, static file servers, and round-robin load balancers, students will internalise the intricate relationship between transport-layer reliability guarantees and application-layer protocol design. The exercises progressively advance from elementary socket operations to sophisticated proxy implementations incorporating security considerations such as directory traversal prevention and rate limiting.

The Docker-based infrastructure mirrors production deployment patterns, with nginx serving as the reference reverse proxy while student-implemented Python servers demonstrate the underlying mechanics. Wireshark captures throughout the session illuminate the three-way handshake, connection teardown, and the header-body structure of HTTP over TCP.

## Learning Objectives

By the end of this laboratory session, you will be able to:

1. **Identify** the components of TCP and UDP headers and explain the significance of port numbers in process demultiplexing
2. **Describe** the three-way handshake mechanism and articulate why connection establishment requires precisely three message exchanges
3. **Implement** a functional HTTP/1.1 server capable of parsing requests, serving static files, and generating properly formatted responses
4. **Construct** a reverse proxy with round-robin load balancing that distributes requests across multiple backend servers
5. **Analyse** packet captures to distinguish TCP flags, correlate request-response pairs, and identify connection state transitions
6. **Evaluate** security vulnerabilities in HTTP servers (directory traversal, resource exhaustion) and implement appropriate mitigations

## Prerequisites

### Knowledge Requirements
- Socket programming fundamentals from Week 3 (TCP client-server model)
- HTTP message format and status codes (application layer concepts)
- Basic understanding of process multiplexing and port allocation
- Familiarity with Docker container orchestration

### Software Requirements
- Windows 10/11 with WSL2 enabled
- Docker Desktop (WSL2 backend) version 4.0+
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

```powershell
# Open PowerShell as Administrator
cd WEEK8_WSLkit

# Verify prerequisites
python setup/verify_environment.py

# If any issues, run the installer helper
python setup/install_prerequisites.py

# Configure Docker for optimal performance
python setup/configure_docker.py
```

### Starting the Laboratory

```powershell
# Start all services (nginx + 3 backend servers)
python scripts/start_lab.py

# Verify everything is running
python scripts/start_lab.py --status

# View real-time logs
docker compose -f docker/docker-compose.yml logs -f
```

### Accessing Services

| Service | URL/Port | Description |
|---------|----------|-------------|
| Portainer | https://localhost:9443 | Container management (set credentials on first access) |
| nginx Proxy | http://localhost:8080 | Load-balanced entry point |
| nginx HTTPS | https://localhost:8443 | TLS-enabled proxy (self-signed) |
| Backend 1 | Internal only (8080) | Python HTTP server (BACKEND_ID=1) |
| Backend 2 | Internal only (8080) | Python HTTP server (BACKEND_ID=2) |
| Backend 3 | Internal only (8080) | Python HTTP server (BACKEND_ID=3) |

## Laboratory Exercises

### Exercise 1: Minimal HTTP Server Implementation

**Objective:** Implement core HTTP request parsing and static file serving with security considerations

**Duration:** 45–60 minutes

**Conceptual Foundation:**

The HTTP/1.1 protocol transmits requests as plaintext over TCP, with a rigidly defined structure: a request line (`METHOD SP REQUEST-TARGET SP HTTP-VERSION CRLF`), followed by header fields (`field-name ":" OWS field-value CRLF`), an empty line demarcating header termination, and an optional message body. Your implementation must correctly parse this format, map request targets to filesystem paths, and construct conformant responses.

**Steps:**

1. Navigate to the exercise file and examine the provided skeleton:
   ```powershell
   cd WEEK8_WSLkit
   # View the exercise template
   python -c "print(open('src/exercises/ex_8_01_http_server.py').read())"
   ```

2. Implement the `parse_request()` function:
   - Decode raw bytes using ISO-8859-1 (the canonical HTTP header encoding)
   - Split on CRLF to separate request line from headers
   - Extract method, target, and HTTP version from the request line
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
   ```powershell
   # Start your server
   python src/exercises/ex_8_01_http_server.py --port 8081 --docroot www
   
   # In another terminal, test with curl
   curl -v http://localhost:8081/
   curl -v http://localhost:8081/hello.txt
   curl -v http://localhost:8081/../../etc/passwd
   curl -I http://localhost:8081/  # HEAD request
   ```

**Verification:**
```powershell
python tests/test_exercises.py --exercise 1
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

A reverse proxy operates as an intermediary, accepting client connections and forwarding requests to backend servers. Round-robin load balancing cycles through available backends sequentially, distributing load evenly (assuming homogeneous request costs). The proxy must preserve HTTP semantics, inject appropriate headers (e.g., `X-Forwarded-For`), and maintain connection management across both client-proxy and proxy-backend segments.

**Steps:**

1. Examine the exercise template:
   ```powershell
   python -c "print(open('src/exercises/ex_8_02_reverse_proxy.py').read())"
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
   ```powershell
   # Terminal 1
   python src/apps/backend_server.py --port 9001 --id A
   
   # Terminal 2
   python src/apps/backend_server.py --port 9002 --id B
   
   # Terminal 3
   python src/apps/backend_server.py --port 9003 --id C
   ```

5. Start your proxy:
   ```powershell
   # Terminal 4
   python src/exercises/ex_8_02_reverse_proxy.py --port 8888 --backends 127.0.0.1:9001,127.0.0.1:9002,127.0.0.1:9003
   ```

6. Generate traffic and observe distribution:
   ```powershell
   for i in {1..9}; do curl -sS http://localhost:8888/ 2>/dev/null | grep -o 'Backend [A-C]'; done
   ```

**Verification:**
```powershell
python tests/test_exercises.py --exercise 2
```

**Expected Observations:**
- Requests cycle through backends: A → B → C → A → B → C...
- Response headers include `X-Served-By` indicating the backend
- Proxy adds `X-Forwarded-For` with client address

---

### Exercise 3: POST Request Handling

**Objective:** Extend the HTTP server to process POST requests with body content

**Duration:** 30–40 minutes

**Steps:**

1. Implement Content-Length parsing in request headers
2. Read exactly Content-Length bytes for the request body
3. Parse form data (application/x-www-form-urlencoded)
4. Implement a simple endpoint that echoes received data

**Verification:**
```powershell
python tests/test_exercises.py --exercise 3

# Manual test
curl -X POST -d "name=Student&course=Networks" http://localhost:8081/api/echo
```

---

### Exercise 4: Rate Limiting

**Objective:** Implement token bucket rate limiting to prevent resource exhaustion

**Duration:** 35–45 minutes

**Conceptual Foundation:**

The token bucket algorithm maintains a reservoir of tokens that replenish at a fixed rate. Each request consumes one token; if the bucket is empty, the request is rejected (429 Too Many Requests). This provides burst tolerance while enforcing sustained rate limits.

**Verification:**
```powershell
python tests/test_exercises.py --exercise 4

# Flood test
for i in {1..100}; do curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8081/; done | sort | uniq -c
```

---

### Exercise 5: Caching Proxy

**Objective:** Implement response caching with Cache-Control header interpretation

**Duration:** 45–55 minutes

**Verification:**
```powershell
python tests/test_exercises.py --exercise 5
```

---

## Demonstrations

### Demo 1: Docker Infrastructure with nginx Load Balancer

This demonstration showcases the production-grade nginx reverse proxy configuration with three Python backend servers.

```powershell
python scripts/run_demo.py --demo docker-nginx
```

**What to observe:**
- nginx distributes requests using round-robin by default
- Backend identification via X-Backend-ID header
- Graceful handling of backend failures
- Access logs showing request routing

### Demo 2: HTTP Server Internals

Visualises the request-response cycle with detailed logging.

```powershell
python scripts/run_demo.py --demo http-server
```

**What to observe:**
- Request parsing breakdown (method, path, headers)
- File resolution and MIME type detection
- Response construction with proper headers

### Demo 3: Three-Way Handshake Capture

Captures and analyses TCP connection establishment.

```powershell
python scripts/run_demo.py --demo handshake
```

**What to observe:**
- SYN packet from client
- SYN-ACK response from server
- ACK completing the handshake
- Sequence number initialisation

## Packet Capture and Analysis

### Capturing Traffic

```powershell
# Start capture for HTTP traffic
python scripts/capture_traffic.py --interface lo --filter "tcp port 8080" --output pcap/week8_http.pcap

# Capture proxy-to-backend traffic
python scripts/capture_traffic.py --interface docker0 --filter "tcp port 8080" --output pcap/week8_proxy.pcap
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

```powershell
# Stop all containers (preserves data and images)
python scripts/stop_lab.py

# Verify shutdown
docker ps
```

### Full Cleanup (Before Next Week)

```powershell
# Remove all containers, networks, and volumes for this week
python scripts/cleanup.py --full

# Also prune unused Docker resources
python scripts/cleanup.py --full --prune

# Verify cleanup
docker system df
```

## Homework Assignments

See the `homework/` directory for take-home exercises.

### Assignment 1: HTTPS Server with Self-Signed Certificate
Extend the HTTP server to support TLS using Python's `ssl` module. Generate a self-signed certificate and configure the server to accept HTTPS connections. Document the TLS handshake observed in Wireshark.

**Deliverables:** Python implementation + Wireshark capture + analysis report

### Assignment 2: Weighted Load Balancer
Modify the round-robin proxy to support weighted distribution. Backend servers should be configurable with weights (e.g., 5:3:1), and requests should be distributed proportionally.

**Deliverables:** Python implementation + test demonstrating distribution

## Troubleshooting

### Common Issues

#### Issue: "Address already in use" when starting server
**Solution:** Another process is using the port. Find and terminate it:
```powershell
# On WSL/Linux
lsof -i :8080
kill -9 <PID>

# Or use a different port
python src/exercises/ex_8_01_http_server.py --port 8082
```

#### Issue: Docker containers fail to start
**Solution:** Ensure Docker Desktop is running and WSL2 integration is enabled:
```powershell
docker info
# Should show "Operating System: ..." without errors
```

#### Issue: curl returns "Connection refused"
**Solution:** Verify the server is running and listening:
```powershell
netstat -tlnp | grep 8080
python scripts/start_lab.py --status
```

#### Issue: Wireshark doesn't show HTTP traffic
**Solution:** Ensure you're capturing on the correct interface. For Docker traffic, use `docker0` or the bridge network interface. For localhost, use the loopback interface.

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
│   WSL2 / Docker Desktop                                             │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │                    docker-compose                            │  │
│   │  ┌────────────────────────────────────────────────────────┐ │  │
│   │  │               seminar8-network (172.28.0.0/16)         │ │  │
│   │  │  ┌─────────────┐                                       │ │  │
│   │  │  │   nginx     │◀─── Port 8080 (HTTP)                  │ │  │
│   │  │  │  (s8-nginx) │◀─── Port 8443 (HTTPS)                 │ │  │
│   │  │  └──────┬──────┘                                       │ │  │
│   │  │         │ Round-Robin                                  │ │  │
│   │  │    ┌────┼────┬────────────┐                           │ │  │
│   │  │    ▼    ▼    ▼            │                           │ │  │
│   │  │  ┌────┐┌────┐┌────┐       │                           │ │  │
│   │  │  │ B1 ││ B2 ││ B3 │ Python HTTP Servers              │ │  │
│   │  │  │8080││8080││8080│ (demo_http_server.py)            │ │  │
│   │  │  └────┘└────┘└────┘                                   │ │  │
│   │  └────────────────────────────────────────────────────────┘ │  │
│   │                                                              │  │
│   │  Volumes:                                                    │  │
│   │  - ./www → /var/www (static content)                        │  │
│   │  - ./nginx → /etc/nginx (configuration)                     │  │
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

*NETWORKING class - ASE, Informatics | by Revolvix*
