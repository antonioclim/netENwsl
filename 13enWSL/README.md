# Week 13: IoT and Security in Computer Networks

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
> 
> by Revolvix

## Overview

This laboratory session explores the intersection of Internet of Things (IoT) technologies and network security fundamentals. The proliferation of IoT devices in enterprise and consumer environments has introduced novel attack surfaces that demand systematic understanding of both offensive reconnaissance techniques and defensive countermeasures.

The practical focus encompasses MQTT (Message Queuing Telemetry Transport) as the predominant IoT messaging protocol, examining the security implications of plaintext versus TLS-encrypted communications. Students will conduct controlled port scanning and service enumeration exercises against intentionally vulnerable targets, developing the analytical skills necessary to interpret reconnaissance outputs and correlate findings with potential security exposures.

This kit provides a reproducible Docker-based laboratory environment featuring vulnerable services (DVWA, vsftpd with simulated backdoor) and an MQTT broker configured for both secure and insecure transport modes. All exercises operate within isolated network segments to ensure safe experimentation without external impact.

## Learning Objectives

By the end of this laboratory session, you will be able to:

1. **Recall** the fundamental components of MQTT architecture including brokers, publishers, subscribers and topic hierarchies
2. **Explain** the differences between plaintext and TLS-encrypted network communications and what metadata remains observable under encryption
3. **Implement** TCP connect scanning using concurrent programming techniques and interpret the resulting port states (open, closed, filtered)
4. **Demonstrate** MQTT publish/subscribe operations using Python client libraries with both plaintext and TLS transport configurations
5. **Analyse** packet captures to distinguish between encrypted and unencrypted traffic flows and identify protocol-specific patterns
6. **Design** a systematic reconnaissance workflow that combines service enumeration, banner grabbing and vulnerability fingerprinting
7. **Evaluate** the security posture of network services based on exposed ports, protocol versions and known vulnerability indicators

## Prerequisites

### Knowledge Requirements
- Understanding of TCP/IP networking fundamentals (Weeks 1-6)
- Familiarity with socket programming concepts (Weeks 2-3)
- Basic knowledge of Docker containerisation (Weeks 10-11)
- Understanding of cryptographic transport (TLS basics from Week 8)

### Software Requirements
- Windows 10/11 with WSL2 enabled
- Docker Desktop (WSL2 backend)
- Wireshark (native Windows installation)
- Python 3.11 or later
- Git (recommended)

### Hardware Requirements
- Minimum 8GB RAM (16GB recommended)
- 10GB free disk space
- Network connectivity (for initial setup only)

## Quick Start

### First-Time Setup (Run Once)

