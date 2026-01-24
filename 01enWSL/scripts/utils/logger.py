#!/usr/bin/env python3
"""
Logging Utilities
NETWORKING class - ASE, Informatics | by Revolvix

Provides consistent logging configuration across all laboratory scripts.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class ColouredFormatter(logging.Formatter):
    """Formatter that adds colour codes for terminal output."""
    
    COLORS = {
        "DEBUG": "\033[36m",     # Cyan
        "INFO": "\033[32m",      # Green
        "WARNING": "\033[33m",   # Yellow
        "ERROR": "\033[31m",     # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"
    

# ═══════════════════════════════════════════════════════════════════════════════
# OUTPUT_FORMATTING
# ═══════════════════════════════════════════════════════════════════════════════
    def format(self, record: logging.LogRecord) -> str:
        # Add colour if outputting to terminal
        if hasattr(sys.stdout, "isatty") and sys.stdout.isatty():
            colour = self.COLORS.get(record.levelname, "")
            record.levelname = f"{colour}{record.levelname}{self.RESET}"
        return super().format(record)



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def setup_logger(
    name: str,
    level: int = logging.INFO,
    log_file: Optional[Path] = None,
    console: bool = True
) -> logging.Logger:
    """
    Configure and return a logger instance.
    
    Args:
        name: Logger name (typically script name without extension)
        level: Logging level (default: INFO)
        log_file: Optional path for file logging
        console: Whether to output to console (default: True)
    
    Returns:
        Configured Logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Console handler with colours
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_formatter = ColouredFormatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%H:%M:%S"
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    # File handler (no colours)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def get_logger(name: str) -> logging.Logger:
    """
    Get an existing logger or create a basic one.
    
    Args:
        name: Logger name
    
    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        return setup_logger(name)
    return logger



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def create_session_log(script_name: str, artifacts_dir: Path) -> Path:
    """
    Create a timestamped log file for a session.
    
    Args:
        script_name: Name of the script creating the log
        artifacts_dir: Directory for log files
    
    Returns:
        Path to the created log file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = artifacts_dir / f"{script_name}_{timestamp}.log"
    return log_file

if __name__ == "__main__":
    # Module loaded directly - display module info
    print(f"Module {__name__} loaded successfully.")
    print(f"This module provides utility functions for the networking laboratory.")
