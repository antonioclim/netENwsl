# 🗳️ Peer Instruction Questions — Week 2: Sockets and Transport Protocols

> NETWORKING class — ASE, CSIE Bucharest  
> Computer Networks Laboratory | by ing. dr. Antonio Clim

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

## ⏱️ Session Timing Guide

| Activity | Duration | Cumulative |
|----------|----------|------------|
| Introduction and protocol explanation | 3 min | 3 min |
| Question 1 (TCP boundaries) | 6 min | 9 min |
| Question 2 (UDP bidirectional) | 6 min | 15 min |
| Question 3 (Bind address) | 6 min | 21 min |
| Question 4 (Handshake frequency) | 6 min | 27 min |
| Question 5 (Threading) | 6 min | 33 min |
| Summary and bonus discussion | 5-10 min | 38-43 min |

**Total session time:** 35-45 minutes

**Tip:** If short on time, prioritise Q1, Q3 and Q5 — these target the most common misconceptions.

---

## 🎯 Facilitator Discussion Prompts

Use these prompts to guide peer discussions when students seem stuck:

| Question | If discussion stalls, ask... |
|----------|------------------------------|
| Q1 | "What does 'stream' mean in SOCK_STREAM?" |
| Q2 | "What information does recvfrom() return besides data?" |
| Q3 | "What's the difference between a network interface and an IP address?" |
| Q4 | "When you make a phone call, do you dial every time you speak?" |
| Q5 | "If you have 10 cashiers vs 1 cashier, how does queue time change?" |

---

## Question 1: TCP Message Boundaries

| Difficulty | ★★☆ Moderate | Bloom Level | UNDERSTAND |
|------------|--------------|-------------|------------|

> 💭 **PREDICTION:** Before looking at the options, predict: if a TCP server sends two messages quickly, how will the client receive them?

### Scenario

A TCP server executes this code:
```python
conn.send(b"Hello")
conn.send(b"World")
```

The client then calls:
```python
data = sock.recv(1024)
print(data)
```

### Question

What will the client print?

### Options

- **A)** Always `b"Hello"` — TCP delivers messages one at a time
- **B)** Always `b"HelloWorld"` — TCP concatenates all data
- **C)** Could be `b"Hello"`, `b"HelloWorld"`, `b"Hel"`, or other variations
- **D)** An error — you cannot call send() twice without recv() between

### Correct Answer

**C** — TCP is a byte stream protocol with no message boundaries. The operating system buffers data and recv() returns whatever bytes are available (up to buffer size). Nagle's algorithm, network timing and OS scheduling all affect how bytes are grouped.

### Targeted Misconception

Many students assume TCP preserves application-level message boundaries like UDP does. This misconception leads to bugs when parsing protocols.

### Instructor Notes

- **Target accuracy:** 40-50% on first vote
- **Key concept:** TCP stream vs message semantics
- **After discussion:** Show Wireshark capture where segments don't align with send() calls

### Follow-up Activity

**Pair exercise (5 min):** Modify the server to send a 4-byte length prefix before each message. Have students implement the client-side framing logic.

```python
# Hint: Server sends length + data
import struct
length = struct.pack(">I", len(message))
conn.send(length + message)
```

---

## Question 2: UDP Socket Communication

| Difficulty | ★☆☆ Easy | Bloom Level | UNDERSTAND |
|------------|----------|-------------|------------|

> 💭 **PREDICTION:** Can a UDP client receive a response from the server using the same socket it used to send?

### Scenario

```python
# UDP Client
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(b"ping", ("127.0.0.1", 9091))
# What happens next?
```

### Question

Can this UDP client receive a response from the server?

### Options

- **A)** No — UDP is send-only; you need a separate socket to receive
- **B)** No — UDP is connectionless, so the server cannot reply
- **C)** Yes — call `sock.recvfrom(1024)` on the same socket
- **D)** Yes — but only if you call `sock.connect()` first

### Correct Answer

**C** — The same UDP socket can both send and receive. "Connectionless" means no handshake is required, not that communication is one-way.

### Targeted Misconception

Students confuse "connectionless" with "one-way" or think separate sockets are needed for bidirectional UDP communication.

### Instructor Notes

- **Target accuracy:** 50-60% on first vote
- **Key concept:** Connectionless ≠ unidirectional
- **After discussion:** Show that recvfrom() returns both data AND sender address

### Follow-up Activity

**Quick demo (3 min):** Run the UDP exercise and observe the client receiving replies. Point out that recvfrom() returns `(data, (ip, port))` — the server knows where to reply because the client's address is in the UDP header.

---

## Question 3: Server Binding Address

| Difficulty | ★★☆ Moderate | Bloom Level | APPLY |
|------------|--------------|-------------|-------|

> 💭 **PREDICTION:** You bind a server to 127.0.0.1:9090. A colleague tries to connect from their laptop. What happens?

### Scenario

Your server code:
```python
sock.bind(("127.0.0.1", 9090))
sock.listen(5)
print("Server running on 127.0.0.1:9090")
```

Your colleague (IP: 192.168.1.50) runs:
```python
client_sock.connect(("192.168.1.100", 9090))  # Your machine's IP
```

### Question

What happens when your colleague tries to connect?

### Options

- **A)** Connection succeeds — 127.0.0.1 means "this machine"
- **B)** Connection refused — server only accepts connections on loopback
- **C)** Connection times out — packets are lost in transit
- **D)** Error on server — cannot bind to 127.0.0.1

### Correct Answer

**B** — Binding to 127.0.0.1 means the server only accepts connections arriving on the loopback interface. External connections arrive on the network interface (e.g., eth0) with destination 192.168.1.100, which doesn't match.

