# Week 12: Email Protocols and Remote Procedure Call

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
> 
> by ing. dr. Antonio Clim

---

## ⚠️ Environment Notice

This laboratory kit is designed for the **WSL2 + Ubuntu 22.04 + Docker + Portainer** environment.

**Repository:** https://github.com/antonioclim/netENwsl
**This Week's Folder:** `12enWSL`

| Component | Details |
|-----------|---------|
| Windows | Windows 10/11 with WSL2 enabled |
| Linux Distribution | Ubuntu 22.04 LTS (default WSL distro) |
| Container Runtime | Docker Engine (in WSL) |
| Management Interface | Portainer CE on port 9000 (global) |
| Packet Analysis | Wireshark (native Windows application) |

---

## 📚 Pedagogical Resources

This week includes structured learning materials:

| Resource | Purpose | Location |
|----------|---------|----------|
| Peer Instruction | MCQ questions with misconception analysis | `docs/peer_instruction.md` |
| Pair Programming | Collaborative exercise guide | `docs/pair_programming_guide.md` |
| Misconceptions | Common errors and corrections | `docs/misconceptions.md` |
| Glossary | Technical terminology | `docs/glossary.md` |
| Code Tracing | Trace execution exercises | `docs/code_tracing.md` |
| Parsons Problems | Code reordering exercises | `docs/parsons_problems.md` |

---

## 📥 Cloning This Week's Laboratory

### Step 1: Open PowerShell (Windows)

Press `Win + X` → Select "Windows Terminal" or "PowerShell"

### Step 2: Open Directory and Clone

```powershell
# Create networking folder if it doesn't exist
mkdir D:\NETWORKING -ErrorAction SilentlyContinue
cd D:\NETWORKING

# Clone Week 12
git clone https://github.com/antonioclim/netENwsl.git WEEK12
cd WEEK12
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
git clone https://github.com/antonioclim/netENwsl.git WEEK12
cd WEEK12
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

💭 **PREDICTION:** What containers do you expect to see running?

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
cd /mnt/d/NETWORKING/WEEK12/12enWSL
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

### Week 12 Network Configuration

Go to: **Networks → week12_net**

Current configuration:
- Subnet: 172.28.12.0/24
- Lab container: week12_lab
- Services: SMTP (1025), JSON-RPC (6200), XML-RPC (6201), gRPC (6251)

**⚠️ NEVER use port 9000** - reserved for Portainer!

---

## 🦈 Wireshark Setup and Usage

### When to Open Wireshark

Open Wireshark:
- **BEFORE** generating network traffic you want to capture
- When exercises mention "capture", "analyse packets" or "observe traffic"

### Step 1: Launch Wireshark

From Windows Start Menu: Search "Wireshark" → Click to open

### Step 2: Select Capture Interface

**CRITICAL:** Select the correct interface for WSL traffic:

| Interface Name | When to Use |
|----------------|-------------|
| **vEthernet (WSL)** | ✅ Most common - captures WSL Docker traffic |
| **Loopback Adapter** | Only for localhost traffic (127.0.0.1) |
| **Ethernet/Wi-Fi** | Physical network traffic (not Docker) |

### Wireshark Filters for Week 12

| Filter | Purpose |
|--------|---------|
| `tcp.port == 1025` | SMTP traffic |
| `tcp.port == 6200 && http` | JSON-RPC traffic |
| `tcp.port == 6201 && http` | XML-RPC traffic |
| `tcp.port == 6251` | gRPC (HTTP/2) traffic |
| `tcp.port in {1025, 6200, 6201, 6251}` | All Week 12 traffic |
| `http.request.method == "POST"` | RPC calls only |
| `http contains "jsonrpc"` | JSON-RPC content |
| `http contains "methodCall"` | XML-RPC content |

### Analysing Protocol Traffic

1. **SMTP Analysis**: Filter `tcp.port == 1025`, follow TCP stream
2. **RPC Comparison**: Compare payload sizes between ports 6200 and 6201
3. **gRPC Analysis**: Filter `tcp.port == 6251`, observe HTTP/2 frames

### Saving Captures

1. **File → Save As**
2. Go to: `D:\NETWORKING\WEEK12\pcap\`
3. Filename: `capture_smtp.pcap` or `capture_rpc.pcap`

---

## Overview

Week 12 covers two key areas of application-layer networking: electronic mail protocols and remote procedure call patterns. The email component explores SMTP (Simple Mail Transfer Protocol) as a clear example of a text-based, stateful application protocol, demonstrating how commands, responses and multi-line data transfers operate at the TCP level. Students will observe the elegance of human-readable protocol dialogues whilst appreciating the precision required for reliable message delivery.

The RPC component shifts focus to distributed computing patterns, examining how modern systems enable function invocation across network boundaries as though calling local procedures. Through comparative analysis of JSON-RPC 2.0, XML-RPC and gRPC with Protocol Buffers, students will understand the trade-offs between simplicity, verbosity and performance that guide architectural decisions in microservices, APIs and enterprise systems.

This laboratory combines theoretical knowledge with hands-on implementation, packet capture analysis and performance benchmarking—providing a solid foundation for understanding how contemporary distributed applications communicate.

## Learning Objectives

By the end of this laboratory session, you will be able to:

1. **Recall** the structure of SMTP dialogues, including commands (HELO, MAIL FROM, RCPT TO, DATA) and response codes
2. **Explain** the RPC abstraction and articulate the roles of client stubs, server stubs and serialisation layers
3. **Implement** educational SMTP servers and RPC endpoints using Python's standard library and third-party frameworks
4. **Demonstrate** client-server communication using netcat, curl and programmatic clients
5. **Analyse** protocol differences between JSON-RPC, XML-RPC and gRPC by examining packet captures and payload structures
6. **Compare** serialisation overhead and latency characteristics through controlled benchmarks
7. **Design** appropriate protocol selections for given distributed system requirements
8. **Evaluate** the suitability of different RPC frameworks for microservices, public APIs and legacy integrations

## Prerequisites

### Knowledge Requirements
- OSI and TCP/IP models (Weeks 2-3)
- Socket programming fundamentals (Week 3)
- HTTP protocol basics (Week 8)
- TCP connection lifecycle and flow control
- Basic understanding of serialisation (JSON, XML)

### Software Requirements
- Windows 10/11 with WSL2 enabled
- Docker Engine (in WSL)
- Portainer CE (running globally on port 9000)
- Wireshark (native Windows)
- Python 3.11 or later
- Git
- Text editor or IDE (VS Code recommended)

### Hardware Requirements
- Minimum 8GB RAM (16GB recommended)
- 10GB free disk space
- Network connectivity

## Quick Start

### First-Time Setup (Run Once)

```bash
# Open Ubuntu terminal (WSL)
wsl

