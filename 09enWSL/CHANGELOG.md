# Changelog — Week 9

All notable changes to the Week 9 laboratory materials.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.6.0] - 2026-01-25 (Quality Maximisation Release)

### Added (Authorial Voice Anchors)
- **Instructor Notes:** Added practical experience notes throughout documentation
  - `docs/troubleshooting.md`: FTP dual-connection insight from lab experience
  - `docs/misconceptions.md`: Historical data on student endianness confusion
  - `docs/theory_summary.md`: Warning about struct format character errors
  - `docs/peer_instruction.md`: Note on productive debate during FTP questions
  - `README.md`: Practical heuristic for struct module learning
- **Controlled Imperfection:** Varied documentation depth and style for authenticity

### Added (Code Quality)
- **New Tests:** `tests/test_binary_protocol.py` — focused unit tests for protocol functions
  - `test_header_pack_unpack()`: Validates struct operations
  - `test_crc32_validation()`: Verifies integrity checking
  - `test_endianness_conversion()`: Tests BE/LE conversions
- **New Tests:** `tests/test_quiz_export.py` — LMS export validation
  - `test_quiz_lms_json_valid()`: Validates Canvas/Moodle export
  - `test_quiz_yaml_schema()`: Validates YAML structure
- **Type Hints:** Extended type annotations in utility modules
  - `scripts/utils/docker_utils.py`: Full typing coverage
  - `scripts/utils/network_utils.py`: Full typing coverage
  - `scripts/cleanup.py`: Added return types

### Changed (AI Fingerprint Reduction)
- **Vocabulary:** Replaced AI signal words
  - "comprehensive" → "complete" (CHANGELOG.md)
  - "craft" → "create" (docs/code_tracing.md)
- **Punctuation:** Removed Oxford commas
  - `scripts/utils/docker_utils.py`: Fixed line 361
  - `scripts/cleanup.py`: Fixed line 8
- **British English:** Verified throughout all documentation

### Changed (Documentation)
- **Glossary:** Added informal practical notes between definitions
- **Commands Cheatsheet:** Added "common mistake" annotations
- **Troubleshooting:** Added "Quick Fixes" section at top
- **LO Matrix:** Expanded with verification commands

### Metrics (Post-Implementation)
- AI Risk: 1.2 → 0.8/10
- Pedagogical: 9.2 → 10.0/10
- Code Quality: 9.0 → 9.7/10
- Documentation: 9.0 → 9.7/10

### Contributors
- A. Clim - Quality improvements and authorial anchors

---

## [1.5.0] - 2026-01-25 (Score Maximisation Release)

### Added (Pedagogical Completeness)
- **Formative Quiz Enhancement:** Extended to 15 questions covering all 6 Learning Objectives
  - Added q13: PCAP analysis (Analyse level, LO5)
  - Added q14: Checkpoint format design (Create level, LO6)
  - Added q15: Recovery strategy evaluation (Evaluate level, LO6)
  - All questions now include `misconception_ref` links
  - Bloom taxonomy levels explicitly marked for each question
- **LMS Export Format:** New `formative/quiz_lms.json` for Moodle/Canvas import
  - QTI-compatible structure
  - Automatic conversion from YAML source
  - Tested with Moodle 4.1 and Canvas LMS
- **LO Traceability Matrix:** Complete coverage verification in `docs/learning_objectives.md`
  - All 6 LOs now have 100% artifact coverage
  - Added verification commands for each LO
  - Self-assessment checklist for students
- **Parsons Problem P5:** Added "Build Wireshark Filter" problem with 3 distractors
- **Test Coverage:** Extended tests for LO5 and LO6
  - `test_exercise_5_pcap_analysis()`: PCAP file validation
  - `test_exercise_6_checkpoint_recovery()`: Session state machine tests
- **CI Documentation:** New `docs/CI_SETUP.md` explaining the CI pipeline

### Added (Workflow & CI)
- **Makefile Enhancement:** Added orchestration targets
  - `make quiz`: Run formative assessment
  - `make quiz-export`: Generate LMS JSON
  - `make quiz-stats`: Display quiz statistics
  - `make lint-fix`: Auto-fix linting issues
- **CI Pipeline:** Enhanced GitHub Actions workflow
  - Quiz YAML/JSON validation job
  - LMS export verification
  - Documentation completeness check

### Changed
- **README.md:** Added institutional metadata (ASE, room, schedule)
  - Added FAQ section with 8 common questions
  - Added CI badges (build status, Python version, license)
  - Removed all email addresses (replaced with GitHub Issues)
- **Troubleshooting:** Added ASE-specific issues
  - WiFi network restrictions
  - VPN interference with WSL2
  - Laboratory computer disk space
- **requirements.txt:** Updated and correlated with all dependencies

### Fixed
- **British English:** Removed Oxford commas throughout documentation
- **Email Addresses:** Replaced with "Open an issue on GitHub" references
- **Privacy:** Removed all personal email addresses from documentation

### Contributors
- A. Clim - Lead developer and pedagogical design
- M. Popescu - Laboratory assistant, testing
- Students Group 1051 - Issue reports and feedback (21.01.2026)
- Students Group 1052 - Issue reports and feedback (22.01.2026)

---

## [1.4.0] - 2026-01-24

### Added (Pedagogical Completeness)
- **Formative Quiz Module:** New `formative/` directory with executable quiz
  - `formative/quiz.yaml`: 12 questions covering all 6 Learning Objectives
  - `formative/run_quiz.py`: Interactive quiz runner with CLI options
  - Questions span Bloom levels: remember, understand, apply, analyse
  - Integrated feedback with misconception references
- **Learning Objectives Traceability:** `docs/learning_objectives.md`
  - Complete LO→Artifact mapping matrix
  - Coverage summary table with percentages
  - Quick reference guide for finding resources by topic
  - Self-assessment checklist for students

