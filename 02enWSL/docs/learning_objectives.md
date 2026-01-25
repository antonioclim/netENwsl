# Learning Objectives — Week 2: Architectural Models and Socket Programming

> NETWORKING class — ASE, CSIE Bucharest  
> Computer Networks Laboratory | by ing. dr. Antonio Clim

---

## Bloom Taxonomy Levels

| Level | Cognitive Process | Verbs | Assessment Type |
|-------|-------------------|-------|-----------------|
| 1. REMEMBER | Retrieve knowledge | Define, list, recall, identify | MCQ, fill-in |
| 2. UNDERSTAND | Construct meaning | Explain, compare, summarise | Short answer |
| 3. APPLY | Use in situations | Implement, execute, demonstrate | Coding exercises |
| 4. ANALYSE | Break into parts | Debug, test, examine, trace | Problem solving |
| 5. EVALUATE | Make judgements | Justify, recommend, critique | Design decisions |
| 6. CREATE | Produce new work | Design, develop, construct | Projects |

---

## Learning Objectives

### Level 1: REMEMBER

| ID | Objective | Key Terms |
|----|-----------|-----------|
| R1 | List the seven layers of the OSI model and their PDUs | OSI, PDU, segment, packet, frame |
| R2 | Identify the four layers of the TCP/IP model | TCP/IP, Application, Transport, Internet, Network Access |
| R3 | Recall socket types for TCP (SOCK_STREAM) and UDP (SOCK_DGRAM) | socket, SOCK_STREAM, SOCK_DGRAM |
| R4 | State default ports for common services (HTTP:80, HTTPS:443, SSH:22) | port, well-known ports |
| R5 | Define key terms: socket, port, handshake, datagram, segment | vocabulary |

### Level 2: UNDERSTAND

| ID | Objective | Key Concepts |
|----|-----------|--------------|
| U1 | Explain the differences between TCP and UDP | reliability, ordering, connection |
| U2 | Describe the TCP three-way handshake sequence | SYN, SYN-ACK, ACK |
| U3 | Compare iterative vs concurrent server architectures | threading, blocking |
| U4 | Classify applications by appropriate protocol choice | real-time, file transfer |
| U5 | Interpret Wireshark TCP capture annotations | flags, sequence numbers |
| U6 | Summarise why TCP lacks message boundaries | byte stream, framing |

### Level 3: APPLY

| ID | Objective | Skills |
|----|-----------|--------|
| A1 | Implement a basic TCP echo server in Python | socket(), bind(), listen(), accept() |
| A2 | Implement a basic UDP echo server in Python | socket(), bind(), recvfrom(), sendto() |
| A3 | Use socket options correctly (SO_REUSEADDR) | setsockopt(), TIME_WAIT |
| A4 | Execute Wireshark filters to isolate traffic | tcp.port, udp.port, ip.addr |
| A5 | Demonstrate concurrent handling with threading | Thread, start(), join() |
| A6 | Apply proper resource cleanup with context managers | with statement, close() |

### Level 4: ANALYSE

| ID | Objective | Tasks |
|----|-----------|-------|
| N1 | Debug "Address already in use" errors systematically | lsof, ss, kill |
| N2 | Examine Wireshark captures to identify protocol issues | packet analysis |
| N3 | Differentiate bind address effects (127.0.0.1 vs 0.0.0.0) | interface binding |
| N4 | Test server behaviour under concurrent load | load testing |
| N5 | Trace code execution to predict output | code tracing |

### Level 5: EVALUATE

| ID | Objective | Decisions |
|----|-----------|-----------|
| E1 | Justify protocol choice (TCP vs UDP) for given scenarios | trade-offs |
| E2 | Assess server architecture appropriateness for workload | scalability |
| E3 | Critique code for proper error handling | exception handling |
| E4 | Recommend improvements for network application design | best practices |

### Level 6: CREATE

| ID | Objective | Products |
|----|-----------|----------|
| C1 | Design a simple application-layer protocol | protocol specification |
| C2 | Develop a complete client-server application | working code |
| C3 | Construct test cases for socket applications | test suite |

---

## Complete Traceability Matrix

### Primary Coverage

