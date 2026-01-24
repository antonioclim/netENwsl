# Changelog — Week 7 Laboratory Kit
## Computer Networks — ASE, CSIE | Computer Networks Laboratory

All notable changes to the Week 7 laboratory kit are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [2.0.0] — 2026-01-24

### Added

#### Pedagogical Enhancements
- **PCAP Sample Files**: Generated 7 reference PCAP files demonstrating key concepts
  - `week07_lo1_tcp_handshake.pcap` — Complete TCP three-way handshake
  - `week07_lo1_udp_baseline.pcap` — UDP connectionless exchange
  - `week07_lo2_tcp_blocked_reject.pcap` — REJECT action demonstration
  - `week07_lo2_tcp_blocked_drop.pcap` — DROP action with retransmissions
  - `week07_lo4_timeout_analysis.pcap` — Timeout scenario for analysis
  - `week07_lo5_stateful_filter.pcap` — Stateful connection tracking
  - `week07_lo6_drop_vs_reject.pcap` — Side-by-side comparison

- **LO5 Test Coverage**: New `tests/test_lo5_profile.py` with comprehensive tests
  - Profile schema validation
  - Rule ordering verification (first-match-wins)
  - Conflict detection
  - Homework validation helper

- **FAQ Document**: New `docs/faq.md` with 25+ common questions and answers

#### CI/CD Pipeline
- **GitHub Actions Workflow**: `.github/workflows/ci.yml`
  - Syntax checking
  - Code linting with ruff
  - Unit tests with pytest
  - YAML/JSON validation
  - Docker build verification
  - PCAP generation
  - Quiz LMS export

- **CI Documentation**: `docs/ci_setup.md` with setup guide
- **Linting Configuration**: `pyproject.toml` with ruff settings

#### Quiz Enhancements
- **LMS Export**: New `formative/quiz_export.py` supporting:
  - Moodle XML format
  - Canvas JSON format
  - Generic JSON for API integration
- **Quiz metadata**: Added LMS-specific configuration in `quiz.yaml`
- **Ordering questions**: Added q13 with distractors for rule ordering

#### Development Tools
- **requirements-dev.txt**: Separate development dependencies
  - pytest, pytest-cov, pytest-timeout
  - ruff, mypy, bandit
  - scapy for PCAP generation

### Changed

- **Learning Objectives Matrix**: Updated to 100% coverage across all LOs
- **Parsons Problems**: Enhanced with 5 problems including distractors
  - P1: TCP Port Probe (3 distractors)
  - P2: Parse iptables Output (3 distractors)
  - P3: UDP Send with Error Handling (3 distractors)
  - P4: Apply Firewall Profile (4 distractors)
  - P5: Analyse PCAP with tshark (3 distractors)

- **Makefile**: Expanded with 30+ targets
  - Added: `make ci`, `make lint`, `make format`, `make export-quiz`
  - Added: `make quiz-lo1` through `make quiz-lo6`
  - Added: `make generate-pcap`, `make verify-pcap`
  - Added: `make pytest-cov`, `make pytest-ci`

- **requirements.txt**: Updated with version constraints and documentation

### Fixed

- LO5 coverage gap (was 80%, now 100%)
- Inconsistent British English spelling
- Missing cross-references in formative_assessment.md

### Security

- Removed all email addresses from documentation
- Added bandit security scanning to CI pipeline

---

## [1.5.0] — 2026-01-15

### Added

- Initial Learning Objectives Traceability Matrix
- Parsons problems (5 problems, no distractors)
- Code tracing exercises (3 exercises)
- Peer instruction questions (5 questions)
- Concept analogies document

### Changed

- Restructured documentation folder
- Improved README with ASCII diagrams

---

## [1.4.0] — 2025-12-20

### Added

- Formative quiz with 15 questions
- Quiz runner script (`run_quiz.py`)
- Misconceptions document (8 entries)
- Troubleshooting guide (24 sections)

### Changed

- Updated theory summary with academic references

---

## [1.3.0] — 2025-11-15

### Added

- Homework assignments (2 assignments with rubrics)
- Test framework (`test_exercises.py`)
- Expected outputs documentation

### Changed

- Improved exercise instructions
- Added verification commands

---

## [1.2.0] — 2025-10-10

### Added

- `firewallctl.py` for profile management
- Firewall profiles JSON configuration
- Packet filter proxy application

### Changed

- Docker network configuration (10.0.7.0/24)
- Port assignments clarified

### Fixed

- Port 9000 conflict with Portainer (RESERVED)

---

## [1.1.0] — 2025-09-05

### Added

- Docker Compose configuration
- TCP Echo Server and Client
- UDP Receiver and Sender
- Basic capture scripts

### Changed

- Migrated from manual setup to Docker

---

## [1.0.0] — 2025-08-01

### Added

- Initial release
- Basic README with exercise instructions
- Theory summary document
- Commands cheatsheet

---

## Version Numbering

This project uses Semantic Versioning:

- **MAJOR** (X.0.0): Incompatible changes or significant restructuring
- **MINOR** (0.X.0): New features added in backwards-compatible manner
- **PATCH** (0.0.X): Backwards-compatible bug fixes

---

## Upgrade Notes

### From 1.x to 2.0

1. Install new development dependencies:
   ```bash
   pip install -r setup/requirements-dev.txt
   ```

2. Generate PCAP samples:
   ```bash
   make generate-pcap
   ```

3. Verify CI configuration:
   ```bash
   make ci
   ```

4. Export quiz to LMS (optional):
   ```bash
   make export-quiz
   ```

---

*Computer Networks — Week 7: Packet Interception, Filtering and Defensive Port Probing*  
*ASE Bucharest, CSIE | Computer Networks Laboratory*
