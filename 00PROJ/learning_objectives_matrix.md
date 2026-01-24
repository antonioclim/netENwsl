# Learning Objectives Traceability Matrix

> **Purpose:** Bidirectional mapping between Learning Objectives, project stages, assessments and artefacts  
> **Course:** Computer Networks (Rețele de Calculatoare)  
> **Institution:** ASE Bucharest - CSIE  
> **Version:** 2.0 (Formalised)  
> **Last Updated:** January 2026

---

## Legend

| Symbol | Meaning |
|--------|---------|
| ✓ | Fully addressed |
| ◐ | Partially addressed |
| — | Not applicable |
| 📖 | Theory coverage |
| 💻 | Lab exercise |
| ✅ | Test validation |
| 📊 | PCAP/instrumentation |
| ⚠️ | Misconception documented |
| 📝 | Quiz question |

---

## How to Use This Matrix

### For Students
1. Identify which LOs your project addresses
2. Ensure you have artefacts for each LO before submission
3. Use the "Weak Coverage" column to identify gaps
4. Review misconceptions before the final presentation

### For Instructors
1. Verify LO coverage meets course requirements
2. Use gap analysis for formative feedback
3. Align assessment rubrics with LO weights

---

## Project LO Coverage Summary

| Project | LO Count | Avg. Bloom | Min Coverage | Assessment Focus |
|---------|----------|------------|--------------|------------------|
| P01 | 5 | Apply | 4/6 artefacts | SDN architecture and firewall rules |
| P06 | 6 | Apply | 4/6 artefacts | OpenFlow controller implementation |
| P07 | 6 | Apply | 4/6 artefacts | IDS signatures and alerting |
| P08 | 6 | Apply | 4/6 artefacts | HTTP parsing and reverse proxy |
| P09 | 6 | Understand | 4/6 artefacts | FTP protocol implementation |
| P10 | 5 | Apply | 4/6 artefacts | Docker network configuration |
| P11 | 6 | Analyse | 5/6 artefacts | QoS and traffic classification |
| P12 | 6 | Apply | 4/6 artefacts | Load balancing algorithms |
| P13 | 6 | Apply | 4/6 artefacts | gRPC streaming patterns |
| P14 | 6 | Evaluate | 5/6 artefacts | Detection accuracy analysis |
| P15 | 6 | Apply | 4/6 artefacts | MQTT QoS and pub-sub |

---

## P01: SDN Firewall with Mininet

### Learning Objectives

| ID | Description | Bloom Level | Verb |
|----|-------------|-------------|------|
| LO1 | Explain SDN architecture and control/data plane separation | Understand | Explain |
| LO2 | Implement OpenFlow flow rules for packet filtering | Apply | Implement |
| LO3 | Configure virtual network topologies in Mininet | Apply | Configure |
| LO4 | Analyse flow table behaviour and packet traces | Analyse | Analyse |
| LO5 | Design security rules for SDN environments | Create | Design |

### Stage Coverage Matrix

| LO | E1 Design | E2 Prototype | E3 Final | E4 Presentation |
|----|-----------|--------------|----------|-----------------|
| LO1 | ✓ Documented | — | — | ✓ Explained |
| LO2 | — | ✓ Implemented | ✓ Complete | ✓ Demonstrated |
| LO3 | ✓ Planned | ✓ Working | ✓ Tested | — |
| LO4 | — | ◐ Basic | ✓ Analysed | ✓ Presented |
| LO5 | ✓ Designed | — | ✓ Evaluated | — |

### Artefact Traceability (LO → Artefact)

| LO | 📖 Theory | 💻 Lab | ✅ Test | 📊 PCAP | ⚠️ Misconception | 📝 Quiz |
|----|-----------|--------|---------|---------|-------------------|---------|
| LO1 | docs/theory_summary.md#sdn | — | — | — | docs/misconceptions.md#control-data-plane | q01, q02, q03 |
| LO2 | docs/theory_summary.md#openflow | src/controller/firewall.py | tests/test_firewall.py | — | docs/misconceptions.md#drop-action | q04, q05, q06 |
| LO3 | docs/theory_summary.md#mininet | mininet/topology.py | tests/test_topology.py | — | — | q07, q08, q09 |
| LO4 | Lecture S7 | — | tests/test_analysis.py | pcap/flow_analysis.pcap | — | q10, q11 |
| LO5 | docs/theory_summary.md#security | src/controller/rules.py | tests/test_rules.py | — | docs/misconceptions.md#security-rules | q12, q13 |

