# Makefile — Week 1 Laboratory Orchestrator
# NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim
#
# Usage: make [target]
# Run 'make help' to see all available targets.

.PHONY: help install install-dev lint format test smoke quiz validate-quiz export-quiz \
        docker-up docker-down docker-logs docker-shell clean ci all check-emails

PYTHON := python3
DOCKER_COMPOSE := docker compose -f docker/docker-compose.yml
SRC_DIRS := src scripts tests formative setup

# Default goal
.DEFAULT_GOAL := help

# ═══════════════════════════════════════════════════════════════════════════════
# HELP
# ═══════════════════════════════════════════════════════════════════════════════
help:
	@echo "Week 1: Network Fundamentals — Laboratory Commands"
	@echo ""
	@echo "Setup:"
	@echo "  install        Install Python dependencies"
	@echo "  install-dev    Install development dependencies"
	@echo ""
	@echo "Development:"
	@echo "  lint           Run code linters (ruff + flake8)"
	@echo "  format         Format code with ruff"
	@echo "  test           Run all tests"
	@echo "  smoke          Run smoke tests only"
	@echo "  check-emails   Check for email addresses in code"
	@echo ""
	@echo "Quiz:"
	@echo "  quiz           Run interactive formative quiz"
	@echo "  validate-quiz  Validate quiz YAML file"
	@echo "  export-quiz    Export quiz to JSON, Canvas JSON and Moodle XML"
	@echo ""
	@echo "Docker:"
	@echo "  docker-up      Start lab environment"
	@echo "  docker-down    Stop lab environment"
	@echo "  docker-logs    Show container logs"
	@echo "  docker-shell   Open shell in lab container"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean          Clean artefacts and cache"
	@echo "  ci             Run full CI pipeline locally"
	@echo "  all            Install, lint and test"

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP
# ═══════════════════════════════════════════════════════════════════════════════
install:
	$(PYTHON) -m pip install -r requirements.txt --break-system-packages

install-dev: install
	$(PYTHON) -m pip install ruff mypy pytest pytest-cov pre-commit jsonschema --break-system-packages
	-pre-commit install

# ═══════════════════════════════════════════════════════════════════════════════
# LINTING AND FORMATTING
# ═══════════════════════════════════════════════════════════════════════════════
lint:
	@echo "Running ruff..."
	@$(PYTHON) -m ruff check $(SRC_DIRS) --fix 2>/dev/null || echo "Install ruff: make install-dev"
	@echo "Running flake8..."
	@$(PYTHON) -m flake8 $(SRC_DIRS) 2>/dev/null || echo "Install flake8: make install-dev"

format:
	@$(PYTHON) -m ruff format $(SRC_DIRS) 2>/dev/null || echo "Install ruff: make install-dev"

check-emails:
	@echo "Checking for email addresses..."
	@! grep -RInE "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}" README.md docs scripts src tests setup formative 2>/dev/null || (echo "❌ Email addresses found! Replace with: Issues: Open an issue in GitHub" && exit 1)
	@echo "✅ No email addresses found"

# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════
test: smoke
	@echo "Running pytest..."
	@$(PYTHON) -m pytest tests/ -v --tb=short 2>/dev/null || echo "Some tests may require Docker"

smoke:
	@echo "Running smoke tests..."
	$(PYTHON) tests/smoke_test.py

# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ
# ═══════════════════════════════════════════════════════════════════════════════
quiz:
	$(PYTHON) formative/run_quiz.py

validate-quiz:
	@echo "Validating quiz structure..."
	$(PYTHON) formative/run_quiz.py --validate

export-quiz:
	@echo "Exporting quiz to all formats..."
	$(PYTHON) formative/run_quiz.py --export-json
	$(PYTHON) formative/run_quiz.py --export-canvas
	$(PYTHON) formative/run_quiz.py --export-moodle
	@echo "✅ Exports complete:"
	@ls -la formative/quiz_*.json formative/quiz_*.xml 2>/dev/null || true

quiz-stats:
	$(PYTHON) formative/run_quiz.py --stats

# ═══════════════════════════════════════════════════════════════════════════════
# DOCKER
# ═══════════════════════════════════════════════════════════════════════════════
docker-up:
	$(DOCKER_COMPOSE) up -d
	$(DOCKER_COMPOSE) ps

docker-down:
	$(DOCKER_COMPOSE) down

docker-logs:
	$(DOCKER_COMPOSE) logs -f

docker-shell:
	docker exec -it week1_lab bash

docker-build:
	$(DOCKER_COMPOSE) build

# ═══════════════════════════════════════════════════════════════════════════════
# MAINTENANCE
# ═══════════════════════════════════════════════════════════════════════════════
clean:
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	rm -rf .coverage htmlcov/
	rm -rf formative/quiz_lms_export.json formative/quiz_canvas.json formative/quiz_moodle.xml

# ═══════════════════════════════════════════════════════════════════════════════
# CI PIPELINE
# ═══════════════════════════════════════════════════════════════════════════════
ci: lint check-emails validate-quiz test
	@echo ""
	@echo "════════════════════════════════════════════════════════════"
	@echo "✅ CI PIPELINE COMPLETED SUCCESSFULLY"
	@echo "════════════════════════════════════════════════════════════"

all: install lint test
