#!/usr/bin/env python3
"""
Week 13 — Network Utilities
===========================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

This module contains small helpers used across the kit. It is written to be:
- dependency-light (standard library only)
- predictable and easy to test
- well-documented for educational purposes

Functions
---------
- resolve_host(hostname) -> ip string
- tcp_connectable(host, port, timeout) -> bool
- parse_ports(spec) -> list[int]
- guess_service(port) -> str
- validate_ip(address) -> bool
- format_port_list(ports) -> str
"""

from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORT_DEPENDENCIES
# ═══════════════════════════════════════════════════════════════════════════════
import ipaddress
import socket
from typing import List, Optional, Set


# ═══════════════════════════════════════════════════════════════════════════════
# HOST_RESOLUTION
# ═══════════════════════════════════════════════════════════════════════════════

def resolve_host(hostname: str) -> str:
    """
    Resolve a hostname to an IPv4 address (best effort).
    
    💭 PREDICTION: What will this return for "localhost"?
       (Answer: "127.0.0.1")
    
    Args:
        hostname: DNS name or IP address string to resolve
    
    Returns:
        IPv4 address as string. If resolution fails, returns the
        original hostname unchanged (allows IP addresses to pass through).
    
    Examples:
        >>> resolve_host("localhost")
        '127.0.0.1'
        >>> resolve_host("10.0.13.11")
        '10.0.13.11'
        >>> resolve_host("nonexistent.invalid")
        'nonexistent.invalid'
    """
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        # Resolution failed — return original (might already be an IP)
        return hostname


def validate_ip(address: str) -> bool:
    """
    Check if a string is a valid IPv4 or IPv6 address.
    
    Args:
        address: String to validate
    
    Returns:
        True if valid IP address, False otherwise
    
    Examples:
        >>> validate_ip("192.168.1.1")
        True
        >>> validate_ip("10.0.13.256")
        False
        >>> validate_ip("not_an_ip")
        False
    """
    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# CONNECTION_TESTING
# ═══════════════════════════════════════════════════════════════════════════════

def tcp_connectable(host: str, port: int, timeout: float = 1.0) -> bool:
    """
    Test if a TCP connection can be established to host:port.
    
    💭 PREDICTION: What happens if the port is filtered by a firewall?
       (Answer: Returns False after timeout expires)
    
    This function attempts a full TCP three-way handshake. It does not
    send any application data after connecting.
    
    Args:
        host: Target hostname or IP address
        port: Target port number (1-65535)
        timeout: Maximum seconds to wait for connection
    
    Returns:
        True if connection succeeds (port is open), False otherwise
        (port closed, filtered, or host unreachable)
    
    Examples:
        >>> tcp_connectable("127.0.0.1", 1883, timeout=0.5)
        True  # If MQTT broker is running
        >>> tcp_connectable("127.0.0.1", 99999, timeout=0.5)
        False  # Invalid port
    """
    if not (1 <= port <= 65535):
        return False
    
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# PORT_PARSING
# ═══════════════════════════════════════════════════════════════════════════════

def parse_ports(spec: str) -> List[int]:
    """
    Parse a port specification string into a sorted list of port numbers.
    
    Supports multiple formats:
    - Single port: "80"
    - Comma-separated: "22,80,443"
    - Range: "1-1024"
    - Mixed: "22,80,8000-8003"
    
    Args:
        spec: Port specification string
    
    Returns:
        Sorted list of unique port numbers
    
    Raises:
        ValueError: If specification contains invalid port numbers
    
    Examples:
        >>> parse_ports("80")
        [80]
        >>> parse_ports("22,80,443")
        [22, 80, 443]
        >>> parse_ports("8000-8003")
        [8000, 8001, 8002, 8003]
        >>> parse_ports("22,80,8000-8002")
        [22, 80, 8000, 8001, 8002]
    """
    ports: Set[int] = set()
    
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        
        if "-" in part:
            # Range specification
            try:
                start_str, end_str = part.split("-", 1)
                start = int(start_str.strip())
                end = int(end_str.strip())
                
                if not (1 <= start <= 65535) or not (1 <= end <= 65535):
                    raise ValueError(f"Port out of range: {part}")
                if start > end:
                    raise ValueError(f"Invalid range: {part}")
                
                ports.update(range(start, end + 1))
            except ValueError as e:
                raise ValueError(f"Invalid port range '{part}': {e}")
        else:
            # Single port
            try:
                port = int(part)
                if not (1 <= port <= 65535):
                    raise ValueError(f"Port out of range: {port}")
                ports.add(port)
            except ValueError:
                raise ValueError(f"Invalid port number: '{part}'")
    
    return sorted(ports)


