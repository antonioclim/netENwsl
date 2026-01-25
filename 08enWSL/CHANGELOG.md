# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-01-25

### Added
- **Canvas QTI Export**
  - `formative/run_quiz.py --export-canvas` for Canvas LMS compatibility
  - QTI 1.2 format with proper assessment structure

- **Enhanced Tests**
  - `tests/test_exports.py` for LMS export validation
  - Tests for Moodle XML and Canvas QTI format correctness
  - Quiz YAML structure validation tests

- **Authorial Voice Anchors** (pedagogical enhancement)
  - Instructor notes with practical experience in docs/
  - Teaching heuristics in peer_instruction.md
  - Experience-based warnings in misconceptions.md

### Changed
- Refactored `formative/run_quiz.py` for better maintainability
- Refactored `formative/progress_tracker.py` with smaller helper functions
- Updated `Makefile` with `test-exports` and `ci-all` targets
- Improved British English consistency throughout

### Fixed
- Minor terminology corrections for British English compliance

---

## [1.1.0] - 2026-01-24

### Added
- **Formative Assessment System**
  - `formative/quiz.yaml` — 15-question quiz covering all 6 Learning Objectives
  - `formative/run_quiz.py` — Interactive quiz runner with immediate feedback
  - Support for filtering by LO, difficulty and Bloom level
  - JSON export for tracking progress over time

- **Learning Objectives Traceability**
  - `docs/learning_objectives.md` — Complete LO → artefact mapping matrix
  - Links from each LO to theory, lab, tests, quiz, Parsons and misconceptions

- **Formative Assessment Guide**
  - `docs/formative_assessment.md` — How to use self-assessment effectively
  - Recommended workflows for before, during and after exercises

- **Makefile Orchestration**
  - `make quiz` — Run formative assessment
  - `make quiz-lo LO=N` — Quiz specific Learning Objective
  - `make test`, `make smoke`, `make start/stop` targets
  - Coloured output and help system

- **Acknowledgments**
  - `ACKNOWLEDGMENTS.md` — Credits to Andrei T. (brainstorming collaboration)
  - Documentation of pedagogical framework from DPPD module, UPB

### Changed
- Enhanced documentation with contributor acknowledgments
- Added inside references to collaborative development process

### Pedagogical Notes
This release emphasises formative assessment as a learning tool, not evaluation.
The quiz system was designed through extensive brainstorming with Andrei T. and
incorporates principles from the psychopedagogy module at Universitatea
Politehnica București.

---

## [1.0.0] - 2026-01-07

### Added
- Initial release of Week 8 Laboratory Starter Kit
- Docker Compose orchestration with nginx reverse proxy and 3 Python backend servers
- Load balancing demonstrations: round-robin, weighted, least-connections, IP hash
- Python exercises for HTTP server implementation and reverse proxy
- Thorough README with learning objectives and exercises
- Setup scripts for environment verification and prerequisite installation
- Traffic capture utilities for Wireshark analysis
- Automated demonstration scripts
- Test suite for environment validation

### Infrastructure
- nginx:alpine reverse proxy container (ports 8080/8443)
- 3x Python 3.11-slim backend server containers
- Optional Portainer CE for container management (port 9443)
- Isolated Docker network (172.28.8.0/24)

### Documentation
- Theory summary covering TCP, UDP, TLS and QUIC protocols
- Commands cheatsheet for Docker, curl and network diagnostics
- Troubleshooting guide for common issues
- References to course materials and RFC specifications

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
