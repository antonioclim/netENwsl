# 🎯 Concept Analogies — Week 13: IoT and Security
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Understanding through everyday analogies before technical details. This follows the Concrete-Pictorial-Abstract (CPA) approach.

---

## 1. MQTT Broker

### 🏠 Real-World Analogy
**MQTT Broker = Post Office Sorting Centre**

Imagine a central post office that:
- Receives letters from senders (publishers)
- Sorts them by destination address (topic)
- Delivers to recipients who registered for that address (subscribers)
- Never opens or reads the letters, just routes them

The post office doesn't care what's inside — it just matches sender topics to subscriber interests.

### 🖼️ Visual Representation
```
    ┌─────────────────────────────────────────────────────────────┐
    │                    POST OFFICE (Broker)                      │
    │                                                              │
    │   INCOMING MAIL          SORTING           DELIVERY ROUTES   │
    │   ┌─────────┐         ┌─────────┐         ┌─────────┐       │
    │   │ Letter  │         │ Topic:  │         │ Sub A   │       │
    │   │ from    │ ──────▶ │ sensors/│ ──────▶ │ wants   │       │
    │   │ Sensor  │         │ temp    │         │ sensors/│       │
    │   └─────────┘         └─────────┘         └─────────┘       │
    │                            │                                 │
    │                            │              ┌─────────┐       │
    │                            └────────────▶ │ Sub B   │       │
    │                                           │ wants   │       │
    │                                           │ sensors/│       │
    │                                           └─────────┘       │
    └─────────────────────────────────────────────────────────────┘
```

### 💻 Technical Reality
```python
# The broker (Mosquitto) runs as a service
# Publishers send to topics:
client.publish("sensors/temperature", "22.5")

# Subscribers register interest:
client.subscribe("sensors/#")  # All sensor topics

# Broker matches and delivers — publishers don't know subscribers
```

### ⚠️ Where the Analogy Breaks Down
- Post offices have physical limits; MQTT can handle thousands of messages/second
- Letters are one-to-one; MQTT topics can have many subscribers (one-to-many)
- Post offices store mail; MQTT is usually real-time (unless retained)

---

## 2. MQTT QoS Levels

### 🏠 Real-World Analogy
**QoS Levels = Shipping Options**

| QoS | Shipping Equivalent | Guarantee |
|-----|---------------------|-----------|
| **0** | Postcard (no tracking) | Might arrive, might not |
| **1** | Tracked package | Confirmed delivery, might arrive twice |
| **2** | Registered mail with signature | Exactly once, confirmed receipt |

### 🖼️ Visual Representation
```
QoS 0: Fire and Forget
┌────────┐    📨    ┌────────┐
│Publisher│ ──────▶ │ Broker │     (no confirmation)
└────────┘         └────────┘

QoS 1: Acknowledged
┌────────┐    📨    ┌────────┐
│Publisher│ ──────▶ │ Broker │
└────────┘ ◀────── └────────┘
              ✓ ACK

QoS 2: Exactly Once (4-way handshake)
┌────────┐  PUBLISH  ┌────────┐
│Publisher│ ───────▶ │ Broker │
│        │ ◀─────── │        │
│        │  PUBREC  │        │
│        │ ───────▶ │        │
│        │  PUBREL  │        │
│        │ ◀─────── │        │
└────────┘  PUBCOMP └────────┘
```

### 💻 Technical Reality
```python
# QoS 0 — fast but unreliable
client.publish("sensors/temp", "22.5", qos=0)

# QoS 1 — guaranteed at least once
client.publish("alerts/critical", "Fire!", qos=1)

# QoS 2 — exactly once (expensive)
client.publish("transactions/payment", "€100", qos=2)
```

### ⚠️ Where the Analogy Breaks Down
- Shipping has days of delay; MQTT is milliseconds
- QoS applies per-hop (publisher→broker, broker→subscriber separately)
- Higher QoS = more network overhead, not higher cost in money

---

## 3. Port Scanning

### 🏠 Real-World Analogy
**Port Scanning = Checking Which Doors Are Unlocked**

Imagine walking down a hotel corridor and trying each door:
- **Open**: Door opens (service listening)
- **Closed**: Door locked, you hear "occupied!" (RST response)
- **Filtered**: No response at all, like the room doesn't exist (firewall DROP)

