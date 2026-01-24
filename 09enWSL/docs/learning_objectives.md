# 🎯 Learning Objectives Traceability Matrix — Week 9

> Session Layer (L5) and Presentation Layer (L6)
> NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

This document provides complete traceability from each Learning Objective (LO) to
all supporting materials in the laboratory kit. Use this matrix to ensure comprehensive
coverage during study and to identify resources for specific topics.

---

## Overview

| LO | Description | Bloom Level | Primary Exercise |
|----|-------------|-------------|------------------|
| LO1 | Identify connection vs session characteristics | Understand | ex_9_02 |
| LO2 | Explain endianness and byte-order mechanisms | Apply | ex_9_01 |
| LO3 | Implement binary framing protocol | Apply | ex_9_01, hw_9_01 |
| LO4 | Demonstrate multi-client FTP session management | Apply | ex_9_03, ex_9_04 |
| LO5 | Analyse packet captures for protocol events | Analyse | capture_traffic.py |
| LO6 | Design checkpoint-recovery mechanisms | Create | hw_9_02 |

---

## Detailed Traceability Matrix

### LO1: Identify Connection vs Session Characteristics

> **Statement:** Identify the distinguishing characteristics of connection-oriented
> transport versus session-based communication, articulating why FTP requires
> separate control and data channels.

| Resource Type | Location | Specific Section |
|---------------|----------|------------------|
| **Theory** | `docs/theory_summary.md` | Lines 33-79: "Session Layer (L5)" |
| **Theory** | `README.md` | Lines 196-202: "Overview" |
| **Exercise** | `src/exercises/ex_9_02_implement_pseudo_ftp.py` | Session state machine implementation |
| **Exercise** | `src/exercises/ex_9_03_ftp_client_demo.py` | FTP session lifecycle demo |
| **Test** | `tests/test_exercises.py` | `test_exercise_2_pseudo_ftp()` |
| **Quiz** | `formative/quiz.yaml` | Questions q01, q02 |
| **Misconception** | `docs/misconceptions.md` | #1: "TCP connection IS a session" |
| **Misconception** | `docs/misconceptions.md` | #2: "FTP uses one connection" |
| **Peer Instruction** | `docs/peer_instruction.md` | Questions 2, 3 |
| **Parsons** | `docs/parsons_problems.md` | P2: FTP Session Setup |
| **Glossary** | `docs/glossary.md` | "Session", "Control Channel", "Data Channel" |

**Verification Command:**
```bash
grep -l "session\|Session" docs/*.md src/exercises/*.py
```

---

### LO2: Explain Endianness and Byte-Order Mechanisms

> **Statement:** Explain the mechanisms by which the Presentation Layer resolves
> byte-ordering ambiguity through explicit endianness specification in binary protocols.

| Resource Type | Location | Specific Section |
|---------------|----------|------------------|
| **Theory** | `docs/theory_summary.md` | Lines 80-150: "Presentation Layer (L6)" |
| **Theory** | `README.md` | Lines 277-331: "Exercise 1: Binary Encoding" |
| **Exercise** | `src/exercises/ex_9_01_demonstrate_endianness.py` | Full file (454 lines) |
| **Test** | `tests/test_exercises.py` | `test_exercise_1_endianness()` Tests 1.1-1.4 |
| **Quiz** | `formative/quiz.yaml` | Questions q03, q04, q05 |
| **Misconception** | `docs/misconceptions.md` | #5: "My computer uses big-endian" |
| **Misconception** | `docs/misconceptions.md` | #7: "struct.pack preserves boundaries" |
| **Peer Instruction** | `docs/peer_instruction.md` | Question 1 |
| **Parsons** | `docs/parsons_problems.md` | P1: Pack a Network Message |
| **Code Tracing** | `docs/code_tracing.md` | Exercises CT1-CT4 |
| **Glossary** | `docs/glossary.md` | "Big-Endian", "Little-Endian", "Network Byte Order" |
| **Cheatsheet** | `docs/commands_cheatsheet.md` | struct format strings section |

**Verification Command:**
```bash
python src/exercises/ex_9_01_demonstrate_endianness.py --selftest --demo
```

---

### LO3: Implement Binary Framing Protocol

> **Statement:** Implement a custom binary framing protocol using Python's `struct`
> module, incorporating length prefixes, message type identifiers and CRC-32 verification.

