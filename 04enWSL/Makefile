# ═══════════════════════════════════════════════════════════════════════════════
# Makefile — Week 4 Laboratory Kit
# NETWORKING class - ASE, Informatics | Computer Networks Laboratory
# by ing. dr. Antonio Clim
# ═══════════════════════════════════════════════════════════════════════════════
#
# Version: 1.6.0
# Last Updated: 2026-01-24
#
# Usage:
#   make help           - Show available commands
#   make verify         - Check environment setup
#   make verify-integrity - Verify all kit artefacts exist
#   make test           - Run all tests
#   make quiz           - Run formative quiz
#   make docker-up      - Start lab containers
#   make docker-down    - Stop lab containers
#   make generate-pcap  - Generate PCAP sample files
#   make export-quiz-moodle - Export quiz to Moodle format
#   make export-quiz-canvas - Export quiz to Canvas format
#
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: help test quiz lint docker-up docker-down clean verify smoke unit start stop
.PHONY: verify-integrity generate-pcap syntax-check typecheck
.PHONY: validate-quiz verify-manifest update-manifest pre-commit-install pre-commit
.PHONY: export-quiz-moodle export-quiz-canvas export-quiz-all

PYTHON := python3
DOCKER_COMPOSE := docker compose -f docker/docker-compose.yml

# Default target
.DEFAULT_GOAL := help


# ═══════════════════════════════════════════════════════════════════════════════
# HELP
# ═══════════════════════════════════════════════════════════════════════════════

help:
	@echo ""
	@echo "╔══════════════════════════════════════════════════════════════╗"
	@echo "║  Week 4 Laboratory Kit — Available Commands                  ║"
	@echo "║  Physical Layer, Data Link Layer & Custom Protocols          ║"
	@echo "║  Version 1.6.0                                               ║"
	@echo "╚══════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "  Environment:"
	@echo "    make verify           - Verify environment setup"
	@echo "    make verify-integrity - Verify all kit artefacts exist"
	@echo "    make start            - Start lab (docker-up + status)"
	@echo "    make stop             - Stop lab and clean"
	@echo ""
	@echo "  Testing:"
	@echo "    make test             - Run all tests"
	@echo "    make smoke            - Run smoke tests only"
	@echo "    make unit             - Run unit tests only"
	@echo "    make syntax-check     - Verify Python syntax"
	@echo ""
	@echo "  Learning:"
	@echo "    make quiz             - Run formative quiz (full)"
	@echo "    make quiz-random      - Run 10 random questions"
	@echo "    make quiz-lo3         - Quiz only LO3 questions"
	@echo "    make quiz-lo4         - Quiz only LO4 questions"
	@echo ""
	@echo "  Quiz Export (LMS):"
	@echo "    make export-quiz-moodle - Export quiz to Moodle JSON"
	@echo "    make export-quiz-canvas - Export quiz to Canvas JSON"
	@echo "    make export-quiz-all    - Export quiz to all formats"
	@echo ""
	@echo "  Docker:"
	@echo "    make docker-up        - Start lab containers"
	@echo "    make docker-down      - Stop lab containers"
	@echo "    make docker-logs      - Follow container logs"
	@echo "    make docker-status    - Show container status"
	@echo ""
	@echo "  Code Quality:"
	@echo "    make lint             - Check code style (ruff)"
	@echo "    make typecheck        - Run type checker (mypy)"
	@echo ""
	@echo "  Integrity & Validation:"
	@echo "    make validate-quiz    - Validate quiz.yaml schema"
	@echo "    make verify-manifest  - Verify file checksums"
	@echo "    make update-manifest  - Update manifest checksums"
	@echo "    make pre-commit       - Run all pre-commit checks"
	@echo ""
	@echo "  PCAP Generation:"
	@echo "    make generate-pcap    - Generate sample PCAP files"
	@echo "    make capture-text     - Capture TEXT protocol traffic"
	@echo "    make capture-binary   - Capture BINARY protocol traffic"
	@echo "    make capture-udp      - Capture UDP sensor traffic"
	@echo ""
	@echo "  Cleanup:"
	@echo "    make clean            - Clean artefacts and caches"
	@echo "    make clean-docker     - Remove Docker volumes"
	@echo ""


