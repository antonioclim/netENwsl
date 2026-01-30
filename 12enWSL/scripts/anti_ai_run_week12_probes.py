#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# MODULE_DOCSTRING
# ═══════════════════════════════════════════════════════════════════════════════
"""Run the Week 12 protocol interactions required by the anti-AI challenge.

This script reads the challenge YAML and performs:

 - an SMTP send with the SMTP subject token
 - a JSON-RPC echo call with the RPC token
 - an XML-RPC echo call with the RPC token

If gRPC dependencies are installed and the gRPC service is running, it also performs a gRPC echo call.

The intent is to make it easy to generate evidence while focusing the homework write-up on analysis rather than plumbing.
"""

from __future__ import annotations

import argparse
import json
import smtplib
import sys
import urllib.request
from email.message import EmailMessage
from pathlib import Path
from typing import Any, Dict, List


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    import yaml
except ImportError:  # pragma: no cover
    print("[ERROR] PyYAML is required: pip install pyyaml")
    raise


def _jsonrpc_echo(url: str, token: str) -> Any:
    payload: Dict[str, Any] = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "echo",
        "params": [token],
        # Extra field included on purpose so the token appears in the request body even if params are modified.
        "token": token,
    }
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url=url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=5) as resp:
        data = resp.read().decode("utf-8", errors="replace")
    return json.loads(data)


def _xmlrpc_echo(url: str, token: str) -> Any:
    import xmlrpc.client

    proxy = xmlrpc.client.ServerProxy(url, allow_none=True)
    return proxy.echo(token)


def _grpc_echo(host: str, port: int, token: str) -> Any:
    try:
        import grpc  # type: ignore

        # Local imports relative to the generated stubs.
        from src.apps.rpc.grpc import calculator_pb2  # type: ignore
        from src.apps.rpc.grpc import calculator_pb2_grpc  # type: ignore
    except Exception as exc:  # pragma: no cover
        return {"skipped": True, "reason": f"gRPC dependencies not available: {exc}"}

    address = f"{host}:{port}"
    with grpc.insecure_channel(address) as channel:
        stub = calculator_pb2_grpc.CalculatorStub(channel)
        resp = stub.Echo(calculator_pb2.EchoRequest(message=token))
        return {"message": resp.message, "timestamp": resp.timestamp}


def _smtp_send(host: str, port: int, token: str, sender: str, recipient: str) -> None:
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = f"Week 12 SMTP {token}"
    msg.set_content(f"Anti-AI token: {token}\n")

    with smtplib.SMTP(host=host, port=port, timeout=10) as s:
        s.send_message(msg)


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Run Week 12 anti-AI probe interactions")
    ap.add_argument(
        "--challenge",
        type=Path,
        required=True,
        help="Challenge YAML (for example artifacts/anti_ai/challenge_<student>.yaml)",
    )
    ap.add_argument("--host", default="127.0.0.1", help="Service host (default: 127.0.0.1)")
    ap.add_argument("--smtp-from", default="student@lab.local", help="SMTP sender address")
    ap.add_argument("--smtp-to", default="teacher@lab.local", help="SMTP recipient address")
    ap.add_argument("--skip-grpc", action="store_true", help="Skip the optional gRPC echo probe")
    return ap.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.challenge.exists():
        print(f"[ERROR] Challenge not found: {args.challenge}")
        return 2

    ch = yaml.safe_load(args.challenge.read_text(encoding="utf-8"))
    ports = ch.get("ports") or {}
    host = str(args.host)

    smtp_port = int(ports.get("smtp", 1025))
    json_port = int(ports.get("jsonrpc", 6200))
    xml_port = int(ports.get("xmlrpc", 6201))
    grpc_port = int(ports.get("grpc", 6251))

    smtp_token = str(ch.get("smtp_subject_token"))
    rpc_token = str(ch.get("rpc_echo_token"))

    print("Week 12 anti-AI probes")
    print(f"SMTP:   {host}:{smtp_port}")
    print(f"JSON:   {host}:{json_port}")
    print(f"XML:    {host}:{xml_port}")
    print(f"gRPC:   {host}:{grpc_port}")
    print()

    # SMTP
    print("[1/3] SMTP send...")
    _smtp_send(host, smtp_port, smtp_token, sender=str(args.smtp_from), recipient=str(args.smtp_to))
    print("  ✓ SMTP sent")

    # JSON-RPC
    print("[2/3] JSON-RPC echo...")
    json_url = f"http://{host}:{json_port}"
    jr = _jsonrpc_echo(json_url, rpc_token)
    print(f"  ✓ JSON-RPC response: {jr}")

    # XML-RPC
    print("[3/3] XML-RPC echo...")
    xml_url = f"http://{host}:{xml_port}"
    xr = _xmlrpc_echo(xml_url, rpc_token)
    print(f"  ✓ XML-RPC response: {xr!r}")

    if not args.skip_grpc:
        print("[optional] gRPC echo...")
        gr = _grpc_echo(host, grpc_port, rpc_token)
        print(f"  ✓ gRPC: {gr}")
    else:
        print("[optional] gRPC echo skipped")

    print("\nDone. If you are capturing traffic, stop the capture and generate evidence.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
