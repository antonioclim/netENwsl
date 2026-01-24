# CI/CD Setup Guide — Week 3 Laboratory Kit

> NETWORKING class - ASE, CSIE | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

---

## Overview

This document describes the Continuous Integration and Continuous Deployment (CI/CD) pipeline for the Week 3 laboratory kit. The pipeline ensures code quality, validates educational materials and runs automated tests.

---

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          GitHub Actions Workflow                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐        │
│  │  lint-and-      │    │  validate-      │    │  docs-check     │        │
│  │  syntax         │    │  structure      │    │                 │        │
│  │                 │    │                 │    │                 │        │
│  │  • Ruff linter  │    │  • Quiz schema  │    │  • Required     │        │
│  │  • py_compile   │    │  • LO matrix    │    │    docs exist   │        │
│  │  • YAML valid   │    │  • Checksums    │    │  • Link check   │        │
│  │  • JSON valid   │    │                 │    │  • Statistics   │        │
│  └────────┬────────┘    └────────┬────────┘    └─────────────────┘        │
│           │                      │                                         │
│           └──────────┬───────────┘                                         │
│                      │                                                     │
│                      ▼                                                     │
│  ┌─────────────────────────────────────────────────────────────────┐      │
│  │                        test-unit                                 │      │
│  │                                                                  │      │
│  │  • pytest (non-Docker tests)                                    │      │
│  │  • Quiz validation                                              │      │
│  │  • LMS export generation                                        │      │
│  └─────────────────────────────────┬───────────────────────────────┘      │
│                                    │                                       │
│                                    ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────┐      │
│  │                       test-docker                                │      │
│  │                                                                  │      │
│  │  • Build Docker images                                          │      │
│  │  • Start containers                                             │      │
│  │  • Run smoke tests                                              │      │
│  │  • Run exercise tests                                           │      │
│  │  • Cleanup                                                      │      │
│  └─────────────────────────────────────────────────────────────────┘      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Jobs Description

### 1. lint-and-syntax

**Purpose:** Ensure code quality and syntax correctness

**Checks performed:**
- **Ruff linter:** Static analysis for Python code style and potential bugs
- **py_compile:** Verify all Python files have valid syntax
- **YAML validation:** Ensure quiz.yaml and other YAML files are parseable
- **JSON validation:** Verify JSON files are well-formed

**Triggers on:** Push to main/develop, Pull requests

### 2. validate-structure

**Purpose:** Validate educational content structure

**Checks performed:**
- **Quiz schema validation:** Verify quiz.yaml matches expected structure
- **LO traceability:** Confirm all Learning Objectives are documented
- **Checksums verification:** Ensure critical files have not been corrupted

**Dependencies:** Runs in parallel with lint-and-syntax

### 3. test-unit

**Purpose:** Run unit tests that do not require Docker

**Tests executed:**
- Environment validation tests
- Quiz loader and validator
- LMS export functionality (Moodle GIFT, Canvas QTI, JSON)

**Dependencies:** Requires lint-and-syntax and validate-structure to pass

### 4. test-docker

**Purpose:** Run integration tests with full Docker environment

**Steps:**
1. Validate docker-compose.yml syntax
2. Build Docker images
3. Start containers (server, router, client, receiver)
4. Run smoke tests (connectivity, port availability)
5. Run exercise tests (broadcast, multicast, tunnel)
6. Show logs on failure
7. Cleanup containers and volumes

**Dependencies:** Requires lint-and-syntax and validate-structure to pass

### 5. docs-check

**Purpose:** Verify documentation completeness

**Checks performed:**
- Required documentation files exist
- Internal links are valid
- Documentation statistics reported

---

## Configuration Files

### .github/workflows/week3-ci.yml

Main workflow file defining all CI jobs.

**Key settings:**
```yaml
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  workflow_dispatch:  # Manual trigger

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

### pyproject.toml

Tool configurations for Ruff, mypy, pytest and coverage.

**Ruff configuration highlights:**
```toml
[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP", "ARG", "SIM", "TCH", "PTH", "RUF", "D"]
```

**mypy strict mode:**
```toml
[tool.mypy]
disallow_untyped_defs = true
check_untyped_defs = true
strict_equality = true
```

### .pre-commit-config.yaml

Local pre-commit hooks for developers.

**Hooks included:**
- trailing-whitespace
- end-of-file-fixer
- check-yaml
- check-json
- ruff (linter and formatter)
- python-syntax-check
- quiz-validation

---

## Running CI Locally

### Simulate Full CI Pipeline

```bash
# Install development dependencies
pip install -r setup/requirements.txt
pip install ruff pytest pytest-cov mypy pre-commit

# Run linting
make lint

# Run syntax check
make syntax-check

# Validate structure
make validate

# Run unit tests
make test-unit

# Run full CI with Docker
make ci-full
```

### Individual Checks

```bash
# Lint only
ruff check src/ scripts/ formative/ tests/

# Type check
mypy src/ scripts/

# Quiz validation
python formative/run_quiz.py --validate

# Docker tests
make docker-up
make test-exercises
make docker-down
```

---

## Setting Up CI for a Fork

### GitHub Actions (Recommended)

1. Fork the repository
2. GitHub Actions is automatically enabled
3. Push to trigger the workflow

### Self-Hosted Runner

For local CI runners:

```bash
# Install GitHub Actions runner
# Follow: https://docs.github.com/en/actions/hosting-your-own-runners

# Ensure Docker is available
docker --version

# Ensure Python 3.11+ is installed
python3 --version
```

---

## Troubleshooting CI Failures

### Lint Failures

```bash
# Check specific errors
ruff check src/ --output-format=full

# Auto-fix where possible
ruff check src/ --fix
```

### Test Failures

```bash
# Run with verbose output
pytest tests/ -v --tb=long

# Run specific test
pytest tests/test_exercises.py::TestExercise1Broadcast -v
```

### Docker Failures

```bash
# Check container logs
docker compose -f docker/docker-compose.yml logs

# Rebuild images
docker compose -f docker/docker-compose.yml build --no-cache

# Check network
docker network inspect week3_network
```

---

## Badge Integration

Add CI status badge to README:

```markdown
[![CI](https://github.com/YOUR_USERNAME/week3-lab/actions/workflows/week3-ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/week3-lab/actions/workflows/week3-ci.yml)
```

---

## Further Reading

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [pytest Documentation](https://docs.pytest.org/)
- [Docker Compose Reference](https://docs.docker.com/compose/)

---

*NETWORKING class - ASE, CSIE | by ing. dr. Antonio Clim*
*Week 3: Network Programming — Broadcast, Multicast and TCP Tunnelling*
