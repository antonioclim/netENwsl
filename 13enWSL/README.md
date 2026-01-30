# Week 13: IoT and Security in Computer Networks

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
> 
> by Revolvix

---

## ⚠️ Environment Notice

This laboratory kit is designed for the **WSL2 + Ubuntu 22.04 + Docker + Portainer** environment.

**Repository:** https://github.com/antonioclim/netENwsl
**This Week's Folder:** `13enWSL`

| Component | Details |
|-----------|---------|
| Windows | Windows 10/11 with WSL2 enabled |
| Linux Distribution | Ubuntu 22.04 LTS (default WSL distro) |
| Container Runtime | Docker Engine (in WSL) |
| Management Interface | Portainer CE on port 9000 (global) |
| Packet Analysis | Wireshark (native Windows application) |

**SECURITY WARNING:** This kit includes intentionally vulnerable services for educational purposes. Do not expose to public networks!

---

## 📥 Cloning This Week's Laboratory

### Step 1: Open PowerShell (Windows)

Press `Win + X` → Select "Windows Terminal" or "PowerShell"

### Step 2: Clone the Repository

```powershell
# Create networking folder if it doesn't exist
mkdir D:\NETWORKING -ErrorAction SilentlyContinue
cd D:\NETWORKING

# Clone Week 13
git clone https://github.com/antonioclim/netENwsl.git WEEK13
cd WEEK13
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
git clone https://github.com/antonioclim/netENwsl.git WEEK13
cd WEEK13
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

Open browser and go to: **http://localhost:9000**

**Login credentials:**
- Username: `stud`
- Password: `studstudstud`

### Step 4: Go to Laboratory Directory

```bash
cd /mnt/d/NETWORKING/WEEK13/13enWSL
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

### Week 13 Network Configuration

Go to: **Networks → week13net**

Current configuration:
- Subnet: 10.0.13.0/24
- Gateway: 10.0.13.1
- Mosquitto MQTT: 10.0.13.100
- DVWA: 10.0.13.11
- vsftpd: 10.0.13.12

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

### Essential Wireshark Filters for Week 13

| Filter | Purpose |
|--------|---------|
| `tcp.port == 1883` | MQTT plaintext traffic |
| `tcp.port == 8883 and tls` | MQTT over TLS |
| `tcp.port == 2121` | FTP control channel |
| `tcp.port == 8080` | HTTP to DVWA |
| `tcp.port == 6200` | Backdoor stub port |
| `tcp.port in {1883, 2121, 6200, 8080, 8883}` | All Week 13 traffic |
| `mqtt.msgtype == 3` | MQTT PUBLISH packets (plaintext only) |
| `tls.handshake` | TLS handshake packets |

### Analysing IoT Security Traffic

1. **Plaintext MQTT**: Filter `tcp.port == 1883`, follow TCP stream to see topics and payloads
2. **TLS MQTT**: Filter `tcp.port == 8883`, observe encrypted Application Data records
3. **Vulnerability Scanning**: Filter by target port to see connection attempts

### Saving Captures

1. **File → Save As**
2. Go to: `D:\NETWORKING\WEEK13\pcap\`
3. Filename: `capture_mqtt.pcap` or `capture_scan.pcap`

---

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
- Docker Engine (in WSL)
- Portainer CE (running globally on port 9000)
- Wireshark (native Windows installation)
- Python 3.11 or later
- Git (recommended)

### Hardware Requirements
- Minimum 8GB RAM (16GB recommended)
- 10GB free disk space
- Network connectivity (for initial setup only)


## Anti-AI assessed submission workflow (optional)

If your instructor enables the anti-AI workflow for Week 13 you will submit a small package that
can be validated automatically. The design goal is simple: AI tools may help you understand and
debug but they are not sufficient on their own because the submission must include execution
artefacts tied to your environment.

**What you submit (typical):**
- a per-student `challenge_*.yaml`
- a security audit report JSON that contains a challenge token
- a PCAP capture that contains a unique MQTT payload token on port 1883
- (optionally required) a TLS handshake capture on port 8883
- an `evidence_*.json` file with SHA256 hashes for integrity

**Workflow:**

```bash
# 1) Issue a challenge
make anti-ai-challenge STUDENT_ID=<your_id>

# 2) Generate probe traffic (capture this in Wireshark or via scripts/capture_traffic.py)
python3 scripts/anti_ai_run_week13_probes.py --challenge "$ANTI_AI_CHALLENGE" --tls

# 3) Produce the security audit report (token is embedded automatically when --challenge is used)
python3 homework/exercises/hw_13_02_security_audit.py \
  --challenge "$ANTI_AI_CHALLENGE" \
  --output "$ANTI_AI_REPORT"

