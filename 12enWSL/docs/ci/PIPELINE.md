# CI Pipeline Architecture — Week 12
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## Pipeline Flow

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  PUSH    │───▶│   LINT   │───▶│   TEST   │───▶│  DOCKER  │
│          │    │          │    │          │    │  (main)  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
```

---

## Stage Details

| Stage | Duration | Checks |
|-------|----------|--------|
| Lint | ~30s | Syntax, Ruff, YAML |
| Test | ~1min | Unit tests, Quiz |
| Docker | ~2min | Build, Run |

---

## Trigger Conditions

| Event | Branches | Stages |
|-------|----------|--------|
| Push | main, develop | All |
| Pull Request | main | Lint, Test |

---

## See Also

- `.github/workflows/ci.yml` — Workflow definition
- `docs/ci/CI_SETUP.md` — Setup guide

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
