# 🔄 Continuous Integration Setup Guide — Week 7
## Computer Networks — ASE, CSIE | Computer Networks Laboratory

> This document explains how to set up and use the CI/CD pipeline for the
> Week 7 laboratory kit.

---

## Overview

The CI pipeline automatically validates the laboratory kit on every push:

- **Syntax checking** — Validates Python files compile correctly
- **Linting** — Checks code style with ruff
- **Unit tests** — Runs pytest test suite
- **Configuration validation** — Validates YAML/JSON files
- **Docker verification** — Tests docker-compose configuration
- **PCAP generation** — Creates sample capture files
- **Quiz export** — Generates LMS-compatible quiz formats

---

## Prerequisites

### Local Development

```bash
# Install development dependencies
pip install -r setup/requirements-dev.txt

# Verify installation
ruff --version
pytest --version
```

### GitHub Actions

The CI workflow runs automatically on GitHub. No additional setup required
if using the default `.github/workflows/ci.yml` configuration.

---

## Running CI Locally

### Full Pipeline

```bash
# Run complete CI pipeline
make ci
```

This executes:
1. Syntax validation
2. Linting
3. Smoke tests
4. Full test suite

### Individual Steps

```bash
# Syntax check only
make syntax-check

# Linting only
make lint

# Tests only
make pytest

# Format check
make format-check
```

---

## GitHub Actions Configuration

### Workflow Location

```
.github/workflows/ci.yml
```

### Trigger Events

The CI workflow runs on:

| Event | Branches | Conditions |
|-------|----------|------------|
| Push | main, develop, feature/** | Python/YAML/JSON changes |
| Pull Request | main, develop | All changes |
| Manual | Any | workflow_dispatch |

### Job Structure

```
┌─────────────────────────────────────────────────────────┐
│                    CI PIPELINE                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   lint ────────────────┐                                │
│                        │                                │
│   validate-config ─────┼───► ci-summary                 │
│                        │                                │
│   docker ──────────────┤                                │
│                        │                                │
│   test ────────────────┤                                │
│                        │                                │
│   pcap ────────────────┤                                │
│                        │                                │
│   quiz-export ─────────┘                                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Artifacts Generated

| Artifact | Description | Retention |
|----------|-------------|-----------|
| test-results | JUnit XML test report | 30 days |
| pcap-samples | Generated PCAP files | 30 days |
| quiz-exports | Moodle/Canvas quiz files | 30 days |

---

## Linting Configuration

### Ruff Settings

Configuration in `pyproject.toml`:

```toml
[tool.ruff]
target-version = "py311"
line-length = 100

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP", "SIM"]
ignore = ["E501", "E402", "F401"]
```

### Running Linter

```bash
# Check for issues
ruff check src/ scripts/ tests/

# Auto-fix issues
ruff check --fix src/

# Format code
ruff format src/
```

### Ignored Rules

| Rule | Reason |
|------|--------|
| E501 | Line length handled by formatter |
| E402 | Path manipulation requires imports after sys.path |
| F401 | Some imports are for re-export |

---

## Test Configuration

### pytest Settings

Configuration in `pytest.ini`:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
markers =
    exercise1: Exercise 1 tests
    exercise2: Exercise 2 tests
    slow: Tests that take >5 seconds
```

### Running Tests

```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov-report=html

# Specific exercise
pytest tests/ -m exercise1

# Skip slow tests
pytest tests/ -m "not slow"
```

---

## Troubleshooting CI Failures

### Lint Failures

```
Error: ruff check found issues
```

**Solution:**
```bash
# View issues
ruff check src/ scripts/

# Auto-fix
ruff check --fix src/ scripts/
```

### Test Failures

```
Error: pytest returned non-zero exit code
```

**Solution:**
```bash
# Run locally with verbose output
pytest tests/ -v --tb=long

# Run specific failing test
pytest tests/test_exercises.py::test_tcp_connectivity -v
```

### YAML Validation Failures

```
Error: Invalid YAML syntax
```

**Solution:**
```bash
# Validate YAML
python -c "import yaml; yaml.safe_load(open('formative/quiz.yaml'))"
```

### Docker Build Failures

```
Error: docker compose config failed
```

**Solution:**
```bash
# Validate compose file
docker compose -f docker/docker-compose.yml config

# Check Docker daemon
docker info
```

---

## Adding New CI Jobs

### Example: Adding Security Scan

1. Edit `.github/workflows/ci.yml`
2. Add new job:

```yaml
security:
  name: Security Scan
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    - run: pip install bandit
    - run: bandit -r src/ scripts/ -ll
```

3. Add to `ci-summary` needs list

---

## Best Practices

### Before Pushing

```bash
# Run full local CI
make ci

# Or at minimum
make lint
make pytest
```

### Commit Messages

Follow conventional commits for better CI integration:

```
feat: Add new quiz question for LO3
fix: Correct iptables command syntax
docs: Update troubleshooting guide
test: Add test for UDP send function
```

### Branch Strategy

| Branch | Purpose | CI Behaviour |
|--------|---------|--------------|
| main | Production-ready | Full CI + artifacts |
| develop | Integration | Full CI |
| feature/* | New features | Lint + tests only |

---

## Support

If CI issues persist:

1. Check the GitHub Actions logs for detailed error messages
2. Review recent changes that might have introduced the issue
3. Run the failing step locally with verbose output
4. Consult the troubleshooting section above

Issues: Open an issue in GitHub

---

*Computer Networks — Week 7: Packet Interception, Filtering and Defensive Port Probing*  
*ASE Bucharest, CSIE | Computer Networks Laboratory*