# 4) Generate evidence and validate locally
make anti-ai-evidence STUDENT_ID=<your_id>
make anti-ai-validate STUDENT_ID=<your_id>
```

If validation fails read the error message carefully as it will point to the missing or invalid
artefact.

## Quick Start

### First-Time Setup (Run Once)

```bash
# Open Ubuntu terminal (WSL)
wsl

# Go to the kit directory
cd /mnt/d/NETWORKING/WEEK13/13enWSL

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
   ```bash
   python3 scripts/start_lab.py
   ```
3. Execute a scan against the laboratory network:
   ```bash
   python3 src/exercises/ex_13_01_port_scanner.py --target 127.0.0.1 --ports 1-1024
   ```
4. Perform a targeted scan of known service ports:
   ```bash
   python3 src/exercises/ex_13_01_port_scanner.py --target 127.0.0.1 --ports 21,80,1883,2121,6200,8080,8883 --json-out artifacts/scan_results.json
   ```
5. Analyse the JSON output and correlate discovered ports with expected services
6. Experiment with different timeout and worker configurations to observe performance trade-offs

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 1
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
   ```bash
   python3 src/exercises/ex_13_02_mqtt_client.py --broker 127.0.0.1 --port 1883 --mode subscribe --topic "iot/sensors/#" --timeout 60
   ```
3. In Terminal 2, publish messages:
   ```bash
   python3 src/exercises/ex_13_02_mqtt_client.py --broker 127.0.0.1 --port 1883 --mode publish --topic "iot/sensors/temperature" --message '{"sensor":"temp01","value":23.5,"unit":"C"}' --count 5
   ```
4. Observe the subscriber receiving the published messages
5. Repeat the exercise using TLS transport (port 8883 with CA certificate):
   ```bash
   python3 src/exercises/ex_13_02_mqtt_client.py --broker 127.0.0.1 --port 8883 --mode subscribe --topic "iot/sensors/#" --timeout 60 --tls --cafile docker/configs/certs/ca.crt
   ```
6. Capture network traffic during both plaintext and TLS sessions for comparison in Exercise 3

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 2
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
   ```bash
   python3 scripts/capture_traffic.py --interface any --output pcap/mqtt_comparison.pcap --duration 120
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
```bash
python3 tests/test_exercises.py --exercise 3
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
   ```bash
   python3 src/exercises/ex_13_04_vuln_checker.py --target 127.0.0.1 --port 8080 --service http --json-out artifacts/vuln_dvwa.json
   ```
2. Run the checker against the FTP service:
   ```bash
   python3 src/exercises/ex_13_04_vuln_checker.py --target 127.0.0.1 --port 2121 --service ftp --json-out artifacts/vuln_ftp.json
   ```
3. Run the checker against the MQTT broker:
   ```bash
   python3 src/exercises/ex_13_04_vuln_checker.py --target 127.0.0.1 --port 1883 --service mqtt --json-out artifacts/vuln_mqtt.json
   ```
4. Review the JSON reports and interpret the severity ratings
5. Execute the educational FTP backdoor detection script:
   ```bash
   python3 src/apps/ftp_backdoor_check.py --target 127.0.0.1 --ftp-port 2121 --backdoor-port 6200
   ```
6. Document findings and discuss the implications of each discovered issue

**Verification:**
```bash
python3 tests/test_exercises.py --exercise 4
```

**Expected Observations:**
- DVWA is fingerprinted as an intentionally vulnerable web application
- vsftpd banner may indicate version information useful for CVE correlation
- The backdoor stub port (6200) demonstrates detection of unexpected exposed services

## Demonstrations

### Demo 1: Full Automated Laboratory Run

This demonstration executes the complete laboratory workflow in automated fashion, suitable for projector display.

```bash
python3 scripts/run_demo.py --demo 1
```

**What to observe:**
- Service startup sequence and health verification
- Sequential execution of port scanning, MQTT messaging and vulnerability checks
- Artefact generation in the `artifacts/` directory
- Summary report with pass/fail indicators

### Demo 2: Plaintext vs TLS Traffic Comparison

Side-by-side demonstration of observable differences between encrypted and unencrypted communications.

```bash
python3 scripts/run_demo.py --demo 2
```

**What to observe:**
- Wireshark capture showing MQTT payload in plaintext
- Same capture showing TLS Application Data records
- Timing correlation between publish operations and packet flows

### Demo 3: Reconnaissance Pipeline

Demonstration of a systematic reconnaissance workflow from discovery to vulnerability assessment.

