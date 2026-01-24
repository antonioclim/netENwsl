# 📝 Homework — Week 6: NAT, ARP and Supporting Protocols

> Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

## Overview

This week's homework focuses on understanding NAT translation tables and ARP cache analysis, with emphasis on troubleshooting and security considerations.

## Assignments

| File | Topic | Difficulty | Est. Time |
|------|-------|------------|-----------|
| `hw_6_01_nat_analysis.py` | NAT Translation Table Analysis | ⭐⭐ Intermediate | 45-60 min |
| `hw_6_02_arp_investigation.py` | ARP Cache Investigation and Anomaly Detection | ⭐⭐⭐ Advanced | 60-75 min |

## Assignment Details

### hw_6_01_nat_analysis.py

Analyse NAT translation tables (conntrack) and port forwarding rules.

**Learning Objectives:**
- Parse and interpret conntrack entries
- Understand PAT port allocation
- Trace packet flow through NAT
- Analyse port forwarding configurations

**Key Skills:**
- Connection tracking analysis
- NAT troubleshooting
- Port forwarding configuration

### hw_6_02_arp_investigation.py

Investigate ARP cache entries and detect potential security anomalies.

**Learning Objectives:**
- Analyse ARP cache lifecycle states
- Detect duplicate MAC addresses (MITM indicators)
- Identify gateway spoofing attempts
- Implement basic anomaly detection logic

**Key Skills:**
- ARP protocol understanding
- Security monitoring
- Anomaly detection algorithms

**⚠️ Ethical Note:** The ARP analysis exercise is for DEFENSIVE purposes only. Understanding attack patterns helps build better network defences.

## Prerequisites

Before starting, ensure you have completed:
- Week 6 lab exercises
- Understanding of NAT types (Static, Dynamic, PAT)
- Familiarity with ARP protocol operation

## Submission Guidelines

1. Complete all `TODO` sections in each file
2. Run the built-in analysis functions
3. Answer all prediction prompts
4. Document any additional findings

## Grading Rubric

| Criterion | Points |
|-----------|--------|
| Correct implementation of parsing functions | 35% |
| Accurate anomaly detection logic | 30% |
| Analysis quality and insights | 20% |
| Code quality and documentation | 15% |

## Tips

- For NAT analysis, focus on understanding the conntrack entry format
- For ARP investigation, establish a baseline of known-good devices first
- Consider both false positives and false negatives in anomaly detection
- Real-world NAT tables can have thousands of entries — efficiency matters

## Security Considerations

The ARP anomaly detection exercise teaches defensive techniques:
- Gateway MAC changes are high-severity events
- Duplicate MACs may indicate MITM attacks OR legitimate load balancers
- Always verify findings before escalating

---

*Week 6 Homework — Computer Networks*
