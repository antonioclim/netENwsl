# 👥 Pair Programming Guide — Week 2: Sockets and Transport Protocols

> NETWORKING class — ASE, CSIE Bucharest  
> Computer Networks Laboratory | by ing. dr. Antonio Clim

---

## Roles

| Role | Responsibilities | Duration |
|------|------------------|----------|
| **Driver** | Types code, controls keyboard and mouse, executes commands | 10-15 min |
| **Navigator** | Reviews code, suggests improvements, checks documentation, spots errors | 10-15 min |

**🔄 SWAP roles every 10-15 minutes!** Set a timer.

---

## Session Structure

### Phase 1: Setup (5 min)

- [ ] Both partners can access the lab environment
- [ ] Verify Docker is running: `docker ps`
- [ ] Navigate to exercise directory
- [ ] Decide who drives first (e.g., alphabetically by name)
- [ ] Review the exercise objectives together

### Phase 2: Implementation (45-50 min)

**Driver responsibilities:**
- Type code at a pace the Navigator can follow
- Explain your thinking out loud ("I'm going to...")
- Ask Navigator before making major decisions
- Don't rush — quality over speed

**Navigator responsibilities:**
- Watch for typos and syntax errors
- Think ahead: "What's our next step?"
- Keep documentation open for reference
- Note questions to discuss later
- Track time and call for role swaps

### Phase 3: Review (10 min)

- [ ] Both partners can explain every line of code
- [ ] Test edge cases together
- [ ] Discuss: "What would we do differently next time?"
- [ ] Document any issues encountered

---

## This Week's Pair Exercises

### Exercise P1: TCP Echo Server with Transformation

**Objective:** Implement a concurrent TCP server that transforms messages.

**Estimated time:** 25 min

**Setup:**
```bash
cd /mnt/d/NETWORKING/WEEK2/2enWSL
# Open src/exercises/ex_2_01_tcp.py for reference
```

**Driver tasks (first 12 min):**
1. Create a new file `pair_tcp_server.py`
2. Implement basic socket setup (create, bind, listen)
3. Write the main accept loop

**Navigator tasks:**
- Verify correct socket type (SOCK_STREAM)
- Check port number doesn't conflict (use 9095)
- Reference documentation for `setsockopt` usage

**🔄 SWAP at accept loop completion**

**Driver tasks (next 12 min):**
1. Implement `handle_client()` function
2. Add threading for concurrent handling
3. Implement message transformation (reverse + uppercase)

**Navigator tasks:**
- Ensure proper thread creation syntax
- Verify socket is passed correctly to thread
- Check for proper cleanup (close)

**Verification:**
```bash
# Terminal 1: Start your server
python pair_tcp_server.py

# Terminal 2: Test with netcat
echo "hello" | nc localhost 9095
# Expected: OLLEH
```

**💭 Prediction checkpoint:** Before running, predict: What will Wireshark show for a single client connection?

#### P1 Reflection Questions

After completing this exercise, discuss with your partner:

1. **TCP understanding:** Why did you need to call `accept()` but not for UDP in P2?
2. **Threading decision:** What would happen if you removed threading? Try it!
3. **Error handling:** What happens if a client disconnects unexpectedly?
4. **Code ownership:** Which part of the code do you understand best? Which part does your partner understand better?

---

### Exercise P2: UDP Protocol with Multiple Commands

**Objective:** Implement a UDP server supporting multiple command types.

**Estimated time:** 25 min

**Required commands:**
- `ping` → `PONG`
- `time` → Current time (HH:MM:SS)
- `rand` → Random number 1-100
- `echo:text` → Returns text unchanged

**Driver tasks (first 12 min):**
1. Create `pair_udp_server.py`
2. Set up UDP socket (SOCK_DGRAM)
3. Implement receive loop with `recvfrom()`

**Navigator tasks:**
- Confirm no `listen()` or `accept()` calls (UDP!)
- Verify bind address is `0.0.0.0` not `127.0.0.1`
- Plan the command parsing strategy

**🔄 SWAP after receive loop works**

