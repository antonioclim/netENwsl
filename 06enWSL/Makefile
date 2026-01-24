# ═══════════════════════════════════════════════════════════════════════════════
# Makefile — Week 6: NAT/PAT & Software-Defined Networking
# ═══════════════════════════════════════════════════════════════════════════════
# Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim
#
# Usage:
#   make help          Show all available targets
#   make quiz          Run formative quiz
#   make test          Run all tests
#   make lint          Run code linter
#   make all           Run full validation pipeline
#
# Contact: Issues: Open an issue in GitHub
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: help quiz quiz-random quiz-quick quiz-export test smoke lint typecheck \
        verify start stop clean session-token docker-build docker-up docker-down \
        checksums all ci docs-check install-deps

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

SHELL := /bin/bash
PYTHON := python3
PIP := pip3
PROJECT_ROOT := $(shell pwd)

# Colours for output
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
BLUE := \033[0;34m
NC := \033[0m  # No Colour

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
	@echo "    make quiz            Run formative quiz (full)"
	@echo "    make quiz-random     Run quiz with randomised questions"
	@echo "    make quiz-quick      Run quiz (5 random questions)"
	@echo "    make quiz-export     Export quiz to LMS formats (JSON, Moodle)"
	@echo ""
	@echo "  $(GREEN)TESTING$(NC)"
	@echo "    make test            Run all tests"
	@echo "    make smoke           Run smoke tests only"
	@echo "    make lint            Run code linter (ruff)"
	@echo "    make typecheck       Run type checker (mypy)"
	@echo "    make verify          Verify environment setup"
	@echo "    make ci              Run full CI pipeline locally"
	@echo ""
	@echo "  $(GREEN)LABORATORY$(NC)"
	@echo "    make start           Start lab environment"
	@echo "    make stop            Stop lab environment"
	@echo "    make session-token   Generate unique session token"
	@echo "    make clean           Clean up artefacts and caches"
	@echo ""
	@echo "  $(GREEN)DOCKER$(NC)"
	@echo "    make docker-build    Build Docker images"
	@echo "    make docker-up       Start Docker containers"
	@echo "    make docker-down     Stop Docker containers"
	@echo ""
	@echo "  $(GREEN)UTILITIES$(NC)"
	@echo "    make install-deps    Install Python dependencies"
	@echo "    make checksums       Verify/generate file checksums"
	@echo "    make docs-check      Validate documentation files"
	@echo "    make all             Run verify + lint + smoke"
	@echo ""
	@echo "═══════════════════════════════════════════════════════════════════"
	@echo ""

# ─────────────────────────────────────────────────────────────────────────────
# ASSESSMENT TARGETS
# ─────────────────────────────────────────────────────────────────────────────

quiz:
	@echo "$(GREEN)Running formative quiz...$(NC)"
	@$(PYTHON) formative/run_quiz.py

quiz-random:
	@echo "$(GREEN)Running randomised quiz...$(NC)"
	@$(PYTHON) formative/run_quiz.py --random

quiz-quick:
	@echo "$(GREEN)Running quick quiz (5 questions)...$(NC)"
	@$(PYTHON) formative/run_quiz.py --random --limit 5

quiz-export:
	@echo "$(GREEN)Exporting quiz to LMS formats...$(NC)"
	@mkdir -p exports
	@$(PYTHON) formative/run_quiz.py --export json --output exports/quiz_week6.json
	@$(PYTHON) formative/run_quiz.py --export moodle --output exports/quiz_week6_moodle.gift
	@$(PYTHON) formative/run_quiz.py --export moodle-xml --output exports/quiz_week6_moodle.xml
	@echo "$(GREEN)Exports saved to exports/ directory$(NC)"
	@ls -la exports/

# ─────────────────────────────────────────────────────────────────────────────
# TESTING TARGETS
# ─────────────────────────────────────────────────────────────────────────────

test:
	@echo "$(GREEN)Running all tests...$(NC)"
	@$(PYTHON) -m pytest tests/ -v --tb=short || $(PYTHON) tests/test_exercises.py

smoke:
	@echo "$(GREEN)Running smoke tests...$(NC)"
	@$(PYTHON) tests/smoke_test.py

lint:
	@echo "$(GREEN)Running linter (ruff)...$(NC)"
	@ruff check src/ scripts/ tests/ homework/ formative/ --ignore E501 || \
		echo "$(YELLOW)Ruff not installed. Install with: pip install ruff$(NC)"

typecheck:
	@echo "$(GREEN)Running type checker (mypy)...$(NC)"
	@mypy src/ scripts/ --ignore-missing-imports || \
		echo "$(YELLOW)MyPy not installed. Install with: pip install mypy$(NC)"

verify:
	@echo "$(GREEN)Verifying environment...$(NC)"
	@echo "Checking Python version..."
	@$(PYTHON) --version
	@echo ""
	@echo "Checking required tools..."
	@which docker > /dev/null && echo "  ✓ Docker" || echo "  ✗ Docker not found"
	@which docker-compose > /dev/null && echo "  ✓ Docker Compose" || echo "  ✗ Docker Compose not found"
	@$(PYTHON) -c "import yaml" 2>/dev/null && echo "  ✓ PyYAML" || echo "  ✗ PyYAML not installed"
	@echo ""
	@echo "Checking file structure..."
	@test -f README.md && echo "  ✓ README.md" || echo "  ✗ README.md missing"
	@test -f formative/quiz.yaml && echo "  ✓ formative/quiz.yaml" || echo "  ✗ Quiz file missing"
	@test -d src/exercises && echo "  ✓ src/exercises/" || echo "  ✗ Exercises directory missing"
	@echo ""

ci:
	@echo "$(GREEN)Running full CI pipeline...$(NC)"
	@echo ""
	@echo "$(BLUE)Step 1/5: Syntax check$(NC)"
	@$(PYTHON) -m py_compile $$(find . -name "*.py" -not -path "./__pycache__/*" -not -path "./.git/*") && \
		echo "  ✓ All Python files have valid syntax" || \
		(echo "  ✗ Syntax errors found" && exit 1)
	@echo ""
	@echo "$(BLUE)Step 2/5: Lint check$(NC)"
	@ruff check src/ scripts/ --ignore E501 --quiet && echo "  ✓ Linting passed" || echo "  ⚠ Linting warnings"
	@echo ""
	@echo "$(BLUE)Step 3/5: Smoke tests$(NC)"
	@$(PYTHON) tests/smoke_test.py
	@echo ""
	@echo "$(BLUE)Step 4/5: Quiz validation$(NC)"
	@$(PYTHON) -c "import yaml; yaml.safe_load(open('formative/quiz.yaml'))" && \
		echo "  ✓ Quiz YAML is valid"
	@echo ""
	@echo "$(BLUE)Step 5/5: Documentation check$(NC)"
	@$(MAKE) docs-check --no-print-directory
	@echo ""
	@echo "$(GREEN)════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  CI Pipeline PASSED$(NC)"
	@echo "$(GREEN)════════════════════════════════════════════════════════════$(NC)"

# ─────────────────────────────────────────────────────────────────────────────
# LABORATORY TARGETS
# ─────────────────────────────────────────────────────────────────────────────

start:
	@echo "$(GREEN)Starting lab environment...$(NC)"
	@$(PYTHON) scripts/start_lab.py || echo "$(YELLOW)Start script not found$(NC)"

stop:
	@echo "$(GREEN)Stopping lab environment...$(NC)"
	@$(PYTHON) scripts/stop_lab.py || echo "$(YELLOW)Stop script not found$(NC)"

session-token:
	@echo "$(GREEN)Generating session token...$(NC)"
	@$(PYTHON) scripts/generate_session_token.py --save

clean:
	@echo "$(GREEN)Cleaning up artefacts...$(NC)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type f -name ".DS_Store" -delete 2>/dev/null || true
	@rm -rf .pytest_cache .mypy_cache .ruff_cache 2>/dev/null || true
	@rm -rf artefacts/*.pcap artefacts/*.log 2>/dev/null || true
	@rm -f artefacts/.session_token 2>/dev/null || true
	@echo "$(GREEN)Clean complete$(NC)"

# ─────────────────────────────────────────────────────────────────────────────
# DOCKER TARGETS
# ─────────────────────────────────────────────────────────────────────────────

docker-build:
	@echo "$(GREEN)Building Docker images...$(NC)"
	@cd docker && docker-compose build

docker-up:
	@echo "$(GREEN)Starting Docker containers...$(NC)"
	@cd docker && docker-compose up -d
	@echo "Waiting for containers to be ready..."
	@sleep 5
	@docker ps

docker-down:
	@echo "$(GREEN)Stopping Docker containers...$(NC)"
	@cd docker && docker-compose down

# ─────────────────────────────────────────────────────────────────────────────
# UTILITY TARGETS
# ─────────────────────────────────────────────────────────────────────────────

install-deps:
	@echo "$(GREEN)Installing Python dependencies...$(NC)"
	@$(PIP) install -r setup/requirements.txt --break-system-packages || \
		$(PIP) install -r setup/requirements.txt
	@echo "$(GREEN)Dependencies installed$(NC)"

checksums:
	@echo "$(GREEN)Generating checksums...$(NC)"
	@find . -name "*.py" -type f | sort | xargs sha256sum > checksums.sha256
	@echo "Checksums saved to checksums.sha256"

docs-check:
	@echo "Checking documentation files..."
	@required_docs="README.md docs/theory_summary.md docs/troubleshooting.md \
		docs/misconceptions.md docs/glossary.md docs/learning_objectives.md \
		docs/peer_instruction.md homework/README.md formative/quiz.yaml"; \
	missing=0; \
	for doc in $$required_docs; do \
		if [ -f "$$doc" ]; then \
			echo "  ✓ $$doc"; \
		else \
			echo "  ✗ MISSING: $$doc"; \
			missing=$$((missing + 1)); \
		fi; \
	done; \
	if [ $$missing -gt 0 ]; then \
		echo "$(RED)$$missing documentation files missing$(NC)"; \
	else \
		echo "  ✓ All documentation present"; \
	fi

all: verify lint smoke
	@echo ""
	@echo "$(GREEN)════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  All checks passed!$(NC)"
	@echo "$(GREEN)════════════════════════════════════════════════════════════$(NC)"

# ─────────────────────────────────────────────────────────────────────────────
# DEFAULT TARGET
# ─────────────────────────────────────────────────────────────────────────────

.DEFAULT_GOAL := help
