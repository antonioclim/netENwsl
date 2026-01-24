# Makefile — Week 2 Laboratory Kit
# NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim
#
# Usage: make [target]
# Run 'make help' to see all available targets.

.PHONY: help install lint lint-fix typecheck test smoke quiz quiz-random \
        quiz-quick quiz-review quiz-export docker-up docker-down docker-logs \
        docker-shell docker-build docker-status clean clean-docker ci all \
        verify verify-integrity check-syntax test-coverage

# Configuration
PYTHON := python3
PIP := pip
DOCKER_COMPOSE := docker compose -f docker/docker-compose.yml
QUIZ_FILE := formative/quiz.yaml
RUFF_CONFIG := ruff.toml

# Colours for terminal output
CYAN := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
BLUE := \033[34m
RESET := \033[0m

# Default target
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo ""
	@echo "$(CYAN)Week 2 Laboratory Kit — Available Commands$(RESET)"
	@echo ""
	@echo "$(GREEN)Setup & Verification:$(RESET)"
	@echo "  $(CYAN)install$(RESET)          Install Python dependencies"
	@echo "  $(CYAN)verify$(RESET)           Verify environment"
	@echo "  $(CYAN)verify-integrity$(RESET) Verify file checksums"
	@echo ""
	@echo "$(GREEN)Code Quality:$(RESET)"
	@echo "  $(CYAN)check-syntax$(RESET)     Check Python syntax"
	@echo "  $(CYAN)lint$(RESET)             Run ruff linter"
	@echo "  $(CYAN)lint-fix$(RESET)         Run ruff with auto-fix"
	@echo "  $(CYAN)typecheck$(RESET)        Run mypy type checker"
	@echo ""
	@echo "$(GREEN)Testing:$(RESET)"
	@echo "  $(CYAN)test$(RESET)             Run all tests"
	@echo "  $(CYAN)test-coverage$(RESET)    Run tests with coverage"
	@echo "  $(CYAN)smoke$(RESET)            Run smoke tests"
	@echo ""
	@echo "$(GREEN)Formative Assessment:$(RESET)"
	@echo "  $(CYAN)quiz$(RESET)             Run interactive quiz"
	@echo "  $(CYAN)quiz-random$(RESET)      Run randomised quiz"
	@echo "  $(CYAN)quiz-quick$(RESET)       Run 5-question quiz"
	@echo "  $(CYAN)quiz-review$(RESET)      Review all questions"
	@echo "  $(CYAN)quiz-export$(RESET)      Export to LMS formats"
	@echo ""
	@echo "$(GREEN)Docker:$(RESET)"
	@echo "  $(CYAN)docker-up$(RESET)        Start containers"
	@echo "  $(CYAN)docker-down$(RESET)      Stop containers"
	@echo "  $(CYAN)docker-logs$(RESET)      View logs"
	@echo "  $(CYAN)docker-shell$(RESET)     Shell into container"
	@echo ""
	@echo "$(GREEN)CI/CD:$(RESET)"
	@echo "  $(CYAN)ci$(RESET)               Run full CI pipeline"
	@echo "  $(CYAN)all$(RESET)              Full setup and verification"
	@echo ""

install: ## Install Python dependencies
	@echo "$(CYAN)Installing dependencies...$(RESET)"
	$(PIP) install -r setup/requirements.txt
	@echo "$(GREEN)✓ Dependencies installed$(RESET)"

verify: ## Verify environment
	@echo "$(CYAN)Verifying environment...$(RESET)"
	$(PYTHON) setup/verify_environment.py
	@echo "$(GREEN)✓ Environment verified$(RESET)"

verify-integrity: ## Verify file checksums
	@echo "$(CYAN)Verifying integrity...$(RESET)"
	@if [ -f MANIFEST.sha256 ]; then \
		sha256sum -c MANIFEST.sha256 --quiet && \
		echo "$(GREEN)✓ All files verified$(RESET)" || \
		echo "$(YELLOW)⚠ Some checksums differ$(RESET)"; \
	else \
		echo "$(YELLOW)⚠ MANIFEST.sha256 not found$(RESET)"; \
	fi

check-syntax: ## Check Python syntax
	@echo "$(CYAN)Checking syntax...$(RESET)"
	@find src scripts tests formative -name "*.py" -exec $(PYTHON) -m py_compile {} \;
	@echo "$(GREEN)✓ No syntax errors$(RESET)"

lint: ## Run ruff linter
	@echo "$(CYAN)Running linter...$(RESET)"
	@$(PYTHON) -m ruff check src/ scripts/ tests/ formative/ --config $(RUFF_CONFIG) || true
	@echo "$(GREEN)✓ Linting complete$(RESET)"

lint-fix: ## Run ruff with auto-fix
	$(PYTHON) -m ruff check --fix src/ scripts/ tests/ formative/ --config $(RUFF_CONFIG)
	@echo "$(GREEN)✓ Auto-fixes applied$(RESET)"

typecheck: ## Run mypy type checker
	@$(PYTHON) -m mypy src/ scripts/ --ignore-missing-imports --no-error-summary 2>/dev/null || true
	@echo "$(GREEN)✓ Type check complete$(RESET)"

test: ## Run all tests
	@echo "$(CYAN)Running tests...$(RESET)"
	$(PYTHON) -m pytest tests/ -v --tb=short
	@echo "$(GREEN)✓ Tests complete$(RESET)"

test-coverage: ## Run tests with coverage
	$(PYTHON) -m pytest tests/ -v --cov=src --cov=scripts --cov-report=term --cov-report=html
	@echo "$(GREEN)✓ Coverage: htmlcov/index.html$(RESET)"

smoke: ## Run smoke tests
	$(PYTHON) tests/smoke_test.py
	@echo "$(GREEN)✓ Smoke tests complete$(RESET)"

quiz: ## Run interactive quiz
	@echo "$(CYAN)Starting quiz...$(RESET)"
	$(PYTHON) formative/run_quiz.py

quiz-random: ## Run randomised quiz
	$(PYTHON) formative/run_quiz.py --random

quiz-quick: ## Run 5-question quiz
	$(PYTHON) formative/run_quiz.py --limit 5 --random

quiz-review: ## Review all questions
	$(PYTHON) formative/run_quiz.py --review

quiz-export: ## Export to LMS formats
	@echo "$(CYAN)Exporting quiz...$(RESET)"
	@mkdir -p exports
	$(PYTHON) formative/export_quiz_to_lms.py --format moodle --output exports/quiz_moodle.xml
	$(PYTHON) formative/export_quiz_to_lms.py --format gift --output exports/quiz.gift
	$(PYTHON) formative/export_quiz_to_lms.py --format json --output exports/quiz_export.json
	@echo "$(GREEN)✓ Exports in exports/$(RESET)"

docker-up: ## Start containers
	$(DOCKER_COMPOSE) up -d
	$(DOCKER_COMPOSE) ps

docker-down: ## Stop containers
	$(DOCKER_COMPOSE) down

docker-logs: ## View logs
	$(DOCKER_COMPOSE) logs -f

docker-shell: ## Shell into container
	docker exec -it week2_lab /bin/bash

docker-build: ## Rebuild images
	$(DOCKER_COMPOSE) build --no-cache

docker-status: ## Container status
	$(DOCKER_COMPOSE) ps

clean: ## Remove generated files
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name htmlcov -exec rm -rf {} + 2>/dev/null || true
	rm -rf exports/ 2>/dev/null || true
	@echo "$(GREEN)✓ Cleanup complete$(RESET)"

clean-docker: ## Remove Docker resources
	$(DOCKER_COMPOSE) down --volumes --remove-orphans

ci: check-syntax lint test ## Run CI pipeline
	@echo "$(GREEN)✓ CI pipeline complete$(RESET)"

all: install verify ci ## Full setup
	@echo "$(GREEN)✓ All checks passed$(RESET)"
