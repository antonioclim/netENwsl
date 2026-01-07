#!/usr/bin/env python3
"""
Logging Utilities for Week 14 Laboratory.

NETWORKING class - ASE, Informatics | by Revolvix

This module provides consistent, colour-coded logging across
all laboratory scripts with support for file and console output.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional
from enum import Enum


class Colours:
    """ANSI colour codes for terminal output."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"
    
    # Foreground colours
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Bright foreground colours
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    
    # Background colours
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"


class ColourSupport(Enum):
    """Colour support modes."""
    AUTO = "auto"
    ALWAYS = "always"
    NEVER = "never"


def supports_colour() -> bool:
    """
    Check if the terminal supports colour output.
    
    Returns:
        True if colour output is supported
    """
    # Check for explicit no-colour environment variable
    import os
    if os.environ.get('NO_COLOR'):
        return False
    
    # Check if stdout is a TTY
    if not hasattr(sys.stdout, 'isatty'):
        return False
    
    if not sys.stdout.isatty():
        return False
    
    # Check for Windows
    if sys.platform == 'win32':
        # Windows 10+ supports ANSI codes
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            # Enable virtual terminal processing
            kernel32.SetConsoleMode(
                kernel32.GetStdHandle(-11),
                7  # ENABLE_VIRTUAL_TERMINAL_PROCESSING
            )
            return True
        except Exception:
            return False
    
    # Unix-like systems generally support colour
    return True


class ColouredFormatter(logging.Formatter):
    """
    Custom formatter that adds colour to log output.
    
    Different log levels are displayed in different colours
    for easy visual identification.
    """
    
    LEVEL_COLOURS = {
        logging.DEBUG: Colours.DIM + Colours.CYAN,
        logging.INFO: Colours.BRIGHT_WHITE,
        logging.WARNING: Colours.BRIGHT_YELLOW,
        logging.ERROR: Colours.BRIGHT_RED,
        logging.CRITICAL: Colours.BOLD + Colours.BG_RED + Colours.WHITE,
    }
    
    STATUS_COLOURS = {
        'PASS': Colours.BRIGHT_GREEN,
        'FAIL': Colours.BRIGHT_RED,
        'WARN': Colours.BRIGHT_YELLOW,
        'INFO': Colours.BRIGHT_CYAN,
        'SKIP': Colours.DIM + Colours.WHITE,
    }
    
    def __init__(
        self,
        fmt: Optional[str] = None,
        datefmt: Optional[str] = None,
        use_colour: bool = True
    ):
        """
        Initialise the formatter.
        
        Args:
            fmt: Log message format string
            datefmt: Date format string
            use_colour: Whether to apply colour formatting
        """
        super().__init__(fmt, datefmt)
        self.use_colour = use_colour
    
    def format(self, record: logging.LogRecord) -> str:
        """Format the log record with optional colour."""
        # Store original values
        original_msg = record.msg
        original_levelname = record.levelname
        
        if self.use_colour:
            # Colour the level name
            colour = self.LEVEL_COLOURS.get(record.levelno, '')
            record.levelname = f"{colour}{record.levelname}{Colours.RESET}"
            
            # Colour status markers in message
            msg = str(record.msg)
            for status, status_colour in self.STATUS_COLOURS.items():
                if f'[{status}]' in msg:
                    msg = msg.replace(
                        f'[{status}]',
                        f'{status_colour}[{status}]{Colours.RESET}'
                    )
            record.msg = msg
        
        # Format the record
        result = super().format(record)
        
        # Restore original values
        record.msg = original_msg
        record.levelname = original_levelname
        
        return result


class LabLogger(logging.Logger):
    """
    Extended logger with laboratory-specific methods.
    
    Provides convenience methods for common logging patterns
    in the laboratory environment.
    """
    
    def __init__(self, name: str, level: int = logging.DEBUG):
        """Initialise the laboratory logger."""
        super().__init__(name, level)
    
    def success(self, msg: str, *args, **kwargs) -> None:
        """Log a success message (INFO level with PASS marker)."""
        self.info(f"[PASS] {msg}", *args, **kwargs)
    
    def failure(self, msg: str, *args, **kwargs) -> None:
        """Log a failure message (ERROR level with FAIL marker)."""
        self.error(f"[FAIL] {msg}", *args, **kwargs)
    
    def skip(self, msg: str, *args, **kwargs) -> None:
        """Log a skipped item (INFO level with SKIP marker)."""
        self.info(f"[SKIP] {msg}", *args, **kwargs)
    
    def section(self, title: str) -> None:
        """Log a section header."""
        self.info("")
        self.info("=" * 60)
        self.info(title)
        self.info("=" * 60)
    
    def subsection(self, title: str) -> None:
        """Log a subsection header."""
        self.info("")
        self.info(f"--- {title} ---")
    
    def divider(self) -> None:
        """Log a visual divider."""
        self.info("-" * 60)
    
    def blank(self) -> None:
        """Log a blank line."""
        self.info("")
    
    def key_value(self, key: str, value: str) -> None:
        """Log a key-value pair."""
        self.info(f"  {key}: {value}")
    
    def step(self, number: int, description: str) -> None:
        """Log a numbered step."""
        self.info(f"Step {number}: {description}")
    
    def progress(
        self,
        current: int,
        total: int,
        prefix: str = "",
        width: int = 40
    ) -> None:
        """Log a progress bar."""
        if total == 0:
            percent = 100
        else:
            percent = int(100 * current / total)
        
        filled = int(width * current / total) if total > 0 else width
        bar = "█" * filled + "░" * (width - filled)
        
        self.info(f"\r{prefix} [{bar}] {percent}% ({current}/{total})")


