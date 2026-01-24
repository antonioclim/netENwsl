# 📋 Version Pinning Documentation — Week 1
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## Overview

This document specifies the exact versions of all software components tested
for Week 1 laboratory exercises. Using these versions ensures reproducibility
and minimizes compatibility issues.

---

## Tested Environment

### Operating System Stack

| Component | Version | Verified Date | Notes |
|-----------|---------|---------------|-------|
| Windows | 10/11 22H2+ | 2026-01-24 | Build 19045+ recommended |
| WSL2 | 2.0.x | 2026-01-24 | `wsl --version` to check |
| Ubuntu | 22.04.3 LTS | 2026-01-24 | Jammy Jellyfish |
| Kernel | 5.15.x | 2026-01-24 | WSL2 default kernel |

### Container Stack

| Component | Version | Verified Date | Notes |
|-----------|---------|---------------|-------|
| Docker Engine | 24.0.x | 2026-01-24 | Community Edition |
| Docker Compose | 2.21.x | 2026-01-24 | V2 plugin (not standalone) |
| Portainer | 2.19.x | 2026-01-24 | Community Edition |

### Python Stack

| Component | Version | Verified Date | Notes |
|-----------|---------|---------------|-------|
| Python | 3.11.7+ | 2026-01-24 | 3.12 also compatible |
| pip | 23.3+ | 2026-01-24 | Modern resolver |
| venv | Built-in | 2026-01-24 | Optional |

### Analysis Tools

| Component | Version | Verified Date | Notes |
|-----------|---------|---------------|-------|
| Wireshark | 4.0.x | 2026-01-24 | Windows installation |
| tcpdump | 4.99.x | 2026-01-24 | Ubuntu package |
| nmap | 7.94+ | 2026-01-24 | Optional |

---

## Python Dependencies

### Core (Required)

| Package | Version | Purpose |
|---------|---------|---------|
| docker | 7.0.0 | Docker API client |
| requests | 2.31.0 | HTTP library |
| PyYAML | 6.0.1 | YAML parsing |

### Analysis (Required for exercises)

| Package | Version | Purpose |
|---------|---------|---------|
| scapy | 2.5.0 | Packet manipulation |
| dpkt | 1.9.8 | PCAP parsing |

### Development (Optional)

| Package | Version | Purpose |
|---------|---------|---------|
| pytest | 8.0.0 | Testing framework |
| pytest-cov | 4.1.0 | Coverage reports |
| ruff | 0.1.14 | Linter & formatter |
| mypy | 1.8.0 | Type checker |
| pre-commit | 3.6.0 | Git hooks |
| jsonschema | 4.21.1 | Schema validation |

---

## Version Verification

### Quick Check Script

Run this to verify your environment:

```bash
python setup/verify_environment.py --strict
```

### Manual Verification

```bash
# Windows/WSL version
wsl --version

# Ubuntu version
lsb_release -a

# Docker versions
docker --version
docker compose version

# Python version
python3 --version
pip3 --version

# Key packages
python3 -c "import docker; print(f'docker: {docker.__version__}')"
python3 -c "import yaml; print(f'PyYAML: {yaml.__version__}')"
python3 -c "import scapy; print(f'scapy: {scapy.__version__}')"
```

---

## Known Compatibility Issues

### Docker Desktop vs Docker Engine

| Setup | Compatibility | Notes |
|-------|---------------|-------|
| Docker Desktop (Windows) | ✅ Works | Default for most students |
| Docker Engine (WSL2 native) | ✅ Works | Better performance |
| Docker Desktop + WSL2 backend | ✅ Works | Recommended |

### Python Version Notes

| Version | Status | Notes |
|---------|--------|-------|
| 3.10.x | ⚠️ Partial | Missing some type hints features |
| 3.11.x | ✅ Recommended | Full compatibility |
| 3.12.x | ✅ Works | Tested, fully compatible |
| 3.13.x | ❓ Unknown | Not yet tested |

### Wireshark Interface Selection

| Interface | Use Case |
|-----------|----------|
| `vEthernet (WSL)` | Docker container traffic |
| `eth0` (in WSL) | WSL internal traffic |
| `Loopback` | Local testing |

---

## Upgrade Notes

### From Previous Versions

If upgrading from an earlier lab kit version:

1. **Update Docker**: `docker pull` new images
2. **Update Python packages**: `pip install -U -r setup/requirements.txt`
3. **Clear caches**: `make clean`

### Breaking Changes

| Version | Change | Migration |
|---------|--------|-----------|
| 1.0.0 | Initial release | N/A |

---

## Reproducibility Guarantee

This laboratory kit was tested on the following reference system:

```
Windows 11 Pro 22H2 (Build 22621.3007)
WSL2 2.0.9.0
Ubuntu 22.04.3 LTS
Docker Engine 24.0.7
Python 3.11.7
```

All exercises complete successfully on this configuration.

---

*NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim*  
*Last updated: 2026-01-24*
