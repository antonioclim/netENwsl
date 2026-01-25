#!/usr/bin/env python3
"""
Logger utility for Week 11 Laboratory scripts.
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Provides consistent, coloured logging across all laboratory scripts.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import logging
import sys
from datetime import datetime
from typing import Optional



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class ColouredFormatter(logging.Formatter):
    """Custom formatter with ANSI colour support for Windows/Unix terminals."""
    
    COLOURS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
    }
    RESET = '\033[0m'
    

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
    def __init__(self, use_colours: bool = True):
        super().__init__()
        self.use_colours = use_colours
    

# ═══════════════════════════════════════════════════════════════════════════════
# OUTPUT_FORMATTING
# ═══════════════════════════════════════════════════════════════════════════════
    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.now().strftime('%H:%M:%S')
        level = record.levelname
        message = record.getMessage()
        
        if self.use_colours and sys.stdout.isatty():
            colour = self.COLOURS.get(level, '')
            return f"{colour}[{timestamp}] [{level:8}]{self.RESET} {message}"
        else:
            return f"[{timestamp}] [{level:8}] {message}"



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def setup_logger(name: str, 
                 level: int = logging.INFO,
                 log_file: Optional[str] = None) -> logging.Logger:
    """
    Configure and return a logger instance.
    
    Args:
        name: Logger name (typically the script name)
        level: Logging level (default: INFO)
        log_file: Optional file path for logging to file
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler with colours
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(ColouredFormatter(use_colours=True))
    logger.addHandler(console_handler)
    
    # Optional file handler
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(ColouredFormatter(use_colours=False))
        logger.addHandler(file_handler)
    
    return logger



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def print_banner(title: str, width: int = 60) -> None:
    """Print a formatted banner."""
    print("=" * width)
    print(f" {title}".centre(width))
    print("=" * width)



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def print_section(title: str, width: int = 60) -> None:
    """Print a section header."""
    print("")
    print("-" * width)
    print(f" {title}")
    print("-" * width)


# ing. dr. Antonio Clim

if __name__ == "__main__":
    # Module loaded directly - display module info
    print(f"Module {__name__} loaded successfully.")
    print(f"This module provides utility functions for the networking laboratory.")
