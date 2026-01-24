# Formative Assessment — Week 4

> NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

## Overview

This directory contains self-assessment tools aligned with the Week 4 Learning Objectives.

## Contents

| File | Description |
|------|-------------|
| `quiz.yaml` | 15 quiz questions covering all 6 LOs |
| `run_quiz.py` | Interactive quiz runner with filtering |

## Quick Start

```bash
# Run full quiz
python formative/run_quiz.py

# Run 10 random questions
python formative/run_quiz.py --random --limit 10

# Or use make
make quiz
make quiz-random
```

## Filter Options

```bash
# By Learning Objective
python formative/run_quiz.py --lo LO3 LO4

# By Bloom level
python formative/run_quiz.py --bloom apply

# Combined
python formative/run_quiz.py --lo LO4 --bloom apply --random
```

## Question Distribution

| Bloom Level | Count | LOs |
|-------------|-------|-----|
| Remember | 3 | LO1 |
| Understand | 4 | LO2 |
| Apply | 5 | LO3, LO4 |
| Analyse | 2 | LO5 |
| Evaluate | 1 | LO6 |

## Passing Score

The default passing score is **70%**. Results are broken down by:

- Learning Objective (identify weak areas)
- Bloom taxonomy level (identify cognitive gaps)

## Related Resources

After completing the quiz, review weak areas using:

- `docs/misconceptions.md` — Common errors
- `docs/code_tracing.md` — Trace through examples
- `docs/parsons_problems.md` — Practice ordering code

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
