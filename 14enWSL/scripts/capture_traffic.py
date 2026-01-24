#!/usr/bin/env python3
"""
capture_traffic.py - Packet Capture Helper
Week 14 - Integrated Recap
NETWORKING class - ASE, Informatics | by Revolvix

Automates packet capture for laboratory exercises.

Usage:
    python scripts/capture_traffic.py --duration 30 --output pcap/demo.pcap
    python scripts/capture_traffic.py --interface "Ethernet" --duration 60 --output pcap/capture.pcap
    python scripts/capture_traffic.py --filter "port 8080" --duration 30 --output pcap/http.pcap
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import subprocess
import sys
import time
import argparse
import signal
import os
from pathlib import Path
from datetime import datetime


PROJECT_ROOT = Path(__file__).parent.parent
PCAP_DIR = PROJECT_ROOT / "pcap"


# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY_UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════
class Colours:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def log(level: str, message: str) -> None:
    """Print timestamped log message."""
    ts = datetime.now().strftime("%H:%M:%S")
    colours = {
        "INFO": Colours.BLUE,
        "OK": Colours.GREEN,
        "WARN": Colours.YELLOW,
        "ERROR": Colours.RED,
    }
    colour = colours.get(level, Colours.RESET)
    print(f"[{ts}] {colour}[{level}]{Colours.RESET} {message}")


# ═══════════════════════════════════════════════════════════════════════════════
# TOOL_DETECTION
# ═══════════════════════════════════════════════════════════════════════════════
def find_tshark() -> str | None:
    """Find tshark executable."""
    import shutil

    # Check if tshark is in PATH
    tshark = shutil.which("tshark")
    if tshark:
        return tshark

    # Common Windows paths
    windows_paths = [
        r"C:\Program Files\Wireshark\tshark.exe",
        r"C:\Program Files (x86)\Wireshark\tshark.exe",
    ]

    for path in windows_paths:
        if Path(path).exists():
            return path

    return None


def find_tcpdump() -> str | None:
    """Find tcpdump executable."""
    import shutil
    return shutil.which("tcpdump")


# ═══════════════════════════════════════════════════════════════════════════════
# INTERFACE_LISTING
# ═══════════════════════════════════════════════════════════════════════════════
def list_interfaces() -> list:
    """List available capture interfaces."""
    tshark = find_tshark()
    if not tshark:
        return []

    try:
        result = subprocess.run(
            [tshark, "-D"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            interfaces = []
            for line in result.stdout.strip().split("\n"):
                if line.strip():
                    interfaces.append(line.strip())
            return interfaces
    except Exception:
        pass

    return []


# ═══════════════════════════════════════════════════════════════════════════════
# TSHARK_CAPTURE
# ═══════════════════════════════════════════════════════════════════════════════
def capture_with_tshark(
    interface: str,
    output: Path,
    duration: int,
    filter_expr: str | None = None
) -> bool:
    """Capture using tshark."""
    tshark = find_tshark()
    if not tshark:
        log("ERROR", "tshark not found. Install Wireshark with command-line tools.")
        return False

    cmd = [
        tshark,
        "-i", interface,
        "-w", str(output),
        "-a", f"duration:{duration}",
    ]

    if filter_expr:
        cmd.extend(["-f", filter_expr])

    log("INFO", f"Starting capture: {' '.join(cmd)}")
    log("INFO", f"Duration: {duration} seconds")
    log("INFO", f"Output: {output}")

    try:
        # Run capture
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Wait with progress indication
        start_time = time.time()
        while process.poll() is None:
            elapsed = int(time.time() - start_time)
            remaining = duration - elapsed
            if remaining > 0:
                print(f"\r  Capturing... {elapsed}/{duration}s ", end="", flush=True)
            time.sleep(1)

        print()

        # Check result
        _, stderr = process.communicate(timeout=5)

        if process.returncode == 0:
            if output.exists():
                size = output.stat().st_size
                log("OK", f"Capture complete: {size} bytes")
                return True
            else:
                log("ERROR", "Capture file not created")
                return False
        else:
            log("ERROR", f"Capture failed: {stderr.decode()}")
            return False

    except KeyboardInterrupt:
        log("WARN", "Capture interrupted by user")
        process.terminate()
        return False
    except Exception as e:
        log("ERROR", f"Capture error: {e}")
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# CONTAINER_CAPTURE
# ═══════════════════════════════════════════════════════════════════════════════
def capture_in_container(
    output: Path,
    duration: int,
    container: str = "week14_client",
    interface: str = "eth0",
    filter_expr: str | None = None
) -> bool:
    """Capture inside a Docker container."""
    # Path inside container
    container_path = f"/app/pcap/{output.name}"

    cmd = [
        "docker", "exec", container,
        "timeout", str(duration),
        "tcpdump",
        "-i", interface,
        "-w", container_path,
    ]

    if filter_expr:
        cmd.append(filter_expr)

    log("INFO", f"Starting capture in container {container}")
    log("INFO", f"Interface: {interface}")
    log("INFO", f"Duration: {duration} seconds")

    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Wait with progress
        start_time = time.time()
        while process.poll() is None:
            elapsed = int(time.time() - start_time)
            remaining = duration - elapsed
            if remaining > 0:
                print(f"\r  Capturing... {elapsed}/{duration}s ", end="", flush=True)
            time.sleep(1)

        print()

        _, stderr = process.communicate(timeout=5)

        # Check if file was created
        if output.exists():
            size = output.stat().st_size
            log("OK", f"Capture complete: {size} bytes")
            return True
        else:
            log("WARN", "Capture file may not have been created")
            return False

    except KeyboardInterrupt:
        log("WARN", "Capture interrupted")
        process.terminate()
        return False
    except Exception as e:
        log("ERROR", f"Capture error: {e}")
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# PARSE_ARGUMENTS
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Capture network traffic for Week 14 laboratory"
    )
    parser.add_argument(
        "--interface", "-i",
        default="any",
        help="Capture interface (default: any)"
    )
    parser.add_argument(
        "--output", "-o",
        default="pcap/week14_capture.pcap",
        help="Output file path"
    )
    parser.add_argument(
        "--duration", "-d",
        type=int,
        default=30,
        help="Capture duration in seconds (default: 30)"
    )
    parser.add_argument(
        "--filter", "-f",
        help="Capture filter expression (e.g., 'port 8080')"
    )
    parser.add_argument(
        "--container",
        action="store_true",
        help="Capture inside Docker container instead of host"
    )
    parser.add_argument(
        "--list-interfaces",
        action="store_true",
        help="List available capture interfaces"
    )
    return parser.parse_args()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point."""
    args = parse_args()

    # Ensure pcap directory exists
    PCAP_DIR.mkdir(parents=True, exist_ok=True)

    print()
    print("=" * 60)
    print(f"  {Colours.BOLD}Packet Capture - Week 14{Colours.RESET}")
    print("=" * 60)
    print()

    if args.list_interfaces:
        log("INFO", "Available interfaces:")
        interfaces = list_interfaces()
        if interfaces:
            for iface in interfaces:
                print(f"    {iface}")
        else:
            log("WARN", "Could not list interfaces (tshark may not be installed)")
        return 0

    output_path = PROJECT_ROOT / args.output

    if args.container:
        success = capture_in_container(
            output=output_path,
            duration=args.duration,
            filter_expr=args.filter
        )
    else:
        success = capture_with_tshark(
            interface=args.interface,
            output=output_path,
            duration=args.duration,
            filter_expr=args.filter
        )

    if success:
        print()
        print("=" * 60)
        log("OK", "Capture complete")
        print("=" * 60)
        print()
        print("To analyse with Wireshark:")
        print(f'  wireshark "{output_path}"')
        print()
        print("To analyse with tshark:")
        print(f'  tshark -r "{output_path}" -q -z conv,tcp')
        print(f'  tshark -r "{output_path}" -Y http.request')
        print()
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
