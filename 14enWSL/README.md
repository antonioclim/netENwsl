# Week 14: Integrated Recap and Project Evaluation

> NETWORKING class — ASE, CSIE | Computer Networks Laboratory
>
> by ing. dr. Antonio Clim

---

## Overview

This laboratory kit provides a comprehensive environment for reviewing and integrating networking concepts from the entire course. Students will work with a multi-container Docker environment featuring load balancing, backend services and packet capture capabilities.

In previous years, students often struggled with understanding the difference between frontend and backend networks. If the topology seems confusing at first, focus on the load balancer as the bridge between the two worlds.

---

## Quick Start

### Prerequisites

- WSL2 with Ubuntu 22.04+
- Docker Engine
- Portainer (running on port 9000)

### Starting the Lab

```bash
# From PowerShell (clone repository)
cd ~
git clone <repository-url> week14
cd week14

# From WSL2/Ubuntu
cd ~/week14

# Ensure Docker is running
sudo service docker start

# Start the lab environment
make docker-up

# Verify everything is running
make smoke
```

### Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| Load Balancer | http://localhost:8080 | Entry point for HTTP requests |
| Backend 1 | http://localhost:8001 | First application server |
| Backend 2 | http://localhost:8002 | Second application server |
| TCP Echo | localhost:9090 | Socket programming exercises |
| Portainer | http://localhost:9000 | Container management UI |

---

## Network Topology

```
                    ┌─────────────────────────────────────────────────┐
                    │              Docker Host (WSL2)                 │
                    │                                                 │
   Internet ───────►│ ┌───────────────────────────────────────────┐  │
   (Windows)        │ │        week14_frontend_net                 │  │
                    │ │              172.20.0.0/24                 │  │
                    │ │                                            │  │
                    │ │  ┌────────────────────────────────────┐   │  │
                    │ │  │     Load Balancer (nginx)          │   │  │
   :8080 ──────────►│ │  │     week14_lb                      │   │  │
                    │ │  │     172.20.0.10                    │   │  │
                    │ │  └──────────────┬─────────────────────┘   │  │
                    │ └─────────────────│─────────────────────────┘  │
                    │                   │                            │
                    │ ┌─────────────────│─────────────────────────┐  │
                    │ │        week14_backend_net                  │  │
                    │ │              172.21.0.0/24                 │  │
                    │ │                 │                          │  │
                    │ │    ┌────────────┴────────────┐            │  │
                    │ │    │                         │            │  │
                    │ │    ▼                         ▼            │  │
                    │ │ ┌──────────────┐   ┌──────────────┐       │  │
                    │ │ │   App 1      │   │   App 2      │       │  │
   :8001 ──────────►│ │ │ week14_app1  │   │ week14_app2  │◄──────│──│── :8002
                    │ │ │ 172.21.0.2   │   │ 172.21.0.3   │       │  │
                    │ │ └──────────────┘   └──────────────┘       │  │
                    │ └───────────────────────────────────────────┘  │
                    └─────────────────────────────────────────────────┘
```

---

## Learning Objectives

By the end of this laboratory, students will be able to:

| LO | Description | Bloom Level |
|----|-------------|-------------|
| LO1 | Recall OSI and TCP/IP layered architectures | Remember |
| LO2 | Explain reverse proxies and load balancers | Understand |
| LO3 | Implement multi-container Docker environment | Apply |
| LO4 | Analyse packet captures to trace HTTP flows | Analyse |
| LO5 | Design verification strategies for services | Create |
| LO6 | Evaluate system behaviour under conditions | Evaluate |

See `docs/learning_objectives.md` for the complete traceability matrix.

---

## Directory Structure

```
14enWSL/
├── README.md                    # This file
├── Makefile                     # Task orchestration
├── ruff.toml                    # Linting configuration
├── docker/
│   ├── docker-compose.yml       # Container definitions
│   ├── Dockerfile               # Custom images
│   └── configs/                 # nginx, app configs
├── docs/
│   ├── learning_objectives.md   # LO traceability matrix
│   ├── theory_summary.md        # Theoretical background
│   ├── misconceptions.md        # Common errors
│   ├── troubleshooting.md       # Problem solving
│   ├── parsons_problems.md      # Code ordering exercises
│   ├── peer_instruction.md      # ConcepTests
│   └── ci_setup.md              # CI pipeline docs
├── formative/
│   ├── quiz.yaml                # YAML quiz (standalone)
│   ├── quiz.json                # JSON quiz (LMS export)
│   ├── run_quiz.py              # Quiz runner
│   └── export_moodle.py         # LMS export tools
├── homework/
│   ├── README.md                # Assignment descriptions
│   └── exercises/               # Homework templates
├── scripts/
│   ├── start_lab.py             # Start environment
│   ├── stop_lab.py              # Stop environment
│   ├── cleanup.py               # Clean resources
│   ├── capture_traffic.py       # Packet capture
│   └── run_demo.py              # Demonstrations
├── setup/
│   └── requirements.txt         # Python dependencies
├── src/
│   ├── exercises/               # Lab exercises
│   └── apps/                    # Application code
└── tests/
    ├── smoke_test.py            # Basic verification
    ├── test_validators.py       # Validation tests
    └── test_exports.py          # Export tests
```

---

## Common Commands

```bash
# Start lab environment
make docker-up

# Run formative quiz
make quiz

# Run all tests
make test

# Start packet capture
make capture

# Stop lab environment
make docker-down

# Full cleanup
make clean-all

# View all available commands
make help
```

---

## Troubleshooting

### Docker not running

```bash
sudo service docker start
```

### Containers not starting

```bash
# Check container status
docker ps -a --filter name=week14

# View container logs
docker logs week14_lb

# Rebuild images
make docker-rebuild
```

### Port conflicts

Check if ports 8080, 8001, 8002 or 9090 are already in use:

```bash
ss -tlnp | grep -E '8080|8001|8002|9090'
```

See `docs/troubleshooting.md` for more detailed guidance.

---

## Assessment

### Formative Quiz

Run the self-assessment quiz:

```bash
make quiz
```

Quiz is available in both YAML and JSON formats for compatibility with various LMS platforms.

### Homework

Three homework assignments are provided in `homework/exercises/`:
- HW 14.01: Enhanced Echo Server
- HW 14.02: Weighted Load Balancer
- HW 14.03: PCAP Analyser

---

## Support

If you encounter issues:

1. Check `docs/troubleshooting.md`
2. Review `docs/misconceptions.md`
3. Open an issue on GitHub

---

*NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim*

*Document version: 2.0 | Week 14: Integrated Recap | January 2025*
