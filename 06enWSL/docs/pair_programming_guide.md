# 👥 Pair Programming Guide — Week 6

## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## Roles

| Role | Responsibilities | Duration |
|------|-----------------|----------|
| **Driver** | Types commands, controls keyboard/mouse | 10-15 min |
| **Navigator** | Reviews output, checks documentation, suggests next steps | 10-15 min |

**SWAP roles every 10-15 minutes!** Set a timer.

---

## Session Structure

### Phase 1: Setup (5 min)

- [ ] Both partners can access the lab environment
- [ ] Decide who drives first (suggestion: less experienced partner drives first)
- [ ] Review the exercise objectives together
- [ ] Open relevant documentation: `docs/commands_cheatsheet.md`, `docs/glossary.md`

### Phase 2: Implementation (40-50 min)

- Driver types, Navigator reviews
- Navigator should:
  - Watch for typos in IP addresses and commands
  - Keep track of what step you're on
  - Look up documentation when stuck
  - Ask "what if..." questions to deepen understanding
  - Note observations for later discussion

### Phase 3: Review (10 min)

- [ ] Both partners can explain what each command did
- [ ] Discuss: "What would happen if we changed X?"
- [ ] Identify any remaining questions for the instructor

---

## Common Mistakes Pairs Make

### ❌ Mistake 1: Navigator goes passive

**Problem:** Navigator stops paying attention, checks phone, or waits silently.

**Fix:** Navigator should constantly ask questions:
- "What do you expect to happen?"
- "Can you explain that command?"
- "Should we check the documentation first?"

### ❌ Mistake 2: Driver ignores Navigator

**Problem:** Driver rushes ahead without listening to Navigator's suggestions.

**Fix:** Driver should:
- Verbalise what they're doing: "I'm going to run ping now..."
- Pause before pressing Enter: "Does this look right?"
- Welcome corrections: "Good catch! Let me fix that."

### ❌ Mistake 3: Skipping predictions

**Problem:** Pair runs commands without predicting outcomes first.

**Fix:** Before EVERY command, Navigator asks: "What do you predict will happen?"

### ❌ Mistake 4: Not swapping roles

**Problem:** Same person drives for 30+ minutes; other person disengages.

**Fix:** Set a phone timer for 12 minutes. When it beeps, SWAP. No exceptions.

### ❌ Mistake 5: Both partners look at different screens

**Problem:** Each person works on their own laptop; no collaboration.

**Fix:** Use ONE computer. The other laptop is only for documentation.

### ❌ Mistake 6: Copying commands without understanding

**Problem:** Pair copies from README without discussing what each part does.

**Fix:** Navigator asks: "What does the `-n` flag do?" If unsure, look it up together.

---

## This Week's Pair Exercises

### Exercise P1: NAT Configuration (40 min)

**Objective:** Configure and observe NAT/PAT translation

**Swap Points:**
1. First swap: After starting topology and verifying interfaces
2. Second swap: After running NAT observer server
3. Third swap: After analysing conntrack table

#### Driver Tasks (First Rotation)

```bash
# Start the NAT topology
python scripts/run_demo.py --demo nat

# Inside Mininet, check router interfaces
rnat ifconfig
rnat iptables -t nat -L -n -v
```

💭 **Navigator:** Before Driver runs `ifconfig`, predict what IPs you'll see on each interface.

#### Navigator Tasks (First Rotation)

- Verify the IP addresses match the topology diagram in README.md
- Note which interface is private (192.168.1.x) and which is public (203.0.113.x)
- Check if MASQUERADE rule is present in iptables output

#### Driver Tasks (Second Rotation — after swap)

```bash
# Start server on h3
h3 python3 src/apps/nat_observer.py server --bind 203.0.113.2 --port 5000

# Send messages from h1 and h2
h1 python3 src/apps/nat_observer.py client --host 203.0.113.2 --port 5000 --msg "Hello from h1"
h2 python3 src/apps/nat_observer.py client --host 203.0.113.2 --port 5000 --msg "Hello from h2"
```

💭 **Navigator:** Before running clients, predict what source IP the server will see.

#### Navigator Tasks (Second Rotation)

- Record the source IP:port shown by the server for each client
- Verify both show 203.0.113.1 (NAT public IP)
- Note the different source ports

#### Driver Tasks (Third Rotation — after swap)

```bash
# Check NAT translation table
rnat conntrack -L 2>/dev/null || rnat cat /proc/net/nf_conntrack
```

#### Navigator Tasks (Third Rotation)

- Count entries in conntrack table
- Identify which entry corresponds to h1 and which to h2
- Explain to your partner how return traffic finds its way back

---

### Exercise P2: SDN Flow Observation (35 min)

**Objective:** Observe SDN flow installation and policy enforcement

