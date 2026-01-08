#!/usr/bin/env python3
"""
Network Testing Utilities
NETWORKING class - ASE, Informatics | by Revolvix

Provides utilities for network testing and validation.
"""

import socket
import subprocess
from typing import Tuple, Optional, List
from .logger import get_logger


logger = get_logger("network")


def check_port_open(host: str, port: int, timeout: float = 2.0) -> bool:
    """
    Check if a TCP port is open and accepting connections.
    
    Args:
        host: Target hostname or IP
        port: Target port number
        timeout: Connection timeout in seconds
    
    Returns:
        True if port is open, False otherwise
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except socket.error:
        return False


def wait_for_port(
    host: str, 
    port: int, 
    timeout: float = 30.0,
    interval: float = 1.0
) -> bool:
    """
    Wait for a port to become available.
    
    Args:
        host: Target hostname or IP
        port: Target port number
        timeout: Maximum time to wait
        interval: Time between checks
    
    Returns:
        True if port became available, False if timeout
    """
    import time
    start = time.time()
    
    while time.time() - start < timeout:
        if check_port_open(host, port):
            return True
        time.sleep(interval)
    
    return False


def tcp_echo_test(
    host: str, 
    port: int, 
    message: str = "ECHO_TEST",
    timeout: float = 5.0
) -> Tuple[bool, str]:
    """
    Test a TCP echo server.
    
    Args:
        host: Server hostname or IP
        port: Server port
        message: Message to send
        timeout: Operation timeout
    
    Returns:
        Tuple of (success, response_or_error)
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        sock.sendall(message.encode())
        response = sock.recv(1024).decode()
        sock.close()
        return True, response
    except socket.error as e:
        return False, str(e)


def udp_send(
    host: str, 
    port: int, 
    message: str,
    broadcast: bool = False
) -> bool:
    """
    Send a UDP datagram.
    
    Args:
        host: Destination hostname or IP
        port: Destination port
        message: Message to send
        broadcast: Enable broadcast mode
    
    Returns:
        True if send succeeded
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if broadcast:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(message.encode(), (host, port))
        sock.close()
        return True
    except socket.error:
        return False


def get_local_ip() -> Optional[str]:
    """Get the local IP address of this machine."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
        sock.close()
        return ip
    except socket.error:
        return None


def ping_host(host: str, count: int = 3, timeout: int = 5) -> Tuple[bool, float]:
    """
    Ping a host and return success status and average RTT.
    
    Args:
        host: Target hostname or IP
        count: Number of pings
        timeout: Timeout in seconds
    
    Returns:
        Tuple of (success, average_rtt_ms)
    """
    try:
        result = subprocess.run(
            ["ping", "-c", str(count), "-W", str(timeout), host],
            capture_output=True,
            text=True,
            timeout=timeout * count + 5
        )
        
        if result.returncode == 0:
            # Parse average RTT from output
            lines = result.stdout.split('\n')
            for line in lines:
                if 'avg' in line or 'average' in line.lower():
                    # Format: min/avg/max/mdev
                    parts = line.split('=')[-1].strip().split('/')
                    if len(parts) >= 2:
                        return True, float(parts[1])
            return True, 0.0
        return False, 0.0
    except (subprocess.TimeoutExpired, Exception):
        return False, 0.0


def resolve_hostname(hostname: str) -> Optional[str]:
    """Resolve a hostname to an IP address."""
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None


def list_interfaces() -> List[Tuple[str, str]]:
    """
    List network interfaces and their IP addresses.
    
    Returns:
        List of (interface_name, ip_address) tuples
    """
    import socket
    import fcntl
    import struct
    import array
    
    interfaces = []
    
    try:
        # This works on Linux
        result = subprocess.run(
            ["ip", "-o", "addr", "show"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                parts = line.split()
                if len(parts) >= 4 and 'inet' in parts:
                    idx = parts.index('inet')
                    if idx + 1 < len(parts):
                        iface = parts[1]
                        addr = parts[idx + 1].split('/')[0]
                        interfaces.append((iface, addr))
    except Exception:
        pass
    
    return interfaces