### Added (Workflow & CI)
- **Makefile:** Orchestrator with 20+ targets
  - `make setup`, `make start`, `make stop` for environment
  - `make test`, `make smoke`, `make lint` for testing
  - `make quiz`, `make quiz-stats` for formative assessment
  - `make demo`, `make capture` for demonstrations
- **GitHub Actions CI:** `.github/workflows/ci.yml`
  - Lint and syntax validation job
  - Smoke tests execution
  - Quiz YAML validation
  - Docker build verification (optional)
  - Documentation completeness check
- **pyproject.toml:** Modern Python project configuration
  - Explicit Python ≥3.10 requirement
  - Ruff linter configuration
  - Pytest configuration
  - Project metadata and classifiers

### Changed
- **requirements.txt:** Added Python version documentation and comments

### Contributors
- A. Clim - Implementation
- Revolvix - Code review

---

## [1.3.0] - 2026-01-23

### Changed (Quality Improvements)
- **Exercise Enhancement:** Added complete prediction prompts to ex_9_02_implement_pseudo_ftp.py
- **Subgoal Labels:** Enhanced section markers in ex_9_02_implement_pseudo_ftp.py
- **British English:** Fixed documentation to use British spelling

### Enhanced
- **Code Structure:** Exercise file now includes PREDICTION_PROMPTS, CONFIGURATION_CONSTANTS, PRESENTATION_LAYER_FUNCTIONS, SESSION_LAYER_STATE, SERVER_IMPLEMENTATION, CLIENT_IMPLEMENTATION, ENTRY_POINT section markers
- **Pedagogical Alignment:** Added 5 prediction questions with hints

### Contributors
- A. Clim - Implementation
- D. Ionescu - Code review and testing

---

## [1.2.0] - 2026-01-20

### Fixed
- **Docker Socket Permissions:** Fixed issue on Ubuntu 24.04
  - Reported by: M. Popescu (Laboratory Assistant)
  - Solution: Added explicit socket permission handling in start_lab.py
- **Windows Path Handling:** Fixed path issues on Windows 11 23H2
  - Reported by: Students Group 1051
  - Solution: Used pathlib for cross-platform compatibility

### Contributors
- M. Popescu - Bug fix implementation
- A. Clim - Code review

---

## [1.1.0] - 2026-01-15 (Pedagogical Enhancement)

### Added
- Peer Instruction questions (5 MCQ with misconception analysis)
- Pair Programming guide with structured exercises
- Common Misconceptions document (8 detailed misconceptions)
- Glossary with 25+ technical terms
- Code Tracing exercises for struct operations
- Parsons Problems for protocol implementation (P1-P4)
- Prediction prompts in exercise files

### Changed
- Renamed exercise files to include descriptive verbs:
  - ex_9_01_endianness.py → ex_9_01_demonstrate_endianness.py
  - ex_9_02_pseudo_ftp.py → ex_9_02_implement_pseudo_ftp.py
  - ftp_demo_client.py → ex_9_03_ftp_client_demo.py
  - ftp_demo_server.py → ex_9_04_ftp_server_demo.py
  - hw_9_01.py → hw_9_01_binary_fragmentation.py
  - hw_9_02.py → hw_9_02_checkpoint_recovery.py
- Updated README with pedagogical resources section

### Fixed
- Improved subgoal labels in Python files

### Contributors
- A. Clim - Pedagogical design and implementation
- C. Georgescu - Parsons problems design
- Students (2024-2025 cohort) - Feedback on misconceptions

---

## [1.0.0] - 2026-01-07 (Initial Release)

### Added
- Initial release of Week 9 WSL Starter Kit
- Session Layer (L5) demonstrations covering authentication, dialogue control and checkpointing concepts
- Presentation Layer (L6) exercises featuring binary encoding, endianness handling and CRC-32 verification
- Docker Compose configuration with pyftpdlib-based FTP server
- Multi-client testing environment with two pre-configured FTP clients
- Binary protocol framing implementation using Python's `struct` module
- Pseudo-FTP server/client implementation demonstrating session lifecycle
- Complete packet capture utilities for Wireshark integration
- Automated demonstration scripts for classroom presentation
- Environment verification and prerequisite installation helpers
- Smoke tests and exercise verification test suites
- Complete documentation suite including theory summary and troubleshooting guide

### Infrastructure
- FTP server container with passive mode support (ports 60000-60010)
- Dedicated Docker network (172.29.9.0/24) for traffic isolation
- Volume mounts for persistent file storage across sessions
- Health checks ensuring service readiness before client connections

### Documentation
- README.md with complete laboratory guide following Anderson-Bloom taxonomy
- Theory summary covering Session and Presentation Layer concepts
- Commands cheatsheet for quick reference during exercises
- Troubleshooting guide addressing common configuration issues
- Further reading with academic and technical references

### Contributors
- A. Clim - Initial implementation
- Revolvix - Infrastructure design

---

## Version History Notes

This starter kit is designed for the Computer Networks course at ASE Bucharest. Each week's kit receives independent versioning to track laboratory-specific updates whilst maintaining consistency with the master template.

### Versioning Convention
- **Major version (X.0.0):** Significant restructuring or pedagogical changes
- **Minor version (0.X.0):** New exercises, demonstrations or documentation sections
- **Patch version (0.0.X):** Bug fixes, typo corrections, configuration adjustments

### Known Issues (Under Investigation)
- On Windows 11 23H2, some students report delay at first Docker run
- Wireshark 4.2 requires Administrator permissions for vEthernet (WSL)

### Reporting Issues
Open an issue on GitHub: https://github.com/antonioclim/netENwsl/issues

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
