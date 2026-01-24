#!/usr/bin/env python3
"""
Logging Utilities
NETWORKING class - ASE, Informatics | by Revolvix

Provides consistent logging configuration across all scripts.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import logging
import sys
from typing import Optional



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def setup_logger(
    name: str,
    level: int = logging.INFO,
    fmt: str = "[%(asctime)s] %(levelname)s: %(message)s",
    datefmt: str = "%H:%M:%S"
) -> logging.Logger:
    """
    Configure and return a logger with consistent formatting.
    
    Args:
        name: Logger name (typically module name)
        level: Logging level (default: INFO)
        fmt: Log message format
        datefmt: Date/time format
        
    Returns:
        Configured Logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding duplicate handlers
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = logging.Formatter(fmt, datefmt=datefmt)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def set_verbose(logger: logging.Logger, verbose: bool = True) -> None:
    """
    Enable or disable verbose (DEBUG) logging.
    
    Args:
        logger: Logger to modify
        verbose: Whether to enable DEBUG level
    """
    if verbose:
        logger.setLevel(logging.DEBUG)
        for handler in logger.handlers:
            handler.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
        for handler in logger.handlers:
            handler.setLevel(logging.INFO)



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class ProgressLogger:
    """
    Context manager for logging progress of multi-step operations.
    """
    

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
    def __init__(self, logger: logging.Logger, operation: str, total_steps: int = 0):
        """
        Initialise progress logger.
        
        Args:
            logger: Logger to use
            operation: Name of the operation
            total_steps: Total number of steps (0 for unknown)
        """
        self.logger = logger
        self.operation = operation
        self.total_steps = total_steps
        self.current_step = 0
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def __enter__(self):
        self.logger.info(f"Starting: {self.operation}")
        return self
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.logger.info(f"Completed: {self.operation}")
        else:
            self.logger.error(f"Failed: {self.operation} - {exc_val}")
        return False
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def step(self, message: str) -> None:
        """Log a progress step."""
        self.current_step += 1
        if self.total_steps > 0:
            self.logger.info(f"  [{self.current_step}/{self.total_steps}] {message}")
        else:
            self.logger.info(f"  [{self.current_step}] {message}")

if __name__ == "__main__":
    # Module loaded directly - display module info
    print(f"Module {__name__} loaded successfully.")
    print(f"This module provides utility functions for the networking laboratory.")
