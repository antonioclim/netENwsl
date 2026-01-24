# 🖧 Computer Networks — Complete Laboratory Kits (WSL Edition)

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-28.2.2+-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![WSL2](https://img.shields.io/badge/WSL2-Ubuntu_22.04_LTS-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com)
[![Wireshark](https://img.shields.io/badge/Wireshark-4.4.x-1679A7?style=for-the-badge&logo=wireshark&logoColor=white)](https://wireshark.org)
[![Portainer](https://img.shields.io/badge/Portainer-2.33.6_LTS-13BEF9?style=for-the-badge&logo=portainer&logoColor=white)](https://portainer.io)
[![Licence](https://img.shields.io/badge/Licence-Restrictive_Educational-red?style=for-the-badge)](LICENCE.md)

> **© 2019–2056 Antonio Clim, Andrei Toma** | by Revolvix

---

## ⚡ QUICK START — Up and Running in 5 Minutes

```bash
# ═══════════════════════════════════════════════════════════════════════════════
# CLONE_REPOSITORY
# ═══════════════════════════════════════════════════════════════════════════════
git clone https://github.com/antonioclim/netENwsl.git
cd netENwsl

# ═══════════════════════════════════════════════════════════════════════════════
# NAVIGATE_TO_WEEK
# ═══════════════════════════════════════════════════════════════════════════════
cd 01enWSL  # or any week (01-14)

# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
python3 setup/verify_environment.py

# ═══════════════════════════════════════════════════════════════════════════════
# START_LABORATORY
# ═══════════════════════════════════════════════════════════════════════════════
python3 scripts/start_lab.py

# ═══════════════════════════════════════════════════════════════════════════════
# ACCESS_PORTAINER
# ═══════════════════════════════════════════════════════════════════════════════
# Open in browser: http://localhost:9000
# Credentials: stud / studstudstud
```

### Quick Credentials

| Service | Username | Password |
|---------|----------|----------|
| **Ubuntu WSL** | `stud` | `stud` |
| **Portainer** | `stud` | `studstudstud` |

> 💭 **PREDICTION:** After running `python3 scripts/start_lab.py`, how many containers do you think will start for Week 1?


**Course:** Computer Networks (25.0205IF3.2-0003)  
**Programme:** Economic Informatics, Year III, Semester 2  
**Institution:** Bucharest University of Economic Studies (ASE), Faculty of Cybernetics, Statistics and Economic Informatics (CSIE)  
**Academic Year:** 2025–2026

---

## ⚠️ IMPORTANT: Two Repositories Available

Laboratory materials are available in **two languages**, organised in separate repositories:

### Main Repositories (WSL Edition — Recommended)

| Repository | Language | URL | Naming Convention |
|------------|----------|-----|-------------------|
| **netENwsl** | 🇬🇧 English | https://github.com/antonioclim/netENwsl | `<NN>enWSL` (e.g. `01enWSL`, `14enWSL`) |
| **netROwsl** | 🇷🇴 Romanian | https://github.com/antonioclim/netROwsl | `<NN>roWSL` (e.g. `01roWSL`, `14roWSL`) |

### Beta Repositories (Linux VM Edition — For Advanced Users)

| Repository | Language | URL | Status |
|------------|----------|-----|--------|
| **NETro** | 🇷🇴 Romanian | https://github.com/antonioclim/NETro | Beta — requires Linux VM |
| **netEN** | 🇬🇧 English | https://github.com/antonioclim/netEN | Beta — requires Linux VM |

### Detailed Comparison: WSL Edition vs VM Edition (Beta)

| Feature | netROwsl / netENwsl (WSL) | NETro / netEN (Beta VM) |
|---------|---------------------------|-------------------------|
| **Execution Environment** | WSL2 + Docker + Portainer | Linux VM + Mininet |
| **Host Operating System** | Native Windows 10/11 | Any OS with VM (VirtualBox/VMware) |
| **Naming Convention** | `<NN>roWSL` / `<N>enWSL` | `WEEK<N>` |
| **Automation** | Python scripts | Makefile |
| **Visual Interface** | Portainer (port 9000) | CLI only |
| **Network Simulation** | Docker bridge networks | Mininet (complex topologies) |
| **Traffic Capture** | Native Windows Wireshark | tcpdump in VM |
| **Setup Complexity** | ⭐⭐ Accessible | ⭐⭐⭐⭐ Advanced |
| **PlantUML Diagrams** | ✓ | ✓ |
| **Presentation Slides** | ✓ | ✓ |
| **Completeness** | 14 complete kits | 14 weeks (variable structure) |
| **Documentation** | 2,400+ lines | ~1,000 lines |
| **Resource Usage** | ~500MB RAM base | ~2-4GB RAM (VM) |

### Advantages of WSL Edition (Recommended for Students)

1. **No separate VM required** — Runs directly on Windows without virtualisation overhead
2. **Visual management** — Portainer provides web interface for containers
3. **Modern Python scripts** — Easier to understand than Makefile (still the Makefile option exists)
4. **Native Wireshark integration** — Direct capture on Windows (Let's say "direct visual contact")
5. **Consistent structure** — All 14 kits have identical organisation
6. **Extended documentation** — Detailed README with complete troubleshooting

### When to Choose Beta Edition (VM)?

- You have Linux experience and prefer CLI
- You need complex Mininet topologies
- You want to practise Linux administration in VM
- Your system does not support WSL2

**This documentation covers the WSL repositories (netROwsl/netENwsl)**, with specific instructions for each language variant.

---

## 📋 Table of Contents

### Part I — Introduction and Overview
- [1. General Overview](#1-general-overview)
- [2. Pedagogical Philosophy](#2-pedagogical-philosophy)
- [3. System Architecture](#3-system-architecture)
- [4. Repository Structure](#4-repository-structure)

### Part II — Environment Setup
- [5. System Requirements](#5-system-requirements)
- [6. Standard Credentials](#6-standard-credentials)
- [7. Step-by-Step Installation](#7-step-by-step-installation)
- [8. Installation Verification](#8-installation-verification)

### Part III — Detailed Weekly Curriculum
- [9. Quick Laboratory Start Guide](#9-quick-laboratory-start-guide)
- [10. Individual Week Cloning](#10-individual-week-cloning)
- [11. Week 1: Network Fundamentals](#11-week-1-network-fundamentals)
- [12. Week 2: Architectural Models and Socket Programming](#12-week-2-architectural-models-and-socket-programming)
- [13. Week 3: Advanced Network Programming Models](#13-week-3-advanced-network-programming-models)
- [14. Week 4: Physical and Data Link Layers](#14-week-4-physical-and-data-link-layers)
- [15. Week 5: Network Layer and IP Addressing](#15-week-5-network-layer-and-ip-addressing)
- [16. Week 6: NAT/PAT, Support Protocols and SDN](#16-week-6-natpat-support-protocols-and-sdn)
- [17. Week 7: Packet Capture, Filtering and Security](#17-week-7-packet-capture-filtering-and-security)
- [18. Week 8: Transport Layer, HTTP and Reverse Proxy](#18-week-8-transport-layer-http-and-reverse-proxy)
- [19. Week 9: Session and Presentation Layers](#19-week-9-session-and-presentation-layers)
- [20. Week 10: Application Layer Protocols](#20-week-10-application-layer-protocols)
- [21. Week 11: Load Balancing](#21-week-11-load-balancing)
- [22. Week 12: Email Protocols and RPC](#22-week-12-email-protocols-and-rpc)
- [23. Week 13: IoT and Network Security](#23-week-13-iot-and-network-security)
- [24. Week 14: Integrated Review and Assessment](#24-week-14-integrated-review-and-assessment)

### Part IV — References and Support
- [25. Standard Kit Structure](#25-standard-kit-structure)
- [26. IP Addressing Plan](#26-ip-addressing-plan)
- [27. Port Allocation Conventions](#27-port-allocation-conventions)
- [28. Technologies and Tools Used](#28-technologies-and-tools-used)
- [29. Complete Troubleshooting Guide](#29-complete-troubleshooting-guide)
- [30. Essential Commands — Quick Reference Sheet](#30-essential-commands--quick-reference-sheet)
- [31. Higher-Level Exercises (EVALUATE & CREATE)](#31-higher-level-exercises-evaluate--create)
- [32. Live Coding Guide for Instructors](#32-live-coding-guide-for-instructors)
- [33. FAQ — Frequently Asked Questions](#33-faq--frequently-asked-questions)
- [34. Licence](#34-licence)

---

# PART I — INTRODUCTION AND OVERVIEW

---

## 1. General Overview

This repository contains **complete laboratory kits** for the **Computer Networks** course, covering all **14 weeks** of the university semester. The materials are designed and optimised specifically for deployment on **Windows 10/11** systems using **WSL2** (Windows Subsystem for Linux) with **Docker** containerisation and visual management through **Portainer CE**, providing students and instructors with a portable, reproducible, isolated and professional laboratory environment.

### 1.1 What Does This Repository Offer?

Each weekly kit constitutes a **self-contained and complete educational unit**, comprising:

| Component | Description |
|-----------|-------------|
| **📚 Structured Documentation** | Clearly articulated theoretical foundations, explicit learning objectives and step-by-step guides |
| **🐍 Python Exercises** | Gradual progression from guided implementations to independent complex problem-solving |
| **🐳 Docker Compose Environments** | Pre-configured multi-container network topologies, ready to use |
| **🖥️ Portainer Interface** | Visual management of Docker containers and networks |
| **🧪 Testing Frameworks** | Automated validation of exercise completion and environment integrity |
| **📡 Capture Facilities** | Scripts for packet capture and protocol forensic analysis |
| **🦈 Wireshark Guides** | Specific filters for each protocol and week |
| **📋 Reference Sheets** | Essential CLI commands consolidated for quick access |
| **📝 Homework Assignments** | Additional exercises with reference solutions for independent study |

### 1.2 Learning Methodology

The pedagogical approach emphasises **learning through direct observation and experimentation**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     EXPERIENTIAL LEARNING CYCLE                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│    ┌──────────────┐      ┌──────────────┐      ┌──────────────┐             │
│    │    BUILD     │ ──▶  │   GENERATE  │ ──▶  │   CAPTURE    │             │
│    │   network    │      │   network    │      │   packets    │             │
│    │   services   │      │   traffic    │      │   PCAP       │             │
│    └──────────────┘      └──────────────┘      └──────┬───────┘             │
│           ▲                                           │                     │
│           │                                           ▼                     │
│    ┌──────┴───────┐                          ┌──────────────┐               │
│    │    APPLY     │ ◀────────────────────── │   ANALYSE    │               │
│    │    new       │                          │  protocols   │               │
│    │  knowledge   │                          │ & behaviour  │               │
│    └──────────────┘                          └──────────────┘               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

This methodology bridges **theoretical models** and **operational reality**, preparing students for careers in:

- 🌐 Computer network engineering
- 🔒 Cybersecurity analysis and auditing
- 🏗️ Distributed systems development
- ☁️ Cloud infrastructure administration
- 🔧 DevOps and Site Reliability Engineering

### 1.3 Who Is This Repository For?

| Target Audience | Benefits |
|-----------------|----------|
| **Students** | Complete materials for independent learning, practical exercises and reference solutions |
| **Lecturers/Teaching Assistants** | Ready-to-use laboratory kits, consistent structure and assessment framework |
| **Self-Learners** | Complete networking curriculum from fundamentals to advanced topics |
| **Professionals** | Concept refresher, experimentation sandbox and technical reference |

---

## 2. Pedagogical Philosophy

### 2.1 Learning Progression Model

The course follows a **bottom-up architectural exploration** aligned with OSI/TCP-IP reference models, beginning with fundamental concepts and diagnostic tools before ascending through the protocol stack:

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                      LEARNING TRAJECTORY — SEMESTER 2                         ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  Week 14 ─┬─ INTEGRATION  ════════════════════════════════════════════════    ║
║           │                                                                   ║
║  Week 13 ─┤                ┌───────────────────────────────────────────┐      ║
║  Week 12 ─┤  APPLICATION   │  • IoT & MQTT (publish/subscribe)         │      ║
║  Week 11 ─┤  LAYER         │  • Email (SMTP, POP3, IMAP)               │      ║
║  Week 10 ─┘                │  • RPC (JSON-RPC, XML-RPC, gRPC)          │      ║
║                            │  • HTTP/HTTPS, REST APIs, DNS, SSH        │      ║
║                            │  • Load Balancing                         │      ║
║                            └───────────────────────────────────────────┘      ║
║                                                                               ║
║  Week 9  ─┬─ SESSION &     ┌───────────────────────────────────────────┐      ║
║           │  PRESENTATION  │  • FTP Active/Passive modes               │      ║
║           │                │  • Binary serialisation                   │      ║
║           │                │  • Session state management               │      ║
║           └────────────────└───────────────────────────────────────────┘      ║
║                                                                               ║
║  Week 8  ─── TRANSPORT     ┌───────────────────────────────────────────┐      ║
║                            │  • TCP 3-way handshake                    │      ║
║                            │  • HTTP/1.1 server implementation         │      ║
║                            │  • Nginx reverse proxy & load balancing   │      ║
║                            └───────────────────────────────────────────┘      ║
║                                                                               ║
║  Week 7  ─── SECURITY      ┌───────────────────────────────────────────┐      ║
║             & FILTERING    │  • iptables firewall rules                │      ║
║                            │  • Packet filtering (DROP/REJECT)         │      ║
║                            │  • Port scanning & reconnaissance         │      ║
║                            │  • tcpdump, tshark, Wireshark             │      ║
║                            └───────────────────────────────────────────┘      ║
║                                                                               ║
║  Week 5  ─┬─ NETWORK       ┌───────────────────────────────────────────┐      ║
║  Week 6  ─┘  LAYER         │  • IP addressing, CIDR, VLSM              │      ║
║                            │  • NAT/PAT, SNAT, DNAT                    │      ║
║                            │  • ARP, DHCP, ICMP, NDP                   │      ║
║                            │  • Software-Defined Networking (SDN)      │      ║
║                            └───────────────────────────────────────────┘      ║
║                                                                               ║
║  Week 4  ─── DATA LINK     ┌───────────────────────────────────────────┐      ║
║                            │  • Ethernet frames, MAC addressing        │      ║
║                            │  • CRC32 error detection                  │      ║
║                            │  • Binary protocol design                 │      ║
║                            │  • Python struct pack/unpack              │      ║
║                            └───────────────────────────────────────────┘      ║
║                                                                               ║
║  Week 1  ─┬─ FUNDAMENTALS  ┌───────────────────────────────────────────┐      ║
║  Week 2  ─┤                │  • CLI diagnostic tools (ip, ss, ping)    │      ║
║  Week 3  ─┘                │  • Socket programming (TCP/UDP)           │      ║
║                            │  • Concurrent servers (threading)         │      ║
║                            │  • Packet capture & analysis              │      ║
║                            └───────────────────────────────────────────┘      ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### 2.2 Competency Development Framework (Anderson-Bloom Taxonomy)

Each laboratory session targets specific cognitive levels, progressing from simple to complex:

| Cognitive Level | Key Verb | Typical Activities | Assessment Methods |
|-----------------|----------|--------------------|--------------------|
| **1. REMEMBER** | Recall, Identify, List | Command syntax, protocol fields, concept definitions | Reference sheet completion, quick quizzes |
| **2. UNDERSTAND** | Explain, Describe, Compare | Protocol behaviour, traffic patterns, data flows | Written analysis, verbal explanations, diagrams |
| **3. APPLY** | Demonstrate, Implement, Use | Using tools in new scenarios, adapting scripts | Functional implementations, logs, reports |
| **4. ANALYSE** | Examine, Differentiate, Investigate | Packet captures, troubleshooting workflows, root cause analysis | PCAP annotations, root cause reports |
| **5. EVALUATE** | Assess, Critique, Justify | Security posture, design trade-offs, architectural choices | Technical recommendations, audits, peer review |
| **6. CREATE** | Design, Build, Develop | Protocol implementations, custom tools, original solutions | Original code, documentation, presentations |

---

## 3. System Architecture

### 3.1 Why WSL2 + Docker (and not Docker Desktop)?

The choice of **WSL2 + native Docker in Ubuntu** architecture (instead of Docker Desktop) is based on several significant advantages for the educational environment:

| Criterion | WSL2 + Native Docker | Docker Desktop |
|-----------|----------------------|----------------|
| **🚀 Performance** | Native Linux kernel, fast I/O | Additional virtualisation overhead |
| **💾 Resource Usage** | ~500MB base, efficient | ~2GB+ base, high RAM consumption |
| **🌐 Network Fidelity** | Complete Linux network stack | Abstraction and limitations |
| **📁 File Integration** | Direct access to Windows file system | Mounts with overhead |
| **💰 Licensing** | Completely free | Enterprise restrictions (>250 employees) |
| **🎓 Educational Value** | Real, transferable Linux skills | Abstraction hiding complexity |
| **🔧 Control** | Complete configuration control | Limited configuration |

### 3.2 Complete Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              WINDOWS 10/11 HOST                                 │
│                                                                                 │
│  ┌────────────────┐   ┌────────────────┐   ┌────────────────┐   ┌────────────┐  │
│  │   Wireshark    │   │    Browser     │   │  PowerShell/   │   │  VS Code   │  │
│  │  (Native Win   │   │   (Portainer   │   │   Terminal     │   │   (IDE)    │  │
│  │   Analyser)    │   │    :9000)      │   │   Windows      │   │            │  │
│  └───────┬────────┘   └───────┬────────┘   └───────┬────────┘   └─────┬──────┘  │
│          │                    │                    │                  │         │
│          │     ┌──────────────┴──────────────┬─────┴──────────────────┘         │
│          │     │                             │                                  │
│          ▼     ▼                             ▼                                  │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │                    vEthernet (WSL) — Virtual Network                      │  │
│  │              Bridge interface between Windows and Linux                   │  │
│  │                     Dynamic IP: 172.x.x.x                                 │  │
│  └───────────────────────────────────────────┬───────────────────────────────┘  │
│                                              │                                  │
│  ┌───────────────────────────────────────────┴───────────────────────────────┐  │
│  │                         WSL2 (Lightweight Virtual Machine)                │  │
│  │  ┌─────────────────────────────────────────────────────────────────────┐  │  │
│  │  │                        Ubuntu 22.04 LTS                             │  │  │
│  │  │                   User: stud | Password: stud                       │  │  │
│  │  │  ┌───────────────────────────────────────────────────────────────┐  │  │  │
│  │  │  │                      Docker Engine 28.2.2                     │  │  │  │
│  │  │  │                                                               │  │  │  │
│  │  │  │   ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │  │  │  │
│  │  │  │   │  Container  │  │  Container  │  │     Portainer CE    │   │  │  │  │
│  │  │  │   │    Lab 1    │  │    Lab 2    │  │   (Port 9000)       │   │  │  │  │
│  │  │  │   │  10.0.X.Y   │  │  10.0.X.Z   │  │  stud/studstudstud  │   │  │  │  │
│  │  │  │   └─────────────┘  └─────────────┘  └─────────────────────┘   │  │  │  │
│  │  │  │                                                               │  │  │  │
│  │  │  │   ┌─────────────────────────────────────────────────────────┐ │  │  │  │
│  │  │  │   │              Docker Networks (bridge)                   │ │  │  │  │
│  │  │  │   │  week1net, week2net, ... week14net (10.0.X.0/24)        │ │  │  │  │
│  │  │  │   └─────────────────────────────────────────────────────────┘ │  │  │  │
│  │  │  └───────────────────────────────────────────────────────────────┘  │  │  │
│  │  └─────────────────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
│                    WSL2 ↔ WINDOWS BOUNDARY                                      │
│    ══════════════════════════════════════════════════════════════════════════   │
│                                │                                                │
│                                ▼                                                │
│         ┌──────────────────────────────────────────────────────────────┐        │
│         │                vEthernet (WSL)                               │        │
│         │    ← Wireshark captures WSL traffic here →                   │        │
│         └──────────────────────────────────────────────────────────────┘        │
│                                │                                                │
│                                ▼                                                │
│                    ┌───────────────────────┐                                    │
│                    │  Windows Network Stack │                                   │
│                    │   (Internet Access)    │                                   │
│                    └───────────────────────┘                                    │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Repository Structure

### 4.1 English Repository (netENwsl)

```
netENwsl/
│
├── 📁 00-startAPPENDIX(week0)/         # ⚠️ READ FIRST! Prerequisites & Python Guide
│   ├── 00BEFORE_ANYTHING_ELSE/         # Essential setup instructions
│   ├── 00LECTURES/                     # Lecture materials
│   ├── 00PREREQUISITES/                # Prerequisites HTML guide
│   │   ├── PREREQUISITES_EN.html       # Interactive HTML guide
│   │   └── wireshark_capture_example.png
│   ├── PYTHON_self_study_guide/        # Python for Networking (self-study)
│   │   ├── PRESENTATIONS_EN/           # 10 HTML presentations
│   │   │   ├── 01_introduction_setup.html
│   │   │   ├── 02_reading_python_code.html
│   │   │   ├── 03_data_types_networking.html
│   │   │   ├── 04_socket_programming.html
│   │   │   ├── 05_code_organisation.html
│   │   │   ├── 06_cli_interfaces.html
│   │   │   ├── 07_packet_analysis.html
│   │   │   ├── 08_concurrency.html
│   │   │   ├── 09_http_protocols.html
│   │   │   └── 10_debugging_best_practices.html
│   │   ├── cheatsheets/                # Quick reference guides
│   │   ├── examples/                   # Python code examples
│   │   └── PYTHON_NETWORKING_GUIDE.md  # Complete guide
│   ├── docs/                           # Pedagogical documentation
│   │   ├── peer_instruction.md
│   │   ├── misconceptions.md
│   │   ├── parsons_problems.md
│   │   └── troubleshooting.md
│   └── LIVE_CODING_INSTRUCTOR_GUIDE.md
│
├── 📁 00PROJ/                          # 📋 Course Projects (Teams of 2)
│   ├── PROJECTS/                       # 15 main projects (P01-P15)
│   │   ├── P01_SDN_Firewall_Mininet.md
│   │   ├── P02_Hybrid_Network_Mininet_Docker.md
│   │   ├── ... (P03-P14)
│   │   └── P15_IoT_Edge_Computing_MQTT.md
│   ├── RESERVE_individual/             # 5 reserve/individual projects (P16-P20)
│   │   ├── P16_HTTP_Analysis_Wireshark.md
│   │   ├── P17_LAN_NAT_DHCP_Network.md
│   │   ├── P18_TCP_Chat_Client_Server.md
│   │   ├── P19_Port_Scanner_Security.md
│   │   └── P20_IoT_Smart_Home_Security.md
│   └── docs/common/                    # Shared project documentation
│       ├── code_quality_standards.md
│       ├── git_workflow_detailed.md
│       ├── pair_programming_guide.md
│       └── presentation_guide.md
│
├── 📁 01enWSL/                         # Week 1: Fundamentals of Computer Networks
├── 📁 02enWSL/                         # Week 2: Architectural Models and Socket Programming
├── 📁 03enWSL/                         # Week 3: Introduction to Network Programming
├── 📁 04enWSL/                         # Week 4: Physical Layer, Data Link Layer & Custom Protocols
├── 📁 05enWSL/                         # Week 5: Network Layer – IP Addressing, Subnetting, VLSM
├── 📁 06enWSL/                         # Week 6: NAT/PAT, Network Support Protocols & SDN
├── 📁 07enWSL/                         # Week 7: Packet Interception, Filtering and Defensive Port Probing
├── 📁 08enWSL/                         # Week 8: Transport Layer — HTTP Server Implementation and Reverse Proxies
├── 📁 09enWSL/                         # Week 9: Session Layer and Presentation Layer
├── 📁 10enWSL/                         # Week 10: Application Layer Protocols
├── 📁 11enWSL/                         # Week 11: Application Protocols – FTP, DNS, SSH & Load Balancing
├── 📁 12enWSL/                         # Week 12: Email Protocols and Remote Procedure Call
├── 📁 13enWSL/                         # Week 13: IoT and Security in Computer Networks
├── 📁 14enWSL/                         # Week 14: Integrated Recap and Project Evaluation
│
├── 📄 README.md                        # Main documentation (this file)
└── 📄 LICENCE.md                       # Restrictive Educational Licence
```

### 4.2 Romanian Repository (netROwsl)

```
netROwsl/
│
├── 📁 00-startAPPENDIX(week0)/         # ⚠️ READ FIRST! Prerequisites
│   ├── CERINTE_PRELIMINARE_RO.html     # Interactive HTML guide
│   ├── CerintePrelimRO.md              # Markdown guide
│   └── exemplu_captura_wireshark.png   # Example screenshot
│
├── 📁 01roWSL/                         # Week 1: Network Fundamentals
├── 📁 02roWSL/                         # Week 2: Models & Sockets
├── 📁 03roWSL/                         # Week 3: Network Programming
├── 📁 04roWSL/                         # Week 4: Physical & Data Link
├── 📁 05roWSL/                         # Week 5: IP Addressing & Subnets
├── 📁 06roWSL/                         # Week 6: NAT/PAT, SDN
├── 📁 07roWSL/                         # Week 7: Filtering & Security
├── 📁 08roWSL/                         # Week 8: Transport & HTTP
├── 📁 09roWSL/                         # Week 9: Session & Presentation
├── 📁 10roWSL/                         # Week 10: Application Protocols
├── 📁 11roWSL/                         # Week 11: Load Balancing
├── 📁 12roWSL/                         # Week 12: Email & RPC
├── 📁 13roWSL/                         # Week 13: IoT & Security
├── 📁 14roWSL/                         # Week 14: Review
│
├── 📄 READMEro.md                      # Main documentation (RO)
└── 📄 LICENCE.md                       # Restrictive Educational Licence
```

### 4.3 Key Differences Between Repositories

| Aspect | netENwsl (English) | netROwsl (Romanian) |
|--------|-------------------|---------------------|
| **Naming Convention** | `<N>enWSL` | `<NN>roWSL` (with zero for 01-09) |
| **Documentation** | README.md, docstrings EN | READMEro.md, comments RO |
| **Script Names** | `start_lab.py`, `stop_lab.py` | `porneste_lab.py`, `opreste_lab.py` |
| **Console Messages** | English | Romanian |
| **Internal Structure** | Identical | Identical |
| **Compatibility** | Complete | Complete |

---

# PART II — ENVIRONMENT SETUP

---

## 5. System Requirements

### 5.1 Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **Processor** | Intel Core i5 / AMD Ryzen 5 | Intel Core i7 / AMD Ryzen 7 |
| **Memory RAM** | 8 GB | 16 GB |
| **Disk Space** | 20 GB free | 50 GB free (SSD) |
| **Virtualisation** | VT-x / AMD-V enabled | VT-x / AMD-V + IOMMU |

### 5.2 Software Requirements

| Software | Minimum Version | Verification |
|----------|-----------------|--------------|
| **Windows** | 10 (build 19041+) or 11 | `winver` |
| **WSL2** | Kernel 5.15+ | `wsl --status` |
| **Ubuntu** | 22.04 LTS | `lsb_release -a` |
| **Docker Engine** | 24.0+ | `docker --version` |
| **Docker Compose** | 2.20+ | `docker compose version` |
| **Python** | 3.11+ | `python3 --version` |
| **Wireshark** | 4.0+ | About → Wireshark |
| **Git** | 2.40+ | `git --version` |

---

## 6. Standard Credentials

### 6.1 Centralised Credentials Table

| Service | Username | Password | URL/Access | Notes |
|---------|----------|----------|------------|-------|
| **Ubuntu WSL** | `stud` | `stud` | WSL Terminal | User with `sudo` privileges |
| **Portainer** | `stud` | `studstudstud` | http://localhost:9000 | Min. 12 character password |

> ⚠️ **IMPORTANT:** Portainer uses **EXCLUSIVELY port 9000**. No other laboratory service should use this port!

---

## 7. Step-by-Step Installation

### 7.1 Installing WSL2 and Ubuntu

> 💭 **PREDICTION:** What minimum Docker Compose version is required? What will `docker compose version` display on your system?

Open PowerShell as Administrator and run:

```powershell
# ═══════════════════════════════════════════════════════════════════════════════
# INSTALL_WSL2
# ═══════════════════════════════════════════════════════════════════════════════
wsl --install -d Ubuntu-22.04

# ═══════════════════════════════════════════════════════════════════════════════
# SET_DEFAULT_VERSION
# ═══════════════════════════════════════════════════════════════════════════════
wsl --set-default-version 2

# ═══════════════════════════════════════════════════════════════════════════════
# RESTART_REQUIRED
# ═══════════════════════════════════════════════════════════════════════════════
# Restart your computer after installation
```

### 7.2 Initial Ubuntu Configuration

After restarting, open Ubuntu from the Start Menu:

```bash
# ═══════════════════════════════════════════════════════════════════════════════
# CREATE_USER
# ═══════════════════════════════════════════════════════════════════════════════
# When prompted, create user: stud
# Password: stud

# ═══════════════════════════════════════════════════════════════════════════════
# UPDATE_SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════
sudo apt update && sudo apt upgrade -y
```

### 7.3 Installing Docker Engine

```bash
# ═══════════════════════════════════════════════════════════════════════════════
# INSTALL_DEPENDENCIES
# ═══════════════════════════════════════════════════════════════════════════════
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# ═══════════════════════════════════════════════════════════════════════════════
# ADD_DOCKER_REPOSITORY
# ═══════════════════════════════════════════════════════════════════════════════
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# ═══════════════════════════════════════════════════════════════════════════════
# INSTALL_DOCKER
# ═══════════════════════════════════════════════════════════════════════════════
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURE_USER_PERMISSIONS
# ═══════════════════════════════════════════════════════════════════════════════
sudo usermod -aG docker $USER

# ═══════════════════════════════════════════════════════════════════════════════
# START_DOCKER_SERVICE
# ═══════════════════════════════════════════════════════════════════════════════
sudo service docker start
```

### 7.4 Installing Portainer CE

```bash
# ═══════════════════════════════════════════════════════════════════════════════
# CREATE_PORTAINER_VOLUME
# ═══════════════════════════════════════════════════════════════════════════════
docker volume create portainer_data

# ═══════════════════════════════════════════════════════════════════════════════
# INSTALL_PORTAINER
# ═══════════════════════════════════════════════════════════════════════════════
docker run -d \
  --name portainer \
  --restart=always \
  -p 9000:9000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:lts

# ═══════════════════════════════════════════════════════════════════════════════
# ACCESS_PORTAINER
# ═══════════════════════════════════════════════════════════════════════════════
# Open browser: http://localhost:9000
# Create account: stud / studstudstud
```

---

## 8. Installation Verification

### 8.1 Verification Script

Create and run this script in Ubuntu:

```bash
#!/bin/bash
# verify_lab_environment.sh
# Complete laboratory environment verification script

# ═══════════════════════════════════════════════════════════════════════════════
# DEFINE_COLOURS_AND_COUNTERS
# ═══════════════════════════════════════════════════════════════════════════════
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Colour

ERRORS=0
WARNINGS=0

# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY_BANNER
# ═══════════════════════════════════════════════════════════════════════════════
echo ""
echo "╔═══════════════════════════════════════════════════════════════════════════╗"
echo "║        COMPUTER NETWORKS LABORATORY ENVIRONMENT VERIFICATION              ║"
echo "║              © 2019–2026 Antonio Clim, Andrei Toma                        ║"
echo "╚═══════════════════════════════════════════════════════════════════════════╝"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# DEFINE_CHECK_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
check_required() {
    if eval "$2" &>/dev/null; then
        echo -e "  ${GREEN}✓${NC} $1"
    else
        echo -e "  ${RED}✗${NC} $1"
        ((ERRORS++))
    fi
}

check_optional() {
    if eval "$2" &>/dev/null; then
        echo -e "  ${GREEN}✓${NC} $1"
    else
        echo -e "  ${YELLOW}○${NC} $1 (optional)"
        ((WARNINGS++))
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY_SYSTEM_INFORMATION
# ═══════════════════════════════════════════════════════════════════════════════
echo -e "${BLUE}▶ SYSTEM INFORMATION${NC}"
echo "  Hostname: $(hostname)"
echo "  Ubuntu: $(lsb_release -d 2>/dev/null | cut -f2)"
echo "  Kernel: $(uname -r)"
echo "  User: $(whoami)"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# CHECK_MAIN_COMPONENTS
# ═══════════════════════════════════════════════════════════════════════════════
echo -e "${BLUE}▶ MAIN COMPONENTS${NC}"
check_required "Python 3.11+" "python3 --version | grep -E 'Python 3\.(1[1-9]|[2-9][0-9])'"
check_required "pip3" "pip3 --version"
check_required "Git" "git --version"
check_required "curl" "curl --version"
check_required "wget" "wget --version"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# CHECK_DOCKER
# ═══════════════════════════════════════════════════════════════════════════════
echo -e "${BLUE}▶ DOCKER${NC}"
check_required "Docker Engine" "docker --version"
check_required "Docker Compose" "docker compose version"
check_required "Docker daemon active" "docker info"
check_required "Docker without sudo" "docker ps"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# CHECK_PORTAINER
# ═══════════════════════════════════════════════════════════════════════════════
echo -e "${BLUE}▶ PORTAINER (Port 9000)${NC}"
if docker ps | grep -q portainer; then
    echo -e "  ${GREEN}✓${NC} Portainer running on port 9000"
else
    echo -e "  ${YELLOW}○${NC} Portainer not running (start manually if needed)"
    ((WARNINGS++))
fi
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# CHECK_NETWORK_TOOLS
# ═══════════════════════════════════════════════════════════════════════════════
echo -e "${BLUE}▶ NETWORK TOOLS${NC}"
check_required "tcpdump" "which tcpdump"
check_optional "tshark" "which tshark"
check_required "netcat" "which nc"
check_optional "nmap" "which nmap"
check_optional "iperf3" "which iperf3"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# CHECK_PYTHON_LIBRARIES
# ═══════════════════════════════════════════════════════════════════════════════
echo -e "${BLUE}▶ PYTHON LIBRARIES${NC}"
check_required "docker" "python3 -c 'import docker'"
check_required "scapy" "python3 -c 'import scapy.all'"
check_required "dpkt" "python3 -c 'import dpkt'"
check_required "requests" "python3 -c 'import requests'"
check_required "flask" "python3 -c 'import flask'"
check_optional "paramiko" "python3 -c 'import paramiko'"
check_optional "pyftpdlib" "python3 -c 'import pyftpdlib'"
check_optional "paho-mqtt" "python3 -c 'import paho.mqtt.client'"
check_optional "dnspython" "python3 -c 'import dns.resolver'"
check_optional "grpcio" "python3 -c 'import grpc'"
echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY_SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════
echo "═══════════════════════════════════════════════════════════════════════════"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ ALL REQUIRED COMPONENTS ARE CORRECTLY INSTALLED!${NC}"
    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}   ($WARNINGS optional components missing)${NC}"
    fi
else
    echo -e "${RED}❌ $ERRORS REQUIRED COMPONENT(S) MISSING${NC}"
fi
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""

exit $ERRORS
```

### 8.2 Quick Wireshark Capture Test

1. Open **Wireshark** on Windows
2. Select the **vEthernet (WSL)** interface and start capture
3. In the Ubuntu terminal, run:

```bash
docker run --rm alpine ping -c 5 8.8.8.8
```

4. In Wireshark, apply the filter: `icmp`
5. Verify that you can see **Echo request** and **Echo reply** packets

---

# PART III — DETAILED WEEKLY CURRICULUM

---

## 9. Quick Laboratory Start Guide

### 9.1 Standard Workflow for Each Week

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                     STANDARD LABORATORY WORKFLOW                             │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. CLONE              2. VERIFY               3. START                      │
│  ┌──────────────┐     ┌──────────────┐       ┌──────────────┐                │
│  │ git clone    │ ──▶ │ python       │  ──▶ │ python       │                │
│  │ repository   │     │ verify_      │       │ start_       │                │
│  │              │     │ environment  │       │ lab.py       │                │
│  └──────────────┘     └──────────────┘       └──────────────┘                │
│                                                      │                       │
│                                                      ▼                       │
│  6. CLEANUP            5. ANALYSIS            4. EXERCISES                   │
│  ┌──────────────┐     ┌──────────────┐       ┌──────────────┐                │
│  │ python       │ ◀── │ Wireshark    │  ◀── │ Python       │                │
│  │ stop_        │     │ PCAP files   │       │ Exercises    │                │
│  │ lab.py       │     │              │       │              │                │
│  └──────────────┘     └──────────────┘       └──────────────┘                │
│                                                                              │
│  ⚠️ NOTE: Portainer (port 9000) remains ALWAYS active between laboratories!  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 Standard Commands Available in Each Kit (English version)

```bash
# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
python3 setup/verify_environment.py

# ═══════════════════════════════════════════════════════════════════════════════
# START_LAB_SERVICES
# ═══════════════════════════════════════════════════════════════════════════════
python3 scripts/start_lab.py

# ═══════════════════════════════════════════════════════════════════════════════
# CHECK_SERVICE_STATUS
# ═══════════════════════════════════════════════════════════════════════════════
python3 scripts/start_lab.py --status

# ═══════════════════════════════════════════════════════════════════════════════
# RUN_DEMONSTRATIONS
# ═══════════════════════════════════════════════════════════════════════════════
python3 scripts/run_demo.py --demo 1

# ═══════════════════════════════════════════════════════════════════════════════
# CAPTURE_TRAFFIC
# ═══════════════════════════════════════════════════════════════════════════════
python3 scripts/capture_traffic.py --duration 30 --output pcap/capture.pcap

# ═══════════════════════════════════════════════════════════════════════════════
# STOP_SERVICES
# ═══════════════════════════════════════════════════════════════════════════════
python3 scripts/stop_lab.py

# ═══════════════════════════════════════════════════════════════════════════════
# COMPLETE_CLEANUP
# ═══════════════════════════════════════════════════════════════════════════════
python3 scripts/cleanup.py --complete
```

---

## 11. Week 1: Network Fundamentals

> 💭 **PREDICTION:** After `ping -c 4 google.com`, how many packets will be sent and how many received under normal conditions?

**EN Directory:** `1enWSL/` | **RO Directory:** `01roWSL/`  
**Docker Network:** `10.0.1.0/24`

### 11.1 Synopsis

Introduction to essential network diagnostic tools and foundational network concepts through hands-on exploration of the Linux network stack within Docker containers.

### 11.2 Learning Objectives (Anderson-Bloom)

| Bloom Level | Verb | Specific Objective |
|-------------|------|-------------------|
| **Remember** | Recall | Essential Linux commands: `ip addr`, `ip route`, `ss`, `ping`, `netcat` |
| **Understand** | Explain | Purpose of network interfaces, routing tables and socket states |
| **Apply** | Demonstrate | Connectivity testing using ICMP and latency measurement interpretation |
| **Apply** | Implement | Basic TCP/UDP channels using netcat and Python sockets |
| **Analyse** | Examine | Network captures to identify protocol behaviour |
| **Analyse** | Compare | TCP vs UDP communication patterns through packet examination |
| **Evaluate** | Diagnose | Common connectivity issues using systematic troubleshooting |

### 11.3 Key Technologies

`ip`, `ss`, `ping`, `traceroute`, `netcat`, `tcpdump`, `tshark`, Python sockets

### 11.4 Exercises

| No. | Title | Duration | Description |
|-----|-------|----------|-------------|
| 1 | Network Interface Inspection | 15 min | Interface enumeration, IP examination, routing documentation |
| 2 | Connectivity Testing | 20 min | Progressive ping tests, latency measurement |
| 3 | TCP Communication with netcat | 25 min | Bidirectional sessions, connection state observation |
| 4 | Traffic Capture and Analysis | 30 min | TCP handshake, field identification, CSV export |
| 5 | Statistical PCAP Analysis | 20 min | Programmatic Python processing of captures |

---

## 12. Week 2: Architectural Models and Socket Programming

> 💭 **PREDICTION:** When creating a TCP socket, which socket type will you use: `SOCK_STREAM` or `SOCK_DGRAM`?

**EN Directory:** `2enWSL/` | **RO Directory:** `02roWSL/`  
**Docker Network:** `10.0.2.0/24`

### 12.1 Synopsis

OSI and TCP/IP reference models as analytical frameworks, followed by practical TCP/UDP socket programming in Python including concurrent server architectures.

### 12.2 Key Technologies

`socket`, `threading`, `selectors`, TCP/UDP sockets, concurrent servers, Python socket API

---

## 13. Week 3: Advanced Network Programming Models

> 💭 **PREDICTION:** If you send a UDP broadcast packet, how many devices on the local network will receive it?

**EN Directory:** `3enWSL/` | **RO Directory:** `03roWSL/`  
**Docker Network:** `172.20.0.0/24`

### 13.1 Synopsis

Laboratory introduces advanced programming patterns including UDP broadcast/multicast, TCP tunnelling and application-level protocol design.

### 13.2 Key Technologies

UDP multicast, broadcast sockets, socket options (`SO_BROADCAST`, `IP_ADD_MEMBERSHIP`), `struct`

---

## 14. Week 4: Physical and Data Link Layers

> 💭 **PREDICTION:** An Ethernet frame has a CRC field. What happens if the calculated CRC does not match the received one?

**EN Directory:** `4enWSL/` | **RO Directory:** `04roWSL/`  
**Docker Network:** `172.28.0.0/16`

### 14.1 Synopsis

Laboratory descends to the lowest accessible layers, examining Ethernet framing, MAC addressing and binary protocol construction with CRC32.

### 14.2 Key Technologies

`struct`, `binascii`, `zlib.crc32`, Ethernet frames, MAC addressing, binary protocols

---

## 15. Week 5: Network Layer and IP Addressing

> 💭 **PREDICTION:** How many usable IP addresses are in the network `192.168.1.0/24`? (Hint: it's not 256)

**EN Directory:** `5enWSL/` | **RO Directory:** `05roWSL/`  
**Docker Network:** `10.5.0.0/24`

### 15.1 Synopsis

Complete coverage of IP addressing, subnetting methodologies (CIDR, FLSM, VLSM) and IPv6 fundamentals.

### 15.2 Key Technologies

`ipaddress` module, CIDR notation, FLSM, VLSM, IPv4, IPv6, subnet calculators

---

## 16. Week 6: NAT/PAT, Support Protocols and SDN

> 💭 **PREDICTION:** What happens to a packet's source IP address when it passes through NAT? Does it stay the same or change?

**EN Directory:** `6enWSL/` | **RO Directory:** `06roWSL/`  
**Docker Network:** Custom topology with multiple segments

### 16.1 Synopsis

Network Address Translation, essential support protocols (ARP, DHCP, ICMP, NDP) and introduction to Software-Defined Networking.

### 16.2 Key Technologies

`iptables`, NAT/PAT, ARP, DHCP, ICMP, NDP, Open vSwitch, os-ken (Ryu fork), Mininet

---

## 17. Week 7: Packet Capture, Filtering and Security

> 💭 **PREDICTION:** What packets will `tcpdump -i any port 80` capture? Only HTTP or others too?

**EN Directory:** `7enWSL/` | **RO Directory:** `07roWSL/`  
**Docker Network:** `10.0.7.0/24`

### 17.1 Synopsis

Essential security and forensic skills through packet filtering, firewall configuration and defensive port scanning.

### 17.2 Key Technologies

`tcpdump`, `tshark`, Wireshark, `iptables`, `nmap`, BPF filters, Scapy

---

## 18. Week 8: Transport Layer, HTTP and Reverse Proxy

> 💭 **PREDICTION:** In TCP 3-way handshake, what is the flag order: SYN → ? → ?

**EN Directory:** `8enWSL/` | **RO Directory:** `08roWSL/`  
**Docker Network:** `10.8.0.0/24`

### 18.1 Synopsis

Detailed examination into TCP mechanics, HTTP/1.1 server implementation from scratch and Nginx as reverse proxy.

### 18.2 Key Technologies

TCP handshake, HTTP/1.1, `http.server`, Nginx, reverse proxy, load balancing, Docker Compose

---

## 19. Week 9: Session and Presentation Layers

> 💭 **PREDICTION:** In FTP, which mode (active or passive) works better when the client is behind a firewall?

**EN Directory:** `9enWSL/` | **RO Directory:** `09roWSL/`  
**Docker Network:** `172.29.9.0/24`

### 19.1 Synopsis

Session management and data presentation, with focus on FTP (active/passive modes) and binary serialisation.

### 19.2 Key Technologies

FTP (active/passive), `ftplib`, `pyftpdlib`, binary framing, `struct`, session state management

---

## 20. Week 10: Application Layer Protocols

> 💭 **PREDICTION:** What port does HTTPS use by default and why isn't it the same as HTTP?

**EN Directory:** `10enWSL/` | **RO Directory:** `10roWSL/`  
**Docker Network:** `172.20.0.0/24`

### 20.1 Synopsis

Survey of critical protocols: HTTP/HTTPS, REST API, DNS, SSH. TLS exploration and programmatic operations.

### 20.2 Key Technologies

HTTP/HTTPS, TLS/SSL, REST APIs, `requests`, DNS, `dnspython`, SSH, `paramiko`

---

## 21. Week 11: Load Balancing

> 💭 **PREDICTION:** With round-robin load balancing and 3 backends, which server will the 4th request reach?

**EN Directory:** `11enWSL/` | **RO Directory:** `11roWSL/`  
**Docker Network:** `week11net` (10.0.11.0/24)  
**Ports:** 8080 (Load Balancer), 8081-8083 (Backends)

### 21.1 Synopsis

This laboratory explores load balancing strategies in distributed systems in depth, implementing and comparing round-robin, weighted round-robin, least connections and IP hash algorithms using Nginx as load balancer. Students will configure health checks for automatic failover and analyse traffic distribution in real time.

### 21.2 Key Technologies

Nginx load balancing, round-robin, weighted round-robin, least connections, IP hash, health checks

---

## 22. Week 12: Email Protocols and RPC

> 💭 **PREDICTION:** How many bytes minimum do you need for a protocol header containing: message type, length and checksum?

**EN Directory:** `12enWSL/` | **RO Directory:** `12roWSL/`  
**Docker Network:** `week12net` (10.0.12.0/24)  
**Ports:** 2525 (SMTP), 5000 (JSON-RPC), 5001 (XML-RPC), 50051 (gRPC)

### 22.1 Synopsis

This laboratory covers two fundamental domains of network communication: email protocols (SMTP for sending, POP3/IMAP for receiving) and Remote Procedure Call (RPC) models that enable calling functions on remote servers as if they were local.

### 22.2 Key Technologies

SMTP, `smtplib`, JSON-RPC, XML-RPC, gRPC, `grpcio`, Protocol Buffers

---

## 23. Week 13: IoT and Network Security

> 💭 **PREDICTION:** How many potential vulnerabilities do you think exist in an MQTT setup without authentication?

**EN Directory:** `13enWSL/` | **RO Directory:** `13roWSL/`  
**Docker Network:** `week13net` (10.0.13.0/24)  
**Ports:** 1883 (MQTT), 8883 (MQTT/TLS), 9001 (MQTT WebSocket)

### 23.1 Synopsis

Internet of Things protocols with security focus. MQTT publish/subscribe architecture, TLS integration, authentication mechanisms.

### 23.2 Key Technologies

MQTT, Mosquitto, `paho-mqtt`, TLS certificates, ACL, IoT security patterns

---

## 24. Week 14: Integrated Review and Assessment

> 💭 **PREDICTION:** How many different protocols have you studied this semester? Can you name at least 10?

**EN Directory:** `14enWSL/` | **RO Directory:** `14roWSL/`  
**Docker Networks:** `week14_backend_net` (172.20.0.0/24), `week14_frontend_net` (172.21.0.0/24)  
**Ports:** 8080 (Load Balancer), 8001-8002 (Backends), 9090 (Echo Server)

> ⚠️ **IMPORTANT NOTE:** The Echo Server uses port **9090**, NOT 9000! Port 9000 is reserved exclusively for Portainer.

### 24.1 Synopsis

Synthesis laboratory — building a complete multi-tier application with load balancing, reverse proxy and complete validation. This week integrates all concepts studied throughout the semester into a complex practical project.

### 24.2 Final Architecture

```
┌─────────────────────────────────────────────┐
│           FRONTEND NETWORK 172.21.0.0/24    │
│                                             │
│    ┌─────────────┐    ┌─────────────┐       │
│    │   CLIENT    │    │     LB      │ ◄──── Port 8080
│    │ 172.21.0.2  │    │ 172.21.0.10 │       │
│    └─────────────┘    └──────┬──────┘       │
└──────────────────────────────┼──────────────┘
                               │
┌──────────────────────────────┼──────────────┐
│           BACKEND NETWORK 172.20.0.0/24     │
│                              │              │
│    ┌─────────────┐    ┌──────▼──────┐       │
│    │    APP1     │◄───┤     LB      │       │
│    │ 172.20.0.2  │    │ 172.20.0.10 │       │
│    └─────────────┘    └──────┬──────┘       │
│                              │              │
│    ┌─────────────┐           │              │
│    │    APP2     │◄──────────┘              │
│    │ 172.20.0.3  │                          │
│    └─────────────┘                          │
│                                             │
│    ┌─────────────┐                          │
│    │    ECHO     │ ◄──────────────── Port 9090
│    │ 172.20.0.20 │   (NOT 9000!)            │
│    └─────────────┘                          │
└─────────────────────────────────────────────┘

Portainer (Global Management): http://localhost:9000
```

---

# PART IV — REFERENCES AND SUPPORT

---

## 25. Standard Kit Structure

Each weekly kit follows this standard structure:

```
<N>enWSL/
├── artifacts/           # Generated outputs (captures, logs)
│   └── .gitkeep
├── docker/              # Container configuration
│   ├── configs/         # Service configurations (nginx.conf, etc.)
│   ├── volumes/         # Persistent data
│   ├── web1/, web2/...  # Backend content
│   └── docker-compose.yml
├── docs/                # Documentation (12 standard files)
│   ├── code_tracing.md          # Code tracing exercises
│   ├── commands_cheatsheet.md   # Quick command reference
│   ├── concept_analogies.md     # Real-world analogies
│   ├── further_reading.md       # Additional resources
│   ├── glossary.md              # Technical terms
│   ├── images/                  # Diagrams and screenshots
│   ├── misconceptions.md        # Common misconceptions
│   ├── pair_programming_guide.md # Pair programming instructions
│   ├── parsons_problems.md      # Parsons problems
│   ├── peer_instruction.md      # Peer instruction questions
│   ├── theory_summary.md        # Theory summary
│   └── troubleshooting.md       # Troubleshooting guide
├── homework/            # Assignments
│   ├── exercises/       # hw_NN_XX_*.py
│   ├── solutions/       # Reference solutions (instructor only)
│   └── README.md
├── pcap/                # Packet captures
│   ├── .gitkeep
│   └── README.md
├── scripts/             # Automation scripts (Python)
│   ├── utils/           # Utility modules
│   │   ├── docker_utils.py
│   │   ├── network_utils.py
│   │   └── logger.py
│   ├── start_lab.py     # Start laboratory environment
│   ├── stop_lab.py      # Stop laboratory environment
│   ├── run_demo.py      # Run demonstrations
│   ├── capture_traffic.py
│   └── cleanup.py
├── setup/               # Environment setup
│   ├── install_prerequisites.py
│   ├── configure_docker.py
│   ├── verify_environment.py
│   └── requirements.txt
├── src/                 # Source code
│   ├── apps/            # Complete applications
│   ├── exercises/       # Exercise implementations
│   └── utils/           # Common utilities
├── tests/               # Automated tests
│   ├── smoke_test.py
│   └── expected_outputs.md
├── CHANGELOG.md
├── LICENCE.md
└── README.md
```

---

## 26. IP Addressing Plan

| Week | Docker Network | Subnet | Gateway | Available Hosts |
|:----:|----------------|--------|---------|-----------------|
| 1 | week1net | 10.0.1.0/24 | 10.0.1.1 | 10.0.1.2-254 |
| 2 | week2net | 10.0.2.0/24 | 10.0.2.1 | 10.0.2.2-254 |
| 3 | week3net | 172.20.0.0/24 | 172.20.0.1 | 172.20.0.2-254 |
| 4 | week4net | 172.28.0.0/16 | 172.28.0.1 | 172.28.0.2-65534 |
| 5 | week5net | 10.5.0.0/24 | 10.5.0.1 | 10.5.0.2-254 |
| 6 | week6net | Custom | Variable | Variable |
| 7 | week7net | 10.0.7.0/24 | 10.0.7.1 | 10.0.7.2-254 |
| 8 | week8net | 10.8.0.0/24 | 10.8.0.1 | 10.8.0.2-254 |
| 9 | week9net | 172.29.9.0/24 | 172.29.9.1 | 172.29.9.2-254 |
| 10 | week10net | 172.20.0.0/24 | 172.20.0.1 | 172.20.0.2-254 |
| 11 | week11net | 10.0.11.0/24 | 10.0.11.1 | 10.0.11.2-254 |
| 12 | week12net | 10.0.12.0/24 | 10.0.12.1 | 10.0.12.2-254 |
| 13 | week13net | 10.0.13.0/24 | 10.0.13.1 | 10.0.13.2-254 |
| 14 | week14_* | 172.20-21.0.0/24 | Variable | Variable |

---

## 27. Port Allocation Conventions

### 27.1 Reserved Ports

| Port | Service | Status |
|:----:|---------|--------|
| **9000** | **Portainer CE** | **PERMANENTLY RESERVED** |
| 22 | SSH (if enabled) | Reserved |
| 80 | HTTP (Windows) | Avoid |
| 443 | HTTPS (Windows) | Avoid |

### 27.2 Ports by Week

| Week | Main Ports | Services |
|:----:|------------|----------|
| 1 | 9090, 9091 | TCP Server, UDP Server |
| 2 | 8080, 8081 | Echo Server, Concurrent Server |
| 3 | 5000, 5001 | Multicast Demo, Tunnel |
| 4 | 7000 | Binary Protocol Server |
| 5 | - | No exposed services |
| 6 | 8080 | NAT Demo |
| 7 | - | Internal filtering only |
| 8 | 8080, 8081, 8082 | Nginx, Backend1, Backend2 |
| 9 | 2121, 8021 | FTP Server (active/passive) |
| 10 | 8080, 8443, 5353 | HTTP, HTTPS, DNS |
| 11 | 8080, 8081-8083 | Load Balancer, Backends |
| 12 | 2525, 5000, 5001, 50051 | SMTP, JSON-RPC, XML-RPC, gRPC |
| 13 | 1883, 8883, 9001 | MQTT, MQTT/TLS, WS |
| 14 | 8080, 8001-8002, 9090 | LB, Backends, Echo |

---

## 28. Technologies and Tools Used

### 28.1 Core Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.11+ | Primary programming language |
| Docker | 28.2.2+ | Containerisation |
| Docker Compose | 2.20+ | Multi-container orchestration |
| Portainer CE | 2.33.6 LTS | Visual container management |
| Nginx | 1.25+ | Web server, reverse proxy, load balancer |
| Wireshark | 4.4.x | Packet analysis |

### 28.2 Python Libraries

| Library | Purpose |
|---------|---------|
| `socket` | Low-level networking |
| `threading` | Concurrent servers |
| `struct` | Binary data packing |
| `scapy` | Packet crafting and analysis |
| `requests` | HTTP client |
| `flask` | Web applications |
| `paramiko` | SSH client |
| `paho-mqtt` | MQTT client |
| `grpcio` | gRPC support |
| `dnspython` | DNS queries |

---

## 29. Complete Troubleshooting Guide

### 29.1 Docker Issues

**Problem:** Docker daemon not running

```bash
# ═══════════════════════════════════════════════════════════════════════════════
# CHECK_DOCKER_STATUS
# ═══════════════════════════════════════════════════════════════════════════════
sudo service docker status

# ═══════════════════════════════════════════════════════════════════════════════
# START_DOCKER
# ═══════════════════════════════════════════════════════════════════════════════
sudo service docker start
# Password: stud
```

**Problem:** Permission denied

```bash
# ═══════════════════════════════════════════════════════════════════════════════
# ADD_USER_TO_DOCKER_GROUP
# ═══════════════════════════════════════════════════════════════════════════════
sudo usermod -aG docker $USER

# ═══════════════════════════════════════════════════════════════════════════════
# LOGOUT_AND_LOGIN_AGAIN
# ═══════════════════════════════════════════════════════════════════════════════
exit
# Then reopen Ubuntu
```

### 29.2 Port Conflicts

**Problem:** "Address already in use"

```bash
# ═══════════════════════════════════════════════════════════════════════════════
# FIND_PROCESS_USING_PORT
# ═══════════════════════════════════════════════════════════════════════════════
ss -tulpn | grep <port>

# ═══════════════════════════════════════════════════════════════════════════════
# STOP_CONFLICTING_CONTAINERS
# ═══════════════════════════════════════════════════════════════════════════════
docker ps
docker stop <container_name>
```

### 29.3 Wireshark Issues

**Problem:** Cannot see container traffic

```bash
# ═══════════════════════════════════════════════════════════════════════════════
# USE_TCPDUMP_IN_WSL
# ═══════════════════════════════════════════════════════════════════════════════
sudo tcpdump -i any port <port> -w capture.pcap

# Then open the .pcap file in Windows Wireshark
```

---

## 30. Essential Commands — Quick Reference Sheet

### 30.1 Docker Commands

```bash
# ═══════════════════════════════════════════════════════════════════════════════
# CONTAINER_MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════
docker ps                          # List running containers
docker ps -a                       # List all containers
docker logs <container>            # View container logs
docker exec -it <container> bash   # Enter container shell
docker stop <container>            # Stop container
docker rm <container>              # Remove container

# ═══════════════════════════════════════════════════════════════════════════════
# COMPOSE_COMMANDS
# ═══════════════════════════════════════════════════════════════════════════════
docker compose up -d               # Start services in background
docker compose down                # Stop and remove services
docker compose logs -f             # Follow logs
docker compose ps                  # List compose services

# ═══════════════════════════════════════════════════════════════════════════════
# NETWORK_COMMANDS
# ═══════════════════════════════════════════════════════════════════════════════
docker network ls                  # List networks
docker network inspect <network>   # Network details
```

### 30.2 Network Diagnostic Commands

```bash
# ═══════════════════════════════════════════════════════════════════════════════
# INTERFACE_INFORMATION
# ═══════════════════════════════════════════════════════════════════════════════
ip addr                            # Show interfaces
ip route                           # Show routing table

# ═══════════════════════════════════════════════════════════════════════════════
# CONNECTIVITY_TESTING
# ═══════════════════════════════════════════════════════════════════════════════
ping -c 4 <host>                   # ICMP ping
traceroute <host>                  # Trace route

# ═══════════════════════════════════════════════════════════════════════════════
# SOCKET_INFORMATION
# ═══════════════════════════════════════════════════════════════════════════════
ss -tulpn                          # TCP/UDP listening sockets
ss -tan                            # All TCP connections
```

---

## 31. Higher-Level Exercises (EVALUATE & CREATE)

### 31.1 EVALUATE Level Exercises

>  **PREDICTION:** What do you think are the most important criteria for choosing a load balancing algorithm?

#### E1. Security Audit (Weeks 7, 13)

**Task:** Conduct a security assessment of a provided Docker Compose setup.

**Deliverables:**
1. Identified vulnerabilities list
2. Risk assessment (High/Medium/Low)
3. Remediation recommendations
4. Improved `docker-compose.yml`

#### E2. Architecture Comparison (Weeks 8, 11)

**Task:** Compare and evaluate different load balancing strategies for a given scenario.

**Deliverables:**
1. Test methodology
2. Performance metrics
3. Recommendation with justification

### 31.2 CREATE Level Exercises

#### C1. Custom Protocol Design (Week 4)

**Task:** Design and implement a custom binary protocol for sensor data transmission.

**Requirements:**
- Header: message type, length, sequence number, checksum
- At least 3 message types
- Error detection
- Python implementation

**Deliverables:**
1. Protocol specification document
2. Server implementation
3. Client implementation
4. Test cases

#### C2. Microservices Application (Weeks 8, 11, 14)

**Task:** Create an original `docker-compose.yml` for a "URL Shortener" type application.

**Mandatory components:**
- API Gateway (Nginx) on port 8080
- 2 backend instances (Python/Flask or Node.js)
- Database (Redis or SQLite in volume)
- Health checks for all services

**Deliverables:**
1. Complete and functional `docker-compose.yml`
2. Backend source code
3. `README.md` with usage instructions
4. Architectural choices justification (1 page)

---

## 32. Live Coding Guide for Instructors

### 32.1 Basic Principles

Live coding is a teaching technique where the instructor writes code in front of students, explaining each step. It is **fundamentally different** from presenting pre-written code.

### 32.2 Live Coding Session Structure

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    LIVE CODING CYCLE (15-20 minutes)                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. CONTEXT (2 min)      Present the problem and objective                  │
│         │                                                                   │
│         ▼                                                                   │
│  2. STRUCTURE (2 min)    Sketch the general solution structure              │
│         │                                                                   │
│         ▼                                                                   │
│  3. INCREMENTAL          Write code in 2-5 line steps                       │
│     IMPLEMENTATION       ┌──────────────────────────────────────┐           │
│     (10-15 min)          │  a) Write 2-5 lines                  │           │
│                          │  b) ASK: "What will this display?"   │           │
│                          │  c) Run and verify                   │           │
│                          │  d) Repeat                           │           │
│                          └──────────────────────────────────────┘           │
│         │                                                                   │
│         ▼                                                                   │
│  4. RECAP (2 min)        Summarise what we built and why                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 32.3 Golden Rules

1. **MAKE MISTAKES INTENTIONALLY** — Make a mistake and show how to debug it
2. **ASK FOR PREDICTIONS** — Before each `python3 script.py`, ask "What will it display?"
3. **TALK WHILE TYPING** — Explain each line
4. **DON'T RUSH** — Better to cover less, but students understand
5. **USE COMMENTS** — Add explanatory comments on the spot

### 32.4 Example for Week 2 (TCP Socket)

```python
# STEP 1: "Let's create a simple TCP socket"
import socket

# QUESTION: "What socket type do we use for TCP?"
# Expected answer: SOCK_STREAM

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created!")

# RUN → verify output

# STEP 2: "Now let's connect to a server"
# QUESTION: "What happens if the server isn't running?"

sock.connect(('localhost', 8080))
print("Connected!")

# RUN → probably error! → DEBUG TOGETHER
```

### 32.5 Pre-Session Checklist

- [ ] Have I tested all the code beforehand?
- [ ] Have I prepared 2-3 intentional mistakes to demonstrate?
- [ ] Have I prepared prediction questions for each step?
- [ ] Is the terminal font large enough (min 18pt)?
- [ ] Have I disabled on-screen notifications?

---

## 33. FAQ — Frequently Asked Questions

### Installation and Configuration Issues

**Q: I get "Address already in use" when starting the laboratory.**

> **A:** Another process is already using the port. Identify and stop it:
> ```bash
> # Find the process
> ss -tulpn | grep <port>
> # Or on Windows
> netstat -ano | findstr <port>
> ```
> Then stop the process or change the port in `docker-compose.yml`.

**Q: Docker won't start in WSL. What do I do?**

> **A:** Start the service manually:
> ```bash
> sudo service docker start
> # Password: stud
> ```
> If it persists, verify WSL2 is configured correctly: `wsl --status`

**Q: Portainer won't open at http://localhost:9000.**

> **A:** Check if the Portainer container is running:
> ```bash
> docker ps | grep portainer
> ```
> If not running, start it:
> ```bash
> docker start portainer
> # Or recreate it per Section 7 instructions
> ```

**Q: I don't have disk space for Docker images.**

> **A:** Clean unused resources:
> ```bash
> docker system prune -a
> # WARNING: Deletes ALL unused images!
> ```

### Issues During Laboratories

**Q: Container starts but service doesn't respond.**

> **A:** Check container logs:
> ```bash
> docker logs <container_name>
> # Or in Portainer: click on container → Logs
> ```

**Q: Wireshark can't see traffic from containers.**

> **A:** In WSL, Docker traffic goes through the `docker0` interface or specific bridge. Use:
> ```bash
> # In Wireshark on Windows, select "Adapter for loopback traffic capture"
> # Or use tcpdump in WSL:
> sudo tcpdump -i any port <port> -w capture.pcap
> ```

**Q: How do I completely reset a laboratory?**

> **A:** Use the cleanup script:
> ```bash
> python3 scripts/cleanup.py --complete
> # Then restart:
> python3 scripts/start_lab.py --rebuild
> ```

### Conceptual Questions

**Q: What's the difference between Docker and a virtual machine?**

> **A:** Docker containers share the kernel with the host and are much lighter (~MB vs ~GB). VMs have their own kernel and offer complete isolation but with higher overhead.

**Q: Why do we use WSL2 and not Docker Desktop?**

> **A:** WSL2 offers:
> - Better performance (native Linux kernel)
> - Lower resource consumption
> - Complete configuration control
> - Transferable Linux skills
> - Completely free licensing

**Q: Is port 9000 for the laboratory?**

> **A:** **NO!** Port 9000 is **PERMANENTLY RESERVED** for Portainer. Laboratories use other ports (8080, 8081, 9090, etc.).

---

## 34. Licence

This project is licensed under a **Restrictive Educational Licence** (v5.0.0).

### Copyright Notice

**© 2019–2026 Antonio Clim, Andrei Toma. All rights reserved.**

The Materials are protected under Romanian law (Law No. 8/1996), EU Directive 2001/29/EC and applicable international treaties.

### Permitted Uses

| Permitted | Description |
|:---------:|-------------|
| ✓ | **Personal Study** — Viewing, reading and studying for your own educational benefit |
| ✓ | **Code Execution** — Running code examples on personal devices for learning purposes |
| ✓ | **Local Modification** — Modifying code locally for personal experimentation and learning |
| ✓ | **Personal Notes** — Creating derivative notes and annotations for personal reference only |
| ✓ | **Academic Citation** — Quoting brief excerpts in academic works with proper attribution |

### Prohibited Uses (without written consent)

| Prohibited | Description |
|:----------:|-------------|
| ✗ | **Publication** — Uploading, posting, publishing or sharing on any platform |
| ✗ | **Teaching** — Using in courses, workshops, seminars or training without authorisation |
| ✗ | **Presentation** — Presenting, demonstrating or displaying to audiences |
| ✗ | **Redistribution** — Distributing copies in any form, modified or not |
| ✗ | **Derivative Works** — Creating and distributing derivative works |
| ✗ | **Commercial Use** — Any commercial purpose |

### Educational Institution Licensing

Educational institutions wishing to incorporate these Materials into their curricula may apply for an institutional licence. Open an issue with the `[LICENCE]` tag for details.

### Attribution

When citing these Materials in academic works:

```
Clim, A., & Toma, A. (2026). Computer Networks — Complete Laboratory Kits 
(WSL Edition, v5.0.0). Bucharest University of Economic Studies.
https://github.com/antonioclim/netENwsl
```

**BibTeX Format:**

```bibtex
@misc{clim2026networks,
  author       = {Clim, Antonio and Toma, Andrei},
  title        = {{netENwsl}: Computer Networks — Complete Laboratory Kits},
  year         = {2026},
  version      = {5.0.0},
  institution  = {Bucharest University of Economic Studies},
  howpublished = {\url{https://github.com/antonioclim/netENwsl}},
  note         = {Educational curriculum materials for computer 
                  networks laboratory}
}
```

**Complete Licence:** [LICENCE.md](LICENCE.md)

**Disclaimer:** Materials are provided "AS IS" without warranty of any kind.

---

##  Good Luck! (or Break a leg?)

If you have followed this guide and configured the environment correctly, you are ready to:

- ✅ Run isolated network experiments with Docker containers
- ✅ Capture and analyse network traffic with Wireshark
- ✅ Manage containers through the Portainer web interface (http://localhost:9000)
- ✅ Automate network tasks with Python
- ✅ Understand in depth how network protocols work
- ✅ Avoid port conflicts (port 9000 = Portainer!)

---

##  Main Changes Summary (January 2026)

This document has been updated to reflect:

1. **Restrictive Educational Licence** — Replacing MIT with restrictive licence for materials protection
2. **Correct Attribution** — © 2019–2056 Antonio Clim, Andrei Toma
3. **18 PREDICTION Questions** — Prediction prompts for each week
4. **Two Separate Repositories** — netENwsl (English) and netROwsl (Romanian)
5. **Distinct Naming Conventions** — `<N>enWSL` vs `<NN>roWSL`
6. **Student Directory Structure** — `D:\NETWORKS\WEEK<N>\<N>enWSL`
7. **Port 9000 PERMANENTLY RESERVED** for Portainer
8. **Subgoal Labels** — Structured comments in code for pedagogy
9. **Specific Wireshark Filters** for each week
10. **BibTeX Format** for academic citations

---

> **© 2019–2056 Antonio Clim, Andrei Toma**  
> Computer Networks Laboratory — ASE Bucharest, CSIE  
> Documentation Version: January 2026
