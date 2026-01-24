# Learning Objectives Traceability Matrix — Week 5

> Computer Networks Laboratory — ASE-CSIE Bucharest
>
> IP Addressing, Subnetting and VLSM

This document provides complete traceability from Learning Objectives to all course artefacts.

---

## Quick Navigation

| LO | Description | Bloom | Coverage |
|----|-------------|-------|----------|
| LO1 | Identify network layer role | L1-L2 | ✅ Complete |
| LO2 | Explain IPv4/IPv6 addressing | L2 | ✅ Complete |
| LO3 | Calculate network parameters | L3 | ✅ Complete |
| LO4 | Apply FLSM subnetting | L3 | ✅ Complete |
| LO5 | Design VLSM schemes | L5-L6 | ✅ Complete |
| LO6 | Evaluate addressing efficiency | L5 | ✅ Complete |

---

## Traceability Matrix Summary

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    LEARNING OBJECTIVES COVERAGE MATRIX                          │
├─────┬────────┬─────────┬───────┬───────┬─────────────┬─────────┬───────┬───────┤
│ LO  │ Theory │ Lecture │ Lab   │ Quiz  │ Misconception│ Parsons │ Trace │ Test  │
├─────┼────────┼─────────┼───────┼───────┼─────────────┼─────────┼───────┼───────┤
│ LO1 │   ✅   │   ✅    │  ✅   │  ✅   │     ✅      │   ✅    │  ⚪   │  ⚪   │
│ LO2 │   ✅   │   ✅    │  ✅   │  ✅   │     ✅      │   ✅    │  ✅   │  ✅   │
│ LO3 │   ✅   │   ✅    │  ✅   │  ✅   │     ✅      │   ✅    │  ✅   │  ✅   │
│ LO4 │   ✅   │   ✅    │  ✅   │  ✅   │     ✅      │   ⚪    │  ✅   │  ✅   │
│ LO5 │   ✅   │   ✅    │  ✅   │  ✅   │     ✅      │   ✅    │  ✅   │  ✅   │
│ LO6 │   ✅   │   ⚪    │  ✅   │  ✅   │     ✅      │   ⚪    │  ⚪   │  ✅   │
└─────┴────────┴─────────┴───────┴───────┴─────────────┴─────────┴───────┴───────┘

Legend: ✅ = Covered | ⚪ = Not applicable/needed
```

---

## Quiz Questions by Learning Objective

| Question | LO | Bloom | Points | Type |
|----------|----|----|--------|------|
| q01 | LO1 | Remember | 1 | Multiple Choice |
| q02 | LO2 | Remember | 1 | Multiple Choice |
| q03 | LO3 | Understand | 2 | Multiple Choice |
| q04 | LO3 | Understand | 2 | Fill Blank |
| q05 | LO3 | Apply | 2 | Multiple Choice |
| q06 | LO4 | Apply | 2 | Multiple Choice |
| q07 | LO5 | Analyse | 3 | Multiple Choice |
| q08 | LO2 | Analyse | 3 | Multiple Choice |
| q09 | LO3 | Apply | 2 | Fill Blank |
| q10 | LO5 | Apply | 3 | Fill Blank |
| q11 | LO6 | Evaluate | 3 | Multiple Choice |
| q12 | LO5 | Create | 4 | Open Response |

**Total: 28 points across 12 questions**

---

## Quick Verification Commands

```bash
# Verify exercise files
python3 -m py_compile src/exercises/ex_5_01_cidr_flsm.py
python3 -m py_compile src/exercises/ex_5_02_vlsm_ipv6.py

# Verify tests pass
python3 tests/smoke_test.py

# Verify quiz YAML
python3 -c "import yaml; yaml.safe_load(open('formative/quiz.yaml'))"

# Run formative quiz
python3 formative/run_quiz.py --limit 3

# Export quiz to LMS format
python3 formative/export_to_lms.py --format json --pretty
```

---

## References

- RFC 791 – Internet Protocol (IPv4)
- RFC 8200 – Internet Protocol Version 6 (IPv6)
- RFC 1918 – Address Allocation for Private Internets
- RFC 4291 – IP Version 6 Addressing Architecture
- RFC 5952 – A Recommendation for IPv6 Address Text Representation
- RFC 1878 – Variable Length Subnet Table For IPv4

---

*Week 5: IP Addressing, Subnetting and VLSM — Learning Objectives Traceability*
*Computer Networks Laboratory — ASE-CSIE Bucharest*
