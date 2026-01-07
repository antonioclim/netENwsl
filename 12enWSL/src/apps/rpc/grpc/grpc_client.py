#!/usr/bin/env python3
"""gRPC client demo for Week 12."""

from __future__ import annotations

import argparse
import grpc

import sys
from pathlib import Path

# Allow running this file directly: python src/rpc/grpc/grpc_client.py
sys.path.insert(0, str(Path(__file__).resolve().parent))

import calculator_pb2
import calculator_pb2_grpc


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Week 12 gRPC client")
    ap.add_argument("--host", default="127.0.0.1", help="Server host")
    ap.add_argument("--port", type=int, default=6251, help="Server port")
    ap.add_argument("--demo", action="store_true", help="Run the interactive demo")
    ap.add_argument("--check", action="store_true", help="Run a minimal self-check and exit")
    return ap.parse_args()


def run_demo(stub: calculator_pb2_grpc.CalculatorStub) -> None:
    print("Week 12 gRPC demo")
    print()

    r = stub.Add(calculator_pb2.CalcRequest(a=2, b=3))
    print(f"Add(2, 3) => {r.result} ({r.operation})")

    r = stub.Multiply(calculator_pb2.CalcRequest(a=6, b=7))
    print(f"Multiply(6, 7) => {r.result} ({r.operation})")

    e = stub.Echo(calculator_pb2.EchoRequest(message="Hello from gRPC"))
    print(f"Echo => {e.message}")

    h = stub.Sha256Hash(calculator_pb2.HashRequest(input="week12"))
    print(f"SHA-256('week12') => {h.hash}")

    stats = stub.GetStats(calculator_pb2.EmptyRequest())
    print(f"Stats => total_calls={stats.total_calls}, uptime_seconds={stats.uptime_seconds}")
    print(f"Call counts => {dict(stats.call_counts)}")

    print()
    print("Intentional error demo:")
    try:
        stub.Divide(calculator_pb2.CalcRequest(a=1, b=0))
    except grpc.RpcError as exc:
        print(f"Divide(1, 0) failed: {exc.code().name} — {exc.details()}")


def run_check(stub: calculator_pb2_grpc.CalculatorStub) -> int:
    r = stub.Add(calculator_pb2.CalcRequest(a=10, b=32))
    return 0 if r.result == 42 else 1


def main() -> int:
    args = parse_args()
    address = f"{args.host}:{int(args.port)}"
    with grpc.insecure_channel(address) as channel:
        stub = calculator_pb2_grpc.CalculatorStub(channel)

        if args.check:
            return run_check(stub)

        if args.demo:
            run_demo(stub)
            return 0

        print("Nothing to do. Use --demo or --check.")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