| LO | Theory | Lab Exercise | Quiz | Peer Instruction | Parsons | Misconception | Code Trace |
|----|--------|--------------|------|------------------|---------|---------------|------------|
| R1 | theory_summary §2 | — | q01, q03 | — | — | — | — |
| R2 | theory_summary §3 | — | q04 | — | — | — | — |
| R3 | theory_summary §4 | ex_2_01, ex_2_02 | q02 | — | tcp_server | #1 | T1 |
| R4 | theory_summary §4 | — | q05 | — | — | — | — |
| R5 | glossary.md | — | q01-q05 | — | — | — | — |
| U1 | theory_summary §4 | ex_2_01, ex_2_02 | q06, q08 | Q2 | — | #2, #8 | T2 |
| U2 | theory_summary §4.1 | ex_2_01 (Wireshark) | q07, q09 | Q4 | — | #7 | T3 |
| U3 | theory_summary §5 | ex_2_01 (modes) | q15 | Q5 | threaded | #4 | — |
| U4 | further_reading | homework | — | — | — | #8 | — |
| U5 | troubleshooting | ex_2_03 | — | — | — | — | — |
| U6 | misconceptions #1 | ex_2_01 | q11 | Q1 | — | #1 | T4 |
| A1 | ex_2_01 docstring | ex_2_01 | — | Q3 | tcp_server | #3, #6 | — |
| A2 | ex_2_02 docstring | ex_2_02 | — | Q2 | udp_client | #2 | — |
| A3 | ex_2_01 comments | ex_2_01 | q10 | — | error_handling | #10 | — |
| A4 | Wireshark guide | ex_2_03 | — | — | — | — | — |
| A5 | ex_2_01 docstring | ex_2_01 | q15 | Q5 | threaded | #4 | T5 |
| A6 | misconceptions #3 | all exercises | q13 | — | error_handling | #3 | — |
| N1 | troubleshooting | all exercises | q13 | — | — | #10 | — |
| N2 | Wireshark guide | ex_2_03 | — | — | — | — | — |
| N3 | misconceptions #6 | ex_2_01 | q14 | Q3 | — | #6 | — |
| N4 | ex_2_01 (load) | ex_2_01 | — | Q5 | — | — | — |
| N5 | code_tracing.md | all traces | — | — | — | — | T1-T5 |
| E1 | peer_instruction Q5 | homework | q15 | Q5 | — | #8 | — |
| E2 | peer_instruction Q5 | homework | — | — | — | #4 | — |
| E3 | code review | homework | — | — | — | #3 | — |
| E4 | reflection | homework | — | — | — | — | — |
| C1 | homework | hw_2_01 | — | — | — | — | — |
| C2 | homework | hw_2_02 | — | — | — | — | — |
| C3 | tests/ | test_exercises | — | — | — | — | — |

### Coverage Summary

| Assessment Type | LOs Covered | Notes |
|-----------------|-------------|-------|
| **Quiz (15 questions)** | R1-R5, U1-U3, U6, A1, A3, N1, N3, E1 | Automated grading |
| **Lab Exercises (3)** | A1-A6, N1-N4, U1-U3, U5-U6 | Hands-on practice |
| **Peer Instruction (5)** | U1-U3, U6, A1, A5, N3, E1 | Class discussion |
| **Parsons Problems (5)** | R3, A1, A2, A5, A6 | Code ordering |
| **Code Tracing (5)** | R3, U1-U2, U6, A5, N5 | Execution prediction |
| **Homework (2)** | C1, C2, E1-E4 | Extended projects |

---

## Assessment Alignment

### Exercise to LO Mapping

| Exercise | Primary Objectives | Bloom Levels |
|----------|-------------------|--------------|
| ex_2_01_tcp.py | A1, A3, A5, A6, N1, N3 | APPLY, ANALYSE |
| ex_2_02_udp.py | A2, A6, U1, U6 | APPLY, UNDERSTAND |
| Exercise 3 (capture) | A4, U5, N2 | APPLY, ANALYSE |
| hw_2_01 (calculator) | C1, C2, E1 | CREATE, EVALUATE |
| hw_2_02 (pcap analysis) | C3, N2, U5 | CREATE, ANALYSE |

### Bloom Level Distribution

| Level | Target % | Actual % | Status |
|-------|----------|----------|--------|
| REMEMBER | 10-15% | 12% (R1-R5) | ✅ On target |
| UNDERSTAND | 20-25% | 24% (U1-U6) | ✅ On target |
| APPLY | 30-35% | 32% (A1-A6, N1-N4) | ✅ On target |
| ANALYSE | 15-20% | 16% (N1-N5) | ✅ On target |
| EVALUATE | 5-10% | 8% (E1-E4) | ✅ On target |
| CREATE | 5-10% | 8% (C1-C3) | ✅ On target |

---

## Prerequisite Knowledge

Students should already be able to:
- Write basic Python programs (functions, classes, file I/O)
- Use command-line interfaces (bash, PowerShell)
- Understand basic networking concepts (IP addresses, ports) from Week 1
- Navigate the WSL/Docker environment

---

## Post-Lab Competencies

After completing Week 2, students will be ready to:
- Implement UDP broadcast and multicast (Week 3)
- Design custom binary protocols (Week 4)
- Debug more complex network applications
- Analyse protocol behaviour using Wireshark

---

*NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim*
