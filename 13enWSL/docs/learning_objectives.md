# 🎯 Learning Objectives Matrix — Week 13

## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## Overview

This document provides explicit traceability between Learning Objectives (LOs) and all pedagogical artifacts in the Week 13 laboratory kit. Each LO is mapped to its supporting materials across theory, lab exercises, assessments, and common misconceptions.

---

## Learning Objectives Summary

| ID | Bloom Level | Description |
|----|-------------|-------------|
| **LO1** | Remember | Recall the fundamental components of MQTT architecture |
| **LO2** | Understand | Explain differences between plaintext and TLS-encrypted communications |
| **LO3** | Apply | Implement TCP connect scanning using concurrent programming |
| **LO4** | Apply | Demonstrate MQTT publish/subscribe operations |
| **LO5** | Analyze | Analyse packet captures to distinguish encrypted vs unencrypted traffic |
| **LO6** | Create | Design a systematic reconnaissance workflow |
| **LO7** | Evaluate | Evaluate security posture based on exposed services |

---

## Traceability Matrix

### Complete Coverage Map

| LO | Theory | Lab Exercise | Test | PCAP | Misconception | Quiz | Parsons |
|----|--------|--------------|------|------|---------------|------|---------|
| **LO1** | ✅ `theory_summary.md` §2 | ✅ `ex_13_02` | ✅ `test_exercises.py` | ⬜ `mqtt_*.pcap` | ✅ #1, #2, #3 | ✅ q01, q02 | ✅ P1 |
| **LO2** | ✅ `theory_summary.md` §3 | ✅ `ex_13_02 --tls` | ✅ `test_exercises.py` | ⬜ `tls_*.pcap` | ✅ #4, #5 | ✅ q03, q04 | ✅ P3 |
| **LO3** | ✅ `theory_summary.md` §4 | ✅ `ex_13_01` | ✅ `test_exercises.py` | ⬜ `scan_*.pcap` | ✅ #6, #7, #8 | ✅ q05 | ✅ P2 |
| **LO4** | ✅ `theory_summary.md` §2.2 | ✅ `ex_13_02` | ✅ `test_exercises.py` | ⬜ `mqtt_pubsub.pcap` | ✅ #2 | ✅ q06 | ✅ P1 |
| **LO5** | ✅ `theory_summary.md` §3 | ✅ `ex_13_03` | ✅ `smoke_test.py` | ⬜ ALL | ✅ #4 | ✅ q07, q08 | ✅ P4 |
| **LO6** | ✅ `theory_summary.md` §4 | ✅ `ex_13_04` | ✅ `test_exercises.py` | ⬜ `recon_*.pcap` | ✅ #6, #7 | ✅ q10 | ✅ P5 |
| **LO7** | ✅ `theory_summary.md` §5 | ✅ `ex_13_04` | ⚠️ Manual | — | ✅ #9, #10 | ✅ q09 | — |

**Legend:**
- ✅ Complete coverage
- ⚠️ Partial coverage
- ⬜ To be generated during lab
- — Not applicable

---

## Detailed LO Specifications

### LO1: Recall MQTT Architecture Components

**Bloom Level:** Remember (Level 1)

**Description:** Recall the fundamental components of MQTT architecture including brokers, publishers, subscribers and topic hierarchies.

**Artifacts:**

| Type | Location | Section/Function |
|------|----------|------------------|
| Theory | `docs/theory_summary.md` | Section 2: MQTT Protocol |
| Lab | `src/exercises/ex_13_02_mqtt_client.py` | `mqtt_publish()`, `mqtt_subscribe()` |
| Test | `tests/test_exercises.py` | `TestExercise2MQTTClient` |
| Quiz | `formative/quiz.yaml` | q01 (port), q02 (QoS) |
| Parsons | `docs/parsons_problems.md` | P1: MQTT Publish with QoS |
| Misconception | `docs/misconceptions.md` | #1 (QoS≠encryption), #2 (wildcards), #3 (anonymous) |
| Peer Instruction | `docs/peer_instruction.md` | Q1 (QoS levels) |

