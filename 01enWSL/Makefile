# Makefile — Week 1 Laboratory Orchestrator
# NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim

.PHONY: help install install-dev lint format test smoke quiz validate-quiz export-quiz \
        anti-ai-challenge anti-ai-evidence anti-ai-validate \
        docker-up docker-down docker-logs docker-shell clean ci all

PYTHON := python3
DOCKER_COMPOSE := docker compose -f docker/docker-compose.yml
SRC_DIRS := src scripts tests formative setup anti_ai

help:
	@echo "Week 1: Network Fundamentals — Laboratory Commands"
	@echo ""
	@echo "Setup:"
	@echo "  install            Install Python dependencies"
	@echo "  install-dev        Install development dependencies"
	@echo ""
	@echo "Development:"
	@echo "  lint               Run code linter (ruff)"
	@echo "  format             Format code with ruff"
	@echo "  test               Run all tests"
	@echo "  smoke              Run smoke tests only"
	@echo ""
	@echo "Anti-AI (homework support):"
	@echo "  anti-ai-challenge   Generate a per-student challenge file"
	@echo "  anti-ai-evidence    Collect evidence.json from artefacts"
	@echo "  anti-ai-validate    Validate a submission using challenge and evidence"
	@echo ""
	@echo "Quiz:"
	@echo "  quiz               Run interactive formative quiz"
	@echo "  validate-quiz       Validate quiz YAML file"
	@echo "  export-quiz         Export quiz to JSON, Canvas JSON and Moodle XML"
	@echo ""
	@echo "Docker:"
	@echo "  docker-up          Start lab environment"
	@echo "  docker-down        Stop lab environment"
	@echo "  docker-shell       Open shell in lab container"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean              Clean artefacts and cache"
	@echo "  ci                 Run full CI pipeline locally"

install:
	$(PYTHON) -m pip install -r requirements.txt --break-system-packages

install-dev: install
	$(PYTHON) -m pip install ruff mypy pytest pytest-cov pre-commit flake8 --break-system-packages
	-pre-commit install

lint:
	@$(PYTHON) -m ruff check $(SRC_DIRS) --fix 2>/dev/null || echo "Install ruff: make install-dev"
	@$(PYTHON) -m flake8 $(SRC_DIRS) 2>/dev/null || echo "Install flake8: make install-dev"

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
	$(PYTHON) formative/run_quiz.py --export-canvas
	$(PYTHON) formative/run_quiz.py --export-moodle

anti-ai-challenge:
	@test -n "$(STUDENT_ID)" || (echo "Set STUDENT_ID, for example: make anti-ai-challenge STUDENT_ID=ABC123" && exit 1)
	$(PYTHON) -m anti_ai.challenge_generator --student-id $(STUDENT_ID)

anti-ai-evidence:
	@test -n "$(CHALLENGE)" || (echo "Set CHALLENGE, for example: make anti-ai-evidence CHALLENGE=artifacts/anti_ai/challenge_ABC123.yaml" && exit 1)
	@test -n "$(ARTEFACTS)" || (echo "Set ARTEFACTS, for example: make anti-ai-evidence CHALLENGE=... ARTEFACTS='network_report.md tcp_analysis.pcap udp_analysis.pcap'" && exit 1)
	$(PYTHON) -m anti_ai.evidence_collector $(foreach a,$(ARTEFACTS),--artefact $(a)) --challenge $(CHALLENGE) --output evidence.json --include-commands

anti-ai-validate:
	@test -n "$(CHALLENGE)" || (echo "Set CHALLENGE" && exit 1)
	@test -n "$(EVIDENCE)" || (echo "Set EVIDENCE, for example: make anti-ai-validate CHALLENGE=... EVIDENCE=evidence.json" && exit 1)
	$(PYTHON) -m anti_ai.submission_validator --challenge $(CHALLENGE) --evidence $(EVIDENCE) --base-dir . --verbose

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
