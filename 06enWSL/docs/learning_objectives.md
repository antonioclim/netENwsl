# 📋 Learning Objectives Traceability Matrix — Week 6

> Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

## Overview

This document maps each Learning Objective (LO) to its supporting artefacts across the laboratory kit. Every LO achieves **6/6 coverage** across artefact types.

---

## Learning Objectives Summary

| LO | Bloom Level | Description |
|----|-------------|-------------|
| **LO1** | Remember | Recall NAT variants (Static, Dynamic, PAT) and supporting protocols (ARP, DHCP, ICMP) |
| **LO2** | Understand | Explain PAT translation tables and conntrack entry lifecycle |
| **LO3** | Apply | Implement NAT/MASQUERADE using iptables on a Linux router |
| **LO4** | Apply | Demonstrate SDN flow installation using ovs-ofctl commands |
| **LO5** | Analyse | Analyse permitted and blocked traffic based on OpenFlow rules |
| **LO6** | Analyse | Compare traditional networking architecture with SDN |
| **LO7** | Create | Design custom OpenFlow policies for security requirements |

---

## Coverage Matrix

| LO | Theory | Lab | Quiz | Misconception | Peer Instruction | Parsons | Total |
|----|--------|-----|------|---------------|------------------|---------|-------|
| LO1 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **6/6** |
| LO2 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **6/6** |
| LO3 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **6/6** |
| LO4 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **6/6** |
| LO5 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **6/6** |
| LO6 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **6/6** |
| LO7 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **6/6** |

**Overall Coverage:** ALL LOs have 6/6 artefact types. ✅

---

## Detailed Traceability

### LO1: Recall NAT Variants and Supporting Protocols

| Artefact Type | File Path | Coverage Type |
|---------------|-----------|---------------|
| **Theory** | `docs/theory_summary.md` § NAT Variants | 📖 Primary |
| **Lab Exercise** | `src/exercises/ex_6_01_nat_topology.py` | 🧪 Hands-on |
| **Quiz** | `formative/quiz.yaml` q01-q03 | ❓ Assessment |
| **Misconception** | `docs/misconceptions.md` #M1 | ⚠️ Self-check |
| **Peer Instruction** | `docs/peer_instruction.md` Q1, Q5 | 🗣️ Discussion |
| **Parsons Problem** | See P1 below | 🧩 Ordering |

---

### LO2: Explain PAT Translation Tables

| Artefact Type | File Path | Coverage Type |
|---------------|-----------|---------------|
| **Theory** | `docs/theory_summary.md` § PAT Operation | 📖 Primary |
| **Lab Exercise** | `src/apps/nat_observer.py` | 🧪 Observation |
| **Quiz** | `formative/quiz.yaml` q04-q06 | ❓ Assessment |
| **Misconception** | `docs/misconceptions.md` #M2, #M4 | ⚠️ Self-check |
| **Peer Instruction** | `docs/peer_instruction.md` Q2 | 🗣️ Discussion |
| **Parsons Problem** | See P2 below | 🧩 Ordering |
| **Code Tracing** | `docs/code_tracing.md` T1, T4 | 🔍 Analysis |

---

### LO3: Implement NAT/MASQUERADE

| Artefact Type | File Path | Coverage Type |
|---------------|-----------|---------------|
| **Theory** | `docs/theory_summary.md` § MASQUERADE | 📖 Reference |
| **Commands** | `docs/commands_cheatsheet.md` § iptables | 📋 Reference |
| **Lab Exercise** | `src/exercises/ex_6_01_nat_topology.py` | 🧪 Primary |
| **Quiz** | `formative/quiz.yaml` q07-q08, q15_live | ❓ Assessment |
| **Misconception** | `docs/misconceptions.md` #M3 | ⚠️ Self-check |
| **Peer Instruction** | `docs/peer_instruction.md` Q6 | 🗣️ Discussion |
| **Parsons Problem** | See P3 below | 🧩 Ordering |
| **Test** | `tests/test_exercises.py` test_exercise_1 | ✅ Validation |

---

### LO4: Demonstrate SDN Flow Installation

| Artefact Type | File Path | Coverage Type |
|---------------|-----------|---------------|
| **Theory** | `docs/theory_summary.md` § OpenFlow Protocol | 📖 Primary |
| **Commands** | `docs/commands_cheatsheet.md` § ovs-ofctl | 📋 Reference |
| **Lab Exercise** | `src/exercises/ex_6_02_sdn_topology.py` | 🧪 Primary |
| **Application** | `src/apps/sdn_policy_controller.py` | 🧪 Controller |
| **Quiz** | `formative/quiz.yaml` q09-q10, q16_live | ❓ Assessment |
| **Misconception** | `docs/misconceptions.md` #M5 | ⚠️ Self-check |
| **Peer Instruction** | `docs/peer_instruction.md` Q4, Q7 | 🗣️ Discussion |
| **Parsons Problem** | See P4 below | 🧩 Ordering |
| **Test** | `tests/test_exercises.py` test_exercise_2 | ✅ Validation |

