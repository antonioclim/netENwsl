# ═══════════════════════════════════════════════════════════════════════════════
# Makefile — Week 8: Transport Layer & HTTP
# Computer Networks — ASE, CSIE
# ═══════════════════════════════════════════════════════════════════════════════
#
# Usage:
#   make help        # Show all available targets
#   make init ID=... # FIRST: Initialise with your student ID
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
CONTEXT_FILE := artifacts/student_context.json
ANTI_AI_CHALLENGE := artifacts/anti_ai/challenge_week08.json
ANTI_AI_EVIDENCE := artifacts/anti_ai/evidence.json

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
	@echo "Computer Networks — ASE, CSIE"
	@echo ""
	@echo "$(BOLD)Usage:$(RESET) make $(CYAN)<target>$(RESET)"
	@echo ""
	@echo "$(BOLD)⭐ Getting Started (in order):$(RESET)"
	@echo "  $(CYAN)init$(RESET)            Initialise with YOUR student ID (REQUIRED FIRST)"
	@echo "                    Example: make init ID=12345ABC"
	@echo "  $(CYAN)start$(RESET)           Start Docker lab environment"
	@echo "  $(CYAN)quiz-basic$(RESET)      Check your prerequisite knowledge"
	@echo ""
	@echo "$(BOLD)Lab Environment:$(RESET)"
	@echo "  $(CYAN)start$(RESET)           Start the lab environment (nginx + backends)"
	@echo "  $(CYAN)stop$(RESET)            Stop the lab environment (keeps Portainer)"
	@echo "  $(CYAN)restart$(RESET)         Restart the lab environment"
	@echo "  $(CYAN)status$(RESET)          Show status of lab containers"
	@echo "  $(CYAN)logs$(RESET)            Show live logs from all containers"
	@echo ""
	@echo "$(BOLD)Assessment:$(RESET)"
	@echo "  $(CYAN)quiz$(RESET)            Run the full formative quiz"
	@echo "  $(CYAN)quiz-lo$(RESET)         Quiz specific LO: make quiz-lo LO=3"
	@echo "  $(CYAN)quiz-basic$(RESET)      Run only basic difficulty questions"
	@echo "  $(CYAN)quiz-advanced$(RESET)   Run only advanced difficulty questions"
	@echo "  $(CYAN)quiz-export$(RESET)     Export quiz for LMS (Moodle/Canvas)"
	@echo "  $(CYAN)parsons$(RESET)         Run Parsons code arrangement problems"
	@echo "  $(CYAN)progress$(RESET)        Show your learning progress over time"
	@echo "  $(CYAN)test$(RESET)            Run all tests (exercise + environment)"
	@echo "  $(CYAN)smoke$(RESET)           Run quick smoke tests"
	@echo ""
	@echo "$(BOLD)Submission:$(RESET)"
	@echo "  $(CYAN)verify-pcap$(RESET)     Verify PCAP files before submission"
	@echo "  $(CYAN)check-context$(RESET)   Show your unique context values"
	@echo "  $(CYAN)anti-ai$(RESET)         Run anti-AI workflow (challenge + evidence + validate)"
	@echo "  $(CYAN)anti-ai-challenge$(RESET) Generate a time-limited challenge file"
	@echo "  $(CYAN)anti-ai-evidence$(RESET) Collect evidence.json for your captures"
	@echo "  $(CYAN)anti-ai-validate$(RESET) Validate evidence.json and PCAPs"
	@echo ""
	@echo "$(BOLD)Development:$(RESET)"
	@echo "  $(CYAN)lint$(RESET)            Run code linter (ruff)"
	@echo "  $(CYAN)verify$(RESET)          Verify environment prerequisites"
	@echo "  $(CYAN)demo$(RESET)            Run interactive demo menu"
	@echo "  $(CYAN)clean$(RESET)           Clean up lab environment"
	@echo ""
	@echo "$(BOLD)Quick Start Workflow:$(RESET)"
	@echo "  1. make init ID=your_student_id"
	@echo "  2. make start"
	@echo "  3. make quiz-basic"
	@echo "  4. [complete exercises]"
	@echo "  5. make verify-pcap"
	@echo "  6. make test"
	@echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# STUDENT INITIALISATION (REQUIRED FIRST STEP)
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: init
init: ## ⭐ FIRST: Initialise session with your student ID
	@if [ -z "$(ID)" ]; then \
		echo "$(RED)╔═══════════════════════════════════════════════════════════════╗$(RESET)"; \
		echo "$(RED)║  ERROR: Student ID required                                   ║$(RESET)"; \
		echo "$(RED)╚═══════════════════════════════════════════════════════════════╝$(RESET)"; \
		echo ""; \
		echo "$(BOLD)Usage:$(RESET) make init ID=your_student_id"; \
		echo ""; \
		echo "This generates YOUR unique exercise parameters."; \
		echo "You MUST run this before starting exercises."; \
		exit 1; \
	fi
	@$(PYTHON) scripts/generate_student_context.py "$(ID)"
	@$(PYTHON) -m anti_ai.challenge_generator --context "$(CONTEXT_FILE)" --out "$(ANTI_AI_CHALLENGE)" --ttl-hours 12
	@echo ""
	@echo "$(GREEN)✓ Session initialised for: $(ID)$(RESET)"
	@echo "  Your context: $(CONTEXT_FILE)"
	@echo "  Your challenge: $(ANTI_AI_CHALLENGE)"
	@echo ""
	@echo "$(BOLD)Next steps:$(RESET)"
	@echo "  1. make start      # Start lab environment"
	@echo "  2. make quiz-basic # Check your prerequisites"
	@echo ""