### 🖼️ Visual Representation
```
    HOTEL CORRIDOR (Target Host)
    ═══════════════════════════════════════════════════
    
    Room 22     Room 80     Room 443    Room 1883
    ┌─────┐     ┌─────┐     ┌─────┐     ┌─────┐
    │ SSH │     │     │     │░░░░░│     │MQTT │
    │     │     │EMPTY│     │GUARD│     │     │
    │ 🟢  │     │ 🔴  │     │ 🟡  │     │ 🟢  │
    │OPEN │     │CLOSED│    │FILTER│    │OPEN │
    └─────┘     └─────┘     └─────┘     └─────┘
    
    Legend:
    🟢 OPEN = Service welcoming connections
    🔴 CLOSED = "Go away!" (RST packet)
    🟡 FILTERED = Silent guard (firewall drops packets)
```

### 💻 Technical Reality
```python
# Knock on the door (TCP connect)
result = sock.connect_ex((host, port))

if result == 0:
    print("OPEN")      # Door opened
elif result == 111:    # ECONNREFUSED
    print("CLOSED")    # Door refused
# Timeout → FILTERED (no answer)
```

### ⚠️ Where the Analogy Breaks Down
- Hotel doors don't change state; ports can open/close dynamically
- You can see hotel doors; ports are invisible until probed
- Walking a corridor is slow; scanning thousands of ports takes seconds

---

## 4. TLS Handshake

### 🏠 Real-World Analogy
**TLS Handshake = Entering a Secure Building**

1. **Client Hello**: "Hi, I'm here to visit. Here are the languages I speak."
2. **Server Hello**: "Welcome. Let's speak English. Here's my ID badge."
3. **Certificate Check**: You verify the ID with the building directory.
4. **Key Exchange**: You both agree on a secret knock pattern.
5. **Encrypted Communication**: Now you speak in code only you two understand.

### 🖼️ Visual Representation
```
    VISITOR                                    SECURITY DESK
    (Client)                                   (Server)
       │                                           │
       │ "Hello, I speak English, French, German" │
       │ ─────────────────────────────────────────▶│
       │                                           │
       │     "Let's use English. My ID badge:"    │
       │◀───────────────────────────────────────── │
       │         [CERTIFICATE: Server Inc.]        │
       │                                           │
       │   (checks ID against trusted list)        │
       │         ✓ ID is valid                     │
       │                                           │
       │  "Here's my secret for our code:"        │
       │ ─────────────────────────────────────────▶│
       │                                           │
       │    "Got it. Ready for coded messages"    │
       │◀───────────────────────────────────────── │
       │                                           │
       │ ════════ ENCRYPTED CHANNEL ════════════  │
       │       🔒 Only we understand 🔒           │
```

### 💻 Technical Reality
```python
# Create secure context (establish trust rules)
context = ssl.create_default_context()
context.load_verify_locations("ca.crt")  # Trusted IDs

# Wrap socket (initiate handshake)
secure_sock = context.wrap_socket(sock, server_hostname="broker.local")

# Now all communication is encrypted
secure_sock.send(b"secret data")
```

### ⚠️ Where the Analogy Breaks Down
- Building entry is one-time; TLS re-keys periodically
- Humans can be tricked; cryptographic verification is mathematical
- Visitors see inside; TLS traffic looks like random bytes to observers

---

## 5. Topic Wildcards

### 🏠 Real-World Analogy
**Topic Wildcards = Mail Forwarding Rules**

Imagine setting up mail forwarding:
- `+` = "Any single word": `building/+/temperature` forwards mail from any floor
- `#` = "Everything after this": `building/#` forwards ALL building mail

### 🖼️ Visual Representation
```
    SUBSCRIPTION: building/+/temperature
    
    ✅ MATCHES:
    building/floor1/temperature  ──▶  [Delivered]
    building/floor2/temperature  ──▶  [Delivered]
    building/basement/temperature ──▶ [Delivered]
    
    ❌ DOES NOT MATCH:
    building/floor1/humidity     ──▶  [Not delivered - wrong ending]
    building/floor1/room1/temperature ──▶ [Not delivered - too many levels]
    weather/temperature          ──▶  [Not delivered - wrong start]
    
    ════════════════════════════════════════════════════════════════
    
    SUBSCRIPTION: building/#
    
    ✅ MATCHES EVERYTHING UNDER building/:
    building/floor1/temperature  ──▶  [Delivered]
    building/floor1/room1/temp   ──▶  [Delivered]
    building/status              ──▶  [Delivered]
    building/a/b/c/d/e/f         ──▶  [Delivered]
```

