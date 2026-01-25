# Learning Objectives Traceability Matrix — Week 1

> Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

This matrix maps each Learning Objective (LO) to its coverage across all course artefacts.

---

## Learning Objectives Summary

| ID | Learning Objective | Bloom Level | Verb |
|----|-------------------|-------------|------|
| LO1 | Measure and interpret network latency using ICMP ping | Apply | Demonstrate, Measure |
| LO2 | Implement basic TCP socket communication | Apply | Implement, Create |
| LO3 | Parse and process network data from various formats | Apply | Parse, Extract |
| LO4 | Capture and analyse network traffic using standard tools | Analyse | Analyse, Interpret |
| LO5 | Calculate transmission delays for different network scenarios | Apply | Calculate, Compute |
| LO6 | Configure and manage Docker containers for network labs | Apply | Configure, Manage |
| LO7 | Use Wireshark to capture and filter network traffic | Apply | Capture, Filter |

---

## Full Traceability Matrix

| LO | Theory | Exercise | Homework | Quiz | PCAP | Parsons | Peer Instr. | Misconceptions |
|----|--------|----------|----------|------|------|---------|-------------|----------------|
| LO1 | theory_summary.md §1,2 | ex_1_01_ping_latency.py | — | q01, q06, q11 | demo_icmp_ping.pcap | P1, P2, P5 | Q1, Q3 | M1, M2, M3 |
| LO2 | theory_summary.md §3 | ex_1_02_tcp_server_client.py | — | q03, q07, q08, q12, q14 | demo_tcp_handshake.pcap | — | Q2, Q5 | M11 |
| LO3 | commands_cheatsheet.md | ex_1_03_parse_csv.py | hw_1_02_pcap_analyser.py | q16, q17 | — | P4 | — | — |
| LO4 | README.md §Wireshark | ex_1_04_pcap_stats.py | hw_1_02_pcap_analyser.py | q15, q22 | All demos | P3 | — | — |
| LO5 | theory_summary.md §4 | ex_1_05_transmission_delay.py | — | q18, q19 | — | — | — | M1 |
| LO6 | glossary.md, README.md | (via all exercises) | — | q02, q04, q05, q09, q10, q13 | — | — | Q4 | M7, M8, M9, M10 |
| LO7 | README.md §Wireshark | scripts/capture_traffic.py | — | q15, q20, q21 | All demos | — | — | — |

---

## Coverage by Artefact Type

### Exercises (src/exercises/)

| File | LOs Covered | Primary Focus |
|------|-------------|---------------|
| ex_1_01_ping_latency.py | LO1 | ICMP ping, RTT measurement |
| ex_1_02_tcp_server_client.py | LO2 | TCP sockets, client-server |
| ex_1_03_parse_csv.py | LO3 | CSV parsing, data extraction |
| ex_1_04_pcap_stats.py | LO4 | PCAP analysis with scapy/dpkt |
| ex_1_05_transmission_delay.py | LO5 | Delay calculations |

### Quiz Questions Coverage

```
LO1: ███░░░░░░░░░ (3 questions: q01, q06, q11)
LO2: █████░░░░░░░ (5 questions: q03, q07, q08, q12, q14)
LO3: ██░░░░░░░░░░ (2 questions: q16, q17)
LO4: ██░░░░░░░░░░ (2 questions: q15, q22)
LO5: ██░░░░░░░░░░ (2 questions: q18, q19)
LO6: ██████░░░░░░ (6 questions: q02, q04, q05, q09, q10, q13)
LO7: ███░░░░░░░░░ (3 questions: q15, q20, q21)
```

### Parsons Problems Coverage

| Problem | LO | Topic |
|---------|-----|-------|
| P1 | LO1 | Ping RTT extraction |
| P2 | LO1 | Interface discovery |
| P3 | LO4 | Socket listing with ss |
| P4 | LO3 | Traceroute hop extraction |
| P5 | LO1 | Loopback routing check |

### Peer Instruction Questions Coverage

| Question | LO | Misconception Targeted |
|----------|-----|------------------------|
| Q1 | LO1 | Latency vs bandwidth confusion |
| Q2 | LO2 | TCP handshake packet count |
| Q3 | LO1 | localhost vs 127.0.0.1 |
| Q4 | LO6 | Container network namespace |
| Q5 | LO2 | Socket LISTEN state |

---

## Gap Analysis

### Well-Covered (≥3 artefacts)
- ✅ LO1: 8 artefacts (theory, exercise, quiz×3, pcap, parsons×3, peer×2)
- ✅ LO2: 7 artefacts (theory, exercise, quiz×5, pcap, peer×2)
- ✅ LO6: 6 artefacts (glossary, readme, quiz×6, peer×1)

### Adequately Covered (2 artefacts)
- 📗 LO3: 4 artefacts (cheatsheet, exercise, homework, quiz×2, parsons)
- 📗 LO4: 4 artefacts (readme, exercise, homework, quiz×2, parsons)
- 📗 LO5: 3 artefacts (theory, exercise, quiz×2)
- 📗 LO7: 4 artefacts (readme, script, quiz×3)

### Recommendations
- All LOs now have minimum coverage
- Consider adding LO5 Parsons problem for Week 2

---

## Self-Assessment Checklist

Use this checklist to verify your understanding before the exam.

### LO1: Latency Measurement
- [ ] I can run `ping -c 4 8.8.8.8` and explain the RTT values
- [ ] I can explain why loopback ping shows <1ms latency
- [ ] I understand the difference between latency and bandwidth
- [ ] I know that traceroute shows one possible path, not the only path

### LO2: TCP Communication
- [ ] I can explain SYN → SYN-ACK → ACK handshake
- [ ] I can write a TCP server that listens on a port
- [ ] I can write a TCP client that connects and sends data
- [ ] I understand LISTEN vs ESTABLISHED socket states

### LO3: Data Parsing
- [ ] I can read a CSV file using Python's csv module
- [ ] I can extract specific fields from structured data
- [ ] I know when to use regex vs structured parsing

### LO4: Traffic Capture
- [ ] I can capture packets using tcpdump or tshark
- [ ] I can read PCAP files with scapy or dpkt
- [ ] I can count packets by protocol type

### LO5: Transmission Delay
- [ ] I can calculate transmission delay: size/bandwidth
- [ ] I can calculate propagation delay: distance/speed
- [ ] I understand the difference between the two

### LO6: Docker Containers
- [ ] I can start/stop containers with docker compose
- [ ] I can view container logs with docker logs
- [ ] I can access Portainer at localhost:9000
- [ ] I understand images vs containers

### LO7: Wireshark
- [ ] I can select the correct interface (vEthernet WSL)
- [ ] I can write display filters (tcp.port == 9090)
- [ ] I can follow a TCP stream
- [ ] I can identify the three-way handshake in captures

---

*NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim*
*Updated: January 2026*
