#!/usr/bin/env python3
"""
Network Testing Utilities
Computer Networks - ASE Bucharest, CSIE | by ing. dr. Antonio Clim

Provides network testing and verification functionality
for the Week 7 laboratory scripts.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import socket
import subprocess
import time
from typing import Tuple, Optional, List

from .logger import get_logger



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class NetworkUtils:
    """Network testing utilities for laboratory verification."""
    

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
    def __init__(self) -> None:
        self.logger = get_logger("network")
    

# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
    def check_port_open(
        self,
        host: str,
        port: int,
        timeout: float = 2.0
    ) -> bool:
        """
        Check if a TCP port is open.
        
        Args:
            host: Target host
            port: Target port
            timeout: Connection timeout in seconds
            
        Returns:
            True if port is open
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except Exception:
            return False
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def wait_for_port(
        self,
        host: str,
        port: int,
        timeout: int = 30,
        interval: float = 1.0
    ) -> bool:
        """
        Wait for a port to become available.
        
        Args:
            host: Target host
            port: Target port
            timeout: Maximum wait time in seconds
            interval: Check interval in seconds
            
        Returns:
            True if port becomes available within timeout
        """
        start_time = time.time()
        self.logger.debug(f"Waiting for {host}:{port}...")
        
        while time.time() - start_time < timeout:
            if self.check_port_open(host, port, timeout=2.0):
                self.logger.debug(f"Port {host}:{port} is open")
                return True
            time.sleep(interval)
        
        self.logger.warning(f"Timeout waiting for {host}:{port}")
        return False
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def probe_ports(
        self,
        host: str,
        ports: List[int],
        timeout: float = 0.5
    ) -> dict[int, str]:
        """
        Probe multiple ports and return their status.
        
        Args:
            host: Target host
            ports: List of ports to probe
            timeout: Timeout per port
            
        Returns:
            Dictionary mapping port to status string
        """
        results = {}
        
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                result = sock.connect_ex((host, port))
                
                if result == 0:
                    results[port] = "open"
                else:
                    results[port] = f"closed ({result})"
            except socket.timeout:
                results[port] = "timeout"
            except Exception as e:
                results[port] = f"error ({e})"
            finally:
                try:
                    sock.close()
                except Exception:
                    pass
        
        return results
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def tcp_echo_test(
        self,
        host: str,
        port: int,
        message: str = "test",
        timeout: float = 5.0
    ) -> Tuple[bool, str]:
        """
        Test TCP echo server functionality.
        
        Args:
            host: Server host
            port: Server port
            message: Message to send
            timeout: Socket timeout
            
        Returns:
            Tuple of (success, response_or_error)
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((host, port))
            sock.sendall(message.encode("utf-8"))
            response = sock.recv(4096).decode("utf-8")
            sock.close()
            
            if response.strip() == message:
                return True, response.strip()
            else:
                return False, f"unexpected response: {response.strip()}"
        except Exception as e:
            return False, str(e)
    

# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def udp_send_test(
        self,
        host: str,
        port: int,
        message: str = "test"
    ) -> Tuple[bool, str]:
        """
        Test UDP send functionality.
        
        Args:
            host: Receiver host
            port: Receiver port
            message: Message to send
            
        Returns:
            Tuple of (success, status_message)
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(message.encode("utf-8"), (host, port))
            sock.close()
            return True, "sent"
        except Exception as e:
            return False, str(e)
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def get_local_ip(self) -> Optional[str]:
        """
        Get the local IP address used for outbound connections.
        
        Returns:
            Local IP address or None
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(("8.8.8.8", 80))
            ip = sock.getsockname()[0]
            sock.close()
            return ip
        except Exception:
            return None
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def resolve_hostname(self, hostname: str) -> Optional[str]:
        """
        Resolve a hostname to IP address.
        
        Args:
            hostname: Hostname to resolve
            
        Returns:
            IP address or None
        """
        try:
            return socket.gethostbyname(hostname)
        except socket.gaierror:
            return None
    

# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
    def check_connectivity(
        self,
        host: str,
        count: int = 1,
        timeout: int = 2
    ) -> Tuple[bool, str]:
        """
        Check network connectivity using ping.
        
        Args:
            host: Target host
            count: Number of pings
            timeout: Timeout per ping
            
        Returns:
            Tuple of (success, output)
        """
        try:
            # Platform-specific ping command
            import platform
            if platform.system() == "Windows":
                args = ["ping", "-n", str(count), "-w", str(timeout * 1000), host]
            else:
                args = ["ping", "-c", str(count), "-W", str(timeout), host]
            
            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                timeout=timeout * count + 5
            )
            
            success = result.returncode == 0
            return success, result.stdout
        except Exception as e:
            return False, str(e)

if __name__ == "__main__":
    # Module loaded directly - display module info
    print(f"Module {__name__} loaded successfully.")
    print(f"This module provides utility functions for the networking laboratory.")
