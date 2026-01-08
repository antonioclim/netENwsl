# 🖧 Computer Networks – Laboratory Kits for WSL (WEEKS 1–14)

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-28.2.2+-2496ED?style=flat&logo=docker&logoColor=white)](https://docker.com)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04_LTS-E95420?style=flat&logo=ubuntu&logoColor=white)](https://ubuntu.com)
[![WSL](https://img.shields.io/badge/WSL-2.0-0078D6?style=flat&logo=windows&logoColor=white)](https://docs.microsoft.com/en-us/windows/wsl/)
[![Portainer](https://img.shields.io/badge/Portainer-2.33.6_LTS-13BEF9?style=flat&logo=portainer&logoColor=white)](https://portainer.io)
[![Wireshark](https://img.shields.io/badge/Wireshark-4.4.x-1679A7?style=flat&logo=wireshark&logoColor=white)](https://wireshark.org)
[![Licence](https://img.shields.io/badge/Licence-MIT-yellow?style=flat)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2025.1-blue?style=flat)]()

> **Complete Laboratory Materials for Computer Networks Course**  
> Bucharest University of Economic Studies (ASE) — Faculty of Cybernetics, Statistics and Economic Informatics (CSIE)  
> *Economic Informatics & AI in Economics and Business Programmes*

**Course Code:** 25.0205IF3.2-0003  
**Programme of Study:** Economic Informatics, Year III, Semester 2  
**Academic Year:** 2024–2025  
**Target Platform:** Windows Subsystem for Linux (WSL 2) with Ubuntu 22.04 LTS

---

## 📋 Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Standard Credentials](#standard-credentials)
- [Critical Port Reservation](#critical-port-reservation)
- [Features and Capabilities](#features-and-capabilities)
- [Repository Architecture](#repository-architecture)
- [Detailed Weekly Curriculum](#detailed-weekly-curriculum)
  - [Week 1: Computer Network Fundamentals](#week-1-computer-network-fundamentals)
  - [Week 2: Architectural Models and Socket Programming](#week-2-architectural-models-and-socket-programming)
  - [Week 3: Broadcast, Multicast and TCP Tunnelling](#week-3-broadcast-multicast-and-tcp-tunnelling)
  - [Week 4: Physical Layer, Data Link Layer and Custom Protocols](#week-4-physical-layer-data-link-layer-and-custom-protocols)
  - [Week 5: Network Layer – IPv4/IPv6 Addressing and Subnetting](#week-5-network-layer--ipv4ipv6-addressing-and-subnetting)
  - [Week 6: NAT/PAT, Support Protocols and SDN](#week-6-natpat-support-protocols-and-sdn)
  - [Week 7: Packet Capture and Filtering](#week-7-packet-capture-and-filtering)
  - [Week 8: Transport Layer – HTTP Server and Reverse Proxy](#week-8-transport-layer--http-server-and-reverse-proxy)
  - [Week 9: Session and Presentation Layers](#week-9-session-and-presentation-layers)
  - [Week 10: Application Layer – HTTPS, REST and Network Services](#week-10-application-layer--https-rest-and-network-services)
  - [Week 11: Application Protocols and Load Balancing](#week-11-application-protocols-and-load-balancing)
  - [Week 12: Email Protocols and Remote Procedure Call](#week-12-email-protocols-and-remote-procedure-call)
  - [Week 13: IoT and Network Security](#week-13-iot-and-network-security)
  - [Week 14: Integrated Review and Project Evaluation](#week-14-integrated-review-and-project-evaluation)
- [Standard Weekly Kit Structure](#standard-weekly-kit-structure)
- [System Requirements](#system-requirements)
- [Complete Installation Guide](#complete-installation-guide)
  - [Step 1: Enable WSL2](#step-1-enable-wsl2)
  - [Step 2: Install Ubuntu 22.04](#step-2-install-ubuntu-2204)
  - [Step 3: Install Docker in WSL](#step-3-install-docker-in-wsl)
  - [Step 4: Deploy Portainer CE (Global Service)](#step-4-deploy-portainer-ce-global-service)
  - [Step 5: Install Wireshark](#step-5-install-wireshark)
  - [Step 6: Install Python Packages](#step-6-install-python-packages)
  - [Step 7: Configure Auto-start](#step-7-configure-auto-start)
- [Repository Cloning](#repository-cloning)
- [Running Your First Laboratory](#running-your-first-laboratory)
- [Transversal IP Addressing Plan](#transversal-ip-addressing-plan)
- [Technologies and Tools](#technologies-and-tools)
- [Repository Statistics](#repository-statistics)
- [Code and Documentation Conventions](#code-and-documentation-conventions)
- [Complete Troubleshooting Guide](#complete-troubleshooting-guide)
- [Quick Reference Card](#quick-reference-card)
- [Supplementary Educational Resources](#supplementary-educational-resources)
- [Final Verification Checklist](#final-verification-checklist)
- [Authors and Contributors](#authors-and-contributors)
- [Licence](#licence)

---

## Overview

This repository contains **complete laboratory kits** for the **Computer Networks** course, organised across the 14 weeks of the academic semester. The materials are specifically designed for execution within the **Windows Subsystem for Linux (WSL 2)** environment with Ubuntu 22.04 LTS, providing students with a practical learning experience in an authentic Linux environment.

### What This Environment Enables

By completing the setup and using these materials, you will have a fully functional containerised environment capable of:

- **Running isolated network experiments** using Docker containers with consistent IP addressing
- **Capturing and analysing network traffic** with Wireshark on Windows via the `vEthernet (WSL)` interface
- **Managing containers visually** through Portainer's web interface at `http://localhost:9000`
- **Scripting network interactions** using Python with docker, scapy and requests libraries
- **Simulating complex network topologies** without affecting your host system

### Why WSL2 + Docker Engine (Not Docker Desktop)?

We use **WSL2 + Docker Engine inside Ubuntu** rather than Docker Desktop for several compelling reasons:

| Aspect | WSL2 + Docker Engine | Docker Desktop |
|--------|----------------------|----------------|
| **Performance** | Native Linux kernel, faster I/O | Virtualisation overhead |
| **Resource Usage** | Lighter memory footprint | Higher RAM consumption |
| **Network Access** | Full Linux networking stack | Abstracted networking |
| **Learning Value** | Real Linux environment | Windows abstraction |
| **Cost** | Completely free | Licensing for enterprises |
| **Wireshark Integration** | Direct capture on vEthernet (WSL) | Complex configuration |
| **Portainer Control** | Full container management | Limited in some cases |

### Pedagogical Philosophy

The kits follow a **progressive and integrated approach** to teaching computer networks:

1. **Learning through discovery** – each exercise guides students towards understanding through direct experimentation
2. **Transversal consistency** – all weeks utilise common conventions for IP addressing (10.0.N.0/24), ports and naming
3. **Complete automation** – Python scripts for setup, demonstration execution and automated testing
4. **Containerisation** – reproducible Docker environments that eliminate configuration issues
5. **Rich documentation** – theory, practical exercises, command cheat sheets and troubleshooting guides
6. **Visual management** – Portainer provides an intuitive web interface for container operations (global service on port 9000)

### Thematic Progression

The materials traverse the TCP/IP protocol stack from fundamentals to complex distributed applications:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              WEEKS 1-14                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  W1-W2    │  Foundations: diagnostics, TCP/UDP sockets, OSI/TCP-IP models  │
│  W3-W4    │  Broadcast/Multicast, tunnelling, custom protocols             │
│  W5-W6    │  IP addressing, VLSM subnetting, NAT/PAT, SDN                   │
│  W7-W8    │  Packet capture, filtering, HTTP, reverse proxy                │
│  W9-W10   │  Session/Presentation layers, FTP, REST, TLS, network services │
│  W11-W12  │  DNS, SSH, load balancing, email (SMTP), RPC/gRPC              │
│  W13-W14  │  IoT/MQTT, network security, integrated project                │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## System Architecture

### Architecture Diagram

Understanding how the components interact is essential for effective troubleshooting and learning:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              WINDOWS 10/11                                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │
│  │   Wireshark     │  │    Browser      │  │   PowerShell    │              │
│  │   (Capture on   │  │  (Portainer at  │  │   (WSL/Docker   │              │
│  │   vEthernet)    │  │  localhost:9000)│  │    commands)    │              │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘              │
│           │                    │                    │                       │
│           ▼                    ▼                    ▼                       │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │                vEthernet (WSL) - Virtual Network Interface              ││
│  │                      (Capture traffic here in Wireshark)                ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                    │                                        │
│  ┌─────────────────────────────────┴───────────────────────────────────────┐│
│  │                              WSL2                                        ││
│  │  ┌───────────────────────────────────────────────────────────────────┐  ││
│  │  │                      Ubuntu 22.04 LTS                              │  ││
│  │  │         Username: stud    |    Password: stud                      │  ││
│  │  │  ┌─────────────────────────────────────────────────────────────┐  │  ││
│  │  │  │                     Docker Engine                            │  │  ││
│  │  │  │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌─────────────┐  │  │  ││
│  │  │  │  │ Container │ │ Container │ │ Container │ │  Portainer  │  │  │  ││
│  │  │  │  │  Server   │ │  Client   │ │  Router   │ │   :9000     │  │  │  ││
│  │  │  │  │10.0.N.x   │ │10.0.N.x   │ │10.0.N.1   │ │  (GLOBAL)   │  │  │  ││
│  │  │  │  └───────────┘ └───────────┘ └───────────┘ └─────────────┘  │  │  ││
│  │  │  │              Docker Networks (weekN_net: 10.0.N.0/24)       │  │  ││
│  │  │  └─────────────────────────────────────────────────────────────┘  │  ││
│  │  └───────────────────────────────────────────────────────────────────┘  ││
│  └─────────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────┘
```

### Network Flow Explanation

1. **Docker containers** communicate through Docker's internal bridge network or custom networks (10.0.N.0/24 per week)
2. **Traffic exits** through the WSL2 virtual network interface (`vEthernet (WSL)`)
3. **Wireshark on Windows** captures all traffic on the `vEthernet (WSL)` interface
4. **Portainer** provides a web-based GUI accessible via `http://localhost:9000` from any Windows browser
5. **Port forwarding** automatically maps container ports to `localhost` on Windows

### Port Mapping Reference

| Service | Container Port | Host Port | Access URL | Notes |
|---------|---------------|-----------|------------|-------|
| **Portainer HTTP** | 9000 | **9000** | http://localhost:9000 | **⚠️ RESERVED - Global service** |
| Lab Web Servers | 80, 443 | 8080, 8443 | http://localhost:8080 | Per-week services |
| Lab Custom Services | Various | 9001-9099 | Varies by exercise | Available range |
| TCP Echo (Week 14) | 9090 | 9090 | nc localhost 9090 | Moved from 9000 |

---

## Standard Credentials

> ⚠️ **Critical:** Use these exact credentials for all laboratory exercises to ensure consistency across the course.

### Ubuntu WSL User

| Field | Value | Notes |
|-------|-------|-------|
| **Username** | `stud` | Created during Ubuntu installation |
| **Password** | `stud` | Has full `sudo` privileges |
| **Home Directory** | `/home/stud` | Store all lab materials here |

### Portainer Administrator

| Field | Value | Notes |
|-------|-------|-------|
| **Username** | `stud` | Create within 5 minutes of first access |
| **Password** | `studstudstud` | Minimum 12 characters required |
| **Access URL** | http://localhost:9000 | Open in any Windows browser |

> 📝 **Important:** Portainer requires a minimum 12-character password, which is why we use `studstudstud` (the word "stud" repeated three times).

### Summary Table

| Service | Username | Password | Access Method |
|---------|----------|----------|---------------|
| Ubuntu WSL | `stud` | `stud` | Terminal / PowerShell: `wsl` |
| Portainer | `stud` | `studstudstud` | Browser: http://localhost:9000 |

---

## Critical Port Reservation

> ⚠️ **EXTREMELY IMPORTANT: Port 9000 is ALWAYS RESERVED for Portainer**

### Why Port 9000 is Reserved

Portainer is deployed as a **global service** that runs independently of any weekly laboratory. It provides:

- Visual container management for all weeks
- Log viewing and debugging capabilities
- Network inspection tools
- Container statistics and monitoring

### Port Allocation Rules

| Port Range | Purpose | Notes |
|------------|---------|-------|
| **9000** | **Portainer (GLOBAL)** | **⚠️ NEVER use in docker-compose files** |
| 9001-9099 | Available for lab services | Safe to use in any week |
| 8080-8089 | HTTP services | Common for web servers |
| 1883, 8883 | MQTT (Week 13) | Plaintext and TLS |
| 9090 | TCP Echo (Week 14) | **Moved from 9000** |

### What Happens If Port 9000 Is Used?

If any laboratory service attempts to bind to port 9000:
- Portainer becomes inaccessible
- Students lose visual container management
- Troubleshooting becomes significantly harder
- The docker-compose stack may fail to start

### Weekly Scripts and Portainer

All weekly scripts (`start_lab.py`, `stop_lab.py`, `cleanup.py`) follow these rules:

- **NEVER** start Portainer (it runs globally)
- **NEVER** stop Portainer (it must remain available)
- **NEVER** remove the Portainer container or volume
- **ALWAYS** check Portainer status and display warnings if not running

---

## Features and Capabilities

### For Students

| Feature | Description |
|---------|-------------|
| **Zero manual configuration** | Automated scripts install all necessary dependencies |
| **Isolated environments** | Each laboratory runs in isolated Docker containers |
| **Graded exercises** | From beginner to advanced level within each week |
| **Automated tests** | Immediate verification of implemented solutions |
| **Structured homework** | Exercises with reference solutions for self-assessment |
| **Packet captures** | Pre-generated PCAP files for analysis |
| **Rich documentation** | Theory, command cheat sheets and troubleshooting guides |
| **Visual container management** | Portainer web interface at http://localhost:9000 |
| **Traffic analysis** | Wireshark integration via vEthernet (WSL) interface |
| **Consistent IP addressing** | 10.0.N.0/24 pattern makes learning intuitive |

### For Teaching Staff

| Feature | Description |
|---------|-------------|
| **Reproducible demonstrations** | `run_demo.py` script for classroom presentation |
| **Assessment flexibility** | Modular exercises adaptable to group level |
| **Complete theoretical materials** | Theoretical summaries and supplementary readings |
| **Progress monitoring** | Automated tests for competency verification |
| **Consistent environment** | All students have identical setups |
| **Global Portainer** | Always available for live demonstrations |

---

## Repository Architecture

```
netENwsl/
│
├── 00_Prerequisites/               # Prerequisites and environment setup
│   ├── PrerequisitesEN.md          # English installation guide
│   ├── PREREQUISITES_EN.html       # Interactive HTML version
│   └── wireshark_capture_example.png
│
├── 1enWSL/                         # Week 1: Network Fundamentals
├── 2enWSL/                         # Week 2: OSI/TCP-IP Models and Sockets
├── 3enWSL/                         # Week 3: Broadcast, Multicast, Tunnelling
├── 4enWSL/                         # Week 4: Physical/Data Link Layers
├── 5enWSL/                         # Week 5: IP Addressing, VLSM Subnetting
├── 6enWSL/                         # Week 6: NAT/PAT, ARP, DHCP, SDN
├── 7enWSL/                         # Week 7: Packet Capture and Filtering
├── 8enWSL/                         # Week 8: HTTP, Reverse Proxy, Load Balancing
├── 9enWSL/                         # Week 9: Session/Presentation Layers, FTP
├── 10enWSL/                        # Week 10: HTTPS, REST, DNS, SSH
├── 11enWSL/                        # Week 11: Advanced Application Protocols
├── 12enWSL/                        # Week 12: Email (SMTP) and RPC
├── 13enWSL/                        # Week 13: IoT (MQTT) and Security
├── 14enWSL/                        # Week 14: Integrated Review and Final Project
│
└── READMEen.md                     # This file
```

### Naming Convention

| Pattern | Example | Description |
|---------|---------|-------------|
| `<N>enWSL/` | `7enWSL/` | Week N laboratory kit (English) |
| `WEEK<N>/` | `WEEK7/` | Local clone directory on Windows |
| `week<N>_net` | `week7_net` | Docker network for week N |
| `week<N>_*` | `week7_lab` | Docker container names |

---

## Detailed Weekly Curriculum

### Week 1: Computer Network Fundamentals

**Network:** `10.0.1.0/24` | **Folder:** `1enWSL`

**Learning Objectives:**
- Identify network interfaces, IP addresses and routing tables using Linux utilities
- Explain the differences between TCP and UDP protocols regarding connection establishment and reliability
- Demonstrate basic network connectivity using ping, netcat and Python sockets
- Analyse captured network traffic using tcpdump, tshark and Wireshark

**Key Concepts:**
The laboratory session introduces fundamental computer networking concepts, focusing on diagnostic tools and analysis techniques essential for understanding network communication. Students gain hands-on experience with command-line network utilities, packet capture and socket programming paradigms. The TCP/IP stack is covered from a practical perspective, demonstrating how data traverses network layers and how various protocols can be observed, captured and analysed.

**Technologies:** `ping`, `traceroute`, `netstat`, `ss`, `tcpdump`, `netcat`, Python sockets

**Practical Exercises:**
1. Network interface enumeration and configuration analysis
2. TCP vs UDP communication comparison with Wireshark observation
3. Basic packet capture and protocol identification
4. Simple client-server socket implementation in Python

**Wireshark Focus:** Capture on `vEthernet (WSL)` interface, filter with `tcp`, `udp`, `icmp`

---

### Week 2: Architectural Models and Socket Programming

**Network:** `10.0.2.0/24` | **Folder:** `2enWSL`

**Learning Objectives:**
- Identify and enumerate the 7 layers of the OSI model and the 4 layers of the TCP/IP model
- Explain fundamental differences between TCP (connection-oriented, reliable) and UDP (connectionless, best-effort)
- Implement concurrent TCP servers and UDP servers with custom protocols
- Observe and analyse the TCP three-way handshake in Wireshark captures

**Key Concepts:**
This week explores the architectural foundations of computer networks, focusing on two essential models: the **OSI model** (Open Systems Interconnection) with its 7 layers and the **TCP/IP model** with 4 layers, which represents the practical foundation of the contemporary Internet. The practical component introduces **socket programming**, the fundamental mechanism through which applications communicate over networks.

**Technologies:** Python TCP/UDP sockets, `scapy`, multi-client servers, threading

**Practical Exercises:**
1. OSI vs TCP/IP layer mapping demonstration
2. Concurrent TCP echo server with threading
3. UDP message broadcast system
4. Custom protocol implementation over TCP

**Wireshark Focus:** TCP handshake observation (SYN, SYN-ACK, ACK), filter: `tcp.flags.syn==1`

---

### Week 3: Broadcast, Multicast and TCP Tunnelling

**Network:** `10.0.3.0/24` | **Folder:** `3enWSL`

**Learning Objectives:**
- Identify differences between unicast, broadcast and multicast communication at conceptual and practical levels
- Explain the IGMP mechanism for multicast group membership management and the role of TTL in packet propagation
- Implement broadcast and multicast applications using Python sockets
- Design and implement TCP tunnelling for transparent connection redirection

**Key Concepts:**
This laboratory session explores fundamental network communication mechanisms through socket programming: broadcast transmission, multicast communication and TCP tunnelling. **Broadcast** transmission allows a single sender to communicate simultaneously with all devices in a network segment. **Multicast** extends this concept by creating interest groups where only member stations receive traffic. **TCP tunnelling** provides transparent connection redirection mechanisms fundamental for proxies, load balancers and VPNs.

**Technologies:** UDP broadcast/multicast sockets, TTL multicast, Python port forwarding, Docker isolated networks

**Practical Exercises:**
1. Local network service discovery using broadcast
2. Multicast chat room implementation
3. TCP tunnel for port redirection
4. Traffic analysis in containerised environments

**Wireshark Focus:** IGMP packets, multicast addresses (224.x.x.x), filter: `igmp or ip.dst matches "224\\."`

---

### Week 4: Physical Layer, Data Link Layer and Custom Protocols

**Network:** `10.0.4.0/24` | **Folder:** `4enWSL`

**Learning Objectives:**
- Understand data transmission and signal encoding at the physical layer
- Implement error detection and correction at the frame level
- Design custom protocols: TEXT (human-readable), BINARY (efficient), UDP Sensor
- Utilise `struct` for binary serialisation and CRC32 for integrity verification

**Key Concepts:**
This session explores the lowest layers of the network stack. The **Physical Layer (L1)** handles signal transmission. The **Data Link Layer (L2)** provides framing, addressing and error detection. Students implement custom protocols demonstrating framing strategies and integrity verification.

**Technologies:** Binary protocols, Python `struct` module, CRC32, Ethernet frames, integrity validation

**Practical Exercises:**
1. TEXT protocol with length-based framing
2. BINARY protocol with fixed headers and CRC32 checksum
3. UDP sensor datagram with integrity validation
4. Protocol analyser implementation

**Wireshark Focus:** Ethernet frame structure, custom protocol bytes in hex view

---

### Week 5: Network Layer – IPv4/IPv6 Addressing and Subnetting

**Network:** `10.0.5.0/24` | **Folder:** `5enWSL`

**Learning Objectives:**
- Identify the role and functions of the Network Layer in OSI and TCP/IP architectures
- Explain differences between IPv4 and IPv6 addressing, including notation and structure
- Calculate subnets using FLSM (Fixed-Length Subnet Mask) and VLSM (Variable-Length Subnet Mask)
- Design efficient addressing schemes that minimise IP address wastage

**Key Concepts:**
This laboratory session explores the **Network Layer** of the TCP/IP model, focusing on fundamental addressing mechanisms that enable communication between devices in interconnected networks. Students examine both IPv4 and IPv6 architecture, understanding design principles, addressing schemes and subnetting techniques that underpin modern internet infrastructure.

**Technologies:** CIDR notation, FLSM, VLSM, IPv6, Python subnet calculators, Docker multi-segment networks

**Practical Exercises:**
1. IPv4 address classification and subnet identification
2. FLSM subnet design for a corporate network
3. VLSM optimisation for hierarchical addressing
4. IPv6 address configuration and verification

**Wireshark Focus:** IP header analysis, TTL field, fragmentation flags

---

### Week 6: NAT/PAT, Support Protocols and SDN

**Network:** `10.0.6.0/24` | **Folder:** `6enWSL`

**Learning Objectives:**
- Recall the purpose and classification of NAT variants (static, dynamic, PAT) and auxiliary protocols (ARP, DHCP, ICMP, NDP)
- Explain how PAT translation tables maintain bidirectional session state
- Configure iptables MASQUERADE rules on a Linux router
- Implement basic SDN flows using Open vSwitch and os-ken controller

**Key Concepts:**
This laboratory session integrates two complementary domains: address translation mechanisms (NAT/PAT) that support the extended lifecycle of IPv4 and software-defined networking (SDN) that decouples control logic from forwarding hardware. Students configure NAT using iptables and implement SDN flows using OpenFlow 1.3.

**Technologies:** `iptables`, Open vSwitch, `os-ken` controller, OpenFlow 1.3, ARP, DHCP, ICMP, NDP

**Practical Exercises:**
1. NAT/PAT configuration with iptables MASQUERADE
2. ARP cache analysis and manipulation
3. DHCP server and client interaction observation
4. Basic SDN flow installation with os-ken

**Wireshark Focus:** ARP request/reply, DHCP discover/offer/request/ack, filter: `arp or bootp`

---

### Week 7: Packet Capture and Filtering

**Network:** `10.0.7.0/24` | **Folder:** `7enWSL`

**Learning Objectives:**
- Identify key packet fields and their significance in TCP/UDP traffic captures
- Explain observable differences between REJECT and DROP behaviour in packet captures
- Implement filtering rules using iptables for traffic control
- Perform defensive port scanning and service enumeration

**Key Concepts:**
This laboratory session explores mechanisms for observing and controlling network traffic at the packet level. Students gain practical experience capturing traffic with tcpdump and tshark, implementing iptables rules and understanding the behavioural distinction between REJECT (sends ICMP error) and DROP (silent discard) actions.

**Technologies:** `tcpdump`, `tshark`, Wireshark, `nmap`, `scapy`, BPF filters, `iptables`

**Practical Exercises:**
1. Traffic capture with custom BPF filters
2. Firewall rule implementation (ACCEPT, DROP, REJECT)
3. Behavioural analysis of filtered connections
4. Defensive port scanning techniques with nmap

**Wireshark Focus:** ICMP destination unreachable (REJECT), TCP RST packets, filter: `icmp.type==3`

---

### Week 8: Transport Layer – HTTP Server and Reverse Proxy

**Network:** `10.0.8.0/24` | **Folder:** `8enWSL`

**Learning Objectives:**
- Identify key components of TCP and UDP protocols and their roles in network communication
- Explain the TCP connection establishment process (three-way handshake) and termination (four-way)
- Implement an HTTP/1.1 server from scratch using Python sockets
- Configure Nginx as a reverse proxy with load balancing algorithms

**Key Concepts:**
The transport layer represents the foundation of reliable communication between applications. This layer ensures data transfer between processes running on different hosts, providing multiplexing, demultiplexing and reliable data transfer with flow control. Students build an HTTP server from scratch and configure Nginx for load balancing.

**Technologies:** TCP handshake, HTTP/1.1 protocol, Nginx, load balancing (round-robin, least-connections), Docker Compose

**Practical Exercises:**
1. TCP three-way handshake observation and analysis
2. HTTP/1.1 server implementation with persistent connections
3. Nginx reverse proxy configuration
4. Load balancing algorithm comparison

**Wireshark Focus:** HTTP request/response, TCP sequence numbers, filter: `http or tcp.port==80`

---

### Week 9: Session and Presentation Layers

**Network:** `10.0.9.0/24` | **Folder:** `9enWSL`

**Learning Objectives:**
- Identify conceptual differences between TCP connection and application session
- Explain the role of L5 and L6 layers in the OSI protocol stack
- Implement a custom FTP server supporting active and passive modes
- Handle binary protocols with attention to byte ordering (endianness)

**Key Concepts:**
Week 9 explores the intermediate layers of the OSI model that bridge the transport layer (L4) and application protocols (L7). The Session Layer (L5) manages dialogue and synchronisation. The Presentation Layer (L6) handles data transformations: serialisation, encoding, compression and encryption.

**Technologies:** FTP protocol, `pyftpdlib`, binary protocols, message framing, endianness handling

**Practical Exercises:**
1. Session state management implementation
2. FTP server with active and passive mode support
3. Binary protocol with network byte order
4. Multi-client session handling

**Wireshark Focus:** FTP commands and responses, data channel establishment, filter: `ftp or ftp-data`

---

### Week 10: Application Layer – HTTPS, REST and Network Services

**Network:** `10.0.10.0/24` | **Folder:** `10enWSL`

**Learning Objectives:**
- Identify main components of HTTP request and response, including methods, headers and status codes
- Explain differences between HTTP and HTTPS, describing TLS role in securing communication
- Interact directly with network services: DNS, SSH and FTP
- Design and implement RESTful APIs following architectural principles

**Key Concepts:**
This laboratory session explores the **application layer** of the TCP/IP stack, focusing on protocols that support modern Internet communication. Students examine HTTP/HTTPS mechanisms, REST architectural principles and interact with essential services like DNS and SSH.

**Technologies:** TLS/SSL, DNS, SSH (`paramiko`), REST API, `requests`, `flask`, certificates

**Practical Exercises:**
1. HTTP request/response analysis and manipulation
2. TLS handshake observation and certificate verification
3. DNS query types and resolution process
4. RESTful API implementation with proper status codes

**Wireshark Focus:** TLS handshake, DNS queries, filter: `tls.handshake or dns`

---

### Week 11: Application Protocols and Load Balancing

**Network:** `10.0.11.0/24` | **Folder:** `11enWSL`

**Learning Objectives:**
- Understand FTP dual-connection architecture and passive mode for NAT traversal
- Explain DNS hierarchical architecture including resolvers and authoritative servers
- Implement SSH channel multiplexing and port forwarding
- Design load balancing algorithms in Python and Nginx

**Key Concepts:**
This laboratory explores application protocols and load balancing techniques. **FTP** uses dual-connection architecture. **DNS** functions as a hierarchical distributed database. **SSH** multiplexes logical channels over encrypted connections. **Load balancing** distributes traffic across backend servers.

**Technologies:** FTP active/passive modes, DNS recursive/authoritative, SSH tunnelling, Nginx upstream, health checks

**Practical Exercises:**
1. FTP passive mode implementation for NAT traversal
2. DNS caching resolver configuration
3. SSH port forwarding for secure tunnelling
4. Custom load balancer with health monitoring

**Wireshark Focus:** DNS recursion, SSH encrypted traffic pattern, filter: `dns.flags.response==0`

---

### Week 12: Email Protocols and Remote Procedure Call

**Network:** `10.0.12.0/24` (172.28.12.0/24 for internal services) | **Folder:** `12enWSL`

**Learning Objectives:**
- Identify components of SMTP transaction and recognise standard protocol commands
- Explain architectural differences between JSON-RPC, XML-RPC and gRPC
- Implement email sending functionality using SMTP dialogues
- Design RPC services using multiple paradigms

**Key Concepts:**
This session explores email protocols and RPC mechanisms. **SMTP** enables message transfer between mail servers using a command-response dialogue (EHLO, MAIL FROM, RCPT TO, DATA, QUIT). **RPC** allows programmes to invoke functions on remote systems. We examine JSON-RPC 2.0, XML-RPC and gRPC (using Protocol Buffers for binary serialisation).

**Technologies:** SMTP (port 1025), JSON-RPC 2.0 (port 6200), XML-RPC (port 6201), gRPC (port 6251), `protobuf`

**Practical Exercises:**
1. SMTP dialogue implementation with manual netcat session
2. JSON-RPC calculator service with batch operations
3. gRPC service with Protocol Buffers
4. RPC performance comparison (JSON vs XML vs gRPC)

**Wireshark Focus:** SMTP commands and three-digit status codes, RPC payload comparison, filter: `tcp.port == 1025` for SMTP, `tcp.port == 6200 && http` for JSON-RPC

---

### Week 13: IoT and Network Security

**Network:** `10.0.13.0/24` | **Folder:** `13enWSL`

**Learning Objectives:**
- Identify IoT architecture components and associated communication protocols
- Explain MQTT protocol operation, including QoS levels and topic structure
- Perform security assessment techniques: port scanning and vulnerability analysis
- Configure controlled testing environments for security exploration

**Key Concepts:**
This session explores the intersection of **IoT technologies** and **network security**. Students examine MQTT (Message Queuing Telemetry Transport) and understand device vulnerabilities. The lab includes intentionally vulnerable services (DVWA, vsftpd simulation) for safe security exploration.

**⚠️ Security Warning:** This week contains intentionally vulnerable services. Never expose to public networks.

**Technologies:** MQTT (`paho-mqtt`), Mosquitto broker (ports 1883/8883), `nmap`, port scanning, DVWA (port 8080), vsftpd (port 2121), backdoor stub (port 6200)

**Practical Exercises:**
1. MQTT publish/subscribe with plaintext and TLS transport
2. IoT sensor data aggregation system
3. Port scanning and service enumeration
4. Vulnerability assessment in controlled environment

**Wireshark Focus:** MQTT packets, TLS encrypted vs plaintext comparison, filter: `mqtt` or `tcp.port == 1883`

---

### Week 14: Integrated Review and Project Evaluation

**Networks:** `172.20.0.0/24` (backend), `172.21.0.0/24` (frontend) | **Folder:** `14enWSL`

**Learning Objectives:**
- Identify components of a load-balanced web architecture
- Explain round-robin distribution and reverse proxy communication
- Demonstrate usage of packet capture and analysis tools
- Analyse TCP/IP behaviour in client-server scenarios
- Build scripts for network service verification
- Evaluate distributed system performance

**Key Concepts:**
This session represents the culmination of the course, integrating concepts from all previous weeks. Students analyse, troubleshoot and optimise a complete distributed system with load balancing.

**⚠️ Important Port Change:** TCP Echo server runs on **port 9090** (not 9000, which is reserved for Portainer).

**Technologies:** Full-stack integration, multi-service Docker Compose, performance metrics, systematic troubleshooting

**Services:**
| Service | IP Address | Host Port |
|---------|------------|-----------|
| Load Balancer | 172.21.0.10 / 172.20.0.10 | 8080 |
| Backend 1 | 172.20.0.2 | 8001 |
| Backend 2 | 172.20.0.3 | 8002 |
| TCP Echo | 172.20.0.20 | **9090** |
| Client | 172.21.0.2 | - |

**Practical Exercises:**
1. Complete system deployment and verification
2. Load balancer behaviour analysis (round-robin)
3. TCP echo protocol testing
4. End-to-end traffic analysis with Wireshark

**Wireshark Focus:** HTTP with X-Backend header, TCP conversations, filter: `http contains "X-Backend"` or `tcp.port == 9090`

---

## Standard Weekly Kit Structure

Each `<N>enWSL/` directory follows a consistent and predictable organisation:

```
<N>enWSL/
│
├── README.md                 # Overview, objectives and quick start instructions
├── CHANGELOG.md              # Modification history
├── LICENSE                   # MIT Licence
│
├── docs/                     # Theoretical documentation and references
│   ├── theory_summary.md     # Core concepts for the current week
│   ├── commands_cheatsheet.md # Command and syntax quick reference
│   ├── troubleshooting.md    # Troubleshooting guide
│   └── further_reading.md    # Resources for further study
│
├── src/                      # Python source code
│   ├── exercises/            # Laboratory exercise implementations
│   │   ├── ex_01_*.py        # Exercise 1
│   │   ├── ex_02_*.py        # Exercise 2
│   │   └── ...
│   ├── apps/                 # Application implementations
│   │   └── *.py
│   └── utils/                # Shared utility modules
│       ├── __init__.py
│       └── net_utils.py
│
├── homework/                 # Individual work assignments
│   ├── README.md             # Assignment descriptions and requirements
│   ├── exercises/            # Problem statements and starter templates
│   └── solutions/            # Reference solutions (optional)
│
├── docker/                   # Containerisation and orchestration
│   ├── Dockerfile            # Docker image for laboratory environment
│   ├── docker-compose.yml    # Multi-container orchestration (NO Portainer!)
│   ├── configs/              # Service configuration files
│   └── volumes/              # Persistent data volumes
│
├── scripts/                  # Automation scripts (Python)
│   ├── start_lab.py          # Start laboratory environment
│   ├── stop_lab.py           # Stop laboratory environment
│   ├── run_demo.py           # Execute all demonstrations
│   ├── capture_traffic.py    # Traffic capture automation
│   ├── cleanup.py            # Clean generated files
│   └── utils/                # Script utilities
│
├── setup/                    # Environment configuration
│   ├── install_prerequisites.py  # Prerequisite installation
│   ├── configure_docker.py       # Docker configuration
│   ├── verify_environment.py     # Environment verification
│   └── requirements.txt          # Python dependencies
│
├── tests/                    # Automated testing
│   ├── test_environment.py   # Environment tests
│   ├── test_exercises.py     # Exercise tests
│   ├── smoke_test.py         # Quick smoke tests
│   └── expected_outputs.md   # Expected output reference
│
├── pcap/                     # Packet capture files
│   ├── README.md             # Capture descriptions
│   └── *.pcap                # Pre-generated captures for analysis
│
└── artifacts/                # Generated results (logs, captures)
    └── .gitkeep
```

### Directory Purposes

| Directory | Purpose |
|-----------|---------|
| `docs/` | All theoretical and reference materials for the week |
| `src/` | Production-quality Python implementations |
| `homework/` | Student assignments with optional solutions |
| `docker/` | Complete containerised environment (**excludes Portainer**) |
| `scripts/` | Automation for setup, execution and cleanup |
| `setup/` | One-time environment configuration |
| `tests/` | Automated verification of exercises |
| `pcap/` | Pre-captured network traffic for Wireshark analysis |
| `artifacts/` | Runtime-generated files (excluded from git) |

### Important: docker-compose.yml Rules

Every `docker-compose.yml` in this repository follows these rules:

1. **NO Portainer service definition** – Portainer runs globally
2. **NO port 9000 usage** – Reserved for Portainer
3. **Comments explaining** that Portainer runs separately
4. **Week-specific networks** using `10.0.N.0/24` pattern

---

## System Requirements

### Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 8 GB | 16 GB |
| CPU Cores | 2 | 4+ |
| Disc Space | 30 GB | 50 GB |
| Architecture | x64 with virtualisation | x64 with VT-x/AMD-V |

### Software Requirements

| Software | Version | Purpose |
|----------|---------|---------|
| **Windows** | 10 (Build 2004+) or 11 | Host operating system |
| **WSL** | 2.x | Windows Subsystem for Linux |
| **Ubuntu** | 22.04 LTS | Linux distribution |
| **Docker Engine** | 28.2.2+ | Container runtime (in WSL) |
| **Docker Compose** | 2.x+ | Multi-container orchestration |
| **Portainer CE** | 2.33.6 LTS | Web-based container management (port 9000) |
| **Wireshark** | 4.4.x | Network protocol analyser |
| **Python** | 3.11+ | Programming language |

### Component Versions Summary

| Component | Version | Status Check Command |
|-----------|---------|---------------------|
| WSL2 | 2.x | `wsl --status` |
| Ubuntu | 22.04 LTS | `lsb_release -a` |
| Docker | 28.2.2 | `docker --version` |
| Docker Compose | 2.x | `docker compose version` |
| Portainer | 2.33.6 LTS | http://localhost:9000 |
| Wireshark | 4.4.x | Windows application |
| Python | 3.11+ | `python3 --version` |

### Time Estimate for Setup

- **Total installation time:** 30-45 minutes
- **Requires restart:** Yes (after WSL2 installation)
- **Internet connection:** Required for all downloads

---

## Complete Installation Guide

### Step 1: Enable WSL2

#### What is WSL2?

**Windows Subsystem for Linux 2 (WSL2)** is a compatibility layer that runs a genuine Linux kernel directly on Windows. Unlike WSL1, WSL2 runs a full Linux kernel in a lightweight virtual machine, providing complete system call compatibility and dramatically improved file system performance.

#### Prerequisites Check

Before installing, verify your system:

```powershell
# Check Windows version (requires Build 19041 or higher)
winver

# Check virtualisation support
systeminfo | findstr /i "Hyper-V"
```

#### Installation Steps

**Step 1.1:** Open PowerShell as Administrator

1. Press `Win + X` or right-click the Start button
2. Select **"Windows Terminal (Admin)"** or **"PowerShell (Admin)"**
3. Click **"Yes"** on the User Account Control prompt

**Step 1.2:** Install WSL2

```powershell
wsl --install
```

This command:
- Enables the WSL optional feature
- Enables the Virtual Machine Platform feature
- Downloads and installs the Linux kernel
- Sets WSL2 as the default version

**Step 1.3:** Restart Your Computer

> ⚠️ **A restart is required.** Save all your work before proceeding.

```powershell
Restart-Computer
```

**Step 1.4:** Verify Installation

After restart, open PowerShell and verify:

```powershell
wsl --status
```

**Expected output:**
```
Default Distribution: Ubuntu
Default Version: 2

Windows Subsystem for Linux was last updated on [date]
WSL automatic updates are on.

Kernel version: 5.15.x.x-microsoft-standard-WSL2
```

---

### Step 2: Install Ubuntu 22.04

#### Why Ubuntu 22.04 LTS?

- **Long Term Support (LTS):** Security updates until April 2027
- **Stability:** Thoroughly tested, production-ready packages
- **Compatibility:** Excellent Docker support
- **Community:** Largest Linux community for troubleshooting

#### Installation Steps

**Step 2.1:** Install Ubuntu from PowerShell (as Administrator)

```powershell
wsl --install -d Ubuntu-22.04 --web-download
```

**Step 2.2:** Create User Account

> ⚠️ **Critical:** Use the standard credentials!

When prompted:
```
Enter new UNIX username: stud
New password: stud
Retype new password: stud
```

**Note:** The password will not display as you type—this is normal Linux security behaviour.

**Step 2.3:** Verify Installation

```powershell
wsl -l -v
```

**Expected output:**
```
  NAME            STATE           VERSION
* Ubuntu-22.04    Running         2
```

---

### Step 3: Install Docker in WSL

#### Step 3.1: Update System Packages

Open Ubuntu terminal (type `wsl` in PowerShell or search for "Ubuntu" in Start menu):

```bash
sudo apt update && sudo apt upgrade -y
```

Enter password `stud` when prompted.

#### Step 3.2: Install Prerequisites

```bash
sudo apt install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    software-properties-common
```

#### Step 3.3: Add Docker Repository

```bash
# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

#### Step 3.4: Install Docker Engine

```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

#### Step 3.5: Configure Docker for Non-Root Usage

```bash
# Add your user to docker group
sudo usermod -aG docker $USER

# Apply group changes immediately
newgrp docker
```

#### Step 3.6: Start Docker Service

```bash
sudo service docker start
```

#### Step 3.7: Verify Installation

```bash
docker --version
docker run hello-world
```

**Expected output:** Docker version information followed by "Hello from Docker!" message.

---

### Step 4: Deploy Portainer CE (Global Service)

Portainer provides a web-based GUI for managing Docker containers, making it easier to visualise and control your laboratory environment.

> ⚠️ **Critical:** Portainer is deployed ONCE and runs GLOBALLY on port 9000. It is NOT included in any weekly docker-compose files.

#### Step 4.1: Create Portainer Volume

```bash
docker volume create portainer_data
```

#### Step 4.2: Deploy Portainer Container

```bash
docker run -d \
    -p 9000:9000 \
    --name portainer \
    --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v portainer_data:/data \
    portainer/portainer-ce:latest
```

#### Step 4.3: Access Portainer

1. Open a web browser on Windows
2. Navigate to: **http://localhost:9000**
3. Create administrator account:
   - **Username:** `stud`
   - **Password:** `studstudstud`

> ⚠️ **Important:** You must create the admin account within **5 minutes** of first access, or Portainer will lock itself for security reasons.

#### Step 4.4: Connect to Local Docker

1. After logging in, select **"Get Started"**
2. Click on **"local"** environment
3. You should see your running containers

#### Step 4.5: Verify Portainer

```bash
docker ps | grep portainer
```

**Expected:** Portainer container running with port 9000 exposed.

#### Why Portainer is Global

| Aspect | Explanation |
|--------|-------------|
| **Single instance** | One Portainer manages all weeks' containers |
| **Persistent** | Survives weekly lab restarts |
| **Port 9000** | Always available at http://localhost:9000 |
| **Never stopped** | Weekly scripts never touch Portainer |

---

### Step 5: Install Wireshark

Wireshark is installed on **Windows** (not in WSL) to capture traffic on the virtual network interface.

#### Step 5.1: Download Wireshark

1. Visit: https://www.wireshark.org/download.html
2. Download the **Windows x64 Installer**
3. Run the installer

#### Step 5.2: Installation Options

During installation, ensure these options are selected:

- ☑️ **Wireshark** (main application)
- ☑️ **TShark** (command-line version)
- ☑️ **Plugins & Extensions**
- ☑️ **Npcap** (packet capture driver) — **Essential!**

#### Step 5.3: Npcap Installation

When the Npcap installer appears, select:

- ☑️ **Install Npcap in WinPcap API-compatible Mode**
- ☑️ **Support raw 802.11 traffic**

#### Step 5.4: Verify Wireshark

1. Launch Wireshark from Start menu
2. Look for **"vEthernet (WSL)"** in the interface list
3. This is the interface where you will capture Docker traffic

#### Step 5.5: Test Capture

1. Start capture on **vEthernet (WSL)**
2. In Ubuntu terminal, run:
   ```bash
   docker run --rm alpine ping -c 5 8.8.8.8
   ```
3. In Wireshark, apply filter: `icmp`
4. Verify you see ICMP Echo Request and Reply packets

---

### Step 6: Install Python Packages

Python packages are installed in WSL for scripting network interactions.

#### Step 6.1: Install Required Packages

In Ubuntu terminal:

```bash
pip install docker requests flask paramiko pyftpdlib paho-mqtt dnspython grpcio grpcio-tools protobuf colorama psutil pyyaml --break-system-packages
```

#### Step 6.2: Verify Python Integration

```bash
python3 -c "import docker; c = docker.from_env(); print(f'Containers: {len(c.containers.list())}')"
```

**Expected:** `Containers: 1` (or more, depending on running containers)

---

### Step 7: Configure Auto-start

Configure Docker to start automatically when you open Ubuntu.

#### Step 7.1: Edit .bashrc

```bash
nano ~/.bashrc
```

Add these lines at the end:

```bash
# Auto-start Docker service
if service docker status 2>&1 | grep -q "is not running"; then
    sudo service docker start
fi
```

Save with `Ctrl+O`, `Enter`, then exit with `Ctrl+X`.

#### Step 7.2: Configure Passwordless Docker Start

```bash
# Create sudoers entry
echo "stud ALL=(ALL) NOPASSWD: /usr/sbin/service docker start" | sudo tee /etc/sudoers.d/docker-start

# Set correct permissions
sudo chmod 440 /etc/sudoers.d/docker-start
```

#### Step 7.3: Test Auto-start

```powershell
# In PowerShell, shutdown WSL completely
wsl --shutdown

# Reopen Ubuntu
wsl

# Docker should start automatically
docker ps
```

---

## Repository Cloning

### Student's Local Directory Structure

Students should organise their work in a dedicated directory on Windows:

```
D:\NETWORKING\
├── WEEK1\          ← Contains cloned 1enWSL content
├── WEEK2\          ← Contains cloned 2enWSL content
├── WEEK3\          ← Contains cloned 3enWSL content
...
└── WEEK14\         ← Contains cloned 14enWSL content
```

### Cloning Individual Weeks (Recommended)

For each week N, run in PowerShell:

```powershell
# Create networking folder if it doesn't exist
mkdir D:\NETWORKING -ErrorAction SilentlyContinue
cd D:\NETWORKING

# Clone specific week
git clone https://github.com/antonioclim/netENwsl.git WEEK<N>
cd WEEK<N>
```

### Specific Week Cloning Commands

#### Week 1
```powershell
cd D:\NETWORKING
git clone https://github.com/antonioclim/netENwsl.git WEEK1
cd WEEK1\1enWSL
```

#### Week 2
```powershell
cd D:\NETWORKING
git clone https://github.com/antonioclim/netENwsl.git WEEK2
cd WEEK2\2enWSL
```

#### Week 3
```powershell
cd D:\NETWORKING
git clone https://github.com/antonioclim/netENwsl.git WEEK3
cd WEEK3\3enWSL
```

#### Week 4
```powershell
cd D:\NETWORKING
git clone https://github.com/antonioclim/netENwsl.git WEEK4
cd WEEK4\4enWSL
```

#### Week 5
```powershell
cd D:\NETWORKING
git clone https://github.com/antonioclim/netENwsl.git WEEK5
cd WEEK5\5enWSL
```

#### Week 6
```powershell
cd D:\NETWORKING
git clone https://github.com/antonioclim/netENwsl.git WEEK6
cd WEEK6\6enWSL
```

#### Week 7
```powershell
cd D:\NETWORKING
git clone https://github.com/antonioclim/netENwsl.git WEEK7
cd WEEK7\7enWSL
```

#### Week 8
```powershell
cd D:\NETWORKING
git clone https://github.com/antonioclim/netENwsl.git WEEK8
cd WEEK8\8enWSL
```

#### Week 9
```powershell
cd D:\NETWORKING
git clone https://github.com/antonioclim/netENwsl.git WEEK9
cd WEEK9\9enWSL
```

#### Week 10
```powershell
cd D:\NETWORKING
git clone https://github.com/antonioclim/netENwsl.git WEEK10
cd WEEK10\10enWSL
```

#### Week 11
```powershell
cd D:\NETWORKING
git clone https://github.com/antonioclim/netENwsl.git WEEK11
cd WEEK11\11enWSL
```

#### Week 12
```powershell
cd D:\NETWORKING
git clone https://github.com/antonioclim/netENwsl.git WEEK12
cd WEEK12\12enWSL
```

#### Week 13
```powershell
cd D:\NETWORKING
git clone https://github.com/antonioclim/netENwsl.git WEEK13
cd WEEK13\13enWSL
```

#### Week 14
```powershell
cd D:\NETWORKING
git clone https://github.com/antonioclim/netENwsl.git WEEK14
cd WEEK14\14enWSL
```

### Accessing from WSL

After cloning, access the week's directory from WSL:

```bash
cd /mnt/d/NETWORKING/WEEK<N>/<N>enWSL
```

For example, Week 7:
```bash
cd /mnt/d/NETWORKING/WEEK7/7enWSL
```

---

## Running Your First Laboratory

### Step 1: Navigate to Week Directory

```bash
# In Ubuntu terminal
cd /mnt/d/NETWORKING/WEEK1/1enWSL
```

### Step 2: Install Python Dependencies

```bash
pip install -r setup/requirements.txt --break-system-packages
```

### Step 3: Verify Environment

```bash
python3 setup/verify_environment.py
```

This checks:
- WSL2 is running
- Docker is available
- Portainer is running on port 9000
- Wireshark is installed
- Required Python packages are present

### Step 4: Start Laboratory

```bash
python3 scripts/start_lab.py
```

This:
- Starts Docker if not running
- Checks Portainer status (but never starts it)
- Builds and starts week-specific containers
- Displays access URLs

### Step 5: Run Demonstrations

```bash
python3 scripts/run_demo.py
```

### Step 6: Capture Traffic in Wireshark

1. Open Wireshark on Windows
2. Select **vEthernet (WSL)** interface
3. Start capture
4. Apply relevant filters (e.g., `tcp`, `http`, `icmp`)

### Step 7: Stop Laboratory

```bash
python3 scripts/stop_lab.py
```

This:
- Stops week-specific containers
- **Never** stops Portainer
- Confirms Portainer is still running

### Step 8: Clean Up

```bash
python3 scripts/cleanup.py --full
```

This:
- Removes week-specific containers and networks
- Cleans artifact files
- **Never** removes Portainer

---

## Transversal IP Addressing Plan

All weekly kits follow a consistent IP addressing scheme to facilitate learning and troubleshooting:

### Per-Week Network Ranges

| Week | Network CIDR | Docker Network Name |
|------|--------------|---------------------|
| 1 | `10.0.1.0/24` | `week1_net` |
| 2 | `10.0.2.0/24` | `week2_net` |
| 3 | `10.0.3.0/24` | `week3_net` |
| 4 | `10.0.4.0/24` | `week4_net` |
| 5 | `10.0.5.0/24` | `week5_net` |
| 6 | `10.0.6.0/24` | `week6_net` |
| 7 | `10.0.7.0/24` | `week7_net` |
| 8 | `10.0.8.0/24` | `week8_net` |
| 9 | `10.0.9.0/24` | `week9_net` |
| 10 | `10.0.10.0/24` | `week10_net` |
| 11 | `10.0.11.0/24` | `week11_net` |
| 12 | `10.0.12.0/24` / `172.28.12.0/24` | `week12_net` |
| 13 | `10.0.13.0/24` | `week13net` |
| 14 | `172.20.0.0/24` + `172.21.0.0/24` | `week14_backend_net` + `week14_frontend_net` |

### Standard Container Addressing Pattern

Within each week's `10.0.N.0/24` network:

| Container Role | IP Address Pattern | Example (Week 7) |
|----------------|-------------------|------------------|
| Gateway | `10.0.N.1` | `10.0.7.1` |
| Primary Server | `10.0.N.10` | `10.0.7.10` |
| Secondary Server | `10.0.N.11` | `10.0.7.11` |
| Client | `10.0.N.100` | `10.0.7.100` |
| Special Service | `10.0.N.20+` | `10.0.7.20` |

### Port Allocation Conventions

| Port Range | Service Category | Notes |
|------------|------------------|-------|
| **9000** | **Portainer (GLOBAL)** | **⚠️ NEVER use in labs** |
| 8080-8089 | HTTP application servers | Common for web servers |
| 8001-8002 | Backend services | Week 14 backends |
| 9001-9099 | Available lab services | Safe to use |
| 9090 | TCP Echo (Week 14) | Moved from 9000 |
| 1883, 8883 | MQTT | Week 13 |
| 1025 | SMTP | Week 12 |
| 6200-6251 | RPC services | Week 12 |

---

## Technologies and Tools

### Core Components

| Component | Version | Purpose |
|-----------|---------|---------|
| **WSL2** | 2.x | Windows Subsystem for Linux |
| **Ubuntu** | 22.04 LTS | Linux distribution |
| **Docker Engine** | 28.2.2 | Container runtime |
| **Docker Compose** | 2.x | Multi-container orchestration |
| **Portainer CE** | 2.33.6 LTS | Web-based container management |
| **Wireshark** | 4.4.x | Network protocol analyser |

### Programming Languages

| Language | Usage |
|----------|-------|
| **Python 3.11+** | Primary implementation language |
| **Bash** | System automation |
| **YAML** | Docker Compose configuration |
| **Protocol Buffers** | gRPC service definitions (Week 12) |

### Network Analysis Tools

| Tool | Platform | Purpose |
|------|----------|---------|
| **Wireshark** | Windows | GUI packet analysis |
| **tcpdump** | Ubuntu/WSL | Command-line capture |
| **tshark** | Ubuntu/WSL | Terminal-based Wireshark |
| **nmap** | Ubuntu/WSL | Port scanning |
| **netcat** | Ubuntu/WSL | TCP/UDP utility |

### Python Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| **docker** | 7.1.0+ | Docker API |
| **requests** | Latest | HTTP client |
| **flask** | Latest | Web framework |
| **paramiko** | Latest | SSH client |
| **pyftpdlib** | Latest | FTP server |
| **paho-mqtt** | Latest | MQTT client |
| **dnspython** | Latest | DNS library |
| **grpcio** | Latest | gRPC framework |

---

## Repository Statistics

| Metric | Value |
|--------|-------|
| **Weekly Kits** | 14 |
| **Total ZIP Size** | ~1.2 MB |
| **Docker Compose Files** | 14 |
| **Python Exercise Files** | 50+ |
| **Documentation Pages** | 70+ |

### Per-Week Statistics (Average)

| Metric | Value |
|--------|-------|
| Python exercises | 3-5 |
| Documentation pages | 4-5 |
| Docker services | 2-5 |
| Test files | 3-4 |
| ZIP size | ~85-130 KB |

---

## Code and Documentation Conventions

### Python Code Style

```python
#!/usr/bin/env python3
"""
Module description.

Course: Computer Networks - ASE, Economic Informatics
Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment
"""

import standard_library
import third_party_library
import local_module

# Constants in UPPER_SNAKE_CASE
DEFAULT_PORT = 8080
PORTAINER_PORT = 9000  # RESERVED - never use

def function_name(parameter: str, optional: int = 10) -> bool:
    """
    Function description.
    
    Args:
        parameter: Description of parameter
        optional: Description with default value
        
    Returns:
        Description of return value
    """
    pass


class ClassName:
    """Class description."""
    
    def __init__(self, value: str) -> None:
        """Initialise instance."""
        self.value = value
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Weekly directories | `<N>enWSL/` | `7enWSL/` |
| Exercise files | `ex_<NN>_<topic>.py` | `ex_01_broadcast.py` |
| Test files | `test_<module>.py` | `test_exercises.py` |
| Docker services | `week<N>_<role>` | `week7_server` |
| Networks | `week<N>_net` | `week7_net` |
| Scripts | `<action>_lab.py` | `start_lab.py` |

---

## Complete Troubleshooting Guide

### WSL Issues

#### "WSL 2 requires an update to its kernel component"

```powershell
wsl --update
```

#### "Please enable the Virtual Machine Platform Windows feature"

```powershell
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```
Restart computer after.

#### WSL won't start

```powershell
# Reset WSL
wsl --shutdown
wsl
```

#### WSL is very slow

Store projects in `/mnt/d/NETWORKING/`, not `/mnt/c/Users/...`. The Windows filesystem through WSL has overhead, but D: drive is typically faster than user folders.

---

### Docker Issues

#### "Cannot connect to the Docker daemon"

```bash
# Start Docker service
sudo service docker start

# Check if dockerd is running
ps aux | grep dockerd
```

#### "Permission denied while trying to connect to Docker daemon socket"

```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Apply changes (or log out and back in)
newgrp docker
```

#### Container not starting

```bash
# Check container logs
docker logs <container_name>

# Check if port is already in use
sudo ss -tulpn | grep <port>
```

---

### Portainer Issues

#### Can't access http://localhost:9000

1. Check if container is running:
   ```bash
   docker ps | grep portainer
   ```

2. If not running, start it:
   ```bash
   docker start portainer
   ```

3. If doesn't exist, create it:
   ```bash
   docker run -d -p 9000:9000 --name portainer --restart=always \
       -v /var/run/docker.sock:/var/run/docker.sock \
       -v portainer_data:/data portainer/portainer-ce:latest
   ```

#### "Portainer has been initialised already" (missed 5-minute window)

```bash
# Remove Portainer and volume
docker stop portainer
docker rm portainer
docker volume rm portainer_data

# Redeploy
docker volume create portainer_data
docker run -d -p 9000:9000 --name portainer --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v portainer_data:/data portainer/portainer-ce:latest
```

Then access http://localhost:9000 and create admin account (`stud`/`studstudstud`) within 5 minutes.

---

### Wireshark Issues

#### No interfaces visible

- Ensure Npcap is installed
- Run Wireshark as Administrator
- Reinstall Npcap from https://npcap.com/

#### "vEthernet (WSL)" not showing

- WSL must be running
- Try: `wsl` in PowerShell, then restart Wireshark

#### No traffic captured

- Ensure capture is on correct interface (`vEthernet (WSL)`)
- Generate traffic: `docker run --rm alpine ping -c 3 8.8.8.8`
- Check display filter isn't too restrictive

---

### Python Issues

#### "Module not found"

```bash
pip install <module> --break-system-packages
```

---

### Network Issues

#### Cannot ping container

```bash
# Verify container is running
docker ps

# Check container network
docker inspect <container> | grep IPAddress

# Verify network exists
docker network ls
```

---

## Quick Reference Card

### Essential Commands

```bash
# ═══════════════════════════════════════════════════════════
# WSL Management (PowerShell)
# ═══════════════════════════════════════════════════════════
wsl --status              # Check WSL status
wsl --shutdown            # Stop all WSL instances
wsl                       # Open default distribution
wsl -l -v                 # List distributions with versions

# ═══════════════════════════════════════════════════════════
# Docker (Ubuntu Terminal)
# ═══════════════════════════════════════════════════════════
sudo service docker start # Start Docker daemon
docker ps                 # List running containers
docker ps -a              # List all containers
docker images             # List images
docker logs <name>        # View container logs
docker exec -it <name> sh # Shell into container
docker stop <name>        # Stop container
docker rm <name>          # Remove container
docker network ls         # List networks
docker volume ls          # List volumes

# ═══════════════════════════════════════════════════════════
# Laboratory Scripts (in week directory)
# ═══════════════════════════════════════════════════════════
python3 scripts/start_lab.py        # Start lab environment
python3 scripts/stop_lab.py         # Stop lab environment
python3 scripts/run_demo.py         # Run demonstrations
python3 scripts/cleanup.py          # Clean up files
python3 setup/verify_environment.py # Verify environment

# ═══════════════════════════════════════════════════════════
# Portainer (Global - Never touch in lab scripts!)
# ═══════════════════════════════════════════════════════════
docker start portainer    # Start Portainer if stopped
# Access: http://localhost:9000
# Credentials: stud / studstudstud
```

### Important URLs

| Service | URL |
|---------|-----|
| Portainer | http://localhost:9000 |
| Repository | https://github.com/antonioclim/netENwsl |
| Docker Docs | https://docs.docker.com/ |
| Wireshark Docs | https://www.wireshark.org/docs/ |
| WSL Docs | https://learn.microsoft.com/en-us/windows/wsl/ |

### Credentials Summary

| Service | Username | Password |
|---------|----------|----------|
| Ubuntu WSL | `stud` | `stud` |
| Portainer | `stud` | `studstudstud` |

### Common Wireshark Filters

| Filter | Purpose |
|--------|---------|
| `tcp` | All TCP traffic |
| `udp` | All UDP traffic |
| `icmp` | Ping packets |
| `http` | HTTP traffic |
| `tls` | TLS/SSL traffic |
| `dns` | DNS queries |
| `tcp.port==8080` | HTTP port |
| `ip.addr==10.0.7.10` | Specific IP |
| `tcp.flags.syn==1` | TCP SYN packets |
| `mqtt` | MQTT protocol |
| `ftp or ftp-data` | FTP traffic |
| `tcp.port==9090` | TCP Echo (Week 14) |

---

## Supplementary Educational Resources

### Official Documentation

| Resource | URL |
|----------|-----|
| Python Documentation | https://docs.python.org/3/ |
| Docker Documentation | https://docs.docker.com/ |
| Wireshark User Guide | https://www.wireshark.org/docs/ |
| RFC Repository | https://www.rfc-editor.org/ |

### Recommended Reading

| Topic | Resource |
|-------|----------|
| TCP/IP Fundamentals | *TCP/IP Illustrated* by W. Richard Stevens |
| Network Programming | *Foundations of Python Network Programming* by Rhodes & Goetzen |
| Computer Networks | *Computer Networking: A Top-Down Approach* by Kurose & Ross |
| Network Security | *Cryptography and Network Security* by William Stallings |
| Protocol Analysis | *Practical Packet Analysis* by Chris Sanders |

### Practice Platforms

| Platform | Purpose |
|----------|---------|
| HackTheBox | Security and networking challenges |
| TryHackMe | Guided cybersecurity learning |
| OverTheWire | Command-line and networking wargames |

---

## Final Verification Checklist

Run through this checklist to confirm your environment is properly configured:

### WSL and Ubuntu

- [ ] `wsl --status` shows "Default Version: 2"
- [ ] `wsl -l -v` shows Ubuntu-22.04 with VERSION 2
- [ ] Can login with username `stud` and password `stud`

### Docker

- [ ] `docker --version` shows 28.2.2 or higher
- [ ] `docker compose version` shows 2.x or higher
- [ ] `docker ps` works without sudo
- [ ] `docker run hello-world` succeeds

### Portainer (Global Service)

- [ ] Container running: `docker ps | grep portainer`
- [ ] Accessible at http://localhost:9000
- [ ] Can login with `stud` / `studstudstud`
- [ ] Local Docker environment visible
- [ ] **Port 9000 is NOT used by any lab service**

### Wireshark

- [ ] Application launches without errors
- [ ] `vEthernet (WSL)` interface visible
- [ ] Can capture traffic from Docker containers
- [ ] ICMP filter works: `docker run --rm alpine ping -c 3 8.8.8.8`

### Python

- [ ] `python3 --version` shows 3.11 or higher
- [ ] `pip show docker` shows version 7.1.0+
- [ ] Docker SDK works: `python3 -c "import docker; print(docker.from_env().info()['ServerVersion'])"`

### Repository

- [ ] Repository cloned successfully
- [ ] Can navigate to week folders
- [ ] Scripts are executable
- [ ] Environment verification passes: `python3 setup/verify_environment.py`

---

## Authors and Contributors

**Laboratory Materials by:** Revolvix

**Institution:**  
Bucharest University of Economic Studies (ASE)  
Faculty of Cybernetics, Statistics and Economic Informatics (CSIE)

**Programmes:**  
- Economic Informatics
- AI in Economics and Business

**Contact:**  
For questions regarding course content, please use the official university communication channels.

**Contributions:**  
Contributions are welcome via GitHub Issues and Pull Requests. Please follow the established code conventions and documentation standards.

---

## Licence

This project is licensed under the **MIT Licence**.

```
MIT License

Copyright (c) 2025 Revolvix - Computer Networks Laboratory, ASE Bucharest

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🎉 Setup Complete!

Your laboratory environment is fully configured. You can now:

- ✅ Run isolated network experiments with Docker containers
- ✅ Capture and analyse traffic with Wireshark on `vEthernet (WSL)`
- ✅ Manage containers through Portainer at http://localhost:9000
- ✅ Automate network tasks with Python
- ✅ Work through all 14 weeks of laboratory exercises

**Next Steps:**
1. Clone Week 1 to `D:\NETWORKING\WEEK1\`
2. Navigate to the kit: `cd /mnt/d/NETWORKING/WEEK1/1enWSL`
3. Verify environment: `python3 setup/verify_environment.py`
4. Start the laboratory: `python3 scripts/start_lab.py`
5. Explore Portainer at http://localhost:9000
6. Practice Wireshark filtering on Docker traffic

**Remember:**
- Port 9000 is **ALWAYS** reserved for Portainer
- Weekly scripts **NEVER** start, stop or remove Portainer
- Each week uses the `10.0.N.0/24` network pattern
- Week 14 TCP Echo uses port **9090** (not 9000)

---

*Computer Networks Laboratory — ASE Bucharest, CSIE*  
*by Revolvix*  
*Documentation version: January 2025*

**Repository:** https://github.com/antonioclim/netENwsl
