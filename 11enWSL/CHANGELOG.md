# Changelog

> NETWORKING class - ASE, Informatics | Computer Networks Laboratory
> 
> by Revolvix

All notable changes to the Week 11 Laboratory Starter Kit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [1.0.0] - 2025-01-07

### Added

#### Core Infrastructure
- Complete Docker Compose orchestration with Nginx load balancer and three backend servers
- Python-based load balancer implementation with round-robin, least-connections and IP hash algorithms
- Automated environment verification scripts for WSL2, Docker Desktop and Python dependencies
- Complete start/stop/cleanup lifecycle management scripts

#### Exercise Suite
- **Exercise 1**: HTTP backend server implementation with request tracking
- **Exercise 2**: Python round-robin load balancer with multiple algorithms
- **Exercise 3**: IP hash sticky session demonstration
- **Exercise 4**: Failover simulation with automatic backend redistribution
- **Exercise 5**: Nginx Docker stack with production-ready configuration
- **Exercise 6**: DNS client with query type support (A, AAAA, MX, NS, TXT)
- **Exercise 7**: Performance benchmarking with latency percentile analysis

#### Documentation
- Complete README with theoretical background and step-by-step instructions
- Commands cheatsheet for quick reference during laboratory sessions
- Troubleshooting guide covering common issues and solutions
- Expected outputs documentation for exercise verification

#### Testing Framework
- Automated smoke tests for rapid environment validation
- Exercise-specific test cases with targeted verification
- Environment prerequisite checking with actionable fix hints

#### Traffic Analysis
- Packet capture helper with tshark/tcpdump integration
- Wireshark filter suggestions for FTP, DNS, SSH and HTTP protocols
- PCAP output directory with organised storage

#### Homework Assignments
- Three take-home exercises extending classroom concepts
- Solution stubs for guided implementation
- Grading rubric with clear evaluation criteria

### Technical Specifications

#### Network Configuration
- Docker network: `s11_network` (172.28.0.0/16)
- Load balancer port: 8080
- Backend ports: 8081-8083 (Python), internal 80 (Docker)
- Health check endpoint: `/health`
- Status endpoint: `/nginx_status`

#### Load Balancing Algorithms
- Round-robin (default): Sequential distribution across backends
- Least-connections: Route to backend with fewest active connections
- IP hash: Consistent routing based on client IP address

#### Failover Configuration
- Maximum failures before marking down: 2
- Failure timeout: 10 seconds
- Automatic recovery on successful health check

---

## [0.1.0] - 2025-01-05

### Added
- Initial project structure based on master template
- Placeholder documentation files
- Docker configuration scaffolding

### Changed
- Refined exercise structure based on course requirements

### Notes
- Pre-release version for internal testing

---

*NETWORKING class - ASE, Informatics | by Revolvix*
