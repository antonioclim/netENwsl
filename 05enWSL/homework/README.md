# 📝 Homework — Week 5: IP Addressing and Subnetting

> Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

## Overview

This week's homework reinforces subnetting concepts and IPv6 transition planning through practical exercises.

## Assignments

| File | Topic | Difficulty | Est. Time |
|------|-------|------------|-----------|
| `hw_5_01_subnet_design.py` | VLSM Subnet Design for an Organisation | ⭐⭐ Intermediate | 60-90 min |
| `hw_5_02_ipv6_transition.py` | IPv6 Analysis and Transition Planning | ⭐⭐ Intermediate | 45-60 min |

## Assignment Details

### hw_5_01_subnet_design.py

Design a complete subnetting scheme using VLSM for a multi-department organisation.

**Learning Objectives:**
- Apply VLSM to allocate variable-sized subnets
- Calculate network addresses, broadcast addresses and usable host ranges
- Optimise address space utilisation
- Document IP allocation plans

**Key Skills:**
- Binary subnet calculations
- CIDR notation
- Address space planning

### hw_5_02_ipv6_transition.py

Analyse IPv6 addresses and understand dual-stack deployment concepts.

**Learning Objectives:**
- Parse and classify IPv6 address types
- Generate EUI-64 interface identifiers
- Compare IPv4 and IPv6 addressing
- Understand transition mechanisms

**Key Skills:**
- IPv6 address notation (expanded/compressed)
- Address type identification
- Transition planning

## Prerequisites

Before starting, ensure you have completed:
- Week 5 lab exercises (ex_5_01, ex_5_02)
- Reading: Theory summary and glossary

## Submission Guidelines

### Anti-AI requirements (if a challenge file is issued)

For this week the homework can be issued as an individual challenge.
If you receive a challenge file you must follow the workflow below.

1. Generate (or receive) your challenge file:

```bash
make anti-ai-challenge STUDENT_ID=ABC123
```

2. Run both homework scripts using the challenge file so that your outputs include the required tokens:

```bash
python homework/exercises/hw_5_01_subnet_design.py \
  --challenge artifacts/anti_ai/challenge_ABC123.yaml

python homework/exercises/hw_5_02_ipv6_transition.py \
  --challenge artifacts/anti_ai/challenge_ABC123.yaml
```

3. Collect evidence and validate locally:

```bash
make anti-ai-evidence STUDENT_ID=ABC123
make anti-ai-validate STUDENT_ID=ABC123
```

4. Submit exactly these four files:

- `artifacts/anti_ai/challenge_<STUDENT_ID>.yaml`
- `subnet_plan_<STUDENT_ID>.json`
- `ipv6_report_<STUDENT_ID>.json`
- `evidence_<STUDENT_ID>.json`


### Standard checklist

1. Complete all `TODO` sections in each file
2. Run the built-in verification tests
3. Ensure all prediction prompts are answered thoughtfully
4. Export any generated reports (JSON files)

## Grading Rubric

| Criterion | Points |
|-----------|--------|
| Correct implementation of core functions | 40% |
| All verification tests passing | 30% |
| Code quality (comments, type hints) | 15% |
| Prediction prompt engagement | 15% |

## Tips

- Start with the subnet design exercise as it reinforces fundamental concepts
- Use the `ipaddress` module for validation
- Draw out subnet allocations on paper first
- Remember: VLSM allocates largest requirements first

---

*Week 5 Homework — Computer Networks*
