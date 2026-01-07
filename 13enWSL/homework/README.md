# Homework Assignments

> Week 13: IoT and Security in Computer Networks  
> NETWORKING class - ASE, Informatics | by Revolvix

---

## Overview

These homework assignments extend the laboratory exercises and require independent work outside of class. Complete them before the next laboratory session.

---

## Assignment 1: Extended Port Scanner

**Objective:** Enhance the basic port scanner with additional reconnaissance capabilities.

**Requirements:**
1. Add service fingerprinting beyond simple banner grabbing
2. Implement OS detection using TCP/IP stack fingerprinting (TTL analysis, window size)
3. Add timing control (slow scan vs fast scan modes)
4. Generate a professional security report in Markdown format

**Deliverables:**
- `hw_13_01_extended_scanner.py` - Enhanced scanner script
- `hw_13_01_report.md` - Sample scan report of the laboratory environment

**Starter code:** See `exercises/hw_13_01.py`

**Evaluation criteria:**
- Correct implementation of fingerprinting techniques (40%)
- Code quality and documentation (20%)
- Report quality and professionalism (20%)
- Error handling and edge cases (20%)

---

## Assignment 2: MQTT Security Analysis Report

**Objective:** Conduct a comprehensive security analysis of MQTT deployments.

**Requirements:**
1. Research and document at least 5 real-world MQTT security incidents
2. Compare security features across MQTT versions (3.1, 3.1.1, 5.0)
3. Analyse the TLS overhead in IoT environments
4. Propose a security hardening checklist for MQTT deployments

**Deliverables:**
- `hw_13_02_mqtt_security_report.md` - Written report (minimum 2000 words)
- `hw_13_02_tls_analysis.py` - Script demonstrating TLS overhead measurement

**Starter code:** See `exercises/hw_13_02.py`

**Evaluation criteria:**
- Research quality and references (30%)
- Technical accuracy (30%)
- Practical recommendations (20%)
- Writing quality (20%)

---

## Assignment 3: Network Segmentation Design (Bonus)

**Objective:** Design a secure network architecture for an IoT deployment.

**Scenario:**
A manufacturing company wants to deploy 50 IoT sensors across their factory floor. Design a network architecture that:
- Isolates IoT traffic from corporate network
- Implements defence in depth
- Allows monitoring and management
- Scales to 500 devices

**Deliverables:**
- Network diagram (draw.io, Visio, or ASCII art)
- Written justification for design decisions
- Docker Compose file demonstrating a scaled-down version

**Evaluation criteria:**
- Security architecture soundness (40%)
- Scalability considerations (20%)
- Practical implementation (20%)
- Documentation quality (20%)

---

## Submission Guidelines

### Format
- All Python files must pass `python -m py_compile <filename>`
- Markdown files should render correctly on GitHub
- Include your student ID in all file headers

### Deadline
Submit before the Week 14 laboratory session.

### Submission Method
Upload to the course platform or as directed by your instructor.

---

## Academic Integrity

- Individual work unless otherwise specified
- Cite all external sources
- Code sharing constitutes academic dishonesty
- Discussion of concepts is permitted; sharing solutions is not

---

## Resources

- Laboratory exercises from this week
- Course textbook chapters on network security
- `docs/further_reading.md` for additional references

---

*NETWORKING class - ASE, Informatics | by Revolvix*
