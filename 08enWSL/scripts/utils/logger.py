#!/usr/bin/env python3
"""
Logging Utility
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Provides consistent logging across all laboratory scripts.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import logging
import sys
from pathlib import Path
from typing import Optional



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def setup_logger(
    name: str,
    level: int = logging.INFO,
    log_file: Optional[Path] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Set up a logger with console and optional file output.
    
    Args:
        name: Logger name
        level: Logging level (default: INFO)
        log_file: Optional path to log file
        format_string: Optional custom format string
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Default format
    if format_string is None:
        format_string = "[%(asctime)s] %(levelname)-8s %(message)s"
    
    formatter = logging.Formatter(format_string, datefmt="%H:%M:%S")
    
    # Console handler with colours
    console_handler = ColourHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(logging.Formatter(
            "[%(asctime)s] %(levelname)-8s %(name)s: %(message)s"
        ))
        logger.addHandler(file_handler)
    
    return logger



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class ColourHandler(logging.StreamHandler):
    """Logging handler with colour support for terminals."""
    
    COLOURS = {
        logging.DEBUG: "\033[36m",     # Cyan
        logging.INFO: "\033[32m",      # Green
        logging.WARNING: "\033[33m",   # Yellow
        logging.ERROR: "\033[31m",     # Red
        logging.CRITICAL: "\033[35m",  # Magenta
    }
    RESET = "\033[0m"
    BOLD = "\033[1m"
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def emit(self, record):
        try:
            # Add colour codes
            colour = self.COLOURS.get(record.levelno, "")
            
            # Format message
            msg = self.format(record)
            
            # Apply colour to level name only
            if colour and hasattr(sys.stdout, "isatty") and sys.stdout.isatty():
                msg = msg.replace(
                    record.levelname,
                    f"{colour}{record.levelname}{self.RESET}"
                )
            
            self.stream.write(msg + self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def print_banner(title: str, subtitle: str = ""):
    """Print a formatted banner."""
    width = 60
    print()
    print("=" * width)
    print(f"  {title}")
    if subtitle:
        print(f"  {subtitle}")
    print("=" * width)
    print()



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def print_section(title: str):
    """Print a section header."""
    print(f"\n\033[1m{title}\033[0m")
    print("-" * 40)



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def print_success(message: str):
    """Print a success message."""
    print(f"\033[92m✓ {message}\033[0m")



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def print_error(message: str):
    """Print an error message."""
    print(f"\033[91m✗ {message}\033[0m")



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def print_warning(message: str):
    """Print a warning message."""
    print(f"\033[93m! {message}\033[0m")



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def print_info(message: str):
    """Print an info message."""
    print(f"\033[94mℹ {message}\033[0m")

if __name__ == "__main__":
    # Module loaded directly - display module info
    print(f"Module {__name__} loaded successfully.")
    print(f"This module provides utility functions for the networking laboratory.")