# ═══════════════════════════════════════════════════════════════════════════════
# ENVIRONMENT VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════

verify:
	@echo "Verifying environment..."
	@$(PYTHON) setup/verify_environment.py

verify-integrity:
	@echo ""
	@echo "Verifying kit integrity..."
	@$(PYTHON) scripts/verify_kit_integrity.py

start: docker-up
	@echo ""
	@echo "╔══════════════════════════════════════════════════════════════╗"
	@echo "║  Lab environment ready!                                      ║"
	@echo "╚══════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "  Services available:"
	@echo "    TEXT Server:   localhost:5400"
	@echo "    BINARY Server: localhost:5401"
	@echo "    UDP Sensor:    localhost:5402"
	@echo "    Portainer:     http://localhost:9000"
	@echo ""
	@echo "  Run exercises with:"
	@echo "    $(PYTHON) src/exercises/ex_4_01_tcp_proto.py"
	@echo ""

stop: docker-down clean
	@echo "Lab environment stopped."


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

test: syntax-check smoke unit
	@echo ""
	@echo "All tests completed."

smoke:
	@echo ""
	@echo "Running smoke tests..."
	@$(PYTHON) tests/smoke_test.py

unit:
	@echo ""
	@echo "Running unit tests..."
	@$(PYTHON) -m pytest tests/test_unit_functions.py -v --tb=short 2>/dev/null || \
		$(PYTHON) tests/test_unit_functions.py

syntax-check:
	@echo ""
	@echo "Checking Python syntax..."
	@find . -name "*.py" -not -path "./.git/*" -not -path "*/__pycache__/*" | \
		xargs $(PYTHON) -m py_compile
	@echo "  ✓ All Python files have valid syntax"


# ═══════════════════════════════════════════════════════════════════════════════
# FORMATIVE QUIZ
# ═══════════════════════════════════════════════════════════════════════════════

quiz:
	@echo ""
	@$(PYTHON) formative/run_quiz.py

quiz-random:
	@echo ""
	@$(PYTHON) formative/run_quiz.py --random 10

quiz-lo3:
	@echo ""
	@$(PYTHON) formative/run_quiz.py --lo LO3

quiz-lo4:
	@echo ""
	@$(PYTHON) formative/run_quiz.py --lo LO4


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ LMS EXPORT
# ═══════════════════════════════════════════════════════════════════════════════

export-quiz-moodle:
	@echo ""
	@echo "Exporting quiz to Moodle format..."
	@$(PYTHON) scripts/export_quiz_lms.py --format moodle

export-quiz-canvas:
	@echo ""
	@echo "Exporting quiz to Canvas format..."
	@$(PYTHON) scripts/export_quiz_lms.py --format canvas

export-quiz-all:
	@echo ""
	@echo "Exporting quiz to all LMS formats..."
	@$(PYTHON) scripts/export_quiz_lms.py --format all


# ═══════════════════════════════════════════════════════════════════════════════
# CODE QUALITY
# ═══════════════════════════════════════════════════════════════════════════════

lint: syntax-check
	@echo ""
	@echo "Checking code style..."
	@echo ""
	@echo "Style check (ruff):"
	@command -v ruff >/dev/null 2>&1 && \
		ruff check src/ scripts/ tests/ --ignore E501 || \
		echo "  (ruff not installed - run: pip install ruff)"

typecheck:
	@echo ""
	@echo "Running type checker..."
	@command -v mypy >/dev/null 2>&1 && \
		mypy src/ --ignore-missing-imports --no-error-summary || \
		echo "(mypy not installed - run: pip install mypy)"


# ═══════════════════════════════════════════════════════════════════════════════
# DOCKER
# ═══════════════════════════════════════════════════════════════════════════════