### Reverse Traceability (Artefact → LO)

| Artefact | Path | Addresses LO |
|----------|------|--------------|
| Theory Summary | docs/theory_summary.md | LO1, LO2, LO3, LO5 |
| Firewall Module | src/controller/firewall.py | LO2 |
| Topology Definition | mininet/topology.py | LO3 |
| Rule Configuration | src/controller/rules.py | LO5 |
| Firewall Tests | tests/test_firewall.py | LO2 |
| Topology Tests | tests/test_topology.py | LO3 |
| Analysis Tests | tests/test_analysis.py | LO4 |
| Flow Analysis PCAP | pcap/flow_analysis.pcap | LO4 |
| Misconceptions Doc | docs/misconceptions.md | LO1, LO2, LO5 |
| Quiz P01 | formative/quiz_p01.yaml | LO1-LO5 |

### Coverage Summary

| LO | Artefacts | Coverage | Status |
|----|-----------|----------|--------|
| LO1 | 📖 ⚠️ 📝 | 3/6 | ⚠️ Add lab exercise |
| LO2 | 📖 💻 ✅ ⚠️ 📝 | 5/6 | ✓ Complete |
| LO3 | 📖 💻 ✅ 📝 | 4/6 | ✓ Adequate |
| LO4 | 📖 ✅ 📊 📝 | 4/6 | ✓ Adequate |
| LO5 | 📖 💻 ✅ ⚠️ 📝 | 5/6 | ✓ Complete |

---

## P06: SDN Controller with OpenFlow

### Learning Objectives

| ID | Description | Bloom Level | Verb |
|----|-------------|-------------|------|
| LO1 | Explain the role of SDN controllers in network management | Understand | Explain |
| LO2 | Implement a learning switch using OpenFlow | Apply | Implement |
| LO3 | Develop topology discovery mechanisms | Apply | Develop |
| LO4 | Monitor network statistics via flow queries | Analyse | Monitor |
| LO5 | Analyse flow table convergence behaviour | Analyse | Analyse |
| LO6 | Design custom network topologies | Create | Design |

### Stage Coverage Matrix

| LO | E1 Design | E2 Prototype | E3 Final | E4 Presentation |
|----|-----------|--------------|----------|-----------------|
| LO1 | ✓ | — | — | ✓ |
| LO2 | — | ✓ | ✓ | ✓ |
| LO3 | — | ◐ | ✓ | ✓ |
| LO4 | — | — | ✓ | ✓ |
| LO5 | — | — | ✓ | ✓ |
| LO6 | ✓ | ✓ | — | — |

### Artefact Traceability

| LO | 📖 Theory | 💻 Lab | ✅ Test | 📊 PCAP | ⚠️ Misconception | 📝 Quiz |
|----|-----------|--------|---------|---------|-------------------|---------|
| LO1 | ✓ | — | — | — | ✓ | ✓ |
| LO2 | ✓ | ✓ | ✓ | — | ✓ | ✓ |
| LO3 | ✓ | ✓ | ✓ | ✓ | — | ✓ |
| LO4 | ✓ | ✓ | ✓ | ✓ | — | ✓ |
| LO5 | ✓ | — | ✓ | ✓ | ✓ | ✓ |
| LO6 | ✓ | ✓ | — | — | — | ✓ |

---

## P10: Docker Network Configuration

### Learning Objectives

| ID | Description | Bloom Level | Verb |
|----|-------------|-------------|------|
| LO1 | Configure Docker bridge and overlay networks | Apply | Configure |
| LO2 | Implement container-to-container communication | Apply | Implement |
| LO3 | Explain DNS resolution within Docker networks | Understand | Explain |
| LO4 | Design multi-tier network architectures | Create | Design |
| LO5 | Troubleshoot Docker networking issues | Analyse | Troubleshoot |

