# 🔄 CI/CD Setup Guide — Week 11
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> This document explains the Continuous Integration pipeline configuration.

---

## Overview

The Week 11 Lab Kit includes a GitHub Actions CI pipeline that automatically validates:

- Python syntax and code quality
- Docker Compose configuration
- Quiz content (YAML and JSON formats)
- Security best practices

---

## Pipeline Structure

```
.github/workflows/ci.yml
├── lint-and-test      # Python validation
├── docker-validate    # Docker config validation
├── quiz-validate      # Quiz content validation
└── security-check     # Security scanning
```

---

## Jobs Explained

### 1. Lint and Test

**Purpose:** Ensure Python code quality and correctness.

**Steps:**
1. Syntax check all Python files
2. Run ruff linter with project configuration
3. Execute smoke tests
4. Run pytest unit tests

**Configuration:** `setup/ruff.toml`

### 2. Docker Validate

**Purpose:** Verify Docker configuration validity.

**Steps:**
1. Validate `docker-compose.yml` syntax
2. Check `nginx.conf` syntax using nginx:alpine

### 3. Quiz Validate

**Purpose:** Ensure quiz content is correctly formatted.

**Steps:**
1. Parse and validate `quiz.yaml` structure
2. Parse and validate `quiz.json` (LMS export)
3. Verify quiz runner functionality

### 4. Security Check

**Purpose:** Identify potential security issues.

**Steps:**
1. Scan for hardcoded credentials
2. Verify `.env` is gitignored
3. Audit dependencies for known vulnerabilities

---

## Triggering the Pipeline

The CI pipeline runs on:

- **Push** to `main` or `develop` branches
- **Pull requests** targeting `main`
- Only when relevant files change (`.py`, `.yaml`, `.yml`, `.json`, `docker/`)

---

## Local Verification

Run these commands locally before pushing:

```bash
# Syntax check
make syntax

# Lint
make lint

# Tests
make test

# Full validation
make verify
```

---

## Configuration Files

### Ruff Linter (`setup/ruff.toml`)

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N"]
ignore = ["E501"]  # Line length handled separately
```

### Requirements (`setup/requirements.txt`)

Development dependencies for CI:
- `ruff` — Linting
- `pytest` — Testing
- `mypy` — Type checking

---

## Viewing Results

### GitHub Actions

1. Navigate to repository → **Actions** tab
2. Select the workflow run
3. Expand job logs to see details

### Local Output

```bash
# View lint results
make lint 2>&1 | head -50

# View test results
make test 2>&1 | tail -20
```

---

## Troubleshooting

### Pipeline Fails on Lint

```bash
# Run locally to see specific issues
ruff check src/ scripts/ --config setup/ruff.toml

# Auto-fix simple issues
ruff check src/ scripts/ --fix
```

### Pipeline Fails on Docker

```bash
# Validate compose file
docker compose -f docker/docker-compose.yml config

# Test nginx config
docker run --rm -v $(pwd)/docker/configs/nginx.conf:/etc/nginx/nginx.conf:ro nginx:alpine nginx -t
```

### Pipeline Fails on Quiz

```bash
# Validate YAML
python -c "import yaml; yaml.safe_load(open('formative/quiz.yaml'))"

# Validate JSON
python -c "import json; json.load(open('formative/quiz.json'))"
```

---

## Extending the Pipeline

To add new validation steps:

1. Edit `.github/workflows/ci.yml`
2. Add new step under appropriate job
3. Test locally first
4. Commit and push

Example: Adding a documentation check

```yaml
- name: Check documentation links
  run: |
    # Find broken internal links
    grep -roh '\[.*\](.*\.md)' docs/ | grep -v http
```

---

## Best Practices

1. **Run locally first** — Use `make verify` before pushing
2. **Fix warnings** — Even non-blocking warnings should be addressed
3. **Keep dependencies updated** — Regular `pip-audit` checks
4. **Review security alerts** — Address any flagged issues promptly

---

## Support

Issues: Open an issue in GitHub

---

*NETWORKING class - ASE, CSIE | Computer Networks Laboratory*  
*Week 11: Application Protocols — FTP, DNS, SSH and Load Balancing*
