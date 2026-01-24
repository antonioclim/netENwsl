# 📚 Learning Objectives Traceability Matrix

> Week 13: IoT and Security in Computer Networks  
> NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

---

## Overview

This document provides a complete traceability matrix mapping each Learning Objective (LO) to its corresponding course materials, exercises, assessments and verification methods. This ensures alignment between intended outcomes and actual course delivery.

---

## Learning Objectives Summary

| ID | Bloom Level | Verb | Description |
|----|-------------|------|-------------|
| LO1 | Remember (1) | Recall | MQTT architecture components |
| LO2 | Understand (2) | Explain | Plaintext vs TLS differences |
| LO3 | Apply (3) | Implement | TCP connect scanning |
| LO4 | Apply (3) | Demonstrate | MQTT pub/sub operations |
| LO5 | Analyse (4) | Analyse | Packet captures |
| LO6 | Create (6) | Design | Reconnaissance workflow |
| LO7 | Evaluate (5) | Evaluate | Security posture |

---

## Detailed Traceability Matrix

### LO1: Recall MQTT Architecture Components

**Bloom Level:** Remember (Level 1)  
**Full Description:** Recall the fundamental components of MQTT architecture including brokers, publishers, subscribers and topic hierarchies.

| Artifact Type | Reference | Coverage |
|--------------|-----------|----------|
| **Theory** | `docs/theory_summary.md` §2 "MQTT Protocol Fundamentals" | ✅ Complete |
| **Exercise** | `ex_13_02_mqtt_client.py` (subscribe/publish modes) | ✅ Complete |
| **Test** | `tests/test_exercises.py::TestExercise2MQTTClient` | ✅ Complete |
| **Quiz** | `formative/quiz.yaml` q01, q02, q03 | ✅ Complete |
| **Misconceptions** | `docs/misconceptions.md` #1 (QoS≠encryption), #2 (wildcards), #3 (anonymous) | ✅ Complete |
| **Parsons** | `docs/parsons_problems.md` P1 (MQTT Publish with QoS) | ✅ Complete |
| **Peer Instruction** | `docs/peer_instruction.md` Q1 (broker role) | ✅ Complete |

**Assessment Criteria:**
- Can identify the three main components: Publisher, Broker, Subscriber
- Can explain the role of topics in message routing
- Can describe QoS levels (0, 1, 2) and their guarantees
- Can draw a basic MQTT architecture diagram

---

### LO2: Explain Plaintext vs TLS Differences

**Bloom Level:** Understand (Level 2)  
**Full Description:** Explain the differences between plaintext and TLS-encrypted network communications and what metadata remains observable under encryption.

| Artifact Type | Reference | Coverage |
|--------------|-----------|----------|
| **Theory** | `docs/theory_summary.md` §3 "Transport Layer Security" | ✅ Complete |
| **Exercise** | `ex_13_02_mqtt_client.py --tls` flag | ✅ Complete |
| **Test** | `tests/test_exercises.py::test_tls_connection` | ✅ Complete |
| **Quiz** | `formative/quiz.yaml` q04, q05, q06 | ✅ Complete |
| **Misconceptions** | `docs/misconceptions.md` #4 (TLS metadata), #5 (TLS 1.3 compatibility) | ✅ Complete |
| **Parsons** | `docs/parsons_problems.md` P3 (TLS Context Configuration) | ✅ Complete |
| **Peer Instruction** | `docs/peer_instruction.md` Q2 (what TLS hides) | ✅ Complete |
| **Wireshark** | Compare captures: port 1883 vs 8883 | ✅ Complete |

**Assessment Criteria:**
- Can explain what TLS encrypts (payload) and what remains visible (metadata)
- Can identify TLS handshake packets in Wireshark
- Can configure TLS client with CA certificate
- Can articulate why TLS is necessary for IoT security

---

### LO3: Implement TCP Connect Scanning

**Bloom Level:** Apply (Level 3)  
**Full Description:** Implement TCP connect scanning using concurrent programming techniques and interpret the resulting port states (open, closed, filtered).