### 💻 Technical Reality
```python
# Single-level wildcard
client.subscribe("sensors/+/temperature")
# Matches: sensors/room1/temperature, sensors/outdoor/temperature
# NOT: sensors/building/floor1/temperature (too deep)

# Multi-level wildcard (end only)
client.subscribe("sensors/#")
# Matches: sensors/anything/at/any/depth
```

### ⚠️ Where the Analogy Breaks Down
- Mail forwarding is per-recipient; MQTT wildcards apply to the subscription
- `#` only works at the end; you can't do `#/temperature`
- Wildcards are for subscribing only, not publishing

---

## 6. Vulnerability Scanning

### 🏠 Real-World Analogy
**Vulnerability Scanning = Home Security Inspection**

A security consultant checks your house:
1. **Reconnaissance**: Walks around, notes all entry points (port scan)
2. **Identification**: Checks door and lock brands (service detection)
3. **Testing**: Tries known weaknesses for those locks (vulnerability check)
4. **Report**: Lists what's at risk and how to fix it

### 🖼️ Visual Representation
```
    YOUR NETWORK (House)
    ════════════════════════════════════════════════════════
    
    PHASE 1: RECONNAISSANCE
    ┌─────────────────────────────────────────────────────┐
    │ "Found 5 entry points (open ports)"                 │
    │  - Front door (22/SSH)                              │
    │  - Back door (80/HTTP)                              │
    │  - Window (1883/MQTT)                               │
    │  - Garage (8080/DVWA)                               │
    │  - Basement (2121/FTP)                              │
    └─────────────────────────────────────────────────────┘
    
    PHASE 2: IDENTIFICATION
    ┌─────────────────────────────────────────────────────┐
    │ "Identified lock brands (service versions)"         │
    │  - Front: OpenSSH 8.9                               │
    │  - Window: Mosquitto 2.0.15                         │
    │  - Basement: vsftpd 2.3.4 ⚠️ KNOWN VULNERABLE      │
    └─────────────────────────────────────────────────────┘
    
    PHASE 3: REPORT
    ┌─────────────────────────────────────────────────────┐
    │ 🔴 HIGH: vsftpd 2.3.4 has backdoor (CVE-2011-2523) │
    │ 🟡 MED: MQTT accepts anonymous connections          │
    │ 🟢 LOW: SSH using secure configuration              │
    └─────────────────────────────────────────────────────┘
```

### 💻 Technical Reality
```python
# Phase 1: Port scan
results = scan_host("10.0.13.11", ports=range(1, 10000))

# Phase 2: Service identification
for port in results.open_ports:
    banner = grab_banner(host, port)
    version = identify_service(banner)

# Phase 3: Vulnerability check
for service in identified_services:
    cves = lookup_vulnerabilities(service.name, service.version)
```

### ⚠️ Where the Analogy Breaks Down
- House inspection requires physical presence; scanning is remote
- Locks don't announce their model; services often reveal versions
- Security consultant needs permission; so does ethical scanning

---

## 7. Filtered Port (Firewall DROP)

### 🏠 Real-World Analogy
**Filtered Port = Silent Security Guard**

Imagine knocking on a door:
- **Open door**: Someone answers and lets you in (service available)
- **Closed door**: Someone shouts "Go away!" through the door (RST packet)
- **Filtered**: A silent guard intercepts you in the corridor and escorts you away without a word — you never even reach the door (firewall DROP)

The guard's job is to make it seem like the room doesn't exist at all.

### 🖼️ Visual Representation
```
    APPROACHING ROOM 443 (Port 443)
    
    Scenario A: No Guard (CLOSED)
    ═══════════════════════════════════════════
    You ──────▶ Door ──────▶ "GO AWAY!" (RST)
                             Response received
    
    Scenario B: Silent Guard (FILTERED)
    ═══════════════════════════════════════════
    You ──────▶ [GUARD] ╳    (intercepted)
                   │
                   └──▶ You wait... and wait... (timeout)
                        No response ever comes
    
    ┌─────────────────────────────────────────┐
    │  From your perspective:                  │
    │  • CLOSED = Someone said "no"           │
    │  • FILTERED = Complete silence          │
    │                                          │
    │  Firewall rule: iptables -j DROP        │
    │  vs             iptables -j REJECT      │
    └─────────────────────────────────────────┘
```

