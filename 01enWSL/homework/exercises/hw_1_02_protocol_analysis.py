#!/usr/bin/env python3
"""Homework 1.02: Protocol Analysis Helper

Computer Networks - Week 1 (WSL Environment)
ASE Bucharest | by ing. dr. Antonio Clim

This starter script helps you capture and analyse TCP and UDP traffic.

Anti-AI note
If you provide a Week 1 challenge file (generated with
`python -m anti_ai.challenge_generator`), the script will embed a unique
payload token into the generated traffic. The validator can then confirm the
token exists inside your PCAP file, which is difficult to fabricate without
running the traffic generation for real.

Objectives
- Demonstrate TCP and UDP traffic generation
- Apply packet capture techniques using tcpdump
- Analyse protocol behaviour using tshark
- Compare TCP and UDP communication patterns

Prerequisites
- tcpdump and tshark installed
- Root or sudo access for packet capture
- Understanding of TCP and UDP differences

Level: Intermediate
Estimated time: 45-60 minutes

Usage
    python hw_1_02_protocol_analysis.py --mode tcp --output tcp_analysis.pcap
    python hw_1_02_protocol_analysis.py --mode udp --output udp_analysis.pcap
    python hw_1_02_protocol_analysis.py --analyse tcp_analysis.pcap

With a challenge file
    python hw_1_02_protocol_analysis.py --challenge artifacts/anti_ai/challenge_ABC123.yaml --mode tcp --output tcp_analysis.pcap
"""

from __future__ import annotations

import argparse
import json
import socket
import subprocess
import threading
import time
from pathlib import Path
from typing import Optional

try:
    import yaml
except ImportError:
    yaml = None


def load_challenge(path: Path) -> dict:
    """Load a Week 1 challenge file (YAML or JSON)."""
    if not path.exists():
        raise FileNotFoundError(f"Challenge file not found: {path}")

    if path.suffix.lower() in {".yaml", ".yml"}:
        if yaml is None:
            raise RuntimeError("PyYAML is required for YAML challenge files")
        return yaml.safe_load(path.read_text(encoding="utf-8"))

    if path.suffix.lower() == ".json":
        return json.loads(path.read_text(encoding="utf-8"))

    raise ValueError("Unsupported challenge type. Use .yaml, .yml or .json")


def prompt_prediction(mode: str, messages: int) -> None:
    """Ask student to predict traffic patterns before capture."""
    print("\n" + "=" * 60)
    print("💭 PREDICTION TIME")
    print("=" * 60)
    print(f"You are about to generate {messages} {mode.upper()} messages.")
    print()
    if mode == "tcp":
        print("Before capture, predict:")
        print("  1. How many packets for the handshake? (hint: 3-way)")
        print("  2. How many data packets for 5 messages and responses?")
        print("  3. How many packets to close the connection?")
        print("  4. What TCP flags will you see? (SYN, ACK, FIN, PSH)")
    else:
        print("Before capture, predict:")
        print("  1. Will there be a handshake? (compare to TCP)")
        print("  2. How many packets for 5 messages and responses?")
        print("  3. What happens if a packet is lost?")
    print("=" * 60)
    input("Press Enter to continue and verify your predictions...")
    print()


def _build_message(base: str, payload_token: Optional[str], i: int) -> bytes:
    token_part = f"|{payload_token}" if payload_token else ""
    return f"{base} {i}{token_part}\n".encode("utf-8")


def create_tcp_traffic(host: str, port: int, messages: int = 5, payload_token: Optional[str] = None) -> None:
    """Generate TCP traffic by running a simple echo server and client."""
    server_ready = threading.Event()

    def server() -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            s.listen(1)
            server_ready.set()

            conn, _ = s.accept()
            with conn:
                for _ in range(messages):
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(b"ACK:" + data)

    server_thread = threading.Thread(target=server, daemon=True)
    server_thread.start()
    server_ready.wait(timeout=5)

    time.sleep(0.5)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        for i in range(1, messages + 1):
            msg = _build_message("Message", payload_token, i)
            s.sendall(msg)
            response = s.recv(1024)
            print(f"Sent: {msg.decode().strip()} | Received: {response.decode().strip()}")
            time.sleep(0.2)

    server_thread.join(timeout=2)


def create_udp_traffic(host: str, port: int, messages: int = 5, payload_token: Optional[str] = None) -> None:
    """Generate UDP traffic by running a simple echo server and client."""
    server_ready = threading.Event()

    def server() -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((host, port))
            s.settimeout(5)
            server_ready.set()
            try:
                for _ in range(messages):
                    data, addr = s.recvfrom(1024)
                    s.sendto(b"ACK:" + data, addr)
            except socket.timeout:
                pass

    server_thread = threading.Thread(target=server, daemon=True)
    server_thread.start()
    server_ready.wait(timeout=5)

    time.sleep(0.5)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(2)
        for i in range(1, messages + 1):
            msg = _build_message("Message", payload_token, i)
            s.sendto(msg, (host, port))
            try:
                response, _ = s.recvfrom(1024)
                print(f"Sent: {msg.decode().strip()} | Received: {response.decode().strip()}")
            except socket.timeout:
                print(f"Sent: {msg.decode().strip()} | No response (timeout)")
            time.sleep(0.2)

    server_thread.join(timeout=2)


