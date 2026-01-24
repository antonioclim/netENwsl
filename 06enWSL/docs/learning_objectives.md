# 🎯 Learning Objectives & Traceability Matrix — Week 6

> Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

## Overview

This document provides a **complete mapping** between Learning Objectives (LOs) and the artefacts that support them. Use this matrix to:
- Verify coverage of all objectives
- Find relevant materials for specific topics
- Plan study sessions before the laboratory

---

## Learning Objectives Summary

| LO | Bloom Level | Description |
|----|-------------|-------------|
| **LO1** | Remember | Recall the purpose and classification of NAT variants (static, dynamic, PAT) and the role of auxiliary protocols (ARP, DHCP, ICMP, NDP) |
| **LO2** | Understand | Explain how PAT translation tables maintain bidirectional session state and why this mechanism creates challenges for inbound connections |
| **LO3** | Apply | Implement NAT/MASQUERADE rules using iptables on a multi-homed Linux router within a simulated topology |
| **LO4** | Apply | Demonstrate SDN flow installation by observing controller-switch communication and inspecting flow tables with ovs-ofctl |
| **LO5** | Analyse | Analyse the behavioural differences between permitted and blocked traffic in an SDN topology, correlating packet outcomes with installed flow rules |
| **LO6** | Analyse | Compare traditional distributed routing with centralised SDN control, articulating trade-offs in scalability, flexibility and failure domains |
| **LO7** | Create | Design custom OpenFlow policies that implement per-host, per-protocol access control within a software-defined network |

---

## Traceability Matrix

### Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Primary coverage — directly addresses LO |
| 📖 | Supporting material — provides context |
| 🧪 | Practical exercise — hands-on application |
| ❓ | Assessment — validates understanding |

---

### LO1: Recall NAT Variants & Supporting Protocols

| Artefact Type | File Path | Coverage |
|---------------|-----------|----------|
| **Theory** | `docs/theory_summary.md` § NAT Variants, Supporting Protocols | ✅ Primary |
| **Theory** | `README.md` § Theoretical Background | 📖 Summary |
| **Glossary** | `docs/glossary.md` § NAT Terms, Protocol Numbers | 📖 Reference |
| **Lab Exercise** | `src/exercises/ex_6_01_nat_topology.py` | 🧪 NAT config |
| **Homework** | `homework/exercises/hw_6_02_arp_investigation.py` | 🧪 ARP analysis |
| **Misconception** | `docs/misconceptions.md` #M1-M4 | ❓ Self-check |
| **Quiz** | `formative/quiz.yaml` q01-q03 | ❓ Assessment |
| **Peer Instruction** | `docs/peer_instruction.md` Q1, Q5 | ❓ Discussion |

---

### LO2: Explain PAT Translation Tables

| Artefact Type | File Path | Coverage |
|---------------|-----------|----------|
| **Theory** | `docs/theory_summary.md` § PAT Operation | ✅ Primary |
| **Code Tracing** | `docs/code_tracing.md` T1, T4 | ✅ Trace exercises |
| **Lab Exercise** | `src/exercises/ex_6_01_nat_topology.py` § conntrack | 🧪 Observation |
| **Application** | `src/apps/nat_observer.py` | 🧪 Visualisation |
| **Homework** | `homework/exercises/hw_6_01_nat_analysis.py` | 🧪 Analysis |
| **Misconception** | `docs/misconceptions.md` #M2, M4 | ❓ Self-check |
| **Quiz** | `formative/quiz.yaml` q04-q05 | ❓ Assessment |
| **Peer Instruction** | `docs/peer_instruction.md` Q2 | ❓ Discussion |

---

### LO3: Implement NAT/MASQUERADE

| Artefact Type | File Path | Coverage |
|---------------|-----------|----------|
| **Commands** | `docs/commands_cheatsheet.md` § iptables | ✅ Reference |
| **Lab Exercise** | `src/exercises/ex_6_01_nat_topology.py` | ✅ Primary |
| **Parsons Problem** | `docs/parsons_problems.md` P1 | 🧪 Ordering |
| **Troubleshooting** | `docs/troubleshooting.md` § NAT Issues | 📖 Debug guide |
| **Misconception** | `docs/misconceptions.md` #M3 | ❓ Self-check |
| **Quiz** | `formative/quiz.yaml` q06-q07 | ❓ Assessment |
| **Test** | `tests/test_exercises.py` test_exercise_1 | ❓ Validation |

---

### LO4: Demonstrate SDN Flow Installation

