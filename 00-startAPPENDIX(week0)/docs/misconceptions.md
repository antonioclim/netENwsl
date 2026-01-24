# ❌ Common Misconceptions — Week 0
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> This document lists the most common misunderstandings and how to correct them.  
> **Use it for self-assessment** and to avoid typical pitfalls.

---

## WSL and Virtualisation

### 🚫 Misconception 1: "WSL2 emulates Linux"

**WRONG:** "WSL2 translates Linux commands into Windows commands, like an emulator."

**CORRECT:** WSL2 runs a **real Linux kernel** (not emulated) in a lightweight virtual machine managed by Hyper-V. Alike WSL1 which translated system calls, WSL2 offers complete compatibility with Linux syscalls.

| Aspect | WSL1 | WSL2 |
|--------|------|------|
| Kernel | Syscall translation | Real Linux kernel |
| Compatibility | ~80% syscalls | 100% syscalls |
| Linux file performance | Slow | Fast |
| Windows file performance | Fast | Slower |
| Native Docker | No | Yes |

**Practical verification:**
```bash
uname -r
# Output: 5.15.x.x-smallrosoft-standard-WSL2
# Note "-smallrosoft-standard-WSL2" = real kernel, customised
```

---

### 🚫 Misconception 2: "Docker Desktop is required for Docker on Windows"

**WRONG:** "I must install Docker Desktop to use Docker on Windows."

**CORRECT:** You can install Docker **natively in WSL2** without Docker Desktop. Native WSL2 installation:
- Consumes fewer resources
- Does not require a licence for commercial use
- Offers more granular control

**Practical verification:**
```bash
docker info 2>/dev/null | grep -i "operating system"
# Output: Operating System: Ubuntu 22.04.x LTS
```

---

## Docker: Images and Containers

### 🚫 Misconception 3: "Container and image are the same thing"

**WRONG:** "I downloaded the nginx container" or "I deleted the image so the containers no longer exist."

**CORRECT:** 
- **Image** = read-only template (like an ISO or a mould)
- **Container** = runnable instance created from an image (like a VM started from ISO)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           IMAGE                                              │
│  (nginx:latest — read-only, ~140MB)                                         │
│                                                                              │
│    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                    │
│    │  Container 1 │  │  Container 2 │  │  Container 3 │                    │
│    │    web1      │  │    web2      │  │    web3      │                    │
│    │  (running)   │  │  (stopped)   │  │  (running)   │                    │
│    └──────────────┘  └──────────────┘  └──────────────┘                    │
│                                                                              │
│    Each container has its own writable layer                                │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 🚫 Misconception 4: "Stopping the container deletes data"

**WRONG:** "If I stop the container, I lose everything I saved in it."

**CORRECT:** `docker stop` does **NOT** delete the container or its data. The container remains on disc in "Exited" state. Data is lost only when:
1. You run `docker rm` (deletes the container)
2. You run `docker run --rm` (auto-remove on stop)
3. You did **NOT** use volumes for persistent data

---

## Docker Networking

### 🚫 Misconception 5: "Container port is automatically accessible from outside"

**WRONG:** "Nginx listens on port 80, so I can access `localhost:80` from my browser."

**CORRECT:** Container ports are **isolated by default**. You must map them explicitly with `-p`:

```bash
# ❌ Does NOT work from browser:
docker run -d nginx

# ✅ Works from browser:
docker run -d -p 8080:80 nginx
# Maps: localhost:8080 (host) → container:80
```

---

### 🚫 Misconception 6: "Localhost is the same everywhere"

**WRONG:** "If Portainer runs on `localhost:9000`, I can access `localhost:9000` from any container."

**CORRECT:** Each container has its **own network namespace**. `localhost` in a container refers to the container itself, not the host.

**Solution:** Use `host.docker.internal` to access host services from a container.

---

### 🚫 Misconception 7: "Docker starts automatically after Windows restart"

**WRONG:** "I configured everything, after restart it will work the same."

**CORRECT:** In native WSL2 (without Docker Desktop), the Docker service does **NOT start automatically**. WSL2 does not have systemd enabled by default, so services do not initialise at boot.

**Immediate solution:**
```bash
sudo service docker start
```

---

### 🚫 Misconception 8: "Portainer manages Docker"

**WRONG:** "Portainer controls Docker. If I delete Portainer, containers disappear."

**CORRECT:** Portainer is just a **management interface** (web UI). Docker Engine is what actually runs and manages containers. You can:
- Delete Portainer → containers remain
- Stop Docker → Portainer (and all containers) stop
- Use only CLI → Portainer becomes useless but Docker works

---

## Quick Summary

| # | Misconception | Reality |
|---|---------------|---------|
| 1 | WSL2 emulates Linux | Real Linux kernel in lightweight VM |
| 2 | Docker Desktop required | Native Docker in WSL2 works |
| 3 | Container = Image | Image = template, Container = instance |
| 4 | Stop deletes data | Stop preserves data, rm deletes |
| 5 | Ports auto-exposed | Must be mapped explicitly with -p |
| 6 | Localhost is global | Each container has its own localhost |
| 7 | Docker auto-starts | Must be configured manually in WSL2 |
| 8 | Portainer = Docker | Portainer is just UI, Docker is the engine |

---

*Misconceptions Document — Week 0: Lab Environment Setup*  
*Computer Networks — ASE Bucharest, CSIE*  
*Version: January 2025*
