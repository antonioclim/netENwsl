# 🎯 Learning Objectives — Week 2: Architectural Models and Socket Programming

> NETWORKING class — ASE, CSIE Bucharest  
> Computer Networks Laboratory | by ing. dr. Antonio Clim

---

## Overview

This document maps Week 2 learning objectives to the revised Anderson-Bloom Taxonomy, providing clear expectations for what students should be able to do at each cognitive level.

---

## Prerequisites

Before starting Week 2, students should be able to:

| Skill | Source | Verification |
|-------|--------|--------------|
| Navigate Linux filesystem | Week 1 | `cd`, `ls`, `pwd` commands |
| Run Python scripts | Week 1 | `python3 script.py` |
| Use Docker basic commands | Week 1 | `docker ps`, `docker exec` |
| Read error messages | Week 1 | Identify file/line number |
| Use terminal multiplexing | Week 1 | Run server + client in separate terminals |

**Self-check:** If any prerequisite is unclear, review Week 1 materials before proceeding.

---

## Bloom Taxonomy Levels

| Level | Cognitive Process | Typical Verbs |
|-------|-------------------|---------------|
| 1. **REMEMBER** | Retrieve knowledge | Define, list, recall, identify |
| 2. **UNDERSTAND** | Construct meaning | Explain, describe, compare, classify |
| 3. **APPLY** | Use in new situations | Implement, execute, use, demonstrate |
| 4. **ANALYSE** | Break into parts | Differentiate, debug, test, examine |
| 5. **EVALUATE** | Make judgements | Justify, critique, recommend, assess |
| 6. **CREATE** | Produce new work | Design, construct, develop, propose |

---

## Week 2 Learning Objectives by Level

### Level 1: REMEMBER (10-15% of assessment)

By the end of Week 2, students will be able to:

| ID | Objective | Assessment Method |
|----|-----------|-------------------|
| R1 | **List** the seven layers of the OSI model in order | Quiz question |
| R2 | **Identify** the four layers of the TCP/IP model | Quiz question |
| R3 | **Recall** the socket types for TCP (SOCK_STREAM) and UDP (SOCK_DGRAM) | Code recognition |
| R4 | **State** the default port for common services (HTTP: 80, HTTPS: 443, SSH: 22) | Quick recall |
| R5 | **Define** terms: socket, port, handshake, datagram, segment | Glossary quiz |

**Evidence of mastery:** Students can answer these without reference materials.

---

### Level 2: UNDERSTAND (20-25% of assessment)

By the end of Week 2, students will be able to:

| ID | Objective | Assessment Method |
|----|-----------|-------------------|
| U1 | **Explain** the difference between connection-oriented (TCP) and connectionless (UDP) protocols | Written explanation |
| U2 | **Describe** the TCP three-way handshake process (SYN → SYN-ACK → ACK) | Diagram completion |
| U3 | **Compare** iterative vs concurrent server architectures | Comparison table |
| U4 | **Classify** applications by appropriate protocol (TCP vs UDP) | Matching exercise |
| U5 | **Interpret** Wireshark capture showing TCP handshake | Capture analysis |
| U6 | **Summarise** why TCP does not preserve message boundaries | Short answer |

**Evidence of mastery:** Students can explain concepts in their own words to a peer.

---

### Level 3: APPLY (30-35% of assessment)

By the end of Week 2, students will be able to:

| ID | Objective | Assessment Method |
|----|-----------|-------------------|
| A1 | **Implement** a basic TCP echo server in Python | Working code |
| A2 | **Implement** a basic UDP echo server in Python | Working code |
| A3 | **Use** socket options (SO_REUSEADDR) to handle port reuse | Code inclusion |
| A4 | **Execute** Wireshark filters to isolate TCP/UDP traffic | Live demonstration |
| A5 | **Demonstrate** concurrent request handling using threading | Load test |
| A6 | **Apply** proper resource cleanup (context managers, close()) | Code review |

**Evidence of mastery:** Students can write working code that passes automated tests.

---

### Level 4: ANALYSE (15-20% of assessment)

By the end of Week 2, students will be able to:

| ID | Objective | Assessment Method |
|----|-----------|-------------------|
| N1 | **Debug** "Address already in use" errors using `ss` command | Troubleshooting exercise |
| N2 | **Examine** Wireshark captures to identify protocol inefficiencies | Capture analysis |
| N3 | **Differentiate** between bind addresses (127.0.0.1 vs 0.0.0.0) effects | Experiment results |
| N4 | **Test** server behaviour under concurrent load | Benchmark report |
| N5 | **Trace** code execution to predict output | Code tracing exercise |

