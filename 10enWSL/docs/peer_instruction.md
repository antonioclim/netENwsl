# 🗳️ Peer Instruction Questions — Week 10
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> HTTP/HTTPS, REST Architecture and Network Services

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

## Question 1: HTTPS and URL Privacy

> 💭 **PREDICTION:** Before reading the options, write down what parts of an HTTPS request you think are encrypted.

### ⏱️ Think Time (60 seconds)

Consider these aspects before answering:
- What happens *before* encryption starts?
- What information does a server need to begin the TLS handshake?
- What can a network observer (ISP, coffee shop WiFi) see?

### Scenario

A user visits `https://bank.example.com/accounts/12345?balance=true` using a modern browser. An attacker is monitoring the network traffic between the user and the server.

### Question

Which of the following can the attacker see in plaintext (unencrypted)?

### Options

- **A)** The full URL including `/accounts/12345?balance=true` — *Misconception: thinking HTTPS encrypts everything*
- **B)** The domain name `bank.example.com` only — **CORRECT**
- **C)** Nothing at all — the entire connection is encrypted — *Misconception: overestimating TLS coverage*
- **D)** The HTTP headers but not the URL path — *Misconception: confusing what TLS protects*

### 💬 Discussion Prompts (for Step 3)

Use these prompts when discussing with your partner:
1. "When does encryption actually start in an HTTPS connection?"
2. "How does the server know which certificate to send if everything is encrypted?"
3. "What is SNI and why does it exist?"

### Correct Answer

**B** — The domain name `bank.example.com` is visible through SNI (Server Name Indication) in the TLS handshake. The URL path, query parameters, headers and body are all encrypted. However, the destination IP address is also visible.

### Targeted Misconception

Many students believe HTTPS encrypts "everything" including the domain name. SNI sends the hostname in plaintext during the TLS handshake so the server knows which certificate to present (important for virtual hosting).

### Instructor Notes

- **Target accuracy:** ~35-50% on first vote
- **Key concept:** TLS encrypts application data, not connection metadata
- **After discussion:** Show Wireshark capture of TLS handshake with SNI visible
- **Follow-up:** Mention ECH (Encrypted Client Hello) as emerging solution

---

## Question 2: REST Maturity Levels

> 💭 **PREDICTION:** What makes an API "truly RESTful" according to the Richardson Maturity Model?

### ⏱️ Think Time (60 seconds)

Consider these aspects before answering:
- What is the difference between a resource URI and an action URI?
- How should HTTP verbs (GET, POST, PUT, DELETE) be used?
- What does "Level 2" specifically require?

### Scenario

Consider this API interaction:

```http
POST /api/users/123/update HTTP/1.1
Content-Type: application/json

{"name": "Alice Updated", "email": "alice@new.example.com"}
```

Response:
```http
HTTP/1.1 200 OK
Content-Type: application/json

{"id": 123, "name": "Alice Updated", "email": "alice@new.example.com"}
```

### Question

According to the Richardson Maturity Model, what level does this API implement?

### Options

- **A)** Level 0 — uses HTTP as transport tunnel — *Misconception: any JSON API is Level 0*
- **B)** Level 1 — resources with URIs but action-style endpoints — **CORRECT**
- **C)** Level 2 — proper HTTP verbs and status codes — *Misconception: seeing POST assumes Level 2*
- **D)** Level 3 — full HATEOAS compliance — *Misconception: JSON response means HATEOAS*

### 💬 Discussion Prompts (for Step 3)

Use these prompts when discussing with your partner:
1. "What would this endpoint look like at Level 2?"
2. "Why is `/update` in the URL a sign of Level 1, not Level 2?"
3. "What HTTP verb should be used for updating a resource?"

### Correct Answer

**B** — This API has resource-oriented URIs (`/api/users/123`) but uses action-style subpaths (`/update`) instead of HTTP verbs. A Level 2 API would use `PUT /api/users/123` instead of `POST /api/users/123/update`.

### Targeted Misconception

Students often confuse "using resources in URLs" with "using HTTP verbs correctly". Level 1 has resources but treats HTTP as a transport. Level 2 uses GET/POST/PUT/DELETE semantically.

### Instructor Notes

- **Target accuracy:** ~40-55% on first vote
- **Key concept:** The difference between Level 1 and Level 2 is verb semantics
- **After discussion:** Show the same operation at all 4 levels
- **Demonstration:** Compare `/users/123/delete` (L1) vs `DELETE /users/123` (L2)