### Stage Coverage Matrix

| LO | E1 Design | E2 Prototype | E3 Final | E4 Presentation |
|----|-----------|--------------|----------|-----------------|
| LO1 | ✓ | ✓ | ✓ | — |
| LO2 | — | ✓ | ✓ | ✓ |
| LO3 | ✓ | ✓ | — | ✓ |
| LO4 | ✓ | — | ✓ | — |
| LO5 | — | ✓ | ✓ | ✓ |

### Artefact Traceability

| LO | 📖 Theory | 💻 Lab | ✅ Test | 📊 Logs | ⚠️ Misconception | 📝 Quiz |
|----|-----------|--------|---------|---------|-------------------|---------|
| LO1 | ✓ | ✓ | ✓ | — | ✓ | ✓ |
| LO2 | ✓ | ✓ | ✓ | ✓ | — | ✓ |
| LO3 | ✓ | ✓ | ✓ | — | ✓ | ✓ |
| LO4 | ✓ | ✓ | — | — | — | ✓ |
| LO5 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

---

## P12: Docker Microservices with Load Balancing

### Learning Objectives

| ID | Description | Bloom Level | Verb |
|----|-------------|-------------|------|
| LO1 | Implement load balancing algorithms (round-robin, weighted) | Apply | Implement |
| LO2 | Design health check mechanisms for backend services | Create | Design |
| LO3 | Configure Docker networks for service communication | Apply | Configure |
| LO4 | Handle backend failures with automatic failover | Apply | Handle |
| LO5 | Measure and analyse load distribution effectiveness | Evaluate | Measure |
| LO6 | Implement service discovery patterns | Apply | Implement |

### Stage Coverage Matrix

| LO | E1 Design | E2 Prototype | E3 Final | E4 Presentation |
|----|-----------|--------------|----------|-----------------|
| LO1 | — | ✓ | ✓ | ✓ |
| LO2 | ✓ | ✓ | ✓ | — |
| LO3 | ✓ | ✓ | — | — |
| LO4 | — | ◐ | ✓ | ✓ |
| LO5 | — | — | ✓ | ✓ |
| LO6 | — | — | ✓ | ✓ |

---

## P13: RPC/gRPC Service

### Learning Objectives

| ID | Description | Bloom Level | Verb |
|----|-------------|-------------|------|
| LO1 | Define services and messages in Protocol Buffer files | Apply | Define |
| LO2 | Implement unary RPC methods | Apply | Implement |
| LO3 | Use server-side streaming for large data transfers | Apply | Use |
| LO4 | Implement client-side streaming for batch operations | Apply | Implement |
| LO5 | Compare gRPC performance with REST APIs | Evaluate | Compare |
| LO6 | Handle errors, deadlines and cancellation | Apply | Handle |

### Stage Coverage Matrix

| LO | E1 Design | E2 Prototype | E3 Final | E4 Presentation |
|----|-----------|--------------|----------|-----------------|
| LO1 | ✓ | ✓ | — | — |
| LO2 | — | ✓ | ✓ | ✓ |
| LO3 | — | ◐ | ✓ | ✓ |
| LO4 | — | — | ✓ | ✓ |
| LO5 | — | — | ✓ | ✓ |
| LO6 | — | — | ✓ | ✓ |

---

## P15: MQTT IoT Application

### Learning Objectives

| ID | Description | Bloom Level | Verb |
|----|-------------|-------------|------|
| LO1 | Implement publish-subscribe communication patterns | Apply | Implement |
| LO2 | Design hierarchical topic structures | Create | Design |
| LO3 | Use different QoS levels appropriately | Apply | Use |
| LO4 | Handle connection loss and reconnection | Apply | Handle |
| LO5 | Implement retained messages and last will | Apply | Implement |
| LO6 | Process real-time sensor data streams | Apply | Process |

