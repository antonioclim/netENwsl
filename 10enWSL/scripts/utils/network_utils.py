"""
Network Testing Utilities
NETWORKING class - ASE, Informatics | by Revolvix

Provides network connectivity and service verification utilities.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import socket
import subprocess
from typing import Optional, Tuple

from .logger import setup_logger

logger = setup_logger("network_utils")



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class NetworkTester:
    """Provides network testing functionality."""
    
    @staticmethod


# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
    def check_tcp_port(host: str, port: int, timeout: float = 5.0) -> bool:
        """
        Check if a TCP port is open.
        
        Args:
            host: Target hostname or IP
            port: Target port
            timeout: Connection timeout in seconds
        
        Returns:
            True if port is open
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                result = sock.connect_ex((host, port))
                return result == 0
        except Exception:
            return False
    
    @staticmethod


# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
    def check_udp_dns(host: str, port: int, query: str, timeout: float = 5.0) -> Optional[str]:
        """
        Send a simple DNS-like UDP query (for the custom lab DNS server).
        
        Args:
            host: DNS server hostname or IP
            port: DNS server port
            query: Hostname to query
            timeout: Query timeout
        
        Returns:
            Response IP or None if failed
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.settimeout(timeout)
                sock.sendto(query.encode(), (host, port))
                data, _ = sock.recvfrom(512)
                return data.decode().strip()
        except Exception:
            return None
    
    @staticmethod


# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def http_get(url: str, timeout: float = 10.0) -> Tuple[int, str]:
        """
        Perform a simple HTTP GET request.
        
        Args:
            url: Target URL
            timeout: Request timeout
        
        Returns:
            Tuple of (status_code, body)
        """
        try:
            import urllib.request
            with urllib.request.urlopen(url, timeout=timeout) as response:
                return response.getcode(), response.read().decode()
        except urllib.error.HTTPError as e:
            return e.code, ""
        except Exception as e:
            logger.error(f"HTTP request failed: {e}")
            return 0, ""
    
    @staticmethod


# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def ping(host: str, count: int = 1, timeout: int = 5) -> bool:
        """
        Ping a host.
        
        Args:
            host: Target hostname or IP
            count: Number of ping packets
            timeout: Timeout in seconds
        
        Returns:
            True if ping succeeds
        """
        import platform
        
        param = "-n" if platform.system().lower() == "windows" else "-c"
        timeout_param = "-w" if platform.system().lower() == "windows" else "-W"
        
        cmd = ["ping", param, str(count), timeout_param, str(timeout * 1000 if platform.system().lower() == "windows" else timeout), host]
        
        result = subprocess.run(cmd, capture_output=True)
        return result.returncode == 0



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def wait_for_service(
    host: str,
    port: int,
    timeout: float = 60.0,
    interval: float = 2.0
) -> bool:
    """
    Wait for a TCP service to become available.
    
    Args:
        host: Target hostname or IP
        port: Target port
        timeout: Maximum wait time
        interval: Check interval
    
    Returns:
        True if service became available
    """
    import time
    
    start = time.time()
    tester = NetworkTester()
    
    while time.time() - start < timeout:
        if tester.check_tcp_port(host, port):
            return True
        time.sleep(interval)
    
    return False

if __name__ == "__main__":
    # Module loaded directly - display module info
    print(f"Module {__name__} loaded successfully.")
    print(f"This module provides utility functions for the networking laboratory.")
