# ═══════════════════════════════════════════════════════════════════════════════
# Makefile — Week 6: NAT/PAT & SDN Laboratory
# ═══════════════════════════════════════════════════════════════════════════════
# Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim
#
# Usage:
#   make help          Show available targets
#   make quiz          Run formative quiz
#   make test          Run all tests
#   make lint          Run code linter
#   make start         Start lab environment
#   make stop          Stop lab environment
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: help quiz quiz-random test smoke lint typecheck start stop clean verify docker-build docker-up docker-down all

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

PYTHON := python3
PIP := pip
DOCKER_COMPOSE := docker compose -f docker/docker-compose.yml

# Colours for terminal output
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m  # No colour

# ─────────────────────────────────────────────────────────────────────────────
# HELP
# ─────────────────────────────────────────────────────────────────────────────

help:
	@echo ""
	@echo "═══════════════════════════════════════════════════════════════════"
	@echo "  Week 6 Laboratory — Available Targets"
	@echo "═══════════════════════════════════════════════════════════════════"
	@echo ""
	@echo "  $(GREEN)ASSESSMENT$(NC)"
	@echo "    make quiz          Run formative quiz (full)"
	@echo "    make quiz-random   Run quiz with randomised questions"
	@echo "    make quiz-quick    Run quiz (5 random questions)"
	@echo ""
	@echo "  $(GREEN)TESTING$(NC)"
	@echo "    make test          Run all tests"
	@echo "    make smoke         Run smoke tests only"
	@echo "    make lint          Run code linter (ruff)"
	@echo "    make typecheck     Run type checker (mypy)"
	@echo "    make verify        Verify environment setup"
	@echo ""
	@echo "  $(GREEN)LABORATORY$(NC)"
	@echo "    make start         Start lab environment"
	@echo "    make stop          Stop lab environment"
	@echo "    make clean         Clean up artifacts and caches"
	@echo ""
	@echo "  $(GREEN)DOCKER$(NC)"
	@echo "    make docker-build  Build Docker images"
	@echo "    make docker-up     Start Docker containers"
	@echo "    make docker-down   Stop Docker containers"
	@echo ""
	@echo "  $(GREEN)UTILITIES$(NC)"
	@echo "    make checksums     Verify file integrity"
	@echo "    make all           Run verify + lint + smoke"
	@echo ""
	@echo "═══════════════════════════════════════════════════════════════════"
	@echo ""

# ─────────────────────────────────────────────────────────────────────────────
# ASSESSMENT TARGETS
# ─────────────────────────────────────────────────────────────────────────────

quiz:
	@echo "$(GREEN)Running formative quiz...$(NC)"
	$(PYTHON) formative/run_quiz.py

quiz-random:
	@echo "$(GREEN)Running formative quiz (randomised)...$(NC)"
	$(PYTHON) formative/run_quiz.py --random

quiz-quick:
	@echo "$(GREEN)Running quick quiz (5 random questions)...$(NC)"
	$(PYTHON) formative/run_quiz.py --random --limit 5

# ─────────────────────────────────────────────────────────────────────────────
# TESTING TARGETS
# ─────────────────────────────────────────────────────────────────────────────

test: smoke
	@echo "$(GREEN)Running exercise tests...$(NC)"
	$(PYTHON) tests/test_exercises.py --all

smoke:
	@echo "$(GREEN)Running smoke tests...$(NC)"
	$(PYTHON) tests/smoke_test.py

lint:
	@echo "$(GREEN)Running linter (ruff)...$(NC)"
	@command -v ruff >/dev/null 2>&1 || { echo "$(YELLOW)Installing ruff...$(NC)"; $(PIP) install ruff --break-system-packages; }
	ruff check src/ scripts/ tests/ homework/ formative/ --ignore E501

typecheck:
	@echo "$(GREEN)Running type checker (mypy)...$(NC)"
	@command -v mypy >/dev/null 2>&1 || { echo "$(YELLOW)Installing mypy...$(NC)"; $(PIP) install mypy --break-system-packages; }
	mypy src/ scripts/ --ignore-missing-imports --no-error-summary || true

verify:
	@echo "$(GREEN)Verifying environment...$(NC)"
	$(PYTHON) setup/verify_environment.py

checksums:
	@echo "$(GREEN)Verifying file checksums...$(NC)"
	@if [ -f checksums.sha256 ]; then \
		sha256sum -c checksums.sha256 --quiet && echo "$(GREEN)✓ All checksums valid$(NC)" || echo "$(RED)✗ Checksum mismatch!$(NC)"; \
	else \
		echo "$(YELLOW)No checksums.sha256 file found. Generating...$(NC)"; \
		find . -name "*.py" -type f | sort | xargs sha256sum > checksums.sha256; \
		echo "$(GREEN)✓ Checksums generated$(NC)"; \
	fi

# ─────────────────────────────────────────────────────────────────────────────
# LABORATORY TARGETS
# ─────────────────────────────────────────────────────────────────────────────

start:
	@echo "$(GREEN)Starting lab environment...$(NC)"
	$(PYTHON) scripts/start_lab.py

stop:
	@echo "$(GREEN)Stopping lab environment...$(NC)"
	$(PYTHON) scripts/stop_lab.py

clean:
	@echo "$(GREEN)Cleaning up...$(NC)"
	$(PYTHON) scripts/cleanup.py
	@echo "$(GREEN)Removing Python cache...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@echo "$(GREEN)Removing artifacts...$(NC)"
	rm -f artifacts/*.pcap artifacts/*.log 2>/dev/null || true
	@echo "$(GREEN)✓ Cleanup complete$(NC)"

# ─────────────────────────────────────────────────────────────────────────────
# DOCKER TARGETS
# ─────────────────────────────────────────────────────────────────────────────

docker-build:
	@echo "$(GREEN)Building Docker images...$(NC)"
	$(DOCKER_COMPOSE) build

docker-up:
	@echo "$(GREEN)Starting Docker containers...$(NC)"
	$(DOCKER_COMPOSE) up -d
	$(DOCKER_COMPOSE) ps

docker-down:
	@echo "$(GREEN)Stopping Docker containers...$(NC)"
	$(DOCKER_COMPOSE) down

# ─────────────────────────────────────────────────────────────────────────────
# COMPOSITE TARGETS
# ─────────────────────────────────────────────────────────────────────────────

all: verify lint smoke
	@echo ""
	@echo "$(GREEN)═══════════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  All checks passed!$(NC)"
	@echo "$(GREEN)═══════════════════════════════════════════════════════════════════$(NC)"
	@echo ""

# ─────────────────────────────────────────────────────────────────────────────
# DEFAULT TARGET
# ─────────────────────────────────────────────────────────────────────────────

.DEFAULT_GOAL := help