**Assessment Criteria:**
- Can name the three MQTT components (broker, publisher, subscriber)
- Can explain topic hierarchy syntax (building/floor1/temperature)
- Can differentiate QoS levels 0, 1, 2

---

### LO2: Explain Plaintext vs TLS Communications

**Bloom Level:** Understand (Level 2)

**Description:** Explain the differences between plaintext and TLS-encrypted network communications and what metadata remains observable under encryption.

**Artifacts:**

| Type | Location | Section/Function |
|------|----------|------------------|
| Theory | `docs/theory_summary.md` | Section 3: TLS |
| Lab | `src/exercises/ex_13_02_mqtt_client.py` | `--tls` flag, TLS context |
| Test | `tests/test_exercises.py` | `test_mqtt_client_help` |
| Quiz | `formative/quiz.yaml` | q03 (metadata visibility), q04 (filtered) |
| Parsons | `docs/parsons_problems.md` | P3: TLS Context Configuration |
| Misconception | `docs/misconceptions.md` | #4 (TLS metadata), #5 (TLS 1.3 compat) |
| Peer Instruction | `docs/peer_instruction.md` | Q2 (TLS metadata) |

**Assessment Criteria:**
- Can list what TLS encrypts (payload) vs what remains visible (metadata)
- Can explain why traffic analysis is still possible with TLS
- Can configure TLS context in Python

---

### LO3: Implement TCP Connect Scanning

**Bloom Level:** Apply (Level 3)

**Description:** Implement TCP connect scanning using concurrent programming techniques and interpret the resulting port states (open, closed, filtered).

**Artifacts:**

| Type | Location | Section/Function |
|------|----------|------------------|
| Theory | `docs/theory_summary.md` | Section 4: Port Scanning |
| Lab | `src/exercises/ex_13_01_port_scanner.py` | `tcp_connect_scan()`, `scan_host()` |
| Test | `tests/test_exercises.py` | `TestExercise1PortScanner` |
| Quiz | `formative/quiz.yaml` | q05 (command syntax) |
| Parsons | `docs/parsons_problems.md` | P2: TCP Port Scanner Function |
| Misconception | `docs/misconceptions.md` | #6 (filtered≠secure), #7 (scanning legality), #8 (open≠vulnerable) |
| Peer Instruction | `docs/peer_instruction.md` | Q3 (port states) |

**Assessment Criteria:**
- Can implement TCP connect scan with sockets
- Can explain difference between open/closed/filtered states
- Can use ThreadPoolExecutor for concurrent scanning

---

### LO4: Demonstrate MQTT Pub/Sub Operations

**Bloom Level:** Apply (Level 3)

**Description:** Demonstrate MQTT publish/subscribe operations using Python client libraries with both plaintext and TLS transport configurations.

**Artifacts:**

| Type | Location | Section/Function |
|------|----------|------------------|
| Theory | `docs/theory_summary.md` | Section 2.2: Topic Structure |
| Lab | `src/exercises/ex_13_02_mqtt_client.py` | Full exercise |
| Test | `tests/test_exercises.py` | `test_mqtt_publish` |
| Quiz | `formative/quiz.yaml` | q06 (wildcards) |
| Parsons | `docs/parsons_problems.md` | P1: MQTT Publish with QoS |
| Misconception | `docs/misconceptions.md` | #2 (wildcards≠regex) |
| Peer Instruction | `docs/peer_instruction.md` | Q4 (topic wildcards) |