### Stage Coverage Matrix

| LO | E1 Design | E2 Prototype | E3 Final | E4 Presentation |
|----|-----------|--------------|----------|-----------------|
| LO1 | — | ✓ | ✓ | ✓ |
| LO2 | ✓ | ✓ | — | — |
| LO3 | — | ◐ | ✓ | ✓ |
| LO4 | — | — | ✓ | ✓ |
| LO5 | — | — | ✓ | ✓ |
| LO6 | — | ✓ | ✓ | ✓ |

---

## Bloom Taxonomy Distribution

### By Level

| Bloom Level | Count | Percentage | Projects |
|-------------|-------|------------|----------|
| Remember | 0 | 0% | — |
| Understand | 8 | 14% | P01, P06, P10 |
| Apply | 38 | 66% | All |
| Analyse | 7 | 12% | P01, P06, P10, P11 |
| Evaluate | 3 | 5% | P12, P13, P14 |
| Create | 6 | 10% | P01, P06, P10, P12, P15 |

### Verbs Used

| Level | Verbs |
|-------|-------|
| Understand | Explain |
| Apply | Implement, Configure, Use, Handle, Define, Process |
| Analyse | Analyse, Troubleshoot, Monitor |
| Evaluate | Measure, Compare, Evaluate |
| Create | Design, Develop |

---

## Lab Week Cross-Reference

| Week | Topic | Related LOs |
|------|-------|-------------|
| 2 | Socket Programming | P08-LO2, P09-LO2, P09-LO4 |
| 6 | SDN Architecture | P01-LO1-5, P06-LO1-6, P11-LO1-6 |
| 7 | Packet Capture | P01-LO4, P03-LO2, P07-LO2, P14-LO1 |
| 8 | HTTP Protocol | P08-LO1, P08-LO5, P12-LO5 |
| 10 | Docker Networking | P10-LO1-5, P12-LO3 |
| 11 | Load Balancing | P08-LO6, P11-LO4, P12-LO1-5 |
| 12 | RPC | P13-LO1-6 |
| 13 | MQTT/IoT | P15-LO1-6, P01-LO5, P07-LO3-5, P14-LO1-6 |

---

## Formative Assessment Mapping

### Quiz Coverage per Project

| Project | Quiz File | Questions | LO Coverage |
|---------|-----------|-----------|-------------|
| P01 | formative/quiz_template.yaml | 13 | LO1-LO5 (100%) |
| P06 | formative/quiz_p06.yaml | 15 | LO1-LO6 (100%) |
| P10 | formative/quiz_p10.yaml | 10 | LO1-LO5 (100%) |
| P12 | formative/quiz_p12.yaml | 12 | LO1-LO6 (100%) |
| P13 | formative/quiz_p13.yaml | 12 | LO1-LO6 (100%) |
| P15 | formative/quiz_p15.yaml | 12 | LO1-LO6 (100%) |

### Parsons Problems Coverage

| Problem ID | Project | LO | Topic |
|------------|---------|-----|-------|
| parsons_001 | P01 | LO2 | OpenFlow drop rule |
| parsons_002 | P08 | LO2 | TCP server socket |
| parsons_003 | P10 | LO1 | Docker Compose |
| parsons_004 | P13 | LO2 | gRPC server |
| parsons_005 | P15 | LO1 | MQTT publish |

---

## Gap Analysis Template

Use this template to identify coverage gaps for your project:

```markdown
### [Project ID] Gap Analysis

| LO | Has Theory | Has Lab | Has Test | Has PCAP | Has Misconception | Has Quiz | Gap Action |
|----|------------|---------|----------|----------|-------------------|----------|------------|
| LO1 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | [Action needed] |
| LO2 | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | [Action needed] |
| ... | ... | ... | ... | ... | ... | ... | ... |

**Minimum Required:** 4/6 artefact types per LO
**Recommended:** 5/6 artefact types per LO
```

---

*Learning Objectives Traceability Matrix v2.0*  
*Computer Networks — ASE Bucharest, CSIE*  
*Generated: January 2026*
