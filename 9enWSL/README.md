# Week 9: Session Layer and Presentation Layer

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
> 
> by Revolvix

---

## ⚠️ Environment Notice

This laboratory kit is designed for the **WSL2 + Ubuntu 22.04 + Docker + Portainer** environment.

**Repository:** https://github.com/antonioclim/netENwsl
**This Week's Folder:** `9enWSL`

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

# Clone Week 9
git clone https://github.com/antonioclim/netENwsl.git WEEK9
cd WEEK9
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
git clone https://github.com/antonioclim/netENwsl.git WEEK9
cd WEEK9
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
cd /mnt/d/NETWORKING/WEEK9/9enWSL
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

### Week 9 Network Configuration

Navigate: **Networks → week9_ftp_network**

Current configuration:
- Subnet: 172.29.9.0/24
- FTP Server: 172.29.9.x (dynamic)
- Client containers: 172.29.9.x (dynamic)

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

### Essential Wireshark Filters for Week 9

| Filter | Purpose |
|--------|---------|
| `tcp.port == 2121` | FTP control channel |
| `tcp.port >= 60000 && tcp.port <= 60010` | FTP passive data channels |
| `tcp.port == 2121 \|\| tcp.port >= 60000` | All FTP traffic |
| `ftp` | FTP commands and responses |
| `ftp.request.command == "USER"` | Authentication requests |
| `ftp.request.command == "PASV"` | Passive mode negotiation |
| `tcp.port == 60100` | Custom pseudo-FTP protocol |

### Analysing FTP Sessions

1. Filter: `tcp.port == 2121`
2. Find the USER/PASS sequence
3. Look for 230 response (authentication success)
4. Find PASV command and response showing port allocation
5. Follow TCP Stream for complete conversation

### Saving Captures

1. **File → Save As**
2. Navigate to: `D:\NETWORKING\WEEK9\pcap\`
3. Filename: `capture_ftp_session.pcap`

---

## Overview

This laboratory explores the upper layers of the OSI model—specifically Layer 5 (Session) and Layer 6 (Presentation)—which provide the crucial bridge between network transport mechanisms and application-level data handling. While often overlooked in favour of more visible protocols, these layers encapsulate essential abstractions for establishing logical communication channels, managing dialogue control, and ensuring data representation consistency across heterogeneous systems.

The Session Layer governs the establishment, maintenance, and termination of logical connections between communicating processes. Unlike the Transport Layer's focus on reliable byte-stream delivery, the Session Layer introduces higher-order concepts: authentication negotiation, checkpoint synchronisation for long-running transfers, and dialogue management (half-duplex versus full-duplex modes). The FTP protocol exemplifies these principles, employing separate control and data channels with explicit session semantics.

The Presentation Layer addresses the fundamental challenge of data heterogeneity: how can systems with different internal representations (big-endian versus little-endian architectures, varying character encodings, distinct serialisation formats) exchange information unambiguously? This layer standardises data encoding through mechanisms such as ASN.1/BER, XDR, JSON, and Protocol Buffers, whilst providing compression and encryption services that operate transparently to applications.

## Learning Objectives

By the end of this laboratory session, you will be able to:

1. **Identify** the distinguishing characteristics of connection-oriented transport versus session-based communication, articulating why FTP requires separate control and data channels
2. **Explain** the mechanisms by which the Presentation Layer resolves byte-ordering ambiguity through explicit endianness specification in binary protocols
3. **Implement** a custom binary framing protocol using Python's `struct` module, incorporating length prefixes, message type identifiers, and CRC-32 integrity verification
4. **Demonstrate** multi-client FTP session management within a containerised environment, observing authentication flows and passive mode negotiation
5. **Analyse** packet captures to distinguish control channel commands from data channel transfers, correlating protocol-level events with application behaviour
6. **Design** a checkpoint-recovery mechanism suitable for resuming interrupted file transfers, applying Session Layer principles to practical scenarios

## Prerequisites

### Knowledge Requirements
- Transport Layer fundamentals: TCP connection lifecycle, port multiplexing, flow control
- Basic socket programming concepts from previous laboratories
- Familiarity with Docker container networking and volume mounts
- Understanding of binary number representations (hexadecimal, two's complement)

### Software Requirements
- Windows 10/11 with WSL2 enabled
- Docker Engine (in WSL)
- Portainer CE (running globally on port 9000)
- Wireshark (native Windows installation)
- Python 3.11 or later
- Git (recommended for version control)

### Hardware Requirements
- Minimum 8GB RAM (16GB recommended)
- 10GB free disk space
- Network connectivity for container image retrieval

## Quick Start

### First-Time Setup (Run Once)

```bash
# Open Ubuntu terminal (WSL)
wsl

