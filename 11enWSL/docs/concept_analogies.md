# 🎯 Concept Analogies — Week 11: Application Protocols & Load Balancing
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> Understanding through everyday analogies before technical details.
> This document uses the **CPA Method** (Concrete → Pictorial → Abstract) to build intuition.

---

## Table of Contents

1. [Load Balancer](#1-load-balancer)
2. [Round-Robin Algorithm](#2-round-robin-algorithm)
3. [Least Connections Algorithm](#3-least-connections-algorithm)
4. [IP Hash (Session Affinity)](#4-ip-hash-session-affinity)
5. [Health Checks](#5-health-checks)
6. [DNS Cache](#6-dns-cache)
7. [DNS TTL](#7-dns-ttl)
8. [FTP Dual Connection](#8-ftp-dual-connection)
9. [SSH Tunnel](#9-ssh-tunnel)
10. [Reverse Proxy vs Load Balancer](#10-reverse-proxy-vs-load-balancer)
11. [Backend Pool](#11-backend-pool)
12. [Failover](#12-failover)

---

## 1. Load Balancer

### 🏠 Real-World Analogy

**Hotel Reception Desk**

Imagine a large hotel with multiple receptionists at the front desk. When guests arrive, a **head receptionist** (the load balancer) directs each guest to an available receptionist (backend server).

- The head receptionist does not check guests in personally
- They only decide WHO will handle each guest
- If one receptionist goes on break, guests are directed to others
- The head receptionist tracks which receptionists are busy

### 🖼️ Visual Representation

```
                    ┌─────────────────┐
    Guests          │ Head Receptionist│         Receptionists
   (Requests)       │ (Load Balancer) │          (Backends)
                    └────────┬────────┘
        │                    │
        ▼                    │
   ┌─────────┐              │         ┌─────────────┐
   │ Guest 1 │──────────────┼────────►│Receptionist1│
   └─────────┘              │         └─────────────┘
   ┌─────────┐              │         ┌─────────────┐
   │ Guest 2 │──────────────┼────────►│Receptionist2│
   └─────────┘              │         └─────────────┘
   ┌─────────┐              │         ┌─────────────┐
   │ Guest 3 │──────────────┼────────►│Receptionist3│
   └─────────┘              │         └─────────────┘
```

### 💻 Technical Reality

```nginx
upstream backend_pool {
    server web1:80;
    server web2:80;
    server web3:80;
}

server {
    location / {
        proxy_pass http://backend_pool;
    }
}
```

### ⚠️ Where the Analogy Breaks Down

- Hotel receptionists can refuse guests; backend servers typically cannot
- Network load balancers operate in milliseconds, not minutes
- A load balancer can handle thousands of "guests" per second

---

## 2. Round-Robin Algorithm

### 🏠 Real-World Analogy

**Dealing Cards in a Card Game**

When dealing cards, you give one card to each player in order, then repeat. Player 1, Player 2, Player 3, Player 1, Player 2, Player 3...

- Each player receives cards in turn
- No player is skipped (unless they leave the game)
- The order is predictable and fair

### 🖼️ Visual Representation

```
Request sequence:  1  2  3  4  5  6  7  8  9
                   │  │  │  │  │  │  │  │  │
                   ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼
Backend:          [A][B][C][A][B][C][A][B][C]

Distribution after 9 requests:
  Backend A: ███ (3 requests)
  Backend B: ███ (3 requests)
  Backend C: ███ (3 requests)
```

### 💻 Technical Reality

```python
next_backend = backends[counter % len(backends)]
counter += 1
```

### ⚠️ Where the Analogy Breaks Down

- Cards take equal time to deal; requests take varying time to process
- If one player is slow, round-robin does not adapt
- Real systems may have backends with different capacities

---

## 3. Least Connections Algorithm

### 🏠 Real-World Analogy

**Supermarket Checkout Queues**

Smart shoppers look for the checkout with the shortest queue. The "least connections" algorithm does the same—it sends new customers to the cashier with the fewest people currently being served.

- New customers go to the least busy cashier
- If a cashier finishes quickly, they get more customers
- Slow cashiers naturally receive fewer customers

### 🖼️ Visual Representation

```
Current state:
  Cashier A: ██████ (6 customers)
  Cashier B: ██     (2 customers)  ◄── Next customer goes here!
  Cashier C: ████   (4 customers)

After new customer arrives:
  Cashier A: ██████ (6 customers)
  Cashier B: ███    (3 customers)
  Cashier C: ████   (4 customers)
```

### 💻 Technical Reality

```nginx
upstream backend_pool {
    least_conn;
    server web1:80;
    server web2:80;
    server web3:80;
}
```

### ⚠️ Where the Analogy Breaks Down

- Supermarket queues are visible; connection counts require tracking overhead
- Customers can switch queues; HTTP requests cannot change backend mid-request

---

## 4. IP Hash (Session Affinity)

### 🏠 Real-World Analogy

**Postal Sorting by Postcode**

The postal service sorts letters by postcode. Letters with postcode 01XXXX always go to Sorting Centre A, 02XXXX to Centre B and so on. Your address determines your sorting centre.

- Same postcode = same sorting centre (consistent)
- You cannot choose your sorting centre
- If a sorting centre closes, postcodes are redistributed

### 🖼️ Visual Representation

```
IP Address          Hash            Backend
─────────────────────────────────────────────
192.168.1.10   ──►  hash=7  ──►   Backend A
192.168.1.25   ──►  hash=3  ──►   Backend B
192.168.1.10   ──►  hash=7  ──►   Backend A  (same IP = same backend)
10.0.0.50      ──►  hash=5  ──►   Backend C
```

### 💻 Technical Reality

```nginx
upstream backend_pool {
    ip_hash;
    server web1:80;
    server web2:80;
    server web3:80;
}
```

```python
backend_index = hash(client_ip) % len(backends)
```

### ⚠️ Where the Analogy Breaks Down

- Postcodes are permanent; IP addresses can change (DHCP, mobile networks)
- Adding/removing backends changes the hash distribution
- Does not guarantee session persistence if backend restarts

---

## 5. Health Checks

### 🏠 Real-World Analogy

**Doctor Checking Patient Vitals**

A doctor periodically checks patients' vital signs (pulse, temperature, blood pressure). If vitals are abnormal, the patient is flagged for attention.

**Passive checks:** The doctor only notices problems when the patient complains (reactive).
**Active checks:** The doctor visits patients regularly, even if they feel fine (proactive).

### 🖼️ Visual Representation

```
PASSIVE HEALTH CHECK (Nginx default):
─────────────────────────────────────
Time ──────────────────────────────────►
      Request 1    Request 2    Request 3
          │            │            │
          ▼            ▼            ▼
      [SUCCESS]    [SUCCESS]     [FAIL!]
                                    │
                                    └──► Backend marked DOWN
                                         (but Request 3 failed)

ACTIVE HEALTH CHECK:
────────────────────
Time ──────────────────────────────────►
      Probe 1      Probe 2      Probe 3
          │            │            │
          ▼            ▼            ▼
      [SUCCESS]    [SUCCESS]     [FAIL!]
                                    │
                                    └──► Backend marked DOWN
                                         (before any real request fails)
```

### 💻 Technical Reality

```nginx
# Passive (default)
upstream backend_pool {
    server web1:80 max_fails=3 fail_timeout=30s;
}

# Active (Nginx Plus or custom implementation)
health_check interval=5s fails=3 passes=2;
```

### ⚠️ Where the Analogy Breaks Down

- Doctors diagnose complex conditions; health checks are simple pass/fail
- Patients communicate symptoms; servers just respond or do not
- Health checks happen every few seconds, not daily

---

## 6. DNS Cache

### 🏠 Real-World Analogy

**Phone Contact List**

Instead of calling directory enquiries every time you want to reach a friend, you save their number in your phone contacts. Next time, you look up your saved contact instead of asking the operator.

- First lookup: ask the operator (DNS query)
- Save the number (cache the response)
- Future lookups: use saved contact (cache hit)
- Numbers can change; contacts become outdated

### 🖼️ Visual Representation

```
First query for "google.com":

[Your Computer] ──"google.com?"──► [DNS Server] ──► [Root] ──► [.com] ──► [Google]
                                                                              │
[Your Computer] ◄──"142.250.74.46"─────────────────────────────────────────────┘
       │
       └──► Save in cache: google.com = 142.250.74.46 (TTL: 300s)

Second query (within 300s):

[Your Computer] ──"google.com?"──► [Local Cache] ──► "142.250.74.46" ✓
                                   (No network query needed!)
```

### 💻 Technical Reality

```bash
# Check DNS cache on Linux
resolvectl statistics

# Query with caching resolver
dig google.com

# Query bypassing cache (direct to authoritative)
dig google.com @8.8.8.8 +norecurse
```

### ⚠️ Where the Analogy Breaks Down

- Phone numbers rarely change; IP addresses can change more frequently
- Multiple levels of caching exist (browser, OS, ISP resolver)
- ISPs may ignore TTL and cache longer

---

## 7. DNS TTL

### 🏠 Real-World Analogy

**Milk Expiration Date**

DNS TTL is like the "best before" date on milk. You can trust the milk is fresh until that date. After expiration, you should get fresh milk (re-query DNS).

- TTL 300 seconds = "trust this answer for 5 minutes"
- After TTL expires, the cached answer is stale
- Some people still use expired milk (ISPs ignoring TTL)

### 🖼️ Visual Representation

```
DNS Record: app.example.com  TTL=60  A  192.168.1.100

Timeline:
0s      60s     120s    180s
│       │       │       │
▼       ▼       ▼       ▼
[FRESH] [STALE] [STALE] [STALE]
        ↑
        └── Should re-query, but some resolvers don't!
```

### 💻 Technical Reality

```
; DNS Zone file
app.example.com.  60  IN  A  192.168.1.100
                  ↑
                  └── TTL in seconds
```

### ⚠️ Where the Analogy Breaks Down

- Milk visibly spoils; stale DNS answers may still work
- Short TTL = more DNS queries = higher load on DNS servers
- Milk cannot be "refreshed"; DNS records can be re-fetched

---

## 8. FTP Dual Connection

### 🏠 Real-World Analogy

**Phone Call + Courier Delivery**

Imagine ordering furniture by phone:

1. **Phone call (Control Connection):** You speak with the sales agent, browse the catalogue, place an order
2. **Courier delivery (Data Connection):** A separate van delivers the furniture to your door

The phone call stays open while you discuss options. The courier only arrives when there's something to deliver.

### 🖼️ Visual Representation

```
┌─────────────────────────────────────────────────────────────────┐
│  CONTROL CONNECTION (Port 21) — Always Open                     │
│  ═══════════════════════════════════════                       │
│  Client: "USER john"                                            │
│  Server: "331 Password required"                                │
│  Client: "PASS secret"                                          │
│  Server: "230 Login successful"                                 │
│  Client: "RETR document.pdf"                                    │
│  Server: "150 Opening data connection"                          │
├─────────────────────────────────────────────────────────────────┤
│  DATA CONNECTION (Ephemeral Port) — Opens for transfer          │
│  ═══════════════════════════════════════════                   │
│  [Binary data: document.pdf contents...]                        │
│  [Connection closes when transfer completes]                    │
└─────────────────────────────────────────────────────────────────┘
```

### 💻 Technical Reality

```bash
# FTP session showing both connections
ftp server.example.com
> USER john
> PASS secret
> PASV          # Request passive mode data connection
> RETR file.txt # Data flows on separate connection
```

### ⚠️ Where the Analogy Breaks Down

- Phone calls are bidirectional; FTP control is command-response
- Couriers are slow; FTP data connections are instant
- Multiple deliveries need multiple vans; FTP reuses connections

---

## 9. SSH Tunnel

### 🏠 Real-World Analogy

**Private Underground Tunnel**

Imagine a private tunnel connecting your house to a friend's house, passing under public streets. Anyone can see cars entering/exiting your house and your friend's house, but they cannot see what travels through the underground tunnel.

- The tunnel is encrypted (opaque to observers)
- Traffic inside is hidden from street-level observers
- BUT: once traffic exits the tunnel, it's visible again

### 🖼️ Visual Representation

```
[Your Laptop]                                              [Internal Server]
     │                                                            ▲
     │ (visible: "going to jump host")                            │
     ▼                                                            │
┌─────────══════════════════════════════════════════─────────┐   │
│            SSH TUNNEL (ENCRYPTED)                           │   │
│  [localhost:8080] ════════════════════► [jumphost:22]       │   │
└─────────══════════════════════════════════════════─────────┘   │
                                               │                  │
                                               │ (PLAINTEXT!)     │
                                               └──────────────────┘
                                                "jumphost → internal:80"
```

### 💻 Technical Reality

```bash
# Local port forwarding
ssh -L 8080:internal-server:80 user@jumphost

# Now access internal server via localhost:8080
curl http://localhost:8080/
```

### ⚠️ Where the Analogy Breaks Down

- Physical tunnels have capacity limits; SSH can multiplex many channels
- Tunnel construction is instant; no digging required
- The "last mile" (jumphost → destination) is NOT protected by SSH

---

## 10. Reverse Proxy vs Load Balancer

### 🏠 Real-World Analogy

**Receptionist vs Traffic Controller**

**Reverse Proxy (Receptionist):**
- Sits between visitors and the office
- Screens visitors, announces them, maybe serves coffee
- Does not necessarily distribute visitors

**Load Balancer (Traffic Controller):**
- Directs traffic to multiple destinations
- Primary goal: distribute load evenly
- May not add extra services

A load balancer is usually implemented AS a reverse proxy, but a reverse proxy does not always balance load.

### 🖼️ Visual Representation

```
REVERSE PROXY (single backend):
────────────────────────────────
[Client] ──► [Reverse Proxy] ──► [Backend]
              │
              ├── SSL termination
              ├── Caching
              ├── Compression
              └── Security filtering

LOAD BALANCER (multiple backends):
──────────────────────────────────
[Client] ──► [Load Balancer] ──┬──► [Backend 1]
                               ├──► [Backend 2]
                               └──► [Backend 3]
```

### 💻 Technical Reality

```nginx
# Reverse proxy (single backend)
location / {
    proxy_pass http://single-backend:80;
}

# Load balancer (multiple backends)
upstream pool {
    server backend1:80;
    server backend2:80;
}
location / {
    proxy_pass http://pool;
}
```

### ⚠️ Where the Analogy Breaks Down

- Nginx can do both simultaneously
- Modern load balancers include reverse proxy features
- The distinction is more about intent than implementation

---

## 11. Backend Pool

### 🏠 Real-World Analogy

**Team of Cashiers**

A backend pool is like having multiple cashiers at a store. Any cashier can serve any customer. The pool exists so that:

- If one cashier is busy, others can help
- If one cashier is sick, the store still operates
- During busy periods, all cashiers work simultaneously

### 🖼️ Visual Representation

```
┌─────────────────────────────────────┐
│         BACKEND POOL                │
│  ┌─────────┐ ┌─────────┐ ┌────────┐│
│  │Backend 1│ │Backend 2│ │Backend3││
│  │  :8081  │ │  :8082  │ │ :8083  ││
│  │ [READY] │ │ [READY] │ │ [BUSY] ││
│  └─────────┘ └─────────┘ └────────┘│
└─────────────────────────────────────┘
         ▲           ▲
         │           │
    Request 1   Request 2
```

### 💻 Technical Reality

```nginx
upstream backend_pool {
    server 192.168.1.10:8081;
    server 192.168.1.11:8082;
    server 192.168.1.12:8083;
}
```

### ⚠️ Where the Analogy Breaks Down

- Cashiers are human; backends are software instances
- Cashiers have shifts; backends can run 24/7
- Adding a cashier requires hiring; adding a backend requires seconds

---

## 12. Failover

### 🏠 Real-World Analogy

**Backup Generator**

When the main power fails, a backup generator kicks in automatically. You might notice a brief flicker, but service continues.

- Primary backend = main power
- Backup backend = generator
- Failover = automatic switch when primary fails

### 🖼️ Visual Representation

```
Normal operation:
─────────────────
[Request] ──► [Primary Backend ✓] ──► [Response]

After primary fails:
────────────────────
[Request] ──► [Primary Backend ✗] 
                    │
                    └──► FAILOVER ──► [Backup Backend ✓] ──► [Response]
                                        (brief delay)
```

### 💻 Technical Reality

```nginx
upstream backend_pool {
    server web1:80;              # Primary
    server web2:80 backup;       # Only used if web1 fails
}
```

### ⚠️ Where the Analogy Breaks Down

- Generators take seconds to start; backend failover is milliseconds
- Generators have fuel limits; backup backends can run indefinitely
- Power is one resource; backend failover can be per-request

---

## Quick Reference Table

| Concept | Analogy | Key Insight |
|---------|---------|-------------|
| Load Balancer | Hotel reception | Distributes, does not process |
| Round-Robin | Dealing cards | Fair, predictable, inflexible |
| Least Connections | Shortest queue | Adapts to processing speed |
| IP Hash | Postal sorting | Consistent but not persistent |
| Health Checks | Doctor visits | Passive = reactive, Active = proactive |
| DNS Cache | Phone contacts | Saves time, can become stale |
| DNS TTL | Milk expiration | Trust period, often ignored |
| FTP Dual Connection | Phone + courier | Control separate from data |
| SSH Tunnel | Underground passage | Encrypted middle, clear ends |
| Reverse Proxy | Receptionist | Screens and adds services |
| Backend Pool | Team of cashiers | Redundancy and scalability |
| Failover | Backup generator | Automatic switch on failure |

---

## Using These Analogies

**In lectures:** Start with the analogy, show the diagram, then introduce technical syntax.

**In troubleshooting:** "Remember, the load balancer is like the hotel receptionist—it only directs traffic. If guests are unhappy, the problem is probably with the receptionist it directed them to (the backend), not the head receptionist (load balancer)."

**In exams:** Use analogies to explain concepts, but always connect back to technical accuracy.

---

*NETWORKING class - ASE, Informatics | Computer Networks Laboratory*
*Week 11: Application Protocols — FTP, DNS, SSH and Load Balancing*
