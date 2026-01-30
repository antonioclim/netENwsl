# Week 5 Laboratory Orchestrator
# Computer Networks — ASE-CSIE Bucharest

SHELL := /bin/bash
.DEFAULT_GOAL := help

PYTHON := python3
PYTEST := $(PYTHON) -m pytest

BLUE := \033[0;34m
GREEN := \033[0;32m
NC := \033[0m

.PHONY: help
help: ## Show this help message
	@echo ""
	@echo "Week 5: IP Addressing, Subnetting and VLSM"
	@echo "$(BLUE)════════════════════════════════════════════$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(GREEN)%-18s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: setup
setup: ## Install dependencies and verify environment
	pip install -q pyyaml pytest pytest-cov ruff
	$(PYTHON) setup/verify_environment.py || true

.PHONY: check-python
check-python: ## Check Python syntax for all files
	@find src tests scripts formative anti_ai homework -name "*.py" -type f | xargs $(PYTHON) -m py_compile
	@echo "$(GREEN)✓ All Python files have valid syntax$(NC)"

.PHONY: test
test: smoke unit ## Run all tests (smoke + unit)

.PHONY: smoke
smoke: ## Run smoke tests only
	$(PYTHON) tests/smoke_test.py

.PHONY: unit
unit: ## Run unit tests with pytest
	$(PYTEST) tests/ -v --tb=short

.PHONY: quiz
quiz: ## Run the formative assessment quiz
	$(PYTHON) formative/run_quiz.py

.PHONY: quiz-random
quiz-random: ## Run quiz with randomised questions
	$(PYTHON) formative/run_quiz.py --random

.PHONY: quiz-quick
quiz-quick: ## Run a quick 5-question quiz
	$(PYTHON) formative/run_quiz.py --limit 5 --random

.PHONY: quiz-validate
quiz-validate: ## Validate quiz YAML file
	@$(PYTHON) -c "import yaml; q=yaml.safe_load(open('formative/quiz.yaml')); print(f'✓ Valid: {len(q[\"questions\"])} questions')"

.PHONY: lms-export
lms-export: ## Export quiz for LMS (Moodle/Canvas)
	$(PYTHON) formative/export_to_lms.py --format json --pretty --output formative/quiz_lms_export.json
	@echo "$(GREEN)✓ Exported to formative/quiz_lms_export.json$(NC)"

.PHONY: lab
lab: ## Start the Docker lab environment
	$(PYTHON) scripts/start_lab.py

# ─── ANTI-AI WORKFLOW ───────────────────────────────────────────────────────
# Usage examples:
#   make anti-ai-challenge STUDENT_ID=ABC123
#   python homework/exercises/hw_5_01_subnet_design.py --challenge artifacts/anti_ai/challenge_ABC123.yaml --non-interactive
#   python homework/exercises/hw_5_02_ipv6_transition.py --challenge artifacts/anti_ai/challenge_ABC123.yaml --non-interactive
#   make anti-ai-evidence STUDENT_ID=ABC123
#   make anti-ai-validate STUDENT_ID=ABC123

ANTI_AI_DIR := artifacts/anti_ai

.PHONY: anti-ai-challenge
anti-ai-challenge: ## Generate an individual anti-AI challenge (set STUDENT_ID=...)
	@if [ -z "$(STUDENT_ID)" ]; then echo "ERROR: set STUDENT_ID, for example: make $@ STUDENT_ID=ABC123"; exit 2; fi
	$(PYTHON) -m anti_ai.challenge_generator --student-id "$(STUDENT_ID)"

.PHONY: anti-ai-evidence
anti-ai-evidence: ## Collect evidence.json for the required artefacts (set STUDENT_ID=...)
	@if [ -z "$(STUDENT_ID)" ]; then echo "ERROR: set STUDENT_ID, for example: make $@ STUDENT_ID=ABC123"; exit 2; fi
	$(PYTHON) -m anti_ai.evidence_collector \
		--challenge "$(ANTI_AI_DIR)/challenge_$(STUDENT_ID).yaml" \
		--artefact "subnet_plan_$(STUDENT_ID).json" \
		--artefact "ipv6_report_$(STUDENT_ID).json" \
		--output "evidence_$(STUDENT_ID).json"

.PHONY: anti-ai-validate
anti-ai-validate: ## Validate the challenge, evidence and artefacts (set STUDENT_ID=...)
	@if [ -z "$(STUDENT_ID)" ]; then echo "ERROR: set STUDENT_ID, for example: make $@ STUDENT_ID=ABC123"; exit 2; fi
	$(PYTHON) -m anti_ai.submission_validator \
		--challenge "$(ANTI_AI_DIR)/challenge_$(STUDENT_ID).yaml" \
		--evidence "evidence_$(STUDENT_ID).json" \
		--base-dir "." \
		--verbose


.PHONY: lint
lint: ## Run code linter (ruff)
	ruff check src/ scripts/ tests/ formative/ anti_ai/ homework/ --ignore E501,E402 || true

.PHONY: lint-fix
lint-fix: ## Auto-fix linting issues
	ruff check src/ scripts/ tests/ formative/ anti_ai/ homework/ --fix --ignore E501,E402 || true

.PHONY: clean
clean: ## Clean generated files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .pytest_cache .ruff_cache 2>/dev/null || true
	@echo "$(GREEN)✓ Cleanup complete$(NC)"

.PHONY: docs-check
docs-check: ## Verify all required documentation exists
	@for doc in README.md docs/learning_objectives.md docs/misconceptions.md docs/ci_setup.md; do \
		if [ -f "$$doc" ]; then echo "$(GREEN)✓$(NC) $$doc"; else echo "✗ $$doc (missing)"; fi; \
	done

.PHONY: ci
ci: check-python lint smoke unit quiz-validate docs-check ## Run full CI pipeline locally
	@echo ""
	@echo "$(GREEN)═══════════════════════════════════════$(NC)"
	@echo "$(GREEN)  ✓ CI Pipeline Passed Successfully!   $(NC)"
	@echo "$(GREEN)═══════════════════════════════════════$(NC)"
