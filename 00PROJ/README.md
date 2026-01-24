# 00PROJ — Computer Networks Projects

> **Course:** Computer Networks (Rețele de Calculatoare)  
> **Programme:** Economic Informatics, Year 3, Semester 2  
> **Institution:** ASE Bucharest - CSIE  
> **Version:** 2.0 (Enhanced)  
> **Last Update:** January 2026

---

## 📋 Overview

This archive contains specifications for **20 network programming projects** designed for the Computer Networks course. Each project applies concepts from laboratory work to build practical network applications.

### Archive Contents

```
00PROJ/
├── README.md                    # This file
├── docs/
│   └── common/                  # Shared guides (5 files)
│       ├── code_quality_standards.md
│       ├── git_workflow_detailed.md
│       ├── pair_programming_guide.md
│       ├── presentation_guide.md
│       └── troubleshooting_common.md
├── PROJECTS/                    # Main projects (15 files)
│   ├── P01_SDN_Firewall_Mininet.md
│   ├── P02-P05...
│   └── P06-P15...
├── RESERVE_individual/          # Reserve projects (5 files)
│   └── P16-P20...
├── templates/                   # Starter kits and templates
│   ├── PROJECT_TEMPLATE.md
│   └── starter_kit/
└── learning_objectives_matrix.md
```

---

## 🗺️ Navigation Map

### By Difficulty Level

| Level | Projects | Description |
|-------|----------|-------------|
| ★★☆☆☆ | P10, P16, P17 | Beginner-friendly |
| ★★★☆☆ | P06, P07, P08, P09, P12, P15, P18 | Intermediate |
| ★★★★☆ | P01, P02, P03, P04, P05, P11, P13, P14, P19, P20 | Advanced |

### By Technology Stack

| Technology | Projects |
|------------|----------|
| **SDN/Mininet** | [P01](PROJECTS/P01_SDN_Firewall_Mininet.md), [P06](PROJECTS/P06_SDN_Mininet_Controller_OpenFlow.md), [P11](PROJECTS/P11_Advanced_SDN_Mininet_OpenFlow.md) |
| **Security/IDS** | [P03](PROJECTS/P03_IDS_Traffic_Monitoring_Python.md), [P07](PROJECTS/P07_Firewall_IDS_Traffic_Monitoring.md), [P14](PROJECTS/P14_Security_IDS_IPS_Simulation.md) |
| **Docker** | [P10](PROJECTS/P10_Docker_Network_Configuration.md), [P12](PROJECTS/P12_Docker_Microservices_Load_Balancing.md) |
| **Web/HTTP** | [P08](PROJECTS/P08_Web_Server_Reverse_Proxy.md) |
| **File Transfer** | [P09](PROJECTS/P09_Multi_Client_FTP_Server.md) |
| **RPC/Protocols** | [P04](PROJECTS/P04_Secure_Communication_Channel.md), [P13](PROJECTS/P13_RPC_gRPC_Service.md) |
| **IoT/MQTT** | [P15](PROJECTS/P15_MQTT_IoT_Client_Server.md), [P20](RESERVE_individual/P20_Reserve.md) |
| **Analysis** | [P05](PROJECTS/P05_Traffic_Generation_Analysis.md), [P16](RESERVE_individual/P16_Network_Traffic_Analyzer.md) |

### By Laboratory Week Reference

| Week | Lab Topic | Related Projects |
|------|-----------|------------------|
| 2 | Socket Programming | P04, P08, P09 |
| 6 | SDN Architecture | P01, P06, P11 |
| 7 | Packet Capture | P03, P07, P14, P16 |
| 8 | HTTP Protocol | P08, P12 |
| 10 | Docker Networking | P10, P12 |
| 12 | RPC | P13 |
| 13 | MQTT/IoT | P15, P20 |
| 14 | Security | P03, P07, P14, P19 |

---

## 📅 Project Timeline

| Stage | Week | Deadline | Deliverables | Weight |
|-------|------|----------|--------------|--------|
| **E1** - Design | 5 | Week 5 | Specifications + Diagrams | 20% |
| **E2** - Prototype | 9 | Week 9 | Partial implementation | 25% |
| **E3** - Final | 13 | Week 13 | Complete + Tests + Docs | 35% |
| **E4** - Presentation | 14 | Week 14 | Live demo + Defence | 20% |

---

## 📚 Essential Guides

Before starting, read these guides:

| Guide | Purpose | Required Reading |
|-------|---------|-----------------|
| [Code Quality Standards](docs/common/code_quality_standards.md) | Python code requirements | **MANDATORY** |
| [Git Workflow](docs/common/git_workflow_detailed.md) | Version control process | **MANDATORY** |
| [Pair Programming](docs/common/pair_programming_guide.md) | Team collaboration | For teams |
| [Presentation Guide](docs/common/presentation_guide.md) | E4 preparation | Before Week 14 |
| [Troubleshooting](docs/common/troubleshooting_common.md) | Common issues | Reference |

---

## 🚀 Quick Start

### 1. Choose Your Project

