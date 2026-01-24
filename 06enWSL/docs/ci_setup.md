# 🔧 CI/CD Setup Guide — Week 6 Laboratory

> Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

## Overview

This document explains how to set up and use the Continuous Integration (CI) pipeline for the Week 6 laboratory kit.

---

## CI Pipeline Structure

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs automatically on:
- Every push to `main`, `develop` or `master` branches
- Every pull request targeting these branches
- Manual trigger via GitHub Actions UI

### Jobs

| Job | Purpose | Required |
|-----|---------|----------|
| `quality` | Syntax checking and linting | Yes |
| `smoke-tests` | Basic functionality tests | Yes |
| `quiz-validation` | Quiz YAML/JSON validation | Yes |
| `docs-validation` | Documentation completeness | No (warning only) |
| `integrity` | Checksum verification (PRs only) | No |
| `ci-summary` | Final status report | Yes |

---

## Local CI Execution

Run the full CI pipeline locally before pushing:

```bash
# Using Make
make ci

# Or manually
python -m py_compile $(find . -name "*.py")
ruff check src/ scripts/ --ignore E501
python tests/smoke_test.py
python -c "import yaml; yaml.safe_load(open('formative/quiz.yaml'))"
```

---

## Linting Configuration

### Ruff (Primary Linter)

Configuration in `pyproject.toml`:

```toml
[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # Pyflakes
    "I",    # isort
    "B",    # flake8-bugbear
    "C4",   # flake8-comprehensions
    "UP",   # pyupgrade
    "SIM",  # flake8-simplify
]
ignore = [
    "E501",  # Line too long (handled by formatter)
    "B008",  # Function call in default argument
]
```

### Running Ruff

```bash
# Check for issues
ruff check src/ scripts/ tests/

# Auto-fix issues
ruff check --fix src/ scripts/

# Format code
ruff format src/ scripts/
```

---

## Type Checking (MyPy)

Configuration in `pyproject.toml`:

```toml
[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
ignore_missing_imports = true
```

### Running MyPy

```bash
mypy src/ scripts/ --ignore-missing-imports
```

---

## Setting Up CI for Your Fork

1. **Fork the repository** on GitHub

2. **Enable GitHub Actions**:
   - Go to your fork's Settings → Actions → General
   - Select "Allow all actions and reusable workflows"

3. **Verify CI runs**:
   - Make any change and push
   - Check the Actions tab for workflow status

---

## CI Badge

Add this badge to your README to show CI status:

```markdown
![CI Status](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/ci.yml/badge.svg)
```

---

## Troubleshooting CI Failures

### Syntax Errors

```
Error: Syntax error in src/exercises/ex_6_01_nat_topology.py
```

**Fix:** Check the file for Python syntax errors:
```bash
python -m py_compile src/exercises/ex_6_01_nat_topology.py
```

### Missing Dependencies

```
ModuleNotFoundError: No module named 'yaml'
```

**Fix:** Install dependencies:
```bash
pip install pyyaml --break-system-packages
```

### Quiz Validation Failures

```
Warning: Question count mismatch in metadata
```

**Fix:** Update `total_questions` in `formative/quiz.yaml` metadata to match actual question count.

### Documentation Missing

```
Warning: MISSING: docs/theory_summary.md
```

**Fix:** Create the missing file or update the CI configuration if intentionally removed.

---

## Adding New CI Checks

To add a new validation step:

1. Edit `.github/workflows/ci.yml`
2. Add a new step to an existing job or create a new job
3. Test locally first using `make ci`

Example: Adding a spell checker:

```yaml
- name: Spell check documentation
  run: |
    pip install codespell
    codespell docs/ --skip="*.yaml,*.json"
  continue-on-error: true
```

---

## CI Environment

The CI runs on:
- **OS:** Ubuntu Latest
- **Python:** 3.11
- **Package manager:** pip with caching

Available in the environment:
- ruff (linting)
- mypy (type checking)
- pyyaml (YAML parsing)
- pytest (testing framework)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-24 | Initial CI pipeline |

---

*Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim*
*Contact: Issues: Open an issue in GitHub*
