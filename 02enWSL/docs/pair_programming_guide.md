# 👥 Pair Programming Guide — Week 2: Socket Programming

> NETWORKING class — ASE, CSIE Bucharest  
> Computer Networks Laboratory | by ing. dr. Antonio Clim

---

## Why Pair Programming?

Research shows pair programming improves code quality and learning outcomes, particularly for networking concepts where debugging requires understanding both code AND protocol behaviour.

**Benefits for socket programming:**
- One person codes while the other monitors Wireshark
- Driver focuses on syntax; Navigator catches logical errors
- Discussion clarifies TCP vs UDP mental models
- Two pairs of eyes catch off-by-one and boundary errors

---

## Roles and Responsibilities

| Role | Responsibilities | Focus |
|------|-----------------|-------|
| **Driver** | Types code, controls keyboard/mouse, executes commands | Syntax, implementation |
| **Navigator** | Reviews code, checks documentation, monitors output | Logic, strategy, Wireshark |

### Driver Guidelines

- Think aloud as you type
- Ask Navigator before major decisions
- Don't race ahead — explain your plan
- Accept Navigator suggestions gracefully

### Navigator Guidelines

- Watch for typos and bugs
- Keep documentation open
- Monitor Wireshark/logs for unexpected behaviour
- Suggest improvements without grabbing keyboard
- Track time for swaps

---

## Swap Schedule

**CRITICAL: Swap roles every 10-15 minutes!**

| Time | Activity | Swap Point |
|------|----------|------------|
| 0:00-0:10 | Setup and TCP server start | ⟳ SWAP |
| 0:10-0:20 | TCP client and first test | ⟳ SWAP |
| 0:20-0:30 | Threaded vs iterative comparison | ⟳ SWAP |
| 0:30-0:40 | UDP server implementation | ⟳ SWAP |
| 0:40-0:50 | UDP client and testing | ⟳ SWAP |
| 0:50-1:00 | Wireshark analysis | ⟳ SWAP |

**Timer recommendation:** Use phone timer set to 10 minutes.

---

## Week 2 Specific Sessions

### Session 1: TCP Server (25 min)

#### Phase 1: Server Setup (Driver A, Navigator B)

**Driver task:** Type the server startup code
```bash
cd /mnt/d/NETWORKING/WEEK2/2enWSL
python3 src/exercises/ex_2_01_tcp.py server --port 9090 --mode threaded
```

**Navigator task:** 
- Open Wireshark on vEthernet (WSL)
- Set filter: `tcp.port == 9090`
- Start capture
- **WATCH FOR:** Server should NOT generate packets yet

**⟳ SWAP after:** Server shows "Waiting for connections..."

---

#### Phase 2: Client Testing (Driver B, Navigator A)

**Driver task:** Run client and send test message
```bash
python3 src/exercises/ex_2_01_tcp.py client --host 127.0.0.1 --port 9090 -m "Hello"
```

**Navigator task:**
- Watch terminal for response
- Check Wireshark for handshake (SYN → SYN-ACK → ACK)
- Count packets: should see ~7-10 (handshake + data + FIN)

**💭 PREDICTION prompt:** How many packets total? Discuss before checking.

**⟳ SWAP after:** Successful response received

---

#### Phase 3: Mode Comparison (Driver A, Navigator B)

**Driver task:** Restart server in iterative mode and run load test
```bash
# Terminal 1: Restart server
python3 src/exercises/ex_2_01_tcp.py server --port 9090 --mode iterative

# Terminal 2: Load test
python3 src/exercises/ex_2_01_tcp.py load --host 127.0.0.1 --port 9090 --clients 5
```

**Navigator task:**
- Note the total time reported
- Predict: ~500ms for iterative (5 × 100ms)
- Compare with threaded mode (~100ms)

**Discussion:** Why is threaded faster? Navigator explains to Driver.

---

### Session 2: UDP Server (20 min)

