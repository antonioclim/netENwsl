# 🔒 Security Guidelines — Week 11 Lab Kit
## Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

> **Version:** 1.0  
> **Last Updated:** 2026-01-24  
> **Classification:** Educational Use Only

---

## ⚠️ Important Notice

This laboratory kit is designed **exclusively** for educational purposes in isolated, local environments (WSL2 + Docker). It is **not** intended for production use.

---

## Scope and Limitations

### ✅ Appropriate Use
- Local WSL2/Docker development environment
- University laboratory sessions
- Personal learning and experimentation
- Isolated network testing

### ❌ Not Appropriate For
- Production or live systems
- Public-facing networks
- Corporate or enterprise environments
- Storage of real or sensitive data
- Any environment with untrusted users

---

## Security Practices

### 1. Credential Management

#### Environment Variables
```bash
# ALWAYS use .env file for credentials
cp setup/.env.example setup/.env

# NEVER commit .env to version control
# .env should be in .gitignore
```

#### Password Requirements
| Context | Requirement |
|---------|-------------|
| Portainer | Min 12 characters, alphanumeric + symbols |
| Lab exercises | Demo credentials acceptable (local only) |
| Any shared environment | Unique, secure credentials required |

#### What Not to Do
```python
# ❌ WRONG — hardcoded credentials in code
password = "mypassword123"

# ✅ CORRECT — load from environment
import os
password = os.getenv("PORTAINER_PASS")
```

---

### 2. Network Security

#### Port Exposure

| Port | Service | Exposure | Risk Level |
|------|---------|----------|------------|
| 8080 | Nginx LB | localhost only | Low |
| 8081-8083 | Backends | Docker network | Low |
| 9000 | Portainer | localhost only | Medium |
| 53 | DNS (exercises) | Not exposed | Low |

#### Network Isolation
```yaml
# docker-compose.yml ensures isolation
networks:
  s11_net:
    driver: bridge
    internal: false  # For internet access in exercises
    # For maximum isolation, set: internal: true
```

---

### 3. Container Security

#### Security Options Applied
```yaml
# In docker-compose.yml
services:
  nginx:
    security_opt:
      - no-new-privileges:true  # Prevent privilege escalation
    read_only: true              # Read-only root filesystem
    cap_drop:
      - ALL                      # Drop all capabilities
    cap_add:
      - NET_BIND_SERVICE         # Only what is needed
```

#### Image Verification
- All images use official sources (nginx:alpine)
- Pin versions where possible
- Regularly update base images

---

### 4. Input Validation

All user input should be validated before use:

```python
from scripts.utils.validation import validate_port, validate_hostname

# Validate port numbers
if not validate_port(user_port):
    raise ValidationError(f"Invalid port: {user_port}")

# Validate hostnames
if not validate_hostname(user_host):
    raise ValidationError(f"Invalid hostname: {user_host}")
```

---

### 5. Data Handling

#### What Data is Processed
| Data Type | Storage | Sensitivity |
|-----------|---------|-------------|
| HTTP requests | Memory only | Low |
| PCAP captures | Local files | Medium |
| Quiz answers | Memory only | Low |
| Logs | Local files | Low |

#### Data Retention
- PCAP files: Delete after lab session
- Logs: Delete after troubleshooting
- Docker volumes: Cleared with `make clean-all`

---

## Security Checklist for Students

Before starting the lab:
- [ ] Created unique credentials in `.env`
- [ ] Verified `.env` is in `.gitignore`
- [ ] Running on local/isolated network only
- [ ] Docker Desktop is updated

After completing the lab:
- [ ] Stopped all containers (`make stop`)
- [ ] Deleted PCAP files with sensitive captures
- [ ] Did not expose any ports externally
- [ ] Removed any temporary credentials

---

## Vulnerability Reporting

### For This Educational Kit

If you discover a security issue in this kit:

1. **Do not** create a public issue with sensitive details
2. **Do not** share exploit details publicly
3. Issues: Open an issue in GitHub with `[SECURITY]` tag
4. **Provide:**
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if known)

### Response Timeline
- Acknowledgment: Within 48 hours
- Assessment: Within 1 week
- Fix (if applicable): Within 2 weeks

---

## Common Security Mistakes to Avoid

### 1. Exposing Ports Publicly
```bash
# ❌ WRONG — binds to all interfaces
docker run -p 8080:80 nginx

# ✅ CORRECT — localhost only
docker run -p 127.0.0.1:8080:80 nginx
```

### 2. Running as Root
```bash
# ❌ WRONG
sudo python3 script.py

# ✅ CORRECT
python3 script.py  # Use regular user
```

### 3. Ignoring Update Warnings
```bash
# ✅ CORRECT — regularly update
docker pull nginx:alpine
pip install --upgrade -r requirements.txt
```

---

## Additional Resources

- Docker Security Best Practices: https://docs.docker.com/develop/security-best-practices/
- OWASP Container Security: https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html
- Python Security: https://python-security.readthedocs.io/

---

## Disclaimer

This security documentation is provided for educational purposes. Whilst we strive to follow security best practices, this kit is designed for learning in controlled environments and should not be considered secure for production use.

The authors and institution are not responsible for any security incidents resulting from:
- Use outside of intended scope
- Failure to follow these guidelines
- Modification of security configurations
- Exposure to untrusted networks

---

*NETWORKING class - ASE, CSIE | Computer Networks Laboratory*  
*Week 11: Application Protocols — FTP, DNS, SSH and Load Balancing*
