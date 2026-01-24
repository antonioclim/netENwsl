# Project 15: IoT Network with Edge Computing and MQTT

> **Course:** Computer Networks | **Institution:** ASE Bucharest - CSIE | **Project type:** Main

**Common guides:** [Pair Programming](../docs/common/pair_programming_guide.md) | [Code Quality](../docs/common/code_quality_standards.md) | [Git Workflow](../docs/common/git_workflow_detailed.md)

### 📅 Stage Calendar
| Stage | Week | Deliverables | Score |
|-------|------|--------------|-------|
| **E1** - Design | Week 5 | Specifications + Diagrams | 20% |
| **E2** - Prototype | Week 9 | Partial implementation | 25% |
| **E3** - Final | Week 13 | Complete version | 35% |
| **E4** - Presentation | Week 14 | Live demo | 20% |

**Repository:** `https://github.com/[username]/retele-proiect-15`

---

## 📚 Project Description

Simulate an IoT network using MQTT protocol with edge computing nodes. Implement sensors, MQTT broker, edge processors and demonstrate real-time data flow with local processing.

### 🎯 Learning Objectives
- **Implement** MQTT publish/subscribe communication
- **Configure** MQTT broker (Mosquitto)
- **Design** edge computing workflows
- **Handle** QoS levels and retained messages

---

## 🎯 Concept Analogies

### MQTT = Newsletter Subscription
🏠 **Analogy:** You subscribe to topics (newsletters) you're interested in. Publishers (sensors) send to topics. You receive only what you subscribed to. The post office (broker) handles delivery.

💻 **Technical:** Sensors publish, applications subscribe, broker routes messages.

### Edge Computing = Local Manager
🏠 **Analogy:** Instead of sending every question to headquarters (cloud), a local manager (edge) handles common tasks immediately.

---

## 🗳️ Peer Instruction Questions

### Question 1: QoS Levels
**Question:** MQTT QoS 2 guarantees:
- A) Fast delivery
- B) At most once delivery
- C) Exactly once delivery ✓
- D) Broadcast delivery

### Question 2: Retained Messages
**Question:** What is a retained message?
- A) Message stored forever
- B) Last message on topic, sent to new subscribers ✓
- C) High priority message
- D) Encrypted message

---

## ❌ Common Misconceptions

### 🚫 "MQTT is only for small messages"
**CORRECT:** MQTT can handle large payloads but is optimised for small, frequent messages.

### 🚫 "QoS 2 is always best"
**CORRECT:** QoS 2 has overhead. For non-critical data (temperature readings), QoS 0 or 1 is more efficient.

---

## 📖 Glossary
| Term | Definition |
|------|------------|
| **MQTT** | Message Queuing Telemetry Transport |
| **Broker** | Server routing messages between clients |
| **Topic** | Hierarchical message channel |
| **QoS** | Quality of Service level (0, 1, 2) |
| **Retained** | Last message kept for new subscribers |
| **Edge Computing** | Processing near data source |

---

## 🔨 Implementation Example

```python
#!/usr/bin/env python3
"""IoT Sensor Simulator with MQTT"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import paho.mqtt.client as mqtt
import json
import time
import random

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════
BROKER = "localhost"
PORT = 1883
SENSOR_ID = "temp_sensor_01"
TOPIC = f"sensors/{SENSOR_ID}/temperature"

# ═══════════════════════════════════════════════════════════════════════════════
# SENSOR_SIMULATOR
# ═══════════════════════════════════════════════════════════════════════════════
def simulate_sensor():
    """Simulate temperature sensor publishing to MQTT."""
    
    client = mqtt.Client(client_id=SENSOR_ID)
    client.connect(BROKER, PORT)
    client.loop_start()
    
    print(f"Sensor {SENSOR_ID} connected to {BROKER}")
    
    try:
        while True:
            # 💭 PREDICTION: What QoS should we use for temperature?
            # Answer: QoS 0 or 1 — losing one reading isn't critical
            
            temperature = 20 + random.uniform(-5, 10)
            payload = json.dumps({
                "sensor_id": SENSOR_ID,
                "temperature": round(temperature, 2),
                "timestamp": time.time()
            })
            
            client.publish(TOPIC, payload, qos=1)
            print(f"Published: {temperature:.2f}°C")
            
            time.sleep(5)
    
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    simulate_sensor()
```

```yaml
# docker-compose.yml for IoT stack
services:
  mosquitto:
    image: eclipse-mosquitto:2
    ports:
      - "1883:1883"
    volumes:
      - ./mosquitto.conf:/mosquitto/config/mosquitto.conf

  edge-processor:
    build: ./edge
    depends_on:
      - mosquitto
    environment:
      - MQTT_BROKER=mosquitto
```

---

## 📚 Laboratory References

Consult these resources from **netENwsl** (https://github.com/antonioclim/netENwsl):

| Week | Folder | Relevant Content |
|------|--------|------------------|
| 13 | `13enWSL/` | IoT with MQTT, Mosquitto |
| 9 | `09enWSL/` | TLS/SSL for secure communication |

---

*Last update: January 2026 — Computer Networks, ASE Bucharest*
