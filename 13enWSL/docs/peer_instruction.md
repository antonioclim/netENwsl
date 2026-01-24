# 🗳️ Peer Instruction Questions — Week 13
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## Peer Instruction Protocol (5 steps)

Each question follows **5 mandatory steps**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 1 (1 min)  │  Read the question and think individually               │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 2 (30 sec) │  Vote your answer (A/B/C/D) — no discussion!            │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 3 (2 min)  │  Discuss with your neighbour — convince them!           │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 4 (30 sec) │  Re-vote — you may change your answer                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 5 (2 min)  │  Instructor explains the correct answer                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Instructor tip:** Set a visible timer for each phase. The discussion phase (Step 3) is where learning happens — resist the urge to shorten it.

---

## Question 1: MQTT Quality of Service

> 💭 **PREDICTION:** Before reading the scenario, what do you think QoS level 2 guarantees in MQTT?

### Scenario
A temperature sensor publishes readings to an MQTT broker every 5 seconds using QoS 2. The broker forwards messages to a monitoring dashboard subscribed with QoS 1.

```python
# Publisher
client.publish("sensors/temp", payload="23.5", qos=2)

# Subscriber
client.subscribe("sensors/temp", qos=1)
```

### Question
What QoS level will the dashboard actually receive messages at?

### Options
- **A)** QoS 2, because the publisher specified QoS 2 — *Misconception: publisher QoS propagates unchanged*
- **B)** QoS 1, because the effective QoS is the minimum of publisher and subscriber — *CORRECT*
- **C)** QoS 0, because different QoS levels cancel each other out — *Misconception: misunderstanding QoS negotiation*
- **D)** QoS 2 for some messages, QoS 1 for others, randomly — *Misconception: QoS is per-message lottery*

### Correct Answer
**B** — The effective QoS for message delivery is always the **minimum** of the publisher's QoS and the subscriber's QoS. Since publisher uses QoS 2 and subscriber uses QoS 1, messages arrive at QoS 1.

### Targeted Misconception
Students often believe that the publisher's QoS level determines delivery guarantees end-to-end. In reality, MQTT QoS is negotiated at each hop: publisher→broker and broker→subscriber independently.

### Instructor Notes
- **Target accuracy:** 40-50% on first vote (if >70%, question may be too easy)
- **Key concept:** QoS is negotiated per-hop, not end-to-end
- **After discussion:** Show diagram of publisher→broker→subscriber with QoS at each hop
- **Demonstration:** Run two terminals with different QoS, observe with Wireshark
- **Time allocation:** Present (1 min) → Vote (30 sec) → Discuss (2-3 min) → Revote (30 sec) → Explain (2 min)

---

## Question 2: TLS Metadata Visibility

> 💭 **PREDICTION:** If MQTT traffic is encrypted with TLS, what can an attacker who captures the packets still observe?

### Scenario
An IoT system uses MQTT over TLS (port 8883) to send sensor data. A network administrator captures traffic with Wireshark using this filter:

```
tcp.port == 8883
```

The capture shows encrypted "Application Data" records.

### Question
Which of the following can the administrator determine from the TLS-encrypted capture?

### Options
- **A)** The MQTT topic names and message payloads — *Misconception: partial encryption belief*
- **B)** Only that encrypted traffic exists, nothing else — *Misconception: TLS hides everything*
- **C)** Source/destination IPs, ports, connection timing and approximate message sizes — *CORRECT*
- **D)** The sensor values but not the topic names — *Misconception: selective encryption*

### Correct Answer
**C** — TLS encrypts the application payload (topics, messages, credentials) but network-layer metadata remains visible: IP addresses, port numbers, packet timing, connection duration and approximate sizes. This is called "metadata leakage".

### Targeted Misconception
Students often believe TLS provides complete invisibility. Understanding what TLS does and does not hide is critical for security analysis and explains why traffic analysis attacks remain possible.

### Instructor Notes
- **Target accuracy:** 35-45% on first vote
- **Key concept:** TLS encrypts content, not metadata
- **After discussion:** Compare Wireshark captures of port 1883 vs 8883 side by side
- **Follow-up:** Discuss why VPNs/Tor exist despite TLS
- **Real-world example:** Website fingerprinting attacks on HTTPS traffic

---

## Question 3: Port Scanner Results

