# ═══════════════════════════════════════════════════════════════════════════════
# Makefile — Week 9: Session Layer and Presentation Layer
# NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim
# ═══════════════════════════════════════════════════════════════════════════════
#
# Usage:
#   make help          Show available targets
#   make setup         Install dependencies and verify environment
#   make start         Start laboratory Docker environment
#   make stop          Stop laboratory environment
#   make test          Run all tests
#   make quiz          Run formative quiz
#   make lint          Run code linter
#   make clean         Clean generated artifacts
#
# ═══════════════════════════════════════════════════════════════════════════════

# Configuration
PYTHON := python3
PIP := pip3
DOCKER_COMPOSE := docker compose -f docker/docker-compose.yml
QUIZ_FILE := formative/quiz.yaml

# Colours for terminal output
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m  # No Colour

.PHONY: help setup start stop status test smoke quiz lint clean verify demo \
        docker-up docker-down docker-logs docker-shell capture all

# ═══════════════════════════════════════════════════════════════════════════════
# DEFAULT TARGET
# ═══════════════════════════════════════════════════════════════════════════════

help:
	@echo ""
	@echo "═══════════════════════════════════════════════════════════════════════"
	@echo "  Week 9 Laboratory — Session Layer and Presentation Layer"
	@echo "═══════════════════════════════════════════════════════════════════════"
	@echo ""
	@echo "  $(GREEN)Setup & Environment:$(NC)"
	@echo "    make setup        Install dependencies and verify environment"
	@echo "    make verify       Verify environment only (no install)"
	@echo ""
	@echo "  $(GREEN)Docker Environment:$(NC)"
	@echo "    make start        Start all Docker containers"
	@echo "    make stop         Stop all Docker containers"
	@echo "    make status       Show container status"
	@echo "    make docker-logs  View container logs"
	@echo "    make docker-shell Shell into FTP server container"
	@echo ""
	@echo "  $(GREEN)Testing:$(NC)"
	@echo "    make test         Run all tests (smoke + exercises)"
	@echo "    make smoke        Run smoke tests only"
	@echo "    make lint         Run code linter (ruff)"
	@echo ""
	@echo "  $(GREEN)Learning:$(NC)"
	@echo "    make quiz         Run formative quiz"
	@echo "    make quiz-stats   Show quiz statistics"
	@echo "    make demo         Run endianness demonstration"
	@echo ""
	@echo "  $(GREEN)Utilities:$(NC)"
	@echo "    make capture      Start packet capture (60 seconds)"
	@echo "    make clean        Remove generated artifacts"
	@echo "    make all          Setup + start + test"
	@echo ""
	@echo "═══════════════════════════════════════════════════════════════════════"

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP & VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════

setup: verify-python
	@echo "$(GREEN)Installing Python dependencies...$(NC)"
	$(PIP) install -r setup/requirements.txt --quiet
	@echo "$(GREEN)Verifying environment...$(NC)"
	$(PYTHON) setup/verify_environment.py
	@echo "$(GREEN)✓ Setup complete$(NC)"

verify: verify-python
	@echo "$(GREEN)Verifying environment...$(NC)"
	$(PYTHON) setup/verify_environment.py

verify-python:
	@echo "$(GREEN)Checking Python version...$(NC)"
	@$(PYTHON) -c "import sys; assert sys.version_info >= (3, 10), \
		'Python 3.10+ required, found ' + sys.version" || \
		(echo "$(RED)Error: Python 3.10+ required$(NC)" && exit 1)
	@echo "  Python: $$($(PYTHON) --version)"

# ═══════════════════════════════════════════════════════════════════════════════
# DOCKER ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════

start: docker-up
	@echo "$(GREEN)✓ Laboratory environment started$(NC)"
	@echo "  FTP Server: localhost:2121 (test/12345)"
	@echo "  Portainer:  http://localhost:9000"

stop: docker-down
	@echo "$(GREEN)✓ Laboratory environment stopped$(NC)"

status:
	@echo "$(GREEN)Container status:$(NC)"
	@docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "s9_|NAMES"