**Swap Points:**
1. First swap: After examining initial flow table
2. Second swap: After testing permitted traffic (h1↔h2)
3. Third swap: After testing blocked traffic (h1→h3)

#### Driver Tasks (First Rotation)

```bash
# Start SDN topology
python scripts/run_demo.py --demo sdn

# Check initial flow table
sh ovs-ofctl -O OpenFlow13 dump-flows s1
```

💭 **Navigator:** How many flows do you expect to see initially?

#### Navigator Tasks (First Rotation)

- Count the number of flow entries
- Identify the table-miss rule (priority=0, actions=CONTROLLER)
- Note any pre-installed policy rules

#### Driver Tasks (Second Rotation — after swap)

```bash
# Test h1 ↔ h2 connectivity
h1 ping -c 3 10.0.6.12
h2 ping -c 3 10.0.6.11

# Check flows again
sh ovs-ofctl -O OpenFlow13 dump-flows s1
```

💭 **Navigator:** Did new flows appear? What do they match on?

#### Navigator Tasks (Second Rotation)

- Compare flow count before and after pings
- Identify new flows installed for h1↔h2 traffic
- Note the packet counters (n_packets=)

#### Driver Tasks (Third Rotation — after swap)

```bash
# Test blocked traffic
h1 ping -c 3 10.0.6.13

# Check flows and statistics
sh ovs-ofctl -O OpenFlow13 dump-flows s1 --rsort=n_packets
```

#### Navigator Tasks (Third Rotation)

- Verify ping fails (100% packet loss)
- Find the drop rule for h3 traffic
- Compare packet counters to see how many were dropped

---

### Exercise P3: SDN Policy Modification (25 min)

**Objective:** Dynamically modify SDN policies

**Swap Points:**
1. First swap: After adding permit rule
2. Second swap: After removing permit rule

#### Driver Tasks (First Rotation)

```bash
# Add rule to permit ICMP from h1 to h3
sh ovs-ofctl -O OpenFlow13 add-flow s1 "priority=300,icmp,nw_src=10.0.6.11,nw_dst=10.0.6.13,actions=output:3"

# Test connectivity
h1 ping -c 3 10.0.6.13

# Check the new flow
sh ovs-ofctl -O OpenFlow13 dump-flows s1 | grep "priority=300"
```

💭 **Navigator:** Why did we use priority=300? What if we used priority=20?

#### Navigator Tasks (First Rotation)

- Verify ping now succeeds
- Explain to partner why priority=300 overrides the drop rule
- Calculate: if drop rule is priority=30, would priority=25 work?

#### Driver Tasks (Second Rotation — after swap)

```bash
# Remove the permit rule
sh ovs-ofctl -O OpenFlow13 del-flows s1 "priority=300,icmp,nw_src=10.0.6.11,nw_dst=10.0.6.13"

# Verify blocking resumes
h1 ping -c 3 10.0.6.13

# Confirm rule is gone
sh ovs-ofctl -O OpenFlow13 dump-flows s1 | grep "priority=300"
```

#### Navigator Tasks (Second Rotation)

- Verify ping fails again
- Confirm no priority=300 rule exists
- Discuss: What's the benefit of dynamic policy changes?

---

## Communication Phrases

### Navigator to Driver

- "What's your plan for this step?"
- "Can you explain what that command does?"
- "I think there might be a typo in the IP address..."
- "The documentation says we should see..."
- "Let's check the expected output before running this"
- "What do you predict will happen?"

### Driver to Navigator

- "I'm going to try..."
- "Does this output look correct to you?"
- "I'm not sure what to do next..."
- "Can you look up what [command/option] does?"
- "My prediction was X, but we got Y. Why?"

---

## Troubleshooting Together

When stuck:

1. **Driver:** Explain your current understanding out loud
2. **Navigator:** Ask clarifying questions
3. **Both:** Re-read the error message carefully — what does it actually say?
4. **Navigator:** Search documentation or `docs/troubleshooting.md`
5. **Driver:** Try a simpler version of the command
6. **If still stuck after 5 min:** Ask the instructor

### Common Issues This Week

| Problem | Quick Check |
|---------|-------------|
| "No such container" | Did you start the topology? |
| Ping timeout in NAT | Is IP forwarding enabled? (`sysctl net.ipv4.ip_forward`) |
| No flows in SDN | Is the controller connected? (`ovs-vsctl show`) |
| Command not found | Are you in the right host? (h1/h2/h3/rnat/sh) |

---

## Reflection Questions (End of Session)

Discuss with your partner:

1. What was the most surprising thing you learned today?
2. Which misconception (from `docs/misconceptions.md`) did you have before this lab?
3. If you had to explain NAT to a non-technical friend, what analogy would you use?
4. What's one thing you want to explore further?

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
