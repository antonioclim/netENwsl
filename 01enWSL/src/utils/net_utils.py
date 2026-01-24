#!/usr/bin/env python3
"""
Network Utility Helpers — Week 1
================================
Computer Networks - ASE Bucharest | by ing. dr. Antonio Clim

This module provides reusable network utility functions for laboratory
exercises and scripts. It follows the transversal standard established
across all weekly kits.

Functions:
    setup_logging: Configure dual console/file logging
    is_valid_ip: Validate IPv4/IPv6 address strings
    is_valid_port: Validate TCP/UDP port numbers
    format_bytes: Human-readable byte formatting
    check_port_open: Test if a TCP port is accepting connections

Example:
    >>> from src.utils.net_utils import is_valid_ip, is_valid_port
    >>> is_valid_ip("192.168.1.1")
    True
    >>> is_valid_port(80)
    True
    >>> is_valid_port(70000)
    False
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import ipaddress
import logging
import socket
from pathlib import Path
from typing import Union


# ═══════════════════════════════════════════════════════════════════════════════
# LOGGING_CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
def setup_logging(log_path: Path, level: int = logging.INFO) -> logging.Logger:
    """
    Create a logger that writes to both console and a file.
    
    Configures a logger with two handlers: one for console output and
    one for file persistence. If handlers already exist, returns the
    existing logger to avoid duplicate log entries.
    
    Args:
        log_path: Path to the log file (created if doesn't exist)
        level: Logging level (default: logging.INFO)
        
    Returns:
        Configured logger instance
        
    Example:
        >>> from pathlib import Path
        >>> logger = setup_logging(Path("logs/week1.log"))
        >>> logger.info("Lab started")
        2025-01-24 10:30:00 INFO Lab started
        
    Note:
        Log format: "%(asctime)s %(levelname)s %(message)s"
    """
    logger = logging.getLogger("week1")
    logger.setLevel(level)

    # Avoid adding duplicate handlers
    if logger.handlers:
        return logger

    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

    # File handler
    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    # Console handler
    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    logger.addHandler(sh)

    return logger


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATION_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def is_valid_ip(value: str) -> bool:
    """
    Check if a string is a valid IPv4 or IPv6 address.
    
    Uses the ipaddress module for reliable validation that handles
    edge cases correctly.
    
    Args:
        value: String to validate as IP address
        
    Returns:
        True if valid IPv4 or IPv6 address, False otherwise
        
    Examples:
        >>> is_valid_ip("192.168.1.1")
        True
        >>> is_valid_ip("10.0.0.1")
        True
        >>> is_valid_ip("::1")
        True
        >>> is_valid_ip("256.1.1.1")
        False
        >>> is_valid_ip("not.an.ip")
        False
        >>> is_valid_ip("")
        False
        
    Note:
        This validates address format only, not reachability.
        CIDR notation (e.g., "192.168.1.0/24") is NOT valid here.
    """
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False


def is_valid_port(port: Union[int, str]) -> bool:
    """
    Check if a value is a valid TCP/UDP port number.
    
    Valid ports are integers in the range 1-65535 inclusive.
    Port 0 is technically valid but reserved, so excluded here.
    
    Args:
        port: Port number to validate (int or string convertible to int)
        
    Returns:
        True if valid port number, False otherwise
        
    Examples:
        >>> is_valid_port(80)
        True
        >>> is_valid_port(443)
        True
        >>> is_valid_port(65535)
        True
        >>> is_valid_port(0)
        False
        >>> is_valid_port(65536)
        False
        >>> is_valid_port(-1)
        False
        >>> is_valid_port("8080")
        True
        
    Note:
        Ports 1-1023 are "well-known" and typically require root.
        Ports 1024-49151 are "registered" for specific services.
        Ports 49152-65535 are "dynamic" (ephemeral client ports).
    """
    try:
        port_int = int(port)
        return 1 <= port_int <= 65535
    except (ValueError, TypeError):
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# FORMATTING_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def format_bytes(num_bytes: int, precision: int = 2) -> str:
    """
    Convert byte count to human-readable string with units.
    
    Uses binary prefixes (KiB, MiB, GiB) which are standard in
    computing contexts (1 KiB = 1024 bytes).
    
    Args:
        num_bytes: Number of bytes to format
        precision: Decimal places for non-byte values (default: 2)
        
    Returns:
        Formatted string with appropriate unit
        
    Examples:
        >>> format_bytes(0)
        '0 B'
        >>> format_bytes(1023)
        '1023 B'
        >>> format_bytes(1024)
        '1.00 KiB'
        >>> format_bytes(1536)
        '1.50 KiB'
        >>> format_bytes(1048576)
        '1.00 MiB'
        >>> format_bytes(1073741824)
        '1.00 GiB'
    """
    if num_bytes < 0:
        return f"-{format_bytes(-num_bytes, precision)}"
    
    for unit in ['B', 'KiB', 'MiB', 'GiB', 'TiB']:
        if abs(num_bytes) < 1024.0:
            if unit == 'B':
                return f"{num_bytes} {unit}"
            return f"{num_bytes:.{precision}f} {unit}"
        num_bytes /= 1024.0
    
    return f"{num_bytes:.{precision}f} PiB"


# ═══════════════════════════════════════════════════════════════════════════════
# CONNECTIVITY_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def check_port_open(host: str, port: int, timeout: float = 2.0) -> bool:
    """
    Check if a TCP port is open and accepting connections.
    
    Attempts to establish a TCP connection to the specified host:port.
    Returns True if the connection succeeds (port is open), False if
    connection is refused or times out.
    
    Args:
        host: Hostname or IP address to check
        port: TCP port number to check
        timeout: Connection timeout in seconds (default: 2.0)
        
    Returns:
        True if port is open, False otherwise
        
    Examples:
        >>> # Assuming nothing on port 12345
        >>> check_port_open("127.0.0.1", 12345)
        False
        >>> # Assuming Portainer running on 9000
        >>> check_port_open("localhost", 9000)
        True
        
    Note:
        This only tests TCP ports. UDP "openness" cannot be reliably
        determined without application-level interaction.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except (socket.error, socket.timeout, OSError):
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# MODULE_TEST
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    # Quick self-test when run directly
    print("net_utils.py self-test")
    print("-" * 40)
    
    # Test is_valid_ip
    test_ips = ["192.168.1.1", "10.0.0.1", "::1", "256.1.1.1", "not.valid"]
    print("\nis_valid_ip tests:")
    for ip in test_ips:
        print(f"  {ip:20} -> {is_valid_ip(ip)}")
    
    # Test is_valid_port
    test_ports = [80, 443, 0, 65535, 65536, -1, "8080"]
    print("\nis_valid_port tests:")
    for port in test_ports:
        print(f"  {str(port):10} -> {is_valid_port(port)}")
    
    # Test format_bytes
    test_bytes = [0, 1023, 1024, 1536, 1048576, 1073741824]
    print("\nformat_bytes tests:")
    for b in test_bytes:
        print(f"  {b:15,} -> {format_bytes(b)}")
    
    # Test check_port_open
    print("\ncheck_port_open tests:")
    print(f"  localhost:9000 -> {check_port_open('localhost', 9000)}")
    print(f"  localhost:12345 -> {check_port_open('localhost', 12345)}")
    
    print("\n" + "-" * 40)
    print("Self-test complete")
