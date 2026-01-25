# ✅ Understanding Checks — Environment Setup Guide
## Supplement for Prerequisites.md

> **Purpose:** This document contains verification questions for each section  
> of the main setup guide. Use it for self-assessment.

---

## How to Use This Document

After completing each section of **Prerequisites.md**, return here and check if you can answer the corresponding questions. If you cannot answer, re-read the section or consult [docs/misconceptions.md](../docs/misconceptions.md).

---

## After Section 1: Introduction
**⏱️ Estimated section time: 5 minutes reading**

### ✓ Understanding Check

Can you answer these questions?

1. **Why do we use WSL2 + Docker instead of Docker Desktop?**
   <details>
   <summary>Answer</summary>
   WSL2 + Docker offers: better performance (native Linux kernel), lower resource consumption, complete access to Linux network stack, greater educational value (real Linux environment) and is completely free.
   </details>

2. **What components will we install and in what order?**
   <details>
   <summary>Answer</summary>
   In order: WSL2 → Ubuntu 22.04 → Docker → Portainer → Wireshark → Python packages
   </details>

3. **How long will the entire installation process take?**
   <details>
   <summary>Answer</summary>
   30-45 minutes, with a restart required after enabling WSL2.
   </details>

---

## After Section 2: System Architecture
**⏱️ Estimated section time: 5 minutes reading**

### ✓ Understanding Check

1. **Briefly describe the flow: Browser → Portainer → Container**
   <details>
   <summary>Answer</summary>
   Browser (Windows) → vEthernet (WSL) → WSL2 → Ubuntu → Docker Engine → Portainer Container (:9000)
   </details>

2. **What role does vEthernet (WSL) play?**
   <details>
   <summary>Answer</summary>
   It is the virtual network that connects Windows with WSL2, enabling communication between the two systems and access to services in containers.
   </details>

📌 **Common confusion:** See [docs/misconceptions.md](../docs/misconceptions.md) — Misconception 1 (WSL2 emulates Linux).

---

## After Section 3: Standard Credentials
**⏱️ Estimated section time: 2 minutes**

### ✓ Understanding Check

1. **What are the credentials for Ubuntu WSL?**
   <details>
   <summary>Answer</summary>
   User: `stud`, Password: `stud`
   </details>

2. **What are the credentials for Portainer?**
   <details>
   <summary>Answer</summary>
   User: `stud`, Password: `studstudstud` (12 characters)
   </details>

3. **Why does the Portainer password have 12 characters and not 4?**
   <details>
   <summary>Answer</summary>
   Portainer enforces a minimum length of 12 characters for the administrator password as a security measure.
   </details>

---

## After Section 4: Enable WSL2
**⏱️ Estimated section time: 10-15 minutes (includes restart)**

### ✓ Understanding Check

1. **What command enables WSL2?**
   <details>
   <summary>Answer</summary>
   `wsl --install` in PowerShell as Administrator
   </details>

2. **How do you verify that WSL2 is the default version?**
   <details>
   <summary>Answer</summary>
   `wsl --status` — should show "Default Version: 2"
   </details>

📌 **Practical verification:**
```powershell
wsl --status
# Expected output: Default Version: 2
```

---

## After Section 5: Install Ubuntu
**⏱️ Estimated section time: 5-10 minutes**

### ✓ Understanding Check

1. **Which Ubuntu version do we install?**
   <details>
   <summary>Answer</summary>
   Ubuntu 22.04 LTS (Long Term Support)
   </details>

2. **What does the `sudo` command do?**
   <details>
   <summary>Answer</summary>
   Executes commands with administrator (root) privileges. "Superuser do".
   </details>

📌 **Practical verification:**
```bash
cat /etc/os-release | grep VERSION
# Expected output: VERSION="22.04.x LTS (Jammy Jellyfish)"
```

---

## After Section 6: Install Docker
**⏱️ Estimated section time: 10-15 minutes**

### ✓ Understanding Check

1. **What does the command `usermod -aG docker $USER` do?**
   <details>
   <summary>Answer</summary>
   Adds the current user to the "docker" group, allowing Docker commands to be run without sudo.
   </details>

2. **Why must you logout/login or run `newgrp docker` after usermod?**
   <details>
   <summary>Answer</summary>
   Group changes only apply to new sessions. The current session must be refreshed to recognise membership in the new group.
   </details>

📌 **Practical verification:**
```bash
docker --version
# Output: Docker version 28.x.x

docker run --rm alpine echo "Test"
# Output: Test
```

📌 **Common confusion:** See [docs/misconceptions.md](../docs/misconceptions.md) — Misconception 3 (Container vs Image).

---

## After Section 7: Install Portainer
**⏱️ Estimated section time: 5 minutes**

### ✓ Understanding Check

1. **What does the `--restart=always` flag do?**
   <details>
   <summary>Answer</summary>
   Configures the container to start automatically when Docker daemon starts, including after restart.
   </details>

2. **On which port do you access Portainer from the browser?**
   <details>
   <summary>Answer</summary>
   http://localhost:9000
   </details>

📌 **Practical verification:**
```bash
docker ps | grep portainer
# Should show "portainer" container in "Up" state
```

📌 **Common confusion:** See [docs/misconceptions.md](../docs/misconceptions.md) — Misconception 8 (Portainer manages Docker).

---

## After Section 10: Auto-start
**⏱️ Estimated section time: 5 minutes (optional)**

### ✓ Understanding Check

1. **Why doesn't Docker start automatically in WSL2 after Windows restart?**
   <details>
   <summary>Answer</summary>
   WSL2 does not have systemd enabled by default, so services do not initialise automatically at boot.
   </details>

2. **What command manually starts Docker in WSL?**
   <details>
   <summary>Answer</summary>
   `sudo service docker start`
   </details>

📌 **Common confusion:** See [docs/misconceptions.md](../docs/misconceptions.md) — Misconception 7 (Docker auto-start).

---

## After Section 11: Final Verification
**⏱️ Estimated section time: 5 minutes**

### ✓ Complete Understanding Check

Can you tick all these points?

- [ ] `wsl --status` shows "Default Version: 2"
- [ ] `docker --version` displays a version (28.x.x)
- [ ] `docker ps` works without sudo
- [ ] Portainer container appears in `docker ps`
- [ ] Can access http://localhost:9000 from browser
- [ ] Can login to Portainer with stud/studstudstud
- [ ] Wireshark sees the "vEthernet (WSL)" interface
- [ ] `python3 -c "import docker, scapy, dpkt"` gives no error

### 🏁 Final Verification with Script

```bash
./verify_lab_environment.sh
# All checks should be PASS (green)
```

---

## Timing Summary for Entire Installation

| Section | Estimated Time |
|---------|---------------|
| 1. Introduction (reading) | 5 min |
| 2. Architecture (reading) | 5 min |
| 3. Credentials (reading) | 2 min |
| 4. Enable WSL2 | 10-15 min |
| 5. Install Ubuntu | 5-10 min |
| 6. Install Docker | 10-15 min |
| 7. Install Portainer | 5 min |
| 8. Install Wireshark | 5 min |
| 9. Python Packages | 5 min |
| 10. Auto-start (optional) | 5 min |
| 11. Final Verification | 5 min |
| **TOTAL** | **~60-75 min** |

*Note: Includes time for downloads and one restart.*

---

*Checks for Prerequisites.md — Week 0*  
*Computer Networks — ASE Bucharest, CSIE*  
*Version: 1.6.0 | January 2026*
