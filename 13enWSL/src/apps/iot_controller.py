#!/usr/bin/env python3
"""
IoT Controller (Subscriber)
===========================
Week 13 - IoT and Security in Computer Networks
ASE Bucharest, CSIE | by ing. dr. Antonio Clim

LEARNING OBJECTIVES:
1. UNDERSTAND MQTT subscription patterns
2. APPLY topic wildcards (+ and #)
3. ANALYSE message flow from sensors to controller

Receives and processes messages from IoT sensors via MQTT.

USAGE:
    # Subscribe to all IoT topics
    python3 src/apps/iot_controller.py --broker localhost --topic "iot/#"

    # Subscribe to specific sensor
    python3 src/apps/iot_controller.py --topic "iot/sensors/temp"

    # With TLS
    python3 src/apps/iot_controller.py --broker localhost --port 8883 \\
        --tls --cafile docker/configs/certs/ca.crt

PAIR PROGRAMMING:
- Run this while partner runs iot_sensor.py
- Try different topic patterns to understand wildcard matching
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORT_DEPENDENCIES
# ═══════════════════════════════════════════════════════════════════════════════
import argparse
import json
from datetime import datetime

try:
    import paho.mqtt.client as mqtt  # type: ignore
    MQTT_AVAILABLE = True
except ImportError:  # pragma: no cover
    mqtt = None  # type: ignore
    MQTT_AVAILABLE = False


# ═══════════════════════════════════════════════════════════════════════════════
# MESSAGE_STATISTICS
# ═══════════════════════════════════════════════════════════════════════════════

class MessageStats:
    """Track message statistics for analysis."""
    
    def __init__(self):
        self.total_count = 0
        self.topics_seen = set()
        self.start_time = datetime.now()
    
    def record(self, topic: str) -> None:
        """Record a received message."""
        self.total_count += 1
        self.topics_seen.add(topic)
    
    def summary(self) -> str:
        """Return summary statistics."""
        duration = (datetime.now() - self.start_time).total_seconds()
        rate = self.total_count / duration if duration > 0 else 0
        return (f"Messages: {self.total_count} | "
                f"Topics: {len(self.topics_seen)} | "
                f"Rate: {rate:.2f}/s")


# Global statistics tracker
stats = MessageStats()


# ═══════════════════════════════════════════════════════════════════════════════
# CALLBACK_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def on_connect(client, userdata, flags, rc):
    """
    Handle connection events.
    
    💭 PREDICTION: What does rc=0 mean?
       (Answer: Connection successful, other values indicate errors)
    """
    if rc == 0:
        print(f"[+] Connected to broker (rc={rc})")
        # Subscribe after connection
        topic = userdata.get("topic", "iot/#")
        qos = userdata.get("qos", 0)
        client.subscribe(topic, qos=qos)
        print(f"[+] Subscribed to: {topic} (QoS {qos})")
    else:
        print(f"[!] Connection failed (rc={rc})")


def on_message(client, userdata, msg):
    """
    Process received messages.
    
    💭 PREDICTION: Will this callback fire for retained messages?
       (Answer: Yes, retained messages are delivered on subscription)
    """
    global stats
    
    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    stats.record(msg.topic)
    
    # ─────────────────────────────────────────────────────────────────────────
    # PARSE_PAYLOAD
    # ─────────────────────────────────────────────────────────────────────────
    try:
        data = json.loads(msg.payload)
        temp = data.get('temperature', '?')
        humidity = data.get('humidity', '?')
        print(f"[{ts}] {msg.topic}: T={temp}°C H={humidity}% (QoS={msg.qos})")
    except json.JSONDecodeError:
        # Non-JSON payload
        payload_str = msg.payload.decode(errors='replace')
        print(f"[{ts}] {msg.topic}: {payload_str[:100]} (QoS={msg.qos})")


def on_subscribe(client, userdata, mid, granted_qos):
    """Handle subscription confirmations."""
    print(f"[+] Subscription confirmed (mid={mid}, granted_qos={granted_qos})")


def on_disconnect(client, userdata, rc):
    """Handle disconnection events."""
    if rc == 0:
        print("[*] Disconnected cleanly")
    else:
        print(f"[!] Unexpected disconnection (rc={rc})")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Main entry point."""
    global stats
    
    # ─────────────────────────────────────────────────────────────────────────
    # PARSE_ARGUMENTS
    # ─────────────────────────────────────────────────────────────────────────
    parser = argparse.ArgumentParser(
        description="IoT Controller (MQTT Subscriber) for Week 13",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --broker localhost --topic "iot/#"
  %(prog)s --topic "iot/sensors/+" --qos 1
  %(prog)s --broker localhost --port 8883 --tls --cafile ca.crt

Topic wildcards:
  +  matches exactly one level: sensors/+/temp matches sensors/room1/temp
  #  matches zero or more levels: sensors/# matches sensors/a/b/c
        """
    )
    parser.add_argument("--broker", default="localhost",
                        help="MQTT broker hostname (default: localhost)")
    parser.add_argument("--port", type=int, default=1883,
                        help="MQTT broker port (default: 1883)")
    parser.add_argument("--topic", default="iot/#",
                        help="MQTT topic filter (default: iot/#)")
    parser.add_argument("--qos", type=int, default=0, choices=[0, 1, 2],
                        help="MQTT QoS level (default: 0)")
    parser.add_argument("--tls", action="store_true",
                        help="Enable TLS encryption")
    parser.add_argument("--cafile", default=None,
                        help="CA certificate file for TLS")
    args = parser.parse_args()

    if not MQTT_AVAILABLE:
        print("paho-mqtt is required for this application")
        print("Install with: pip install paho-mqtt")
        return 1
    
    # ─────────────────────────────────────────────────────────────────────────
    # DISPLAY_BANNER
    # ─────────────────────────────────────────────────────────────────────────
    print("=" * 60)
    print("Week 13 - IoT Controller (Subscriber)")
    print("=" * 60)
    print(f"Broker: {args.broker}:{args.port}")
    print(f"Topic filter: {args.topic}")
    print(f"QoS: {args.qos}")
    print(f"TLS: {args.tls}")
    print()
    
    # ─────────────────────────────────────────────────────────────────────────
    # CREATE_MQTT_CLIENT
    # ─────────────────────────────────────────────────────────────────────────
    client = mqtt.Client(userdata={"topic": args.topic, "qos": args.qos})
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.on_disconnect = on_disconnect
    
    # ─────────────────────────────────────────────────────────────────────────
    # CONFIGURE_TLS (if enabled)
    # ─────────────────────────────────────────────────────────────────────────
    if args.tls:
        if not args.cafile:
            print("[!] TLS enabled but --cafile not specified")
            return 1
        client.tls_set(ca_certs=args.cafile)
    
    # ─────────────────────────────────────────────────────────────────────────
    # CONNECT_AND_LISTEN
    # ─────────────────────────────────────────────────────────────────────────
    try:
        client.connect(args.broker, args.port)
    except Exception as e:
        print(f"[!] Connection failed: {e}")
        return 1
    
    print(f"[*] Listening for messages on: {args.topic}")
    print("    Press Ctrl+C to stop")
    print("-" * 60)
    
    try:
        client.loop_forever()
    
    except KeyboardInterrupt:
        print()
        print("-" * 60)
        print(f"[*] {stats.summary()}")
    
    finally:
        # ─────────────────────────────────────────────────────────────────────
        # CLEANUP_CONNECTION
        # ─────────────────────────────────────────────────────────────────────
        client.disconnect()
    
    return 0


if __name__ == "__main__":
    exit(main())
