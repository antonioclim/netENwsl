# 🎯 Learning Objectives — Week 14: Integrated Recap

> NETWORKING class — ASE, CSIE | Computer Networks Laboratory  
> by ing. dr. Antonio Clim

---

## Overview

This document provides the **complete traceability matrix** linking each Learning Objective (LO) to its supporting artifacts: theory, laboratory exercises, tests, packet captures, and common misconceptions.

**Week 14 Focus:** Integration and synthesis of networking concepts from the entire course, with emphasis on practical verification and troubleshooting skills.

---

## Learning Objectives Summary

| LO ID | Description | Bloom Level | Assessment Weight |
|-------|-------------|-------------|-------------------|
| **LO1** | Recall OSI and TCP/IP layered architectures | Remember | 15% |
| **LO2** | Explain reverse proxies and load balancers | Understand | 20% |
| **LO3** | Implement multi-container Docker environment | Apply | 25% |
| **LO4** | Analyse packet captures to trace HTTP flows | Analyse | 20% |
| **LO5** | Design verification strategies for services | Design | 10% |
| **LO6** | Evaluate system behaviour under conditions | Evaluate | 10% |

---

## Detailed Traceability Matrix

### LO1: Recall OSI and TCP/IP Layered Architectures

| Artifact Type | Location | Coverage | Status |
|---------------|----------|----------|--------|
| **Theory** | `docs/theory_summary.md#1-tcp-ip-protocol-stack-review` | Layer model comparison, encapsulation | ✅ Complete |
| **Lab Exercise** | `src/exercises/ex_14_01_review_drills.py` | Questions q01-q03 | ✅ Complete |
| **Test** | `tests/smoke_test.py::test_docker_running` | Environment check | ✅ Complete |
| **Quiz** | `formative/quiz_week14.yaml` → q01, q02, q03, q06 | MCQ assessment | ✅ Complete |
| **Misconception** | `docs/misconceptions.md#misconception-1`, `#misconception-2`, `#misconception-3` | IP vs MAC, TCP reliability, handshake | ✅ Complete |
| **PCAP Example** | `pcap/README.md` | TCP handshake capture instructions | ✅ Complete |
| **Peer Instruction** | `docs/peer_instruction.md#question-1`, `#question-2` | Layer identification, handshake | ✅ Complete |

**Verification Command:**
```bash
# Show IP and MAC addresses to demonstrate layer concepts
docker exec week14_client ip addr show eth0
docker exec week14_client ip neigh show
```

---

### LO2: Explain Reverse Proxies and Load Balancers

| Artifact Type | Location | Coverage | Status |
|---------------|----------|----------|--------|
| **Theory** | `docs/theory_summary.md#4-load-balancing-and-reverse-proxies` | Architecture, round-robin, headers | ✅ Complete |
| **Lab Exercise** | `src/exercises/ex_14_02_verification_harness.py` | LB testing | ✅ Complete |
| **Test** | `tests/smoke_test.py::test_round_robin` | Distribution verification | ✅ Complete |
| **Quiz** | `formative/quiz_week14.yaml` → q04 | Round-robin understanding | ✅ Complete |
| **Misconception** | `docs/misconceptions.md#misconception-8`, `#misconception-9` | Round-robin not random, LB overhead | ✅ Complete |
| **Application** | `src/apps/lb_proxy.py` | Working implementation | ✅ Complete |
| **Peer Instruction** | `docs/peer_instruction.md#question-3` | Distribution prediction | ✅ Complete |
| **Code Tracing** | `docs/code_tracing.md#exercise-t3` | Round-robin algorithm | ✅ Complete |

**Verification Command:**
```bash
# Observe round-robin distribution
for i in 1 2 3 4; do curl -s http://localhost:8080/ | grep -o "app[12]"; done
# Expected: app1, app2, app1, app2
```

---

### LO3: Implement Multi-Container Docker Environment

