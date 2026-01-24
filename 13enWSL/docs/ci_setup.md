# 🔄 CI/CD Setup Guide

> Week 13: IoT and Security in Computer Networks  
> NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

---

## Overview

This guide explains how to set up Continuous Integration (CI) for the Week 13 laboratory kit using GitHub Actions. The CI pipeline ensures code quality, validates documentation and catches errors before they reach students.

---

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        GitHub Actions Workflow                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────┐    ┌─────────┐    ┌─────────────┐    ┌────────┐           │
│  │  Lint   │───▶│ Syntax  │───▶│Ground Truth │───▶│  Test  │           │
│  │ (ruff)  │    │ (py,yml)│    │ Validation  │    │(pytest)│           │
│  └─────────┘    └─────────┘    └─────────────┘    └────────┘           │
│       │              │               │                 │                │
│       ▼              ▼               ▼                 ▼                │
│  Code style    File validity   Documentation     Functionality         │
│   checks         checks          accuracy          verification        │
│                                                                         │
│                              ┌──────────┐                               │
│                              │  Docker  │  (Optional)                   │
│                              │  Build   │                               │
│                              └──────────┘                               │
│                                   │                                     │
│                                   ▼                                     │
│                           Container validity                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Workflow File Location

The CI workflow is defined in:

```
.github/workflows/ci.yml
```

---

## Pipeline Stages

### Stage 1: Lint (Code Quality)

**Purpose:** Ensure code follows Python best practices and style guidelines.

**Tools:** ruff (fast Python linter)

**Checks:**
- PEP 8 style compliance (E, W rules)
- Import sorting (I rules)
- Naming conventions (N rules)
- Docstring presence (D rules)
- Common bugs (B rules)

**Local execution:**
```bash
make lint
# or
ruff check src/ scripts/ tests/ formative/
```

**Configuration:** See `pyproject.toml` section `[tool.ruff]`

---

### Stage 2: Syntax Validation

**Purpose:** Verify all source files are syntactically valid.

**Checks:**
- Python files compile without errors
- YAML files parse correctly
- JSON files are valid

**Local execution:**
```bash
# Python syntax
find . -name "*.py" -exec python -m py_compile {} \;

# YAML validation
python -c "import yaml; yaml.safe_load(open('formative/quiz.yaml'))"

# JSON validation
python -c "import json; json.load(open('tests/ground_truth.json'))"
```

---

### Stage 3: Ground Truth Validation

**Purpose:** Ensure documentation matches actual kit contents.

**Checks:**
- Python version requirements
- Exercise file existence and line counts
- Port configurations in docker-compose
- Quiz structure and question counts
- Learning objective coverage

**Local execution:**
```bash
make validate
# or
python tests/validate_ground_truth.py
```

**Output:**
```
══════════════════════════════════════════════════════════════════════════
  Ground Truth Validation Report
══════════════════════════════════════════════════════════════════════════

  ✅ PASS  Python Version
         Expected: >= 3.11
         Actual:   3.11

  ✅ PASS  Exercise ex_13_01 line count
         Expected: 582 ± 58
         Actual:   585
  
  ...
  
  ✅ ALL VALIDATIONS PASSED
```

---

### Stage 4: Unit Tests

**Purpose:** Verify exercise functionality and test coverage.

**Checks:**
- Exercise help flags work
- Smoke tests pass
- Unit tests pass (when services available)

**Local execution:**
```bash
make test
# or
python -m pytest tests/ -v
```

**Test categories:**

| Marker | Description | Requires |
|--------|-------------|----------|
| (none) | Basic tests | Python only |
| `@pytest.mark.integration` | Docker tests | Running services |
| `@pytest.mark.network` | Network tests | Network access |
| `@pytest.mark.slow` | Long-running tests | Time |

---

### Stage 5: Docker Build (Optional)

**Purpose:** Validate container configurations.

**Checks:**
- Custom Dockerfiles build successfully
- docker-compose.yml is valid
- Images can be pulled

**Local execution:**
```bash
docker compose -f docker/docker-compose.yml config --quiet
docker compose -f docker/docker-compose.yml build
```

