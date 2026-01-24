# ══════════════════════════════════════════════════════════════════════════════
# Week 13: IoT and Security — Makefile
# Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim
# ══════════════════════════════════════════════════════════════════════════════
#
# This Makefile provides convenient shortcuts for common laboratory tasks.
#
# Quick reference:
#   make help        - Show all available commands
#   make start       - Start laboratory environment
#   make stop        - Stop laboratory environment
#   make quiz        - Run formative assessment quiz
#   make test        - Run all tests
#
# ══════════════════════════════════════════════════════════════════════════════

.PHONY: help start stop restart status logs clean clean-full \
        quiz quiz-random quiz-bloom quiz-export \
        test smoke lint verify validate \
        ex1 ex2 ex3 ex4 prelab postlab all

# Default target
.DEFAULT_GOAL := help

# Colours for terminal output
CYAN := \033[96m
GREEN := \033[92m
YELLOW := \033[93m
RED := \033[91m
RESET := \033[0m
BOLD := \033[1m

# ══════════════════════════════════════════════════════════════════════════════
# HELP
# ══════════════════════════════════════════════════════════════════════════════

help:
	@echo ""
	@echo "$(CYAN)══════════════════════════════════════════════════════════════════════════════$(RESET)"
	@echo "$(BOLD)  Week 13: IoT and Security — Laboratory Commands$(RESET)"
	@echo "$(CYAN)══════════════════════════════════════════════════════════════════════════════$(RESET)"
	@echo ""
	@echo "$(BOLD)Environment Management:$(RESET)"
	@echo "  $(GREEN)make start$(RESET)         Start laboratory Docker containers"
	@echo "  $(GREEN)make stop$(RESET)          Stop laboratory containers (Portainer stays)"
	@echo "  $(GREEN)make restart$(RESET)       Restart laboratory containers"
	@echo "  $(GREEN)make status$(RESET)        Show container status"
	@echo "  $(GREEN)make logs$(RESET)          View container logs"
	@echo ""
	@echo "$(BOLD)Formative Assessment:$(RESET)"
	@echo "  $(GREEN)make quiz$(RESET)          Run full quiz (16 questions)"
	@echo "  $(GREEN)make quiz-random$(RESET)   Run 5 random questions"
	@echo "  $(GREEN)make quiz-bloom$(RESET)    Run quiz filtered by Bloom level"
	@echo "  $(GREEN)make quiz-export$(RESET)   Export quiz to Moodle XML format"
	@echo ""
	@echo "$(BOLD)Testing and Validation:$(RESET)"
	@echo "  $(GREEN)make test$(RESET)          Run all tests"
	@echo "  $(GREEN)make smoke$(RESET)         Run quick smoke tests"
	@echo "  $(GREEN)make lint$(RESET)          Run code linter (ruff)"
	@echo "  $(GREEN)make verify$(RESET)        Verify environment setup"
	@echo "  $(GREEN)make validate$(RESET)      Validate ground truth"
	@echo ""
	@echo "$(BOLD)Exercise Shortcuts:$(RESET)"
	@echo "  $(GREEN)make ex1$(RESET)           Run Exercise 1 (Port Scanner)"
	@echo "  $(GREEN)make ex2$(RESET)           Run Exercise 2 (MQTT Client)"
	@echo "  $(GREEN)make ex3$(RESET)           Run Exercise 3 (Packet Sniffer)"
	@echo "  $(GREEN)make ex4$(RESET)           Run Exercise 4 (Vulnerability Checker)"
	@echo ""
	@echo "$(BOLD)Cleanup:$(RESET)"
	@echo "  $(GREEN)make clean$(RESET)         Remove temporary files"
	@echo "  $(GREEN)make clean-full$(RESET)    Remove containers, networks and volumes"
	@echo ""
	@echo "$(BOLD)Workflows:$(RESET)"
	@echo "  $(GREEN)make prelab$(RESET)        Pre-laboratory preparation"
	@echo "  $(GREEN)make postlab$(RESET)       Post-laboratory cleanup and export"
	@echo "  $(GREEN)make all$(RESET)           Full verification suite"
	@echo ""
	@echo "$(CYAN)══════════════════════════════════════════════════════════════════════════════$(RESET)"
	@echo ""

# ══════════════════════════════════════════════════════════════════════════════
# ENVIRONMENT MANAGEMENT
# ══════════════════════════════════════════════════════════════════════════════

start:
	@echo "$(CYAN)[*] Starting Week 13 laboratory environment...$(RESET)"
	@python3 scripts/start_lab.py
	@echo "$(GREEN)[✓] Laboratory started$(RESET)"

stop:
	@echo "$(CYAN)[*] Stopping Week 13 laboratory containers...$(RESET)"
	@docker compose -f docker/docker-compose.yml down 2>/dev/null || true
	@echo "$(GREEN)[✓] Laboratory stopped (Portainer remains running)$(RESET)"

restart: stop start
	@echo "$(GREEN)[✓] Laboratory restarted$(RESET)"

status:
	@echo "$(CYAN)[*] Container Status:$(RESET)"
	@docker ps --filter "name=week13" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
	@echo ""
	@echo "$(CYAN)[*] Network Info:$(RESET)"
	@docker network inspect week13net --format '{{range .Containers}}{{.Name}}: {{.IPv4Address}}{{"\n"}}{{end}}' 2>/dev/null || echo "Network not found"

logs:
	@echo "$(CYAN)[*] Recent logs from all Week 13 containers:$(RESET)"
	@echo ""
	@echo "$(BOLD)--- Mosquitto MQTT ---$(RESET)"
	@docker logs --tail 20 week13_mosquitto 2>/dev/null || echo "Container not running"
	@echo ""
	@echo "$(BOLD)--- DVWA ---$(RESET)"
	@docker logs --tail 20 week13_dvwa 2>/dev/null || echo "Container not running"
	@echo ""
	@echo "$(BOLD)--- vsftpd ---$(RESET)"
	@docker logs --tail 20 week13_vsftpd 2>/dev/null || echo "Container not running"

# ══════════════════════════════════════════════════════════════════════════════
# FORMATIVE ASSESSMENT
# ══════════════════════════════════════════════════════════════════════════════

quiz:
	@echo "$(CYAN)[*] Starting formative assessment quiz...$(RESET)"
	@python3 formative/run_quiz.py

quiz-random:
	@echo "$(CYAN)[*] Starting random quiz (5 questions)...$(RESET)"
	@python3 formative/run_quiz.py --random --limit 5

quiz-bloom:
	@echo "$(CYAN)[*] Quiz filtered by Bloom level$(RESET)"
	@echo "Usage: python3 formative/run_quiz.py --bloom [remember|understand|apply|analyse|evaluate|create]"
	@echo ""
	@echo "Example: python3 formative/run_quiz.py --bloom apply"

quiz-export:
	@echo "$(CYAN)[*] Exporting quiz to Moodle XML format...$(RESET)"
	@python3 formative/run_quiz.py --export-moodle artifacts/quiz_moodle_export.xml
	@echo "$(GREEN)[✓] Exported to artifacts/quiz_moodle_export.xml$(RESET)"

# ══════════════════════════════════════════════════════════════════════════════
# TESTING AND VALIDATION
# ══════════════════════════════════════════════════════════════════════════════

test:
	@echo "$(CYAN)[*] Running all tests...$(RESET)"
	@python3 -m pytest tests/ -v --tb=short || python3 tests/test_exercises.py

smoke:
	@echo "$(CYAN)[*] Running smoke tests...$(RESET)"
	@python3 tests/smoke_test.py

lint:
	@echo "$(CYAN)[*] Running code linter (ruff)...$(RESET)"
	@ruff check src/ scripts/ tests/ formative/ --output-format=concise 2>/dev/null || \
		echo "$(YELLOW)[!] Install ruff: pip install ruff$(RESET)"

lint-fix:
	@echo "$(CYAN)[*] Running linter with auto-fix...$(RESET)"
	@ruff check src/ scripts/ tests/ formative/ --fix 2>/dev/null || \
		echo "$(YELLOW)[!] Install ruff: pip install ruff$(RESET)"

verify:
	@echo "$(CYAN)[*] Verifying environment setup...$(RESET)"
	@python3 setup/verify_environment.py

validate:
	@echo "$(CYAN)[*] Validating ground truth...$(RESET)"
	@python3 tests/validate_ground_truth.py

type-check:
	@echo "$(CYAN)[*] Running type checker (mypy)...$(RESET)"
	@mypy src/ --ignore-missing-imports 2>/dev/null || \
		echo "$(YELLOW)[!] Install mypy: pip install mypy$(RESET)"

# ══════════════════════════════════════════════════════════════════════════════
# EXERCISE SHORTCUTS
# ══════════════════════════════════════════════════════════════════════════════

ex1:
	@echo "$(CYAN)[*] Exercise 1: Port Scanner$(RESET)"
	@echo "$(YELLOW)Usage:$(RESET) python3 src/exercises/ex_13_01_port_scanner.py --target <IP> --ports <PORTS>"
	@echo ""
	@echo "$(BOLD)Example commands:$(RESET)"
	@echo "  python3 src/exercises/ex_13_01_port_scanner.py --target 127.0.0.1 --ports 1-1024"
	@echo "  python3 src/exercises/ex_13_01_port_scanner.py --target 10.0.13.11 --ports 22,80,443,8080"
	@echo ""
	@python3 src/exercises/ex_13_01_port_scanner.py --help

ex2:
	@echo "$(CYAN)[*] Exercise 2: MQTT Client$(RESET)"
	@echo "$(YELLOW)Usage:$(RESET) python3 src/exercises/ex_13_02_mqtt_client.py --mode <publish|subscribe> --topic <TOPIC>"
	@echo ""
	@echo "$(BOLD)Example commands:$(RESET)"
	@echo "  python3 src/exercises/ex_13_02_mqtt_client.py --mode subscribe --topic '#'"
	@echo "  python3 src/exercises/ex_13_02_mqtt_client.py --mode publish --topic sensors/temp --message '23.5'"
	@echo ""
	@python3 src/exercises/ex_13_02_mqtt_client.py --help

ex3:
	@echo "$(CYAN)[*] Exercise 3: Packet Sniffer$(RESET)"
	@echo "$(YELLOW)Usage:$(RESET) sudo python3 src/exercises/ex_13_03_packet_sniffer.py --filter <BPF>"
	@echo ""
	@echo "$(BOLD)Example commands:$(RESET)"
	@echo "  sudo python3 src/exercises/ex_13_03_packet_sniffer.py --filter 'tcp port 1883' --count 20"
	@echo "  sudo python3 src/exercises/ex_13_03_packet_sniffer.py --filter 'tcp port 8080' --output capture.pcap"
	@echo ""
	@python3 src/exercises/ex_13_03_packet_sniffer.py --help

ex4:
	@echo "$(CYAN)[*] Exercise 4: Vulnerability Checker$(RESET)"
	@echo "$(YELLOW)Usage:$(RESET) python3 src/exercises/ex_13_04_vuln_checker.py --target <IP> --port <PORT> --service <TYPE>"
	@echo ""
	@echo "$(BOLD)Example commands:$(RESET)"
	@echo "  python3 src/exercises/ex_13_04_vuln_checker.py --target 10.0.13.11 --port 8080 --service http"
	@echo "  python3 src/exercises/ex_13_04_vuln_checker.py --target 10.0.13.12 --port 2121 --service ftp"
	@echo ""
	@python3 src/exercises/ex_13_04_vuln_checker.py --help

# ══════════════════════════════════════════════════════════════════════════════
# CLEANUP
# ══════════════════════════════════════════════════════════════════════════════

clean:
	@echo "$(CYAN)[*] Cleaning temporary files...$(RESET)"
	@rm -rf __pycache__ */__pycache__ */*/__pycache__
	@rm -rf .pytest_cache .mypy_cache .ruff_cache
	@rm -rf artifacts/*.json artifacts/*.xml artifacts/*.log 2>/dev/null || true
	@rm -rf pcap/*.pcap 2>/dev/null || true
	@echo "$(GREEN)[✓] Temporary files removed$(RESET)"

clean-full: clean
	@echo "$(CYAN)[*] Full cleanup: removing containers, networks and volumes...$(RESET)"
	@docker compose -f docker/docker-compose.yml down -v 2>/dev/null || true
	@docker network rm week13net 2>/dev/null || true
	@echo "$(GREEN)[✓] Full cleanup complete$(RESET)"

# ══════════════════════════════════════════════════════════════════════════════
# WORKFLOWS
# ══════════════════════════════════════════════════════════════════════════════

prelab: verify start status
	@echo ""
	@echo "$(GREEN)══════════════════════════════════════════════════════════════════════════════$(RESET)"
	@echo "$(BOLD)  Pre-laboratory preparation complete!$(RESET)"
	@echo "$(GREEN)══════════════════════════════════════════════════════════════════════════════$(RESET)"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Open Portainer: http://localhost:9000"
	@echo "  2. Open DVWA: http://localhost:8080"
	@echo "  3. Start Wireshark and select 'vEthernet (WSL)'"
	@echo "  4. Begin with Exercise 1: make ex1"
	@echo ""

postlab:
	@echo "$(CYAN)[*] Post-laboratory cleanup...$(RESET)"
	@echo ""
	@echo "$(BOLD)Quiz Results:$(RESET)"
	@python3 formative/run_quiz.py --export artifacts/final_quiz_results.json 2>/dev/null || true
	@echo ""
	@$(MAKE) stop
	@$(MAKE) clean
	@echo ""
	@echo "$(GREEN)══════════════════════════════════════════════════════════════════════════════$(RESET)"
	@echo "$(BOLD)  Post-laboratory complete!$(RESET)"
	@echo "$(GREEN)══════════════════════════════════════════════════════════════════════════════$(RESET)"
	@echo ""
	@echo "Remember to:"
	@echo "  1. Save your PCAP captures from pcap/ folder"
	@echo "  2. Export scan results from artifacts/ folder"
	@echo "  3. Complete the online self-assessment if required"
	@echo ""

all: verify lint validate smoke
	@echo ""
	@echo "$(GREEN)══════════════════════════════════════════════════════════════════════════════$(RESET)"
	@echo "$(BOLD)  Full verification suite complete!$(RESET)"
	@echo "$(GREEN)══════════════════════════════════════════════════════════════════════════════$(RESET)"

# ══════════════════════════════════════════════════════════════════════════════
# DOCKER COMPOSE SHORTCUTS
# ══════════════════════════════════════════════════════════════════════════════

up:
	@docker compose -f docker/docker-compose.yml up -d

down:
	@docker compose -f docker/docker-compose.yml down

build:
	@docker compose -f docker/docker-compose.yml build

pull:
	@docker compose -f docker/docker-compose.yml pull

# ══════════════════════════════════════════════════════════════════════════════
# DEVELOPMENT HELPERS
# ══════════════════════════════════════════════════════════════════════════════

install-dev:
	@echo "$(CYAN)[*] Installing development dependencies...$(RESET)"
	@pip install -r setup/requirements.txt
	@pip install ruff pytest pytest-cov mypy
	@echo "$(GREEN)[✓] Development dependencies installed$(RESET)"

format:
	@echo "$(CYAN)[*] Formatting code with ruff...$(RESET)"
	@ruff format src/ scripts/ tests/ formative/ 2>/dev/null || \
		echo "$(YELLOW)[!] Install ruff: pip install ruff$(RESET)"

# ══════════════════════════════════════════════════════════════════════════════
