# 📋 Assessment Rubric — Week 13

## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Evaluation criteria for Week 13 laboratory exercises and self-assessment checklist.

---

## Exercise Evaluation Criteria

### Exercise 1: TCP Port Scanner

| Criterion | Excellent (9-10) | Good (7-8) | Adequate (5-6) | Needs Work (<5) |
|-----------|------------------|------------|----------------|-----------------|
| **Functionality** | Scans all specified ports correctly, handles all edge cases | Scans ports correctly, minor edge case issues | Basic scanning works, some ports missed | Does not scan correctly |
| **Concurrency** | Efficient ThreadPoolExecutor usage, configurable workers | Uses threading, reasonable performance | Sequential scanning, slow but works | No concurrency or crashes |
| **Output Quality** | JSON export complete, well-formatted, includes all data | JSON export works, minor formatting issues | Basic output, missing some fields | No structured output |
| **Error Handling** | Graceful handling of timeouts, refused connections, network errors | Handles common errors | Some error handling | Crashes on errors |
| **Code Quality** | Clear structure, good documentation, type hints | Readable code, some documentation | Works but hard to follow | Poor structure |

### Exercise 2: MQTT Client

| Criterion | Excellent (9-10) | Good (7-8) | Adequate (5-6) | Needs Work (<5) |
|-----------|------------------|------------|----------------|-----------------|
| **Plaintext Mode** | Publish and subscribe work flawlessly | Both modes work with minor issues | One mode works correctly | Neither mode works |
| **TLS Mode** | TLS connections work with proper certificate verification | TLS works with some configuration help | TLS connects but verification issues | TLS does not work |
| **QoS Understanding** | Correctly explains and demonstrates all QoS levels | Understands QoS 0 and 1 | Basic QoS understanding | Confused about QoS |
| **Topic Wildcards** | Correctly uses + and # wildcards | Uses wildcards with minor errors | Basic wildcard usage | Does not understand wildcards |
| **Traffic Analysis** | Can identify MQTT packets in Wireshark, compare encrypted vs plain | Identifies basic MQTT traffic | Sees traffic but cannot analyse | Cannot capture traffic |

### Exercise 3: Packet Sniffer

| Criterion | Excellent (9-10) | Good (7-8) | Adequate (5-6) | Needs Work (<5) |
|-----------|------------------|------------|----------------|-----------------|
| **Capture Ability** | Captures traffic on correct interface, applies filters | Captures traffic with some guidance | Basic capture works | Cannot capture |
| **Protocol Identification** | Identifies MQTT, HTTP, FTP traffic patterns | Identifies most protocols | Identifies some traffic | Cannot distinguish protocols |
| **TLS vs Plaintext** | Clearly explains what is visible in each mode | Understands the difference | Partial understanding | Does not understand |
| **Analysis Skills** | Uses display filters effectively, follows streams | Basic filter usage | Minimal filtering | No filtering ability |

### Exercise 4: Vulnerability Checker

| Criterion | Excellent (9-10) | Good (7-8) | Adequate (5-6) | Needs Work (<5) |
|-----------|------------------|------------|----------------|-----------------|
| **Service Detection** | Correctly identifies all lab services and versions | Identifies most services | Identifies some services | Cannot identify services |
| **Vulnerability Awareness** | Understands CVEs, explains risks appropriately | Knows about vulnerabilities | Basic awareness | No understanding |
| **Report Quality** | Structured JSON report with severity ratings | Basic report with findings | Incomplete report | No report generated |
| **Ethical Understanding** | Clearly articulates ethical boundaries | Understands basic ethics | Partial understanding | Does not consider ethics |

---

## Self-Assessment Checklist

Use this checklist before submitting or at the end of the laboratory session.

### Technical Skills

- [ ] I can start and stop the laboratory environment using the provided scripts
- [ ] I can verify container status using `docker ps` and Portainer
- [ ] I understand the difference between plaintext (1883) and TLS (8883) MQTT
- [ ] I can capture network traffic with Wireshark or the packet sniffer script
- [ ] I can identify open, closed and filtered port states
- [ ] I can explain what information TLS hides and what it does not

### Conceptual Understanding

- [ ] I can explain the MQTT publish/subscribe model without looking at notes
- [ ] I understand QoS levels 0, 1 and 2 and when to use each
- [ ] I know how MQTT topic wildcards (+ and #) work
- [ ] I can describe the TLS handshake in simple terms
- [ ] I understand why default credentials are a critical vulnerability
- [ ] I can explain the difference between vulnerability scanning and exploitation

### Practical Application

- [ ] I completed all four exercises successfully
- [ ] I generated JSON output files in the artifacts directory
- [ ] I captured at least one pcap file for analysis
- [ ] I can demonstrate the MQTT client to a peer
- [ ] I followed the pair programming protocol during the session

### Documentation and Communication

- [ ] I documented any issues encountered and how I resolved them
- [ ] I can explain my code to someone else
- [ ] I reviewed the troubleshooting guide when stuck
- [ ] I asked for help appropriately (after trying for 5+ minutes)

---

## Grading Scale

| Grade | Points | Description |
|-------|--------|-------------|
| **A** | 90-100 | All exercises completed excellently, deep understanding demonstrated |
| **B** | 80-89 | All exercises completed well, good understanding |
| **C** | 70-79 | Most exercises completed, adequate understanding |
| **D** | 60-69 | Some exercises completed, basic understanding |
| **F** | <60 | Insufficient completion or understanding |

---

## Common Deductions

| Issue | Deduction | How to Avoid |
|-------|-----------|--------------|
| Missing JSON output files | -5 points | Run exercises with `--json-out` flag |
| No pcap captures | -5 points | Run packet sniffer during exercises |
| Cannot explain own code | -10 points | Use pair programming, discuss with partner |
| Ethical violation (scanning without permission) | -20 points | Only scan laboratory environment |
| Plagiarism | -100 points | Write your own code, cite sources |

---

## Feedback Request

After completing the exercises, consider these reflection questions:

1. What was the most challenging part of this laboratory?
2. What concept became clearer after the hands-on practice?
3. What would you like to explore further?
4. How could the laboratory materials be improved?

Share your feedback with your instructor or via the course platform.

---

*Computer Networks — Week 13: IoT and Security*
*ASE Bucharest, CSIE | by ing. dr. Antonio Clim*
