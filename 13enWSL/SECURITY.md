# 🔒 Security Notice — Week 13 Laboratory

## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

---

## ⚠️ CRITICAL: Intentionally Vulnerable Services

This laboratory kit contains **intentionally vulnerable services** designed for **educational purposes only**.

```
╔════════════════════════════════════════════════════════════════════════════════╗
║                                                                                 ║
║   DO NOT expose these services to public networks!                             ║
║   DO NOT use techniques learned here for malicious purposes!                   ║
║   DO NOT scan systems without explicit written authorization!                  ║
║                                                                                 ║
║   Violation constitutes criminal offense under Romanian Penal Code Art. 360    ║
║                                                                                 ║
╚════════════════════════════════════════════════════════════════════════════════╝
```

---

## Vulnerable Services Inventory

| Service | Container | Port(s) | Vulnerability Type | Educational Purpose |
|---------|-----------|---------|-------------------|---------------------|
| **DVWA** | `week13_dvwa` | 8080 | SQL injection, XSS, CSRF, etc. | Web security testing |
| **vsftpd** | `week13_vsftpd` | 2121, 6200 | Simulated backdoor | Backdoor detection |
| **Mosquitto** | `week13_mosquitto` | 1883, 8883 | Anonymous access (1883) | IoT security analysis |

---

## Security Controls Implemented

### 1. Network Isolation

All vulnerable services run in an **isolated Docker network**:

```
Network: week13net
Subnet:  10.0.13.0/24
Gateway: 10.0.13.1
Type:    Bridge (not routable externally)
```

**Verification command:**
```bash
docker network inspect week13net | grep -A5 "IPAM"
```

### 2. Port Binding Restrictions

Services bind to **localhost** or Docker internal network only:

| Port | Binding | Accessible From |
|------|---------|-----------------|
| 1883 | localhost:1883 | Local machine only |
| 8080 | localhost:8080 | Local machine only |
| 2121 | localhost:2121 | Local machine only |
| 8883 | localhost:8883 | Local machine only |
| 6200 | localhost:6200 | Local machine only |

**Verification command:**
```bash
# Should show 127.0.0.1 or 0.0.0.0, NOT external IPs
netstat -tlnp 2>/dev/null | grep -E ":(1883|8080|2121|6200|8883)"
```

### 3. Container Isolation

Each container runs with:
- Limited capabilities (no `--privileged`)
- Read-only config mounts where possible
- Separate network namespace
- No host network access

### 4. Intentional Weak Credentials (EDUCATIONAL)

These credentials are **intentionally weak** for laboratory exercises:

| Service | Username | Password | Purpose |
|---------|----------|----------|---------|
| Portainer | `stud` | `studstudstud` | Container management |
| DVWA | `admin` | `password` | Web app testing |
| MQTT | (anonymous) | (none) | Protocol analysis |

**⚠️ These credentials exist ONLY for educational purposes within the isolated lab environment.**

---

## Ethical Guidelines

### ✅ PERMITTED Activities

1. Scanning containers within `week13net` (10.0.13.0/24)
2. Scanning localhost (127.0.0.1)
3. Testing vulnerabilities in DVWA
4. Analyzing MQTT traffic on lab broker
5. Learning reconnaissance techniques on lab targets

### ❌ PROHIBITED Activities

1. Scanning ANY system without written authorization
2. Exposing lab containers to public networks
3. Using learned techniques for malicious purposes
4. Sharing credentials outside educational context
5. Attempting to access systems outside lab scope

---

## Input Validation (Port Scanner)

The port scanner (`ex_13_01_port_scanner.py`) includes safety checks:

```python
ALLOWED_PREFIXES = [
    "127.",           # Localhost
    "10.0.13.",       # Lab subnet
    "192.168.",       # Private RFC1918
    "10.",            # Private RFC1918
    "172.16." - "172.31.",  # Private RFC1918
]
```

Scanning public IPs requires explicit `--allow-public` flag with additional confirmation.

---

## Audit Trail

Security-relevant operations are logged to `artifacts/audit.log`:

```
2026-01-24T10:30:00 | PORT_SCAN       | target=10.0.13.11 ports=1-1024
2026-01-24T10:31:00 | VULN_CHECK      | target=10.0.13.11 service=http
2026-01-24T10:32:00 | SERVICE_START   | containers=mosquitto,dvwa,vsftpd
```

Review audit log periodically:
```bash
cat artifacts/audit.log | tail -20
```

---

## Incident Response

### If You Suspect Unauthorized Access

1. **Stop all containers immediately:**
   ```bash
   python scripts/stop_lab.py
   # or
   docker compose -f docker/docker-compose.yml down
   ```

2. **Perform full cleanup:**
   ```bash
   python scripts/cleanup.py --full --prune
   ```

3. **Check audit log:**
   ```bash
   cat artifacts/audit.log
   ```

4. **Report to instructor** with:
   - Timestamp of suspicious activity
   - Audit log excerpt
   - Network capture if available

### If Lab Services Become Unresponsive

1. Check container status: `docker ps -a | grep week13`
2. Check logs: `docker logs week13_<service>`
3. Restart specific container or full lab
4. If persistent issues, perform full cleanup and restart

---

## Compliance References

This laboratory complies with:

- **GDPR Art. 32**: Security of processing (educational data isolation)
- **Romanian Penal Code Art. 360**: Unauthorized computer access (explicit authorization)
- **OWASP Testing Guide v4**: Ethical penetration testing principles
- **EC-Council CEH Ethics**: Code of ethics for security professionals

---

## Security Checklist (Before Lab Session)

```
□ Docker Desktop running and updated
□ Portainer accessible at localhost:9000
□ No external network exposure (verify with netstat)
□ Audit log cleared from previous session
□ VPN/proxy disabled (to prevent accidental external access)
□ Wireshark capturing on correct interface (vEthernet WSL)
```

---

## Contact

For security concerns or to report vulnerabilities in lab materials:

- **Instructor:** ing. dr. Antonio Clim
- **Course:** Computer Networks, ASE Bucharest
- **Response time:** Within 24 hours during semester

---

*Security documentation version 1.0 — January 2026*
*Compliant with responsible disclosure practices*