# Go to the kit directory
cd /mnt/d/NETWORKING/WEEK12/12enWSL

# Start Docker if not running
sudo service docker start

# Verify prerequisites
python3 setup/verify_environment.py

# If any issues, run the installer helper
python3 setup/install_prerequisites.py
```

### Starting the Laboratory

💭 **PREDICTION:** Before starting, predict how many containers will be created for Week 12.

```bash
# Start all services
python3 scripts/start_lab.py

# Verify everything is running
python3 scripts/start_lab.py --status
```

### Accessing Services

| Service | URL/Port | Description |
|---------|----------|-------------|
| Portainer | http://localhost:9000 | Docker management interface (stud/studstudstud) |
| SMTP Server | localhost:1025 | Educational SMTP server |
| JSON-RPC | http://localhost:6200 | JSON-RPC 2.0 calculator API |
| XML-RPC | http://localhost:6201 | XML-RPC calculator API |
| gRPC | localhost:6251 | gRPC calculator service |

## Laboratory Exercises

### Exercise 1: SMTP Protocol Exploration

**Objective:** Understand the structure and flow of SMTP dialogues through hands-on interaction

**Duration:** 45 minutes

**Background:**
SMTP is a text-based protocol operating over TCP port 25 (or 587 for submission, 1025 for testing). Each command from the client receives a numeric response code from the server, where 2xx indicates success, 3xx indicates intermediate status, 4xx indicates temporary failure and 5xx indicates permanent failure.

💭 **PREDICTION:** What response code will the server send after you type `DATA`? (Hint: it's not 250!)

**Steps:**

1. Start the SMTP server in one terminal:
   ```bash
   python3 scripts/start_lab.py --service smtp
   ```

2. Open a manual SMTP session using netcat:
   ```bash
   # In WSL terminal
   nc localhost 1025
   ```

3. Conduct a complete SMTP dialogue:
   ```
   EHLO client.example.test
   MAIL FROM:<alice@example.test>
   RCPT TO:<bob@example.test>
   DATA
   Subject: Week 12 Test Message
   From: alice@example.test
   To: bob@example.test

   This is the message body.
   Multiple lines are permitted.
   .
   QUIT
   ```

4. Observe the response codes at each stage:
   - 220: Service ready greeting
   - 250: Requested action completed
   - 354: Start mail input
   - 221: Service closing

5. Inspect the stored message:
   ```bash
   ls docker/volumes/spool/*.eml
   cat docker/volumes/spool/*.eml
   ```

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 1
```

**Expected Observations:**
- SMTP dialogue is human-readable plain text
- The DATA phase streams content until a lone period terminates
- Message headers and body are separated by a blank line
- Server stores complete RFC 5322 compliant messages

### Exercise 2: JSON-RPC Implementation

**Objective:** Implement and test JSON-RPC 2.0 requests including batch operations and error handling

**Duration:** 30 minutes

💭 **PREDICTION:** What HTTP status code will a method-not-found error return? (Hint: check `docs/misconceptions.md`)

**Steps:**

1. Start the JSON-RPC server:
   ```bash
   python3 scripts/start_lab.py --service jsonrpc
   ```

2. Test with curl (single request):
   ```bash
   curl -s -X POST "http://localhost:6200" \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc":"2.0","id":1,"method":"add","params":[10,32]}'
   ```

3. Test batch requests:
   ```bash
   curl -s -X POST "http://localhost:6200" \
     -H "Content-Type: application/json" \
     -d '[{"jsonrpc":"2.0","id":1,"method":"add","params":[1,2]},{"jsonrpc":"2.0","id":2,"method":"multiply","params":[3,4]}]'
   ```

4. Test error handling:
   ```bash
   curl -s -X POST "http://localhost:6200" \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc":"2.0","id":1,"method":"divide","params":[10,0]}'
   ```

5. Run the Python client demonstration:
   ```bash
   python3 src/apps/rpc/jsonrpc/jsonrpc_client.py --demo
   ```

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 2
```

### Exercise 3: XML-RPC Comparison

**Objective:** Compare XML-RPC with JSON-RPC to understand serialisation overhead

**Duration:** 25 minutes

💭 **PREDICTION:** Which protocol will have larger payloads — JSON-RPC or XML-RPC?

**Steps:**

1. Start the XML-RPC server:
   ```bash
   python3 scripts/start_lab.py --service xmlrpc
   ```

2. Use Python's built-in client:
   ```python
   import xmlrpc.client
   proxy = xmlrpc.client.ServerProxy("http://localhost:6201", allow_none=True)
   print(proxy.add(10, 32))
   print(proxy.system.listMethods())
   ```

3. Compare payload sizes by capturing both protocols:
   ```bash
   python3 scripts/capture_traffic.py --duration 30 --ports 6200,6201
   ```

4. In parallel, run equivalent operations on both servers

**Expected Observations:**
- XML-RPC requests are significantly larger due to XML verbosity
- Both protocols transport over HTTP POST
- XML-RPC provides introspection via system.* methods

### Exercise 4: gRPC and Protocol Buffers

**Objective:** Experience strongly-typed RPC with HTTP/2 and binary serialisation

**Duration:** 30 minutes

💭 **PREDICTION:** Can you read a gRPC payload in Wireshark like you can JSON-RPC?

**Steps:**

1. Examine the Protocol Buffer definition:
   ```bash
   cat src/apps/rpc/grpc/calculator.proto
   ```

2. Start the gRPC server:
   ```bash
   python3 scripts/start_lab.py --service grpc
   ```

3. Run the gRPC client:
   ```bash
   python3 src/apps/rpc/grpc/grpc_client.py --demo
   ```

4. Observe error handling with division by zero

**Expected Observations:**
- gRPC uses binary Protocol Buffers (not human-readable)
- Error responses use gRPC status codes rather than HTTP status
- Strong typing enforced at compile time via generated stubs

### Exercise 5: Performance Benchmarking

**Objective:** Quantify the performance characteristics of different RPC frameworks

**Duration:** 20 minutes

💭 **PREDICTION:** Which protocol will have the lowest latency — JSON-RPC, XML-RPC or gRPC?

**Steps:**

1. Run the automated benchmark:
   ```bash
   python3 scripts/run_demo.py --demo benchmark
   ```

2. Analyse the results for:
   - Requests per second
   - Mean latency
   - Payload overhead

3. Discuss factors affecting results:
   - Serialisation cost
   - HTTP connection reuse
   - Python GIL limitations

## Demonstrations

### Demo 1: Complete Email Flow

Demonstrates SMTP message submission with packet capture.

```bash
python3 scripts/run_demo.py --demo smtp
```

**What to observe:**
- TCP three-way handshake before SMTP dialogue
- Clear text command/response exchange
- DATA phase with dot-stuffing for termination

### Demo 2: RPC Protocol Comparison

Side-by-side demonstration of JSON-RPC, XML-RPC and gRPC.

```bash
python3 scripts/run_demo.py --demo rpc-compare
```

**What to observe:**
- Payload size differences
- Response time variations
- Error format differences

### Demo 3: Error Handling Scenarios

Demonstrates error handling across all protocols.

```bash
python3 scripts/run_demo.py --demo errors
```

**What to observe:**
- SMTP rejection codes (5xx)
- JSON-RPC error objects with codes
- gRPC status codes and details

## Project Structure

```
12enWSL/
├── artifacts/                    # Generated files (pcap, logs)
├── docker/
│   ├── configs/                  # Service configuration files
│   ├── volumes/
│   │   └── spool/               # SMTP message storage
│   ├── docker-compose.yml       # Container orchestration
│   └── Dockerfile               # Custom image definition
├── docs/
│   ├── commands_cheatsheet.md   # Quick reference
│   ├── further_reading.md       # Academic resources
│   ├── theory_summary.md        # Protocol theory
│   ├── troubleshooting.md       # Problem solving guide
│   ├── peer_instruction.md      # MCQ with misconceptions
│   ├── pair_programming_guide.md # Collaborative exercises
│   ├── misconceptions.md        # Common errors
│   ├── glossary.md              # Terminology
│   ├── code_tracing.md          # Trace exercises
│   └── parsons_problems.md      # Reorder exercises
├── homework/
│   ├── exercises/               # Homework problems
│   ├── solutions/               # Reference solutions
│   └── README.md
├── pcap/                        # Packet captures
├── scripts/
│   ├── utils/                   # Shared utilities
│   ├── start_lab.py            # Environment startup
│   ├── stop_lab.py             # Environment shutdown
│   ├── run_demo.py             # Demonstrations
│   ├── capture_traffic.py      # Packet capture helper
│   └── cleanup.py              # Resource cleanup
├── setup/
│   ├── install_prerequisites.py
│   ├── verify_environment.py
│   └── requirements.txt
├── src/
│   ├── apps/
│   │   ├── email/              # SMTP client/server
│   │   └── rpc/
│   │       ├── grpc/           # gRPC implementation
│   │       ├── jsonrpc/        # JSON-RPC implementation
│   │       └── xmlrpc/         # XML-RPC implementation
│   ├── exercises/
│   │   ├── ex_12_01_explore_smtp.py
│   │   └── ex_12_02_compare_rpc.py
│   └── utils/                  # Shared utilities
├── tests/
│   ├── test_environment.py
│   ├── test_exercises.py
│   └── expected_outputs.md
├── CHANGELOG.md
├── LICENSE
└── README.md
```

## Key Concepts

### SMTP Protocol

SMTP (Simple Mail Transfer Protocol) governs email transmission:

- **Commands:** EHLO, MAIL FROM, RCPT TO, DATA, QUIT
- **Response codes:** 2xx (success), 3xx (intermediate), 4xx (temporary error), 5xx (permanent error)
- **Envelope vs headers:** Routing (envelope) is separate from message display (headers)
- **Data termination:** A single dot on its own line ends the message body

### RPC Abstraction

Remote Procedure Call allows calling functions across networks:

- **Client stub:** Serialises parameters, sends request, deserialises response
- **Server stub:** Deserialises request, calls function, serialises response
- **Serialisation format:** JSON (human-readable), XML (verbose but self-describing), Protocol Buffers (compact binary)
- **Transport protocol:** HTTP/1.1 (JSON-RPC, XML-RPC), HTTP/2 (gRPC with multiplexing)
- **Type safety:** Loose (JSON-RPC), Schema-enforced (gRPC)
- **Error handling:** Structured error objects with codes and messages

### Protocol Selection Guidelines

| Use Case | Recommended Protocol | Rationale |
|----------|---------------------|-----------|
| Public API | JSON-RPC | Human-readable, easy debugging, wide tooling support |
| Browser clients | JSON-RPC | Native JSON support, no binary handling needed |
| Internal microservices | gRPC | Performance, strong contracts, streaming support |
| Legacy integration | XML-RPC | Compatibility with older systems |
| Mobile backends | gRPC | Bandwidth efficiency, built-in code generation |
| Blockchain APIs | JSON-RPC | Industry standard (Bitcoin, Ethereum) |

## References

- Kurose, J. & Ross, K. (2021). *Computer Networking: A Top-Down Approach* (8th ed.). Pearson.
- Rhodes, B. & Goerzen, J. (2014). *Foundations of Python Network Programming* (3rd ed.). Apress.
- Postel, J. (1982). RFC 821: Simple Mail Transfer Protocol. IETF.
- Klensin, J. (2008). RFC 5321: Simple Mail Transfer Protocol. IETF.
- JSON-RPC 2.0 Specification. https://www.jsonrpc.org/specification
- gRPC Documentation. https://grpc.io/docs/
- Protocol Buffers Language Guide. https://protobuf.dev/

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        WEEK 12 LABORATORY                           │
│              (WSL2 + Ubuntu 22.04 + Docker + Portainer)             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐          │
│   │   SMTP      │     │  JSON-RPC   │     │   XML-RPC   │          │
│   │   Server    │     │   Server    │     │   Server    │          │
│   │  :1025      │     │   :6200     │     │   :6201     │          │
│   │  (TCP)      │     │   (HTTP)    │     │   (HTTP)    │          │
│   └──────┬──────┘     └──────┬──────┘     └──────┬──────┘          │
│          │                   │                   │                  │
│   ┌──────┴───────────────────┴───────────────────┴──────┐          │
│   │                   Docker Network                     │          │
│   │                   (week12_net)                       │          │
│   │                   172.28.12.0/24                     │          │
│   └──────┬───────────────────┬───────────────────┬──────┘          │
│          │                   │                   │                  │
│   ┌──────┴──────┐     ┌──────┴──────┐     ┌──────┴──────┐          │
│   │   gRPC      │     │  Wireshark  │     │  Portainer  │          │
│   │   Server    │     │  Capture    │     │    CE       │          │
│   │   :6251     │     │  Interface  │     │   :9000     │          │
│   │  (HTTP/2)   │     │             │     │  (Global)   │          │
│   └─────────────┘     └─────────────┘     └─────────────┘          │
│                                                                     │
│   Data Flow:                                                        │
│   ─────────────────────────────────────────────────────────         │
│   Client ──▶ [Serialisation] ──▶ TCP/HTTP ──▶ Server                │
│          ◀── [Deserialisation] ◀── TCP/HTTP ◀──                     │
│                                                                     │
│   Portainer: http://localhost:9000 (global service)                 │
│   Credentials: stud / studstudstud                                  │
└─────────────────────────────────────────────────────────────────────┘
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
- ✅ Check that traffic is being generated DURING capture
- ✅ Check display filter isn't hiding packets (clear filter)
- ✅ Try "Capture → Options" and enable promiscuous mode

**Problem:** "No interfaces found" or permission error
- Run Wireshark as Administrator (right-click → Run as administrator)
- Reinstall Npcap with "WinPcap API-compatible Mode" option checked

**Problem:** Can't see Docker container traffic
- Select `vEthernet (WSL)` interface, not `Ethernet` or `Wi-Fi`
- Check that containers are on bridge network, not host network

### Network Issues

**Problem:** Container can't reach internet
```bash
# Check Docker network
docker network ls
docker network inspect week12_net

# Check DNS in container
docker exec week12_lab cat /etc/resolv.conf
```

**Problem:** Port already in use
```bash
# Find what's using the port
sudo netstat -tlnp | grep 1025
# Or
sudo ss -tlnp | grep 1025

# Kill the process or use different port
```

### Service-Specific Issues

**Problem:** SMTP server not accepting connections
```bash
# Check if server is running inside container
docker exec week12_lab ps aux | grep smtp
docker logs week12_lab
```

**Problem:** gRPC import errors
```bash
# Reinstall grpc tools
pip install grpcio grpcio-tools --break-system-packages
# Regenerate stubs
python3 -m grpc_tools.protoc -I src/apps/rpc/grpc --python_out=src/apps/rpc/grpc --grpc_python_out=src/apps/rpc/grpc src/apps/rpc/grpc/calculator.proto
```

---

## 🧹 Complete Cleanup Procedure

### End of Session (Quick)

```bash
# Stop lab containers (Portainer stays running!)
cd /mnt/d/NETWORKING/WEEK12/12enWSL
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

## 📊 Week 12 Network Configuration Summary

| Resource | Value | Notes |
|----------|-------|-------|
| Network Subnet | 172.28.12.0/24 | week12_net |
| Lab Container | week12_lab | Main laboratory container |
| SMTP Server | localhost:1025 | Educational mail server |
| JSON-RPC Server | localhost:6200 | Calculator API |
| XML-RPC Server | localhost:6201 | Calculator API |
| gRPC Server | localhost:6251 | Calculator service (HTTP/2) |
| Portainer | 9000 | **RESERVED - Global service** |

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
*Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment*
