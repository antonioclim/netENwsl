# CI/CD Setup Guide — Week 2 Laboratory Kit

> NETWORKING class — ASE, CSIE Bucharest  
> Computer Networks Laboratory | by ing. dr. Antonio Clim

## Overview

This document describes the Continuous Integration setup for the Week 2 kit.

## Local CI Commands

```bash
make ci              # Full pipeline
make check-syntax    # Syntax verification
make lint            # Run ruff linter
make typecheck       # Run mypy
make test            # Run pytest
make test-coverage   # Tests with coverage
```

## Pipeline Architecture

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Lint    │───▶│  Test    │───▶│  Quiz    │───▶│ Integrity│
└──────────┘    └──────────┘    └──────────┘    └──────────┘
```

## Jobs

| Job | Purpose |
|-----|---------|
| `lint` | Syntax, ruff, mypy |
| `test` | pytest with coverage |
| `validate-quiz` | Quiz YAML/JSON validation |
| `validate-parsons` | Parsons problems validation |
| `integrity` | Required files check |

## Linting Rules (ruff.toml)

- E, W: pycodestyle
- F: Pyflakes
- I: isort
- B: flake8-bugbear
- C4: comprehensions
- UP: pyupgrade
- SIM: simplify

## Troubleshooting

### Lint Failures
```bash
make lint-fix    # Auto-fix
make lint        # Check remaining
```

### Test Failures
```bash
pytest tests/ -v --tb=long
```

### Quiz Validation
```bash
python -c "import yaml; yaml.safe_load(open('formative/quiz.yaml'))"
```

## Support

Issues: Open an issue in GitHub

---

*NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim*
