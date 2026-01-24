# 📋 Quick Reference Card — Week 11
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> **Print this page** for easy reference during the laboratory session!

---

## 🚀 Essential Commands

| Action | Command |
|--------|---------|
| **Start lab** | `make lab` |
| **Stop lab** | `make stop` |
| **Check status** | `make status` |
| **Run quiz** | `make quiz` |
| **Run basic quiz** | `make quiz-basic` |
| **Run advanced quiz** | `make quiz-advanced` |
| **Run tests** | `make test` |
| **View logs** | `make logs` |
| **Full cleanup** | `make clean-all` |
| **Help** | `make help` |

---

## 🌐 Ports Reference

| Port | Service | Access URL |
|------|---------|------------|
| **8080** | Nginx Load Balancer | http://localhost:8080 |
| 8081 | Backend 1 | http://localhost:8081 |
| 8082 | Backend 2 | http://localhost:8082 |
| 8083 | Backend 3 | http://localhost:8083 |
| **9000** | Portainer (RESERVED) | http://localhost:9000 |

### Protocol Ports (for exercises)

| Protocol | Port | Transport |
|----------|------|-----------|
| FTP Control | 21 | TCP |
| FTP Data | 20 | TCP |
| SSH | 22 | TCP |
| DNS | 53 | UDP/TCP |
| HTTP | 80 | TCP |
| HTTPS | 443 | TCP |

---

## 🦈 Wireshark Filters

```
# Load balancer traffic
tcp.port == 8080

# HTTP requests only
http.request

# HTTP responses only
http.response

# Lab network traffic
ip.addr == 172.28.0.0/16

# DNS queries
dns

# Specific backend
http contains "Backend 1"

# X-Served-By header
http contains "X-Served-By"
```

---

## 🐳 Docker Commands

```bash
# View running containers
docker ps

# View all containers (including stopped)
docker ps -a

# View container logs
docker logs s11_nginx_lb

# Enter container shell
docker exec -it s11_nginx_lb sh

# Stop specific container
docker stop s11_backend_2

# Start stopped container
docker start s11_backend_2

# Restart container
docker restart s11_nginx_lb

# View network
docker network inspect s11_network
```

---

## 🧪 Testing Commands

```bash
# Single request to load balancer
curl http://localhost:8080/

# Multiple requests (observe distribution)
for i in {1..10}; do curl -s http://localhost:8080/ | grep Backend; done

# With timing
time curl http://localhost:8080/

# Show headers
curl -i http://localhost:8080/

# Nginx status
curl http://localhost:8080/nginx_status

# Health check
curl http://localhost:8080/health
```

---

## 🔧 Troubleshooting Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| Docker not running | `sudo service docker start` |
| Permission denied | `sudo usermod -aG docker $USER && newgrp docker` |
| Port in use | `make clean-all && make lab` |
| Container will not start | `docker compose -f docker/docker-compose.yml down -v && make lab` |
| 502 Bad Gateway | Check if backends are running: `docker ps` |
| All requests to same backend | Check algorithm: `cat docker/configs/nginx.conf \| grep ip_hash` |

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `README.md` | Main documentation |
| `docker/docker-compose.yml` | Container configuration |
| `docker/configs/nginx.conf` | Nginx configuration |
| `src/exercises/ex_11_02_loadbalancer.py` | Python load balancer |
| `formative/quiz.yaml` | Quiz questions (YAML) |
| `formative/quiz.json` | Quiz questions (LMS export) |
| `docs/troubleshooting.md` | Detailed troubleshooting |
| `docs/learning_objectives.md` | LO traceability matrix |

---

## 📊 Load Balancing Algorithms

| Algorithm | Nginx Directive | Behaviour |
|-----------|-----------------|-----------|
| Round Robin | (default) | 1→2→3→1→2→3 |
| Least Connections | `least_conn;` | Routes to least busy |
| IP Hash | `ip_hash;` | Same IP → same backend |

### Nginx Config Example
```nginx
upstream backend_pool {
    # Uncomment ONE algorithm:
    # least_conn;
    # ip_hash;
    
    server web1:80 weight=3;
    server web2:80 weight=2;
    server web3:80 weight=1;
}
```

---

## ✅ Pre-Lab Checklist

- [ ] Docker running (`docker ps` works)
- [ ] Portainer accessible (http://localhost:9000)
- [ ] Lab started (`make lab`)
- [ ] Wireshark ready (correct interface selected)
- [ ] Terminal in lab folder (`cd /mnt/d/NETWORKING/WEEK11/11enWSL`)

## ✅ Post-Lab Checklist

- [ ] Stopped containers (`make stop`)
- [ ] Saved any important PCAP files
- [ ] Completed quiz (`make quiz`)
- [ ] Submitted homework (if required)

---

## 🆘 Getting Help

1. Check `docs/troubleshooting.md`
2. Run `make verify` for environment check
3. Check Docker logs: `make logs`
4. Issues: Open an issue in GitHub

---

## 📞 Quick Links

- **Theory:** `docs/theory_summary.md`
- **Misconceptions:** `docs/misconceptions.md`
- **Commands:** `docs/commands_cheatsheet.md`
- **Glossary:** `docs/glossary.md`
- **Learning Paths:** `docs/learning_paths.md`

---

*Week 11: Application Protocols — FTP, DNS, SSH and Load Balancing*  
*NETWORKING class - ASE, CSIE | Computer Networks Laboratory*
