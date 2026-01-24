# 🎯 Learning Objectives — Week 10
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> HTTP/HTTPS, REST Architecture and Network Services

This document provides complete traceability from Learning Objectives to all course artefacts.

---

## Overview

Week 10 covers Application Layer Protocols with five core learning objectives aligned to Bloom's Taxonomy levels 2-5 (Understand through Evaluate).

| LO | Bloom Level | Verb | Topic |
|----|-------------|------|-------|
| LO1 | 2 (Understand) | Explain | TLS certificates in HTTPS |
| LO2 | 4 (Analyse) | Compare | REST API Richardson levels |
| LO3 | 4 (Analyse) | Analyse | DNS query/response structure |
| LO4 | 3 (Apply) | Implement | Protocol clients (HTTP, DNS, SSH, FTP) |
| LO5 | 5 (Evaluate) | Evaluate | Encrypted vs unencrypted security |

---

## LO1: Explain TLS Certificates in HTTPS

> **By the end of this lab, students will be able to explain the role of TLS certificates in HTTPS communication.**

### Artefact Mapping

| Artefact Type | Location | Description |
|---------------|----------|-------------|
| **Theory** | `docs/theory_summary.md#tls-https` | TLS handshake, certificate chain |
| **Analogy** | `docs/concept_analogies.md#https-passport` | "HTTPS is like a passport checkpoint" |
| **Lab Exercise** | `src/exercises/ex_10_01_tls_rest_crud.py` | Generate self-signed certificate, HTTPS server |
| **Test** | `tests/test_exercises.py::test_exercise_5` | HTTPS selftest verification |
| **Quiz** | `formative/quiz.yaml` q01, q02 | SNI visibility, symmetric vs asymmetric |
| **Misconception** | `docs/misconceptions.md#misconception-1` | "HTTPS encrypts everything including domain" |
| **Misconception** | `docs/misconceptions.md#misconception-2` | "HTTPS means the site is trustworthy" |
| **Peer Instruction** | `docs/peer_instruction.md` Q1, Q5 | SNI privacy, TLS handshake purpose |
| **Parsons** | `docs/parsons_problems.md` P1, P5 | HTTPS client, certificate verification |
| **Code Tracing** | `docs/code_tracing.md` Exercise 1 | TLS context setup |
| **Commands** | `docs/commands_cheatsheet.md#curl` | curl -k, --cacert options |

### Success Criteria

Students can:
- [ ] Generate a self-signed TLS certificate using OpenSSL
- [ ] Start an HTTPS server with the generated certificate
- [ ] Explain what SNI reveals during TLS handshake
- [ ] Describe why symmetric encryption is used for bulk data

### Verification Commands

```bash
# Generate certificate
python3 src/exercises/ex_10_01_tls_rest_crud.py generate-cert

# Test HTTPS server
python3 src/exercises/ex_10_01_tls_rest_crud.py selftest

# Verify SNI in Wireshark
# Filter: ssl.handshake.extensions_server_name
```

---

## LO2: Compare REST API Designs

> **By the end of this lab, students will be able to compare REST API designs across Richardson Maturity Model levels.**

### Artefact Mapping

| Artefact Type | Location | Description |
|---------------|----------|-------------|
| **Theory** | `docs/theory_summary.md#rest-richardson` | Four maturity levels explained |
| **Analogy** | `docs/concept_analogies.md#rest-restaurant` | "REST levels are like restaurant service" |
| **Lab Exercise** | `src/exercises/ex_10_02_richardson_maturity.py` | Flask server with all 4 levels |
| **Test** | `tests/test_exercises.py::test_exercise_6` | REST selftest verification |
| **Quiz** | `formative/quiz.yaml` q03, q04, q05 | Level identification, status codes, HATEOAS |
| **Misconception** | `docs/misconceptions.md#misconception-4` | "REST is a protocol" |
| **Misconception** | `docs/misconceptions.md#misconception-5` | "Any JSON API is RESTful" |
| **Misconception** | `docs/misconceptions.md#misconception-6` | "PUT and POST are interchangeable" |
| **Peer Instruction** | `docs/peer_instruction.md` Q2 | Richardson level identification |
| **Parsons** | `docs/parsons_problems.md` P3 | Flask REST handler |
| **Homework** | `homework/exercises/hw_10_02_rest_client.py` | REST client implementation |
| **Commands** | `docs/commands_cheatsheet.md#curl` | curl -X POST, PUT, DELETE |

