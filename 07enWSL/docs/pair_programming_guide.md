# 👥 Pair Programming Guide — Week 7
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## Why Pair Programming?

Pair programming improves code quality, catches errors earlier and builds communication skills essential for professional networking work. In Week 7, you will analyse packet captures and configure filtering rules — tasks that benefit from two sets of eyes.

---

## Roles

| Role | Responsibilities | Focus |
|------|-----------------|-------|
| **Driver** | Types commands, controls keyboard/mouse | Execution, syntax |
| **Navigator** | Reviews output, checks documentation, suggests next steps | Strategy, correctness |

**SWAP roles every 10-15 minutes!** Set a timer.

---

## Session Structure

### Phase 1: Setup (5 min)

- [ ] Both partners have Ubuntu terminal open
- [ ] Both can access http://localhost:9000 (Portainer)
- [ ] Decide who drives first (suggestion: less experienced partner)
- [ ] Review exercise objectives together
- [ ] **Driver:** Read the exercise aloud
- [ ] **Navigator:** Open relevant documentation

### Phase 2: Implementation (40-50 min)

Follow the exercise steps. Key behaviours:

**Driver should:**
- Think aloud: "I'm going to run tcpdump with filter X because..."
- Ask when uncertain: "Does this filter syntax look right?"
- Pause at verification points

**Navigator should:**
- Watch for typos in IP addresses and port numbers
- Track which step you're on
- Check command output against expected results
- Look up documentation when needed (man pages, cheatsheet)

### Phase 3: Review (10 min)

- [ ] Both partners can explain what each command did
- [ ] Review packet captures together in Wireshark
- [ ] Discuss: "What would happen if we changed X?"
- [ ] Document any unexpected observations

---

## Week 7 Pair Exercises

### Exercise P1: Baseline Traffic Capture

**Objective:** Establish and verify TCP/UDP connectivity with packet evidence.

**Duration:** 20 minutes (swap at 10 min)

| Phase | Driver Task | Navigator Task |
|-------|------------|----------------|
| Setup | Start lab environment | Verify Portainer shows containers running |
| Capture | Run `capture_traffic.py` | Monitor terminal for errors |
| Generate | Run `tcp_client.py` and `udp_sender.py` | Note timestamps of each command |
| Analyse | Open pcap in Wireshark | Guide filter application |

**Swap point:** After starting the capture, swap before generating traffic.

**Prediction prompt (both answer before proceeding):**
> "How many packets will we see for the TCP echo test?"

---

### Exercise P2: TCP Blocking with REJECT

**Objective:** Apply a blocking rule and observe client-side failure mode.

**Duration:** 25 minutes (swap at 12 min)

| Phase | Driver Task | Navigator Task |
|-------|------------|----------------|
| Baseline | Verify TCP echo works | Confirm expected output |
| Apply rule | Run `firewallctl.py --profile block_tcp_9090` | Read the profile JSON |
| Capture | Start new capture | Note start time |
| Test | Run `tcp_client.py` with timeout | Time how long until failure |
| Analyse | Filter for RST or ICMP packets | Document packet evidence |

**Swap point:** After applying the rule, swap before testing.

**Prediction prompt:**
> "Will the client fail immediately or timeout? What packet will Wireshark show?"

---

### Exercise P3: UDP Blocking with DROP

**Objective:** Compare DROP behaviour to REJECT behaviour.

**Duration:** 25 minutes (swap at 12 min)

| Phase | Driver Task | Navigator Task |
|-------|------------|----------------|
| Restore | Apply baseline profile | Verify UDP works first |
| Apply rule | Apply `block_udp_9091` profile | Check rule details |
| Capture | Start capture with UDP filter | Prepare to observe silence |
| Test | Run `udp_sender.py` | Note sender output |
| Analyse | Look for missing response | Compare to REJECT capture |

**Swap point:** After applying the rule, swap before sending UDP.

**Prediction prompt:**
> "The sender will report 'success'. Why? What will Wireshark show?"

---

### Exercise P4: Application-Layer Filtering

**Objective:** Use the packet filter proxy to implement allow/block lists.

**Duration:** 30 minutes (swap at 15 min)