### Targeted Misconception

Students think 127.0.0.1 means "this computer" rather than specifically "the loopback interface only."

### Instructor Notes

- **Target accuracy:** 40-50% on first vote
- **Key concept:** Bind address = which interface to listen on
- **After discussion:** Show `ss -tlnp` output comparing 127.0.0.1 vs 0.0.0.0 bindings
- **Fix:** Use `0.0.0.0` to accept connections on all interfaces

### Follow-up Activity

**Verification exercise (5 min):** Have students:
1. Start server bound to `127.0.0.1:9090`
2. Connect from same machine — succeeds
3. Try `docker exec` from container — fails
4. Rebind to `0.0.0.0:9090` — container connection succeeds

---

## Question 4: TCP Handshake Frequency

| Difficulty | ★☆☆ Easy | Bloom Level | REMEMBER |
|------------|----------|-------------|----------|

> 💭 **PREDICTION:** How many three-way handshakes occur when a client connects, sends 10 messages and disconnects?

### Scenario

```python
# Client code
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 9090))  # Handshake here?

for i in range(10):
    sock.send(f"Message {i}".encode())  # Handshake here?
    response = sock.recv(1024)

sock.close()  # Handshake here?
```

### Question

How many three-way handshakes (SYN → SYN-ACK → ACK) occur?

### Options

- **A)** 1 — handshake only at connect()
- **B)** 10 — one per send() call
- **C)** 11 — one at connect(), one per send()
- **D)** 12 — one at connect(), one per send(), one at close()

### Correct Answer

**A** — The TCP handshake occurs only once, when connect() is called. The connection then remains open for all subsequent send()/recv() calls. Closing uses a separate sequence (FIN → ACK → FIN → ACK) which is not a "handshake."

### Targeted Misconception

Students sometimes think each message requires a new handshake, confusing TCP connections with HTTP/1.0 request-response (where connections were often closed between requests).

### Instructor Notes

- **Target accuracy:** 60-70% on first vote (easier question)
- **Key concept:** Connection state persists across messages
- **After discussion:** Show Wireshark capture of full conversation — one handshake, many data segments

### Follow-up Activity

**Wireshark exercise (5 min):** Capture traffic while running the TCP exercise. Count:
- How many SYN packets? (should be 1)
- How many data packets? (depends on message count and TCP buffering)
- How many FIN packets? (should be 2 — one from each side)

---

## Question 5: Threaded vs Iterative Server

| Difficulty | ★★★ Hard | Bloom Level | ANALYSE |
|------------|----------|-------------|---------|

> 💭 **PREDICTION:** You have 10 clients connecting simultaneously. Each request takes 100ms to process. How does total time differ between server designs?

### Scenario

```python
# ITERATIVE SERVER
while True:
    conn, addr = sock.accept()
    handle_client(conn)  # Takes 100ms, blocks accept()

# THREADED SERVER
while True:
    conn, addr = sock.accept()
    Thread(target=handle_client, args=(conn,)).start()  # Returns immediately
```

10 clients connect at the exact same moment (t=0).

### Question

What is the total time until ALL clients receive responses?

### Options

- **A)** Iterative: 100ms, Threaded: 100ms — same work, same time
- **B)** Iterative: 1000ms, Threaded: ~100ms
- **C)** Iterative: 1000ms, Threaded: ~1000ms — threading has overhead
- **D)** Iterative: 100ms, Threaded: ~1000ms — thread creation is slow

### Correct Answer

**B** — The iterative server processes clients sequentially: client 1 at 0-100ms, client 2 at 100-200ms, ..., client 10 at 900-1000ms. Total: 1000ms. The threaded server processes all 10 in parallel: all complete around 100ms (plus small thread overhead).

### Targeted Misconception

Some students don't grasp that iterative servers serialize all requests, making them unsuitable for concurrent workloads. Others overestimate threading overhead.

### Instructor Notes

- **Target accuracy:** 40-50% on first vote
- **Key concept:** Parallelism enables concurrent processing
- **After discussion:** Run `ex_2_01_tcp.py load --clients 10` with both modes, show timing
- **Nuance:** Threading has limits (memory, context switching) — discuss thread pools

### Follow-up Activity

**Benchmarking exercise (10 min):**
```bash
# Start iterative server
python ex_2_01_tcp.py server --port 9090 --mode iterative &

# Run load test, note total time
time python ex_2_01_tcp.py load --port 9090 --clients 10

# Restart as threaded
python ex_2_01_tcp.py server --port 9090 --mode threaded &

# Compare
time python ex_2_01_tcp.py load --port 9090 --clients 10
```

**Discussion:** What happens with 1000 clients? When might iterative be better?

---

## Summary Table

| Q# | Topic | Difficulty | Bloom | Misconception Targeted |
|----|-------|------------|-------|------------------------|
| Q1 | TCP message boundaries | ★★☆ | UNDERSTAND | "TCP preserves message boundaries" |
| Q2 | UDP bidirectional | ★☆☆ | UNDERSTAND | "UDP is send-only" |
| Q3 | Bind address | ★★☆ | APPLY | "127.0.0.1 means this machine" |
| Q4 | Handshake frequency | ★☆☆ | REMEMBER | "Handshake per message" |
| Q5 | Threading benefits | ★★★ | ANALYSE | "Iterative is simpler so equally fast" |

---

## Question Selection Guide

| Time Available | Recommended Questions | Focus |
|----------------|----------------------|-------|
| 15 min | Q1, Q5 | Core misconceptions |
| 25 min | Q1, Q3, Q5 | Balanced coverage |
| 35 min | All five | Complete session |
| 45 min | All five + follow-ups | Deep understanding |

---

*NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim*
