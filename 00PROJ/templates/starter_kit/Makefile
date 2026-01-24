# Makefile for Computer Networks Project
# Usage: make [target]
#
# This Makefile provides common development tasks.
# Run 'make help' for available targets.

.PHONY: help install lint format test smoke run clean docker-up docker-down submit-check

# Configuration
PYTHON := python3
PIP := pip3
SRC := src
TESTS := tests
DOCKER_COMPOSE := docker-compose

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

# Default target
.DEFAULT_GOAL := help

help:
	@echo "$(GREEN)Available targets:$(NC)"
	@echo ""
	@echo "  $(YELLOW)Setup:$(NC)"
	@echo "    install      - Install Python dependencies"
	@echo "    install-dev  - Install development dependencies"
	@echo ""
	@echo "  $(YELLOW)Code Quality:$(NC)"
	@echo "    lint         - Run code linter (ruff)"
	@echo "    format       - Auto-format code"
	@echo "    type-check   - Run type checker (mypy)"
	@echo ""
	@echo "  $(YELLOW)Testing:$(NC)"
	@echo "    test         - Run all tests"
	@echo "    smoke        - Run smoke tests only (REQUIRED before submission)"
	@echo "    coverage     - Run tests with coverage report"
	@echo ""
	@echo "  $(YELLOW)Running:$(NC)"
	@echo "    run          - Run the application"
	@echo "    run-verbose  - Run with verbose logging"
	@echo "    dry-run      - Validate config without starting"
	@echo ""
	@echo "  $(YELLOW)Docker:$(NC)"
	@echo "    docker-up    - Start Docker containers"
	@echo "    docker-down  - Stop Docker containers"
	@echo "    docker-logs  - View container logs"
	@echo "    docker-clean - Remove containers and volumes"
	@echo ""
	@echo "  $(YELLOW)Submission:$(NC)"
	@echo "    submit-check - Run all checks before submission"
	@echo "    clean        - Remove generated files"
	@echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP
# ═══════════════════════════════════════════════════════════════════════════════

install:
	@echo "$(GREEN)Installing dependencies...$(NC)"
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)Done!$(NC)"

install-dev: install
	@echo "$(GREEN)Installing development dependencies...$(NC)"
	$(PIP) install ruff mypy pytest-cov
	@echo "$(GREEN)Done!$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# CODE QUALITY
# ═══════════════════════════════════════════════════════════════════════════════

lint:
	@echo "$(GREEN)Running linter...$(NC)"
	$(PYTHON) -m ruff check $(SRC) $(TESTS) --ignore E501
	@echo "$(GREEN)Lint passed!$(NC)"

format:
	@echo "$(GREEN)Formatting code...$(NC)"
	$(PYTHON) -m ruff format $(SRC) $(TESTS)
	@echo "$(GREEN)Done!$(NC)"

type-check:
	@echo "$(GREEN)Running type checker...$(NC)"
	$(PYTHON) -m mypy $(SRC) --ignore-missing-imports || true
	@echo "$(YELLOW)Type check complete (warnings shown above)$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

test: smoke
	@echo "$(GREEN)Running all tests...$(NC)"
	$(PYTHON) -m pytest $(TESTS) -v --tb=short
	@echo "$(GREEN)All tests passed!$(NC)"

smoke:
	@echo "$(GREEN)Running smoke tests...$(NC)"
	$(PYTHON) -m pytest $(TESTS)/test_smoke.py -v
	@echo "$(GREEN)Smoke tests passed!$(NC)"

coverage:
	@echo "$(GREEN)Running tests with coverage...$(NC)"
	$(PYTHON) -m pytest $(TESTS) -v --cov=$(SRC) --cov-report=term-missing --cov-report=html
	@echo "$(GREEN)Coverage report generated in htmlcov/$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# RUNNING
# ═══════════════════════════════════════════════════════════════════════════════

run:
	@echo "$(GREEN)Starting application...$(NC)"
	$(PYTHON) $(SRC)/main.py

run-verbose:
	@echo "$(GREEN)Starting application (verbose)...$(NC)"
	$(PYTHON) $(SRC)/main.py --verbose

dry-run:
	@echo "$(GREEN)Validating configuration...$(NC)"
	$(PYTHON) $(SRC)/main.py --dry-run
	@echo "$(GREEN)Configuration valid!$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# DOCKER
# ═══════════════════════════════════════════════════════════════════════════════

docker-up:
	@echo "$(GREEN)Starting Docker containers...$(NC)"
	$(DOCKER_COMPOSE) -f docker/docker-compose.yml up -d
	$(DOCKER_COMPOSE) -f docker/docker-compose.yml ps
	@echo "$(GREEN)Containers started!$(NC)"

docker-down:
	@echo "$(GREEN)Stopping Docker containers...$(NC)"
	$(DOCKER_COMPOSE) -f docker/docker-compose.yml down
	@echo "$(GREEN)Containers stopped!$(NC)"

docker-logs:
	$(DOCKER_COMPOSE) -f docker/docker-compose.yml logs -f

docker-clean:
	@echo "$(YELLOW)Removing Docker containers and volumes...$(NC)"
	$(DOCKER_COMPOSE) -f docker/docker-compose.yml down -v --remove-orphans
	@echo "$(GREEN)Done!$(NC)"

docker-build:
	@echo "$(GREEN)Building Docker images...$(NC)"
	$(DOCKER_COMPOSE) -f docker/docker-compose.yml build
	@echo "$(GREEN)Build complete!$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# SUBMISSION
# ═══════════════════════════════════════════════════════════════════════════════

submit-check: lint smoke
	@echo ""
	@echo "$(GREEN)═══════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  ✅ All checks passed! Ready for submission.$(NC)"
	@echo "$(GREEN)═══════════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(YELLOW)Remember to:$(NC)"
	@echo "  1. Update CHANGELOG.md"
	@echo "  2. Commit all changes"
	@echo "  3. Push to GitHub"
	@echo "  4. Create the submission archive"
	@echo ""

clean:
	@echo "$(GREEN)Cleaning generated files...$(NC)"
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type f -name "*.log" -delete 2>/dev/null || true
	@echo "$(GREEN)Done!$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════

check-python:
	@echo "$(GREEN)Python version:$(NC)"
	@$(PYTHON) --version
	@echo ""
	@echo "$(GREEN)Installed packages:$(NC)"
	@$(PIP) list | grep -E "(pytest|ruff|pyyaml)"

tree:
	@tree -I '__pycache__|.git|.pytest_cache|.ruff_cache|htmlcov' || find . -type f -name "*.py" | head -20
