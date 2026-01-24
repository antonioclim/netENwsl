# ═══════════════════════════════════════════════════════════════════════════════
# Makefile — Week 5 Laboratory Orchestrator
# NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim
# ═══════════════════════════════════════════════════════════════════════════════
#
# Usage:
#   make help         Show all available targets
#   make setup        Install dependencies and verify environment
#   make test         Run all tests
#   make quiz         Run formative assessment quiz
#   make lab          Start the Docker lab environment
#   make clean        Clean up generated files
#
# ═══════════════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
SHELL := /bin/bash
.DEFAULT_GOAL := help

# Python configuration
PYTHON := python3
PIP := pip3
PYTEST := $(PYTHON) -m pytest

# Docker configuration
DOCKER_COMPOSE := docker compose -f docker/docker-compose.yml
CONTAINER_PREFIX := week5

# Directories
SRC_DIR := src
TEST_DIR := tests
DOCS_DIR := docs
FORMATIVE_DIR := formative
ARTIFACTS_DIR := artifacts
PCAP_DIR := pcap

# Colours for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m  # No Color
BOLD := \033[1m

# ─────────────────────────────────────────────────────────────────────────────
# HELP
# ─────────────────────────────────────────────────────────────────────────────
.PHONY: help
help: ## Show this help message
	@echo ""
	@echo "$(BOLD)Week 5: IP Addressing, Subnetting, VLSM$(NC)"
	@echo "$(BLUE)════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(BOLD)Available targets:$(NC)"
	@echo ""
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(BOLD)Examples:$(NC)"
	@echo "  make setup        # First-time setup"
	@echo "  make test         # Run all tests"
	@echo "  make quiz         # Take formative quiz"
	@echo "  make lab          # Start Docker environment"
	@echo ""

# ─────────────────────────────────────────────────────────────────────────────
# SETUP & VERIFICATION
# ─────────────────────────────────────────────────────────────────────────────
.PHONY: setup
setup: ## Install dependencies and verify environment
	@echo "$(BLUE)═══ Setting up Week 5 Laboratory ═══$(NC)"
	@echo ""
	@echo "$(YELLOW)Installing Python dependencies...$(NC)"
	$(PIP) install -q pyyaml pytest pytest-cov ruff
	@if [ -f setup/requirements.txt ]; then \
		$(PIP) install -q -r setup/requirements.txt || true; \
	fi
	@echo "$(GREEN)✓ Dependencies installed$(NC)"
	@echo ""
	@echo "$(YELLOW)Verifying environment...$(NC)"
	$(PYTHON) setup/verify_environment.py || true
	@echo ""
	@echo "$(GREEN)✓ Setup complete!$(NC)"
	@echo "  Run 'make test' to verify installation"
	@echo "  Run 'make lab' to start Docker environment"

.PHONY: verify
verify: ## Verify environment is correctly configured
	@echo "$(BLUE)═══ Verifying Environment ═══$(NC)"
	$(PYTHON) setup/verify_environment.py

.PHONY: check-python
check-python: ## Check Python syntax for all files
	@echo "$(BLUE)═══ Checking Python Syntax ═══$(NC)"
	@find $(SRC_DIR) $(TEST_DIR) scripts -name "*.py" -type f | xargs $(PYTHON) -m py_compile
	@echo "$(GREEN)✓ All Python files have valid syntax$(NC)"

# ─────────────────────────────────────────────────────────────────────────────
# TESTING
# ─────────────────────────────────────────────────────────────────────────────
.PHONY: test
test: smoke unit ## Run all tests (smoke + unit)

.PHONY: smoke
smoke: ## Run smoke tests only
	@echo "$(BLUE)═══ Running Smoke Tests ═══$(NC)"
	$(PYTHON) $(TEST_DIR)/smoke_test.py

.PHONY: unit
unit: ## Run unit tests with pytest
	@echo "$(BLUE)═══ Running Unit Tests ═══$(NC)"
	$(PYTEST) $(TEST_DIR)/ -v --tb=short

.PHONY: coverage
coverage: ## Run tests with coverage report
	@echo "$(BLUE)═══ Running Tests with Coverage ═══$(NC)"
	$(PYTEST) $(TEST_DIR)/ -v --cov=$(SRC_DIR) --cov-report=term-missing --cov-report=html:$(ARTIFACTS_DIR)/coverage
	@echo ""
	@echo "$(GREEN)Coverage report: $(ARTIFACTS_DIR)/coverage/index.html$(NC)"

.PHONY: test-exercise
test-exercise: ## Run tests for specific exercise (e.g., make test-exercise EX=1)
	@echo "$(BLUE)═══ Running Exercise $(EX) Tests ═══$(NC)"
	$(PYTEST) $(TEST_DIR)/test_exercises.py -v -k "Exercise$(EX)" --tb=short

# ─────────────────────────────────────────────────────────────────────────────
# FORMATIVE ASSESSMENT
# ─────────────────────────────────────────────────────────────────────────────
.PHONY: quiz
quiz: ## Run the formative assessment quiz
	@echo "$(BLUE)═══ Starting Formative Quiz ═══$(NC)"
	$(PYTHON) $(FORMATIVE_DIR)/run_quiz.py

.PHONY: quiz-random
quiz-random: ## Run quiz with randomized questions
	$(PYTHON) $(FORMATIVE_DIR)/run_quiz.py --random

.PHONY: quiz-quick
quiz-quick: ## Run a quick 5-question quiz
	$(PYTHON) $(FORMATIVE_DIR)/run_quiz.py --limit 5 --random

.PHONY: quiz-apply
quiz-apply: ## Run quiz focusing on Apply-level questions
	$(PYTHON) $(FORMATIVE_DIR)/run_quiz.py --category apply

.PHONY: quiz-validate
quiz-validate: ## Validate quiz YAML file
	@echo "$(BLUE)═══ Validating Quiz YAML ═══$(NC)"
	@$(PYTHON) -c "import yaml; quiz = yaml.safe_load(open('$(FORMATIVE_DIR)/quiz.yaml')); print(f'✓ Valid YAML with {len(quiz[\"questions\"])} questions')"

# ─────────────────────────────────────────────────────────────────────────────
# EXERCISES
# ─────────────────────────────────────────────────────────────────────────────
.PHONY: ex1
ex1: ## Run Exercise 5.01 (CIDR/FLSM) demo
	@echo "$(BLUE)═══ Exercise 5.01: CIDR Analysis & FLSM ═══$(NC)"
	@echo ""
	@echo "$(YELLOW)Example 1: Analyse 192.168.10.14/26$(NC)"
	$(PYTHON) $(SRC_DIR)/exercises/ex_5_01_cidr_flsm.py analyse 192.168.10.14/26
	@echo ""
	@echo "$(YELLOW)Example 2: Split 10.0.0.0/24 into 4 subnets$(NC)"
	$(PYTHON) $(SRC_DIR)/exercises/ex_5_01_cidr_flsm.py flsm 10.0.0.0/24 4

.PHONY: ex2
ex2: ## Run Exercise 5.02 (VLSM/IPv6) demo
	@echo "$(BLUE)═══ Exercise 5.02: VLSM & IPv6 ═══$(NC)"
	@echo ""
	@echo "$(YELLOW)Example 1: VLSM allocation$(NC)"
	$(PYTHON) $(SRC_DIR)/exercises/ex_5_02_vlsm_ipv6.py vlsm 172.16.0.0/24 60 20 10 2
	@echo ""
	@echo "$(YELLOW)Example 2: IPv6 analysis$(NC)"
	$(PYTHON) $(SRC_DIR)/exercises/ex_5_02_vlsm_ipv6.py ipv6 2001:db8::1

.PHONY: ex3
ex3: ## Run Exercise 5.03 (Quiz Generator) interactive mode
	@echo "$(BLUE)═══ Exercise 5.03: Interactive Quiz ═══$(NC)"
	$(PYTHON) $(SRC_DIR)/exercises/ex_5_03_quiz_generator.py --interactive

# ─────────────────────────────────────────────────────────────────────────────
# DOCKER LAB ENVIRONMENT
# ─────────────────────────────────────────────────────────────────────────────
.PHONY: lab
lab: ## Start the Docker lab environment
	@echo "$(BLUE)═══ Starting Lab Environment ═══$(NC)"
	$(PYTHON) scripts/start_lab.py

.PHONY: lab-up
lab-up: ## Start Docker containers directly
	@echo "$(BLUE)═══ Starting Docker Containers ═══$(NC)"
	$(DOCKER_COMPOSE) up -d
	@echo ""
	@echo "$(GREEN)Containers started. Use 'make lab-status' to check.$(NC)"

.PHONY: lab-down
lab-down: ## Stop Docker containers
	@echo "$(BLUE)═══ Stopping Docker Containers ═══$(NC)"
	$(DOCKER_COMPOSE) down

.PHONY: lab-status
lab-status: ## Show status of lab containers
	@echo "$(BLUE)═══ Lab Container Status ═══$(NC)"
	@docker ps --filter "name=$(CONTAINER_PREFIX)" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

.PHONY: lab-logs
lab-logs: ## Show logs from lab containers
	$(DOCKER_COMPOSE) logs --tail=50

.PHONY: lab-shell
lab-shell: ## Open shell in Python container
	@echo "$(BLUE)═══ Opening Shell in Python Container ═══$(NC)"
	docker exec -it $(CONTAINER_PREFIX)_python bash

.PHONY: lab-rebuild
lab-rebuild: ## Rebuild Docker images from scratch
	@echo "$(BLUE)═══ Rebuilding Docker Images ═══$(NC)"
	$(DOCKER_COMPOSE) build --no-cache
	$(DOCKER_COMPOSE) up -d

# ─────────────────────────────────────────────────────────────────────────────
# CODE QUALITY
# ─────────────────────────────────────────────────────────────────────────────
.PHONY: lint
lint: ## Run code linter (ruff)
	@echo "$(BLUE)═══ Running Linter ═══$(NC)"
	ruff check $(SRC_DIR)/ scripts/ $(TEST_DIR)/ --ignore E501,E402 || true

.PHONY: lint-fix
lint-fix: ## Auto-fix linting issues
	@echo "$(BLUE)═══ Auto-fixing Lint Issues ═══$(NC)"
	ruff check $(SRC_DIR)/ scripts/ $(TEST_DIR)/ --fix --ignore E501,E402 || true

.PHONY: format
format: ## Format code with ruff
	@echo "$(BLUE)═══ Formatting Code ═══$(NC)"
	ruff format $(SRC_DIR)/ scripts/ $(TEST_DIR)/

# ─────────────────────────────────────────────────────────────────────────────
# CLEANUP
# ─────────────────────────────────────────────────────────────────────────────
.PHONY: clean
clean: ## Clean generated files (keep Docker)
	@echo "$(BLUE)═══ Cleaning Generated Files ═══$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	rm -rf $(ARTIFACTS_DIR)/*.pcap $(ARTIFACTS_DIR)/*.log 2>/dev/null || true
	rm -rf .pytest_cache .ruff_cache 2>/dev/null || true
	@echo "$(GREEN)✓ Cleanup complete$(NC)"

.PHONY: clean-docker
clean-docker: lab-down ## Stop and remove Docker containers
	@echo "$(BLUE)═══ Cleaning Docker Resources ═══$(NC)"
	$(DOCKER_COMPOSE) down --volumes --remove-orphans
	@echo "$(GREEN)✓ Docker cleanup complete$(NC)"

.PHONY: clean-all
clean-all: clean clean-docker ## Full cleanup (files + Docker)
	@echo "$(GREEN)✓ Full cleanup complete$(NC)"

# ─────────────────────────────────────────────────────────────────────────────
# DOCUMENTATION
# ─────────────────────────────────────────────────────────────────────────────
.PHONY: docs-check
docs-check: ## Verify all required documentation exists
	@echo "$(BLUE)═══ Checking Documentation ═══$(NC)"
	@for doc in README.md docs/theory_summary.md docs/misconceptions.md docs/troubleshooting.md docs/glossary.md docs/learning_objectives.md; do \
		if [ -f "$$doc" ]; then \
			echo "$(GREEN)✓$(NC) $$doc"; \
		else \
			echo "$(RED)✗$(NC) $$doc (missing)"; \
		fi \
	done

# ─────────────────────────────────────────────────────────────────────────────
# PACKET CAPTURE
# ─────────────────────────────────────────────────────────────────────────────
.PHONY: capture
capture: ## Start packet capture (requires lab running)
	@echo "$(BLUE)═══ Starting Packet Capture ═══$(NC)"
	$(PYTHON) scripts/capture_traffic.py

.PHONY: capture-list
capture-list: ## List captured PCAP files
	@echo "$(BLUE)═══ PCAP Files ═══$(NC)"
	@ls -la $(PCAP_DIR)/*.pcap 2>/dev/null || echo "No PCAP files found"

# ─────────────────────────────────────────────────────────────────────────────
# CI SIMULATION
# ─────────────────────────────────────────────────────────────────────────────
.PHONY: ci
ci: check-python lint smoke unit quiz-validate docs-check ## Run full CI pipeline locally
	@echo ""
	@echo "$(GREEN)═══════════════════════════════════════$(NC)"
	@echo "$(GREEN)  ✓ CI Pipeline Passed Successfully!  $(NC)"
	@echo "$(GREEN)═══════════════════════════════════════$(NC)"

# ─────────────────────────────────────────────────────────────────────────────
# QUICK REFERENCE
# ─────────────────────────────────────────────────────────────────────────────
.PHONY: info
info: ## Show week 5 configuration info
	@echo "$(BOLD)Week 5 Configuration$(NC)"
	@echo "$(BLUE)────────────────────$(NC)"
	@echo "Topic:        IP Addressing, Subnetting, VLSM"
	@echo "Network:      10.5.0.0/24"
	@echo "Gateway:      10.5.0.1"
	@echo "Python:       10.5.0.10"
	@echo "UDP Server:   10.5.0.20:9999"
	@echo "UDP Client:   10.5.0.30"
	@echo "Portainer:    http://localhost:9000"
	@echo ""
	@echo "$(BOLD)Quick Commands$(NC)"
	@echo "$(BLUE)────────────────────$(NC)"
	@echo "make setup    - First-time setup"
	@echo "make test     - Run tests"
	@echo "make quiz     - Take quiz"
	@echo "make lab      - Start Docker lab"
	@echo "make ci       - Run full CI locally"
