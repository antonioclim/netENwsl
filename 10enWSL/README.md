# Week 10: Application Layer Protocols
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> HTTP/HTTPS, REST Architecture and Network Services

---

## 🎯 Learning Objectives

By the end of this laboratory, students will be able to:

1. **Explain** the role of TLS certificates in HTTPS communication
2. **Compare** REST API designs across Richardson Maturity Model levels
3. **Analyse** DNS query and response structure
4. **Implement** basic clients for HTTP, DNS, SSH and FTP protocols
5. **Evaluate** security differences between encrypted and unencrypted protocols

---

## 📋 Prerequisites

- WSL2 with Ubuntu 22.04+ installed
- Docker and Docker Compose
- Python 3.11+
- Basic understanding of TCP/IP networking
- Familiarity with command-line tools

### Required Python packages

```bash
pip install flask requests paramiko dnspython
```

---

## 🚀 Quick Start

### 1. Start the laboratory environment

```bash
cd /mnt/d/NETWORKING/WEEK10/10enWSL
python3 scripts/start_lab.py
```

### 2. Verify services are running

```bash
python3 tests/smoke_test.py
```

### 3. Begin exercises

Follow the exercises in order:
1. `src/exercises/ex_10_01_tls_rest_crud.py` — TLS Certificates and REST CRUD
2. `src/exercises/ex_10_02_richardson_maturity.py` — Richardson Maturity Model
3. `src/exercises/ex_10_03_dns_query_analysis.py` — DNS Query Analysis
4. `src/exercises/ex_10_04_secure_transfer.py` — SSH and FTP Services

---

## 📚 Learning Path

Follow this recommended order for maximum learning effectiveness:

| Step | Duration | Activity | Resources |
|:----:|:--------:|----------|-----------|
| 1 | 15 min | Read theory and analogies | [Theory Summary](docs/theory_summary.md), [Concept Analogies](docs/concept_analogies.md) |
| 2 | 10 min | Review key terms | [Glossary](docs/glossary.md) |
| 3 | 25 min | Exercise 1: HTTPS/TLS | `ex_10_01_tls_rest_crud.py` |
| 4 | 30 min | Exercise 2: REST Levels | `ex_10_02_richardson_maturity.py` |
| 5 | 20 min | Exercise 3: DNS | `ex_10_03_dns_query_analysis.py` |
| 6 | 20 min | Exercise 4: SSH/FTP | `ex_10_04_secure_transfer.py` |
| 7 | 15 min | Peer Instruction (in class) | [Peer Instruction](docs/peer_instruction.md) |
| 8 | 10 min | Self-assessment | [Misconceptions](docs/misconceptions.md) |

**Total estimated time:** ~2.5 hours

---

## 📁 Project Structure

```
10enWSL/
├── README.md                    # This file
├── CHANGELOG.md                 # Version history
├── docs/                        # Documentation
│   ├── theory_summary.md        # Core concepts with analogies
│   ├── concept_analogies.md     # CPA method analogies (NEW)
│   ├── peer_instruction.md      # MCQ questions for class discussion
│   ├── misconceptions.md        # Common errors and corrections
│   ├── pair_programming_guide.md# Structured pair exercises
│   ├── glossary.md              # Technical terms reference
│   ├── commands_cheatsheet.md   # Quick command reference
│   ├── further_reading.md       # RFCs, books, resources
│   ├── troubleshooting.md       # Common issues and fixes
│   ├── code_tracing.md          # Code tracing exercises
│   └── parsons_problems.md      # Code reordering exercises
├── src/
│   ├── exercises/               # Main exercise scripts
│   │   ├── ex_10_01_tls_rest_crud.py     # TLS and REST CRUD
│   │   ├── ex_10_02_richardson_maturity.py # REST Maturity Levels
│   │   ├── ex_10_03_dns_query_analysis.py  # DNS Query Analysis
│   │   └── ex_10_04_secure_transfer.py     # SSH and FTP Services
│   └── apps/                    # Supporting applications
├── scripts/                     # Utility scripts
│   ├── start_lab.py             # Start Docker containers
│   └── cleanup.py               # Stop and clean up
├── docker/                      # Docker configurations
│   ├── docker-compose.yml       # Service definitions
│   └── */                       # Per-service configs
├── tests/                       # Test scripts
│   ├── smoke_test.py            # Basic connectivity tests
│   └── expected_outputs.md      # Reference outputs
├── homework/                    # Homework assignments
│   ├── README.md                # Homework instructions
│   └── exercises/               # Homework templates
│       ├── hw_10_01_https_analysis.py  # HTTPS analysis helper
│       ├── hw_10_02_rest_client.py     # REST client template
│       └── hw_10_03_dns_tool.py        # DNS configuration tool
└── output/                      # Generated files
    └── tls/                     # TLS certificates
```

---

## 📚 Documentation

### Core Concepts
- [Theory Summary](docs/theory_summary.md) — Key concepts with concrete analogies
- [Concept Analogies](docs/concept_analogies.md) — CPA method: everyday analogies before technical details
- [Glossary](docs/glossary.md) — Technical terms and definitions

### Learning Activities
- [Peer Instruction Questions](docs/peer_instruction.md) — 5 MCQ questions for class discussion
- [Pair Programming Guide](docs/pair_programming_guide.md) — Structured exercises for pairs
- [Code Tracing](docs/code_tracing.md) — Trace code execution manually
- [Parsons Problems](docs/parsons_problems.md) — Reorder code blocks

