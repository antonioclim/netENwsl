# ❌ Common Misconceptions — Week 13
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> This document lists common misunderstandings about IoT, MQTT and network security, with corrections and practical verifications.

---

## MQTT Protocol

### 🚫 Misconception 1: "MQTT QoS 2 means the message is encrypted"

**WRONG:** "QoS 2 provides the highest security because it's the highest level."

**CORRECT:** QoS (Quality of Service) refers only to **delivery guarantees**, not security or encryption. QoS 2 ensures exactly-once delivery through a four-way handshake, but the message content remains plaintext unless TLS is used.

| QoS Level | Delivery Guarantee | Security Provided |
|-----------|-------------------|-------------------|
| 0 | At most once (fire and forget) | None |
| 1 | At least once (acknowledged) | None |
| 2 | Exactly once (4-way handshake) | None |

**Practical verification:**
```bash
# Subscribe with Wireshark capturing on port 1883
mosquitto_sub -h localhost -p 1883 -t "test/#" -v &

# Publish with QoS 2
mosquitto_pub -h localhost -p 1883 -t "test/secret" -m "password123" -q 2

# In Wireshark: Follow TCP stream — message is visible in plaintext!
```

---

### 🚫 Misconception 2: "MQTT topic wildcards work like regular expressions"

**WRONG:** "The + wildcard matches any number of characters, like .* in regex."

**CORRECT:** MQTT wildcards have specific, limited behaviour:
- `+` matches exactly **one topic level** (between slashes)
- `#` matches **zero or more levels**, but only at the **end** of a subscription

| Pattern | Matches | Does NOT Match |
|---------|---------|----------------|
| `sensors/+/temp` | `sensors/room1/temp` | `sensors/building/room1/temp` |
| `sensors/#` | `sensors/a/b/c/d` | (matches everything under sensors/) |
| `+/+/temp` | `a/b/temp` | `a/temp`, `a/b/c/temp` |

**Practical verification:**
```bash
# Terminal 1: Subscribe with single-level wildcard
mosquitto_sub -h localhost -p 1883 -t "building/+/temperature" -v

# Terminal 2: Test various publishes
mosquitto_pub -h localhost -p 1883 -t "building/floor1/temperature" -m "22"  # ✅ Received
mosquitto_pub -h localhost -p 1883 -t "building/floor1/room1/temperature" -m "23"  # ❌ NOT received
```

---

### 🚫 Misconception 3: "Anonymous MQTT access is secure for internal networks"

**WRONG:** "If the broker is on a private network, we don't need authentication."

**CORRECT:** Internal networks are frequently compromised. Anonymous access allows any device on the network to:
- Subscribe to all topics (including sensitive data)
- Publish malicious commands to actuators
- Conduct man-in-the-middle attacks

**Why this matters:** The Mirai botnet specifically targeted IoT devices with default/no credentials on "internal" networks.

**Practical verification:**
```bash
# Anyone on the network can subscribe to everything
mosquitto_sub -h broker.internal -p 1883 -t "#" -v
# Output reveals: sensor data, commands, device status...

# Attacker can publish fake commands
mosquitto_pub -h broker.internal -p 1883 -t "factory/line1/emergency_stop" -m "STOP"
```

---

## TLS and Encryption

### 🚫 Misconception 4: "TLS encrypts everything, including IP addresses"

**WRONG:** "With TLS enabled, attackers can't see any information about my traffic."

**CORRECT:** TLS encrypts the **application layer payload** but network metadata remains visible:

| Visible (NOT encrypted) | Hidden (encrypted) |
|------------------------|-------------------|
| Source IP address | Message content |
| Destination IP address | MQTT topics |
| Port numbers | Usernames/passwords |
| Packet sizes | Application data |
| Connection timing | Session tokens |
| Traffic patterns | Payload structure |

**Why this matters:** Traffic analysis attacks can infer activity patterns, device types and even message content based on timing and sizes.

**Practical verification:**
```bash
# Capture TLS traffic
tcpdump -i any port 8883 -w tls_capture.pcap &

# Generate MQTT over TLS traffic
python3 src/exercises/ex_13_02_mqtt_client.py --mode publish \
  --broker localhost --port 8883 --tls --cafile docker/configs/certs/ca.crt \
  --topic "secret/data" --message "confidential"

# In Wireshark: You can see IPs, ports, timing — but not topic or message
```

---

### 🚫 Misconception 5: "TLS 1.3 is backwards compatible with TLS 1.1"

**WRONG:** "Our server supports TLS 1.3 so it will work with all clients."

**CORRECT:** TLS 1.3 removed support for older, insecure cipher suites. Clients that only support TLS 1.1 or earlier **cannot** connect to a TLS 1.3-only server.

| TLS Version | Status | Compatible With |
|-------------|--------|-----------------|
| TLS 1.0 | Deprecated | 1.0, 1.1, 1.2 |
| TLS 1.1 | Deprecated | 1.0, 1.1, 1.2 |
| TLS 1.2 | Current | 1.2, 1.3 (usually) |
| TLS 1.3 | Current | 1.2 (fallback), 1.3 |

**Practical verification:**
```bash
# Check what TLS versions the server supports
openssl s_client -connect localhost:8883 -tls1_1 2>&1 | grep -i "protocol\|error"
# May show: "no protocols available" if TLS 1.1 is disabled
```

---

## Port Scanning

### 🚫 Misconception 6: "Filtered port means the service is protected"

**WRONG:** "The scan shows 'filtered', so that port is secure."

