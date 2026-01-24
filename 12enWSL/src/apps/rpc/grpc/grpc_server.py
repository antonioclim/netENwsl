#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# MODULE_DOCSTRING
# ═══════════════════════════════════════════════════════════════════════════════
"""gRPC calculator server for Week 12."""


# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import logging
import time
from concurrent import futures
from typing import Dict

import grpc

import sys
from pathlib import Path

# Allow running this file directly: python src/rpc/grpc/grpc_server.py
sys.path.insert(0, str(Path(__file__).resolve().parent))

import calculator_pb2
import calculator_pb2_grpc


LOG = logging.getLogger("week12.grpc")



# ═══════════════════════════════════════════════════════════════════════════════
# CALCULATORSERVICE_CLASS
# ═══════════════════════════════════════════════════════════════════════════════
class CalculatorService(calculator_pb2_grpc.CalculatorServicer):
    def __init__(self) -> None:
        self._start = time.time()
        self._counts: Dict[str, int] = {}

    def _count(self, name: str) -> None:
        self._counts[name] = self._counts.get(name, 0) + 1

    def _ts(self) -> int:
        return int(time.time())

    def Add(self, request, context):
        self._count("Add")
        return calculator_pb2.CalcResponse(result=request.a + request.b, operation="add", timestamp=self._ts())

    def Subtract(self, request, context):
        self._count("Subtract")
        return calculator_pb2.CalcResponse(result=request.a - request.b, operation="subtract", timestamp=self._ts())

    def Multiply(self, request, context):
        self._count("Multiply")
        return calculator_pb2.CalcResponse(result=request.a * request.b, operation="multiply", timestamp=self._ts())

    def Divide(self, request, context):
        self._count("Divide")
        if request.b == 0:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Division by zero")
        return calculator_pb2.CalcResponse(result=request.a / request.b, operation="divide", timestamp=self._ts())

    def Echo(self, request, context):
        self._count("Echo")
        return calculator_pb2.EchoResponse(message=request.message, timestamp=self._ts())

    def Sha256Hash(self, request, context):
        import hashlib

        self._count("Sha256Hash")
        h = hashlib.sha256(request.input.encode("utf-8")).hexdigest()
        return calculator_pb2.HashResponse(hash=h, timestamp=self._ts())

    def GetStats(self, request, context):
        self._count("GetStats")
        total = sum(self._counts.values())
        uptime = int(time.time() - self._start)
        return calculator_pb2.StatsResponse(call_counts=self._counts, total_calls=total, uptime_seconds=uptime)



# ═══════════════════════════════════════════════════════════════════════════════
# PARSE_ARGS_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Week 12 gRPC calculator server")
    ap.add_argument("--host", default="127.0.0.1", help="Bind address")
    ap.add_argument("--port", type=int, default=6251, help="TCP port (default: 6251)")
    ap.add_argument("--verbose", action="store_true", help="Verbose logging")
    return ap.parse_args()



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    args = parse_args()
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level, format="[%(asctime)s] %(levelname)s %(name)s: %(message)s")

    address = f"{args.host}:{int(args.port)}"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    calculator_pb2_grpc.add_CalculatorServicer_to_server(CalculatorService(), server)
    server.add_insecure_port(address)

    LOG.info("Starting gRPC server on %s", address)
    server.start()

    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        LOG.info("Stopping (Ctrl+C)")
        server.stop(grace=None)
    return 0



# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    raise SystemExit(main())
