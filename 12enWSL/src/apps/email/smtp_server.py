#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# MODULE_DOCSTRING
# ═══════════════════════════════════════════════════════════════════════════════
"""Educational SMTP server (Week 12).

This is a deliberately small SMTP server for teaching purposes. It supports a
subset of RFC 5321 and adds one *non-standard* convenience command:

- LIST   lists stored messages in the spool directory

It is **not** intended for production use.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import logging
import os
import re
import socketserver
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


LOG = logging.getLogger("week12.smtp")


ADDRESS_RE = re.compile(r"<([^>]+)>")



# ═══════════════════════════════════════════════════════════════════════════════
# PRIVATE_HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def _extract_address(token: str) -> str:
    m = ADDRESS_RE.search(token)
    if m:
        return m.group(1).strip()
    return token.strip().strip("<>").strip()


@dataclass

# ═══════════════════════════════════════════════════════════════════════════════
# MAILTRANSACTION_CLASS
# ═══════════════════════════════════════════════════════════════════════════════
class MailTransaction:
    mail_from: Optional[str] = None
    rcpt_to: List[str] | None = None
    data_lines: List[str] | None = None

    def reset(self) -> None:
        self.mail_from = None
        self.rcpt_to = []
        self.data_lines = []

    @property
    def ready_for_data(self) -> bool:
        return bool(self.mail_from) and bool(self.rcpt_to)



# ═══════════════════════════════════════════════════════════════════════════════
# SMTPHANDLER_CLASS
# ═══════════════════════════════════════════════════════════════════════════════
class SMTPHandler(socketserver.StreamRequestHandler):
    server: "SMTPServer"

    def setup(self) -> None:
        super().setup()
        self.session_id = f"{int(time.time())}-{os.getpid()}-{id(self)}"
        self.helo_name: Optional[str] = None
        self.tx = MailTransaction()
        self.tx.reset()

    def _send(self, line: str) -> None:
        LOG.debug("→ %s", line)
        self.wfile.write((line + "\r\n").encode("utf-8"))

    def _send_multiline_250(self, lines: List[str]) -> None:
        for i, l in enumerate(lines):
            if i < len(lines) - 1:
                self._send(f"250-{l}")
            else:
                self._send(f"250 {l}")

    def handle(self) -> None:
        peer = f"{self.client_address[0]}:{self.client_address[1]}"
        LOG.info("Connection from %s", peer)
        self._send("220 Week12 SMTP server ready")

        in_data = False

        while True:
            raw = self.rfile.readline()
            if not raw:
                break
            line = raw.decode("utf-8", errors="replace").rstrip("\r\n")
            LOG.debug("← %s", line)

            if in_data:
                if line == ".":
                    # End of DATA
                    in_data = False
                    try:
                        path = self.server.store_message(self.tx)
                        self._send(f"250 Message accepted for delivery (stored as {path.name})")
                        LOG.info("Stored message: %s", path)
                    except Exception as exc:
                        LOG.exception("Failed to store message")
                        self._send(f"451 Requested action aborted: local error in processing ({exc})")
                    finally:
                        self.tx.reset()
                    continue
                else:
                    # Dot-stuffing
                    if line.startswith(".."):
                        line = line[1:]
                    self.tx.data_lines.append(line)
                    continue

            if not line:
                self._send("500 Empty command")
                continue

            parts = line.split()
            cmd = parts[0].upper()
            args = line[len(parts[0]):].strip() if len(parts) > 1 else ""

            if cmd in {"HELO", "EHLO"}:
                self.helo_name = args or "client"
                self._send_multiline_250([
                    f"Hello {self.helo_name}",
                    "SIZE 1048576",
                    "8BITMIME",
                    "PIPELINING",
                    "This server is for education only",
                ])

            elif cmd == "NOOP":
                self._send("250 OK")

            elif cmd == "RSET":
                self.tx.reset()
                self._send("250 OK (state reset)")

            elif cmd == "QUIT":
                self._send("221 Bye")
                break

            elif cmd == "VRFY":
                self._send("252 Cannot VRFY user, but will accept message")

            elif cmd == "HELP":
                self._send_multiline_250([
                    "Supported: HELO, EHLO, MAIL, RCPT, DATA, RSET, NOOP, QUIT, HELP, LIST",
                    "LIST is a non-standard command used by this teaching kit",
                ])

            elif cmd == "LIST":
                items = self.server.list_messages()
                if not items:
                    self._send_multiline_250(["0 message(s) in spool", "End of list"])
                else:
                    lines = [f"{len(items)} message(s) in spool"]
                    for it in items[:50]:
                        lines.append(f"{it.name} ({it.stat().st_size} bytes)")
                    if len(items) > 50:
                        lines.append(f"… {len(items) - 50} more not shown")
                    lines.append("End of list")
                    self._send_multiline_250(lines)

            elif cmd == "MAIL":
                if not args.upper().startswith("FROM:"):
                    self._send("501 Syntax: MAIL FROM:<address>")
                    continue
                addr = _extract_address(args[5:].strip())
                if not addr:
                    self._send("501 Syntax: MAIL FROM:<address>")
                    continue
                self.tx.mail_from = addr
                self.tx.rcpt_to = []
                self.tx.data_lines = []
                self._send("250 OK")

            elif cmd == "RCPT":
                if not args.upper().startswith("TO:"):
                    self._send("501 Syntax: RCPT TO:<address>")
                    continue
                addr = _extract_address(args[3:].strip())
                if not addr:
                    self._send("501 Syntax: RCPT TO:<address>")
                    continue
                self.tx.rcpt_to.append(addr)
                self._send("250 OK")

            elif cmd == "DATA":
                if not self.tx.ready_for_data:
                    self._send("503 Bad sequence of commands (need MAIL FROM and RCPT TO)")
                    continue
                in_data = True
                self._send("354 End data with <CR><LF>.<CR><LF>")

            else:
                self._send(f"502 Command not implemented: {cmd}")

        LOG.info("Connection closed: %s", peer)



# ═══════════════════════════════════════════════════════════════════════════════
# SMTPSERVER_CLASS
# ═══════════════════════════════════════════════════════════════════════════════
class SMTPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

    def __init__(self, server_address, handler_cls, spool_dir: Path):
        super().__init__(server_address, handler_cls)
        self.spool_dir = spool_dir
        self.spool_dir.mkdir(parents=True, exist_ok=True)
        self._counter = 0

    def store_message(self, tx: MailTransaction) -> Path:
        self._counter += 1
        ts = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{ts}_{os.getpid()}_{self._counter:04d}.eml"
        path = self.spool_dir / filename

        # Store a minimal RFC 5322 message for convenience
        lines: List[str] = []
        lines.append(f"From: {tx.mail_from}")
        lines.append(f"To: {', '.join(tx.rcpt_to)}")
        lines.append(f"Date: {time.strftime('%a, %d %b %Y %H:%M:%S %z')}")
        lines.append("Subject: Week 12 SMTP message")
        lines.append("")
        lines.extend(tx.data_lines or [])
        content = "\r\n".join(lines) + "\r\n"
        path.write_text(content, encoding="utf-8")
        return path

    def list_messages(self) -> List[Path]:
        return sorted(self.spool_dir.glob("*.eml"), key=lambda p: p.stat().st_mtime, reverse=True)



# ═══════════════════════════════════════════════════════════════════════════════
# PARSE_ARGS_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Educational SMTP server (Week 12)")
    ap.add_argument("--host", default="127.0.0.1", help="Bind address (default: 127.0.0.1)")
    ap.add_argument("--port", type=int, default=1025, help="TCP port (default: 1025)")
    ap.add_argument("--spool", default="spool", help="Spool directory for stored .eml files")
    ap.add_argument("--maildir", default=None, help="Alias for --spool (kept for compatibility)")
    ap.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    return ap.parse_args()



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    args = parse_args()

    spool = Path(args.spool)
    if args.maildir:
        spool = Path(args.maildir)

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level, format="[%(asctime)s] %(levelname)s %(name)s: %(message)s")

    host = args.host
    port = int(args.port)

    LOG.info("Starting SMTP server on %s:%s", host, port)
    LOG.info("Spool directory: %s", spool.resolve())

    with SMTPServer((host, port), SMTPHandler, spool_dir=spool) as srv:
        try:
            srv.serve_forever(poll_interval=0.2)
        except KeyboardInterrupt:
            LOG.info("Stopping (Ctrl+C)")
    return 0



# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    raise SystemExit(main())