```powershell
# Open PowerShell as Administrator
cd WEEK13_WSLkit

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
| DVWA | http://localhost:8080 | admin / password (after setup) |
| MQTT Broker (plain) | localhost:1883 | None required |
| MQTT Broker (TLS) | localhost:8883 | Requires CA certificate |
| vsftpd | localhost:2121 | Anonymous |
| Backdoor Stub | localhost:6200 | Educational stub only |

## Laboratory Exercises

### Exercise 1: TCP Port Scanning and Service Enumeration

**Objective:** Implement and execute a concurrent TCP connect scanner to enumerate open ports and identify running services on target hosts.

**Duration:** 45 minutes

**Steps:**

1. Review the port scanner implementation in `src/exercises/ex_13_01_port_scanner.py`
2. Start the laboratory environment if not already running:
   ```powershell
   python scripts/start_lab.py
   ```
3. Execute a scan against the laboratory network:
   ```powershell
   python src/exercises/ex_13_01_port_scanner.py --target 127.0.0.1 --ports 1-1024
   ```
4. Perform a targeted scan of known service ports:
   ```powershell
   python src/exercises/ex_13_01_port_scanner.py --target 127.0.0.1 --ports 21,80,1883,2121,6200,8080,8883 --json-out artifacts/scan_results.json
   ```
5. Analyse the JSON output and correlate discovered ports with expected services
6. Experiment with different timeout and worker configurations to observe performance trade-offs

**Verification:**
```powershell
python tests/test_exercises.py --exercise 1
```

**Expected Observations:**
- Ports 1883, 2121, 6200, 8080 and 8883 should report as OPEN
- Banner grabbing should reveal service identifiers for FTP and HTTP
- Closed ports return immediately whilst filtered ports timeout

---

### Exercise 2: MQTT Publish/Subscribe with Plaintext and TLS

**Objective:** Establish MQTT communications using both plaintext and TLS-encrypted transport, then compare the observable traffic patterns.

**Duration:** 40 minutes

**Steps:**

1. Open two terminal windows for publisher and subscriber operations
2. In Terminal 1, start an MQTT subscriber (plaintext):
   ```powershell
   python src/exercises/ex_13_02_mqtt_client.py --broker 127.0.0.1 --port 1883 --mode subscribe --topic "iot/sensors/#" --timeout 60
   ```
3. In Terminal 2, publish messages:
   ```powershell
   python src/exercises/ex_13_02_mqtt_client.py --broker 127.0.0.1 --port 1883 --mode publish --topic "iot/sensors/temperature" --message '{"sensor":"temp01","value":23.5,"unit":"C"}' --count 5
   ```
4. Observe the subscriber receiving the published messages
5. Repeat the exercise using TLS transport (port 8883 with CA certificate):
   ```powershell
   python src/exercises/ex_13_02_mqtt_client.py --broker 127.0.0.1 --port 8883 --mode subscribe --topic "iot/sensors/#" --timeout 60 --tls --cafile docker/configs/certs/ca.crt
   ```
6. Capture network traffic during both plaintext and TLS sessions for comparison in Exercise 3

**Verification:**
```powershell
python tests/test_exercises.py --exercise 2
```

**Expected Observations:**
- Subscriber receives all published messages in both modes
- QoS 0 provides at-most-once delivery semantics
- TLS connection requires valid CA certificate for verification

---

### Exercise 3: Network Traffic Analysis and Protocol Inspection

**Objective:** Capture and analyse network traffic to distinguish between plaintext and encrypted MQTT communications, identifying observable metadata in each scenario.

**Duration:** 35 minutes

**Steps:**

1. Start a packet capture targeting laboratory ports:
   ```powershell
   python scripts/capture_traffic.py --interface any --output pcap/mqtt_comparison.pcap --duration 120
   ```
2. In parallel terminals, generate both plaintext and TLS MQTT traffic as per Exercise 2
3. Stop the capture after generating sufficient traffic
4. Open the capture file in Wireshark (Windows native):
   - Apply filter: `tcp.port == 1883`
   - Examine plaintext MQTT packets and identify topic names, message payloads
   - Apply filter: `tcp.port == 8883`
   - Observe TLS handshake and encrypted application data
5. Document your findings regarding:
   - What information is visible in plaintext mode
   - What information remains observable even with TLS (endpoints, timing, sizes)
   - The TLS handshake sequence and cipher negotiation

**Verification:**
```powershell
python tests/test_exercises.py --exercise 3
```

**Expected Observations:**
- Plaintext MQTT traffic reveals topic strings, payload content and client identifiers
- TLS traffic shows handshake packets followed by encrypted Application Data
- Metadata (IP addresses, ports, packet timing, approximate sizes) remains observable regardless of encryption

---

### Exercise 4: Vulnerability Assessment and Defensive Checks

**Objective:** Conduct systematic vulnerability assessment against laboratory services using defensive fingerprinting techniques, interpreting findings in a security context.

**Duration:** 30 minutes

**Steps:**

1. Run the vulnerability checker against DVWA:
   ```powershell
   python src/exercises/ex_13_04_vuln_checker.py --target 127.0.0.1 --port 8080 --service http --json-out artifacts/vuln_dvwa.json
   ```
2. Run the checker against the FTP service:
   ```powershell
   python src/exercises/ex_13_04_vuln_checker.py --target 127.0.0.1 --port 2121 --service ftp --json-out artifacts/vuln_ftp.json
   ```
3. Run the checker against the MQTT broker:
   ```powershell
   python src/exercises/ex_13_04_vuln_checker.py --target 127.0.0.1 --port 1883 --service mqtt --json-out artifacts/vuln_mqtt.json
   ```
4. Review the JSON reports and interpret the severity ratings
5. Execute the educational FTP backdoor detection script:
   ```powershell
   python src/apps/ftp_backdoor_check.py --target 127.0.0.1 --ftp-port 2121 --backdoor-port 6200
   ```
6. Document findings and discuss the implications of each discovered issue

**Verification:**
```powershell
python tests/test_exercises.py --exercise 4
```

**Expected Observations:**
- DVWA is fingerprinted as an intentionally vulnerable web application
- vsftpd banner may indicate version information useful for CVE correlation
- The backdoor stub port (6200) demonstrates detection of unexpected exposed services

## Demonstrations

### Demo 1: Full Automated Laboratory Run

This demonstration executes the complete laboratory workflow in automated fashion, suitable for projector display.

```powershell
python scripts/run_demo.py --demo 1
```

**What to observe:**
- Service startup sequence and health verification
- Sequential execution of port scanning, MQTT messaging and vulnerability checks
- Artefact generation in the `artifacts/` directory
- Summary report with pass/fail indicators

### Demo 2: Plaintext vs TLS Traffic Comparison

Side-by-side demonstration of observable differences between encrypted and unencrypted communications.

```powershell
python scripts/run_demo.py --demo 2
```

**What to observe:**
- Wireshark capture showing MQTT payload in plaintext
- Same capture showing TLS Application Data records
- Timing correlation between publish operations and packet flows

### Demo 3: Reconnaissance Pipeline

Demonstration of a systematic reconnaissance workflow from discovery to vulnerability assessment.

```powershell
python scripts/run_demo.py --demo 3
```

**What to observe:**
- Host discovery phase identifying active services
- Port enumeration with service fingerprinting
- Vulnerability correlation based on banner analysis
- Structured report generation

## Packet Capture and Analysis

### Capturing Traffic

```powershell
# Start capture with Python helper
python scripts/capture_traffic.py --interface any --output pcap/week13_capture.pcap --duration 60

