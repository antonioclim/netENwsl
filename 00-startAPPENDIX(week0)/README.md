# 📚 Week 0 — Lab Environment Setup
## Computer Networks — ASE Bucharest, CSIE | by ing. dr. Antonio Clim

![CI Status](https://img.shields.io/badge/CI-passing-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![License](https://img.shields.io/badge/License-Educational-orange)

> **Prerequisites kit** for the 14-week Computer Networks laboratory course.  
> **Complete this before Week 1!**

---

## 🎯 Learning Objectives

By completing Week 0, you will be able to:

| ID | Objective | Bloom Level | Assessment |
|----|-----------|-------------|------------|
| LO0.1 | Configure complete WSL2 + Docker environment | Apply | Quiz Q1-Q2 |
| LO0.2 | Distinguish Docker images from containers | Understand | Quiz Q3, Q10 |
| LO0.3 | Apply port mapping between host and containers | Apply | Quiz Q4-Q5 |
| LO0.4 | Convert between bytes and strings in Python | Apply | Quiz Q6-Q7 |
| LO0.5 | Create and configure basic TCP sockets | Apply | Quiz Q8-Q9 |

📖 **Full details:** [`docs/learning_objectives.md`](docs/learning_objectives.md)

---

## 🚀 Quick Start

### Step 1: Verify Your Environment

```bash
cd 00BEFORE_ANYTHING_ELSE/
chmod +x verify_lab_environment.sh
./verify_lab_environment.sh
```

**Expected result:** All checks should show ✓ (green)

### Step 2: Complete the Self-Study Guide

1. 📖 Read [`00BEFORE_ANYTHING_ELSE/Prerequisites.md`](00BEFORE_ANYTHING_ELSE/Prerequisites.md)
2. 🐍 Work through [`PYTHON_self_study_guide/`](PYTHON_self_study_guide/)
3. 💻 Run the examples in `PYTHON_self_study_guide/examples/`

### Step 3: Test Your Knowledge

```bash
# Using Make (recommended)
make quiz

# Or directly
python formative/run_quiz.py
```

**Target:** Score ≥70% to proceed to Week 1

### Step 4: Review Common Mistakes

📖 Read [`docs/misconceptions.md`](docs/misconceptions.md) — avoid these 12 common errors!

---

## 📁 Folder Structure

```
00-startAPPENDIX(week0)/
│
├── 00BEFORE_ANYTHING_ELSE/        # 🔧 Environment setup & verification
│   ├── Prerequisites.md           # Complete setup guide
│   ├── Prerequisites_CHECKS.md    # Verification checklist
│   └── verify_lab_environment.sh  # Automated verification script
│
├── 00LECTURES/                    # 📚 S1-S14 theory presentations
│   └── S{1-14}Theory_Week{1-14}_EN.html
│
├── 00PREREQUISITES/               # 📄 HTML version of prerequisites
│   └── PREREQUISITES_EN.html
│
├── docs/                          # 📖 Pedagogical documents
│   ├── learning_objectives.md     # LO → Bloom → Artefact mapping
│   ├── misconceptions.md          # 12 common errors and corrections
│   ├── troubleshooting.md         # Solutions to common issues
│   ├── glossary.md                # Key terms and definitions
│   ├── concept_analogies.md       # Analogies for complex concepts
│   ├── code_tracing.md            # Code tracing exercises
│   ├── parsons_problems.md        # 5 code ordering exercises
│   ├── peer_instruction.md        # Discussion questions
│   ├── pair_programming_guide.md  # Collaboration guide
│   └── ci_setup.md                # CI/CD documentation
│
├── formative/                     # ✅ Self-assessment quiz
│   ├── quiz.yaml                  # 10 questions, 3 Bloom levels
│   ├── quiz.json                  # LMS export format (Moodle/Canvas)
│   └── run_quiz.py                # Interactive CLI runner
│
├── PYTHON_self_study_guide/       # 🐍 Python for networking
│   ├── PYTHON_NETWORKING_GUIDE.md # Complete guide (~80KB)
│   ├── cheatsheets/PYTHON_QUICK.md# Quick reference
│   ├── examples/                  # Runnable code examples
│   │   ├── 01_socket_tcp.py       # TCP client/server
│   │   ├── 02_bytes_vs_str.py     # Encoding/decoding
│   │   ├── 03_struct_parsing.py   # Binary protocol parsing
│   │   └── tests/test_smoke.py    # Verification tests
│   └── PRESENTATIONS_EN/          # HTML slides (10 modules)
│
├── .github/workflows/             # 🔄 CI/CD
│   └── ci.yml                     # GitHub Actions pipeline
│
├── Makefile                       # 🛠️ Build automation
├── ruff.toml                      # 🔍 Linting configuration
├── CHANGELOG.md                   # 📋 Version history
├── LIVE_CODING_INSTRUCTOR_GUIDE.md# 👨‍🏫 Instructor resources
└── README.md                      # ← You are here
```

---

## 🛠️ Using the Makefile

```bash
make help          # Show all available targets

# Quiz commands
make quiz          # Run interactive quiz
make quiz-review   # Show answers (review mode)
make quiz-random   # Randomised questions

# Development commands
make test          # Run smoke tests
make lint          # Run code linter
make validate      # Validate YAML/JSON files

# Export commands
make export        # Export quiz to all formats
make export-json   # Export to JSON (LMS)
make export-moodle # Export to Moodle GIFT

# Utility
make clean         # Remove generated files
make all           # Run lint + test + validate
```

---

## ✅ Self-Assessment Checklist

Before proceeding to Week 1, verify you can:

- [ ] Start WSL2 and Docker without errors
- [ ] Access Portainer at `http://localhost:9000` (user: `stud`, pass: `studstudstud`)
- [ ] Run `verify_lab_environment.sh` with all checks passing
- [ ] Score ≥70% on `formative/quiz.yaml`
- [ ] Explain the container/image relationship to a peer
- [ ] Write a simple TCP client that connects and sends a message
- [ ] Convert between bytes and strings without errors
- [ ] Identify the correct socket sequence for server vs client

---

## 🔧 Troubleshooting

**Common issues and solutions:** [`docs/troubleshooting.md`](docs/troubleshooting.md)

### Quick Fixes

| Problem | Solution |
|---------|----------|
| Docker not starting | `sudo service docker start` |
| Port 9000 in use | `sudo lsof -i :9000` then stop conflicting process |
| WSL networking issues | Check `docs/troubleshooting.md#wsl-issues` |
| Python import errors | `pip install pyyaml` |
| Permission denied | `chmod +x script.sh` |

---

## 📚 Key Resources

| Resource | Location | Description |
|----------|----------|-------------|
| 📖 Prerequisites Guide | `00BEFORE_ANYTHING_ELSE/Prerequisites.md` | Complete setup instructions |
| 🐍 Python Guide | `PYTHON_self_study_guide/PYTHON_NETWORKING_GUIDE.md` | Python for networking |
| 📝 Glossary | `docs/glossary.md` | Key terms and definitions |
| ❌ Misconceptions | `docs/misconceptions.md` | 12 common errors to avoid |
| 🔧 Troubleshooting | `docs/troubleshooting.md` | ~25 common issues solved |
| 🧩 Parsons Problems | `docs/parsons_problems.md` | 5 code ordering exercises |

---

## 🎓 Learning Path

```
Week 0 (Prerequisites)
    │
    ├── 1. Environment Setup ──────► Prerequisites.md
    │       └── Verify: verify_lab_environment.sh
    │
    ├── 2. Python Basics ──────────► PYTHON_NETWORKING_GUIDE.md
    │       └── Practice: examples/*.py
    │
    ├── 3. Parsons Problems ───────► docs/parsons_problems.md
    │       └── 5 code ordering exercises
    │
    ├── 4. Self-Assessment ────────► make quiz
    │       └── Target: ≥70%
    │
    └── 5. Ready for Week 1! ──────► 01enWSL/
```

---

## 🔄 CI/CD

This kit includes a GitHub Actions CI pipeline that validates:
- Python syntax
- Code linting (ruff)
- YAML/JSON validity
- Smoke tests
- Documentation completeness

See [`docs/ci_setup.md`](docs/ci_setup.md) for setup instructions.

---

## 📞 Support

- **Course forum:** Check Moodle/course platform
- **Office hours:** According to schedule
- **Troubleshooting:** Start with `docs/troubleshooting.md`

---

## 📋 Version Information

| Field | Value |
|-------|-------|
| Version | 1.5.0 |
| Last Updated | January 2026 |
| Author | ing. dr. Antonio Clim |
| Institution | ASE Bucharest, CSIE |
| Python | 3.11+ |

---

*Week 0 — Computer Networks | Academy of Economic Studies, Bucharest*  
*Faculty of Cybernetics, Statistics and Economic Informatics*
