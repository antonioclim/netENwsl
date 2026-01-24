# 🗳️ Peer Instruction Questions — Week 1
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

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

---

## Question 1: Ping and Network Metrics

> 💭 **PREDICTION:** Before reading the scenario, what do you think `ping` measures?

### Scenario

You run the following command inside your lab container:

```bash
ping -c 4 8.8.8.8
```

The output shows:
```
64 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=12.3 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=117 time=11.8 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=117 time=12.1 ms
64 bytes from 8.8.8.8: icmp_seq=4 ttl=117 time=11.9 ms
```

### Question

What does the `time=12.3 ms` value represent?

### Options

- **A)** The download speed to Google's DNS server — *Misconception: confuses latency with bandwidth*
- **B)** The round-trip time (RTT) for the ICMP packet to reach the server and return — **CORRECT**
- **C)** The time it takes for the server to process the request — *Misconception: ignores network transit time*
- **D)** The maximum bandwidth available on this connection — *Misconception: confuses latency with throughput*

### Correct Answer

**B** — The `time` value in ping output represents the Round-Trip Time (RTT): the total time for an ICMP echo request packet to travel from your machine to the destination and for the echo reply to return. It measures latency, not bandwidth or processing time.

### Targeted Misconception

Many students confuse **latency** (how long a packet takes to travel) with **bandwidth** (how much data can flow per second). A connection can have low latency but low bandwidth (like a narrow pipe that's very short) or high latency but high bandwidth (like a wide pipe that's very long).

### Instructor Notes

- **Target accuracy:** 40-60% on first vote
- **Key concept:** Latency ≠ Bandwidth
- **After discussion:** Draw the pipe analogy — width (bandwidth) vs length (latency)
- **Timing:** Present (1 min) → Vote (1 min) → Discuss (3 min) → Revote (30 sec) → Explain (2 min)

---

## Question 2: TCP Three-Way Handshake

> 💭 **PREDICTION:** How many packets does TCP need to establish a connection?

### Scenario

You start a TCP server and client in separate terminals:

```bash
# Terminal 1 (Server)
nc -l -p 9090

# Terminal 2 (Client)  
nc localhost 9090
```

You capture the traffic with Wireshark and see packets with these flags:
```
Packet 1: [SYN]
Packet 2: [SYN, ACK]
Packet 3: [ACK]
```

### Question

After Packet 3 is received, what is the state of the TCP connection?

### Options

- **A)** The connection is half-open; only the client can send data — *Misconception: confuses with half-open scan*
- **B)** The connection is fully established; both sides can send data — **CORRECT**
- **C)** The connection requires one more ACK from the server to be complete — *Misconception: invents a fourth step*
- **D)** The client is connected but the server is still in LISTEN state — *Misconception: misunderstands state transitions*

### Correct Answer

**B** — After the three-way handshake completes (SYN → SYN-ACK → ACK), both endpoints transition to the ESTABLISHED state. This is a full-duplex connection where either side can send data immediately.

### Targeted Misconception

Students often think the three-way handshake is asymmetric or that additional packets are needed. The handshake is precisely three packets by design: it allows both sides to synchronise sequence numbers and confirm readiness with minimum overhead.

### Instructor Notes

- **Target accuracy:** 50-70% on first vote
- **Key concept:** Three-way handshake creates bidirectional connection
- **After discussion:** Show `ss -tn` output with ESTABLISHED state on both sides
- **Demonstration:** Have students run `ss -tn | grep 9090` during the exercise

---

## Question 3: Loopback Interface

> 💭 **PREDICTION:** What happens when you ping 127.0.0.1?

### Scenario

Inside your lab container, you run:

```bash
ping -c 1 127.0.0.1
```

And separately:

```bash
ping -c 1 localhost
```

Both commands succeed with similar RTT values (~0.04 ms).

### Question

What is the relationship between `127.0.0.1` and `localhost`?

### Options

- **A)** They are completely different addresses; localhost is your machine's hostname — *Misconception: confuses hostname with loopback*
- **B)** localhost resolves to 127.0.0.1; both refer to the loopback interface — **CORRECT**
- **C)** 127.0.0.1 is faster because it skips DNS resolution — *Misconception: true detail but wrong conclusion about relationship*
- **D)** localhost connects through the network card while 127.0.0.1 stays internal — *Misconception: reverses the truth*

### Correct Answer

