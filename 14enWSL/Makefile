# ═══════════════════════════════════════════════════════════════════════════════
# Makefile — Week 14 Lab Kit Extended Orchestrator
# ═══════════════════════════════════════════════════════════════════════════════
# NETWORKING class — ASE, CSIE | Computer Networks Laboratory
# by ing. dr. Antonio Clim
#
# Version: 2.0.0 (Extended with anti-AI assessment and improved tooling)
# Usage: make <target>
# Run `make help` to see all available targets
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: help install install-dev lint lint-fix format test test-cov smoke typecheck \
        quiz quiz-random quiz-quick quiz-verify quiz-export exam exam-practice \
        docker-up docker-down docker-logs docker-ps docker-restart docker-rebuild \
        validate validate-full capture demo clean clean-docker clean-all \
        ci ci-full security docs verify-env all

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

PYTHON := python3
PIP := pip3
DOCKER_COMPOSE := docker compose -f docker/docker-compose.yml
PYTEST := $(PYTHON) -m pytest
RUFF := $(PYTHON) -m ruff
MYPY := $(PYTHON) -m mypy

# Colours for output
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
CYAN := \033[0;36m
BOLD := \033[1m
NC := \033[0m

# Version info
VERSION := 2.0.0
WEEK := 14

# ═══════════════════════════════════════════════════════════════════════════════
# HELP
# ═══════════════════════════════════════════════════════════════════════════════

help:
	@echo ""
	@echo "$(CYAN)╔════════════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(CYAN)║$(NC)  $(BOLD)Week $(WEEK) Lab Kit v$(VERSION) — Available Commands$(NC)                     $(CYAN)║$(NC)"
	@echo "$(CYAN)╠════════════════════════════════════════════════════════════════════╣$(NC)"
	@echo "$(CYAN)║$(NC)                                                                    $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)  $(YELLOW)Setup & Installation:$(NC)                                            $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make install        - Install all dependencies                  $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make install-dev    - Install with development tools            $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make verify-env     - Verify environment setup                  $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)                                                                    $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)  $(YELLOW)Code Quality:$(NC)                                                    $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make lint           - Run linter (ruff check)                   $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make lint-fix       - Auto-fix lint issues                      $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make format         - Format code (ruff format)                 $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make typecheck      - Run type checker (mypy)                   $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)                                                                    $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)  $(YELLOW)Testing:$(NC)                                                         $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make test           - Run all unit tests                        $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make test-cov       - Run tests with coverage report            $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make smoke          - Run smoke tests only                      $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make validate       - Validate kit integrity                    $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make validate-full  - Full validation with all checks           $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)                                                                    $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)  $(YELLOW)Docker Environment:$(NC)                                              $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make docker-up      - Start lab containers                      $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make docker-down    - Stop lab containers                       $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make docker-restart - Restart all containers                    $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make docker-logs    - View container logs (follow)              $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make docker-ps      - Show container status                     $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make docker-rebuild - Rebuild Docker images                     $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)                                                                    $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)  $(YELLOW)Learning & Assessment:$(NC)                                           $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make quiz           - Run formative quiz (standard)             $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make quiz-random    - Run quiz with randomised questions        $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make quiz-quick     - Run quick quiz (5 questions)              $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make quiz-verify    - Run quiz with environment verification    $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make quiz-export    - Export quiz to JSON/Moodle                $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make exam           - Start practical examination               $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make exam-practice  - Practice exam (no grading)                $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)                                                                    $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)  $(YELLOW)Network Tools:$(NC)                                                   $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make capture        - Start traffic capture                     $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make demo           - Run demonstration                         $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)                                                                    $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)  $(YELLOW)Maintenance:$(NC)                                                     $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make clean          - Clean generated artefacts                 $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make clean-docker   - Clean Docker resources                    $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make clean-all      - Full cleanup                              $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)                                                                    $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)  $(YELLOW)CI/CD:$(NC)                                                           $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make ci             - Run local CI pipeline (lint+test)         $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make ci-full        - Full CI (lint+typecheck+test+security)    $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make security       - Run security scan (bandit)                $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)                                                                    $(CYAN)║$(NC)"
	@echo "$(CYAN)╚════════════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(GREEN)NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim$(NC)"
	@echo "$(CYAN)Version: $(VERSION) | Week: $(WEEK)$(NC)"
	@echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP & INSTALLATION
# ═══════════════════════════════════════════════════════════════════════════════

install:
	@echo "$(CYAN)Installing dependencies...$(NC)"
	$(PIP) install --upgrade pip
	$(PIP) install -r setup/requirements.txt
	@echo "$(GREEN)Dependencies installed$(NC)"

install-dev: install
	@echo "$(CYAN)Installing development dependencies...$(NC)"
	$(PIP) install ruff mypy pytest pytest-cov pytest-timeout bandit pip-audit pre-commit
	@echo "$(CYAN)Setting up pre-commit hooks...$(NC)"
	pre-commit install || true
	@echo "$(GREEN)Development environment ready$(NC)"

verify-env:
	@echo "$(CYAN)Verifying environment...$(NC)"
	@$(PYTHON) setup/verify_environment.py || echo "$(YELLOW)Run setup/verify_environment.py manually$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# CODE QUALITY
# ═══════════════════════════════════════════════════════════════════════════════

lint:
	@echo "$(CYAN)Running linter...$(NC)"
	$(RUFF) check src/ scripts/ tests/ formative/ || true
	@echo "$(GREEN)Linting complete$(NC)"

lint-fix:
	@echo "$(CYAN)Auto-fixing lint issues...$(NC)"
	$(RUFF) check --fix src/ scripts/ tests/ formative/
	$(RUFF) format src/ scripts/ tests/ formative/
	@echo "$(GREEN)Lint fixes applied$(NC)"

format:
	@echo "$(CYAN)Formatting code...$(NC)"
	$(RUFF) format src/ scripts/ tests/ formative/
	@echo "$(GREEN)Formatting complete$(NC)"

typecheck:
	@echo "$(CYAN)Running type checker...$(NC)"
	$(MYPY) src/ scripts/ formative/ --config-file mypy.ini || true
	@echo "$(GREEN)Type checking complete$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

test:
	@echo "$(CYAN)Running all tests...$(NC)"
	$(PYTEST) tests/ -v --tb=short --timeout=60
	@echo "$(GREEN)Tests complete$(NC)"

test-cov:
	@echo "$(CYAN)Running tests with coverage...$(NC)"
	$(PYTEST) tests/ -v --tb=short --timeout=60 \
		--cov=src --cov=scripts --cov=formative \
		--cov-report=term-missing --cov-report=html
	@echo "$(GREEN)Coverage report: htmlcov/index.html$(NC)"

smoke:
	@echo "$(CYAN)Running smoke tests...$(NC)"
	$(PYTHON) tests/smoke_test.py
	@echo "$(GREEN)Smoke tests complete$(NC)"

validate:
	@echo "$(CYAN)Validating kit integrity...$(NC)"
	@$(PYTHON) -c "import yaml; yaml.safe_load(open('formative/quiz.yaml'))" && \
		echo "  $(GREEN)YAML quiz valid$(NC)"
	@$(PYTHON) -c "import json; json.load(open('formative/quiz.json'))" && \
		echo "  $(GREEN)JSON quiz valid$(NC)"
	@$(PYTHON) -m py_compile formative/run_quiz.py && \
		echo "  $(GREEN)Quiz runner valid$(NC)"
	@test -f README.md && echo "  $(GREEN)README.md exists$(NC)"
	@test -f CHANGELOG.md && echo "  $(GREEN)CHANGELOG.md exists$(NC)"
	@test -f docs/learning_objectives.md && echo "  $(GREEN)LO matrix exists$(NC)"
	@test -f docs/grading_rubric.md && echo "  $(GREEN)Grading rubric exists$(NC)" || \
		echo "  $(YELLOW)Grading rubric missing$(NC)"
	@echo "$(GREEN)Kit validation complete$(NC)"

validate-full: validate lint typecheck
	@echo "$(CYAN)Running full validation...$(NC)"
	@$(PYTHON) scripts/validate_kit.py || true
	@echo "$(GREEN)Full validation complete$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# DOCKER ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════

docker-up:
	@echo "$(CYAN)Starting lab environment...$(NC)"
	$(DOCKER_COMPOSE) up -d
	@echo "$(YELLOW)Waiting for services to initialise...$(NC)"
	@sleep 10
	@$(DOCKER_COMPOSE) ps
	@echo ""
	@echo "$(GREEN)Lab environment ready$(NC)"
	@echo ""
	@echo "$(CYAN)Access points:$(NC)"
	@echo "  Load Balancer: http://localhost:8080"
	@echo "  Backend 1:     http://localhost:8001"
	@echo "  Backend 2:     http://localhost:8002"
	@echo "  TCP Echo:      localhost:9090"
	@echo "  Portainer:     http://localhost:9000"
	@echo ""

docker-down:
	@echo "$(CYAN)Stopping lab environment...$(NC)"
	$(DOCKER_COMPOSE) down
	@echo "$(GREEN)Lab environment stopped$(NC)"

docker-logs:
	@echo "$(CYAN)Container logs (Ctrl+C to exit)...$(NC)"
	$(DOCKER_COMPOSE) logs -f

docker-ps:
	@echo "$(CYAN)Container status:$(NC)"
	@$(DOCKER_COMPOSE) ps

docker-restart:
	@echo "$(CYAN)Restarting lab environment...$(NC)"
	$(DOCKER_COMPOSE) restart
	@echo "$(GREEN)Containers restarted$(NC)"

docker-rebuild:
	@echo "$(CYAN)Rebuilding Docker images...$(NC)"
	$(DOCKER_COMPOSE) build --no-cache
	@echo "$(GREEN)Images rebuilt$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# LEARNING & ASSESSMENT
# ═══════════════════════════════════════════════════════════════════════════════

quiz:
	@echo "$(CYAN)Starting formative quiz...$(NC)"
	@echo ""
	@$(PYTHON) formative/run_quiz.py

quiz-random:
	@echo "$(CYAN)Starting quiz (randomised)...$(NC)"
	@echo ""
	@$(PYTHON) formative/run_quiz.py --random

quiz-quick:
	@echo "$(CYAN)Starting quick quiz (5 questions)...$(NC)"
	@echo ""
	@$(PYTHON) formative/run_quiz.py --random --limit 5 --no-prediction

quiz-verify:
	@echo "$(CYAN)Starting quiz with environment verification...$(NC)"
	@echo ""
	@echo "$(YELLOW)This quiz requires a running Docker environment!$(NC)"
	@echo ""
	@$(PYTHON) formative/anti_ai_verification.py || \
		echo "$(RED)Anti-AI verification not available. Run standard quiz.$(NC)"

quiz-export:
	@echo "$(CYAN)Exporting quiz...$(NC)"
	@$(PYTHON) formative/run_quiz.py --export json --output quiz_export.json || true
	@$(PYTHON) formative/export_moodle.py || true
	@echo "$(GREEN)Quiz exported$(NC)"

exam:
	@echo "$(CYAN)Starting practical examination...$(NC)"
	@echo ""
	@echo "$(RED)This is a GRADED examination!$(NC)"
	@echo "$(YELLOW)    Requires running Docker environment.$(NC)"
	@echo "$(YELLOW)    Time limits are enforced.$(NC)"
	@echo ""
	@$(PYTHON) formative/practical_exam.py || \
		echo "$(RED)Practical exam not available. Check formative/practical_exam.py$(NC)"

exam-practice:
	@echo "$(CYAN)Starting practice examination...$(NC)"
	@echo ""
	@echo "$(GREEN)Practice mode - no grading$(NC)"
	@echo ""
	@$(PYTHON) formative/practical_exam.py --practice || \
		echo "$(YELLOW)Practice exam not available$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# NETWORK TOOLS
# ═══════════════════════════════════════════════════════════════════════════════

capture:
	@echo "$(CYAN)Starting traffic capture...$(NC)"
	@$(PYTHON) scripts/capture_traffic.py

demo:
	@echo "$(CYAN)Running demonstration...$(NC)"
	@$(PYTHON) scripts/run_demo.py

# ═══════════════════════════════════════════════════════════════════════════════
# MAINTENANCE
# ═══════════════════════════════════════════════════════════════════════════════

clean:
	@echo "$(CYAN)Cleaning artefacts...$(NC)"
	@rm -rf artefacts/*.pcap artefacts/*.log 2>/dev/null || true
	@rm -rf __pycache__ */__pycache__ */*/__pycache__ 2>/dev/null || true
	@rm -rf .pytest_cache .ruff_cache .mypy_cache 2>/dev/null || true
	@rm -rf *.pyc */*.pyc */*/*.pyc 2>/dev/null || true
	@rm -rf .coverage coverage.xml htmlcov/ 2>/dev/null || true
	@rm -rf exam_report_*.json quiz_export*.json 2>/dev/null || true
	@echo "$(GREEN)Artefacts cleaned$(NC)"

clean-docker:
	@echo "$(CYAN)Cleaning Docker resources...$(NC)"
	@$(DOCKER_COMPOSE) down --volumes --remove-orphans 2>/dev/null || true
	@docker image prune -f 2>/dev/null || true
	@echo "$(GREEN)Docker resources cleaned$(NC)"

clean-all: clean clean-docker
	@echo "$(GREEN)Full cleanup complete$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# CI/CD
# ═══════════════════════════════════════════════════════════════════════════════

ci: lint test validate
	@echo ""
	@echo "$(GREEN)═══════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)Local CI pipeline complete$(NC)"
	@echo "$(GREEN)═══════════════════════════════════════════════════════$(NC)"

ci-full: lint typecheck test-cov validate-full security
	@echo ""
	@echo "$(GREEN)═══════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)Full CI pipeline complete$(NC)"
	@echo "$(GREEN)═══════════════════════════════════════════════════════$(NC)"

security:
	@echo "$(CYAN)Running security scan...$(NC)"
	@$(PYTHON) -m bandit -r src/ scripts/ formative/ -ll -ii || true
	@echo "$(GREEN)Security scan complete$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# DOCUMENTATION
# ═══════════════════════════════════════════════════════════════════════════════

docs:
	@echo "$(CYAN)Documentation overview:$(NC)"
	@echo ""
	@echo "  Core Documentation:"
	@echo "    - README.md                      Main documentation"
	@echo "    - docs/learning_objectives.md    LO traceability matrix"
	@echo "    - docs/grading_rubric.md         Evaluation criteria"
	@echo ""
	@echo "  Learning Resources:"
	@echo "    - docs/theory_summary.md         Theory review"
	@echo "    - docs/misconceptions.md         Common errors"
	@echo "    - docs/troubleshooting.md        Problem solving"
	@echo "    - docs/commands_cheatsheet.md    Quick reference"
	@echo ""
	@echo "  Pedagogical Tools:"
	@echo "    - docs/peer_instruction.md       ConcepTests"
	@echo "    - docs/parsons_problems.md       Code ordering"
	@echo "    - docs/code_tracing.md           Trace exercises"
	@echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# FULL SETUP
# ═══════════════════════════════════════════════════════════════════════════════

all: install verify-env docker-up smoke
	@echo ""
	@echo "$(GREEN)═══════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)Lab environment ready!$(NC)"
	@echo "$(GREEN)═══════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(CYAN)Next steps:$(NC)"
	@echo "  1. Run 'make quiz' to test your knowledge"
	@echo "  2. Run 'make quiz-verify' for environment-verified assessment"
	@echo "  3. Open http://localhost:8080 in your browser"
	@echo "  4. Start Wireshark and capture traffic"
	@echo ""
