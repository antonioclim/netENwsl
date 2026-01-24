# 🔄 CI/CD Setup Guide

> NETWORKING class — ASE, CSIE | Computer Networks Laboratory  
> by ing. dr. Antonio Clim

---

## Overview

This document describes the Continuous Integration (CI) pipeline configuration for the Week 14 Lab Kit. The pipeline ensures code quality, validates quiz content and tests Docker configurations automatically.

---

## Pipeline Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Push/PR   │───▶│   GitHub    │───▶│  CI Runner  │
│  to main    │    │   Actions   │    │  (Ubuntu)   │
└─────────────┘    └─────────────┘    └─────────────┘
                                             │
                   ┌─────────────────────────┼─────────────────────────┐
                   │                         │                         │
                   ▼                         ▼                         ▼
            ┌─────────────┐          ┌─────────────┐          ┌─────────────┐
            │    Lint     │          │    Test     │          │    Quiz     │
            │   (Ruff)    │          │  (pytest)   │          │ Validation  │
            └─────────────┘          └─────────────┘          └─────────────┘
                   │                         │                         │
                   └─────────────────────────┼─────────────────────────┘
                                             │
                                             ▼
                                    ┌─────────────────┐
                                    │  Docker Build   │
                                    │  & Integration  │
                                    └─────────────────┘
                                             │
                                             ▼
                                    ┌─────────────────┐
                                    │ Security Scan   │
                                    │   (Bandit)      │
                                    └─────────────────┘
```

---

## Jobs Description

### 1. Lint (Code Quality)

**Purpose:** Ensure code follows Python best practices.

**Tools:** Ruff (fast Python linter and formatter)

**Local execution:**
```bash
make lint           # Run linter
make lint-fix       # Auto-fix issues
```

---

### 2. Test (Unit Tests)

**Purpose:** Validate code functionality.

**Tools:** pytest, pytest-cov, pytest-timeout

**Local execution:**
```bash
make test           # Run all tests
make smoke          # Run smoke tests only
```

---

### 3. Quiz Validation

**Purpose:** Ensure quiz files are valid and properly structured.

**Checks:**
- YAML syntax validation
- JSON syntax validation
- Required fields present
- Minimum question count (5+)

**Local execution:**
```bash
make validate       # Validate quiz files
```

---

### 4. Docker Build

**Purpose:** Verify Docker configuration.

**Local execution:**
```bash
make docker-up      # Start environment
make docker-down    # Stop environment
```

---

### 5. Security Scan

**Purpose:** Identify potential security vulnerabilities.

**Tools:** Bandit, pip-audit

**Local execution:**
```bash
pip install bandit
bandit -r src/ scripts/ formative/ -ll -ii
```

---

## Running CI Locally

```bash
# Full CI pipeline
make ci

# Individual steps
make lint
make test
make validate
```

---

## Troubleshooting CI Failures

### Lint Failures
```bash
ruff check src/ --output-format=full
ruff check --fix src/
```

### Test Failures
```bash
pytest tests/ -v --tb=long
```

### Quiz Validation Failures
```bash
python -c "import yaml; yaml.safe_load(open('formative/quiz.yaml'))"
python -c "import json; json.load(open('formative/quiz.json'))"
```

---

*NETWORKING class — ASE, CSIE | Computer Networks Laboratory*  
*CI Setup Guide v1.0.0 | January 2026*
