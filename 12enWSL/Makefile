# Makefile — Week 12: Email Protocols and RPC
# NETWORKING class - ASE, CSIE | by ing. dr. Antonio Clim
#
# Usage: make help

.PHONY: help start stop status logs test smoke quiz lint lint-fix syntax verify clean
.PHONY: anti-ai-challenge anti-ai-run anti-ai-evidence anti-ai-validate
.PHONY: smtp-server smtp-send smtp-list demo-smtp demo-rpc capture analyse
.PHONY: ci docker-build docker-test export-moodle export-canvas export-csv

PYTHON := python3
COMPOSE := docker compose -f docker/docker-compose.yml
RUFF := ruff

# ═══════════════════════════════════════════════════════════════════════════════
# HELP
# ═══════════════════════════════════════════════════════════════════════════════
help:
	@echo ""
	@echo "Week 12 Laboratory Commands"
	@echo "═══════════════════════════════════════════════════════════════════════"
	@echo ""
	@echo "Lab Environment:"
	@echo "  make start         Start laboratory containers"
	@echo "  make stop          Stop laboratory containers"
	@echo "  make status        Show container status"
	@echo "  make logs          Follow container logs"
	@echo ""
	@echo "Testing and Quality:"
	@echo "  make test          Run all pytest tests"
	@echo "  make smoke         Run smoke tests only"
	@echo "  make quiz          Run formative self-assessment quiz"
	@echo "  make lint          Run ruff linter (check only)"
	@echo "  make lint-fix      Run ruff linter with auto-fix"
	@echo "  make syntax        Check Python syntax only"
	@echo "  make ci            Run full CI pipeline locally"
	@echo ""
	@echo "Quiz Export (LMS):"
	@echo "  make export-moodle Export quiz to Moodle XML format"
	@echo "  make export-canvas Export quiz to Canvas QTI format"
	@echo "  make export-csv    Export quiz to CSV format"
	@echo ""
	@echo "Development:"
	@echo "  make verify        Verify environment setup"
	@echo "  make clean         Clean artifacts and caches"
	@echo "  make anti-ai-challenge STUDENT_ID=...  Issue a short-lived anti-AI challenge"
	@echo "  make anti-ai-run STUDENT_ID=...        Run the required protocol interactions"
	@echo "  make anti-ai-evidence STUDENT_ID=... PCAP=...  Write evidence JSON"
	@echo "  make anti-ai-validate STUDENT_ID=...  Validate evidence against the challenge"
	@echo ""
	@echo "SMTP Services:"
	@echo "  make smtp-server   Start SMTP server (foreground)"
	@echo "  make smtp-send     Send a test email"
	@echo "  make smtp-list     List stored emails"
	@echo ""
	@echo "Demos:"
	@echo "  make demo-smtp     Run SMTP demonstration"
	@echo "  make demo-rpc      Run RPC comparison demo"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build  Build Docker image"
	@echo "  make docker-test   Test Docker container"
	@echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# LAB ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
start:
	@echo "Starting Week 12 laboratory..."
	@$(PYTHON) scripts/start_lab.py

stop:
	@echo "Stopping Week 12 laboratory..."
	@$(PYTHON) scripts/stop_lab.py

status:
	@$(COMPOSE) ps

logs:
	@$(COMPOSE) logs -f

# ═══════════════════════════════════════════════════════════════════════════════
# TESTING AND QUALITY
# ═══════════════════════════════════════════════════════════════════════════════

test:
	@echo "Running pytest..."
	@$(PYTHON) -m pytest tests/ -v --tb=short

smoke:
	@echo "Running smoke tests..."
	@$(PYTHON) tests/smoke_test.py

quiz:
	@echo "Starting formative quiz..."
	@$(PYTHON) formative/run_quiz.py

quiz-random:
	@echo "Starting randomised quiz..."
	@$(PYTHON) formative/run_quiz.py --random

quiz-lo:
	@echo "Available Learning Objectives:"
	@$(PYTHON) formative/run_quiz.py --list-lo

lint:
	@echo "Running ruff linter..."
	@$(RUFF) check src/ scripts/ tests/ formative/ anti_ai/ --config ruff.toml || true
	@echo "Lint check complete."

lint-fix:
	@echo "Running ruff linter with auto-fix..."
	@$(RUFF) check src/ scripts/ tests/ formative/ anti_ai/ --config ruff.toml --fix

syntax:
	@echo "Checking Python syntax..."
	@$(PYTHON) -m compileall -q src scripts tests formative anti_ai && echo "  ✓ compileall OK"
	@echo "Syntax check complete."

