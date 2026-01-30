# Week 1 Homework Assignments

> NETWORKING class - ASE, Informatics | by Revolvix

## Overview

These homework assignments extend the laboratory exercises and are designed to
be completed independently. Submit your work according to the course
requirements.

## Anti-AI workflow (challenge, evidence and validation)

For this week, the homework includes a light-weight anti-AI mechanism. The goal
is not to forbid AI tools. The goal is to ensure that a valid submission includes
artefacts that cannot be produced credibly by a language model alone, especially
PCAP captures.

You will work with three files:
- a challenge file (generated per student)
- your artefacts (report and PCAP files)
- an evidence.json file (hashes and optional command transcript)

### 1) Generate your challenge file

From the Week 1 kit root, run:

```bash
python -m anti_ai.challenge_generator --student-id <YOUR_ID>
```

This creates `artifacts/anti_ai/challenge_<YOUR_ID>.yaml`.

### 2) Produce the required artefacts using the challenge

- Homework 1.01: include the *report token* in your report by running:

```bash
python homework/exercises/hw_1_01_network_report.py --challenge artifacts/anti_ai/challenge_<YOUR_ID>.yaml --output network_report.md
```

- Homework 1.02: embed the *payload token* in your TCP and UDP traffic by running:

```bash
# TCP
sudo python homework/exercises/hw_1_02_protocol_analysis.py --challenge artifacts/anti_ai/challenge_<YOUR_ID>.yaml --mode tcp --output tcp_analysis.pcap

# UDP
sudo python homework/exercises/hw_1_02_protocol_analysis.py --challenge artifacts/anti_ai/challenge_<YOUR_ID>.yaml --mode udp --output udp_analysis.pcap
```

### 3) Collect evidence and validate locally

Create `evidence.json`:

```bash
python -m anti_ai.evidence_collector \
  --challenge artifacts/anti_ai/challenge_<YOUR_ID>.yaml \
  --artefact network_report.md \
  --artefact tcp_analysis.pcap \
  --artefact udp_analysis.pcap \
  --output evidence.json \
  --include-commands
```

Validate your submission:

```bash
python -m anti_ai.submission_validator \
  --challenge artifacts/anti_ai/challenge_<YOUR_ID>.yaml \
  --evidence evidence.json \
  --base-dir . \
  --verbose
```

If validation fails, fix the issue and regenerate the affected artefact.

---

## Assignment 1: Network Configuration Report

**Objective:** Document the network configuration of your personal computer or a
designated laboratory machine.

**Deliverables:**
- A markdown report (`network_report.md`) containing:
  - All network interfaces with their IP addresses and MAC addresses
  - The routing table with explanation of each route
  - Active network connections at the time of analysis
  - DNS configuration
  - The Anti-AI Verification section if you used a challenge file

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

## Assignment 2: TCP and UDP Traffic Analysis

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
hw1_<student_id>.zip
```

Example: `hw1_12345.zip`

### Archive Contents

```
hw1_12345/
├── artifacts/anti_ai/
│   └── challenge_12345.yaml
├── network_report.md
├── tcp_analysis.pcap
├── udp_analysis.pcap
├── evidence.json
└── protocol_analysis.md
```

---

## Academic Integrity

- You may use AI tools for drafting explanations, checking grammar and exploring
  concepts.
- You must not submit AI-generated artefacts (for example fabricated PCAPs or
  invented command outputs).
- Your submission must pass the provided validator.

---

*NETWORKING class - ASE, Informatics | by Revolvix*
