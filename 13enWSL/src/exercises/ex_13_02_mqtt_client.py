#!/usr/bin/env python3
"""
Exercise 2: MQTT Client (Plaintext and TLS)
==========================================
Week 13 - IoT and Security in Computer Networks
ASE Bucharest, CSIE | by ing. dr. Antonio Clim

LEARNING OBJECTIVES (Anderson-Bloom Taxonomy):
1. UNDERSTAND the MQTT publish/subscribe model
2. APPLY QoS levels appropriately for different use cases
3. COMPARE plaintext vs TLS-encrypted MQTT traffic
4. ANALYSE Wireshark captures to identify protocol differences
5. CONFIGURE TLS client authentication with CA certificates

PAIR PROGRAMMING NOTES:
- Driver: Implement client configuration, handle callbacks
- Navigator: Monitor Wireshark capture, verify message delivery
- Swap after: Completing plaintext publish/subscribe cycle

USAGE EXAMPLES:
    # Plaintext publish:
    python3 ex_13_02_mqtt_client.py --broker 127.0.0.1 --port 1883 \\
        --mode publish --topic iot/sensors/temperature \\
        --message '{"sensor":"temp","value":24.3}' --count 3

    # TLS publish (server authentication):
    python3 ex_13_02_mqtt_client.py --broker 127.0.0.1 --port 8883 \\
        --mode publish --topic iot/sensors/temperature \\
        --message '{"sensor":"temp","value":24.3}' --count 3 \\
        --tls --cafile docker/configs/certs/ca.crt

    # Subscribe with timeout:
    python3 ex_13_02_mqtt_client.py --broker 127.0.0.1 --port 1883 \\
        --mode subscribe --topic iot/sensors/# --timeout 20
"""

from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORT_DEPENDENCIES
# ═══════════════════════════════════════════════════════════════════════════════
import argparse
import json
import os
import sys
import time
from dataclasses import dataclass
from typing import Optional

import paho.mqtt.client as mqtt


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION_DATA_STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class MqttConfig:
    """Configuration for MQTT client operations."""
    broker: str
    port: int
    mode: str  # "publish" or "subscribe"
    topic: str
    message: str
    count: int
    qos: int
    username: Optional[str]
    password: Optional[str]
    tls: bool
    cafile: Optional[str]
    insecure: bool
    timeout: int


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def _format_message_for_print(msg: str) -> str:
    """Format message for display, prettifying JSON if valid."""
    msg = msg.strip()
    if not msg:
        return msg
    try:
        obj = json.loads(msg)
        return json.dumps(obj, indent=2, sort_keys=True)
    except Exception:
        return msg


def _ensure_cafile(cafile: Optional[str]) -> str:
    """
    Verify CA certificate file exists.
    
    💭 PREDICTION: What happens if you specify --tls but forget --cafile?
       (Answer: This function raises ValueError)
    
    Args:
        cafile: Path to CA certificate file
    
    Returns:
        Validated path to CA file
    
    Raises:
        ValueError: If cafile is None
        FileNotFoundError: If file doesn't exist
    """
    if not cafile:
        raise ValueError("TLS is enabled but --cafile was not provided.")
    if not os.path.exists(cafile):
        raise FileNotFoundError(f"CA file not found: {cafile}")
    return cafile


# ═══════════════════════════════════════════════════════════════════════════════
# CLIENT_CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

def build_client(cfg: MqttConfig) -> mqtt.Client:
    """
    Build and configure MQTT client based on provided configuration.
    
    💭 PREDICTION: If both username and TLS are configured, which is checked first?
       (Answer: Both are configured, but TLS wraps the connection)
    
    Args:
        cfg: Client configuration
    
    Returns:
        Configured mqtt.Client instance
    """
    client = mqtt.Client(protocol=mqtt.MQTTv311)

    # ─────────────────────────────────────────────────────────────────────────
    # CONFIGURE_AUTHENTICATION (if credentials provided)
    # ─────────────────────────────────────────────────────────────────────────
    if cfg.username is not None:
        client.username_pw_set(cfg.username, cfg.password)

    # ─────────────────────────────────────────────────────────────────────────
    # CONFIGURE_TLS (if enabled)
    # ─────────────────────────────────────────────────────────────────────────
    if cfg.tls:
        cafile = _ensure_cafile(cfg.cafile)
        client.tls_set(ca_certs=cafile)
        client.tls_insecure_set(cfg.insecure)

    return client


