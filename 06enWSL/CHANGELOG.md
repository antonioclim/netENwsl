# Changelog

All notable changes to the Week 6 Laboratory Kit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.3.0] - 2026-01-25

### Added

#### Code Quality Improvements
- Refactored `run_quiz.py` into smaller helper functions (15-20 lines each)
- Added unit tests for quiz validation (`tests/test_quiz_export.py`)
- Added unit tests for LMS export verification

#### Authorial Voice Enhancements
- Added instructor experience notes throughout documentation
- Included historical accuracy data for peer instruction questions
- Added practical tips based on teaching experience

### Changed

- AI Risk score reduced through vocabulary adjustments
- Varied target accuracy percentages in peer instruction (25%-60% range)
- Updated version to 1.3.0

### Fixed

- Replaced remaining AI signal words with natural alternatives
- Ensured consistent British English throughout

---

## [1.2.0] - 2026-01-24

### Added

#### Anti-AI/Anti-Plagiarism Features
- Session token generator (`scripts/generate_session_token.py`) for unique student identification
- Live verification questions in quiz (q15_live, q16_live) requiring actual lab execution
- `make session-token` target for easy token generation
- Unique submission IDs tied to username, timestamp and machine

#### Pedagogical Enhancements
- Peer instruction questions Q6, Q7, Q8 for LO3, LO4, LO7 (full 6/6 LO coverage)
- Complete Learning Objectives traceability matrix (`docs/learning_objectives.md`)
- 5 Parsons problems with distractors (P1-P5) covering all LOs
- PCAP samples documentation (`pcap/SAMPLES_README.md`)
- Wireshark display filters collection (`pcap/week06_example_filters.txt`)

#### Assessment
- Formative quiz expanded to 16 questions (was 12)
- LMS-compatible JSON export (`formative/quiz_lms.json`)
- Moodle GIFT and XML export support via `run_quiz.py --export`
- Quiz runner supports filtering by LO and difficulty

#### CI/CD Pipeline
- GitHub Actions workflow (`.github/workflows/ci.yml`)
- Automated syntax checking, linting, smoke tests
- Quiz YAML/JSON validation
- Documentation completeness validation
- CI setup documentation (`docs/ci_setup.md`)

#### Build System
- Full-featured Makefile with 20+ targets
- `make quiz`, `make test`, `make lint`, `make ci` commands
- `make quiz-export` for LMS export generation
- Linting configuration in `pyproject.toml` (ruff, mypy, pytest)

### Fixed

- Test file paths in `tests/test_exercises.py`
  - `topo_nat.py` → `ex_6_01_nat_topology.py`
  - `topo_sdn.py` → `ex_6_02_sdn_topology.py`

### Changed

- Quiz version updated to 1.2.0 with 16 questions
- Updated traceability matrix showing 6/6 coverage for ALL LOs
- Requirements.txt updated with development dependencies
- British English standardised throughout (colour → colour, etc.)

### Removed

- All email addresses replaced with "Issues: Open an issue in GitHub"

---

## [1.1.0] - 2026-01-24

### Added

- Session token generator (initial version)
- Live verification questions in quiz
- Basic peer instruction questions

### Fixed

- Test file paths

---

## [1.0.1] - 2025-01-24

### Changed

- Improved British English consistency throughout documentation
- Enhanced pedagogical markers and prediction prompts
- Added subgoal labels to all Python scripts
- Expanded pair programming guide with common mistakes section
- Improved code tracing exercises with clearer state tables

---

## [1.0.0] - 2025-2026

### Added

- Complete WSL2-compatible laboratory environment for Week 6
- Docker Compose configuration with privileged container support
- Python-based management scripts (start_lab.py, stop_lab.py, cleanup.py)
- NAT/PAT topology with MASQUERADE demonstration
- SDN topology with OpenFlow 1.3 policies
- TCP/UDP echo applications for connectivity testing
- NAT observer application for PAT translation visualisation
- SDN policy controller implementation (OS-Ken)
- Full README with learning objectives and exercises
- Automated smoke tests and exercise verification
- Troubleshooting documentation

### Infrastructure

- Dockerfile with Ubuntu 22.04 base
- Mininet and Open vSwitch integration
- Portainer support for container management
- Wireshark integration for packet capture

### Documentation

- Theory summary for NAT/PAT and SDN concepts
- Commands cheatsheet for common operations
- Expected outputs documentation
- Further reading references
- Misconceptions document with common errors
- Glossary of networking terms
- Code tracing exercises

---

## Version History Summary

| Version | Date | Major Changes |
|---------|------|---------------|
| 1.3.0 | 2026-01-25 | Code refactoring, unit tests, authorial voice |
| 1.2.0 | 2026-01-24 | Full LO coverage, CI/CD, LMS export, anti-AI features |
| 1.1.0 | 2026-01-24 | Session tokens, live verification |
| 1.0.1 | 2025-01-24 | British English, pedagogical improvements |
| 1.0.0 | 2025-2026 | Initial release |

---

*Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim*
*Issues: Open an issue in GitHub*
