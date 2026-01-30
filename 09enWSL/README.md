# Week 9: Session Layer and Presentation Layer

[![CI Status](https://github.com/antonioclim/netENwsl/actions/workflows/ci.yml/badge.svg)](https://github.com/antonioclim/netENwsl/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-complete-green.svg)](./docs/)
[![Quiz](https://img.shields.io/badge/quiz-15_questions-orange.svg)](./formative/)

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
> 
> by ing. dr. Antonio Clim

---

## 📋 Course Information

| Field | Details |
|-------|---------|
| **Course** | Computer Networks / Rețele de Calculatoare |
| **Programme** | Economic Cybernetics, Year II, Semester I |
| **Institution** | Bucharest University of Economic Studies (ASE) |
| **Faculty** | Cybernetics, Statistics and Economic Informatics (CSIE) |
| **Laboratory** | ing. dr. Antonio Clim |
| **Academic Year** | 2025-2026 |
| **Week** | 9 of 14 |
| **Room** | Networks Laboratory, Virgil Madgearu Building, Floor 2 |
| **Schedule** | Tuesday 14:00-16:00 (Group 1051), Wednesday 10:00-12:00 (Group 1052) |

---

## ⚠️ Environment Notice

This laboratory kit is designed for the **WSL2 + Ubuntu 22.04 + Docker + Portainer** environment.

**Repository:** https://github.com/antonioclim/netENwsl
**This Week's Folder:** `09enWSL`

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
cd /mnt/d/NETWORKING/WEEK9/09enWSL
ls -la
```

---

## 🚀 Quick Start with Makefile

This laboratory includes a Makefile for easy orchestration:

```bash
# Show all available commands
make help

# Setup environment (first time)
make setup

# Start laboratory containers
make start

# Run formative quiz
make quiz

# Run all tests
make test

# Stop laboratory
make stop

# Full cleanup
make clean
```

---


## 🧪 Anti-AI submission workflow

This week includes a small *challenge–evidence–validator* toolkit. It is not an AI detector. Instead it asks you to produce time-bounded, student-specific evidence tied to real network traffic and your own written explanation.

### What you will submit

- One capture file (`.pcap` or `.pcapng`) that contains your **payload token** inside TCP payload on the *challenge-selected control port*
- One short written report (`.md` or `.txt`) that contains your **report token**
- The generated challenge and evidence JSON files

### Step-by-step

1. **Generate your challenge**
   ```bash
   make anti-ai-challenge STUDENT_ID=YOURID
   ```
   This creates:
   - `artifacts/anti_ai/challenge_week09_YOURID.json`

2. **Read your tokens and required port**
   Open the challenge JSON and note:
   - `tokens.payload_token`
   - `tokens.report_token`
   - `constraints.expected_control_port`

3. **Create a tokenised payload file for pseudo-FTP**
   ```bash
   mkdir -p server-files
   echo "PASTE_PAYLOAD_TOKEN_HERE" > server-files/payload.txt
   ```

4. **Capture traffic while transferring the file**
   In terminal A (server):
   ```bash
   python src/exercises/ex_9_02_implement_pseudo_ftp.py server --host 127.0.0.1 --port EXPECTED_PORT --root ./server-files
   ```

   In terminal B (capture, 30 seconds):
   ```bash
   python scripts/capture_traffic.py --port EXPECTED_PORT --duration 30 --output pcap/week09_YOURID.pcapng
   ```

   In terminal C (client):
   ```bash
   python src/exercises/ex_9_02_implement_pseudo_ftp.py client --host 127.0.0.1 --port EXPECTED_PORT --user test --password 12345 get payload.txt
   ```

5. **Write your short report**
   Create a file such as:
   - `artifacts/week09_report_YOURID.md`

   Include at minimum:
   - `Report token: PASTE_REPORT_TOKEN_HERE`
   - A short explanation of what you captured and where the token appears in the stream

6. **Collect evidence and validate locally**
   ```bash
   make anti-ai-evidence STUDENT_ID=YOURID ANTI_AI_PCAP=pcap/week09_YOURID.pcapng ANTI_AI_REPORT=artifacts/week09_report_YOURID.md
   make anti-ai-validate STUDENT_ID=YOURID
   ```

If `make anti-ai-validate` passes, your evidence bundle is internally consistent.


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

### Essential Wireshark Filters for Week 9

| Filter | Purpose |
|--------|---------|
| `tcp.port == 2121` | FTP control channel |
| `tcp.port >= 60000 && tcp.port <= 60010` | FTP passive data channels |
| `tcp.port == 2121 \|\| tcp.port >= 60000` | All FTP traffic |
| `ftp` | FTP commands and responses |
| `ftp.request.command == "USER"` | Authentication requests |
| `ftp.request.command == "PASV"` | Passive mode negotiation |

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

This laboratory explores the upper layers of the OSI model—specifically Layer 5 (Session) and Layer 6 (Presentation)—which provide the crucial bridge between network transport mechanisms and application-level data handling. While often overlooked in favour of more visible protocols, these layers encapsulate essential abstractions for establishing logical communication channels, managing dialogue control and ensuring data representation consistency across heterogeneous systems.

The Session Layer governs the establishment, maintenance and termination of logical connections between communicating processes. Unlike the Transport Layer's focus on reliable byte-stream delivery, the Session Layer introduces higher-order concepts: authentication negotiation, checkpoint synchronisation for long-running transfers and dialogue management (half-duplex versus full-duplex modes). The FTP protocol exemplifies these principles, employing separate control and data channels with explicit session semantics.

The Presentation Layer addresses the fundamental challenge of data heterogeneity: how can systems with different internal representations (big-endian versus little-endian architectures, varying character encodings, distinct serialisation formats) exchange information unambiguously? This layer standardises data encoding through mechanisms such as ASN.1/BER, XDR, JSON and Protocol Buffers, whilst providing compression and encryption services that operate transparently to applications.

## Learning Objectives

By the end of this laboratory session, you will be able to:

1. **Identify** the distinguishing characteristics of connection-oriented transport versus session-based communication, articulating why FTP requires separate control and data channels
2. **Explain** the mechanisms by which the Presentation Layer resolves byte-ordering ambiguity through explicit endianness specification in binary protocols
3. **Implement** a custom binary framing protocol using Python's `struct` module, incorporating length prefixes, message type identifiers and CRC-32 integrity verification
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
- Python 3.10 or later
- Git (recommended for version control)

### Hardware Requirements
- Minimum 8GB RAM (16GB recommended for smooth Docker operation)
- 20GB free disk space
- Network connectivity for initial Docker image pulls

---

## 📁 Laboratory Structure

```
09enWSL/
├── .github/workflows/     # CI/CD pipeline configuration
│   └── ci.yml
├── artifacts/             # Generated outputs (pcap, logs, anti-AI evidence)
├── docker/                # Docker configuration
│   ├── docker-compose.yml
│   ├── configs/
│   └── volumes/
├── docs/                  # Pedagogical documentation
│   ├── learning_objectives.md    # LO traceability matrix
│   ├── theory_summary.md
│   ├── misconceptions.md
│   ├── troubleshooting.md
│   ├── glossary.md
│   ├── parsons_problems.md
│   ├── peer_instruction.md
│   ├── code_tracing.md
│   ├── commands_cheatsheet.md
│   ├── concept_analogies.md
│   ├── further_reading.md
│   ├── pair_programming_guide.md
│   └── CI_SETUP.md               # CI documentation
├── formative/             # Self-assessment quiz
│   ├── quiz.yaml          # YAML format (standalone)
│   ├── quiz_lms.json      # JSON format (Moodle/Canvas)
│   └── run_quiz.py        # Quiz runner
├── anti_ai/               # Anti-AI challenge, evidence collector and validator
├── homework/              # Take-home assignments
│   ├── exercises/
│   └── README.md
├── pcap/                  # Packet captures
├── scripts/               # Automation scripts
├── setup/                 # Environment setup
├── src/                   # Source code
│   ├── exercises/
│   └── utils/
├── tests/                 # Automated tests
├── Makefile               # Orchestration commands
├── pyproject.toml         # Project configuration
└── README.md              # This file
```

---

## 🧪 Exercises Overview

### Exercise 1: Binary Encoding and Endianness (ex_9_01)

Demonstrates Presentation Layer concepts:
- Big-endian vs little-endian byte ordering
- Network byte order conventions
- Binary protocol framing with `struct.pack/unpack`
- CRC-32 integrity verification

```bash
python src/exercises/ex_9_01_demonstrate_endianness.py --selftest --demo
```

### Exercise 2: Pseudo-FTP Protocol (ex_9_02)

Implements a simplified FTP-like protocol:
- Session state machine (authentication, commands)
- Binary message framing
- Multi-client server architecture

```bash
python src/exercises/ex_9_02_implement_pseudo_ftp.py --help
```

### Exercise 3: FTP Client Demo (ex_9_03)

Interactive FTP client for testing:
- Connection and authentication
- Directory listing and file transfer
- Passive mode negotiation

```bash
python src/exercises/ex_9_03_ftp_client_demo.py --host localhost --port 2121
```

### Exercise 4: FTP Server Demo (ex_9_04)

Python-based FTP server:
- pyftpdlib integration
- Multi-client support
- Passive port configuration

```bash
python src/exercises/ex_9_04_ftp_server_demo.py --help
```

---

## 📊 Network Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     Week 9 Laboratory Architecture                       │
│                        (172.29.9.0/24 Network)                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────────┐                                                   │
│  │                  │      Control Channel (2121)                       │
│  │   FTP Server     │◄────────────────────────────────┐                │
│  │   (pyftpdlib)    │      Passive Data (60000-60010) │                │
│  │   172.29.9.x     │◄─────────────────────┐          │                │
│  │                  │                      │          │                │
│  └──────────────────┘                      │          │                │
│           │                                │          │                │
│           │ Shared Volume                  │          │                │
│           │ (server-files)                 │          │                │
│           ▼                                │          │                │
│  ┌──────────────────┐                 ┌────┴───────┐  │                │
│  │   /srv/ftp/      │                 │            │  │                │
│  │   - test_file.txt│                 │   Client 1 │  │                │
│  │   - sample_data/ │                 │   (LIST)   ├──┘                │
│  └──────────────────┘                 │   172.29.9.x                   │
│                                       └────────────┘                   │
│                                                                         │
│                                       ┌────────────┐                   │
│  ┌──────────────────┐                 │            │                   │
│  │  Host Machine    │                 │   Client 2 │                   │
│  │  (Windows/WSL2)  │◄───Wireshark───►│   (GET)    │                   │
│  │  localhost:2121  │    Capture      │   172.29.9.x                   │
│  └──────────────────┘                 └────────────┘                   │
│                                                                         │
│  Portainer: http://localhost:9000 (global service)                      │
│  Credentials: stud / studstudstud                                       │
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
cd /mnt/d/NETWORKING/WEEK9/09enWSL
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

## ❓ Frequently Asked Questions (FAQ)

### Q: Why do we use port 2121 instead of 21 for FTP?

**A:** Ports below 1024 require root/administrator privileges. By using 2121, students can run the laboratory without `sudo`. In production environments, FTP uses port 21.

### Q: Can I use this kit on macOS?

**A:** Yes, with Docker Desktop for Mac. Replace WSL commands with native terminal. Wireshark works identically on macOS.

### Q: Why do containers stop after I finish the exercise?

**A:** Client containers are configured to run a single command and exit (intentional design). The server remains active for reconnections.

### Q: How do I save a PCAP from inside a container?

**A:** Use `docker cp`:
```bash
docker exec s9_ftp_server tcpdump -c 100 -w /tmp/capture.pcap -i eth0
docker cp s9_ftp_server:/tmp/capture.pcap ./pcap/my_capture.pcap
```

### Q: Can I modify the source code for experiments?

**A:** Absolutely! Experimentation is encouraged. Make a backup first:
```bash
cp src/exercises/ex_9_01_demonstrate_endianness.py src/exercises/ex_9_01_demonstrate_endianness.py.bak
```

### Q: Why does the quiz have both YAML and JSON formats?

**A:** YAML is human-readable and used by the standalone Python runner. JSON is for LMS import (Moodle, Canvas). Both contain identical questions.

### Q: How do I run the formative quiz?

**A:** Multiple options:
```bash
# Interactive mode
make quiz

# Or directly
python formative/run_quiz.py

# Filter by learning objective
python formative/run_quiz.py --lo LO2

# Export statistics
python formative/run_quiz.py --stats
```

### Q: What if I encounter issues not covered in troubleshooting?

**A:** Open an issue on GitHub: https://github.com/antonioclim/netENwsl/issues

---

## 📚 Additional Resources

- **Learning Objectives:** `docs/learning_objectives.md`
- **Theory Summary:** `docs/theory_summary.md`
- **Common Misconceptions:** `docs/misconceptions.md`
- **Command Cheatsheet:** `docs/commands_cheatsheet.md`
- **Further Reading:** `docs/further_reading.md`
- **Formative Quiz:** `formative/quiz.yaml`
- **CI Setup Guide:** `docs/CI_SETUP.md`

---

## 🤝 Support

- **Issues:** Open an issue on GitHub: https://github.com/antonioclim/netENwsl/issues
- **Course Forum:** Moodle ASE → Computer Networks 2025-2026
- **Office Hours:** Check course schedule on Moodle

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
*Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment*
*Week 9: Session Layer and Presentation Layer*