> 💭 **PREDICTION:** What causes a port scanner to report a port as "filtered" rather than "closed"?

### Scenario
A student runs the Week 13 port scanner against a target:

```bash
python3 ex_13_01_port_scanner.py --target 10.0.13.50 --ports 22,80,443
```

Results:
```
Port 22:  open
Port 80:  closed
Port 443: filtered
```

### Question
What is the most likely explanation for port 443 showing as "filtered"?

### Options
- **A)** The service on port 443 crashed during the scan — *Misconception: filtered = service error*
- **B)** A firewall is dropping packets to port 443 without sending a response — *CORRECT*
- **C)** The port is open but requires authentication first — *Misconception: filtered = auth required*
- **D)** Port 443 is reserved for HTTPS and cannot be scanned — *Misconception: protocol restrictions*

### Correct Answer
**B** — A "filtered" result means the scanner received no response (timeout). This typically occurs when a firewall silently drops packets (DROP rule) rather than rejecting them (REJECT). A "closed" port actively responds with RST, while "filtered" means no response at all.

### Targeted Misconception
Students confuse "filtered" with "closed" or think filtered means the port has some special status. Understanding the three states (open/closed/filtered) and their network-level causes is essential for security assessment.

### Instructor Notes
- **Target accuracy:** 45-55% on first vote
- **Key concept:** filtered = no response (firewall DROP)
- **After discussion:** Show iptables DROP vs REJECT difference
- **Demonstration:** Add DROP rule, rescan, observe change
- **Command to show:** `sudo iptables -A INPUT -p tcp --dport 443 -j DROP`

---

## Question 4: MQTT Topic Wildcards

> 💭 **PREDICTION:** How do MQTT wildcard characters + and # differ in their matching behaviour?

### Scenario
A subscriber connects to an MQTT broker and subscribes to monitor building sensors:

```python
client.subscribe("building/+/temperature")
```

The following topics have active publishers:
- `building/floor1/temperature`
- `building/floor2/temperature`
- `building/floor1/humidity`
- `building/floor1/room101/temperature`
- `temperature`

### Question
Which topics will the subscriber receive messages from?

### Options
- **A)** All five topics, because + matches everything — *Misconception: + is like regex .**
- **B)** Only `building/floor1/temperature` and `building/floor2/temperature` — *CORRECT*
- **C)** The three temperature topics: floor1, floor2 and room101 — *Misconception: + matches multiple levels*
- **D)** Only `building/floor1/temperature` because + matches the first occurrence — *Misconception: + matches once globally*

### Correct Answer
**B** — The `+` wildcard matches exactly **one level** in the topic hierarchy. So `building/+/temperature` matches `building/floor1/temperature` and `building/floor2/temperature`, but NOT `building/floor1/room101/temperature` (too many levels) or `building/floor1/humidity` (wrong final segment).

### Targeted Misconception
Students often confuse MQTT wildcards with regular expressions. The `+` matches exactly one level (between slashes), while `#` matches zero or more levels but only at the end of a pattern.

### Instructor Notes
- **Target accuracy:** 40-50% on first vote
- **Key concept:** + = single level, # = multi-level (end only)
- **After discussion:** Show subscription with # and compare results
- **Exercise:** Have students predict matches for `sensors/#`
- **Common error:** Trying to use # in the middle of a pattern

---

## Question 5: IoT Security Vulnerabilities

> 💭 **PREDICTION:** What is the most common vulnerability category in IoT devices according to OWASP?

### Scenario
A security audit of an IoT deployment reveals:
- MQTT broker accepts anonymous connections
- Devices use factory-default credentials (admin/admin)
- Firmware updates transmitted over HTTP
- No encryption on sensor data transmission

```bash
# Connecting without credentials works
mosquitto_sub -h broker.local -t "#" -v
# Output: sensors/door/status open
# Output: sensors/camera/feed [binary data]
```

### Question
According to OWASP IoT Top 10, which vulnerability should be prioritised for remediation first?

### Options
- **A)** Insecure data transfer (no encryption) — *Misconception: encryption is always priority #1*
- **B)** Weak, guessable or hardcoded passwords — *CORRECT*
- **C)** Anonymous MQTT access — *Misconception: conflating authentication methods*
- **D)** Insecure firmware update mechanism — *Misconception: update security is most critical*