#### Phase 1: UDP Server (Driver B, Navigator A)

**Driver task:**
```bash
python3 src/exercises/ex_2_02_udp.py server --port 9091
```

**Navigator task:**
- Clear Wireshark
- Set filter: `udp.port == 9091`
- **WATCH FOR:** No packets on server start (same as TCP)

**⟳ SWAP after:** Server shows "Listening..."

---

#### Phase 2: Interactive Testing (Driver A, Navigator B)

**Driver task:**
```bash
python3 src/exercises/ex_2_02_udp.py client --host 127.0.0.1 --port 9091 -i
```

Then type commands:
```
> ping
> upper:hello world
> time
> exit
```

**Navigator task:**
- Count packets per command (should be 2: request + response)
- Compare with TCP packet count
- Note: NO handshake packets!

**Discussion:** Why fewer packets than TCP?

---

### Session 3: Wireshark Analysis (25 min)

#### Phase 1: TCP Capture (Driver B, Navigator A)

**Driver task:** Generate complete TCP session while Navigator captures

**Navigator task:**
1. Start fresh capture
2. After session completes, stop capture
3. Right-click a packet → Follow → TCP Stream
4. Save as: `pcap/tcp_session.pcap`

**⟳ SWAP after:** Capture saved

---

#### Phase 2: Analysis Discussion (Both)

Work together to answer:
1. How many SYN packets? (Should be 1)
2. How many data packets?
3. What is the TCP header overhead per segment?
4. Identify the FIN sequence

---

## Communication Phrases

### Navigator to Driver

| Situation | Say this |
|-----------|----------|
| Spot a typo | "I think there's a typo in line X" |
| Suggest approach | "What if we tried..." |
| Need clarification | "Can you explain your plan for this part?" |
| Time check | "We should swap in 2 minutes" |
| Wireshark finding | "I see something interesting — pause a moment" |

### Driver to Navigator

| Situation | Say this |
|-----------|----------|
| Stuck | "I'm not sure how to... what do you think?" |
| Explaining | "I'm going to try X because..." |
| Finished step | "Does this look right before I continue?" |
| Need doc | "Can you look up the syntax for...?" |

---

## Conflict Resolution

### When you disagree on approach

1. **State positions:** Each person explains their reasoning (30 sec each)
2. **Quick experiment:** If fast to test, try both and compare
3. **Time-box:** If neither is obviously better, pick one and move on
4. **Document:** Note the alternative for later consideration

### When stuck together

1. **Re-read the error message** — slowly, word by word
2. **Check troubleshooting guide:** [docs/troubleshooting.md](troubleshooting.md)
3. **Review misconceptions:** [docs/misconceptions.md](misconceptions.md)
4. **5-minute rule:** If still stuck after 5 min, ask instructor

### When pace differs

- Faster partner: Practice patience, focus on teaching
- Slower partner: Ask questions freely, don't apologise
- Both: Adjust swap frequency if needed

---

## Post-Session Reflection

At the end of your pair session, discuss:

1. What worked well in our collaboration?
2. What would we do differently next time?
3. What concept became clearer through discussion?
4. Did we swap roles frequently enough?

---

## Assessment Rubric (for graded pair work)

| Criterion | Excellent | Good | Needs Work |
|-----------|-----------|------|------------|
| **Role switching** | Swapped every 10-15 min | Swapped 2-3 times | Rarely swapped |
| **Communication** | Constant dialogue | Regular discussion | Mostly silent |
| **Code quality** | Both understand all code | Minor gaps | One person dominated |
| **Problem solving** | Collaborative debugging | Some joint effort | Individual work |
| **Time management** | Completed all tasks | Most tasks done | Behind schedule |

---

## Tips from Past Students

> "Having one person watch Wireshark while the other codes is a game-changer. You catch timing issues immediately."

> "We found that swapping after each successful test worked better than fixed time intervals."

> "The Navigator should actually navigate — keep the documentation open!"

---

*NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim*
