# 🎯 Learning Objectives — Week 8: Transport Layer & HTTP
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> This document maps each Learning Objective to its supporting materials,
> enabling targeted review and ensuring comprehensive coverage.
>
> **Design philosophy:** Every LO should be verifiable through at least three
> different artefacts (theory, practice, assessment) — a principle from the
> psychopedagogy module at Universitatea Politehnica București.

---

## Overview

Week 8 covers the transport layer with a focus on practical implementation.
Students progress from understanding protocol headers to building functional
HTTP servers and reverse proxies.

| LO | Bloom Level | Topic |
|----|-------------|-------|
| LO1 | Remember/Understand | TCP/UDP headers and port demultiplexing |
| LO2 | Understand | Three-way handshake mechanism |
| LO3 | Apply | HTTP/1.1 server implementation |
| LO4 | Apply | Reverse proxy with load balancing |
| LO5 | Analyse | Packet capture analysis |
| LO6 | Evaluate | Security vulnerability assessment |

---

## Detailed Traceability Matrix

### LO1: TCP/UDP Headers and Port Demultiplexing

> **Objective:** Identify the components of TCP and UDP headers and explain how
> port numbers enable process demultiplexing.

| Artefact Type | Location | Specific Content |
|---------------|----------|------------------|
| **Theory** | [docs/theory_summary.md](theory_summary.md#transport-layer) | TCP/UDP header diagrams, port ranges |
| **Theory** | [README.md](../README.md#theoretical-background) | Transport layer fundamentals section |
| **Lecture** | `00LECTURES/S8Theory_Week8_EN.html` | Slides 5-18: Protocol headers |
| **Glossary** | [docs/glossary.md](glossary.md#transport-layer-terms) | TCP, UDP, Port, Socket definitions |
| **Misconception** | [docs/misconceptions.md](misconceptions.md#port-size) | Port number field size confusion |
| **Quiz** | [formative/quiz.yaml](../formative/quiz.yaml) | Questions q01, q02, q03 |
| **Peer Instruction** | [docs/peer_instruction.md](peer_instruction.md) | Q4: Keep-alive behaviour |
| **Code Tracing** | [docs/code_tracing.md](code_tracing.md#t1) | Exercise T1: socket creation |

**Verification criteria:** Student can correctly identify TCP vs UDP use cases
and explain why applications bind to specific ports.

---

### LO2: Three-Way Handshake Mechanism

> **Objective:** Describe the three-way handshake and articulate why connection
> establishment requires exactly three messages.

| Artefact Type | Location | Specific Content |
|---------------|----------|------------------|
| **Theory** | [docs/theory_summary.md](theory_summary.md#tcp-connection) | Handshake sequence diagram |
| **Lecture** | `00LECTURES/S8Theory_Week8_EN.html` | Slides 19-27: Connection states |
| **Misconception** | [docs/misconceptions.md](misconceptions.md#third-ack-optional) | "Third ACK is optional" myth |
| **Quiz** | [formative/quiz.yaml](../formative/quiz.yaml) | Questions q04, q05, q06 |
| **Peer Instruction** | [docs/peer_instruction.md](peer_instruction.md#q1) | Q1: Why exactly three packets? |
| **Demo** | [scripts/run_demo.py](../scripts/run_demo.py) | `--demo handshake` |
| **Wireshark Filter** | [README.md](../README.md#wireshark-filters) | `tcp.flags.syn == 1` |
| **PCAP** | [pcap/](../pcap/) | Capture during demo |

**Verification criteria:** Student can trace a handshake in Wireshark and
explain what happens if the third ACK is lost.

---

### LO3: HTTP/1.1 Server Implementation

> **Objective:** Implement a functional HTTP/1.1 server capable of parsing
> requests, serving static files and generating properly formatted responses.

| Artefact Type | Location | Specific Content |
|---------------|----------|------------------|
| **Exercise** | [src/exercises/ex_8_01_http_server.py](../src/exercises/ex_8_01_http_server.py) | Complete scaffold with TODOs |
| **Theory** | [docs/theory_summary.md](theory_summary.md#http) | HTTP message format |
| **Code Tracing** | [docs/code_tracing.md](code_tracing.md#t1) | T1: Request parsing |
| **Code Tracing** | [docs/code_tracing.md](code_tracing.md#t4) | T4: Response building |
| **Parsons** | [docs/parsons_problems.md](parsons_problems.md#p2) | P2: HTTP response builder |
| **Misconception** | [docs/misconceptions.md](misconceptions.md#head-returns-head-metadata) | HEAD request behaviour |
| **Quiz** | [formative/quiz.yaml](../formative/quiz.yaml) | Questions q07, q08, q09 |
| **Tests** | [tests/test_exercises.py](../tests/test_exercises.py) | TestExercise1HTTPServer |
| **Demo** | [scripts/run_demo.py](../scripts/run_demo.py) | `--demo http-server` |
| **Web Root** | [www/](../www/) | index.html, hello.txt for testing |

**Verification criteria:** Server correctly handles GET, HEAD, returns proper
status codes and prevents directory traversal.

---

### LO4: Reverse Proxy with Load Balancing

> **Objective:** Construct a reverse proxy that distributes incoming requests
> across multiple backend servers using round-robin load balancing.

| Artefact Type | Location | Specific Content |
|---------------|----------|------------------|
| **Exercise** | [src/exercises/ex_8_02_reverse_proxy.py](../src/exercises/ex_8_02_reverse_proxy.py) | RoundRobinBalancer scaffold |
| **Theory** | [docs/theory_summary.md](theory_summary.md#reverse-proxy) | Proxy architecture diagram |
| **Theory** | [README.md](../README.md#reverse-proxy-architecture) | ASCII diagram of architecture |
| **Code Tracing** | [docs/code_tracing.md](code_tracing.md#t3) | T3: Round-robin selection |
| **Code Tracing** | [docs/code_tracing.md](code_tracing.md#t5) | T5: Connection forwarding |
| **Parsons** | [docs/parsons_problems.md](parsons_problems.md#p3) | P3: next_backend() implementation |
| **Parsons** | [docs/parsons_problems.md](parsons_problems.md#p6) | P6: Proxy header injection |
| **Misconception** | [docs/misconceptions.md](misconceptions.md#reverse-vs-forward-proxy) | Reverse vs forward proxy |
| **Misconception** | [docs/misconceptions.md](misconceptions.md#round-robin-equal-load) | Equal requests ≠ equal load |
| **Quiz** | [formative/quiz.yaml](../formative/quiz.yaml) | Questions q10, q11, q12 |
| **Peer Instruction** | [docs/peer_instruction.md](peer_instruction.md#q3) | Q3: Client knowledge of backends |
| **Tests** | [tests/test_exercises.py](../tests/test_exercises.py) | TestExercise2ReverseProxy |
| **Docker** | [docker/docker-compose.yml](../docker/docker-compose.yml) | nginx + 3 backends |
| **Demo** | [scripts/run_demo.py](../scripts/run_demo.py) | `--demo docker-nginx` |
| **Backend App** | [src/apps/backend_server.py](../src/apps/backend_server.py) | Reference implementation |

**Verification criteria:** Proxy correctly cycles through backends, adds
X-Forwarded-For header and handles backend failures gracefully.

---

### LO5: Packet Capture Analysis

> **Objective:** Analyse packet captures to distinguish TCP flags, correlate
> request-response pairs and identify connection state transitions.

| Artefact Type | Location | Specific Content |
|---------------|----------|------------------|
| **Theory** | [README.md](../README.md#wireshark-filters) | Filter reference table |
| **Theory** | [docs/commands_cheatsheet.md](commands_cheatsheet.md#wireshark) | Wireshark commands |
| **Script** | [scripts/capture_traffic.py](../scripts/capture_traffic.py) | Automated capture utility |
| **Quiz** | [formative/quiz.yaml](../formative/quiz.yaml) | Questions q13, q14 |
| **Peer Instruction** | [docs/peer_instruction.md](peer_instruction.md#q4) | Q4: Keep-alive identification |
| **PCAP Directory** | [pcap/](../pcap/) | Storage for captured files |
| **PCAP README** | [pcap/README.md](../pcap/README.md) | Capture instructions |
| **Misconception** | [docs/misconceptions.md](misconceptions.md#http-one-request-per-connection) | One request per connection myth |

**Verification criteria:** Student can capture HTTP traffic, identify the
three-way handshake and explain observed TCP flags.

---

### LO6: Security Vulnerability Assessment

> **Objective:** Evaluate security vulnerabilities in HTTP servers (directory
> traversal, resource exhaustion) and implement appropriate mitigations.

| Artefact Type | Location | Specific Content |
|---------------|----------|------------------|
| **Exercise** | [src/exercises/ex_8_01_http_server.py](../src/exercises/ex_8_01_http_server.py) | is_safe_path() function |
| **Code Tracing** | [docs/code_tracing.md](code_tracing.md#t2) | T2: Path safety validation |
| **Parsons** | [docs/parsons_problems.md](parsons_problems.md#p4) | P4: Safe path validation |
| **Quiz** | [formative/quiz.yaml](../formative/quiz.yaml) | Question q15 |
| **Peer Instruction** | [docs/peer_instruction.md](peer_instruction.md#q2) | Q2: 403 vs 404 for security |
| **Misconception** | [docs/misconceptions.md](misconceptions.md#403-vs-404) | Status code semantics |
| **Exercise 4** | [README.md](../README.md#exercise-4-rate-limiting) | Token bucket rate limiting |
| **Homework** | [homework/README.md](../homework/README.md) | TLS implementation assignment |

**Verification criteria:** Student can identify path traversal attempts,
implement proper validation and articulate the security rationale.

---

## Coverage Summary

| LO | Theory | Lab | Tests | Quiz | Peer Instr. | Parsons | Misconception |
|----|--------|-----|-------|------|-------------|---------|---------------|
| LO1 | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ |
| LO2 | ✅ | ✅ | ⚠️ | ✅ | ✅ | — | ✅ |
| LO3 | ✅ | ✅ | ✅ | ✅ | — | ✅ | ✅ |
| LO4 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| LO5 | ✅ | ✅ | ⚠️ | ✅ | ✅ | — | ✅ |
| LO6 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

**Legend:**
- ✅ = Fully covered
- ⚠️ = Partial coverage (manual verification required)
- — = Not applicable for this LO

---

## How to Use This Matrix

### For Students

1. **Before lab:** Review theory links for each LO
2. **During lab:** Complete exercises with TODOs
3. **After lab:** Take the formative quiz (`python formative/run_quiz.py --lo LOx`)
4. **Self-assessment:** Check which LOs need more work based on quiz results

### For Instructors

1. **Preparation:** Verify all links are accessible
2. **During session:** Use Peer Instruction questions for discussion
3. **Assessment:** Refer to verification criteria when grading
4. **Continuous improvement:** Note which LOs students struggle with

### For Teaching Assistants

1. **Lab support:** Use Parsons problems for students who are stuck
2. **Debugging:** Refer students to Code Tracing exercises
3. **Common issues:** Point to relevant Misconception entries

---

## Acknowledgments

This traceability matrix was developed with contributions from:
- **Andrei T.** — Reviewing LO alignment and suggesting additional artefacts
- **DPPD Module, Universitatea Politehnica București** — Pedagogical framework
  for learning objective design and assessment alignment

The "minimum three artefacts per LO" principle comes from constructive alignment
theory (Biggs, 1996) as applied in the Romanian higher education context.

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
*"If you can't trace it, you can't teach it."*
