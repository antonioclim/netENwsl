# ═══════════════════════════════════════════════════════════════════════════════
# Makefile — Week 9: Session Layer and Presentation Layer
# NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: help setup start stop restart test smoke quiz quiz-stats quiz-export \
        lint lint-fix format validate demo capture clean clean-docker

PYTHON := python3
PIP := pip3
DOCKER_COMPOSE := docker compose -f docker/docker-compose.yml

help:
	@echo "Week 9: Session Layer and Presentation Layer"
	@echo ""
	@echo "Setup & Environment:"
	@echo "  make setup         Install dependencies and verify environment"
	@echo "  make install       Install Python dependencies only"
	@echo ""
	@echo "Docker Management:"
	@echo "  make start         Start laboratory Docker containers"
	@echo "  make stop          Stop laboratory containers"
	@echo "  make restart       Restart laboratory containers"
	@echo ""
	@echo "Testing:"
	@echo "  make test          Run all tests"
	@echo "  make smoke         Run smoke tests only"
	@echo "  make validate      Validate quiz and configuration"
	@echo ""
	@echo "Formative Assessment:"
	@echo "  make quiz          Run formative quiz interactively"
	@echo "  make quiz-stats    Show quiz statistics"
	@echo "  make quiz-export   Export quiz to LMS JSON format"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint          Run code linting (ruff)"
	@echo "  make lint-fix      Auto-fix linting issues"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean         Clean up artifacts and caches"
	@echo "  make clean-docker  Remove Docker containers and volumes"

setup: install
	@echo "Setup complete"

install:
	$(PIP) install -r setup/requirements.txt

start:
	$(DOCKER_COMPOSE) up -d
	@sleep 5
	$(DOCKER_COMPOSE) ps

stop:
	$(DOCKER_COMPOSE) down

restart: stop start

test: smoke
	$(PYTHON) tests/test_exercises.py

smoke:
	$(PYTHON) tests/smoke_test.py

validate:
	$(PYTHON) formative/run_quiz.py --validate

quiz:
	$(PYTHON) formative/run_quiz.py

quiz-stats:
	$(PYTHON) formative/run_quiz.py --stats

quiz-export:
	$(PYTHON) formative/run_quiz.py --export json

lint:
	$(PYTHON) -m ruff check src/ scripts/ tests/ formative/ --ignore E501,E402

lint-fix:
	$(PYTHON) -m ruff check --fix src/ scripts/ tests/ formative/

clean:
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf .pytest_cache .ruff_cache
	rm -rf artifacts/*.pcap artifacts/*.log

clean-docker:
	$(DOCKER_COMPOSE) down --volumes --remove-orphans