---

## Question 3: DNS Transport Protocol

> 💭 **PREDICTION:** Why would DNS ever use TCP instead of UDP?

### ⏱️ Think Time (60 seconds)

Consider these aspects before answering:
- What is the traditional UDP packet size limit?
- When might a DNS response be very large?
- What does the "truncation" flag in DNS mean?

### Scenario

A DNS resolver sends a query for `mail.largecorp.example.com` to an authoritative DNS server. The query is 45 bytes.

### Question

Under what circumstances will this DNS query use TCP instead of UDP?

### Options

- **A)** Never — DNS always uses UDP for queries — *Misconception: DNS = UDP only*
- **B)** When the response exceeds 512 bytes (traditional) or ~1232 bytes (EDNS) — **CORRECT**
- **C)** When querying for MX or TXT records specifically — *Misconception: record type determines transport*
- **D)** Only during zone transfers between DNS servers — *Misconception: TCP only for AXFR*

### 💬 Discussion Prompts (for Step 3)

Use these prompts when discussing with your partner:
1. "What happens when a UDP DNS response is too large?"
2. "What is the TC (truncation) bit in a DNS response?"
3. "Why is UDP preferred for most DNS queries?"

### Correct Answer

**B** — DNS uses UDP by default for efficiency, but switches to TCP when responses are too large. Traditional DNS limits UDP to 512 bytes; EDNS0 extends this but TCP is still used for very large responses. Zone transfers (AXFR/IXFR) always use TCP, but regular queries can also use TCP.

### Targeted Misconception

Students often memorise "DNS uses port 53/UDP" without understanding that TCP is also valid and necessary for large responses. The truncation bit (TC) in DNS responses signals the client to retry over TCP.

### Instructor Notes

- **Target accuracy:** ~30-45% on first vote
- **Key concept:** Protocol choice depends on response size, not query type
- **After discussion:** Use `dig +tcp` vs `dig +notcp` to demonstrate
- **Command:** `dig @127.0.0.1 -p 5353 example.com +tcp`

---

## Question 4: FTP Connection Architecture

> 💭 **PREDICTION:** How many TCP connections does FTP need to transfer a single file?

### ⏱️ Think Time (60 seconds)

Consider these aspects before answering:
- How does FTP separate commands from data?
- What is the difference between active and passive FTP?
- Why would a protocol use multiple connections?

### Scenario

A client connects to an FTP server to download a 10MB file. The server is behind a NAT firewall and uses passive mode.

```
Client: PASV
Server: 227 Entering Passive Mode (192,168,1,100,117,48)
Client: RETR largefile.zip
Server: 150 Opening BINARY mode data connection
[... file transfer ...]
Server: 226 Transfer complete
```

### Question

How many TCP connections are established for this file transfer?

### Options

- **A)** One connection for everything — *Misconception: FTP works like HTTP*
- **B)** Two connections — control (port 21) and data (high port) — **CORRECT**
- **C)** Three connections — control, command and data — *Misconception: over-complicating FTP*
- **D)** One connection, but the port changes during transfer — *Misconception: port hopping*

### 💬 Discussion Prompts (for Step 3)

Use these prompts when discussing with your partner:
1. "What is sent on the control channel vs the data channel?"
2. "Why does passive mode exist? What problem does it solve?"
3. "How do you calculate the port number from `(192,168,1,100,117,48)`?"

### Correct Answer

**B** — FTP uses a dual-channel architecture: a persistent control connection on port 21 for commands/responses and a separate data connection for actual file transfers. In passive mode, the server opens a high port (here: 117×256+48 = 30000) and the client connects to it.

### Targeted Misconception

Students familiar with HTTP expect one connection for everything. FTP's separation of control and data channels is unusual but allows features like transfer monitoring and concurrent operations.

### Instructor Notes

- **Target accuracy:** ~45-60% on first vote
- **Key concept:** FTP command channel vs data channel separation
- **After discussion:** Show both connections in Wireshark or `netstat`
- **Comparison:** Explain why HTTP/2 multiplexing is more efficient

---

## Question 5: TLS Handshake Purpose

> 💭 **PREDICTION:** What is exchanged during a TLS handshake before encrypted communication begins?

### ⏱️ Think Time (60 seconds)

Consider these aspects before answering:
- Why is asymmetric cryptography "slow"?
- What is a symmetric key and why is it needed?
- What does the server's certificate prove?

### Scenario

A browser initiates an HTTPS connection to `shop.example.com`. The TLS 1.3 handshake begins.

