# Week 10: Application Layer Protocols — HTTP/HTTPS, REST and Network Services

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
>
> by Revolvix

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
- Docker Desktop (WSL2 backend)
- Wireshark (native Windows installation)
- Python 3.11 or later
- Git (recommended)

### Hardware Requirements
- Minimum 8GB RAM (16GB recommended)
- 10GB free disk space
- Network connectivity for initial setup

## Quick Start

### First-Time Setup (Run Once)

```powershell
# Open PowerShell as Administrator
cd WEEK10_WSLkit

# Verify prerequisites are installed
python setup/verify_environment.py

# If any issues arise, run the installer helper
python setup/install_prerequisites.py
```

### Starting the Laboratory

```powershell
# Start all Docker services
python scripts/start_lab.py

# Verify services are healthy
python scripts/start_lab.py --status
```

### Accessing Services

| Service | URL/Port | Credentials |
|---------|----------|-------------|
| Portainer | https://localhost:9443 | Set on first access |
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
   ```powershell
   python scripts/start_lab.py --status
   ```

2. Query the HTTP service from PowerShell:
   ```powershell
   curl.exe -v http://localhost:8000/
   curl.exe -v http://localhost:8000/hello.txt
   ```

3. Observe the following in the verbose output:
   - HTTP version in the response line (HTTP/1.0 or HTTP/1.1)
   - Response headers: Content-Type, Content-Length, Server
   - Connection behaviour (Keep-Alive vs close)

4. Open Wireshark and capture on the Docker network interface.

5. Re-run the curl commands and correlate HTTP requests with TCP segments.

**Verification:**
```powershell
python tests/test_exercises.py --exercise 1
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
   ```powershell
   docker exec -it week10_debug bash
   dig @dns-server -p 5353 web.lab.local +short
   ```

3. Observe the difference between successful resolution and NXDOMAIN responses.

**Verification:**
```powershell
python tests/test_exercises.py --exercise 2
```

**Expected Observations:**
- DNS typically uses UDP (connectionless)
- Single request yields single response
- NXDOMAIN (RCODE 3) indicates non-existent domain

### Exercise 3: SSH Encrypted Communication

**Objective:** Observe SSH handshake and understand why payload is not visible in captures.

**Duration:** 15 minutes

**Steps:**

1. Connect to the SSH server from PowerShell:
   ```powershell
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
   ```powershell
   python src/apps/ssh_demo.py
   ```

4. Capture the SSH traffic in Wireshark and examine the handshake packets.

**Verification:**
```powershell
python tests/test_exercises.py --exercise 3
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
   ```powershell
   python src/apps/ftp_demo.py
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
```powershell
python tests/test_exercises.py --exercise 4
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
   ```powershell
   python src/exercises/ex_10_01_https.py generate-cert
   ```

2. Start the HTTPS server:
   ```powershell
   python src/exercises/ex_10_01_https.py serve --host 0.0.0.0 --port 8443
   ```

3. In another terminal, interact with the API:
   ```powershell
   # List resources (initially empty)
   curl.exe -k https://localhost:8443/api/resources

   # Create a resource
   curl.exe -k -X POST https://localhost:8443/api/resources -H "Content-Type: application/json" -d "{\"name\":\"sensor1\",\"value\":42}"

   # Get the created resource
   curl.exe -k https://localhost:8443/api/resources/1

   # Update the resource
   curl.exe -k -X PUT https://localhost:8443/api/resources/1 -H "Content-Type: application/json" -d "{\"name\":\"sensor1-updated\",\"value\":100}"

   # Delete the resource
   curl.exe -k -X DELETE https://localhost:8443/api/resources/1
   ```

4. Run the automated selftest:
   ```powershell
   python src/exercises/ex_10_01_https.py selftest
   ```

**Verification:**
```powershell
python tests/test_exercises.py --exercise 5
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
   ```powershell
   python src/exercises/ex_10_02_rest_levels.py serve --host 127.0.0.1 --port 5000
   ```

2. Test Level 0 (RPC style):
   ```powershell
   curl.exe -X POST http://localhost:5000/level0/service -H "Content-Type: application/json" -d "{\"action\":\"list_users\"}"
   curl.exe -X POST http://localhost:5000/level0/service -H "Content-Type: application/json" -d "{\"action\":\"get_user\",\"id\":1}"
   ```

