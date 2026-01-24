"""
Logging Configuration
NETWORKING class - ASE, Informatics | by Revolvix

Provides consistent logging setup for all laboratory scripts.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import logging
import sys
from typing import Optional



# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def setup_logger(
    name: str,
    level: int = logging.INFO,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Configure and return a logger with consistent formatting.
    
    Args:
        name: Logger name (typically script name)
        level: Logging level (default INFO)
        log_file: Optional file path for logging output
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Formatter
    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S"
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class LabLogger:
    """Context manager for laboratory script logging."""
    

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
    def __init__(self, name: str, log_file: Optional[str] = None):
        self.logger = setup_logger(name, log_file=log_file)
        self.name = name
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def __enter__(self):
        self.logger.info(f"Starting {self.name}")
        return self.logger
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.logger.error(f"{self.name} failed: {exc_val}")
        else:
            self.logger.info(f"{self.name} completed")
        return False

if __name__ == "__main__":
    # Module loaded directly - display module info
    print(f"Module {__name__} loaded successfully.")
    print(f"This module provides utility functions for the networking laboratory.")
