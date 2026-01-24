# Homework: Week 7

> NETWORKING class - ASE, Informatics | by Revolvix

## Overview

These assignments extend the laboratory exercises and must be completed individually. Submit your work through the course portal by the deadline specified in class.

## Assignment 1: Custom Firewall Profile

**Objective:** Design and implement a firewall profile that meets specific security requirements.

**Task:**

Create a new firewall profile (`configs/firewall_profiles.json`) that:

1. Allows TCP traffic on port 9090 only from the subnet 10.0.7.0/24
2. Blocks all UDP traffic to port 9091 except from host 10.0.7.200
3. Logs all dropped packets (hint: use iptables LOG target before DROP)
4. Allows established connections to continue (stateful filtering)

**Deliverables:**

1. `hw_7_01_profile.json` - Your custom profile definition
2. `hw_7_01_test.py` - Script to verify your profile works
3. `hw_7_01_report.md` - Short report (max 1 page) explaining:
   - Your rule logic
   - How you verified each requirement
   - Any challenges encountered

**Evaluation criteria:**
- Correctness of rules (40%)
- Test coverage (30%)
- Report clarity (30%)

## Assignment 2: Failure Analysis Report

**Objective:** Analyse a network failure scenario using packet captures.

**Task:**

Using the laboratory environment:

1. Start with a working baseline (TCP and UDP connectivity verified)
2. Apply the `mixed_filtering` profile from `configs/firewall_profiles.json`
3. Capture traffic during the following sequence:
   - TCP client sends message to server
   - UDP sender sends datagram to receiver
   - Port probe scans ports 9090-9091
4. Analyse the capture and explain exactly what happens at the packet level

**Deliverables:**

1. `hw_7_02_capture.pcap` - Your packet capture (use BPF filter to keep size reasonable)
2. `hw_7_02_analysis.md` - Analysis report containing:
   - For each scenario: expected behaviour vs observed behaviour
   - Specific packet references (frame numbers, timestamps)
   - Explanation of filtering effects (which rules matched)
   - Timeline diagram of the communication attempts

**Evaluation criteria:**
- Capture quality (20%)
- Analysis accuracy (40%)
- Use of evidence from capture (40%)

## Submission Guidelines

### File Format

- Code files: UTF-8 encoded, LF line endings
- Reports: Markdown format
- Captures: Standard pcap format (not pcapng)

### Naming Convention

```
StudentID_WEEK7_HW1.zip
StudentID_WEEK7_HW2.zip
```

Each ZIP should contain:
```
StudentID_WEEK7_HW1/
├── hw_7_01_profile.json
├── hw_7_01_test.py
└── hw_7_01_report.md
```

### Submission Checklist

- [ ] All files are present
- [ ] Code runs without errors
- [ ] Report follows structure guidelines
- [ ] No absolute paths in code
- [ ] No credentials or sensitive data
- [ ] ZIP file under 10MB

## Academic Integrity

- Work must be your own
- Code sharing is not permitted
- Discussion of concepts is encouraged; sharing solutions is not
- Cite any external resources used

## Getting Help

- Office hours: See course schedule
- Discussion forum: Technical questions only (no solution sharing)
- Email: For administrative issues only

---

*NETWORKING class - ASE, Informatics | by Revolvix*
