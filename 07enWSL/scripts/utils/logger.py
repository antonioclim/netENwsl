#!/usr/bin/env python3
"""
Enhanced Logger Utility — Week 7
================================
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Provides consistent logging across all laboratory scripts with:
- Configurable log levels (DEBUG, INFO, WARNING, ERROR)
- Dual output (console + optional file)
- ISO 8601 timestamps
- Coloured console output (if colorama available)
- Context managers for scoped logging

Usage:
    from scripts.utils.logger import LabLogger, LogLevel
    
    logger = LabLogger(name="start_lab", level=LogLevel.DEBUG)
    logger.info("Starting laboratory...")
    logger.debug("Configuration loaded")
    logger.warning("Port 9000 is reserved")
    logger.error("Docker not running!")
    
    # With file output
    logger = LabLogger(name="demo", log_file="artifacts/demo.log")
    
    # Context manager for timed operations
    with logger.timed("Container startup"):
        # ... operation ...
"""

from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import sys
import time
from contextlib import contextmanager
from datetime import datetime
from enum import IntEnum
from pathlib import Path
from typing import IO, Optional, Union

# Optional colorama for coloured output
try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False


# ═══════════════════════════════════════════════════════════════════════════════
# LOG LEVEL ENUMERATION
# ═══════════════════════════════════════════════════════════════════════════════
class LogLevel(IntEnum):
    """Log severity levels (lower value = more verbose)."""
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50
    SILENT = 100  # Suppress all output


# ═══════════════════════════════════════════════════════════════════════════════
# COLOUR DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════════════
if COLORAMA_AVAILABLE:
    LEVEL_COLOURS = {
        LogLevel.DEBUG: Fore.CYAN,
        LogLevel.INFO: Fore.GREEN,
        LogLevel.WARNING: Fore.YELLOW,
        LogLevel.ERROR: Fore.RED,
        LogLevel.CRITICAL: Fore.RED + Style.BRIGHT,
    }
    RESET = Style.RESET_ALL
else:
    LEVEL_COLOURS = {}
    RESET = ""


LEVEL_NAMES = {
    LogLevel.DEBUG: "DEBUG",
    LogLevel.INFO: "INFO",
    LogLevel.WARNING: "WARN",
    LogLevel.ERROR: "ERROR",
    LogLevel.CRITICAL: "CRIT",
}

LEVEL_ICONS = {
    LogLevel.DEBUG: "🔍",
    LogLevel.INFO: "ℹ️ ",
    LogLevel.WARNING: "⚠️ ",
    LogLevel.ERROR: "❌",
    LogLevel.CRITICAL: "🚨",
}


