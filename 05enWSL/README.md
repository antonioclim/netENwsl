# Week 5: Network Layer – IP Addressing, Subnetting and VLSM

[![CI Status](https://img.shields.io/badge/CI-passing-brightgreen)](../../actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Bloom Coverage](https://img.shields.io/badge/Bloom-L1--L6-purple.svg)](docs/learning_objectives.md)
[![Quiz Questions](https://img.shields.io/badge/Quiz-12_questions-orange.svg)](formative/quiz.yaml)

> Computer Networks Laboratory — ASE-CSIE Bucharest

| Version | Last Updated | Quiz Questions | LO Coverage |
|---------|--------------|----------------|-------------|
| 1.1.0 | 2026-01-24 | 12 (Bloom L1-L6) | 6/6 Complete |

---

## Quick Start

```bash
# Navigate to kit directory
cd /mnt/d/NETWORKING/WEEK5/05enWSL

# Start Docker
sudo service docker start

# Install dependencies
pip install -r setup/requirements.txt

# Verify environment
python3 setup/verify_environment.py

# Start lab
python3 scripts/start_lab.py

# Run quiz
make quiz
```

---

## Learning Objectives

1. **Identify** the role and functions of the network layer (LO1)
2. **Explain** IPv4 and IPv6 addressing schemes (LO2)
3. **Calculate** network addresses and host ranges (LO3)
4. **Apply** FLSM subnetting (LO4)
5. **Design** VLSM allocation schemes (LO5)
6. **Evaluate** addressing efficiency (LO6)

See [docs/learning_objectives.md](docs/learning_objectives.md) for complete traceability matrix.

---

## Formative Assessment

```bash
# Full quiz (12 questions, Bloom L1-L6)
python3 formative/run_quiz.py

# Quick quiz (5 random questions)
python3 formative/run_quiz.py --random --limit 5

# Export for Moodle/Canvas
python3 formative/export_to_lms.py --format json --pretty
```

| Bloom Level | Questions | Points |
|-------------|-----------|--------|
| Remember | q01, q02 | 2 |
| Understand | q03, q04 | 4 |
| Apply | q05, q06, q09, q10 | 9 |
| Analyse | q07, q08 | 6 |
| Evaluate | q11 | 3 |
| Create | q12 | 4 |
| **Total** | **12** | **28** |

---

## Anti-AI submission workflow

This kit supports an evidence-based workflow for homework submission.
Each student receives an individual challenge file, then generates two JSON artefacts that include per-task tokens.

```bash
# 1) Generate your challenge
make anti-ai-challenge STUDENT_ID=ABC123

# 2) Produce the required artefacts
python homework/exercises/hw_5_01_subnet_design.py \
  --challenge artifacts/anti_ai/challenge_ABC123.yaml \
  --non-interactive

python homework/exercises/hw_5_02_ipv6_transition.py \
  --challenge artifacts/anti_ai/challenge_ABC123.yaml \
  --non-interactive

# 3) Collect evidence and validate locally
make anti-ai-evidence STUDENT_ID=ABC123
make anti-ai-validate STUDENT_ID=ABC123
```

Submission package (Week 5):
- `artifacts/anti_ai/challenge_<STUDENT_ID>.yaml`
- `subnet_plan_<STUDENT_ID>.json`
- `ipv6_report_<STUDENT_ID>.json`
- `evidence_<STUDENT_ID>.json`

---

## Make Targets

| Target | Description |
|--------|-------------|
| `make help` | Show all targets |
| `make setup` | Install dependencies |
| `make test` | Run all tests |
| `make quiz` | Run formative quiz |
| `make ci` | Run CI pipeline locally |
| `make lms-export` | Export quiz for LMS |
| `make lab` | Start Docker environment |

---

## Network Configuration

| Resource | Value |
|----------|-------|
| Subnet | 10.5.0.0/24 |
| Python Container | 10.5.0.10 |
| UDP Server | 10.5.0.20:9999 |
| UDP Client | 10.5.0.30 |

---

## Support

For issues with this laboratory kit:

1. Check [docs/troubleshooting.md](docs/troubleshooting.md)
2. Review [docs/misconceptions.md](docs/misconceptions.md)
3. Open an issue in GitHub

---

*Computer Networks Laboratory — ASE-CSIE Bucharest*
