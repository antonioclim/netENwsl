#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# MODULE_DOCSTRING
# ═══════════════════════════════════════════════════════════════════════════════
"""XML-RPC server for Week 12.

This server uses Python's built-in xmlrpc.server to expose a small calculator API.

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

Protocol: XML-RPC over HTTP
"""


# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import logging
import time
from dataclasses import dataclass, field
from typing import Dict, Any
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler


LOG = logging.getLogger("week12.xmlrpc")



# ═══════════════════════════════════════════════════════════════════════════════
# REQUESTHANDLER_CLASS
# ═══════════════════════════════════════════════════════════════════════════════
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/", "/RPC2")


@dataclass

# ═══════════════════════════════════════════════════════════════════════════════
# CALCULATORSERVICE_CLASS
# ═══════════════════════════════════════════════════════════════════════════════
class CalculatorService:
    call_counts: Dict[str, int] = field(default_factory=dict)

    def _count(self, name: str) -> None:
        self.call_counts[name] = self.call_counts.get(name, 0) + 1

    def add(self, a: float, b: float) -> float:
        self._count("add")
        return float(a) + float(b)

    def subtract(self, a: float, b: float) -> float:
        self._count("subtract")
        return float(a) - float(b)

    def multiply(self, a: float, b: float) -> float:
        self._count("multiply")
        return float(a) * float(b)

    def divide(self, a: float, b: float) -> float:
        self._count("divide")
        b = float(b)
        if b == 0:
            raise ValueError("Division by zero")
        return float(a) / b

    def echo(self, value: Any) -> Any:
        self._count("echo")
        return value

    def sort_list(self, items: Any, reverse: bool = False) -> Any:
        """Sort a list of comparable items."""
        self._count("sort_list")
        if not isinstance(items, list):
            raise ValueError("items must be a list")
        return sorted(items, reverse=bool(reverse))

    def get_time(self) -> str:
        self._count("get_time")
        return time.strftime("%Y-%m-%d %H:%M:%S %Z")

    def get_server_info(self) -> Dict[str, str]:
        self._count("get_server_info")
        return {
            "name": "Week 12 XML-RPC server",
            "version": "1.0",
            "protocol": "XML-RPC over HTTP",
        }

    def get_stats(self) -> Dict[str, Any]:
        self._count("get_stats")
        total = sum(self.call_counts.values())
        return {"total_calls": total, "call_counts": dict(self.call_counts)}



# ═══════════════════════════════════════════════════════════════════════════════
# PARSE_ARGS_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Week 12 XML-RPC server")
    ap.add_argument("--host", default="127.0.0.1", help="Bind address")
    ap.add_argument("--port", type=int, default=6201, help="TCP port (default: 6201)")
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

    service = CalculatorService()

    with SimpleXMLRPCServer((host, port), requestHandler=RequestHandler, allow_none=True, logRequests=True) as server:
        server.register_instance(service)
        server.register_introspection_functions()

        LOG.info("Starting XML-RPC server on http://%s:%s", host, port)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            LOG.info("Stopping (Ctrl+C)")
    return 0



# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    raise SystemExit(main())
