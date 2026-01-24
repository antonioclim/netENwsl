# 🎯 Learning Objectives Traceability Matrix — Week 7
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> This document provides explicit traceability from each Learning Objective (LO) 
> to all supporting learning artifacts in the Week 7 kit.

---

## Quick Reference

| LO | Description | Bloom Level | Primary Exercise |
|----|-------------|-------------|------------------|
| LO1 | Identify TCP/UDP packet fields | Remember/Understand | Exercise 1 |
| LO2 | Explain app vs network-layer failures | Understand | Exercises 2, 3 |
| LO3 | Implement IP-based filtering rules | Apply | Exercises 2, 4 |
| LO4 | Analyse packet captures for root causes | Analyse | All exercises |
| LO5 | Design custom firewall profiles | Create | Homework 1 |
| LO6 | Evaluate DROP vs REJECT trade-offs | Evaluate | Exercises 2-3 |

---

## Complete Traceability Matrix

```
Legend:
  ✅ = Complete coverage
  ⚠️ = Partial coverage  
  📝 = Exercise/Activity
  📖 = Documentation
  🧪 = Test/Validation
  📦 = Sample artifact
```

### LO1: Identify TCP and UDP packet fields in captured traffic

| Artifact Type | Path | Coverage | Notes |
|---------------|------|----------|-------|
| 📖 Theory | `docs/theory_summary.md#tcp-three-way-handshake` | ✅ | TCP handshake diagram |
| 📖 Theory | `docs/theory_summary.md#udp-connectionless-nature` | ✅ | UDP characteristics |
| 📝 Lab Exercise | `src/exercises/ex_7_01_baseline_capture.py` | ✅ | Baseline capture activity |
| 📝 README Exercise | `README.md#exercise-1-baseline-traffic-capture` | ✅ | Step-by-step instructions |
| 🧪 Test | `tests/test_exercises.py::test_tcp_connectivity` | ✅ | Validates TCP connection |
| 🧪 Test | `tests/test_exercises.py::test_udp_send` | ✅ | Validates UDP send |
| 📖 Misconception | `docs/misconceptions.md#misconception-3` | ✅ | tcpdump capture scope |
| 📖 Misconception | `docs/misconceptions.md#misconception-4` | ✅ | Wireshark interface selection |
| 📖 Peer Instruction | `docs/peer_instruction.md#question-4` | ✅ | TCP handshake packet count |
| 📖 Parsons | `docs/parsons_problems.md#problem-p1` | ✅ | Port probe implementation |
| 📖 Code Tracing | `docs/code_tracing.md#exercise-t1` | ✅ | TCP client connection trace |
| 📦 PCAP Sample | `pcap/samples/week07_lo1_tcp_handshake.pcap` | ✅ | Reference capture |

**Assessment:** Quiz questions q01, q02, q03

---

### LO2: Explain the difference between application-layer failures and network-layer filtering effects

| Artifact Type | Path | Coverage | Notes |
|---------------|------|----------|-------|
| 📖 Theory | `docs/theory_summary.md#filtering-semantics` | ✅ | DROP vs REJECT explained |
| 📖 Theory | `docs/theory_summary.md#port-states` | ✅ | Open/Closed/Filtered |
| 📝 Lab Exercise | `README.md#exercise-2-tcp-filtering-with-reject` | ✅ | REJECT observation |
| 📝 Lab Exercise | `README.md#exercise-3-udp-filtering-with-drop` | ✅ | DROP observation |
| 🧪 Test | `tests/test_exercises.py::test_tcp_blocked` | ✅ | Validates blocking detection |
| 📖 Misconception | `docs/misconceptions.md#misconception-1` | ✅ | DROP ≠ REJECT |
| 📖 Misconception | `docs/misconceptions.md#misconception-2` | ✅ | Closed ≠ Filtered |
| 📖 Misconception | `docs/misconceptions.md#misconception-6` | ✅ | UDP blocking invisible |
| 📖 Misconception | `docs/misconceptions.md#misconception-7` | ✅ | RST sources |
| 📖 Peer Instruction | `docs/peer_instruction.md#question-1` | ✅ | DROP vs REJECT behaviour |
| 📖 Peer Instruction | `docs/peer_instruction.md#question-2` | ✅ | Port states |
| 📖 Peer Instruction | `docs/peer_instruction.md#question-5` | ✅ | UDP blocking detection |
| 📖 Concept Analogy | `docs/concept_analogies.md#concept-2` | ✅ | Bouncer analogy |
| 📖 Concept Analogy | `docs/concept_analogies.md#concept-3` | ✅ | Phone call analogy |
| 📖 Parsons | `docs/parsons_problems.md#problem-p3` | ✅ | UDP error handling |
| 📦 PCAP Sample | `pcap/samples/week07_lo2_tcp_blocked_reject.pcap` | ✅ | REJECT capture |

