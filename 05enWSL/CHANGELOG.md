# Changelog

All notable changes to the Week 5 Laboratory Kit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.1.0] - 2026-01-24

### Added
- **Quiz Enhancement**: 2 new questions at Bloom L5 (Evaluate) and L6 (Create) levels
  - q11: VLSM efficiency evaluation (3 pts)
  - q12: Complete VLSM design exercise with rubric (4 pts)
- **LMS Export**: New `export_to_lms.py` script for Moodle/Canvas compatibility
  - JSON export format for generic LMS import
  - Moodle XML export format
  - Canvas JSON export format
  - Pre-generated `quiz_lms_export.json` file
- **Misconception #0**: OSI Layer confusion for routers (LO1 coverage)
- **Parsons Problems**: 5 problems with distractors in `formative/parsons/problems.json`
- **CI Documentation**: New `docs/ci_setup.md` with pipeline explanation
- **Linting Configuration**: `pyproject.toml` with ruff and pytest settings
- **Self-Assessment**: Personalised study plan in quiz results based on missed LOs
- Version badges and status info in README.md

### Changed
- Quiz now covers all 6 Bloom taxonomy levels (L1-L6)
- Total quiz questions: 10 → 12
- Total possible points: 21 → 28
- `run_quiz.py`: Added evaluate/create to --category choices
- `learning_objectives.md`: Complete traceability matrix with all LOs covered
- `requirements.txt`: Comprehensive dependency list with categories
- British English throughout (analyse, colour, etc.)

### Fixed
- **CRITICAL**: Syntax error in `formative/run_quiz.py` line 154-155
  - Escaped quotes issue resolved with variable extraction
  - Quiz runner now executes without errors

### Documentation
- `pcap/README.md`: Comprehensive packet capture guide
- `docs/ci_setup.md`: CI/CD setup and troubleshooting guide
- `docs/learning_objectives.md`: Complete LO traceability matrix
- `docs/misconceptions.md`: Added Misconception #0 for OSI layers
- `README.md`: Updated with badges, LMS export instructions

## [1.0.0] - 2026-01-07

### Added
- Initial release of Week 5 WSL Starter Kit
- Docker environment with Python 3.11, UDP server/client containers
- CIDR analysis and subnetting exercises (FLSM/VLSM)
- IPv6 addressing utilities and exercises
- Interactive quiz generator for self-assessment
- Complete documentation and troubleshooting guides

---

*Computer Networks Laboratory — ASE-CSIE Bucharest*
