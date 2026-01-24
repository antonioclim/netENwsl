# 🎯 Concept Analogies — Week 6: NAT/PAT & SDN

## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Understanding through everyday analogies before technical details. Each concept follows the Concrete → Pictorial → Abstract progression.

---

## Concept 1: NAT (Network Address Translation)

### 🏠 Real-World Analogy: Hotel Reception Desk

Imagine a large hotel where guests stay in numbered rooms. The hotel has one public phone number (the reception), but many internal room extensions.

- **External caller** dials the hotel's public number
- **Reception** (NAT router) answers and asks "Which guest?"
- **Reception** connects the call to the correct room extension
- **Guest** picks up — they don't need their own public phone number

When a guest calls out:
- **Guest** dials from room 203
- **Reception** routes the call through the hotel's main line
- **Outside party** sees the hotel's caller ID, not room 203's extension
- **Return calls** come to the hotel and reception routes them to room 203

### 🖼️ Visual Representation

```
HOTEL (NAT Router)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                                                      
  Room 101 ─┐                     ┌─ Public Phone
  (Private) │      ┌─────────┐   │  Number
            ├─────▶│Reception│───┤  555-1234
  Room 203 ─┤      │ (NAT)   │   │  (Public IP)
  (Private) │      └─────────┘   │
            │                     │
  Room 456 ─┘                     └─▶ Outside World

Guest in 101 calls out → Reception connects → Outside sees 555-1234
Outside calls 555-1234 → Reception → "Room 203 please" → Connected
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 💻 Technical Reality

```
Private Network                NAT Router               Internet
192.168.1.0/24                203.0.113.1              

  h1 (192.168.1.10) ─┐         ┌─────────┐
                     ├────────▶│ Conntrack│─────────▶ 8.8.8.8
  h2 (192.168.1.20) ─┤         │  Table   │
                     │         └─────────┘
  h3 (192.168.1.30) ─┘         
                               
Outbound: 192.168.1.10:45678 → [NAT] → 203.0.113.1:50001 → 8.8.8.8:443
Return:   8.8.8.8:443 → 203.0.113.1:50001 → [NAT] → 192.168.1.10:45678
```

### ⚠️ Where the Analogy Breaks Down

| Hotel | NAT |
|-------|-----|
| Reception can announce visitors | NAT blocks unsolicited inbound by default |
| Room numbers are fixed | Port mappings are dynamic and expire |
| One call per room at a time | Many connections per host simultaneously |
| Reception knows guest names | NAT only tracks IP:port tuples |

---

## Concept 2: PAT (Port Address Translation)

### 🏠 Real-World Analogy: Apartment Building Intercom

An apartment building has one street address (123 Main St) but many units. The intercom system uses unit numbers to route visitors.

- **Building address**: 123 Main St (public IP)
- **Unit numbers**: #101, #203, #456 (translated ports)
- **Residents**: Can all receive deliveries at the same street address
- **Delivery person**: Sees building address + unit number

When multiple residents order pizza:
- All orders go out from "123 Main St"
- Each order has a unique unit number attached
- Delivery person brings pizza to the right unit
- The building manages which unit gets which delivery

### 🖼️ Visual Representation

```
APARTMENT BUILDING (PAT Router with single public IP)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                     ┌────────────────────────────────────┐
  Apt 101 ──────────▶│                                    │
  (192.168.1.10)     │         Building Address           │
                     │         123 Main St                │──▶ Pizza Shop
  Apt 203 ──────────▶│         (203.0.113.1)              │
  (192.168.1.20)     │                                    │
                     │  ┌──────────────────────────────┐  │
  Apt 456 ──────────▶│  │ Delivery Log (Conntrack)     │  │
  (192.168.1.30)     │  │ Apt 101 → Unit #50001        │  │
                     │  │ Apt 203 → Unit #50002        │  │
                     │  │ Apt 456 → Unit #50003        │  │
                     │  └──────────────────────────────┘  │
                     └────────────────────────────────────┘

Pizza shop sees: 123 Main St Unit #50001, #50002, #50003
                 (same address, different unit numbers)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 💻 Technical Reality

```bash
# Multiple internal hosts sharing one public IP via port multiplexing

Conntrack table:
┌─────────────────────────────────────────────────────────────────────┐
│ Internal             External              Remote                   │
├─────────────────────────────────────────────────────────────────────┤
│ 192.168.1.10:45678 → 203.0.113.1:50001 ↔ 8.8.8.8:443              │
│ 192.168.1.20:45678 → 203.0.113.1:50002 ↔ 8.8.8.8:443              │
│ 192.168.1.30:12345 → 203.0.113.1:50003 ↔ 8.8.8.8:80               │
└─────────────────────────────────────────────────────────────────────┘

Note: Both .10 and .20 use internal port 45678, but get different external ports!
```

