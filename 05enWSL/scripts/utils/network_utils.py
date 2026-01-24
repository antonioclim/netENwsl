#!/usr/bin/env python3
"""
Network Utility Module
NETWORKING class - ASE, Informatics | by Revolvix

Provides network testing and validation functions.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import socket
import subprocess
import time
from typing import Tuple, Optional, List
from dataclasses import dataclass

from .logger import get_logger

logger = get_logger("network_utils")


@dataclass


# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class PortCheckResult:
    """Result of a port availability check."""
    port: int
    is_open: bool
    service: Optional[str] = None
    response_time_ms: Optional[float] = None



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_tcp_port(host: str, port: int, timeout: float = 2.0) -> PortCheckResult:
    """
    Check if a TCP port is open.
    
    Args:
        host: Target hostname or IP
        port: Port number to check
        timeout: Connection timeout in seconds
    
    Returns:
        PortCheckResult with status
    """
    start = time.time()
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        elapsed = (time.time() - start) * 1000
        sock.close()
        
        return PortCheckResult(
            port=port,
            is_open=(result == 0),
            response_time_ms=elapsed if result == 0 else None
        )
    except socket.error as e:
        logger.debug(f"Socket error checking {host}:{port}: {e}")
        return PortCheckResult(port=port, is_open=False)



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_udp_port(host: str, port: int, timeout: float = 2.0) -> PortCheckResult:
    """
    Check if a UDP port responds (sends a probe and waits for response).
    
    Args:
        host: Target hostname or IP
        port: Port number to check
        timeout: Response timeout in seconds
    
    Returns:
        PortCheckResult with status
    """
    start = time.time()
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        
        # Send a probe
        sock.sendto(b"PROBE", (host, port))
        
        try:
            data, addr = sock.recvfrom(1024)
            elapsed = (time.time() - start) * 1000
            sock.close()
            return PortCheckResult(
                port=port,
                is_open=True,
                response_time_ms=elapsed
            )
        except socket.timeout:
            sock.close()
            # No response doesn't necessarily mean closed for UDP
            return PortCheckResult(port=port, is_open=False)
    except socket.error as e:
        logger.debug(f"Socket error checking {host}:{port}/udp: {e}")
        return PortCheckResult(port=port, is_open=False)



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def ping_host(host: str, count: int = 3, timeout: float = 1.0) -> Tuple[bool, float]:
    """
    Ping a host and return reachability and average RTT.
    
    Args:
        host: Target hostname or IP
        count: Number of ping packets
        timeout: Timeout per packet in seconds
    
    Returns:
        Tuple of (is_reachable, avg_rtt_ms)
    """
    # Determine platform-specific ping command
    import platform
    
    if platform.system().lower() == "windows":
        cmd = ["ping", "-n", str(count), "-w", str(int(timeout * 1000)), host]
    else:
        cmd = ["ping", "-c", str(count), "-W", str(int(timeout)), host]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=count * timeout + 5)
        
        if result.returncode == 0:
            # Parse average RTT from output
            output = result.stdout
            
            # Look for average time
            import re
            
            # Windows format: Average = Xms
            # Linux format: min/avg/max/mdev = X/Y/Z/W ms
            match = re.search(r'Average\s*=\s*(\d+)ms', output)
            if not match:
                match = re.search(r'min/avg/max/mdev\s*=\s*[\d.]+/([\d.]+)/', output)
            if not match:
                # macOS format
                match = re.search(r'round-trip\s+min/avg/max/stddev\s*=\s*[\d.]+/([\d.]+)/', output)
            
            avg_rtt = float(match.group(1)) if match else 0.0
            return True, avg_rtt
        else:
            return False, 0.0
    except subprocess.TimeoutExpired:
        return False, 0.0
    except FileNotFoundError:
        logger.warning("ping command not found")
        return False, 0.0



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def resolve_hostname(hostname: str) -> List[str]:
    """
    Resolve a hostname to IP addresses.
    
    Args:
        hostname: Hostname to resolve
    
    Returns:
        List of IP addresses
    """
    try:
        result = socket.getaddrinfo(hostname, None)
        addresses = list(set(addr[4][0] for addr in result))
        return addresses
    except socket.gaierror:
        return []



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def get_local_ip() -> Optional[str]:
    """
    Get the local IP address used for outbound connections.
    
    Returns:
        Local IP address or None
    """
    try:
        # Create a dummy connection to determine local IP
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
def scan_ports(host: str, ports: List[int], timeout: float = 1.0) -> List[PortCheckResult]:
    """
    Scan multiple ports on a host.
    
    Args:
        host: Target hostname or IP
        ports: List of ports to scan
        timeout: Timeout per port
    
    Returns:
        List of PortCheckResult
    """
    results = []
    for port in ports:
        result = check_tcp_port(host, port, timeout)
        results.append(result)
        logger.debug(f"Port {port}: {'open' if result.is_open else 'closed'}")
    return results



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def wait_for_port(host: str, port: int, timeout: float = 30.0, interval: float = 1.0) -> bool:
    """
    Wait for a port to become available.
    
    Args:
        host: Target hostname or IP
        port: Port to wait for
        timeout: Maximum wait time in seconds
        interval: Check interval in seconds
    
    Returns:
        True if port became available within timeout
    """
    start = time.time()
    
    while time.time() - start < timeout:
        result = check_tcp_port(host, port, timeout=interval)
        if result.is_open:
            logger.info(f"Port {host}:{port} is now available")
            return True
        time.sleep(interval)
    
    logger.warning(f"Timeout waiting for {host}:{port}")
    return False



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def validate_ip_address(ip: str) -> Tuple[bool, str]:
    """
    Validate an IP address (IPv4 or IPv6).
    
    Args:
        ip: IP address string
    
    Returns:
        Tuple of (is_valid, address_type)
    """
    import ipaddress
    
    try:
        addr = ipaddress.ip_address(ip)
        if isinstance(addr, ipaddress.IPv4Address):
            return True, "IPv4"
        else:
            return True, "IPv6"
    except ValueError:
        return False, "Invalid"



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def validate_cidr(cidr: str) -> Tuple[bool, str]:
    """
    Validate a CIDR notation.
    
    Args:
        cidr: CIDR notation string (e.g., 192.168.1.0/24)
    
    Returns:
        Tuple of (is_valid, message)
    """
    import ipaddress
    
    try:
        network = ipaddress.ip_network(cidr, strict=True)
        return True, f"Valid {network.version} network with {network.num_addresses} addresses"
    except ValueError as e:
        # Try non-strict (host address with prefix)
        try:
            interface = ipaddress.ip_interface(cidr)
            return True, f"Valid {interface.version} interface in network {interface.network}"
        except ValueError:
            return False, str(e)


if __name__ == "__main__":
    # Quick demonstration
    print("Network Utilities Demonstration")
    print("=" * 40)
    
    # Check local IP
    local_ip = get_local_ip()
    print(f"Local IP: {local_ip}")
    
    # Validate some addresses
    test_cidrs = ["192.168.1.0/24", "10.0.0.1/8", "invalid"]
    for cidr in test_cidrs:
        valid, msg = validate_cidr(cidr)
        print(f"{cidr}: {msg}")
    
    # Ping localhost
    reachable, rtt = ping_host("127.0.0.1", count=1)
    print(f"Localhost ping: {'reachable' if reachable else 'unreachable'}, RTT: {rtt}ms")
