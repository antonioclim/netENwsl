#!/usr/bin/env python3
"""Week 6 demonstration runner.

This helper starts the relevant Mininet topologies for Week 6.
It is a convenience wrapper around the exercise scripts in src/exercises.

Examples
    python scripts/run_demo.py nat
    python scripts/run_demo.py sdn --install-flows
    python scripts/run_demo.py nat-test
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


PROJECT_ROOT = Path(__file__).parent.parent


DEMOS = {
    "nat": {
        "description": "NAT/PAT topology with MASQUERADE translation (interactive)",
        "script": "src/exercises/ex_6_01_nat_topology.py",
        "args": ["--cli"],
    },
    "nat-test": {
        "description": "NAT topology smoke test",
        "script": "src/exercises/ex_6_01_nat_topology.py",
        "args": ["--test"],
    },
    "sdn": {
        "description": "SDN topology with OpenFlow policies (interactive)",
        "script": "src/exercises/ex_6_02_sdn_topology.py",
        "args": ["--cli"],
    },
    "sdn-test": {
        "description": "SDN topology smoke test",
        "script": "src/exercises/ex_6_02_sdn_topology.py",
        "args": ["--test"],
    },
}


def check_mininet_available() -> bool:
    """Return True if Mininet appears to be installed."""
    try:
        p = subprocess.run(["mn", "--version"], capture_output=True, text=True, timeout=5)
        return p.returncode == 0
    except Exception:
        return False


def run_demo(demo_key: str, extra_args: Optional[List[str]] = None) -> int:
    if demo_key not in DEMOS:
        print(f"Unknown demo: {demo_key}")
        return 2

    if not check_mininet_available():
        print("Mininet does not appear to be installed or is not on PATH.")
        print("If you are using the Docker lab, run this inside the container.")
        return 3

    demo = DEMOS[demo_key]
    script_path = PROJECT_ROOT / demo["script"]
    if not script_path.exists():
        print(f"Demo script not found: {demo['script']}")
        return 4

    args = [sys.executable, str(script_path)] + list(demo.get("args", []))
    if demo_key.startswith("sdn") and extra_args:
        # Allow pass-through for SDN specific flags like --install-flows.
        args += extra_args

    print("=" * 70)
    print(f"DEMO: {demo_key}")
    print(demo["description"])
    print("=" * 70)
    print()

    try:
        return subprocess.call(args)
    except KeyboardInterrupt:
        return 130


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run a Week 6 demonstration")
    p.add_argument(
        "demo",
        choices=sorted(DEMOS.keys()),
        help="Which demo to run",
    )
    p.add_argument(
        "--install-flows",
        action="store_true",
        help="For SDN demos: install default flows",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    extra: List[str] = []
    if args.install_flows:
        extra.append("--install-flows")
    return run_demo(args.demo, extra_args=extra)


if __name__ == "__main__":
    raise SystemExit(main())
