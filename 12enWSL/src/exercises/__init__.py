# ═══════════════════════════════════════════════════════════════════════════════
# MODULE_DOCSTRING
# ═══════════════════════════════════════════════════════════════════════════════
"""
Week 12 Laboratory Exercises
============================
Computer Networks - ASE Bucharest | by ing. dr. Antonio Clim

This module contains guided exercises for Week 12:
- ex_12_01_explore_smtp: SMTP protocol exploration
- ex_12_02_compare_rpc: RPC protocol comparison (JSON-RPC, XML-RPC, gRPC)
"""


# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Any

__all__ = [
    "ex_12_01_explore_smtp",
    "ex_12_02_compare_rpc",
]

EXERCISES_DIR = Path(__file__).parent
