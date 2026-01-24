#!/usr/bin/env python3
"""
Homework 12.1: SMTP Client Implementation
=========================================
Computer Networks - Week 12 (WSL Environment)
ASE Bucharest, CSIE | by ing. dr. Antonio Clim

Objectives:
- Implement a basic SMTP client following RFC 5321
- Understand SMTP command sequence (EHLO, MAIL FROM, RCPT TO, DATA)
- Handle SMTP response codes correctly

Level: Intermediate (⭐⭐)
Estimated time: 60-75 minutes
"""

from __future__ import annotations
import socket
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

SMTP_PORT = 2525
CRLF = "\r\n"
TIMEOUT = 10

# ═══════════════════════════════════════════════════════════════════════════════
# DATA_STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class SMTPResponse:
    """Represents an SMTP server response."""
    code: int
    message: str
    is_success: bool
    
    @classmethod
    def parse(cls, raw: str) -> "SMTPResponse":
        lines = raw.strip().split(CRLF)
        if not lines:
            return cls(0, "Empty response", False)
        final_line = lines[-1]
        try:
            code = int(final_line[:3])
            message = final_line[4:] if len(final_line) > 4 else ""
            return cls(code, message, 200 <= code < 400)
        except (ValueError, IndexError):
            return cls(0, raw, False)

@dataclass
class Email:
    """Represents an email message."""
    sender: str
    recipients: List[str]
    subject: str
    body: str
    
    def to_data(self) -> str:
        headers = [
            f"From: {self.sender}",
            f"To: {', '.join(self.recipients)}",
            f"Subject: {self.subject}",
            f"Date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}",
        ]
        return CRLF.join(headers) + CRLF + CRLF + self.body

# ═══════════════════════════════════════════════════════════════════════════════
# SMTP_CLIENT
# ═══════════════════════════════════════════════════════════════════════════════
class SMTPClient:
    """Basic SMTP client implementation."""
    
    def __init__(self, host: str = "localhost", port: int = SMTP_PORT):
        self.host = host
        self.port = port
        self.socket: Optional[socket.socket] = None
        self.debug = True
    
    def connect(self) -> SMTPResponse:
        """Connect to SMTP server."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(TIMEOUT)
        if self.debug:
            print(f"[*] Connecting to {self.host}:{self.port}...")
        try:
            self.socket.connect((self.host, self.port))
            return self._recv()
        except socket.error as e:
            return SMTPResponse(0, str(e), False)
    
    def _send(self, command: str) -> None:
        if self.debug:
            print(f"[>] {command.strip()}")
        self.socket.sendall((command + CRLF).encode("utf-8"))
    
    def _recv(self) -> SMTPResponse:
        data = self.socket.recv(4096).decode("utf-8")
        response = SMTPResponse.parse(data)
        if self.debug:
            print(f"[<] {response.code} {response.message}")
        return response
    
    def ehlo(self, domain: str = "localhost") -> SMTPResponse:
        self._send(f"EHLO {domain}")
        return self._recv()
    
    def mail_from(self, sender: str) -> SMTPResponse:
        # TODO: Implement MAIL FROM
        self._send(f"MAIL FROM:<{sender}>")
        return self._recv()
    
    def rcpt_to(self, recipient: str) -> SMTPResponse:
        # TODO: Implement RCPT TO
        self._send(f"RCPT TO:<{recipient}>")
        return self._recv()
    
    def data(self, content: str) -> SMTPResponse:
        self._send("DATA")
        intermediate = self._recv()
        if intermediate.code != 354:
            return intermediate
        # Send content with terminating period
        self.socket.sendall((content + CRLF + "." + CRLF).encode("utf-8"))
        return self._recv()
    
    def quit(self) -> SMTPResponse:
        self._send("QUIT")
        response = self._recv()
        self.socket.close()
        return response
    
    def send_email(self, email: Email) -> bool:
        """Send an email through complete SMTP sequence."""
        try:
            if not self.connect().is_success:
                return False
            if not self.ehlo().is_success:
                return False
            if not self.mail_from(email.sender).is_success:
                return False
            for recipient in email.recipients:
                if not self.rcpt_to(recipient).is_success:
                    return False
            if not self.data(email.to_data()).is_success:
                return False
            self.quit()
            return True
        except Exception as e:
            print(f"[!] Error: {e}")
            return False

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point."""
    print("=" * 70)
    print("Homework 12.1: SMTP Client Implementation")
    print("Computer Networks - Week 12 | ASE Bucharest, CSIE")
    print("=" * 70)
    
    print("""
SMTP Command Sequence:
  220 ← Server greeting
  EHLO → 250
  MAIL FROM → 250
  RCPT TO → 250
  DATA → 354
  [message] → 250
  QUIT → 221
""")
    
    email = Email(
        sender="student@lab.local",
        recipients=["teacher@lab.local"],
        subject="Week 12 Test",
        body="This is a test email."
    )
    
    print(f"Test email formatted:\n{email.to_data()}\n")
    
    try:
        client = SMTPClient()
        if client.send_email(email):
            print("\n✅ Email sent successfully!")
        else:
            print("\n❌ Email sending failed")
    except Exception as e:
        print(f"\n⚠️ Could not connect: {e}")
    
    print("\n📝 Key SMTP Response Codes:")
    print("   220 - Service ready")
    print("   250 - OK")
    print("   354 - Start mail input")
    print("   221 - Closing connection")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