| Artifact Type | Reference | Coverage |
|--------------|-----------|----------|
| **Theory** | `docs/theory_summary.md` §4 "Port Scanning Techniques" | ✅ Complete |
| **Exercise** | `ex_13_01_port_scanner.py` (full implementation) | ✅ Complete |
| **Test** | `tests/test_exercises.py::TestExercise1PortScanner` | ✅ Complete |
| **Quiz** | `formative/quiz.yaml` q07, q08 | ✅ Complete |
| **Misconceptions** | `docs/misconceptions.md` #6 (filtered), #7 (legality), #8 (open≠vulnerable) | ✅ Complete |
| **Parsons** | `docs/parsons_problems.md` P2 (TCP Port Scanner Function) | ✅ Complete |
| **Code Tracing** | `docs/code_tracing.md` Exercise 1 | ✅ Complete |

**Assessment Criteria:**
- Can explain TCP three-way handshake
- Can differentiate between open, closed and filtered port states
- Can implement socket-based port scanning
- Can use ThreadPoolExecutor for concurrent scanning
- Can interpret scan results and correlate with services

---

### LO4: Demonstrate MQTT Pub/Sub Operations

**Bloom Level:** Apply (Level 3)  
**Full Description:** Demonstrate MQTT publish/subscribe operations using Python client libraries with both plaintext and TLS transport configurations.

| Artifact Type | Reference | Coverage |
|--------------|-----------|----------|
| **Theory** | `docs/theory_summary.md` §2.2 "Publish/Subscribe Pattern" | ✅ Complete |
| **Exercise** | `ex_13_02_mqtt_client.py` (both modes) | ✅ Complete |
| **Test** | `tests/test_exercises.py::test_mqtt_publish`, `::test_mqtt_subscribe` | ✅ Complete |
| **Quiz** | `formative/quiz.yaml` q09, q10 | ✅ Complete |
| **Misconceptions** | `docs/misconceptions.md` #2 (wildcards) | ✅ Complete |
| **Parsons** | `docs/parsons_problems.md` P1 (MQTT Publish with QoS) | ✅ Complete |
| **Peer Instruction** | `docs/peer_instruction.md` Q3 (QoS selection) | ✅ Complete |