| Artifact Type | Location | Coverage | Status |
|---------------|----------|----------|--------|
| **Theory** | `docs/theory_summary.md#8-docker-networking` | Network types, service discovery | ✅ Complete |
| **Lab Exercise** | `docker/docker-compose.yml` | Complete topology definition | ✅ Complete |
| **Test** | `tests/test_environment.py` | Docker environment validation | ✅ Complete |
| **Quiz** | `formative/quiz_week14.yaml` → q05, q07 | Port mapping, commands | ✅ Complete |
| **Misconception** | `docs/misconceptions.md#misconception-4` through `#misconception-7` | Container vs VM, ports, networks, data | ✅ Complete |
| **Troubleshooting** | `docs/troubleshooting.md#docker-issues` | Common Docker problems | ✅ Complete |
| **Peer Instruction** | `docs/peer_instruction.md#question-4`, `#question-5` | Port mapping, network isolation | ✅ Complete |
| **Parsons Problem** | `docs/parsons_problems.md#problem-p3` | Container status checker | ✅ Complete |

**Verification Command:**
```bash
# Verify network isolation
docker exec week14_client ping -c 1 172.20.0.2  # Should fail (different network)
docker exec week14_client ping -c 1 172.21.0.10 # Should succeed (same network)
```

---

### LO4: Analyse Packet Captures to Trace HTTP Flows

| Artifact Type | Location | Coverage | Status |
|---------------|----------|----------|--------|
| **Theory** | `docs/theory_summary.md#6-packet-analysis-concepts` | Capture points, Wireshark filters | ✅ Complete |
| **Lab Exercise** | `src/exercises/ex_14_03_advanced_challenges.py` | PCAP analysis tasks | ✅ Complete |
| **Test** | `tests/expected_outputs.md` | Expected capture patterns | ✅ Complete |
| **Quiz** | `formative/quiz_week14.yaml` → q08, q09 | Wireshark filters, RST analysis | ✅ Complete |
| **Misconception** | `docs/misconceptions.md#misconception-12` | Wireshark visibility limits | ✅ Complete |
| **PCAP Capture** | `scripts/capture_traffic.py` | Automated capture script | ✅ Complete |
| **Code Tracing** | `docs/code_tracing.md#exercise-t1`, `#exercise-t2` | Socket connections, HTTP parsing | ✅ Complete |
| **Commands** | `docs/commands_cheatsheet.md` | Wireshark filter reference | ✅ Complete |

**Verification Command:**
```bash
# Capture traffic while generating requests
python scripts/capture_traffic.py &
curl http://localhost:8080/
# Analyse with: tshark -r artifacts/capture.pcap -Y "http"
```

---

### LO5: Design Verification Strategies for Network Services

| Artifact Type | Location | Coverage | Status |
|---------------|----------|----------|--------|
| **Theory** | `docs/troubleshooting.md` | Symptom → Cause → Fix methodology | ✅ Complete |
| **Lab Exercise** | `src/exercises/ex_14_02_verification_harness.py` | Test harness design | ✅ Complete |
| **Test** | `tests/smoke_test.py` | Complete verification suite | ✅ Complete |
| **Homework** | `homework/exercises/hw_14_01_enhanced_echo.py` | Test suite deliverable | ✅ Complete |
| **Scripts** | `setup/verify_environment.py` | Environment validation | ✅ Complete |
| **Code Tracing** | `docs/code_tracing.md#exercise-t4` | Container health check | ✅ Complete |
| **Parsons Problem** | `docs/parsons_problems.md#problem-p1` | Port checker function | ✅ Complete |

**Verification Command:**
```bash
# Run comprehensive verification
python tests/smoke_test.py -v
python setup/verify_environment.py
```

---

### LO6: Evaluate System Behaviour Under Various Conditions

| Artifact Type | Location | Coverage | Status |
|---------------|----------|----------|--------|
| **Theory** | `docs/theory_summary.md#4` | Failover mechanisms | ✅ Complete |
| **Lab Exercise** | `src/exercises/ex_14_03_advanced_challenges.py` | Failure scenario testing | ✅ Complete |
| **Test** | `tests/test_exercises.py` | Behaviour validation | ✅ Complete |
| **Quiz** | `formative/quiz_week14.yaml` → q10 | 502 error diagnosis | ✅ Complete |
| **Misconception** | `docs/misconceptions.md#misconception-9`, `#misconception-11` | LB overhead, HTTP 200 | ✅ Complete |
| **Peer Instruction** | `docs/peer_instruction.md#question-3` | Backend failure scenarios | ✅ Complete |
| **Homework** | `homework/exercises/hw_14_02_weighted_lb.py` | Weighted distribution analysis | ✅ Complete |

