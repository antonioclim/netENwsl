# 🎯 Learning Objectives Traceability — Week 12
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> **Topic:** Email Protocols and Remote Procedure Call  
> This document maps each Learning Objective to its supporting materials.

---

## Quick Reference Matrix

| LO | Description | Bloom | Theory | Lab | Test | Quiz | Misconception |
|----|-------------|-------|--------|-----|------|------|---------------|
| LO1 | Recall SMTP dialogues | Remember | ✅ | ✅ | ✅ | q1,q2,q10 | #1,#2,#3,#4 |
| LO2 | Explain RPC abstraction | Understand | ✅ | ✅ | ✅ | q3 | #5,#6 |
| LO3 | Implement SMTP/RPC | Apply | ✅ | ✅ | ✅ | — | — |
| LO4 | Demonstrate communication | Apply | ✅ | ✅ | ✅ | q8,q9 | — |
| LO5 | Analyse protocol differences | Analyse | ✅ | ✅ | ✅ | q4,q5 | #5,#7,#9 |
| LO6 | Compare serialisation | Analyse | ✅ | ✅ | — | — | #5,#9 |
| LO7 | Design protocol selection | Create | ✅ | ✅ | — | q6,q7 | #8 |
| LO8 | Evaluate RPC suitability | Evaluate | ✅ | ✅ | — | q6,q7 | #8 |

**Coverage: 100%** — All LOs have multiple supporting materials.

---

## Detailed LO Mapping

### LO1: Recall SMTP Dialogues

**Bloom Level:** Remember  
**Description:** Recall the structure of SMTP dialogues, including commands (HELO, MAIL FROM, RCPT TO, DATA) and response codes.

| Artefact Type | Location | Section/Item |
|---------------|----------|--------------|
| Theory | `docs/theory_summary.md` | SMTP Protocol section |
| Lab Exercise | `src/exercises/ex_12_01_explore_smtp.py` | Parts A, B, C |
| Test | `tests/test_exercises.py` | `TestExercise1SMTP` (5 tests) |
| Quiz | `formative/quiz.yaml` | q1, q2, q10 |
| Misconception | `docs/misconceptions.md` | #1, #2, #3, #4 |
| Parsons | `docs/parsons_problems.md` | P1: SMTP Client Dialogue |
| Code Tracing | `docs/code_tracing.md` | T1: SMTP State Machine |
| Peer Instruction | `docs/peer_instruction.md` | Q1: Response Codes |

**Artefact Count: 8/8** ✅

---

### LO2: Explain RPC Abstraction

**Bloom Level:** Understand  
**Description:** Explain the RPC abstraction and articulate the roles of client stubs, server stubs and serialisation layers.

| Artefact Type | Location | Section/Item |
|---------------|----------|--------------|
| Theory | `docs/theory_summary.md` | RPC Architecture section |
| Lab Exercise | `src/exercises/ex_12_02_compare_rpc.py` | Part A: RPC Basics |
| Test | `tests/test_exercises.py` | `TestExercise2JSONRPC` |
| Quiz | `formative/quiz.yaml` | q3 |
| Misconception | `docs/misconceptions.md` | #5, #6 |
| Glossary | `docs/glossary.md` | Client stub, Server stub, Marshalling |
| Peer Instruction | `docs/peer_instruction.md` | Q2: JSON-RPC vs REST |

**Artefact Count: 7/8** ✅

---

### LO3: Implement SMTP/RPC

**Bloom Level:** Apply  
**Description:** Implement educational SMTP servers and RPC endpoints using Python's standard library and third-party frameworks.

| Artefact Type | Location | Section/Item |
|---------------|----------|--------------|
| Theory | `docs/commands_cheatsheet.md` | Implementation commands |
| Lab Exercise | `src/exercises/ex_12_01_explore_smtp.py` | Server implementation |
| Lab Exercise | `src/exercises/ex_12_02_compare_rpc.py` | RPC client implementation |
| Test | `tests/test_exercises.py` | Integration tests |
| Source Code | `src/apps/email/smtp_server.py` | Reference implementation |
| Source Code | `src/apps/rpc/jsonrpc/jsonrpc_server.py` | Reference implementation |
| Homework | `homework/exercises/hw_12_01_smtp_client.py` | SMTP client scaffold |

**Artefact Count: 7/8** ✅

---

### LO4: Demonstrate Communication

**Bloom Level:** Apply  
**Description:** Demonstrate client-server communication using netcat, curl and programmatic clients.

| Artefact Type | Location | Section/Item |
|---------------|----------|--------------|
| Theory | `docs/commands_cheatsheet.md` | netcat, curl commands |
| Lab Exercise | `src/exercises/ex_12_01_explore_smtp.py` | Part B: Manual dialogue |
| Demo Script | `scripts/run_demo.py` | smtp, rpc demos |
| Test | `tests/smoke_test.py` | Service connectivity |
| Quiz | `formative/quiz.yaml` | q8, q9 (port numbers) |
| Pair Programming | `docs/pair_programming_guide.md` | P1, P2 exercises |

