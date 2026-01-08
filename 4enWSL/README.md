# Week 4: Physical Layer, Data Link Layer & Custom Protocols

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
> 
> by Revolvix

---

## ⚠️ Environment Notice

This laboratory kit is designed for the **WSL2 + Ubuntu 22.04 + Docker + Portainer** environment.

**Repository:** https://github.com/antonioclim/netENwsl
**This Week's Folder:** `4enWSL`

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

# Clone Week 4
git clone https://github.com/antonioclim/netENwsl.git WEEK4
cd WEEK4
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
git clone https://github.com/antonioclim/netENwsl.git WEEK4
cd WEEK4
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
cd /mnt/d/NETWORKING/WEEK4/4enWSL
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

### Modifying Container IP Address

1. Navigate: **Networks → week4_network**
2. View current IPAM configuration (172.28.0.0/16)
3. To change:
   - Stop containers using the network
   - Edit `docker-compose.yml`
   - Recreate: `docker compose down && docker compose up -d`

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

### Essential Wireshark Filters for Week 4

| Filter | Purpose |
|--------|---------|
| `tcp.port == 5400` | TEXT protocol traffic |
| `tcp.port == 5401` | BINARY protocol traffic |
| `udp.port == 5402` | UDP sensor traffic |
| `tcp.port == 5400 && tcp.len > 0` | TEXT data packets only |
| `tcp.payload contains "SET"` | TEXT commands containing SET |

### Following a TCP Conversation

1. Find any packet in the conversation
2. Right-click → **Follow → TCP Stream**
3. View complete conversation in readable text

### Viewing Binary Protocol Headers

1. Select a packet on port 5401
2. View → Bytes to see hex dump
3. Identify: magic (2B), version (1B), type (1B), length (2B), seq (4B), CRC32 (4B)

### Saving Captures

1. **File → Save As**
2. Navigate to: `D:\NETWORKING\WEEK4\pcap\`
3. Filename: `capture_exercise_N.pcap`

---

## Overview

This laboratory session bridges the theoretical foundations of network communication—the Physical and Data Link layers—with practical protocol implementation skills. The Physical Layer transforms bits into signals that traverse physical media, whilst the Data Link Layer structures these bits into meaningful frames with addressing, error detection, and medium access control.

Whilst application programmers rarely interact directly with Layers 1 and 2, comprehending their mechanics proves essential for diagnosing network anomalies, optimising performance, and designing efficient protocols. When packets mysteriously vanish, when latency spikes unpredictably, or when architectural decisions demand choosing between Ethernet and WiFi for mission-critical applications, these foundational concepts transition from theoretical abstractions to practical necessities.

The practical component focuses on implementing custom protocols over TCP and UDP—demonstrating the fundamental difference between stream-oriented and datagram-oriented communication. You will construct text-based protocols with length-prefixed framing, binary protocols with structured headers and CRC32 integrity verification, and UDP sensor protocols that handle connectionless communication.

## Learning Objectives

By the end of this laboratory session, you will be able to:

1. **Recall** the function of the Physical Layer and enumerate transmission media characteristics including attenuation, noise, crosstalk, and dispersion
2. **Explain** the distinction between text and binary protocols, articulating the trade-offs in overhead, parsing complexity, and human readability
3. **Implement** concurrent TCP servers utilising multi-threading and construct custom protocols with proper framing mechanisms
4. **Apply** the `struct` module for binary serialisation and CRC32 checksums for integrity verification
5. **Analyse** captured network traffic using tcpdump and Wireshark to identify protocol overhead and diagnose communication anomalies
6. **Evaluate** the efficiency of different protocol designs by comparing overhead ratios and parsing complexity

## Prerequisites

### Knowledge Requirements
- TCP and UDP socket fundamentals from Week 3
- Basic Python threading concepts
- Understanding of byte representations and encoding
- Familiarity with Docker container operations

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
- Network connectivity

## Quick Start

### First-Time Setup (Run Once)

```bash
# Open Ubuntu terminal (WSL)
wsl

# Navigate to the kit directory
cd /mnt/d/NETWORKING/WEEK4/4enWSL

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
| TEXT Protocol Server | localhost:5400 | None |
| BINARY Protocol Server | localhost:5401 | None |
| UDP Sensor Server | localhost:5402/udp | None |

## Laboratory Exercises

### Exercise 1: Text Protocol Implementation

**Objective:** Implement a custom TEXT protocol server supporting multiple commands with length-prefixed framing.

**Duration:** 45 minutes

**Protocol Specification:**
```
Frame Format: "<LENGTH> <PAYLOAD>"
Example: "11 SET name Alice"
         ^^  ^^^^^^^^^^^^^^
         |   payload (11 bytes)
         payload length
```

