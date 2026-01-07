# Changelog

All notable changes to the Week 12 WSL Starter Kit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2025-01-07

### Added

#### Core Infrastructure
- Complete Docker Compose configuration with single multi-service container
- Python 3.12-slim base image with networking tools (tcpdump, tshark, netcat)
- Portainer CE integration for container management
- Dedicated bridge network `week12_net` (172.28.12.0/24)
- Persistent volume for SMTP spool directory

#### SMTP Implementation
- Educational SMTP server supporting RFC 5321 commands
- Custom LIST command for mailbox inspection
- Email storage in EML format with timestamps
- Port 1025 to avoid privilege requirements

#### RPC Implementations
- **JSON-RPC 2.0** server (port 6200)
  - Arithmetic operations (add, subtract, multiply, divide)
  - Utility methods (echo, sort_list, get_time)
  - Server introspection (get_server_info, get_stats)
  - Batch request support
  - Full error code compliance (-32700 through -32603)

- **XML-RPC** server (port 6201)
  - Calculator service implementation
  - Introspection support (system.listMethods, system.methodHelp)
  - All standard XML-RPC data types

- **gRPC** server (port 6251)
  - Protocol Buffer definitions (calculator.proto)
  - Calculator service with arithmetic and utility methods
  - SHA-256 hashing capability
  - Statistics tracking

#### Scripts
- `start_lab.py` — Service launcher with health checks and status display
- `stop_lab.py` — Graceful shutdown with optional volume preservation
- `cleanup.py` — Full environment cleanup with dry-run support
- `capture_traffic.py` — Packet capture wrapper for tcpdump/tshark
- `run_demo.py` — Automated demonstrations for classroom use

#### Utilities
- `logger.py` — Coloured console output and file logging
- `docker_utils.py` — Docker Compose management wrapper
- `network_utils.py` — SMTP, JSON-RPC, and XML-RPC test clients

#### Test Suite
- Environment validation tests (Python version, dependencies, ports)
- Exercise verification tests with conditional markers
- Smoke test for rapid service health check
- Expected outputs documentation

#### Documentation
- Comprehensive README with 8 learning objectives
- Theory summary covering SMTP and RPC architectures
- Commands cheatsheet with protocol-specific examples
- Troubleshooting guide for common issues
- Further reading with RFC references and tutorials
- Homework assignments with three practical exercises

#### Setup
- `verify_environment.py` — Prerequisite checker for Python, Docker, WSL2
- `install_prerequisites.py` — Automated dependency installation
- `requirements.txt` — Python package specifications

### Technical Notes

- All services run within single container for simplified networking
- Week-specific resource naming (week12_*) prevents conflicts
- Non-standard ports used throughout (1025, 6200, 6201, 6251)
- Compatible with Windows 10/11 + WSL2 + Docker Desktop
- British English spelling throughout documentation

---

## [Unreleased]

### Planned
- Additional gRPC streaming examples
- SMTP STARTTLS support demonstration
- Integration with mail clients (Thunderbird configuration)
- Performance benchmarking script improvements

---

*NETWORKING class - ASE, Informatics | by Revolvix*
