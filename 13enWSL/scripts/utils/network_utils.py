#!/usr/bin/env python3
"""
Network Testing Utilities
NETWORKING class - ASE, Informatics | by Revolvix

Provides network connectivity testing functions for Week 13 laboratory.
"""

import socket
import subprocess
from typing import Optional, Tuple, List


def check_port(
    host: str,
    port: int,
    timeout: float = 2.0
) -> bool:
    """
    Check if a TCP port is accepting connections.
    
    Args:
        host: Target hostname or IP
        port: Target port number
        timeout: Connection timeout in seconds
    
    Returns:
        True if connection successful
    """
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False


def grab_banner(
    host: str,
    port: int,
    timeout: float = 2.0
) -> Optional[str]:
    """
    Attempt to grab a service banner from a port.
    
    Args:
        host: Target hostname or IP
        port: Target port number
        timeout: Connection timeout in seconds
    
    Returns:
        Banner string if received, None otherwise
    """
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            sock.settimeout(timeout)
            # Send newline to stimulate response
            try:
                sock.sendall(b"\r\n")
            except Exception:
                pass
            
            data = sock.recv(1024)
            if data:
                return data.decode("utf-8", errors="replace").strip()[:200]
    except Exception:
        pass
    return None


def resolve_hostname(hostname: str) -> Optional[str]:
    """
    Resolve a hostname to an IP address.
    
    Args:
        hostname: Hostname to resolve
    
    Returns:
        IP address string or None if resolution fails
    """
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None


def get_local_ip() -> str:
    """
    Get the local machine's primary IP address.
    
    Returns:
        Local IP address string
    """
    try:
        # Create a UDP socket to determine outgoing interface
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"


def scan_port_range(
    host: str,
    start_port: int,
    end_port: int,
    timeout: float = 0.5
) -> List[int]:
    """
    Scan a range of ports for open services.
    
    Args:
        host: Target hostname or IP
        start_port: First port in range
        end_port: Last port in range
        timeout: Connection timeout per port
    
    Returns:
        List of open port numbers
    """
    open_ports = []
    for port in range(start_port, end_port + 1):
        if check_port(host, port, timeout):
            open_ports.append(port)
    return open_ports


def ping_host(host: str, count: int = 1, timeout: int = 2) -> bool:
    """
    Ping a host to check reachability.
    
    Args:
        host: Target hostname or IP
        count: Number of ping packets
        timeout: Timeout in seconds
    
    Returns:
        True if host responds to ping
    """
    try:
        # Platform-specific ping command
        import platform
        if platform.system().lower() == "windows":
            cmd = ["ping", "-n", str(count), "-w", str(timeout * 1000), host]
        else:
            cmd = ["ping", "-c", str(count), "-W", str(timeout), host]
        
        result = subprocess.run(cmd, capture_output=True, timeout=timeout * count + 5)
        return result.returncode == 0
    except Exception:
        return False


class ServiceChecker:
    """Check availability of laboratory services."""
    
    SERVICES = {
        "mqtt_plain": {"port": 1883, "name": "MQTT (Plaintext)"},
        "mqtt_tls": {"port": 8883, "name": "MQTT (TLS)"},
        "dvwa": {"port": 8080, "name": "DVWA HTTP"},
        "ftp": {"port": 2121, "name": "vsftpd FTP"},
        "backdoor": {"port": 6200, "name": "Backdoor Stub"},
    }
    
    def __init__(self, host: str = "127.0.0.1"):
        self.host = host
    
    def check_all(self) -> dict:
        """Check all laboratory services."""
        results = {}
        for key, config in self.SERVICES.items():
            port = config["port"]
            name = config["name"]
            available = check_port(self.host, port)
            banner = grab_banner(self.host, port) if available else None
            results[key] = {
                "name": name,
                "port": port,
                "available": available,
                "banner": banner
            }
        return results
    
    def print_status(self) -> None:
        """Print status of all services."""
        results = self.check_all()
        print("\nService Availability:")
        print("-" * 60)
        for key, info in results.items():
            status = "✓ Available" if info["available"] else "✗ Unavailable"
            print(f"  {info['name']:20s} (:{info['port']}) - {status}")
            if info["banner"]:
                print(f"    Banner: {info['banner'][:50]}")
        print("-" * 60)
