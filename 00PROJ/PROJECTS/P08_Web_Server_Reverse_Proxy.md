# Project 08: Custom Web Server and Reverse Proxy

> **Course:** Computer Networks | **Institution:** ASE Bucharest - CSIE | **Project type:** Main

**Common guides:** [Pair Programming](../docs/common/pair_programming_guide.md) | [Code Quality](../docs/common/code_quality_standards.md) | [Git Workflow](../docs/common/git_workflow_detailed.md)

### 📅 Stage Calendar
| Stage | Week | Deliverables | Score |
|-------|------|--------------|-------|
| **E1** - Design | Week 5 | Specifications + Diagrams | 20% |
| **E2** - Prototype | Week 9 | Partial implementation | 25% |
| **E3** - Final | Week 13 | Complete version | 35% |
| **E4** - Presentation | Week 14 | Live demo | 20% |

**Repository:** `https://github.com/[username]/retele-proiect-08`

---

## 📚 Project Description

Build a simple HTTP server from scratch using sockets, then implement a reverse proxy that forwards requests to backend servers with basic load balancing.

### 🎯 Learning Objectives
- **Parse** HTTP request/response format
- **Handle** multiple concurrent connections
- **Implement** reverse proxy forwarding
- **Add** basic load balancing

---

## 🎯 Concept Analogies

### Reverse Proxy = Hotel Reception
🏠 **Analogy:** Guests (clients) ask reception (proxy) for services. Reception knows which department (backend server) handles each request and forwards appropriately. Guests never interact directly with departments.

💻 **Technical:** Client connects to proxy, proxy connects to appropriate backend based on URL/rules.

---

## 🗳️ Peer Instruction Questions

### Question 1: Keep-Alive
**Question:** What does HTTP Keep-Alive do?
- A) Keeps server running
- B) Reuses TCP connection for multiple requests ✓
- C) Sends heartbeat packets
- D) Prevents timeouts

**Explanation:** Without Keep-Alive, each HTTP request needs a new TCP connection (expensive 3-way handshake).

### Question 2: Host Header
**Question:** Why is the Host header mandatory in HTTP/1.1?
- A) For logging
- B) For authentication
- C) For virtual hosting (multiple sites on one IP) ✓
- D) For caching

---

## ❌ Common Misconceptions

### 🚫 "HTTP is stateful"
**CORRECT:** HTTP itself is stateless. State is maintained through cookies, sessions, or tokens.

### 🚫 "Reverse proxy = load balancer"
**CORRECT:** Reverse proxy forwards requests. Load balancer distributes across servers. A reverse proxy CAN do load balancing but doesn't have to.

---

## 📖 Glossary
| Term | Definition |
|------|------------|
| **Reverse Proxy** | Server forwarding client requests to backends |
| **Load Balancing** | Distributing requests across servers |
| **Virtual Host** | Multiple websites on one server |
| **Keep-Alive** | Persistent HTTP connections |

---

## 🔨 Implementation Example

```python
# ═══════════════════════════════════════════════════════════════════════════════
# HTTP_PARSER
# ═══════════════════════════════════════════════════════════════════════════════
def parse_http_request(data: bytes) -> dict:
    """
    Parse raw HTTP request into components.
    
    Returns:
        Dict with method, path, headers, body
    """
    lines = data.decode('utf-8', errors='ignore').split('\r\n')
    
    # First line: METHOD PATH VERSION
    # 💭 PREDICTION: What if request is malformed?
    method, path, version = lines[0].split(' ')
    
    # Headers until empty line
    headers = {}
    for line in lines[1:]:
        if not line:
            break
        key, value = line.split(': ', 1)
        headers[key] = value
    
    return {'method': method, 'path': path, 'headers': headers}
```

---

## 📚 Laboratory References

Consult these resources from **netENwsl** (https://github.com/antonioclim/netENwsl):

| Week | Folder | Relevant Content |
|------|--------|------------------|
| 8 | `08enWSL/` | HTTP server implementation, reverse proxy |
| 10 | `10enWSL/` | Application protocols, REST API |

---

*Last update: January 2026 — Computer Networks, ASE Bucharest*
