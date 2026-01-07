#!/usr/bin/env python3
"""XML-RPC client demo for Week 12."""

from __future__ import annotations

import argparse
import xmlrpc.client


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Week 12 XML-RPC client")
    ap.add_argument("--host", default="127.0.0.1", help="Server host")
    ap.add_argument("--port", type=int, default=6201, help="Server port")
    ap.add_argument("--demo", action="store_true", help="Run the interactive demo")
    ap.add_argument("--check", action="store_true", help="Run a minimal self-check and exit")
    return ap.parse_args()


def run_demo(url: str) -> None:
    proxy = xmlrpc.client.ServerProxy(url, allow_none=True)
    print("Week 12 XML-RPC demo")
    print(f"Endpoint: {url}")
    print()

    print(f"add(2, 3) => {proxy.add(2, 3)}")
    print(f"subtract(10, 4) => {proxy.subtract(10, 4)}")
    print(f"multiply(6, 7) => {proxy.multiply(6, 7)}")
    print(f"divide(22, 7) => {proxy.divide(22, 7)}")
    print(f"echo('Hello, XML-RPC') => {proxy.echo('Hello, XML-RPC')}")
    print(f"sort_list([5, 3, 9, 1]) => {proxy.sort_list([5, 3, 9, 1])}")
    print(f"get_server_info() => {proxy.get_server_info()}")
    print(f"get_stats() => {proxy.get_stats()}")
    print()

    print("Intentional error demo:")
    try:
        proxy.divide(1, 0)
    except Exception as exc:
        print(f"divide(1, 0) raised: {exc}")


def run_check(url: str) -> int:
    proxy = xmlrpc.client.ServerProxy(url, allow_none=True)
    r = proxy.add(10, 32)
    if r != 42:
        print(f"Check failed: expected 42, got {r!r}")
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
