# Week 12: Email Protocols and Remote Procedure Call

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
> 
> by Revolvix

## Overview

Week 12 bridges two essential pillars of application-layer networking: electronic mail protocols and remote procedure call paradigms. The email component explores SMTP (Simple Mail Transfer Protocol) as a canonical example of a text-based, stateful application protocol, demonstrating how commands, responses, and multi-line data transfers operate at the TCP level. Students will observe the elegance of human-readable protocol dialogues whilst appreciating the precision required for reliable message delivery.

The RPC component shifts focus to distributed computing patterns, examining how modern systems enable function invocation across network boundaries as though calling local procedures. Through comparative analysis of JSON-RPC 2.0, XML-RPC, and gRPC with Protocol Buffers, students will understand the trade-offs between simplicity, verbosity, and performance that guide architectural decisions in microservices, APIs, and enterprise systems.

This laboratory synthesises theoretical knowledge with hands-on implementation, packet capture analysis, and performance benchmarking—providing a comprehensive foundation for understanding how contemporary distributed applications communicate.

## Learning Objectives

By the end of this laboratory session, you will be able to:

1. **Recall** the structure of SMTP dialogues, including commands (HELO, MAIL FROM, RCPT TO, DATA) and response codes
2. **Explain** the RPC abstraction and articulate the roles of client stubs, server stubs, and serialisation layers
3. **Implement** educational SMTP servers and RPC endpoints using Python's standard library and third-party frameworks
4. **Demonstrate** client-server communication using netcat, curl, and programmatic clients
5. **Analyse** protocol differences between JSON-RPC, XML-RPC, and gRPC by examining packet captures and payload structures
6. **Compare** serialisation overhead and latency characteristics through controlled benchmarks
7. **Design** appropriate protocol selections for given distributed system requirements
8. **Evaluate** the suitability of different RPC frameworks for microservices, public APIs, and legacy integrations

## Prerequisites

### Knowledge Requirements
- OSI and TCP/IP models (Weeks 2-3)
- Socket programming fundamentals (Week 3)
- HTTP protocol basics (Week 8)
- TCP connection lifecycle and flow control
- Basic understanding of serialisation (JSON, XML)

### Software Requirements
- Windows 10/11 with WSL2 enabled
- Docker Desktop (WSL2 backend)
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

```powershell
# Open PowerShell as Administrator
cd WEEK12_WSLkit

# Verify prerequisites
python setup/verify_environment.py

# If any issues, run the installer helper
python setup/install_prerequisites.py
```

### Starting the Laboratory

```powershell
# Start all services
python scripts/start_lab.py

# Verify everything is running
python scripts/start_lab.py --status
```

### Accessing Services

| Service | URL/Port | Description |
|---------|----------|-------------|
| Portainer | https://localhost:9443 | Docker management interface |
| SMTP Server | localhost:1025 | Educational SMTP server |
| JSON-RPC | http://localhost:6200 | JSON-RPC 2.0 calculator API |
| XML-RPC | http://localhost:6201 | XML-RPC calculator API |
| gRPC | localhost:6251 | gRPC calculator service |

## Laboratory Exercises

### Exercise 1: SMTP Protocol Exploration

**Objective:** Understand the structure and flow of SMTP dialogues through hands-on interaction

**Duration:** 45 minutes

**Background:**
SMTP is a text-based protocol operating over TCP port 25 (or 587 for submission, 1025 for testing). Each command from the client receives a numeric response code from the server, where 2xx indicates success, 3xx indicates intermediate status, 4xx indicates temporary failure, and 5xx indicates permanent failure.

**Steps:**

1. Start the SMTP server in one terminal:
   ```powershell
   python scripts/start_lab.py --service smtp
   ```