# Navigate to the kit directory
cd /mnt/d/NETWORKING/WEEK9/9enWSL

# Start Docker if not running
sudo service docker start

# Verify prerequisites
python3 setup/verify_environment.py

# If any issues, run the installer helper
python3 setup/install_prerequisites.py
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
| FTP Server | localhost:2121 | test / 12345 |
| FTP Passive Ports | 60000-60010 | (Data channel range) |

## Laboratory Exercises

### Exercise 1: Binary Encoding and Endianness

**Objective:** Understand byte-ordering conventions and implement binary message framing with integrity verification

**Duration:** 30-40 minutes

**Theoretical Foundation:**

Multi-byte integers admit two canonical orderings: big-endian (most significant byte first, network byte order) and little-endian (least significant byte first, x86 native order). The Presentation Layer's responsibility includes resolving this ambiguity through explicit format specification. Our exercise employs Python's `struct` module, which provides format strings indicating both byte order (`>` for big-endian, `<` for little-endian) and field types (`I` for unsigned 32-bit integer, `H` for unsigned 16-bit).

**Steps:**

1. Navigate to the exercises directory and open the endianness demonstration:
   ```bash
   cd src/exercises
   python3 ex_9_01_endianness.py
   ```

2. Observe the output comparing big-endian and little-endian representations of the same integer value. Note how the byte sequence differs whilst representing identical numerical quantities.

3. Examine the binary framing structure implemented in the script:
   - 4-byte magic number ("NET9")
   - 4-byte message length (big-endian)
   - 4-byte message type identifier
   - 4-byte CRC-32 checksum
   - Variable-length payload

4. Modify the script to encode a custom message and verify the CRC-32 computation:
   ```python
   # Try encoding your own message
   custom_payload = b"Session Layer demonstrates dialogue control"
   packed = pack_message(MSG_TYPE_DATA, custom_payload)
   ```

5. Introduce a deliberate bit-flip in the payload and observe the CRC verification failure.

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 1
```

**Expected Output:**
```
=== Endianness Demonstration ===
Integer value: 0x12345678 (305419896)
Big-endian bytes:    12 34 56 78
Little-endian bytes: 78 56 34 12

=== Binary Framing Demo ===
Header format: >4sIII (magic, length, type, crc)
Packed message (hex): 4e455439 00000020 00000001 a1b2c3d4 ...
Unpacked successfully: type=1, payload=28 bytes
CRC verification: PASS
```

---

### Exercise 2: Custom FTP Server and Multi-Client Sessions

**Objective:** Implement and observe session-based file transfer with authentication and mode negotiation

**Duration:** 45-60 minutes

**Theoretical Foundation:**

FTP exemplifies Session Layer concepts through its dual-channel architecture. The control channel (typically port 21, here port 2121) maintains an authenticated session handling commands (USER, PASS, LIST, RETR, STOR, QUIT) whilst data channels transfer file contents. Active mode has the server initiate data connections to the client; passive mode (PASV) reverses this, with clients connecting to server-specified ephemeral ports—essential for NAT traversal.

**Steps:**

1. Start the laboratory environment if not already running:
   ```bash
   python3 scripts/start_lab.py
   ```

2. Verify the FTP server is operational:
   ```bash
   python3 scripts/start_lab.py --status
   ```

3. Connect to the FTP server using the demonstration client:
   ```bash
   cd src/exercises
   python3 ftp_demo_client.py --host localhost --port 2121 --user test --password 12345
   ```

4. Execute session commands and observe the protocol exchange:
   ```
   ftp> LIST
   ftp> PWD
   ftp> PASV
   ftp> QUIT
   ```

5. Open Wireshark and capture traffic on the Docker network interface. Apply the filter:
   ```
   tcp.port == 2121 || tcp.port >= 60000
   ```

6. Run the multi-client demonstration to observe concurrent session handling:
   ```bash
   python3 scripts/run_demo.py --demo multi_client
   ```

7. In Wireshark, follow the TCP streams for each client session. Note the independent authentication sequences and how passive mode assigns different ports to each client.

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 2
```

