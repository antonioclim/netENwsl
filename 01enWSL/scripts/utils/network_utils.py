#!/usr/bin/env python3
"""
Network Testing Utilities
NETWORKING class - ASE, Informatics | by Revolvix

Provides network connectivity testing and diagnostic functions.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import socket
import subprocess
import time
from dataclasses import dataclass
from typing import Optional, Tuple, List

from .logger import get_logger


@dataclass(frozen=True)


# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class PingResult:
    """Result of a ping operation."""
    host: str
    transmitted: int
    received: int
    loss_percent: float
    min_rtt_ms: Optional[float]
    avg_rtt_ms: Optional[float]
    max_rtt_ms: Optional[float]
    
    @property


# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def success(self) -> bool:
        """Check if ping was successful (at least one reply)."""
        return self.received > 0


@dataclass(frozen=True)


# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class PortCheckResult:
    """Result of a port check operation."""
    host: str
    port: int
    is_open: bool
    response_time_ms: Optional[float]
    error: Optional[str]



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class NetworkTester:
    """Network connectivity testing utilities."""
    

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
    def __init__(self) -> None:
        self.logger = get_logger("network_utils")
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def ping(
        self,
        host: str,
        count: int = 4,
        timeout: int = 2
    ) -> PingResult:
        """
        Perform ICMP ping test.
        
        Args:
            host: Target host or IP address
            count: Number of ping requests
            timeout: Timeout per packet in seconds
        
        Returns:
            PingResult with statistics
        """
        import re
        
        cmd = ["ping", "-n", "-c", str(count), "-W", str(timeout), host]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=count * timeout + 5
            )
            output = result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return PingResult(
                host=host,
                transmitted=count,
                received=0,
                loss_percent=100.0,
                min_rtt_ms=None,
                avg_rtt_ms=None,
                max_rtt_ms=None
            )
        
        # Parse output
        transmitted = count
        received = 0
        loss = 100.0
        min_rtt = avg_rtt = max_rtt = None
        
        # Parse packet statistics
        m = re.search(r"(\d+) packets transmitted, (\d+) received", output)
        if m:
            transmitted = int(m.group(1))
            received = int(m.group(2))
            loss = 100.0 * (1 - received / transmitted) if transmitted > 0 else 100.0
        
        # Parse RTT statistics
        m = re.search(r"rtt min/avg/max/mdev = ([\d.]+)/([\d.]+)/([\d.]+)/", output)
        if m:
            min_rtt = float(m.group(1))
            avg_rtt = float(m.group(2))
            max_rtt = float(m.group(3))
        
        return PingResult(
            host=host,
            transmitted=transmitted,
            received=received,
            loss_percent=loss,
            min_rtt_ms=min_rtt,
            avg_rtt_ms=avg_rtt,
            max_rtt_ms=max_rtt
        )
    

# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
    def check_tcp_port(
        self,
        host: str,
        port: int,
        timeout: float = 2.0
    ) -> PortCheckResult:
        """
        Check if a TCP port is open.
        
        Args:
            host: Target host
            port: Port number
            timeout: Connection timeout in seconds
        
        Returns:
            PortCheckResult with connection status
        """
        start_time = time.time()
        
        try:
            with socket.create_connection((host, port), timeout=timeout):
                elapsed_ms = (time.time() - start_time) * 1000
                return PortCheckResult(
                    host=host,
                    port=port,
                    is_open=True,
                    response_time_ms=elapsed_ms,
                    error=None
                )
        except socket.timeout:
            return PortCheckResult(
                host=host,
                port=port,
                is_open=False,
                response_time_ms=None,
                error="Connection timed out"
            )
        except ConnectionRefusedError:
            return PortCheckResult(
                host=host,
                port=port,
                is_open=False,
                response_time_ms=None,
                error="Connection refused"
            )
        except socket.error as e:
            return PortCheckResult(
                host=host,
                port=port,
                is_open=False,
                response_time_ms=None,
                error=str(e)
            )
    

# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
    def check_udp_port(
        self,
        host: str,
        port: int,
        timeout: float = 2.0,
        probe_data: bytes = b"probe"
    ) -> PortCheckResult:
        """
        Check if a UDP port is responding.
        
        Note: UDP port checking is inherently unreliable since UDP is
        connectionless. This sends a probe and waits for a response.
        
        Args:
            host: Target host
            port: Port number
            timeout: Response timeout in seconds
            probe_data: Data to send as probe
        
        Returns:
            PortCheckResult (is_open indicates response received)
        """
        start_time = time.time()
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(timeout)
            sock.sendto(probe_data, (host, port))
            
            try:
                sock.recvfrom(1024)
                elapsed_ms = (time.time() - start_time) * 1000
                return PortCheckResult(
                    host=host,
                    port=port,
                    is_open=True,
                    response_time_ms=elapsed_ms,
                    error=None
                )
            except socket.timeout:
                return PortCheckResult(
                    host=host,
                    port=port,
                    is_open=False,
                    response_time_ms=None,
                    error="No response (may still be open)"
                )
        except socket.error as e:
            return PortCheckResult(
                host=host,
                port=port,
                is_open=False,
                response_time_ms=None,
                error=str(e)
            )
        finally:
            sock.close()
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def get_local_interfaces(self) -> List[Tuple[str, str]]:
        """
        Get list of local network interfaces and their IP addresses.
        
        Returns:
            List of (interface_name, ip_address) tuples
        """
        interfaces = []
        
        try:
            result = subprocess.run(
                ["ip", "-4", "-o", "addr", "show"],
                capture_output=True,
                text=True
            )
            
            for line in result.stdout.strip().split("\n"):
                parts = line.split()
                if len(parts) >= 4:
                    iface = parts[1]
                    ip_cidr = parts[3]
                    ip = ip_cidr.split("/")[0]
                    interfaces.append((iface, ip))
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Fallback: use socket
            hostname = socket.gethostname()
            try:
                ip = socket.gethostbyname(hostname)
                interfaces.append(("default", ip))
            except socket.error:
                interfaces.append(("lo", "127.0.0.1"))
        
        return interfaces
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def get_default_gateway(self) -> Optional[str]:
        """
        Get the default gateway IP address.
        
        Returns:
            Gateway IP or None if not found
        """
        try:
            result = subprocess.run(
                ["ip", "route", "show", "default"],
                capture_output=True,
                text=True
            )
            
            # Parse "default via X.X.X.X ..."
            for line in result.stdout.strip().split("\n"):
                parts = line.split()
                if "via" in parts:
                    via_idx = parts.index("via")
                    if via_idx + 1 < len(parts):
                        return parts[via_idx + 1]
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        return None
    

# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
    def run_connectivity_test(self) -> dict:
        """
        Run a complete connectivity test.
        
        Returns:
            Dictionary with test results
        """
        results = {
            "loopback": None,
            "gateway": None,
            "internet": None,
            "dns": None
        }
        
        # Test loopback
        self.logger.info("Testing loopback...")
        results["loopback"] = self.ping("127.0.0.1", count=2)
        
        # Test gateway
        gateway = self.get_default_gateway()
        if gateway:
            self.logger.info(f"Testing gateway ({gateway})...")
            results["gateway"] = self.ping(gateway, count=2)
        else:
            self.logger.warning("No default gateway found")
        
        # Test internet (Google DNS)
        self.logger.info("Testing internet connectivity...")
        results["internet"] = self.ping("8.8.8.8", count=2)
        
        # Test DNS resolution
        self.logger.info("Testing DNS resolution...")
        try:
            socket.gethostbyname("google.com")
            results["dns"] = True
        except socket.error:
            results["dns"] = False
        
        return results

if __name__ == "__main__":
    # Module loaded directly - display module info
    print(f"Module {__name__} loaded successfully.")
    print(f"This module provides utility functions for the networking laboratory.")