### Correct Answer
**B** — OWASP IoT Top 10 (2018) ranks "Weak, Guessable, or Hardcoded Passwords" as vulnerability #1. While all listed issues are serious, default credentials provide the easiest attack vector and are exploited by malware like Mirai to build massive botnets.

### Targeted Misconception
Students often prioritise encryption over authentication, but credentials are typically the weakest link. An encrypted channel with default passwords still allows unauthorised access.

### Instructor Notes
- **Target accuracy:** 50-60% on first vote
- **Key concept:** Authentication before encryption in priority
- **After discussion:** Reference Mirai botnet case study
- **Real-world:** Show Shodan searches for default credentials
- **Statistic:** Mirai infected 600,000+ devices using just 62 default username/password pairs

---

## Question 6: Concurrent Scanning Performance

> 💭 **PREDICTION:** How does increasing the number of worker threads affect port scanning speed and accuracy?

### Scenario
A student scans 1000 ports using the Week 13 port scanner with different worker configurations:

```bash
# Configuration A: 10 workers, 1.0s timeout
python3 ex_13_01_port_scanner.py --target 10.0.13.11 --ports 1-1000 --workers 10 --timeout 1.0

# Configuration B: 500 workers, 0.1s timeout  
python3 ex_13_01_port_scanner.py --target 10.0.13.11 --ports 1-1000 --workers 500 --timeout 0.1
```

Configuration A takes 100 seconds and finds 5 open ports.
Configuration B takes 2 seconds and finds 3 open ports.

### Question
Why did Configuration B miss 2 open ports?

### Options
- **A)** The target host rate-limited the connections — *Partially correct but not primary cause*
- **B)** The 0.1s timeout was too short for some services to respond — *CORRECT*
- **C)** 500 workers exceeded Python's threading limit — *Misconception: Python thread limits*
- **D)** Open ports randomly close during fast scans — *Misconception: port state volatility*

### Correct Answer
**B** — Some services take longer than 0.1 seconds to respond to connection attempts, especially under load. The scanner interpreted these slow responses as "filtered" (timeout) when they were actually open. This is a classic trade-off between scanning speed and accuracy.

### Targeted Misconception
Students assume faster scanning is always better. In reality, aggressive scanning introduces false negatives (missed open ports) and may trigger intrusion detection systems.

### Instructor Notes
- **Target accuracy:** 40-50% on first vote
- **Key concept:** Speed vs accuracy trade-off in scanning
- **After discussion:** Run both configurations live and compare results
- **Follow-up:** Discuss how IDS systems detect port scans
- **Real-world:** Nmap's timing templates (-T0 through -T5) address this trade-off

---

## Summary: Key Misconceptions Targeted

| Question | Topic | Primary Misconception |
|----------|-------|----------------------|
| Q1 | MQTT QoS | QoS is end-to-end, not per-hop |
| Q2 | TLS Security | TLS hides everything including metadata |
| Q3 | Port Scanning | Filtered means something other than firewall DROP |
| Q4 | MQTT Wildcards | + works like regex .* |
| Q5 | IoT Security | Encryption is always the top priority |
| Q6 | Scanning Performance | Faster scanning is always better |

---

## Timing Reference

| Phase | Duration | Activity |
|-------|----------|----------|
| Present question | 1 min | Read scenario and options |
| First vote | 30 sec | Individual response (A/B/C/D) |
| Peer discussion | 2-3 min | Convince your neighbour |
| Second vote | 30 sec | May change answer |
| Explanation | 2 min | Instructor reveals and explains |
| **Total per question** | **6-7 min** | |
| **All 6 questions** | **36-42 min** | |

---

## Tips for Effective Peer Instruction

### For Students
1. **Commit to your first vote** — don't wait to see what others choose
2. **Explain your reasoning** — not just your answer
3. **Listen actively** — your neighbour might know something you don't
4. **Change your mind** — if convinced by better reasoning

### For Instructors
1. **Don't reveal the answer** before the second vote
2. **Walk around** during discussion — listen for interesting arguments
3. **Call on students** to explain their reasoning after the second vote
4. **If >80% correct on first vote** — the question was too easy, move faster
5. **If <30% correct on first vote** — spend extra time on explanation

---

*Computer Networks — Week 13: IoT and Security*
*ASE Bucharest, CSIE | by ing. dr. Antonio Clim*