**Expected Observations:**
- Each client receives a unique passive port within the 60000-60010 range
- Control channel remains open throughout the session whilst data channels are ephemeral
- Authentication failure (wrong credentials) terminates the session without establishing data channels

---

### Exercise 3: Pseudo-FTP Protocol Implementation

**Objective:** Build a simplified FTP-like protocol demonstrating session establishment, command parsing, and binary data transfer

**Duration:** 50-60 minutes

**Steps:**

1. Examine the pseudo-FTP server implementation:
   ```bash
   cd src/exercises
   # Review the code structure
   cat ex_9_02_pseudo_ftp.py
   ```

2. Start the pseudo-FTP server in one terminal:
   ```bash
   python3 ex_9_02_pseudo_ftp.py --mode server --port 60100
   ```

3. In a second terminal, connect with the client:
   ```bash
   python3 ex_9_02_pseudo_ftp.py --mode client --host localhost --port 60100
   ```

4. Test the session lifecycle:
   ```
   > AUTH test 12345
   > LIST
   > GET readme.txt
   > PUT local_file.txt
   > QUIT
   ```

5. Observe the binary protocol framing in Wireshark. Note the magic number prefix, length fields, and CRC validation occurring at the Presentation Layer.

6. Experiment with session checkpointing by interrupting a transfer (Ctrl+C during a large file PUT) and resuming.

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 3
```

---

## Demonstrations

### Demo 1: Endianness Visualisation

Automated demonstration showing byte-order differences across architectures:

```bash
python3 scripts/run_demo.py --demo endianness
```

**What to observe:**
- Side-by-side comparison of big-endian and little-endian byte sequences
- Hexadecimal dump of binary-packed structures
- CRC-32 computation producing identical checksums regardless of intermediate byte order

### Demo 2: FTP Session Lifecycle

Complete demonstration of FTP session establishment, command exchange, and teardown:

```bash
python3 scripts/run_demo.py --demo ftp_session
```

**What to observe:**
- Three-way TCP handshake preceding FTP banner
- USER/PASS authentication sequence with 230 response on success
- PASV mode negotiation revealing ephemeral port assignment
- LIST command triggering separate data channel for directory listing
- QUIT command and graceful connection termination

### Demo 3: Multi-Client Stress Test

Concurrent client connections demonstrating session isolation:

```bash
python3 scripts/run_demo.py --demo multi_client
```

**What to observe:**
- Server handling multiple simultaneous authentications
- Independent passive port allocation per client
- Session state isolation (one client's commands do not affect another)

### Demo 4: Binary Protocol Analysis

Deep inspection of custom binary protocol framing:

```bash
python3 scripts/run_demo.py --demo binary_protocol
```

**What to observe:**
- Magic number identification for protocol demarcation
- Length-prefixed message boundaries enabling reliable framing
- CRC-32 verification detecting simulated corruption

---

## Packet Capture and Analysis

### Capturing Traffic

```bash
# Start capture with helper script
python3 scripts/capture_traffic.py --duration 60 --output pcap/week9_ftp.pcap

# Or use Wireshark directly on Windows
# Select vEthernet (WSL) interface
```

### Suggested Wireshark Filters

```
# FTP control channel only
tcp.port == 2121

# FTP control and data channels
tcp.port == 2121 || (tcp.port >= 60000 && tcp.port <= 60010)

# FTP commands and responses
ftp

# Specific FTP commands
ftp.request.command == "LIST" || ftp.request.command == "RETR"

# FTP authentication
ftp.request.command == "USER" || ftp.request.command == "PASS"