# ═══════════════════════════════════════════════════════════════════════════════
# PUBLISH_MODE
# ═══════════════════════════════════════════════════════════════════════════════

def run_publish(cfg: MqttConfig) -> int:
    """
    Execute MQTT publish operation.
    
    💭 PREDICTION: With QoS 1, how many packets are exchanged per message?
       (Answer: 2 - PUBLISH from client, PUBACK from broker)
    
    Args:
        cfg: Client configuration
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    client = build_client(cfg)

    connected = False
    connection_rc: Optional[int] = None

    # ─────────────────────────────────────────────────────────────────────────
    # DEFINE_CALLBACKS
    # ─────────────────────────────────────────────────────────────────────────
    def on_connect(_client, _userdata, _flags, rc):
        nonlocal connected, connection_rc
        connection_rc = rc
        connected = True

    def on_publish(_client, _userdata, mid):
        print(f"[PUBLISH] ack mid={mid}")

    client.on_connect = on_connect
    client.on_publish = on_publish

    # ─────────────────────────────────────────────────────────────────────────
    # DISPLAY_CONFIGURATION
    # ─────────────────────────────────────────────────────────────────────────
    print("=" * 72)
    print("Week 13 - MQTT Publish")
    print("=" * 72)
    print(f"Broker: {cfg.broker}:{cfg.port}")
    print(f"TLS: {cfg.tls}")
    if cfg.tls:
        print(f"CA file: {cfg.cafile}")
        print(f"TLS insecure: {cfg.insecure}")
    if cfg.username:
        print(f"Auth: username={cfg.username!r}")
    else:
        print("Auth: none (anonymous)")
    print(f"Topic: {cfg.topic}")
    print(f"QoS: {cfg.qos}")
    print(f"Count: {cfg.count}")
    print("Message:")
    print(_format_message_for_print(cfg.message))
    print()

    # ─────────────────────────────────────────────────────────────────────────
    # CONNECT_TO_BROKER
    # ─────────────────────────────────────────────────────────────────────────
    try:
        client.connect(cfg.broker, cfg.port, keepalive=30)
    except Exception as exc:
        print(f"[ERROR] Connect failed: {exc}")
        return 1

    client.loop_start()

    # Wait for connection callback
    deadline = time.time() + 5
    while not connected and time.time() < deadline:
        time.sleep(0.05)

    if not connected:
        print("[ERROR] Connection timed out (no CONNACK).")
        client.loop_stop()
        return 1

    if connection_rc != 0:
        print(f"[ERROR] Connection rejected, rc={connection_rc}")
        client.loop_stop()
        return 1

    # ─────────────────────────────────────────────────────────────────────────
    # PUBLISH_MESSAGES
    # ─────────────────────────────────────────────────────────────────────────
    for i in range(cfg.count):
        payload = cfg.message
        info = client.publish(cfg.topic, payload=payload, qos=cfg.qos, retain=False)
        print(f"[PUBLISH] sent {i+1}/{cfg.count} mid={info.mid}")
        time.sleep(0.5)

    # Allow time for final acknowledgements
    time.sleep(1.0)
    
    # ─────────────────────────────────────────────────────────────────────────
    # CLEANUP_CONNECTION
    # ─────────────────────────────────────────────────────────────────────────
    client.disconnect()
    client.loop_stop()
    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# SUBSCRIBE_MODE
# ═══════════════════════════════════════════════════════════════════════════════

def run_subscribe(cfg: MqttConfig) -> int:
    """
    Execute MQTT subscribe operation.
    
    💭 PREDICTION: If you subscribe to "sensors/#", will you receive messages
       published to "sensors/temp/room1"? (Answer: Yes - # matches all levels)
    
    Args:
        cfg: Client configuration
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    client = build_client(cfg)

    received = 0
    connected = False
    connection_rc: Optional[int] = None

    # ─────────────────────────────────────────────────────────────────────────
    # DEFINE_CALLBACKS
    # ─────────────────────────────────────────────────────────────────────────
    def on_connect(_client, _userdata, _flags, rc):
        nonlocal connected, connection_rc
        connection_rc = rc
        connected = True
        if rc == 0:
            _client.subscribe(cfg.topic, qos=cfg.qos)

    def on_message(_client, _userdata, msg):
        nonlocal received
        received += 1
        payload = msg.payload.decode(errors="replace")
        print(f"[MESSAGE] topic={msg.topic} qos={msg.qos} retained={msg.retain}")
        print(_format_message_for_print(payload))
        print("-" * 40)

    def on_subscribe(_client, _userdata, mid, granted_qos):
        print(f"[SUBSCRIBED] mid={mid} granted_qos={granted_qos}")

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe

    # ─────────────────────────────────────────────────────────────────────────
    # DISPLAY_CONFIGURATION
    # ─────────────────────────────────────────────────────────────────────────
    print("=" * 72)
    print("Week 13 - MQTT Subscribe")
    print("=" * 72)
    print(f"Broker: {cfg.broker}:{cfg.port}")
    print(f"TLS: {cfg.tls}")
    if cfg.tls:
        print(f"CA file: {cfg.cafile}")
        print(f"TLS insecure: {cfg.insecure}")
    if cfg.username:
        print(f"Auth: username={cfg.username!r}")
    else:
        print("Auth: none (anonymous)")
    print(f"Topic filter: {cfg.topic}")
    print(f"QoS: {cfg.qos}")
    print(f"Timeout: {cfg.timeout}s")
    print()

    # ─────────────────────────────────────────────────────────────────────────
    # CONNECT_TO_BROKER
    # ─────────────────────────────────────────────────────────────────────────
    try:
        client.connect(cfg.broker, cfg.port, keepalive=30)
    except Exception as exc:
        print(f"[ERROR] Connect failed: {exc}")
        return 1

    client.loop_start()

    # Wait for connection
    deadline = time.time() + 5
    while not connected and time.time() < deadline:
        time.sleep(0.05)

    if not connected:
        print("[ERROR] Connection timed out (no CONNACK).")
        client.loop_stop()
        return 1

    if connection_rc != 0:
        print(f"[ERROR] Connection rejected, rc={connection_rc}")
        client.loop_stop()
        return 1

    # ─────────────────────────────────────────────────────────────────────────
    # WAIT_FOR_MESSAGES
    # ─────────────────────────────────────────────────────────────────────────
    print(f"[INFO] Waiting for messages ({cfg.timeout}s timeout)...")
    end_time = time.time() + cfg.timeout
    while time.time() < end_time:
        time.sleep(0.1)

    # ─────────────────────────────────────────────────────────────────────────
    # CLEANUP_CONNECTION
    # ─────────────────────────────────────────────────────────────────────────
    client.disconnect()
    client.loop_stop()

    if received == 0:
        print("[INFO] No messages received within the timeout window.")
    else:
        print(f"[INFO] Received {received} message(s).")
    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# ARGUMENT_PARSING
# ═══════════════════════════════════════════════════════════════════════════════

def parse_args() -> MqttConfig:
    """Parse command-line arguments into MqttConfig."""
    parser = argparse.ArgumentParser(
        description="Week 13 - MQTT client (plaintext and TLS)"
    )
    parser.add_argument("--broker", default="127.0.0.1",
                        help="MQTT broker host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=1883,
                        help="MQTT broker port (default: 1883)")
    parser.add_argument("--mode", choices=["publish", "subscribe"], required=True,
                        help="Client mode")
    parser.add_argument("--topic", required=True,
                        help="Topic (publish) or topic filter (subscribe)")
    parser.add_argument("--message", default="",
                        help="Payload for publish mode")
    parser.add_argument("--count", type=int, default=1,
                        help="Number of publish messages (default: 1)")
    parser.add_argument("--qos", type=int, default=0, choices=[0, 1, 2],
                        help="QoS level (default: 0)")
    parser.add_argument("--username", default=None,
                        help="Username (optional)")
    parser.add_argument("--password", default=None,
                        help="Password (optional)")
    parser.add_argument("--tls", action="store_true",
                        help="Enable TLS")
    parser.add_argument("--cafile", default=None,
                        help="CA certificate file for TLS")
    parser.add_argument("--insecure", action="store_true",
                        help="Disable TLS certificate verification")
    parser.add_argument("--timeout", type=int, default=20,
                        help="Subscribe timeout in seconds (default: 20)")
    args = parser.parse_args()

    if args.mode == "publish" and not args.message:
        raise SystemExit("Publish mode requires --message.")

    return MqttConfig(
        broker=args.broker,
        port=args.port,
        mode=args.mode,
        topic=args.topic,
        message=args.message,
        count=args.count,
        qos=args.qos,
        username=args.username,
        password=args.password,
        tls=args.tls,
        cafile=args.cafile,
        insecure=args.insecure,
        timeout=args.timeout,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Main entry point."""
    cfg = parse_args()
    if cfg.mode == "publish":
        return run_publish(cfg)
    return run_subscribe(cfg)


if __name__ == "__main__":
    sys.exit(main())
