# Week 13: IoT and Security — Learning Objectives

**Computer Networks** — ASE, CSIE | ing. dr. Antonio Clim

---

## Learning Objectives

Upon successful completion of this module, students will be able to:

### LO1: MQTT Protocol Architecture
**Explain** the MQTT publish-subscribe architecture, including the roles of publishers, subscribers, and brokers.

- Bloom Level: **Remember/Understand**
- Assessment: Quiz Q01-Q03, Exercise 13.01
- Key Concepts: Topic hierarchy, client identification, connection lifecycle

### LO2: Quality of Service Semantics
**Differentiate** between MQTT QoS levels (0, 1, 2) and select appropriate levels for given application requirements.

- Bloom Level: **Understand/Apply**
- Assessment: Quiz Q04-Q06, Exercise 13.01
- Key Concepts: At-most-once, at-least-once, exactly-once delivery guarantees

### LO3: Network Traffic Analysis
**Analyse** captured network traffic to identify protocol behaviours and potential security weaknesses.

- Bloom Level: **Analyse**
- Assessment: Quiz Q07-Q08, Exercises 13.01-13.02
- Key Concepts: Packet capture, protocol dissection, traffic patterns

### LO4: Broker Security Configuration
**Configure** MQTT broker security controls including authentication, authorisation, and TLS encryption.

- Bloom Level: **Apply**
- Assessment: Quiz Q09-Q10, Exercises 13.02-13.03
- Key Concepts: ACLs, certificate management, secure defaults

### LO5: OWASP IoT Vulnerability Identification
**Identify** vulnerabilities in IoT deployments using the OWASP IoT Top 10 framework.

- Bloom Level: **Analyse/Evaluate**
- Assessment: Quiz Q11-Q12, Exercise 13.04
- Key Concepts: Vulnerability taxonomy, risk prioritisation, remediation strategies

### LO6: Defence-in-Depth Strategies
**Design** defence-in-depth security architectures for IoT deployments.

- Bloom Level: **Evaluate/Create**
- Assessment: Quiz Q15-Q16, Exercise 13.04
- Key Concepts: Layered security, network segmentation, secure boot

### LO7: Security Posture Evaluation
**Evaluate** the overall security posture of IoT deployments and recommend improvements.

- Bloom Level: **Evaluate**
- Assessment: Quiz Q13-Q14, Final Project
- Key Concepts: Risk assessment, security auditing, compliance

---

## Bloom Taxonomy Distribution

| Level | Count | Questions | Exercises |
|-------|-------|-----------|-----------|
| Remember | 3 | Q01, Q02, Q03 | — |
| Understand | 3 | Q04, Q05, Q06 | Ex 13.01 |
| Apply | 3 | Q07, Q08, Q09 | Ex 13.02, 13.03 |
| Analyse | 3 | Q10, Q11, Q12 | Ex 13.01, 13.04 |
| Evaluate | 2 | Q13, Q14 | Ex 13.04 |
| Create | 2 | Q15, Q16 | Final Project |

---

## LO-to-Exercise Traceability Matrix

| Exercise | LO1 | LO2 | LO3 | LO4 | LO5 | LO6 | LO7 |
|----------|-----|-----|-----|-----|-----|-----|-----|
| Ex 13.01 MQTT Traffic Analysis | ● | ● | ● | ○ | ○ | ○ | ○ |
| Ex 13.02 Broker Configuration | ○ | ○ | ● | ● | ○ | ○ | ○ |
| Ex 13.03 TLS Implementation | ○ | ○ | ○ | ● | ○ | ● | ○ |
| Ex 13.04 Vulnerability Scanner | ○ | ○ | ○ | ○ | ● | ● | ● |
| Quiz | ● | ● | ● | ● | ● | ● | ● |

**Legend**: ● = Primary coverage | ○ = Secondary/partial coverage

---

## LO-to-Quiz Traceability Matrix

| Question | LO1 | LO2 | LO3 | LO4 | LO5 | LO6 | LO7 | Bloom |
|----------|-----|-----|-----|-----|-----|-----|-----|-------|
| Q01 | ● | | | | | | | Remember |
| Q02 | ● | | | | | | | Remember |
| Q03 | ● | | | | | | | Remember |
| Q04 | | ● | | | | | | Understand |
| Q05 | | ● | | | | | | Understand |
| Q06 | | ● | | | | | | Understand |
| Q07 | | | ● | | | | | Apply |
| Q08 | | | ● | | | | | Apply |
| Q09 | | | | ● | | | | Apply |
| Q10 | | | | ● | | | | Analyse |
| Q11 | | | | | ● | | | Analyse |
| Q12 | | | | | ● | | | Analyse |
| Q13 | | | | | | | ● | Evaluate |
| Q14 | | | | | | | ● | Evaluate |
| Q15 | | | | | | ● | | Create |
| Q16 | | | | | | ● | | Create |

---

## Assessment Weights

| Component | Weight | LOs Assessed |
|-----------|--------|--------------|
| Formative Quiz | 0% (practice) | LO1-LO7 |
| Laboratory Exercises | 40% | LO1-LO6 |
| Final Project | 30% | LO6-LO7 |
| Written Examination | 30% | LO1-LO5 |

---

## Prerequisites

Students should have completed:

- Week 1-4: Network fundamentals (OSI model, TCP/IP)
- Week 5-7: Transport layer protocols (TCP, UDP)
- Week 8-9: Application layer protocols (HTTP, DNS)
- Week 10-12: Network security fundamentals (TLS, firewalls)

---

## Resources

### Required Reading
- OWASP IoT Top 10 (2024 edition)
- MQTT v5.0 Specification (Sections 1-4)

### Recommended Reading
- Mosquitto Documentation
- NIST IR 8259: IoT Device Cybersecurity Capability Core Baseline

### Laboratory Resources
- Docker environment with Mosquitto broker
- DVWA (Damn Vulnerable Web Application) for security testing
- tcpdump and Wireshark for traffic analysis

---

*Document version: 2.0 | Language: en-GB | Last updated: January 2026*
