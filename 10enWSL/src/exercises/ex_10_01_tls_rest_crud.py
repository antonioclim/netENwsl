#!/usr/bin/env python3
"""
Week 10 - Exercise 1: TLS Certificates and REST CRUD Operations
===================================================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

This exercise provides a small HTTPS server implemented with the Python
standard library. The server exposes a JSON API to demonstrate:

- TLS termination (HTTPS)
- HTTP verbs and status codes
- Basic CRUD operations over a resource collection

Objectives:
- Explain the role of TLS certificates in HTTPS
- Implement a minimal HTTPS server with CRUD endpoints
- Analyse the difference between HTTP and HTTPS traffic

Prerequisites:
- OpenSSL installed in WSL
- Python 3.11+
- requests library (for selftest)

Pair Programming Notes:
- Driver: Generate certificate and start server
- Navigator: Prepare curl commands and verify responses
- Swap after: First successful HTTPS request

Common Errors
-------------
1. "SSL: CERTIFICATE_VERIFY_FAILED" → Use curl -k or verify=False
2. "Connection refused on 8443" → Server not started; run 'serve' first
3. "OpenSSL not found" → Install with: sudo apt install openssl
4. "Address already in use" → Another process on port 8443; kill it or use --port

Security note
-------------
A self-signed certificate is generated for local laboratory use. In a real
deployment you would use a certificate issued by a trusted CA and enforce
strict TLS validation on the client.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import json
import os
import ssl
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8443
DEFAULT_CN = "lab.network.local"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TLS_DIR = PROJECT_ROOT / "output" / "tls"
DEFAULT_CERT = DEFAULT_TLS_DIR / "server.crt"
DEFAULT_KEY = DEFAULT_TLS_DIR / "server.key"


# ═══════════════════════════════════════════════════════════════════════════════
# DATA_MODEL
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class Resource:
    """A simple resource with id, name and value."""
    id: int
    name: str
    value: Any


class ResourceStore:
    """Thread-safe in-memory storage for resources."""
    
    def __init__(self) -> None:
        self._items: Dict[int, Resource] = {}
        self._next_id = 1
        self._lock = threading.Lock()

    def list(self) -> list[dict[str, Any]]:
        """Return all resources as a list of dictionaries."""
        with self._lock:
            return [self._to_dict(r) for r in self._items.values()]

    def create(self, name: str, value: Any) -> dict[str, Any]:
        """Create a new resource and return it."""
        with self._lock:
            rid = self._next_id
            self._next_id += 1
            res = Resource(id=rid, name=name, value=value)
            self._items[rid] = res
            return self._to_dict(res)

    def get(self, rid: int) -> Optional[dict[str, Any]]:
        """Get a resource by ID, or None if not found."""
        with self._lock:
            res = self._items.get(rid)
            return None if res is None else self._to_dict(res)

    def update(self, rid: int, name: Optional[str], value: Any) -> Optional[dict[str, Any]]:
        """Update a resource, return updated resource or None if not found."""
        with self._lock:
            res = self._items.get(rid)
            if res is None:
                return None
            if name is not None:
                res.name = name
            res.value = value
            return self._to_dict(res)

    def delete(self, rid: int) -> bool:
        """Delete a resource, return True if deleted."""
        with self._lock:
            return self._items.pop(rid, None) is not None

    @staticmethod
    def _to_dict(r: Resource) -> dict[str, Any]:
        """Convert Resource to dictionary."""
        return {"id": r.id, "name": r.name, "value": r.value}


STORE = ResourceStore()


# ═══════════════════════════════════════════════════════════════════════════════
# HTTP_HANDLER
# ═══════════════════════════════════════════════════════════════════════════════
class Handler(BaseHTTPRequestHandler):
    """HTTP request handler for the REST API."""
    
    server_version = "ASE-Week10-HTTPS/1.0"

    def _send_json(self, status: int, payload: Any | None = None) -> None:
        """Send a JSON response with the given status code."""
        body = b""
        if payload is not None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def _send_html(self, status: int, html: str) -> None:
        """Send an HTML response."""
        body = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> Tuple[Optional[dict[str, Any]], Optional[str]]:
        """Read and parse JSON from request body."""
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return None, "Missing JSON body"
        try:
            raw = self.rfile.read(length)
            data = json.loads(raw.decode("utf-8"))
            if not isinstance(data, dict):
                return None, "JSON body must be an object"
            return data, None
        except Exception as exc:
            return None, f"Invalid JSON: {exc}"

    def _route(self) -> Tuple[str, Optional[int]]:
        """Parse the request path and extract route information."""
        path = self.path.split("?", 1)[0]
        if path == "/":
            return "/", None
        if path == "/api/resources":
            return "/api/resources", None
        if path.startswith("/api/resources/"):
            try:
                rid = int(path.rsplit("/", 1)[1])
                return "/api/resources/:id", rid
            except ValueError:
                return "invalid", None
        return "unknown", None

    def do_GET(self) -> None:  # noqa: N802
        """Handle GET requests."""
        # Optional anti-AI verification endpoint.
        path = self.path.split("?", 1)[0]
        if path.startswith("/verify/"):
            token = path[len("/verify/"):]
            self._handle_verify(token)
            return

        route, rid = self._route()
        if route == "/":
            self._send_html(
                200,
                """<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Week 10 - HTTPS REST API</title></head>
