"""
Scripts Utilities Module — Week 7
=================================
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Shared utilities for laboratory scripts:
- logger.py: Enhanced logging with configurable levels

Usage:
    from scripts.utils.logger import LabLogger, LogLevel
    
    logger = LabLogger(name="my_script", level=LogLevel.DEBUG)
    logger.info("Script started")
"""

from .logger import LabLogger, LogLevel, get_logger

__all__ = ["LabLogger", "LogLevel", "get_logger"]
__version__ = "1.0.0"
