# CI/CD Setup Guide — Week 12
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

This guide explains the Continuous Integration (CI) setup for Week 12.

---

## Overview

The CI pipeline automatically validates code quality on every push and pull request.

```
Push/PR  ───▶  Lint  ───▶  Test  ───▶  Docker Build (main only)
```

---

## Pipeline Stages

### Stage 1: Lint and Syntax Check

- Python syntax validation (`py_compile`)
- Code style with ruff linter
- Quiz YAML/JSON validity

### Stage 2: Unit Tests

- Environment tests (non-Docker)
- Quiz runner functionality
- Module imports

### Stage 3: Docker Build (main branch only)

- Docker image builds successfully
- Container starts and runs Python

---

## Local CI Commands

```bash
make ci           # Run full CI pipeline locally
make lint         # Run ruff linter
make syntax       # Check Python syntax
make test         # Run pytest
make quiz         # Test quiz runner
```

---

## See Also

- `.github/workflows/ci.yml` — Workflow definition
- `docs/ci/LINTING.md` — Linting configuration
- `docs/ci/PIPELINE.md` — Pipeline architecture

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
