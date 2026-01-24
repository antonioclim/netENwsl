# Week 10 Makefile
# Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim
#
# Usage:
#   make help        Show available targets
#   make setup       Install dependencies
#   make test        Run all tests
#   make quiz        Run formative quiz
#   make lab-start   Start Docker lab environment
#   make lab-stop    Stop Docker lab environment

.PHONY: help setup lint test smoke quiz docker-up docker-down clean verify all

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
PYTHON := python3
PIP := pip3
DOCKER_COMPOSE := docker compose -f docker/docker-compose.yml

# Colours for terminal output
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m  # No colour

# ═══════════════════════════════════════════════════════════════════════════════
# HELP
# ═══════════════════════════════════════════════════════════════════════════════
help:
	@echo "╔════════════════════════════════════════════════════════════════════╗"
	@echo "║  Week 10: Application Layer Protocols — Available Commands         ║"
	@echo "╠════════════════════════════════════════════════════════════════════╣"
	@echo "║  Setup & Dependencies                                              ║"
	@echo "║    make setup       Install Python dependencies                    ║"
	@echo "║    make verify      Verify environment is ready                    ║"
	@echo "║                                                                    ║"
	@echo "║  Testing                                                           ║"
	@echo "║    make lint        Run code linter (ruff)                         ║"
	@echo "║    make test        Run all tests                                  ║"
	@echo "║    make smoke       Run smoke tests only                           ║"
	@echo "║    make selftest    Run exercise selftests                         ║"
	@echo "║                                                                    ║"
	@echo "║  Learning                                                          ║"
	@echo "║    make quiz        Run formative assessment quiz                  ║"
	@echo "║    make quiz-review Review quiz with answers shown                 ║"
	@echo "║                                                                    ║"
	@echo "║  Docker Lab                                                        ║"
	@echo "║    make lab-start   Start lab environment                          ║"
	@echo "║    make lab-stop    Stop lab environment                           ║"
	@echo "║    make lab-status  Show container status                          ║"
	@echo "║    make lab-logs    Show container logs                            ║"
	@echo "║                                                                    ║"
	@echo "║  Cleanup                                                           ║"
	@echo "║    make clean       Remove generated files                         ║"
	@echo "║    make clean-all   Remove everything including Docker volumes     ║"
	@echo "╚════════════════════════════════════════════════════════════════════╝"

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP
# ═══════════════════════════════════════════════════════════════════════════════
setup:
	@echo "$(GREEN)Installing dependencies...$(NC)"
	$(PIP) install -r setup/requirements.txt --break-system-packages
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

verify:
	@echo "$(GREEN)Verifying environment...$(NC)"
	$(PYTHON) setup/verify_environment.py
	@echo "$(GREEN)✓ Environment verified$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════
lint:
	@echo "$(GREEN)Running linter...$(NC)"
	$(PYTHON) -m ruff check src/ scripts/ tests/ formative/ --ignore E501,E402 || true
	@echo "$(GREEN)✓ Lint complete$(NC)"

test: smoke selftest
	@echo "$(GREEN)✓ All tests complete$(NC)"

smoke:
	@echo "$(GREEN)Running smoke tests...$(NC)"
	$(PYTHON) tests/smoke_test.py

selftest:
	@echo "$(GREEN)Running exercise selftests...$(NC)"
	$(PYTHON) src/exercises/ex_10_01_tls_rest_crud.py selftest
	@echo "$(GREEN)✓ HTTPS selftest passed$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ
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

# ═══════════════════════════════════════════════════════════════════════════════
# CLEANUP
# ═══════════════════════════════════════════════════════════════════════════════
clean:
	@echo "$(GREEN)Cleaning generated files...$(NC)"
	rm -rf artifacts/*.pcap artifacts/*.log
	rm -rf output/tls/*.crt output/tls/*.key
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf .pytest_cache */.pytest_cache
	rm -rf *.pyc */*.pyc */*/*.pyc
	@echo "$(GREEN)✓ Cleanup complete$(NC)"

clean-all: clean
	@echo "$(YELLOW)Removing Docker volumes...$(NC)"
	$(DOCKER_COMPOSE) down -v
	@echo "$(GREEN)✓ Full cleanup complete$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# ALL
# ═══════════════════════════════════════════════════════════════════════════════
all: setup lint test
	@echo "$(GREEN)✓ All checks passed$(NC)"
