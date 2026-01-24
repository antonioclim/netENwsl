# Makefile — Week 12: Email Protocols and RPC
# NETWORKING class - ASE, CSIE | by ing. dr. Antonio Clim
#
# Usage: make help

.PHONY: help start stop status logs test smoke quiz lint verify clean
.PHONY: smtp-server smtp-send smtp-list demo-smtp demo-rpc capture analyse

PYTHON := python3
COMPOSE := docker compose -f docker/docker-compose.yml

# ═══════════════════════════════════════════════════════════════════════════════
# HELP
# ═══════════════════════════════════════════════════════════════════════════════
help:
	@echo ""
	@echo "Week 12 Laboratory Commands"
	@echo "═══════════════════════════════════════════════════════════════════════"
	@echo ""
	@echo "Lab Environment:"
	@echo "  make start       Start laboratory containers"
	@echo "  make stop        Stop laboratory containers"
	@echo "  make status      Show container status"
	@echo "  make logs        Follow container logs"
	@echo ""
	@echo "Testing:"
	@echo "  make test        Run all pytest tests"
	@echo "  make smoke       Run smoke tests only"
	@echo "  make quiz        Run formative self-assessment quiz"
	@echo ""
	@echo "Development:"
	@echo "  make lint        Check Python syntax"
	@echo "  make verify      Verify environment setup"
	@echo "  make clean       Clean artifacts and caches"
	@echo ""
	@echo "SMTP Services:"
	@echo "  make smtp-server Start SMTP server (foreground, verbose)"
	@echo "  make smtp-send   Send a test email"
	@echo "  make smtp-list   List stored emails in spool"
	@echo ""
	@echo "RPC Demos:"
	@echo "  make demo-smtp   Run SMTP demonstration"
	@echo "  make demo-rpc    Run RPC comparison demo"
	@echo ""
	@echo "Packet Capture:"
	@echo "  make capture     Capture traffic for 30 seconds (needs sudo)"
	@echo "  make analyse     Analyse captured packets with tshark"
	@echo ""

# ═══════════════════════════════════════════════════════════════════════════════
# LAB_ENVIRONMENT
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
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════
test: smoke
	@echo "Running pytest..."
	@$(PYTHON) -m pytest tests/ -v --tb=short

smoke:
	@echo "Running smoke tests..."
	@$(PYTHON) tests/smoke_test.py

quiz:
	@echo "Starting formative quiz..."
	@$(PYTHON) formative/run_quiz.py

# ═══════════════════════════════════════════════════════════════════════════════
# DEVELOPMENT
# ═══════════════════════════════════════════════════════════════════════════════
lint:
	@echo "Checking Python syntax..."
	@$(PYTHON) -m py_compile src/apps/email/*.py src/apps/rpc/*/*.py 2>/dev/null && echo "  ✓ src/apps/ OK" || echo "  ✗ Errors in src/apps/"
	@$(PYTHON) -m py_compile src/exercises/*.py 2>/dev/null && echo "  ✓ src/exercises/ OK" || echo "  ✗ Errors in src/exercises/"
	@$(PYTHON) -m py_compile scripts/*.py 2>/dev/null && echo "  ✓ scripts/ OK" || echo "  ✗ Errors in scripts/"
	@$(PYTHON) -m py_compile tests/*.py 2>/dev/null && echo "  ✓ tests/ OK" || echo "  ✗ Errors in tests/"
	@$(PYTHON) -m py_compile formative/*.py 2>/dev/null && echo "  ✓ formative/ OK" || echo "  ✗ Errors in formative/"
	@echo "Syntax check complete."

verify:
	@$(PYTHON) setup/verify_environment.py

clean:
	@echo "Cleaning artifacts..."
	@rm -rf artifacts/*.pcap artifacts/*.log 2>/dev/null || true
	@rm -rf pcap/*.pcap 2>/dev/null || true
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "Clean complete."

# ═══════════════════════════════════════════════════════════════════════════════
# SMTP_SERVICES
# ═══════════════════════════════════════════════════════════════════════════════
smtp-server:
	@echo "Starting SMTP server on localhost:1025..."
	@$(PYTHON) src/apps/email/smtp_server.py --verbose --spool docker/volumes/spool

smtp-send:
	@echo "Sending test email..."
	@$(PYTHON) src/apps/email/smtp_client.py

smtp-list:
	@echo "Stored emails in spool:"
	@ls -la docker/volumes/spool/*.eml 2>/dev/null || echo "  (no emails stored yet)"

# ═══════════════════════════════════════════════════════════════════════════════
# DEMOS
# ═══════════════════════════════════════════════════════════════════════════════
demo-smtp:
	@$(PYTHON) scripts/run_demo.py smtp

demo-rpc:
	@$(PYTHON) scripts/run_demo.py rpc

# ═══════════════════════════════════════════════════════════════════════════════
# PACKET_CAPTURE
# ═══════════════════════════════════════════════════════════════════════════════
capture:
	@echo "Starting packet capture (30 seconds)..."
	@echo "Note: This may require sudo privileges."
	@sudo $(PYTHON) scripts/capture_traffic.py --duration 30 --output pcap/

analyse:
	@echo "Analysing captured packets..."
	@command -v tshark >/dev/null 2>&1 && \
		tshark -r pcap/*.pcap -Y "smtp or http" 2>/dev/null | head -50 || \
		echo "tshark not found. Install Wireshark CLI tools."
