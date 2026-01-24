# 📊 Learning Objectives Traceability Matrix — Week 5
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> IP Addressing, Subnetting and VLSM

This document provides complete traceability from Learning Objectives to all course artefacts, ensuring comprehensive coverage and alignment with assessment.

---

## Quick Navigation

| LO | Description | Coverage |
|----|-------------|----------|
| [LO1](#lo1-network-layer-identification) | Identify network layer role | ✅ Complete |
| [LO2](#lo2-ipv4ipv6-addressing) | Explain IPv4/IPv6 addressing | ✅ Complete |
| [LO3](#lo3-cidr-calculations) | Calculate network parameters | ✅ Complete |
| [LO4](#lo4-flsm-subnetting) | Apply FLSM subnetting | ✅ Complete |
| [LO5](#lo5-vlsm-design) | Design VLSM schemes | ✅ Complete |
| [LO6](#lo6-evaluation) | Evaluate addressing efficiency | ✅ Complete |

---

## LO Definitions (Bloom Taxonomy Aligned)

### LO1: Network Layer Identification
**Bloom Level**: Remember / Understand (L1-L2)

> **Objective**: Identify the role and functions of the network layer within the OSI and TCP/IP reference models

| Artefact Type | Path | Section/Function | Status |
|--------------|------|------------------|--------|
| **Theory** | `docs/theory_summary.md` | "Network Layer Functions" | ✅ |
| **Lecture** | `../00LECTURES/S5Theory_Week5_EN.html` | Slides 5-12 | ✅ |
| **Lab Exercise** | `src/exercises/ex_5_01_cidr_flsm.py` | `cmd_analyze()` | ✅ |
| **Quiz** | `formative/quiz.yaml` | q01 | ✅ |
| **Misconception** | `docs/misconceptions.md` | N/A (no specific misconception) | ⚪ |
| **Peer Instruction** | `docs/peer_instruction.md` | Q2 (network address) | ✅ |
| **Glossary** | `docs/glossary.md` | "Network Layer", "Routing" | ✅ |

**Assessment Methods**:
- Quiz: Multiple choice (q01)
- Peer Instruction: Q2 discussion

---

### LO2: IPv4/IPv6 Addressing
**Bloom Level**: Understand (L2)

> **Objective**: Explain the structural differences between IPv4 and IPv6 header formats and addressing schemes

| Artefact Type | Path | Section/Function | Status |
|--------------|------|------------------|--------|
| **Theory** | `docs/theory_summary.md` | "IPv4 vs IPv6" | ✅ |
| **Lecture** | `../00LECTURES/S5Theory_Week5_EN.html` | Slides 15-28 | ✅ |
| **Lab Exercise** | `src/exercises/ex_5_02_vlsm_ipv6.py` | `cmd_ipv6()` | ✅ |
| **Quiz** | `formative/quiz.yaml` | q02, q08 | ✅ |
| **Misconception** | `docs/misconceptions.md` | #8 (:: usage), #9 (NAT), #10 (link-local) | ✅ |
| **Peer Instruction** | `docs/peer_instruction.md` | Q4 (IPv6 compression) | ✅ |
| **Code Tracing** | `docs/code_tracing.md` | T4 (IPv6 compression logic) | ✅ |
| **Parsons** | `docs/parsons_problems.md` | P4 (IPv6 expansion) | ✅ |
| **Glossary** | `docs/glossary.md` | "IPv4", "IPv6", "Link-local" | ✅ |

**Assessment Methods**:
- Quiz: q02 (IPv4 size), q08 (IPv6 validity)
- Code Tracing: T4
- Parsons: P4

**RFC References**:
- RFC 791 (IPv4)
- RFC 8200 (IPv6)
- RFC 5952 (IPv6 text representation)

---

### LO3: CIDR Calculations
**Bloom Level**: Apply (L3)

> **Objective**: Calculate network addresses, broadcast addresses and usable host ranges from CIDR notation

| Artefact Type | Path | Section/Function | Status |
|--------------|------|------------------|--------|
| **Theory** | `docs/theory_summary.md` | "CIDR Notation" | ✅ |
| **Lecture** | `../00LECTURES/S5Theory_Week5_EN.html` | Slides 30-45 | ✅ |
| **Lab Exercise** | `src/exercises/ex_5_01_cidr_flsm.py` | `cmd_analyze()`, `cmd_binary()` | ✅ |
| **Quiz** | `formative/quiz.yaml` | q03, q04, q05, q09 | ✅ |
| **Misconception** | `docs/misconceptions.md` | #1 (usable hosts), #2 (network addr), #3 (boundaries), #4 (broadcast) | ✅ |
| **Peer Instruction** | `docs/peer_instruction.md` | Q1, Q2, Q5 | ✅ |
| **Code Tracing** | `docs/code_tracing.md` | T1 (prefix calculation) | ✅ |
| **Parsons** | `docs/parsons_problems.md` | P1 (usable hosts), P2 (network address) | ✅ |
| **Troubleshooting** | `docs/troubleshooting.md` | "Subnetting Calculation Errors" | ✅ |
| **Homework** | `homework/exercises/hw_5_01_subnet_design.py` | Full implementation | ✅ |
| **Test** | `tests/test_exercises.py` | `TestCIDRAnalysis` | ✅ |

**Key Formulas** (RFC 791, RFC 1878):
```
Network Address = IP AND Subnet Mask
Broadcast Address = Network + 2^(32-prefix) - 1
Usable Hosts = 2^(32-prefix) - 2
```

**Verification Commands**:
```bash
python src/exercises/ex_5_01_cidr_flsm.py analyse 192.168.10.14/26 --verbose
python -c "print(2**(32-26) - 2)"  # Output: 62
```

---

### LO4: FLSM Subnetting
**Bloom Level**: Apply (L3)

> **Objective**: Apply FLSM subnetting to partition networks into equal-sized segments

| Artefact Type | Path | Section/Function | Status |
|--------------|------|------------------|--------|
| **Theory** | `docs/theory_summary.md` | "FLSM Subnetting" | ✅ |
| **Lecture** | `../00LECTURES/S5Theory_Week5_EN.html` | Slides 48-55 | ✅ |
| **Lab Exercise** | `src/exercises/ex_5_01_cidr_flsm.py` | `cmd_flsm()` | ✅ |
| **Quiz** | `formative/quiz.yaml` | q06 | ✅ |
| **Misconception** | `docs/misconceptions.md` | #5 (FLSM vs VLSM) | ✅ |
| **Peer Instruction** | `docs/peer_instruction.md` | Q3 (implicit in VLSM context) | ✅ |
| **Code Tracing** | `docs/code_tracing.md` | T2 (FLSM generation) | ✅ |
| **Test** | `tests/test_exercises.py` | `TestFLSM` | ✅ |

**Key Formula**:
```
new_prefix = original_prefix + ceil(log₂(num_subnets))
hosts_per_subnet = 2^(32 - new_prefix) - 2
```

**Verification Commands**:
```bash
python src/exercises/ex_5_01_cidr_flsm.py flsm 192.168.100.0/24 8 --json
```

---

### LO5: VLSM Design
**Bloom Level**: Create (L5)

> **Objective**: Design VLSM allocation schemes that optimise address space utilisation for varied requirements

| Artefact Type | Path | Section/Function | Status |
|--------------|------|------------------|--------|
| **Theory** | `docs/theory_summary.md` | "VLSM Allocation" | ✅ |
| **Lecture** | `../00LECTURES/S5Theory_Week5_EN.html` | Slides 58-72 | ✅ |
| **Lab Exercise** | `src/exercises/ex_5_02_vlsm_ipv6.py` | `cmd_vlsm()` | ✅ |
| **Quiz** | `formative/quiz.yaml` | q07, q10 | ✅ |
| **Misconception** | `docs/misconceptions.md` | #5 (efficiency), #6 (allocation order) | ✅ |
| **Peer Instruction** | `docs/peer_instruction.md` | Q3 (VLSM ordering) | ✅ |
| **Code Tracing** | `docs/code_tracing.md` | T3 (alignment), T5 (complete VLSM) | ✅ |
| **Parsons** | `docs/parsons_problems.md` | P3 (prefix calculator) | ✅ |
| **Homework** | `homework/exercises/hw_5_01_subnet_design.py` | VLSM implementation | ✅ |
| **Test** | `tests/test_exercises.py` | `TestVLSM` | ✅ |

**Key Algorithm** (RFC 1878):
```
1. Sort requirements largest-first
2. For each requirement:
   a. Calculate minimum prefix: 32 - ceil(log₂(hosts + 2))
   b. Align to block boundary
   c. Allocate subnet
   d. Advance cursor
```

**Verification Commands**:
```bash
python src/exercises/ex_5_02_vlsm_ipv6.py vlsm 10.0.0.0/24 100 50 20 2 --json
```

---

### LO6: Evaluation
**Bloom Level**: Evaluate (L5)

> **Objective**: Evaluate the efficiency and correctness of addressing schemes through programmatic validation

| Artefact Type | Path | Section/Function | Status |
|--------------|------|------------------|--------|
| **Theory** | `docs/theory_summary.md` | "Efficiency Metrics" | ✅ |
| **Lab Exercise** | `src/exercises/ex_5_02_vlsm_ipv6.py` | Efficiency output | ✅ |
| **Lab Exercise** | `src/exercises/ex_5_03_quiz_generator.py` | Self-assessment | ✅ |
| **Quiz** | `formative/quiz.yaml` | All questions (self-evaluation) | ✅ |
| **Misconception** | `docs/misconceptions.md` | All (error prevention) | ✅ |
| **Test** | `tests/test_exercises.py` | `test_vlsm_efficiency()` | ✅ |
| **Test** | `tests/smoke_test.py` | Complete validation | ✅ |

**Efficiency Formula**:
```
efficiency = (required_hosts / usable_hosts) × 100%
```

---

## Coverage Summary Matrix

| LO | Theory | Lecture | Lab | Quiz | Misconception | PI | Trace | Parsons | Test | Homework |
|----|--------|---------|-----|------|---------------|----|----|---------|------|----------|
| LO1 | ✅ | ✅ | ✅ | ✅ | ⚪ | ✅ | ⚪ | ⚪ | ⚪ | ⚪ |
| LO2 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| LO3 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| LO4 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ | ✅ | ⚪ |
| LO5 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| LO6 | ✅ | ⚪ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ✅ | ⚪ |

**Legend**: ✅ = Covered | ⚪ = Not applicable/needed

---

## Alignment with Bloom Taxonomy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  BLOOM LEVEL          │  LOs    │  ASSESSMENT TYPES                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  L6: Create           │  LO5    │  Homework (design), Project              │
│  L5: Evaluate         │  LO6    │  Test validation, Efficiency analysis    │
│  L4: Analyze          │  (q07,  │  Peer Instruction, Code Tracing          │
│                       │   q08)  │                                          │
│  L3: Apply            │  LO3,   │  Lab exercises, Quiz fill-blank,         │
│                       │  LO4    │  Homework calculations                   │
│  L2: Understand       │  LO1,   │  Quiz MC, Misconceptions review          │
│                       │  LO2    │                                          │
│  L1: Remember         │  (q01,  │  Quiz MC (definitions)                   │
│                       │   q02)  │                                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Quick Verification Commands

Test that all artefacts are accessible:

```bash
# Verify exercise files exist and are syntactically correct
python3 -m py_compile src/exercises/ex_5_01_cidr_flsm.py
python3 -m py_compile src/exercises/ex_5_02_vlsm_ipv6.py
python3 -m py_compile src/exercises/ex_5_03_quiz_generator.py

# Verify tests pass
python3 tests/smoke_test.py

# Verify quiz YAML is valid
python3 -c "import yaml; yaml.safe_load(open('formative/quiz.yaml'))"

# Verify documentation exists
ls -la docs/*.md

# Run formative quiz
python3 formative/run_quiz.py --limit 3
```

---

## References

- RFC 791 – Internet Protocol (IPv4)
- RFC 8200 – Internet Protocol, Version 6 (IPv6)
- RFC 1918 – Address Allocation for Private Internets
- RFC 4291 – IP Version 6 Addressing Architecture
- RFC 5952 – A Recommendation for IPv6 Address Text Representation
- RFC 1878 – Variable Length Subnet Table For IPv4
- RFC 3021 – Using 31-Bit Prefixes on Point-to-Point Links

---

*Week 5: IP Addressing, Subnetting, VLSM — Learning Objectives Traceability*
*Computer Networks Laboratory — ASE, CSIE Bucharest*
