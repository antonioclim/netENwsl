#!/usr/bin/env python3
"""
Exercise 12.01: Explore SMTP Protocol
=====================================
Computer Networks - Week 12 (WSL Environment)
ASE Bucharest | by ing. dr. Antonio Clim

Objectives:
- UNDERSTAND the structure of SMTP dialogue (commands and reply codes)
- APPLY manual SMTP commands using netcat
- ANALYSE captured SMTP traffic in Wireshark

Prerequisites:
- Docker running in WSL
- Lab containers started (make start or python3 scripts/start_lab.py)

Level: Intermediate
Estimated time: 45 minutes

Pair Programming Notes:
- Driver: Types SMTP commands in netcat
- Navigator: Verifies response codes against RFC 5321
- Swap after: Completing MAIL FROM/RCPT TO sequence
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations
from typing import Optional, List, Dict, Tuple, Any

import sys
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# EXERCISE_DOCUMENTATION
# ═══════════════════════════════════════════════════════════════════════════════

EXERCISE_TEXT = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    EXERCISE 12.01: EXPLORE SMTP PROTOCOL                      ║
╚═══════════════════════════════════════════════════════════════════════════════╝

This exercise guides you through manual SMTP interaction to understand the
protocol's command-response structure.

───────────────────────────────────────────────────────────────────────────────
PART A: Run the Teaching SMTP Server
───────────────────────────────────────────────────────────────────────────────

Terminal 1:
  make smtp-server
  # Or: python3 src/apps/email/smtp_server.py --verbose

The server listens on 127.0.0.1:1025 and stores messages in `docker/volumes/spool/`.

Terminal 2:
  make smtp-send
  # Or: python3 src/apps/email/smtp_client.py

💭 PREDICTION: What response code will you see when connecting?
   (Hint: It indicates "service ready")

Inspect the stored message:
  ls -la docker/volumes/spool/
  cat docker/volumes/spool/*.eml | head -20

───────────────────────────────────────────────────────────────────────────────
PART B: Manual SMTP Dialogue Using netcat
───────────────────────────────────────────────────────────────────────────────

💭 PREDICTION: Before starting, predict what response code DATA will return.
   Is it 250 (success) or something else?

Terminal 2 (while the server is running):
  nc 127.0.0.1 1025

Type the following commands EXACTLY (press Enter after each line):

  EHLO client
  MAIL FROM:<alice@example.test>
  RCPT TO:<bob@example.test>
  DATA
  Subject: Manual SMTP test

  Hello from a manual SMTP session.
  This message was typed by hand.
  .
  QUIT

Observe and record:
┌───────────────────────────────────────────────────────────────────────────────┐
│ Command          │ Expected Code │ Your Observed Code │ Match? │
├───────────────────────────────────────────────────────────────────────────────┤
│ (on connect)     │ 220           │ __________________ │ ______ │
│ EHLO             │ 250           │ __________________ │ ______ │
│ MAIL FROM        │ 250           │ __________________ │ ______ │
│ RCPT TO          │ 250           │ __________________ │ ______ │
│ DATA             │ 354           │ __________________ │ ______ │
│ (after dot)      │ 250           │ __________________ │ ______ │
│ QUIT             │ 221           │ __________________ │ ______ │
└───────────────────────────────────────────────────────────────────────────────┘

Key observations:
- 220 = greeting on connect
- 250 = command successful
- 354 = ready for message content (NOT 250!)
- 221 = closing connection

───────────────────────────────────────────────────────────────────────────────
PART C: LIST Command (Non-Standard Teaching Extension)
───────────────────────────────────────────────────────────────────────────────

The Week 12 SMTP server implements a convenience command called LIST
(not part of RFC 5321 — for teaching purposes only):

Terminal 2:
  make smtp-list
  # Or: nc 127.0.0.1 1025, then type: EHLO check / LIST / QUIT

💭 PREDICTION: How many messages will LIST show?

───────────────────────────────────────────────────────────────────────────────
PART D: Capture and Inspect (Optional)
───────────────────────────────────────────────────────────────────────────────

Capture traffic while running a short demo (requires tcpdump and sudo):

  sudo make capture
  # Or: python3 scripts/capture_traffic.py --duration 30 --ports 1025

Inspect quickly with tshark:

  make analyse
  # Or: tshark -r pcap/smtp_capture.pcap -Y smtp

Open the pcap in Wireshark and identify:
- TCP 3-way handshake (SYN, SYN-ACK, ACK)
- SMTP commands and responses
- The DATA phase, including termination with a single dot

───────────────────────────────────────────────────────────────────────────────
DELIVERABLES
───────────────────────────────────────────────────────────────────────────────

1. A brief transcript of a manual SMTP dialogue (Part B table completed)
2. A screenshot or short note from Wireshark showing the DATA phase
3. One stored `.eml` file from `docker/volumes/spool/` (or an excerpt)

───────────────────────────────────────────────────────────────────────────────
REFLECTION QUESTIONS
───────────────────────────────────────────────────────────────────────────────

1. Why does SMTP use a different response code (354) for DATA instead of 250?

2. What is the purpose of the lone period (.) that terminates message content?

3. How does SMTP handle a period at the start of a line in the actual message?
   (Hint: Look up "dot-stuffing")

4. Why might the EHLO response be multi-line while other responses are single-line?

═══════════════════════════════════════════════════════════════════════════════
"""


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """
    Display exercise instructions.
    
    This exercise is primarily instructional text guiding students
    through manual SMTP interaction.
    
    Returns:
        int: Exit code (0 for success)
    """
    print(EXERCISE_TEXT)
    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    raise SystemExit(main())