### Success Criteria

Students can:
- [ ] Identify the Richardson Maturity level of a given API
- [ ] Explain the difference between Level 1 and Level 2
- [ ] Implement proper HTTP verb semantics (GET, POST, PUT, DELETE)
- [ ] Describe what HATEOAS adds to a Level 2 API

### Verification Commands

```bash
# Start server
python3 src/exercises/ex_10_02_richardson_maturity.py serve

# Compare levels
curl -X POST http://localhost:5000/level0/service -d '{"action":"list_users"}'
curl http://localhost:5000/level2/users
curl http://localhost:5000/level3/users | jq '._links'
```

---

## LO3: Analyse DNS Query Structure

> **By the end of this lab, students will be able to analyse DNS query and response structure.**

### Artefact Mapping

| Artefact Type | Location | Description |
|---------------|----------|-------------|
| **Theory** | `docs/theory_summary.md#dns` | DNS message format, record types |
| **Analogy** | `docs/concept_analogies.md#dns-phonebook` | "DNS is like a phone book lookup" |
| **Lab Exercise** | `src/exercises/ex_10_03_dns_query_analysis.py` | DNS query builder, response parser |
| **Docker** | `docker/dns-server/dns_server.py` | Custom DNS server (dnslib) |
| **Test** | `tests/test_exercises.py::test_exercise_2` | DNS resolution test |
| **Quiz** | `formative/quiz.yaml` q06, q07 | UDP vs TCP, truncation handling |
| **Misconception** | `docs/misconceptions.md#misconception-7` | "DNS only uses UDP" |
| **Misconception** | `docs/misconceptions.md#misconception-8` | "DNS caching improves privacy" |
| **Peer Instruction** | `docs/peer_instruction.md` Q3 | DNS transport protocol |
| **Parsons** | `docs/parsons_problems.md` P2 | DNS query function |
| **Homework** | `homework/exercises/hw_10_03_dns_tool.py` | DNS configuration tool |
| **Commands** | `docs/commands_cheatsheet.md#dig` | dig @server, +tcp, +trace |

### Success Criteria

Students can:
- [ ] Build a DNS query programmatically
- [ ] Parse DNS response sections (answer, authority, additional)
- [ ] Explain when DNS uses TCP instead of UDP
- [ ] Interpret the TC (truncation) bit

### Verification Commands

```bash
# Query lab DNS server
dig @127.0.0.1 -p 5353 web.lab.local +short

# Force TCP
dig @127.0.0.1 -p 5353 web.lab.local +tcp

# Run exercise
python3 src/exercises/ex_10_03_dns_query_analysis.py demo
```

---

## LO4: Implement Protocol Clients

> **By the end of this lab, students will be able to implement basic clients for HTTP, DNS, SSH and FTP protocols.**

### Artefact Mapping

| Artefact Type | Location | Description |
|---------------|----------|-------------|
| **Theory** | `docs/theory_summary.md#application-protocols` | Protocol overviews |
| **Lab Exercise** | `src/exercises/ex_10_04_secure_transfer.py` | SSH and FTP clients |
| **Apps** | `src/apps/ssh_demo.py`, `src/apps/ftp_demo.py` | Demo applications |
| **Docker** | `docker/ssh-server/`, `docker/ftp-server/` | Lab services |
| **Test** | `tests/test_exercises.py::test_exercise_3,4` | SSH and FTP tests |
| **Quiz** | `formative/quiz.yaml` q08 | FTP dual-channel architecture |
| **Misconception** | `docs/misconceptions.md#misconception-11` | "FTP uses single connection" |
| **Misconception** | `docs/misconceptions.md#misconception-12` | "Active and passive FTP are equivalent" |
| **Peer Instruction** | `docs/peer_instruction.md` Q4 | FTP connection count |
| **Parsons** | `docs/parsons_problems.md` P4 | FTP download function |
| **Commands** | `docs/commands_cheatsheet.md#ssh`, `#ftp` | ssh -p, ftp passive mode |