**Assessment Criteria:**
- Can write MQTT publisher code using paho-mqtt
- Can write MQTT subscriber code with topic filters
- Can use topic wildcards (+ and #) correctly
- Can configure client for TLS transport

---

### LO5: Analyse Packet Captures

**Bloom Level:** Analyse (Level 4)  
**Full Description:** Analyse packet captures to distinguish between encrypted and unencrypted traffic flows and identify protocol-specific patterns.

| Artifact Type | Reference | Coverage |
|--------------|-----------|----------|
| **Theory** | `docs/theory_summary.md` §3 "Traffic Analysis" | ✅ Complete |
| **Exercise** | `ex_13_03_packet_sniffer.py` | ✅ Complete |
| **Smoke Test** | `tests/smoke_test.py::test_scapy_available` | ✅ Complete |
| **Quiz** | `formative/quiz.yaml` q11, q12 | ✅ Complete |
| **Misconceptions** | `docs/misconceptions.md` #4 (TLS metadata visible) | ✅ Complete |
| **Parsons** | `docs/parsons_problems.md` P4 (Packet Capture Filter) | ✅ Complete |
| **Wireshark Guide** | `README.md` Wireshark section | ✅ Complete |

**Assessment Criteria:**
- Can capture packets using Scapy or Wireshark
- Can write BPF filter expressions
- Can identify MQTT packets in plaintext captures
- Can distinguish TLS Application Data from plaintext
- Can analyse TCP handshake sequence

---

### LO6: Design Reconnaissance Workflow

**Bloom Level:** Create (Level 6)  
**Full Description:** Design a systematic reconnaissance workflow that combines service enumeration, banner grabbing and vulnerability fingerprinting.

| Artifact Type | Reference | Coverage |
|--------------|-----------|----------|
| **Theory** | `docs/theory_summary.md` §4 "Security Assessment Methodology" | ✅ Complete |
| **Exercise** | `ex_13_04_vuln_checker.py` | ✅ Complete |
| **Test** | `tests/test_exercises.py::TestExercise4VulnChecker` | ✅ Complete |
| **Quiz** | `formative/quiz.yaml` q15, q16 | ✅ Complete |
| **Misconceptions** | `docs/misconceptions.md` #6 (filtered), #7 (legality) | ✅ Complete |
| **Parsons** | `docs/parsons_problems.md` P5 (Vulnerability Check Workflow) | ✅ Complete |
| **Architecture** | `docs/images/architecture_week13.md` Diagram 6 | ✅ Complete |

**Assessment Criteria:**
- Can describe phases of security assessment (discovery, enumeration, analysis)
- Can combine multiple tools into coherent workflow
- Can document findings in structured format
- Can prioritise findings by risk level

---

### LO7: Evaluate Security Posture

**Bloom Level:** Evaluate (Level 5)  
**Full Description:** Evaluate the security posture of network services based on exposed ports, protocol versions and known vulnerability indicators.

| Artifact Type | Reference | Coverage |
|--------------|-----------|----------|
| **Theory** | `docs/theory_summary.md` §5 "Risk Assessment" | ✅ Complete |
| **Exercise** | `ex_13_04_vuln_checker.py` (report generation) | ✅ Complete |
| **Manual Evaluation** | Laboratory report rubric | ✅ Complete |
| **Quiz** | `formative/quiz.yaml` q13, q14 | ✅ Complete |
| **Misconceptions** | `docs/misconceptions.md` #9 (simple≠safe), #10 (encrypt vs authenticate) | ✅ Complete |
| **SECURITY.md** | Ethical guidelines and compliance | ✅ Complete |

**Assessment Criteria:**
- Can assess risk based on service exposure
- Can identify insecure configurations (anonymous access, plaintext)
- Can recommend mitigations for identified vulnerabilities
- Can articulate trade-offs between security and usability

---

## Coverage Summary

### By Artifact Type

| Artifact | LO1 | LO2 | LO3 | LO4 | LO5 | LO6 | LO7 | Total |
|----------|-----|-----|-----|-----|-----|-----|-----|-------|
| Theory | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 7/7 |
| Exercise | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 7/7 |
| Test | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 7/7 |
| Quiz | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 7/7 |
| Misconceptions | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 7/7 |
| Parsons | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | 6/7 |
| Peer Instruction | ✅ | ✅ | — | ✅ | — | — | — | 3/7 |

### By Bloom Level

| Bloom Level | LOs | Quiz Questions | Exercises |
|-------------|-----|----------------|-----------|
| Remember (1) | LO1 | q01, q02, q03 | ex_13_02 |
| Understand (2) | LO2 | q04, q05, q06 | ex_13_02 |
| Apply (3) | LO3, LO4 | q07, q08, q09, q10 | ex_13_01, ex_13_02 |
| Analyse (4) | LO5 | q11, q12 | ex_13_03 |
| Evaluate (5) | LO7 | q13, q14 | ex_13_04 |
| Create (6) | LO6 | q15, q16 | ex_13_04 |

---

## Verification Checklist

Before each laboratory session, verify:

- [ ] All exercises are syntactically correct: `make lint`
- [ ] Tests pass: `make test`
- [ ] Quiz loads correctly: `make quiz --dry-run`
- [ ] Docker services start: `make start && make status`
- [ ] Ground truth validates: `make validate`

---

## Cross-Reference: Quiz Questions to LOs

| Question | LO | Bloom | Topic |
|----------|-----|-------|-------|
| q01 | LO1 | Remember | MQTT port number |
| q02 | LO1 | Remember | QoS levels |
| q03 | LO1 | Remember | MQTT components |
| q04 | LO2 | Understand | TLS encryption scope |
| q05 | LO2 | Understand | Port states |
| q06 | LO2 | Understand | TLS compatibility |
| q07 | LO3 | Apply | TCP handshake |
| q08 | LO3 | Apply | Socket programming |
| q09 | LO4 | Apply | MQTT publish |
| q10 | LO4 | Apply | MQTT subscribe |
| q11 | LO5 | Analyse | Packet analysis |
| q12 | LO5 | Analyse | Traffic patterns |
| q13 | LO7 | Evaluate | Risk assessment |
| q14 | LO7 | Evaluate | Security posture |
| q15 | LO6 | Create | Workflow design |
| q16 | LO6 | Create | Report generation |

---

## Continuous Improvement

This matrix should be reviewed and updated:

1. **After each semester**: Incorporate student feedback
2. **When exercises change**: Update artifact references
3. **When quiz questions change**: Update LO mappings
4. **When new tools emerge**: Consider coverage gaps

**Feedback:** Open an issue in the GitHub repository

---

*Computer Networks — Week 13: IoT and Security*  
*ASE Bucharest, CSIE | by ing. dr. Antonio Clim*
