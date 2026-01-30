#!/usr/bin/env python3
"""
IoT Sensor Simulator
====================
Week 13 - IoT and Security in Computer Networks
ASE Bucharest, CSIE | by ing. dr. Antonio Clim

LEARNING OBJECTIVES:
1. UNDERSTAND IoT telemetry patterns
2. APPLY MQTT publish operations
3. ANALYSE sensor data flow in Wireshark

Simulates an IoT sensor publishing temperature and humidity readings
at regular intervals via MQTT.

USAGE:
    # Basic sensor (plaintext MQTT)
    python3 src/apps/iot_sensor.py --broker localhost --port 1883

    # Custom topic and interval
    python3 src/apps/iot_sensor.py --topic "building/floor1/temp" --interval 2.0

    # TLS connection
    python3 src/apps/iot_sensor.py --broker localhost --port 8883 \\
        --tls --cafile docker/configs/certs/ca.crt

PAIR PROGRAMMING:
- Run this in one terminal while partner monitors with mosquitto_sub
- Observe traffic patterns in Wireshark
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORT_DEPENDENCIES
# ═══════════════════════════════════════════════════════════════════════════════
import argparse
import json
import time
import random
import ssl
from datetime import datetime
from typing import Optional, List, Dict, Tuple, Any

try:
    import paho.mqtt.client as mqtt  # type: ignore
    MQTT_AVAILABLE = True
except ImportError:  # pragma: no cover
    mqtt = None  # type: ignore
    MQTT_AVAILABLE = False


# ═══════════════════════════════════════════════════════════════════════════════
# SENSOR_SIMULATION
# ═══════════════════════════════════════════════════════════════════════════════

def generate_reading() -> dict:
    """
    Generate simulated sensor reading.
    
    💭 PREDICTION: What range of temperatures will this produce?
       (Answer: 15°C to 30°C based on 20 + random(-5, 10))
    
    Returns:
        Dictionary with timestamp, temperature and humidity
    """
    return {
        "timestamp": datetime.now().isoformat(),
        "temperature": round(20 + random.uniform(-5, 10), 2),
        "humidity": round(50 + random.uniform(-10, 10), 1),
        "unit": "celsius"
    }


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Main entry point."""
    
    # ─────────────────────────────────────────────────────────────────────────
    # PARSE_ARGUMENTS
    # ─────────────────────────────────────────────────────────────────────────
    parser = argparse.ArgumentParser(
        description="IoT Sensor Simulator for Week 13",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --broker localhost --port 1883
  %(prog)s --topic "sensors/outdoor/weather" --interval 10
  %(prog)s --broker localhost --port 8883 --tls --cafile ca.crt
        """
    )
    parser.add_argument("--broker", default="localhost",
                        help="MQTT broker hostname (default: localhost)")
    parser.add_argument("--port", type=int, default=1883,
                        help="MQTT broker port (default: 1883)")
    parser.add_argument("--topic", default="iot/sensors/temp",
                        help="MQTT topic to publish to (default: iot/sensors/temp)")
    parser.add_argument("--interval", type=float, default=5.0,
                        help="Publishing interval in seconds (default: 5.0)")
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
    # CREATE_MQTT_CLIENT
    # ─────────────────────────────────────────────────────────────────────────
    sensor_id = f"sensor-{random.randint(1000, 9999)}"
    client = mqtt.Client(client_id=sensor_id)
    
    # ─────────────────────────────────────────────────────────────────────────
    # CONFIGURE_TLS (if enabled)
    # ─────────────────────────────────────────────────────────────────────────
    if args.tls:
        if not args.cafile:
            print("[!] TLS enabled but --cafile not specified")
            return 1
        client.tls_set(ca_certs=args.cafile)
    
    # ─────────────────────────────────────────────────────────────────────────
    # CONNECT_TO_BROKER
    # ─────────────────────────────────────────────────────────────────────────
    print("=" * 60)
    print("Week 13 - IoT Sensor Simulator")
    print("=" * 60)
    print(f"Sensor ID: {sensor_id}")
    print(f"Broker: {args.broker}:{args.port}")
    print(f"Topic: {args.topic}")
    print(f"Interval: {args.interval}s")
    print(f"QoS: {args.qos}")
    print(f"TLS: {args.tls}")
    print()
    
    try:
        client.connect(args.broker, args.port)
        client.loop_start()
        print(f"[+] Connected to broker")
    except Exception as e:
        print(f"[!] Connection failed: {e}")
        return 1
    
    # ─────────────────────────────────────────────────────────────────────────
    # PUBLISH_READINGS_LOOP
    # ─────────────────────────────────────────────────────────────────────────
    print(f"[*] Publishing to {args.topic} every {args.interval}s")
    print("    Press Ctrl+C to stop")
    print("-" * 60)
    
    count = 0
    try:
        while True:
            payload = generate_reading()
            result = client.publish(args.topic, json.dumps(payload), qos=args.qos)
            count += 1
            
            # Display reading
            print(f"[{count:4d}] temp={payload['temperature']:5.1f}°C "
                  f"humidity={payload['humidity']:4.1f}% "
                  f"(mid={result.mid})")
            
            time.sleep(args.interval)
    
    except KeyboardInterrupt:
        print()
        print("-" * 60)
        print(f"[*] Stopped after {count} readings")
    
    finally:
        # ─────────────────────────────────────────────────────────────────────
        # CLEANUP_CONNECTION
        # ─────────────────────────────────────────────────────────────────────
        client.loop_stop()
        client.disconnect()
        print("[+] Disconnected from broker")
    
    return 0


if __name__ == "__main__":
    exit(main())
