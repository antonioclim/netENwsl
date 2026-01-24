# 👥 Pair Programming Guide — Week 13
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## Why Pair Programming?

Pair programming is not just about sharing a keyboard — it's a proven pedagogical technique that:
- Reduces errors through real-time code review
- Builds communication skills essential for professional environments
- Helps both partners learn through explanation and questioning
- Makes debugging faster with two perspectives

---

## Roles

| Role | Responsibilities | Focus |
|------|------------------|-------|
| **Driver** | Types code, controls keyboard and mouse | Implementation details, syntax |
| **Navigator** | Reviews each line, thinks ahead, checks docs | Strategy, error detection, research |

**⚠️ SWAP roles every 10-15 minutes!** Set a timer.

---

## Session Structure

### Phase 1: Setup (5 min)
- [ ] Both partners can access the WSL environment
- [ ] Both have the lab containers running (`python scripts/start_lab.py`)
- [ ] Decide who drives first (suggestion: less experienced partner starts)
- [ ] Review the exercise objectives together aloud

### Phase 2: Implementation (40-50 min)
- Driver types, Navigator reviews
- **Navigator responsibilities:**
  - Watch for typos and syntax errors
  - Question unclear variable names
  - Look up documentation when stuck
  - Ask "what if..." questions
  - Track progress against objectives
- **Driver responsibilities:**
  - Explain your thinking as you type
  - Pause when Navigator has questions
  - Don't rush ahead without Navigator understanding

### Phase 3: Review (10 min)
- [ ] Both partners can explain every function
- [ ] Test edge cases together
- [ ] Discuss: "What would we do differently next time?"

---

## This Week's Pair Exercises

### Exercise P1: Port Scanner Exploration
**File:** `src/exercises/ex_13_01_port_scanner.py`
**Objective:** Understand TCP connect scanning and interpret results
**Estimated time:** 25 min

#### Driver Tasks (First 12 min)
1. Run the scanner against localhost with common ports
2. Modify the `KNOWN_PORTS` dictionary to add MQTT ports
3. Implement a simple progress indicator

#### Navigator Tasks
- Verify the correct port states are being detected
- Research: What's the difference between `connect()` and `connect_ex()`?
- Watch for proper socket cleanup (`.close()` calls)

#### 🔄 Swap Point
After the scanner successfully identifies open ports on lab containers

#### Driver Tasks (After swap, 12 min)
1. Add JSON export functionality
2. Test with different timeout values
3. Add a summary statistics function

#### Navigator Tasks
- Verify JSON output is valid
- Time the scans and note performance differences
- Check error handling for invalid inputs

#### 💭 Prediction Prompts
Before running, both predict:
- "How many ports will show as open on localhost?"
- "What will happen if we set timeout to 0.01 seconds?"

---

### Exercise P2: MQTT Publish/Subscribe
**File:** `src/exercises/ex_13_02_mqtt_client.py`
**Objective:** Implement MQTT communication with QoS understanding
**Estimated time:** 30 min

#### Driver Tasks (First 15 min)
1. Connect to broker on plaintext port (1883)
2. Publish 5 temperature readings to `iot/sensors/temp`
3. Observe messages in a separate subscriber terminal

#### Navigator Tasks
- Open Wireshark and capture MQTT traffic
- Verify topic names in the capture
- Count PUBLISH and PUBACK packets for QoS 1

#### 🔄 Swap Point
After successfully publishing and receiving plaintext messages

#### Driver Tasks (After swap, 15 min)
1. Modify client to use TLS (port 8883)
2. Configure CA certificate path correctly
3. Compare Wireshark capture (encrypted vs plaintext)

#### Navigator Tasks
- Guide through TLS configuration errors
- Verify certificate file exists before running
- Document the differences observed in Wireshark

#### 💭 Prediction Prompts
- "What will Wireshark show differently for TLS traffic?"
- "If we use QoS 2, how many packets per message?"

---

### Exercise P3: Packet Sniffing
**File:** `src/exercises/ex_13_03_packet_sniffer.py`
**Objective:** Capture and analyse IoT traffic patterns
**Estimated time:** 25 min

