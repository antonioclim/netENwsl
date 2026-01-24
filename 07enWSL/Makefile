# ============================================================================
# Makefile — Week 7: Packet Interception, Filtering and Defensive Port Probing
# NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim
# ============================================================================
#
# Usage:
#   make help        - Show available targets
#   make start       - Start lab environment
#   make stop        - Stop lab environment
#   make test        - Run all tests
#   make quiz        - Run formative quiz
#
# ============================================================================

.PHONY: all help start stop restart clean test quiz parsons smoke verify install

# Default target
all: help

# ─── HELP ────────────────────────────────────────────────────────────────────

help:
	@echo "╔════════════════════════════════════════════════════════════════╗"
	@echo "║          Week 7 Laboratory - Available Commands                ║"
	@echo "╠════════════════════════════════════════════════════════════════╣"
	@echo "║                                                                ║"
	@echo "║  Environment:                                                  ║"
	@echo "║    make start      Start Docker containers                     ║"
	@echo "║    make stop       Stop Docker containers                      ║"
	@echo "║    make restart    Restart all containers                      ║"
	@echo "║    make clean      Remove containers and networks              ║"
	@echo "║    make verify     Verify environment setup                    ║"
	@echo "║                                                                ║"
	@echo "║  Testing:                                                      ║"
	@echo "║    make test       Run all exercise tests                      ║"
	@echo "║    make smoke      Run smoke tests only                        ║"
	@echo "║    make test-1     Run Exercise 1 tests                        ║"
	@echo "║    make test-2     Run Exercise 2 tests                        ║"
	@echo "║    make test-3     Run Exercise 3 tests                        ║"
	@echo "║    make test-4     Run Exercise 4 tests                        ║"
	@echo "║    make test-5     Run Exercise 5 tests                        ║"
	@echo "║                                                                ║"
	@echo "║  Formative Assessment:                                         ║"
	@echo "║    make quiz       Run formative quiz (15 questions)           ║"
	@echo "║    make quiz-quick Run quick quiz (5 random questions)         ║"
	@echo "║    make parsons    Run Parsons problems                        ║"
	@echo "║    make review     Review quiz (show answers)                  ║"
	@echo "║                                                                ║"
	@echo "║  Setup:                                                        ║"
	@echo "║    make install    Install Python dependencies                 ║"
	@echo "║                                                                ║"
	@echo "╚════════════════════════════════════════════════════════════════╝"

# ─── ENVIRONMENT MANAGEMENT ──────────────────────────────────────────────────

start:
	@echo "Starting Week 7 laboratory environment..."
	python3 scripts/start_lab.py

stop:
	@echo "Stopping laboratory environment..."
	python3 scripts/stop_lab.py

restart: stop start
	@echo "Laboratory restarted."

clean:
	@echo "Cleaning up Docker resources..."
	python3 scripts/cleanup.py --full
	@echo "Cleanup complete."

verify:
	@echo "Verifying environment setup..."
	python3 setup/verify_environment.py

# ─── TESTING ─────────────────────────────────────────────────────────────────

test:
	@echo "Running all exercise tests..."
	python3 tests/test_exercises.py --all

smoke:
	@echo "Running smoke tests..."
	python3 tests/smoke_test.py

test-1:
	@echo "Testing Exercise 1: Baseline Traffic Capture..."
	python3 tests/test_exercises.py --exercise 1

test-2:
	@echo "Testing Exercise 2: TCP Filtering with REJECT..."
	python3 tests/test_exercises.py --exercise 2

test-3:
	@echo "Testing Exercise 3: UDP Filtering with DROP..."
	python3 tests/test_exercises.py --exercise 3

test-4:
	@echo "Testing Exercise 4: Application-Layer Filter..."
	python3 tests/test_exercises.py --exercise 4

test-5:
	@echo "Testing Exercise 5: Defensive Port Probing..."
	python3 tests/test_exercises.py --exercise 5

# ─── PYTEST INTEGRATION ──────────────────────────────────────────────────────

pytest:
	@echo "Running tests with pytest..."
	pytest tests/ -v

pytest-cov:
	@echo "Running tests with coverage..."
	pytest tests/ --cov=src --cov=scripts --cov-report=term-missing

# ─── FORMATIVE ASSESSMENT ────────────────────────────────────────────────────

quiz:
	@echo "Starting formative quiz..."
	python3 formative/run_quiz.py

quiz-quick:
	@echo "Starting quick quiz (5 random questions)..."
	python3 formative/run_quiz.py --random --limit 5

quiz-lo1:
	python3 formative/run_quiz.py --lo LO1

quiz-lo2:
	python3 formative/run_quiz.py --lo LO2

quiz-lo3:
	python3 formative/run_quiz.py --lo LO3

quiz-lo4:
	python3 formative/run_quiz.py --lo LO4

quiz-lo6:
	python3 formative/run_quiz.py --lo LO6

review:
	@echo "Quiz review mode (answers shown)..."
	python3 formative/run_quiz.py --review

parsons:
	@echo "Starting Parsons problems..."
	python3 formative/parsons_runner.py

parsons-hint:
	@echo "Parsons problems with hints..."
	python3 formative/parsons_runner.py --hint

# ─── SETUP ───────────────────────────────────────────────────────────────────

install:
	@echo "Installing Python dependencies..."
	pip install -r setup/requirements.txt
	@echo "Dependencies installed."

install-dev:
	@echo "Installing development dependencies..."
	pip install -r setup/requirements.txt pytest pytest-cov ruff
	@echo "Development dependencies installed."

# ─── DOCKER COMPOSE SHORTCUTS ────────────────────────────────────────────────

dc-up:
	docker compose -f docker/docker-compose.yml up -d

dc-down:
	docker compose -f docker/docker-compose.yml down

dc-logs:
	docker compose -f docker/docker-compose.yml logs -f

dc-ps:
	docker compose -f docker/docker-compose.yml ps

# ─── CAPTURE SHORTCUTS ───────────────────────────────────────────────────────

capture:
	@echo "Starting packet capture (60 seconds)..."
	python3 scripts/capture_traffic.py --duration 60 --output artifacts/capture_$$(date +%Y%m%d_%H%M%S).pcap

capture-tcp:
	@echo "Capturing TCP traffic only..."
	python3 scripts/capture_traffic.py --duration 60 --filter "tcp port 9090" --output artifacts/tcp_capture.pcap

capture-udp:
	@echo "Capturing UDP traffic only..."
	python3 scripts/capture_traffic.py --duration 60 --filter "udp port 9091" --output artifacts/udp_capture.pcap

# ============================================================================