**Verification Command:**
```bash
# Test failover: stop one backend and observe behaviour
docker stop week14_app2
for i in 1 2 3 4; do curl -s http://localhost:8080/ | grep -o "app[12]"; done
# All requests should go to app1
docker start week14_app2
```

---

## Bloom's Taxonomy Coverage

| Bloom Level | LO(s) | Question Types | Assessment Methods |
|-------------|-------|----------------|-------------------|
| **Remember** | LO1 | MCQ, Fill-blank | Quiz q01-q03, Review drills |
| **Understand** | LO2 | MCQ, Explanation | Quiz q04-q06, Peer instruction |
| **Apply** | LO3 | Practical, Commands | Quiz q07-q08, Docker exercises |
| **Analyse** | LO4 | PCAP analysis, Debugging | Quiz q09, Code tracing |
| **Evaluate** | LO6 | Scenario analysis | Quiz q10, Peer instruction |
| **Create** | LO5 | Design tasks | Homework assignments, Projects |

---

## Assessment Alignment

### Formative Assessment (Quiz)

| Question | LO | Bloom | Points |
|----------|-----|-------|--------|
| q01 | LO1 | Remember | 1 |
| q02 | LO1 | Remember | 1 |
| q03 | LO1 | Remember | 1 |
| q04 | LO2 | Understand | 2 |
| q05 | LO3 | Understand | 2 |
| q06 | LO1 | Understand | 2 |
| q07 | LO3 | Apply | 2 |
| q08 | LO4 | Apply | 2 |
| q09 | LO4 | Analyse | 3 |
| q10 | LO6 | Analyse | 3 |

**Run quiz:** `make quiz` or `python formative/run_quiz.py`

### Summative Assessment (Homework)

| Assignment | LO Coverage | Weight |
|------------|-------------|--------|
| hw_14_01_enhanced_echo.py | LO3, LO5 | 30% |
| hw_14_02_weighted_lb.py | LO2, LO6 | 35% |
| hw_14_03_pcap_analyser.py | LO4, LO1 | 35% |

---

## Cross-Reference: Files → Learning Objectives

| File | LO1 | LO2 | LO3 | LO4 | LO5 | LO6 |
|------|-----|-----|-----|-----|-----|-----|
| `README.md` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `docs/theory_summary.md` | ✅ | ✅ | ✅ | ✅ | | |
| `docs/misconceptions.md` | ✅ | ✅ | ✅ | ✅ | | ✅ |
| `docs/peer_instruction.md` | ✅ | ✅ | ✅ | | | ✅ |
| `docs/code_tracing.md` | ✅ | ✅ | ✅ | ✅ | ✅ | |
| `docs/parsons_problems.md` | | | ✅ | | ✅ | |
| `docs/troubleshooting.md` | | | ✅ | | ✅ | ✅ |
| `formative/quiz_week14.yaml` | ✅ | ✅ | ✅ | ✅ | | ✅ |
| `src/exercises/ex_14_01_*.py` | ✅ | | | | | |
| `src/exercises/ex_14_02_*.py` | | ✅ | | | ✅ | |
| `src/exercises/ex_14_03_*.py` | | | | ✅ | | ✅ |
| `homework/exercises/hw_14_01_*.py` | | | ✅ | | ✅ | |
| `homework/exercises/hw_14_02_*.py` | | ✅ | | | | ✅ |
| `homework/exercises/hw_14_03_*.py` | ✅ | | | ✅ | | |
| `tests/smoke_test.py` | | ✅ | ✅ | | ✅ | |
| `tests/test_exercises.py` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## Quick Reference Commands

```bash
# Run formative quiz
make quiz

# Verify all LOs coverage
make validate

# Run smoke tests (LO3, LO5)
make smoke

# Start lab environment (LO3)
make docker-up

# Capture traffic (LO4)
make capture

# View LB distribution (LO2, LO6)
for i in {1..10}; do curl -s localhost:8080/ | grep app; done
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-24 | Initial LO traceability matrix |

---

*NETWORKING class — ASE, CSIE | Computer Networks Laboratory*  
*Learning Objectives v1.0.0 | Week 14: Integrated Recap*