2. Open a manual SMTP session using netcat:
   ```powershell
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
   ```powershell
   dir docker/volumes/spool/*.eml
   type docker/volumes/spool/*.eml
   ```

**Verification:**
```powershell
python tests/test_exercises.py --exercise 1
```

**Expected Observations:**
- SMTP dialogue is human-readable plain text
- The DATA phase streams content until a lone period terminates
- Message headers and body are separated by a blank line
- Server stores complete RFC 5322 compliant messages

### Exercise 2: JSON-RPC Implementation

**Objective:** Implement and test JSON-RPC 2.0 requests including batch operations and error handling

**Duration:** 30 minutes

**Steps:**

1. Start the JSON-RPC server:
   ```powershell
   python scripts/start_lab.py --service jsonrpc
   ```

2. Test with curl (single request):
   ```powershell
   curl -s -X POST "http://localhost:6200" `
     -H "Content-Type: application/json" `
     -d '{"jsonrpc":"2.0","id":1,"method":"add","params":[10,32]}'
   ```

3. Test batch requests:
   ```powershell
   curl -s -X POST "http://localhost:6200" `
     -H "Content-Type: application/json" `
     -d '[{"jsonrpc":"2.0","id":1,"method":"add","params":[1,2]},{"jsonrpc":"2.0","id":2,"method":"multiply","params":[3,4]}]'
   ```

4. Test error handling:
   ```powershell
   curl -s -X POST "http://localhost:6200" `
     -H "Content-Type: application/json" `
     -d '{"jsonrpc":"2.0","id":1,"method":"divide","params":[10,0]}'
   ```

5. Run the Python client demonstration:
   ```powershell
   python src/apps/rpc/jsonrpc/jsonrpc_client.py --demo
   ```

**Verification:**
```powershell
python tests/test_exercises.py --exercise 2
```

### Exercise 3: XML-RPC Comparison

**Objective:** Compare XML-RPC with JSON-RPC to understand serialisation overhead

**Duration:** 25 minutes

**Steps:**

1. Start the XML-RPC server:
   ```powershell
   python scripts/start_lab.py --service xmlrpc
   ```

2. Use Python's built-in client:
   ```python
   import xmlrpc.client
   proxy = xmlrpc.client.ServerProxy("http://localhost:6201", allow_none=True)
   print(proxy.add(10, 32))
   print(proxy.system.listMethods())
   ```

3. Compare payload sizes by capturing both protocols:
   ```powershell
   python scripts/capture_traffic.py --duration 30 --ports 6200,6201
   ```

4. In parallel, run equivalent operations on both servers

**Expected Observations:**
- XML-RPC requests are significantly larger due to XML verbosity
- Both protocols transport over HTTP POST
- XML-RPC provides introspection via system.* methods

### Exercise 4: gRPC and Protocol Buffers

**Objective:** Experience strongly-typed RPC with HTTP/2 and binary serialisation

**Duration:** 30 minutes

**Steps:**

1. Examine the Protocol Buffer definition:
   ```powershell
   type src/apps/rpc/grpc/calculator.proto
   ```

2. Start the gRPC server:
   ```powershell
   python scripts/start_lab.py --service grpc
   ```

3. Run the gRPC client:
   ```powershell
   python src/apps/rpc/grpc/grpc_client.py --demo
   ```

4. Observe error handling with division by zero

**Expected Observations:**
- gRPC uses binary Protocol Buffers (not human-readable)
- Error responses use gRPC status codes rather than HTTP status
- Strong typing enforced at compile time via generated stubs

### Exercise 5: Performance Benchmarking

**Objective:** Quantify the performance characteristics of different RPC frameworks

**Duration:** 20 minutes

**Steps:**

1. Run the automated benchmark:
   ```powershell
   python scripts/run_demo.py --demo benchmark
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

```powershell
python scripts/run_demo.py --demo smtp
```

**What to observe:**
- TCP three-way handshake before SMTP dialogue
- Clear text command/response exchange
- DATA phase with dot-stuffing for termination

### Demo 2: RPC Protocol Comparison

Side-by-side demonstration of JSON-RPC, XML-RPC, and gRPC.

```powershell
python scripts/run_demo.py --demo rpc-compare
```

**What to observe:**
- Payload size differences
- Response time variations
- Error format differences

### Demo 3: Batch Request Efficiency

Demonstrates the efficiency gains from JSON-RPC batch requests.

```powershell
python scripts/run_demo.py --demo batch
```

## Packet Capture and Analysis

### Capturing Traffic

```powershell
# Start capture for all Week 12 ports
python scripts/capture_traffic.py --interface any --output pcap/week12_capture.pcap

# Or use Wireshark directly on Windows
# Interface: \Device\NPF_Loopback (for localhost traffic)
```

### Suggested Wireshark Filters

```
# SMTP traffic
tcp.port == 1025

# JSON-RPC (HTTP)
tcp.port == 6200 && http

# XML-RPC (HTTP)
tcp.port == 6201 && http

# gRPC (HTTP/2)
tcp.port == 6251

# All Week 12 traffic
tcp.port in {1025, 6200, 6201, 6251}

# HTTP POST requests only (RPC calls)
http.request.method == "POST"

# JSON-RPC content
http contains "jsonrpc"

# XML-RPC content
http contains "methodCall"
```

### Analysis Guidelines

1. **SMTP Analysis:**
   - Follow TCP stream to see complete dialogue
   - Identify each command and response pair
   - Locate the DATA phase termination

2. **RPC Payload Comparison:**
   - Export HTTP content for identical operations
   - Compare byte counts between JSON and XML
   - Note HTTP header overhead

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

### Assignment 1: Extended SMTP Client

Implement an SMTP client that supports MIME attachments and proper header formatting. Your client should be able to send emails with attachments to the educational server.

### Assignment 2: Custom RPC Method

Extend the JSON-RPC server with a new method `string_stats(text)` that returns statistics about the input string (length, word count, character frequency). Implement corresponding client code and write tests.

### Assignment 3: Protocol Analysis Report

Capture traffic for identical operations across all three RPC protocols. Prepare a brief report (1-2 pages) comparing payload sizes, header overhead, and observed latency. Include annotated Wireshark screenshots.

## Troubleshooting

### Common Issues

#### Issue: Port already in use
**Solution:** Check for existing processes and either stop them or use alternative ports:
```powershell
netstat -ano | findstr ":1025"
python scripts/start_lab.py --smtp-port 2025
```

#### Issue: Docker containers fail to start
**Solution:** Ensure Docker Desktop is running with WSL2 backend:
```powershell
docker info | findstr "Operating System"
# Should show: Operating System: Docker Desktop
```

#### Issue: gRPC import errors
**Solution:** Regenerate Protocol Buffer stubs:
```powershell
python -m grpc_tools.protoc -I src/apps/rpc/grpc --python_out=src/apps/rpc/grpc --grpc_python_out=src/apps/rpc/grpc src/apps/rpc/grpc/calculator.proto
```

#### Issue: Permission denied for packet capture
**Solution:** Run capture tools with appropriate privileges or use Wireshark on Windows instead of tcpdump in WSL.

See `docs/troubleshooting.md` for more solutions.

## Theoretical Background

### SMTP Protocol

SMTP, defined in RFC 5321, operates as a push protocol for mail transfer. The protocol follows a command-response model where the client issues commands (HELO, MAIL FROM, RCPT TO, DATA, QUIT) and the server responds with three-digit status codes. The mail transaction involves three phases: envelope specification (sender and recipients), data transfer (headers and body), and commitment (server accepts responsibility for delivery).

### RPC Paradigm

Remote Procedure Call abstracts network communication, presenting remote function invocations with the same syntax as local calls. The RPC middleware handles marshalling (serialising parameters), transmission, unmarshalling (deserialising on the server), execution, and result return. Key considerations include:

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
│   └──────┬───────────────────┬───────────────────┬──────┘          │
│          │                   │                   │                  │
│   ┌──────┴──────┐     ┌──────┴──────┐     ┌──────┴──────┐          │
│   │   gRPC      │     │  Wireshark  │     │  Portainer  │          │
│   │   Server    │     │  Capture    │     │    CE       │          │
│   │   :6251     │     │  Interface  │     │   :9443     │          │
│   │  (HTTP/2)   │     │             │     │  (HTTPS)    │          │
│   └─────────────┘     └─────────────┘     └─────────────┘          │
│                                                                     │
│   Data Flow:                                                        │
│   ─────────────────────────────────────────────────────────         │
│   Client ──▶ [Serialisation] ──▶ TCP/HTTP ──▶ Server                │
│          ◀── [Deserialisation] ◀── TCP/HTTP ◀──                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

*NETWORKING class - ASE, Informatics | by Revolvix*
