# 🎯 Learning Objectives — Week 11
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> This document provides explicit traceability between Learning Objectives and all course artifacts.

---

## Quick Navigation

| LO | Topic | Theory | Lab | Test | Quiz | Misconception |
|----|-------|--------|-----|------|------|---------------|
| [LO1](#lo1) | Protocol Architecture | [§1-3](#theory) | [Ex1,6](#labs) | [T1,T6](#tests) | [Q1-Q3](#quiz) | [M2-M4](#misc) |
| [LO2](#lo2) | FTP/DNS/SSH Mechanics | [§1-3](#theory) | [Ex6](#labs) | [T6](#tests) | [Q2,Q3,Q5](#quiz) | [M2,M3,M4](#misc) |
| [LO3](#lo3) | Load Balancer Implementation | [§4](#theory) | [Ex2,3](#labs) | [T2,T3](#tests) | [Q1,Q4](#quiz) | [M1](#misc) |
| [LO4](#lo4) | Nginx Configuration | [§5](#theory) | [Ex5](#labs) | [T5](#tests) | [Q1](#quiz) | [M5](#misc) |
| [LO5](#lo5) | Traffic Analysis | [README](#readme) | [Ex5,7](#labs) | [—](#tests) | [—](#quiz) | [—](#misc) |
| [LO6](#lo6) | Container Architecture | [§5](#theory) | [Ex5](#labs) | [T5](#tests) | [—](#quiz) | [—](#misc) |
| [LO7](#lo7) | Performance Evaluation | [§4.1](#theory) | [Ex7](#labs) | [T7](#tests) | [—](#quiz) | [M1.1](#misc) |

---

## Learning Objectives (Bloom Taxonomy)

<a name="lo1"></a>
### LO1: Identify Protocol Components (Remember/Understand)

**Statement:** Identify the architectural components of FTP, DNS and SSH protocols, including their port assignments, message formats and operational modes.

| Artifact Type | Location | Specific Section |
|---------------|----------|------------------|
| **Theory** | `docs/theory_summary.md` | §1 FTP, §2 DNS, §3 SSH |
| **Lab Exercise** | `src/exercises/ex_11_03_dns_client.py` | DNS query construction |
| **Lab Exercise** | `README.md` | Exercise 6: DNS Protocol Analysis |
| **Test** | `tests/test_exercises.py` | `TestExercise6DNS` |
| **Quiz** | `docs/peer_instruction.md` | Q2 (DNS), Q3 (FTP), Q5 (SSH) |
| **Quiz** | `formative/quiz.yaml` | q1-q5 |
| **Misconception** | `docs/misconceptions.md` | §2.2 (DNS ports), §3.2 (FTP connections) |
| **Glossary** | `docs/glossary.md` | FTP, DNS, SSH entries |
| **Code Tracing** | `docs/code_tracing.md` | T2 (DNS encoding) |

**Assessment Criteria:**
- [ ] Can list FTP ports (21 control, 20 data)
- [ ] Can explain DNS record types (A, AAAA, MX, NS, CNAME)
- [ ] Can identify SSH protocol layers (transport, auth, connection)

---

<a name="lo2"></a>
### LO2: Explain Protocol Differences (Understand)

**Statement:** Explain the differences between FTP active and passive modes, the DNS resolution hierarchy and SSH key exchange mechanisms.

| Artifact Type | Location | Specific Section |
|---------------|----------|------------------|
| **Theory** | `docs/theory_summary.md` | §1.2 Active vs Passive, §2.2 Resolution |
| **Lab Exercise** | `src/exercises/ex_11_03_dns_client.py` | Recursive vs iterative |
| **Quiz** | `docs/peer_instruction.md` | Q2, Q3, Q5 |
| **Misconception** | `docs/misconceptions.md` | §2.1 (TTL), §3.1 (passive mode) |
| **Analogy** | `docs/concept_analogies.md` | FTP restaurant analogy |

**Assessment Criteria:**
- [ ] Can explain why passive mode works through NAT
- [ ] Can trace DNS resolution path for a domain
- [ ] Can describe Diffie-Hellman key exchange purpose

---

<a name="lo3"></a>
### LO3: Implement Load Balancer (Apply)

**Statement:** Implement a functional Python load balancer supporting multiple distribution algorithms and passive health checking.

| Artifact Type | Location | Specific Section |
|---------------|----------|------------------|
| **Theory** | `docs/theory_summary.md` | §4 Load Balancing Theory |
| **Lab Exercise** | `src/exercises/ex_11_02_loadbalancer.py` | Complete implementation |
| **Lab Exercise** | `README.md` | Exercise 2, 3, 4 |
| **Test** | `tests/test_exercises.py` | `TestExercise2RoundRobin`, `TestExercise3IPHash` |
| **Quiz** | `docs/peer_instruction.md` | Q1, Q4 |
| **Misconception** | `docs/misconceptions.md` | §1.1-1.5 |
| **Code Tracing** | `docs/code_tracing.md` | T1 (round-robin), T3 (health check), T4 (IP hash) |
| **Homework** | `homework/README.md` | HW 11.01 |

**Assessment Criteria:**
- [ ] Can implement round-robin algorithm
- [ ] Can implement IP hash for sticky sessions
- [ ] Can implement passive health checking with fail_timeout

---

<a name="lo4"></a>
### LO4: Demonstrate Nginx Configuration (Apply)

**Statement:** Demonstrate Nginx reverse proxy configuration with upstream pools, weighted backends and automatic failover.

| Artifact Type | Location | Specific Section |
|---------------|----------|------------------|
| **Theory** | `docs/theory_summary.md` | §5 Nginx Reverse Proxy |
| **Lab Exercise** | `docker/configs/nginx.conf` | Upstream configuration |
| **Lab Exercise** | `README.md` | Exercise 5 |
| **Test** | `tests/test_exercises.py` | `TestExercise5NginxDocker` |
| **Quiz** | `docs/peer_instruction.md` | Q1 |
| **Misconception** | `docs/misconceptions.md` | §5.1, §5.2 |
| **Cheatsheet** | `docs/commands_cheatsheet.md` | Nginx commands |

**Assessment Criteria:**
- [ ] Can configure upstream block with weights
- [ ] Can set proxy headers (X-Real-IP, X-Forwarded-For)
- [ ] Can configure failover with proxy_next_upstream

---

<a name="lo5"></a>
### LO5: Analyse Network Traffic (Analyze)

**Statement:** Analyse network traffic patterns using packet capture tools to verify load distribution and protocol behaviour.

| Artifact Type | Location | Specific Section |
|---------------|----------|------------------|
| **Theory** | `README.md` | §Wireshark Setup and Usage |
| **Lab Exercise** | `scripts/capture_traffic.py` | Capture automation |
| **Lab Exercise** | `README.md` | §Packet Capture and Analysis |
| **PCAP Storage** | `pcap/` | Output directory |
| **Filters** | `README.md` | Wireshark filter table |

**Assessment Criteria:**
- [ ] Can capture traffic on correct interface (vEthernet WSL)
- [ ] Can apply display filters for HTTP, DNS, FTP
- [ ] Can identify load balancer distribution from captures

---

<a name="lo6"></a>
### LO6: Design Container Architecture (Create)

**Statement:** Design containerised multi-tier architectures using Docker Compose with proper networking isolation and service dependencies.

| Artifact Type | Location | Specific Section |
|---------------|----------|------------------|
| **Theory** | `docs/theory_summary.md` | §5 (Nginx architecture) |
| **Lab Exercise** | `docker/docker-compose.yml` | Complete stack |
| **Lab Exercise** | `README.md` | Exercise 5 |
| **Test** | `tests/test_exercises.py` | `TestExercise5NginxDocker` |
| **Troubleshooting** | `docs/troubleshooting.md` | §1 Docker issues |

**Assessment Criteria:**
- [ ] Can define multi-service docker-compose.yml
- [ ] Can configure custom networks with IPAM
- [ ] Can set service dependencies and health checks

---

<a name="lo7"></a>
### LO7: Evaluate Performance (Evaluate)

**Statement:** Evaluate the performance characteristics of different load balancing algorithms through systematic benchmarking.

| Artifact Type | Location | Specific Section |
|---------------|----------|------------------|
| **Theory** | `docs/theory_summary.md` | §4.1 Distribution Algorithms |
| **Lab Exercise** | `src/exercises/ex_11_02_loadbalancer.py` | loadgen subcommand |
| **Lab Exercise** | `README.md` | Exercise 7 |
| **Test** | `tests/test_exercises.py` | `TestExercise7Benchmark` |
| **Misconception** | `docs/misconceptions.md` | §1.1 (distribution expectations) |

**Assessment Criteria:**
- [ ] Can run benchmark with configurable concurrency
- [ ] Can interpret requests/second and latency percentiles
- [ ] Can compare Python LB vs Nginx performance

---

## Cross-Reference Tables

<a name="theory"></a>
### Theory Coverage by Section

| Section | Topics | LOs Covered |
|---------|--------|-------------|
| §1 FTP | Dual-connection, Active/Passive, Security | LO1, LO2 |
| §2 DNS | Hierarchy, Resolution, Record Types, DNSSEC | LO1, LO2 |
| §3 SSH | Layering, Authentication, Port Forwarding | LO1, LO2 |
| §4 Load Balancing | Algorithms, Health Checks, L4 vs L7 | LO3, LO7 |
| §5 Nginx | Upstream, Headers, Failover | LO4, LO6 |

<a name="labs"></a>
### Lab Exercise Mapping

| Exercise | File/Section | LOs Covered | Duration |
|----------|--------------|-------------|----------|
| Ex1 | `ex_11_01_backend.py` | LO3 | 10 min |
| Ex2 | `ex_11_02_loadbalancer.py` (rr) | LO3 | 20 min |
| Ex3 | `ex_11_02_loadbalancer.py` (ip_hash) | LO3 | 15 min |
| Ex4 | Failover simulation | LO3, LO4 | 15 min |
| Ex5 | Docker Nginx stack | LO4, LO5, LO6 | 20 min |
| Ex6 | `ex_11_03_dns_client.py` | LO1, LO2 | 20 min |
| Ex7 | Benchmarking | LO7 | 15 min |

<a name="tests"></a>
### Test Coverage Mapping

| Test Class | File | LOs Validated |
|------------|------|---------------|
| `TestExercise1Backend` | `test_exercises.py` | LO3 |
| `TestExercise2RoundRobin` | `test_exercises.py` | LO3 |
| `TestExercise3IPHash` | `test_exercises.py` | LO3 |
| `TestExercise4Failover` | `test_exercises.py` | LO3, LO4 |
| `TestExercise5NginxDocker` | `test_exercises.py` | LO4, LO6 |
| `TestExercise6DNS` | `test_exercises.py` | LO1, LO2 |
| `TestExercise7Benchmark` | `test_exercises.py` | LO7 |

<a name="quiz"></a>
### Quiz Question Mapping

| Question | File | LOs Assessed | Misconception Targeted |
|----------|------|--------------|----------------------|
| Q1 | `peer_instruction.md` | LO3, LO4 | Instant failure detection |
| Q2 | `peer_instruction.md` | LO1, LO2 | TTL guarantees |
| Q3 | `peer_instruction.md` | LO1, LO2 | FTP single connection |
| Q4 | `peer_instruction.md` | LO3 | IP hash persistence |
| Q5 | `peer_instruction.md` | LO1, LO2 | SSH end-to-end encryption |

<a name="misc"></a>
### Misconception Coverage

| ID | Section | Topic | LOs Related |
|----|---------|-------|-------------|
| M1.1-1.5 | §1 | Load Balancing | LO3, LO7 |
| M2.1-2.3 | §2 | DNS | LO1, LO2 |
| M3.1-3.2 | §3 | FTP | LO1, LO2 |
| M4.1-4.2 | §4 | SSH | LO1, LO2 |
| M5.1-5.2 | §5 | Nginx | LO4 |

---

## Self-Assessment Checklist

Before completing Week 11, verify you can:

### Foundational (LO1, LO2)
- [ ] Draw the FTP dual-connection architecture
- [ ] Explain why passive mode works through NAT
- [ ] Trace a DNS query through the hierarchy
- [ ] List SSH protocol layers and their purposes

### Applied (LO3, LO4)
- [ ] Implement round-robin in Python (see `code_tracing.md` T1)
- [ ] Configure Nginx upstream with weights
- [ ] Set up passive health checking

### Analytical (LO5, LO7)
- [ ] Capture and filter HTTP traffic in Wireshark
- [ ] Interpret benchmark results (RPS, latency)
- [ ] Compare algorithm performance characteristics

### Creative (LO6)
- [ ] Design a multi-tier Docker Compose stack
- [ ] Configure service dependencies and networks

---

*NETWORKING class - ASE, Informatics | Computer Networks Laboratory*
*Week 11: Application Protocols — FTP, DNS, SSH and Load Balancing*
