# CI/CD Setup Guide — Week 14

> NETWORKING class — ASE, CSIE | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

This document explains the Continuous Integration (CI) pipeline configuration for the Week 14 laboratory kit.

---

## Overview

The CI pipeline automatically validates code quality, runs tests and ensures the lab kit maintains high standards. It runs on every push to `main` or `develop` branches and on pull requests.

---

## Pipeline Jobs

### 1. Code Quality (lint)

Runs Ruff linter to check for:
- PEP 8 style violations
- Common programming errors
- Import ordering
- Code complexity

```bash
# Run locally
make lint
```

### 2. Type Checking (typecheck)

Runs mypy for static type analysis:
- Verifies type hints are correct
- Catches type-related bugs early
- Ensures API consistency

```bash
# Run locally
make typecheck
```

### 3. Unit Tests (test)

Runs pytest with coverage:
- Executes all tests in `tests/`
- Generates coverage report
- Uploads to Codecov

```bash
# Run locally
make test-cov
```

### 4. Quiz Validation (quiz-validation)

Validates quiz files:
- Checks YAML structure
- Validates JSON format
- Verifies consistency between formats
- Tests quiz runner imports

```bash
# Run locally
python -c "import yaml; yaml.safe_load(open('formative/quiz.yaml'))"
```

### 5. Docker Build (docker-build)

Tests Docker configuration:
- Validates docker-compose.yml syntax
- Builds all images
- Tests container startup

```bash
# Run locally
make docker-rebuild
```

### 6. Security Scan (security-scan)

Runs security checks:
- Bandit for Python security issues
- Checks for hardcoded secrets
- pip-audit for vulnerable dependencies

```bash
# Run locally
make security
```

### 7. Documentation Check (docs-check)

Verifies documentation:
- Checks required files exist
- Validates LO traceability
- Counts Parsons problems

---

## Local CI

Run the full CI pipeline locally before pushing:

```bash
# Quick CI (lint + test + validate)
make ci

# Full CI (all checks)
make ci-full
```

---

## Configuration Files

| File | Purpose |
|------|---------|
| `.github/workflows/ci.yml` | GitHub Actions workflow |
| `ruff.toml` | Linter configuration |
| `pyproject.toml` | Project metadata and tool config |
| `setup/requirements.txt` | Python dependencies |

---

## Adding New Jobs

To add a new CI job:

1. Edit `.github/workflows/ci.yml`
2. Add job definition with:
   - Clear name
   - Appropriate dependencies (`needs:`)
   - Required steps
3. Test locally first
4. Ensure job can `continue-on-error` for non-critical checks

---

## Troubleshooting

### CI Fails on Lint

```bash
# Auto-fix most issues
make lint-fix
```

### CI Fails on Type Check

```bash
# Check specific file
python -m mypy src/file.py
```

### CI Fails on Tests

```bash
# Run specific test
python -m pytest tests/test_file.py -v
```

---

*Document version: 2.0 | Week 14: Integrated Recap | January 2025*
*NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim*
