# Pair Programming Guide — Week 3

> Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## Why Pair Programming?

Pair programming is not just about writing code together — it is a proven technique that:
- Catches errors earlier (Navigator reviews in real-time)
- Deepens understanding through explanation
- Builds communication skills needed for professional work
- Reduces frustration when debugging network issues

---

## Roles

| Role | Responsibilities | Focus |
|------|------------------|-------|
| **Driver** | Types code, controls keyboard and mouse | Implementation details, syntax |
| **Navigator** | Reviews code, checks documentation, thinks ahead | Strategy, correctness, edge cases |

**Golden Rule:** The Navigator should never touch the keyboard. Communicate verbally!

**SWAP roles every 10-15 minutes** or at natural breakpoints (completing a function, fixing a bug).

---

## Session Structure

### Phase 1: Setup (5 minutes)

- [ ] Both partners can access the lab environment (WSL terminal open)
- [ ] Both can see the screen (side-by-side or screen share)
- [ ] Decide who drives first (suggestion: less experienced partner starts as Driver)
- [ ] Review the exercise objectives together
- [ ] Open relevant documentation (this guide, troubleshooting.md)

### Phase 2: Implementation (40-50 minutes)

Follow the swap schedule below for each exercise.

**Driver responsibilities:**
- Type code as discussed
- Explain what you are typing
- Ask Navigator when unsure

**Navigator responsibilities:**
- Watch for typos and syntax errors
- Check that code matches the plan
- Look up documentation when needed
- Ask "what if..." questions
- Track time for role swaps

### Phase 3: Review (10 minutes)

- [ ] Both partners can explain every line of code
- [ ] Test with edge cases (empty messages, timeouts, disconnections)
- [ ] Discuss what you learned
- [ ] Note any remaining questions for the instructor

---

## This Week's Pair Exercises

### Exercise P1: UDP Broadcast Sender/Receiver

**Objective:** Implement and test UDP broadcast communication between containers.

**Estimated time:** 25 minutes

**Starting point:** `src/exercises/ex_3_01_udp_broadcast.py`

#### Round 1 — Driver A (10 min)

**Driver task:** Implement the broadcast receiver
- Open receiver terminal: `docker exec -it week3_receiver bash`
- Examine the `cmd_recv()` function
- Start the receiver: `python3 /app/src/exercises/ex_3_01_udp_broadcast.py recv --port 5007 --count 3`

**Navigator task:**
- Open a second terminal for monitoring
- Run: `docker exec week3_receiver tcpdump -i eth0 udp port 5007`
- Verify the socket binds correctly (check for errors)
- Prepare prediction: "What source IP will we see?"

#### 🔄 SWAP ROLES

#### Round 2 — Driver B (10 min)

**Driver task:** Implement and run the broadcast sender
- Open client terminal: `docker exec -it week3_client bash`
- Start the sender: `python3 /app/src/exercises/ex_3_01_udp_broadcast.py send --dst 255.255.255.255 --port 5007 --count 3`

**Navigator task:**
- Watch the receiver terminal — do messages arrive?
- Watch tcpdump — verify broadcast address (255.255.255.255)
- Check: Does the receiver show the correct source IP?

#### 🔄 SWAP ROLES

#### Round 3 — Together (5 min)

- Discuss: Why does SO_BROADCAST need to be set?
- Try removing it and observe the error
- Document your findings

---

### Exercise P2: Multicast Group Membership

**Objective:** Configure multicast group join and observe IGMP messages.

**Estimated time:** 30 minutes

**Starting point:** `src/exercises/ex_3_02_udp_multicast.py`

#### Round 1 — Driver A (10 min)

**Driver task:** Set up the multicast receiver with group join
- Terminal: `docker exec -it week3_client bash`
- Start: `python3 /app/src/exercises/ex_3_02_udp_multicast.py recv --group 239.1.1.1 --port 5008 --count 3`

**Navigator task:**
- In another terminal, capture IGMP: `docker exec week3_client tcpdump -i eth0 igmp`
- 💭 **PREDICTION:** What IGMP message type will appear when the receiver starts?
- Verify group membership: `docker exec week3_client ip maddr show dev eth0`

#### 🔄 SWAP ROLES

#### Round 2 — Driver B (10 min)

