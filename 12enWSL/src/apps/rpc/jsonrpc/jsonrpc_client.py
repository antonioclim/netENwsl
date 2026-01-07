#!/usr/bin/env python3
"""JSON-RPC client demo for Week 12."""

from __future__ import annotations

import argparse
import json
import urllib.request
from typing import Any, Dict


def jsonrpc_call(url: str, method: str, params: Any, req_id: int = 1) -> Dict[str, Any]:
    payload = {"jsonrpc": "2.0", "id": req_id, "method": method, "params": params}
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url=url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=5) as resp:
        data = resp.read().decode("utf-8")
    return json.loads(data)


def jsonrpc_batch(url: str, batch: list[dict]) -> Any:
    body = json.dumps(batch).encode("utf-8")
    req = urllib.request.Request(url=url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=5) as resp:
        if resp.status == 204:
            return None
        data = resp.read().decode("utf-8")
    return json.loads(data)


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Week 12 JSON-RPC client")
    ap.add_argument("--host", default="127.0.0.1", help="Server host")
    ap.add_argument("--port", type=int, default=6200, help="Server port")
    ap.add_argument("--demo", action="store_true", help="Run the interactive demo")
    ap.add_argument("--check", action="store_true", help="Run a minimal self-check and exit")
    return ap.parse_args()


def run_demo(url: str) -> None:
    print("Week 12 JSON-RPC demo")
    print(f"Endpoint: {url}")
    print()

    calls = [
        ("add", [2, 3]),
        ("subtract", [10, 4]),
        ("multiply", [6, 7]),
        ("divide", [22, 7]),
        ("echo", ["Hello from JSON-RPC"]),
        ("sort_list", [[5, 3, 9, 1]]),
        ("get_server_info", []),
        ("get_stats", []),
    ]

    for i, (method, params) in enumerate(calls, start=1):
        resp = jsonrpc_call(url, method, params, req_id=i)
        if "result" in resp:
            print(f"{method}({params}) => {resp['result']}")
        else:
            print(f"{method}({params}) => ERROR: {resp.get('error')}")
    print()

    print("Batch request demo:")
    batch = [
        {"jsonrpc": "2.0", "id": 101, "method": "add", "params": [1, 2]},
        {"jsonrpc": "2.0", "id": 102, "method": "multiply", "params": [6, 7]},
        {"jsonrpc": "2.0", "id": 103, "method": "sort_list", "params": [[3, 1, 2]]},
    ]
    print(json.dumps(jsonrpc_batch(url, batch), indent=2))
    print()

    print("Intentional error demo:")
    resp = jsonrpc_call(url, "this_method_does_not_exist", [], req_id=999)
    print(json.dumps(resp, indent=2))
    print()


def run_check(url: str) -> int:
    resp = jsonrpc_call(url, "add", [10, 32], req_id=1)
    if resp.get("result") != 42:
        print(f"Check failed: expected 42, got {resp!r}")
        return 1
    return 0


def main() -> int:
    args = parse_args()
    url = f"http://{args.host}:{int(args.port)}"

    if args.check:
        return run_check(url)

    if args.demo:
        run_demo(url)
        return 0

    print("Nothing to do. Use --demo or --check.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
