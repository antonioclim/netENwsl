# 🎯 Concept Analogies — Week 14: Integrated Recap

> NETWORKING class — ASE, CSIE | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

Understanding technical concepts through everyday analogies (CPA method).

---

## 1. Load Balancer = Hotel Reception Desk

| Hotel | Networking |
|-------|------------|
| Guest | HTTP request |
| Reception desk | Load balancer |
| Receptionist | Backend server |
| Queue manager | Round-robin algorithm |
| "Next available" | Health check |

**How it works:** Guests don't choose which receptionist to talk to — a queue manager directs them to the next available receptionist.

---

## 2. Port Mapping = Apartment Building Intercom

| Building | Networking |
|----------|------------|
| Street address | Host IP (localhost) |
| Intercom button "101" | Host port (8080) |
| Apartment door | Container port (80) |

**Memory aid:** `HOST:CONTAINER` = `Outside:Inside` = `Intercom:Apartment`

```yaml
ports:
  - "8080:80"   # Intercom 8080 → Apartment door 80
```

---

## 3. Docker Network = Gated Community

| Community | Networking |
|-----------|------------|
| Gated community | Docker network |
| Internal street address | Container IP |
| Main gate | Published port |
| Resident in multiple communities | Container on multiple networks |

**Key insight:** Containers on different networks cannot communicate directly, just like residents of different gated communities.

---

## 4. TCP Handshake = Phone Call Greeting

| Phone call | TCP |
|------------|-----|
| "Hello?" | SYN packet |
| "Hello! Yes, I hear you." | SYN-ACK packet |
| "Great, I hear you too." | ACK packet |
| Actual conversation | Data transfer |
| "Goodbye" - "Bye" | FIN packets |

```
Client                    Server
  |── "Hello?" (SYN) ────────▶|
  |◀── "Hello, yes!" (SYN-ACK)─|
  |── "Great!" (ACK) ─────────▶|
  [CONVERSATION BEGINS]
```

---

## 5. Container = Shipping Container

| Shipping | Docker |
|----------|--------|
| Container contents | Application and dependencies |
| Container dimensions | Container image format |
| Ship/truck/train | Any host with Docker |
| Bill of lading | Dockerfile |

**Key insight:** Containers are standardised, portable and isolated — just like shipping containers that work on any ship, truck or train.

---

## 6. DNS = Phone Directory

| Phone directory | DNS |
|-----------------|-----|
| Person's name | Domain name (example.com) |
| Phone number | IP address (93.184.216.34) |
| Looking up a name | DNS query |
| Memorising a number | DNS cache |

---

## 7. HTTP Request/Response = Restaurant Order

| Restaurant | HTTP |
|------------|------|
| "I'd like the burger" | GET /burger |
| "Add extra cheese" | Request headers |
| Waiter brings food | Response body |
| "Enjoy your meal" | Status 200 OK |
| "Sorry, we're out" | Status 404 Not Found |

---

## 8. Wireshark = Security Camera Footage

| Security camera | Wireshark |
|-----------------|-----------|
| Camera view | Network interface |
| Recording | Packet capture |
| Timestamp | Packet timestamp |
| Playback | Analysis |
| Zoom/filter | Display filters |

**Key insight:** You can only see traffic on interfaces you have access to — just like security cameras only record what's in their field of view.

---

## Where Analogies Break Down

| Analogy | Limitation | Technical reality |
|---------|------------|-------------------|
| Hotel reception | Receptionists get tired | Servers have consistent capacity |
| Phone call | Conversation is synchronous | TCP data flows both ways independently |
| Shipping container | Physical objects | Containers are virtual, start in milliseconds |
| Security camera | Records everything in view | Can only capture accessible interfaces |

---

*Document version: 2.0 | Week 14: Integrated Recap | January 2025*
