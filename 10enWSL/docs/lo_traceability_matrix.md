# 📊 Learning Objectives Traceability Matrix — Week 10
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Complete traceability from Learning Objectives to all course artefacts

---

## Traceability Matrix

This matrix provides complete verification of LO coverage across all course materials.

### Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Primary coverage |
| 🔗 | Supporting coverage |
| 📝 | Assessment item |
| 🧪 | Practical verification |

---

### Full Traceability Matrix

| LO | Bloom | Theory | Analogy | Exercise | Test | Quiz | Misconception | Peer Q | Parsons | Homework | Commands |
|----|-------|--------|---------|----------|------|------|---------------|--------|---------|----------|----------|
| **LO1** | Understand | ✅ theory_summary.md#tls | ✅ concept_analogies.md#https | ✅ ex_10_01 | 🧪 test_5 | 📝 q01,q02 | ✅ M1,M2 | 📝 Q1,Q5 | 📝 P1,P5 | 🔗 hw_10_01 | ✅ curl |
| **LO2** | Analyse | ✅ theory_summary.md#rest | ✅ concept_analogies.md#rest | ✅ ex_10_02 | 🧪 test_6 | 📝 q03-q05 | ✅ M4,M5,M6 | 📝 Q2 | 📝 P3 | ✅ hw_10_02 | ✅ curl |
| **LO3** | Analyse | ✅ theory_summary.md#dns | ✅ concept_analogies.md#dns | ✅ ex_10_03 | 🧪 test_2 | 📝 q06,q07 | ✅ M7,M8 | 📝 Q3 | 📝 P2 | ✅ hw_10_03 | ✅ dig |
| **LO4** | Apply | ✅ theory_summary.md#protocols | 🔗 concept_analogies.md | ✅ ex_10_04 | 🧪 test_3,4 | 📝 q08 | ✅ M11,M12 | 📝 Q4 | 📝 P4 | — | ✅ ssh,ftp |
| **LO5** | Evaluate | ✅ theory_summary.md#security | 🔗 concept_analogies.md | 🔗 ex_10_01 | 🧪 test_5 | 📝 q09,q10 | ✅ M9,M10 | 📝 Q1 | — | 🔗 hw_10_01 | ✅ wireshark |

---

### Artefact File Locations

| Artefact Type | File Path | Description |
|---------------|-----------|-------------|
| Theory Summary | `docs/theory_summary.md` | Conceptual explanations |
| Concept Analogies | `docs/concept_analogies.md` | CPA methodology analogies |
| Exercises | `src/exercises/ex_10_0*.py` | Hands-on Python exercises |
| Tests | `tests/test_exercises.py` | Automated verification |
| Formative Quiz | `formative/quiz.yaml` | Self-assessment questions |
| Misconceptions | `docs/misconceptions.md` | Common errors and corrections |
| Peer Instruction | `docs/peer_instruction.md` | Discussion questions |
| Parsons Problems | `docs/parsons_problems.md` | Code ordering exercises |
| Homework | `homework/exercises/hw_10_0*.py` | Take-home assignments |
| Commands | `docs/commands_cheatsheet.md` | Quick reference |

---

### Coverage Statistics

| Metric | Count | Coverage |
|--------|-------|----------|
| Learning Objectives | 5 | 100% |
| Theory sections | 5 | 100% |
| Analogies | 5 | 100% |
| Exercises | 4 | 80% (LO4 combines SSH/FTP) |
| Quiz questions (standard) | 10 | 100% |
| Quiz questions (live) | 5 | 100% |
| Misconceptions | 12 | 100% |
| Peer questions | 5 | 100% |
| Parsons problems | 5 | 100% |
| Homework assignments | 3 | 60% (LO4/LO5 optional) |

---

### Verification Commands by LO

#### LO1: TLS Certificates

```bash
# Generate certificate
python3 src/exercises/ex_10_01_tls_rest_crud.py generate-cert

# Test HTTPS server
python3 src/exercises/ex_10_01_tls_rest_crud.py selftest

# Verify SNI visibility (Wireshark)
tshark -r capture.pcap -Y "tls.handshake.extensions_server_name"
```

#### LO2: REST Richardson Levels

```bash
# Start REST server
python3 src/exercises/ex_10_02_richardson_maturity.py serve

# Test all levels
curl -X POST http://localhost:5000/level0/service -d '{"action":"list"}'
curl http://localhost:5000/level2/users
curl http://localhost:5000/level3/users | jq '._links'
```

#### LO3: DNS Structure

```bash
# Query lab DNS
dig @127.0.0.1 -p 5353 web.lab.local +short

# Force TCP
dig @127.0.0.1 -p 5353 web.lab.local +tcp

# Full query details
dig @127.0.0.1 -p 5353 web.lab.local +noall +answer +authority +additional
```

#### LO4: Protocol Clients

```bash
# SSH connection
ssh -p 2222 labuser@localhost

# FTP connection
ftp localhost 2121

# Run exercise
python3 src/exercises/ex_10_04_secure_transfer.py demo
```

#### LO5: Security Evaluation

```bash
# Compare HTTP vs HTTPS traffic
tcpdump -i any port 8000 -w http.pcap
tcpdump -i any port 8443 -w https.pcap

# Analyse in Wireshark
wireshark http.pcap https.pcap
```

---

### Assessment Alignment

| Assessment Type | LO1 | LO2 | LO3 | LO4 | LO5 | Weight |
|-----------------|-----|-----|-----|-----|-----|--------|
| Lab Exercises | ✅ | ✅ | ✅ | ✅ | 🔗 | 40% |
| Formative Quiz | ✅ | ✅ | ✅ | ✅ | ✅ | 20% |
| Live Verification | ✅ | ✅ | ✅ | ✅ | ✅ | 20% |
| Homework | ✅ | ✅ | ✅ | — | 🔗 | 20% |

---

### Anti-AI Verification Mapping

| LO | Live Quiz Question | Verification Method |
|----|-------------------|---------------------|
| LO1 | q_live_03 | HTTPS server response verification |
| LO2 | q_live_04 | Web server content check |
| LO3 | q_live_01 | DNS query to lab server |
| LO4 | q_live_02 | SSH container hostname |
| LO5 | q_live_05 | Docker container listing |

---

*Computer Networks — Week 10 | ASE, CSIE Bucharest*
*Laboratory materials by ing. dr. Antonio Clim*
