# 📊 Learning Objectives Traceability Matrix — Week 3

> **NETWORKING class - ASE, CSIE** | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

---

## Overview

This document provides complete traceability from Learning Objectives (LOs) to all educational artefacts in the Week 3 laboratory kit. Each LO is mapped to theory, lab exercises, tests, captures, assessments, and common misconceptions.

---

## Learning Objectives Summary

| ID | Description | Bloom Level | Verb |
|----|-------------|-------------|------|
| **LO1** | Recall unicast/broadcast/multicast differences and socket options | Remember | Recall, Identify |
| **LO2** | Explain broadcast L2 constraints, multicast IGMP, TTL propagation | Understand | Explain, Describe |
| **LO3** | Implement UDP broadcast/multicast using Python sockets | Apply | Implement, Configure |
| **LO4** | Construct a TCP tunnel with bidirectional forwarding | Apply | Construct, Build |
| **LO5** | Analyse captured traffic (UDP, IGMP, TCP handshakes) | Analyze | Analyse, Differentiate |
| **LO6** | Evaluate appropriateness of communication modes for scenarios | Evaluate | Evaluate, Judge |

---

## Full Traceability Matrix

### LO1: Recall Communication Modes and Socket Options

| Artefact Type | Path | Section/Content | Status |
|---------------|------|-----------------|--------|
| **Theory** | `README.md` | §Theoretical Background: UDP Socket Programming | ✅ |
| **Theory** | `docs/theory_summary.md` | Full section on addressing modes | ✅ |
| **Glossary** | `docs/glossary.md` | Unicast, Broadcast, Multicast, SO_BROADCAST | ✅ |
| **Lab Exercise** | `src/exercises/ex_3_01_udp_broadcast.py` | Lines 16-20: KEY CONCEPTS | ✅ |
| **Lab Exercise** | `src/exercises/ex_3_02_udp_multicast.py` | Multicast group addressing | ✅ |
| **Test** | `tests/test_exercises.py` | `TestExercise1Broadcast` | ✅ |
| **Quiz** | `formative/quiz.yaml` | Q01, Q02, Q03, Q04 | ✅ |
| **Misconception** | `docs/misconceptions.md` | #1, #2, #6 | ✅ |
| **Peer Instruction** | `docs/peer_instruction.md` | Q1, Q2 | ✅ |
| **Parsons Problem** | `docs/parsons_problems.md` | P1: UDP Broadcast Sender | ✅ |

**Coverage Score: 10/10** ✅

---

### LO2: Explain L2 Constraints, IGMP, and TTL

| Artefact Type | Path | Section/Content | Status |
|---------------|------|-----------------|--------|
| **Theory** | `README.md` | §Theoretical Background: Broadcast vs Multicast | ✅ |
| **Theory** | `docs/theory_summary.md` | IGMP, TTL explanation | ✅ |
| **Glossary** | `docs/glossary.md` | IGMP, TTL, Layer 2 domain | ✅ |
| **Lab Exercise** | `src/exercises/ex_3_02_udp_multicast.py` | TTL parameter, group join | ✅ |
| **Wireshark Filter** | `README.md` | §Essential Wireshark Filters: `igmp` | ✅ |
| **Demo** | `scripts/run_demo.py` | `--demo igmp` | ✅ |
| **Test** | `tests/test_exercises.py` | `test_multicast_support` | ✅ |
| **Quiz** | `formative/quiz.yaml` | Q05, Q06, Q07, Q08 | ✅ |
| **Misconception** | `docs/misconceptions.md` | #1, #4, #5 | ✅ |
| **Peer Instruction** | `docs/peer_instruction.md` | Q3, Q4 | ✅ |
| **Analogies** | `docs/concept_analogies.md` | Radio station analogy | ✅ |

**Coverage Score: 11/10** ✅ (exceeds minimum)

---

### LO3: Implement UDP Broadcast and Multicast

| Artefact Type | Path | Section/Content | Status |
|---------------|------|-----------------|--------|
| **Theory** | `README.md` | §Exercise 1, §Exercise 2 step-by-step | ✅ |
| **Lab Exercise** | `src/exercises/ex_3_01_udp_broadcast.py` | Complete implementation (376 lines) | ✅ |
| **Lab Exercise** | `src/exercises/ex_3_02_udp_multicast.py` | Complete implementation (376 lines) | ✅ |
| **Code Tracing** | `docs/code_tracing.md` | Trace exercises for socket calls | ✅ |
| **Homework** | `homework/exercises/hw_3_01_broadcast_statistics.py` | Enhanced receiver scaffold | ✅ |
| **Homework** | `homework/exercises/hw_3_02_multicast_chat.py` | Chat app scaffold | ✅ |
| **Test** | `tests/test_exercises.py` | `test_broadcast_sender_runs`, `test_multicast_sender_runs` | ✅ |
| **Smoke Test** | `tests/smoke_test.py` | `test_broadcast_port`, `test_multicast_support` | ✅ |
| **Quiz** | `formative/quiz.yaml` | Q09, Q10 (fill-blank) | ✅ |
| **Parsons Problem** | `docs/parsons_problems.md` | P1, P2 | ✅ |
| **Cheatsheet** | `docs/commands_cheatsheet.md` | Socket creation commands | ✅ |

**Coverage Score: 11/10** ✅

---

### LO4: Construct TCP Tunnel

