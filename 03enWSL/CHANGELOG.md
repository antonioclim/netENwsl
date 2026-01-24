# Changelog

All notable changes to the Week 3 WSL Starter Kit are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-01-24

### Changed
- Improved British English consistency (removed Oxford commas throughout)
- Renamed homework files to follow naming conventions (hw_3_0X_descriptive_name.py)
- Added subgoal labels to all scripts/ Python files
- Added module docstrings to all __init__.py files

### Added
- docs/parsons_problems.md — code reordering exercises for active learning
- Type hints in scripts/ modules

### Fixed
- American spelling "colour" → "colour" in logger.py
- Replaced AI-flagged word "comprehensive" with "detailed"/"thorough"

## [1.0.0] - 2026-01-06

### Added
- Initial release of WEEK3_WSLkit for Windows/WSL2 environment
- Complete Docker Compose orchestration with four containers (server, router, client, receiver)
- Python scripts for UDP broadcast, UDP multicast and TCP tunnel demonstrations
- Automated setup and verification scripts for Windows/WSL2
- Detailed README with step-by-step exercise instructions
- Test suite with environment validation and exercise verification
- Packet capture helper scripts with Wireshark integration
- Homework assignments with solution stubs
- Documentation including theory summary, commands cheatsheet and troubleshooting guide

### Infrastructure
- Docker network configuration: 172.20.0.0/24
- Service ports: Echo server (8080), TCP tunnel (9090), Broadcast (5007), Multicast (5008)
- Container naming convention: week3_* prefix for all resources

### Python Examples Included
- ex_3_01_udp_broadcast.py - UDP broadcast sender and receiver
- ex_3_02_udp_multicast.py - UDP multicast with IGMP group membership
- ex_3_03_tcp_tunnel.py - TCP port forwarding with bidirectional relay
- ex_3_04_echo_server.py - Simple TCP echo server for testing

---

*NETWORKING class - ASE, Informatics | by Revolvix*