**Supported Commands:**
| Command | Description | Example Input | Example Output |
|---------|-------------|---------------|----------------|
| PING | Connectivity test | `PING` | `OK pong` |
| SET | Store key-value pair | `SET name Alice` | `OK stored name` |
| GET | Retrieve value | `GET name` | `OK name Alice` |
| DEL | Delete key | `DEL name` | `OK deleted` |
| COUNT | Count stored keys | `COUNT` | `OK 3 keys` |
| KEYS | List all keys | `KEYS` | `OK key1 key2 key3` |
| QUIT | Close connection | `QUIT` | `OK bye` |

**Steps:**

1. Start the TEXT protocol server:
   ```bash
   python3 scripts/start_lab.py --service text
   ```

2. Connect using the interactive client:
   ```bash
   python3 src/apps/text_proto_client.py --host localhost --port 5400
   ```

3. Execute a sequence of commands:
   ```bash
   python3 src/apps/text_proto_client.py --host localhost --port 5400 \
       -c "SET name Alice" -c "SET city Bucharest" -c "GET name" -c "COUNT"
   ```

4. Observe the framing mechanism—note how each message includes its length prefix.

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 1
```

### Exercise 2: Binary Protocol Implementation

**Objective:** Implement a binary protocol with fixed headers, sequence numbers, and CRC32 integrity verification.

**Duration:** 60 minutes

**Protocol Specification:**

Fixed header (14 bytes):
```
+--------+--------+--------+------------+--------+--------+
| magic  |version | type   |payload_len |  seq   | crc32  |
| 2B     | 1B     | 1B     | 2B         |  4B    | 4B     |
+--------+--------+--------+------------+--------+--------+
  "NP"      1     1-255     0-65535     uint32   uint32
```

**Message Types:**
| Type | Code | Description |
|------|------|-------------|
| ECHO_REQ | 1 | Echo request |
| ECHO_RESP | 2 | Echo response |
| PUT_REQ | 3 | Store key-value |
| PUT_RESP | 4 | Storage confirmation |
| GET_REQ | 5 | Retrieve value |
| GET_RESP | 6 | Retrieved value |
| KEYS_REQ | 7 | List keys |
| KEYS_RESP | 8 | Keys list |
| COUNT_REQ | 9 | Count keys |
| COUNT_RESP | 10 | Key count |
| ERROR | 255 | Error response |

**Steps:**

1. Start the BINARY protocol server:
   ```bash
   python3 scripts/start_lab.py --service binary
   ```

2. Launch the interactive binary client:
   ```bash
   python3 src/apps/binary_proto_client.py --host localhost --port 5401
   ```

3. Available commands in interactive mode: `echo`, `put`, `get`, `count`, `keys`, `quit`

4. Examine the CRC32 verification by intentionally corrupting a packet (use `--corrupt` flag with the client).

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 2
```

### Exercise 3: UDP Sensor Protocol

**Objective:** Implement a UDP-based sensor data aggregator that collects, validates, and reports sensor readings.

**Duration:** 45 minutes

**Datagram Structure (23 bytes):**
```
+--------+-----------+--------+----------+--------+
|version | sensor_id |  temp  | location | crc32  |
| 1B     | 4B        | 4B(f)  | 10B      | 4B     |
+--------+-----------+--------+----------+--------+
```

**Steps:**

1. Start the UDP sensor server:
   ```bash
   python3 scripts/start_lab.py --service udp
   ```

2. Simulate a single sensor reading:
   ```bash
   python3 src/apps/udp_sensor_client.py --host localhost --port 5402 \
       --sensor-id 1 --temp 23.5 --location "Lab1"
   ```

3. Run continuous sensor simulation:
   ```bash
   python3 src/apps/udp_sensor_client.py --host localhost --port 5402 \
       --sensor-id 1 --location "Lab1" --continuous --interval 1.0
   ```

4. Test error detection with corrupted packets:
   ```bash
   python3 src/apps/udp_sensor_client.py --host localhost --port 5402 \
       --sensor-id 99 --temp 0.0 --location "Test" --corrupt
   ```

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 3
```

### Exercise 4: Protocol Overhead Analysis

**Objective:** Compare and analyse the overhead characteristics of TEXT vs BINARY protocols.

**Duration:** 30 minutes

**Steps:**

1. Generate identical operations using both protocols
2. Capture traffic for each protocol
3. Calculate overhead ratios:
   - TEXT: (total bytes - payload bytes) / total bytes
   - BINARY: (header bytes) / total bytes

**Analysis Questions:**
- Which protocol has lower overhead for small payloads?
- How does overhead scale with payload size?
- What are the parsing complexity trade-offs?

## Demonstrations

### Demo 1: Protocol Comparison

Run the automated protocol comparison demonstration:

```bash
python3 scripts/run_demo.py --demo 1
```

**What to observe:**
- Same data sent via TEXT and BINARY protocols
- Overhead differences in packet sizes
- Timing differences due to parsing complexity

### Demo 2: CRC Validation

Test the integrity verification system:

```bash
python3 scripts/run_demo.py --demo 2
```

**What to observe:**
- Valid packets accepted and processed
- Corrupted packets detected and rejected
- CRC mismatch error messages in server logs

## Packet Capture and Analysis

### Capturing Traffic

```bash
# Start capture on all interfaces
python3 scripts/capture_traffic.py --interface any --output pcap/week4_capture.pcap

