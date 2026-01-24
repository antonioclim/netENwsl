# 👥 Pair Programming Guide — Week 1
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## Why Pair Programming?

Research shows that pair programming:
- Reduces bugs by catching errors in real-time
- Improves learning through explanation and discussion
- Builds communication skills essential for IT careers
- Makes debugging less frustrating (two heads are better than one!)

---

## Roles

| Role | Responsibilities | Focus |
|------|-----------------|-------|
| **🚗 Driver** | Types code, controls keyboard and mouse | Implementation details, syntax |
| **🧭 Navigator** | Reviews code, suggests improvements, checks docs | Big picture, strategy, errors |

**SWAP roles every 10-15 minutes!** Set a timer.

### Driver Guidelines

- Think aloud as you type — explain your reasoning
- Don't rush ahead without the Navigator understanding
- Ask "Does this look right?" before moving on
- Accept suggestions gracefully

### Navigator Guidelines

- Watch for typos and logical errors
- Keep the goal in mind — are we solving the right problem?
- Look up documentation when needed (man pages, `--help`)
- Ask clarifying questions: "What will happen if...?"
- Don't grab the keyboard! Guide with words.

---

## Session Structure

### Phase 1: Setup (5 minutes)

- [ ] Both partners can access the lab environment (WSL terminal)
- [ ] Verify Docker is running: `docker ps`
- [ ] Navigate to lab directory: `cd /mnt/d/NETWORKING/WEEK1/1enWSL`
- [ ] Decide who drives first (rock-paper-scissors?)
- [ ] Read exercise objectives together

### Phase 2: Implementation (40-50 minutes)

Follow the Driver/Navigator pattern with regular swaps.

**Swap triggers:**
- Timer goes off (10-15 min)
- After completing a logical section
- When stuck for more than 2 minutes
- When the Navigator has a strong idea to try

### Phase 3: Review (10 minutes)

- [ ] Both partners can explain every line of code
- [ ] Test edge cases together
- [ ] Discuss: "What would happen if...?"
- [ ] Document any insights or surprises

---

## This Week's Pair Exercises

### Exercise P1: Network Interface Discovery

**Objective:** Identify and document network configuration

**Estimated time:** 15 minutes (swap at 7 min)

**Driver task:**
```bash
# Enter the lab container
docker exec -it week1_lab bash

# Run these commands and document output
ip addr show
ip route show
ss -tlnp
```

**Navigator task:**
- Watch for typos in commands
- Note down the interface names (eth0, lo)
- Identify the IP address and subnet mask
- Check: Does the default gateway make sense?

**Swap point:** After `ip addr show` — Navigator becomes Driver for routing.

**💭 PREDICTION (before running):**
- How many network interfaces do you expect to see?
- What IP range do you expect for the container?

---

### Exercise P2: TCP Communication Test

**Objective:** Establish and observe a TCP connection

**Estimated time:** 20 minutes (swap every 7 min)

**Setup:** You need TWO terminal windows in the container.

```bash
# Terminal 1
docker exec -it week1_lab bash

# Terminal 2 (new window)
docker exec -it week1_lab bash
```

**Round 1 — Driver starts server:**
```bash
# Terminal 1 (Driver)
nc -l -p 9095
```

**Navigator:** While Driver sets up server, open Terminal 2 and prepare client command.

**Round 2 — Swap! Navigator (now Driver) connects:**
```bash
# Terminal 2 (new Driver)
nc localhost 9095
```

**Round 3 — Together:**
- Type messages in both terminals
- Observe bidirectional communication
- Check connection with: `ss -tn | grep 9095`

**💭 PREDICTION:**
- What state will `ss` show for the connection?
- What happens when you press Ctrl+C in the server?

**Discussion points:**
- Which side initiated the connection?
- How does TCP know to deliver data to the right process?

---

### Exercise P3: Capture and Analyse Traffic

**Objective:** Use tcpdump to capture TCP handshake

**Estimated time:** 20 minutes (swap every 7 min)

**Round 1 — Driver sets up capture:**
```bash
# Terminal 1 (Driver)
tcpdump -i lo port 9096 -w /work/pcap/pair_exercise.pcap &
```

**Navigator:** Verify capture is running, prepare server command.

**Round 2 — Swap! Start server and client:**
```bash
# Terminal 1 (new Driver)
nc -l -p 9096

# Terminal 2
echo "Hello from pair programming!" | nc localhost 9096
```

**Round 3 — Swap! Analyse capture:**
```bash
# Stop tcpdump (Ctrl+C or kill %1)
# Analyse
tshark -r /work/pcap/pair_exercise.pcap
```

**💭 PREDICTION:**
- How many packets for connection setup?
- How many packets total (setup + data + teardown)?

**Navigator checks:**
- Can you identify the SYN, SYN-ACK, ACK sequence?
- Which packet contains "Hello from pair programming!"?

---

## Communication Phrases

Use these phrases to communicate effectively:

### Navigator to Driver

| Situation | Phrase |
|-----------|--------|
| Clarifying intent | "What's your plan for this part?" |
| Spotted an error | "I think there might be an issue with..." |
| Need explanation | "Could you explain that line?" |
| Found documentation | "The man page says..." |
| Suggesting approach | "What if we tried...?" |
| Confirming understanding | "So we're trying to..." |

### Driver to Navigator

| Situation | Phrase |
|-----------|--------|
| Explaining action | "I'm going to try..." |
| Seeking validation | "Does this look right?" |
| Admitting confusion | "I'm stuck on..." |
| Requesting research | "Can you check what [command] does?" |
| Thinking aloud | "I expect this to..." |

---

## Troubleshooting Together

When stuck, follow this protocol:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 1  │  Driver: Explain your current understanding out loud            │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 2  │  Navigator: Ask clarifying questions                            │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 3  │  Both: Re-read the error message carefully, word by word        │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 4  │  Navigator: Search documentation (man pages, --help)            │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 5  │  If stuck > 5 min: Ask instructor (not a failure!)              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Common Week 1 Issues

| Symptom | Navigator Should Check |
|---------|----------------------|
| "Connection refused" | Is the server running? Right port? |
| "Address already in use" | Previous nc still running? Try `ss -tlnp` |
| "Permission denied" | Need sudo? Check file permissions |
| "Command not found" | Typo? Package not installed? |
| No output from tcpdump | Correct interface? Traffic generated? |

---

## Reflection Questions (End of Session)

Discuss with your partner:

1. What was the most confusing part? How did you resolve it?
2. Did you discover anything unexpected?
3. What would you do differently next time?
4. Rate your communication (1-5): Did you explain clearly? Listen well?

---

## Pair Programming Checklist

Before starting:
- [ ] Both partners have working environment
- [ ] Roles assigned (Driver/Navigator)
- [ ] Timer set for role swaps
- [ ] Exercise objectives understood

During:
- [ ] Driver thinks aloud
- [ ] Navigator actively watches and suggests
- [ ] Regular swaps happening
- [ ] Predictions made before running commands

After:
- [ ] Both can explain the code/commands
- [ ] Edge cases tested
- [ ] Insights documented
- [ ] Reflection completed

---

*NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim*
*Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment*
