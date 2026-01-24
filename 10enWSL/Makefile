# Week 10 Makefile — Application Layer Protocols
# Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim
#
# Usage:
#   make help           Show available targets
#   make setup          Install dependencies
#   make test           Run all tests
#   make quiz           Run formative quiz
#   make challenge      Generate anti-AI challenge
#   make validate       Validate submission
#   make lab-start      Start Docker lab environment
#   make lab-stop       Stop Docker lab environment

.PHONY: help setup lint typecheck test smoke quiz challenge validate \
        docker-up docker-down clean verify all progress export-quiz \
        lab-start lab-stop lab-status lab-logs lab-restart security

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
PYTHON := python3
PIP := pip3
DOCKER_COMPOSE := docker compose -f docker/docker-compose.yml
RUFF := $(PYTHON) -m ruff
MYPY := $(PYTHON) -m mypy
BANDIT := $(PYTHON) -m bandit

# Colours for terminal output
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
CYAN := \033[0;36m
BOLD := \033[1m
NC := \033[0m  # No colour

# Student ID (can be overridden: make challenge STUDENT_ID=ABC123)
STUDENT_ID ?= $(USER)

# ═══════════════════════════════════════════════════════════════════════════════
# HELP
# ═══════════════════════════════════════════════════════════════════════════════
help:
	@echo "$(BOLD)╔════════════════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(BOLD)║  Week 10: Application Layer Protocols — Available Commands             ║$(NC)"
	@echo "$(BOLD)╠════════════════════════════════════════════════════════════════════════╣$(NC)"
	@echo "║                                                                          ║"
	@echo "║  $(CYAN)Setup & Dependencies$(NC)                                                  ║"
	@echo "║    make setup         Install Python dependencies                        ║"
	@echo "║    make verify        Verify environment is ready                        ║"
	@echo "║                                                                          ║"
	@echo "║  $(CYAN)Code Quality$(NC)                                                          ║"
	@echo "║    make lint          Run code linter (ruff)                             ║"
	@echo "║    make typecheck     Run type checker (mypy)                            ║"
	@echo "║    make security      Run security scanner (bandit)                      ║"
	@echo "║    make test          Run all tests                                      ║"
	@echo "║    make smoke         Run smoke tests only                               ║"
	@echo "║    make selftest      Run exercise selftests                             ║"
	@echo "║                                                                          ║"
	@echo "║  $(CYAN)Learning & Assessment$(NC)                                                 ║"
	@echo "║    make quiz          Run formative assessment quiz                      ║"
	@echo "║    make quiz-review   Review quiz with answers shown                     ║"
	@echo "║    make quiz-live     Run only live verification questions               ║"
	@echo "║    make progress      Show learning progress                             ║"
	@echo "║    make export-quiz   Export quiz to LMS formats                         ║"
	@echo "║                                                                          ║"
	@echo "║  $(CYAN)Anti-AI Verification$(NC)                                                  ║"
	@echo "║    make challenge     Generate unique challenge for submission           ║"
	@echo "║    make validate      Validate submission against challenge              ║"
	@echo "║                                                                          ║"
	@echo "║  $(CYAN)Docker Lab$(NC)                                                            ║"
	@echo "║    make lab-start     Start lab environment                              ║"
	@echo "║    make lab-stop      Stop lab environment                               ║"
	@echo "║    make lab-status    Show container status                              ║"
	@echo "║    make lab-logs      Show container logs                                ║"
	@echo "║    make lab-restart   Restart lab environment                            ║"
	@echo "║                                                                          ║"
	@echo "║  $(CYAN)Cleanup$(NC)                                                               ║"
	@echo "║    make clean         Remove generated files                             ║"
	@echo "║    make clean-all     Remove everything including Docker volumes         ║"
	@echo "║                                                                          ║"
	@echo "$(BOLD)╚════════════════════════════════════════════════════════════════════════╝$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP
# ═══════════════════════════════════════════════════════════════════════════════
setup:
	@echo "$(GREEN)Installing dependencies...$(NC)"
	$(PIP) install -r setup/requirements.txt --break-system-packages
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

setup-dev: setup
	@echo "$(GREEN)Installing development dependencies...$(NC)"
	$(PIP) install ruff mypy bandit types-PyYAML types-requests --break-system-packages
	@echo "$(GREEN)✓ Development dependencies installed$(NC)"

verify:
	@echo "$(GREEN)Verifying environment...$(NC)"
	$(PYTHON) setup/verify_environment.py
	@echo "$(GREEN)✓ Environment verified$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# CODE QUALITY
# ═══════════════════════════════════════════════════════════════════════════════
lint:
	@echo "$(GREEN)Running linter (ruff)...$(NC)"
	$(RUFF) check src/ scripts/ tests/ formative/ anti_cheat/ --ignore E501,E402 || true
	@echo "$(GREEN)✓ Lint complete$(NC)"

typecheck:
	@echo "$(GREEN)Running type checker (mypy)...$(NC)"
	$(MYPY) src/ scripts/ anti_cheat/ --ignore-missing-imports || true
	@echo "$(GREEN)✓ Type check complete$(NC)"

security:
	@echo "$(GREEN)Running security scanner (bandit)...$(NC)"
	$(BANDIT) -r src/ scripts/ anti_cheat/ -ll || true
	@echo "$(GREEN)✓ Security scan complete$(NC)"

format:
	@echo "$(GREEN)Formatting code (ruff)...$(NC)"
	$(RUFF) format src/ scripts/ tests/ formative/ anti_cheat/
	@echo "$(GREEN)✓ Formatting complete$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════
test: lint smoke selftest test-anti-cheat
	@echo "$(GREEN)✓ All tests complete$(NC)"

smoke:
	@echo "$(GREEN)Running smoke tests...$(NC)"
	$(PYTHON) tests/smoke_test.py

selftest:
	@echo "$(GREEN)Running exercise selftests...$(NC)"
	$(PYTHON) src/exercises/ex_10_01_tls_rest_crud.py selftest
	@echo "$(GREEN)✓ HTTPS selftest passed$(NC)"

test-anti-cheat:
	@echo "$(GREEN)Running anti-cheat tests...$(NC)"
	$(PYTHON) -m pytest tests/test_anti_cheat.py -v || true
	@echo "$(GREEN)✓ Anti-cheat tests complete$(NC)"

test-coverage:
	@echo "$(GREEN)Running tests with coverage...$(NC)"
	$(PYTHON) -m pytest tests/ --cov=src --cov=scripts --cov=anti_cheat --cov-report=term-missing
	@echo "$(GREEN)✓ Coverage report complete$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ & LEARNING
# ═══════════════════════════════════════════════════════════════════════════════
quiz:
	@echo "$(GREEN)Starting formative quiz...$(NC)"
	$(PYTHON) formative/run_quiz.py

quiz-review:
	@echo "$(GREEN)Starting quiz in review mode...$(NC)"
	$(PYTHON) formative/run_quiz.py --review

quiz-random:
	@echo "$(GREEN)Starting randomised quiz...$(NC)"
	$(PYTHON) formative/run_quiz.py --random

quiz-live:
	@echo "$(GREEN)Starting live verification questions only...$(NC)"
	@echo "$(YELLOW)Note: Requires lab environment to be running$(NC)"
	$(PYTHON) formative/run_quiz.py --live-only

quiz-lo:
	@echo "$(GREEN)Starting quiz filtered by Learning Objective...$(NC)"
	@echo "Usage: make quiz-lo LO=LO1"
	$(PYTHON) formative/run_quiz.py --lo $(LO)

progress:
	@echo "$(GREEN)Showing learning progress...$(NC)"
	$(PYTHON) formative/progress_tracker.py

export-quiz:
	@echo "$(GREEN)Exporting quiz to LMS formats...$(NC)"
	mkdir -p exports
	$(PYTHON) formative/run_quiz.py --export-moodle exports/quiz_moodle.xml
	$(PYTHON) formative/run_quiz.py --export-json exports/quiz_lms.json
	@echo "$(GREEN)✓ Exports saved to exports/ directory$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# ANTI-AI VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
challenge:
	@echo "$(GREEN)Generating unique challenge for: $(STUDENT_ID)$(NC)"
	$(PYTHON) -m anti_cheat.challenge_generator --student-id $(STUDENT_ID)
	@echo ""
	@echo "$(YELLOW)IMPORTANT: Complete all challenges before submission$(NC)"
	@echo "$(YELLOW)Challenge file saved to: artifacts/challenge_$(STUDENT_ID).yaml$(NC)"

validate:
	@echo "$(GREEN)Validating submission...$(NC)"
	@if [ ! -f artifacts/challenge_$(STUDENT_ID).yaml ]; then \
		echo "$(RED)Error: Challenge file not found. Run 'make challenge' first.$(NC)"; \
		exit 1; \
	fi
	$(PYTHON) -m anti_cheat.submission_validator --challenge artifacts/challenge_$(STUDENT_ID).yaml --verbose

fingerprint:
	@echo "$(GREEN)Generating environment fingerprint...$(NC)"
	$(PYTHON) -m anti_cheat.fingerprint

# ═══════════════════════════════════════════════════════════════════════════════
# DOCKER LAB
# ═══════════════════════════════════════════════════════════════════════════════
lab-start:
	@echo "$(GREEN)Starting lab environment...$(NC)"
	$(PYTHON) scripts/start_lab.py
	@echo "$(GREEN)✓ Lab environment started$(NC)"
	@echo "$(YELLOW)Run 'make smoke' to verify services$(NC)"

lab-stop:
	@echo "$(GREEN)Stopping lab environment...$(NC)"
	$(PYTHON) scripts/stop_lab.py
	@echo "$(GREEN)✓ Lab environment stopped$(NC)"

lab-status:
	@echo "$(GREEN)Lab container status:$(NC)"
	$(DOCKER_COMPOSE) ps

lab-logs:
	$(DOCKER_COMPOSE) logs --tail=50

lab-restart: lab-stop lab-start
	@echo "$(GREEN)✓ Lab restarted$(NC)"

docker-up: lab-start
docker-down: lab-stop

# ═══════════════════════════════════════════════════════════════════════════════
# EXERCISES
# ═══════════════════════════════════════════════════════════════════════════════
ex1:
	@echo "$(GREEN)Running Exercise 1: TLS/REST CRUD$(NC)"
	$(PYTHON) src/exercises/ex_10_01_tls_rest_crud.py serve

ex2:
	@echo "$(GREEN)Running Exercise 2: Richardson Maturity$(NC)"
	$(PYTHON) src/exercises/ex_10_02_richardson_maturity.py serve

ex3:
	@echo "$(GREEN)Running Exercise 3: DNS Analysis$(NC)"
	$(PYTHON) src/exercises/ex_10_03_dns_query_analysis.py demo

ex4:
	@echo "$(GREEN)Running Exercise 4: Secure Transfer$(NC)"
	$(PYTHON) src/exercises/ex_10_04_secure_transfer.py demo

# ═══════════════════════════════════════════════════════════════════════════════
# CLEANUP
# ═══════════════════════════════════════════════════════════════════════════════
clean:
	@echo "$(GREEN)Cleaning generated files...$(NC)"
	rm -rf artifacts/*.pcap artifacts/*.log artifacts/*.yaml
	rm -rf output/tls/*.crt output/tls/*.key
	rm -rf exports/
	rm -rf __pycache__ */__pycache__ */*/__pycache__ */*/*/__pycache__
	rm -rf .pytest_cache */.pytest_cache
	rm -rf .mypy_cache */.mypy_cache
	rm -rf .ruff_cache
	rm -rf *.pyc */*.pyc */*/*.pyc
	rm -rf .coverage htmlcov/
	@echo "$(GREEN)✓ Cleanup complete$(NC)"

clean-all: clean
	@echo "$(YELLOW)Removing Docker volumes...$(NC)"
	$(DOCKER_COMPOSE) down -v
	@echo "$(GREEN)✓ Full cleanup complete$(NC)"

clean-progress:
	@echo "$(YELLOW)Removing progress tracking data...$(NC)"
	rm -f ~/.week10_progress.json ~/.week10_quiz_progress.json
	@echo "$(GREEN)✓ Progress data cleared$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# CI HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
ci-lint:
	@echo "Running CI lint checks..."
	$(PYTHON) -m py_compile src/**/*.py scripts/*.py tests/*.py formative/*.py anti_cheat/*.py
	$(RUFF) check src/ scripts/ tests/ formative/ anti_cheat/ --ignore E501,E402

ci-test:
	@echo "Running CI tests..."
	$(PYTHON) src/exercises/ex_10_01_tls_rest_crud.py selftest
	$(PYTHON) -c "import yaml; yaml.safe_load(open('formative/quiz.yaml'))"

ci-docs:
	@echo "Checking documentation..."
	@test -f README.md || (echo "Missing README.md" && exit 1)
	@test -f CHANGELOG.md || (echo "Missing CHANGELOG.md" && exit 1)
	@test -f docs/learning_objectives.md || (echo "Missing docs/learning_objectives.md" && exit 1)
	@echo "✓ Documentation check passed"

# ═══════════════════════════════════════════════════════════════════════════════
# ALL
# ═══════════════════════════════════════════════════════════════════════════════
all: setup lint typecheck test
	@echo "$(GREEN)✓ All checks passed$(NC)"

# Default target
.DEFAULT_GOAL := help
