#!/usr/bin/env python3
"""
Logging Utilities — Week 6: NAT/PAT & SDN Laboratory
====================================================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

Provides consistent logging configuration across all laboratory scripts.

Usage:
    from scripts.utils.logger import setup_logger, ProgressLogger
    
    logger = setup_logger(__name__)
    logger.info("Starting operation...")
    
    with ProgressLogger(logger, "Building topology", total_steps=3) as progress:
        progress.step("Creating hosts")
        progress.step("Configuring links")
        progress.step("Starting services")
"""

from __future__ import annotations

import logging
import sys
from contextlib import contextmanager
from typing import Any, Generator, Optional, TextIO, Union


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

DEFAULT_FORMAT = "[%(asctime)s] %(levelname)s: %(message)s"
DEFAULT_DATEFMT = "%H:%M:%S"
VERBOSE_FORMAT = "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)d]: %(message)s"


# ═══════════════════════════════════════════════════════════════════════════════
# LOGGER_SETUP
# ═══════════════════════════════════════════════════════════════════════════════

def setup_logger(
    name: str,
    level: int = logging.INFO,
    fmt: str = DEFAULT_FORMAT,
    datefmt: str = DEFAULT_DATEFMT,
    stream: Optional[TextIO] = None,
) -> logging.Logger:
    """
    Configure and return a logger with consistent formatting.
    
    Args:
        name: Logger name (typically __name__ of the calling module)
        level: Logging level (default: INFO)
        fmt: Log message format string
        datefmt: Date/time format string
        stream: Output stream (default: sys.stdout)
        
    Returns:
        Configured Logger instance
        
    Example:
        >>> logger = setup_logger(__name__)
        >>> logger.info("Hello, world!")
        [10:30:45] INFO: Hello, world!
    """
    if stream is None:
        stream = sys.stdout
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding duplicate handlers
    if not logger.handlers:
        handler = logging.StreamHandler(stream)
        handler.setLevel(level)
        formatter = logging.Formatter(fmt, datefmt=datefmt)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


def set_verbose(logger: logging.Logger, verbose: bool = True) -> None:
    """
    Enable or disable verbose (DEBUG) logging.
    
    When verbose mode is enabled, the log format is also changed to include
    the module name and line number for easier debugging.
    
    Args:
        logger: Logger to modify
        verbose: Whether to enable DEBUG level
        
    Example:
        >>> logger = setup_logger(__name__)
        >>> set_verbose(logger, True)
        >>> logger.debug("Detailed debug info")
        [10:30:45] DEBUG [mymodule:42]: Detailed debug info
    """
    new_level = logging.DEBUG if verbose else logging.INFO
    new_format = VERBOSE_FORMAT if verbose else DEFAULT_FORMAT
    
    logger.setLevel(new_level)
    
    for handler in logger.handlers:
        handler.setLevel(new_level)
        handler.setFormatter(logging.Formatter(new_format, datefmt=DEFAULT_DATEFMT))


@contextmanager
def temporary_log_level(
    logger: logging.Logger,
    level: int
) -> Generator[logging.Logger, None, None]:
    """
    Temporarily change logger level within a context.
    
    Args:
        logger: Logger to modify
        level: Temporary logging level
        
    Yields:
        The modified logger
        
    Example:
        >>> with temporary_log_level(logger, logging.DEBUG):
        ...     logger.debug("This will be shown")
        >>> logger.debug("This won't be shown")
    """
    old_level = logger.level
    old_handler_levels = [(h, h.level) for h in logger.handlers]
    
    try:
        logger.setLevel(level)
        for handler in logger.handlers:
            handler.setLevel(level)
        yield logger
    finally:
        logger.setLevel(old_level)
        for handler, old_handler_level in old_handler_levels:
            handler.setLevel(old_handler_level)


# ═══════════════════════════════════════════════════════════════════════════════
# PROGRESS_LOGGER
# ═══════════════════════════════════════════════════════════════════════════════

