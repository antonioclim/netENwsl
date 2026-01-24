#!/usr/bin/env python3
"""
Network utilities for Week 9 Laboratory
NETWORKING class - ASE, Informatics | by Revolvix

Provides helper functions for network testing, port checking,
and connectivity verification.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import socket
import subprocess
import time
from typing import Optional, Tuple, List

from .logger import setup_logger

logger = setup_logger("network_utils")



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_port(
    host: str,
    port: int,
    timeout: float = 2.0
) -> bool:
    """
    Check if a port is open and accepting connections.
    
    Args:
        host: Target hostname or IP address
        port: Port number to check
        timeout: Connection timeout in seconds
    
    Returns:
        True if port is open
    
    Example:
        >>> check_port("localhost", 2121)
        True
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            return result == 0
    except socket.error:
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def wait_for_port(
    host: str,
    port: int,
    timeout: float = 30.0,
    interval: float = 1.0
) -> bool:
    """
    Wait for a port to become available.
    
    Args:
        host: Target hostname or IP address
        port: Port number to check
        timeout: Maximum wait time in seconds
        interval: Time between checks in seconds
    
    Returns:
        True if port became available within timeout
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        if check_port(host, port):
            logger.debug(f"Port {host}:{port} is now available")
            return True
        time.sleep(interval)
    
    logger.warning(f"Port {host}:{port} not available after {timeout}s")
    return False



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def get_local_ip() -> str:
    """
    Get the local IP address of this machine.
    
    Returns:
        Local IP address as string
    """
    try:
        # Create a socket and connect to an external address
        # to determine the local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except socket.error:
        return "127.0.0.1"



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def find_free_port(
    start: int = 10000,
    end: int = 65535
) -> Optional[int]:
    """
    Find a free port in the given range.
    
    Args:
        start: Start of port range
        end: End of port range
    
    Returns:
        Free port number or None if no port available
    """
    for port in range(start, end):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    return None



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def resolve_hostname(hostname: str) -> Optional[str]:
    """
    Resolve a hostname to an IP address.
    
    Args:
        hostname: Hostname to resolve
    
    Returns:
        IP address or None if resolution failed
    """
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def ping_host(
    host: str,
    count: int = 3,
    timeout: int = 5
) -> Tuple[bool, float]:
    """
    Ping a host and measure latency.
    
    Args:
        host: Target hostname or IP address
        count: Number of ping packets
        timeout: Timeout per packet in seconds
    
    Returns:
        Tuple of (success, average_latency_ms)
    """
    import platform
    
    # Windows uses -n, Unix uses -c
    count_flag = "-n" if platform.system().lower() == "windows" else "-c"
    timeout_flag = "-w" if platform.system().lower() == "windows" else "-W"
    
    try:
        result = subprocess.run(
            ["ping", count_flag, str(count), timeout_flag, str(timeout), host],
            capture_output=True,
            text=True,
            timeout=timeout * count + 5
        )
        
        if result.returncode == 0:
            # Try to extract average latency
            output = result.stdout
            
            # Windows format: "Average = Xms"
            # Linux format: "rtt min/avg/max/mdev = X/Y/Z/W ms"
            if "Average" in output:
                # Windows
                import re
                match = re.search(r'Average = (\d+)ms', output)
                if match:
                    return True, float(match.group(1))
            elif "avg" in output:
                # Linux
                import re
                match = re.search(r'rtt.*= [\d.]+/([\d.]+)/', output)
                if match:
                    return True, float(match.group(1))
            
            return True, 0.0
        else:
            return False, 0.0
            
    except (subprocess.SubprocessError, subprocess.TimeoutExpired):
        return False, 0.0



# ═══════════════════════════════════════════════════════════════════════════════
# NETWORK_OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════════
def get_active_connections(
    port: Optional[int] = None
) -> List[dict]:
    """
    Get list of active network connections.
    
    Args:
        port: Filter by specific port (optional)
    
    Returns:
        List of connection information dictionaries
    """
    connections = []
    
    try:
        result = subprocess.run(
            ["netstat", "-an"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'ESTABLISHED' in line or 'LISTEN' in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        conn = {
                            'proto': parts[0],
                            'local': parts[3] if len(parts) > 3 else '',
                            'remote': parts[4] if len(parts) > 4 else '',
                            'state': parts[-1]
                        }
                        
                        if port is None:
                            connections.append(conn)
                        elif str(port) in conn['local']:
                            connections.append(conn)
                            
    except subprocess.SubprocessError:
        pass
    
    return connections



# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def test_ftp_connection(
    host: str,
    port: int,
    timeout: float = 5.0
) -> Tuple[bool, str]:
    """
    Test connection to an FTP-like server.
    
    Args:
        host: Server hostname or IP
        port: Server port
        timeout: Connection timeout
    
    Returns:
        Tuple of (success, banner_message)
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect((host, port))
            
            # Try to receive welcome banner
            sock.settimeout(2.0)
            try:
                banner = sock.recv(1024).decode('utf-8', errors='replace')
                return True, banner.strip()
            except socket.timeout:
                return True, "(no banner)"
                
    except socket.error as e:
        return False, str(e)



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def get_network_interfaces() -> List[dict]:
    """
    Get list of network interfaces and their IP addresses.
    
    Returns:
        List of interface information dictionaries
    """
    interfaces = []
    
    try:
        import platform
        
        if platform.system().lower() == "windows":
            result = subprocess.run(
                ["ipconfig"],
                capture_output=True,
                text=True,
                timeout=10
            )
        else:
            result = subprocess.run(
                ["ip", "addr"],
                capture_output=True,
                text=True,
                timeout=10
            )
        
        # Basic parsing (platform-specific)
        # For detailed parsing, use the netifaces package
        interfaces.append({
            'output': result.stdout
        })
        
    except subprocess.SubprocessError:
        pass
    
    return interfaces


# =============================================================================
# Module test
# =============================================================================

if __name__ == "__main__":
    print("Network Utilities Test")
    print("=" * 40)
    
    print(f"Local IP: {get_local_ip()}")
    
    free_port = find_free_port(9000, 9100)
    print(f"Free port in range 9000-9100: {free_port}")
    
    print(f"Port 80 on localhost: {'open' if check_port('localhost', 80) else 'closed'}")
    
    success, latency = ping_host("localhost", count=2)
    print(f"Ping localhost: {'success' if success else 'failed'} (avg: {latency}ms)")
