# 📋 Verified Versions — Week 7 Laboratory Kit
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> This document specifies the exact versions of all components verified to work with this laboratory kit.
> Using different versions may result in unexpected behaviour.

---

## Core Environment

| Component | Required Version | Verified Version | Verification Command |
|-----------|------------------|------------------|---------------------|
| Windows | 10 (build 19041+) or 11 | Windows 11 23H2 | `winver` |
| WSL | 2.0+ | 2.0.14 | `wsl --version` |
| Ubuntu (WSL) | 22.04 LTS | 22.04.3 LTS | `lsb_release -a` |
| Docker Engine | 24.0+ | 24.0.7 | `docker --version` |
| Docker Compose | 2.20+ | 2.23.3 | `docker compose version` |
| Python | 3.11+ | 3.11.6 | `python3 --version` |

---

## Python Dependencies

All versions pinned in `setup/requirements.txt`:

| Package | Required Version | Purpose | PyPI |
|---------|------------------|---------|------|
| PyYAML | 6.0.1 | YAML parsing for configs | [Link](https://pypi.org/project/PyYAML/) |
| docker | 7.0.0 | Docker SDK for Python | [Link](https://pypi.org/project/docker/) |
| requests | 2.31.0 | HTTP client for health checks | [Link](https://pypi.org/project/requests/) |
| colorama | 0.4.6 | Terminal colour output | [Link](https://pypi.org/project/colorama/) |

**Installation:**
```bash
pip install -r setup/requirements.txt
```

---

## Docker Images

| Image | Tag | Purpose | Size |
|-------|-----|---------|------|
| python | 3.11-slim | Base for all services | ~150MB |

**Note:** Images are pulled automatically by docker-compose on first run.

---

## Network Tools (WSL)

| Tool | Package | Verified Version | Installation |
|------|---------|------------------|--------------|
| tcpdump | tcpdump | 4.99.3 | `sudo apt install tcpdump` |
| tshark | tshark | 4.0.6 | `sudo apt install tshark` |
| netcat | netcat-openbsd | 1.218 | `sudo apt install netcat-openbsd` |
| iptables | iptables | 1.8.7 | Pre-installed in Ubuntu |
| curl | curl | 7.81.0 | Pre-installed in Ubuntu |

**Verification:**
```bash
python3 setup/verify_environment.py
```

---

## Windows Applications

| Application | Version | Purpose | Download |
|-------------|---------|---------|----------|
| Wireshark | 4.2.x | Packet analysis | [wireshark.org](https://www.wireshark.org/) |
| Docker Desktop | 4.26+ | Docker management | [docker.com](https://www.docker.com/products/docker-desktop/) |
| Windows Terminal | 1.18+ | Terminal emulator | Microsoft Store |

**Wireshark Configuration:**
- Install with Npcap (default)
- Enable "WinPcap API-compatible Mode" during Npcap setup

---

## Port Allocations

| Port | Protocol | Service | Configurable |
|------|----------|---------|--------------|
| 9000 | TCP | Portainer (RESERVED) | ❌ No |
| 9090 | TCP | TCP Echo Server | ✅ Yes |
| 9091 | UDP | UDP Receiver | ✅ Yes |
| 8888 | TCP | Packet Filter Proxy | ✅ Yes |

**⚠️ Port 9000 is globally reserved for Portainer - NEVER use for lab services!**

---

## Network Configuration

| Resource | Value | Notes |
|----------|-------|-------|
| Docker Network | week7net | Created by docker-compose |
| Subnet | 10.0.7.0/24 | Week 7 specific |
| Gateway | 10.0.7.1 | Docker bridge |
| TCP Server IP | 10.0.7.100 | Static assignment |
| TCP Client IP | 10.0.7.11 | Static assignment |
| UDP Receiver IP | 10.0.7.200 | Static assignment |
| UDP Sender IP | 10.0.7.12 | Static assignment |
| Packet Filter IP | 10.0.7.50 | Static assignment |

---

## Compatibility Notes

### Known Working Configurations

| Windows | WSL | Docker Desktop | Status |
|---------|-----|----------------|--------|
| 11 23H2 | 2.0.14 | 4.26.1 | ✅ Verified |
| 11 22H2 | 2.0.9 | 4.25.0 | ✅ Verified |
| 10 22H2 | 2.0.14 | 4.26.1 | ✅ Verified |
| 10 21H2 | 1.x | 4.x | ⚠️ WSL1 not supported |

### Known Issues

| Issue | Affected Versions | Workaround |
|-------|-------------------|------------|
| Wireshark no packets | Docker Desktop < 4.20 | Update Docker Desktop |
| WSL slow file access | WSL 2.0.0-2.0.5 | Update WSL: `wsl --update` |
| Docker socket permission | Ubuntu fresh install | `sudo usermod -aG docker $USER` |

---

## Version Verification Script

Run this to verify all versions:

```bash
#!/bin/bash
echo "=== Version Verification ==="
echo ""
echo "WSL Version:"
wsl.exe --version 2>/dev/null || echo "Run from Windows PowerShell"
echo ""
echo "Ubuntu Version:"
lsb_release -d
echo ""
echo "Python Version:"
python3 --version
echo ""
echo "Docker Version:"
docker --version
echo ""
echo "Docker Compose Version:"
docker compose version
echo ""
echo "tcpdump Version:"
tcpdump --version 2>&1 | head -1
echo ""
echo "tshark Version:"
tshark --version 2>&1 | head -1
echo ""
echo "=== Python Packages ==="
pip list | grep -E "PyYAML|docker|requests|colorama"
```

Save as `verify_versions.sh` and run with `bash verify_versions.sh`.

---

## Updating Components

### Update WSL
```powershell
# In Windows PowerShell (Administrator)
wsl --update
wsl --shutdown
# Restart WSL
```

### Update Docker Desktop
Download latest from [docker.com](https://www.docker.com/products/docker-desktop/)

### Update Python Packages
```bash
pip install --upgrade -r setup/requirements.txt
```

---

## Reporting Version Issues

If you encounter version-related problems:

1. Run `python3 setup/verify_environment.py`
2. Note which checks fail
3. Compare your versions against this document
4. Check `docs/troubleshooting.md` for solutions
5. Report persistent issues via course forum

---

*Last verified: 2026-01-24*  
*Computer Networks — Week 7 Laboratory Kit*  
*ASE Bucharest, CSIE | by ing. dr. Antonio Clim*
