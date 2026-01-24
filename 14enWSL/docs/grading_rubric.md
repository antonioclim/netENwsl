# 📊 Grading Rubric — Week 14 Homework Assignments

> NETWORKING class — ASE, CSIE | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

---

## Overview

This document provides detailed evaluation criteria for all Week 14 homework assignments. Each criterion includes specific indicators for each grade level.

**Grading Scale:** 1-10 (Romanian system)

| Grade | Description | Percentage |
|-------|-------------|------------|
| 10 | Exceptional, exceeds requirements | 95-100% |
| 9 | Excellent, fully meets requirements | 85-94% |
| 8 | Very good, minor issues | 75-84% |
| 7 | Good, some gaps | 65-74% |
| 6 | Satisfactory, meets minimum | 55-64% |
| 5 | Sufficient, barely acceptable | 45-54% |
| 1-4 | Insufficient, does not meet requirements | 0-44% |

---

## HW 14.01: Enhanced Echo Protocol (100 points)

### Criterion 1: Command Implementation (30 points)

| Points | Description | Indicators |
|--------|-------------|------------|
| 30 | All 5 commands work correctly | ECHO, TIME, CALC, QUIT, HELP all functional |
| 25 | 4 commands work | One command missing or broken |
| 20 | 3 commands work | Two commands missing or broken |
| 15 | 2 commands work | Basic functionality only |
| 10 | 1 command works | Minimal implementation |
| 0 | No commands work | Server does not respond |

**Verification:**
```bash
# Automated test (must pass all)
echo "ECHO test" | nc localhost 9001
echo "TIME" | nc localhost 9001
echo "CALC 2+3" | nc localhost 9001
echo "HELP" | nc localhost 9001
```

### Criterion 2: Error Handling (25 points)

| Points | Description | Indicators |
|--------|-------------|------------|
| 25 | Comprehensive error handling | Malformed input, edge cases, graceful recovery |
| 20 | Good error handling | Most errors caught, some edge cases missed |
| 15 | Basic error handling | Common errors caught |
| 10 | Minimal error handling | Server crashes on some inputs |
| 0 | No error handling | Server crashes frequently |

**Test Cases:**
```bash
# These should NOT crash the server
echo "" | nc localhost 9001                    # Empty input
echo "UNKNOWN_CMD" | nc localhost 9001         # Unknown command
echo "CALC abc" | nc localhost 9001            # Invalid expression
echo "CALC 1/0" | nc localhost 9001            # Division by zero
printf "A%.0s" {1..10000} | nc localhost 9001  # Very long input
```

### Criterion 3: Code Quality (20 points)

| Points | Description | Indicators |
|--------|-------------|------------|
| 20 | Professional quality | Type hints, docstrings, clean structure |
| 16 | Good quality | Some type hints, basic docs |
| 12 | Acceptable | Works but messy |
| 8 | Poor quality | Hard to read, no docs |
| 0 | Unacceptable | Cannot understand code |

**Checklist:**
- [ ] Type hints on all function signatures
- [ ] Docstrings on classes and public methods
- [ ] Meaningful variable names
- [ ] No hardcoded magic numbers
- [ ] Consistent formatting

### Criterion 4: Test Coverage (15 points)

| Points | Description | Indicators |
|--------|-------------|------------|
| 15 | Comprehensive tests | All commands, edge cases, stress tests |
| 12 | Good tests | All commands tested |
| 9 | Basic tests | Some commands tested |
| 6 | Minimal tests | Only happy path |
| 0 | No tests | No test file provided |

### Criterion 5: Backwards Compatibility (10 points)

| Points | Description | Indicators |
|--------|-------------|------------|
| 10 | Fully compatible | Plain text echoed without command prefix |
| 5 | Partially compatible | Works with warnings |
| 0 | Not compatible | Rejects plain text |

---

## HW 14.02: Weighted Load Balancer (100 points)

### Criterion 1: Algorithm Correctness (35 points)

| Points | Description | Indicators |
|--------|-------------|------------|
| 35 | Perfect distribution | Weights respected within 5% variance |
| 28 | Good distribution | Weights respected within 10% variance |
| 21 | Acceptable | Weights roughly followed |
| 14 | Poor | Distribution incorrect |
| 0 | Broken | Does not distribute |

**Verification Script:**
```python
# Must show correct weight distribution
weights = {"app1": 3, "app2": 1}  # 75%/25% expected
results = [request() for _ in range(1000)]
# app1 should be ~750±50, app2 should be ~250±50
```

