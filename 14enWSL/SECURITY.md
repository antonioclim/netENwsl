# 🔒 Security Policy

> NETWORKING class — ASE, CSIE | Computer Networks Laboratory  
> by ing. dr. Antonio Clim

## Overview

This document outlines the security practices and policies for the Week 14 Laboratory Kit. As an educational resource designed for controlled lab environments, this kit prioritizes **transparency**, **isolation**, and **safe learning**.

---

## 🛡️ Security Principles

### 1. No Real Credentials

This kit contains **NO real API keys, passwords, or secrets** that could be used maliciously.

| Item | Value | Purpose | Risk Level |
|------|-------|---------|------------|
| Portainer password | `studstudstud` | Lab access only | 🟢 NONE — Local only |
| WSL user | `stud` | Lab environment | 🟢 NONE — Local only |
| Docker networks | `172.20.0.0/24`, `172.21.0.0/24` | Internal container networking | 🟢 NONE — Non-routable |

**⚠️ These credentials are intentionally simple and documented for educational purposes. They are NOT used in any production system.**

### 2. Container Isolation

All code runs inside Docker containers with strict isolation:

```yaml
# Security constraints in docker-compose.yml
services:
  app1:
    # No privileged mode
    # No host network access
    # No sensitive volume mounts
    # Health checks for reliability
    networks:
      backend_net:
        ipv4_address: 172.20.0.2  # Internal only
```

**Isolation guarantees:**
- ✅ Containers cannot access host filesystem (except designated volumes)
- ✅ Containers use internal Docker networks only
- ✅ No containers run with `privileged: true`
- ✅ No sensitive host paths mounted
- ✅ Port 9000 reserved for Portainer (documented)

### 3. Input Validation

All user-facing scripts implement input validation:

```python
# Example from scripts/start_lab.py
def validate_input(user_input: str) -> bool:
    """Validate user input to prevent injection attacks."""
    # No shell metacharacters
    if any(c in user_input for c in [';', '|', '&', '$', '`', '>', '<']):
        return False
    # Length limits
    if len(user_input) > 256:
        return False
    return True
```

### 4. No AI Integration

This kit contains **NO direct integration with AI/ML models, APIs, or services**.

- ❌ No OpenAI/Anthropic API calls
- ❌ No machine learning model loading
- ❌ No LLM prompt injection vectors
- ❌ No automated code execution from external sources

**AI Risk Assessment: MINIMAL (10/10 safety)**

---

## 🔍 Vulnerability Reporting

### Scope

We accept vulnerability reports for:

- Python scripts (`*.py` files)
- Docker configurations (`Dockerfile`, `docker-compose.yml`)
- Shell scripts (`*.sh` files)
- Documentation that could lead to security issues

### Out of Scope

- Issues requiring physical access to the host machine
- Issues in upstream dependencies (report to maintainers)
- Issues in Docker/WSL2 themselves
- Social engineering attacks
- Theoretical attacks without proof of concept

### How to Report

1. **Email:** Open an issue on GitHub
2. **Subject:** `[SECURITY] Week 14 Lab Kit - Brief Description`
3. **Include:**
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### Response Timeline

| Stage | Timeline |
|-------|----------|
| Acknowledgment | 48 hours |
| Initial assessment | 7 days |
| Fix (if applicable) | 30 days |
| Public disclosure | 90 days (coordinated) |

---

## 🧪 Security Testing Checklist

Before each release, the following checks are performed:

### Code Security

- [ ] No hardcoded secrets (except documented lab credentials)
- [ ] No `eval()` or `exec()` with user input
- [ ] No shell injection vectors (`os.system()`, `subprocess.run()` with `shell=True`)
- [ ] No path traversal vulnerabilities
- [ ] No pickle deserialization from untrusted sources

### Docker Security

- [ ] No `privileged: true` in any service
- [ ] No host network mode (`network_mode: host`)
- [ ] No sensitive host path mounts (`/`, `/etc`, `/root`)
- [ ] All images from trusted sources (Docker Hub official images)
- [ ] Health checks defined for all services

### Network Security

- [ ] All services on internal Docker networks
- [ ] Only necessary ports exposed to host
- [ ] Port 9000 documented as reserved
- [ ] No services listening on 0.0.0.0 externally

### Documentation Security

- [ ] No real credentials in documentation
- [ ] Security warnings clearly visible
- [ ] Attack vectors not documented in detail

---

## 🔐 Secure Usage Guidelines

### For Instructors

1. **Use in controlled environments** — Lab computers, VMs, or student personal machines
2. **Change default credentials** if deploying to shared infrastructure
3. **Monitor student activity** during labs to prevent misuse
4. **Update regularly** to get security patches

### For Students

1. **Do NOT use lab credentials** elsewhere
2. **Do NOT expose Docker ports** to the internet
3. **Do NOT run untrusted code** in the lab environment
4. **Report suspicious activity** to your instructor

### For Contributors

1. **Never commit secrets** — Use `.env.example` with placeholders
2. **Run security linters** — `bandit`, `pip-audit`
3. **Follow secure coding** — OWASP guidelines
4. **Document security implications** of new features

---

## 📋 Dependency Security

### Monitoring

Dependencies are monitored using:

```bash
# Check for known vulnerabilities
pip-audit -r setup/requirements.txt

# Run security linter
bandit -r src/ scripts/ formative/
```

### Update Policy

| Severity | Action | Timeline |
|----------|--------|----------|
| Critical | Immediate patch | 24 hours |
| High | Priority update | 7 days |
| Medium | Next release | 30 days |
| Low | Scheduled update | 90 days |

---

## 📜 Compliance

This kit is designed for **educational use** and follows:

- **GDPR**: No personal data collected or stored
- **FERPA**: No student records processed
- **Academic Integrity**: Original work, properly attributed

---

## 📞 Contact

**Security Contact:** Open an issue on GitHub  
**PGP Key:** Available upon request  
**Response Time:** 48 hours (business days)

---

## 📝 Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-01-24 | 1.0.0 | Initial security policy |

---

*NETWORKING class — ASE, CSIE | Computer Networks Laboratory*  
*Security Policy v1.0.0 | January 2026*