### Success Criteria

Students can:
- [ ] Execute remote commands via SSH using Paramiko
- [ ] Transfer files via FTP using ftplib
- [ ] Explain FTP control vs data channels
- [ ] Distinguish active vs passive FTP modes

### Verification Commands

```bash
# Test SSH
ssh -p 2222 labuser@localhost  # Password: labpass

# Test FTP
ftp -p localhost 2121  # User: labftp, Pass: labftp

# Run exercise
python3 src/exercises/ex_10_04_secure_transfer.py demo
```

---

## LO5: Evaluate Security Differences

> **By the end of this lab, students will be able to evaluate security differences between encrypted and unencrypted protocols.**

### Artefact Mapping

| Artefact Type | Location | Description |
|---------------|----------|-------------|
| **Theory** | `docs/theory_summary.md#security` | Encryption comparison |
| **Analogy** | `docs/concept_analogies.md#encryption-postcard` | "HTTP is like a postcard, HTTPS like sealed envelope" |
| **Lab Exercise** | `src/exercises/ex_10_01_tls_rest_crud.py` | HTTP vs HTTPS comparison |
| **Homework** | `homework/exercises/hw_10_01_https_analysis.py` | Traffic analysis |
| **Quiz** | `formative/quiz.yaml` q09, q10 | SSH keys, FTP plaintext |
| **Misconception** | `docs/misconceptions.md#misconception-9` | "SSH and SSL/TLS are the same" |
| **Misconception** | `docs/misconceptions.md#misconception-10` | "SSH key auth is less secure" |
| **Peer Instruction** | `docs/peer_instruction.md` Q1 | HTTPS privacy limits |
| **Code Tracing** | `docs/code_tracing.md` Exercise 2 | Credential exposure |
| **Troubleshooting** | `docs/troubleshooting.md` | Security-related issues |

### Success Criteria

Students can:
- [ ] Capture and compare HTTP vs HTTPS traffic in Wireshark
- [ ] Identify what is visible in unencrypted protocols
- [ ] Explain why SSH key authentication is more secure than passwords
- [ ] Recommend appropriate protocols for sensitive data

### Verification Commands

```bash
# Capture FTP credentials (plaintext!)
tcpdump -i any port 2121 -A | grep -E '(USER|PASS)'

# Capture HTTPS (encrypted)
tcpdump -i any port 8443 -A  # No readable content

# Wireshark HTTP vs HTTPS comparison
# See homework/README.md Assignment 1
```

---

## Traceability Matrix Summary

| LO | Theory | Exercise | Test | Quiz | Misconception | Peer Inst | Parsons | Homework |
|----|--------|----------|------|------|---------------|-----------|---------|----------|
| LO1 | ✅ | ex_10_01 | ✅ | q01,q02 | M1,M2 | Q1,Q5 | P1,P5 | hw_10_01 |
| LO2 | ✅ | ex_10_02 | ✅ | q03-q05 | M4,M5,M6 | Q2 | P3 | hw_10_02 |
| LO3 | ✅ | ex_10_03 | ✅ | q06,q07 | M7,M8 | Q3 | P2 | hw_10_03 |
| LO4 | ✅ | ex_10_04 | ✅ | q08 | M11,M12 | Q4 | P4 | — |
| LO5 | ✅ | ex_10_01 | ✅ | q09,q10 | M9,M10 | Q1 | — | hw_10_01 |

**Legend:**
- ✅ = Complete coverage
- M# = Misconception number
- Q# = Peer Instruction question
- P# = Parsons problem

---

## Assessment Alignment

| Assessment Type | Weight | LO Coverage |
|-----------------|--------|-------------|
| Lab Exercises | 40% | LO1, LO2, LO3, LO4 |
| Homework | 30% | LO1, LO2, LO3, LO5 |
| Formative Quiz | 0% (self-assessment) | All LOs |
| Peer Instruction | 0% (in-class) | All LOs |

---

*Computer Networks — Week 10 | ASE, CSIE Bucharest*
*Learning Objectives traceability by ing. dr. Antonio Clim*
