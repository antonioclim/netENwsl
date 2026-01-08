#!/usr/bin/env python3
"""
Logging utilities for Week 2 laboratory scripts.
NETWORKING class - ASE, Informatics | by Revolvix
"""

import logging
import sys
from datetime import datetime
from typing import Optional


class ColorFormatter(logging.Formatter):
    """Custom formatter with colour support for terminal output."""
    
    COLORS = {
        "DEBUG": "\033[36m",     # Cyan
        "INFO": "\033[32m",      # Green
        "WARNING": "\033[33m",   # Yellow
        "ERROR": "\033[31m",     # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"
    
    def format(self, record: logging.LogRecord) -> str:
        # Add colour to level name
        color = self.COLORS.get(record.levelname, "")
        record.levelname = f"{color}{record.levelname:8s}{self.RESET}"
        return super().format(record)


def setup_logger(
    name: str,
    level: int = logging.INFO,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Set up and configure a logger.
    
    Args:
        name: Logger name (usually module name)
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
    
    # Format: [HH:MM:SS.mmm][LEVEL   ] message
    console_format = "[%(asctime)s][%(levelname)s] %(message)s"
    console_handler.setFormatter(ColorFormatter(console_format, datefmt="%H:%M:%S"))
    logger.addHandler(console_handler)
    
    # Optional file handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        file_handler.setFormatter(logging.Formatter(file_format))
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get existing logger or create new one with default settings."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        return setup_logger(name)
    return logger


def timestamp() -> str:
    """Get current timestamp string for logging."""
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]
