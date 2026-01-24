# ❓ Frequently Asked Questions — Week 7
## Computer Networks — ASE, CSIE | Computer Networks Laboratory

> Quick answers to common questions about the Week 7 laboratory kit.

---

## Table of Contents

1. [Setup and Installation](#setup-and-installation)
2. [Docker and Containers](#docker-and-containers)
3. [Packet Capture](#packet-capture)
4. [Firewall Rules](#firewall-rules)
5. [Quiz and Assessment](#quiz-and-assessment)
6. [Troubleshooting](#troubleshooting)

---

## Setup and Installation

### Q: What Python version do I need?

**A:** Python 3.11 or higher is required. Check your version:

```bash
python3 --version
```

If you have an older version, install Python 3.11 via your package manager or pyenv.

---

### Q: How do I install the dependencies?

**A:** Run the following command from the kit root directory:

```bash
pip install -r setup/requirements.txt
```

For development tools (testing, linting), also install:

```bash
pip install -r setup/requirements-dev.txt
```

---

### Q: Can I use this kit on Windows without WSL?

**A:** The kit is designed for WSL2 (Windows Subsystem for Linux) and native Linux. Running directly on Windows is not supported because:

- Docker networking behaves differently on native Windows
- Packet capture tools have different interfaces
- Shell scripts require bash

Install WSL2 following Microsoft's official guide.

---

### Q: How do I verify my environment is set up correctly?

**A:** Run the verification script:

```bash
make verify
# or
python3 setup/verify_environment.py
```

This checks Docker, Python and network connectivity.

---

## Docker and Containers

### Q: Why does `make start` fail with "Cannot connect to Docker daemon"?

**A:** Docker Desktop needs to be running. On WSL2:

1. Start Docker Desktop on Windows
2. Ensure "Use the WSL 2 based engine" is enabled in Docker Desktop settings
3. Wait 30 seconds for Docker to initialise
4. Try again

---

### Q: What are the container IP addresses?

**A:** The Week 7 network uses the 10.0.7.0/24 subnet:

| Container | IP Address | Port |
|-----------|------------|------|
| TCP Server | 10.0.7.100 | 9090 |
| UDP Receiver | 10.0.7.200 | 9091 |
| TCP Client | 10.0.7.11 | - |
| UDP Sender | 10.0.7.12 | - |
| Packet Filter | 10.0.7.50 | 8888 |

**Note:** Port 9000 is RESERVED for Portainer and should not be used.

---

### Q: How do I access Portainer?

**A:** 
1. Ensure Docker is running
2. Open http://localhost:9000 in your browser
3. Login with credentials: `stud` / `studstudstud`

---

### Q: How do I view container logs?

**A:** Use Docker commands or the Makefile:

```bash
# All containers
make dc-logs

# Specific container
docker logs week7_tcp_server_1 -f
```

---

## Packet Capture

### Q: Which Wireshark interface should I use on Windows?

**A:** Select **vEthernet (WSL)** to capture Docker traffic from WSL2.

Do NOT use:
- Ethernet (only external traffic)
- Wi-Fi (only wireless traffic)  
- Loopback (only Windows localhost)

---

### Q: Why is my capture empty?

**A:** Common causes:

1. **Wrong interface** — Use vEthernet (WSL) on Windows
2. **No traffic** — Generate traffic with `make test-1`
3. **Filter too restrictive** — Remove display filters temporarily
4. **Permissions** — Run Wireshark as Administrator on Windows

---

### Q: How do I filter TCP traffic to port 9090?

**A:** Use these filters:

**Capture filter (tcpdump):**
```
tcp port 9090
```

**Display filter (Wireshark):**
```
tcp.port == 9090
```

---

### Q: What do the PCAP sample files contain?

**A:** Each sample demonstrates a specific concept:

| File | Content |
|------|---------|
| `week07_lo1_tcp_handshake.pcap` | Complete TCP SYN/SYN-ACK/ACK sequence |
| `week07_lo2_tcp_blocked_reject.pcap` | SYN followed by RST (REJECT) |
| `week07_lo2_tcp_blocked_drop.pcap` | SYN retransmissions with no response (DROP) |
| `week07_lo6_drop_vs_reject.pcap` | Side-by-side comparison |

Generate samples with:
```bash
make generate-pcap
```

---

## Firewall Rules

### Q: What is the difference between DROP and REJECT?

**A:**

| Aspect | DROP | REJECT |
|--------|------|--------|
| Response | None (silent) | RST or ICMP message |
| Client sees | Timeout | "Connection refused" |
| Stealth | High (hides firewall) | Low (reveals firewall) |
| Best for | External attackers | Internal debugging |

---

### Q: Why do my iptables rules disappear after reboot?

**A:** iptables rules are not persistent by default. They are stored in memory only.

To save rules:
```bash
sudo iptables-save > /etc/iptables/rules.v4
```

To restore:
```bash
sudo iptables-restore < /etc/iptables/rules.v4
```

---

### Q: How do I view current iptables rules?

**A:**
```bash
# All chains with line numbers
sudo iptables -L -n -v --line-numbers

# Specific chain
sudo iptables -L INPUT -n
```

---

### Q: Why does rule order matter?

**A:** iptables uses **first-match-wins** semantics. Rules are evaluated top-to-bottom and the first matching rule determines the action.

**Correct order:**
```bash
iptables -A INPUT -p tcp --dport 9090 -j ACCEPT  # Specific first
iptables -A INPUT -p tcp -j DROP                  # General last
```

**Wrong order:**
```bash
iptables -A INPUT -p tcp -j DROP                  # Blocks everything!
iptables -A INPUT -p tcp --dport 9090 -j ACCEPT  # Never reached
```

---

## Quiz and Assessment

### Q: How do I run the formative quiz?

**A:**
```bash
# Full quiz (15 questions)
make quiz

# Quick quiz (5 random questions)
make quiz-quick

# Specific learning objective
make quiz-lo1
```

---

### Q: What score do I need to pass?

**A:** The passing threshold is 70% (22 out of 32 points).

Grade boundaries:
- A: 90%+ (29+ points)
- B: 80%+ (26+ points)
- C: 70%+ (22+ points)
- D: 60%+ (19+ points)

---

### Q: How do I export the quiz for Moodle?

**A:**
```bash
# Export to all formats
make export-quiz

# Specific format
python3 formative/quiz_export.py --format moodle --output quiz.xml
```

Supported formats:
- Moodle XML
- Canvas JSON
- Generic JSON (for custom LMS)

---

### Q: What are Parsons problems?

**A:** Parsons problems present code blocks that need to be arranged in the correct order. They help develop understanding of procedural logic without requiring syntax memorisation.

Run Parsons problems:
```bash
make parsons
```

---

## Troubleshooting

### Q: "Permission denied" when running scripts

**A:** Make scripts executable:
```bash
chmod +x scripts/*.py
```

Or run with Python explicitly:
```bash
python3 scripts/start_lab.py
```

---

### Q: Tests fail with "Connection refused"

**A:** The lab environment is not running. Start it first:
```bash
make start
```

Wait 10-15 seconds for containers to initialise before running tests.

---

### Q: "Module not found" errors

**A:** Dependencies are not installed. Run:
```bash
pip install -r setup/requirements.txt
```

If using a virtual environment, ensure it is activated:
```bash
source .venv/bin/activate
```

---

### Q: How do I completely reset the environment?

**A:**
```bash
# Stop and remove everything
make clean

# Start fresh
make start
```

This removes containers, networks and temporary files.

---

### Q: Where can I get help?

**A:** Resources in order of preference:

1. **This FAQ** — Check if your question is answered here
2. **Troubleshooting guide** — `docs/troubleshooting.md`
3. **Theory summary** — `docs/theory_summary.md`
4. **Misconceptions** — `docs/misconceptions.md` for common errors

Issues: Open an issue in GitHub

---

## Quick Reference

### Essential Commands

```bash
# Start lab
make start

# Stop lab
make stop

# Run tests
make test

# Run quiz
make quiz

# View help
make help
```

### Key Files

| Purpose | Location |
|---------|----------|
| Main instructions | `README.md` |
| Theory | `docs/theory_summary.md` |
| Commands | `docs/commands_cheatsheet.md` |
| Quiz | `formative/quiz.yaml` |
| Profiles | `docker/configs/firewall_profiles.json` |

---

*Computer Networks — Week 7: Packet Interception, Filtering and Defensive Port Probing*  
*ASE Bucharest, CSIE | Computer Networks Laboratory*