### 💻 Technical Reality
```python
# In port scanner code:
try:
    sock.connect((host, port))
    return "open"
except ConnectionRefusedError:
    return "closed"    # Got RST response
except socket.timeout:
    return "filtered"  # No response at all
```

```bash
# Firewall configuration difference:
# DROP - silent, causes "filtered" result
sudo iptables -A INPUT -p tcp --dport 443 -j DROP

# REJECT - sends RST, causes "closed" result  
sudo iptables -A INPUT -p tcp --dport 443 -j REJECT
```

### ⚠️ Where the Analogy Breaks Down
- Guards are visible; firewall rules are invisible to external observers
- Guards might eventually respond; DROP never responds
- You could argue with a guard; there's no negotiating with a DROP rule

---

## 8. Certificate Authority Verification

### 🏠 Real-World Analogy
**Certificate Verification = Checking ID at a Government Office**

When someone shows you an ID badge:
1. **Look at the badge** (receive server certificate)
2. **Check who issued it** (identify Certificate Authority)
3. **Verify the issuer is trusted** (check CA against your trusted list)
4. **Confirm the badge matches the person** (hostname verification)
5. **Check expiration date** (certificate validity period)

If any step fails, you refuse entry.

### 🖼️ Visual Representation
```
    VERIFICATION PROCESS
    ════════════════════════════════════════════════════════════
    
    SERVER PRESENTS:
    ┌─────────────────────────────────────────────────────────┐
    │  CERTIFICATE                                            │
    │  ─────────────────────────────────────────────────────  │
    │  Subject: broker.local                                  │
    │  Issuer:  Week13 Lab CA                                │
    │  Valid:   2025-01-01 to 2026-01-01                     │
    │  Signature: [cryptographic signature]                   │
    └─────────────────────────────────────────────────────────┘
    
    CLIENT CHECKS:
    ┌─────────────────────────────────────────────────────────┐
    │  TRUSTED CA LIST (ca.crt)                              │
    │  ─────────────────────────────────────────────────────  │
    │  ✓ Week13 Lab CA                                       │
    │  ✓ Let's Encrypt                                       │
    │  ✓ DigiCert                                            │
    └─────────────────────────────────────────────────────────┘
    
    VERIFICATION:
    1. Is "Week13 Lab CA" in trusted list?  ✓ YES
    2. Does signature verify correctly?      ✓ YES  
    3. Is certificate still valid?           ✓ YES
    4. Does subject match hostname?          ✓ YES
    
    RESULT: ✅ TRUST ESTABLISHED
```

### 💻 Technical Reality
```python
import ssl

# Create context with trusted CAs
context = ssl.create_default_context()
context.load_verify_locations("docker/configs/certs/ca.crt")

# This will FAIL if certificate not signed by our CA
try:
    secure_sock = context.wrap_socket(sock, server_hostname="broker.local")
    print("Certificate verified!")
except ssl.SSLCertVerificationError as e:
    print(f"Certificate verification FAILED: {e}")
```

### ⚠️ Where the Analogy Breaks Down
- ID badges can be forged convincingly; cryptographic signatures cannot (practically)
- Humans verify IDs visually; computers verify mathematically
- Government IDs expire in years; certificates often expire in months

---

## Summary: From Concrete to Abstract

| Concept | Concrete (Analogy) | Abstract (Technical) |
|---------|-------------------|---------------------|
| MQTT Broker | Post office sorting centre | Message routing server |
| QoS Levels | Shipping options | Delivery guarantee protocol |
| Port Scanning | Checking doors | TCP connect attempts |
| TLS Handshake | Secure building entry | Cryptographic negotiation |
| Topic Wildcards | Mail forwarding rules | Pattern matching syntax |
| Vulnerability Scanning | Home security inspection | Automated security assessment |
| Filtered Port | Silent security guard | Firewall DROP rule |
| Certificate Verification | Checking ID at government office | X.509 chain validation |

---

*Computer Networks — Week 13: IoT and Security*
*ASE Bucharest, CSIE | by ing. dr. Antonio Clim*