```bash
python3 scripts/run_demo.py --demo 3
```

**What to observe:**
- Host discovery phase identifying active services
- Port enumeration with service fingerprinting
- Vulnerability correlation based on banner analysis
- Structured report generation

## Packet Capture and Analysis

### Capturing Traffic

```bash
# Start capture with Python helper
python3 scripts/capture_traffic.py --interface any --output pcap/week13_capture.pcap --duration 60

# Alternative: use Wireshark directly
# Open Wireshark > Select vEthernet (WSL) interface > Start capture
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

```bash
# Stop all containers (Portainer stays running!)
python3 scripts/stop_lab.py

# Verify shutdown
docker ps
```

### Full Cleanup (Before Next Week)

```bash
# Remove all containers, networks and volumes for this week
python3 scripts/cleanup.py --full

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
**Solution:** Ensure Docker is running in WSL. Try `docker info` to verify connectivity. If permission errors occur, check group membership with `groups` command.

#### Issue: MQTT TLS connection fails with certificate error
**Solution:** Verify that certificates were generated during setup. Run `python3 setup/configure_docker.py --regenerate-certs` to create new certificates. Ensure the CA certificate path in commands matches `docker/configs/certs/ca.crt`.

#### Issue: Port scanner reports all ports as filtered
**Solution:** This typically indicates a firewall blocking connections. Ensure Docker network is configured correctly and containers are running. Verify with `docker ps` and check container health.

#### Issue: Wireshark cannot capture Docker traffic
**Solution:** On Windows, capture on the `vEthernet (WSL)` adapter. Alternatively, capture from within containers using tcpdump.

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

## 📚 Pedagogical Resources

This laboratory kit includes several resources designed to support effective learning:

### For Students

| Resource | Purpose | Location |
|----------|---------|----------|
| **Concept Analogies** | Understand new concepts through everyday comparisons | `docs/concept_analogies.md` |
| **Glossary** | Quick reference for Week 13 terminology | `docs/glossary.md` |
| **Code Tracing** | Practice predicting code behaviour | `docs/code_tracing.md` |
| **Parsons Problems** | Reinforce code structure understanding | `docs/parsons_problems.md` |
| **Misconceptions** | Common errors and how to avoid them | `docs/misconceptions.md` |

### For Pair Programming

This laboratory is designed for **pair programming**. See `docs/pair_programming_guide.md` for:
- Role definitions (Driver/Navigator)
- Structured exercises with swap points
- Communication phrases
- Troubleshooting together

**Recommended workflow:**
1. Read the exercise objectives together
2. Predict outcomes before running code
3. Swap roles every 10-15 minutes
4. Both partners should be able to explain the solution

### For Self-Assessment

Use the Peer Instruction questions in `docs/peer_instruction.md` to test your understanding. Each question targets a common misconception about IoT, MQTT or network security.

---

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
│              (WSL2 + Ubuntu 22.04 + Docker + Portainer)             │
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
│   localhost:9000 ──────────────── Portainer (global service)        │
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
docker network inspect week13net

# Check DNS in container
docker exec week13_mosquitto cat /etc/resolv.conf
```

**Problem:** Port already in use
```bash
# Find what's using the port
sudo netstat -tlnp | grep 1883
# Or
sudo ss -tlnp | grep 1883

# Kill the process or use different port
```

### Security Lab-Specific Issues

**Problem:** DVWA not loading after container start
```bash
# Check container logs
docker logs week13_dvwa
# May need to wait for database initialisation
```

**Problem:** MQTT client can't connect with TLS
```bash
# Verify certificate exists
ls -la docker/configs/certs/
# Regenerate if missing
python3 setup/configure_docker.py --regenerate-certs
```

---

## 🧹 Complete Cleanup Procedure

### End of Session (Quick)

```bash
# Stop lab containers (Portainer stays running!)
cd /mnt/d/NETWORKING/WEEK13/13enWSL
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

## 📊 Week 13 Network Configuration Summary

| Resource | Value | Notes |
|----------|-------|-------|
| Network Subnet | 10.0.13.0/24 | week13net |
| Gateway | 10.0.13.1 | Docker bridge |
| Mosquitto MQTT | 10.0.13.100 | Ports 1883 (plain), 8883 (TLS) |
| DVWA | 10.0.13.11 | Port 8080 (HTTP) |
| vsftpd | 10.0.13.12 | Ports 2121 (FTP), 6200 (stub) |
| Portainer | 9000 | **RESERVED - Global service** |

---

*NETWORKING class - ASE, Informatics | by Revolvix*
*Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment*