# ═══════════════════════════════════════════════════════════════════════════════
# ANTI-AI (HOMEWORK)
# ═══════════════════════════════════════════════════════════════════════════════
anti-ai-challenge:
	@if [ -z "$(STUDENT_ID)" ]; then echo "Usage: make anti-ai-challenge STUDENT_ID=..."; exit 2; fi
	@$(PYTHON) scripts/anti_ai_issue_challenge.py --student-id "$(STUDENT_ID)" $(if $(STRICT),--strict,)

anti-ai-run:
	@if [ -z "$(STUDENT_ID)" ]; then echo "Usage: make anti-ai-run STUDENT_ID=..."; exit 2; fi
	@$(PYTHON) scripts/anti_ai_run_week12_probes.py --challenge artifacts/anti_ai/challenge_$(STUDENT_ID).yaml

anti-ai-evidence:
	@if [ -z "$(STUDENT_ID)" ] || [ -z "$(PCAP)" ]; then echo "Usage: make anti-ai-evidence STUDENT_ID=... PCAP=..."; exit 2; fi
	@$(PYTHON) scripts/anti_ai_generate_evidence.py --student-id "$(STUDENT_ID)" --pcap "$(PCAP)"

anti-ai-validate:
	@if [ -z "$(STUDENT_ID)" ]; then echo "Usage: make anti-ai-validate STUDENT_ID=..."; exit 2; fi
	@$(PYTHON) scripts/anti_ai_validate.py --challenge artifacts/anti_ai/challenge_$(STUDENT_ID).yaml --evidence artifacts/anti_ai/evidence_$(STUDENT_ID).json

ci: syntax lint
	@echo ""
	@echo "Running CI checks..."
	@echo "═══════════════════════════════════════════════════════════════════════"
	@echo "1. Validating quiz YAML..."
	@$(PYTHON) -c "import yaml; data=yaml.safe_load(open('formative/quiz.yaml')); print(f'   ✓ Quiz has {len(data[\"questions\"])} questions')"
	@echo "2. Validating quiz JSON..."
	@$(PYTHON) -c "import json; data=json.load(open('formative/quiz.json')); print(f'   ✓ Quiz JSON has {len(data[\"questions\"])} questions')"
	@echo "3. Testing quiz runner..."
	@$(PYTHON) formative/run_quiz.py --list-lo > /dev/null && echo "   ✓ Quiz runner works"
	@echo ""
	@echo "CI checks complete."

verify:
	@$(PYTHON) setup/verify_environment.py

clean:
	@echo "Cleaning artifacts..."
	@rm -rf artifacts/*.pcap artifacts/*.log 2>/dev/null || true
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@rm -rf .pytest_cache .mypy_cache .ruff_cache 2>/dev/null || true
	@echo "Clean complete."

# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ EXPORT (LMS)
# ═══════════════════════════════════════════════════════════════════════════════
export-moodle:
	@echo "Exporting quiz to Moodle XML format..."
	@$(PYTHON) formative/export_lms.py --format moodle

export-canvas:
	@echo "Exporting quiz to Canvas QTI format..."
	@$(PYTHON) formative/export_lms.py --format canvas

export-csv:
	@echo "Exporting quiz to CSV format..."
	@$(PYTHON) formative/export_lms.py --format csv

# ═══════════════════════════════════════════════════════════════════════════════
# SMTP SERVICES
# ═══════════════════════════════════════════════════════════════════════════════
smtp-server:
	@echo "Starting SMTP server on localhost:1025..."
	@$(PYTHON) src/apps/email/smtp_server.py --verbose

smtp-send:
	@echo "Sending test email..."
	@$(PYTHON) src/apps/email/smtp_client.py

smtp-list:
	@echo "Stored emails:"
	@ls -la docker/volumes/spool/*.eml 2>/dev/null || echo "  (no emails stored)"

# ═══════════════════════════════════════════════════════════════════════════════
# DEMOS
# ═══════════════════════════════════════════════════════════════════════════════
demo-smtp:
	@$(PYTHON) scripts/run_demo.py smtp

demo-rpc:
	@$(PYTHON) scripts/run_demo.py rpc

# ═══════════════════════════════════════════════════════════════════════════════
# DOCKER
# ═══════════════════════════════════════════════════════════════════════════════
docker-build:
	@echo "Building Docker image..."
	@docker build -t week12-lab -f docker/Dockerfile .
	@echo "✓ Docker image built"

docker-test:
	@echo "Testing Docker container..."
	@docker run --rm week12-lab python --version
	@echo "✓ Container runs successfully"
