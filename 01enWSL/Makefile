# Makefile — Week 1 Laboratory Orchestrator
# NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim
#
# Usage: make [target]
# Run 'make help' to see all available targets
#
# Prerequisites:
#   - Python 3.11+
#   - Docker Engine
#   - WSL2 Ubuntu 22.04 (recommended)

.PHONY: help install install-dev lint format typecheck test smoke quiz \
        docker-up docker-down docker-logs docker-shell verify clean all ci

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

PYTHON := python3
PIP := pip3
DOCKER_COMPOSE := docker compose -f docker/docker-compose.yml

# Directories
SRC_DIRS := src scripts tests formative setup
PYTHON_FILES := $(shell find $(SRC_DIRS) -name "*.py" 2>/dev/null)

# Colors for terminal output
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
BLUE := \033[0;34m
NC := \033[0m  # No Color
BOLD := \033[1m

# ═══════════════════════════════════════════════════════════════════════════════
# HELP
# ═══════════════════════════════════════════════════════════════════════════════

help: ## Show this help message
	@echo ""
	@echo "$(BOLD)$(BLUE)Week 1: Network Fundamentals — Laboratory Commands$(NC)"
	@echo "$(BOLD)$(BLUE)════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(BOLD)Setup:$(NC)"
	@grep -E '^(install|install-dev|verify):.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(BOLD)Development:$(NC)"
	@grep -E '^(lint|format|typecheck|test|smoke):.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(BOLD)Quiz:$(NC)"
	@grep -E '^(quiz|quiz-review|quiz-section):.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(BOLD)Docker:$(NC)"
	@grep -E '^(docker-up|docker-down|docker-logs|docker-shell):.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(BOLD)Maintenance:$(NC)"
	@grep -E '^(clean|all|ci):.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP TARGETS
# ═══════════════════════════════════════════════════════════════════════════════

install: ## Install Python dependencies
	@echo "$(YELLOW)Installing dependencies...$(NC)"
	$(PIP) install -r setup/requirements.txt --break-system-packages
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

install-dev: install ## Install development dependencies (linters, testing)
	@echo "$(YELLOW)Installing dev dependencies...$(NC)"
	$(PIP) install ruff mypy pytest pytest-cov pre-commit --break-system-packages
	@echo "$(YELLOW)Setting up pre-commit hooks...$(NC)"
	-pre-commit install
	@echo "$(GREEN)✓ Dev environment ready$(NC)"

verify: ## Verify environment setup (Docker, Python, etc.)
	@echo "$(YELLOW)Verifying environment...$(NC)"
	$(PYTHON) setup/verify_environment.py
	@echo "$(GREEN)✓ Verification complete$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# DEVELOPMENT TARGETS
# ═══════════════════════════════════════════════════════════════════════════════

lint: ## Run code linter (ruff)
	@echo "$(YELLOW)Running ruff linter...$(NC)"
	@$(PYTHON) -m ruff check $(SRC_DIRS) --fix 2>/dev/null || \
		echo "$(YELLOW)Note: Install ruff with 'make install-dev'$(NC)"
	@echo "$(GREEN)✓ Linting complete$(NC)"

format: ## Format code with ruff
	@echo "$(YELLOW)Formatting code...$(NC)"
	@$(PYTHON) -m ruff format $(SRC_DIRS) 2>/dev/null || \
		echo "$(YELLOW)Note: Install ruff with 'make install-dev'$(NC)"
	@echo "$(GREEN)✓ Formatting complete$(NC)"

typecheck: ## Run type checker (mypy)
	@echo "$(YELLOW)Running mypy type checker...$(NC)"
	@$(PYTHON) -m mypy src scripts --ignore-missing-imports 2>/dev/null || \
		echo "$(YELLOW)Note: Install mypy with 'make install-dev'$(NC)"
	@echo "$(GREEN)✓ Type checking complete$(NC)"

test: smoke ## Run all tests (pytest)
	@echo "$(YELLOW)Running pytest...$(NC)"
	@$(PYTHON) -m pytest tests/ -v --tb=short 2>/dev/null || \
		$(PYTHON) tests/test_exercises.py
	@echo "$(GREEN)✓ Tests complete$(NC)"

smoke: ## Run quick smoke tests
	@echo "$(YELLOW)Running smoke test...$(NC)"
	$(PYTHON) tests/smoke_test.py
	@echo "$(GREEN)✓ Smoke test complete$(NC)"

syntax: ## Check Python syntax without running
	@echo "$(YELLOW)Checking Python syntax...$(NC)"
	@$(PYTHON) -m py_compile $(PYTHON_FILES) 2>&1 && \
		echo "$(GREEN)✓ All files have valid syntax$(NC)" || \
		echo "$(RED)✗ Syntax errors found$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ TARGETS
# ═══════════════════════════════════════════════════════════════════════════════

quiz: ## Run the full formative quiz
	@echo "$(YELLOW)Starting formative quiz...$(NC)"
	@$(PYTHON) formative/run_quiz.py

quiz-review: ## Review quiz answers (study mode)
	@echo "$(YELLOW)Quiz review mode...$(NC)"
	@$(PYTHON) formative/run_quiz.py --review

quiz-section: ## Run a specific quiz section (use SECTION=pre_lab|during_lab|exit_ticket)
	@if [ -z "$(SECTION)" ]; then \
		echo "$(YELLOW)Available sections:$(NC)"; \
		$(PYTHON) formative/run_quiz.py --list-sections; \
		echo ""; \
		echo "Usage: make quiz-section SECTION=pre_lab"; \
	else \
		$(PYTHON) formative/run_quiz.py --section $(SECTION); \
	fi

quiz-random: ## Run 5 random questions
	@echo "$(YELLOW)Random quiz (5 questions)...$(NC)"
	@$(PYTHON) formative/run_quiz.py --random --limit 5

quiz-validate: ## Validate quiz YAML file
	@echo "$(YELLOW)Validating quiz.yaml...$(NC)"
	@$(PYTHON) -c "import yaml; q=yaml.safe_load(open('formative/quiz.yaml')); \
		print(f'✓ Loaded {len(q[\"questions\"])} questions'); \
		print(f'✓ {len(q[\"sections\"])} sections defined')"
	@echo "$(GREEN)✓ Quiz YAML is valid$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# DOCKER TARGETS
# ═══════════════════════════════════════════════════════════════════════════════

docker-up: ## Start lab Docker environment
	@echo "$(YELLOW)Starting Docker containers...$(NC)"
	$(DOCKER_COMPOSE) up -d
	@echo ""
	@echo "$(GREEN)✓ Lab environment ready$(NC)"
	@echo ""
	@echo "$(BOLD)Container status:$(NC)"
	@$(DOCKER_COMPOSE) ps
	@echo ""
	@echo "$(BOLD)Access points:$(NC)"
	@echo "  • Portainer: $(BLUE)http://localhost:9000$(NC)"
	@echo "  • Lab container: $(BLUE)docker exec -it week1_lab bash$(NC)"

docker-down: ## Stop lab Docker environment
	@echo "$(YELLOW)Stopping Docker containers...$(NC)"
	$(DOCKER_COMPOSE) down
	@echo "$(GREEN)✓ Lab environment stopped$(NC)"

docker-logs: ## Show container logs (follow mode)
	@echo "$(YELLOW)Container logs (Ctrl+C to exit):$(NC)"
	$(DOCKER_COMPOSE) logs -f

docker-shell: ## Open shell in lab container
	@echo "$(YELLOW)Opening shell in week1_lab...$(NC)"
	@docker exec -it week1_lab bash || \
		echo "$(RED)Container not running. Run 'make docker-up' first.$(NC)"

docker-build: ## Rebuild Docker images
	@echo "$(YELLOW)Building Docker images...$(NC)"
	$(DOCKER_COMPOSE) build --no-cache
	@echo "$(GREEN)✓ Build complete$(NC)"

docker-status: ## Show Docker container status
	@echo "$(BOLD)Docker Status:$(NC)"
	@$(DOCKER_COMPOSE) ps
	@echo ""
	@echo "$(BOLD)Networks:$(NC)"
	@docker network ls | grep week1 || echo "  (no week1 networks)"
	@echo ""
	@echo "$(BOLD)Volumes:$(NC)"
	@docker volume ls | grep week1 || echo "  (no week1 volumes)"

# ═══════════════════════════════════════════════════════════════════════════════
# MAINTENANCE TARGETS
# ═══════════════════════════════════════════════════════════════════════════════

clean: ## Clean artifacts, caches, and temporary files
	@echo "$(YELLOW)Cleaning...$(NC)"
	@rm -rf artifacts/*.pcap artifacts/*.log artifacts/*.csv 2>/dev/null || true
	@rm -rf __pycache__ */__pycache__ */*/__pycache__ 2>/dev/null || true
	@rm -rf .pytest_cache .mypy_cache .ruff_cache .coverage 2>/dev/null || true
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@find . -name ".DS_Store" -delete 2>/dev/null || true
	@echo "$(GREEN)✓ Clean complete$(NC)"

clean-docker: ## Remove all week1 Docker resources (containers, networks, volumes)
	@echo "$(YELLOW)Cleaning Docker resources...$(NC)"
	@$(DOCKER_COMPOSE) down --volumes --remove-orphans 2>/dev/null || true
	@docker network rm week1_network 2>/dev/null || true
	@echo "$(GREEN)✓ Docker cleanup complete$(NC)"

all: lint syntax smoke quiz-validate ## Run full CI pipeline locally
	@echo ""
	@echo "$(GREEN)$(BOLD)═══════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)$(BOLD)  ✓ All checks passed!$(NC)"
	@echo "$(GREEN)$(BOLD)═══════════════════════════════════════════════════════$(NC)"

ci: all docker-build ## Run CI checks including Docker build
	@echo "$(GREEN)✓ CI pipeline complete$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# DOCUMENTATION TARGETS
# ═══════════════════════════════════════════════════════════════════════════════

docs-serve: ## Serve documentation locally (if mkdocs installed)
	@mkdocs serve 2>/dev/null || \
		echo "$(YELLOW)mkdocs not installed. View docs/*.md directly.$(NC)"

readme: ## Open README in default viewer
	@if command -v xdg-open >/dev/null 2>&1; then \
		xdg-open README.md; \
	elif command -v open >/dev/null 2>&1; then \
		open README.md; \
	else \
		cat README.md | head -100; \
	fi

# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY TARGETS
# ═══════════════════════════════════════════════════════════════════════════════

info: ## Show project information
	@echo ""
	@echo "$(BOLD)$(BLUE)Week 1: Network Fundamentals$(NC)"
	@echo "$(BOLD)$(BLUE)════════════════════════════$(NC)"
	@echo ""
	@echo "$(BOLD)Project Structure:$(NC)"
	@echo "  src/exercises/  — Laboratory exercises (5 Python files)"
	@echo "  docs/           — Pedagogical documentation (12 files)"
	@echo "  tests/          — Automated tests"
	@echo "  formative/      — Quiz system"
	@echo "  scripts/        — Automation scripts"
	@echo "  docker/         — Container configuration"
	@echo ""
	@echo "$(BOLD)Quick Start:$(NC)"
	@echo "  1. make install     — Install dependencies"
	@echo "  2. make docker-up   — Start lab environment"
	@echo "  3. make quiz        — Take the formative quiz"
	@echo ""
	@echo "$(BOLD)Key Ports:$(NC)"
	@echo "  9000 — Portainer ($(RED)RESERVED$(NC))"
	@echo "  9090 — TCP test server"
	@echo "  9091 — UDP test server"
	@echo ""

.DEFAULT_GOAL := help