**Driver task:** Set up a second receiver (without join) for comparison
- Terminal: `docker exec -it week3_receiver bash`
- Start receiver WITHOUT proper multicast setup (just bind to port)

**Navigator task:**
- Prepare the sender command
- 💭 **PREDICTION:** Will this receiver get the multicast messages?
- Compare `ip maddr` output between client and receiver containers

#### 🔄 SWAP ROLES

#### Round 3 — Driver A (10 min)

**Driver task:** Send multicast messages and analyse results
- Terminal: `docker exec -it week3_server bash`
- Send: `python3 /app/src/exercises/ex_3_02_udp_multicast.py send --group 239.1.1.1 --port 5008 --count 3 --ttl 4`

**Navigator task:**
- Observe which receivers get messages
- Verify prediction about IGMP (should see Membership Report)
- Discuss: What is the difference between receiver with join and without?

---

### Exercise P3: TCP Tunnel Analysis

**Objective:** Trace data flow through the TCP tunnel and count connections.

**Estimated time:** 25 minutes

**Starting point:** Understanding `src/apps/tcp_tunnel.py`

#### Round 1 — Driver A (10 min)

**Driver task:** Examine the tunnel setup
- Check tunnel is running: `docker exec week3_router ps aux | grep tcp_tunnel`
- View connections on router: `docker exec week3_router ss -tn`
- Test direct connection: `docker exec week3_client bash -c "echo 'DIRECT' | nc server 8080"`

**Navigator task:**
- 💭 **PREDICTION:** How many connections will `ss -tn` show on the router when a client connects through the tunnel?
- Prepare Wireshark filter: `tcp.port == 9090 or tcp.port == 8080`
- Start Wireshark capture on vEthernet (WSL)

#### 🔄 SWAP ROLES

#### Round 2 — Driver B (10 min)

**Driver task:** Send data through the tunnel
- Run: `docker exec week3_client bash -c "echo 'TUNNEL TEST' | nc router 9090"`
- Immediately check: `docker exec week3_router ss -tn`

**Navigator task:**
- Count connections in `ss` output (should be 2: client↔router, router↔server)
- In Wireshark, identify the two separate TCP handshakes
- Note the different port pairs

#### 🔄 SWAP ROLES

#### Round 3 — Together (5 min)

- Draw a diagram of the connection flow
- Discuss: Why does the tunnel create two connections?
- Discuss: What happens if the server is down?

---

## Communication Phrases

### Navigator to Driver

| Situation | Phrase |
|-----------|--------|
| Planning | "What is your plan for this function?" |
| Clarification | "Could you explain that line?" |
| Spotted issue | "I think there might be an issue with..." |
| Found info | "The documentation says..." |
| Suggestion | "What if we tried..." |
| Time check | "We should swap roles in 2 minutes" |

### Driver to Navigator

| Situation | Phrase |
|-----------|--------|
| Starting | "I am going to start by..." |
| Checking | "Does this look right?" |
| Stuck | "I am stuck on..." |
| Need help | "Can you look up what [function] does?" |
| Thinking | "Give me a moment to think about this" |

---

## Troubleshooting Together

When you get stuck:

1. **Driver:** Explain your current understanding out loud
2. **Navigator:** Ask clarifying questions (not leading questions)
3. **Both:** Re-read the error message carefully, word by word
4. **Navigator:** Search documentation (`docs/troubleshooting.md`)
5. **Swap roles:** Fresh perspective often helps
6. **If stuck for more than 5 minutes:** Ask the instructor

### Common Pair Programming Pitfalls

| Problem | Solution |
|---------|----------|
| Navigator grabs keyboard | Verbal communication only! |
| Driver ignores Navigator | Pause and discuss before proceeding |
| One person dominates | Set a timer, enforce swaps |
| Both get stuck silently | Talk through the problem out loud |
| Frustration building | Take a 2-minute break, then swap roles |

---

## Role Swap Checklist

When swapping roles:

- [ ] Driver saves current work
- [ ] Driver explains current state to Navigator
- [ ] New Driver reviews the code before continuing
- [ ] New Navigator opens relevant documentation
- [ ] Both agree on the next goal

---

## End of Session Reflection

Discuss with your partner:

1. What did we learn that we did not know before?
2. What was the most confusing part?
3. How did pair programming help (or hinder) us?
4. What would we do differently next time?

---

*Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim*
