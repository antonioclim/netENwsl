# 📝 Formative Assessment — Week 6

> Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

## Overview

This folder contains **self-assessment materials** designed to be completed **before** the laboratory session. The formative quiz helps you identify knowledge gaps and prepares you for hands-on exercises.

## Contents

| File | Purpose |
|------|---------|
| `quiz.yaml` | Quiz questions in YAML format (12 questions) |
| `run_quiz.py` | Interactive CLI quiz runner |
| `README.md` | This file |

## Quick Start

```bash
# Run the full quiz
python formative/run_quiz.py

# Run with randomised order
python formative/run_quiz.py --random

# Limit to 5 questions
python formative/run_quiz.py --limit 5

# Filter by Learning Objective
python formative/run_quiz.py --lo LO1 LO2

# Filter by difficulty
python formative/run_quiz.py --difficulty basic

# Export results to JSON
python formative/run_quiz.py --export my_results.json
```

## Requirements

```bash
pip install pyyaml --break-system-packages
```

## Quiz Structure

The quiz covers all 7 Learning Objectives:

| LO | Topic | Questions |
|----|-------|-----------|
| LO1 | NAT variants & supporting protocols | 3 |
| LO2 | PAT translation tables | 2 |
| LO3 | Implement NAT/MASQUERADE | 2 |
| LO4 | SDN flow installation | 1 |
| LO5 | Analyse permitted/blocked traffic | 2 |
| LO6 | Compare traditional vs SDN | 1 |
| LO7 | Design OpenFlow policies | 1 |

## Difficulty Distribution

- **Basic:** 4 questions (Remember/Understand)
- **Intermediate:** 5 questions (Understand/Apply)
- **Advanced:** 3 questions (Analyse)

## Passing Score

- **70%** (8/12 correct) indicates readiness for the laboratory
- Results below 70% suggest reviewing `docs/theory_summary.md` and `docs/misconceptions.md`

## Interactive Features

During the quiz:
- Type `hint` for a hint (if available)
- Type `skip` to skip a question
- Type `quit` to exit early

## After the Quiz

Your results will show:
- Overall score and pass/fail status
- Performance breakdown by Learning Objective
- Recommended next steps based on your score

## Integration with Lab

The quiz is also available via Makefile:

```bash
make quiz           # Run full quiz
make quiz-random    # Run with randomised questions
```

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
