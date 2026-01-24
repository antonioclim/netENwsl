# 🔄 CI/CD Setup Guide — Week 10
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Continuous Integration pipeline documentation

---

## Overview

This laboratory uses GitHub Actions for automated testing and validation. The CI pipeline ensures code quality, runs tests and validates documentation before changes are merged.

---

## Pipeline Structure

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         GitHub Actions CI                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐        │
│   │  Syntax  │───▶│   Lint   │───▶│   Test   │───▶│  Docker  │        │
│   │  Check   │    │  (ruff)  │    │          │    │  Build   │        │
│   └──────────┘    └──────────┘    └──────────┘    └──────────┘        │
│         │              │              │                                 │
│         │         ┌────┴────┐         │                                 │
│         │         ▼         ▼         │                                 │
│         │    ┌────────┐ ┌────────┐    │                                 │
│         │    │Typecheck│ │Security│    │                                 │
│         │    │ (mypy) │ │(bandit)│    │                                 │
│         │    └────────┘ └────────┘    │                                 │
│         │                             │                                 │
│         └──────────────┬──────────────┘                                 │
│                        ▼                                                │
│                   ┌──────────┐                                          │
│                   │   Docs   │                                          │
│                   │  Check   │                                          │
│                   └──────────┘                                          │
│                        │                                                │
│                        ▼                                                │
│                   ┌──────────┐                                          │
│                   │   LMS    │                                          │
│                   │  Export  │                                          │
│                   └──────────┘                                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Jobs Description

### 1. Syntax Check

**Purpose:** Verify all Python files have valid syntax before further processing.

```yaml
- name: Check Python syntax
  run: find . -name "*.py" -type f | xargs python -m py_compile
```

### 2. Lint (ruff)

**Purpose:** Code style and quality checks using ruff linter.

**Configuration:** See `ruff.toml` in the repository root.

```bash
# Run locally
ruff check src/ scripts/ tests/ formative/

# Auto-fix issues
ruff check --fix src/
```

### 3. Type Check (mypy)

**Purpose:** Static type analysis to catch type errors.

**Configuration:** See `mypy.ini` in the repository root.

```bash
# Run locally
mypy src/ scripts/ --ignore-missing-imports
```

### 4. Security Scan (bandit)

**Purpose:** Identify common security issues in Python code.

```bash
# Run locally
bandit -r src/ scripts/ -ll
```

### 5. Unit Tests

**Purpose:** Run pytest test suite and exercise selftests.

```bash
# Run locally
pytest tests/ -v
python src/exercises/ex_10_01_tls_rest_crud.py selftest
```

### 6. Docker Build

**Purpose:** Verify Docker images build and containers start correctly.

```bash
# Run locally
docker compose -f docker/docker-compose.yml build
docker compose -f docker/docker-compose.yml up -d
```

### 7. Documentation Check

**Purpose:** Verify required documentation files exist and are valid.

**Required files:**
- `README.md`
- `CHANGELOG.md`
- `docs/theory_summary.md`
- `docs/misconceptions.md`
- `docs/troubleshooting.md`
- `docs/learning_objectives.md`
- `docs/peer_instruction.md`
- `docs/parsons_problems.md`
- `formative/quiz.yaml`

### 8. LMS Export Test

**Purpose:** Verify quiz exports correctly to LMS formats.

```bash
# Run locally
python formative/run_quiz.py --export-moodle exports/quiz.xml
python formative/run_quiz.py --export-json exports/quiz.json
```

---

## Workflow File

The CI workflow is defined in `.github/workflows/ci.yml`.

### Triggers

```yaml
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  workflow_dispatch:  # Manual trigger
```

### Concurrency

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

This cancels in-progress runs when new commits are pushed, saving CI minutes.

---

## Running CI Locally

### Using Make

```bash
# Run all CI checks
make ci-lint
make ci-test
make ci-docs

# Or run everything
make all
```

### Manual Commands

```bash
# 1. Syntax check
find . -name "*.py" -type f | xargs python -m py_compile

# 2. Lint
ruff check src/ scripts/ tests/

# 3. Type check
mypy src/ scripts/ --ignore-missing-imports

# 4. Security scan
bandit -r src/ scripts/ -ll

# 5. Tests
pytest tests/ -v
python src/exercises/ex_10_01_tls_rest_crud.py selftest

# 6. Docker build
docker compose -f docker/docker-compose.yml build

# 7. Quiz validation
python -c "import yaml; yaml.safe_load(open('formative/quiz.yaml'))"
```

---

## Configuration Files

### ruff.toml

```toml
[lint]
select = ["E", "F", "W", "I", "N", "B"]
ignore = ["E501", "E402"]
```

### mypy.ini

```ini
[mypy]
python_version = 3.11
ignore_missing_imports = True
warn_return_any = True
```

---

## Troubleshooting CI Failures

### Lint Failures

```
error: E501 Line too long (120 > 88 characters)
```

**Solution:** Ignored in configuration. If you see other errors, run:
```bash
ruff check --fix src/
```

### Type Check Failures

```
error: Missing type annotation for function argument
```

**Solution:** Add type hints or use `# type: ignore` for third-party code.

### Test Failures

```
FAILED tests/test_exercises.py::test_exercise_1 - ConnectionRefusedError
```

**Solution:** Ensure Docker containers are running:
```bash
make lab-start
```

### Docker Build Failures

```
error: failed to solve: dockerfile parse error
```

**Solution:** Check Dockerfile syntax and ensure base images are available.

---

## Badge Integration

Add CI status badge to README:

```markdown
[![CI](https://github.com/YOUR_USERNAME/week10/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/week10/actions/workflows/ci.yml)
```

---

## Support

If CI issues persist:

- Check GitHub Actions logs for detailed error messages
- Run checks locally to reproduce the issue
- Issues: Open an issue in GitHub

---

*Computer Networks — Week 10 | ASE, CSIE Bucharest*
*Laboratory materials by ing. dr. Antonio Clim*
