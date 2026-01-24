# 👥 Pair Programming Guide — Week 14

> NETWORKING class — ASE, CSIE | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

---

## Why Pair Programming?

Research in computing education shows that pair programming:

- Reduces errors by 15-20% compared to solo work
- Improves understanding through verbalisation
- Builds professional collaboration skills
- Makes debugging less frustrating

**This is not "one person works, one watches"** — both partners are actively engaged with different responsibilities.

---

## Roles

| Role | Responsibilities | Focus |
|------|-----------------|-------|
| **Driver** | Types code, controls keyboard and mouse | Tactical — the current line of code |
| **Navigator** | Reviews, suggests, checks documentation | Strategic — the overall approach |

### Driver responsibilities

- Type the code
- Explain what you are typing as you go
- Ask Navigator for input when unsure
- Follow Navigator's directions for architecture

### Navigator responsibilities

- Watch for typos and syntax errors
- Think ahead — what comes next?
- Look up documentation when needed
- Ask "what if..." questions
- Keep track of the overall goal

**SWAP roles every 10-15 minutes!** Set a timer.

---

## Session Structure (75 minutes)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PHASE 1: Setup (5 min)                                                     │
│  - Both partners verify environment works                                   │
│  - Decide who drives first                                                  │
│  - Read exercise objectives together                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  PHASE 2: Implementation (50 min)                                           │
│  - Work through exercises with role swaps                                   │
│  - Swap every 10-15 minutes (use timer!)                                    │
│  - Both partners must be able to explain every line                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  PHASE 3: Testing and Review (15 min)                                       │
│  - Run all tests together                                                   │
│  - Discuss alternative approaches                                           │
│  - Document any issues encountered                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│  PHASE 4: Reflection (5 min)                                                │
│  - What did you learn from your partner?                                    │
│  - What would you do differently?                                           │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## This Week's Pair Exercises

### Exercise P1: Environment Verification

**Objective:** Verify the complete lab environment functions correctly

**Estimated time:** 15 minutes

**Setup checklist (both partners verify):**

- [ ] Docker is running (`docker ps` shows Portainer)
- [ ] Can access Portainer at http://localhost:9000
- [ ] Lab containers are running (`docker compose ps`)
- [ ] Can reach load balancer at http://localhost:8080

**Driver task (first 7 min):**

```bash
# Run these commands, explain each output to Navigator
cd /mnt/d/NETWORKING/WEEK14/14enWSL
python3 setup/verify_environment.py
python3 scripts/start_lab.py --status
```

**Navigator task:**

- Check each output against expected values
- Note any warnings or errors
- Look up any unfamiliar messages

**Swap point:** After verification script completes

**Driver task (next 7 min):**

```bash
# Test connectivity to all services
curl -s http://localhost:8080/ | head -5
curl -s http://localhost:8080/lb-status
docker exec client ping -c 2 172.21.0.10
```

**Navigator task:**

- Verify HTTP responses are valid
- Check that ping succeeds
- Compare output to expected_outputs.md

---

### Exercise P2: Load Balancer Analysis

**Objective:** Observe and document round-robin load balancing behaviour

**Estimated time:** 20 minutes

**💭 PREDICTION (discuss together before starting):**

> "If we send 10 requests to the load balancer, how many will go to each backend?"

Write down your prediction: app1: ___ requests, app2: ___ requests

**Driver task (first 10 min):**

```python
# Create this script together
# File: test_lb_distribution.py

import subprocess
import re
from collections import Counter

results = []
for i in range(10):
    output = subprocess.run(
        ["curl", "-s", "http://localhost:8080/"],
        capture_output=True, text=True
    ).stdout
    
    # Extract backend identifier
    match = re.search(r"Backend[:\s]+(\w+)", output)
    if match:
        results.append(match.group(1))
    print(f"Request {i+1}: {results[-1] if results else 'unknown'}")

print(f"\nDistribution: {Counter(results)}")
```

**Navigator task:**

- Watch for syntax errors
- Suggest improvements to the regex
- Verify the Counter import is correct

**Swap point:** After script runs successfully

**Driver task (next 10 min):**

```bash
# Now test with one backend stopped
docker stop week14-app2-1

# Run the same test
python3 test_lb_distribution.py

# Observe the difference
# Restart the backend
docker start week14-app2-1
```

**Navigator task:**

- Document what happens when app2 is down
- Predict what the load balancer status page shows
- Check http://localhost:8080/lb-status

**Discussion questions:**

1. Did your prediction match the actual distribution?
2. How quickly did the load balancer detect the failed backend?
3. What HTTP status codes did you see during failover?

---

### Exercise P3: Packet Capture Analysis

**Objective:** Capture and analyse HTTP traffic through the load balancer

**Estimated time:** 25 minutes

**💭 PREDICTION (discuss together):**