# Capture specific port only
python3 scripts/capture_traffic.py --interface any --port 5400 --output pcap/text_proto.pcap

# Or use Wireshark directly (run as Administrator on Windows)
# Open Wireshark > Select appropriate interface > Start capture
```

### Suggested Wireshark Filters

```
# TEXT protocol traffic
tcp.port == 5400

# BINARY protocol traffic
tcp.port == 5401

# UDP sensor traffic
udp.port == 5402

# Show only data packets (exclude TCP handshake)
tcp.port == 5400 && tcp.len > 0

# Filter by payload content (TEXT protocol)
tcp.port == 5400 && tcp.payload contains "SET"
```

### Traffic Analysis Tips

1. **Frame inspection**: Right-click packet → Follow → TCP Stream to view complete exchanges
2. **Hex dump**: View → Bytes to examine binary protocol headers
3. **Time analysis**: Statistics → Flow Graph to visualise request-response timing

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

### Assignment 1: Extended Command Set

Extend the TEXT protocol server with additional commands:
- `APPEND key value` - Append to existing value
- `INCR key` - Increment numeric value
- `EXPIRE key seconds` - Set key expiration

**Deadline:** Before Week 5 laboratory

### Assignment 2: Multi-Sensor Aggregator

Modify the UDP sensor aggregator to:
- Support multiple sensor types (temperature, humidity, pressure)
- Implement sliding window averages
- Generate alerts for out-of-range values

**Deadline:** Before Week 5 laboratory

## Troubleshooting

### Common Issues

#### Issue: Port already in use
**Symptoms:** "Address already in use" error when starting server
**Solution:**
```bash
# Find process using port (in WSL)
sudo ss -tlnp | grep 5400

# Or using lsof
lsof -i :5400

# Kill the process
kill <PID>

# Or use cleanup script
python3 scripts/cleanup.py --full
```

#### Issue: Docker containers not starting
**Symptoms:** "Cannot connect to Docker daemon" error
**Solution:**
```bash
sudo service docker start
docker ps
```

#### Issue: Connection refused from client
**Symptoms:** Client cannot connect to server
**Solution:**
```bash
# Verify server is running
python3 scripts/start_lab.py --status

# Check Docker container logs
docker logs week4_demo