# Custom protocol (by port if using ex_9_02)
tcp.port == 60100
```

### Analysis Exercises

1. **Session Duration Analysis:** Calculate the time between initial SYN and final FIN for an FTP session
2. **Passive Port Mapping:** Document the relationship between PASV response and subsequent data connection
3. **Byte-Order Verification:** Export raw bytes from a captured packet and manually verify endianness

---

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

---

## Homework Assignments

See the `homework/` directory for take-home exercises.

### Assignment 1: Enhanced Binary Protocol

Extend the binary framing protocol to support:
- Message fragmentation for payloads exceeding 1KB
- Sequence numbering for fragment reassembly
- Acknowledgement frames with selective retransmission

**Deliverable:** Modified `hw_9_01.py` implementing fragmentation/reassembly

### Assignment 2: Session Checkpoint Recovery

Implement a checkpoint mechanism for file transfers:
- Server records byte offsets at configurable intervals
- Client can query last checkpoint and resume from that position
- Handle out-of-order checkpoint requests gracefully

**Deliverable:** `hw_9_02.py` with checkpoint-enabled transfer protocol

---

## Troubleshooting

### Common Issues

#### Issue: FTP server not responding on port 2121
**Solution:** Verify Docker containers are running with `python3 scripts/start_lab.py --status`. If the container shows unhealthy, check logs with `docker logs s9_ftp_server`. Ensure no other service occupies port 2121.

#### Issue: Passive mode connections fail
**Solution:** Confirm ports 60000-60010 are exposed and not blocked by Windows Firewall. The Docker Compose configuration binds these ports to localhost.

#### Issue: CRC verification fails unexpectedly
**Solution:** Ensure consistent byte ordering when packing and unpacking. The format string must match exactly on both sides. Verify no truncation occurs during transmission.

#### Issue: Wireshark shows no traffic on Docker interface
**Solution:** Select the correct interface. On Windows with WSL, try `vEthernet (WSL)`. You may need to capture on `any` interface.

See `docs/troubleshooting.md` for additional solutions.

---

## Theoretical Background

### Session Layer (OSI Layer 5)

The Session Layer provides the mechanism for opening, closing, and managing a session between end-user application processes. Key responsibilities include:

**Dialogue Control:** Determining which participant may transmit at any moment (half-duplex, full-duplex, simplex modes). FTP's control channel operates in half-duplex fashion—client sends command, server responds—whilst data transfers may proceed independently.

**Synchronisation:** Inserting checkpoints into data streams for recovery purposes. Long file transfers can be checkpointed, allowing resumption from the last confirmed position rather than restarting entirely.

**Session Establishment:** Unlike transport connections (which deal in byte streams), sessions have semantic meaning—authentication state, negotiated parameters, and application context persist across multiple transport interactions.

### Presentation Layer (OSI Layer 6)

The Presentation Layer ensures that information sent from the application layer of one system is readable by the application layer of another system. Key functions include:

**Data Translation:** Converting between different character encodings (ASCII, EBCDIC, UTF-8), integer representations (big-endian, little-endian), and floating-point formats.

**Data Encryption:** Applying cryptographic transformations transparently to applications. TLS operates at this layer conceptually, though implementations often integrate with transport.

**Data Compression:** Reducing bandwidth requirements through algorithmic compression (gzip, zlib, brotli), decompressing before delivery to applications.

### Binary Protocol Design Principles

Well-designed binary protocols incorporate:

1. **Magic Numbers:** Fixed byte sequences identifying protocol and version, enabling quick rejection of malformed packets
2. **Length Prefixing:** Explicit payload length preceding variable data, enabling reliable message boundary detection
3. **Type Identifiers:** Numeric codes distinguishing message categories (request, response, error, data)
4. **Integrity Checksums:** CRC or cryptographic hashes detecting transmission errors or corruption
5. **Versioning:** Protocol version fields enabling graceful evolution and backward compatibility

---

## References

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (7th ed.). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress.
- Postel, J. & Reynolds, J. (1985). RFC 959: File Transfer Protocol. IETF.
- Stevens, W.R. (1994). *TCP/IP Illustrated, Volume 1: The Protocols*. Addison-Wesley.
- Python Documentation. *struct — Interpret bytes as packed binary data*. https://docs.python.org/3/library/struct.html

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Week 9 Laboratory Network                        │
│              (WSL2 + Ubuntu 22.04 + Docker + Portainer)                 │
│                         172.29.9.0/24 (Docker)                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────────┐      Control Channel (2121)                       │
│  │                  │◄────────────────────────────────────┐             │
│  │   FTP Server     │                                     │             │
│  │   (pyftpdlib)    │      Passive Data (60000-60010)     │             │
│  │   172.29.9.x     │◄─────────────────────────┐          │             │
│  │                  │                          │          │             │
│  └──────────────────┘                          │          │             │
│           │                                    │          │             │
│           │ Shared Volume                      │          │             │
│           │ (server-files)                     │          │             │
│           ▼                                    │          │             │
│  ┌──────────────────┐                 ┌────────┴───────┐  │             │
│  │   /srv/ftp/      │                 │                │  │             │
│  │   - test_file.txt│                 │   Client 1     │  │             │
│  │   - sample_data/ │                 │   (LIST test)  ├──┘             │
│  └──────────────────┘                 │   172.29.9.x   │                │
│                                       └────────────────┘                │
│                                                                         │
│                                       ┌────────────────┐                │
│  ┌──────────────────┐                 │                │                │
│  │  Host Machine    │                 │   Client 2     │                │
│  │  (Windows/WSL2)  │◄───Wireshark───►│   (GET test)   │                │
│  │  localhost:2121  │    Capture      │   172.29.9.x   │                │
│  └──────────────────┘                 └────────────────┘                │
│                                                                         │
│  Portainer: http://localhost:9000 (global service)                      │
│  Credentials: stud / studstudstud                                       │
└─────────────────────────────────────────────────────────────────────────┘

Session Layer Abstraction:
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   Client                              Server                            │
│   ┌─────────────┐                     ┌─────────────┐                   │
│   │ Application │                     │ Application │                   │
│   └──────┬──────┘                     └──────┬──────┘                   │
│          │                                   │                          │
│   ┌──────▼──────┐   Session Commands  ┌──────▼──────┐                   │
│   │   Session   │◄═══════════════════►│   Session   │                   │
│   │   (AUTH,    │   USER/PASS/QUIT    │   (State    │                   │
│   │   State)    │                     │   Machine)  │                   │
│   └──────┬──────┘                     └──────┬──────┘                   │
│          │                                   │                          │
│   ┌──────▼──────┐  Binary Framing     ┌──────▼──────┐                   │
│   │Presentation │◄═══════════════════►│Presentation │                   │
│   │ (Encoding,  │  struct.pack/unpack │ (Decoding,  │                   │
│   │  CRC-32)    │                     │  Verify)    │                   │
│   └──────┬──────┘                     └──────┬──────┘                   │
│          │                                   │                          │
│   ┌──────▼──────┐    TCP Segments     ┌──────▼──────┐                   │
│   │  Transport  │◄═══════════════════►│  Transport  │                   │
│   │    (TCP)    │                     │    (TCP)    │                   │
│   └─────────────┘                     └─────────────┘                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
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
docker network inspect week9_ftp_network

# Check DNS in container
docker exec s9_ftp_server cat /etc/resolv.conf
```

**Problem:** Port already in use
```bash
# Find what's using the port
sudo netstat -tlnp | grep 2121
# Or
sudo ss -tlnp | grep 2121

# Kill the process or use different port
```

### FTP-Specific Issues

**Problem:** FTP server returns "530 Login incorrect"
- Verify credentials: test / 12345
- Check environment variables in docker-compose.yml

**Problem:** Passive mode shows wrong IP
- Server may report internal Docker IP; this is normal for localhost connections

---

## 🧹 Complete Cleanup Procedure

### End of Session (Quick)

```bash
# Stop lab containers (Portainer stays running!)
cd /mnt/d/NETWORKING/WEEK9/9enWSL
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

## 📊 Week 9 Network Configuration Summary

| Resource | Value | Notes |
|----------|-------|-------|
| Network Subnet | 172.29.9.0/24 | week9_ftp_network |
| FTP Control Port | 2121 | Control channel |
| FTP Passive Range | 60000-60010 | Data channels |
| FTP Credentials | test / 12345 | Demo account |
| Pseudo-FTP Port | 60100 | Exercise 3 |
| Portainer | 9000 | **RESERVED - Global service** |

---

*NETWORKING class - ASE, Informatics | by Revolvix*
*Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment*
