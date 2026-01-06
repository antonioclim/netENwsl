#!/usr/bin/env python3
"""
Network testing utilities for Week 2 laboratory scripts.
NETWORKING class - ASE, Informatics | by Revolvix
"""

import socket
import subprocess
import time
from typing import Optional, Tuple
from .logger import setup_logger

logger = setup_logger("network_utils")


class NetworkUtils:
    """Network testing and diagnostics utilities."""
    
    @staticmethod
    def check_port(host: str, port: int, timeout: float = 2.0) -> bool:
        """
        Check if a TCP port is open and accepting connections.
        
        Args:
            host: Target hostname or IP
            port: Port number
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
    def wait_for_port(
        host: str,
        port: int,
        timeout: float = 30.0,
        interval: float = 0.5
    ) -> bool:
        """
        Wait for a port to become available.
        
        Args:
            host: Target hostname or IP
            port: Port number
            timeout: Maximum wait time in seconds
            interval: Check interval in seconds
        
        Returns:
            True if port became available within timeout
        """
        start = time.time()
        while time.time() - start < timeout:
            if NetworkUtils.check_port(host, port):
                return True
            time.sleep(interval)
        return False
    
    @staticmethod
    def tcp_echo_test(
        host: str,
        port: int,
        message: bytes = b"test",
        timeout: float = 5.0
    ) -> Tuple[bool, Optional[bytes], float]:
        """
        Send TCP message and receive response.
        
        Args:
            host: Target hostname or IP
            port: Port number
            message: Message to send
            timeout: Operation timeout in seconds
        
        Returns:
            Tuple of (success, response_data, round_trip_time_ms)
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                t0 = time.perf_counter()
                sock.connect((host, port))
                sock.sendall(message)
                response = sock.recv(4096)
                rtt = (time.perf_counter() - t0) * 1000
                return True, response, rtt
        except socket.timeout:
            return False, None, 0.0
        except Exception as e:
            logger.debug(f"TCP test failed: {e}")
            return False, None, 0.0
    
    @staticmethod
    def udp_echo_test(
        host: str,
        port: int,
        message: bytes = b"ping",
        timeout: float = 2.0
    ) -> Tuple[bool, Optional[bytes], float]:
        """
        Send UDP datagram and receive response.
        
        Args:
            host: Target hostname or IP
            port: Port number
            message: Message to send
            timeout: Operation timeout in seconds
        
        Returns:
            Tuple of (success, response_data, round_trip_time_ms)
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.settimeout(timeout)
                t0 = time.perf_counter()
                sock.sendto(message, (host, port))
                response, _ = sock.recvfrom(4096)
                rtt = (time.perf_counter() - t0) * 1000
                return True, response, rtt
        except socket.timeout:
            return False, None, 0.0
        except Exception as e:
            logger.debug(f"UDP test failed: {e}")
            return False, None, 0.0
    
    @staticmethod
    def get_local_ip() -> str:
        """Get the local machine's primary IP address."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.connect(("8.8.8.8", 80))
                return sock.getsockname()[0]
        except Exception:
            return "127.0.0.1"
    
    @staticmethod
    def list_interfaces() -> list:
        """List available network interfaces."""
        interfaces = []
        try:
            result = subprocess.run(
                ["ip", "link", "show"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if ':' in line and '@' not in line:
                        parts = line.split(':')
                        if len(parts) >= 2:
                            iface = parts[1].strip()
                            if iface:
                                interfaces.append(iface)
        except FileNotFoundError:
            # Windows - try different approach
            try:
                result = subprocess.run(
                    ["ipconfig", "/all"],
                    capture_output=True,
                    text=True
                )
                # Parse Windows output
                interfaces = ["Loopback", "Ethernet", "Wi-Fi"]
            except Exception:
                pass
        
        return interfaces
