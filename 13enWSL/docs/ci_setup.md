# 🔄 CI/CD Setup Guide — Week 13

## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## Overview

This laboratory kit includes a GitHub Actions CI/CD pipeline that automatically validates code quality, tests and quiz syntax on every push and pull request.

---

## Pipeline Stages

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CI Pipeline Flow                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   Push/PR ──► [Lint] ──► [Test] ──► [Quiz] ──► [Docker] ──► [Summary]       │
│                 │          │          │           │             │            │
│                 ▼          ▼          ▼           ▼             ▼            │
│              ruff      smoke      YAML/JSON    Build        Report          │
│              syntax    tests      validate     images        results        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Stage 1: Lint (Code Quality)

**Purpose:** Ensure code follows Python best practices and has no syntax errors.

**Tools:**
- **ruff** — Fast Python linter (preferred)
- **py_compile** — Syntax verification fallback

**Checks performed:**
- Import ordering
- Unused variables/imports
- Line length (max 120)
- Common anti-patterns

**Configuration:** See `setup/ruff.toml`

### Stage 2: Test

**Purpose:** Verify exercise code and environment setup.

**Tests run:**
- `tests/smoke_test.py` — Basic environment checks
- `tests/test_exercises.py` — Exercise syntax and help output

**Note:** Full integration tests require Docker services and run only in `docker` stage.

### Stage 3: Quiz Validation

**Purpose:** Ensure formative assessment files are syntactically correct and complete.

**Validates:**
- `formative/quiz.yaml` — YAML syntax and required fields
- `formative/quiz_moodle.json` — JSON syntax for LMS export
- Quiz runner functionality

**Required fields per question:**
- `id` — Unique identifier
- `type` — Question type (multiple_choice, fill_blank, short_answer)
- `stem` — Question text
- `bloom_level` — Taxonomy level
- `lo_ref` — Learning objective reference

### Stage 4: Docker (Optional)

**Purpose:** Build and validate container configurations.

**Runs when:**
- Push to `main` branch
- Manual trigger with `run_docker: true`

**Tests:**
- Dockerfile.vulnerable build
- docker-compose.yml syntax validation

---

## Local CI Execution

Run the full CI pipeline locally before pushing:

```bash
# Full pipeline
make ci-local

# Individual stages
make lint      # Code quality
make smoke     # Smoke tests
make verify    # Environment check
```

---

## GitHub Actions Configuration

### Workflow File Location

```
.github/
└── workflows/
    └── ci.yml
```

### Trigger Events

| Event | Branches | Conditions |
|-------|----------|------------|
| `push` | main, develop, master | Changes to src/, scripts/, tests/, formative/ |
| `pull_request` | main, master | All PRs |
| `workflow_dispatch` | — | Manual trigger |

### Required Secrets

No secrets required for basic CI. For Docker Hub publishing (future):
- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

---

## Adding CI to Your Fork

1. **Fork the repository** on GitHub

2. **Enable Actions:**
   - Go to repository Settings → Actions → General
   - Select "Allow all actions and reusable workflows"
   - Click Save

3. **Trigger first run:**
   - Make any commit to trigger the workflow
   - Or go to Actions → Week 13 Lab CI → Run workflow

4. **View results:**
   - Actions tab shows workflow runs
   - Click on a run to see detailed logs

---

## Customising the Pipeline

### Adding New Test Files

1. Create test file in `tests/` directory
2. Follow naming convention: `test_*.py`
3. Pipeline automatically discovers and runs new tests

### Modifying Lint Rules

Edit `setup/ruff.toml`:

```toml
[tool.ruff]
line-length = 120
ignore = ["E501", "E402"]

[tool.ruff.per-file-ignores]
"tests/*" = ["S101"]  # Allow assert in tests
```

### Adding CI Stages

Edit `.github/workflows/ci.yml`:

```yaml
new-stage:
  name: 🆕 New Stage
  runs-on: ubuntu-latest
  needs: [lint]  # Run after lint
  steps:
    - uses: actions/checkout@v4
    - name: Your step
      run: echo "Custom step"
```

---

## Troubleshooting CI

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Lint fails | Code style violations | Run `make lint` locally and fix |
| Quiz validation fails | Missing required fields | Check quiz.yaml structure |
| Docker stage fails | Invalid Dockerfile | Validate with `docker build` locally |

### Viewing Logs

1. Go to Actions tab in GitHub
2. Click on failed workflow run
3. Expand failed job
4. Click on failed step to see detailed output

### Re-running Failed Jobs

1. Go to failed workflow run
2. Click "Re-run failed jobs" button
3. Optionally enable debug logging

---

## CI Badges

Add status badge to README:

```markdown
![CI Status](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/ci.yml/badge.svg)
```

---

## Best Practices

1. **Run locally first:** `make ci-local` before pushing
2. **Small commits:** Easier to identify issues
3. **Fix immediately:** Don't let CI failures accumulate
4. **Review logs:** Understand why tests fail
5. **Keep dependencies updated:** Regular `pip` updates

---

*Week 13: IoT and Security — CI/CD Documentation*
*Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim*
