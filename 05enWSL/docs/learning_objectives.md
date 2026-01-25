# Learning Objectives — Week 5

> Computer Networks Laboratory — ASE-CSIE Bucharest
>
> IP Addressing, Subnetting and VLSM

---

## Learning Objectives

| ID | Bloom Level | Objective |
|----|-------------|-----------|
| LO1 | Remember | **Identify** the role and functions of the network layer |
| LO2 | Understand | **Explain** IPv4 and IPv6 header formats and addressing schemes |
| LO3 | Apply | **Calculate** network addresses, broadcast addresses and host ranges |
| LO4 | Apply | **Apply** FLSM subnetting to partition networks |
| LO5 | Analyse | **Design** VLSM allocation schemes |
| LO6 | Evaluate | **Evaluate** efficiency of addressing schemes |

---

## LO Traceability Matrix

### Quiz Questions → LOs

| Question | LO | Bloom | Points | Topic |
|----------|-----|-------|--------|-------|
| q01 | LO1 | Remember | 1 | OSI Layer identification |
| q02 | LO2 | Remember | 1 | IPv4 address size |
| q03 | LO3 | Understand | 2 | Usable hosts explanation |
| q04 | LO3 | Understand | 2 | Broadcast calculation |
| q05 | LO3 | Apply | 2 | Network address calculation |
| q06 | LO4 | Apply | 2 | FLSM prefix calculation |
| q07 | LO5 | Analyse | 3 | VLSM allocation order |
| q08 | LO2 | Analyse | 3 | IPv6 validation |
| q09 | LO3 | Apply | 2 | Host count calculation |
| q10 | LO5 | Apply | 3 | Prefix for hosts |
| q11 | LO6 | Evaluate | 3 | VLSM efficiency |
| q12 | LO5 | Create | 4 | Complete VLSM design |

### LOs → Resources

| LO | Exercises | Docs | Quiz | Parsons |
|----|-----------|------|------|---------|
| LO1 | — | theory_summary.md, misconceptions.md#0 | q01 | — |
| LO2 | ex_5_02 | theory_summary.md | q02, q08 | P4 |
| LO3 | ex_5_01 | code_tracing.md | q03, q04, q05, q09 | P1, P3, P7 |
| LO4 | ex_5_01 | code_tracing.md | q06 | P8 |
| LO5 | ex_5_02 | misconceptions.md#5-6 | q07, q10, q12 | P2, P6 |
| LO6 | ex_5_02, hw_5_01 | theory_summary.md | q11 | — |

### Coverage Summary

| LO | Quiz Coverage | Exercise Coverage | Doc Coverage |
|----|---------------|-------------------|--------------|
| LO1 | ✅ 1 question | — | ✅ theory, misconceptions |
| LO2 | ✅ 2 questions | ✅ ex_5_02 | ✅ theory |
| LO3 | ✅ 4 questions | ✅ ex_5_01 | ✅ code_tracing |
| LO4 | ✅ 1 question | ✅ ex_5_01 | ✅ code_tracing |
| LO5 | ✅ 3 questions | ✅ ex_5_02 | ✅ misconceptions |
| LO6 | ✅ 1 question | ✅ hw_5_01 | ✅ theory |

**Total: 6/6 LOs fully covered**

---

## Bloom Taxonomy Distribution

| Level | Target | Actual | Questions |
|-------|--------|--------|-----------|
| Remember (L1) | 10-15% | 7% | q01, q02 |
| Understand (L2) | 20-25% | 14% | q03, q04 |
| Apply (L3) | 30-35% | 32% | q05, q06, q09, q10 |
| Analyse (L4) | 15-20% | 21% | q07, q08 |
| Evaluate (L5) | 5-10% | 11% | q11 |
| Create (L6) | 5-10% | 14% | q12 |

The distribution slightly exceeds upper-level targets, which is appropriate for a Week 5 topic building on earlier fundamentals.

---

## Assessment Alignment

### Formative Assessment
- **Quiz**: 12 questions, 28 points total
- **Parsons Problems**: 8 problems with distractors
- **Code Tracing**: 5 exercises in docs/code_tracing.md

### Exercise Alignment
| Exercise | Primary LOs | Bloom Levels |
|----------|-------------|--------------|
| ex_5_01_cidr_flsm.py | LO3, LO4 | Apply |
| ex_5_02_vlsm_ipv6.py | LO2, LO5, LO6 | Apply, Analyse |
| ex_5_03_quiz_generator.py | LO3, LO4 | Apply |

### Homework Alignment
| Homework | Primary LOs | Bloom Levels |
|----------|-------------|--------------|
| hw_5_01_subnet_design.py | LO4, LO5, LO6 | Apply, Analyse, Evaluate |
| hw_5_02_ipv6_transition.py | LO2 | Understand, Apply |

---

*Week 5: IP Addressing, Subnetting and VLSM — Learning Objectives*
*Computer Networks Laboratory — ASE-CSIE Bucharest*