| Resource Type | Location | Specific Section |
|---------------|----------|------------------|
| **Theory** | `docs/theory_summary.md` | Lines 151-200: "Binary Protocol Design" |
| **Theory** | `README.md` | Lines 629-637: "Binary Protocol Design Principles" |
| **Exercise** | `src/exercises/ex_9_01_demonstrate_endianness.py` | `pack_message()`, `unpack_message()` |
| **Homework** | `homework/exercises/hw_9_01_binary_fragmentation.py` | Full assignment (479 lines) |
| **Test** | `tests/test_exercises.py` | Test 1.4: Protocol header structure |
| **Expected Output** | `tests/expected_outputs.md` | "Binary Framing Demo" section |
| **Quiz** | `formative/quiz.yaml` | Questions q06, q07 |
| **Misconception** | `docs/misconceptions.md` | #6: "CRC-32 provides security" |
| **Parsons** | `docs/parsons_problems.md` | P1, P3 |
| **Pair Programming** | `docs/pair_programming_guide.md` | Exercise P1: Binary Protocol Header |
| **Glossary** | `docs/glossary.md` | "Magic Number", "Length Prefix", "CRC-32" |

**Verification Command:**
```bash
python tests/test_exercises.py --exercise 1
```

---

### LO4: Demonstrate Multi-Client FTP Session Management

> **Statement:** Demonstrate multi-client FTP session management within a containerised
> environment, observing authentication flows and passive mode negotiation.

| Resource Type | Location | Specific Section |
|---------------|----------|------------------|
| **Theory** | `docs/theory_summary.md` | Lines 54-79: "Session Layer in Practice" |
| **Theory** | `README.md` | Lines 334-391: "Exercise 2: Custom FTP Server" |
| **Exercise** | `src/exercises/ex_9_03_ftp_client_demo.py` | FTP client implementation |
| **Exercise** | `src/exercises/ex_9_04_ftp_server_demo.py` | FTP server implementation |
| **Demo** | `scripts/run_demo.py` | `--demo multi_client` |
| **Docker** | `docker/docker-compose.yml` | ftp-server, client1, client2 services |
| **Test** | `tests/test_exercises.py` | `test_exercise_2_pseudo_ftp()` |
| **Quiz** | `formative/quiz.yaml` | Questions q08, q09 |
| **Misconception** | `docs/misconceptions.md` | #3: "Active and Passive modes are interchangeable" |
| **Misconception** | `docs/misconceptions.md` | #4: "Closing control channel stops transfer" |
| **Peer Instruction** | `docs/peer_instruction.md` | Question 2 |
| **Pair Programming** | `docs/pair_programming_guide.md` | Exercise P2: FTP Session Lifecycle |
| **Troubleshooting** | `docs/troubleshooting.md` | "FTP Issues" section |
| **Glossary** | `docs/glossary.md` | "PASV", "Active Mode", "Passive Mode" |

**Verification Command:**
```bash
python scripts/run_demo.py --demo ftp_session
docker compose -f docker/docker-compose.yml ps
```

---

### LO5: Analyse Packet Captures for Protocol Events

> **Statement:** Analyse packet captures to distinguish control channel commands
> from data channel transfers, correlating protocol-level events with application behaviour.

| Resource Type | Location | Specific Section |
|---------------|----------|------------------|
| **Theory** | `README.md` | Lines 497-536: "Packet Capture and Analysis" |
| **Theory** | `README.md` | Lines 146-194: "Wireshark Setup and Usage" |
| **Script** | `scripts/capture_traffic.py` | Full file (456 lines) |
| **PCAP Guide** | `pcap/README.md` | Capture instructions |
| **Demo** | `scripts/run_demo.py` | `--demo binary_protocol` |
| **Quiz** | `formative/quiz.yaml` | Question q10 |
| **Misconception** | `docs/misconceptions.md` | #8: "PASV port is single number" |
| **Peer Instruction** | `docs/peer_instruction.md` | Question 5 |
| **Cheatsheet** | `docs/commands_cheatsheet.md` | Wireshark filters section |
| **Troubleshooting** | `docs/troubleshooting.md` | "Wireshark Issues" section |
| **Glossary** | `docs/glossary.md` | "PCAP", "Wireshark", "TCP Stream" |

**Verification Command:**
```bash
python scripts/capture_traffic.py --duration 10 --output pcap/test_capture.pcap
# Then analyse with Wireshark: filter tcp.port == 2121
```

---

