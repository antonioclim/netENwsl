#!/usr/bin/env python3
"""Exercise 01 — SMTP (Week 12)

Learning goals
- Understand the structure of an SMTP dialogue (commands and reply codes)
- Understand how message data is transferred after the DATA command
- Practise running a local SMTP service and verifying it using different clients
- Capture and inspect SMTP traffic (optional)

Prerequisites
- Run `make setup` and `make verify` in the Week 12 directory.

---

Part A — Run the teaching SMTP server

Terminal 1
  make smtp-server

The server listens on 127.0.0.1:1025 by default and stores received messages in `spool/`.

Terminal 2
  make smtp-send

Inspect the stored message:
  ls -la spool
  sed -n '1,120p' spool/*.eml

---

Part B — Manual SMTP dialogue using netcat (nc)

Terminal 2 (while the server is running)
  nc 127.0.0.1 1025

Type the following commands exactly (press Enter after each line):

  EHLO client
  MAIL FROM:<alice@example.test>
  RCPT TO:<bob@example.test>
  DATA
  Subject: Manual SMTP test

  Hello from a manual SMTP session.
  .
  QUIT

Observe:
- 220 greeting on connect
- 250 replies for successful commands
- 354 reply after DATA
- 250 reply after message termination (a single dot on its own line)

---

Part C — LIST (non-standard teaching command)

The Week 12 SMTP server implements a convenience command called LIST (not part of RFC 5321):

Terminal 2
  make smtp-list

---

Part D — Capture and inspect (optional)

Capture traffic while running a short demo (requires tcpdump and sudo):

  sudo make capture

Inspect quickly with tshark:

  make analyse

Open the pcap in Wireshark and identify:
- TCP 3-way handshake
- SMTP commands and responses
- the DATA phase, including termination with a single dot

---

Deliverables (typical)
1. A brief transcript of a manual SMTP dialogue (Part B)
2. A screenshot or short note from Wireshark showing the DATA phase
3. One stored `.eml` file from `spool/` (or an excerpt)

"""

from __future__ import annotations


def main() -> int:
    # This exercise is primarily instructional text.
    print(__doc__)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