**Artefact Count: 6/8** ✅

---

### LO5: Analyse Protocol Differences

**Bloom Level:** Analyse  
**Description:** Analyse protocol differences between JSON-RPC, XML-RPC and gRPC by examining packet captures and payload structures.

| Artefact Type | Location | Section/Item |
|---------------|----------|--------------|
| Theory | `docs/theory_summary.md` | Protocol comparison table |
| Lab Exercise | `src/exercises/ex_12_02_compare_rpc.py` | Parts B, C, D |
| Test | `tests/test_exercises.py` | `TestExercise2JSONRPC`, `TestExercise3XMLRPC` |
| Quiz | `formative/quiz.yaml` | q4, q5 |
| Misconception | `docs/misconceptions.md` | #5, #7, #9 |
| Peer Instruction | `docs/peer_instruction.md` | Q3: gRPC Serialisation |
| PCAP Guide | `pcap/README.md` | Capture instructions |

**Artefact Count: 7/8** ✅

---

### LO6: Compare Serialisation

**Bloom Level:** Analyse  
**Description:** Compare serialisation overhead and latency characteristics through controlled benchmarks.

| Artefact Type | Location | Section/Item |
|---------------|----------|--------------|
| Theory | `docs/theory_summary.md` | Serialisation comparison |
| Lab Exercise | `src/apps/rpc/benchmark_rpc.py` | Benchmark script |
| Misconception | `docs/misconceptions.md` | #5, #9 |
| Parsons | `docs/parsons_problems.md` | P5: RPC Benchmark |
| Code Tracing | `docs/code_tracing.md` | T3: Protobuf Encoding |
| Homework | `homework/exercises/hw_12_02_rpc_comparison.py` | Benchmark analysis |

**Artefact Count: 6/8** ✅

---

### LO7: Design Protocol Selection

**Bloom Level:** Create  
**Description:** Design appropriate protocol selections for given distributed system requirements.

| Artefact Type | Location | Section/Item |
|---------------|----------|--------------|
| Theory | `README.md` | Protocol Selection Guidelines table |
| Quiz | `formative/quiz.yaml` | q6 (mobile banking), q7 (legacy) |
| Misconception | `docs/misconceptions.md` | #8 (XML-RPC not obsolete) |
| Homework | `homework/exercises/hw_12_02_rpc_comparison.py` | Selection justification |
| Peer Instruction | `docs/peer_instruction.md` | Q2: Architectural differences |

**Artefact Count: 5/8** ✅

---

### LO8: Evaluate RPC Suitability

**Bloom Level:** Evaluate  
**Description:** Evaluate the suitability of different RPC frameworks for microservices, public APIs and legacy integrations.

| Artefact Type | Location | Section/Item |
|---------------|----------|--------------|
| Theory | `docs/theory_summary.md` | Use case recommendations |
| Quiz | `formative/quiz.yaml` | q6, q7 |
| Misconception | `docs/misconceptions.md` | #8 |
| Homework | `homework/exercises/hw_12_02_rpc_comparison.py` | Evaluation criteria |
| Peer Instruction | `docs/peer_instruction.md` | Q5: Error Handling |

**Artefact Count: 5/8** ✅

---

## Protocol Selection Decision Framework

Use this framework when answering LO7/LO8 questions:

| Requirement | Recommended | Rationale |
|-------------|-------------|-----------|
| Public REST-like API | JSON-RPC | Human-readable, easy debugging |
| Browser/JavaScript clients | JSON-RPC | Native JSON support |
| Internal microservices | gRPC | Performance, streaming, contracts |
| Legacy system integration | XML-RPC | 20+ years of compatibility |
| Mobile with bandwidth limits | gRPC | Protobuf binary efficiency |
| Real-time bidirectional | gRPC | HTTP/2 streaming |
| Blockchain/cryptocurrency | JSON-RPC | Industry standard |

---

## Self-Assessment Checklist

Before completing Week 12, verify you can:

- [ ] Write SMTP commands in correct sequence without notes
- [ ] Explain why DATA returns 354, not 250
- [ ] Construct a valid JSON-RPC request manually
- [ ] Explain the difference between HTTP errors and RPC errors
- [ ] Justify protocol choice for a given scenario
- [ ] Pass the formative quiz with ≥70%

---

## Cross-References

- `docs/misconceptions.md` — Detailed error explanations
- `docs/peer_instruction.md` — MCQ questions for discussion
- `docs/parsons_problems.md` — Code ordering exercises
- `docs/code_tracing.md` — Execution trace exercises
- `formative/quiz.yaml` — Self-assessment quiz

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
