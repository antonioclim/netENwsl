# Week 13: IoT and Security — CI/CD Setup

**Computer Networks** — ASE, CSIE | ing. dr. Antonio Clim

---

## Overview

This document describes the continuous integration and continuous deployment (CI/CD) pipeline for the Week 13 laboratory materials. The pipeline automates testing, validation, and deployment to ensure material quality.

---

## Pipeline Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Commit    │───▶│   Lint &    │───▶│    Unit     │───▶│   Deploy    │
│   Push      │    │   Format    │    │   Tests     │    │   Artefact  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

---

## GitHub Actions Workflow

### Trigger Events

The pipeline runs on:
- Push to `main` or `develop` branches
- Pull requests targeting `main`
- Manual dispatch via workflow_dispatch

### Job Definitions

#### 1. Lint Job

Validates code style and formatting:

```yaml
lint:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: pip install flake8 black isort
    - name: Run flake8
      run: flake8 src/ formative/ tests/ --max-line-length=100
    - name: Check formatting
      run: black --check src/ formative/ tests/
    - name: Check imports
      run: isort --check-only src/ formative/ tests/
```

#### 2. Test Job

Executes unit tests and validates exports:

```yaml
test:
  runs-on: ubuntu-latest
  needs: lint
  steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: pip install -r setup/requirements.txt
    - name: Run unit tests
      run: python -m pytest tests/ -v --tb=short
    - name: Validate quiz exports
      run: |
        python formative/run_quiz.py --export-moodle /tmp/quiz.xml
        python formative/run_quiz.py --export-canvas /tmp/quiz.json
```

#### 3. Deploy Job

Creates release artefacts:

```yaml
deploy:
  runs-on: ubuntu-latest
  needs: test
  if: github.ref == 'refs/heads/main'
  steps:
    - uses: actions/checkout@v4
    - name: Create release archive
      run: |
        zip -r 13enWSL.zip . -x "*.git*" -x "__pycache__/*"
    - name: Upload artefact
      uses: actions/upload-artifact@v4
      with:
        name: week13-materials
        path: 13enWSL.zip
```

---

## Local Development

### Running Tests Locally

```bash
# Install test dependencies
pip install pytest pyyaml

# Run all tests
python -m pytest tests/ -v

# Run specific test module
python -m pytest tests/test_quiz_exports.py -v

# Run with coverage
pip install pytest-cov
python -m pytest tests/ --cov=formative --cov-report=html
```

### Linting Locally

```bash
# Install linters
pip install flake8 black isort

# Run linters
flake8 src/ formative/ tests/ --max-line-length=100
black --check src/ formative/ tests/
isort --check-only src/ formative/ tests/

# Auto-fix formatting
black src/ formative/ tests/
isort src/ formative/ tests/
```

### Using Make Targets

The Makefile provides convenience targets:

```bash
make lint          # Run all linters
make test          # Run unit tests
make test-exports  # Test LMS exports
make quiz-moodle   # Export Moodle XML
make quiz-canvas   # Export Canvas JSON
make all           # Full verification
```

---

## Quality Gates

### Required Checks

All pull requests must pass:

| Check | Threshold | Tool |
|-------|-----------|------|
| Lint (flake8) | 0 errors | flake8 |
| Format (black) | Conformant | black |
| Import order | Conformant | isort |
| Unit tests | 100% pass | pytest |
| Export validation | Valid XML/JSON | Custom |

### Code Coverage

Minimum coverage requirements:

| Module | Minimum |
|--------|---------|
| formative/ | 80% |
| src/exercises/ | 70% |
| tests/ | N/A |

---

## Environment Variables

### CI Environment

| Variable | Description | Default |
|----------|-------------|---------|
| `PYTHONDONTWRITEBYTECODE` | Prevent .pyc files | `1` |
| `PYTEST_ADDOPTS` | Additional pytest options | `--tb=short` |

### Docker Environment

For local Docker testing:

```bash
docker build -t week13-tests -f Dockerfile.test .
docker run --rm week13-tests pytest tests/ -v
```

---

## Troubleshooting

### Common Issues

**Test Discovery Failures**

Ensure `__init__.py` files exist in all Python directories:

```bash
touch tests/__init__.py formative/__init__.py
```

**YAML Parsing Errors**

Validate quiz.yaml syntax:

```bash
python -c "import yaml; yaml.safe_load(open('formative/quiz.yaml'))"
```

**Import Errors**

Ensure PYTHONPATH includes project root:

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

---

## Release Process

1. **Create release branch**: `git checkout -b release/v2.0`
2. **Update version**: Bump version in `quiz.yaml` metadata
3. **Run full validation**: `make all`
4. **Create PR**: Merge to `main` via pull request
5. **Tag release**: `git tag -a v2.0 -m "Week 13 v2.0"`
6. **Push tag**: `git push origin v2.0`

The pipeline automatically creates release artefacts upon tag push.

---

## Security Considerations

### Secrets Management

- No secrets stored in repository
- Docker credentials via GitHub Secrets
- API keys via environment variables

### Dependency Scanning

Enable Dependabot for automated vulnerability alerts:

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/setup"
    schedule:
      interval: "weekly"
```

---

*Document version: 2.0 | Language: en-GB | Last updated: January 2026*
