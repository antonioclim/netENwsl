# 🎯 Learning Objectives — Week 8: Transport Layer & HTTP

> Computer Networks — ASE, CSIE

This document maps each Learning Objective to its supporting materials
enabling targeted review and ensuring comprehensive coverage.

**Design philosophy:** Every LO should be verifiable through at least three
different artefacts (theory, practice, assessment).

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

## Complete Traceability Matrix

| LO | Theory | Lab Exercise | Tests | Quiz | Parsons | Misconception | PCAP |
|----|--------|--------------|-------|------|---------|---------------|------|
| LO1 | ✅ theory_summary.md | ✅ ex_8_01 | ✅ test_exercises.py | ✅ q01-q04 | ✅ P1 | ✅ #port-size | ⚠️ |
| LO2 | ✅ theory_summary.md | ✅ Demo | ⚠️ manual | ✅ q05-q07 | — | ✅ #third-ack | ✅ handshake.pcap |
| LO3 | ✅ theory_summary.md | ✅ ex_8_01 | ✅ test_exercises.py | ✅ q08-q11 | ✅ P2 | ✅ #head-method | ✅ http.pcap |
| LO4 | ✅ theory_summary.md | ✅ ex_8_02 | ✅ test_exercises.py | ✅ q12-q15 | ✅ P3, P5 | ✅ #round-robin | ✅ loadbalance.pcap |
| LO5 | ✅ README.md | ✅ capture_traffic.py | ⚠️ manual | ✅ q16-q18 | — | ✅ #keep-alive | ✅ required |
| LO6 | ✅ theory_summary.md | ✅ ex_8_01 | ✅ test_exercises.py | ✅ q19-q20 | ✅ P4 | ✅ #403-vs-404 | — |

**Legend:**
- ✅ = Fully covered with specific artefact
- ⚠️ = Partial coverage or manual verification required
- — = Not applicable for this LO

---

## Detailed LO Breakdown

### LO1: TCP/UDP Headers and Port Demultiplexing

> **Objective:** Identify the components of TCP and UDP headers and explain how
> port numbers enable process demultiplexing.

| Artefact Type | Location | Specific Content |
|---------------|----------|------------------|
| **Theory** | docs/theory_summary.md | TCP/UDP header diagrams, port ranges |
| **Theory** | README.md | Transport layer fundamentals section |
| **Glossary** | docs/glossary.md | TCP, UDP, Port, Socket definitions |
| **Misconception** | docs/misconceptions.md#port-size | Port number field size confusion |
| **Quiz** | formative/quiz.yaml | Questions q01, q02, q03, q04 |
| **Parsons** | formative/parsons/problems.json | P1: TCP Server Socket Setup |
| **Code Tracing** | docs/code_tracing.md | Exercise T1: socket creation |

**Verification criteria:** Student can correctly identify TCP vs UDP use cases
and explain why applications bind to specific ports.

---

### LO2: Three-Way Handshake Mechanism

> **Objective:** Describe the three-way handshake and articulate why connection
> establishment requires exactly three messages.

| Artefact Type | Location | Specific Content |
|---------------|----------|------------------|
| **Theory** | docs/theory_summary.md | Handshake sequence diagram |
| **Misconception** | docs/misconceptions.md#third-ack-optional | "Third ACK is optional" myth |
| **Quiz** | formative/quiz.yaml | Questions q05, q06, q07 |
| **Peer Instruction** | docs/peer_instruction.md | Q1: Why exactly three packets? |
| **Demo** | scripts/run_demo.py | `--demo handshake` |
| **Wireshark Filter** | README.md | `tcp.flags.syn == 1` |
| **PCAP Required** | student_context.json | handshake.pcap capture |

**Verification criteria:** Student can trace a handshake in Wireshark and
explain what happens if the third ACK is lost.

---

### LO3: HTTP/1.1 Server Implementation

> **Objective:** Implement a functional HTTP/1.1 server capable of parsing
> requests, serving static files and generating properly formatted responses.

| Artefact Type | Location | Specific Content |
|---------------|----------|------------------|
| **Exercise** | src/exercises/ex_8_01_http_server.py | Complete scaffold with TODOs |
| **Theory** | docs/theory_summary.md | HTTP message format |
| **Code Tracing** | docs/code_tracing.md | T1: Request parsing, T4: Response building |
| **Parsons** | formative/parsons/problems.json | P2: HTTP Response Construction |
| **Misconception** | docs/misconceptions.md#head-returns-head-metadata | HEAD request behaviour |
| **Quiz** | formative/quiz.yaml | Questions q08, q09, q10, q11 |
| **Tests** | tests/test_exercises.py | TestExercise1HTTPServer |
| **Demo** | scripts/run_demo.py | `--demo http-server` |
| **Web Root** | www/ | index.html, hello.txt for testing |