### Question

What is the PRIMARY purpose of the asymmetric cryptography (public/private keys) used in the TLS handshake?

### Options

- **A)** To encrypt all application data between client and server — *Misconception: asymmetric encrypts everything*
- **B)** To authenticate the server and establish a shared symmetric key — **CORRECT**
- **C)** To verify the integrity of transmitted data using digital signatures — *Misconception: confusing authentication with integrity*
- **D)** To compress data before encryption for efficiency — *Misconception: unrelated to key exchange*

### 💬 Discussion Prompts (for Step 3)

Use these prompts when discussing with your partner:
1. "Why would using RSA for all traffic be impractical?"
2. "What is the difference between authentication and encryption?"
3. "What symmetric algorithms does TLS typically use for bulk data?"

### Correct Answer

**B** — Asymmetric cryptography in TLS serves two purposes: (1) authenticating the server via its certificate and (2) securely exchanging or deriving a shared symmetric key. The actual data encryption uses symmetric algorithms (AES, ChaCha20) because they are much faster.

### Targeted Misconception

Students often think public-key cryptography encrypts all HTTPS traffic. In reality, asymmetric crypto is only used briefly during handshake — symmetric encryption handles the bulk data transfer for performance reasons.

### Instructor Notes

- **Target accuracy:** ~35-50% on first vote
- **Key concept:** Asymmetric for key exchange, symmetric for data
- **After discussion:** Show TLS handshake in Wireshark, identify cipher suite
- **Numbers:** RSA ~1000x slower than AES for equivalent security

---

## Summary Table

| Q# | Topic | Targeted Misconception | Difficulty |
|----|-------|------------------------|------------|
| 1 | HTTPS/TLS | "HTTPS encrypts everything including domain" | Medium |
| 2 | REST Levels | "Resource URIs = Level 2 compliance" | Medium |
| 3 | DNS Transport | "DNS only uses UDP" | Hard |
| 4 | FTP Architecture | "FTP uses single connection like HTTP" | Medium |
| 5 | TLS Handshake | "Asymmetric crypto encrypts all data" | Hard |

---

## Recommended Question Order

1. **Start with Q1** (HTTPS) — most students have used HTTPS
2. **Then Q5** (TLS) — builds on Q1's security theme
3. **Then Q2** (REST) — connects to practical API work
4. **Then Q3** (DNS) — fundamental protocol understanding
5. **End with Q4** (FTP) — multi-channel architecture concept

---

## 📝 After-Class Reflection

Use these questions for self-assessment after completing the peer instruction session:

### For Students

1. **Which question changed your answer after discussion?** What argument convinced you?
2. **Which misconception did you hold before today?** How has your understanding changed?
3. **Can you explain SNI to someone who has never heard of it?** Try it in 30 seconds.
4. **What is the one key difference between REST Level 1 and Level 2?**
5. **Why does FTP use two connections while HTTP uses one?** What are the trade-offs?

### Metacognitive Check

Rate your confidence (1-5) on each topic:

| Topic | Before Session | After Session |
|-------|----------------|---------------|
| HTTPS/SNI privacy | ☐ 1 ☐ 2 ☐ 3 ☐ 4 ☐ 5 | ☐ 1 ☐ 2 ☐ 3 ☐ 4 ☐ 5 |
| REST Maturity Model | ☐ 1 ☐ 2 ☐ 3 ☐ 4 ☐ 5 | ☐ 1 ☐ 2 ☐ 3 ☐ 4 ☐ 5 |
| DNS UDP vs TCP | ☐ 1 ☐ 2 ☐ 3 ☐ 4 ☐ 5 | ☐ 1 ☐ 2 ☐ 3 ☐ 4 ☐ 5 |
| FTP dual-channel | ☐ 1 ☐ 2 ☐ 3 ☐ 4 ☐ 5 | ☐ 1 ☐ 2 ☐ 3 ☐ 4 ☐ 5 |
| TLS handshake | ☐ 1 ☐ 2 ☐ 3 ☐ 4 ☐ 5 | ☐ 1 ☐ 2 ☐ 3 ☐ 4 ☐ 5 |

### Action Items

- [ ] Review any topic where confidence < 3
- [ ] Try the Wireshark exercises to see these protocols in action
- [ ] Explain one concept to a classmate who missed the session

---

*Computer Networks — Week 10 | ASE, CSIE Bucharest*
*Peer Instruction questions by ing. dr. Antonio Clim*