#### Driver Tasks (First 12 min)
1. Run the sniffer with appropriate BPF filter
2. Generate MQTT traffic from another terminal
3. Modify to extract and display MQTT topics

#### Navigator Tasks
- Verify sudo/elevated privileges are being used
- Cross-reference captured packets with Wireshark
- Watch for proper error handling on permission errors

#### 🔄 Swap Point
After successfully capturing and displaying MQTT packets

#### Driver Tasks (After swap, 12 min)
1. Add payload extraction for plaintext MQTT
2. Implement packet counting statistics
3. Save capture to PCAP file

#### Navigator Tasks
- Verify PCAP file is valid (open in Wireshark)
- Check that sensitive data handling is appropriate
- Time the capture duration accuracy

#### 💭 Prediction Prompts
- "Why do we need elevated privileges for packet capture?"
- "What will we see for TLS-encrypted MQTT?"

---

### Exercise P4: Vulnerability Assessment
**File:** `src/exercises/ex_13_04_vuln_checker.py`
**Objective:** Systematic security reconnaissance
**Estimated time:** 25 min

#### Driver Tasks (First 12 min)
1. Run basic port scan on lab containers
2. Implement banner grabbing for open ports
3. Check for anonymous MQTT access

#### Navigator Tasks
- Document all findings in a structured format
- Research CVE numbers for identified services
- Ensure ethical boundaries are maintained

#### 🔄 Swap Point
After completing initial reconnaissance

#### Driver Tasks (After swap, 12 min)
1. Check DVWA for common misconfigurations
2. Test FTP anonymous access
3. Generate JSON vulnerability report

#### Navigator Tasks
- Categorise findings by severity
- Cross-reference with OWASP IoT Top 10
- Verify all tests stay within lab environment

#### 💭 Prediction Prompts
- "Which service do you predict has the most vulnerabilities?"
- "What default credentials should we test?"

---

## Communication Phrases

### Navigator → Driver

| Situation | Phrase |
|-----------|--------|
| Need clarification | "What's your plan for handling [X]?" |
| Spotted an issue | "I think line [N] might have an issue with..." |
| Suggesting improvement | "What if we tried [approach] instead?" |
| Need to slow down | "Can you walk me through that last part?" |
| Found documentation | "The docs say [X] works like..." |
| Positive feedback | "Good catch on that edge case!" |

### Driver → Navigator

| Situation | Phrase |
|-----------|--------|
| Thinking aloud | "I'm going to try [approach] because..." |
| Checking understanding | "Does this variable name make sense to you?" |
| Stuck | "I'm not sure how to [X], can you check the docs?" |
| Ready to swap | "Good stopping point — want to switch?" |
| Requesting review | "Can you trace through this function with me?" |

---

## Troubleshooting Together

### When You're Both Stuck

Follow this 5-step process:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 1  │  Driver: explain your current understanding aloud               │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 2  │  Navigator: ask clarifying questions                            │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 3  │  Both: re-read the error message very carefully                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 4  │  Navigator: search documentation or Stack Overflow              │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 5  │  If stuck > 5 min: ask instructor (describe what you tried)     │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Common Issues This Week

| Problem | Driver Action | Navigator Action |
|---------|---------------|------------------|
| Connection refused | Check container status | Verify port number in docs |
| Permission denied | Try with sudo | Check if Docker group is set |
| Module not found | Run pip install | Read requirements.txt |
| Timeout errors | Increase timeout value | Check network connectivity |
| TLS errors | Verify cert path | Check cert file exists |

---

## End of Session Checklist

- [ ] Both partners can run all exercises independently
- [ ] Code is committed/saved with both names in comments
- [ ] Key learnings documented (what surprised you?)
- [ ] Containers cleaned up (`python scripts/stop_lab.py`)
- [ ] Swap count: aimed for 3-4 swaps per session

---

## Reflection Questions

Discuss with your partner at the end of the session:

1. What was the most challenging part of today's exercises?
2. Did we swap roles frequently enough?
3. What would we do differently next time?
4. What concept became clearer through explanation?

---

*Computer Networks — Week 13: IoT and Security*
*ASE Bucharest, CSIE | by ing. dr. Antonio Clim*