---

## Trigger Conditions

The pipeline runs on:

| Event | Condition |
|-------|-----------|
| Push | To `main` or `develop` branches |
| Pull Request | Targeting `main` branch |
| Manual | Via "Run workflow" button |

**Path filters:** Only triggers when files in `13enWSL/` change.

---

## Setting Up GitHub Actions

### Step 1: Create Workflow Directory

```bash
mkdir -p .github/workflows
```

### Step 2: Copy Workflow File

The workflow file is already provided at `.github/workflows/ci.yml`.

### Step 3: Configure Repository Secrets (Optional)

If using private Docker images:

1. Go to repository **Settings → Secrets → Actions**
2. Add `DOCKER_USERNAME` and `DOCKER_PASSWORD`

### Step 4: Enable Actions

1. Go to repository **Settings → Actions → General**
2. Select "Allow all actions and reusable workflows"
3. Save

---

## Local CI Simulation

Run the same checks locally before pushing:

```bash
# Full CI simulation
make all

# Individual stages
make lint      # Stage 1
make verify    # Stages 2-3
make test      # Stage 4
```

---

## Linting Configuration

### Ruff Configuration (pyproject.toml)

```toml
[tool.ruff]
target-version = "py311"
line-length = 100

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "F",      # Pyflakes
    "W",      # pycodestyle warnings
    "I",      # isort
    "N",      # pep8-naming
    "D",      # pydocstyle
    "UP",     # pyupgrade
    "B",      # flake8-bugbear
]

ignore = [
    "D100",   # Missing docstring in public module
    "D104",   # Missing docstring in public package
]
```

### Running Lint with Auto-fix

```bash
# Check only
ruff check src/

# Auto-fix safe issues
ruff check src/ --fix

# Format code
ruff format src/
```

---

## Common CI Failures and Fixes

### "Lint failed: E501 line too long"

**Fix:** Break long lines or increase line-length in pyproject.toml

```python
# Before
result = some_very_long_function_name(argument1, argument2, argument3, argument4)

# After
result = some_very_long_function_name(
    argument1, argument2, argument3, argument4
)
```

### "Syntax: YAML parse error"

**Fix:** Check YAML indentation (use spaces, not tabs)

```yaml
# Wrong
questions:
	- id: q01  # TAB character

# Correct
questions:
  - id: q01   # 2 spaces
```

### "Ground truth: Exercise line count mismatch"

**Fix:** Update `tests/ground_truth.json` after significant code changes

```bash
# Check actual line count
wc -l src/exercises/ex_13_01_port_scanner.py

# Update ground_truth.json accordingly
```

### "Test failed: ModuleNotFoundError"

**Fix:** Install missing dependencies

```bash
pip install -r setup/requirements.txt
```

---

## CI Badge

Add this badge to your README:

```markdown
![CI Status](https://github.com/antonioclim/netENwsl/actions/workflows/ci.yml/badge.svg)
```

---

## Monitoring CI Runs

### View Run History

1. Go to repository **Actions** tab
2. Click on workflow name
3. View individual runs

### Download Artifacts

Test reports and validation results are uploaded as artifacts:

1. Click on completed run
2. Scroll to "Artifacts" section
3. Download `validation-report` or `test-report`

---

## Best Practices

1. **Run locally first:** Use `make all` before pushing
2. **Small commits:** Easier to identify which change broke CI
3. **Fix immediately:** Do not let failures accumulate
4. **Update ground truth:** Keep documentation accurate
5. **Review warnings:** Even non-failing issues deserve attention

---

## Troubleshooting

### "Workflow not triggering"

- Check path filters in workflow file
- Verify branch names match
- Check Actions are enabled in repository settings

### "Permission denied in workflow"

- Check `permissions` section in workflow file
- Ensure required secrets are configured

### "Docker build timeout"

- Increase timeout in workflow file
- Use smaller base images
- Enable Docker layer caching

---

*Computer Networks — Week 13: IoT and Security*  
*ASE Bucharest, CSIE | by ing. dr. Antonio Clim*