| Phase | Driver Task | Navigator Task |
|-------|------------|----------------|
| Start server | Run `tcp_server.py` | Verify listening on 9090 |
| Start proxy | Run `packet_filter.py` on 8888 | Note proxy configuration |
| Test direct | Connect to 9090 | Confirm works |
| Test proxy | Connect to 8888 | Compare behaviour |
| Add filter | Restart proxy with `--allow` flag | Predict filter effect |
| Verify | Test allowed vs blocked sources | Document results |

**Swap point:** After starting the proxy, swap before adding filters.

**Prediction prompt:**
> "If we allow only 127.0.0.1, can a container on 10.0.7.x connect through the proxy?"

---

### Exercise P5: Defensive Port Probing

**Objective:** Verify service accessibility through systematic probing.

**Duration:** 20 minutes (swap at 10 min)

| Phase | Driver Task | Navigator Task |
|-------|------------|----------------|
| Configure | Apply `mixed_filtering` profile | Read profile rules |
| Predict | — | Write expected results for each port |
| Probe | Run `port_probe.py` | Compare results to predictions |
| Analyse | Capture during probe | Identify open/closed/filtered evidence |
| Document | Record findings | Suggest rule improvements |

**Swap point:** After configuration, swap for probing.

**Prediction prompt (Navigator writes predictions before Driver probes):**
> "For ports 22, 80, 443, 8080, 9090, 9091 — predict: open, closed, or filtered?"

---

## Communication Phrases

Use these phrases to maintain productive collaboration:

### Navigator to Driver

| Situation | Phrase |
|-----------|--------|
| Suggesting direction | "What's your plan for capturing the handshake?" |
| Asking for explanation | "Could you explain why that filter uses `tcp.flags.syn`?" |
| Spotting potential issue | "I think the port number might be wrong — can we check?" |
| Referencing docs | "The cheatsheet says `tcpdump -w` needs a filename" |
| Encouraging | "Good catch on that timeout setting" |

### Driver to Navigator

| Situation | Phrase |
|-----------|--------|
| Thinking aloud | "I'm going to try applying the DROP rule first because..." |
| Seeking confirmation | "Does this iptables syntax look right to you?" |
| Asking for help | "I'm stuck on parsing this output — can you look it up?" |
| At decision point | "Should we use REJECT or DROP here? What do you think?" |
| Sharing observation | "Look at this — the RST packet came from the firewall, not the server" |

---

## Troubleshooting Together

When stuck, follow this protocol:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 1: Driver explains current understanding                               │
│         "I expected to see RST packets but the capture is empty"           │
├─────────────────────────────────────────────────────────────────────────────┤
│ STEP 2: Navigator asks clarifying questions                                 │
│         "Are you capturing on the right interface?"                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ STEP 3: Both re-read error message or unexpected output carefully          │
│         "Wait — it says 'permission denied', not 'connection refused'"     │
├─────────────────────────────────────────────────────────────────────────────┤
│ STEP 4: Navigator searches documentation                                    │
│         "Let me check the troubleshooting guide for permission errors"     │
├─────────────────────────────────────────────────────────────────────────────┤
│ STEP 5: If stuck after 5 minutes, ask instructor                           │
│         Explain what you tried and what you observed                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Common Week 7 Pitfalls

| Problem | Solution |
|---------|----------|
| Wireshark shows no packets | Check capture interface (use vEthernet WSL) |
| "Permission denied" on tcpdump | Use `sudo` or run inside container |
| TCP client hangs forever | Check if rule is DROP (causes timeout) vs REJECT |
| UDP sender "succeeds" but receiver empty | This is expected — UDP has no delivery confirmation |
| Filter rule not applying | Run `iptables -L` to verify; check rule order |
| Capture file empty | Ensure capture started BEFORE generating traffic |

---

## End-of-Session Checklist

Before leaving:

- [ ] Both partners can explain all exercise outcomes
- [ ] Packet captures saved with descriptive names
- [ ] Any unexpected behaviour documented
- [ ] Lab environment stopped (`python3 scripts/stop_lab.py`)
- [ ] Questions for instructor noted

---

*Computer Networks — Week 7: Packet Interception, Filtering and Defensive Port Probing*  
*ASE Bucharest, CSIE | by ing. dr. Antonio Clim*