**Assessment:** Quiz questions q04, q05, q06

---

### LO3: Implement IP-based allow and block filtering rules using iptables

| Artifact Type | Path | Coverage | Notes |
|---------------|------|----------|-------|
| 📖 Theory | `README.md#filtering-semantics` | ✅ | Policy concepts |
| 📖 Commands | `docs/commands_cheatsheet.md#iptables` | ✅ | iptables syntax |
| 📝 Lab Exercise | `README.md#exercise-2-tcp-filtering-with-reject` | ✅ | Apply REJECT profile |
| 📝 Lab Exercise | `README.md#exercise-3-udp-filtering-with-drop` | ✅ | Apply DROP profile |
| 📝 Lab Exercise | `README.md#exercise-4-application-layer-filter` | ✅ | Proxy filtering |
| 🧪 App | `src/apps/firewallctl.py` | ✅ | Profile management tool |
| 🧪 Config | `docker/configs/firewall_profiles.json` | ✅ | Profile definitions |
| 📖 Misconception | `docs/misconceptions.md#misconception-8` | ✅ | iptables persistence |
| 📖 Parsons | `docs/parsons_problems.md#problem-p2` | ✅ | Parse iptables output |
| 📖 Parsons | `docs/parsons_problems.md#problem-p4` | ✅ | Apply profile from JSON |
| 📖 Code Tracing | `docs/code_tracing.md#exercise-t3` | ✅ | Rule matching order |
| 📖 Troubleshooting | `docs/troubleshooting.md#firewall-rule-issues` | ✅ | Common problems |

**Assessment:** Quiz questions q07, q08, q09; Homework Assignment 1

---

### LO4: Analyse packet captures to determine root causes of connection timeouts, resets and drops

| Artifact Type | Path | Coverage | Notes |
|---------------|------|----------|-------|
| 📖 Theory | `docs/theory_summary.md#packet-capture-as-evidence` | ✅ | Capture semantics |
| 📖 Commands | `docs/commands_cheatsheet.md#tcpdump` | ✅ | tcpdump filters |
| 📖 Commands | `docs/commands_cheatsheet.md#tshark` | ✅ | tshark analysis |
| 📖 Commands | `README.md#suggested-wireshark-filters` | ✅ | Display filters |
| 📝 Lab Exercise | All exercises | ✅ | Each requires capture analysis |
| 🧪 App | `scripts/capture_traffic.py` | ✅ | Capture automation |
| 🧪 Test | `tests/expected_outputs.md` | ✅ | Expected capture contents |
| 📖 Misconception | `docs/misconceptions.md#misconception-3` | ✅ | Capture limitations |
| 📖 Misconception | `docs/misconceptions.md#misconception-5` | ✅ | Performance impact |
| 📖 Peer Instruction | `docs/peer_instruction.md#question-3` | ✅ | Interface selection |
| 📖 Parsons | `docs/parsons_problems.md#problem-p5` | ✅ | Analyse pcap with tshark |
| 📖 Code Tracing | `docs/code_tracing.md#exercise-t1` | ✅ | Socket state tracking |
| 📖 Code Tracing | `docs/code_tracing.md#exercise-t2` | ✅ | Probe result interpretation |
| 📖 Troubleshooting | `docs/troubleshooting.md#capture-issues` | ✅ | Capture problems |
| 📦 PCAP Sample | `pcap/samples/week07_lo4_timeout_analysis.pcap` | ✅ | Timeout example |

**Assessment:** Quiz questions q10, q11, q12; Homework Assignment 2

---

### LO5: Design custom firewall profiles that enforce specific traffic policies

