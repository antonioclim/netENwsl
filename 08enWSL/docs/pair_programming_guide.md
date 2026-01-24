# 👥 Pair Programming Guide — Week 8
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## Roles

| Role | Responsibilities | Duration |
|------|-----------------|----------|
| **Driver** | Types code, controls keyboard/mouse, implements ideas | 10-15 min |
| **Navigator** | Reviews code, suggests improvements, checks documentation, thinks ahead | 10-15 min |

**SWAP roles every 10-15 minutes or after completing a function!**

---

## Why Pair Programming?

Research shows pair programming:
- **Catches more bugs** — two pairs of eyes spot more errors
- **Spreads knowledge** — both partners learn the codebase
- **Improves code quality** — constant review during writing
- **Keeps focus** — social pressure reduces distractions

For networking exercises specifically:
- Navigator can monitor Wireshark while Driver codes
- Navigator can test with curl while Driver implements
- Both partners understand the full request-response cycle

---

## Session Structure

### Phase 1: Setup (5 min)

- [ ] Both partners have the lab environment running
- [ ] Both can access http://localhost:8080 (verify nginx is up)
- [ ] Decide who drives first (suggestion: less experienced with topic)
- [ ] Review the exercise objectives together
- [ ] Read the PREDICTION CHECKPOINT together and discuss

### Phase 2: Implementation (40-50 min)

**Driver's focus:**
- Type the code
- Explain your thinking as you code
- Ask Navigator when unsure

**Navigator's focus:**
- Watch for typos and syntax errors
- Think about edge cases
- Look up documentation when needed
- Track progress against exercise goals

**Swap triggers:**
- After completing each TODO function
- Every 15 minutes maximum
- When Driver gets stuck (fresh perspective helps)
- When Navigator has an idea they want to try

### Phase 3: Review & Test (10 min)

- [ ] Both partners can explain every function
- [ ] Run all test cases together
- [ ] Test edge cases (what happens with bad input?)
- [ ] Discuss alternative approaches

---

## This Week's Pair Exercises

### Exercise 1: HTTP Server (45-60 min)

**Learning goal:** Understand HTTP request/response format through implementation

#### Swap Schedule

| Phase | Driver Task | Navigator Task | Swap After |
|-------|-------------|----------------|------------|
| 1 | Implement `parse_request()` | Monitor for CRLF handling issues | Function complete |
| 2 | Implement `is_safe_path()` | Research path traversal attacks | Function complete |
| 3 | Implement `serve_file()` | Test with curl, watch MIME types | Function complete |
| 4 | Implement `build_response()` | Verify HTTP format compliance | Function complete |
| 5 | Implement `handle_request()` | Test GET vs HEAD behaviour | Exercise complete |

#### Navigator Checklist (Ex 1)

While Driver implements, verify:

- [ ] `parse_request()`: Headers are case-insensitive?
- [ ] `is_safe_path()`: What about `%2e%2e` (URL-encoded `..`)?
- [ ] `serve_file()`: What if path is a directory?
- [ ] `build_response()`: Is there a blank line before body?
- [ ] `handle_request()`: HEAD returns Content-Length but no body?

#### Testing Commands (Navigator runs while Driver implements)

```bash
# Basic test
curl -v http://localhost:8081/

# HEAD vs GET
curl -I http://localhost:8081/hello.txt
curl -v http://localhost:8081/hello.txt

# Security test
curl -v http://localhost:8081/../../etc/passwd

# Non-existent file
curl -v http://localhost:8081/doesnotexist.html
```

---

### Exercise 2: Reverse Proxy (40-50 min)

**Learning goal:** Understand proxy forwarding and load balancing

#### Swap Schedule

| Phase | Driver Task | Navigator Task | Swap After |
|-------|-------------|----------------|------------|
| 1 | Implement `RoundRobinBalancer.__init__()` | Verify thread safety with Lock | Method complete |
| 2 | Implement `RoundRobinBalancer.next_backend()` | Check modular arithmetic | Method complete |
| 3 | Implement `add_proxy_headers()` | Verify X-Forwarded-For format | Function complete |
| 4 | Implement `forward_request()` | Monitor backend terminals | Function complete |
| 5 | Implement `check_backend_health()` | Test timeout behaviour | Function complete |

#### Navigator Checklist (Ex 2)