def start_capture(interface: str, port: int, output: Path) -> subprocess.Popen:
    """Start tcpdump capture in the background."""
    cmd = [
        "tcpdump",
        "-i",
        interface,
        "-w",
        str(output),
        f"port {port}",
        "-c",
        "200",
    ]

    print(f"Starting capture: {' '.join(cmd)}")
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def analyse_pcap(pcap_file: Path) -> None:
    """Analyse a PCAP file using tshark and display statistics."""
    if not pcap_file.exists():
        print(f"Error: File not found: {pcap_file}")
        return

    print(f"\n{'=' * 60}")
    print(f"Analysis of: {pcap_file}")
    print(f"{'=' * 60}\n")

    print("1. Packet Summary:")
    result = subprocess.run(["tshark", "-r", str(pcap_file), "-q", "-z", "io,stat,0"], capture_output=True, text=True)
    print(result.stdout)

    print("\n2. Protocol Hierarchy:")
    result = subprocess.run(["tshark", "-r", str(pcap_file), "-q", "-z", "io,phs"], capture_output=True, text=True)
    print(result.stdout)

    print("\n3. Conversations:")
    result = subprocess.run(["tshark", "-r", str(pcap_file), "-q", "-z", "conv,tcp"], capture_output=True, text=True)
    if result.stdout.strip():
        print(result.stdout)
    else:
        result = subprocess.run(["tshark", "-r", str(pcap_file), "-q", "-z", "conv,udp"], capture_output=True, text=True)
        print(result.stdout)

    print("\n4. First 10 Packets:")
    result = subprocess.run(["tshark", "-r", str(pcap_file), "-c", "10"], capture_output=True, text=True)
    print(result.stdout)

    print("\n5. TCP Flags (if applicable):")
    result = subprocess.run(
        [
            "tshark",
            "-r",
            str(pcap_file),
            "-Y",
            "tcp",
            "-T",
            "fields",
            "-e",
            "frame.number",
            "-e",
            "tcp.flags.str",
        ],
        capture_output=True,
        text=True,
    )
    if result.stdout.strip():
        print("Frame\tFlags")
        print("-" * 30)
        for line in result.stdout.strip().split("\n")[:15]:
            print(line)
    else:
        print("No TCP packets found")

    print(f"\n{'=' * 60}")
    print("Analysis complete. Use Wireshark for detailed inspection.")
    print(f"{'=' * 60}\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Protocol Analysis Helper for Homework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate and capture TCP traffic
  python hw_1_02_protocol_analysis.py --mode tcp --output tcp_analysis.pcap

  # Generate and capture UDP traffic
  python hw_1_02_protocol_analysis.py --mode udp --output udp_analysis.pcap

  # Analyse an existing capture
  python hw_1_02_protocol_analysis.py --analyse tcp_analysis.pcap

  # Use a Week 1 challenge and embed the payload token
  python hw_1_02_protocol_analysis.py --challenge artifacts/anti_ai/challenge_ABC123.yaml --mode tcp --output tcp_analysis.pcap
""",
    )

    parser.add_argument("--challenge", type=Path, default=None, help="Week 1 challenge file (.yaml/.json)")
    parser.add_argument("--mode", choices=["tcp", "udp"], help="Traffic mode to generate")
    parser.add_argument("--output", "-o", type=Path, help="Output PCAP file")
    parser.add_argument("--analyse", "-a", type=Path, help="Analyse existing PCAP file")
    parser.add_argument("--port", "-p", type=int, default=None, help="Port to use")
    parser.add_argument("--interface", "-i", default="lo", help="Interface to capture on (default: lo)")
    parser.add_argument("--no-predict", action="store_true", help="Skip the prediction prompt")
    parser.add_argument("--messages", type=int, default=5, help="Number of messages to exchange (default: 5)")

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.analyse:
        analyse_pcap(args.analyse)
        return 0

    if not args.mode or not args.output:
        print("Error: Specify --mode and --output or use --analyse")
        return 1

    payload_token: Optional[str] = None
    if args.challenge:
        challenge = load_challenge(args.challenge)
        payload_token = str(challenge.get("challenges", {}).get("pcap", {}).get("payload_token") or "")

    port = args.port
    if port is None:
        if args.challenge:
            port = int(challenge.get("challenges", {}).get("pcap", {}).get("recommended_port") or 9999)
        else:
            port = 9999

    print(f"\n{'=' * 60}")
    print(f"Protocol Analysis Helper - {args.mode.upper()} Mode")
    print(f"{'=' * 60}\n")

    if args.challenge and payload_token:
        print("Anti-AI payload token embedded in traffic")
        print(f"  Token: {payload_token}")
        print(f"  Port: {port}\n")

    if not args.no_predict:
        prompt_prediction(args.mode, args.messages)

    print(f"Starting capture on {args.interface}, port {port}...")
    print("(Run with sudo if permission denied)\n")

    try:
        capture = start_capture(args.interface, port, args.output)
        time.sleep(1)

        print(f"\nGenerating {args.mode.upper()} traffic...\n")

        if args.mode == "tcp":
            create_tcp_traffic("127.0.0.1", port, messages=args.messages, payload_token=payload_token)
        else:
            create_udp_traffic("127.0.0.1", port, messages=args.messages, payload_token=payload_token)

        time.sleep(2)
        capture.terminate()
        capture.wait(timeout=5)

        print(f"\n✅ Capture saved to: {args.output}")
        analyse_pcap(args.output)

    except PermissionError:
        print("\n❌ Error: Permission denied. Run with sudo:")
        print(f"  sudo python {__file__} --mode {args.mode} --output {args.output}")
        return 1
    except FileNotFoundError:
        print("\n❌ Error: tcpdump not found. Install it or use Wireshark for capture.")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