**Verification criteria:** Server correctly handles GET and HEAD, returns proper
status codes and prevents directory traversal.

---

### LO4: Reverse Proxy with Load Balancing

> **Objective:** Construct a reverse proxy that distributes incoming requests
> across multiple backend servers using round-robin load balancing.

| Artefact Type | Location | Specific Content |
|---------------|----------|------------------|
| **Exercise** | src/exercises/ex_8_02_reverse_proxy.py | RoundRobinBalancer scaffold |
| **Theory** | docs/theory_summary.md | Proxy architecture diagram |
| **Theory** | README.md | ASCII diagram of architecture |
| **Code Tracing** | docs/code_tracing.md | T3: Round-robin selection, T5: Connection forwarding |
| **Parsons** | formative/parsons/problems.json | P3: Round-Robin Selection, P5: Proxy Forwarding |
| **Misconception** | docs/misconceptions.md#reverse-vs-forward-proxy | Reverse vs forward proxy |
| **Misconception** | docs/misconceptions.md#round-robin-equal-load | Equal requests ≠ equal load |
| **Quiz** | formative/quiz.yaml | Questions q12, q13, q14, q15 |
| **Peer Instruction** | docs/peer_instruction.md | Q3: Client knowledge of backends |
| **Tests** | tests/test_exercises.py | TestExercise2ReverseProxy |
| **Docker** | docker/docker-compose.yml | nginx + 3 backends |
| **Demo** | scripts/run_demo.py | `--demo docker-nginx` |
| **Backend App** | src/apps/backend_server.py | Reference implementation |

**Verification criteria:** Proxy correctly cycles through backends, adds
X-Forwarded-For header and handles backend failures gracefully.

---

### LO5: Packet Capture Analysis

> **Objective:** Analyse packet captures to distinguish TCP flags, correlate
> request-response pairs and identify connection state transitions.

| Artefact Type | Location | Specific Content |
|---------------|----------|------------------|
| **Theory** | README.md | Wireshark filter reference table |
| **Theory** | docs/commands_cheatsheet.md | Wireshark commands |
| **Script** | scripts/capture_traffic.py | Automated capture utility |
| **Quiz** | formative/quiz.yaml | Questions q16, q17, q18 |
| **Peer Instruction** | docs/peer_instruction.md | Q4: Keep-alive identification |
| **PCAP Directory** | pcap/ | Storage for captured files |
| **PCAP README** | pcap/README.md | Capture instructions |
| **Misconception** | docs/misconceptions.md#http-one-request-per-connection | One request per connection myth |

**Verification criteria:** Student can capture HTTP traffic, identify the
three-way handshake and explain observed TCP flags.

---

### LO6: Security Vulnerability Assessment

> **Objective:** Evaluate security vulnerabilities in HTTP servers (directory
> traversal, resource exhaustion) and implement appropriate mitigations.

| Artefact Type | Location | Specific Content |
|---------------|----------|------------------|
| **Exercise** | src/exercises/ex_8_01_http_server.py | is_safe_path() function |
| **Code Tracing** | docs/code_tracing.md | T2: Path safety validation |
| **Parsons** | formative/parsons/problems.json | P4: Path Traversal Prevention |
| **Quiz** | formative/quiz.yaml | Questions q19, q20 |
| **Peer Instruction** | docs/peer_instruction.md | Q2: 403 vs 404 for security |
| **Misconception** | docs/misconceptions.md#403-vs-404 | Status code semantics |
| **Homework** | homework/README.md | TLS implementation assignment |

**Verification criteria:** Student can identify path traversal attempts,
implement proper validation and articulate the security rationale.

---

## How to Use This Matrix

### For Students

1. **Before lab:** Review theory links for each LO
2. **During lab:** Complete exercises with TODOs
3. **After lab:** Take the formative quiz (`make quiz --lo LOx`)
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

## Quick Reference: LO to Quiz Mapping

| Learning Objective | Quiz Questions | Difficulty Range |
|-------------------|----------------|------------------|
| LO1 | q01, q02, q03, q04 | basic → intermediate |
| LO2 | q05, q06, q07 | basic → advanced |
| LO3 | q08, q09, q10, q11 | basic → intermediate |
| LO4 | q12, q13, q14, q15 | basic → intermediate |
| LO5 | q16, q17, q18 | intermediate → advanced |
| LO6 | q19, q20 | advanced |

---

## Quick Reference: LO to Parsons Mapping

| Learning Objective | Parsons Problem | Focus |
|-------------------|-----------------|-------|
| LO1 | P1 | TCP Server Socket Setup |
| LO3 | P2 | HTTP Response Construction |
| LO4 | P3, P5 | Round-Robin Selection, Proxy Forwarding |
| LO6 | P4 | Path Traversal Prevention |

---

*Computer Networks — ASE, CSIE*

*"If you cannot trace it you cannot teach it."*