| Artefact Type | File Path | Coverage |
|---------------|-----------|----------|
| **Theory** | `docs/theory_summary.md` § OpenFlow Protocol | ✅ Primary |
| **Commands** | `docs/commands_cheatsheet.md` § ovs-ofctl | ✅ Reference |
| **Lab Exercise** | `src/exercises/ex_6_02_sdn_topology.py` | ✅ Primary |
| **Application** | `src/apps/sdn_policy_controller.py` | 🧪 Controller |
| **Glossary** | `docs/glossary.md` § OpenFlow Terms | 📖 Reference |
| **Quiz** | `formative/quiz.yaml` q08 | ❓ Assessment |
| **Test** | `tests/test_exercises.py` test_exercise_2 | ❓ Validation |

---

### LO5: Analyse Permitted/Blocked Traffic

| Artefact Type | File Path | Coverage |
|---------------|-----------|----------|
| **Code Tracing** | `docs/code_tracing.md` T2 | ✅ Primary |
| **Lab Exercise** | `src/exercises/ex_6_02_sdn_topology.py` Ex2-Ex3 | ✅ Hands-on |
| **Misconception** | `docs/misconceptions.md` #M6, M8 | ❓ Priority trap |
| **Quiz** | `formative/quiz.yaml` q09-q10 | ❓ Assessment |
| **Peer Instruction** | `docs/peer_instruction.md` Q3 | ❓ Discussion |
| **Troubleshooting** | `docs/troubleshooting.md` § SDN Issues | 📖 Debug guide |

---

### LO6: Compare Traditional vs SDN

| Artefact Type | File Path | Coverage |
|---------------|-----------|----------|
| **Theory** | `docs/theory_summary.md` § SDN Architecture, Benefits, Challenges | ✅ Primary |
| **Concept Analogies** | `docs/concept_analogies.md` § SDN analogies | 📖 Understanding |
| **Glossary** | `docs/glossary.md` § SDN Architecture Terms | 📖 Reference |
| **Lab Discussion** | `README.md` § Reflection Questions | 🧪 Discussion |
| **Misconception** | `docs/misconceptions.md` #M5 | ❓ Self-check |
| **Quiz** | `formative/quiz.yaml` q11 | ❓ Assessment |
| **Peer Instruction** | `docs/peer_instruction.md` Q4 | ❓ Discussion |

---

### LO7: Design OpenFlow Policies

| Artefact Type | File Path | Coverage |
|---------------|-----------|----------|
| **Parsons Problem** | `docs/parsons_problems.md` P2, P3 | ✅ Design practice |
| **Lab Exercise** | `src/exercises/ex_6_02_sdn_topology.py` Ex3 | ✅ Custom policies |
| **Commands** | `docs/commands_cheatsheet.md` § Flow Rule Syntax | 📖 Reference |
| **Application** | `src/apps/sdn_policy_controller.py` | 🧪 Implementation |
| **Misconception** | `docs/misconceptions.md` #M6, M7 | ❓ Priority/timeout |
| **Quiz** | `formative/quiz.yaml` q12 | ❓ Assessment |

---

## Coverage Summary

| LO | Theory | Lab | Test | Misconception | Quiz | Peer | Total |
|----|--------|-----|------|---------------|------|------|-------|
| LO1 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 6/6 |
| LO2 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 6/6 |
| LO3 | ✅ | ✅ | ✅ | ✅ | ✅ | — | 5/6 |
| LO4 | ✅ | ✅ | ✅ | — | ✅ | — | 4/6 |
| LO5 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 6/6 |
| LO6 | ✅ | ✅ | — | ✅ | ✅ | ✅ | 5/6 |
| LO7 | ✅ | ✅ | — | ✅ | ✅ | — | 4/6 |

**Overall Coverage:** All LOs have minimum 4/6 artefact types supporting them.

---

## Recommended Study Path

### Before Laboratory (30-45 min)
1. `formative/run_quiz.py` — Identify knowledge gaps
2. `docs/theory_summary.md` — Review concepts for weak areas
3. `docs/misconceptions.md` — Check common errors

### During Laboratory (90 min)
1. `README.md` Quick Start — Setup environment
2. `src/exercises/ex_6_01_*.py` — NAT exercises
3. `src/exercises/ex_6_02_*.py` — SDN exercises
4. `docs/troubleshooting.md` — If issues arise

### After Laboratory (30 min)
1. `docs/code_tracing.md` — Reinforce understanding
2. `homework/` — Complete assignments
3. `docs/further_reading.md` — Deep dive (optional)

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
