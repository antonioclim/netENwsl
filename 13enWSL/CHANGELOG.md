# Changelog

All notable changes to Week 13 laboratory kit will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [2.1.0] - 2026-01-24

### Added

**Pedagogical Enhancements**
- Beginner Mode in exercises with step-by-step explanations
- Pre-flight Checklist in README for environment verification
- Beginner Errors section in troubleshooting guide
- API Quick Reference (`docs/api_reference.md`)

**AI Risk Mitigation**
- Ground Truth System (`tests/ground_truth.json`) for fact verification
- Validation Script (`tests/validate_ground_truth.py`)
- Fact-checking metadata in quiz with authoritative sources

**CI/CD Infrastructure**
- GitHub Actions Workflow (`.github/workflows/ci.yml`)
- Linting with ruff configuration
- Syntax validation for Python, YAML and JSON
- Ground truth validation as CI stage

**Project Configuration**
- `pyproject.toml` for modern Python packaging
- `py.typed` marker for type hint support
- Enhanced `requirements.txt` with version constraints

### Changed
- Standardised British English terminology (analyse, colour)
- Fixed inconsistent naming (`Colors` vs `Colours`)
- Added complete type hints to exercise functions

### Fixed
- Inconsistent variable naming in port scanner
- Missing type hints in utility functions

---

## [2.0.0] - 2026-01-15

### Added
- Quiz YAML with 16 questions
- LO Traceability Matrix
- 5 Parsons Problems with distractors
- SECURITY.md with ethical guidelines
- 7 Mermaid architecture diagrams
- Makefile with 20+ targets

---

## [1.0.0] - 2026-01-01

### Added
- Initial release with 4 exercises
- Docker-based lab environment
- Mosquitto, DVWA and vsftpd services

---

*Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim*
