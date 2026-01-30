"""Local integration tests for Week 12 applications.

These tests start the servers in-process on ephemeral ports and exercise the public
client interfaces. They are designed to run without Docker.
"""

from __future__ import annotations

import json
import threading
import time
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.request import Request, urlopen

import pytest

from src.apps.email.smtp_client import send_email
from src.apps.email.smtp_server import SMTPHandler, SMTPServer
from src.apps.rpc.jsonrpc.jsonrpc_server import Handler as JSONRPCHandler
from src.apps.rpc.xmlrpc.xmlrpc_server import CalculatorService, RequestHandler


def _run_in_thread(target, *, daemon: bool = True) -> threading.Thread:
    t = threading.Thread(target=target, daemon=daemon)
    t.start()
    return t


def test_smtp_server_and_client_round_trip() -> None:
    with TemporaryDirectory() as td:
        spool = Path(td)

        server = SMTPServer(("127.0.0.1", 0), SMTPHandler, spool_dir=spool)
        host, port = server.server_address
        thread = _run_in_thread(server.serve_forever)

        try:
            send_email(
                host=str(host),
                port=int(port),
                sender="alice@example.test",
                recipients=["bob@example.test"],
                subject="Test SMTP",
                body="Hello from test",
            )

            # Give the server a moment to write the spool.
            time.sleep(0.2)
            emls = list(spool.glob("*.eml"))
            assert emls, "SMTP server did not store any .eml files"
            text = emls[0].read_text(encoding="utf-8", errors="replace")
            assert "From:" in text
            assert "To:" in text
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)


def test_jsonrpc_server_echo() -> None:
    from http.server import ThreadingHTTPServer

    server = ThreadingHTTPServer(("127.0.0.1", 0), JSONRPCHandler)
    host, port = server.server_address
    thread = _run_in_thread(server.serve_forever)

    try:
        payload = {"jsonrpc": "2.0", "id": 1, "method": "echo", "params": ["hi"]}
        body = json.dumps(payload).encode("utf-8")
        req = Request(url=f"http://{host}:{port}", data=body, headers={"Content-Type": "application/json"})
        with urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        assert data["result"] == "hi"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_xmlrpc_server_echo() -> None:
    import xmlrpc.client
    from xmlrpc.server import SimpleXMLRPCServer

    service = CalculatorService()
    server = SimpleXMLRPCServer(("127.0.0.1", 0), requestHandler=RequestHandler, allow_none=True, logRequests=False)
    server.register_instance(service)
    server.register_introspection_functions()
    host, port = server.server_address
    thread = _run_in_thread(server.serve_forever)

    try:
        proxy = xmlrpc.client.ServerProxy(f"http://{host}:{port}", allow_none=True)
        assert proxy.echo("hello") == "hello"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_grpc_server_echo_if_available() -> None:
    grpc = pytest.importorskip("grpc")
    from concurrent import futures

    from src.apps.rpc.grpc.calculator_pb2 import EchoRequest
    from src.apps.rpc.grpc.calculator_pb2_grpc import CalculatorStub, add_CalculatorServicer_to_server
    from src.apps.rpc.grpc.grpc_server import CalculatorService

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    add_CalculatorServicer_to_server(CalculatorService(), server)
    port = server.add_insecure_port("127.0.0.1:0")
    server.start()

    try:
        with grpc.insecure_channel(f"127.0.0.1:{port}") as channel:
            stub = CalculatorStub(channel)
            resp = stub.Echo(EchoRequest(message="ping"))
            assert resp.message == "ping"
    finally:
        server.stop(grace=None)