# Alternative: use Wireshark directly
# Open Wireshark > Select appropriate interface > Start capture
```

### Suggested Wireshark Filters

```
# MQTT plaintext traffic
tcp.port == 1883

# MQTT over TLS
tcp.port == 8883 and tls

# FTP control channel
tcp.port == 2121

# HTTP to DVWA
tcp.port == 8080

# All laboratory traffic
tcp.port in {1883, 2121, 6200, 8080, 8883}

# MQTT PUBLISH packets (plaintext only)
mqtt.msgtype == 3

# TLS handshake packets
tls.handshake
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
# Remove all containers, networks and volumes for this week
python scripts/cleanup.py --full

# Verify cleanup
docker system df
```

## Homework Assignments

See the `homework/` directory for take-home exercises.

### Assignment 1: Extended Port Scanner
Extend the port scanner to support UDP scanning and implement service detection heuristics beyond banner grabbing. Document the challenges of UDP scanning compared to TCP.

### Assignment 2: MQTT Security Analysis
Write a brief report (500-750 words) analysing the security implications of running MQTT without TLS in an IoT deployment. Include specific attack scenarios and mitigation recommendations.

## Troubleshooting

### Common Issues

#### Issue: Docker containers fail to start
**Solution:** Ensure Docker Desktop is running and WSL2 integration is enabled. Try `docker info` to verify connectivity. If permission errors occur, run PowerShell as Administrator.

#### Issue: MQTT TLS connection fails with certificate error
**Solution:** Verify that certificates were generated during setup. Run `python setup/configure_docker.py --regenerate-certs` to create new certificates. Ensure the CA certificate path in commands matches `docker/configs/certs/ca.crt`.

#### Issue: Port scanner reports all ports as filtered
**Solution:** This typically indicates a firewall blocking connections. Ensure Docker network is configured correctly and containers are running. Verify with `docker ps` and check container health.

#### Issue: Wireshark cannot capture Docker traffic
**Solution:** On Windows, capture on the `vEthernet (WSL)` adapter or use the `any` pseudo-interface within WSL. Alternatively, capture from within containers using tcpdump.

See `docs/troubleshooting.md` for additional solutions.

## Theoretical Background

### MQTT Protocol Fundamentals

MQTT (Message Queuing Telemetry Transport) is a lightweight publish/subscribe messaging protocol designed for constrained devices and low-bandwidth networks. The architecture comprises:

- **Broker**: Central server that receives all messages and routes them to appropriate subscribers
- **Publishers**: Clients that send messages to specific topics
- **Subscribers**: Clients that register interest in topics and receive matching messages
- **Topics**: Hierarchical namespace strings (e.g., `sensors/building1/temperature`) supporting wildcards (`+` single level, `#` multi-level)

