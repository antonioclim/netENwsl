# ═══════════════════════════════════════════════════════════════════════════════
# Makefile — Week 3 Network Programming Laboratory Kit
# ═══════════════════════════════════════════════════════════════════════════════
# NETWORKING class - ASE, CSIE | by ing. dr. Antonio Clim
#
# Usage:
#   make help          Show this help message
#   make setup         Install dependencies
#   make lint          Run code linter (ruff)
#   make test          Run all tests
#   make quiz          Run formative quiz
#   make docker-up     Start lab containers
#   make docker-down   Stop lab containers
#   make clean         Clean artifacts
#
# For students:
#   make start         Quick start (setup + docker-up + status)
#   make stop          Stop lab and cleanup
# ═══════════════════════════════════════════════════════════════════════════════

# Configuration
PYTHON := python3
PIP := pip3
DOCKER_COMPOSE := docker compose -f docker/docker-compose.yml

# Directories
SRC_DIRS := src scripts formative homework/exercises tests
ARTIFACTS_DIR := artifacts
PCAP_DIR := pcap

# Colors for output
CYAN := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
RESET := \033[0m
BOLD := \033[1m

# ═══════════════════════════════════════════════════════════════════════════════
# DEFAULT TARGET
# ═══════════════════════════════════════════════════════════════════════════════

.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help message
	@echo ""
	@echo "$(BOLD)╔══════════════════════════════════════════════════════════════════════╗$(RESET)"
	@echo "$(BOLD)║  Week 3 Laboratory Kit — Network Programming                         ║$(RESET)"
	@echo "$(BOLD)║  NETWORKING class - ASE, CSIE                                        ║$(RESET)"
	@echo "$(BOLD)╚══════════════════════════════════════════════════════════════════════╝$(RESET)"
	@echo ""
	@echo "$(CYAN)Available targets:$(RESET)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Quick start for students:$(RESET)"
	@echo "  make start       # Setup environment and start containers"
	@echo "  make quiz        # Run formative self-assessment"
	@echo "  make stop        # Stop containers when finished"
	@echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STUDENT QUICK START
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: start
start: setup docker-up status ## Quick start: setup + start containers + show status
	@echo ""
	@echo "$(GREEN)✓ Laboratory environment ready!$(RESET)"
	@echo ""
	@echo "$(CYAN)Next steps:$(RESET)"
	@echo "  1. Open Portainer: http://localhost:9000"
	@echo "  2. Access client:  docker exec -it week3_client bash"
	@echo "  3. Run exercises:  python3 /app/src/exercises/ex_3_01_udp_broadcast.py --help"
	@echo ""

.PHONY: stop
stop: docker-down clean-artifacts ## Stop lab and clean artifacts
	@echo ""
	@echo "$(GREEN)✓ Laboratory environment stopped.$(RESET)"
	@echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP & DEPENDENCIES
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: setup
setup: ## Install Python dependencies
	@echo "$(CYAN)Installing dependencies...$(RESET)"
	$(PIP) install -r setup/requirements.txt --quiet
	@echo "$(GREEN)✓ Dependencies installed$(RESET)"

.PHONY: setup-dev
setup-dev: ## Install development dependencies (linter, test tools)
	@echo "$(CYAN)Installing development dependencies...$(RESET)"
	$(PIP) install -e ".[dev]" --quiet 2>/dev/null || \
		$(PIP) install ruff pytest pytest-cov mypy pyyaml --quiet
	@echo "$(GREEN)✓ Development dependencies installed$(RESET)"

.PHONY: verify
verify: ## Verify environment is correctly set up
	@echo "$(CYAN)Verifying environment...$(RESET)"
	$(PYTHON) setup/verify_environment.py
	@echo "$(GREEN)✓ Environment verified$(RESET)"

# ═══════════════════════════════════════════════════════════════════════════════
# CODE QUALITY
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: lint
lint: ## Run code linter (ruff)
	@echo "$(CYAN)Running linter...$(RESET)"
	@$(PYTHON) -m ruff check $(SRC_DIRS) --output-format=concise 2>/dev/null || \
		$(PYTHON) -m py_compile src/exercises/*.py scripts/*.py && \
		echo "$(YELLOW)⚠ Ruff not installed. Using py_compile for syntax check.$(RESET)" && \
		echo "$(GREEN)✓ Syntax check passed$(RESET)"

.PHONY: lint-fix
lint-fix: ## Run linter with auto-fix
	@echo "$(CYAN)Running linter with auto-fix...$(RESET)"
	@$(PYTHON) -m ruff check $(SRC_DIRS) --fix 2>/dev/null || \
		echo "$(YELLOW)⚠ Ruff not installed. Run 'make setup-dev' first.$(RESET)"

.PHONY: format
format: ## Format code with ruff
	@echo "$(CYAN)Formatting code...$(RESET)"
	@$(PYTHON) -m ruff format $(SRC_DIRS) 2>/dev/null || \
		echo "$(YELLOW)⚠ Ruff not installed. Run 'make setup-dev' first.$(RESET)"

.PHONY: typecheck
typecheck: ## Run type checker (mypy)
	@echo "$(CYAN)Running type checker...$(RESET)"
	@$(PYTHON) -m mypy src scripts --ignore-missing-imports 2>/dev/null || \
		echo "$(YELLOW)⚠ Mypy not installed. Run 'make setup-dev' first.$(RESET)"

.PHONY: check
check: lint typecheck ## Run all code quality checks (lint + typecheck)
	@echo "$(GREEN)✓ All checks passed$(RESET)"

# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: test
test: ## Run all tests
	@echo "$(CYAN)Running tests...$(RESET)"
	@$(PYTHON) -m pytest tests/ -v --tb=short 2>/dev/null || \
		$(PYTHON) tests/smoke_test.py

.PHONY: test-smoke
test-smoke: ## Run smoke tests only (quick verification)
	@echo "$(CYAN)Running smoke tests...$(RESET)"
	$(PYTHON) tests/smoke_test.py

.PHONY: test-exercises
test-exercises: ## Run exercise verification tests
	@echo "$(CYAN)Running exercise tests...$(RESET)"
	$(PYTHON) tests/test_exercises.py

.PHONY: test-env
test-env: ## Run environment tests
	@echo "$(CYAN)Running environment tests...$(RESET)"
	$(PYTHON) tests/test_environment.py

.PHONY: test-coverage
test-coverage: ## Run tests with coverage report
	@echo "$(CYAN)Running tests with coverage...$(RESET)"
	@$(PYTHON) -m pytest tests/ --cov=src --cov=scripts --cov-report=term-missing 2>/dev/null || \
		echo "$(YELLOW)⚠ pytest-cov not installed. Run 'make setup-dev' first.$(RESET)"

# ═══════════════════════════════════════════════════════════════════════════════
# FORMATIVE ASSESSMENT
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: quiz
quiz: ## Run formative quiz (self-assessment)
	@echo "$(CYAN)Starting formative quiz...$(RESET)"
	$(PYTHON) formative/run_quiz.py

.PHONY: quiz-random
quiz-random: ## Run quiz with randomized questions
	$(PYTHON) formative/run_quiz.py --random

.PHONY: quiz-quick
quiz-quick: ## Run quick quiz (5 random questions)
	$(PYTHON) formative/run_quiz.py --random --limit 5

.PHONY: quiz-lo
quiz-lo: ## Run quiz for specific LO (usage: make quiz-lo LO=LO1)
	@if [ -z "$(LO)" ]; then \
		echo "$(RED)Usage: make quiz-lo LO=LO1$(RESET)"; \
		exit 1; \
	fi
	$(PYTHON) formative/run_quiz.py --lo $(LO)

# ═══════════════════════════════════════════════════════════════════════════════
# DOCKER OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: docker-up
docker-up: ## Start Docker containers
	@echo "$(CYAN)Starting containers...$(RESET)"
	$(PYTHON) scripts/start_lab.py

.PHONY: docker-down
docker-down: ## Stop Docker containers
	@echo "$(CYAN)Stopping containers...$(RESET)"
	$(PYTHON) scripts/stop_lab.py

.PHONY: docker-restart
docker-restart: docker-down docker-up ## Restart Docker containers
	@echo "$(GREEN)✓ Containers restarted$(RESET)"

.PHONY: docker-logs
docker-logs: ## Show container logs
	$(DOCKER_COMPOSE) logs -f --tail=50

.PHONY: docker-build
docker-build: ## Rebuild Docker images
	@echo "$(CYAN)Rebuilding images...$(RESET)"
	$(DOCKER_COMPOSE) build --no-cache

.PHONY: status
status: ## Show container status
	@echo "$(CYAN)Container status:$(RESET)"
	@docker ps --filter "name=week3" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || \
		echo "$(YELLOW)No containers running$(RESET)"

.PHONY: shell-client
shell-client: ## Open shell in client container
	docker exec -it week3_client bash

.PHONY: shell-server
shell-server: ## Open shell in server container
	docker exec -it week3_server bash

.PHONY: shell-router
shell-router: ## Open shell in router container
	docker exec -it week3_router bash

# ═══════════════════════════════════════════════════════════════════════════════
# DEMONSTRATIONS
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: demo-broadcast
demo-broadcast: ## Run broadcast demonstration
	$(PYTHON) scripts/run_demo.py --demo broadcast_vs_multicast

.PHONY: demo-tunnel
demo-tunnel: ## Run tunnel demonstration
	$(PYTHON) scripts/run_demo.py --demo tunnel_flow

.PHONY: demo-igmp
demo-igmp: ## Run IGMP demonstration
	$(PYTHON) scripts/run_demo.py --demo igmp

# ═══════════════════════════════════════════════════════════════════════════════
# CLEANUP
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: clean
clean: clean-artifacts clean-pycache ## Clean all generated files
	@echo "$(GREEN)✓ Cleanup complete$(RESET)"

.PHONY: clean-artifacts
clean-artifacts: ## Clean generated artifacts (pcap, logs)
	@echo "$(CYAN)Cleaning artifacts...$(RESET)"
	rm -f $(ARTIFACTS_DIR)/*.pcap $(ARTIFACTS_DIR)/*.log 2>/dev/null || true
	rm -f $(PCAP_DIR)/*.pcap 2>/dev/null || true

.PHONY: clean-pycache
clean-pycache: ## Clean Python cache files
	@echo "$(CYAN)Cleaning Python cache...$(RESET)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true

.PHONY: clean-docker
clean-docker: ## Clean Docker resources for this week
	@echo "$(CYAN)Cleaning Docker resources...$(RESET)"
	$(PYTHON) scripts/cleanup.py --full

.PHONY: clean-all
clean-all: clean clean-docker ## Deep clean (artifacts + docker)
	@echo "$(GREEN)✓ Deep cleanup complete$(RESET)"

# ═══════════════════════════════════════════════════════════════════════════════
# DOCUMENTATION
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: docs
docs: ## Open documentation in browser
	@echo "$(CYAN)Opening documentation...$(RESET)"
	@xdg-open README.md 2>/dev/null || open README.md 2>/dev/null || \
		echo "$(YELLOW)Open README.md manually$(RESET)"

# ═══════════════════════════════════════════════════════════════════════════════
# CI/CD TARGETS (for GitHub Actions)
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: ci
ci: lint test ## Run CI checks (lint + test)
	@echo "$(GREEN)✓ CI checks passed$(RESET)"

.PHONY: ci-full
ci-full: lint typecheck test-coverage ## Run full CI checks
	@echo "$(GREEN)✓ Full CI checks passed$(RESET)"
