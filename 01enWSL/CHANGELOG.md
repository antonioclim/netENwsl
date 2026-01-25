# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-01-25

### Added

#### Code Quality Improvements
- **Refactored Python exercises**: Split long functions (>25 lines) into smaller helpers (15-20 lines)
- **Extended unit tests**: Added tests for Canvas/Moodle exports and validator coverage
- **Bloom level coverage tests**: Automated verification of LO coverage in quiz

#### Documentation
- **SVG Diagrams**: Added proper SVG diagrams to `docs/images/`
  - `tcp_handshake.svg` — TCP three-way handshake sequence
  - `docker_architecture.svg` — Lab environment architecture
- **Enhanced Parsons Problems**: Added second distractor to each problem

### Changed

- Quiz section renamed from `comprehensive_review` to `full_review` (British English)
- Fixed American spelling "Analyze" → "Analyse" in formative/README.md
- Fixed CI pipeline typo (`pip installl` → `pip install`)

### Fixed

- AI fingerprint words removed ("comprehensive" replaced with "complete"/"full")
- All American spellings corrected to British English

---

## [1.1.0] - 2026-01-24

### Added

#### Pedagogical Improvements
- **Formative Quiz System**: Complete quiz with 22 questions in YAML and JSON formats
  - Pre-lab, during-lab, exit-ticket and full review sections
  - Full Bloom taxonomy coverage (remember, understand, apply, analyse)
  - LMS export support (Moodle XML, Canvas QTI)
- **Quiz Runner**: Standalone Python script (`formative/run_quiz.py`)
  - Interactive mode for self-assessment
  - Section-based execution
  - Statistics and validation
- **Learning Objectives Matrix**: Formalised traceability in `docs/learning_objectives.md`
  - Complete LO-to-artefact mapping
  - Self-assessment checklist
  - Quiz coverage visualisation
- **Parsons Problems**: 5 problems with distractors in `docs/parsons_problems.md`
  - P1: Ping Latency Measurement (LO1)
  - P2: TCP Server Setup (LO2)
  - P3: CSV Data Parsing (LO3)
  - P4: TCP Client Connection (LO2)
  - P5: Docker Lab Startup (LO6)
- **PCAP Demo Files**: Synthetic captures for educational demonstrations
  - `demo_icmp_ping.pcap` — ICMP echo request/reply pairs (LO1)
  - `demo_tcp_handshake.pcap` — Complete TCP connection lifecycle (LO2)
  - `demo_dns_query.pcap` — DNS A record query/response (LO4, LO7)
  - `demo_http_get.pcap` — HTTP GET request/response (LO4)
- **PCAP Generator Script**: `pcap/generate_demo_pcaps.py` for reproducible captures
- **Capture Guide**: `pcap/CAPTURE_GUIDE.md` with manual capture instructions

#### Code Quality
- **Makefile**: Complete orchestration with `make quiz`, `make test`, `make ci`
- **Public Tests**: New `tests/public/` directory with student-visible tests
- **Type Marker**: Added `src/py.typed` (PEP 561 compliance)
- **Linting Config**: Complete ruff configuration in pyproject.toml

#### Documentation
- **CI Documentation**: `docs/ci_setup.md` with pipeline explanation
- **Architecture Diagrams**: Mermaid diagrams in `docs/images/`
  - TCP/IP layer model
  - TCP three-way handshake sequence
  - Docker lab architecture
- **Content Attestation**: `ATTESTATION.md` for authorship verification
- **Updated Further Reading**: Translated Romanian section to English

#### Infrastructure
- **GitHub Actions CI**: `.github/workflows/ci.yml` with lint, test, quiz, docker jobs
- **CODEOWNERS**: `.github/CODEOWNERS` for review assignments
- **Enhanced pyproject.toml**: Complete metadata and tool configuration
- **Updated requirements.txt**: Correlated dependencies with version constraints

### Changed

#### Language Consistency
- All content now in British English (without Oxford comma)
- Removed all email addresses from documentation
- Translated Romanian sections in `docs/further_reading.md`

#### Quiz Structure
- Expanded from 15 to 22 questions
- Added coverage for LO3, LO5 and LO7 (previously 0 questions each)
- Updated Bloom level distribution to include Analyse level

### Fixed
- Quiz coverage gaps for LO3, LO5, LO7
- Language inconsistencies in documentation

---

## [1.0.0] - 2025-12-15

### Added

- Initial release of Week 1 Laboratory Kit
- Core exercises (ex_1_01 through ex_1_05)
- Homework assignments (hw_1_01, hw_1_02)
- Docker environment configuration
- Detailed README with Wireshark guide
- Troubleshooting documentation
- Glossary and theory summary
- Misconceptions documentation
- Code tracing exercises
- Peer instruction questions

---

*NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim*