3. Test Level 1 (Resource URIs with action endpoints):
   ```powershell
   curl.exe http://localhost:5000/level1/users
   curl.exe http://localhost:5000/level1/users/1
   curl.exe -X POST http://localhost:5000/level1/users/1/update -H "Content-Type: application/json" -d "{\"name\":\"Updated\"}"
   ```

4. Test Level 2 (Proper HTTP verbs):
   ```powershell
   curl.exe http://localhost:5000/level2/users
   curl.exe -X POST http://localhost:5000/level2/users -H "Content-Type: application/json" -d "{\"name\":\"New User\",\"email\":\"new@example.test\"}"
   curl.exe -X PUT http://localhost:5000/level2/users/3 -H "Content-Type: application/json" -d "{\"name\":\"Modified\"}"
   curl.exe -X DELETE http://localhost:5000/level2/users/3
   ```

5. Test Level 3 (HATEOAS):
   ```powershell
   curl.exe http://localhost:5000/level3/users
   ```
   Note the `_links` section in responses.

6. Run the selftest:
   ```powershell
   python src/exercises/ex_10_02_rest_levels.py selftest
   ```

**Verification:**
```powershell
python tests/test_exercises.py --exercise 6
```

**Expected Observations:**
- Level 0: Single endpoint, action parameter distinguishes operations
- Level 1: Resources have distinct URIs, but verbs are inconsistent
- Level 2: GET, POST, PUT, DELETE semantics respected
- Level 3: Hypermedia links enable client navigation

## Demonstrations

### Demo 1: Complete Service Stack

Automated demonstration of all Docker services.

```powershell
python scripts/run_demo.py --demo 1
```

**What to observe:**
- HTTP fetch returns HTML content
- DNS queries resolve to configured IP addresses
- SSH connection executes remote command
- FTP lists directory contents

### Demo 2: Protocol Comparison

Side-by-side comparison of HTTP vs HTTPS traffic visibility.

```powershell
python scripts/run_demo.py --demo 2
```

**What to observe:**
- HTTP request/response visible in plaintext
- HTTPS shows TLS handshake, encrypted application data
- Certificate information extractable from handshake

## Packet Capture and Analysis

### Capturing Traffic

```powershell
# Start capture (requires elevated privileges)
python scripts/capture_traffic.py --interface eth0 --output pcap/week10_capture.pcap

# Or use Wireshark directly on the Docker network
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

```powershell
# DNS queries and responses
tshark -r pcap/week10_capture.pcap -Y "udp.port==5353" -T fields -e dns.qry.name -e dns.flags.rcode

# HTTP requests
tshark -r pcap/week10_capture.pcap -Y "http.request" -T fields -e http.request.method -e http.host -e http.request.uri

# TCP connection initiators
tshark -r pcap/week10_capture.pcap -Y "tcp.flags.syn==1 && tcp.flags.ack==0" -T fields -e ip.dst -e tcp.dstport
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

### Assignment 1: SOAP Endpoint Implementation

Implement a minimal SOAP service and compare its message structure with the REST exercises. Document the XML envelope format and error handling patterns.

### Assignment 2: HTTPS Certificate Chain Analysis

Using OpenSSL and Wireshark, analyse the certificate chain of a public HTTPS website. Document the root CA, intermediate certificates and end-entity certificate. Explain the role of each.

### Assignment 3: Multi-Service Docker Composition

Extend the provided Docker Compose configuration to include an additional service (e.g., a reverse proxy with nginx). Document the network topology changes and demonstrate traffic flow.

## Troubleshooting

### Common Issues

#### Issue: Docker permission denied
**Solution:** Ensure Docker Desktop is running and WSL2 integration is enabled. In Docker Desktop settings, verify your WSL distro is enabled under Resources > WSL Integration.

#### Issue: Port already in use
**Solution:** Check with `netstat -ano | findstr :<PORT>` and terminate the conflicting process, or modify the port mapping in docker-compose.yml.

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
└─────────────────────────────────────────────────────────────────────┘

Host Port Mappings:
  • 8000  → web:8000        (HTTP)
  • 5353  → dns-server:5353 (DNS/UDP)
  • 2222  → ssh-server:22   (SSH)
  • 2121  → ftp-server:2121 (FTP control)
  • 30000-30009 → ftp-server (FTP passive data)
```

---

*NETWORKING class - ASE, Informatics | by Revolvix*
