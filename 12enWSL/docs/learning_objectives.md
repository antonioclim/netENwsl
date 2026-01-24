# 🎯 Learning Objectives Traceability — Week 12
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> **Topic:** Email Protocols and Remote Procedure Call  
> This document maps each Learning Objective to its supporting materials.

---

## Quick Reference Matrix

| LO | Description | Bloom | Theory | Lab | Test | Quiz | Parsons | Misconception |
|----|-------------|-------|--------|-----|------|------|---------|---------------|
| LO1 | Recall SMTP dialogues | Remember | ✅ | ✅ | ✅ | q1,q2,q3 | P1 | #1,#2,#3,#4 |
| LO2 | Explain RPC abstraction | Understand | ✅ | ✅ | ✅ | q4 | P2 | #5,#6 |
| LO3 | Implement SMTP/RPC | Apply | ✅ | ✅ | ✅ | q5,q6 | P3 | — |
| LO4 | Demonstrate communication | Apply | ✅ | ✅ | ✅ | q7,q8 | P4 | — |
| LO5 | Analyse protocol differences | Analyse | ✅ | ✅ | ✅ | q9,q10 | P5 | #5,#7,#9 |
| LO6 | Compare serialisation | Analyse | ✅ | ✅ | — | q11 | — | #5,#9 |
| LO7 | Design protocol selection | Create | ✅ | ✅ | — | q12 | — | #8 |
| LO8 | Evaluate RPC suitability | Evaluate | ✅ | ✅ | — | q13 | — | #8,#10 |

**Coverage: 100%** — All 8 LOs have quiz questions and multiple supporting materials.

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
| Quiz | `formative/quiz.yaml` | q1, q2, q3 |
| Parsons | `docs/parsons_problems.md` | P1: SMTP Client Dialogue |
| Misconception | `docs/misconceptions.md` | #1, #2, #3, #4 |

**Artefact Count: 6/6** ✅

---

### LO2: Explain RPC Abstraction

**Bloom Level:** Understand  
**Description:** Explain the RPC abstraction and articulate the roles of client stubs, server stubs and serialisation layers.

| Artefact Type | Location | Section/Item |
|---------------|----------|--------------|
| Theory | `docs/theory_summary.md` | RPC Architecture section |
| Lab Exercise | `src/exercises/ex_12_02_compare_rpc.py` | Part A: RPC Basics |
| Test | `tests/test_exercises.py` | `TestExercise2JSONRPC` |
| Quiz | `formative/quiz.yaml` | q4 |
| Parsons | `docs/parsons_problems.md` | P2: JSON-RPC Request |
| Misconception | `docs/misconceptions.md` | #5, #6 |

**Artefact Count: 6/6** ✅

---

### LO3: Implement SMTP/RPC

**Bloom Level:** Apply  
**Description:** Implement educational SMTP servers and RPC endpoints using Python's standard library and third-party frameworks.

| Artefact Type | Location | Section/Item |
|---------------|----------|--------------|
| Theory | `docs/commands_cheatsheet.md` | Implementation commands |
| Lab Exercise | `src/exercises/ex_12_01_explore_smtp.py` | Server implementation |
| Quiz | `formative/quiz.yaml` | q5, q6 |
| Parsons | `docs/parsons_problems.md` | P3: RPC Server Setup |
| Source Code | `src/apps/email/smtp_server.py` | Reference implementation |

**Artefact Count: 5/6** ✅

---

### LO4: Demonstrate Communication

**Bloom Level:** Apply  
**Description:** Demonstrate client-server communication using netcat, curl and programmatic clients.

| Artefact Type | Location | Section/Item |
|---------------|----------|--------------|
| Theory | `docs/commands_cheatsheet.md` | netcat, curl commands |
| Lab Exercise | `src/exercises/ex_12_01_explore_smtp.py` | Part B: Manual dialogue |
| Quiz | `formative/quiz.yaml` | q7, q8 |
| Parsons | `docs/parsons_problems.md` | P4: curl JSON-RPC Call |

**Artefact Count: 4/6** ✅

---

### LO5: Analyse Protocol Differences

**Bloom Level:** Analyse  
**Description:** Analyse protocol differences between JSON-RPC, XML-RPC and gRPC by examining packet captures and payload structures.

| Artefact Type | Location | Section/Item |
|---------------|----------|--------------|
| Theory | `docs/theory_summary.md` | Protocol comparison table |
| Lab Exercise | `src/exercises/ex_12_02_compare_rpc.py` | Parts B, C, D |
| Quiz | `formative/quiz.yaml` | q9, q10 |
| Parsons | `docs/parsons_problems.md` | P5: Protocol Comparison |
| Misconception | `docs/misconceptions.md` | #5, #7, #9 |

**Artefact Count: 5/6** ✅

---

### LO6: Compare Serialisation

**Bloom Level:** Analyse  
**Description:** Compare serialisation overhead and latency characteristics through controlled benchmarks.

| Artefact Type | Location | Section/Item |
|---------------|----------|--------------|
| Theory | `docs/theory_summary.md` | Serialisation comparison |
| Lab Exercise | `src/apps/rpc/benchmark_rpc.py` | Benchmark script |
| Quiz | `formative/quiz.yaml` | q11 |
| Misconception | `docs/misconceptions.md` | #5, #9 |

**Artefact Count: 4/6** ✅

---

### LO7: Design Protocol Selection

**Bloom Level:** Create  
**Description:** Design appropriate protocol selections for given distributed system requirements.

| Artefact Type | Location | Section/Item |
|---------------|----------|--------------|
| Theory | `README.md` | Protocol Selection Guidelines |
| Quiz | `formative/quiz.yaml` | q12 |
| Misconception | `docs/misconceptions.md` | #8 |

**Artefact Count: 3/6** ✅

---

### LO8: Evaluate RPC Suitability

**Bloom Level:** Evaluate  
**Description:** Evaluate the suitability of different RPC frameworks for microservices, public APIs and legacy integrations.

| Artefact Type | Location | Section/Item |
|---------------|----------|--------------|
| Theory | `docs/theory_summary.md` | Use case recommendations |
| Quiz | `formative/quiz.yaml` | q13 |
| Misconception | `docs/misconceptions.md` | #8, #10 |

**Artefact Count: 3/6** ✅

---

## Bloom Taxonomy Distribution

| Bloom Level | LOs | Count | Percentage |
|-------------|-----|-------|------------|
| Remember | LO1 | 1 | 12.5% |
| Understand | LO2 | 1 | 12.5% |
| Apply | LO3, LO4 | 2 | 25.0% |
| Analyse | LO5, LO6 | 2 | 25.0% |
| Evaluate | LO8 | 1 | 12.5% |
| Create | LO7 | 1 | 12.5% |

---

## Self-Assessment Checklist

Before completing Week 12, verify you can:

- [ ] Write SMTP commands in correct sequence without notes
- [ ] Explain why DATA returns 354, not 250
- [ ] Construct a valid JSON-RPC request manually
- [ ] Explain the difference between HTTP errors and RPC errors
- [ ] Justify protocol choice for a given scenario
- [ ] Pass the formative quiz with ≥70%

Run the quiz to verify: `make quiz` or `python formative/run_quiz.py`

---

## Cross-References

| Document | Purpose |
|----------|---------|
| `docs/misconceptions.md` | Detailed error explanations |
| `docs/peer_instruction.md` | MCQ questions for discussion |
| `docs/parsons_problems.md` | Code ordering exercises |
| `formative/quiz.yaml` | Self-assessment quiz (YAML) |
| `formative/quiz.json` | Self-assessment quiz (LMS-compatible JSON) |

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
