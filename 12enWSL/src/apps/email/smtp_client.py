#!/usr/bin/env python3
"""SMTP client helper for Week 12.

This client supports two teaching-oriented actions:

1) Send a test email to the local SMTP server (using smtplib).
2) List stored messages via the server's non-standard LIST command.

The LIST command is not part of standard SMTP. It exists only for convenience in
this kit.
"""

from __future__ import annotations

import argparse
import socket
import smtplib
from email.message import EmailMessage
from typing import List


def send_email(host: str, port: int, sender: str, recipients: List[str], subject: str, body: str) -> None:
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(host=host, port=port, timeout=5) as s:
        s.send_message(msg)


def list_messages(host: str, port: int) -> str:
    # This uses the kit's non-standard LIST command.
    with socket.create_connection((host, port), timeout=5) as sock:
        f = sock.makefile("rwb", buffering=0)

        def recv_line() -> str:
            line = f.readline()
            if not line:
                return ""
            return line.decode("utf-8", errors="replace").rstrip("\r\n")

        def send_line(s: str) -> None:
            f.write((s + "\r\n").encode("utf-8"))

        banner = recv_line()
        if banner:
            pass

        send_line("EHLO client")
        # Read multi-line 250 response
        while True:
            line = recv_line()
            if not line:
                break
            if line.startswith("250 "):
                break

        send_line("LIST")
        lines: List[str] = []
        while True:
            line = recv_line()
            if not line:
                break
            lines.append(line)
            # Last line of multi-line 250 reply starts with '250 '
            if line.startswith("250 "):
                break

        send_line("QUIT")
        return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="SMTP client helper (Week 12)")
    ap.add_argument("--host", default="127.0.0.1", help="SMTP server host")
    ap.add_argument("--port", type=int, default=1025, help="SMTP server port")
    ap.add_argument("--from", dest="sender", default=None, help="Sender address")
    ap.add_argument("--to", dest="recipients", action="append", default=[], help="Recipient address (repeatable)")
    ap.add_argument("--subject", default="Test message", help="Email subject")
    ap.add_argument("--body", default="Hello from Week 12.", help="Email body")
    ap.add_argument("--list", action="store_true", help="List stored messages (non-standard LIST command)")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    host = args.host
    port = int(args.port)

    if args.list:
        out = list_messages(host, port)
        print(out)
        return 0

    if not args.sender or not args.recipients:
        raise SystemExit("To send an email you must provide --from and at least one --to")

    send_email(host, port, args.sender, args.recipients, args.subject, args.body)
    print(f"Sent email from {args.sender} to {', '.join(args.recipients)} via {host}:{port}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
