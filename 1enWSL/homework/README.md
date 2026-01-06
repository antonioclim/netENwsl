# Week 1 Homework Assignments

> NETWORKING class - ASE, Informatics | by Revolvix

## Overview

These homework assignments extend the laboratory exercises and are designed to be completed independently. Submit your work according to the course requirements.

---

## Assignment 1: Network Configuration Report

**Objective:** Document the network configuration of your personal computer or a designated laboratory machine.

**Deliverables:**
- A markdown report (`network_report.md`) containing:
  - All network interfaces with their IP addresses and MAC addresses
  - The routing table with explanation of each route
  - Active network connections at the time of analysis
  - DNS configuration

**Instructions:**

1. Use the commands learned in the laboratory to gather information
2. Include command outputs as code blocks
3. Provide brief explanations for each section
4. Analyse at least one unusual or interesting finding

**Starter template:** See `exercises/hw_1_01_network_report.py`

**Grading criteria:**
- Completeness of information (40%)
- Correctness of explanations (30%)
- Quality of analysis (20%)
- Formatting and presentation (10%)

---

## Assignment 2: TCP/UDP Traffic Analysis

**Objective:** Capture and analyse network traffic to identify protocol behaviour.

**Deliverables:**
- A PCAP file (`tcp_analysis.pcap`) containing a TCP conversation
- A PCAP file (`udp_analysis.pcap`) containing UDP traffic
- A written report (`protocol_analysis.md`) containing:
  - TCP three-way handshake identification
  - Comparison of packet counts between TCP and UDP
  - Analysis of overhead differences

**Instructions:**

1. Generate TCP traffic using netcat or the Python exercises
2. Capture the traffic using tcpdump or Wireshark
3. Identify the handshake packets in your TCP capture
4. Create equivalent UDP traffic and capture it
5. Compare the two captures in your report

**Starter template:** See `exercises/hw_1_02_protocol_analysis.py`

**Grading criteria:**
- Valid PCAP files with correct traffic (30%)
- Correct identification of handshake (25%)
- Accurate comparison and analysis (30%)
- Report quality (15%)

---

## Submission Guidelines

### File Naming Convention

```
hw1_<student_id>_<assignment_number>.zip
```

Example: `hw1_12345_01.zip` for Assignment 1

### Archive Contents

```
hw1_12345_01/
├── network_report.md
├── screenshots/          # If applicable
│   └── *.png
└── scripts/              # Any custom scripts used
    └── *.py
```

### Submission Deadline

Refer to the course schedule for the deadline.

---

## Tips for Success

1. **Start early** - Network configuration changes; document it when stable

2. **Use screenshots** where text output is insufficient

3. **Explain, don't just list** - Show understanding, not just commands

4. **Verify your captures** - Open PCAP files in Wireshark before submitting

5. **Test your scripts** - Ensure they run without errors

---

## Academic Integrity

- All work must be your own
- You may discuss concepts with classmates
- Do not share your submissions
- Cite any external resources used

---

*NETWORKING class - ASE, Informatics | by Revolvix*
