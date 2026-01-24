"""
Setup utilities for Week 8 Laboratory Environment.

This package contains scripts for environment verification,
prerequisite installation and Docker configuration.

NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim
"""

from pathlib import Path
from typing import Optional, List, Dict, Tuple, Any

SETUP_DIR = Path(__file__).parent
PROJECT_ROOT = SETUP_DIR.parent

__all__ = ['SETUP_DIR', 'PROJECT_ROOT']
