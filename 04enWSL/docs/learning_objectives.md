# Learning Objectives Traceability Matrix — Week 4

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

## Physical Layer, Data Link Layer & Custom Protocols

This document maps each Learning Objective to its supporting artefacts, ensuring complete pedagogical coverage and facilitating targeted study.

**Kit Version:** 1.1.0  
**Last Verified:** 2026-01-24  
**Integrity Check:** `make verify-integrity`

---

## Bloom Taxonomy Distribution

| Level | Count | LO IDs | Verbs Used |
|-------|-------|--------|------------|
| Remember | 1 | LO1 | Recall, enumerate |
| Understand | 1 | LO2 | Explain, distinguish |
| Apply | 2 | LO3, LO4 | Implement, apply |
| Analyse | 1 | LO5 | Analyse, identify, diagnose |
| Evaluate | 1 | LO6 | Evaluate, compare |

---

## Complete Traceability Matrix

### LO1: Recall Physical Layer Functions (Remember)

> **Statement:** Recall the function of the Physical Layer and enumerate transmission media characteristics including attenuation, noise, crosstalk and dispersion.

| Artefact Type | Location | Content | Status |
|---------------|----------|---------|--------|
| Theory | `docs/theory_summary.md` § Physical Layer | Transmission media, line coding, modulation | ✅ |
| Theory | `README.md` § Theoretical Background | Physical Layer concepts overview | ✅ |
| Concept Analogy | `docs/concept_analogies.md` | Physical Layer as postal service analogy | ✅ |
| Glossary | `docs/glossary.md` | attenuation, crosstalk, dispersion, NRZ, Manchester | ✅ |
| Quiz | `formative/quiz.yaml` q01, q02, q03 | 3 remember-level questions | ✅ |

**Coverage:** 5/5 ✅ **Complete**

---

### LO2: Explain Text vs Binary Protocols (Understand)

> **Statement:** Explain the distinction between text and binary protocols, explaining the trade-offs in overhead, parsing complexity and human readability.

| Artefact Type | Location | Content | Status |
|---------------|----------|---------|--------|
| Theory | `docs/theory_summary.md` § Protocol Design | Text vs binary trade-offs | ✅ |
| Theory | `README.md` § Protocol Specification | TEXT and BINARY protocol specs | ✅ |
| Misconception | `docs/misconceptions.md` #7 | "Binary protocols are always faster" | ✅ |
| Peer Instruction | `docs/peer_instruction.md` Q5 | Overhead comparison question | ✅ |
| Code Tracing | `docs/code_tracing.md` T3 | Length-prefix framing trace | ✅ |
| Quiz | `formative/quiz.yaml` q04-q07 | 4 understand-level questions | ✅ |

**Coverage:** 6/6 ✅ **Complete**

---

### LO3: Implement Concurrent TCP Servers (Apply)

> **Statement:** Implement concurrent TCP servers utilising multi-threading and construct custom protocols with proper framing mechanisms.

| Artefact Type | Location | Content | Status |
|---------------|----------|---------|--------|
| Theory | `README.md` § Exercise 1 | Protocol specification, framing | ✅ |
| Lab Exercise | `src/exercises/ex_4_01_tcp_proto.py` | Scaffold with TODO markers | ✅ |
| Demo App | `src/apps/text_proto_server.py` | Reference implementation | ✅ |
| Demo App | `src/apps/text_proto_client.py` | Client for testing | ✅ |
| Test | `tests/test_exercises.py::TestTextProtocol` | 3 test cases | ✅ |
| Misconception | `docs/misconceptions.md` #1 | "TCP preserves message boundaries" | ✅ |
| Misconception | `docs/misconceptions.md` #2 | "Length-prefix works with any data" | ✅ |
| Parsons | `docs/parsons_problems.md` P2, P3 | recv_exact, parse framed message | ✅ |
| PCAP Sample | `pcap/week04_lo3_text_commands.pcap` | TEXT protocol session capture | ✅ |
| Quiz | `formative/quiz.yaml` q08, q12 | 2 apply-level questions | ✅ |

**Coverage:** 10/10 ✅ **Complete**

---

### LO4: Apply struct Module and CRC32 (Apply)

> **Statement:** Apply the `struct` module for binary serialisation and CRC32 checksums for integrity verification.