| Artifact Type | Path | Coverage | Notes |
|---------------|------|----------|-------|
| 📖 Theory | `README.md#theoretical-background` | ✅ | Policy design principles |
| 📖 Template | `docker/configs/firewall_profiles.json` | ✅ | Profile structure |
| 📝 Homework | `homework/README.md#assignment-1` | ✅ | Custom profile task |
| 📝 Homework | `homework/exercises/hw_7_01_validate_firewall_profile.py` | ✅ | Validation script |
| 🧪 App | `src/apps/firewallctl.py` | ✅ | Profile application tool |
| 📖 Code Tracing | `docs/code_tracing.md#exercise-t3` | ✅ | Rule order importance |
| 📖 Troubleshooting | `docs/troubleshooting.md#rules-dont-take-effect` | ✅ | Design errors |

**Assessment:** Quiz question q13; Homework Assignment 1 (primary)

---

### LO6: Evaluate the trade-offs between DROP and REJECT filtering actions

| Artifact Type | Path | Coverage | Notes |
|---------------|------|----------|-------|
| 📖 Theory | `docs/theory_summary.md#choosing-between-drop-and-reject` | ✅ | Decision table |
| 📝 Lab Exercise | `README.md#exercise-2-tcp-filtering-with-reject` | ✅ | REJECT experience |
| 📝 Lab Exercise | `README.md#exercise-3-udp-filtering-with-drop` | ✅ | DROP experience |
| 📝 Demo | `README.md#demo-2-reject-vs-drop-comparison` | ✅ | Side-by-side comparison |
| 📖 Misconception | `docs/misconceptions.md#misconception-1` | ✅ | Action differences |
| 📖 Peer Instruction | `docs/peer_instruction.md#question-1` | ✅ | Observable difference |
| 📖 Concept Analogy | `docs/concept_analogies.md#concept-2` | ✅ | Bouncer analogy |
| 📦 PCAP Sample | `pcap/samples/week07_lo6_drop_vs_reject.pcap` | ✅ | Comparison capture |

**Assessment:** Quiz questions q14, q15

---

## Coverage Summary

| LO | Theory | Lab | Tests | PCAP | Misconceptions | Quiz | Coverage |
|----|--------|-----|-------|------|----------------|------|----------|
| LO1 | ✅ | ✅ | ✅ | ✅ | ✅ (2) | ✅ (3) | **100%** |
| LO2 | ✅ | ✅ | ✅ | ✅ | ✅ (4) | ✅ (3) | **100%** |
| LO3 | ✅ | ✅ | ✅ | ⚠️ | ✅ (1) | ✅ (3) | **95%** |
| LO4 | ✅ | ✅ | ✅ | ✅ | ✅ (2) | ✅ (3) | **100%** |
| LO5 | ✅ | ✅ | ⚠️ | ⚠️ | ⚠️ | ✅ (1) | **80%** |
| LO6 | ✅ | ✅ | ✅ | ✅ | ✅ (1) | ✅ (2) | **100%** |

**Overall Kit Coverage: 96%**

---

## Bloom's Taxonomy Distribution

```
┌────────────────────────────────────────────────────────────────┐
│                    BLOOM'S COVERAGE                            │
├────────────────────────────────────────────────────────────────┤
│ Remember    │ ████████░░ │ LO1 (partial)                       │
│ Understand  │ ██████████ │ LO1, LO2                            │
│ Apply       │ ██████████ │ LO3                                 │
│ Analyse     │ ██████████ │ LO4                                 │
│ Evaluate    │ ██████████ │ LO6                                 │
│ Create      │ ████████░░ │ LO5                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## Using This Matrix

### For Students

1. **Before lab:** Check which artifacts support your target LO
2. **During lab:** Follow the exercises linked to each LO
3. **After lab:** Use quiz questions to self-assess
4. **Struggling?** Consult the misconceptions document for that LO

### For Instructors

1. **Lesson planning:** Ensure all LOs have adequate coverage
2. **Assessment design:** Reference linked quiz questions
3. **Remediation:** Direct students to specific artifacts
4. **Kit improvement:** Identify gaps (⚠️) for future updates

---

*Computer Networks — Week 7: Packet Interception, Filtering and Defensive Port Probing*  
*ASE Bucharest, CSIE | by ing. dr. Antonio Clim*