<body>
<h1>Week 10 - HTTPS REST API</h1>
<p>Available endpoints:</p>
<ul>
  <li><code>GET /api/resources</code></li>
  <li><code>POST /api/resources</code></li>
  <li><code>GET /api/resources/&lt;id&gt;</code></li>
  <li><code>PUT /api/resources/&lt;id&gt;</code></li>
  <li><code>DELETE /api/resources/&lt;id&gt;</code></li>
</ul>
</body></html>""",
            )
            return

        if route == "/api/resources":
            self._send_json(200, {"resources": STORE.list()})
            return

        if route == "/api/resources/:id" and rid is not None:
            item = STORE.get(rid)
            if item is None:
                self._send_json(404, {"error": "Resource not found"})
            else:
                self._send_json(200, item)
            return

        if route == "invalid":
            self._send_json(400, {"error": "Invalid resource id"})
            return

        self._send_json(404, {"error": "Not found"})

    def _handle_verify(self, token: str) -> None:
        """Handle the anti-AI verification endpoint.

        This endpoint is intentionally simple and only becomes active if the
        server is started with a challenge configuration.
        """
        expected_token = getattr(self.server, "verify_token", None)
        expected_response = getattr(self.server, "verify_response", None)

        if not expected_token or expected_response is None:
            self._send_json(404, {"error": "Verification endpoint not enabled"})
            return

        if token != expected_token:
            self._send_json(404, {"error": "Invalid verification token"})
            return

        # Prevent caching.
        self.send_response(HTTPStatus.OK)
        body = json.dumps(expected_response, ensure_ascii=False).encode("utf-8")
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:  # noqa: N802
        """Handle POST requests (create resource)."""
        route, _ = self._route()
        if route != "/api/resources":
            self._send_json(404, {"error": "Not found"})
            return

        data, err = self._read_json()
        if err is not None or data is None:
            self._send_json(400, {"error": err})
            return

        name = str(data.get("name", "")).strip()
        if not name:
            self._send_json(400, {"error": "Field 'name' is required"})
            return

        value = data.get("value")
        created = STORE.create(name=name, value=value)
        self._send_json(201, created)

    def do_PUT(self) -> None:  # noqa: N802
        """Handle PUT requests (update resource)."""
        route, rid = self._route()
        if route != "/api/resources/:id" or rid is None:
            self._send_json(404, {"error": "Not found"})
            return

        data, err = self._read_json()
        if err is not None or data is None:
            self._send_json(400, {"error": err})
            return

        name = data.get("name")
        if name is not None:
            name = str(name).strip()
            if not name:
                self._send_json(400, {"error": "Field 'name' must not be empty"})
                return

        value = data.get("value")
        updated = STORE.update(rid=rid, name=name, value=value)
        if updated is None:
            self._send_json(404, {"error": "Resource not found"})
            return
        self._send_json(200, updated)

    def do_DELETE(self) -> None:  # noqa: N802
        """Handle DELETE requests (remove resource)."""
        route, rid = self._route()
        if route != "/api/resources/:id" or rid is None:
            self._send_json(404, {"error": "Not found"})
            return

        if not STORE.delete(rid):
            self._send_json(404, {"error": "Resource not found"})
            return
        self._send_json(204, None)

    def log_message(self, fmt: str, *args: Any) -> None:
        """Log HTTP requests concisely."""
        sys.stderr.write("[HTTP] %s - %s\n" % (self.address_string(), fmt % args))


# ═══════════════════════════════════════════════════════════════════════════════
# CERTIFICATE_GENERATION
# ═══════════════════════════════════════════════════════════════════════════════
def generate_self_signed_certificate(cert_path: Path, key_path: Path, common_name: str) -> None:
    """
    Generate a self-signed TLS certificate using OpenSSL.
    
    💭 PREDICTION: What fields will the certificate contain?
    Think about: Country, Organisation, Common Name (CN).
    """
    cert_path.parent.mkdir(parents=True, exist_ok=True)

    if cert_path.exists() and key_path.exists():
        return

    openssl = "openssl"
    cmd = [
        openssl,
        "req",
        "-x509",
        "-newkey",
        "rsa:2048",
        "-nodes",
        "-keyout",
        str(key_path),
        "-out",
        str(cert_path),
        "-days",
        "365",
        "-subj",
        f"/C=RO/O=ASE-CSIE/OU=Computer Networks/CN={common_name}",
        "-addext",
        f"subjectAltName=DNS:{common_name},IP:127.0.0.1",
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        raise SystemExit("OpenSSL is required to generate the self-signed certificate")
    except subprocess.CalledProcessError as exc:
        raise SystemExit(f"OpenSSL failed to generate a certificate: {exc}")


# ═══════════════════════════════════════════════════════════════════════════════
# SERVER_SETUP
# ═══════════════════════════════════════════════════════════════════════════════
def load_https_challenge(challenge_path: Path) -> tuple[int, str, Dict[str, Any]]:
    """Load the anti-AI HTTPS challenge from a Week 10 challenge YAML file.

    The file is produced by :mod:`anti_cheat.challenge_generator`.

    Returns:
        (port, token, expected_response)
    """
    try:
        import yaml  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise SystemExit(f"PyYAML is required to read the challenge file: {exc}")

    data = yaml.safe_load(challenge_path.read_text(encoding="utf-8")) or {}
    https = (data.get("challenges") or {}).get("https")
    if not https:
        raise SystemExit("Challenge file does not contain an HTTPS challenge")

    port = int(https.get("port"))
    endpoint = str(https.get("endpoint", ""))
    expected = https.get("expected_response")

    if not endpoint.startswith("/verify/"):
        raise SystemExit("HTTPS challenge endpoint is invalid (expected /verify/<token>)")
    token = endpoint.split("/verify/", 1)[1]
    if not token:
        raise SystemExit("HTTPS challenge token is missing")

    if not isinstance(expected, dict):
        raise SystemExit("HTTPS challenge expected_response must be a JSON object")

    return port, token, expected


def build_server(
    host: str,
    port: int,
    cert: Path,
    key: Path,
    verify_token: Optional[str] = None,
    verify_response: Optional[Dict[str, Any]] = None,
) -> ThreadingHTTPServer:
    """
    Build an HTTPS server with the given certificate.
    
    💭 PREDICTION: What will happen if we try to connect with HTTP (not HTTPS)?
    """
    httpd = ThreadingHTTPServer((host, port), Handler)
    # Attach optional anti-AI verification parameters.
    setattr(httpd, "verify_token", verify_token)
    setattr(httpd, "verify_response", verify_response)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=str(cert), keyfile=str(key))
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    return httpd


def serve(
    host: str,
    port: int,
    cert: Path,
    key: Path,
    common_name: str,
    verify_token: Optional[str] = None,
    verify_response: Optional[Dict[str, Any]] = None,
) -> None:
    """Start the HTTPS server and serve requests."""
    generate_self_signed_certificate(cert, key, common_name)
    httpd = build_server(host, port, cert, key, verify_token=verify_token, verify_response=verify_response)

    print("[INFO] HTTPS server ready")
    print(f"[INFO] URL: https://{host}:{httpd.server_address[1]}/")
    print(f"[INFO] Certificate: {cert}")
    if verify_token and verify_response is not None:
        print("[INFO] Verification endpoint enabled")
        print(f"[INFO] Verify URL: https://{host}:{httpd.server_address[1]}/verify/{verify_token}")
    print("[INFO] Press Ctrl+C to stop")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
        print("[INFO] Server stopped")


# ═══════════════════════════════════════════════════════════════════════════════
# SELFTEST
# ═══════════════════════════════════════════════════════════════════════════════
def selftest() -> int:
    """
    Run automated tests for the HTTPS server.
    
    💭 PREDICTION: What status codes should CREATE, UPDATE and DELETE return?
    - CREATE: ?
    - UPDATE: ?
    - DELETE: ?
    """
    try:
        import requests  # type: ignore
        import urllib3

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    except Exception as exc:
        print(f"[ERROR] requests is required for selftest: {exc}")
        return 1

    cert = DEFAULT_CERT
    key = DEFAULT_KEY
    generate_self_signed_certificate(cert, key, DEFAULT_CN)

    server = build_server(DEFAULT_HOST, 0, cert, key)
    actual_port = server.server_address[1]

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    base = f"https://{DEFAULT_HOST}:{actual_port}"

    try:
        # Create — expect 201 Created
        r = requests.post(
            f"{base}/api/resources",
            json={"name": "example", "value": 123},
            timeout=5,
            verify=False,
        )
        assert r.status_code == HTTPStatus.CREATED, r.text
        created = r.json()
        rid = int(created["id"])

        # List — expect 200 OK
        r = requests.get(f"{base}/api/resources", timeout=5, verify=False)
        assert r.status_code == HTTPStatus.OK, r.text
        data = r.json()
        assert any(x["id"] == rid for x in data["resources"])

        # Update — expect 200 OK
        r = requests.put(
            f"{base}/api/resources/{rid}",
            json={"name": "example-updated", "value": 456},
            timeout=5,
            verify=False,
        )
        assert r.status_code == HTTPStatus.OK, r.text
        assert r.json()["name"] == "example-updated"

        # Delete — expect 204 No Content
        r = requests.delete(f"{base}/api/resources/{rid}", timeout=5, verify=False)
        assert r.status_code == HTTPStatus.NO_CONTENT

        print("[OK] HTTPS selftest passed")
        return 0
    except AssertionError as exc:
        print(f"[ERROR] HTTPS selftest failed: {exc}")
        return 1
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


# ═══════════════════════════════════════════════════════════════════════════════
# ARGUMENT_PARSING
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Week 10 HTTPS REST API")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_serve = sub.add_parser("serve", help="Start the HTTPS server")
    p_serve.add_argument("--host", default=DEFAULT_HOST)
    p_serve.add_argument("--port", type=int, default=DEFAULT_PORT)
    p_serve.add_argument("--cert", default=str(DEFAULT_CERT))
    p_serve.add_argument("--key", default=str(DEFAULT_KEY))
    p_serve.add_argument("--cn", default=DEFAULT_CN, help="Certificate common name")
    p_serve.add_argument(
        "--challenge",
        type=str,
        default=None,
        help=(
            "Path to a Week 10 anti-AI challenge YAML file. "
            "When supplied, the server enables /verify/<token> and uses the HTTPS port from the file."
        ),
    )

    p_cert = sub.add_parser("generate-cert", help="Generate a self-signed TLS certificate")
    p_cert.add_argument("--cert", default=str(DEFAULT_CERT))
    p_cert.add_argument("--key", default=str(DEFAULT_KEY))
    p_cert.add_argument("--cn", default=DEFAULT_CN)

    sub.add_parser("selftest", help="Run a local selftest")

    return parser.parse_args(argv)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main(argv: list[str]) -> int:
    """Main entry point."""
    args = parse_args(argv)

    if args.cmd == "generate-cert":
        cert = Path(args.cert)
        key = Path(args.key)
        generate_self_signed_certificate(cert, key, args.cn)
        print(f"[OK] Certificate generated: {cert}")
        print(f"[OK] Key generated: {key}")
        return 0

    if args.cmd == "serve":
        verify_token = None
        verify_response = None
        port = args.port

        if args.challenge:
            challenge_path = Path(args.challenge)
            port, verify_token, verify_response = load_https_challenge(challenge_path)
            if port != args.port:
                print(f"[INFO] Port overridden by challenge file: {args.port} -> {port}")
            print("[INFO] Anti-AI verification enabled from challenge file")

        serve(
            args.host,
            port,
            Path(args.cert),
            Path(args.key),
            args.cn,
            verify_token=verify_token,
            verify_response=verify_response,
        )
        return 0

    if args.cmd == "selftest":
        return selftest()

    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
