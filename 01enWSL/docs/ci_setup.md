# CI/CD Pipeline Documentation

> Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

## Pipeline Overview

```
LINT → TEST → QUIZ → DOCKER → Summary
```

## Jobs

| Job | Purpose | Tools |
|-----|---------|-------|
| lint | Code quality | ruff, py_compile |
| test | Unit tests | pytest, smoke_test.py |
| quiz | Quiz validation | YAML/JSON parsing |
| docker | Container build | docker compose |

## Running Locally

```bash
make ci           # Full pipeline
make lint         # Linting only
make test         # Tests only
make validate-quiz # Quiz validation
```

## Configuration Files

- `.github/workflows/ci.yml` — Pipeline definition
- `pyproject.toml` — Tool configuration (ruff, mypy, pytest)
- `setup/requirements.txt` — Dependencies

## Troubleshooting

### Lint Failures
```bash
ruff check src/ --diff  # See issues
ruff check src/ --fix   # Auto-fix
```

### Test Failures
```bash
pytest tests/ -v --tb=long
```

### Docker Failures
```bash
docker compose -f docker/docker-compose.yml logs
```

---
*NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim*