### ⚠️ Where the Analogy Breaks Down

| Apartment | PAT |
|-----------|-----|
| Unit numbers are permanent | Translated ports are temporary |
| Limited units per building | Thousands of ports available (1-65535) |
| Physical delivery required | Packets routed electronically |
| Building intercom is manual | Translation is automatic and instant |

---

## Concept 3: SDN Controller

### 🏠 Real-World Analogy: Air Traffic Control Tower

An airport has runways (switches) where planes (packets) land and take off. The control tower (controller) decides which runway each plane uses, but the tower doesn't carry the planes — the runways do.

- **Control tower**: Makes decisions, gives instructions
- **Runways**: Execute landing/takeoff (forward packets)
- **Planes**: Follow assigned runway (flow rules)
- **Tower doesn't physically move planes** — it just tells them where to go

When a new plane approaches:
1. **Pilot contacts tower** (packet-in)
2. **Tower decides** which runway to use (policy)
3. **Tower instructs pilot** (flow-mod)
4. **Plane lands on assigned runway** (forwarding)
5. **Similar planes follow same instructions** (flow table)

### 🖼️ Visual Representation

```
AIRPORT (SDN Network)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

          ┌─────────────────────────────────┐
          │      AIR TRAFFIC CONTROL        │
          │         (SDN Controller)        │
          │                                 │
          │  "Flight 123, use Runway 2"     │
          │  "Flight 456, use Runway 1"     │
          │  "Flight 789, hold - blocked"   │
          └────────────────┬────────────────┘
                           │ Instructions (OpenFlow)
                           ▼
          ┌─────────────────────────────────┐
          │      RUNWAY SYSTEM (Switch)     │
          │  ┌───────────────────────────┐  │
          │  │ Flight Rules (Flow Table) │  │
          │  │ • Flight 123 → Runway 2   │  │
          │  │ • Flight 456 → Runway 1   │  │
          │  │ • Flight 789 → Denied     │  │
          │  └───────────────────────────┘  │
          └─────────────────────────────────┘
                    │         │
           ┌────────┘         └────────┐
           ▼                           ▼
      ✈️ Runway 1                 ✈️ Runway 2
      (Port 1)                   (Port 2)

Tower decides → Runways execute → Planes follow rules
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 💻 Technical Reality

```
SDN Architecture:
┌─────────────────────────────────────────────────────────────────────┐
│                        CONTROL PLANE                                │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    SDN Controller (OS-Ken)                    │  │
│  │  • Receives packet-in from switches                          │  │
│  │  • Computes forwarding decisions                             │  │
│  │  • Installs flows via flow-mod                               │  │
│  │  • Does NOT forward packets itself                           │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────────┬────────────────────────────────────┘
                                 │ OpenFlow Protocol
┌────────────────────────────────▼────────────────────────────────────┐
│                         DATA PLANE                                  │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    OVS Switch (s1)                            │  │
│  │  • Matches packets against flow table                        │  │
│  │  • Executes actions (forward, drop, modify)                  │  │
│  │  • Operates at line rate                                     │  │
│  │  • Forwards millions of packets per second                   │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

### ⚠️ Where the Analogy Breaks Down

| Air Traffic Control | SDN Controller |
|---------------------|----------------|
| Constant communication | First packet only, then rules apply |
| One plane per runway at a time | Millions of packets simultaneously |
| Tower can see all planes | Controller only sees what switches report |
| Emergencies override rules | Priority system, but no real "emergency" mode |

---

## Concept 4: Flow Table

### 🏠 Real-World Analogy: Restaurant Order Tickets

A restaurant kitchen receives order tickets that tell the chef what to cook and where to send it.

- **Order ticket** = Flow entry
- **Customer description** = Match fields (table 5, wants steak)
- **Cooking instructions** = Actions (grill medium-rare, send to table 5)
- **Order priority** = Priority (VIP orders first)
- **Order expiry** = Timeout (stale orders discarded)

Kitchen workflow:
1. **New order arrives** matching no existing ticket → ask manager (controller)
2. **Manager writes ticket** with instructions
3. **Similar orders** follow the same ticket
4. **Ticket counters** track how many meals served

### 🖼️ Visual Representation

