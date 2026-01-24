# 🎯 Learning Objectives Traceability Matrix — Week 9

> Session Layer (L5) and Presentation Layer (L6)
> NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

## Overview

| LO | Description | Bloom Level | Primary Exercise | Quiz Coverage |
|----|-------------|-------------|------------------|---------------|
| LO1 | Identify connection vs session | Understand | ex_9_02, ex_9_03 | q01, q02 |
| LO2 | Explain endianness mechanisms | Apply | ex_9_01 | q03, q04, q05 |
| LO3 | Implement binary framing | Apply | ex_9_01, hw_9_01 | q06, q07 |
| LO4 | Demonstrate FTP sessions | Apply | ex_9_03, ex_9_04 | q08, q09 |
| LO5 | Analyse packet captures | Analyse | capture_traffic.py | q10, q13 |
| LO6 | Design checkpoint-recovery | Create | hw_9_02 | q11, q12, q14, q15 |

## Coverage Summary

| Resource Type | LO1 | LO2 | LO3 | LO4 | LO5 | LO6 | Coverage |
|---------------|-----|-----|-----|-----|-----|-----|----------|
| Theory | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 100% |
| Exercises | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 100% |
| Tests | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 100% |
| Quiz (15 Q) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 100% |
| Misconceptions | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 100% |
| Parsons (5) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 100% |

## Verification Commands

```bash
# Run formative quiz filtered by LO
python formative/run_quiz.py --lo LO1 --stats
python formative/run_quiz.py --lo LO2 --stats
# etc.

# Run all tests
make test
```

## Self-Assessment Checklist

- [ ] LO1: Explain why FTP session state is lost when TCP reconnects
- [ ] LO2: Convert a 32-bit integer to network byte order
- [ ] LO3: Design a protocol header with magic, length, type and CRC
- [ ] LO4: Start Docker environment and observe FTP sessions
- [ ] LO5: Capture FTP traffic and identify control vs data packets
- [ ] LO6: Describe checkpoint-based recovery mechanisms

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
