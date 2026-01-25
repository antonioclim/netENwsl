# Changelog — Week 7: Packet Interception, Filtering and Defensive Port Probing

All notable changes to this laboratory kit are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [2.1.0] — 2026-01-25

### Added
- Authorial voice anchors throughout documentation for authentic instructor perspective
- Unit tests for LMS export validation (`tests/test_quiz_export.py`)
- Unit tests for firewall profile validator (`tests/test_validator.py`)
- Refactored helper functions in `firewallctl.py` with complete docstrings

### Changed
- Improved documentation with practical instructor notes and experiential references
- British English consistency audit (spelling and punctuation)
- Code quality improvements: docstrings for all public functions
- Fixed duplicate subgoal label in `firewallctl.py`

### Fixed
- American spelling "Initialize" → "Initialise" in logger.py
- Removed Oxford comma in theory_summary.md
- Consistent British English throughout all documentation

---

## [2.0.0] — 2026-01-24

### Added
- **LO Traceability Matrix**: Complete `docs/learning_objectives.md` with artifact mapping
- **Formative Assessment Framework**: Full quiz system with LMS export
- **LO5 Test Coverage**: New `tests/test_lo5_profile.py` with thorough tests
- **GitHub Actions CI**: Automated validation pipeline
- **Parsons Problems**: Interactive code ordering exercises with distractors
- **Code Tracing**: Step-by-step execution tracing exercises

### Changed
- Quiz system now exports to Moodle XML and Canvas JSON
- Makefile extended with quiz and CI targets
- Documentation restructured for better navigation

---

## [1.5.0] — 2026-01-23

### Added
- Peer Instruction questions with misconception analysis
- Pair Programming guide with Driver/Navigator protocols
- Misconceptions document covering 8 common errors
- Glossary with 50+ technical terms
- Concept analogies for CPA method support
- PCAP sample files for all learning objectives

### Changed
- README.md expanded with detailed Portainer and Wireshark guidance
- Troubleshooting section enhanced with WSL-specific solutions

---

## [1.0.0] — 2026-01-08

### Added
- Initial Week 7 laboratory kit for WSL2 environment
- Docker Compose configuration for lab topology
- Core Python exercises for packet capture and filtering
- Basic documentation structure

---

*NETWORKING class — ASE, Informatics | Computer Networks Laboratory*
