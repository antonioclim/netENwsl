# 🎯 Concept Analogies — Week 7: Packet Interception, Filtering and Defensive Port Probing
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Understanding through everyday analogies before technical details.  
> Each concept follows the CPA progression: Concrete → Pictorial → Abstract

---

## Concept 1: Packet Capture

### 🏠 Real-World Analogy

**Packet capture is like a security camera at a building entrance.**

- The camera records everyone passing through (all packets on the interface)
- You can review footage later (read pcap files)
- You can filter footage by criteria: "show only people in red shirts" (BPF filters)
- The camera doesn't stop anyone — it just observes and records
- Recording takes storage space and processing power

| Camera Analogy | Packet Capture |
|----------------|----------------|
| Camera lens | Network interface |
| Recording | pcap file |
| Footage review | Wireshark analysis |
| Motion detection filter | BPF capture filter |
| Storage tape | Disk space |

### 🖼️ Visual Representation

```
                    NETWORK TRAFFIC FLOW
                           │
                           ▼
    ┌──────────────────────────────────────────────┐
    │            CAPTURE POINT (tcpdump)           │
    │  ┌────────────────────────────────────────┐  │
    │  │  📹 "Recording all packets..."         │  │
    │  │                                        │  │
    │  │  Filter: "port 9090"                   │  │
    │  │  ═══════════════════                   │  │
    │  │  ✓ TCP:9090 → record                   │  │
    │  │  ✗ TCP:80   → ignore                   │  │
    │  │  ✓ TCP:9090 → record                   │  │
    │  └────────────────────────────────────────┘  │
    │                     │                        │
    │                     ▼                        │
    │              ┌─────────────┐                 │
    │              │ capture.pcap│                 │
    │              │ (saved file)│                 │
    │              └─────────────┘                 │
    └──────────────────────────────────────────────┘
                           │
                           ▼
                    CONTINUES TO DESTINATION
```

### 💻 Technical Reality

```bash
# Start recording (capture)
sudo tcpdump -i eth0 -w capture.pcap port 9090

# Review recording (analysis)
wireshark capture.pcap
# Or
tshark -r capture.pcap -Y "tcp.port==9090"
```

### ⚠️ Where the Analogy Breaks Down

- Security cameras are passive; tcpdump can actually drop packets if the system can't keep up
- Cameras record continuously; captures often have filters and time limits
- Cameras don't need special permissions; packet capture requires root/admin access

---

## Concept 2: DROP vs REJECT

### 🏠 Real-World Analogy

**Firewall actions are like a nightclub bouncer's responses.**

| Bouncer Response | Firewall Action | What Happens |
|------------------|-----------------|--------------|
| "Sorry, you can't come in" | **REJECT** | Clear refusal, you know immediately |
| Completely ignores you | **DROP** | No response, you wait wondering |
| "Welcome, go ahead" | **ACCEPT** | Allowed through |

**REJECT** = The bouncer says "No entry" — you know to leave.  
**DROP** = The bouncer pretends you don't exist — you stand there confused, eventually give up.

### 🖼️ Visual Representation

```
CLIENT                    FIREWALL                    SERVER
  │                          │                          │
  │  "Can I connect?"        │                          │
  │  ────────────────────▶   │                          │
  │        (SYN)             │                          │
  │                          │                          │
  │                    ┌─────┴─────┐                    │
  │                    │  DECISION │                    │
  │                    └─────┬─────┘                    │
  │                          │                          │
  │    ╔═════════════════════╧═════════════════════╗   │
  │    ║                                           ║   │
  │    ▼                                           ▼   │
  │  REJECT                                      DROP  │
  │  ───────                                     ────  │
  │  ◀──────────────────                              │
  │  "No!" (RST/ICMP)        ┌─────────────────────┐  │
  │                          │ (nothing happens)   │  │
  │  Client knows            │ Client waits...     │  │
  │  immediately             │ ...and waits...     │  │
  │                          │ ...timeout!         │  │
  │                          └─────────────────────┘  │
```

### 💻 Technical Reality

```bash
# REJECT rule — sends RST or ICMP response
sudo iptables -A INPUT -p tcp --dport 9090 -j REJECT
# Client sees: "Connection refused" (immediate)

# DROP rule — silent discard
sudo iptables -A INPUT -p tcp --dport 9090 -j DROP
# Client sees: [timeout after N seconds]
```

### ⚠️ Where the Analogy Breaks Down

- Bouncers are visible; firewalls are often hidden
- Bouncers can explain why; REJECT just sends a code
- You can argue with a bouncer; you can't argue with a firewall

---

## Concept 3: Port States (Open/Closed/Filtered)

### 🏠 Real-World Analogy

**Port states are like calling a phone number.**

| Phone Call Result | Port State | What It Means |
|-------------------|------------|---------------|
| Someone answers | **Open** | Service is running and accepting connections |
| "Number not in service" tone | **Closed** | No service, but phone system works |
| No ring, no tone, nothing | **Filtered** | Something blocking the call entirely |

### 🖼️ Visual Representation

```
PORT PROBE RESULTS
══════════════════

OPEN (Port 9090)                 CLOSED (Port 9999)
────────────────                 ─────────────────
    Client                           Client
       │                                │
       │ SYN ──────▶ Server             │ SYN ──────▶ Server
       │                                │
       │ ◀────── SYN-ACK                │ ◀────── RST
       │                                │
       │ "Someone home!"                │ "Nobody here,
       │                                │  but house exists"


FILTERED (Port 8888)
────────────────────
    Client
       │
       │ SYN ──────▶ ??? (Firewall)
       │
       │            [silence]
       │
       │ ⏱️ ...waiting...
       │
       │ "Is anyone there?
       │  Did they get my message?
       │  Is the address wrong?"
```

