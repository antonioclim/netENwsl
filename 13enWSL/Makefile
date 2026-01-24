# ══════════════════════════════════════════════════════════════════════════════
# Week 13: IoT and Security — Laboratory Makefile
# Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim
# ══════════════════════════════════════════════════════════════════════════════
#
# Usage:
#   make help     - Show all available targets
#   make start    - Start laboratory environment
#   make quiz     - Run formative assessment quiz
#   make test     - Run all tests
#
# ══════════════════════════════════════════════════════════════════════════════

.PHONY: help start stop restart quiz quiz-random test smoke lint verify clean all

# Configuration
PYTHON := python3
COMPOSE := docker compose -f docker/docker-compose.yml
QUIZ_FILE := formative/quiz.yaml

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[0;33m
CYAN := \033[0;36m
RESET := \033[0m

# ══════════════════════════════════════════════════════════════════════════════
# DEFAULT TARGET
# ══════════════════════════════════════════════════════════════════════════════

help:
	@echo ""
	@echo "$(CYAN)╔══════════════════════════════════════════════════════════════════╗$(RESET)"
	@echo "$(CYAN)║         Week 13: IoT and Security Laboratory                     ║$(RESET)"
	@echo "$(CYAN)║         Computer Networks — ASE, CSIE                            ║$(RESET)"
	@echo "$(CYAN)╠══════════════════════════════════════════════════════════════════╣$(RESET)"
	@echo "$(CYAN)║  ENVIRONMENT                                                     ║$(RESET)"
	@echo "$(CYAN)║    make start      - Start laboratory containers                 ║$(RESET)"
	@echo "$(CYAN)║    make stop       - Stop laboratory containers                  ║$(RESET)"
	@echo "$(CYAN)║    make restart    - Restart laboratory environment              ║$(RESET)"
	@echo "$(CYAN)║    make status     - Show container status                       ║$(RESET)"
	@echo "$(CYAN)║                                                                  ║$(RESET)"
	@echo "$(CYAN)║  ASSESSMENT                                                      ║$(RESET)"
	@echo "$(CYAN)║    make quiz       - Run full formative quiz (10 questions)      ║$(RESET)"
	@echo "$(CYAN)║    make quiz-random- Run random 5 questions                      ║$(RESET)"
	@echo "$(CYAN)║    make quiz-bloom - Run quiz filtered by Bloom level            ║$(RESET)"
	@echo "$(CYAN)║                                                                  ║$(RESET)"
	@echo "$(CYAN)║  TESTING                                                         ║$(RESET)"
	@echo "$(CYAN)║    make test       - Run all tests                               ║$(RESET)"
	@echo "$(CYAN)║    make smoke      - Run smoke tests only                        ║$(RESET)"
	@echo "$(CYAN)║    make lint       - Check code syntax                           ║$(RESET)"
	@echo "$(CYAN)║    make verify     - Verify environment setup                    ║$(RESET)"
	@echo "$(CYAN)║                                                                  ║$(RESET)"
	@echo "$(CYAN)║  MAINTENANCE                                                     ║$(RESET)"
	@echo "$(CYAN)║    make clean      - Clean artifacts and caches                  ║$(RESET)"
	@echo "$(CYAN)║    make clean-full - Full cleanup including Docker               ║$(RESET)"
	@echo "$(CYAN)║    make all        - Full cycle: lint → test → quiz              ║$(RESET)"
	@echo "$(CYAN)╚══════════════════════════════════════════════════════════════════╝$(RESET)"
	@echo ""

# ══════════════════════════════════════════════════════════════════════════════
# ENVIRONMENT MANAGEMENT
# ══════════════════════════════════════════════════════════════════════════════

start:
	@echo "$(GREEN)🚀 Starting Week 13 laboratory environment...$(RESET)"
	@$(PYTHON) scripts/start_lab.py
	@echo "$(GREEN)✅ Laboratory started. Access:$(RESET)"
	@echo "   - Portainer: http://localhost:9000"
	@echo "   - DVWA:      http://localhost:8080"
	@echo "   - MQTT:      localhost:1883 (plain) / 8883 (TLS)"

stop:
	@echo "$(YELLOW)🛑 Stopping Week 13 laboratory...$(RESET)"
	@$(PYTHON) scripts/stop_lab.py
	@echo "$(GREEN)✅ Laboratory stopped.$(RESET)"

restart: stop start
	@echo "$(GREEN)✅ Laboratory restarted.$(RESET)"

status:
	@echo "$(CYAN)📊 Container Status:$(RESET)"
	@docker ps --filter "name=week13" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

logs:
	@echo "$(CYAN)📋 Recent logs (all containers):$(RESET)"
	@docker logs week13_mosquitto --tail 10 2>/dev/null || echo "  mosquitto: not running"
	@docker logs week13_dvwa --tail 10 2>/dev/null || echo "  dvwa: not running"
	@docker logs week13_vsftpd --tail 10 2>/dev/null || echo "  vsftpd: not running"

# ══════════════════════════════════════════════════════════════════════════════
# FORMATIVE ASSESSMENT
# ══════════════════════════════════════════════════════════════════════════════

quiz:
	@echo "$(GREEN)📝 Starting formative quiz...$(RESET)"
	@$(PYTHON) formative/run_quiz.py

quiz-random:
	@echo "$(GREEN)📝 Starting random quiz (5 questions)...$(RESET)"
	@$(PYTHON) formative/run_quiz.py --random --limit 5

quiz-bloom:
	@echo "$(CYAN)Available Bloom levels: remember, understand, apply, analyze, evaluate, create$(RESET)"
	@read -p "Enter Bloom level: " level; \
	$(PYTHON) formative/run_quiz.py --bloom $$level

quiz-export:
	@echo "$(GREEN)📝 Running quiz with export...$(RESET)"
	@$(PYTHON) formative/run_quiz.py --export artifacts/quiz_results.json
	@echo "$(GREEN)✅ Results exported to artifacts/quiz_results.json$(RESET)"

# ══════════════════════════════════════════════════════════════════════════════
# TESTING
# ══════════════════════════════════════════════════════════════════════════════

test: lint smoke
	@echo "$(GREEN)🧪 Running exercise tests...$(RESET)"
	@$(PYTHON) tests/test_exercises.py --all || true
	@echo "$(GREEN)✅ Tests completed.$(RESET)"

smoke:
	@echo "$(CYAN)💨 Running smoke tests...$(RESET)"
	@$(PYTHON) tests/smoke_test.py

lint:
	@echo "$(CYAN)🔍 Checking Python syntax...$(RESET)"
	@$(PYTHON) -m py_compile src/exercises/*.py && echo "  ✅ src/exercises/ OK"
	@$(PYTHON) -m py_compile scripts/*.py && echo "  ✅ scripts/ OK"
	@$(PYTHON) -m py_compile tests/*.py && echo "  ✅ tests/ OK"
	@$(PYTHON) -m py_compile formative/*.py 2>/dev/null && echo "  ✅ formative/ OK" || true
	@echo "$(GREEN)✅ Syntax check passed.$(RESET)"

verify:
	@echo "$(CYAN)🔧 Verifying environment...$(RESET)"
	@$(PYTHON) setup/verify_environment.py

# ══════════════════════════════════════════════════════════════════════════════
# EXERCISES (shortcuts)
# ══════════════════════════════════════════════════════════════════════════════

ex1:
	@echo "$(CYAN)Running Exercise 1: Port Scanner$(RESET)"
	@$(PYTHON) src/exercises/ex_13_01_port_scanner.py --help

ex2:
	@echo "$(CYAN)Running Exercise 2: MQTT Client$(RESET)"
	@$(PYTHON) src/exercises/ex_13_02_mqtt_client.py --help

ex3:
	@echo "$(CYAN)Running Exercise 3: Packet Sniffer$(RESET)"
	@$(PYTHON) src/exercises/ex_13_03_packet_sniffer.py --help

ex4:
	@echo "$(CYAN)Running Exercise 4: Vulnerability Checker$(RESET)"
	@$(PYTHON) src/exercises/ex_13_04_vuln_checker.py --help

# ══════════════════════════════════════════════════════════════════════════════
# MAINTENANCE
# ══════════════════════════════════════════════════════════════════════════════

clean:
	@echo "$(YELLOW)🧹 Cleaning artifacts and caches...$(RESET)"
	@rm -rf artifacts/*.pcap artifacts/*.log artifacts/*.json 2>/dev/null || true
	@rm -rf __pycache__ */__pycache__ */*/__pycache__ 2>/dev/null || true
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@find . -name ".pytest_cache" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✅ Cleanup complete.$(RESET)"

clean-full: clean
	@echo "$(YELLOW)🧹 Full cleanup including Docker resources...$(RESET)"
	@$(PYTHON) scripts/cleanup.py --full 2>/dev/null || true
	@echo "$(GREEN)✅ Full cleanup complete.$(RESET)"

# ══════════════════════════════════════════════════════════════════════════════
# COMBINED WORKFLOWS
# ══════════════════════════════════════════════════════════════════════════════

all: lint smoke test quiz
	@echo ""
	@echo "$(GREEN)════════════════════════════════════════════════════════════════$(RESET)"
	@echo "$(GREEN)  ✅ All checks completed successfully!$(RESET)"
	@echo "$(GREEN)════════════════════════════════════════════════════════════════$(RESET)"

# Pre-lab check (run before starting a lab session)
prelab: verify lint
	@echo "$(GREEN)✅ Pre-lab checks passed. Ready to start!$(RESET)"
	@echo "$(CYAN)Run 'make start' to begin the laboratory.$(RESET)"

# Post-lab cleanup
postlab: stop clean
	@echo "$(GREEN)✅ Post-lab cleanup complete.$(RESET)"

# ══════════════════════════════════════════════════════════════════════════════
# DOCUMENTATION
# ══════════════════════════════════════════════════════════════════════════════

docs:
	@echo "$(CYAN)📚 Available documentation:$(RESET)"
	@echo "   README.md              - Main laboratory guide"
	@echo "   SECURITY.md            - Security notice and guidelines"
	@echo "   docs/theory_summary.md - Theoretical background"
	@echo "   docs/troubleshooting.md- Problem solving guide"
	@echo "   docs/misconceptions.md - Common errors"
	@echo "   docs/peer_instruction.md - Discussion questions"

# Show security notice
security:
	@cat SECURITY.md | head -50
	@echo ""
	@echo "$(YELLOW)... (see SECURITY.md for full document)$(RESET)"