def format_port_list(ports: List[int], max_display: int = 10) -> str:
    """
    Format a list of ports for display, truncating if too long.
    
    Args:
        ports: List of port numbers
        max_display: Maximum ports to show before truncating
    
    Returns:
        Formatted string representation
    
    Examples:
        >>> format_port_list([22, 80, 443])
        '22, 80, 443'
        >>> format_port_list(list(range(1, 20)), max_display=5)
        '1, 2, 3, 4, 5, ... (19 total)'
    """
    if len(ports) <= max_display:
        return ", ".join(str(p) for p in ports)
    else:
        shown = ", ".join(str(p) for p in ports[:max_display])
        return f"{shown}, ... ({len(ports)} total)"


# ═══════════════════════════════════════════════════════════════════════════════
# SERVICE_IDENTIFICATION
# ═══════════════════════════════════════════════════════════════════════════════

# Well-known ports relevant to Week 13 laboratory
_SERVICE_MAP = {
    20: "FTP-Data",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    993: "IMAPS",
    995: "POP3S",
    1883: "MQTT",
    2121: "FTP-Alt",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    6200: "Backdoor-Stub",
    6379: "Redis",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
    8883: "MQTT-TLS",
    9000: "Portainer",
    27017: "MongoDB",
}


def guess_service(port: int) -> str:
    """
    Return a human-readable service name for a well-known port.
    
    Args:
        port: Port number to look up
    
    Returns:
        Service name string, or "unknown" if port is not in the map
    
    Examples:
        >>> guess_service(80)
        'HTTP'
        >>> guess_service(1883)
        'MQTT'
        >>> guess_service(12345)
        'unknown'
    """
    return _SERVICE_MAP.get(port, "unknown")


def get_all_known_ports() -> List[int]:
    """
    Return a sorted list of all ports with known service mappings.
    
    Returns:
        Sorted list of port numbers from the service map
    """
    return sorted(_SERVICE_MAP.keys())


# ═══════════════════════════════════════════════════════════════════════════════
# SELF_TEST
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Minimal self-test (no network traffic required)
    print("Running net_utils self-tests...")
    
    # Test parse_ports
    assert parse_ports("22,80,8000-8002") == [22, 80, 8000, 8001, 8002]
    assert parse_ports("443") == [443]
    assert parse_ports("1-5") == [1, 2, 3, 4, 5]
    print("  ✓ parse_ports")
    
    # Test guess_service
    assert guess_service(80) == "HTTP"
    assert guess_service(1883) == "MQTT"
    assert guess_service(99999) == "unknown"
    print("  ✓ guess_service")
    
    # Test validate_ip
    assert validate_ip("192.168.1.1") is True
    assert validate_ip("10.0.13.11") is True
    assert validate_ip("not_an_ip") is False
    assert validate_ip("256.1.1.1") is False
    print("  ✓ validate_ip")
    
    # Test format_port_list
    assert format_port_list([22, 80, 443]) == "22, 80, 443"
    assert "total" in format_port_list(list(range(1, 100)), max_display=5)
    print("  ✓ format_port_list")
    
    print("\nnet_utils: All self-tests passed ✓")
