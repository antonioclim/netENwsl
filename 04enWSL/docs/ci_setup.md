# CI/CD Setup Guide — Week 4 Laboratory Kit

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

This document explains how to set up and use the Continuous Integration (CI) pipeline for the Week 4 laboratory kit.

---

## Overview

The CI pipeline automatically validates the laboratory kit whenever changes are pushed to the repository. It ensures that all Python files have valid syntax, the quiz is properly formatted, all required artefacts exist and tests pass.

### What Gets Checked

| Check | Description | Failure Impact |
|-------|-------------|----------------|
| **Syntax** | All `.py` files compile without errors | Blocks merge |
| **Linting** | Code style (Ruff) | Warning only |
| **Quiz Schema** | `quiz.yaml` matches JSON schema | Blocks merge |
| **LMS Export** | Quiz exports to Moodle/Canvas | Blocks merge |
| **Integrity** | All LO artefacts exist | Blocks merge |
| **Manifest** | File checksums match | Blocks merge |
| **Tests** | Smoke and unit tests pass | Blocks merge |

---

## Quick Start

### For Contributors

The CI runs automatically on every push and pull request. You do not need to configure anything.

Before submitting a PR, run locally:

```bash
make pre-commit
```

This runs the same checks as CI.

### For Repository Maintainers

1. Enable GitHub Actions in your repository settings
2. The workflow file is at `.github/workflows/ci.yml`
3. No secrets or tokens are required for basic operation

---

## Pipeline Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                        CI Pipeline                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────┐   ┌──────────────────┐   ┌───────────────┐        │
│   │  Lint   │   │ Quiz Validation  │   │   Integrity   │        │
│   │         │   │                  │   │               │        │
│   │ • syntax│   │ • schema check   │   │ • LO artefacts│        │
│   │ • ruff  │   │ • LMS export     │   │ • checksums   │        │
│   └────┬────┘   └────────┬─────────┘   └───────────────┘        │
│        │                 │                                       │
│        └────────┬────────┘                                       │
│                 ▼                                                 │
│          ┌───────────┐                                           │
│          │   Tests   │                                           │
│          │           │                                           │
│          │ • smoke   │                                           │
│          │ • unit    │                                           │
│          └───────────┘                                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Local Development

### Prerequisites

```bash
pip install ruff pyyaml jsonschema pytest --break-system-packages
```

### Running Checks Locally

```bash
# Run all pre-commit checks (recommended)
make pre-commit

# Individual checks
make syntax-check      # Python syntax only
make lint              # Ruff linting
make validate-quiz     # Quiz schema validation
make verify-integrity  # Kit integrity
make verify-manifest   # File checksums
make test              # All tests
```

---

## Linting Configuration

The project uses **Ruff** for Python linting. Configuration is in `pyproject.toml`:

```toml
[tool.ruff]
target-version = "py38"
line-length = 100

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # Pyflakes
    "I",      # isort
    "N",      # pep8-naming
    "UP",     # pyupgrade
]
```

### Ignored Rules

| Rule | Reason |
|------|--------|
| `E501` | Line length handled separately |
| `E402` | Path setup requires imports after sys.path modification |

### Running Ruff Locally

```bash
# Check for issues
ruff check .

# Auto-fix issues
ruff check . --fix

# Format code
ruff format .
```

---

## Quiz Validation

The quiz is validated against a JSON schema to ensure consistency.

### Schema Location

`formative/quiz_schema.json`

### Validation Script

```bash
python scripts/validate_quiz_schema.py
```

### Common Validation Errors

| Error | Cause | Fix |
|-------|-------|-----|
| Missing `id` | Question lacks identifier | Add `id: qNN` |
| Invalid `bloom_level` | Typo in level name | Use: remember, understand, apply, analyse, evaluate, create |
| Missing `correct` | No correct answer specified | Add `correct:` field |
| Bad `misconception_ref` | Path does not exist | Check file path |

---

## LMS Export

The quiz can be exported to Learning Management System formats.

### Supported Formats

| Format | Target LMS | File Type |
|--------|------------|-----------|
| `moodle` | Moodle GIFT/XML | JSON |
| `canvas` | Canvas QTI | JSON |

### Export Commands

```bash
# Export to Moodle format
python scripts/export_quiz_lms.py --format moodle --output quiz_moodle.json

# Export to Canvas format
python scripts/export_quiz_lms.py --format canvas --output quiz_canvas.json

# Via Makefile
make export-quiz-moodle
make export-quiz-canvas
```

---

## Troubleshooting CI Failures

### Syntax Check Failed

```
ERROR: Bad syntax in file.py
```

**Solution:** Run `python -m py_compile file.py` locally to see the error.

### Quiz Validation Failed

```
ERROR: quiz.yaml validation failed
```

**Solution:** Run `python scripts/validate_quiz_schema.py` locally for details.

### Integrity Check Failed

```
ERROR: Missing artefact: docs/missing_file.md
```

**Solution:** Either create the missing file or remove it from `scripts/verify_kit_integrity.py`.

### Manifest Check Failed

```
ERROR: Checksum mismatch for file.md
```

**Solution:** If the change was intentional, run `python scripts/verify_manifest.py --update`.

---

## Adding New Checks

To add a new CI check:

1. Add a new job in `.github/workflows/ci.yml`
2. Document the check in this file
3. Add a corresponding Makefile target
4. Update the pre-commit target

Example job structure:

```yaml
new-check:
  name: My New Check
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.10'
    - run: python my_check_script.py
```

---

## Workflow Triggers

| Trigger | Branches | Condition |
|---------|----------|-----------|
| Push | main, develop | Excludes docs-only changes |
| Pull Request | main | Always |
| Manual | Any | Via Actions UI |

### Skipping CI

To skip CI on a commit, add `[skip ci]` to the commit message:

```bash
git commit -m "Update README [skip ci]"
```

---

## Support

If you encounter issues with the CI pipeline:

1. Check the Actions tab in GitHub for detailed logs
2. Run `make pre-commit` locally to reproduce
3. Issues: Open an issue in GitHub

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
*Week 4: Physical Layer, Data Link Layer & Custom Protocols*
