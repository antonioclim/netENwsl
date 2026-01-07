# Changelog

All notable changes to the WEEK13_WSLkit package will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.0.0] - 2026-01-07

### Added
- Initial release of Week 13: IoT and Security in Computer Networks laboratory kit
- Docker Compose configuration with three vulnerable services:
  - Mosquitto MQTT broker (plaintext and TLS endpoints)
  - DVWA (Damn Vulnerable Web Application)
  - vsftpd with educational backdoor stub
- Four Python exercises:
  - Port scanner with concurrent execution
  - MQTT client for IoT communication
  - Packet sniffer with protocol identification
  - Vulnerability checker for defensive assessment
- IoT simulation applications (sensor and controller)
- Automated demonstration scripts
- Comprehensive documentation and theory summary
- Environment verification and setup scripts
- Test suite with smoke tests

### Security Notes
- All vulnerable services are isolated within a Docker network
- Backdoor stub does NOT execute commands (educational only)
- Prominent warnings included throughout documentation

---

*NETWORKING class - ASE, Informatics | by Revolvix*