.PHONY: verify-pcap
verify-pcap: ## Verify PCAP submissions before homework submission
	@if [ ! -f "$(CONTEXT_FILE)" ]; then \
		echo "$(RED)Error: Run 'make init ID=...' first$(RESET)"; \
		exit 1; \
	fi
	@$(PYTHON) scripts/verify_pcap_submission.py

.PHONY: check-context
check-context: ## Show your unique context values
	@if [ ! -f "$(CONTEXT_FILE)" ]; then \
		echo "$(RED)No context found. Run: make init ID=your_student_id$(RESET)"; \
		exit 1; \
	fi
	@echo "$(BOLD)Your Unique Context:$(RESET)"
	@cat $(CONTEXT_FILE) | $(PYTHON) -m json.tool

.PHONY: anti-ai-challenge
anti-ai-challenge: ## Generate a time-limited anti-AI challenge file
	@if [ ! -f "$(CONTEXT_FILE)" ]; then \
		echo "$(RED)Error: Run 'make init ID=...' first$(RESET)"; \
		exit 1; \
	fi
	@$(PYTHON) -m anti_ai.challenge_generator --context "$(CONTEXT_FILE)" --out "$(ANTI_AI_CHALLENGE)" --ttl-hours 12

.PHONY: anti-ai-evidence
anti-ai-evidence: ## Collect evidence.json for PCAP captures
	@if [ ! -f "$(CONTEXT_FILE)" ]; then \
		echo "$(RED)Error: Run 'make init ID=...' first$(RESET)"; \
		exit 1; \
	fi
	@$(PYTHON) scripts/collect_anti_ai_evidence.py --context "$(CONTEXT_FILE)" --out "$(ANTI_AI_EVIDENCE)"

.PHONY: anti-ai-validate
anti-ai-validate: ## Validate evidence.json and PCAPs
	@if [ ! -f "$(ANTI_AI_CHALLENGE)" ]; then \
		echo "$(RED)Error: Challenge missing. Run: make anti-ai-challenge$(RESET)"; \
		exit 1; \
	fi
	@if [ ! -f "$(ANTI_AI_EVIDENCE)" ]; then \
		echo "$(RED)Error: Evidence missing. Run: make anti-ai-evidence$(RESET)"; \
		exit 1; \
	fi
	@$(PYTHON) scripts/validate_anti_ai_submission.py --challenge "$(ANTI_AI_CHALLENGE)" --evidence "$(ANTI_AI_EVIDENCE)"