class ProgressLogger:
    """
    Context manager for logging progress of multi-step operations.
    
    Provides structured logging with automatic start/completion messages
    and optional step counting.
    
    Attributes:
        logger: The underlying logger instance
        operation: Name of the operation being tracked
        total_steps: Total number of expected steps (0 for unknown)
        current_step: Current step counter
        
    Example:
        >>> with ProgressLogger(logger, "Installing flows", total_steps=3) as p:
        ...     p.step("Configuring switch s1")
        ...     p.step("Adding ARP rules")
        ...     p.step("Adding forwarding rules")
        [10:30:45] INFO: Starting: Installing flows
        [10:30:45] INFO:   [1/3] Configuring switch s1
        [10:30:46] INFO:   [2/3] Adding ARP rules
        [10:30:46] INFO:   [3/3] Adding forwarding rules
        [10:30:47] INFO: Completed: Installing flows
    """
    
    def __init__(
        self,
        logger: logging.Logger,
        operation: str,
        total_steps: int = 0,
        log_level: int = logging.INFO,
    ) -> None:
        """
        Initialise progress logger.
        
        Args:
            logger: Logger to use for output
            operation: Name of the operation being tracked
            total_steps: Total number of steps (0 for unknown/variable)
            log_level: Logging level for progress messages
        """
        self.logger = logger
        self.operation = operation
        self.total_steps = total_steps
        self.log_level = log_level
        self.current_step = 0
        self._started = False
        self._completed = False
    
    def __enter__(self) -> "ProgressLogger":
        """Start the operation and return self for step tracking."""
        self.logger.log(self.log_level, f"Starting: {self.operation}")
        self._started = True
        return self
    
    def __exit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Any,
    ) -> bool:
        """
        Log completion or failure of the operation.
        
        Returns:
            False (exceptions are not suppressed)
        """
        if exc_type is None:
            self.logger.log(self.log_level, f"Completed: {self.operation}")
            self._completed = True
        else:
            self.logger.error(f"Failed: {self.operation} - {exc_val}")
        return False
    
    def step(self, message: str) -> None:
        """
        Log a progress step.
        
        Args:
            message: Description of the current step
            
        Raises:
            RuntimeError: If called outside context manager
        """
        if not self._started:
            raise RuntimeError("ProgressLogger.step() called outside context manager")
        
        self.current_step += 1
        
        if self.total_steps > 0:
            self.logger.log(
                self.log_level,
                f"  [{self.current_step}/{self.total_steps}] {message}"
            )
        else:
            self.logger.log(self.log_level, f"  [{self.current_step}] {message}")
    
    def substep(self, message: str) -> None:
        """
        Log a sub-step (indented further than regular steps).
        
        Args:
            message: Description of the sub-step
        """
        self.logger.log(self.log_level, f"    → {message}")
    
    def warning(self, message: str) -> None:
        """
        Log a warning during the operation.
        
        Args:
            message: Warning message
        """
        self.logger.warning(f"  ⚠ {message}")


# ═══════════════════════════════════════════════════════════════════════════════
# COLOURED_OUTPUT
# ═══════════════════════════════════════════════════════════════════════════════

class ColouredFormatter(logging.Formatter):
    """
    Formatter that adds ANSI colour codes to log output.
    
    Only applies colours when output is to a TTY terminal.
    """
    
    COLOURS = {
        logging.DEBUG: "\033[36m",     # Cyan
        logging.INFO: "\033[32m",      # Green
        logging.WARNING: "\033[33m",   # Yellow
        logging.ERROR: "\033[31m",     # Red
        logging.CRITICAL: "\033[35m",  # Magenta
    }
    RESET = "\033[0m"
    
    def __init__(
        self,
        fmt: str = DEFAULT_FORMAT,
        datefmt: str = DEFAULT_DATEFMT,
        use_colours: bool = True,
    ) -> None:
        """
        Initialise formatter.
        
        Args:
            fmt: Log message format
            datefmt: Date/time format
            use_colours: Whether to use ANSI colours
        """
        super().__init__(fmt, datefmt)
        self.use_colours = use_colours and sys.stdout.isatty()
    
    def format(self, record: logging.LogRecord) -> str:
        """Format the log record with optional colours."""
        message = super().format(record)
        
        if self.use_colours:
            colour = self.COLOURS.get(record.levelno, "")
            if colour:
                message = f"{colour}{message}{self.RESET}"
        
        return message


def setup_coloured_logger(
    name: str,
    level: int = logging.INFO,
) -> logging.Logger:
    """
    Set up a logger with coloured output.
    
    Args:
        name: Logger name
        level: Logging level
        
    Returns:
        Configured logger with colour support
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        handler.setFormatter(ColouredFormatter())
        logger.addHandler(handler)
    
    return logger


# ═══════════════════════════════════════════════════════════════════════════════
# MODULE_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Demonstrate logging capabilities
    print("Logger module demonstration:")
    print("=" * 50)
    
    demo_logger = setup_coloured_logger("demo")
    
    demo_logger.debug("Debug message (not shown at INFO level)")
    demo_logger.info("Info message")
    demo_logger.warning("Warning message")
    demo_logger.error("Error message")
    
    print()
    
    with ProgressLogger(demo_logger, "Demo operation", total_steps=3) as progress:
        progress.step("First step")
        progress.substep("Sub-step detail")
        progress.step("Second step")
        progress.step("Third step")