Quality of Service (QoS) levels define delivery guarantees:
- QoS 0: At most once (fire and forget)
- QoS 1: At least once (acknowledged delivery)
- QoS 2: Exactly once (four-part handshake)

### Transport Layer Security in IoT

TLS provides confidentiality, integrity and authentication for network communications. In IoT contexts:

- **Confidentiality**: Encrypts payload content preventing eavesdropping
- **Integrity**: Detects tampering through message authentication codes
- **Authentication**: Verifies server identity (optionally client identity)

However, TLS does not conceal:
- Endpoint IP addresses and ports
- Connection timing and duration
- Approximate message sizes
- Traffic patterns and frequencies

### Port Scanning Methodology

TCP connect scanning establishes full connections to determine port states:

- **Open**: Three-way handshake completes successfully
- **Closed**: RST packet received in response to SYN
- **Filtered**: No response (packet dropped by firewall)

Ethical considerations require explicit authorisation before scanning systems outside controlled laboratory environments.

## References

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (7th ed.). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming* (3rd ed.). Apress.
- OASIS Standard. (2019). *MQTT Version 5.0*. OASIS.
- Banks, A. & Gupta, R. (2014). *MQTT Version 3.1.1*. OASIS Standard.
- Stallings, W. (2017). *Cryptography and Network Security* (7th ed.). Pearson.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    WEEK 13 Laboratory Network                        │
│                        10.0.13.0/24                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ┌─────────────────┐    ┌─────────────────┐    ┌────────────────┐  │
│   │   Mosquitto     │    │      DVWA       │    │    vsftpd      │  │
│   │   MQTT Broker   │    │  (Vulnerable)   │    │  (Vulnerable)  │  │
│   │                 │    │                 │    │                │  │
│   │  10.0.13.100    │    │   10.0.13.11    │    │  10.0.13.12    │  │
│   │                 │    │                 │    │                │  │
│   │  :1883 (plain)  │    │   :80 (HTTP)    │    │  :21 (FTP)     │  │
│   │  :8883 (TLS)    │    │                 │    │  :6200 (stub)  │  │
│   └────────┬────────┘    └────────┬────────┘    └───────┬────────┘  │
│            │                      │                      │          │
│            └──────────────────────┼──────────────────────┘          │
│                                   │                                  │
│                        ┌──────────┴──────────┐                      │
│                        │   Docker Network    │                      │
│                        │    (week13net)      │                      │
│                        └──────────┬──────────┘                      │
│                                   │                                  │
├───────────────────────────────────┼──────────────────────────────────┤
│                          Host Ports                                  │
│                                                                      │
│   localhost:1883 ──────────────── MQTT Plain                        │
│   localhost:8883 ──────────────── MQTT TLS                          │
│   localhost:8080 ──────────────── DVWA HTTP                         │
│   localhost:2121 ──────────────── vsftpd FTP                        │
│   localhost:6200 ──────────────── Backdoor Stub                     │
│   localhost:9443 ──────────────── Portainer (optional)              │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

*NETWORKING class - ASE, Informatics | by Revolvix*