.PHONY: anti-ai
anti-ai: verify-pcap anti-ai-evidence anti-ai-validate ## Run the full anti-AI workflow

# ═══════════════════════════════════════════════════════════════════════════════
# LAB ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: start
start: ## Start the lab environment (nginx + backends)
	@echo "$(BOLD)Starting Week 8 laboratory environment...$(RESET)"
	@$(PYTHON) scripts/start_lab.py 2>/dev/null || $(DOCKER_COMPOSE) up -d
	@echo ""
	@echo "$(GREEN)✓ Lab started successfully!$(RESET)"
	@echo ""
	@echo "Access points:"
	@echo "  • HTTP Proxy:  http://localhost:8080"
	@echo "  • HTTPS Proxy: https://localhost:8443"
	@echo "  • Portainer:   http://localhost:9000"
	@echo ""

.PHONY: stop
stop: ## Stop the lab environment (keeps Portainer running)
	@echo "$(BOLD)Stopping Week 8 laboratory...$(RESET)"
	@$(PYTHON) scripts/stop_lab.py 2>/dev/null || $(DOCKER_COMPOSE) down
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

.PHONY: quiz-export
quiz-export: ## Export quiz for LMS (JSON format)
	@mkdir -p artifacts
	@$(PYTHON) formative/run_quiz.py --export-lms artifacts/quiz_lms_export.json
	@$(PYTHON) formative/run_quiz.py --export-moodle artifacts/quiz_moodle_export.xml
	@echo "$(GREEN)✓ Exported to artifacts/quiz_lms_export.json$(RESET)"
	@echo "$(GREEN)✓ Exported to artifacts/quiz_moodle_export.xml$(RESET)"

.PHONY: parsons
parsons: ## Run Parsons code arrangement problems
	@$(PYTHON) formative/parsons/run_parsons.py

.PHONY: parsons-lo
parsons-lo: ## Run Parsons for specific LO (use: make parsons-lo LO=3)
	@if [ -z "$(LO)" ]; then \
		echo "$(RED)Error: Specify LO number, e.g., make parsons-lo LO=3$(RESET)"; \
		exit 1; \
	fi
	@$(PYTHON) formative/parsons/run_parsons.py --lo LO$(LO)

.PHONY: parsons-list
parsons-list: ## List available Parsons problems
	@$(PYTHON) formative/parsons/run_parsons.py --list

.PHONY: progress
progress: ## Show your learning progress over time
	@$(PYTHON) formative/progress_tracker.py

.PHONY: progress-reset
progress-reset: ## Reset progress tracking (start fresh)
	@$(PYTHON) formative/progress_tracker.py --reset

.PHONY: test
test: ## Run all tests (exercise + environment)
	@echo "$(BOLD)Running all tests...$(RESET)"
	@$(PYTHON) -m pytest tests/ -v --tb=short 2>/dev/null || $(PYTHON) tests/test_exercises.py
	@echo ""
	@echo "$(GREEN)✓ Tests completed$(RESET)"

.PHONY: test-ex1
test-ex1: ## Run tests for Exercise 1 only
	@$(PYTHON) tests/test_exercises.py --exercise 1 2>/dev/null || \
		$(PYTHON) -m pytest tests/test_exercises.py -k "Exercise1" -v

.PHONY: test-ex2
test-ex2: ## Run tests for Exercise 2 only
	@$(PYTHON) tests/test_exercises.py --exercise 2 2>/dev/null || \
		$(PYTHON) -m pytest tests/test_exercises.py -k "Exercise2" -v