| Artefact Type | Location | Content | Status |
|---------------|----------|---------|--------|
| Theory | `README.md` § Exercise 2 | Binary protocol header spec | ✅ |
| Lab Exercise | `src/exercises/ex_4_02_udp_sensor.py` | UDP sensor protocol scaffold | ✅ |
| Demo App | `src/apps/binary_proto_server.py` | Binary server reference | ✅ |
| Demo App | `src/apps/binary_proto_client.py` | Binary client for testing | ✅ |
| Code Tracing | `docs/code_tracing.md` T1 | struct.pack byte order | ✅ |
| Code Tracing | `docs/code_tracing.md` T2 | CRC32 calculation | ✅ |
| Code Tracing | `docs/code_tracing.md` T4 | Binary header construction | ✅ |
| Test | `tests/test_exercises.py::TestCRC32` | CRC32 function tests | ✅ |
| Test | `tests/test_exercises.py::TestBinaryProtocol` | Binary protocol tests | ✅ |
| Misconception | `docs/misconceptions.md` #3 | "struct.pack is only for C" | ✅ |
| Misconception | `docs/misconceptions.md` #4 | "Endianness interchangeable" | ✅ |
| Misconception | `docs/misconceptions.md` #5 | "CRC guarantees integrity" | ✅ |
| Misconception | `docs/misconceptions.md` #6 | "CRC32 = checksum" | ✅ |
| Parsons | `docs/parsons_problems.md` P1, P4, P5 | Header build, CRC verify, UDP packet | ✅ |
| PCAP Sample | `pcap/week04_lo4_binary_header.pcap` | BINARY protocol with CRC verification | ✅ |
| Quiz | `formative/quiz.yaml` q09, q10, q11 | 3 apply-level questions | ✅ |

**Coverage:** 16/16 ✅ **Complete**

---

### LO5: Analyse Captured Network Traffic (Analyse)

> **Statement:** Analyse captured network traffic using tcpdump and Wireshark to identify protocol overhead and diagnose communication anomalies.

| Artefact Type | Location | Content | Status |
|---------------|----------|---------|--------|
| Theory | `README.md` § Wireshark Setup | Interface selection, filters | ✅ |
| Theory | `README.md` § Traffic Analysis Tips | Frame inspection, hex dump | ✅ |
| Lab Exercise | `README.md` § Exercise 4 | Protocol overhead analysis | ✅ |
| Capture Script | `scripts/capture_traffic.py` | Automated packet capture | ✅ |
| PCAP Instructions | `pcap/README.md` | Capture procedures | ✅ |
| PCAP Sample | `pcap/week04_lo5_tcp_handshake.pcap` | Clean TCP 3-way handshake | ✅ |
| PCAP Sample | `pcap/week04_lo5_udp_sensor.pcap` | UDP sensor datagrams | ✅ |
| Peer Instruction | `docs/peer_instruction.md` Q1 | TCP boundary analysis | ✅ |
| Quiz | `formative/quiz.yaml` q13, q14 | 2 analyse-level questions | ✅ |

**Coverage:** 9/9 ✅ **Complete**

---

### LO6: Evaluate Protocol Efficiency (Evaluate)

> **Statement:** Evaluate the efficiency of different protocol designs by comparing overhead ratios and parsing complexity.

| Artefact Type | Location | Content | Status |
|---------------|----------|---------|--------|
| Theory | `README.md` § Exercise 4 | Analysis questions | ✅ |
| Peer Instruction | `docs/peer_instruction.md` Q5 | Binary vs text overhead | ✅ |
| Misconception | `docs/misconceptions.md` #7 | "Binary always better" | ✅ |
| Homework | `homework/exercises/hw_4_01_*.py` | Enhanced protocol design | ✅ |
| Homework | `homework/exercises/hw_4_02_*.py` | Reliable UDP design | ✅ |
| Quiz | `formative/quiz.yaml` q15 | 1 evaluate-level question | ✅ |

**Coverage:** 6/6 ✅ **Complete**

---

## Summary Table

| LO | Bloom Level | Artefact Count | Coverage | Status |
|----|-------------|----------------|----------|--------|
| LO1 | Remember | 5 | 5/5 (100%) | ✅ Complete |
| LO2 | Understand | 6 | 6/6 (100%) | ✅ Complete |
| LO3 | Apply | 10 | 10/10 (100%) | ✅ Complete |
| LO4 | Apply | 16 | 16/16 (100%) | ✅ Complete |
| LO5 | Analyse | 9 | 9/9 (100%) | ✅ Complete |
| LO6 | Evaluate | 6 | 6/6 (100%) | ✅ Complete |
| **Total** | — | **52** | **52/52 (100%)** | ✅ |

