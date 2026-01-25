# 🎯 Learning Objectives — Week 14: Integrated Recap

> NETWORKING class — ASE, CSIE | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

---

## Overview

This document provides the **complete traceability matrix** linking each Learning Objective (LO) to its supporting artefacts: theory, laboratory exercises, tests, packet captures, formative assessment and common misconceptions.

**Week 14 Focus:** Integration and synthesis of networking concepts from the entire course, with emphasis on practical verification and troubleshooting skills.

---

## Learning Objectives Summary

| LO ID | Description | Bloom Level | Assessment Weight |
|-------|-------------|-------------|-------------------|
| **LO1** | Recall OSI and TCP/IP layered architectures | Remember | 15% |
| **LO2** | Explain reverse proxies and load balancers | Understand | 20% |
| **LO3** | Implement multi-container Docker environment | Apply | 25% |
| **LO4** | Analyse packet captures to trace HTTP flows | Analyse | 20% |
| **LO5** | Design verification strategies for services | Create | 10% |
| **LO6** | Evaluate system behaviour under conditions | Evaluate | 10% |

---

## Detailed Traceability Matrix

### LO1: Recall OSI and TCP/IP Layered Architectures

**Bloom Level:** Remember (L1)

| Artefact Type | Location | Coverage | Status |
|---------------|----------|----------|--------|
| **Theory** | `docs/theory_summary.md#1-tcp-ip-protocol-stack-review` | Layer model comparison, encapsulation | ✅ Complete |
| **Lab Exercise** | `src/exercises/ex_14_01_review_drills.py` | Questions q01-q03 | ✅ Complete |
| **Test** | `tests/smoke_test.py::test_docker_running` | Environment check | ✅ Complete |
| **Quiz** | `formative/quiz.yaml` → q01, q02, q03, q06 | MCQ assessment | ✅ Complete |
| **Misconception** | `docs/misconceptions.md#misconception-1`, `#misconception-2`, `#misconception-3` | IP vs MAC, TCP reliability, handshake | ✅ Complete |
| **PCAP Example** | `pcap/README.md` | TCP handshake capture instructions | ✅ Complete |
| **Peer Instruction** | `docs/peer_instruction.md#question-1`, `#question-2` | Layer identification, handshake | ✅ Complete |
| **Parsons Problem** | `docs/parsons_problems.md#problem-p1` | TCP port checker | ✅ Complete |

**Verification Command:**
```bash
# Show IP and MAC addresses to demonstrate layer concepts
docker exec week14_client ip addr show eth0
docker exec week14_client ip neigh show
```

---

### LO2: Explain Reverse Proxies and Load Balancers

**Bloom Level:** Understand (L2)

| Artefact Type | Location | Coverage | Status |
|---------------|----------|----------|--------|
| **Theory** | `docs/theory_summary.md#4-load-balancing-and-reverse-proxy` | Algorithms, nginx config | ✅ Complete |
| **Lab Exercise** | `src/exercises/ex_14_02_verification_harness.py` | Distribution testing | ✅ Complete |
| **Test** | `tests/test_exercises.py` | Round-robin verification | ✅ Complete |
| **Quiz** | `formative/quiz.yaml` → q04, q05 | LB distribution, port mapping | ✅ Complete |
| **Misconception** | `docs/misconceptions.md#misconception-8`, `#misconception-9` | Random vs round-robin, sticky sessions | ✅ Complete |
| **Code Tracing** | `docs/code_tracing.md#exercise-t2` | LB algorithm tracing | ✅ Complete |
| **Peer Instruction** | `docs/peer_instruction.md#question-3` | LB algorithm selection | ✅ Complete |
| **Parsons Problem** | `docs/parsons_problems.md#problem-p2` | HTTP GET request | ✅ Complete |

**Verification Command:**
```bash
# Verify round-robin distribution
for i in $(seq 1 4); do curl -s http://localhost:8080/ | grep -o 'app[12]'; done
```

---

### LO3: Implement Multi-Container Docker Environment

**Bloom Level:** Apply (L3)