.PHONY: test-context
test-context: ## Run tests that verify unique context usage
	@$(PYTHON) -m pytest tests/test_unique_context.py -v 2>/dev/null || \
		echo "$(YELLOW)Context tests require student context. Run 'make init ID=...' first.$(RESET)"

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
lint: ## Run code linter (ruff)
	@echo "$(BOLD)Running linter...$(RESET)"
	@$(PYTHON) -m ruff check src/ scripts/ tests/ formative/ anti_ai/ homework/ --ignore E501 2>/dev/null || \
		echo "$(YELLOW)Ruff not installed. Install with: pip install ruff$(RESET)"

.PHONY: lint-fix
lint-fix: ## Run linter and auto-fix issues
	@$(PYTHON) -m ruff check src/ scripts/ tests/ formative/ anti_ai/ homework/ --fix 2>/dev/null || \
		echo "$(YELLOW)Ruff not installed. Install with: pip install ruff$(RESET)"

.PHONY: format
format: ## Format code with ruff
	@$(PYTHON) -m ruff format src/ scripts/ tests/ formative/ anti_ai/ homework/ 2>/dev/null || \
		echo "$(YELLOW)Ruff not installed. Install with: pip install ruff$(RESET)"

.PHONY: typecheck
typecheck: ## Run type checker (mypy)
	@$(PYTHON) -m mypy src/exercises/ scripts/ --ignore-missing-imports 2>/dev/null || \
		echo "$(YELLOW)Mypy not installed. Install with: pip install mypy$(RESET)"

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
# CI/CD TARGETS (for automated pipelines)
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: ci-lint
ci-lint: ## CI: Run linting checks
	@$(PYTHON) -m ruff check src/ scripts/ tests/ formative/ anti_ai/ homework/

.PHONY: ci-test
ci-test: ## CI: Run tests for CI pipeline
	@$(PYTHON) -m pytest tests/ -v --tb=short --ignore=tests/test_unique_context.py

.PHONY: ci-syntax
ci-syntax: ## CI: Check Python syntax
	@find . -name "*.py" -not -path "*/__pycache__/*" -exec $(PYTHON) -m py_compile {} \;
	@echo "$(GREEN)✓ Syntax check passed$(RESET)"

.PHONY: ci-docker
ci-docker: ## CI: Verify Docker configuration
	@$(DOCKER_COMPOSE) config --quiet
	@echo "$(GREEN)✓ Docker Compose configuration valid$(RESET)"

# ═══════════════════════════════════════════════════════════════════════════════
# QUICK REFERENCE
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: cheatsheet
cheatsheet: ## Show quick command reference
	@echo ""
	@echo "$(BOLD)Quick Reference — Week 8$(RESET)"
	@echo ""
	@echo "$(CYAN)Start your session:$(RESET)"
	@echo "  make init ID=your_id  # Generate unique context"
	@echo "  make start            # Start Docker environment"
	@echo "  make smoke            # Verify everything works"
	@echo ""
	@echo "$(CYAN)Work on exercises:$(RESET)"
	@echo "  make demo-http        # See HTTP server in action"
	@echo "  make test-ex1         # Test your Exercise 1"
	@echo "  make test-ex2         # Test your Exercise 2"
	@echo ""
	@echo "$(CYAN)Self-assessment:$(RESET)"
	@echo "  make quiz             # Full formative quiz"
	@echo "  make quiz-lo LO=3     # Quiz specific LO"
	@echo "  make parsons          # Code arrangement practice"
	@echo "  make progress         # View your progress"
	@echo ""
	@echo "$(CYAN)Before submission:$(RESET)"
	@echo "  make verify-pcap      # Check PCAP files"
	@echo "  make test             # Run all tests"
	@echo ""
	@echo "$(CYAN)End your session:$(RESET)"
	@echo "  make stop             # Stop containers"
	@echo "  make clean            # Full cleanup"
	@echo ""
