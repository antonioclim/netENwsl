#!/usr/bin/env python3
"""
Network Testing Utilities for Week 14 Laboratory.

NETWORKING class - ASE, Informatics | by Revolvix

This module provides utilities for testing network connectivity,
analysing traffic, and validating service endpoints within
the laboratory environment.
"""

import socket
import subprocess
import time
import json
import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
from urllib.parse import urlparse
from pathlib import Path

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

from .logger import get_logger

logger = get_logger(__name__)


class Protocol(Enum):
    """Network protocol enumeration."""
    TCP = "tcp"
    UDP = "udp"
    HTTP = "http"
    HTTPS = "https"
    ICMP = "icmp"


@dataclass
class ConnectivityResult:
    """Result of a connectivity test."""
    host: str
    port: int
    protocol: Protocol
    success: bool
    latency_ms: float
    error: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


@dataclass
class HTTPResult:
    """Result of an HTTP request."""
    url: str
    status_code: int
    success: bool
    latency_ms: float
    headers: Dict[str, str]
    body: Optional[str] = None
    error: Optional[str] = None


@dataclass
class PortScanResult:
    """Result of a port scan."""
    host: str
    port: int
    state: str  # open, closed, filtered
    service: Optional[str] = None
    banner: Optional[str] = None


class NetworkError(Exception):
    """Exception raised for network-related errors."""
    pass


