#!/usr/bin/env python3
"""
Logging Utility Module
======================
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Provides consistent logging configuration across all scripts.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════════
# DEFINE_COLOUR_FORMATTER
# ═══════════════════════════════════════════════════════════════════════════════
class ColourFormatter(logging.Formatter):
    """Custom formatter with colour support for terminal output."""
    
    COLOURS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    def __init__(self, use_colour: bool = True):
        """
        Initialise the colour formatter.
        
        Args:
            use_colour: Enable colour output if terminal supports it
        """
        super().__init__()
        self.use_colour = use_colour and sys.stdout.isatty()
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format a log record with optional colour.
        
        Args:
            record: The log record to format
            
        Returns:
            Formatted log string
        """
        timestamp = datetime.fromtimestamp(record.created).strftime('%H:%M:%S')
        
        if self.use_colour:
            colour = self.COLOURS.get(record.levelname, '')
            level = f"{colour}{record.levelname:>8}{self.RESET}"
        else:
            level = f"{record.levelname:>8}"
        
        return f"[{timestamp}] {level} | {record.getMessage()}"


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURE_LOGGER
# ═══════════════════════════════════════════════════════════════════════════════
def setup_logger(
    name: str,
    level: int = logging.INFO,
    log_file: Optional[Path] = None,
    use_colour: bool = True
) -> logging.Logger:
    """
    Configure and return a logger instance.
    
    Args:
        name: Logger name (typically script name)
        level: Logging level (default: INFO)
        log_file: Optional path for file logging
        use_colour: Enable colour output (default: True)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(ColourFormatter(use_colour=use_colour))
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
        ))
        logger.addHandler(file_handler)
    
    return logger


# ═══════════════════════════════════════════════════════════════════════════════
# GET_EXISTING_LOGGER
# ═══════════════════════════════════════════════════════════════════════════════
def get_logger(name: str) -> logging.Logger:
    """
    Get an existing logger or create a new one with defaults.
    
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
# DEMONSTRATION
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    # Demonstration
    log = setup_logger("demo")
    log.debug("This is a debug message")
    log.info("This is an info message")
    log.warning("This is a warning message")
    log.error("This is an error message")
    log.critical("This is a critical message")