### Reference
- [Commands Cheatsheet](docs/commands_cheatsheet.md) — curl, dig, ssh, ftp quick reference
- [Troubleshooting](docs/troubleshooting.md) — Common issues and solutions
- [Further Reading](docs/further_reading.md) — RFCs, books, online resources

### Common Errors
- [Misconceptions](docs/misconceptions.md) — 12 common mistakes and corrections

---

## 🔬 Exercises Overview

### Exercise 1: TLS Certificates and REST CRUD
**File:** `src/exercises/ex_10_01_tls_rest_crud.py`
**Duration:** ~25 minutes

Implement a minimal HTTPS server with CRUD endpoints:
- Generate self-signed TLS certificates
- Handle GET, POST, PUT, DELETE requests
- Return appropriate HTTP status codes

```bash
# Generate certificate
python3 src/exercises/ex_10_01_tls_rest_crud.py generate-cert

# Start server
python3 src/exercises/ex_10_01_tls_rest_crud.py serve

# Test with curl
curl -k https://127.0.0.1:8443/
curl -k -X POST https://127.0.0.1:8443/api/resources \
  -H "Content-Type: application/json" \
  -d '{"name": "test", "value": 42}'
```

### Exercise 2: Richardson Maturity Model
**File:** `src/exercises/ex_10_02_richardson_maturity.py`
**Duration:** ~30 minutes

Compare API designs across Richardson Maturity Model levels:
- Level 0: RPC-style single endpoint
- Level 1: Resource-oriented URIs
- Level 2: HTTP verbs and status codes
- Level 3: Hypermedia controls (HATEOAS)

```bash
# Start server
python3 src/exercises/ex_10_02_richardson_maturity.py serve

# Compare levels
curl -X POST http://127.0.0.1:5000/level0/service \
  -H "Content-Type: application/json" \
  -d '{"action": "list_users"}'

curl http://127.0.0.1:5000/level2/users
curl http://127.0.0.1:5000/level3/users
```

### Exercise 3: DNS Query Analysis
**File:** `src/exercises/ex_10_03_dns_query_analysis.py`
**Duration:** ~20 minutes

Analyse DNS query and response structure:
- Build DNS queries programmatically
- Compare UDP vs TCP transport
- Parse response sections (answer, authority, additional)

```bash
# Run demonstrations
python3 src/exercises/ex_10_03_dns_query_analysis.py demo

# Query specific domain
python3 src/exercises/ex_10_03_dns_query_analysis.py query web.lab.local

# Interactive mode
python3 src/exercises/ex_10_03_dns_query_analysis.py interactive
```

### Exercise 4: Secure Shell and File Transfer
**File:** `src/exercises/ex_10_04_secure_transfer.py`
**Duration:** ~20 minutes

Test SSH and FTP services:
- Execute remote commands via SSH
- Transfer files via FTP
- Compare encrypted vs unencrypted protocols

```bash
# Run all demos
python3 src/exercises/ex_10_04_secure_transfer.py demo

# SSH only
python3 src/exercises/ex_10_04_secure_transfer.py ssh

# FTP only
python3 src/exercises/ex_10_04_secure_transfer.py ftp
```

---

## 🛠️ Lab Services

| Service | Container | Port | Credentials |
|---------|-----------|------|-------------|
| Web Server | week10_web | 8000 | — |
| DNS Server | week10_dns | 5353 | — |
| SSH Server | week10_ssh | 2222 | labuser / labpass |
| FTP Server | week10_ftp | 2121 | labftp / labftp |
| Debug Shell | week10_debug | — | — |

### DNS Records (lab.local zone)

| Domain | IP Address |
|--------|------------|
| myservice.lab.local | 10.10.10.10 |
| api.lab.local | 10.10.10.20 |
| web.lab.local | 172.20.0.10 |
| ssh.lab.local | 172.20.0.22 |
| ftp.lab.local | 172.20.0.21 |

---

## ⚠️ Common Misconceptions

> See [docs/misconceptions.md](docs/misconceptions.md) for detailed explanations.

1. **"HTTPS encrypts everything"** — Domain name is visible via SNI
2. **"REST is a protocol"** — REST is an architectural style
3. **"DNS only uses UDP"** — TCP is used for large responses
4. **"FTP uses one connection"** — FTP uses control + data channels

---

## 🧪 Running Tests

```bash
# Basic connectivity tests
python3 tests/smoke_test.py

# Exercise self-tests
python3 src/exercises/ex_10_01_tls_rest_crud.py selftest
```

---

## 🧹 Cleanup

```bash
# Stop all containers
python3 scripts/cleanup.py

# Or manually
docker compose -f docker/docker-compose.yml down
```

---

## 📖 Further Reading

- [RFC 7230-7235](https://datatracker.ietf.org/doc/html/rfc7230) — HTTP/1.1 Specification
- [RFC 8446](https://datatracker.ietf.org/doc/html/rfc8446) — TLS 1.3
- [RFC 1035](https://datatracker.ietf.org/doc/html/rfc1035) — DNS Implementation
- [Fielding's Dissertation](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm) — REST Architecture

See [docs/further_reading.md](docs/further_reading.md) for complete list.

---

## 📝 Homework

See [homework/README.md](homework/README.md) for this week's assignments.

Homework templates are available in `homework/exercises/`:
- `hw_10_01_https_analysis.py` — Helper for HTTPS traffic analysis
- `hw_10_02_rest_client.py` — Template for REST API client
- `hw_10_03_dns_tool.py` — Tool for DNS configuration

---

*Computer Networks — Week 10 | ASE, CSIE Bucharest*
*Laboratory materials by ing. dr. Antonio Clim*