| Artefact Type | Path | Section/Content | Status |
|---------------|------|-----------------|--------|
| **Theory** | `README.md` | §Exercise 3, §TCP Connection Forwarding | ✅ |
| **Theory** | `docs/theory_summary.md` | Tunnel architecture | ✅ |
| **Lab Exercise** | `src/exercises/ex_3_03_tcp_tunnel.py` | Complete implementation (415 lines) | ✅ |
| **Application** | `src/apps/tcp_tunnel.py` | Production tunnel (344 lines) | ✅ |
| **Docker** | `docker/docker-compose.yml` | Router service with tunnel | ✅ |
| **Homework** | `homework/exercises/hw_3_03_tunnel_logging.py` | Enhanced tunnel scaffold | ✅ |
| **Test** | `tests/test_exercises.py` | `test_echo_through_tunnel`, `test_direct_echo` | ✅ |
| **Smoke Test** | `tests/smoke_test.py` | `test_tunnel_connectivity` | ✅ |
| **Quiz** | `formative/quiz.yaml` | Q11, Q12 | ✅ |
| **Misconception** | `docs/misconceptions.md` | #7, #8 | ✅ |
| **Parsons Problem** | `docs/parsons_problems.md` | P3, P4 | ✅ |
| **Demo** | `scripts/run_demo.py` | `--demo tunnel_flow` | ✅ |

**Coverage Score: 12/10** ✅

---

### LO5: Analyse Captured Traffic

| Artefact Type | Path | Section/Content | Status |
|---------------|------|-----------------|--------|
| **Theory** | `README.md` | §Wireshark Setup and Usage, §Packet Capture Guide | ✅ |
| **Wireshark Filters** | `README.md` | §Essential Wireshark Filters | ✅ |
| **Capture Script** | `scripts/capture_traffic.py` | Automated capture (231 lines) | ✅ |
| **PCAP Guide** | `pcap/README.md` | Capture instructions | ✅ |
| **Lab Exercise** | All exercises | tcpdump commands embedded | ✅ |
| **Test** | `tests/smoke_test.py` | `test_tcpdump_available` | ✅ |
| **Quiz** | `formative/quiz.yaml` | Q13, Q14 (analyze level) | ✅ |
| **Peer Instruction** | `docs/peer_instruction.md` | Q5: TCP tunnel connection count | ✅ |
| **Troubleshooting** | `docs/troubleshooting.md` | §Wireshark Capture Problems | ✅ |

**Coverage Score: 9/10** ✅

---

### LO6: Evaluate Communication Mode Appropriateness

| Artefact Type | Path | Section/Content | Status |
|---------------|------|-----------------|--------|
| **Theory** | `README.md` | §Broadcast vs Multicast (comparison) | ✅ |
| **Theory** | `docs/theory_summary.md` | When to use each mode | ✅ |
| **Analogies** | `docs/concept_analogies.md` | Real-world scenarios | ✅ |
| **Quiz** | `formative/quiz.yaml` | Q15 (evaluate level - streaming scenario) | ✅ |
| **Peer Instruction** | `docs/peer_instruction.md` | Discussion questions on trade-offs | ✅ |
| **Homework** | `homework/README.md` | Design decisions in assignments | ✅ |
| **Further Reading** | `docs/further_reading.md` | RFC references for deep understanding | ✅ |

**Coverage Score: 7/10** ⚠️ (adequate but could add case study)

---

## Coverage Summary

| LO | Minimum Required | Actual | Status |
|----|------------------|--------|--------|
| LO1 | 5 artefacts | 10 | ✅ Excellent |
| LO2 | 5 artefacts | 11 | ✅ Excellent |
| LO3 | 5 artefacts | 11 | ✅ Excellent |
| LO4 | 5 artefacts | 12 | ✅ Excellent |
| LO5 | 5 artefacts | 9 | ✅ Good |
| LO6 | 5 artefacts | 7 | ✅ Adequate |

**Overall Traceability: 60/60 minimum → 60/50 actual = 120%** ✅

---

## Bloom Level Distribution

| Level | LOs | Quiz Questions | Lab Exercises | Homework |
|-------|-----|----------------|---------------|----------|
| **Remember** | LO1 | Q01-Q04 (4) | — | — |
| **Understand** | LO2 | Q05-Q08 (4) | — | — |
| **Apply** | LO3, LO4 | Q09-Q12 (4) | ex_3_01, ex_3_02, ex_3_03 | hw_3_01, hw_3_02, hw_3_03 |
| **Analyze** | LO5 | Q13-Q14 (2) | PCAP analysis in all exercises | — |
| **Evaluate** | LO6 | Q15 (1) | Design decisions | Assignment design choices |

---

## Quick Reference: Where to Find What

| If student struggles with... | Direct them to... |
|------------------------------|-------------------|
| Basic terminology | `docs/glossary.md` |
| Conceptual understanding | `docs/theory_summary.md`, `docs/concept_analogies.md` |
| Common errors | `docs/misconceptions.md`, `docs/troubleshooting.md` |
| Implementation | `src/exercises/`, `docs/code_tracing.md` |
| Practice problems | `docs/parsons_problems.md`, `formative/quiz.yaml` |
| Self-assessment | `make quiz` or `python formative/run_quiz.py` |
| Peer discussion | `docs/peer_instruction.md` |

---

*NETWORKING class - ASE, CSIE | by ing. dr. Antonio Clim*
*Week 3: Network Programming — Broadcast, Multicast & TCP Tunnelling*