**CORRECT:** "Filtered" only means a firewall is **dropping packets** without response. It indicates:
- A firewall rule exists (DROP, not REJECT)
- The scanner received no reply (timeout)
- The actual service state is **unknown**

| Port State | What Happened | What It Means |
|------------|---------------|---------------|
| Open | Connection succeeded | Service is accepting connections |
| Closed | RST packet received | No service, but host is reachable |
| Filtered | No response (timeout) | Firewall dropping packets |

**Why this matters:** "Filtered" is not "secure" — the service might be running and vulnerable, just behind a firewall that could be bypassed.

**Practical verification:**
```bash
# Scan a port with DROP rule
python3 src/exercises/ex_13_01_port_scanner.py --target 10.0.13.50 --ports 443 --timeout 2
# Output: "filtered" (if firewall drops)

# Scan a closed port (no service)
python3 src/exercises/ex_13_01_port_scanner.py --target localhost --ports 12345
# Output: "closed" (RST received)
```

---

### 🚫 Misconception 7: "Port scanning is always illegal"

**WRONG:** "I can't practice port scanning because it's a crime."

**CORRECT:** Port scanning legality depends on **context and authorisation**:

| Scenario | Legal? |
|----------|--------|
| Scanning your own systems | ✅ Yes |
| Scanning with explicit written permission | ✅ Yes |
| Scanning a controlled lab environment | ✅ Yes |
| Scanning without permission | ❌ No (unauthorised access) |
| Scanning to find vulnerable targets | ❌ No (malicious intent) |

**In this laboratory:** All scanning is against containers you control — completely legal and encouraged for learning.

**Practical verification:**
```bash
# This is legal — scanning our own lab containers
python3 src/exercises/ex_13_01_port_scanner.py --target localhost --ports 1-10000

# Document your authorisation for any scanning outside the lab
```

---

### 🚫 Misconception 8: "An open port means the service is vulnerable"

**WRONG:** "Port 22 is open, so the server is hackable via SSH."

**CORRECT:** An open port only means a service is **accepting connections**. Vulnerability depends on:
- Software version and patch level
- Configuration (authentication, encryption)
- Access controls (allowed users, IPs)
- Known CVEs for that service

| Open Port | Service | Vulnerable? |
|-----------|---------|-------------|
| 22 | SSH | Depends on version, key/password policy |
| 80 | HTTP | Depends on web application security |
| 1883 | MQTT | Depends on authentication configuration |

**Practical verification:**
```bash
# Port is open, but is it vulnerable?
# Step 1: Identify service version
echo "" | nc -v localhost 22 2>&1 | head -1
# Output: "SSH-2.0-OpenSSH_8.9p1 Ubuntu..."

# Step 2: Check for known vulnerabilities
# Search: "OpenSSH 8.9p1 CVE"
```

---

## IoT Security

### 🚫 Misconception 9: "IoT devices are too simple to be hacked"

**WRONG:** "My temperature sensor just sends numbers — what could an attacker do?"

**CORRECT:** IoT devices are prime targets because they often have:
- Minimal security (no authentication, no encryption)
- Long lifespans with no updates
- Network access (can be pivots to internal systems)
- Compute resources (can be used for DDoS)

**Real-world example:** The Mirai botnet infected ~600,000 IoT devices (cameras, routers, DVRs) and launched a 1.2 Tbps DDoS attack against Dyn DNS in 2016.

**Attack vectors for "simple" sensors:**
| Attack | Impact |
|--------|--------|
| Data injection | False readings → wrong decisions |
| Eavesdropping | Privacy breach, industrial espionage |
| Device recruitment | DDoS botnet participation |
| Lateral movement | Pivot to more valuable systems |

---

### 🚫 Misconception 10: "Encryption is more important than authentication"

**WRONG:** "We need to encrypt everything first, then worry about passwords."

**CORRECT:** Authentication should be prioritised before encryption because:
- Encrypted channel with default password = attacker has encrypted access
- Strong authentication with plaintext = attacker can see but not act
- OWASP IoT Top 10 ranks "Weak Passwords" as #1, "Insecure Data Transfer" as #7

| Priority | Security Measure | Reason |
|----------|-----------------|--------|
| 1 | Strong authentication | Prevents unauthorised access |
| 2 | Authorisation (ACLs) | Limits what authenticated users can do |
| 3 | Encryption (TLS) | Protects data in transit |
| 4 | Monitoring/logging | Detects and responds to breaches |

**Practical verification:**
```bash
# Scenario A: Encryption but weak auth
# Attacker with credentials has full encrypted access

# Scenario B: Strong auth but no encryption
# Attacker can see traffic but cannot send commands

# Which is worse? Usually A — attacker has control
```

---

## Quick Reference: Misconception → Reality

| # | Misconception | Reality |
|---|---------------|---------|
| 1 | QoS 2 = encryption | QoS = delivery guarantee only |
| 2 | + wildcard = regex .* | + = exactly one topic level |
| 3 | Internal network = safe | Internal networks get compromised |
| 4 | TLS hides everything | Metadata remains visible |
| 5 | TLS 1.3 backwards compatible | Old clients may not connect |
| 6 | Filtered = protected | Filtered = unknown state |
| 7 | Scanning always illegal | Legal with authorisation |
| 8 | Open port = vulnerable | Depends on configuration |
| 9 | Simple devices = safe | Simple = easy target |
| 10 | Encrypt before authenticate | Authenticate first |

---

*Computer Networks — Week 13: IoT and Security*
*ASE Bucharest, CSIE | by ing. dr. Antonio Clim*