### LO6: Design Checkpoint-Recovery Mechanisms

> **Statement:** Design a checkpoint-recovery mechanism suitable for resuming
> interrupted file transfers, applying Session Layer principles to practical scenarios.

| Resource Type | Location | Specific Section |
|---------------|----------|------------------|
| **Theory** | `docs/theory_summary.md` | Lines 64-79: "Checkpoint and Recovery" |
| **Theory** | `README.md` | Lines 576-584: "Assignment 2: Session Checkpoint Recovery" |
| **Homework** | `homework/exercises/hw_9_02_checkpoint_recovery.py` | Full assignment (599 lines) |
| **Homework Spec** | `homework/README.md` | Assignment 2 requirements and rubric |
| **Quiz** | `formative/quiz.yaml` | Questions q11, q12 |
| **Misconception** | `docs/misconceptions.md` | #4: "Closing control channel stops transfer" |
| **Pair Programming** | `docs/pair_programming_guide.md` | Exercise P3: Pseudo-FTP Implementation |
| **Glossary** | `docs/glossary.md` | "Checkpoint", "Synchronisation Point", "Recovery" |
| **Further Reading** | `docs/further_reading.md` | RFC 959 sections on restart |

**Verification Command:**
```bash
python homework/exercises/hw_9_02_checkpoint_recovery.py --help
```

---

## Coverage Summary

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    LEARNING OBJECTIVES COVERAGE MATRIX                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   Resource Type        LO1   LO2   LO3   LO4   LO5   LO6   Coverage        │
│   ─────────────────────────────────────────────────────────────────────────│
│   Theory Summary       ✅    ✅    ✅    ✅    ⚠️    ✅    5/6 (83%)        │
│   README.md            ✅    ✅    ✅    ✅    ✅    ✅    6/6 (100%)       │
│   Exercises            ✅    ✅    ✅    ✅    ✅    —     5/6 (83%)        │
│   Homework             —     —     ✅    —     —     ✅    2/6 (33%)        │
│   Tests                ✅    ✅    ✅    ✅    ⚠️    ⚠️    4/6 (67%)        │
│   Quiz                 ✅    ✅    ✅    ✅    ✅    ✅    6/6 (100%)       │
│   Misconceptions       ✅    ✅    ✅    ✅    ✅    ✅    6/6 (100%)       │
│   Peer Instruction     ✅    ✅    —     ✅    ✅    —     4/6 (67%)        │
│   Parsons Problems     ✅    ✅    ✅    —     —     —     3/6 (50%)        │
│   Glossary             ✅    ✅    ✅    ✅    ✅    ✅    6/6 (100%)       │
│                                                                             │
│   Legend: ✅ = Complete coverage  ⚠️ = Partial  — = Not applicable         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Quick Reference: Find Resources by Topic

| If you need help with... | Start here | Then check |
|--------------------------|------------|------------|
| Session vs Connection concept | `docs/misconceptions.md#1` | `docs/theory_summary.md` |
| Big-endian vs Little-endian | `src/exercises/ex_9_01...py` | `docs/code_tracing.md` |
| struct.pack format strings | `docs/commands_cheatsheet.md` | `docs/code_tracing.md` |
| FTP dual-channel architecture | `docs/misconceptions.md#2` | `README.md` Exercise 2 |
| Passive mode port calculation | `docs/misconceptions.md#8` | `docs/peer_instruction.md` Q5 |
| CRC-32 vs security hashes | `docs/misconceptions.md#6` | `docs/theory_summary.md` |
| Docker container issues | `docs/troubleshooting.md` | `README.md` Troubleshooting |
| Wireshark capture setup | `README.md` Wireshark section | `docs/commands_cheatsheet.md` |

---

## Self-Assessment Checklist

Before the laboratory session ends, verify you can:

- [ ] **LO1:** Explain why FTP session state is lost when TCP reconnects
- [ ] **LO2:** Convert a 32-bit integer to network byte order using struct.pack
- [ ] **LO3:** Design a protocol header with magic, length, type and CRC fields
- [ ] **LO4:** Start the Docker environment and observe multi-client FTP sessions
- [ ] **LO5:** Capture FTP traffic and identify control vs data channel packets
- [ ] **LO6:** Describe how checkpoint-based recovery reduces retransmission

**Run the formative quiz to verify understanding:**
```bash
python formative/run_quiz.py
```

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
*Week 9: Session Layer and Presentation Layer*