Browse the [projects list](#projects-list) below and select based on:
- Interest area
- Difficulty level
- Technology preference

### 2. Set Up Environment

```bash
# Clone your repository
git clone https://github.com/[username]/retele-proiect-XX.git
cd retele-proiect-XX

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run smoke tests
make smoke
```

### 3. Follow Stage Calendar

Each project specification contains:
- Detailed requirements
- Assessment rubric
- Code examples
- Expected outputs

---

## 📋 Projects List

### Main Projects (Teams of 1-3)

| # | Project | Technology | Difficulty |
|---|---------|------------|------------|
| P01 | [SDN Firewall with Mininet](PROJECTS/P01_SDN_Firewall_Mininet.md) | Mininet, POX | ★★★★☆ |
| P02 | [SDN Learning Switch](PROJECTS/P02_SDN_Learning_Switch.md) | Mininet, Ryu | ★★★☆☆ |
| P03 | [IDS Traffic Monitoring](PROJECTS/P03_IDS_Traffic_Monitoring_Python.md) | Scapy, Python | ★★★★☆ |
| P04 | [Secure Communication Channel](PROJECTS/P04_Secure_Communication_Channel.md) | Cryptography | ★★★★☆ |
| P05 | [Traffic Generation & Analysis](PROJECTS/P05_Traffic_Generation_Analysis.md) | Scapy, iperf | ★★★★☆ |
| P06 | [SDN Controller OpenFlow](PROJECTS/P06_SDN_Mininet_Controller_OpenFlow.md) | Ryu, OpenFlow | ★★★☆☆ |
| P07 | [Firewall & IDS Monitoring](PROJECTS/P07_Firewall_IDS_Traffic_Monitoring.md) | Scapy, iptables | ★★★☆☆ |
| P08 | [Web Server & Reverse Proxy](PROJECTS/P08_Web_Server_Reverse_Proxy.md) | Sockets, HTTP | ★★★☆☆ |
| P09 | [Multi-Client FTP Server](PROJECTS/P09_Multi_Client_FTP_Server.md) | Sockets, FTP | ★★★☆☆ |
| P10 | [Docker Network Configuration](PROJECTS/P10_Docker_Network_Configuration.md) | Docker | ★★☆☆☆ |
| P11 | [Advanced SDN QoS](PROJECTS/P11_Advanced_SDN_Mininet_OpenFlow.md) | Ryu, QoS | ★★★★☆ |
| P12 | [Microservices Load Balancing](PROJECTS/P12_Docker_Microservices_Load_Balancing.md) | Docker, Flask | ★★★☆☆ |
| P13 | [RPC/gRPC Service](PROJECTS/P13_RPC_gRPC_Service.md) | gRPC, Protobuf | ★★★★☆ |
| P14 | [IDS/IPS Simulation](PROJECTS/P14_Security_IDS_IPS_Simulation.md) | Scapy, Security | ★★★★☆ |
| P15 | [MQTT IoT Application](PROJECTS/P15_MQTT_IoT_Client_Server.md) | MQTT, paho | ★★★☆☆ |

### Reserve Projects (Individual)

| # | Project | Technology |
|---|---------|------------|
| P16 | [Network Traffic Analyzer](RESERVE_individual/P16_Network_Traffic_Analyzer.md) | Scapy |
| P17 | [DNS Client/Server](RESERVE_individual/P17_Reserve.md) | DNS Protocol |
| P18 | [Network Chat Application](RESERVE_individual/P18_Reserve.md) | Sockets |
| P19 | [Port Scanner](RESERVE_individual/P19_Reserve.md) | Scapy |
| P20 | [IoT Security](RESERVE_individual/P20_Reserve.md) | MQTT, TLS |

---

## 📦 Submission Format

### Archive Naming Convention

**Format:** `SURNAME_Firstname_GGGG_PXX_EY.zip`

| Field | Description | Example |
|-------|-------------|---------|
| SURNAME | Family name (UPPERCASE) | POPESCU |
| Firstname | First name | Ion |
| GGGG | Group number | 1098 |
| PXX | Project number | P01 |
| EY | Stage (E1-E4) | E1 |

**Example:** `POPESCU_Ion_1098_P01_E1.zip`

### Required Files

| Stage | Required Contents |
|-------|-------------------|
| E1 | `docs/specificatii.md`, `docs/diagrame/`, `README.md`, `MANIFEST.txt` |
| E2 | + `src/` (partial), `docker/`, `docs/raport_progres.md` |
| E3 | + `tests/`, `docs/documentatie_finala.md`, `CHANGELOG.md` |
| E4 | Complete repository + git tag `v1.0-final` |

---

## 🔧 Development Environment

### Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| **Python** | 3.10+ | Programming |
| **Docker** | 24.0+ | Containerisation |
| **Git** | 2.40+ | Version control |
| **WSL2** | Latest | Windows users |

### Recommended Setup

```bash
# Credentials for WSL Ubuntu (from netENwsl)
user: stud
pass: stud

# Portainer (localhost:9000)
user: stud
pass: studstudstud
```

---

## ❓ Frequently Asked Questions

**Q: Can I change project after E1?**  
A: No, project assignment is final after E1 submission.

**Q: Can I work alone on a team project?**  
A: Yes, but you must complete all requirements for team size 1.

**Q: What if I miss a deadline?**  
A: Late submissions receive 10% penalty per day (max 3 days).

**Q: Where do I submit?**  
A: Upload to the course portal + push to GitHub.

---

## 📚 External Resources

### Laboratory Materials
- **netENwsl:** https://github.com/antonioclim/netENwsl

### Documentation
- **Python:** https://docs.python.org/3/
- **Docker:** https://docs.docker.com/
- **Scapy:** https://scapy.readthedocs.io/
- **Ryu SDN:** https://ryu-sdn.org/

---

## 📞 Support

- **Course Forum:** Check before asking
- **Office Hours:** Posted on course page
- **Troubleshooting Guide:** [troubleshooting_common.md](docs/common/troubleshooting_common.md)

---

*Computer Networks — ASE Bucharest, CSIE*  
*Academic Year 2025-2026*