# Module-level logger registry
_loggers: dict = {}
_default_level = logging.INFO
_colour_mode = ColourSupport.AUTO
_log_file: Optional[Path] = None


def setup_logger(
    name: str,
    level: int = logging.INFO,
    log_file: Optional[Path] = None,
    colour_mode: ColourSupport = ColourSupport.AUTO,
    format_string: Optional[str] = None
) -> LabLogger:
    """
    Set up and return a configured logger.
    
    Args:
        name: Logger name (typically __name__ or script name)
        level: Logging level
        log_file: Optional file path for log output
        colour_mode: Colour output mode
        format_string: Custom format string
        
    Returns:
        Configured LabLogger instance
    """
    global _default_level, _colour_mode, _log_file
    
    # Determine colour support
    if colour_mode == ColourSupport.AUTO:
        use_colour = supports_colour()
    elif colour_mode == ColourSupport.ALWAYS:
        use_colour = True
    else:
        use_colour = False
    
    # Create logger
    logging.setLoggerClass(LabLogger)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Default format
    if format_string is None:
        format_string = "%(message)s"
    
    # Console handler with colour
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_formatter = ColouredFormatter(format_string, use_colour=use_colour)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler (no colour)
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    # Store in registry
    _loggers[name] = logger
    _default_level = level
    _colour_mode = colour_mode
    _log_file = log_file
    
    return logger


def get_logger(name: str) -> LabLogger:
    """
    Get an existing logger or create a new one.
    
    Args:
        name: Logger name
        
    Returns:
        LabLogger instance
    """
    if name in _loggers:
        return _loggers[name]
    
    return setup_logger(name, _default_level, _log_file, _colour_mode)


def set_global_level(level: int) -> None:
    """Set the logging level for all registered loggers."""
    global _default_level
    _default_level = level
    
    for logger in _loggers.values():
        logger.setLevel(level)


# Convenience functions for quick coloured output
def print_success(message: str) -> None:
    """Print a success message."""
    if supports_colour():
        print(f"{Colours.BRIGHT_GREEN}[PASS]{Colours.RESET} {message}")
    else:
        print(f"[PASS] {message}")


def print_failure(message: str) -> None:
    """Print a failure message."""
    if supports_colour():
        print(f"{Colours.BRIGHT_RED}[FAIL]{Colours.RESET} {message}")
    else:
        print(f"[FAIL] {message}")


def print_warning(message: str) -> None:
    """Print a warning message."""
    if supports_colour():
        print(f"{Colours.BRIGHT_YELLOW}[WARN]{Colours.RESET} {message}")
    else:
        print(f"[WARN] {message}")


def print_info(message: str) -> None:
    """Print an info message."""
    if supports_colour():
        print(f"{Colours.BRIGHT_CYAN}[INFO]{Colours.RESET} {message}")
    else:
        print(f"[INFO] {message}")


def print_header(title: str, char: str = "=", width: int = 60) -> None:
    """Print a section header."""
    print()
    print(char * width)
    print(title)
    print(char * width)


def print_table(
    headers: list,
    rows: list,
    column_widths: Optional[list] = None
) -> None:
    """
    Print a formatted table.
    
    Args:
        headers: Column headers
        rows: List of row data (each row is a list)
        column_widths: Optional fixed column widths
    """
    if column_widths is None:
        # Calculate widths based on content
        column_widths = []
        for i, header in enumerate(headers):
            max_width = len(str(header))
            for row in rows:
                if i < len(row):
                    max_width = max(max_width, len(str(row[i])))
            column_widths.append(max_width + 2)
    
    # Print headers
    header_line = " | ".join(
        str(h).ljust(w) for h, w in zip(headers, column_widths)
    )
    print(header_line)
    print("-" * len(header_line))
    
    # Print rows
    for row in rows:
        row_line = " | ".join(
            str(cell).ljust(w) if i < len(row) else " " * w
            for i, (cell, w) in enumerate(zip(row + [""] * len(headers), column_widths))
        )
        print(row_line)


# Create a default logger for immediate use
default_logger = setup_logger("lab")
