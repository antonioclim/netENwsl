# Changelog — Week 7 Laboratory Kit
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

All notable changes to this laboratory kit are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Formative quiz system (`formative/quiz.yaml`, `formative/run_quiz.py`)
  - 15 questions covering all 6 Learning Objectives
  - Multiple question types: MCQ, fill-blank, ordering
  - Configurable filters by LO and difficulty
  - JSON export for results
- Parsons problems runner (`formative/parsons_runner.py`)
  - Interactive code reordering exercises
  - Hint mode for distractor identification
- Learning Objectives traceability matrix (`docs/learning_objectives.md`)
  - Complete mapping of LOs to artifacts
  - Coverage analysis with percentages
- Unified formative assessment guide (`docs/formative_assessment.md`)
  - Checkpoint questions for each exercise
  - Self-assessment rubrics
- VERSIONS.md with explicit version pinning
  - All component versions documented
  - Verification commands included
- Makefile for command orchestration
  - `make quiz`, `make test`, `make start`, etc.
  - Help target with command reference
- PCAP samples directory with naming convention (`pcap/samples/`)
  - Reference captures for each LO
  - Generation instructions
- pytest.ini configuration
  - Markers for exercise-specific tests
  - Logging configuration

### Changed
- `setup/requirements.txt`: Pinned exact versions (PyYAML==6.0.1, docker==7.0.0, etc.)
- `scripts/utils/logger.py`: Enhanced with configurable levels, dual output, context managers
- `tests/test_exercises.py`: Added complete type hints, pytest compatibility, removed duplications
- `docs/theory_summary.md`: Extended with ASCII diagrams, port state diagram, RFC references
- `pcap/README.md`: Added formal naming convention standard

### Fixed
- Consistent IP addressing scheme documentation
- Type hints in test functions

---

## [1.0.0] — 2026-01-20

### Added
- Initial release of Week 7 laboratory kit
- 5 hands-on exercises covering packet capture and filtering
- Docker-based isolated environment
- TCP Echo Server and Client
- UDP Sender and Receiver
- Packet Filter Proxy (application-layer)
- Port Probe utility
- Firewall profile management (`firewallctl.py`)
- Comprehensive documentation suite:
  - `docs/theory_summary.md`
  - `docs/troubleshooting.md`
  - `docs/misconceptions.md`
  - `docs/peer_instruction.md`
  - `docs/parsons_problems.md`
  - `docs/code_tracing.md`
  - `docs/concept_analogies.md`
  - `docs/glossary.md`
  - `docs/commands_cheatsheet.md`
  - `docs/pair_programming_guide.md`
  - `docs/further_reading.md`
- Homework assignments with validation scripts
- Automated lab startup and cleanup scripts
- Test suite for exercise verification

---

## Version History Summary

| Version | Date | Highlights |
|---------|------|------------|
| [Unreleased] | — | Formative assessment system, version pinning |
| 1.0.0 | 2026-01-20 | Initial release |

---

## Upgrade Notes

### From 1.0.0 to [Unreleased]

**New files to add:**
```
formative/
├── quiz.yaml
├── run_quiz.py
└── parsons_runner.py

docs/
├── learning_objectives.md
└── formative_assessment.md

pcap/
├── README.md (updated)
└── samples/
    └── README.md

Makefile
VERSIONS.md
pytest.ini
```

**Files to update:**
- `setup/requirements.txt` — Replace with pinned versions
- `scripts/utils/logger.py` — Replace with enhanced version
- `tests/test_exercises.py` — Replace with pytest-compatible version
- `docs/theory_summary.md` — Replace with extended version

**No files need to be deleted.**

---

## Contributing

When making changes:

1. Add entry under `[Unreleased]` section
2. Use categories: Added, Changed, Deprecated, Removed, Fixed, Security
3. Reference files affected
4. Update version table if releasing

---

*Computer Networks — Week 7 Laboratory Kit*  
*ASE Bucharest, CSIE | by ing. dr. Antonio Clim*