# Manual server start with verbose output
python3 src/apps/text_proto_server.py --verbose
```

#### Issue: CRC validation failures
**Symptoms:** All packets rejected as invalid
**Solution:**
1. Verify client and server use identical `struct` format strings
2. Check byte order (should be big-endian: `>`)
3. Ensure CRC is calculated over correct payload bytes

See `docs/troubleshooting.md` for additional solutions.

## Theoretical Background

### Physical Layer Concepts

The Physical Layer (Layer 1 of OSI) manages bit-to-signal conversion across transmission media. Key concepts include:

- **Transmission Media**: Guided (coaxial, twisted pair, fibre) and unguided (wireless)
- **Line Coding**: NRZ, NRZI, Manchester encoding for synchronisation
- **Modulation**: ASK, FSK, PSK, QAM for wireless transmission
- **Channel Impairments**: Attenuation, noise, crosstalk, dispersion

### Data Link Layer Concepts

The Data Link Layer (Layer 2) structures bit streams into frames:

- **MAC Addressing**: 48-bit hardware addresses (OUI + interface ID)
- **Framing**: Delimiting messages within continuous bit streams
- **Error Detection**: CRC/FCS checksums
- **Medium Access**: CSMA/CD (Ethernet), CSMA/CA (WiFi)
- **Switching**: CAM learning and frame forwarding

### Protocol Design Principles

- **Framing**: Length-prefix vs delimiter-based approaches
- **Integrity**: Checksums (CRC32) vs cryptographic hashes
- **Efficiency**: Binary compactness vs text readability
- **Extensibility**: Version fields and reserved bytes

## References

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (7th ed.). Pearson.
- Rhodes, B. & Goerzen, J. (2014). *Foundations of Python Network Programming*. Apress.
- Stevens, W.R. (1994). *TCP/IP Illustrated, Volume 1*. Addison-Wesley.
- IEEE 802.3 Ethernet Standard
- IEEE 802.11 Wireless LAN Standard

### Python Documentation
- [socket — Low-level networking interface](https://docs.python.org/3/library/socket.html)
- [struct — Interpret bytes as packed binary data](https://docs.python.org/3/library/struct.html)
- [zlib — Compression compatible with gzip](https://docs.python.org/3/library/zlib.html)
- [threading — Thread-based parallelism](https://docs.python.org/3/library/threading.html)

### Relevant RFCs
- RFC 793 - Transmission Control Protocol
- RFC 768 - User Datagram Protocol
- RFC 826 - Address Resolution Protocol

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    WEEK 4 Laboratory Architecture                    │
│               (WSL2 + Ubuntu 22.04 + Docker + Portainer)            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ┌─────────────────────┐     ┌─────────────────────────────────┐   │
│   │   Windows Host      │     │   Docker Container (week4_demo)  │   │
│   │                     │     │                                  │   │
│   │  ┌───────────────┐  │     │  ┌─────────────────────────────┐│   │
│   │  │  Wireshark    │  │     │  │   TEXT Server (TCP:5400)    ││   │
│   │  │  (Analysis)   │  │     │  │   - Length-prefix framing   ││   │
│   │  └───────────────┘  │     │  │   - Key-value store         ││   │
│   │                     │     │  └─────────────────────────────┘│   │
│   │  ┌───────────────┐  │     │                                  │   │
│   │  │  Python       │◄─┼─────┼──┌─────────────────────────────┐│   │
│   │  │  Clients      │  │     │  │  BINARY Server (TCP:5401)   ││   │
│   │  └───────────────┘  │     │  │   - Fixed 14-byte header    ││   │
│   │         │           │     │  │   - CRC32 validation        ││   │
│   │         │           │     │  └─────────────────────────────┘│   │
│   │         │           │     │                                  │   │
│   │         │           │     │  ┌─────────────────────────────┐│   │
│   │         └───────────┼─────┼──│  UDP Sensor (UDP:5402)      ││   │
│   │                     │     │  │   - 23-byte datagrams       ││   │
│   │                     │     │  │   - Periodic reporting      ││   │
│   │                     │     │  └─────────────────────────────┘│   │
│   │                     │     │                                  │   │
│   │  ┌───────────────┐  │     └─────────────────────────────────┘   │
│   │  │  Portainer    │  │                                            │
│   │  │  :9000        │◄─┼──── http://localhost:9000                  │
│   │  │  (global)     │  │     Credentials: stud / studstudstud       │
│   │  └───────────────┘  │                                            │
│   │                     │                                            │
│   └─────────────────────┘                                            │
│                                                                      │
│   Port Mapping:                                                      │
│   • 5400:5400/tcp  → TEXT Protocol Server                           │
│   • 5401:5401/tcp  → BINARY Protocol Server                         │
│   • 5402:5402/udp  → UDP Sensor Server                              │
│   • 9000 (global)  → Portainer Management (RESERVED)                │
│                                                                      │
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
docker network inspect week4_network

# Check DNS in container
docker exec week4_demo cat /etc/resolv.conf
```

**Problem:** Port already in use
```bash
# Find what's using the port
sudo netstat -tlnp | grep 5400
# Or
sudo ss -tlnp | grep 5400

# Kill the process or use different port
```

### Protocol-Specific Issues

**Problem:** TEXT protocol parsing errors
```bash
# Enable verbose mode
python3 src/apps/text_proto_server.py --verbose

# Check frame format
# Expected: "<LENGTH> <PAYLOAD>"
```

**Problem:** CRC32 mismatch in BINARY protocol
```bash
# Verify byte order
python3 -c "import struct; print(struct.pack('>I', 12345).hex())"
# Should be big-endian
```

---

## 🧹 Complete Cleanup Procedure

### End of Session (Quick)

```bash
# Stop lab containers (Portainer stays running!)
cd /mnt/d/NETWORKING/WEEK4/4enWSL
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

## 📊 Week 4 Network Configuration Summary

| Resource | Value | Notes |
|----------|-------|-------|
| Subnet | 172.28.0.0/16 | Week 4 dedicated subnet |
| TEXT Protocol Port | 5400/tcp | Length-prefix framing |
| BINARY Protocol Port | 5401/tcp | Fixed header with CRC32 |
| UDP Sensor Port | 5402/udp | 23-byte datagrams |
| Portainer | 9000 | **RESERVED - Global service** |

---

*NETWORKING class - ASE, Informatics | by Revolvix*
*Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment*
