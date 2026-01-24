# CI/CD Setup Guide — Week 5 Laboratory Kit

> Computer Networks Laboratory — ASE-CSIE Bucharest
>
> Continuous Integration and Automated Testing

---

## Overview

The CI pipeline automatically validates:

- Python syntax and code quality
- Unit tests and smoke tests
- Quiz YAML format
- Docker build
- Documentation completeness

---

## Pipeline Architecture

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│   Lint   │───▶│   Test   │───▶│   Quiz   │───▶│  Docker  │
│  (ruff)  │    │ (pytest) │    │ Validate │    │  Build   │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
```

---

## Local CI Simulation

Run the full CI pipeline locally before pushing:

```bash
# Run complete CI locally
make ci

# Or run individual steps
make check-python    # Syntax check
make lint            # Code linting
make smoke           # Smoke tests
make unit            # Unit tests
make quiz-validate   # Quiz YAML validation
make docs-check      # Documentation check
```

---

## Linting Configuration

The project uses `ruff` for linting, configured in `pyproject.toml`:

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B"]
ignore = ["E501", "E402"]
```

### Running Linter

```bash
# Check for issues
ruff check src/ scripts/ tests/

# Auto-fix issues
ruff check --fix src/ scripts/ tests/
```

---

## Test Configuration

Tests are configured in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = ["-v", "--tb=short"]
```

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make coverage

# Run specific test file
python -m pytest tests/test_exercises.py -v
```

---

## Quiz Validation

The quiz YAML is validated for:

- Valid YAML syntax
- Required metadata fields
- Question structure
- Correct answer format

```bash
# Validate quiz
make quiz-validate

# Or manually
python -c "
import yaml
quiz = yaml.safe_load(open('formative/quiz.yaml'))
assert 'metadata' in quiz
assert 'questions' in quiz
print(f'Valid: {len(quiz[\"questions\"])} questions')
"
```

---

## Support

If CI issues persist:

1. Check the Actions tab in GitHub for detailed logs
2. Run `make ci` locally to reproduce
3. Review recent changes that may have caused failures
4. Open an issue in GitHub with CI logs attached

---

*Week 5: IP Addressing, Subnetting and VLSM — CI/CD Setup Guide*
*Computer Networks Laboratory — ASE-CSIE Bucharest*
