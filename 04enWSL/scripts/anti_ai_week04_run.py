#!/usr/bin/env python3
"""
Week 4 Anti-AI Traffic Runner
=============================

This helper generates the required protocol traffic for the Week 4 anti-AI challenge.

It does not capture packets for you. Start Wireshark or tcpdump first then run this script.

Usage:
  python3 scripts/anti_ai_week04_run.py --challenge artifacts/anti_ai/week04_challenge.yaml

Recommended capture options:
  - TEXT (TCP 5400):  port 5400
  - BINARY (TCP 5401): port 5401
  - UDP sensor (UDP 5402): port 5402
"""

from __future__ import annotations

import argparse
import socket
import sys
from pathlib import Path
from typing import Tuple

import yaml

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.proto_common import TYPE_PUT_REQ, encode_kv, pack_bin_message, pack_udp_sensor
from src.utils.io_utils import recv_exact, recv_until


def _recv_text_framed(conn: socket.socket) -> str:
    raw = recv_until(conn, b" ", max_bytes=16)
    len_str = raw[:-1].decode("ascii", errors="strict").strip()
    if not len_str.isdigit():
        raise ValueError(f"Invalid length prefix: {len_str!r}")
    payload_len = int(len_str)
    payload_bytes = recv_exact(conn, payload_len)
    return payload_bytes.decode("utf-8", errors="replace")


def _send_text_framed(conn: socket.socket, payload: str) -> None:
    payload_bytes = payload.encode("utf-8")
    header = f"{len(payload_bytes)} ".encode("ascii")
    conn.sendall(header + payload_bytes)


def run_text(host: str, port: int, token: str, timeout_s: float = 5.0) -> None:
    cmd1 = f"SET anti_ai {token}"
    cmd2 = "GET anti_ai"
    cmd3 = "QUIT"

    with socket.create_connection((host, port), timeout=timeout_s) as conn:
        _send_text_framed(conn, cmd1)
        _ = _recv_text_framed(conn)
        _send_text_framed(conn, cmd2)
        _ = _recv_text_framed(conn)
        _send_text_framed(conn, cmd3)
        _ = _recv_text_framed(conn)


def run_binary(host: str, port: int, token: str, timeout_s: float = 5.0) -> None:
    payload = encode_kv("anti_ai", token)
    msg = pack_bin_message(TYPE_PUT_REQ, payload, seq=1)
    with socket.create_connection((host, port), timeout=timeout_s) as conn:
        conn.sendall(msg)
        # Read at least a header worth of response (server may close later)
        _ = conn.recv(4096)


def run_udp(host: str, port: int, sensor_id: int, location_tag: str) -> None:
    datagram = pack_udp_sensor(sensor_id=sensor_id, temp_c=21.5, location=location_tag)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(datagram, (host, port))


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Week 4 anti-AI protocol traffic")
    parser.add_argument("--challenge", required=True, help="Challenge YAML path")
    parser.add_argument("--dry-run", action="store_true", help="Do not send network traffic")
    parser.add_argument("--timeout", type=float, default=5.0, help="TCP timeout in seconds (default: 5)")
    args = parser.parse_args()

    ch_path = (PROJECT_ROOT / args.challenge).resolve()
    ch = yaml.safe_load(ch_path.read_text(encoding="utf-8"))

    host = str(ch.get("host", "localhost"))
    text_port = int(ch.get("text_port", 5400))
    bin_port = int(ch.get("binary_port", 5401))
    udp_port = int(ch.get("udp_port", 5402))

    text_token = str(ch["text_token"])
    bin_token = str(ch["binary_token"])
    udp_loc = str(ch["udp_location_tag"])
    udp_sensor_id = int(ch["udp_sensor_id"])

    if args.dry_run:
        print("Dry run")
        print(f"TEXT:  {host}:{text_port} token={text_token}")
        print(f"BINARY:{host}:{bin_port} token={bin_token}")
        print(f"UDP:   {host}:{udp_port} sensor_id={udp_sensor_id} location={udp_loc}")
        return 0

    run_text(host, text_port, text_token, timeout_s=args.timeout)
    run_binary(host, bin_port, bin_token, timeout_s=args.timeout)
    run_udp(host, udp_port, udp_sensor_id, udp_loc)

    print("Generated Week 4 anti-AI traffic. Capture should now contain tokens.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
