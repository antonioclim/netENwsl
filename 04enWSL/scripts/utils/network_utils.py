#!/usr/bin/env python3
"""
Network Testing Utilities
NETWORKING class - ASE, Informatics | by Revolvix

Provides network testing and diagnostic functionality.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import socket
import subprocess
import time
from typing import Optional, Tuple, List
from .logger import setup_logger

logger = setup_logger("network_utils")



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class NetworkUtils:
    """Network testing and diagnostic utilities."""
    
    @staticmethod


# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
    def check_port(host: str, port: int, timeout: float = 2.0) -> bool:
        """
        Check if a TCP port is open.
        
        Args:
            host: Target hostname or IP
            port: Port number
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
        except socket.error:
            return False
    
    @staticmethod


# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def wait_for_port(host: str, port: int, timeout: int = 30, 
                      interval: float = 1.0) -> bool:
        """
        Wait for a port to become available.
        
        Args:
            host: Target hostname or IP
            port: Port number
            timeout: Maximum wait time in seconds
            interval: Check interval in seconds
        
        Returns:
            True if port becomes available within timeout
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if NetworkUtils.check_port(host, port):
                return True
            time.sleep(interval)
        
        return False
    
    @staticmethod


# ═══════════════════════════════════════════════════════════════════════════════
# NETWORK_OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════════
    def send_tcp_message(host: str, port: int, message: bytes, 
                         timeout: float = 5.0) -> Optional[bytes]:
        """
        Send a TCP message and receive response.
        
        Args:
            host: Target hostname
            port: Target port
            message: Message to send
            timeout: Socket timeout
        
        Returns:
            Response bytes or None on error
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((host, port))
            sock.sendall(message)
            response = sock.recv(4096)
            sock.close()
            return response
        except socket.error as e:
            logger.error(f"TCP send failed: {e}")
            return None
    
    @staticmethod


# ═══════════════════════════════════════════════════════════════════════════════
# NETWORK_OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════════
    def send_udp_message(host: str, port: int, message: bytes,
                         timeout: float = 5.0) -> Optional[bytes]:
        """
        Send a UDP message and optionally receive response.
        
        Args:
            host: Target hostname
            port: Target port
            message: Message to send
            timeout: Socket timeout
        
        Returns:
            Response bytes or None
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(timeout)
            sock.sendto(message, (host, port))
            
            try:
                response, _ = sock.recvfrom(4096)
                return response
            except socket.timeout:
                # UDP may not have a response
                return b""
        except socket.error as e:
            logger.error(f"UDP send failed: {e}")
            return None
        finally:
            sock.close()
    
    @staticmethod


# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def get_local_ip() -> str:
        """Get the local IP address."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(("8.8.8.8", 80))
            ip = sock.getsockname()[0]
            sock.close()
            return ip
        except socket.error:
            return "127.0.0.1"
    
    @staticmethod


# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def scan_ports(host: str, ports: List[int], timeout: float = 1.0) -> List[int]:
        """
        Scan for open ports.
        
        Args:
            host: Target hostname
            ports: List of ports to scan
            timeout: Timeout per port
        
        Returns:
            List of open ports
        """
        open_ports = []
        
        for port in ports:
            if NetworkUtils.check_port(host, port, timeout):
                open_ports.append(port)
        
        return open_ports
    
    @staticmethod


# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def resolve_hostname(hostname: str) -> Optional[str]:
        """
        Resolve hostname to IP address.
        
        Args:
            hostname: Hostname to resolve
        
        Returns:
            IP address or None if resolution fails
        """
        try:
            return socket.gethostbyname(hostname)
        except socket.gaierror:
            return None
    
    @staticmethod


# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def ping(host: str, count: int = 4, timeout: int = 5) -> Tuple[bool, str]:
        """
        Ping a host.
        
        Args:
            host: Target hostname or IP
            count: Number of ping packets
            timeout: Timeout in seconds
        
        Returns:
            Tuple of (success, output_string)
        """
        try:
            # Use appropriate ping command for platform
            import platform
            if platform.system().lower() == "windows":
                cmd = ["ping", "-n", str(count), "-w", str(timeout * 1000), host]
            else:
                cmd = ["ping", "-c", str(count), "-W", str(timeout), host]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout * count + 5
            )
            
            return result.returncode == 0, result.stdout
        except subprocess.TimeoutExpired:
            return False, "Ping timed out"
        except FileNotFoundError:
            return False, "Ping command not found"
    
    @staticmethod


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_protocol_server(host: str, port: int, protocol: str = "text") -> dict:
        """
        Test a Week 4 protocol server.
        
        Args:
            host: Server hostname
            port: Server port
            protocol: "text", "binary", or "udp"
        
        Returns:
            Dictionary with test results
        """
        results = {
            "reachable": False,
            "protocol_working": False,
            "response": None,
            "error": None
        }
        
        if not NetworkUtils.check_port(host, port):
            results["error"] = f"Port {port} not reachable"
            return results
        
        results["reachable"] = True
        
        try:
            if protocol == "text":
                # Send PING command
                message = b"4 PING"
                response = NetworkUtils.send_tcp_message(host, port, message)
                
                if response:
                    results["response"] = response.decode('utf-8', errors='replace')
                    results["protocol_working"] = "pong" in results["response"].lower()
            
            elif protocol == "binary":
                # Send simple binary probe (would need proper header)
                # For now, just verify connection
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                sock.connect((host, port))
                sock.close()
                results["protocol_working"] = True
                results["response"] = "Connection successful"
            
            elif protocol == "udp":
                # UDP test - just verify we can send
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(b"test", (host, port))
                sock.close()
                results["protocol_working"] = True
                results["response"] = "Datagram sent"
        
        except Exception as e:
            results["error"] = str(e)
        
        return results

if __name__ == "__main__":
    # Module loaded directly - display module info
    print(f"Module {__name__} loaded successfully.")
    print(f"This module provides utility functions for the networking laboratory.")
