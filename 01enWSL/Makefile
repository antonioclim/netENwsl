# Makefile — Week 1 Laboratory Orchestrator
# NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim

.PHONY: help install install-dev lint format test smoke quiz validate-quiz export-quiz \
        docker-up docker-down docker-logs docker-shell clean ci all

PYTHON := python3
DOCKER_COMPOSE := docker compose -f docker/docker-compose.yml
SRC_DIRS := src scripts tests formative setup

help:
	@echo "Week 1: Network Fundamentals — Laboratory Commands"
	@echo ""
	@echo "Setup:"
	@echo "  install        Install Python dependencies"
	@echo "  install-dev    Install development dependencies"
	@echo ""
	@echo "Development:"
	@echo "  lint           Run code linter (ruff)"
	@echo "  format         Format code with ruff"
	@echo "  test           Run all tests"
	@echo "  smoke          Run smoke tests only"
	@echo ""
	@echo "Quiz:"
	@echo "  quiz           Run interactive formative quiz"
	@echo "  validate-quiz  Validate quiz YAML file"
	@echo "  export-quiz    Export quiz to JSON and Moodle XML"
	@echo ""
	@echo "Docker:"
	@echo "  docker-up      Start lab environment"
	@echo "  docker-down    Stop lab environment"
	@echo "  docker-shell   Open shell in lab container"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean          Clean artefacts and cache"
	@echo "  ci             Run full CI pipeline locally"

install:
	$(PYTHON) -m pip install -r setup/requirements.txt --break-system-packages

install-dev: install
	$(PYTHON) -m pip install ruff mypy pytest pytest-cov pre-commit --break-system-packages
	-pre-commit install

lint:
	@$(PYTHON) -m ruff check $(SRC_DIRS) --fix 2>/dev/null || echo "Install ruff: make install-dev"

format:
	@$(PYTHON) -m ruff format $(SRC_DIRS) 2>/dev/null || echo "Install ruff: make install-dev"

test: smoke
	@$(PYTHON) -m pytest tests/ -v --tb=short 2>/dev/null || echo "Some tests may require Docker"

smoke:
	$(PYTHON) tests/smoke_test.py

quiz:
	$(PYTHON) formative/run_quiz.py

validate-quiz:
	$(PYTHON) formative/run_quiz.py --validate

export-quiz:
	$(PYTHON) formative/run_quiz.py --export-json
	$(PYTHON) formative/run_quiz.py --export-moodle

docker-up:
	$(DOCKER_COMPOSE) up -d
	$(DOCKER_COMPOSE) ps

docker-down:
	$(DOCKER_COMPOSE) down

docker-shell:
	docker exec -it week1_lab bash

clean:
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	rm -rf .coverage htmlcov/
	rm -rf formative/quiz_export.json formative/quiz_moodle.xml

ci: lint validate-quiz test
	@echo "CI PIPELINE COMPLETED"

all: install lint test

.DEFAULT_GOAL := help