### 💻 Technical Reality

```python
# Open: connect_ex returns 0
result = sock.connect_ex((host, 9090))  # result = 0

# Closed: connect_ex returns error code (e.g., 111 = ECONNREFUSED)
result = sock.connect_ex((host, 9999))  # result = 111

# Filtered: connect_ex times out
sock.settimeout(2.0)
result = sock.connect_ex((host, 8888))  # raises socket.timeout
```

### ⚠️ Where the Analogy Breaks Down

- Phone calls have one path; network packets can take multiple routes
- Phone "not in service" is permanent; ports can change state
- Phone system charges per call; port probes are essentially free

---

## Concept 4: TCP Three-Way Handshake

### 🏠 Real-World Analogy

**TCP handshake is like starting a phone conversation politely.**

1. **SYN** = "Hello, can you hear me?" (Caller initiates)
2. **SYN-ACK** = "Yes, I hear you. Can you hear me?" (Callee confirms and checks)
3. **ACK** = "Yes, I hear you too. Let's talk." (Caller confirms ready)

Only after these three exchanges can the actual conversation begin.

### 🖼️ Visual Representation

```
CLIENT                                              SERVER
  │                                                    │
  │  1. "Hello, can you hear me?"                      │
  │     ─────────────────────────────────────────▶     │
  │     [SYN] seq=100                                  │
  │                                                    │
  │  2. "Yes I hear you! Can you hear me?"             │
  │     ◀─────────────────────────────────────────     │
  │     [SYN-ACK] seq=300, ack=101                     │
  │                                                    │
  │  3. "Yes! Let's talk."                             │
  │     ─────────────────────────────────────────▶     │
  │     [ACK] seq=101, ack=301                         │
  │                                                    │
  │  ═══════════ CONNECTION ESTABLISHED ═══════════   │
  │                                                    │
  │  4. Now actual data can flow                       │
  │     ─────────────────────────────────────────▶     │
  │     [DATA] "Hello World"                           │
```

### 💻 Technical Reality

```bash
# Wireshark filter to see handshake
tcp.flags.syn == 1

# Frame 1: SYN (client → server)
# tcp.flags.syn=1, tcp.flags.ack=0

# Frame 2: SYN-ACK (server → client)  
# tcp.flags.syn=1, tcp.flags.ack=1

# Frame 3: ACK (client → server)
# tcp.flags.syn=0, tcp.flags.ack=1
```

### ⚠️ Where the Analogy Breaks Down

- Phone conversations don't have sequence numbers
- You can interrupt a phone call; TCP has strict rules about who can send when
- Hanging up a phone is instant; TCP close has its own handshake (FIN-ACK)

---

## Concept 5: Firewall Rules as a Checklist

### 🏠 Real-World Analogy

**Firewall rules are like an airport security checklist.**

Security checks each passenger against a list of rules, in order:
1. ✅ Pilot badge? → Let through immediately
2. ✅ Business class ticket? → Express lane
3. ❌ On no-fly list? → Reject
4. ❌ Carrying prohibited items? → Reject
5. ✅ Default: Regular security check

**Key insight:** Rules are checked in order. First match wins. More specific rules must come before general rules.

### 🖼️ Visual Representation

```
INCOMING PACKET
     │
     ▼
┌─────────────────────────────────────────┐
│ RULE 1: Is it TCP port 9090?            │
│         ──────────────────────          │
│         YES → ACCEPT ───────────────────┼───▶ ALLOWED
│         NO  → continue                  │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│ RULE 2: Is it TCP port 9091?            │
│         ──────────────────────          │
│         YES → REJECT ───────────────────┼───▶ BLOCKED (with RST)
│         NO  → continue                  │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│ RULE 3: Is it any TCP?                  │
│         ──────────────────              │
│         YES → DROP ─────────────────────┼───▶ BLOCKED (silent)
│         NO  → continue                  │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│ DEFAULT POLICY: ACCEPT                  │
│                 ──────                  │
└─────────────────────────────────────────┼───▶ ALLOWED
```

### 💻 Technical Reality

```bash
# Rules in order (specific → general)
sudo iptables -A INPUT -p tcp --dport 9090 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 9091 -j REJECT
sudo iptables -A INPUT -p tcp -j DROP

# Check rule order
sudo iptables -L INPUT -n --line-numbers
```

### ⚠️ Where the Analogy Breaks Down

- Airport security can use judgement; firewalls follow rules exactly
- Airport checks are slow; firewall rules execute in microseconds
- You can appeal airport decisions; you can't appeal to a firewall

---

## Summary: CPA Progression

| Concept | Concrete Analogy | Pictorial | Abstract |
|---------|------------------|-----------|----------|
| Packet Capture | Security camera | Traffic flow diagram | `tcpdump -w file.pcap` |
| DROP vs REJECT | Bouncer responses | Client-firewall-server diagram | `iptables -j DROP/REJECT` |
| Port States | Phone call results | SYN/RST/timeout diagram | `connect_ex()` return values |
| TCP Handshake | Phone greeting ritual | 3-packet sequence diagram | SYN, SYN-ACK, ACK flags |
| Firewall Rules | Airport security checklist | Rule chain flowchart | `iptables -A` rule order |

---

*Computer Networks — Week 7: Packet Interception, Filtering and Defensive Port Probing*  
*ASE Bucharest, CSIE | by ing. dr. Antonio Clim*
