# Formative Assessment — Week 2

> NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim

## Overview

This folder contains self-assessment tools to help you verify your understanding of Week 2 concepts before the homework deadline or exam.

## Contents

| File | Purpose |
|------|---------|
| `quiz.yaml` | 15 questions covering all Bloom levels |
| `run_quiz.py` | Interactive quiz runner |
| `parsons_problems.json` | Code reordering exercises |

## Quick Start

### Run the Quiz

```bash
# Full quiz (15 questions)
python formative/run_quiz.py

# Or use the Makefile
make quiz
```

### Quiz Options

```bash
# Randomise question order
python formative/run_quiz.py --random

# Quick 5-question quiz
python formative/run_quiz.py --limit 5

# Only specific Bloom level
python formative/run_quiz.py --level 3  # Apply-level questions

# Study mode (shows answers immediately)
python formative/run_quiz.py --review
```

## Question Types

### Multiple Choice

Select the correct option (a, b, c or d):

```
Which socket type constant is used for TCP connections?
    a) SOCK_DGRAM
    b) SOCK_STREAM  ← correct
    c) SOCK_RAW
    d) SOCK_TCP

Your answer: b
```

### Fill-in-the-Blank

Type your answer:

```
The TCP/IP model has ___ layers.

Your answer: 4
```

### Code Output

Predict what code will produce:

```python
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print(s.type == socket.SOCK_STREAM)
```

Options: True / False / None / Error

## Bloom Taxonomy Coverage

| Level | Questions | Topics |
|-------|-----------|--------|
| 1. Remember | q01–q05 | OSI layers, port numbers, socket types |
| 2. Understand | q06–q09 | TCP vs UDP, handshake, TIME_WAIT |
| 3. Apply | q10–q12 | SO_REUSEADDR, bind addresses, code |
| 4. Analyse | q13–q14 | Debugging, Docker networking |
| 5. Evaluate | q15 | Protocol selection for real scenarios |

## Scoring

| Grade | Percentage | Meaning |
|-------|------------|---------|
| A | 90–100% | Excellent — ready for advanced topics |
| B | 75–89% | Good — solid understanding |
| C | 60–74% | Satisfactory — review weak areas |
| D | 50–59% | Passing — significant review needed |
| F | <50% | Review theory_summary.md and retry |

## After the Quiz

If you scored below 70%:

1. Review `docs/theory_summary.md`
2. Check `docs/misconceptions.md` for common errors
3. Re-run exercises `ex_2_01_tcp.py` and `ex_2_02_udp.py`
4. Try the Parsons problems in `parsons_problems.json`
5. Retake the quiz with `--random` flag

## Parsons Problems

The `parsons_problems.json` file contains code reordering exercises. These are not yet automated but can be used for self-study:

1. Open the JSON file
2. Read the `blocks` array (shuffled code)
3. Determine the correct order
4. Check against `correct_order`
5. Read the `explanation`

---

*NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim*