**Driver tasks (next 12 min):**
1. Implement command parsing (split on `:`)
2. Add all four command handlers
3. Send responses with `sendto()`

**Navigator tasks:**
- Test each command mentally before running
- Ensure `addr` from `recvfrom` is used in `sendto`
- Watch for encoding issues (bytes vs strings)

**Verification:**
```bash
# Terminal 1: Start server
python pair_udp_server.py

# Terminal 2: Test commands
echo "ping" | nc -u localhost 9096
echo "time" | nc -u localhost 9096
echo "echo:hello world" | nc -u localhost 9096
```

**💭 Prediction checkpoint:** What's different in Wireshark between this and the TCP exercise?

#### P2 Reflection Questions

After completing this exercise, discuss with your partner:

1. **Protocol comparison:** How does the code structure differ from TCP? Which feels simpler?
2. **Address handling:** Why do you need `addr` from `recvfrom()` to send a reply?
3. **Error scenarios:** What happens if you send an unknown command? Should you handle it?
4. **Collaboration quality:** Did the Navigator catch any bugs before running? Which ones?

---

### Exercise P3: Concurrent Server Stress Test

**Objective:** Compare iterative vs threaded server under load.

**Estimated time:** 20 min

**Driver tasks (first 10 min):**
1. Modify TCP server to have configurable mode (iterative/threaded)
2. Add artificial delay: `time.sleep(0.5)` in handler
3. Create timing wrapper for measurements

**Navigator tasks:**
- Plan how to switch modes (command-line argument?)
- Prepare test client that measures total time
- Note the expected difference in timings

**🔄 SWAP after mode switching works**

**Driver tasks (next 10 min):**
1. Write load test client (10 concurrent connections)
2. Run against iterative server, record time
3. Run against threaded server, record time

**Navigator tasks:**
- Calculate expected times:
  - Iterative: 10 clients × 0.5s = 5 seconds
  - Threaded: ~0.5 seconds (parallel)
- Document actual results
- Explain any discrepancies

**Results table:**

| Mode | Expected time | Actual time | Difference |
|------|---------------|-------------|------------|
| Iterative | 5.0s | ___s | ___ |
| Threaded | 0.5s | ___s | ___ |

**💭 Prediction checkpoint:** What happens if we use 100 clients instead of 10?

#### P3 Reflection Questions

After completing this exercise, discuss with your partner:

1. **Performance insight:** Was the actual timing close to your prediction? What might cause differences?
2. **Scalability thinking:** At what point would threading stop being the answer? (Hint: think about 10,000 clients)
3. **Code evolution:** How would you refactor your code to support a thread pool?
4. **Learning transfer:** Where else might you apply this iterative vs concurrent pattern?

---

## Common Pair Pitfalls

Avoid these common mistakes that harm pair programming effectiveness:

### ⚠️ Pitfall 1: Navigator Disengagement

**Symptoms:**
- Navigator checks phone or browses unrelated tabs
- Navigator only speaks when asked directly
- Navigator doesn't notice obvious typos

**Why it happens:**
- Driver is "in the zone" and moving fast
- Navigator feels their role is less important
- Fatigue from watching without typing

**Remedy:**
- Navigator: Keep a notepad for questions and observations
- Driver: Pause frequently and ask "What do you think?"
- Both: Shorter swap intervals (8-10 min) keep both engaged

---

### ⚠️ Pitfall 2: Backseat Driving

**Symptoms:**
- Navigator dictates every keystroke ("Type def, now space, now...")
- Driver feels like a typist, not a programmer
- Frustration builds on both sides

**Why it happens:**
- Navigator is impatient or thinks they know the "right" way
- Power imbalance (experience difference)

**Remedy:**
- Navigator: Give direction at the strategy level, not keystroke level
- Say "We need a function to handle the client" NOT "Type d-e-f space handle..."
- Driver: Ask Navigator to step back if feeling micromanaged

---

### ⚠️ Pitfall 3: Silent Driving

**Symptoms:**
- Driver types without explaining
- Navigator has to ask "What are you doing?" repeatedly
- Misunderstandings emerge later

