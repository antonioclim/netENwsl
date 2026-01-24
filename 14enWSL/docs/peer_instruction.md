# 🗳️ Peer Instruction Questions — Week 14

> NETWORKING class — ASE, CSIE | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

---

## Peer Instruction Protocol (5 steps)

Each question follows **5 mandatory steps**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 1 (1 min)  │  Read the question and think individually               │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 2 (30 sec) │  Vote your answer (A/B/C/D) — no discussion!            │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 3 (2 min)  │  Discuss with your neighbour — convince them!           │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 4 (30 sec) │  Re-vote — you may change your answer                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  STEP 5 (2 min)  │  Instructor explains the correct answer                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Why this works:** Research shows that peer discussion improves understanding more than instructor explanation alone. When students with different answers discuss, they must articulate their reasoning, exposing and correcting misconceptions.

---

## Question 1: OSI Layer Identification

> 💭 **PREDICTION:** Before looking at the options, which layer do you think handles logical addressing?

### Scenario

You are debugging network connectivity between two containers. You run `ip addr` and see:

```
eth0: 172.20.0.2/24
```

You then run `ip neigh` and see:

```
172.20.0.1 dev eth0 lladdr 02:42:ac:14:00:01 REACHABLE
```

### Question

The IP address `172.20.0.2` operates at which OSI layer and the MAC address `02:42:ac:14:00:01` operates at which layer?

### Options

- **A)** IP at Layer 2, MAC at Layer 1 — *Misconception: confusing physical addressing with data link*
- **B)** IP at Layer 3, MAC at Layer 2 — **CORRECT**
- **C)** IP at Layer 4, MAC at Layer 3 — *Misconception: confusing transport ports with network addressing*
- **D)** Both operate at Layer 3 — *Misconception: treating all addresses as equivalent*

### Correct Answer

**B** — IP addresses provide logical addressing at the Network Layer (3), enabling routing between networks. MAC addresses provide physical addressing at the Data Link Layer (2), enabling communication within a local network segment. The `ip neigh` command shows the ARP cache, which maps Layer 3 addresses to Layer 2 addresses.

### Targeted Misconception

Students often confuse the roles of IP and MAC addresses, thinking they serve the same purpose or operate at the same layer. This question forces them to distinguish between logical (routable) and physical (local) addressing.

### Instructor Notes

- **Target accuracy:** 50-70% on first vote
- **Key concept:** Layer separation — each layer has distinct addressing
- **After discussion:** Show the encapsulation diagram: Data → Segment → Packet (IP) → Frame (MAC)
- **Demo command:** `docker exec client ip neigh show` to see ARP entries
- **Timing:** Present (1 min) → Vote (1 min) → Discuss (3 min) → Revote (30 sec) → Explain (2 min)

---

## Question 2: TCP Three-Way Handshake

> 💭 **PREDICTION:** How many packets are exchanged before data can be sent over TCP?

### Scenario

You capture traffic with Wireshark while a container connects to the load balancer:

```bash
docker exec client curl http://172.21.0.10:8080/
```

You filter by `tcp.flags.syn == 1` and see packets.

### Question

During TCP connection establishment, what is the correct sequence of flag combinations?

### Options

- **A)** SYN → ACK → SYN-ACK — *Misconception: wrong order, ACK cannot come before SYN-ACK*
- **B)** SYN → SYN-ACK → ACK — **CORRECT**
- **C)** SYN → SYN → ACK — *Misconception: thinking both sides send SYN separately*
- **D)** ACK → SYN-ACK → SYN — *Misconception: reversed sequence*

### Correct Answer

**B** — The TCP three-way handshake follows this sequence:
1. Client sends **SYN** (synchronise sequence number)
2. Server responds with **SYN-ACK** (synchronise + acknowledge)
3. Client sends **ACK** (acknowledge)

Only after this exchange can application data flow.

### Targeted Misconception

Students often think TCP connections are simpler (two packets) or confuse the combined SYN-ACK flag with separate packets. This question clarifies that SYN-ACK is a single packet with both flags set.

### Instructor Notes

- **Target accuracy:** 60-75% on first vote
- **Key concept:** Connection establishment requires three packets minimum
- **After discussion:** Show Wireshark capture with tcp.flags column visible
- **Wireshark filter:** `tcp.flags.syn == 1 && tcp.flags.ack == 0` for initial SYN only
- **Follow-up:** Ask "Why three packets? Why not two?" (Answer: to confirm both directions work)

---

## Question 3: Load Balancer Behaviour

> 💭 **PREDICTION:** If you send 4 requests to a round-robin load balancer with 2 backends, how will they be distributed?

### Scenario

The lab environment has this configuration:

```yaml
services:
  lb:
    # Round-robin load balancer
    # Backends: app1 (172.20.0.2), app2 (172.20.0.3)
```

You run:

```bash
for i in 1 2 3 4; do curl -s http://localhost:8080/ | grep "Backend"; done
```

### Question

With round-robin scheduling and both backends healthy, what output do you expect?

### Options