**Evidence of mastery:** Students can diagnose issues and explain root causes.

---

### Level 5: EVALUATE (5-10% of assessment)

By the end of Week 2, students will be able to:

| ID | Objective | Assessment Method |
|----|-----------|-------------------|
| E1 | **Justify** protocol choice (TCP vs UDP) for given scenarios | Scenario analysis |
| E2 | **Assess** whether iterative or threaded server is appropriate | Design decision |
| E3 | **Critique** code for proper error handling and resource management | Code review |
| E4 | **Recommend** improvements to a given server implementation | Written recommendations |

**Evidence of mastery:** Students can defend their technical decisions with evidence.

---

### Level 6: CREATE (5-10% of assessment)

By the end of Week 2, students will be able to:

| ID | Objective | Assessment Method |
|----|-----------|-------------------|
| C1 | **Design** a simple application protocol with framing | Protocol specification |
| C2 | **Develop** a client-server application for a specified use case | Complete implementation |
| C3 | **Construct** test cases for socket applications | Test suite |

**Evidence of mastery:** Students can produce original, working solutions to novel problems.

---

## Assessment Mapping

### Lab Exercises

| Exercise | Primary Objectives | Bloom Levels |
|----------|-------------------|--------------|
| ex_2_01_tcp.py | A1, A5, A6, N1 | APPLY, ANALYSE |
| ex_2_02_udp.py | A2, A6, U1 | APPLY, UNDERSTAND |
| Pair Exercise P1 | A1, A5, N4 | APPLY, ANALYSE |
| Pair Exercise P2 | A2, U4 | APPLY, UNDERSTAND |
| Pair Exercise P3 | N4, E2 | ANALYSE, EVALUATE |

### Peer Instruction Questions

| Question | Targets Misconception | Bloom Level |
|----------|----------------------|-------------|
| Q1: TCP boundaries | U6 | UNDERSTAND |
| Q2: UDP bidirectional | U1 | UNDERSTAND |
| Q3: Bind address | N3 | ANALYSE |
| Q4: Handshake frequency | U2 | UNDERSTAND |
| Q5: Threading | E2 | EVALUATE |

### Homework Assignments

| Assignment | Objectives | Bloom Levels |
|------------|-----------|--------------|
| hw_2_01 | A1, A6, C2 | APPLY, CREATE |
| hw_2_02 | N5, E3 | ANALYSE, EVALUATE |

---

## Skills Assessment Checklist

Students can use this checklist for self-assessment:

### Foundational Skills (Required)

- [ ] I can explain why TCP is called "connection-oriented"
- [ ] I can explain why UDP is called "connectionless"
- [ ] I can draw the TCP three-way handshake
- [ ] I can write a basic TCP server from memory
- [ ] I can write a basic UDP server from memory
- [ ] I can use Wireshark to capture and filter traffic

### Intermediate Skills (Expected)

- [ ] I can implement concurrent handling with threading
- [ ] I can debug "Address already in use" errors
- [ ] I can explain why TCP doesn't preserve message boundaries
- [ ] I can choose between TCP and UDP for a given scenario
- [ ] I can use `ss` to inspect socket states

### Advanced Skills (Stretch Goals)

- [ ] I can design a simple application protocol with framing
- [ ] I can benchmark server performance under load
- [ ] I can explain when thread pools are better than per-connection threads
- [ ] I can implement proper timeout handling

---

## Post-Requisites

After completing Week 2, students will be prepared for:

| Week | Topic | Connection to Week 2 |
|------|-------|---------------------|
| Week 3 | UDP Broadcast/Multicast | Extends UDP concepts |
| Week 4 | Custom Protocols | Builds on framing concepts |
| Week 8 | HTTP/Transport | TCP in action |
| Week 10 | HTTPS/REST | Secure TCP connections |

---

## Revision Priorities

If time is limited, focus on these high-value objectives:

| Priority | Objectives | Rationale |
|----------|-----------|-----------|
| **Must know** | R3, U1, U2, A1, A2 | Core competencies needed for later weeks |
| **Should know** | U3, A5, N1, N3 | Common practical issues |
| **Nice to know** | E1, E2, C1 | Deeper understanding, less frequently assessed |

---

*NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim*