While Driver implements, verify:

- [ ] `next_backend()`: What if all backends are unhealthy?
- [ ] `next_backend()`: Is the lock used correctly?
- [ ] `add_proxy_headers()`: What if X-Forwarded-For already exists?
- [ ] `forward_request()`: Is the socket closed on error?
- [ ] `check_backend_health()`: Timeout is short enough?

#### Testing Commands (Navigator runs)

```bash
# Start backends in separate terminals first!
# Terminal 1: python3 src/apps/backend_server.py --port 9001 --id A
# Terminal 2: python3 src/apps/backend_server.py --port 9002 --id B  
# Terminal 3: python3 src/apps/backend_server.py --port 9003 --id C

# Test round-robin distribution
for i in {1..9}; do 
    curl -s http://localhost:8888/ | grep -o 'Backend [A-C]'
done

# Check X-Forwarded-For header (look at backend terminal output)
curl -v http://localhost:8888/
```

---

## Communication Phrases

### Navigator to Driver

**Suggestions:**
- "What's your plan for handling [edge case]?"
- "Could you explain that line? I want to make sure I follow."
- "I think there might be an issue with [specific thing]..."
- "The documentation says [specific information]."
- "What if the input is [unusual case]?"

**Encouragement:**
- "That's a good approach."
- "I see where you're going with this."
- "Nice catch on [specific detail]."

**Redirection:**
- "Let's step back — what are we trying to achieve?"
- "Can we test what we have so far?"
- "I'm not sure about that approach — can we discuss?"

### Driver to Navigator

**Thinking aloud:**
- "I'm going to try [approach] because [reason]."
- "I'm thinking we need to handle [case] here."
- "Let me just get this working, then we can refactor."

**Requests:**
- "Can you check what [function/command] does?"
- "Does this look right to you?"
- "I'm stuck on [specific issue] — any ideas?"
- "Can you test this with curl while I watch the output?"

---

## Troubleshooting Together

### When Stuck (5-Minute Rule)

If stuck for more than 5 minutes:

1. **Driver:** Explain your current understanding out loud
2. **Navigator:** Ask clarifying questions (not leading questions)
3. **Both:** Re-read the error message CAREFULLY
4. **Navigator:** Search documentation for relevant info
5. **Both:** If still stuck, raise hand and ask instructor

### Common Week 8 Debugging

| Symptom | Navigator Should Check |
|---------|----------------------|
| "Connection refused" | Is the server running? Right port? |
| Empty response | Is body being sent? Check Content-Length |
| 502 Bad Gateway | Are backends running? Check nginx upstream |
| Garbled output | Encoding issue? Check for binary vs text |
| Only one backend used | Is round-robin index incrementing? |

### Using Wireshark Together

**Split-screen approach:**
1. Navigator opens Wireshark, starts capture
2. Driver runs curl command
3. Navigator finds the relevant packets
4. Both analyse the capture together

**What to look for:**
- TCP handshake (3 packets)
- HTTP request format
- HTTP response format
- Connection reuse (keep-alive)

---

## Reflection Questions (End of Session)

Discuss with your partner:

1. What was the trickiest part of today's exercise?
2. Did we catch any bugs that one person might have missed alone?
3. What would we do differently next time?
4. What's one thing we learned from each other?

---

## Tips for Effective Pairing

### Do ✅

- **Communicate constantly** — silence means confusion
- **Take breaks** — stand up, stretch every 30 minutes
- **Celebrate small wins** — "Nice, that test passes!"
- **Be patient** — different people think at different speeds
- **Stay engaged** — Navigator should never zone out

### Don't ❌

- **Don't grab the keyboard** — ask "May I drive for a bit?"
- **Don't dictate code** — suggest approaches, not exact syntax
- **Don't stay silent** — if confused, say so immediately
- **Don't check phone** — respect your partner's time
- **Don't blame** — bugs are "ours" not "yours"

---

## Remote Pairing (If Needed)

If pairing remotely:

1. **Screen share** — Driver shares their screen
2. **Voice chat** — Keep microphone on (mute background noise)
3. **Swap via git** — Push code when swapping roles
4. **Use comments** — Leave TODO comments for partner

```bash
# Quick swap workflow
git add -A && git commit -m "WIP: swap to partner"
git push
# Partner pulls and continues
```

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