**Why it happens:**
- Driver is focused and forgets to verbalise
- Assumed knowledge ("You know what I mean")

**Remedy:**
- Driver: Practise thinking aloud — it feels awkward at first but helps
- Navigator: Ask "Can you walk me through that?" when lost
- Rule: No code gets written without verbal explanation first

---

### ⚠️ Pitfall 4: Unequal Swap Time

**Symptoms:**
- One person drives most of the session
- "I'll just finish this part..." lasts 20 minutes
- One partner understands the code much better than the other

**Why it happens:**
- Natural stopping points don't align with time
- One partner is more confident/experienced

**Remedy:**
- Use a timer (phone alarm) — no exceptions
- Swap even mid-function; this forces explanation
- Experience difference? Swap more often, not less

---

### ⚠️ Pitfall 5: Solving Different Problems

**Symptoms:**
- Driver and Navigator have different understanding of the task
- Arguments about approach before code is written
- Wasted time redoing work

**Why it happens:**
- Skipped the "Review objectives together" step
- Different interpretations of requirements

**Remedy:**
- Before ANY coding: both partners state their understanding
- Navigator reads the objective aloud
- Driver summarises what they plan to build
- If descriptions differ, resolve before typing

---

### ⚠️ Pitfall 6: Fear of Looking Stupid

**Symptoms:**
- Partner doesn't admit confusion
- Questions go unasked
- Mistakes are hidden rather than discussed

**Why it happens:**
- Ego, especially with peers
- Cultural pressure to appear competent

**Remedy:**
- Explicitly normalise "I don't know" — instructors should model this
- Frame pairing as learning, not performance
- Celebrate questions: "Good question — let's figure it out together"

---

## Communication Phrases

### Navigator to Driver

| Situation | What to say |
|-----------|-------------|
| Spotted a typo | "I think there's a typo on line X" |
| Suggesting approach | "What if we tried...?" |
| Need clarification | "Can you explain why you're doing that?" |
| Reference needed | "Let me look up the syntax for that" |
| Time to swap | "Good stopping point — let's switch roles" |

### Driver to Navigator

| Situation | What to say |
|-----------|-------------|
| Thinking out loud | "I'm going to create the socket first..." |
| Asking for input | "What do you think — should we...?" |
| Stuck | "I'm not sure what to do next" |
| Verifying | "Does this look right to you?" |
| Before running | "What do you think will happen?" |

---

## Troubleshooting Together

When stuck, follow this protocol:

1. **Driver:** Explain your current understanding of the problem
2. **Navigator:** Ask clarifying questions (don't jump to solutions)
3. **Both:** Re-read the error message carefully, word by word
4. **Navigator:** Search documentation while Driver tries small tests
5. **If stuck > 5 minutes:** Call the instructor — that's what they're for!

### Common Issues This Week

| Symptom | Driver checks | Navigator checks |
|---------|---------------|------------------|
| "Address already in use" | Previous server still running? | SO_REUSEADDR set? |
| "Connection refused" | Server started? Right port? | Firewall? |
| No output from UDP | Server bound to 0.0.0.0? | Client using right port? |
| Thread not starting | `t.start()` called? | Target function correct? |

---

## End-of-Session Reflection

At the end of the session, discuss:

1. What was the hardest part of this exercise?
2. Did swapping roles feel natural? Why or why not?
3. What's one thing your partner did that helped you?
4. What would you do differently next time?
5. **Rate your collaboration:** 1 (frustrating) to 5 (excellent) — discuss why

---

## Tips for Effective Pairing

**For Drivers:**
- Verbalise your thought process
- Pause at decision points to consult Navigator
- Don't take control back if Navigator makes a suggestion
- Celebrate small wins together

**For Navigators:**
- Stay engaged — don't check your phone!
- Phrase feedback constructively ("What if..." vs "That's wrong")
- Trust the Driver to find their own path sometimes
- Keep the big picture in mind

**For both:**
- Take breaks if frustrated
- Different approaches are okay — discuss trade-offs
- Learning matters more than finishing
- Thank your partner at the end

---

*NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim*
