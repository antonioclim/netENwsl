# Changelog — Week 2 Laboratory Kit

All notable changes to this laboratory kit are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] — 2026-01-25

### Added
- Authorial voice anchors throughout documentation (instructor experience notes)
- `docs/reflection_prompts.md` — Post-lab reflection questions
- `tests/test_lms_export.py` — Unit tests for quiz export functionality
- Enhanced LO traceability matrix with complete coverage
- Difficulty ratings in `docs/further_reading.md`
- Diagnostic flowchart in troubleshooting guide

### Changed
- Refactored `ex_2_01_tcp.py` — split large functions into 15-20 line helpers
- Refactored `ex_2_02_udp.py` — improved modularity
- Refactored `formative/export_quiz_to_lms.py` — better testability
- Improved type hints throughout `scripts/utils/`
- Enhanced `docs/peer_instruction.md` with vote distribution expectations
- Enhanced `docs/pair_programming_guide.md` with explicit swap points
- Updated `docs/commands_cheatsheet.md` with debugging section
- British English verification pass (no Oxford commas, correct spellings)

### Fixed
- Removed remaining AI-signal vocabulary patterns
- Corrected inconsistent section depths in documentation

## [2.0.0] — 2026-01-24

### Added
- Complete formative assessment system
  - `formative/quiz.yaml` — 15 questions across Bloom levels
  - `formative/run_quiz.py` — Interactive quiz runner
  - `formative/export_quiz_to_lms.py` — Moodle/Canvas/GIFT export
  - `formative/parsons_problems.json` — 5 code reordering problems
- GitHub Actions CI pipeline (`.github/workflows/ci.yml`)
- `docs/learning_objectives.md` — LO traceability matrix
- `docs/formative_assessment.md` — Assessment documentation
- `docs/CI_SETUP.md` — CI configuration guide
- `Makefile` with targets for quiz, test and lint
- `ruff.toml` — Linting configuration
- `pytest.ini` — Test configuration
- SVG diagrams in `docs/images/`

### Changed
- Restructured exercises with subgoal labels
- Added prediction prompts (Brown & Wilson Principle 4)
- Enhanced docstrings with Args/Returns sections
- Added type hints to public functions
- Complete update of all documentation files
- Improved troubleshooting with step-by-step guides

## [1.1.0] — 2026-01-23

### Added
- `docs/peer_instruction.md` — 5 MCQ questions
- `docs/pair_programming_guide.md` — Collaboration structure
- `docs/misconceptions.md` — 12 common errors
- `docs/glossary.md` — Technical terms
- `docs/code_tracing.md` — Execution trace exercises
- `docs/parsons_problems.md` — Code reordering (Markdown)
- `docs/concept_analogies.md` — CPA concrete phase

### Changed
- Improved `README.md` structure
- Enhanced troubleshooting section

## [1.0.0] — 2026-01-22

### Added
- Initial release
- TCP exercise (`ex_2_01_tcp.py`)
- UDP exercise (`ex_2_02_udp.py`)
- Docker configuration
- Basic documentation
- Setup scripts

---

*NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim*
