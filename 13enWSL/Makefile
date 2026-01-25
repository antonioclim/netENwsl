# ══════════════════════════════════════════════════════════════════════════════
# Week 13: IoT and Security — Makefile
# Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim
# ══════════════════════════════════════════════════════════════════════════════

PYTHON := python3
PYTEST := $(PYTHON) -m pytest
QUIZ_RUNNER := formative/run_quiz.py
VULN_CHECKER := src/exercises/ex_13_04_vuln_checker.py

# Directories
ARTIFACTS_DIR := artifacts
DOCS_DIR := docs

.PHONY: all help setup lint test test-exports quiz quiz-random quiz-moodle quiz-canvas quiz-export scan clean

# ──────────────────────────────────────────────────────────────────────────────
# Default target
# ──────────────────────────────────────────────────────────────────────────────

all: lint test-exports
	@echo "✅ All checks passed"

help:
	@echo "Week 13: IoT and Security — Available Targets"
	@echo "══════════════════════════════════════════════"
	@echo ""
	@echo "Setup:"
	@echo "  make setup          Install Python dependencies"
	@echo ""
	@echo "Quality:"
	@echo "  make lint           Run flake8 linter"
	@echo "  make test           Run all unit tests"
	@echo "  make test-exports   Run LMS export tests"
	@echo "  make all            Run lint + test-exports"
	@echo ""
	@echo "Quiz:"
	@echo "  make quiz           Run interactive quiz"
	@echo "  make quiz-random    Run 5 random questions"
	@echo "  make quiz-moodle    Export to Moodle XML"
	@echo "  make quiz-canvas    Export to Canvas JSON"
	@echo "  make quiz-export    Export to both formats"
	@echo ""
	@echo "Security:"
	@echo "  make scan           Run vulnerability scanner (localhost)"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean          Remove generated files"

# ──────────────────────────────────────────────────────────────────────────────
# Setup
# ──────────────────────────────────────────────────────────────────────────────

setup:
	pip install -r setup/requirements.txt
	@echo "✅ Dependencies installed"

# ──────────────────────────────────────────────────────────────────────────────
# Code Quality
# ──────────────────────────────────────────────────────────────────────────────

lint:
	@echo "Running flake8..."
	flake8 formative/ src/ tests/ --max-line-length=100 --ignore=E501,W503
	@echo "✅ Linting passed"

test:
	$(PYTEST) tests/ -v --tb=short

test-exports:
	$(PYTEST) tests/test_quiz_exports.py -v --tb=short
	@echo "✅ Export tests passed"

# ──────────────────────────────────────────────────────────────────────────────
# Quiz Operations
# ──────────────────────────────────────────────────────────────────────────────

quiz:
	$(PYTHON) $(QUIZ_RUNNER)

quiz-random:
	$(PYTHON) $(QUIZ_RUNNER) --random --limit 5

quiz-bloom-%:
	$(PYTHON) $(QUIZ_RUNNER) --bloom $*

# ──────────────────────────────────────────────────────────────────────────────
# LMS Exports
# ──────────────────────────────────────────────────────────────────────────────

$(ARTIFACTS_DIR):
	mkdir -p $(ARTIFACTS_DIR)

quiz-moodle: $(ARTIFACTS_DIR)
	$(PYTHON) $(QUIZ_RUNNER) --export-moodle $(ARTIFACTS_DIR)/quiz_moodle.xml
	@echo "✅ Moodle XML: $(ARTIFACTS_DIR)/quiz_moodle.xml"

quiz-canvas: $(ARTIFACTS_DIR)
	$(PYTHON) $(QUIZ_RUNNER) --export-canvas $(ARTIFACTS_DIR)/quiz_canvas.json
	@echo "✅ Canvas JSON: $(ARTIFACTS_DIR)/quiz_canvas.json"

quiz-export: quiz-moodle quiz-canvas
	@echo "✅ All LMS exports complete"

# ──────────────────────────────────────────────────────────────────────────────
# Security Scanning
# ──────────────────────────────────────────────────────────────────────────────

scan:
	$(PYTHON) $(VULN_CHECKER) --target localhost

scan-report: $(ARTIFACTS_DIR)
	$(PYTHON) $(VULN_CHECKER) --target localhost --output $(ARTIFACTS_DIR)/vuln_report.json

# ──────────────────────────────────────────────────────────────────────────────
# Maintenance
# ──────────────────────────────────────────────────────────────────────────────

clean:
	rm -rf $(ARTIFACTS_DIR)
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf .pytest_cache */.pytest_cache
	rm -rf *.pyc */*.pyc */*/*.pyc
	rm -rf .coverage htmlcov/
	@echo "✅ Cleaned generated files"
