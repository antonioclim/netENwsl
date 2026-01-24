#!/usr/bin/env python3
"""
Homework 13.1: MQTT IoT Sensor Dashboard
========================================
Computer Networks - Week 13 (WSL Environment)
ASE Bucharest, CSIE | by ing. dr. Antonio Clim

Objectives:
- Subscribe to multiple MQTT topics for sensor data
- Aggregate and display real-time statistics
- Implement topic wildcards for flexible subscriptions

Level: Intermediate (⭐⭐)
Estimated time: 60-75 minutes
"""

from __future__ import annotations
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime
from statistics import mean
from typing import Dict, List, Optional

try:
    import paho.mqtt.client as mqtt
    MQTT_AVAILABLE = True
except ImportError:
    MQTT_AVAILABLE = False

BROKER_HOST = "localhost"
BROKER_PORT = 1883

# ═══════════════════════════════════════════════════════════════════════════════
# DATA_STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class SensorStats:
    """Statistics for a sensor topic."""
    topic: str
    count: int = 0
    total: float = 0.0
    min_value: float = float("inf")
    max_value: float = float("-inf")
    last_value: float = 0.0
    
    def update(self, value: float) -> None:
        self.count += 1
        self.total += value
        self.min_value = min(self.min_value, value)
        self.max_value = max(self.max_value, value)
        self.last_value = value
    
    @property
    def average(self) -> float:
        return self.total / self.count if self.count > 0 else 0.0

# ═══════════════════════════════════════════════════════════════════════════════
# MQTT_DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
class MQTTDashboard:
    """MQTT-based IoT sensor dashboard."""
    
    def __init__(self, host: str = BROKER_HOST, port: int = BROKER_PORT):
        self.host = host
        self.port = port
        self.stats: Dict[str, SensorStats] = {}
        self.message_count = 0
    
    def on_message(self, client, userdata, msg):
        """Callback when message received."""
        self.message_count += 1
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
            value = float(payload.get("value", 0))
            if msg.topic not in self.stats:
                self.stats[msg.topic] = SensorStats(topic=msg.topic)
            self.stats[msg.topic].update(value)
        except (json.JSONDecodeError, ValueError):
            pass
    
    def display_dashboard(self) -> None:
        """Display current sensor statistics."""
        print(f"\n{'='*70}")
        print(f"IoT DASHBOARD — {datetime.now().strftime('%H:%M:%S')} — Messages: {self.message_count}")
        print("=" * 70)
        
        if not self.stats:
            print("No sensor data received...")
            return
        
        print(f"{'Topic':<30} {'Last':<10} {'Avg':<10} {'Min':<10} {'Max':<10}")
        print("-" * 70)
        for topic, stats in sorted(self.stats.items()):
            print(f"{topic:<30} {stats.last_value:<10.2f} {stats.average:<10.2f} "
                  f"{stats.min_value:<10.2f} {stats.max_value:<10.2f}")

def simulate_dashboard() -> None:
    """Simulate dashboard with fake data."""
    import random
    
    print("\n" + "=" * 70)
    print("SIMULATED IoT SENSOR DASHBOARD")
    print("=" * 70)
    
    stats = {
        "sensors/temperature/room1": SensorStats("sensors/temperature/room1"),
        "sensors/humidity/room1": SensorStats("sensors/humidity/room1"),
        "sensors/power/total": SensorStats("sensors/power/total"),
    }
    
    for _ in range(50):
        stats["sensors/temperature/room1"].update(random.uniform(20, 25))
        stats["sensors/humidity/room1"].update(random.uniform(40, 60))
        stats["sensors/power/total"].update(random.uniform(1500, 3000))
    
    print(f"\n{'Topic':<30} {'Last':<10} {'Avg':<10} {'Min':<10} {'Max':<10}")
    print("-" * 70)
    for topic, s in sorted(stats.items()):
        print(f"{topic:<30} {s.last_value:<10.2f} {s.average:<10.2f} "
              f"{s.min_value:<10.2f} {s.max_value:<10.2f}")

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point."""
    print("=" * 70)
    print("Homework 13.1: MQTT IoT Sensor Dashboard")
    print("Computer Networks - Week 13 | ASE Bucharest, CSIE")
    print("=" * 70)
    
    print("""
MQTT Topic Wildcards:
  sensors/temperature/+    → Single-level (any room)
  sensors/#                → Multi-level (all sensors)
    """)
    
    print("""
QoS Levels:
  0 - At most once  (fire and forget)
  1 - At least once (may duplicate)
  2 - Exactly once  (guaranteed)
    """)
    
    if MQTT_AVAILABLE:
        print("paho-mqtt is available. Try connecting to broker...")
    else:
        print("paho-mqtt not installed. Using simulation.")
    
    simulate_dashboard()
    
    print("\n📝 Key Takeaways:")
    print("   1. MQTT is lightweight and ideal for IoT")
    print("   2. Topic wildcards enable flexible subscriptions")
    print("   3. QoS levels balance reliability vs performance")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
