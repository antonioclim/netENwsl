# Changelog

All notable changes to the Week 14 Laboratory Kit.

## [2.0.0] - 2025-01-23

### Added

- Pedagogical support files:
  - `docs/peer_instruction.md` - 5 MCQ questions with misconception analysis
  - `docs/pair_programming_guide.md` - Collaborative exercise structure
  - `docs/misconceptions.md` - 14 common misconceptions with corrections
  - `docs/glossary.md` - Technical terms and definitions
  - `docs/code_tracing.md` - 5 code tracing exercises
  - `docs/parsons_problems.md` - 5 code reordering exercises
  - `docs/concept_analogies.md` - 8 CPA concrete phase analogies
- Prediction prompts in exercises for active learning
- Reflection prompts after assessments
- Subgoal labels in all Python exercises

### Changed

- Renamed exercise files with descriptive suffixes:
  - `ex_14_01.py` → `ex_14_01_review_drills.py`
  - `ex_14_02.py` → `ex_14_02_verification_harness.py`
  - `ex_14_03.py` → `ex_14_03_advanced_challenges.py`
- Enhanced docstrings with level, time estimates and pair programming notes
- Fixed British English spellings (analyse, synchronise)
- Removed AI signal words for academic authenticity
- Updated README with pedagogical resources section

### Fixed

- Oxford comma usage standardised
- American spellings corrected to British English

---

## [1.0.0] - 2025-01-07

### Added

- Initial release of WEEK14_WSLkit
- Complete Docker Compose infrastructure with:
  - Two backend HTTP servers (app1, app2)
  - Load balancer / reverse proxy (lb)
  - Client container for testing
  - TCP echo server
- Python management scripts:
  - `start_lab.py` - Environment launcher with health checks
  - `stop_lab.py` - Graceful shutdown
  - `cleanup.py` - Full cleanup for next week
  - `capture_traffic.py` - Packet capture automation
  - `run_demo.py` - Automated demonstrations
- Setup scripts:
  - `verify_environment.py` - Prerequisites checker
  - `install_prerequisites.py` - Installation helper
  - `configure_docker.py` - Docker configuration
- Test suite:
  - `test_environment.py` - Environment validation
  - `test_exercises.py` - Exercise verification
  - `smoke_test.py` - Quick functionality check
- Documentation:
  - Complete README with exercises
  - Theory summary
  - Commands cheatsheet
  - Troubleshooting guide
- Laboratory exercises:
  - Exercise 1: Environment verification
  - Exercise 2: Load balancer behaviour analysis
  - Exercise 3: TCP echo protocol testing
  - Exercise 4: Packet capture and analysis
- Source code:
  - Backend HTTP server implementation
  - Load balancer proxy implementation
  - TCP echo server and client
  - HTTP client for traffic generation
  - Network utilities library

### Infrastructure

- Dual Docker network topology (frontend/backend)
- Fixed IP addressing scheme (172.20.0.0/24, 172.21.0.0/24)
- Health checks for all services
- Port mappings for host access

---

*NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim*
