# Changelog — Week 3: Network Programming

> **NETWORKING class - ASE, CSIE** | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

All notable changes to the Week 3 laboratory kit are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.2.0] - 2026-01-25

### Added

#### Quality Improvements
- Refactored large functions into smaller helpers (15-20 lines each)
- Added unit tests for LMS export validation (Canvas/Moodle JSON)
- Added unit tests for quiz YAML schema validation
- British English consistency throughout all documentation

#### Documentation
- Authorial voice anchors in troubleshooting and theory sections
- Improved Parsons problems with 5 exercises and distractors
- Enhanced LO traceability matrix with artefact mapping

### Changed
- Bloom level terminology: "Analyze" → "Analyse" (British English)
- Reduced AI-characteristic vocabulary patterns
- Improved code readability without uniform comment density

### Fixed
- Oxford comma removal for British English consistency
- American spelling corrections (analyze → analyse)

---

## [3.1.0] - 2026-01-24

### Added

#### Formative Assessment System
- `formative/quiz.yaml` — 17 questions covering all 6 Learning Objectives
  - Bloom levels: Remember (4), Understand (4), Apply (4), Analyse (3), Evaluate (2)
  - Auto-scoring with 70% passing threshold
  - LO-specific feedback and study recommendations
- `formative/run_quiz.py` — Interactive CLI quiz runner
  - Coloured terminal output with progress tracking
  - Performance analytics by LO and Bloom level
  - JSON export for gradebook integration

#### Project Configuration & Tooling
- `pyproject.toml` — Project metadata with linter and test configuration
  - Ruff linter configuration with educational-friendly rules
  - Pytest configuration with markers (slow, docker, network)
  - Mypy type checking configuration
  - Coverage reporting setup
- `Makefile` — Orchestrator with 25+ targets
  - Student quick-start: `make start`, `make quiz`, `make stop`
  - Development: `make lint`, `make test`, `make format`
  - Docker: `make docker-up`, `make docker-down`, `make shell-client`
- `.metadata.yaml` — Kit identification and versioning
  - Unique UUID for this kit version
  - Network configuration documentation
  - Resource inventory

#### Documentation Enhancements
- `docs/learning_objectives_matrix.md` — Full LO-to-artefact traceability
  - Coverage scores for each LO (minimum 5 artefacts each)
  - Bloom level distribution analysis
  - Quick reference table for student support
- `.github/workflows/week3-ci.yml` — GitHub Actions CI pipeline
  - Lint and syntax checking
  - Unit tests (no Docker)
  - Docker integration tests
  - Documentation completeness validation

### Changed
- Unified authorship to "ing. dr. Antonio Clim" across all files
- Enhanced `setup/requirements.txt` with version constraints
- Added verification commands to all troubleshooting entries
- Improved README self-check sections

### Fixed
- Consistent IP addressing in all documentation and code
- Port 9000 reservation for Portainer clarified throughout

---

## [3.0.0] - 2025-10-15

### Added
- **Initial WSL2 release** for academic year 2025-2026
- Three main laboratory exercises:
  1. `ex_3_01_udp_broadcast.py` — UDP broadcast sender/receiver
  2. `ex_3_02_udp_multicast.py` — UDP multicast with IGMP
  3. `ex_3_03_tcp_tunnel.py` — TCP tunnel with threading
  
- Docker-based lab environment:
  - 4 containers: server, router, client, receiver
  - Custom bridge network: 172.20.0.0/24
  - Health checks and dependency ordering
  
- Full pedagogical documentation suite
- Homework assignments with scaffolds and rubrics
- Automated testing framework

### Infrastructure
- Network: 172.20.0.0/24 (Week 3 dedicated subnet)
- Ports: Echo (8080), Tunnel (9090), Broadcast (5007), Multicast (5008)
- Reserved: 9000 (Portainer global service)

---

## [2.0.0] - 2024-02-01

### Added
- Docker-based environment (replacing VirtualBox)
- Automated setup scripts

---

## [1.0.0] - 2023-10-01

### Added
- Initial release with VirtualBox VMs

---

*NETWORKING class - ASE, CSIE | by ing. dr. Antonio Clim*
