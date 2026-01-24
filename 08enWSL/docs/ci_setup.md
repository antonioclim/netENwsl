# CI/CD Setup Guide — Week 8 Laboratory

> Computer Networks — ASE, CSIE

This document explains the Continuous Integration (CI) pipeline configuration
and how to set it up for your own repository.

---

## Overview

The CI pipeline automatically validates code quality on every push and pull request:

| Stage | Tool | Purpose |
|-------|------|---------|
| Syntax | py_compile | Verify all Python files are syntactically correct |
| Linting | ruff | Enforce code style and catch common errors |
| Type Checking | mypy | Validate type annotations |
| Unit Tests | pytest | Verify exercise implementations |
| Docker Build | docker compose | Ensure containers build correctly |
| Documentation | custom | Verify required files exist |

---

## GitHub Actions Workflow

The workflow file is located at `.github/workflows/ci.yml`.

### Trigger Events

```yaml
on:
  push:
    branches: [main, develop, "week*"]
  pull_request:
    branches: [main]
  workflow_dispatch:  # Manual trigger
```

### Jobs

1. **lint** — Runs ruff linter and mypy type checker
2. **test** — Runs pytest on unit tests
3. **docker** — Builds and tests Docker containers
4. **docs** — Validates documentation files exist
5. **status** — Aggregates results from all jobs

---

## Local Development

### Running CI Checks Locally

Before pushing use the Makefile targets to run the same checks:

```bash
# Syntax check
make ci-syntax

# Linting
make lint

# Tests
make test

# Docker validation
make ci-docker
```

### Installing CI Tools

```bash
pip install ruff mypy pytest pytest-asyncio
```

---

## Linting Configuration

Linting is configured in `pyproject.toml`:

```toml
[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP", "SIM"]
ignore = ["E501"]  # Line length handled separately
```

### Key Rules

| Code | Meaning |
|------|---------|
| E | pycodestyle errors |
| W | pycodestyle warnings |
| F | Pyflakes (undefined names, unused imports) |
| I | isort (import sorting) |
| B | flake8-bugbear (common bugs) |
| C4 | flake8-comprehensions |
| UP | pyupgrade (modern Python syntax) |
| SIM | flake8-simplify |

### Fixing Lint Errors

```bash
# Show errors
make lint

# Auto-fix what can be fixed
make lint-fix

# Format code
make format
```

---

## Type Checking

Type hints are checked with mypy:

```bash
make typecheck
```

Configuration in `pyproject.toml`:

```toml
[tool.mypy]
python_version = "3.10"
warn_return_any = true
ignore_missing_imports = true
```

---

## Test Configuration

Tests use pytest with configuration in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = ["-v", "--tb=short"]
```

### Running Specific Tests

```bash
# All tests
make test

# Exercise 1 only
make test-ex1

# Exercise 2 only
make test-ex2

# Smoke tests only
make smoke
```

---

## Docker Validation

The CI pipeline verifies:

1. `docker-compose.yml` syntax is valid
2. All images build successfully
3. Containers start and pass health checks

```bash
# Validate locally
make ci-docker
```

---

## Setting Up CI for Your Fork

1. **Fork the repository** on GitHub

2. **Enable GitHub Actions**:
   - Go to repository Settings → Actions → General
   - Select "Allow all actions and reusable workflows"

3. **Push to trigger CI**:
   ```bash
   git push origin main
   ```

4. **Check results**:
   - Go to Actions tab in your repository
   - Click on the latest workflow run

---

## Troubleshooting CI Failures

### Lint Failures

```
Error: ruff check found issues
```

**Solution:** Run `make lint-fix` locally and commit the fixes.

### Test Failures

```
Error: pytest returned non-zero exit code
```

**Solution:** Run `make test` locally to see detailed error messages.

### Docker Build Failures

```
Error: docker compose build failed
```

**Solution:** 
1. Check `docker-compose.yml` syntax with `make ci-docker`
2. Ensure Dockerfiles exist and are valid
3. Check for missing files referenced in volumes

### Documentation Failures

```
Error: Missing required file
```

**Solution:** Ensure all required documentation files exist:
- README.md
- CHANGELOG.md
- docs/learning_objectives.md
- docs/troubleshooting.md
- formative/quiz.yaml

---

## Badge (Optional)

Add a CI status badge to your README:

```markdown
![CI](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/Lab%20CI/badge.svg)
```

---

## Support

For issues with the CI pipeline:

- Check the workflow logs in the Actions tab
- Review this documentation
- Open an issue in GitHub

---

*Computer Networks — ASE, CSIE*
