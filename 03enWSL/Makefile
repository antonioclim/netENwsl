# Week 3 Makefile - Network Programming Lab
# NETWORKING class - ASE, CSIE | by ing. dr. Antonio Clim

PYTHON := python3
DOCKER_COMPOSE := docker compose -f docker/docker-compose.yml

.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

.PHONY: setup
setup: ## Install dependencies
	$(PYTHON) -m pip install -r setup/requirements.txt

.PHONY: start
start: setup docker-up status ## Quick start: setup + docker + status

.PHONY: stop
stop: docker-down ## Stop lab environment

.PHONY: lint
lint: ## Run ruff linter
	$(PYTHON) -m ruff check src/ scripts/ formative/ tests/ anti_ai/

.PHONY: test
test: ## Run all tests
	$(PYTHON) -m pytest tests/ -v

.PHONY: test-unit
test-unit: ## Run unit tests (no Docker)
	$(PYTHON) -m pytest tests/test_environment.py -v -k "not docker"

.PHONY: quiz
quiz: ## Run formative quiz
	$(PYTHON) formative/run_quiz.py

.PHONY: quiz-validate
quiz-validate: ## Validate quiz structure
	$(PYTHON) formative/run_quiz.py --validate

.PHONY: export-lms
export-lms: ## Export quiz to LMS formats
	$(PYTHON) formative/run_quiz.py --export-lms moodle
	$(PYTHON) formative/run_quiz.py --export-lms canvas
	$(PYTHON) formative/run_quiz.py --export-lms json

.PHONY: docker-build
docker-build: ## Build Docker images
	$(DOCKER_COMPOSE) build

.PHONY: docker-up
docker-up: ## Start lab containers
	$(DOCKER_COMPOSE) up -d

.PHONY: docker-down
docker-down: ## Stop lab containers
	$(DOCKER_COMPOSE) down

.PHONY: docker-logs
docker-logs: ## Show container logs
	$(DOCKER_COMPOSE) logs --tail=50

.PHONY: status
status: ## Show container status
	$(DOCKER_COMPOSE) ps

# ─────────────────────────────────────────────────────────────────────────────
# Anti-AI workflow (Week 3)
# ─────────────────────────────────────────────────────────────────────────────
STUDENT_ID ?= YOUR_STUDENT_ID
CHALLENGE ?= artifacts/anti_ai/challenge_$(STUDENT_ID).yaml
EVIDENCE ?= artifacts/anti_ai/evidence_$(STUDENT_ID).json

.PHONY: anti-ai-challenge
anti-ai-challenge: ## Generate a per-student anti-AI challenge file
	$(PYTHON) -m anti_ai.challenge_generator --student-id $(STUDENT_ID)

.PHONY: anti-ai-evidence
anti-ai-evidence: ## Collect evidence (hashes and fingerprint) for a submission
	$(PYTHON) -m anti_ai.evidence_collector \
		--challenge $(CHALLENGE) \
		--base-dir . \
		--output $(EVIDENCE) \
		--artefact artifacts/anti_ai/w03_report_$(STUDENT_ID).md \
		--artefact artifacts/anti_ai/w03_broadcast_$(STUDENT_ID).pcap \
		--artefact artifacts/anti_ai/w03_multicast_$(STUDENT_ID).pcap \
		--artefact artifacts/anti_ai/w03_tunnel_$(STUDENT_ID).pcap

.PHONY: anti-ai-validate
anti-ai-validate: ## Validate a submission against the challenge (anti-AI)
	$(PYTHON) -m anti_ai.submission_validator \
		--challenge $(CHALLENGE) \
		--evidence $(EVIDENCE) \
		--base-dir . \
		--verbose

.PHONY: validate
validate: quiz-validate ## Run all validations
	@echo "Validating YAML files..."
	@$(PYTHON) -c "import yaml; from pathlib import Path; [yaml.safe_load(f.read_text()) for f in Path('.').rglob('*.yaml')]"
	@echo "All validations passed!"

.PHONY: verify-checksums
verify-checksums: ## Verify file checksums
	$(PYTHON) setup/verify_checksums.py

.PHONY: clean
clean: ## Clean generated files
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache htmlcov .coverage

.PHONY: ci
ci: lint validate test-unit ## Simulate CI locally