| Artefact Type | Location | Coverage | Status |
|---------------|----------|----------|--------|
| **Theory** | `docs/theory_summary.md#5-docker-networking` | Networks, compose, volumes | ✅ Complete |
| **Lab Exercise** | `src/exercises/ex_14_03_advanced_challenges.py` | Network creation, container linking | ✅ Complete |
| **Test** | `tests/smoke_test.py::test_all_containers_running` | Container health verification | ✅ Complete |
| **Quiz** | `formative/quiz.yaml` → q07, q14 | Docker commands, compose design | ✅ Complete |
| **Misconception** | `docs/misconceptions.md#misconception-5`, `#misconception-6` | Port mapping, network isolation | ✅ Complete |
| **Homework** | `homework/exercises/hw_14_01_enhanced_echo.py` | Full implementation task | ✅ Complete |
| **Parsons Problem** | `docs/parsons_problems.md#problem-p3` | Docker container management | ✅ Complete |

**Verification Command:**
```bash
# List all week14 containers and networks
docker ps --filter name=week14
docker network ls | grep week14
```

---

### LO4: Analyse Packet Captures to Trace HTTP Flows

**Bloom Level:** Analyse (L4)

| Artefact Type | Location | Coverage | Status |
|---------------|----------|----------|--------|
| **Theory** | `docs/theory_summary.md#6-packet-analysis-with-wireshark` | Wireshark filters, TCP streams | ✅ Complete |
| **Lab Exercise** | `scripts/capture_traffic.py` | PCAP capture automation | ✅ Complete |
| **Test** | `tests/test_environment.py` | PCAP validation | ✅ Complete |
| **Quiz** | `formative/quiz.yaml` → q08, q09, q10 | Wireshark filters, TCP analysis | ✅ Complete |
| **Misconception** | `docs/misconceptions.md#misconception-4` | HTTP vs HTTPS capture | ✅ Complete |
| **Code Tracing** | `docs/code_tracing.md#exercise-t1` | TCP state machine tracing | ✅ Complete |
| **PCAP Samples** | `pcap/` | Sample captures for analysis | ✅ Complete |
| **Parsons Problem** | `docs/parsons_problems.md#problem-p4` | Round-robin selector | ✅ Complete |

**Verification Command:**
```bash
# Capture HTTP traffic
python scripts/capture_traffic.py --duration 30 --output pcap/demo.pcap
```

---

### LO5: Design Verification Strategies for Network Services

**Bloom Level:** Create (L6)

| Artefact Type | Location | Coverage | Status |
|---------------|----------|----------|--------|
| **Theory** | `docs/theory_summary.md#7-troubleshooting-methodology` | Test patterns, health checks | ✅ Complete |
| **Lab Exercise** | `src/exercises/ex_14_02_verification_harness.py` | Test design tasks | ✅ Complete |
| **Test** | `tests/test_validators.py` | Verification utilities | ✅ Complete |
| **Quiz** | `formative/quiz.yaml` → q12, q13, q15 | Diagnosis, test design, troubleshooting | ✅ Complete |
| **Troubleshooting** | `docs/troubleshooting.md` | Systematic problem-solving | ✅ Complete |
| **Homework** | `homework/exercises/hw_14_03_pcap_analyser.py` | Analysis tool design | ✅ Complete |
| **Parsons Problem** | `docs/parsons_problems.md#problem-p5` | Docker network parser | ✅ Complete |

**Verification Command:**
```bash
# Run validation suite
make validate-full
python tests/smoke_test.py
```

---

### LO6: Evaluate System Behaviour Under Various Conditions

**Bloom Level:** Evaluate (L5)

| Artefact Type | Location | Coverage | Status |
|---------------|----------|----------|--------|
| **Theory** | `docs/theory_summary.md#7-troubleshooting-methodology` | Failure patterns, recovery | ✅ Complete |
| **Lab Exercise** | `scripts/run_demo.py --demo failover` | Fault injection experiments | ✅ Complete |
| **Test** | `tests/test_environment.py` | Failure scenario tests | ✅ Complete |
| **Quiz** | `formative/quiz.yaml` → q10, q11 | 502 diagnosis, distribution anomaly | ✅ Complete |
| **Misconception** | `docs/misconceptions.md#misconception-7` | Container running ≠ service working | ✅ Complete |
| **Peer Instruction** | `docs/peer_instruction.md#question-4`, `#question-5` | Failure analysis scenarios | ✅ Complete |
| **Practical Exam** | `formative/practical_exam.py` | Live troubleshooting tasks | ✅ Complete |

