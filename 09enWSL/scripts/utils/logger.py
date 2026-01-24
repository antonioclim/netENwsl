#!/usr/bin/env python3
"""
Logging utilities for Week 9 Laboratory
NETWORKING class - ASE, Informatics | by Revolvix

Provides consistent logging across all laboratory scripts with
coloured output for better readability in terminal sessions.
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
    """
    Custom formatter that adds ANSI colour codes to log messages.
    
    Colours are applied based on log level:
    - DEBUG: Cyan
    - INFO: Green
    - WARNING: Yellow
    - ERROR: Red
    - CRITICAL: Bold Red
    """
    
    # ANSI colour codes
    COLOURS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[1;31m' # Bold Red
    }
    RESET = '\033[0m'
    

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
    def __init__(self, use_colour: bool = True):
        super().__init__()
        self.use_colour = use_colour and sys.stdout.isatty()
    

# ═══════════════════════════════════════════════════════════════════════════════
# OUTPUT_FORMATTING
# ═══════════════════════════════════════════════════════════════════════════════
    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.now().strftime('%H:%M:%S')
        level = record.levelname
        message = record.getMessage()
        
        if self.use_colour and level in self.COLOURS:
            colour = self.COLOURS[level]
            return f"{colour}[{timestamp}] [{level:>8}]{self.RESET} {message}"
        else:
            return f"[{timestamp}] [{level:>8}] {message}"



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def setup_logger(
    name: str,
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    use_colour: bool = True
) -> logging.Logger:
    """
    Configure and return a logger instance.
    
    Args:
        name: Logger name (typically module name)
        level: Logging level (default: INFO)
        log_file: Optional path to log file
        use_colour: Whether to use coloured output (default: True)
    
    Returns:
        Configured logger instance
    
    Example:
        >>> logger = setup_logger("start_lab")
        >>> logger.info("Starting laboratory environment")
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler with colour formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(ColouredFormatter(use_colour=use_colour))
    logger.addHandler(console_handler)
    
    # Optional file handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def print_banner(title: str, width: int = 60) -> None:
    """
    Print a decorative banner for section headers.
    
    Args:
        title: Banner title text
        width: Total width of the banner
    """
    padding = (width - len(title) - 2) // 2
    print()
    print("=" * width)
    print(f"{'=' * padding} {title} {'=' * padding}")
    print("=" * width)
    print()



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def print_status(label: str, status: str, ok: bool = True) -> None:
    """
    Print a status line with coloured indicator.
    
    Args:
        label: Description of the item being checked
        status: Status text
        ok: Whether status is positive (green) or negative (red)
    """
    if sys.stdout.isatty():
        colour = '\033[32m' if ok else '\033[31m'
        reset = '\033[0m'
        indicator = '✓' if ok else '✗'
        print(f"  [{colour}{indicator}{reset}] {label}: {status}")
    else:
        indicator = 'OK' if ok else 'FAIL'
        print(f"  [{indicator}] {label}: {status}")


# =============================================================================
# Module test
# =============================================================================

if __name__ == "__main__":
    logger = setup_logger("test", level=logging.DEBUG)
    
    print_banner("Logger Test")
    
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    
    print()
    print_status("Python version", "3.11.0", ok=True)
    print_status("Docker", "Not found", ok=False)