- **A)** All 4 requests go to app1 — *Misconception: thinking load balancer picks one server*
- **B)** Requests alternate: app1, app2, app1, app2 — **CORRECT**
- **C)** Random distribution, could be any pattern — *Misconception: confusing round-robin with random*
- **D)** First 2 to app1, next 2 to app2 — *Misconception: thinking load balancer batches requests*

### Correct Answer

**B** — Round-robin scheduling distributes requests in sequential order across all available backends. With two backends, requests alternate: 1→app1, 2→app2, 3→app1, 4→app2. This provides even distribution regardless of request timing.

### Targeted Misconception

Students often confuse round-robin (deterministic, sequential) with random load balancing, or think the load balancer might "stick" to one server. This question demonstrates the predictable nature of round-robin.

### Instructor Notes

- **Target accuracy:** 55-70% on first vote
- **Key concept:** Round-robin is deterministic and sequential
- **After discussion:** Run the actual command and show results
- **Extension:** Ask "What happens if app2 goes down?" (Answer: all requests go to app1)
- **Demo:** Stop app2 with `docker stop week14-app2-1` and repeat the test

---

## Question 4: Docker Port Mapping

> 💭 **PREDICTION:** When you access localhost:8080, where does the traffic actually go?

### Scenario

The docker-compose.yml contains:

```yaml
services:
  lb:
    ports:
      - "8080:80"
    networks:
      frontend_net:
        ipv4_address: 172.21.0.10
```

You access `http://localhost:8080` from Windows.

### Question

What is the complete path of this HTTP request?

### Options

- **A)** Windows → Container port 8080 — *Misconception: ignoring port mapping*
- **B)** Windows → WSL → Docker → Container port 80 — **CORRECT**
- **C)** Windows → Container port 80 directly — *Misconception: thinking containers are directly accessible*
- **D)** Windows → WSL port 8080 → Container port 8080 — *Misconception: same port throughout*

### Correct Answer

**B** — The request travels: Windows browser → WSL2 network → Docker Engine → Container's port 80. The `-p 8080:80` mapping means "host port 8080 forwards to container port 80". The container internally listens on port 80, but external access uses port 8080.

### Targeted Misconception

Students frequently confuse the host port (external, what you type in browser) with the container port (internal, what the service listens on). The colon in port mapping separates these: `HOST:CONTAINER`.

### Instructor Notes

- **Target accuracy:** 45-65% on first vote
- **Key concept:** Port mapping translates between external and internal ports
- **Memory aid:** "Left is outside, right is inside" (like reading direction)
- **After discussion:** Show `docker ps` output with PORTS column
- **Verification:** `docker exec lb netstat -tlnp` shows listening on port 80, not 8080

---

## Question 5: Container Networking

> 💭 **PREDICTION:** Can containers on different Docker networks communicate directly?

### Scenario

The lab has two networks:

```yaml
networks:
  frontend_net:
    ipam:
      config:
        - subnet: 172.21.0.0/24
  backend_net:
    ipam:
      config:
        - subnet: 172.20.0.0/24
```

The `client` container is only on `frontend_net`. The `app1` container is only on `backend_net`.

### Question

What happens when you run `docker exec client ping 172.20.0.2` (app1's IP)?

### Options

- **A)** Ping succeeds — containers can always reach each other — *Misconception: ignoring network isolation*
- **B)** Ping fails — no route between different Docker networks — **CORRECT**
- **C)** Ping succeeds but slowly — networks are bridged automatically — *Misconception: thinking Docker auto-bridges*
- **D)** Ping fails with "unknown host" — DNS issue — *Misconception: confusing routing with DNS*

### Correct Answer

**B** — Docker networks provide isolation by default. Containers on `frontend_net` cannot directly reach containers on `backend_net` unless a container (like the load balancer) is connected to both networks and acts as a gateway. This is intentional for security.

### Targeted Misconception

Students often assume all Docker containers can communicate with each other by default, not understanding that Docker networks provide isolation similar to VLANs. This question demonstrates that network boundaries matter.

### Instructor Notes

- **Target accuracy:** 40-60% on first vote
- **Key concept:** Docker networks isolate containers; multi-homed containers bridge networks
- **After discussion:** Draw the network topology showing lb connected to both networks
- **Demo:** Run the ping command to show "Network unreachable" error
- **Follow-up:** "How does client reach app1 then?" (Answer: through lb, which is on both networks)

---

## Summary: Misconceptions Targeted

| Question | Primary Misconception |
|----------|----------------------|
| Q1 | IP and MAC addresses serve the same purpose |
| Q2 | TCP connection is simpler than three-way handshake |
| Q3 | Round-robin is random or sticky |
| Q4 | Host port equals container port |
| Q5 | All containers can communicate regardless of network |

---

## Usage Guidelines

1. **Timing:** Allow 6-8 minutes per question (total: 30-40 minutes for all 5)
2. **Voting:** Use hand raising, coloured cards, or digital polling
3. **Discussion:** Encourage students to explain their reasoning, not just state answers
4. **Flexibility:** Skip questions if time is short; Q1, Q3, Q4 are highest priority
5. **Follow-up:** Reference these questions during hands-on exercises

---

*Document version: 2.0 | Week 14: Integrated Recap | January 2025*
