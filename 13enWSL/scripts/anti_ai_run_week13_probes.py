#!/usr/bin/env python3
"""Run Week 13 probes required for the anti-AI evidence package.

The probe script is designed to generate network traffic that can be captured into a PCAP:
- Plain MQTT publish containing the payload token on port 1883
- Optional TLS connect attempt on port 8883 (handshake evidence only)

It supports a dry-run mode so it can be tested without a running broker.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import yaml

try:
    import paho.mqtt.client as mqtt  # type: ignore
    MQTT_AVAILABLE = True
except ImportError:
    mqtt = None  # type: ignore
    MQTT_AVAILABLE = False


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Run Week 13 anti-AI probes")
    p.add_argument("--challenge", required=True, help="Challenge YAML path")
    p.add_argument("--broker", default="127.0.0.1", help="Broker host")
    p.add_argument("--dry-run", action="store_true", help="Print actions without connecting")
    p.add_argument("--tls", action="store_true", help="Attempt a TLS connection on 8883")
    p.add_argument("--timeout", type=int, default=5, help="Connect timeout in seconds")
    return p


def _publish_plain(host: str, port: int, topic: str, payload: str, timeout: int) -> None:
    if not MQTT_AVAILABLE:
        raise RuntimeError("paho-mqtt is required. Install with: pip install paho-mqtt")

    done = {"published": False}

    def on_connect(client, userdata, flags, rc):  # pragma: no cover
        client.publish(topic, payload, qos=0)
        done["published"] = True
        client.disconnect()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(host, port, timeout)
    client.loop_start()
    t0 = time.time()
    while time.time() - t0 < timeout and not done["published"]:
        time.sleep(0.05)
    client.loop_stop()


def _attempt_tls(host: str, port: int, timeout: int) -> None:
    if not MQTT_AVAILABLE:
        raise RuntimeError("paho-mqtt is required. Install with: pip install paho-mqtt")

    client = mqtt.Client()
    # Intentionally insecure here because the goal is handshake traffic, not trust policy.
    client.tls_set()  # pragma: no cover
    client.tls_insecure_set(True)  # pragma: no cover
    client.connect(host, port, timeout)  # pragma: no cover
    client.disconnect()  # pragma: no cover


def main() -> int:
    args = build_arg_parser().parse_args()
    challenge = yaml.safe_load(Path(args.challenge).read_text(encoding="utf-8"))
    topic = str(challenge.get("mqtt_topic"))
    payload_token = str(challenge.get("payload_token"))
    report_token = str(challenge.get("report_token"))
    plain_port = int(challenge.get("mqtt_plain_port", 1883))
    tls_port = int(challenge.get("mqtt_tls_port", 8883))

    payload = json.dumps({"token": payload_token, "report_token": report_token, "ts": time.time()})

    if args.dry_run:
        print("[DRY RUN] Would publish to:")
        print(f"  broker={args.broker} port={plain_port} topic={topic}")
        print(f"  payload={payload}")
        if args.tls:
            print(f"[DRY RUN] Would attempt TLS connection to {args.broker}:{tls_port}")
        return 0

    _publish_plain(args.broker, plain_port, topic, payload, args.timeout)
    if args.tls:
        try:
            _attempt_tls(args.broker, tls_port, args.timeout)
        except Exception:
            # TLS evidence is best-effort
            pass
    print("[OK] Probes completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
