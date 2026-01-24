# README.md Additions — Insert after line 25

This file contains additions to be merged with the existing README.md.
The key additions are:

1. Pre-Flight Checklist section (after Environment Notice)
2. Beginner Mode section (after Pre-Flight Checklist)
3. Updated author attribution

## ✈️ Pre-Flight Checklist (For Beginners)

Before running any exercise, verify these conditions:

### Level 1: Basic Requirements (Mandatory)

```bash
# 1. Am I in the correct directory?
cd /mnt/d/NETWORKING/WEEK13/13enWSL
ls README.md > /dev/null 2>&1 && echo "✅ Directory OK" || echo "❌ Wrong directory"

# 2. Is Docker running?
docker info > /dev/null 2>&1 && echo "✅ Docker OK" || echo "❌ Start Docker Desktop"

# 3. Is Python 3.11+ installed?
python3 --version | grep -E "3\.(1[1-9]|[2-9][0-9])" && echo "✅ Python OK" || echo "❌ Need 3.11+"
```

### Level 2: Dependencies Check

```bash
# Run the automated verification
make verify
```

### Level 3: Conceptual Readiness

- [ ] TCP three-way handshake (SYN, SYN-ACK, ACK)
- [ ] Port states: OPEN, CLOSED, FILTERED
- [ ] MQTT publish/subscribe model

**Study resources:** `docs/theory_summary.md`

---

## 🎓 Beginner Mode

All exercises support **Beginner Mode** with step-by-step explanations.

### How to Enable

```bash
export WEEK13_BEGINNER_MODE=1
python3 src/exercises/ex_13_01_port_scanner.py --target localhost --ports 80
```

### What You Will See

```
💡 EXPLANATION: Creating a TCP socket. SOCK_STREAM means TCP (connection-oriented).

💡 EXPLANATION: Setting timeout to 0.5 seconds. If no response, port is 'filtered'.
```

---
