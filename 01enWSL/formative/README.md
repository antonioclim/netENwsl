# 📝 Formative Assessment — Week 1
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## Overview

This directory contains the **machine-readable formative assessment system** for Week 1.

| File | Purpose |
|------|---------|
| `quiz.yaml` | Quiz questions in structured YAML format |
| `quiz.json` | Quiz questions in JSON format (LMS compatible) |
| `run_quiz.py` | Interactive CLI quiz runner |
| `quiz_schema.json` | JSON Schema for validation |

---

## Quick Start

### Run Full Quiz

```bash
# From the 01enWSL directory:
python formative/run_quiz.py

# Or using Makefile:
make quiz
```

### Run Specific Section

```bash
# Pre-lab (before starting exercises)
python formative/run_quiz.py --section pre_lab

# During-lab (checkpoints)
python formative/run_quiz.py --section during_lab

# Exit ticket (before leaving)
python formative/run_quiz.py --section exit_ticket
```

### Review Mode (Study)

```bash
# See all answers without being asked
python formative/run_quiz.py --review
```

### Random Practice

```bash
# 5 random questions
python formative/run_quiz.py --random --limit 5
```

---

## Quiz Structure

### Sections

| Section | Questions | Time | When to Take |
|---------|-----------|------|--------------|
| `pre_lab` | 5 | ~5 min | Before starting lab |
| `during_lab` | 5 | No limit | At checkpoints |
| `exit_ticket` | 5 | ~10 min | Before leaving |
| `full_review` | 7 | ~15 min | End of week |

### Question Types

| Type | Format | Example |
|------|--------|---------|
| `multiple_choice` | A/B/C/D | "What does RTT measure?" |
| `fill_blank` | Text input | "ip ___" → "addr" |
| `true_false` | True/False | "Ping measures bandwidth." |
| `numeric` | Number | "What port does Portainer use?" |
| `command` | Shell command | "Ping google.com 4 times" |
| `code_trace` | Predict output | "What will print?" |
| `matching` | Match pairs | "Command → Purpose" |
| `short_answer` | Keywords | "Why use UDP?" |
| `ordering` | Sequence | "Order the handshake steps" |

### Difficulty Levels

| Level | Points | Description |
|-------|--------|-------------|
| Basic | 1 pt | Remember/Recall |
| Intermediate | 2 pts | Understand/Apply |
| Advanced | 3 pts | Apply/Analyse |

---

## Grading Scale

| Score | Grade | Meaning |
|-------|-------|---------|
| 90-100% | 🌟 Excellent | Ready for advanced topics |
| 80-89% | ✅ Very Good | Minor review needed |
| 70-79% | 📗 Good | Some reinforcement needed |
| 60-69% | 📚 Developing | Significant review needed |
| 50-59% | ⚠️ Needs Improvement | Seek instructor help |
| 0-49% | 🔄 Incomplete | Schedule office hours |

**Passing threshold: 70%**

---

## Learning Objectives Coverage

Each question maps to a Learning Objective (LO):

| LO | Topic | Questions |
|----|-------|-----------|
| LO1 | ICMP ping and latency | q01, q06, q11 |
| LO2 | TCP sockets | q03, q07, q08, q12, q14 |
| LO3 | Data parsing | q16, q17 |
| LO4 | Traffic capture | q15, q22 |
| LO5 | Transmission delay | q18, q19 |
| LO6 | Docker containers | q02, q04, q05, q09, q10, q13 |
| LO7 | Wireshark capture | q15, q20, q21 |

---

## Validation

### Check Quiz Syntax

```bash
# Validate YAML
python -c "import yaml; yaml.safe_load(open('formative/quiz.yaml'))"

# Validate using the quiz runner
python formative/run_quiz.py --validate

# Or using Makefile
make validate-quiz
```

---

## Export Formats

The quiz supports multiple export formats for LMS integration:

### Export Commands

```bash
# Export to JSON (internal format)
python formative/run_quiz.py --export-json

# Export to Canvas JSON
python formative/run_quiz.py --export-canvas

# Export to Moodle XML
python formative/run_quiz.py --export-moodle

# Or export all at once
make export-quiz
```

### Generated Files

| File | Format | LMS Compatibility |
|------|--------|-------------------|
| `quiz_lms_export.json` | JSON | Generic LMS import |
| `quiz_canvas.json` | Canvas JSON | Canvas LMS |
| `quiz_moodle.xml` | Moodle XML | Moodle question bank |

---

## For Instructors

### Adding Questions

1. Edit `quiz.yaml`
2. Follow the schema in `quiz_schema.json`
3. Link to `docs/misconceptions.md` where applicable
4. Add to appropriate section
5. Run validation

### Question Template

```yaml
- id: qNN
  type: multiple_choice
  lo_ref: LOX
  bloom_level: understand
  difficulty: intermediate
  points: 2
  stem: "Question text"
  options:
    a: "Option A"
    b: "Option B"
    c: "Option C"
    d: "Option D"
  correct: b
  explanation: "Why B is correct"
  misconception_ref: "docs/misconceptions.md#misconception-X"
  feedback:
    correct: "✅ Well done!"
    incorrect: "❌ Review section X"
```

---

## Support

If you need help: Issues: Open an issue in GitHub.

---

*NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim*
