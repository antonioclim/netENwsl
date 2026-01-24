#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# MODULE_DOCSTRING
# ═══════════════════════════════════════════════════════════════════════════════
"""
Week 12 Scripts Package
=======================
Computer Networks - ASE Bucharest | by ing. dr. Antonio Clim

This package contains utility scripts for managing the Week 12 laboratory
environment, including container lifecycle and traffic capture.

Scripts:
    start_lab.py      — Start Docker containers for the lab
    stop_lab.py       — Stop and clean up lab containers
    cleanup.py        — Remove containers, volumes and networks
    run_demo.py       — Run interactive demonstrations
    capture_traffic.py — Capture network traffic for analysis
"""

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE_EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════
__all__ = [
    "start_lab",
    "stop_lab",
    "cleanup",
    "run_demo",
    "capture_traffic",
]
