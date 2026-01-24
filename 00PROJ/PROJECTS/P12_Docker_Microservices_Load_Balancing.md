# Project 12: Docker Microservices with Load Balancing

> **Course:** Computer Networks | **Institution:** ASE Bucharest - CSIE | **Project type:** Main

**Common guides:** [Pair Programming](../docs/common/pair_programming_guide.md) | [Code Quality](../docs/common/code_quality_standards.md) | [Git Workflow](../docs/common/git_workflow_detailed.md)

### 📅 Stage Calendar
| Stage | Week | Deliverables | Score |
|-------|------|--------------|-------|
| **E1** - Design | Week 5 | Specifications + Diagrams | 20% |
| **E2** - Prototype | Week 9 | Partial implementation | 25% |
| **E3** - Final | Week 13 | Complete version | 35% |
| **E4** - Presentation | Week 14 | Live demo | 20% |

**Repository:** `https://github.com/[username]/retele-proiect-12`

---

## 📚 Project Description

Build a distributed web application using microservices architecture in Docker with Nginx load balancing. Implement service scaling, health checks and demonstrate fault tolerance.

### 🎯 Learning Objectives
- **Design** microservices architecture
- **Configure** Nginx as load balancer
- **Implement** health checks and failover
- **Scale** services dynamically

---

## 🎯 Concept Analogies

### Load Balancer = Restaurant Host
🏠 **Analogy:** A restaurant host distributes arriving guests among available waiters (servers) to balance workload. If a waiter is busy or sick (unhealthy), guests go to others.

💻 **Technical:** Nginx distributes requests across backend containers.

### Microservices = Food Court
🏠 **Analogy:** Instead of one restaurant doing everything, a food court has specialised stalls (services). Each does one thing well.

---

## 🗳️ Peer Instruction Questions

### Question 1: Load Balancing Algorithms
**Question:** Round-robin sends requests to:
- A) The fastest server
- B) Each server in turn ✓
- C) The least loaded server
- D) Random server

### Question 2: Health Checks
**Question:** What happens when a health check fails?
- A) Server restarts
- B) Traffic stops going to that server ✓
- C) Alert is sent
- D) Nothing

---

## ❌ Common Misconceptions

### 🚫 "More replicas = more speed"
**CORRECT:** More replicas help with concurrent requests but don't make individual requests faster.

### 🚫 "Load balancer handles sessions automatically"
**CORRECT:** Stateless apps work easily; stateful need sticky sessions or external session storage.

---

## 📖 Glossary
| Term | Definition |
|------|------------|
| **Load Balancer** | Distributes traffic across servers |
| **Round Robin** | Sequential distribution algorithm |
| **Health Check** | Periodic service status verification |
| **Horizontal Scaling** | Adding more instances |

---

## 🔨 Implementation Example

```nginx
# nginx.conf
upstream backend {
    # 💭 PREDICTION: What if web2 goes down?
    # Answer: Nginx stops sending traffic to it (passive health check)
    
    least_conn;  # Send to least busy server
    
    server web1:5000 weight=3;
    server web2:5000 weight=2;
    server web3:5000 backup;  # Only if others fail
}

server {
    listen 80;
    
    location / {
        proxy_pass http://backend;
        proxy_connect_timeout 5s;
        proxy_next_upstream error timeout;
    }
    
    location /health {
        return 200 'OK';
    }
}
```

```yaml
# docker-compose.yml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - web1
      - web2
      - web3

  web1:
    build: ./app
    environment:
      - INSTANCE=web1

  web2:
    build: ./app
    environment:
      - INSTANCE=web2

  web3:
    build: ./app
    environment:
      - INSTANCE=web3
```

---

## 📚 Laboratory References

Consult these resources from **netENwsl** (https://github.com/antonioclim/netENwsl):

| Week | Folder | Relevant Content |
|------|--------|------------------|
| 1 | `01enWSL/` | Docker basics |
| 11 | `11enWSL/` | Load balancing with Nginx |

---

*Last update: January 2026 — Computer Networks, ASE Bucharest*
