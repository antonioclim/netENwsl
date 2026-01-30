# ============================================================================
# Makefile — Week 7: Packet Interception, Filtering and Defensive Port Probing
# NETWORKING class - ASE, Informatics | Computer Networks Laboratory
# ============================================================================
#
# Usage:
#   make help          - Show available targets
#   make start         - Start lab environment
#   make stop          - Stop lab environment
#   make test          - Run all tests
#   make quiz          - Run formative quiz
#   make lint          - Run code linting
#   make ci            - Run full CI pipeline locally
#
# Prerequisites:
#   - Python 3.11+
#   - Docker and Docker Compose
#   - pip install -r setup/requirements.txt
#
# ============================================================================

.PHONY: all help start stop restart clean test quiz parsons smoke verify install
.PHONY: lint format ci export-quiz generate-pcap anti-ai-challenge anti-ai-evidence anti-ai-validate
.DEFAULT_GOAL := help

# ─── CONFIGURATION ──────────────────────────────────────────────────────────

PYTHON := python3
PIP := pip3
DOCKER_COMPOSE := docker compose -f docker/docker-compose.yml

# Colours for terminal output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
NC := \033[0m # No Colour

# ─── HELP ───────────────────────────────────────────────────────────────────

help:
	@echo ""
	@echo "$(BLUE)╔════════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(BLUE)║          Week 7 Laboratory - Available Commands                ║$(NC)"
	@echo "$(BLUE)╠════════════════════════════════════════════════════════════════╣$(NC)"
	@echo "$(BLUE)║                                                                ║$(NC)"
	@echo "$(BLUE)║$(NC)  $(GREEN)Environment Management:$(NC)                                      $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)    make start        Start Docker containers                   $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)    make stop         Stop Docker containers                    $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)    make restart      Restart all containers                    $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)    make clean        Remove containers and networks            $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)    make verify       Verify environment setup                  $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)                                                                $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)  $(GREEN)Testing:$(NC)                                                      $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)    make test         Run all exercise tests                    $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)    make smoke        Run smoke tests only                      $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)    make test-1       Run Exercise 1 tests                      $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)    make test-2       Run Exercise 2 tests                      $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)    make test-3       Run Exercise 3 tests                      $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)    make test-4       Run Exercise 4 tests                      $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)    make test-5       Run Exercise 5 tests                      $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)                                                                $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)  $(GREEN)Formative Assessment:$(NC)                                         $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)    make quiz         Run formative quiz (15 questions)         $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)    make quiz-quick   Run quick quiz (5 random questions)       $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)    make quiz-lo1     Run LO1 questions only                    $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)    make parsons      Run Parsons problems                      $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)    make review       Review quiz (show answers)                $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)    make export-quiz  Export quiz to LMS formats                $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)                                                                $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)  $(GREEN)Code Quality:$(NC)                                                 $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)    make lint         Run linter (ruff)                         $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)    make format       Format code (ruff format)                 $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)    make ci           Run full CI pipeline locally              $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)                                                                $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)  $(GREEN)Setup:$(NC)                                                        $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)    make install      Install Python dependencies               $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)    make install-dev  Install development dependencies          $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)    make generate-pcap Generate PCAP sample files               $(BLUE)║$(NC)"
	@echo "$(BLUE)║$(NC)                                                                $(BLUE)║$(NC)"
	@echo "$(BLUE)╚════════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""

# ─── ENVIRONMENT MANAGEMENT ─────────────────────────────────────────────────

start:
	@echo "$(GREEN)Starting Week 7 laboratory environment...$(NC)"
	@$(PYTHON) scripts/start_lab.py
	@echo "$(GREEN)Laboratory started successfully.$(NC)"

stop:
	@echo "$(YELLOW)Stopping laboratory environment...$(NC)"
	@$(PYTHON) scripts/stop_lab.py
	@echo "$(YELLOW)Laboratory stopped.$(NC)"

restart: stop start
	@echo "$(GREEN)Laboratory restarted.$(NC)"

clean:
	@echo "$(RED)Cleaning up Docker resources...$(NC)"
	@$(PYTHON) scripts/cleanup.py --full 2>/dev/null || true
	@$(DOCKER_COMPOSE) down --volumes --remove-orphans 2>/dev/null || true
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@rm -rf artifacts/*.pcap artifacts/*.log 2>/dev/null || true
	@echo "$(GREEN)Cleanup complete.$(NC)"

verify:
	@echo "$(BLUE)Verifying environment setup...$(NC)"
	@$(PYTHON) setup/verify_environment.py

# ─── TESTING ────────────────────────────────────────────────────────────────

test:
	@echo "$(BLUE)Running all exercise tests...$(NC)"
	@$(PYTHON) tests/test_exercises.py --all

smoke:
	@echo "$(BLUE)Running smoke tests...$(NC)"
	@$(PYTHON) tests/smoke_test.py

test-1:
	@echo "$(BLUE)Testing Exercise 1: Baseline Traffic Capture...$(NC)"
	@$(PYTHON) tests/test_exercises.py --exercise 1

test-2:
	@echo "$(BLUE)Testing Exercise 2: TCP Filtering with REJECT...$(NC)"
	@$(PYTHON) tests/test_exercises.py --exercise 2

test-3:
	@echo "$(BLUE)Testing Exercise 3: UDP Filtering with DROP...$(NC)"
	@$(PYTHON) tests/test_exercises.py --exercise 3

test-4:
	@echo "$(BLUE)Testing Exercise 4: Application-Layer Filter...$(NC)"
	@$(PYTHON) tests/test_exercises.py --exercise 4

test-5:
	@echo "$(BLUE)Testing Exercise 5: Defensive Port Probing...$(NC)"
	@$(PYTHON) tests/test_exercises.py --exercise 5

# ─── PYTEST INTEGRATION ─────────────────────────────────────────────────────

pytest:
	@echo "$(BLUE)Running tests with pytest...$(NC)"
	@$(PYTHON) -m pytest tests/ -v

pytest-cov:
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	@$(PYTHON) -m pytest tests/ --cov=src --cov=scripts --cov-report=term-missing --cov-report=html

pytest-ci:
	@echo "$(BLUE)Running pytest in CI mode...$(NC)"
	@$(PYTHON) -m pytest tests/ -v --tb=short --junit-xml=test-results.xml

# ─── FORMATIVE ASSESSMENT ───────────────────────────────────────────────────

quiz:
	@echo "$(GREEN)Starting formative quiz...$(NC)"
	@$(PYTHON) formative/run_quiz.py

quiz-quick:
	@echo "$(GREEN)Starting quick quiz (5 random questions)...$(NC)"
	@$(PYTHON) formative/run_quiz.py --random --limit 5

quiz-lo1:
	@$(PYTHON) formative/run_quiz.py --lo LO1

quiz-lo2:
	@$(PYTHON) formative/run_quiz.py --lo LO2

quiz-lo3:
	@$(PYTHON) formative/run_quiz.py --lo LO3

quiz-lo4:
	@$(PYTHON) formative/run_quiz.py --lo LO4

quiz-lo5:
	@$(PYTHON) formative/run_quiz.py --lo LO5

quiz-lo6:
	@$(PYTHON) formative/run_quiz.py --lo LO6

review:
	@echo "$(BLUE)Quiz review mode (answers shown)...$(NC)"
	@$(PYTHON) formative/run_quiz.py --review

parsons:
	@echo "$(GREEN)Starting Parsons problems...$(NC)"
	@$(PYTHON) formative/parsons_runner.py

parsons-hint:
	@echo "$(GREEN)Parsons problems with hints...$(NC)"
	@$(PYTHON) formative/parsons_runner.py --hint

export-quiz:
	@echo "$(BLUE)Exporting quiz to LMS formats...$(NC)"
	@mkdir -p exports
	@$(PYTHON) formative/quiz_export.py --format all --output-dir exports/
	@echo "$(GREEN)Quiz exported to exports/ directory.$(NC)"

# ─── CODE QUALITY ───────────────────────────────────────────────────────────

lint:
	@echo "$(BLUE)Running linter (ruff)...$(NC)"
	@$(PYTHON) -m ruff check src/ scripts/ tests/ formative/ anti_ai/ --ignore E501,E402 || true
	@echo "$(GREEN)Linting complete.$(NC)"

lint-fix:
	@echo "$(BLUE)Running linter with auto-fix...$(NC)"
	@$(PYTHON) -m ruff check src/ scripts/ tests/ formative/ anti_ai/ --fix --ignore E501,E402 || true

format:
	@echo "$(BLUE)Formatting code...$(NC)"
	@$(PYTHON) -m ruff format src/ scripts/ tests/ formative/ anti_ai/ || true
	@echo "$(GREEN)Formatting complete.$(NC)"

format-check:
	@echo "$(BLUE)Checking code formatting...$(NC)"
	@$(PYTHON) -m ruff format --check src/ scripts/ tests/ formative/ anti_ai/

typecheck:
	@echo "$(BLUE)Running type checker (mypy)...$(NC)"
	@$(PYTHON) -m mypy src/ scripts/ --ignore-missing-imports || true

# ─── CI PIPELINE ────────────────────────────────────────────────────────────

ci: lint-ci syntax-check smoke pytest-ci
	@echo "$(GREEN)CI pipeline completed successfully.$(NC)"

lint-ci:
	@echo "$(BLUE)CI: Running linter...$(NC)"
	@$(PYTHON) -m ruff check src/ scripts/ tests/ formative/ anti_ai/ --output-format=github --ignore E501,E402

syntax-check:
	@echo "$(BLUE)CI: Checking Python syntax...$(NC)"
	@$(PYTHON) -m py_compile src/apps/*.py scripts/*.py tests/*.py formative/*.py
	@$(PYTHON) -m py_compile anti_ai/*.py
	@echo "$(GREEN)Syntax check passed.$(NC)"

security-check:
	@echo "$(BLUE)CI: Running security scan (bandit)...$(NC)"
	@$(PYTHON) -m bandit -r src/ scripts/ -ll || true

# ─── SETUP ──────────────────────────────────────────────────────────────────

install:
	@echo "$(BLUE)Installing Python dependencies...$(NC)"
	@$(PIP) install -r setup/requirements.txt
	@echo "$(GREEN)Dependencies installed.$(NC)"

install-dev:
	@echo "$(BLUE)Installing development dependencies...$(NC)"
	@$(PIP) install -r setup/requirements.txt
	@$(PIP) install -r setup/requirements-dev.txt
	@echo "$(GREEN)Development dependencies installed.$(NC)"

generate-pcap:
	@echo "$(BLUE)Generating PCAP sample files...$(NC)"
	@$(PYTHON) pcap/samples/generate_samples.py --output-dir pcap/samples/
	@echo "$(GREEN)PCAP samples generated.$(NC)"

verify-pcap:
	@echo "$(BLUE)Verifying PCAP samples...$(NC)"
	@$(PYTHON) pcap/samples/generate_samples.py --verify

# ─── DOCKER COMPOSE SHORTCUTS ───────────────────────────────────────────────

dc-up:
	@$(DOCKER_COMPOSE) up -d

dc-down:
	@$(DOCKER_COMPOSE) down

dc-logs:
	@$(DOCKER_COMPOSE) logs -f

dc-ps:
	@$(DOCKER_COMPOSE) ps

dc-build:
	@$(DOCKER_COMPOSE) build

dc-pull:
	@$(DOCKER_COMPOSE) pull

# ─── CAPTURE SHORTCUTS ──────────────────────────────────────────────────────

capture:
	@echo "$(BLUE)Starting packet capture (60 seconds)...$(NC)"
	@$(PYTHON) scripts/capture_traffic.py --duration 60 --output artifacts/capture_$$(date +%Y%m%d_%H%M%S).pcap

capture-tcp:
	@echo "$(BLUE)Capturing TCP traffic only...$(NC)"
	@$(PYTHON) scripts/capture_traffic.py --duration 60 --filter "tcp port 9090" --output artifacts/tcp_capture.pcap

capture-udp:
	@echo "$(BLUE)Capturing UDP traffic only...$(NC)"
	@$(PYTHON) scripts/capture_traffic.py --duration 60 --filter "udp port 9091" --output artifacts/udp_capture.pcap

# ─── DOCUMENTATION ──────────────────────────────────────────────────────────

docs-serve:
	@echo "$(BLUE)Serving documentation locally...$(NC)"
	@$(PYTHON) -m http.server 8080 --directory docs/

# ─── RELEASE ────────────────────────────────────────────────────────────────

dist: clean
	@echo "$(BLUE)Creating distribution package...$(NC)"
	@mkdir -p dist
	@zip -r dist/week7_lab_$$(date +%Y%m%d).zip \
		docker/ docs/ formative/ homework/ pcap/ scripts/ setup/ src/ tests/ \
		Makefile README.md CHANGELOG.md LICENSE VERSIONS.md pytest.ini \
		-x "*.pyc" -x "__pycache__/*" -x "*.log" -x "artifacts/*"
	@echo "$(GREEN)Package created: dist/week7_lab_$$(date +%Y%m%d).zip$(NC)"

# ============================================================================

# ─── ANTI-AI WORKFLOW ─────────────────────────────────────────────────────────

anti-ai-challenge:
	@if [ -z "$(STUDENT_ID)" ]; then echo "Set STUDENT_ID, for example: make anti-ai-challenge STUDENT_ID=123"; exit 2; fi
	@mkdir -p artifacts/anti_ai
	@$(PYTHON) -m anti_ai.challenge_generator --student-id $(STUDENT_ID) --output artifacts/anti_ai/challenge_$(STUDENT_ID).yaml

anti-ai-evidence:
	@if [ -z "$(STUDENT_ID)" ]; then echo "Set STUDENT_ID, for example: make anti-ai-evidence STUDENT_ID=123"; exit 2; fi
	@mkdir -p artifacts/anti_ai
	@$(PYTHON) -m anti_ai.evidence_collector \
		--challenge artifacts/anti_ai/challenge_$(STUDENT_ID).yaml \
		--artefact homework/hw_7_01_report.md \
		--artefact artifacts/anti_ai/week07_tokens.pcap \
		--artefact docker/configs/firewall_profiles.json \
		--probe "python3 src/apps/port_probe.py --host localhost --ports 9090,9091" \
		--output artifacts/anti_ai/evidence_$(STUDENT_ID).json

anti-ai-validate:
	@if [ -z "$(STUDENT_ID)" ]; then echo "Set STUDENT_ID, for example: make anti-ai-validate STUDENT_ID=123"; exit 2; fi
	@$(PYTHON) -m anti_ai.submission_validator \
		--challenge artifacts/anti_ai/challenge_$(STUDENT_ID).yaml \
		--evidence artifacts/anti_ai/evidence_$(STUDENT_ID).json \
		--base-dir . \
		--verbose
