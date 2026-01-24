# =============================================================================
# Makefile — Week 11 WSL Kit Command Orchestration
# =============================================================================
# NETWORKING class - ASE, Informatics | by Revolvix
#
# Usage:
#   make help          Show all available commands
#   make setup         Install dependencies and verify environment
#   make lab           Start the laboratory environment
#   make quiz          Run formative quiz
#   make test          Run all tests
#   make clean         Clean up environment
# =============================================================================

.PHONY: help setup verify install lab stop quiz test lint clean docker-up docker-down

# Default Python interpreter
PYTHON := python3
PIP := pip3

# Docker Compose file
COMPOSE := docker compose -f docker/docker-compose.yml

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m

# =============================================================================
# HELP
# =============================================================================

help:
	@echo ""
	@echo "$(GREEN)Week 11 Laboratory Kit - Available Commands$(NC)"
	@echo "=============================================="
	@echo ""
	@echo "$(YELLOW)Setup:$(NC)"
	@echo "  make setup        Install dependencies and verify environment"
	@echo "  make verify       Verify environment only"
	@echo "  make install      Install Python dependencies only"
	@echo ""
	@echo "$(YELLOW)Laboratory:$(NC)"
	@echo "  make lab          Start full laboratory environment"
	@echo "  make stop         Stop laboratory environment"
	@echo "  make status       Show container status"
	@echo "  make logs         Show container logs"
	@echo ""
	@echo "$(YELLOW)Docker:$(NC)"
	@echo "  make docker-up    Start Docker containers"
	@echo "  make docker-down  Stop Docker containers"
	@echo "  make docker-build Rebuild Docker images"
	@echo ""
	@echo "$(YELLOW)Learning:$(NC)"
	@echo "  make quiz         Run formative assessment quiz"
	@echo "  make quiz-random  Run quiz with random order"
	@echo "  make quiz-review  Review all quiz answers"
	@echo ""
	@echo "$(YELLOW)Testing:$(NC)"
	@echo "  make test         Run all tests"
	@echo "  make smoke        Run smoke tests only"
	@echo "  make test-ex N=1  Test specific exercise (N=1-7)"
	@echo ""
	@echo "$(YELLOW)Code Quality:$(NC)"
	@echo "  make lint         Run code linter (ruff)"
	@echo "  make typecheck    Run type checker (mypy)"
	@echo "  make format       Format code (ruff)"
	@echo ""
	@echo "$(YELLOW)Cleanup:$(NC)"
	@echo "  make clean        Clean artifacts and caches"
	@echo "  make clean-all    Full cleanup including Docker"
	@echo ""

# =============================================================================
# SETUP
# =============================================================================

setup: install verify
	@echo "$(GREEN)✓ Setup complete!$(NC)"

verify:
	@echo "$(YELLOW)Verifying environment...$(NC)"
	$(PYTHON) setup/verify_environment.py

install:
	@echo "$(YELLOW)Installing dependencies...$(NC)"
	$(PIP) install -r setup/requirements.txt --break-system-packages
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

# =============================================================================
# LABORATORY
# =============================================================================

lab:
	@echo "$(YELLOW)Starting laboratory environment...$(NC)"
	$(PYTHON) scripts/start_lab.py

stop:
	@echo "$(YELLOW)Stopping laboratory environment...$(NC)"
	$(PYTHON) scripts/stop_lab.py

status:
	@echo "$(YELLOW)Container status:$(NC)"
	$(PYTHON) scripts/start_lab.py --status

logs:
	$(COMPOSE) logs -f

# =============================================================================
# DOCKER
# =============================================================================

docker-up:
	@echo "$(YELLOW)Starting Docker containers...$(NC)"
	$(COMPOSE) up -d
	@echo "$(GREEN)✓ Containers started$(NC)"
	$(COMPOSE) ps

docker-down:
	@echo "$(YELLOW)Stopping Docker containers...$(NC)"
	$(COMPOSE) down
	@echo "$(GREEN)✓ Containers stopped$(NC)"

docker-build:
	@echo "$(YELLOW)Rebuilding Docker images...$(NC)"
	$(COMPOSE) build --no-cache
	@echo "$(GREEN)✓ Images rebuilt$(NC)"

docker-logs:
	$(COMPOSE) logs -f

# =============================================================================
# LEARNING / ASSESSMENT
# =============================================================================

quiz:
	@echo "$(YELLOW)Starting formative quiz...$(NC)"
	$(PYTHON) formative/run_quiz.py

quiz-random:
	$(PYTHON) formative/run_quiz.py --random

quiz-review:
	$(PYTHON) formative/run_quiz.py --review

quiz-topic:
	@echo "Usage: make quiz-topic T=DNS"
	@echo "Topics: DNS, FTP, SSH, Load Balancing, Nginx"
ifdef T
	$(PYTHON) formative/run_quiz.py --topic "$(T)"
endif

# =============================================================================
# TESTING
# =============================================================================

test:
	@echo "$(YELLOW)Running all tests...$(NC)"
	$(PYTHON) -m pytest tests/ -v

smoke:
	@echo "$(YELLOW)Running smoke tests...$(NC)"
	$(PYTHON) tests/smoke_test.py

test-ex:
	@echo "$(YELLOW)Testing exercise $(N)...$(NC)"
ifdef N
	$(PYTHON) tests/test_exercises.py --exercise $(N)
else
	@echo "$(RED)Error: Specify exercise number with N=1$(NC)"
	@echo "Usage: make test-ex N=1"
endif

test-env:
	@echo "$(YELLOW)Testing environment...$(NC)"
	$(PYTHON) -m pytest tests/test_environment.py -v

# =============================================================================
# CODE QUALITY
# =============================================================================

lint:
	@echo "$(YELLOW)Running linter...$(NC)"
	$(PYTHON) -m ruff check src/ scripts/ tests/ formative/ || true

format:
	@echo "$(YELLOW)Formatting code...$(NC)"
	$(PYTHON) -m ruff format src/ scripts/ tests/ formative/

typecheck:
	@echo "$(YELLOW)Running type checker...$(NC)"
	$(PYTHON) -m mypy src/ scripts/ --ignore-missing-imports || true

syntax:
	@echo "$(YELLOW)Checking Python syntax...$(NC)"
	$(PYTHON) -m py_compile src/exercises/*.py scripts/*.py tests/*.py
	@echo "$(GREEN)✓ Syntax OK$(NC)"

# =============================================================================
# CLEANUP
# =============================================================================

clean:
	@echo "$(YELLOW)Cleaning artifacts...$(NC)"
	rm -rf artifacts/*.pcap artifacts/*.log
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	rm -rf *.egg-info dist/ build/
	@echo "$(GREEN)✓ Cleaned$(NC)"

clean-all: clean docker-down
	@echo "$(YELLOW)Full cleanup...$(NC)"
	$(PYTHON) scripts/cleanup.py --full
	@echo "$(GREEN)✓ Full cleanup complete$(NC)"

# =============================================================================
# UTILITIES
# =============================================================================

capture:
	@echo "$(YELLOW)Starting traffic capture...$(NC)"
	$(PYTHON) scripts/capture_traffic.py

demo:
	@echo "$(YELLOW)Running demo...$(NC)"
	$(PYTHON) scripts/run_demo.py --demo 1

# =============================================================================
# Revolvix&Hypotheticalandrei
# =============================================================================
