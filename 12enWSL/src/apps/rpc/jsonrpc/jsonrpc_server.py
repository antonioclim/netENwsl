#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# MODULE_DOCSTRING
# ═══════════════════════════════════════════════════════════════════════════════
"""JSON-RPC 2.0 server for Week 12.

The server exposes a small 'calculator' API over HTTP POST. It is designed for
teaching and includes:

- clear error handling (JSON-RPC error objects)
- optional batch requests (JSON-RPC 2.0 feature)
- a few utility methods to illustrate non-numeric parameters

Supported methods:
  - add(a, b)
  - subtract(a, b)
  - multiply(a, b)
  - divide(a, b)
  - echo(value)
  - sort_list(items, reverse=False)
  - get_time()
  - get_server_info()
  - get_stats()

Protocol: JSON-RPC 2.0 over HTTP
"""


# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import json
import logging
import threading
import time
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict, List, Tuple


LOG = logging.getLogger("week12.jsonrpc")

JSONRPC_VERSION = "2.0"
SERVER_VERSION = "Week12-JSONRPC/1.1"

_START_TIME = time.time()
_CALL_COUNTS: Dict[str, int] = {}
_CALL_LOCK = threading.Lock()



# ═══════════════════════════════════════════════════════════════════════════════
# JSONRPCERROR_CLASS
# ═══════════════════════════════════════════════════════════════════════════════
class JSONRPCError(Exception):
    def __init__(self, code: int, message: str, data: Any | None = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.data = data



# ═══════════════════════════════════════════════════════════════════════════════
# PRIVATE_HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def _count(method: str) -> None:
    with _CALL_LOCK:
        _CALL_COUNTS[method] = _CALL_COUNTS.get(method, 0) + 1



# ═══════════════════════════════════════════════════════════════════════════════
# PRIVATE_HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def _ok(result: Any, req_id: Any) -> Dict[str, Any]:
    return {"jsonrpc": JSONRPC_VERSION, "id": req_id, "result": result}



# ═══════════════════════════════════════════════════════════════════════════════
# PRIVATE_HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def _err(err: JSONRPCError, req_id: Any) -> Dict[str, Any]:
    obj: Dict[str, Any] = {"code": err.code, "message": err.message}
    if err.data is not None:
        obj["data"] = err.data
    return {"jsonrpc": JSONRPC_VERSION, "id": req_id, "error": obj}



# ═══════════════════════════════════════════════════════════════════════════════
# PRIVATE_HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def _parse_json(raw: bytes) -> Any:
    try:
        return json.loads(raw.decode("utf-8"))
    except Exception as exc:
        raise JSONRPCError(-32700, "Parse error", data=str(exc))



# ═══════════════════════════════════════════════════════════════════════════════
# PRIVATE_HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def _validate_request(obj: Any) -> Dict[str, Any]:
    if not isinstance(obj, dict):
        raise JSONRPCError(-32600, "Invalid Request", data="Request must be a JSON object")
    if obj.get("jsonrpc") != JSONRPC_VERSION:
        raise JSONRPCError(-32600, "Invalid Request", data="jsonrpc must be '2.0'")
    if "method" not in obj:
        raise JSONRPCError(-32600, "Invalid Request", data="Missing 'method'")
    return obj



# ═══════════════════════════════════════════════════════════════════════════════
# PRIVATE_HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def _get_params(obj: Dict[str, Any]) -> Tuple[list, dict]:
    params = obj.get("params", [])
    if params is None:
        return [], {}
    if isinstance(params, list):
        return params, {}
    if isinstance(params, dict):
        return [], params
    raise JSONRPCError(-32602, "Invalid params", data="params must be a list or object")



# ═══════════════════════════════════════════════════════════════════════════════
# PRIVATE_HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def _need2(pos: list, named: dict) -> Tuple[float, float]:
    if pos and len(pos) >= 2:
        return float(pos[0]), float(pos[1])
    if "a" in named and "b" in named:
        return float(named["a"]), float(named["b"])
    raise JSONRPCError(-32602, "Invalid params", data="Expected parameters a and b")



# ═══════════════════════════════════════════════════════════════════════════════
# PRIVATE_HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def _dispatch(method: str, pos: list, named: dict) -> Any:
    method = method.strip()

    if method == "add":
        _count("add")
        a, b = _need2(pos, named)
        return a + b

    if method == "subtract":
        _count("subtract")
        a, b = _need2(pos, named)
        return a - b

    if method == "multiply":
        _count("multiply")
        a, b = _need2(pos, named)
        return a * b

    if method == "divide":
        _count("divide")
        a, b = _need2(pos, named)
        if b == 0:
            raise JSONRPCError(-32000, "Division by zero")
        return a / b

    if method == "echo":
        _count("echo")
        if pos:
            return pos[0]
        if "value" in named:
            return named["value"]
        return None

    if method == "sort_list":
        _count("sort_list")
        items = None
        reverse = False
        if pos:
            items = pos[0]
            if len(pos) > 1:
                reverse = bool(pos[1])
        else:
            items = named.get("items")
            reverse = bool(named.get("reverse", False))
        if not isinstance(items, list):
            raise JSONRPCError(-32602, "Invalid params", data="items must be a list")
        return sorted(items, reverse=reverse)

    if method == "get_time":
        _count("get_time")
        return time.strftime("%Y-%m-%d %H:%M:%S %Z")

    if method == "get_server_info":
        _count("get_server_info")
        return {
            "name": "Week 12 JSON-RPC server",
            "version": "1.1",
            "protocol": "JSON-RPC 2.0 over HTTP",
        }

    if method == "get_stats":
        _count("get_stats")
        with _CALL_LOCK:
            total = sum(_CALL_COUNTS.values())
            counts = dict(_CALL_COUNTS)
        uptime = int(time.time() - _START_TIME)
        return {"total_calls": total, "uptime_seconds": uptime, "call_counts": counts}

    raise JSONRPCError(-32601, "Method not found", data=method)



# ═══════════════════════════════════════════════════════════════════════════════
# PRIVATE_HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def _handle_one(raw_req: Any) -> Tuple[bool, Dict[str, Any] | None]:
    """Handle one request object. Returns (has_response, response_obj)."""
    req_id: Any = None
    try:
        req = _validate_request(raw_req)
        req_id = req.get("id", None)
        method = str(req.get("method"))
        pos, named = _get_params(req)
        result = _dispatch(method, pos, named)

        # Notification (id is absent): do not reply
        if "id" not in req:
            return False, None

        return True, _ok(result, req_id)
    except JSONRPCError as e:
        if raw_req and isinstance(raw_req, dict) and "id" not in raw_req:
            return False, None
        return True, _err(e, req_id)
    except Exception as exc:
        LOG.exception("Unhandled server error")
        if raw_req and isinstance(raw_req, dict) and "id" not in raw_req:
            return False, None
        return True, _err(JSONRPCError(-32603, "Internal error", data=str(exc)), req_id)



# ═══════════════════════════════════════════════════════════════════════════════
# HANDLER_CLASS
# ═══════════════════════════════════════════════════════════════════════════════
class Handler(BaseHTTPRequestHandler):
    server_version = SERVER_VERSION

    def log_message(self, fmt: str, *args: Any) -> None:
        LOG.info("%s - %s", self.address_string(), fmt % args)

    def do_GET(self) -> None:
        body = (
            "Week 12 JSON-RPC server\n"
            "Send JSON-RPC 2.0 requests via HTTP POST.\n"
            "Example: {\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"add\",\"params\":[2,3]}\n"
        ).encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length)

        try:
            parsed = _parse_json(raw)
        except JSONRPCError as e:
            out = json.dumps(_err(e, None)).encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(out)))
            self.end_headers()
            self.wfile.write(out)
            return

        # Single request
        if isinstance(parsed, dict):
            has_resp, resp_obj = _handle_one(parsed)
            if not has_resp:
                self.send_response(HTTPStatus.NO_CONTENT)
                self.end_headers()
                return
            out = json.dumps(resp_obj).encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(out)))
            self.end_headers()
            self.wfile.write(out)
            return

        # Batch request
        if isinstance(parsed, list):
            if len(parsed) == 0:
                out = json.dumps(_err(JSONRPCError(-32600, "Invalid Request", data="Empty batch"), None)).encode("utf-8")
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(out)))
                self.end_headers()
                self.wfile.write(out)
                return

            responses: List[Dict[str, Any]] = []
            for item in parsed:
                has_resp, resp_obj = _handle_one(item)
                if has_resp and resp_obj is not None:
                    responses.append(resp_obj)

            if not responses:
                self.send_response(HTTPStatus.NO_CONTENT)
                self.end_headers()
                return

            out = json.dumps(responses).encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(out)))
            self.end_headers()
            self.wfile.write(out)
            return

        # Anything else is invalid
        out = json.dumps(_err(JSONRPCError(-32600, "Invalid Request", data="Expected object or array"), None)).encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)



# ═══════════════════════════════════════════════════════════════════════════════
# PARSE_ARGS_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Week 12 JSON-RPC server")
    ap.add_argument("--host", default="127.0.0.1", help="Bind address")
    ap.add_argument("--port", type=int, default=6200, help="TCP port (default: 6200)")
    ap.add_argument("--verbose", action="store_true", help="Verbose logging")
    return ap.parse_args()



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    args = parse_args()
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level, format="[%(asctime)s] %(levelname)s %(name)s: %(message)s")

    host = args.host
    port = int(args.port)

    LOG.info("Starting JSON-RPC server on http://%s:%s", host, port)
    httpd = ThreadingHTTPServer((host, port), Handler)
    try:
        httpd.serve_forever(poll_interval=0.2)
    except KeyboardInterrupt:
        LOG.info("Stopping (Ctrl+C)")
    finally:
        httpd.server_close()
    return 0



# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    raise SystemExit(main())