> "How many TCP packets are needed for a single HTTP GET request and response?"

Your prediction: ___ packets

**Driver task (first 8 min):**

```bash
# Start packet capture in container
docker exec -d client tcpdump -i eth0 -w /tmp/lb_traffic.pcap port 8080

# Generate traffic
for i in 1 2 3; do
    docker exec client curl -s http://172.21.0.10:8080/ > /dev/null
    sleep 1
done

# Stop capture (find the tcpdump process and kill it)
docker exec client pkill tcpdump

# Copy capture file out
docker cp client:/tmp/lb_traffic.pcap ./pcap/lb_traffic.pcap
```

**Navigator task:**

- Note the tcpdump filter syntax
- Count the curl requests
- Verify the pcap file was created

**Swap point:** After pcap file is copied

**Driver task (next 8 min):**

```bash
# Analyse in container (if tshark available)
docker exec client tshark -r /tmp/lb_traffic.pcap -Y "http" 2>/dev/null || echo "Use Wireshark on Windows"

# Alternative: open in Wireshark on Windows
# Navigate to D:\NETWORKING\WEEK14\14enWSL\pcap\
```

**Navigator task:**

- Guide the Wireshark filter setup
- Help identify TCP handshakes vs HTTP data
- Count packets per request

**Swap point:** After initial analysis

**Driver task (final 8 min):**

Open Wireshark on Windows and:

1. Open `lb_traffic.pcap`
2. Apply filter: `http.request.method == "GET"`
3. Right-click a request → Follow → TCP Stream
4. Document the complete request/response cycle

**Navigator task:**

- Help identify the TCP handshake packets (SYN, SYN-ACK, ACK)
- Find the HTTP request and response
- Count total packets for one complete transaction

**Analysis questions:**

1. How many packets for TCP handshake?
2. How many packets for HTTP request?
3. How many packets for HTTP response?
4. How many packets for TCP teardown?
5. Was your prediction correct?

---

## Communication Phrases

### Navigator to Driver

Use these phrases to guide without taking over:

| Situation | Say this | Not this |
|-----------|----------|----------|
| Spotted a typo | "I think line 5 has a typo — check the variable name" | "You spelled it wrong, let me fix it" |
| Have an idea | "What if we tried using a dictionary here?" | "Do it this way instead" |
| Driver is stuck | "Want me to look up the syntax for that?" | *silence* |
| Something looks wrong | "Can you walk me through what that line does?" | "That's wrong" |
| Need to understand | "Before we move on, can you explain the logic?" | *pretending to understand* |

### Driver to Navigator

| Situation | Say this |
|-----------|----------|
| Starting new section | "I'm going to start the TCP connection part now" |
| Need input | "Does this look right to you?" |
| Stuck | "I'm not sure how to handle the timeout — any ideas?" |
| Explaining | "This line creates a socket because..." |
| Finished section | "That completes the setup — ready to move on?" |

---

## Troubleshooting Together

When stuck, follow this sequence:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. Driver: Explain your current understanding out loud                      │
│    "I think the problem is... because..."                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. Navigator: Ask clarifying questions                                      │
│    "What value did you expect there?"                                       │
│    "What does the error message say exactly?"                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. Both: Re-read the error message carefully                                │
│    Often the answer is in the message itself                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. Navigator: Search documentation                                          │
│    Check docs/troubleshooting.md first                                      │
│    Then docs/commands_cheatsheet.md                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ 5. If stuck after 5 minutes: Ask instructor                                 │
│    Explain what you tried and what you observed                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Common issues and quick fixes

| Symptom | First thing to check |
|---------|---------------------|
| "Connection refused" | Is the container running? `docker ps` |
| "No route to host" | Are you on the right network? |
| "Permission denied" | Did you use `sudo` where needed? |
| "Command not found" | Are you in the right shell (Bash vs PowerShell)? |
| Wireshark shows nothing | Did you select the correct interface? |

---

## Swap Reminder Checklist

Before swapping roles, the current Driver should:

- [ ] Save all files
- [ ] Explain where you stopped
- [ ] Describe what comes next

The new Driver should:

- [ ] Restate the current goal
- [ ] Ask any clarifying questions
- [ ] Confirm you understand the code so far

---

## Reflection Questions

At the end of the session, discuss:

1. **Learning:** "What did I learn from watching my partner work?"
2. **Teaching:** "What did I explain that helped clarify my own understanding?"
3. **Process:** "What would we do differently next time?"
4. **Blockers:** "What slowed us down most and how could we avoid it?"

---

## Assessment Notes

For pair programming exercises in this course:

- Both partners receive the same grade
- Both must be able to explain any part of the code
- Instructor may ask either partner questions during review
- Unequal participation will be noted and addressed

---

*Document version: 2.0 | Week 14: Integrated Recap | January 2025*