**B** — `localhost` is a hostname that resolves to `127.0.0.1` (defined in `/etc/hosts`). Both refer to the loopback interface (`lo`), which is a virtual network interface that allows a machine to communicate with itself without using the physical network.

### Targeted Misconception

Students sometimes believe `localhost` and `127.0.0.1` behave differently or that one is "more local" than the other. In reality, `localhost` is simply a convenient name for the loopback address. The loopback interface never touches any physical network hardware.

### Instructor Notes

- **Target accuracy:** 60-80% on first vote (easier question)
- **Key concept:** Loopback interface for local testing
- **After discussion:** Show `/etc/hosts` content and `ip addr show lo`
- **Follow-up:** Ask what `127.0.0.2` would do (also loopback!)

---

## Question 4: Docker Container Networking

> 💭 **PREDICTION:** Can a Docker container access the host's localhost?

### Scenario

You have Portainer running on your host at `http://localhost:9000`. Inside the week1_lab container, you try:

```bash
docker exec -it week1_lab bash
curl http://localhost:9000
```

The connection fails with "Connection refused".

### Question

Why does `localhost` inside the container not reach Portainer on the host?

### Options

- **A)** Portainer is blocking connections from containers for security — *Misconception: assumes application-level blocking*
- **B)** Docker containers have their own network namespace; localhost refers to the container itself — **CORRECT**
- **C)** The container's firewall is blocking port 9000 — *Misconception: containers don't have firewalls by default*
- **D)** You need to use HTTPS instead of HTTP — *Misconception: confuses protocol with networking*

### Correct Answer

**B** — Docker containers run in isolated network namespaces. When you reference `localhost` or `127.0.0.1` inside a container, you're referring to the container's own loopback interface, not the host's. To reach host services, you need the host's IP or use special Docker networking (like `host.docker.internal` on some platforms).

### Targeted Misconception

The concept of network namespaces is fundamental to container isolation. Students often assume containers share the host's network stack. Understanding that each container has its own `localhost` is crucial for debugging connectivity issues.

### Instructor Notes

- **Target accuracy:** 30-50% on first vote (harder concept)
- **Key concept:** Network namespace isolation
- **After discussion:** Show `ip addr` inside container vs on host
- **Demonstration:** Compare `curl localhost:9000` from WSL vs from container

---

## Question 5: Socket States

> 💭 **PREDICTION:** What state is a server socket in before any client connects?

### Scenario

You start a TCP server:

```bash
nc -l -p 9090
```

Before any client connects, you check socket states:

```bash
ss -tlnp | grep 9090
```

Output:
```
LISTEN  0  1  0.0.0.0:9090  0.0.0.0:*  users:(("nc",pid=1234,fd=3))
```

### Question

What does the `LISTEN` state indicate?

### Options

- **A)** The server is actively sending data to connected clients — *Misconception: confuses LISTEN with ESTABLISHED*
- **B)** The server has bound to the port and is waiting for incoming connections — **CORRECT**
- **C)** The server is waiting for DNS resolution to complete — *Misconception: DNS is unrelated to socket states*
- **D)** The connection is half-closed and waiting for final ACK — *Misconception: describes TIME_WAIT or CLOSE_WAIT*

### Correct Answer

**B** — The LISTEN state indicates that a socket has been created, bound to an address/port and is now waiting to accept incoming connection requests. No data transfer occurs in this state; it's purely waiting for the SYN packet of a three-way handshake.

### Targeted Misconception

Students often confuse socket states with data transfer states. LISTEN is a passive state — the server is ready but not yet communicating. Only after `accept()` completes and a connection moves to ESTABLISHED can data flow.

### Instructor Notes

- **Target accuracy:** 50-70% on first vote
- **Key concept:** Socket lifecycle (bind → listen → accept → established)
- **After discussion:** Draw state diagram on board
- **Follow-up:** What state after client connects? (ESTABLISHED)

---

## Summary of Targeted Misconceptions

| Question | Primary Misconception |
|----------|----------------------|
| Q1 (Ping) | Confusing latency with bandwidth |
| Q2 (TCP Handshake) | Expecting more than 3 packets for connection |
| Q3 (Loopback) | Thinking localhost and 127.0.0.1 differ |
| Q4 (Docker Network) | Assuming containers share host's localhost |
| Q5 (Socket States) | Confusing LISTEN with active communication |

---

*NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim*
*Adapted for WSL2 + Ubuntu 22.04 + Docker + Portainer Environment*
