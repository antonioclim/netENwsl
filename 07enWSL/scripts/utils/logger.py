#!/usr/bin/env python3
"""
Logging Utilities
Computer Networks - ASE Bucharest, CSIE | by ing. dr. Antonio Clim

Provides consistent logging across all laboratory scripts.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Optional


# Module-level logger cache
_loggers: dict[str, logging.Logger] = {}



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class ColorFormatter(logging.Formatter):
    """Formatter that adds colour codes for terminal output."""
    
    COLOURS = {
        "DEBUG": "\033[36m",      # Cyan
        "INFO": "\033[32m",       # Green
        "WARNING": "\033[33m",    # Yellow
        "ERROR": "\033[31m",      # Red
        "CRITICAL": "\033[35m",   # Magenta
    }
    RESET = "\033[0m"
    

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
    def __init__(self, use_colour: bool = True) -> None:
        super().__init__(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        self.use_colour = use_colour


# ═══════════════════════════════════════════════════════════════════════════════
# OUTPUT_FORMATTING
# ═══════════════════════════════════════════════════════════════════════════════
    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        if self.use_colour and record.levelname in self.COLOURS:
            colour = self.COLOURS[record.levelname]
            message = f"{colour}{message}{self.RESET}"
        return message



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def setup_logger(
    name: str,
    level: int = logging.INFO,
    log_file: Optional[Path] = None,
    use_colour: bool = True
) -> logging.Logger:
    """
    Set up and return a logger with consistent formatting.
    
    Args:
        name: Logger name (typically the script name)
        level: Logging level (default: INFO)
        log_file: Optional file path for logging
        use_colour: Whether to use colour codes in terminal output
        
    Returns:
        Configured logger instance
    """
    if name in _loggers:
        return _loggers[name]
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(ColorFormatter(use_colour=use_colour))
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        ))
        logger.addHandler(file_handler)
    
    _loggers[name] = logger
    return logger



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def get_logger(name: str) -> logging.Logger:
    """
    Get an existing logger or create a new one with defaults.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    if name in _loggers:
        return _loggers[name]
    return setup_logger(name)

if __name__ == "__main__":
    # Module loaded directly - display module info
    print(f"Module {__name__} loaded successfully.")
    print(f"This module provides utility functions for the networking laboratory.")