---

## Cross-Reference Index

### By Document Type

| Document | LOs Covered | Primary Purpose |
|----------|-------------|-----------------|
| `README.md` | All (LO1-LO6) | Entry point, exercises, theory overview |
| `docs/theory_summary.md` | LO1, LO2 | Theoretical foundations |
| `docs/misconceptions.md` | LO2, LO3, LO4, LO6 | Error prevention |
| `docs/peer_instruction.md` | LO2, LO5, LO6 | Active learning |
| `docs/code_tracing.md` | LO2, LO4 | Mental execution practice |
| `docs/parsons_problems.md` | LO3, LO4 | Code ordering practice |
| `formative/quiz.yaml` | All (LO1-LO6) | Self-assessment |
| `src/exercises/*.py` | LO3, LO4 | Hands-on implementation |
| `homework/exercises/*.py` | LO3, LO4, LO6 | Extended practice |
| `pcap/*.pcap` | LO3, LO4, LO5 | Traffic analysis practice |

### By Bloom Level

| Level | Documents |
|-------|-----------|
| Remember | theory_summary, glossary, quiz (q01-q03) |
| Understand | misconceptions, peer_instruction, quiz (q04-q07) |
| Apply | exercises, parsons_problems, code_tracing, pcap samples, quiz (q08-q12) |
| Analyse | pcap/, capture_traffic.py, peer_instruction, quiz (q13-q14) |
| Evaluate | homework/, peer_instruction Q5, quiz (q15) |

### PCAP Sample Index

| File | Size | Packets | LO Coverage | Wireshark Filter |
|------|------|---------|-------------|------------------|
| `week04_lo3_text_commands.pcap` | ~5KB | 25+ | LO3 | `tcp.port == 5400` |
| `week04_lo4_binary_header.pcap` | ~3KB | 18+ | LO4 | `tcp.port == 5401` |
| `week04_lo5_tcp_handshake.pcap` | ~2KB | 12+ | LO5 | `tcp.flags.syn == 1` |
| `week04_lo5_udp_sensor.pcap` | ~4KB | 30+ | LO5 | `udp.port == 5402` |

---

## Recommended Study Path

### For Students Struggling with Physical Layer (LO1)

1. Read `docs/concept_analogies.md` § Physical Layer
2. Study `docs/glossary.md` terms: attenuation, crosstalk, NRZ, Manchester
3. Review `docs/theory_summary.md` § Physical Layer
4. Take quiz: `python formative/run_quiz.py --lo LO1`

### For Students Struggling with Protocol Design (LO2, LO6)

1. Read `docs/misconceptions.md` #7 ("Binary always better")
2. Study `docs/peer_instruction.md` Q5
3. Complete `docs/code_tracing.md` T3
4. Take quiz: `python formative/run_quiz.py --lo LO2 LO6`

### For Students Struggling with Implementation (LO3, LO4)

1. Complete `docs/parsons_problems.md` P1-P5
2. Trace through `docs/code_tracing.md` T1, T2, T4
3. Study `docs/misconceptions.md` #1-#6
4. Implement `src/exercises/ex_4_01_tcp_proto.py`
5. Take quiz: `python formative/run_quiz.py --lo LO3 LO4 --bloom apply`

### For Students Struggling with Analysis (LO5)

1. Review `README.md` § Wireshark Setup
2. Open PCAP samples in `pcap/` with Wireshark
3. Study `docs/peer_instruction.md` Q1
4. Run Exercise 4 and capture own traffic
5. Take quiz: `python formative/run_quiz.py --lo LO5`

---

## Verification

Run `make verify-integrity` to confirm all artefacts exist:

```bash
$ make verify-integrity
✓ All 52 artefacts verified
✓ All PCAP samples present and valid
✓ Quiz covers all 6 Learning Objectives
✓ Kit integrity check passed
```

---

## Action Items for Instructors

- [x] Generate and commit PCAP samples for LO5
- [x] Add PCAP samples for LO3 and LO4
- [x] Create integrity verification script
- [ ] Update quiz questions based on common errors observed
- [ ] Add peer instruction questions for LO1 if needed
- [ ] Review homework submissions for LO6 coverage

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
*Week 4: Physical Layer, Data Link Layer & Custom Protocols*
*Version 1.1.0 — Last updated: 2026-01-24*