docker-up:
	@echo "$(GREEN)Starting Docker containers...$(NC)"
	$(DOCKER_COMPOSE) up -d
	@echo "Waiting for services to be healthy..."
	@sleep 5
	$(DOCKER_COMPOSE) ps

docker-down:
	@echo "$(GREEN)Stopping Docker containers...$(NC)"
	$(DOCKER_COMPOSE) down

docker-logs:
	$(DOCKER_COMPOSE) logs -f

docker-shell:
	@echo "$(GREEN)Opening shell in FTP server container...$(NC)"
	docker exec -it s9_ftp_server /bin/bash

# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

test: smoke test-exercises
	@echo "$(GREEN)✓ All tests passed$(NC)"

smoke:
	@echo "$(GREEN)Running smoke tests...$(NC)"
	$(PYTHON) tests/smoke_test.py

test-exercises:
	@echo "$(GREEN)Running exercise tests...$(NC)"
	$(PYTHON) tests/test_exercises.py

lint:
	@echo "$(GREEN)Running linter...$(NC)"
	@$(PYTHON) -m ruff check src/ scripts/ tests/ --ignore E501 2>/dev/null || \
		$(PYTHON) -m py_compile src/exercises/*.py scripts/*.py tests/*.py
	@echo "$(GREEN)✓ Lint check complete$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# LEARNING
# ═══════════════════════════════════════════════════════════════════════════════

quiz:
	@echo "$(GREEN)Starting formative quiz...$(NC)"
	$(PYTHON) formative/run_quiz.py

quiz-random:
	$(PYTHON) formative/run_quiz.py --random --limit 5

quiz-stats:
	$(PYTHON) formative/run_quiz.py --stats

demo:
	@echo "$(GREEN)Running endianness demonstration...$(NC)"
	$(PYTHON) src/exercises/ex_9_01_demonstrate_endianness.py --demo --selftest

demo-ftp:
	@echo "$(GREEN)Running FTP session demonstration...$(NC)"
	$(PYTHON) scripts/run_demo.py --demo ftp_session

demo-multi:
	@echo "$(GREEN)Running multi-client demonstration...$(NC)"
	$(PYTHON) scripts/run_demo.py --demo multi_client

# ═══════════════════════════════════════════════════════════════════════════════
# UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════

capture:
	@echo "$(GREEN)Starting packet capture (60 seconds)...$(NC)"
	@mkdir -p pcap
	$(PYTHON) scripts/capture_traffic.py --duration 60 --output pcap/week9_capture.pcap

clean:
	@echo "$(GREEN)Cleaning artifacts...$(NC)"
	rm -rf artifacts/*.pcap artifacts/*.log
	rm -rf pcap/*.pcap
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "$(GREEN)✓ Clean complete$(NC)"

clean-docker: docker-down
	@echo "$(GREEN)Removing Docker volumes...$(NC)"
	$(DOCKER_COMPOSE) down -v
	docker network prune -f
	@echo "$(GREEN)✓ Docker cleanup complete$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# COMBINED TARGETS
# ═══════════════════════════════════════════════════════════════════════════════

all: setup start test
	@echo ""
	@echo "$(GREEN)═══════════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  ✓ Week 9 Laboratory Ready$(NC)"
	@echo "$(GREEN)═══════════════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "  Next steps:"
	@echo "    1. Run 'make quiz' to test your knowledge"
	@echo "    2. Open Wireshark and capture on vEthernet (WSL)"
	@echo "    3. Start Exercise 1: make demo"
	@echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# CI TARGETS (for automated testing)
# ═══════════════════════════════════════════════════════════════════════════════

ci-lint:
	$(PYTHON) -m py_compile src/exercises/*.py scripts/*.py tests/*.py setup/*.py
	@echo "$(GREEN)✓ Syntax check passed$(NC)"

ci-test: ci-lint smoke
	@echo "$(GREEN)✓ CI tests passed$(NC)"

# ═══════════════════════════════════════════════════════════════════════════════
# END OF MAKEFILE
# ═══════════════════════════════════════════════════════════════════════════════
