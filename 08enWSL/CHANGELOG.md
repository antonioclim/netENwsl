# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-07

### Added
- Initial release of Week 8 Laboratory Starter Kit
- Docker Compose orchestration with nginx reverse proxy and 3 Python backend servers
- Load balancing demonstrations: round-robin, weighted, least-connections, IP hash
- Python exercises for HTTP server implementation and reverse proxy
- Thorough README with learning objectives and exercises
- Setup scripts for environment verification and prerequisite installation
- Traffic capture utilities for Wireshark analysis
- Automated demonstration scripts
- Test suite for environment validation

### Infrastructure
- nginx:alpine reverse proxy container (ports 8080/8443)
- 3x Python 3.11-slim backend server containers
- Optional Portainer CE for container management (port 9443)
- Isolated Docker network (172.28.8.0/24)

### Documentation
- Theory summary covering TCP, UDP, TLS and QUIC protocols
- Commands cheatsheet for Docker, curl and network diagnostics
- Troubleshooting guide for common issues
- References to course materials and RFC specifications

---

*NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim*
