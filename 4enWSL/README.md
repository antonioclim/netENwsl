# Week 4: Physical Layer, Data Link Layer & Custom Protocols

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
> 
> by Revolvix

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
- Docker Desktop (WSL2 backend)
- Wireshark (native Windows installation)
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
cd WEEK4_WSLkit

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

| Service | URL/Port | Credentials |
|---------|----------|-------------|
| Portainer | https://localhost:9443 | Set on first access |
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
   ```powershell
   python scripts/start_lab.py --service text
   ```

2. Connect using the interactive client:
   ```powershell
   python src/apps/text_proto_client.py --host localhost --port 5400
   ```

3. Execute a sequence of commands:
   ```powershell
   python src/apps/text_proto_client.py --host localhost --port 5400 \
       -c "SET name Alice" -c "SET city Bucharest" -c "GET name" -c "COUNT"
   ```

4. Observe the framing mechanism—note how each message includes its length prefix.

**Verification:**
```powershell
python tests/test_exercises.py --exercise 1
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
   ```powershell
   python scripts/start_lab.py --service binary
   ```

2. Launch the interactive binary client:
   ```powershell
   python src/apps/binary_proto_client.py --host localhost --port 5401
   ```

3. Available commands in interactive mode: `echo`, `put`, `get`, `count`, `keys`, `quit`

4. Examine the CRC32 verification by intentionally corrupting a packet (use `--corrupt` flag with the client).

**Verification:**
```powershell
python tests/test_exercises.py --exercise 2
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
   ```powershell
   python scripts/start_lab.py --service udp
   ```

2. Simulate a single sensor reading:
   ```powershell
   python src/apps/udp_sensor_client.py --host localhost --port 5402 \
       --sensor-id 1 --temp 23.5 --location "Lab1"
   ```

3. Run continuous sensor simulation:
   ```powershell
   python src/apps/udp_sensor_client.py --host localhost --port 5402 \
       --sensor-id 1 --location "Lab1" --continuous --interval 1.0
   ```

4. Test error detection with corrupted packets:
   ```powershell
   python src/apps/udp_sensor_client.py --host localhost --port 5402 \
       --sensor-id 99 --temp 0.0 --location "Test" --corrupt
   ```

**Verification:**
```powershell
python tests/test_exercises.py --exercise 3
```

### Exercise 4: Protocol Overhead Analysis

**Objective:** Compare the efficiency of TEXT versus BINARY protocols for equivalent operations.

**Duration:** 30 minutes

**Steps:**

1. Start traffic capture:
   ```powershell
   python scripts/capture_traffic.py --interface any --output pcap/overhead_analysis.pcap
   ```

2. Execute identical operations on both servers:
   ```powershell
   # TEXT protocol
   python src/apps/text_proto_client.py --host localhost --port 5400 \
       -c "SET username administrator" -c "GET username"
   
   # BINARY protocol
   python src/apps/binary_proto_client.py --host localhost --port 5401 \
       -c "put username administrator" -c "get username"
   ```

3. Stop capture and analyse:
   ```powershell
   # Open in Wireshark
   wireshark pcap/overhead_analysis.pcap
   ```

4. Calculate overhead ratios using the analysis guide in `docs/overhead_analysis.md`.

**Verification:**
```powershell
python tests/test_exercises.py --exercise 4
```

## Demonstrations

### Demo 1: Complete Protocol Showcase

Automated demonstration of all three protocol implementations:

```powershell
python scripts/run_demo.py --demo 1
```

**What to observe:**
- TEXT protocol command-response cycle with length-prefixed framing
- BINARY protocol header structure and CRC32 validation
- UDP sensor datagrams with periodic reporting
- Server logs showing concurrent client handling

### Demo 2: Error Detection in Action

Demonstrates CRC32 integrity verification:

```powershell
python scripts/run_demo.py --demo 2
```

**What to observe:**
- Valid packets accepted and processed
- Corrupted packets detected and rejected
- CRC mismatch error messages in server logs

## Packet Capture and Analysis

### Capturing Traffic

```powershell
# Start capture on all interfaces
python scripts/capture_traffic.py --interface any --output pcap/week4_capture.pcap

# Capture specific port only
python scripts/capture_traffic.py --interface any --port 5400 --output pcap/text_proto.pcap

# Or use Wireshark directly (run as Administrator)
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
```powershell
# Find process using port
netstat -ano | findstr :5400

# Terminate process (replace PID)
taskkill /PID <PID> /F

# Or use cleanup script
python scripts/cleanup.py --full
```

#### Issue: Docker containers not starting
**Symptoms:** "Cannot connect to Docker daemon" error
**Solution:**
1. Ensure Docker Desktop is running
2. Check WSL2 integration is enabled in Docker Desktop settings
3. Restart Docker Desktop if necessary

#### Issue: Connection refused from client
**Symptoms:** Client cannot connect to server
**Solution:**
```powershell
# Verify server is running
python scripts/start_lab.py --status

# Check Docker container logs
docker logs week4_demo

# Manual server start with verbose output
python src/apps/text_proto_server.py --verbose
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
│   │  ┌───────────────┐  │     │  │   - Periodic reporting      ││   │
│   │  │  Portainer    │◄─┼─────┼──└─────────────────────────────┘│   │
│   │  │  :9443        │  │     │                                  │   │
│   │  └───────────────┘  │     └─────────────────────────────────┘   │
│   │                     │                                            │
│   └─────────────────────┘                                            │
│                                                                      │
│   Port Mapping:                                                      │
│   • 5400:5400/tcp  → TEXT Protocol Server                           │
│   • 5401:5401/tcp  → BINARY Protocol Server                         │
│   • 5402:5402/udp  → UDP Sensor Server                              │
│   • 9443:9443/tcp  → Portainer Management                           │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

*NETWORKING class - ASE, Informatics | by Revolvix*
