# ═══════════════════════════════════════════════════════════════════════════════
# Makefile — Week 9: Session Layer and Presentation Layer
# NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: help setup install start stop restart test smoke quiz quiz-stats quiz-export         lint lint-fix format validate demo capture clean clean-docker         anti-ai-challenge anti-ai-evidence anti-ai-validate

PYTHON := python3
PIP := pip3
DOCKER_COMPOSE := docker compose -f docker/docker-compose.yml

# Anti-AI defaults (override on the command line)
STUDENT_ID ?= STUDENTID
ANTI_AI_DIR ?= artifacts/anti_ai
ANTI_AI_CHALLENGE ?= $(ANTI_AI_DIR)/challenge_week09_$(STUDENT_ID).json
ANTI_AI_EVIDENCE ?= $(ANTI_AI_DIR)/evidence_week09_$(STUDENT_ID).json
ANTI_AI_REPORT ?= artifacts/week09_report_$(STUDENT_ID).md
ANTI_AI_PCAP ?= pcap/week09_$(STUDENT_ID).pcapng

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
	@echo "Anti-AI workflow:"
	@echo "  make anti-ai-challenge STUDENT_ID=...               Generate a time-bound challenge"
	@echo "  make anti-ai-evidence STUDENT_ID=... ANTI_AI_PCAP=... Collect evidence (hashes and provenance)"
	@echo "  make anti-ai-validate STUDENT_ID=...                Validate evidence before submission"
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

anti-ai-challenge:
	$(PYTHON) -m anti_ai.challenge_generator --student-id $(STUDENT_ID)

anti-ai-evidence:
	$(PYTHON) -m anti_ai.evidence_collector --challenge $(ANTI_AI_CHALLENGE) --pcap $(ANTI_AI_PCAP) --report $(ANTI_AI_REPORT)

anti-ai-validate:
	$(PYTHON) -m anti_ai.submission_validator --challenge $(ANTI_AI_CHALLENGE) --evidence $(ANTI_AI_EVIDENCE)

lint:
	$(PYTHON) -m ruff check src/ scripts/ tests/ formative/ anti_ai/ --ignore E501,E402

lint-fix:
	$(PYTHON) -m ruff check --fix src/ scripts/ tests/ formative/ anti_ai/

clean:
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf .pytest_cache .ruff_cache
	rm -rf artifacts/*.pcap artifacts/*.log
	rm -rf artifacts/anti_ai/*.json

clean-docker:
	$(DOCKER_COMPOSE) down --volumes --remove-orphans
