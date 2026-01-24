# 🎯 Learning Objectives Matrix — Week 1
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> This document provides centralized traceability between Learning Objectives (LOs) 
> and all related educational artifacts for Week 1: Network Fundamentals.

---

## Quick Reference

| ID | Learning Objective | Bloom Level |
|----|-------------------|-------------|
| LO1 | Measure and interpret network latency using ICMP ping | Apply |
| LO2 | Implement basic TCP socket communication | Apply |
| LO3 | Parse and process network data from various formats | Apply |
| LO4 | Capture and analyse network traffic using standard tools | Analyse |
| LO5 | Calculate transmission delays for different network scenarios | Apply |
| LO6 | Configure and manage Docker containers for network labs | Apply |
| LO7 | Use Wireshark to capture and filter network traffic | Apply |

---

## Full Traceability Matrix

### Artifact Links per LO

| LO | Theory | Lab Exercise | Test | Quiz Questions | PCAP | Misconception | Parsons |
|----|--------|--------------|------|----------------|------|---------------|---------|
| **LO1** | [theory_summary.md](theory_summary.md#transport-protocols) | [ex_1_01_ping_latency.py](../src/exercises/ex_1_01_ping_latency.py) | [test_exercise_2](../tests/test_exercises.py) | q01, q06, q11 | ✓ | [#1](misconceptions.md#misconception-1) | — |
| **LO2** | [theory_summary.md](theory_summary.md#tcp-transmission-control-protocol) | [ex_1_02_tcp_server_client.py](../src/exercises/ex_1_02_tcp_server_client.py) | [test_exercise_3](../tests/test_exercises.py) | q03, q07, q08, q12, q14 | ✓ | [#5, #6, #11](misconceptions.md) | P1, P3 |
| **LO3** | [commands_cheatsheet.md](commands_cheatsheet.md) | [ex_1_03_parse_csv.py](../src/exercises/ex_1_03_parse_csv.py) | [test_exercise_5](../tests/test_exercises.py) | — | — | — | P2 |
| **LO4** | [README.md](../README.md#wireshark-setup-and-usage) | [ex_1_04_pcap_stats.py](../src/exercises/ex_1_04_pcap_stats.py) | [test_exercise_4](../tests/test_exercises.py) | q15 | ✓ | [#10](misconceptions.md#misconception-10) | — |
| **LO5** | [theory_summary.md](theory_summary.md) | [ex_1_05_transmission_delay.py](../src/exercises/ex_1_05_transmission_delay.py) | partial | — | — | [#1](misconceptions.md#misconception-1) | — |
| **LO6** | [glossary.md](glossary.md#docker-terms) | [README.md](../README.md) | [smoke_test.py](../tests/smoke_test.py) | q02, q04, q05, q07, q13 | — | [#7, #8](misconceptions.md) | P3 |
| **LO7** | [README.md](../README.md#wireshark-setup-and-usage) | [capture_traffic.py](../scripts/capture_traffic.py) | — | q15 | ✓ | [#10](misconceptions.md#misconception-10) | — |

**Legend:**
- ✓ = Fully covered with examples
- partial = Exists but needs expansion
- — = Not applicable for this LO

---

## Detailed LO Specifications

### LO1: Network Latency Measurement

**Full Statement:**  
Students will be able to measure and interpret network latency using ICMP ping, 
correctly distinguishing between latency (time) and bandwidth (throughput) metrics.

**Bloom Taxonomy Level:** Apply (Level 3)

**Action Verbs:** Measure, Interpret, Distinguish, Execute, Demonstrate

**Assessment Criteria:**
1. Execute `ping` command with correct parameters (`-c` for count)
2. Interpret RTT (Round-Trip Time) values correctly
3. Explain why loopback ping shows <1ms latency
4. Distinguish latency from bandwidth in practical scenarios
5. Predict RTT ranges for local vs. remote hosts

**Linked Artifacts:**

| Type | Path | Relevant Section |
|------|------|------------------|
| Theory | `docs/theory_summary.md` | "Transport Protocols", "Latency vs Bandwidth" |
| Exercise | `src/exercises/ex_1_01_ping_latency.py` | Entire file — prediction + execution + interpretation |
| Test | `tests/test_exercises.py` | `test_exercise_2()` |
| Quiz | `formative/quiz.yaml` | Questions q01, q06, q11 |
| Misconception | `docs/misconceptions.md` | #1: "Ping measures bandwidth" |
| Code Tracing | `docs/code_tracing.md` | Exercise T2 |

**Pre-requisite Knowledge:**
- Basic command line usage
- Understanding of IP addresses

---

### LO2: TCP Socket Communication

**Full Statement:**  
Students will implement basic TCP client-server communication using Python sockets, 
demonstrating understanding of the three-way handshake and connection states.

**Bloom Taxonomy Level:** Apply (Level 3)

**Action Verbs:** Implement, Demonstrate, Create, Execute, Identify

**Assessment Criteria:**
1. Create TCP socket with correct parameters (`AF_INET`, `SOCK_STREAM`)
2. Implement server pattern: `bind()` → `listen()` → `accept()`
3. Implement client pattern: `connect()` → `send()` → `recv()`
4. Identify handshake packets (SYN → SYN-ACK → ACK) in Wireshark
5. Explain socket states (LISTEN, ESTABLISHED, TIME_WAIT)

**Linked Artifacts:**

| Type | Path | Relevant Section |
|------|------|------------------|
| Theory | `docs/theory_summary.md` | "TCP (Transmission Control Protocol)", "Three-Way Handshake" |
| Exercise | `src/exercises/ex_1_02_tcp_server_client.py` | Entire file with server/client implementation |
| Test | `tests/test_exercises.py` | `test_exercise_3()` |
| Quiz | `formative/quiz.yaml` | Questions q03, q07, q08, q12, q14 |
| Misconceptions | `docs/misconceptions.md` | #5: "TCP guarantees instant delivery", #6: "UDP is useless", #11: "LISTEN means communicating" |
| Parsons | `docs/parsons_problems.md` | Problems P1 (TCP Port Checker), P3 (Docker Container Status) |
| Peer Instruction | `docs/peer_instruction.md` | Question 2: TCP Three-Way Handshake |

**Pre-requisite Knowledge:**
- Basic Python programming
- Understanding of ports and IP addresses
- Concept of client-server architecture

---

### LO3: Network Data Parsing

**Full Statement:**  
Students will parse and process network data from various formats (CSV, structured output), 
extracting relevant information for analysis.

**Bloom Taxonomy Level:** Apply (Level 3)

**Action Verbs:** Parse, Process, Extract, Transform, Validate

**Assessment Criteria:**
1. Read and parse CSV files with network data
2. Extract specific fields (IP, port, protocol)
3. Handle malformed data gracefully
4. Transform data for further analysis

**Linked Artifacts:**

| Type | Path | Relevant Section |
|------|------|------------------|
| Theory | `docs/commands_cheatsheet.md` | Data format examples |
| Exercise | `src/exercises/ex_1_03_parse_csv.py` | CSV parsing implementation |
| Test | `tests/test_exercises.py` | `test_exercise_5()` |
| Parsons | `docs/parsons_problems.md` | Problem P2 (Ping Output Parser) |

**Pre-requisite Knowledge:**
- Python file I/O
- Basic understanding of CSV format

---

### LO4: Network Traffic Capture and Analysis

**Full Statement:**  
Students will capture network traffic using standard tools (tcpdump, Wireshark) 
and analyse the captured data to understand protocol behaviour.

**Bloom Taxonomy Level:** Analyse (Level 4)

**Action Verbs:** Capture, Analyse, Filter, Identify, Compare

**Assessment Criteria:**
1. Start packet capture on correct interface
2. Apply display filters in Wireshark
3. Identify protocol headers and fields
4. Follow TCP streams to see conversation
5. Export captures in PCAP format

**Linked Artifacts:**

| Type | Path | Relevant Section |
|------|------|------------------|
| Theory | `../README.md` | "Wireshark Setup and Usage" (500+ lines) |
| Exercise | `src/exercises/ex_1_04_pcap_stats.py` | PCAP analysis implementation |
| Script | `scripts/capture_traffic.py` | Automated capture |
| Test | `tests/test_exercises.py` | `test_exercise_4()` |
| Quiz | `formative/quiz.yaml` | Question q15 |
| Misconception | `docs/misconceptions.md` | #10: "Wireshark captures all traffic" |
| PCAP Guide | `pcap/README.md` | Capture instructions |

**Pre-requisite Knowledge:**
- Understanding of network protocols
- Basic Wireshark installation

---

### LO5: Transmission Delay Calculation

**Full Statement:**  
Students will calculate transmission delays for different network scenarios, 
understanding the relationship between packet size, bandwidth, and propagation delay.

**Bloom Taxonomy Level:** Apply (Level 3)

**Action Verbs:** Calculate, Apply, Predict, Compare

**Assessment Criteria:**
1. Calculate transmission delay: `delay = packet_size / bandwidth`
2. Understand propagation delay vs transmission delay
3. Apply formulas to realistic scenarios
4. Predict total end-to-end delay

**Linked Artifacts:**

| Type | Path | Relevant Section |
|------|------|------------------|
| Theory | `docs/theory_summary.md` | Latency components |
| Exercise | `src/exercises/ex_1_05_transmission_delay.py` | Delay calculation implementation |
| Test | `tests/test_exercises.py` | Partial coverage |
| Misconception | `docs/misconceptions.md` | #1: Relates to understanding delay types |

**Pre-requisite Knowledge:**
- Basic arithmetic
- Understanding of units (bits, bytes, seconds)

---

### LO6: Docker Container Management

**Full Statement:**  
Students will configure and manage Docker containers for network laboratory exercises, 
understanding the relationship between images, containers, and networks.

**Bloom Taxonomy Level:** Apply (Level 3)

**Action Verbs:** Configure, Start, Stop, Inspect, Connect

**Assessment Criteria:**
1. Start/stop containers with `docker compose`
2. Check container status with `docker ps`
3. Execute commands inside containers with `docker exec`
4. Understand port mapping (`-p host:container`)
5. Distinguish between images and containers

**Linked Artifacts:**

| Type | Path | Relevant Section |
|------|------|------------------|
| Theory | `docs/glossary.md` | "Docker Terms" section |
| Guide | `../README.md` | "Initial Environment Setup", "Understanding Portainer Interface" |
| Test | `tests/smoke_test.py` | Docker verification |
| Quiz | `formative/quiz.yaml` | Questions q02, q04, q05, q07, q13 |
| Misconceptions | `docs/misconceptions.md` | #7: "Container localhost = Host localhost", #8: "docker ps shows all" |
| Parsons | `docs/parsons_problems.md` | Problem P3 (Docker Container Status Check) |
| Troubleshooting | `docs/troubleshooting.md` | Docker Issues section |

**Pre-requisite Knowledge:**
- Basic command line usage
- Understanding of virtualisation concept

---

### LO7: Wireshark Traffic Filtering

**Full Statement:**  
Students will use Wireshark to capture network traffic and apply filters 
to isolate specific protocols and conversations.

**Bloom Taxonomy Level:** Apply (Level 3)

**Action Verbs:** Capture, Filter, Select, Follow, Export

**Assessment Criteria:**
1. Select correct capture interface (vEthernet WSL for Docker traffic)
2. Apply display filters (`tcp.port`, `ip.addr`, protocol names)
3. Follow TCP streams
4. Identify colour coding meaning
5. Save captures for later analysis

**Linked Artifacts:**

| Type | Path | Relevant Section |
|------|------|------------------|
| Guide | `../README.md` | "Wireshark Setup and Usage" — comprehensive 200+ line guide |
| Script | `scripts/capture_traffic.py` | Programmatic capture |
| Quiz | `formative/quiz.yaml` | Question q15 |
| Misconception | `docs/misconceptions.md` | #10: "Wireshark captures all traffic" |
| Filters | `../README.md` | "Key Wireshark Filters" table |

**Pre-requisite Knowledge:**
- Wireshark installed on Windows
- Understanding of network protocols

---

## Self-Assessment Checklist

Before completing the laboratory, verify you can do ALL of the following:

### LO1: Latency Measurement
- [ ] Run `ping -c 4 8.8.8.8` and explain what RTT means
- [ ] Explain why loopback ping shows <1ms latency
- [ ] Distinguish between latency and bandwidth with an example

### LO2: TCP Communication
- [ ] Explain the three packets in SYN → SYN-ACK → ACK
- [ ] Write a simple TCP server that listens on a port
- [ ] Identify LISTEN vs ESTABLISHED socket states

### LO3: Data Parsing
- [ ] Parse a CSV file containing network data
- [ ] Extract IP addresses using string operations or regex

### LO4: Traffic Capture
- [ ] Capture traffic with `tcpdump -i eth0 -w capture.pcap`
- [ ] Open capture in Wireshark and apply a filter

### LO5: Delay Calculation
- [ ] Calculate transmission delay for a 1500-byte packet on 100 Mbps link
- [ ] Explain the difference between transmission and propagation delay

### LO6: Docker Management
- [ ] Start the lab with `docker compose up -d`
- [ ] Check running containers with `docker ps`
- [ ] Explain why `docker ps -a` shows more containers

### LO7: Wireshark Filtering
- [ ] Apply filter `tcp.port == 9090` in Wireshark
- [ ] Follow a TCP stream to see the conversation
- [ ] Identify which interface to capture for Docker traffic

---

## Cross-References

### Quiz Coverage by LO

```
LO1: ████████░░ (3 questions: q01, q06, q11)
LO2: ██████████ (5 questions: q03, q07, q08, q12, q14)
LO3: ░░░░░░░░░░ (0 questions — covered in exercises)
LO4: ██░░░░░░░░ (1 question: q15)
LO5: ░░░░░░░░░░ (0 questions — covered in exercises)
LO6: ██████████ (5 questions: q02, q04, q05, q07, q13)
LO7: ██░░░░░░░░ (1 question: q15, shared with LO4)
```

### Misconception Coverage by LO

| LO | Misconceptions Addressed |
|----|-------------------------|
| LO1 | #1 (Ping measures bandwidth) |
| LO2 | #5 (TCP instant delivery), #6 (UDP useless), #11 (LISTEN = communicating) |
| LO4 | #10 (Wireshark captures all) |
| LO5 | #1 (related) |
| LO6 | #7 (Container localhost), #8 (docker ps shows all) |
| LO7 | #10 (Wireshark captures all) |

---

*NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim*  
*Week 1: Network Fundamentals — Learning Objectives Traceability*
