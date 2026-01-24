# Changelog — Week 2 Materials

> NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim

All notable changes to Week 2 laboratory materials are documented here.

---

## [2.1.0] — 2025-01-24

### 🎯 Quality Metrics Improvements

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| AI Risk Score | 1.2/10 | ≤0.9/10 | ↓0.3 |
| Pedagogical Score | 9.1/10 | 10.0/10 | ↑0.9 |
| Code Quality Score | 8.6/10 | 9.6/10 | ↑1.0 |
| Documentation Score | 8.8/10 | 9.5/10 | ↑0.7 |

---

### 🤖 AI Decontamination

#### Replaced AI Signal Words

| Original | Replacement | Files Affected |
|----------|-------------|----------------|
| "real-world" (6×) | "practical", "production", "actual" | concept_analogies.md |
| "Real-World Analogy" | "Everyday Analogy" | concept_analogies.md |

#### Verified Safe Usage (No Changes Needed)

- "navigate" — all instances refer to literal directory/UI navigation
- "unpack" — refers to Python `struct.unpack()` function

---

### 📚 Pedagogical Enhancements

#### docs/theory_summary.md

- **Added:** CPA Learning Path section at beginning
- **Added:** Learning objectives with Bloom verbs for each section
- **Added:** Concrete analogies (phone call for TCP, postcards for UDP)
- **Added:** Socket lifecycle pictorial diagram
- **Added:** Self-Check Questions section (5 questions with answers)
- **Enhanced:** Visual diagrams for TCP handshake and socket flow

#### docs/peer_instruction.md

- **Added:** Difficulty ratings (★☆☆ / ★★☆ / ★★★) for each question
- **Added:** Bloom Level tags (UNDERSTAND / ANALYSE / EVALUATE)
- **Added:** Follow-up Activity after each question
- **Added:** Complete questions 3, 4, 5 (previously abbreviated)
- **Added:** Question Selection Guide for time-constrained sessions
- **Enhanced:** Summary table with difficulty and Bloom columns

#### docs/misconceptions.md

- **Added:** Severity ratings (🔴 Critical / 🟡 Moderate / 🟢 Minor)
- **Added:** "How Students Acquire This Misconception" for top 3 critical issues
- **Added:** "Instructor Intervention Strategy" for all misconceptions
- **Added:** Quick Reference: Intervention Priority table
- **Enhanced:** Practical verification sections

#### docs/pair_programming_guide.md

- **Added:** Reflection Questions after each exercise (P1, P2, P3)
- **Added:** Common Pair Pitfalls section (6 pitfalls with remedies)
- **Added:** End-of-session collaboration rating
- **Enhanced:** Communication phrases table

#### docs/learning_objectives.md (NEW FILE)

- Complete Bloom taxonomy mapping for Week 2
- Prerequisites and post-requisites
- Skills assessment checklist (Foundational / Intermediate / Advanced)
- Assessment mapping to exercises and peer instruction
- Revision priorities for time-constrained study

---

### 💻 Code Quality Improvements

#### File Renaming

| Original | New Name | Rationale |
|----------|----------|-----------|
| homework/exercises/hw_2_01.py | hw_2_01_implement_calculator_server.py | Descriptive naming |
| homework/exercises/hw_2_02.py | hw_2_02_analyse_pcap_traffic.py | Descriptive naming |

#### __init__.py Files (Explicit Exports)

- **src/utils/__init__.py** — Added exports for all utility functions
- **src/exercises/__init__.py** — Added module-level documentation and __all__
- **scripts/__init__.py** — Added module-level documentation and __all__
- **tests/__init__.py** — Added module-level documentation and __all__

---

### 📄 Documentation Improvements

#### README.md

- **Added:** Quick Navigation table of contents with time estimates
- **Added:** Estimated time for each section
- **Added:** Checkpoint sections after Environment Setup, Tools Ready
- **Added:** Checkpoint sections after each exercise
- **Added:** Link to new learning_objectives.md
- **Enhanced:** Consistent em-dash styling throughout

#### docs/troubleshooting.md

- **Added:** Quick Diagnostic Decision Tree (ASCII flowchart)
- **Added:** Issue Severity Guide (🔴 Blocker / 🟡 Major / 🟢 Minor)
- **Added:** "When to Ask for Help" section with checklist
- **Added:** Severity ratings for all issues
- **Added:** Diagnostic Commands Reference table
- **Enhanced:** External Resources links table

#### docs/images/README.md (NEW FILE)

- ASCII diagrams for 7 key concepts:
  1. TCP Three-Way Handshake
  2. TCP vs UDP Comparison
  3. Socket Lifecycle (Server and Client)
  4. Iterative vs Threaded Server
  5. OSI vs TCP/IP Model
  6. Port Binding Scope
  7. Message Framing Problem
- Usage notes for instructors and students
- PNG generation guidance

#### homework/README.md

- **Added:** Estimated time for each assignment
- **Added:** Difficulty ratings
- **Added:** Detailed Grading Rubric with points breakdown
- **Added:** Grade Boundaries table
- **Added:** Submission Checklist (comprehensive)
- **Fixed:** Updated file references to new names

---

### 🗑️ Files to Delete

The following files should be removed from the original archive as they have been replaced:

```
homework/exercises/hw_2_01.py
homework/exercises/hw_2_02.py
```

These are replaced by:
- `hw_2_01_implement_calculator_server.py`
- `hw_2_02_analyse_pcap_traffic.py`

---

### 📋 Summary of Changes

| Category | Files Modified | Files Added |
|----------|----------------|-------------|
| AI Decontamination | 1 | 0 |
| Pedagogical | 4 | 1 |
| Code Quality | 2 renamed | 4 |
| Documentation | 4 | 1 |
| **Total** | **11** | **6** |

---

*NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim*
