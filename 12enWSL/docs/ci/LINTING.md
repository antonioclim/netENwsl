# Linting Configuration — Week 12
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

The project uses **ruff** as the primary linter.

---

## Running the Linter

```bash
# Check all code
ruff check src/ scripts/ tests/ formative/

# Auto-fix issues
ruff check src/ --fix

# Via Makefile
make lint      # Check only
make lint-fix  # Auto-fix
```

---

## Rule Categories

| Category | Description |
|----------|-------------|
| E | pycodestyle errors |
| F | Pyflakes |
| I | isort (import sorting) |
| N | pep8-naming |
| W | pycodestyle warnings |

---

## Ignored Rules

- `E501` — Line too long (handled manually)
- `E402` — Module level import not at top

---

## See Also

- `ruff.toml` — Configuration file
- [Ruff Documentation](https://docs.astral.sh/ruff/)

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