---

### LO5: Analyse Permitted/Blocked Traffic

| Artefact Type | File Path | Coverage Type |
|---------------|-----------|---------------|
| **Theory** | `docs/theory_summary.md` § Flow Matching | 📖 Primary |
| **Lab Exercise** | `src/exercises/ex_6_02_sdn_topology.py` Ex2-Ex3 | 🧪 Analysis |
| **Quiz** | `formative/quiz.yaml` q11-q12 | ❓ Assessment |
| **Misconception** | `docs/misconceptions.md` #M6 | ⚠️ Self-check |
| **Peer Instruction** | `docs/peer_instruction.md` Q3 | 🗣️ Discussion |
| **Parsons Problem** | See P5 below | 🧩 Ordering |
| **Code Tracing** | `docs/code_tracing.md` T2 | 🔍 Analysis |

---

### LO6: Compare Traditional vs SDN

| Artefact Type | File Path | Coverage Type |
|---------------|-----------|---------------|
| **Theory** | `docs/theory_summary.md` § SDN Architecture | 📖 Primary |
| **Concept Analogies** | `docs/concept_analogies.md` | 🎯 Understanding |
| **Quiz** | `formative/quiz.yaml` q13 | ❓ Assessment |
| **Misconception** | `docs/misconceptions.md` #M5 | ⚠️ Self-check |
| **Peer Instruction** | `docs/peer_instruction.md` Q4 | 🗣️ Discussion |
| **Parsons Problem** | Covered in P4 context | 🧩 Ordering |

---

### LO7: Design OpenFlow Policies

| Artefact Type | File Path | Coverage Type |
|---------------|-----------|---------------|
| **Theory** | `docs/theory_summary.md` § Policy Design | 📖 Primary |
| **Lab Exercise** | `src/exercises/ex_6_02_sdn_topology.py` Ex3 | 🧪 Custom policies |
| **Application** | `src/apps/sdn_policy_controller.py` | 🧪 Implementation |
| **Quiz** | `formative/quiz.yaml` q14 | ❓ Assessment |
| **Misconception** | `docs/misconceptions.md` #M6, #M7 | ⚠️ Self-check |
| **Peer Instruction** | `docs/peer_instruction.md` Q8 | 🗣️ Discussion |
| **Parsons Problem** | See P5 below | 🧩 Ordering |

---

# 🧩 Parsons Problems

Parsons problems require students to arrange code blocks in correct order. Each problem includes **distractors** (incorrect blocks) marked with ❌.

---

## P1: ARP Resolution Sequence (LO1)

**Task:** Arrange the steps that occur when Host A (192.168.1.10) wants to send a packet to Host B (192.168.1.20) for the first time.

### Correct Blocks (arrange these):

```
1. Host A checks its ARP cache for 192.168.1.20's MAC address
2. ARP cache miss — no entry found
3. Host A broadcasts ARP Request: "Who has 192.168.1.20?"
4. All hosts on the segment receive the broadcast
5. Host B recognises its own IP and prepares a reply
6. Host B sends ARP Reply (unicast) with its MAC address
7. Host A adds the mapping to its ARP cache
8. Host A sends the original packet to Host B's MAC
```

### Distractors (do NOT use):

```
❌ Host A sends the packet to the default gateway
❌ Host B broadcasts its ARP Reply to all hosts
❌ The switch performs ARP resolution on behalf of hosts
❌ Host A waits for DHCP to provide the MAC address
```

### Solution Order: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8

---

## P2: Conntrack Entry Lifecycle (LO2)

**Task:** Arrange the stages of a conntrack entry for a TCP connection through NAT.

### Correct Blocks (arrange these):

```
1. Internal host initiates TCP SYN to external server
2. NAT creates conntrack entry in NEW state
3. NAT translates source IP and port (MASQUERADE)
4. External server responds with SYN-ACK
5. Conntrack entry transitions to ESTABLISHED state
6. Bidirectional traffic flows using the translation mapping
7. TCP FIN exchange begins connection termination
8. Conntrack entry transitions to TIME_WAIT
9. Entry expires and is removed after timeout
```

### Distractors (do NOT use):

```
❌ Conntrack entry is created when the server responds
❌ NAT assigns a new IP address from a pool
❌ The entry is permanent until manually deleted
❌ UDP connections skip the ESTABLISHED state
```

### Solution Order: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9

---

## P3: Configuring NAT with iptables (LO3)

**Task:** Arrange the commands to configure NAT on a Linux router (eth0=private, eth1=public).