# ═══════════════════════════════════════════════════════════════════════════════
# LAB LOGGER CLASS
# ═══════════════════════════════════════════════════════════════════════════════
class LabLogger:
    """
    Enhanced logger for laboratory scripts.
    
    Attributes:
        name: Logger identifier (appears in output)
        level: Minimum level to log
        log_file: Optional file path for persistent logging
        use_icons: Whether to show emoji icons
        use_colours: Whether to use terminal colours
    """
    
    def __init__(
        self,
        name: str = "lab",
        level: Union[LogLevel, int] = LogLevel.INFO,
        log_file: Optional[Union[str, Path]] = None,
        use_icons: bool = True,
        use_colours: bool = True
    ) -> None:
        """
        Initialize the logger.
        
        Args:
            name: Logger identifier
            level: Minimum log level (default: INFO)
            log_file: Path to log file (creates parent directories if needed)
            use_icons: Show emoji icons in output
            use_colours: Use terminal colours (requires colorama)
        """
        self.name = name
        self.level = LogLevel(level) if isinstance(level, int) else level
        self.use_icons = use_icons
        self.use_colours = use_colours and COLORAMA_AVAILABLE
        
        self._file_handle: Optional[IO] = None
        if log_file:
            self._setup_file_logging(Path(log_file))
    
    def _setup_file_logging(self, path: Path) -> None:
        """Setup file logging, creating directories as needed."""
        path.parent.mkdir(parents=True, exist_ok=True)
        self._file_handle = open(path, "a", encoding="utf-8")
        self._log(LogLevel.DEBUG, f"Log file opened: {path}")
    
    def _format_timestamp(self) -> str:
        """Return ISO 8601 formatted timestamp."""
        return datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
    
    def _format_message(
        self,
        level: LogLevel,
        message: str,
        for_console: bool = True
    ) -> str:
        """
        Format a log message.
        
        Args:
            level: Log severity level
            message: Message content
            for_console: If True, include colours/icons for console
            
        Returns:
            Formatted log string
        """
        timestamp = self._format_timestamp()
        level_name = LEVEL_NAMES.get(level, "???")
        
        if for_console:
            icon = LEVEL_ICONS.get(level, "  ") if self.use_icons else ""
            colour = LEVEL_COLOURS.get(level, "") if self.use_colours else ""
            reset = RESET if self.use_colours else ""
            
            return f"{timestamp} {colour}[{level_name}]{reset} {icon} [{self.name}] {message}"
        else:
            # Plain format for file output
            return f"{timestamp} [{level_name}] [{self.name}] {message}"
    
    def _log(self, level: LogLevel, message: str) -> None:
        """
        Internal log method.
        
        Args:
            level: Log severity level
            message: Message to log
        """
        if level < self.level:
            return
        
        # Console output
        console_msg = self._format_message(level, message, for_console=True)
        output = sys.stderr if level >= LogLevel.ERROR else sys.stdout
        print(console_msg, file=output, flush=True)
        
        # File output
        if self._file_handle:
            file_msg = self._format_message(level, message, for_console=False)
            self._file_handle.write(file_msg + "\n")
            self._file_handle.flush()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PUBLIC LOGGING METHODS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def debug(self, message: str) -> None:
        """Log a debug message."""
        self._log(LogLevel.DEBUG, message)
    
    def info(self, message: str) -> None:
        """Log an informational message."""
        self._log(LogLevel.INFO, message)
    
    def warning(self, message: str) -> None:
        """Log a warning message."""
        self._log(LogLevel.WARNING, message)
    
    def error(self, message: str) -> None:
        """Log an error message."""
        self._log(LogLevel.ERROR, message)
    
    def critical(self, message: str) -> None:
        """Log a critical error message."""
        self._log(LogLevel.CRITICAL, message)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # UTILITY METHODS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def section(self, title: str) -> None:
        """Log a section header for visual separation."""
        separator = "═" * 60
        self._log(LogLevel.INFO, separator)
        self._log(LogLevel.INFO, f"  {title}")
        self._log(LogLevel.INFO, separator)
    
    def step(self, step_num: int, total: int, description: str) -> None:
        """Log a numbered step in a process."""
        self._log(LogLevel.INFO, f"[{step_num}/{total}] {description}")
    
    def success(self, message: str) -> None:
        """Log a success message (INFO level with checkmark)."""
        icon = "✅" if self.use_icons else "[OK]"
        self._log(LogLevel.INFO, f"{icon} {message}")
    
    def failure(self, message: str) -> None:
        """Log a failure message (ERROR level with cross)."""
        icon = "❌" if self.use_icons else "[FAIL]"
        self._log(LogLevel.ERROR, f"{icon} {message}")
    
    @contextmanager
    def timed(self, operation: str):
        """
        Context manager for timing an operation.
        
        Usage:
            with logger.timed("Container startup"):
                start_containers()
        
        Args:
            operation: Description of the operation being timed
            
        Yields:
            None
        """
        self.debug(f"Starting: {operation}")
        start = time.perf_counter()
        try:
            yield
        finally:
            elapsed = time.perf_counter() - start
            self.debug(f"Completed: {operation} ({elapsed:.2f}s)")
    
    @contextmanager
    def indented(self, prefix: str = "  "):
        """
        Context manager for indented log output.
        
        Args:
            prefix: String to prepend to messages
        """
        original_name = self.name
        self.name = f"{prefix}{original_name}"
        try:
            yield
        finally:
            self.name = original_name
    
    # ═══════════════════════════════════════════════════════════════════════════
    # LIFECYCLE METHODS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def set_level(self, level: Union[LogLevel, int]) -> None:
        """Change the minimum log level."""
        self.level = LogLevel(level) if isinstance(level, int) else level
        self.debug(f"Log level changed to {self.level.name}")
    
    def close(self) -> None:
        """Close the log file if open."""
        if self._file_handle:
            self._file_handle.close()
            self._file_handle = None
    
    def __enter__(self) -> "LabLogger":
        """Context manager entry."""
        return self
    
    def __exit__(self, *args) -> None:
        """Context manager exit - close file handle."""
        self.close()


# ═══════════════════════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def get_logger(
    name: str = "lab",
    level: Union[LogLevel, int] = LogLevel.INFO,
    log_file: Optional[str] = None
) -> LabLogger:
    """
    Factory function to create a configured logger.
    
    Args:
        name: Logger identifier
        level: Minimum log level
        log_file: Optional file path
        
    Returns:
        Configured LabLogger instance
    """
    return LabLogger(name=name, level=level, log_file=log_file)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN (DEMO)
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Demonstrate logger capabilities
    print("=" * 60)
    print("LabLogger Demonstration")
    print("=" * 60)
    print()
    
    logger = LabLogger(name="demo", level=LogLevel.DEBUG)
    
    logger.section("Basic Logging")
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    logger.section("Utility Methods")
    logger.step(1, 3, "First step")
    logger.step(2, 3, "Second step")
    logger.step(3, 3, "Third step")
    logger.success("Operation completed successfully")
    logger.failure("Something went wrong")
    
    logger.section("Timed Operation")
    with logger.timed("Simulated delay"):
        time.sleep(0.5)
    
    print()
    print("Demonstration complete.")



def setup_logger(
    name: str = "week7",
    *,
    level: Optional[int] = None,
    log_file: Optional[str] = None,
) -> logging.Logger:
    """Backwards compatible wrapper for older scripts.

    Several helper scripts historically imported `setup_logger`. The newer
    implementation uses `get_logger`. This wrapper keeps the public API stable.
    """
    if level is None:
        return get_logger(name=name, log_file=log_file)
    return get_logger(name=name, level=level, log_file=log_file)