class NetworkUtils:
    """
    Provides network testing and analysis utilities.
    
    This class offers methods for testing connectivity, making HTTP
    requests, scanning ports, and capturing network traffic.
    
    Attributes:
        timeout: Default timeout for operations in seconds
    """
    
    def __init__(self, timeout: float = 5.0):
        """
        Initialise network utilities.
        
        Args:
            timeout: Default timeout for network operations
        """
        self.timeout = timeout
    
    def test_tcp_connection(
        self,
        host: str,
        port: int,
        timeout: Optional[float] = None
    ) -> ConnectivityResult:
        """
        Test TCP connectivity to a host:port.
        
        Args:
            host: Target hostname or IP address
            port: Target port number
            timeout: Connection timeout (uses default if None)
            
        Returns:
            ConnectivityResult with connection status
        """
        timeout = timeout or self.timeout
        start_time = time.time()
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            
            result = sock.connect_ex((host, port))
            latency = (time.time() - start_time) * 1000
            
            sock.close()
            
            if result == 0:
                return ConnectivityResult(
                    host=host,
                    port=port,
                    protocol=Protocol.TCP,
                    success=True,
                    latency_ms=latency
                )
            else:
                return ConnectivityResult(
                    host=host,
                    port=port,
                    protocol=Protocol.TCP,
                    success=False,
                    latency_ms=latency,
                    error=f"Connection refused (error code: {result})"
                )
                
        except socket.timeout:
            return ConnectivityResult(
                host=host,
                port=port,
                protocol=Protocol.TCP,
                success=False,
                latency_ms=timeout * 1000,
                error="Connection timed out"
            )
        except socket.gaierror as e:
            return ConnectivityResult(
                host=host,
                port=port,
                protocol=Protocol.TCP,
                success=False,
                latency_ms=0,
                error=f"Name resolution failed: {e}"
            )
        except Exception as e:
            return ConnectivityResult(
                host=host,
                port=port,
                protocol=Protocol.TCP,
                success=False,
                latency_ms=0,
                error=str(e)
            )
    
    def test_udp_connection(
        self,
        host: str,
        port: int,
        message: bytes = b"ping",
        timeout: Optional[float] = None
    ) -> ConnectivityResult:
        """
        Test UDP connectivity by sending a packet and waiting for response.
        
        Note: UDP is connectionless, so this only confirms the port
        accepts packets if a response is received.
        
        Args:
            host: Target hostname or IP address
            port: Target port number
            message: Payload to send
            timeout: Response timeout (uses default if None)
            
        Returns:
            ConnectivityResult with test status
        """
        timeout = timeout or self.timeout
        start_time = time.time()
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(timeout)
            
            sock.sendto(message, (host, port))
            
            try:
                data, addr = sock.recvfrom(1024)
                latency = (time.time() - start_time) * 1000
                sock.close()
                
                return ConnectivityResult(
                    host=host,
                    port=port,
                    protocol=Protocol.UDP,
                    success=True,
                    latency_ms=latency,
                    details={"response_size": len(data)}
                )
            except socket.timeout:
                latency = (time.time() - start_time) * 1000
                sock.close()
                
                # UDP timeout doesn't necessarily mean failure
                return ConnectivityResult(
                    host=host,
                    port=port,
                    protocol=Protocol.UDP,
                    success=False,
                    latency_ms=latency,
                    error="No response (port may still be open)"
                )
                
        except Exception as e:
            return ConnectivityResult(
                host=host,
                port=port,
                protocol=Protocol.UDP,
                success=False,
                latency_ms=0,
                error=str(e)
            )
    
    def http_request(
        self,
        url: str,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Any] = None,
        json_data: Optional[Dict] = None,
        timeout: Optional[float] = None,
        verify_ssl: bool = True
    ) -> HTTPResult:
        """
        Make an HTTP request and return the result.
        
        Args:
            url: Target URL
            method: HTTP method (GET, POST, etc.)
            headers: Request headers
            data: Form data
            json_data: JSON payload
            timeout: Request timeout
            verify_ssl: Verify SSL certificates
            
        Returns:
            HTTPResult with response details
        """
        if not HAS_REQUESTS:
            return HTTPResult(
                url=url,
                status_code=0,
                success=False,
                latency_ms=0,
                headers={},
                error="requests library not installed"
            )
        
        timeout = timeout or self.timeout
        start_time = time.time()
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                data=data,
                json=json_data,
                timeout=timeout,
                verify=verify_ssl
            )
            latency = (time.time() - start_time) * 1000
            
            return HTTPResult(
                url=url,
                status_code=response.status_code,
                success=200 <= response.status_code < 400,
                latency_ms=latency,
                headers=dict(response.headers),
                body=response.text[:4096] if response.text else None
            )
            
        except requests.exceptions.Timeout:
            return HTTPResult(
                url=url,
                status_code=0,
                success=False,
                latency_ms=timeout * 1000,
                headers={},
                error="Request timed out"
            )
        except requests.exceptions.ConnectionError as e:
            return HTTPResult(
                url=url,
                status_code=0,
                success=False,
                latency_ms=0,
                headers={},
                error=f"Connection failed: {e}"
            )
        except Exception as e:
            return HTTPResult(
                url=url,
                status_code=0,
                success=False,
                latency_ms=0,
                headers={},
                error=str(e)
            )
    
    def ping(
        self,
        host: str,
        count: int = 3,
        timeout: Optional[float] = None
    ) -> ConnectivityResult:
        """
        Ping a host using ICMP.
        
        Args:
            host: Target hostname or IP address
            count: Number of ping packets
            timeout: Per-packet timeout
            
        Returns:
            ConnectivityResult with ping statistics
        """
        timeout = timeout or self.timeout
        
        try:
            # Use platform-appropriate ping command
            import platform
            if platform.system().lower() == "windows":
                cmd = ["ping", "-n", str(count), "-w", str(int(timeout * 1000)), host]
            else:
                cmd = ["ping", "-c", str(count), "-W", str(int(timeout)), host]
            
            start_time = time.time()
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout * count + 5
            )
            latency = (time.time() - start_time) * 1000 / count
            
            success = result.returncode == 0
            
            # Parse average latency from output
            avg_match = re.search(r'(?:Average|avg)[^\d]*(\d+\.?\d*)', result.stdout)
            if avg_match:
                latency = float(avg_match.group(1))
            
            return ConnectivityResult(
                host=host,
                port=0,
                protocol=Protocol.ICMP,
                success=success,
                latency_ms=latency,
                details={"output": result.stdout[:500]}
            )
            
        except subprocess.TimeoutExpired:
            return ConnectivityResult(
                host=host,
                port=0,
                protocol=Protocol.ICMP,
                success=False,
                latency_ms=timeout * 1000,
                error="Ping timed out"
            )
        except Exception as e:
            return ConnectivityResult(
                host=host,
                port=0,
                protocol=Protocol.ICMP,
                success=False,
                latency_ms=0,
                error=str(e)
            )
    
    def scan_port(
        self,
        host: str,
        port: int,
        timeout: Optional[float] = None,
        grab_banner: bool = False
    ) -> PortScanResult:
        """
        Scan a single port and optionally grab banner.
        
        Args:
            host: Target hostname or IP address
            port: Port to scan
            timeout: Connection timeout
            grab_banner: Attempt to grab service banner
            
        Returns:
            PortScanResult with scan details
        """
        timeout = timeout or min(self.timeout, 2.0)
        
        result = self.test_tcp_connection(host, port, timeout)
        
        if not result.success:
            return PortScanResult(
                host=host,
                port=port,
                state="closed" if "refused" in (result.error or "") else "filtered"
            )
        
        banner = None
        if grab_banner:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                sock.connect((host, port))
                
                # Send HTTP request for web services
                if port in [80, 8080, 8000, 8001, 8002, 443, 8443]:
                    sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                sock.close()
            except Exception:
                pass
        
        # Guess service from well-known ports
        service_map = {
            22: "ssh", 80: "http", 443: "https",
            8080: "http-proxy", 9000: "echo",
            8001: "http-alt", 8002: "http-alt"
        }
        
        return PortScanResult(
            host=host,
            port=port,
            state="open",
            service=service_map.get(port),
            banner=banner
        )
    
    def scan_ports(
        self,
        host: str,
        ports: List[int],
        timeout: Optional[float] = None
    ) -> List[PortScanResult]:
        """
        Scan multiple ports on a host.
        
        Args:
            host: Target hostname or IP address
            ports: List of ports to scan
            timeout: Per-port timeout
            
        Returns:
            List of PortScanResult for each port
        """
        results = []
        for port in ports:
            results.append(self.scan_port(host, port, timeout))
        return results
    
    def test_echo_server(
        self,
        host: str,
        port: int,
        message: str = "Hello, Echo!",
        timeout: Optional[float] = None
    ) -> Tuple[bool, str, float]:
        """
        Test a TCP echo server.
        
        Args:
            host: Echo server host
            port: Echo server port
            message: Message to send
            timeout: Response timeout
            
        Returns:
            Tuple of (success, response, latency_ms)
        """
        timeout = timeout or self.timeout
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            
            start_time = time.time()
            sock.connect((host, port))
            
            sock.sendall(message.encode('utf-8'))
            
            response = sock.recv(4096).decode('utf-8')
            latency = (time.time() - start_time) * 1000
            
            sock.close()
            
            success = response.strip() == message.strip()
            return success, response, latency
            
        except Exception as e:
            return False, str(e), 0
    
    def check_load_balancer(
        self,
        url: str,
        num_requests: int = 10,
        timeout: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Test load balancer distribution.
        
        Args:
            url: Load balancer URL
            num_requests: Number of requests to make
            timeout: Per-request timeout
            
        Returns:
            Dictionary with distribution statistics
        """
        if not HAS_REQUESTS:
            return {"error": "requests library not installed"}
        
        timeout = timeout or self.timeout
        backends = {}
        latencies = []
        errors = 0
        
        for _ in range(num_requests):
            try:
                start = time.time()
                response = requests.get(url, timeout=timeout)
                latency = (time.time() - start) * 1000
                latencies.append(latency)
                
                # Try to identify backend from headers or body
                backend = response.headers.get('X-Backend', 'unknown')
                if backend == 'unknown' and response.text:
                    # Try to extract from body
                    match = re.search(r'app[12]|backend[12]', response.text.lower())
                    if match:
                        backend = match.group()
                
                backends[backend] = backends.get(backend, 0) + 1
                
            except Exception:
                errors += 1
        
        return {
            "total_requests": num_requests,
            "successful": num_requests - errors,
            "errors": errors,
            "backend_distribution": backends,
            "avg_latency_ms": sum(latencies) / len(latencies) if latencies else 0,
            "min_latency_ms": min(latencies) if latencies else 0,
            "max_latency_ms": max(latencies) if latencies else 0
        }
    
    def wait_for_service(
        self,
        host: str,
        port: int,
        timeout: float = 60,
        interval: float = 2
    ) -> bool:
        """
        Wait for a service to become available.
        
        Args:
            host: Service host
            port: Service port
            timeout: Maximum wait time
            interval: Check interval
            
        Returns:
            True if service became available within timeout
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            result = self.test_tcp_connection(host, port, timeout=interval)
            if result.success:
                return True
            time.sleep(interval)
        
        return False


def validate_ip(ip: str) -> bool:
    """Validate an IPv4 address."""
    try:
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            num = int(part)
            if num < 0 or num > 255:
                return False
        return True
    except ValueError:
        return False


def validate_port(port: int) -> bool:
    """Validate a port number."""
    return isinstance(port, int) and 0 < port <= 65535


def parse_host_port(address: str) -> Tuple[str, int]:
    """
    Parse a host:port string.
    
    Args:
        address: String in format "host:port"
        
    Returns:
        Tuple of (host, port)
        
    Raises:
        ValueError: If address format is invalid
    """
    parts = address.rsplit(':', 1)
    if len(parts) != 2:
        raise ValueError(f"Invalid address format: {address}")
    
    host = parts[0]
    try:
        port = int(parts[1])
    except ValueError:
        raise ValueError(f"Invalid port: {parts[1]}")
    
    return host, port
