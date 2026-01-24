# Makefile — Week 2 Laboratory Kit
# NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim
#
# Usage: make [target]
# Run 'make help' to see all available targets.

.PHONY: help install lint test smoke quiz docker-up docker-down docker-logs \
        clean verify all ci check-syntax

# Configuration
PYTHON := python3
PIP := pip
DOCKER_COMPOSE := docker compose -f docker/docker-compose.yml
QUIZ_FILE := formative/quiz.yaml

# Colours for terminal output
CYAN := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
RESET := \033[0m

# Default target
.DEFAULT_GOAL := help

# ═══════════════════════════════════════════════════════════════════════════════
# HELP
# ═══════════════════════════════════════════════════════════════════════════════

help: ## Show this help message
	@echo ""
	@echo "$(CYAN)Week 2 Laboratory Kit — Available Commands$(RESET)"
	@echo ""
	@echo "$(GREEN)Development:$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(CYAN)%-15s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Quick Start:$(RESET)"
	@echo "  1. make install     # Install dependencies"
	@echo "  2. make verify      # Check environment"
	@echo "  3. make docker-up   # Start lab containers"
	@echo "  4. make test        # Run all tests"
	@echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP
# ═══════════════════════════════════════════════════════════════════════════════

install: ## Install Python dependencies
	@echo "$(CYAN)Installing dependencies...$(RESET)"
	$(PIP) install -r setup/requirements.txt
	@echo "$(GREEN)✓ Dependencies installed$(RESET)"

verify: ## Verify environment is correctly configured
	@echo "$(CYAN)Verifying environment...$(RESET)"
	$(PYTHON) setup/verify_environment.py
	@echo "$(GREEN)✓ Environment verification complete$(RESET)"

# ═══════════════════════════════════════════════════════════════════════════════
# CODE QUALITY
# ═══════════════════════════════════════════════════════════════════════════════

check-syntax: ## Check Python syntax (no external deps)
	@echo "$(CYAN)Checking Python syntax...$(RESET)"
	@find src scripts tests formative -name "*.py" -exec $(PYTHON) -m py_compile {} \;
	@echo "$(GREEN)✓ No syntax errors$(RESET)"

lint: ## Run ruff linter on all Python files
	@echo "$(CYAN)Running ruff linter...$(RESET)"
	@$(PYTHON) -m ruff check src/ scripts/ tests/ formative/ --config ruff.toml || true
	@echo "$(GREEN)✓ Linting complete$(RESET)"

lint-fix: ## Run ruff with auto-fix
	@echo "$(CYAN)Running ruff with auto-fix...$(RESET)"
	$(PYTHON) -m ruff check --fix src/ scripts/ tests/ formative/ --config ruff.toml
	@echo "$(GREEN)✓ Auto-fixes applied$(RESET)"

# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

test: ## Run all tests with pytest
	@echo "$(CYAN)Running all tests...$(RESET)"
	$(PYTHON) -m pytest tests/ -v --tb=short
	@echo "$(GREEN)✓ All tests complete$(RESET)"

smoke: ## Run quick smoke tests only
	@echo "$(CYAN)Running smoke tests...$(RESET)"
	$(PYTHON) tests/smoke_test.py
	@echo "$(GREEN)✓ Smoke tests complete$(RESET)"

test-exercises: ## Run exercise-specific tests
	@echo "$(CYAN)Running exercise tests...$(RESET)"
	$(PYTHON) tests/test_exercises.py
	@echo "$(GREEN)✓ Exercise tests complete$(RESET)"

# ═══════════════════════════════════════════════════════════════════════════════
# FORMATIVE ASSESSMENT
# ═══════════════════════════════════════════════════════════════════════════════

quiz: ## Run the interactive formative quiz
	@echo "$(CYAN)Starting formative quiz...$(RESET)"
	$(PYTHON) formative/run_quiz.py

quiz-random: ## Run quiz with randomised questions
	$(PYTHON) formative/run_quiz.py --random

quiz-quick: ## Run a quick 5-question quiz
	$(PYTHON) formative/run_quiz.py --limit 5 --random

quiz-review: ## Review all questions with answers
	$(PYTHON) formative/run_quiz.py --review

# ═══════════════════════════════════════════════════════════════════════════════
# DOCKER
# ═══════════════════════════════════════════════════════════════════════════════

docker-up: ## Start laboratory Docker containers
	@echo "$(CYAN)Starting Docker containers...$(RESET)"
	$(DOCKER_COMPOSE) up -d
	@echo "$(GREEN)✓ Containers started$(RESET)"
	@echo ""
	@echo "Container status:"
	$(DOCKER_COMPOSE) ps

docker-down: ## Stop laboratory Docker containers
	@echo "$(CYAN)Stopping Docker containers...$(RESET)"
	$(DOCKER_COMPOSE) down
	@echo "$(GREEN)✓ Containers stopped$(RESET)"

docker-logs: ## View container logs (follow mode)
	$(DOCKER_COMPOSE) logs -f

docker-shell: ## Open shell in lab container
	docker exec -it week2_lab /bin/bash

docker-build: ## Rebuild Docker images
	@echo "$(CYAN)Building Docker images...$(RESET)"
	$(DOCKER_COMPOSE) build --no-cache
	@echo "$(GREEN)✓ Images rebuilt$(RESET)"

docker-status: ## Show container status
	$(DOCKER_COMPOSE) ps

# ═══════════════════════════════════════════════════════════════════════════════
# EXERCISES
# ═══════════════════════════════════════════════════════════════════════════════

run-tcp-server: ## Start TCP server (Exercise 1)
	$(PYTHON) src/exercises/ex_2_01_tcp.py server --port 9090

run-tcp-client: ## Run TCP client (Exercise 1)
	$(PYTHON) src/exercises/ex_2_01_tcp.py client --host 127.0.0.1 --port 9090 -m "Hello"

run-udp-server: ## Start UDP server (Exercise 2)
	$(PYTHON) src/exercises/ex_2_02_udp.py server --port 9091

run-udp-client: ## Run UDP client (Exercise 2)
	$(PYTHON) src/exercises/ex_2_02_udp.py client --host 127.0.0.1 --port 9091 -o ping

# ═══════════════════════════════════════════════════════════════════════════════
# CLEANUP
# ═══════════════════════════════════════════════════════════════════════════════

clean: ## Remove generated files and caches
	@echo "$(CYAN)Cleaning up...$(RESET)"
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf artifacts/*.pcap artifacts/*.log 2>/dev/null || true
	@echo "$(GREEN)✓ Cleanup complete$(RESET)"

clean-docker: ## Remove Docker containers, volumes and networks
	@echo "$(YELLOW)Warning: This will remove all Week 2 Docker resources$(RESET)"
	$(DOCKER_COMPOSE) down --volumes --remove-orphans
	@echo "$(GREEN)✓ Docker resources removed$(RESET)"

# ═══════════════════════════════════════════════════════════════════════════════
# CI/CD
# ═══════════════════════════════════════════════════════════════════════════════

ci: check-syntax lint test ## Run full CI pipeline (syntax + lint + tests)
	@echo "$(GREEN)✓ CI pipeline complete$(RESET)"

all: install verify ci ## Full setup and verification
	@echo "$(GREEN)✓ All checks passed$(RESET)"

# ═══════════════════════════════════════════════════════════════════════════════
# CAPTURE
# ═══════════════════════════════════════════════════════════════════════════════

capture: ## Start traffic capture (requires sudo)
	@echo "$(CYAN)Starting traffic capture...$(RESET)"
	@echo "$(YELLOW)Note: May require sudo for raw socket access$(RESET)"
	$(PYTHON) scripts/capture_traffic.py --interface eth0 --output pcap/capture_$$(date +%Y%m%d_%H%M%S).pcap
