# ═══════════════════════════════════════════════════════════════════════════════
# Makefile — Week 14 Lab Kit Orchestrator
# ═══════════════════════════════════════════════════════════════════════════════
# NETWORKING class — ASE, CSIE | Computer Networks Laboratory
# by ing. dr. Antonio Clim
#
# Usage: make <target>
# Run `make help` to see all available targets
# ═══════════════════════════════════════════════════════════════════════════════

.PHONY: help install lint test quiz docker-up docker-down docker-logs \
        validate clean smoke capture verify-env all ci

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

PYTHON := python3
PIP := pip3
DOCKER_COMPOSE := docker compose -f docker/docker-compose.yml
PYTEST := $(PYTHON) -m pytest
RUFF := $(PYTHON) -m ruff

# Colours for output
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
CYAN := \033[0;36m
NC := \033[0m # No Colour

# ═══════════════════════════════════════════════════════════════════════════════
# HELP
# ═══════════════════════════════════════════════════════════════════════════════

help:
	@echo ""
	@echo "$(CYAN)╔═══════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(CYAN)║$(NC)  $(GREEN)Week 14 Lab Kit — Available Commands$(NC)                        $(CYAN)║$(NC)"
	@echo "$(CYAN)╠═══════════════════════════════════════════════════════════════╣$(NC)"
	@echo "$(CYAN)║$(NC)                                                               $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)  $(YELLOW)Setup & Installation:$(NC)                                       $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make install      - Install Python dependencies            $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make verify-env   - Verify environment setup               $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)                                                               $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)  $(YELLOW)Development:$(NC)                                                $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make lint         - Run code linter (ruff)                 $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make test         - Run all unit tests                     $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make smoke        - Run smoke tests only                   $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make validate     - Validate entire kit integrity          $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)                                                               $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)  $(YELLOW)Docker Environment:$(NC)                                         $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make docker-up    - Start lab containers                   $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make docker-down  - Stop lab containers                    $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make docker-logs  - View container logs                    $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make docker-ps    - Show container status                  $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)                                                               $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)  $(YELLOW)Learning & Assessment:$(NC)                                      $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make quiz         - Run formative assessment quiz          $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make quiz-random  - Run quiz with randomized questions     $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make capture      - Capture network traffic                $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)                                                               $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)  $(YELLOW)Maintenance:$(NC)                                                $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make clean        - Clean generated artifacts              $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make ci           - Run full CI pipeline locally           $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)    make all          - Setup and start everything             $(CYAN)║$(NC)"
	@echo "$(CYAN)║$(NC)                                                               $(CYAN)║$(NC)"
	@echo "$(CYAN)╚═══════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(GREEN)NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim$(NC)"
	@echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP & INSTALLATION
# ═══════════════════════════════════════════════════════════════════════════════

install:
	@echo "$(CYAN)📦 Installing dependencies...$(NC)"
	$(PIP) install --upgrade pip
	$(PIP) install -r setup/requirements.txt
	$(PIP) install ruff pytest pytest-timeout
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

verify-env:
	@echo "$(CYAN)🔍 Verifying environment...$(NC)"
	$(PYTHON) setup/verify_environment.py

# ═══════════════════════════════════════════════════════════════════════════════
# DEVELOPMENT
# ═══════════════════════════════════════════════════════════════════════════════

lint:
	@echo "$(CYAN)🔍 Running linter...$(NC)"
	$(RUFF) check src/ scripts/ tests/ formative/ || true
	@echo "$(GREEN)✓ Linting complete$(NC)"

lint-fix:
	@echo "$(CYAN)🔧 Auto-fixing lint issues...$(NC)"
	$(RUFF) check --fix src/ scripts/ tests/ formative/
	$(RUFF) format src/ scripts/ tests/ formative/
	@echo "$(GREEN)✓ Lint fixes applied$(NC)"

test:
	@echo "$(CYAN)🧪 Running all tests...$(NC)"
	$(PYTEST) tests/ -v --tb=short --timeout=60
	@echo "$(GREEN)✓ Tests complete$(NC)"

smoke:
	@echo "$(CYAN)🚬 Running smoke tests...$(NC)"
	$(PYTHON) tests/smoke_test.py
	@echo "$(GREEN)✓ Smoke tests complete$(NC)"

validate:
	@echo "$(CYAN)✅ Validating kit integrity...$(NC)"
	@# Validate YAML quiz
	$(PYTHON) -c "import yaml; yaml.safe_load(open('formative/quiz_week14.yaml'))" && \
		echo "  $(GREEN)✓ YAML quiz valid$(NC)"
	@# Validate JSON quiz
	$(PYTHON) -c "import json; json.load(open('formative/quiz_week14.json'))" && \
		echo "  $(GREEN)✓ JSON quiz valid$(NC)"
	@# Validate Python syntax
	$(PYTHON) -m py_compile formative/run_quiz.py && \
		echo "  $(GREEN)✓ Quiz runner valid$(NC)"
	@# Check required files
	@test -f README.md && echo "  $(GREEN)✓ README.md exists$(NC)"
	@test -f CHANGELOG.md && echo "  $(GREEN)✓ CHANGELOG.md exists$(NC)"
	@test -f SECURITY.md && echo "  $(GREEN)✓ SECURITY.md exists$(NC)"
	@test -f docs/learning_objectives.md && echo "  $(GREEN)✓ LO matrix exists$(NC)"
	@echo "$(GREEN)✓ Kit validation complete$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# DOCKER ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════

docker-up:
	@echo "$(CYAN)🚀 Starting lab environment...$(NC)"
	$(DOCKER_COMPOSE) up -d
	@echo "$(YELLOW)⏳ Waiting for services to initialize...$(NC)"
	@sleep 10
	$(DOCKER_COMPOSE) ps
	@echo ""
	@echo "$(GREEN)✓ Lab environment ready$(NC)"
	@echo ""
	@echo "$(CYAN)Access points:$(NC)"
	@echo "  Load Balancer: http://localhost:8080"
	@echo "  Backend 1:     http://localhost:8001"
	@echo "  Backend 2:     http://localhost:8002"
	@echo "  TCP Echo:      localhost:9090"
	@echo "  Portainer:     http://localhost:9000"
	@echo ""

docker-down:
	@echo "$(CYAN)🛑 Stopping lab environment...$(NC)"
	$(DOCKER_COMPOSE) down
	@echo "$(GREEN)✓ Lab environment stopped$(NC)"

docker-logs:
	@echo "$(CYAN)📋 Container logs (Ctrl+C to exit)...$(NC)"
	$(DOCKER_COMPOSE) logs -f

docker-ps:
	@echo "$(CYAN)📊 Container status:$(NC)"
	$(DOCKER_COMPOSE) ps

docker-restart:
	@echo "$(CYAN)🔄 Restarting lab environment...$(NC)"
	$(DOCKER_COMPOSE) restart
	@echo "$(GREEN)✓ Containers restarted$(NC)"

docker-rebuild:
	@echo "$(CYAN)🔨 Rebuilding Docker images...$(NC)"
	$(DOCKER_COMPOSE) build --no-cache
	@echo "$(GREEN)✓ Images rebuilt$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# LEARNING & ASSESSMENT
# ═══════════════════════════════════════════════════════════════════════════════

quiz:
	@echo "$(CYAN)📝 Starting formative assessment quiz...$(NC)"
	@echo ""
	$(PYTHON) formative/run_quiz.py

quiz-random:
	@echo "$(CYAN)📝 Starting quiz (randomized)...$(NC)"
	@echo ""
	$(PYTHON) formative/run_quiz.py --random

quiz-quick:
	@echo "$(CYAN)📝 Starting quick quiz (5 questions)...$(NC)"
	@echo ""
	$(PYTHON) formative/run_quiz.py --random --limit 5 --no-prediction

quiz-export:
	@echo "$(CYAN)📤 Exporting quiz to JSON...$(NC)"
	$(PYTHON) formative/run_quiz.py --export json --output quiz_export.json
	@echo "$(GREEN)✓ Quiz exported to quiz_export.json$(NC)"

capture:
	@echo "$(CYAN)📡 Starting traffic capture...$(NC)"
	$(PYTHON) scripts/capture_traffic.py

demo:
	@echo "$(CYAN)🎬 Running demonstration...$(NC)"
	$(PYTHON) scripts/run_demo.py

# ═══════════════════════════════════════════════════════════════════════════════
# MAINTENANCE
# ═══════════════════════════════════════════════════════════════════════════════

clean:
	@echo "$(CYAN)🧹 Cleaning artifacts...$(NC)"
	rm -rf artifacts/*.pcap artifacts/*.log 2>/dev/null || true
	rm -rf __pycache__ */__pycache__ */*/__pycache__ 2>/dev/null || true
	rm -rf .pytest_cache .ruff_cache 2>/dev/null || true
	rm -rf *.pyc */*.pyc */*/*.pyc 2>/dev/null || true
	rm -rf .coverage coverage.xml htmlcov/ 2>/dev/null || true
	@echo "$(GREEN)✓ Artifacts cleaned$(NC)"

clean-docker:
	@echo "$(CYAN)🧹 Cleaning Docker resources...$(NC)"
	$(DOCKER_COMPOSE) down --volumes --remove-orphans
	docker image prune -f
	@echo "$(GREEN)✓ Docker resources cleaned$(NC)"

clean-all: clean clean-docker
	@echo "$(GREEN)✓ Full cleanup complete$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# CI PIPELINE (LOCAL)
# ═══════════════════════════════════════════════════════════════════════════════

ci: lint test validate
	@echo ""
	@echo "$(GREEN)═══════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)✓ Local CI pipeline complete$(NC)"
	@echo "$(GREEN)═══════════════════════════════════════════════════════$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# FULL SETUP
# ═══════════════════════════════════════════════════════════════════════════════

all: install verify-env docker-up smoke
	@echo ""
	@echo "$(GREEN)═══════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)✓ Lab environment ready!$(NC)"
	@echo "$(GREEN)═══════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(CYAN)Next steps:$(NC)"
	@echo "  1. Run 'make quiz' to test your knowledge"
	@echo "  2. Open http://localhost:8080 in your browser"
	@echo "  3. Start Wireshark and capture traffic"
	@echo ""
