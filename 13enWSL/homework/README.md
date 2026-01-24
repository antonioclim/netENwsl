# 📝 Homework — Week 13: IoT Protocols and Network Security

> Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

## Overview

This week's homework combines IoT protocol implementation with network security auditing, providing both offensive understanding and defensive skills.

## Assignments

| File | Topic | Difficulty | Est. Time |
|------|-------|------------|-----------|
| `hw_13_01_mqtt_dashboard.py` | MQTT IoT Sensor Dashboard | ⭐⭐ Intermediate | 60-75 min |
| `hw_13_02_security_audit.py` | Network Security Audit Script | ⭐⭐⭐ Advanced | 75-90 min |

## Assignment Details

### hw_13_01_mqtt_dashboard.py

Build a real-time dashboard for IoT sensor data using MQTT.

**Learning Objectives:**
- Subscribe to MQTT topics with wildcards
- Parse and aggregate sensor messages
- Display real-time statistics
- Understand MQTT QoS levels

**Key Skills:**
- MQTT client programming
- Topic wildcard patterns (`+` and `#`)
- Real-time data aggregation
- Event-driven programming

**MQTT Concepts Covered:**
- Topic hierarchies (e.g., `sensors/temperature/room1`)
- Single-level wildcard (`+`)
- Multi-level wildcard (`#`)
- QoS 0, 1, 2 trade-offs
- Retained messages

### hw_13_02_security_audit.py

Implement a network security audit tool for service discovery and vulnerability detection.

**Learning Objectives:**
- Perform TCP port scanning
- Implement banner grabbing for service identification
- Detect common vulnerabilities from version information
- Generate security assessment reports

**Key Skills:**
- Socket programming for scanning
- Service fingerprinting
- Vulnerability assessment
- Report generation

**⚠️ Ethical Note:** Only scan systems you own or have explicit permission to test. This exercise is for EDUCATIONAL purposes on lab environments only.

## Prerequisites

Before starting, ensure you have completed:
- Week 13 lab exercises
- Understanding of MQTT protocol
- Basic security concepts

For MQTT exercise:
- Mosquitto broker should be running (port 1883)
- Install paho-mqtt: `pip install paho-mqtt`

## Submission Guidelines

1. Complete all `TODO` sections
2. For MQTT: Demonstrate dashboard with sample data
3. For Security: Generate audit report for localhost
4. Document findings and recommendations

## Grading Rubric

| Criterion | Points |
|-----------|--------|
| Correct implementation | 40% |
| Functional demonstration | 25% |
| Analysis and recommendations | 20% |
| Code quality and ethics compliance | 15% |

## Tips

### MQTT Dashboard
- Test with simulated data if broker unavailable
- Use wildcards strategically for flexible subscriptions
- Consider message parsing errors gracefully
- Statistics should handle missing/malformed data

### Security Audit
- Start with localhost (always safe to scan)
- Parallelise port scanning for efficiency
- Banner grabbing requires patience (timeouts)
- Not all open ports are vulnerabilities — context matters

## Security Considerations

The security audit exercise teaches:
- **Reconnaissance techniques** used by both attackers and defenders
- **Service identification** through banner analysis
- **Risk assessment** based on exposed services
- **Defensive recommendations** for hardening

Remember: The goal is to understand how to PROTECT networks, not attack them.

### Common Findings to Understand

| Finding | Risk Level | Typical Recommendation |
|---------|------------|------------------------|
| Telnet open | High | Replace with SSH |
| Anonymous FTP | Medium | Disable or restrict |
| Database exposed | High | Firewall + authentication |
| Outdated versions | Varies | Update software |

---

*Week 13 Homework — Computer Networks*
