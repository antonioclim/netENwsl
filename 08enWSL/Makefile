# ═══════════════════════════════════════════════════════════════════════════════
# Makefile — Week 8: Transport Layer & HTTP
# Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim
# ═══════════════════════════════════════════════════════════════════════════════
#
# This Makefile was created after extensive discussion with Andrei T. about
# what targets students actually need. The answer: fewer than you'd think.
#
# Principle from DPPD module: "Make the easy path the correct path."
#
# Usage:
#   make help        # Show all available targets
#   make start       # Start the lab environment
#   make quiz        # Run formative assessment
#   make test        # Run all tests
#   make clean       # Clean up environment
#
# ═══════════════════════════════════════════════════════════════════════════════

# Configuration
PYTHON := python3
DOCKER_COMPOSE := docker compose -f docker/docker-compose.yml
QUIZ_FILE := formative/quiz.yaml
SHELL := /bin/bash

# Colours for output (works on most terminals)
GREEN := \033[92m
YELLOW := \033[93m
CYAN := \033[96m
RED := \033[91m
RESET := \033[0m
BOLD := \033[1m

# Default target
.DEFAULT_GOAL := help

# ═══════════════════════════════════════════════════════════════════════════════
# HELP
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: help
help: ## Show this help message
	@echo ""
	@echo "$(BOLD)Week 8 Laboratory — Transport Layer & HTTP$(RESET)"
	@echo "Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim"
	@echo ""
	@echo "$(BOLD)Usage:$(RESET) make $(CYAN)<target>$(RESET)"
	@echo ""
	@echo "$(BOLD)Lab Environment:$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '(start|stop|status|logs|clean)' | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(CYAN)%-15s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(BOLD)Assessment:$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '(quiz|test|smoke)' | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(CYAN)%-15s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(BOLD)Development:$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '(lint|verify|demo)' | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(CYAN)%-15s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(BOLD)Examples:$(RESET)"
	@echo "  make start          # Start Docker environment"
	@echo "  make quiz           # Take the formative quiz"
	@echo "  make quiz-lo LO=3   # Quiz only LO3 questions"
	@echo "  make test           # Run all tests"
	@echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# LAB ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: start
start: ## Start the lab environment (nginx + backends)
	@echo "$(BOLD)Starting Week 8 laboratory environment...$(RESET)"
	@$(PYTHON) scripts/start_lab.py
	@echo ""
	@echo "$(GREEN)✓ Lab started successfully!$(RESET)"
	@echo ""
	@echo "Access points:"
	@echo "  • HTTP Proxy:  http://localhost:8080"
	@echo "  • HTTPS Proxy: https://localhost:8443"
	@echo "  • Portainer:   http://localhost:9000 (stud/studstudstud)"
	@echo ""

.PHONY: stop
stop: ## Stop the lab environment (keeps Portainer running)
	@echo "$(BOLD)Stopping Week 8 laboratory...$(RESET)"
	@$(PYTHON) scripts/stop_lab.py
	@echo "$(GREEN)✓ Lab stopped$(RESET)"

.PHONY: status
status: ## Show status of lab containers
	@echo "$(BOLD)Container Status:$(RESET)"
	@$(DOCKER_COMPOSE) ps 2>/dev/null || echo "$(YELLOW)Lab not running. Use 'make start' to begin.$(RESET)"

.PHONY: logs
logs: ## Show live logs from all containers
	@$(DOCKER_COMPOSE) logs -f

.PHONY: logs-nginx
logs-nginx: ## Show logs from nginx only
	@$(DOCKER_COMPOSE) logs -f nginx

.PHONY: logs-backends
logs-backends: ## Show logs from backend servers
	@$(DOCKER_COMPOSE) logs -f backend1 backend2 backend3

.PHONY: restart
restart: stop start ## Restart the lab environment

# ═══════════════════════════════════════════════════════════════════════════════
# ASSESSMENT
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: quiz
quiz: ## Run the formative assessment quiz
	@echo ""
	@$(PYTHON) formative/run_quiz.py

.PHONY: quiz-random
quiz-random: ## Run quiz with randomised questions
	@$(PYTHON) formative/run_quiz.py --random

.PHONY: quiz-lo
quiz-lo: ## Run quiz for specific LO (use: make quiz-lo LO=3)
	@if [ -z "$(LO)" ]; then \
		echo "$(RED)Error: Specify LO number, e.g., make quiz-lo LO=3$(RESET)"; \
		exit 1; \
	fi
	@$(PYTHON) formative/run_quiz.py --lo LO$(LO)

.PHONY: quiz-review
quiz-review: ## Review mode — see all answers
	@$(PYTHON) formative/run_quiz.py --review

.PHONY: quiz-basic
quiz-basic: ## Run only basic difficulty questions
	@$(PYTHON) formative/run_quiz.py --difficulty basic

.PHONY: quiz-advanced
quiz-advanced: ## Run only advanced difficulty questions
	@$(PYTHON) formative/run_quiz.py --difficulty advanced

.PHONY: quiz-list
quiz-list: ## List all quiz questions
	@$(PYTHON) formative/run_quiz.py --list-questions

.PHONY: test
test: ## Run all tests (exercise + environment)
	@echo "$(BOLD)Running all tests...$(RESET)"
	@$(PYTHON) -m pytest tests/ -v --tb=short 2>/dev/null || $(PYTHON) tests/test_exercises.py
	@echo ""
	@echo "$(GREEN)✓ Tests completed$(RESET)"

.PHONY: test-ex1
test-ex1: ## Run tests for Exercise 1 only
	@$(PYTHON) tests/test_exercises.py --exercise 1

.PHONY: test-ex2
test-ex2: ## Run tests for Exercise 2 only
	@$(PYTHON) tests/test_exercises.py --exercise 2

.PHONY: smoke
smoke: ## Run smoke tests to verify environment
	@echo "$(BOLD)Running smoke tests...$(RESET)"
	@$(PYTHON) tests/smoke_test.py

# ═══════════════════════════════════════════════════════════════════════════════
# DEVELOPMENT
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: verify
verify: ## Verify environment prerequisites
	@echo "$(BOLD)Verifying environment...$(RESET)"
	@$(PYTHON) setup/verify_environment.py

.PHONY: install
install: ## Install Python dependencies
	@echo "$(BOLD)Installing dependencies...$(RESET)"
	@pip install -r setup/requirements.txt --break-system-packages --quiet
	@echo "$(GREEN)✓ Dependencies installed$(RESET)"

.PHONY: lint
lint: ## Run code linter (if ruff is installed)
	@echo "$(BOLD)Running linter...$(RESET)"
	@$(PYTHON) -m ruff check src/ scripts/ tests/ formative/ --ignore E501 2>/dev/null || \
		echo "$(YELLOW)Ruff not installed. Install with: pip install ruff$(RESET)"

.PHONY: demo
demo: ## Run interactive demo menu
	@$(PYTHON) scripts/run_demo.py

.PHONY: demo-nginx
demo-nginx: ## Run nginx load balancer demo
	@$(PYTHON) scripts/run_demo.py --demo docker-nginx

.PHONY: demo-http
demo-http: ## Run HTTP server demo
	@$(PYTHON) scripts/run_demo.py --demo http-server

.PHONY: demo-handshake
demo-handshake: ## Run TCP handshake capture demo
	@$(PYTHON) scripts/run_demo.py --demo handshake

.PHONY: capture
capture: ## Start packet capture (saves to pcap/)
	@$(PYTHON) scripts/capture_traffic.py --interface lo --output pcap/capture_$$(date +%Y%m%d_%H%M%S).pcap

# ═══════════════════════════════════════════════════════════════════════════════
# CLEANUP
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: clean
clean: ## Clean up lab environment (containers + networks)
	@echo "$(BOLD)Cleaning up...$(RESET)"
	@$(PYTHON) scripts/cleanup.py --full 2>/dev/null || $(DOCKER_COMPOSE) down -v 2>/dev/null || true
	@echo "$(GREEN)✓ Cleanup complete$(RESET)"

.PHONY: clean-all
clean-all: ## Full cleanup including Docker images
	@echo "$(BOLD)Full cleanup (including images)...$(RESET)"
	@$(PYTHON) scripts/cleanup.py --full --prune 2>/dev/null || \
		($(DOCKER_COMPOSE) down -v --rmi local 2>/dev/null && docker system prune -f)
	@echo "$(GREEN)✓ Full cleanup complete$(RESET)"

.PHONY: clean-pcap
clean-pcap: ## Remove captured PCAP files
	@rm -f pcap/*.pcap
	@echo "$(GREEN)✓ PCAP files removed$(RESET)"

.PHONY: clean-artifacts
clean-artifacts: ## Remove generated artifacts
	@rm -f artifacts/*.pcap artifacts/*.log artifacts/*.json
	@echo "$(GREEN)✓ Artifacts removed$(RESET)"

.PHONY: clean-pycache
clean-pycache: ## Remove Python cache directories
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "$(GREEN)✓ Python cache removed$(RESET)"

# ═══════════════════════════════════════════════════════════════════════════════
# QUICK REFERENCE
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: cheatsheet
cheatsheet: ## Show quick command reference
	@echo ""
	@echo "$(BOLD)Quick Reference — Week 8$(RESET)"
	@echo ""
	@echo "$(CYAN)Start your session:$(RESET)"
	@echo "  make start        # Start Docker environment"
	@echo "  make smoke        # Verify everything works"
	@echo ""
	@echo "$(CYAN)Work on exercises:$(RESET)"
	@echo "  make demo-http    # See HTTP server in action"
	@echo "  make test-ex1     # Test your Exercise 1"
	@echo "  make test-ex2     # Test your Exercise 2"
	@echo ""
	@echo "$(CYAN)Self-assessment:$(RESET)"
	@echo "  make quiz         # Full formative quiz"
	@echo "  make quiz-lo LO=3 # Quiz specific LO"
	@echo "  make quiz-review  # See all answers"
	@echo ""
	@echo "$(CYAN)End your session:$(RESET)"
	@echo "  make stop         # Stop containers"
	@echo "  make clean        # Full cleanup"
	@echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# Acknowledgments
# ═══════════════════════════════════════════════════════════════════════════════
#
# Makefile design informed by:
# - Andrei T. (ASE) — "Students need 5 targets, not 50"
# - DPPD module, UPB — "Reduce cognitive load in tooling"
#
# The colour scheme uses ANSI codes that work on WSL/Ubuntu terminals.
# If colours don't display, your terminal may need configuration.
#
# ═══════════════════════════════════════════════════════════════════════════════