### Correct Blocks (arrange these):

```
1. # Enable IP forwarding
2. sysctl -w net.ipv4.ip_forward=1
3. # Allow forwarding between interfaces
4. iptables -A FORWARD -i eth0 -o eth1 -j ACCEPT
5. iptables -A FORWARD -i eth1 -o eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT
6. # Enable MASQUERADE for outbound traffic
7. iptables -t nat -A POSTROUTING -o eth1 -s 192.168.1.0/24 -j MASQUERADE
8. # Verify configuration
9. iptables -t nat -L -n -v
```

### Distractors (do NOT use):

```
❌ iptables -t nat -A PREROUTING -i eth0 -j MASQUERADE
❌ sysctl -w net.ipv4.ip_forward=0
❌ iptables -A INPUT -j MASQUERADE
❌ iptables -t nat -A POSTROUTING -o eth0 -j SNAT
```

### Solution Order: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9

**Key Insight:** MASQUERADE must be in POSTROUTING chain, on the public interface (-o eth1), for traffic from the private subnet.

---

## P4: Installing an OpenFlow Rule (LO4)

**Task:** Arrange the steps to install a flow rule that forwards HTTP traffic to port 2.

### Correct Blocks (arrange these):

```
1. # Connect to the switch using OpenFlow 1.3
2. ovs-ofctl -O OpenFlow13 \
3. # Add a new flow rule
4. add-flow s1 \
5. # Set priority and match criteria
6. "priority=100,tcp,tp_dst=80,\
7. # Define the action
8. actions=output:2"
9. # Verify the rule was installed
10. ovs-ofctl -O OpenFlow13 dump-flows s1
```

### Distractors (do NOT use):

```
❌ ovs-ofctl -O OpenFlow10 add-flow s1
❌ "priority=100,udp,tp_dst=80,actions=drop"
❌ ovs-vsctl add-flow s1 "tcp,actions=output:2"
❌ "priority=100,http,actions=output:2"
```

### Solution Order: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10

**Key Insight:** OpenFlow matches on tcp,tp_dst=80 not "http". Protocol version flag is required.

---

## P5: Designing an SDN Security Policy (LO5, LO7)

**Task:** Arrange the flow rules to implement: "Allow SSH to server, block all else to server, allow everything else."

### Correct Blocks (arrange these):

```
1. # Rule 1: Allow SSH (port 22) to server 10.0.6.12
2. ovs-ofctl -O OpenFlow13 add-flow s1 \
3. "priority=100,tcp,nw_dst=10.0.6.12,tp_dst=22,actions=output:2"

4. # Rule 2: Block all other traffic to server
5. ovs-ofctl -O OpenFlow13 add-flow s1 \
6. "priority=50,ip,nw_dst=10.0.6.12,actions=drop"

7. # Rule 3: Default allow for all other traffic
8. ovs-ofctl -O OpenFlow13 add-flow s1 \
9. "priority=10,ip,actions=NORMAL"
```

### Distractors (do NOT use):

```
❌ "priority=50,tcp,nw_dst=10.0.6.12,tp_dst=22,actions=output:2"
❌ "priority=100,ip,nw_dst=10.0.6.12,actions=drop"
❌ "priority=10,ip,nw_dst=10.0.6.12,actions=NORMAL"
❌ "priority=100,ip,actions=drop"
```

### Solution Order: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9

**Key Insight:** Specific permit (100) > General deny (50) > Default allow (10). Higher priority number = checked first.

---

## Parsons Problem Answer Key

| Problem | LO Coverage | Correct Order | Common Mistake |
|---------|-------------|---------------|----------------|
| P1 | LO1 | 1-2-3-4-5-6-7-8 | Thinking ARP reply is broadcast |
| P2 | LO2 | 1-2-3-4-5-6-7-8-9 | Missing NEW state before ESTABLISHED |
| P3 | LO3 | 1-2-3-4-5-6-7-8-9 | Using PREROUTING instead of POSTROUTING |
| P4 | LO4 | 1-2-3-4-5-6-7-8-9-10 | Forgetting -O OpenFlow13 flag |
| P5 | LO5, LO7 | 1-2-3-4-5-6-7-8-9 | Putting block rule at highest priority |

---

## Assessment Integration

Each Parsons problem can be:
- Used as **pre-lab warm-up** (paper-based)
- Integrated into **LMS quizzes** (drag-and-drop)
- Part of **peer instruction** sessions
- Included in **homework** assignments

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.2.0 | 2026-01-24 | Added 5 Parsons problems with distractors |
| 1.1.0 | 2026-01-24 | Full 6/6 LO coverage achieved |
| 1.0.0 | 2025-01-24 | Initial traceability matrix |

---

*Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim*
*Contact: Issues: Open an issue in GitHub*