docker-up:
	@echo ""
	@echo "Starting lab containers..."
	@$(DOCKER_COMPOSE) up -d
	@echo ""
	@$(DOCKER_COMPOSE) ps

docker-down:
	@echo ""
	@echo "Stopping lab containers..."
	@$(DOCKER_COMPOSE) down

docker-logs:
	@$(DOCKER_COMPOSE) logs -f

docker-status:
	@$(DOCKER_COMPOSE) ps

docker-restart: docker-down docker-up


# ═══════════════════════════════════════════════════════════════════════════════
# PCAP GENERATION
# ═══════════════════════════════════════════════════════════════════════════════

generate-pcap:
	@echo ""
	@echo "Generating PCAP sample files..."
	@$(PYTHON) scripts/generate_pcap_samples.py

capture-text:
	@echo "Capturing TEXT protocol traffic..."
	@$(PYTHON) scripts/capture_traffic.py --interface any --port 5400 --output pcap/week04_lo3_text_proto.pcap

capture-binary:
	@echo "Capturing BINARY protocol traffic..."
	@$(PYTHON) scripts/capture_traffic.py --interface any --port 5401 --output pcap/week04_lo4_binary_proto.pcap

capture-udp:
	@echo "Capturing UDP sensor traffic..."
	@$(PYTHON) scripts/capture_traffic.py --interface any --port 5402 --output pcap/week04_lo5_udp_sensor.pcap


# ═══════════════════════════════════════════════════════════════════════════════
# CLEANUP
# ═══════════════════════════════════════════════════════════════════════════════

clean:
	@echo ""
	@echo "Cleaning artefacts..."
	@rm -rf artifacts/*.pcap artifacts/*.log 2>/dev/null || true
	@rm -rf __pycache__ */__pycache__ */*/__pycache__ 2>/dev/null || true
	@rm -rf .pytest_cache .mypy_cache .ruff_cache 2>/dev/null || true
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@find . -name ".DS_Store" -delete 2>/dev/null || true
	@echo "  ✓ Cleanup complete"

clean-docker:
	@echo ""
	@echo "Removing Docker volumes..."
	@$(DOCKER_COMPOSE) down --volumes --remove-orphans 2>/dev/null || true
	@docker image prune -f 2>/dev/null || true
	@echo "  ✓ Docker cleanup complete"

clean-all: clean clean-docker
	@echo ""
	@echo "Full cleanup complete."


# ═══════════════════════════════════════════════════════════════════════════════
# AI RISK PREVENTION (Integrity & Validation)
# ═══════════════════════════════════════════════════════════════════════════════

validate-quiz:
	@echo ""
	@echo "Validating quiz schema..."
	@$(PYTHON) scripts/validate_quiz_schema.py

verify-manifest:
	@echo ""
	@echo "Verifying file checksums..."
	@$(PYTHON) scripts/verify_manifest.py

update-manifest:
	@echo ""
	@echo "Updating manifest checksums..."
	@$(PYTHON) scripts/verify_manifest.py --update


# ═══════════════════════════════════════════════════════════════════════════════
# PRE-COMMIT HOOKS
# ═══════════════════════════════════════════════════════════════════════════════

pre-commit-install:
	@echo ""
	@echo "Installing pre-commit hooks..."
	@command -v pre-commit >/dev/null 2>&1 && \
		pre-commit install || \
		echo "(pre-commit not installed - run: pip install pre-commit)"

pre-commit: verify-integrity syntax-check validate-quiz verify-manifest lint
	@echo ""
	@echo "╔══════════════════════════════════════════════════════════════╗"
	@echo "║  ✓ All pre-commit checks passed                              ║"
	@echo "╚══════════════════════════════════════════════════════════════╝"


# ═══════════════════════════════════════════════════════════════════════════════
# DEVELOPMENT (Instructor use)
# ═══════════════════════════════════════════════════════════════════════════════

demo1:
	@$(PYTHON) scripts/run_demo.py --demo 1

demo2:
	@$(PYTHON) scripts/run_demo.py --demo 2