### Criterion 2: Configuration (20 points)

| Points | Description | Indicators |
|--------|-------------|------------|
| 20 | Dynamic config | Weights from file/env, hot reload |
| 15 | Static config | Weights from config file |
| 10 | Hardcoded | Weights in code but configurable |
| 0 | Fixed | Cannot change weights |

### Criterion 3: Health Checks (20 points)

| Points | Description | Indicators |
|--------|-------------|------------|
| 20 | Active health checks | Periodic checks, automatic failover |
| 15 | Passive checks | Failover on error only |
| 10 | Manual checks | Must restart to update |
| 0 | No checks | Sends to dead backends |

### Criterion 4: Metrics and Logging (15 points)

| Points | Description | Indicators |
|--------|-------------|------------|
| 15 | Comprehensive | Per-backend stats, response times |
| 10 | Basic | Request counts only |
| 5 | Minimal | Only errors logged |
| 0 | None | No logging |

### Criterion 5: Documentation (10 points)

| Points | Description | Indicators |
|--------|-------------|------------|
| 10 | Complete | README, examples, architecture |
| 7 | Good | README with usage |
| 4 | Basic | Comments only |
| 0 | None | No documentation |

---

## HW 14.03: PCAP Analyser (100 points)

### Criterion 1: Parsing Accuracy (30 points)

| Points | Description | Indicators |
|--------|-------------|------------|
| 30 | Parses all layers | Ethernet, IP, TCP/UDP, HTTP |
| 24 | Parses most layers | IP and TCP/UDP |
| 18 | Parses some | IP only |
| 12 | Minimal | Counts packets only |
| 0 | Broken | Cannot read PCAP |

### Criterion 2: Analysis Features (25 points)

| Points | Description | Indicators |
|--------|-------------|------------|
| 25 | Rich analysis | Flow tracking, timing, anomalies |
| 20 | Good analysis | Statistics per protocol |
| 15 | Basic analysis | Packet counts by type |
| 10 | Minimal | Lists packets |
| 0 | None | No analysis |

### Criterion 3: Output Format (20 points)

| Points | Description | Indicators |
|--------|-------------|------------|
| 20 | Multiple formats | JSON, CSV, human-readable |
| 15 | Two formats | JSON + text |
| 10 | One format | JSON only |
| 5 | Unstructured | Print statements |
| 0 | Broken | Cannot output |

### Criterion 4: Performance (15 points)

| Points | Description | Indicators |
|--------|-------------|------------|
| 15 | Handles large files | 100MB+ PCAP in <30s |
| 10 | Acceptable | 10MB in <30s |
| 5 | Slow | Small files only |
| 0 | Unusable | Crashes on normal files |

### Criterion 5: Error Handling (10 points)

| Points | Description | Indicators |
|--------|-------------|------------|
| 10 | Robust | Handles malformed packets, partial files |
| 5 | Basic | Handles common errors |
| 0 | Fragile | Crashes on bad input |

---

## Submission Checklist

Before submitting, verify:

### All Assignments

- [ ] Code runs without errors
- [ ] All required files present
- [ ] README.md with usage instructions
- [ ] No hardcoded paths (use relative paths)
- [ ] Tested on lab environment (WSL2 + Docker)

### File Naming Convention

```
homework/
├── hw_14_01_enhanced_echo/
│   ├── README.md
│   ├── server.py
│   ├── client.py
│   ├── test_server.py
│   └── report.md
├── hw_14_02_weighted_lb/
│   └── ...
└── hw_14_03_pcap_analyser/
    └── ...
```

### Penalty Deductions

| Issue | Deduction |
|-------|-----------|
| Late submission (per day) | -10% |
| Missing README | -5 points |
| Code does not run | -20 points |
| Plagiarism detected | -100% + disciplinary |

---

## Grade Calculation

```
Final Grade = (HW1 × 0.30) + (HW2 × 0.35) + (HW3 × 0.35)
```

| Total Points | Grade |
|--------------|-------|
| 95-100 | 10 |
| 85-94 | 9 |
| 75-84 | 8 |
| 65-74 | 7 |
| 55-64 | 6 |
| 45-54 | 5 |
| <45 | 4 (fail) |

---

## Support

If you encounter issues with the grading rubric or have questions about evaluation criteria:

- **Issues:** Open an issue in GitHub
- **Office Hours:** Check the course schedule for availability

---

*NETWORKING class — ASE, CSIE | Computer Networks Laboratory*
*Grading Rubric v2.0.0 | Week 14*
