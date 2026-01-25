# CI/CD Pipeline Documentation

> Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

This document explains the Continuous Integration pipeline for the Week 1 laboratory.

---

## Pipeline Overview

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│  LINT   │────►│  TEST   │────►│  QUIZ   │────►│ DOCKER  │
└─────────┘     └─────────┘     └─────────┘     └─────────┘
     │               │               │               │
     ▼               ▼               ▼               ▼
  ruff            pytest        validate        compose
  flake8         smoke_test      export          build
  py_compile                                      up/down
```

---

## Jobs

| Job | Purpose | Tools | Trigger |
|-----|---------|-------|---------|
| lint | Code quality and syntax | ruff, flake8, py_compile | Push/PR to main |
| test | Unit and smoke tests | pytest, smoke_test.py | After lint |
| quiz | Quiz validation and export | YAML/JSON parsing | Push/PR |
| docker | Container build and test | docker compose | After lint+test |

---

## Running Locally

### Full Pipeline

```bash
make ci
```

This runs: lint → check-emails → validate-quiz → test

### Individual Steps

```bash
make lint          # Linting only (ruff + flake8)
make format        # Auto-format code
make test          # Unit tests
make smoke         # Smoke tests only
make validate-quiz # Quiz validation
make export-quiz   # Export quiz to all formats
make check-emails  # Check for email addresses
```

---

## Configuration Files

| File | Purpose |
|------|---------|
| `.github/workflows/ci.yml` | GitHub Actions pipeline definition |
| `pyproject.toml` | Tool configuration (ruff, mypy, pytest, black) |
| `.flake8` | Flake8 linting rules |
| `.pre-commit-config.yaml` | Pre-commit hooks |
| `requirements.txt` | All dependencies including dev tools |
| `setup/requirements.txt` | Runtime dependencies only |

---

## Linting Configuration

### Ruff

Ruff handles both linting and formatting. Configuration in `pyproject.toml`:

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "W"]
ignore = ["E501"]  # Line length handled separately
```

### Flake8

Secondary linter for additional style checks. Configuration in `.flake8`:

```ini
[flake8]
max-line-length = 100
extend-ignore = E203, W503
exclude = .git, __pycache__, .venv
```

---

## Quiz Validation

The CI pipeline validates the quiz in several ways:

1. **YAML Syntax**: Ensures valid YAML structure
2. **Schema Validation**: Checks required fields and types
3. **Export Testing**: Verifies all export formats work

```bash
# Manual validation
python formative/run_quiz.py --validate

# View statistics
python formative/run_quiz.py --stats
```

---

## Troubleshooting

### Lint Failures

```bash
# See what ruff wants to change
ruff check src/ --diff

# Auto-fix issues
ruff check src/ --fix

# Format code
ruff format src/
```

### Test Failures

```bash
# Verbose output
pytest tests/ -v --tb=long

# Run specific test
pytest tests/test_formative_quiz_exports.py -v

# Show print output
pytest tests/ -v -s
```

### Docker Failures

```bash
# Check logs
docker compose -f docker/docker-compose.yml logs

# Rebuild from scratch
docker compose -f docker/docker-compose.yml build --no-cache

# Verify config
docker compose -f docker/docker-compose.yml config
```

### Email Check Failures

If the CI reports email addresses found:

```bash
# Find the offending files
grep -RInE "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}" docs/ src/

# Replace with the standard phrase
# "Issues: Open an issue in GitHub"
```

---

## Dependencies

CI installs dependencies from `requirements.txt` which includes:

- `setup/requirements.txt` (runtime dependencies) via `-r`
- Development tools: ruff, flake8, mypy, pytest, pre-commit
- JSON Schema validation for quiz

Install locally:

```bash
pip install -r requirements.txt --break-system-packages
```

---

## Support

Issues: Open an issue in GitHub

---

*NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim*
