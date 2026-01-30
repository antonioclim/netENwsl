#!/usr/bin/env python3
"""Week 10 - Minimal custom DNS server (dnslib).

This container demonstrates:
- UDP request/response behaviour
- DNS message structure (header, question, answer sections and RCODE)
- The difference between Docker's embedded DNS and a custom authoritative server

The server responds with static A records and optional TXT records.

Examples
--------
From the host:
  dig @127.0.0.1 -p 5353 myservice.lab.local +short

TXT record (used by the Week 10 anti-AI challenge):
  dig @127.0.0.1 -p 5353 verify-<token>.lab.local TXT +short

From the debug container:
  dig @dns-server -p 5353 api.lab.local +short

NETWORKING class - ASE, CSIE | by ing. dr. Antonio Clim
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import socket
from typing import Dict

from dnslib import A, CNAME, DNSRecord, QTYPE, RR, TXT


# Static records used in the laboratory.
STATIC_A_RECORDS: Dict[str, str] = {
    "myservice.lab.local": "10.10.10.10",
    "api.lab.local": "10.10.10.20",
    "ssh.lab.local": "172.20.0.22",
    "ftp.lab.local": "172.20.0.21",
    "web.lab.local": "172.20.0.10",
    "dns.lab.local": "172.20.0.53",
}

# Static CNAME records.
# Example: STATIC_CNAME_RECORDS["www.student.lab.local"] = "student.lab.local"
STATIC_CNAME_RECORDS: Dict[str, str] = {}

# TXT records are intentionally kept separate so students can add to them
# without touching the A records used by the exercises.
STATIC_TXT_RECORDS: Dict[str, str] = {
    # Example:
    # "student.lab.local": "Your Name Here",
}


# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def _normalise_name(name: str) -> str:
    """Normalise a DNS name (remove trailing dot and lowercase)."""
    return name.rstrip(".").lower()


def build_response(request: DNSRecord) -> DNSRecord:
    """Build a DNS response for a given request."""
    reply = request.reply()

    qname = _normalise_name(str(request.q.qname))
    qtype = QTYPE[request.q.qtype]

    if qtype == "A":
        if qname in STATIC_A_RECORDS:
            reply.add_answer(RR(qname, QTYPE.A, rdata=A(STATIC_A_RECORDS[qname]), ttl=60))
            return reply

        # If this name is an alias, return the CNAME and (when possible) the A record
        # of the canonical name. This matches what students typically observe when
        # querying with ``dig``.
        if qname in STATIC_CNAME_RECORDS:
            target = _normalise_name(STATIC_CNAME_RECORDS[qname])
            reply.add_answer(RR(qname, QTYPE.CNAME, rdata=CNAME(target), ttl=60))
            if target in STATIC_A_RECORDS:
                reply.add_answer(RR(target, QTYPE.A, rdata=A(STATIC_A_RECORDS[target]), ttl=60))
            return reply

        reply.header.rcode = 3  # NXDOMAIN
        return reply

    if qtype == "CNAME":
        if qname in STATIC_CNAME_RECORDS:
            target = _normalise_name(STATIC_CNAME_RECORDS[qname])
            reply.add_answer(RR(qname, QTYPE.CNAME, rdata=CNAME(target), ttl=60))
        else:
            reply.header.rcode = 3  # NXDOMAIN
        return reply

    if qtype == "TXT":
        if qname in STATIC_TXT_RECORDS:
            reply.add_answer(RR(qname, QTYPE.TXT, rdata=TXT(STATIC_TXT_RECORDS[qname]), ttl=60))
        else:
            reply.header.rcode = 3  # NXDOMAIN
        return reply

    # For teaching simplicity we do not implement other types.
    return reply


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> None:
    parser = argparse.ArgumentParser(description="Week 10 DNS server (dnslib)")
    parser.add_argument("--host", default="0.0.0.0", help="Bind address")
    parser.add_argument("--port", type=int, default=5353, help="UDP port")
    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((args.host, args.port))

    print("[INFO] Week 10 DNS server started")
    print(f"[INFO] Bind: {args.host}:{args.port} (UDP)")

    print("[INFO] A records:")
    for k, v in STATIC_A_RECORDS.items():
        print(f"  - {k} -> {v}")

    if STATIC_CNAME_RECORDS:
        print("[INFO] CNAME records:")
        for k, v in STATIC_CNAME_RECORDS.items():
            print(f"  - {k} -> {v}")
    else:
        print("[INFO] CNAME records: (none)")

    if STATIC_TXT_RECORDS:
        print("[INFO] TXT records:")
        for k, v in STATIC_TXT_RECORDS.items():
            print(f"  - {k} -> {v!r}")
    else:
        print("[INFO] TXT records: (none)")

    while True:
        try:
            data, addr = sock.recvfrom(512)
            request = DNSRecord.parse(data)
            qname = _normalise_name(str(request.q.qname))
            qtype = QTYPE[request.q.qtype]

            print(f"[DNS] Query from {addr[0]}:{addr[1]} - {qname} ({qtype})")

            reply = build_response(request)
            sock.sendto(reply.pack(), addr)
        except Exception as exc:
            print(f"[WARN] Failed to process DNS query: {exc}")


if __name__ == "__main__":
    main()