```
RESTAURANT KITCHEN (SDN Switch)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   ORDER TICKET BOARD (Flow Table)
   ┌────────────────────────────────────────────────────────┐
   │ Priority │ Match (Who/What)      │ Action   │ Count   │
   ├──────────┼───────────────────────┼──────────┼─────────┤
   │   100    │ VIP + Steak           │ Chef A   │   15    │
   │    50    │ Table 5 + Any         │ Chef B   │   42    │
   │    10    │ Any + Soup            │ Chef C   │  108    │
   │     0    │ Unknown order         │ Ask Mgr  │   23    │
   └────────────────────────────────────────────────────────┘
   
   New order: "Table 5, Steak" → Matches row 2 → Chef B handles it
   New order: "VIP, Steak"     → Matches row 1 (higher priority!) → Chef A
   New order: "Table 9, Pizza" → No match → Ask Manager (packet-in)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 💻 Technical Reality

```bash
# ovs-ofctl -O OpenFlow13 dump-flows s1

cookie=0x0, duration=300s, table=0, n_packets=150, n_bytes=12600,
    priority=100, ip, nw_src=10.0.6.11, nw_dst=10.0.6.12
    actions=output:2

cookie=0x0, duration=300s, table=0, n_packets=45, n_bytes=3780,
    priority=50, ip, nw_dst=10.0.6.13
    actions=drop

cookie=0x0, duration=300s, table=0, n_packets=23, n_bytes=1932,
    priority=0
    actions=CONTROLLER:65535

# Match fields = What to look for
# Actions = What to do
# n_packets = How many matched
# priority = Check order (higher first)
```

### ⚠️ Where the Analogy Breaks Down

| Restaurant Tickets | Flow Table |
|--------------------|------------|
| Human reads tickets | Hardware/software matching |
| One order at a time | Millions of matches per second |
| Tickets are paper | Entries in TCAM memory |
| Flexible interpretation | Exact binary matching |

---

## Concept 5: OpenFlow Protocol

### 🏠 Real-World Analogy: Waiter Communication System

A restaurant uses a specific communication protocol between waiters (switches) and the manager (controller).

- **"I don't know this order"** = Packet-in (table-miss)
- **"Here's how to handle it"** = Flow-mod (install rule)
- **"Send this dish to table 5"** = Packet-out (specific action)
- **"How many orders today?"** = Stats request/reply

The protocol ensures everyone speaks the same language, regardless of which waiter or manager is working.

### 🖼️ Visual Representation

```
WAITER-MANAGER PROTOCOL (OpenFlow)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   MANAGER (Controller)              WAITER (Switch)
   ┌─────────────────┐               ┌─────────────────┐
   │                 │               │                 │
   │  "Handle VIP    │◀─ Packet-In ──│  "Unknown order │
   │   orders with   │   (question)  │   from VIP..."  │
   │   priority..."  │               │                 │
   │                 │── Flow-Mod ──▶│  "Got it, I'll  │
   │                 │   (answer)    │   remember"     │
   │                 │               │                 │
   │  "Send this to  │── Packet-Out─▶│  "Delivering    │
   │   table 5 now"  │   (command)   │   now..."       │
   │                 │               │                 │
   │  "How many      │── Stats-Req ─▶│                 │
   │   orders?"      │               │                 │
   │                 │◀─ Stats-Rep ──│  "42 orders     │
   │                 │               │   served"       │
   └─────────────────┘               └─────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 💻 Technical Reality

```
OpenFlow Message Types (Version 1.3):
┌─────────────────┬────────────────────────────────────────────────┐
│ Message         │ Purpose                                        │
├─────────────────┼────────────────────────────────────────────────┤
│ PACKET_IN       │ Switch → Controller: "Unknown packet"          │
│ FLOW_MOD        │ Controller → Switch: "Add/modify/delete flow"  │
│ PACKET_OUT      │ Controller → Switch: "Send this packet out"    │
│ STATS_REQUEST   │ Controller → Switch: "Give me statistics"      │
│ STATS_REPLY     │ Switch → Controller: "Here are the stats"      │
│ FEATURES_REQUEST│ Controller → Switch: "What can you do?"        │
│ FEATURES_REPLY  │ Switch → Controller: "I support these features"│
└─────────────────┴────────────────────────────────────────────────┘

# Capture OpenFlow traffic:
tshark -i lo -f "port 6633" -Y "openflow_v4"
```

### ⚠️ Where the Analogy Breaks Down

| Waiter Protocol | OpenFlow |
|-----------------|----------|
| Natural language | Binary protocol with strict format |
| Interpretation allowed | Exact semantics defined in spec |
| Verbal communication | TCP connection (reliable) |
| One conversation at a time | Asynchronous messages |

---

## Summary: From Concrete to Abstract

| Concept | Concrete Analogy | Key Insight |
|---------|------------------|-------------|
| NAT | Hotel reception | One public identity, many private rooms |
| PAT | Apartment intercom | Same address, different unit numbers |
| SDN Controller | Air traffic control | Decides but doesn't execute |
| Flow Table | Restaurant tickets | Match → Action, with priority |
| OpenFlow | Waiter protocol | Standardised communication |

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
