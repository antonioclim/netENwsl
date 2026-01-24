#!/usr/bin/env python3
"""
Network Testing Utilities
=========================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

Provides network connectivity testing functions for Week 13 laboratory.
These utilities are used by the lab scripts to verify service availability.

Functions:
- check_port: Test TCP connectivity to a port
- grab_banner: Attempt to read service banner
- resolve_hostname: DNS resolution
- get_local_ip: Determine local machine IP
- scan_port_range: Scan a range of ports
- ping_host: ICMP reachability test
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORT_DEPENDENCIES
# ═══════════════════════════════════════════════════════════════════════════════
import socket
import subprocess
from typing import Dict, List, Optional


# ═══════════════════════════════════════════════════════════════════════════════
# PORT_CONNECTIVITY
# ═══════════════════════════════════════════════════════════════════════════════

def check_port(
    host: str,
    port: int,
    timeout: float = 2.0
) -> bool:
    """
    Check if a TCP port is accepting connections.
    
    💭 PREDICTION: What will this return for a port with a firewall DROP rule?
       (Answer: False, after waiting for the timeout to expire)
    
    This function performs a full TCP three-way handshake to determine
    if a service is listening on the specified port.
    
    Args:
        host: Target hostname or IP address
        port: Target port number (1-65535)
        timeout: Connection timeout in seconds
    
    Returns:
        True if connection successful (port open), False otherwise
    
    Examples:
        >>> check_port("127.0.0.1", 1883)  # MQTT broker
        True
        >>> check_port("127.0.0.1", 99999)  # Invalid port
        False
    """
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False


def grab_banner(
    host: str,
    port: int,
    timeout: float = 2.0
) -> Optional[str]:
    """
    Attempt to grab a service banner from a port.
    
    💭 PREDICTION: Will this work for MQTT on port 1883?
       (Answer: Usually not — MQTT requires a proper CONNECT packet first)
    
    Many services send a welcome message immediately upon connection.
    This function attempts to read that message for service identification.
    
    Args:
        host: Target hostname or IP address
        port: Target port number
        timeout: Connection timeout in seconds
    
    Returns:
        Banner string if received (max 200 chars), None otherwise
    
    Note:
        Some services (like MQTT, HTTPS) do not send banners and require
        protocol-specific interaction to identify.
    """
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            sock.settimeout(timeout)
            
            # Send newline to stimulate response from some services
            try:
                sock.sendall(b"\r\n")
            except OSError:
                pass
            
            data = sock.recv(1024)
            if data:
                # Decode and clean up the banner
                banner = data.decode("utf-8", errors="replace").strip()
                return banner[:200] if banner else None
    except (socket.timeout, ConnectionRefusedError, OSError):
        pass
    
    return None


# ═══════════════════════════════════════════════════════════════════════════════
# DNS_AND_IP_UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════

def resolve_hostname(hostname: str) -> Optional[str]:
    """
    Resolve a hostname to an IP address.
    
    Args:
        hostname: DNS name to resolve
    
    Returns:
        IPv4 address string, or None if resolution fails
    
    Examples:
        >>> resolve_hostname("localhost")
        '127.0.0.1'
        >>> resolve_hostname("nonexistent.invalid")
        None
    """
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None


def get_local_ip() -> str:
    """
    Get the local machine's primary IP address.
    
    This works by creating a UDP socket that "connects" to an external
    address (without actually sending data) to determine which interface
    would be used for outgoing traffic.
    
    Returns:
        Local IP address string, or "127.0.0.1" if detection fails
    """
    try:
        # Create UDP socket — no actual connection made
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"


# ═══════════════════════════════════════════════════════════════════════════════
# PORT_SCANNING
# ═══════════════════════════════════════════════════════════════════════════════

def scan_port_range(
    host: str,
    start_port: int,
    end_port: int,
    timeout: float = 0.5
) -> List[int]:
    """
    Scan a range of ports for open services.
    
    ⚠️ WARNING: This is a simple sequential scanner intended for
    educational use on local laboratory environments only. For real
    scanning, use the threaded scanner in Exercise 1.
    
    Args:
        host: Target hostname or IP address
        start_port: First port in range (inclusive)
        end_port: Last port in range (inclusive)
        timeout: Connection timeout per port
    
    Returns:
        List of open port numbers
    
    Examples:
        >>> scan_port_range("127.0.0.1", 1880, 1890)
        [1883]  # If only MQTT is running
    """
    open_ports: List[int] = []
    
    for port in range(start_port, end_port + 1):
        if check_port(host, port, timeout):
            open_ports.append(port)
    
    return open_ports


# ═══════════════════════════════════════════════════════════════════════════════
# ICMP_TESTING
# ═══════════════════════════════════════════════════════════════════════════════

def ping_host(host: str, count: int = 1, timeout: int = 2) -> bool:
    """
    Ping a host to check ICMP reachability.
    
    💭 PREDICTION: If ping fails but check_port succeeds, what does that tell you?
       (Answer: Host is up but ICMP is blocked — common in firewalled environments)
    
    Args:
        host: Target hostname or IP address
        count: Number of ping packets to send
        timeout: Timeout in seconds per packet
    
    Returns:
        True if host responds to at least one ping, False otherwise
    
    Note:
        This function uses the system ping command, which requires
        appropriate permissions and may behave differently on Windows vs Linux.
    """
    try:
        import platform
        
        if platform.system().lower() == "windows":
            # Windows ping: -n for count, -w for timeout in milliseconds
            cmd = ["ping", "-n", str(count), "-w", str(timeout * 1000), host]
        else:
            # Linux ping: -c for count, -W for timeout in seconds
            cmd = ["ping", "-c", str(count), "-W", str(timeout), host]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=timeout * count + 5
        )
        return result.returncode == 0
    
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# SERVICE_CHECKER_CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class ServiceChecker:
    """
    Check availability of Week 13 laboratory services.
    
    This class provides a convenient way to verify that all expected
    services are running and accessible.
    
    Attributes:
        SERVICES: Dictionary mapping service keys to port/name info
        host: Target host for all checks
    
    Example:
        >>> checker = ServiceChecker("127.0.0.1")
        >>> checker.print_status()
        Service Availability:
        ------------------------------------------------------------
          MQTT (Plaintext)       (:1883) - ✓ Available
          MQTT (TLS)             (:8883) - ✓ Available
          ...
    """
    
    SERVICES = {
        "mqtt_plain": {"port": 1883, "name": "MQTT (Plaintext)"},
        "mqtt_tls": {"port": 8883, "name": "MQTT (TLS)"},
        "dvwa": {"port": 8080, "name": "DVWA HTTP"},
        "ftp": {"port": 2121, "name": "vsftpd FTP"},
        "backdoor": {"port": 6200, "name": "Backdoor Stub"},
    }
    
    def __init__(self, host: str = "127.0.0.1"):
        """
        Initialise service checker.
        
        Args:
            host: Target host for all service checks
        """
        self.host = host
    
    def check_all(self) -> Dict[str, Dict]:
        """
        Check all laboratory services.
        
        Returns:
            Dictionary with results for each service, including:
            - name: Human-readable service name
            - port: Port number
            - available: Boolean indicating if service is reachable
            - banner: Service banner if available
        """
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
        """Print formatted status of all services to stdout."""
        results = self.check_all()
        
        print("\nService Availability:")
        print("-" * 60)
        
        for key, info in results.items():
            status = "✓ Available" if info["available"] else "✗ Unavailable"
            print(f"  {info['name']:20s} (:{info['port']}) - {status}")
            
            if info["banner"]:
                # Truncate long banners
                banner = info["banner"][:50]
                print(f"    Banner: {banner}")
        
        print("-" * 60)
    
    def all_available(self) -> bool:
        """
        Check if all services are available.
        
        Returns:
            True if all services respond, False if any is unavailable
        """
        results = self.check_all()
        return all(info["available"] for info in results.values())


# ═══════════════════════════════════════════════════════════════════════════════
# SELF_TEST
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Network Utilities — Self Test")
    print("=" * 50)
    
    # Test local IP detection
    local_ip = get_local_ip()
    print(f"Local IP: {local_ip}")
    
    # Test hostname resolution
    localhost_ip = resolve_hostname("localhost")
    print(f"localhost resolves to: {localhost_ip}")
    
    # Test service checker
    print("\nChecking laboratory services...")
    checker = ServiceChecker()
    checker.print_status()
