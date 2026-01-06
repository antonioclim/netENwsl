# Changelog

All notable changes to this laboratory kit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-06

### Added
- Initial release of WEEK4_WSLkit
- Complete Python management scripts for Windows/WSL2 environment
- Docker Compose configuration with Portainer integration
- TEXT protocol server and client (TCP port 5400)
- BINARY protocol server and client (TCP port 5401)
- UDP sensor protocol server and client (UDP port 5402)
- Comprehensive environment verification scripts
- Automated demonstration scripts
- Smoke tests and exercise verification
- Packet capture helper utilities
- Complete documentation suite

### Features
- Length-prefixed framing for TEXT protocol
- 14-byte fixed header with CRC32 for BINARY protocol
- 23-byte datagrams with CRC32 for UDP sensor protocol
- Multi-threaded concurrent client handling
- Graceful shutdown and cleanup procedures

### Documentation
- Comprehensive README with exercises and troubleshooting
- Theory summary covering Physical and Data Link layers
- Commands cheatsheet for tcpdump, tshark, and netcat
- Protocol overhead analysis guide

---

*NETWORKING class - ASE, Informatics | by Revolvix*
