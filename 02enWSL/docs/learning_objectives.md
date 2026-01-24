# Learning Objectives — Week 2: Architectural Models and Socket Programming

> NETWORKING class — ASE, CSIE Bucharest  
> Computer Networks Laboratory | by ing. dr. Antonio Clim

## Bloom Taxonomy Levels

| Level | Cognitive Process | Verbs |
|-------|-------------------|-------|
| 1. REMEMBER | Retrieve knowledge | Define, list, recall |
| 2. UNDERSTAND | Construct meaning | Explain, compare |
| 3. APPLY | Use in situations | Implement, execute |
| 4. ANALYSE | Break into parts | Debug, test, examine |
| 5. EVALUATE | Make judgements | Justify, recommend |
| 6. CREATE | Produce new work | Design, develop |

## Learning Objectives

### Level 1: REMEMBER
| ID | Objective |
|----|-----------|
| R1 | List the seven layers of the OSI model |
| R2 | Identify the four layers of TCP/IP |
| R3 | Recall socket types for TCP and UDP |
| R4 | State default ports for common services |
| R5 | Define: socket, port, handshake, datagram |

### Level 2: UNDERSTAND
| ID | Objective |
|----|-----------|
| U1 | Explain TCP vs UDP differences |
| U2 | Describe the TCP three-way handshake |
| U3 | Compare iterative vs concurrent servers |
| U4 | Classify applications by protocol |
| U5 | Interpret Wireshark TCP captures |
| U6 | Summarise why TCP lacks message boundaries |

### Level 3: APPLY
| ID | Objective |
|----|-----------|
| A1 | Implement a basic TCP echo server |
| A2 | Implement a basic UDP echo server |
| A3 | Use socket options (SO_REUSEADDR) |
| A4 | Execute Wireshark filters |
| A5 | Demonstrate concurrent handling with threading |
| A6 | Apply proper resource cleanup |

### Level 4: ANALYSE
| ID | Objective |
|----|-----------|
| N1 | Debug "Address already in use" errors |
| N2 | Examine Wireshark captures for issues |
| N3 | Differentiate bind addresses (127.0.0.1 vs 0.0.0.0) |
| N4 | Test server behaviour under load |
| N5 | Trace code execution to predict output |

### Level 5: EVALUATE
| ID | Objective |
|----|-----------|
| E1 | Justify protocol choice (TCP vs UDP) |
| E2 | Assess server architecture appropriateness |
| E3 | Critique code for error handling |
| E4 | Recommend server improvements |

### Level 6: CREATE
| ID | Objective |
|----|-----------|
| C1 | Design a simple application protocol |
| C2 | Develop a client-server application |
| C3 | Construct test cases |

## Traceability Matrix

| LO | Theory | Lab | Test | Quiz | PCAP | Misconception | Parsons |
|----|--------|-----|------|------|------|---------------|---------|
| R1 | ✅ theory | — | ✅ q01,q03 | ✅ | — | — | — |
| R3 | ✅ theory | ✅ ex_2_01 | ✅ q02 | ✅ | — | ✅ #1 | ✅ tcp_server |
| U1 | ✅ theory | ✅ both | ✅ q06,q08 | ✅ | — | ✅ #2,#8 | — |
| U2 | ✅ theory | ✅ Wireshark | ✅ q07,q09 | ✅ | ✅ tcp | ✅ #7 | — |
| A1 | ✅ docstring | ✅ ex_2_01 | ✅ test_tcp | ✅ q11,q12 | ✅ tcp | ✅ #3 | ✅ tcp_server |
| A2 | ✅ docstring | ✅ ex_2_02 | ✅ test_udp | — | ✅ udp | ✅ #2 | ✅ udp_client |
| A3 | ✅ comments | ✅ ex_2_01 | ✅ q10 | ✅ | — | ✅ #10 | — |
| A5 | ✅ docstring | ✅ ex_2_01 | ✅ load | — | ✅ multi | ✅ #4 | ✅ threaded |
| N1 | ✅ troubleshoot | ✅ peer Q3 | ✅ q13 | ✅ | — | — | — |
| N3 | ✅ misconceptions | ✅ peer Q3 | ✅ q14 | ✅ | — | ✅ #6 | — |
| E1 | ✅ peer Q5 | — | ✅ q15 | ✅ | — | ✅ #8 | — |

## Assessment Mapping

| Exercise | Primary Objectives | Bloom Levels |
|----------|-------------------|--------------|
| ex_2_01_tcp.py | A1, A3, A5, A6, N1 | APPLY, ANALYSE |
| ex_2_02_udp.py | A2, A6, U1 | APPLY, UNDERSTAND |
| Exercise 3 (capture) | A4, U5, N2 | APPLY, ANALYSE |

---

*NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim*