**Assessment Criteria:**
- Can publish messages to MQTT topics
- Can subscribe with wildcards (+ and #)
- Can configure QoS for reliable delivery

---

### LO5: Analyse Packet Captures

**Bloom Level:** Analyze (Level 4)

**Description:** Analyse packet captures to distinguish between encrypted and unencrypted traffic flows and identify protocol-specific patterns.

**Artifacts:**

| Type | Location | Section/Function |
|------|----------|------------------|
| Theory | `docs/theory_summary.md` | Section 3: TLS Analysis |
| Lab | `src/exercises/ex_13_03_packet_sniffer.py` | Full exercise |
| Test | `tests/smoke_test.py` | Service connectivity |
| Quiz | `formative/quiz.yaml` | q07 (QoS negotiation), q08 (TCP handshake) |
| Parsons | `docs/parsons_problems.md` | P4: Packet Capture Filter |
| Misconception | `docs/misconceptions.md` | #4 (TLS metadata) |
| PCAP | `pcap/` | Generated during lab |

**Assessment Criteria:**
- Can capture traffic with appropriate filters
- Can distinguish MQTT from other protocols
- Can identify encrypted vs plaintext in Wireshark

---

### LO6: Design Reconnaissance Workflow

**Bloom Level:** Create (Level 6)

**Description:** Design a systematic reconnaissance workflow that combines service enumeration, banner grabbing and vulnerability fingerprinting.

**Artifacts:**

| Type | Location | Section/Function |
|------|----------|------------------|
| Theory | `docs/theory_summary.md` | Section 4: Reconnaissance |
| Lab | `src/exercises/ex_13_04_vuln_checker.py` | Full exercise |
| Test | `tests/test_exercises.py` | `TestExercise4VulnChecker` |
| Quiz | `formative/quiz.yaml` | q10 (workflow design) |
| Parsons | `docs/parsons_problems.md` | P5: Vulnerability Check |
| Misconception | `docs/misconceptions.md` | #6, #7 (scanning context) |

**Assessment Criteria:**
- Can design multi-step reconnaissance process
- Can combine scanning + fingerprinting + CVE lookup
- Can document findings systematically

---

### LO7: Evaluate Security Posture

**Bloom Level:** Evaluate (Level 5)

**Description:** Evaluate the security posture of network services based on exposed ports, protocol versions and known vulnerability indicators.

**Artifacts:**

| Type | Location | Section/Function |
|------|----------|------------------|
| Theory | `docs/theory_summary.md` | Section 5: IoT Security |
| Lab | `src/exercises/ex_13_04_vuln_checker.py` | `generate_report()` |
| Test | Manual evaluation | Instructor review |
| Quiz | `formative/quiz.yaml` | q09 (OWASP priority) |
| Misconception | `docs/misconceptions.md` | #9 (simple≠safe), #10 (auth vs encrypt) |
| Peer Instruction | `docs/peer_instruction.md` | Q5 (IoT vulnerabilities) |

**Assessment Criteria:**
- Can prioritize vulnerabilities by severity
- Can apply OWASP IoT Top 10 framework
- Can make security recommendations based on findings

---

## Coverage Summary

| Category | Items | Coverage |
|----------|-------|----------|
| Learning Objectives | 7 | 100% mapped |
| Lab Exercises | 4 | All linked to LOs |
| Quiz Questions | 10 | All linked to LOs |
| Misconceptions | 10 | All linked to LOs |
| Parsons Problems | 5 | 5/7 LOs covered |
| Peer Instruction | 6 | All linked to LOs |

---

## Quick Reference

```
LO1 (Remember)    → ex_13_02 → MQTT basics        → q01, q02 → #1,2,3
LO2 (Understand)  → ex_13_02 → TLS comparison     → q03, q04 → #4,5
LO3 (Apply)       → ex_13_01 → Port scanning      → q05      → #6,7,8
LO4 (Apply)       → ex_13_02 → Pub/sub ops        → q06      → #2
LO5 (Analyze)     → ex_13_03 → Packet analysis    → q07, q08 → #4
LO6 (Create)      → ex_13_04 → Reconnaissance     → q10      → #6,7
LO7 (Evaluate)    → ex_13_04 → Security posture   → q09      → #9,10
```

---

*Week 13: IoT and Security — Learning Objectives Traceability*
*Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim*