**Verification Command:**
```bash
# Test failure scenario
docker stop week14_app1
curl -v http://localhost:8080/  # Observe LB behaviour
docker start week14_app1
```

---

## Bloom Taxonomy Coverage Summary

| Level | LO Coverage | Quiz Questions | Assessment |
|-------|-------------|----------------|------------|
| **L1: Remember** | LO1 | q01, q02, q03 | 3 pts (7%) |
| **L2: Understand** | LO2 | q04, q05, q06 | 6 pts (14%) |
| **L3: Apply** | LO3 | q07, q08 | 4 pts (10%) |
| **L4: Analyse** | LO4 | q09, q10 | 6 pts (14%) |
| **L5: Evaluate** | LO6 | q11, q12 | 8 pts (19%) |
| **L6: Create** | LO5 | q13, q14, q15 | 15 pts (36%) |

**Total:** 42 points across 15 questions covering all 6 Bloom levels.

---

## Parsons Problems Traceability

| Problem | LO Reference | Distractors | Difficulty |
|---------|--------------|-------------|------------|
| P1: TCP Port Checker | LO1 | 1 (bind) | Intermediate |
| P2: HTTP GET Request | LO2 | 1 (single recv) | Intermediate |
| P3: Container Status Checker | LO3 | 1 (returncode check) | Basic |
| P4: Round-Robin Backend Selector | LO4 | 1 (no modulo) | Intermediate |
| P5: Parse Docker Network Output | LO5 | 1 (wrong indexing) | Advanced |

---

## Assessment Methods Summary

| Method | Coverage | Weight | Anti-AI |
|--------|----------|--------|---------|
| **Formative Quiz** | All LOs | 20% | Partial |
| **Environment-Verified Quiz** | All LOs | 25% | High |
| **Practical Examination** | LO3, LO4, LO5, LO6 | 30% | Very High |
| **Homework Assignments** | LO2, LO3, LO4 | 25% | Medium |

---

## Quick Reference: LO to Artefact Mapping

```
LO1 (Remember) ─────┬── theory_summary.md §1
                    ├── quiz.yaml q01-03, q06
                    ├── misconceptions.md #1-3
                    ├── peer_instruction.md #1-2
                    └── parsons_problems.md P1

LO2 (Understand) ───┬── theory_summary.md §4
                    ├── quiz.yaml q04-05
                    ├── misconceptions.md #8-9
                    ├── peer_instruction.md #3
                    └── parsons_problems.md P2

LO3 (Apply) ────────┬── theory_summary.md §5
                    ├── quiz.yaml q07, q14
                    ├── misconceptions.md #5-6
                    ├── homework hw_14_01
                    └── parsons_problems.md P3

LO4 (Analyse) ──────┬── theory_summary.md §6
                    ├── quiz.yaml q08-10
                    ├── misconceptions.md #4
                    ├── code_tracing.md T1
                    └── parsons_problems.md P4

LO5 (Create) ───────┬── theory_summary.md §7
                    ├── quiz.yaml q12-13, q15
                    ├── troubleshooting.md
                    ├── homework hw_14_03
                    └── parsons_problems.md P5

LO6 (Evaluate) ─────┬── theory_summary.md §7
                    ├── quiz.yaml q10-11
                    ├── misconceptions.md #7
                    ├── peer_instruction.md #4-5
                    └── practical_exam.py
```

---

## Verification Checklist

Before considering Week 14 complete, verify:

- [x] All quiz questions link to at least one LO
- [x] Each LO has at least 2 quiz questions
- [x] All Bloom levels (L1-L6) are covered
- [x] Each Parsons problem has at least 1 distractor
- [x] Misconceptions are referenced from quiz explanations
- [x] Practical exam tasks are environment-dependent

---

*NETWORKING class — ASE, CSIE | Computer Networks Laboratory*
*LO Traceability Matrix v2.1.0 | Week 14*
*by ing. dr. Antonio Clim*
