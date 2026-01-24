# Project 10: Network Services Orchestration with Docker

> **Course:** Computer Networks | **Institution:** ASE Bucharest - CSIE | **Project type:** Main

**Common guides:** [Pair Programming](../docs/common/pair_programming_guide.md) | [Code Quality](../docs/common/code_quality_standards.md) | [Git Workflow](../docs/common/git_workflow_detailed.md)

### 📅 Stage Calendar
| Stage | Week | Deliverables | Score |
|-------|------|--------------|-------|
| **E1** - Design | Week 5 | Specifications + Diagrams | 20% |
| **E2** - Prototype | Week 9 | Partial implementation | 25% |
| **E3** - Final | Week 13 | Complete version | 35% |
| **E4** - Presentation | Week 14 | Live demo | 20% |

**Repository:** `https://github.com/[username]/retele-proiect-10`

---

## 📚 Project Description

Deploy and orchestrate multiple network services (DNS, SSH, FTP) using Docker Compose. Configure inter-service communication, demonstrate service discovery and implement monitoring.

### 🎯 Learning Objectives
- **Deploy** network services in containers
- **Configure** Docker networking for service communication
- **Implement** DNS-based service discovery
- **Monitor** service health and logs

---

## 🎯 Concept Analogies

### Docker Compose = Orchestra Conductor
🏠 **Analogy:** A conductor ensures all musicians (services) start at the right time, play in harmony (network), and follow the same score (compose file).

💻 **Technical:** Compose defines services, networks, volumes in one file.

### Service Discovery = Phone Directory
🏠 **Analogy:** Instead of remembering everyone's phone number (IP), you look up names in a directory (DNS).

💻 **Technical:** Containers use service names, Docker's internal DNS resolves to IPs.

---

## 🗳️ Peer Instruction Questions

### Question 1: Container DNS
**Question:** In Docker Compose, how do containers find each other?
- A) By IP address
- B) By service name (Docker DNS) ✓
- C) By container ID
- D) By port number

**Explanation:** Docker provides internal DNS. Service names resolve to container IPs automatically.

### Question 2: Depends_on
**Question:** What does `depends_on` guarantee?
- A) Service starts after dependency
- B) Service waits for dependency to be healthy ✓ (with condition)
- C) Both A and B always
- D) Network connectivity

**Explanation:** Basic `depends_on` only ensures start order, not readiness. Use `condition: service_healthy` for health checks.

---

## ❌ Common Misconceptions

### 🚫 "Containers have fixed IPs"
**CORRECT:** Container IPs are dynamic. Use service names for reliable communication.

### 🚫 "depends_on waits for service ready"
**CORRECT:** By default, it only waits for container start, not application ready. Use health checks!

---

## 📖 Glossary
| Term | Definition |
|------|------------|
| **Docker Compose** | Multi-container orchestration tool |
| **Service** | Container definition in compose file |
| **Network** | Isolated communication channel |
| **Volume** | Persistent data storage |
| **Health Check** | Command to verify service readiness |

---

## 🔨 Implementation Example

```yaml
# docker-compose.yml
version: '3.8'

services:
  # ═══════════════════════════════════════════════════════════════════════════
  # DNS_SERVER
  # ═══════════════════════════════════════════════════════════════════════════
  dns:
    image: coredns/coredns
    volumes:
      - ./dns/Corefile:/etc/coredns/Corefile
      - ./dns/zones:/etc/coredns/zones
    ports:
      - "53:53/udp"
    networks:
      - services-net
    healthcheck:
      test: ["CMD", "dig", "@localhost", "test.local"]
      interval: 10s
      timeout: 5s
      retries: 3

  # ═══════════════════════════════════════════════════════════════════════════
  # SSH_SERVER
  # ═══════════════════════════════════════════════════════════════════════════
  ssh:
    image: linuxserver/openssh-server
    environment:
      - PUID=1000
      - PGID=1000
      - PASSWORD_ACCESS=true
      - USER_NAME=admin
      - USER_PASSWORD=secure123
    ports:
      - "2222:2222"
    networks:
      - services-net
    depends_on:
      dns:
        condition: service_healthy

  # ═══════════════════════════════════════════════════════════════════════════
  # FTP_SERVER
  # ═══════════════════════════════════════════════════════════════════════════
  ftp:
    image: fauria/vsftpd
    environment:
      - FTP_USER=ftpuser
      - FTP_PASS=ftppass
    volumes:
      - ./ftp-data:/home/vsftpd
    ports:
      - "21:21"
      - "21100-21110:21100-21110"
    networks:
      - services-net

networks:
  services-net:
    driver: bridge
    # 💭 PREDICTION: What subnet will Docker assign?
```

---

## ❓ Frequently Asked Questions

**Q: Services can't resolve each other's names**
A: Ensure they're on the same Docker network.

**Q: FTP passive mode doesn't work**
A: Expose passive port range and set PASV_ADDRESS.

---

## 📚 Laboratory References

Consult these resources from **netENwsl** (https://github.com/antonioclim/netENwsl):

| Week | Folder | Relevant Content |
|------|--------|------------------|
| 1 | `01enWSL/` | Docker basics, environment setup |
| 11 | `11enWSL/` | FTP, DNS, SSH, Docker orchestration |

---

*Last update: January 2026 — Computer Networks, ASE Bucharest*
