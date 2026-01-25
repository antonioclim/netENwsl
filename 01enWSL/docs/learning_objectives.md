# Learning Objectives Matrix — Week 1

> Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

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

## Traceability Matrix

| LO | Theory | Lab Exercise | Quiz | PCAP | Parsons |
|----|--------|--------------|------|------|---------|
| LO1 | theory_summary.md | ex_1_01_ping_latency.py | q01,q06,q11 | demo_icmp_ping.pcap | P1 |
| LO2 | theory_summary.md | ex_1_02_tcp_server_client.py | q03,q07,q08,q12,q14 | demo_tcp_handshake.pcap | P2,P4 |
| LO3 | commands_cheatsheet.md | ex_1_03_parse_csv.py | q16,q17 | — | P3 |
| LO4 | README.md | ex_1_04_pcap_stats.py | q15,q22 | All demos | — |
| LO5 | theory_summary.md | ex_1_05_transmission_delay.py | q18,q19 | — | — |
| LO6 | glossary.md | README.md | q02,q04,q05,q09,q10,q13 | — | P5 |
| LO7 | README.md | scripts/capture_traffic.py | q15,q20,q21 | All demos | — |

## Quiz Coverage

```
LO1: ███░░░░░░░░░ (3 questions)
LO2: █████░░░░░░░ (5 questions)
LO3: ██░░░░░░░░░░ (2 questions)
LO4: ██░░░░░░░░░░ (2 questions)
LO5: ██░░░░░░░░░░ (2 questions)
LO6: ██████░░░░░░ (6 questions)
LO7: ███░░░░░░░░░ (3 questions)
```

## Self-Assessment Checklist

### LO1: Latency Measurement
- [ ] Run `ping -c 4 8.8.8.8` and explain RTT
- [ ] Explain why loopback ping shows <1ms latency
- [ ] Distinguish between latency and bandwidth

### LO2: TCP Communication
- [ ] Explain SYN → SYN-ACK → ACK handshake
- [ ] Write a TCP server that listens on a port
- [ ] Identify LISTEN vs ESTABLISHED states

### LO3: Data Parsing
- [ ] Parse a CSV file containing network data
- [ ] Extract IP addresses using regex

### LO4: Traffic Capture
- [ ] Capture traffic with tcpdump
- [ ] Apply Wireshark display filters

### LO5: Delay Calculation
- [ ] Calculate transmission delay for 1500-byte packet on 100 Mbps
- [ ] Explain transmission vs propagation delay

### LO6: Docker Management
- [ ] Start lab with `docker compose up -d`
- [ ] Explain `docker ps` vs `docker ps -a`

### LO7: Wireshark Filtering
- [ ] Apply filter `tcp.port == 9090`
- [ ] Select correct interface for Docker traffic

---
*NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim*


---

## Traceability

A formal LO-to-activity traceability matrix is available in `docs/lo_traceability_matrix.md`.
