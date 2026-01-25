#!/usr/bin/env python3
"""Packet Capture Helper — Week 14.

NETWORKING class — ASE, CSIE | Computer Networks Laboratory
by ing. dr. Antonio Clim

Automates packet capture for laboratory exercises.

Usage:
    python scripts/capture_traffic.py --duration 30 --output pcap/demo.pcap
    python scripts/capture_traffic.py --interface eth0 --filter "port 8080"
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional

PROJECT_ROOT = Path(__file__).parent.parent
PCAP_DIR = PROJECT_ROOT / "pcap"


def log(level: str, message: str) -> None:
    """Print timestamped log message."""
    ts = datetime.now().strftime("%H:%M:%S")
    colours = {"INFO": "\033[94m", "WARN": "\033[93m", "ERROR": "\033[91m", "OK": "\033[92m"}
    colour = colours.get(level, "\033[0m")
    print(f"[{ts}] {colour}[{level}]\033[0m {message}")


def list_interfaces() -> List[str]:
    """List available network interfaces."""
    interfaces = []
    try:
        result = subprocess.run(["ip", "-o", "link", "show"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            for line in result.stdout.strip().split("\n"):
                parts = line.split(":")
                if len(parts) >= 2:
                    iface = parts[1].strip().split("@")[0]
                    if iface != "lo":
                        interfaces.append(iface)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return interfaces


def detect_docker_interface() -> Optional[str]:
    """Detect the Docker bridge interface."""
    try:
        result = subprocess.run(["ip", "-o", "link", "show"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            for line in result.stdout.strip().split("\n"):
                if "docker" in line.lower() or "br-" in line:
                    parts = line.split(":")
                    if len(parts) >= 2:
                        return parts[1].strip().split("@")[0]
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def start_capture(interface: str, output_file: Path, duration: int, filter_expr: Optional[str] = None) -> bool:
    """Start packet capture with tcpdump."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    cmd = ["sudo", "tcpdump", "-i", interface, "-w", str(output_file), "-c", "10000"]
    if filter_expr:
        cmd.extend(filter_expr.split())

    log("INFO", f"Starting capture on {interface}")
    log("INFO", f"Output: {output_file}")
    log("INFO", f"Duration: {duration}s")

    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        log("INFO", "Capturing... (press Ctrl+C to stop early)")
        try:
            process.wait(timeout=duration)
        except subprocess.TimeoutExpired:
            process.terminate()
            process.wait(timeout=5)

        log("OK", f"Capture saved to {output_file}")
        if output_file.exists():
            size_kb = output_file.stat().st_size / 1024
            log("INFO", f"File size: {size_kb:.1f} KB")
        return True
    except KeyboardInterrupt:
        log("WARN", "Capture interrupted by user")
        if process:
            process.terminate()
        return True
    except Exception as e:
        log("ERROR", f"Capture failed: {e}")
        return False


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Capture network traffic for analysis",
        epilog="NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim",
    )
    parser.add_argument("--interface", "-i", help="Network interface")
    parser.add_argument("--output", "-o", default="pcap/capture.pcap")
    parser.add_argument("--duration", "-d", type=int, default=30)
    parser.add_argument("--filter", "-f", help="BPF filter expression")
    parser.add_argument("--list-interfaces", action="store_true")
    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("  Packet Capture Helper — Week 14")
    print("  NETWORKING class — ASE, CSIE")
    print("=" * 60 + "\n")

    if args.list_interfaces:
        for iface in list_interfaces():
            docker_tag = " (Docker)" if "docker" in iface or "br-" in iface else ""
            print(f"    - {iface}{docker_tag}")
        return 0

    interface = args.interface or detect_docker_interface() or (list_interfaces() or ["eth0"])[0]
    output_file = Path(args.output) if Path(args.output).is_absolute() else PROJECT_ROOT / args.output

    success = start_capture(interface, output_file, args.duration, args.filter)
    if success:
        print(f"\n  ✓ Capture complete\n  Open in Wireshark: wireshark {output_file}\n")
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
