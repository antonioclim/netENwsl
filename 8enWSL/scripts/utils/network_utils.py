#!/usr/bin/env python3
"""
Network Utilities
NETWORKING class - ASE, Informatics | by Revolvix

Provides network testing functions for laboratory scripts.
"""

import socket
import subprocess
import time
from typing import Optional, Tuple, List, Dict, Any
import urllib.request
import urllib.error

from .logger import setup_logger

logger = setup_logger("network_utils")


def check_port_open(host: str, port: int, timeout: float = 2.0) -> bool:
    """
    Check if a port is open and accepting connections.
    
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
    except (socket.error, socket.timeout):
        return False


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
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        if check_port_open(host, port, timeout=min(2.0, interval)):
            return True
        time.sleep(interval)
    
    return False


def http_get(
    url: str,
    timeout: float = 10.0,
    headers: Optional[Dict[str, str]] = None
) -> Tuple[int, Dict[str, str], bytes]:
    """
    Perform an HTTP GET request.
    
    Args:
        url: Target URL
        timeout: Request timeout in seconds
        headers: Optional request headers
    
    Returns:
        Tuple of (status_code, response_headers, body)
    """
    try:
        req = urllib.request.Request(url)
        
        if headers:
            for key, value in headers.items():
                req.add_header(key, value)
        
        with urllib.request.urlopen(req, timeout=timeout) as response:
            status = response.status
            resp_headers = dict(response.headers)
            body = response.read()
            return status, resp_headers, body
            
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()
    except urllib.error.URLError as e:
        logger.error(f"URL error: {e.reason}")
        return 0, {}, b""
    except Exception as e:
        logger.error(f"Request error: {e}")
        return 0, {}, b""


def check_http_health(url: str, timeout: float = 5.0) -> bool:
    """
    Check if an HTTP endpoint is healthy (returns 2xx).
    
    Args:
        url: Health check URL
        timeout: Request timeout
    
    Returns:
        True if endpoint returns 2xx status
    """
    status, _, _ = http_get(url, timeout=timeout)
    return 200 <= status < 300


def get_local_ip() -> str:
    """Get the local IP address."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("8.8.8.8", 80))
            return sock.getsockname()[0]
    except Exception:
        return "127.0.0.1"


def get_free_port() -> int:
    """Find an available ephemeral port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def dns_resolve(hostname: str) -> Optional[str]:
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


def ping_host(host: str, count: int = 3) -> Tuple[bool, float]:
    """
    Ping a host and measure latency.
    
    Args:
        host: Target hostname or IP
        count: Number of ping packets
    
    Returns:
        Tuple of (reachable, avg_latency_ms)
    """
    try:
        # Windows uses -n, Unix uses -c
        import platform
        param = "-n" if platform.system().lower() == "windows" else "-c"
        
        result = subprocess.run(
            ["ping", param, str(count), host],
            capture_output=True,
            text=True,
            timeout=count * 2 + 5
        )
        
        if result.returncode == 0:
            # Parse average latency from output
            output = result.stdout.lower()
            if "average" in output or "avg" in output:
                import re
                match = re.search(r'(?:average|avg)[^=]*=\s*([\d.]+)', output)
                if match:
                    return True, float(match.group(1))
            return True, 0.0
        else:
            return False, 0.0
            
    except Exception as e:
        logger.debug(f"Ping failed: {e}")
        return False, 0.0


def traceroute(host: str, max_hops: int = 30) -> List[Tuple[int, str, float]]:
    """
    Trace route to a host.
    
    Args:
        host: Target hostname or IP
        max_hops: Maximum number of hops
    
    Returns:
        List of (hop_number, ip_address, latency_ms) tuples
    """
    import platform
    
    if platform.system().lower() == "windows":
        cmd = ["tracert", "-d", "-h", str(max_hops), host]
    else:
        cmd = ["traceroute", "-n", "-m", str(max_hops), host]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=max_hops * 3
        )
        
        hops = []
        import re
        
        for line in result.stdout.split("\n"):
            # Match hop number and IP
            match = re.search(r'^\s*(\d+)\s+.*?(\d+\.\d+\.\d+\.\d+)', line)
            if match:
                hop = int(match.group(1))
                ip = match.group(2)
                
                # Try to extract latency
                latency_match = re.search(r'([\d.]+)\s*ms', line)
                latency = float(latency_match.group(1)) if latency_match else 0.0
                
                hops.append((hop, ip, latency))
        
        return hops
        
    except Exception as e:
        logger.debug(f"Traceroute failed: {e}")
        return []


def test_connectivity(targets: List[Tuple[str, int]]) -> Dict[str, bool]:
    """
    Test connectivity to multiple targets.
    
    Args:
        targets: List of (host, port) tuples
    
    Returns:
        Dictionary mapping "host:port" to reachability status
    """
    results = {}
    
    for host, port in targets:
        key = f"{host}:{port}"
        results[key] = check_port_open(host, port)
    
    return results
