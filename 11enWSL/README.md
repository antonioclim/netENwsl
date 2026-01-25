# Week 11: Application Protocols – FTP, DNS, SSH & Load Balancing

> NETWORKING class - ASE, CSIE | Computer Networks Laboratory
> 
> by ing. dr. Antonio Clim

---

## ⚠️ Environment Notice

This laboratory kit is designed for the **WSL2 + Ubuntu 22.04 + Docker + Portainer** environment.

**Repository:** https://github.com/antonioclim/netENwsl
**Issues:** Open an issue in GitHub

| Component | Details |
|-----------|---------|
| Windows | Windows 10/11 with WSL2 enabled |
| Linux Distribution | Ubuntu 22.04 LTS (default WSL distro) |
| Container Runtime | Docker Engine (in WSL) |
| Management Interface | Portainer CE on port 9000 (global) |
| Packet Analysis | Wireshark (native Windows application) |

---

## 📥 Quick Start

### First-Time Setup

```bash
# Open Ubuntu terminal (WSL)
wsl

# Navigate to laboratory directory
cd /mnt/d/NETWORKING/WEEK11/11enWSL

# Start Docker if not running
sudo service docker start

# Install Python dependencies
pip install -r setup/requirements.txt --break-system-packages

# Verify environment
python3 setup/verify_environment.py
```

A common pitfall: forgetting to start Docker after Windows restart. This catches most students at least once during the semester.

### Starting the Laboratory

```bash
# Start all services
make lab

# Or manually
python3 scripts/start_lab.py

# Run formative quiz
make quiz

# Run all tests
make test
```

### Accessing Services

| Service | URL/Port | Credentials |
|---------|----------|-------------|
| Portainer | http://localhost:9000 | stud / studstudstud |
| Nginx Load Balancer | http://localhost:8080 | None |
| Backend 1 | http://localhost:8081 | None |
| Backend 2 | http://localhost:8082 | None |
| Backend 3 | http://localhost:8083 | None |

---

## Overview

This laboratory session explores three fundamental application layer protocols: FTP (File Transfer Protocol), DNS (Domain Name System) and SSH (Secure Shell). These protocols exemplify distinct communication approaches—FTP employs a dual-connection architecture separating control and data channels, DNS operates predominantly over UDP with hierarchically structured query mechanisms and SSH establishes multiplexed encrypted channels for secure remote access.

The practical component focuses on distributed application architectures, specifically reverse proxy configurations and load balancing strategies using both custom Python implementations and industrial-strength Nginx deployments.

## Pedagogical Approach

This laboratory employs evidence-based teaching methods:

- **Concept Analogies**: See `docs/concept_analogies.md` for everyday analogies (CPA method)
- **Peer Instruction**: See `docs/peer_instruction.md` for quiz questions with misconception analysis
- **Pair Programming**: See `docs/pair_programming_guide.md` for collaborative exercise structure
- **Prediction Prompts**: Each exercise includes "What do you expect?" moments
- **Common Misconceptions**: See `docs/misconceptions.md` for typical errors and corrections
- **Code Tracing**: See `docs/code_tracing.md` for step-by-step execution exercises
- **Parsons Problems**: See `docs/parsons_problems.md` for code ordering exercises
- **Formative Assessment**: Run `python formative/run_quiz.py` for automated self-assessment
- **LO Traceability**: See `docs/learning_objectives.md` for complete mapping of objectives to artefacts

## Learning Objectives

> 📋 **Full traceability matrix**: See [`docs/learning_objectives.md`](docs/learning_objectives.md)

By the end of this laboratory session, you will be able to:

1. **Identify** the architectural components of FTP, DNS and SSH protocols
2. **Explain** the differences between FTP active/passive modes, DNS resolution hierarchy and SSH key exchange
3. **Implement** a functional Python load balancer with multiple distribution algorithms
4. **Demonstrate** Nginx reverse proxy configuration with upstream pools and failover
5. **Analyse** network traffic patterns using packet capture tools
6. **Design** containerised multi-tier architectures using Docker Compose
7. **Evaluate** performance characteristics of different load balancing algorithms

## Laboratory Exercises

### Exercise 1: HTTP Backend Servers
**Duration:** 10 minutes | **LO:** LO3

Deploy and test multiple HTTP backend servers for load balancing.

### Exercise 2: Python Load Balancer with Round-Robin
**Duration:** 20 minutes | **LO:** LO3

Implement and test round-robin distribution.

### Exercise 3: Sticky Sessions with IP Hash
**Duration:** 15 minutes | **LO:** LO3

Configure session affinity using IP-based hashing.

### Exercise 4: Failover Simulation
**Duration:** 15 minutes | **LO:** LO3, LO7

Observe automatic failover behaviour.

### Exercise 5: Nginx Docker Load Balancer
**Duration:** 20 minutes | **LO:** LO4, LO6

Deploy industrial-strength Nginx using Docker Compose.

### Exercise 6: DNS Protocol Analysis
**Duration:** 20 minutes | **LO:** LO1, LO2

Construct and analyse DNS queries.

### Exercise 7: Performance Benchmarking
**Duration:** 15 minutes | **LO:** LO7

Compare Python vs Nginx load balancer performance.

---

## 🦈 Wireshark Setup

### Essential Filters for Week 11

| Filter | Purpose |
|--------|---------|
| `tcp.port == 8080` | HTTP traffic to load balancer |
| `udp.port == 53` | DNS queries |
| `tcp.port == 21` | FTP control channel |
| `http contains "X-Served-By"` | Load balancer routing |

---

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
sudo netstat -tlnp | grep 8080
sudo kill <pid>
```

**Docker containers won't start:**
```bash
docker compose down -v
docker system prune -f
docker compose up -d
```

**Python module not found:**
```bash
pip install -r setup/requirements.txt --break-system-packages
```

See `docs/troubleshooting.md` for comprehensive solutions.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         WEEK 11 - NETWORK TOPOLOGY                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│    ┌─────────┐                                                              │
│    │ Client  │                                                              │
│    └────┬────┘                                                              │
│         │ HTTP :8080                                                        │
│         ▼                                                                   │
│    ┌─────────────────────────────────┐                                      │
│    │      LOAD BALANCER              │                                      │
│    │  Python LB (didactic)           │                                      │
│    │  Nginx (production)             │                                      │
│    │                                 │                                      │
│    │  Algorithms: RR, LC, IP Hash    │                                      │
│    └────────────┬────────────────────┘                                      │
│     ┌───────────┼───────────┐                                               │
│     ▼           ▼           ▼                                               │
│ ┌───────┐   ┌───────┐   ┌───────┐                                           │
│ │Backend│   │Backend│   │Backend│    Docker Network: s11_network            │
│ │   1   │   │   2   │   │   3   │    Subnet: 172.28.0.0/16                  │
│ │ :8081 │   │ :8082 │   │ :8083 │                                           │
│ └───────┘   └───────┘   └───────┘                                           │
│                                                                             │
│  Portainer: http://localhost:9000 (global service)                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## References

- Kurose, J. & Ross, K. (2021). *Computer Networking: A Top-Down Approach* (8th ed.). Pearson
- RFC 959 – File Transfer Protocol (FTP)
- RFC 1035 – Domain Names - Implementation and Specification
- RFC 4251-4254 – The Secure Shell (SSH) Protocol Architecture
- [Nginx Load Balancing Documentation](https://nginx.org/en/docs/http/load_balancing.html)

---

*NETWORKING class - ASE, CSIE | by ing. dr. Antonio Clim*
*Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment*
