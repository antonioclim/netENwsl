# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-07

### Added
- Initial release of WEEK10_WSLkit
- Docker Compose orchestration for network services (HTTP, DNS, SSH, FTP)
- Python-based laboratory scripts for WSL2 environment
- HTTPS REST API exercise with self-signed certificate generation
- REST maturity levels demonstration (Richardson model)
- Comprehensive README with learning objectives and exercises
- Environment verification and prerequisite installation scripts
- Packet capture utilities for Wireshark integration
- Automated smoke tests for all exercises
- Homework assignments with solution stubs
- Theory summaries and command cheatsheets

### Services
- `web`: Python HTTP server on port 8000
- `dns-server`: Custom dnslib-based DNS server on UDP 5353
- `ssh-server`: OpenSSH server on port 2222
- `ssh-client`: Paramiko-based SSH automation container
- `ftp-server`: pyftpdlib FTP server on port 2121
- `debug`: Diagnostic container with network tools

### Exercises
- Exercise 1: HTTP service exploration
- Exercise 2: DNS resolution with custom server
- Exercise 3: SSH encrypted communication
- Exercise 4: FTP multi-channel protocol
- Exercise 5: HTTPS with TLS certificate
- Exercise 6: REST maturity levels comparison

---

*NETWORKING class - ASE, Informatics | by Revolvix*
