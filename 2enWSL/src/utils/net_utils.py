#!/usr/bin/env python3
"""
Network Utilities Module
NETWORKING class - ASE, Informatics | by Revolvix

Common networking utilities for socket programming exercises.
"""

import socket
import struct
import time
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class ConnectionInfo:
    """Information about a network connection."""
    local_address: Tuple[str, int]
    remote_address: Optional[Tuple[str, int]] = None
    protocol: str = "TCP"
    connected_at: float = 0.0


def create_tcp_socket(
    timeout: Optional[float] = None,
    reuse_addr: bool = True
) -> socket.socket:
    """
    Create a TCP socket with common options.
    
    Args:
        timeout: Socket timeout in seconds (None for blocking)
        reuse_addr: Enable SO_REUSEADDR option
        
    Returns:
        Configured TCP socket
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    if reuse_addr:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    if timeout is not None:
        sock.settimeout(timeout)
    
    return sock


def create_udp_socket(
    timeout: Optional[float] = None,
    broadcast: bool = False
) -> socket.socket:
    """
    Create a UDP socket with common options.
    
    Args:
        timeout: Socket timeout in seconds (None for blocking)
        broadcast: Enable SO_BROADCAST option
        
    Returns:
        Configured UDP socket
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    if broadcast:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    if timeout is not None:
        sock.settimeout(timeout)
    
    return sock


def format_address(address: Tuple[str, int]) -> str:
    """Format an address tuple as 'host:port'."""
    return f"{address[0]}:{address[1]}"


def parse_address(address_str: str, default_port: int = 9090) -> Tuple[str, int]:
    """
    Parse an address string into (host, port) tuple.
    
    Args:
        address_str: Address in format 'host:port' or just 'host'
        default_port: Port to use if not specified
        
    Returns:
        Tuple of (host, port)
    """
    if ':' in address_str:
        host, port_str = address_str.rsplit(':', 1)
        return (host, int(port_str))
    return (address_str, default_port)


def get_local_ip() -> str:
    """
    Get the local IP address used for external connections.
    
    Returns:
        Local IP address as string
    """
    try:
        # Create a UDP socket and connect to an external address
        # This doesn't actually send any data, just determines the route
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"


def is_port_available(port: int, host: str = "127.0.0.1") -> bool:
    """
    Check if a TCP port is available for binding.
    
    Args:
        port: Port number to check
        host: Host address to check
        
    Returns:
        True if port is available
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            return True
    except OSError:
        return False


def wait_for_port(
    port: int,
    host: str = "127.0.0.1",
    timeout: float = 30.0,
    interval: float = 0.5
) -> bool:
    """
    Wait for a TCP port to become available for connection.
    
    Args:
        port: Port number to wait for
        host: Host address
        timeout: Maximum time to wait in seconds
        interval: Time between checks in seconds
        
    Returns:
        True if port became available, False if timeout
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1.0)
                s.connect((host, port))
                return True
        except (ConnectionRefusedError, socket.timeout, OSError):
            time.sleep(interval)
    
    return False


def measure_rtt(
    host: str,
    port: int,
    message: bytes = b"ping",
    timeout: float = 5.0
) -> Optional[float]:
    """
    Measure round-trip time to a TCP server.
    
    Args:
        host: Server host
        port: Server port
        message: Message to send
        timeout: Socket timeout
        
    Returns:
        RTT in milliseconds, or None if failed
    """
    try:
        with create_tcp_socket(timeout=timeout) as sock:
            start_time = time.perf_counter()
            sock.connect((host, port))
            sock.sendall(message)
            sock.recv(1024)
            end_time = time.perf_counter()
            return (end_time - start_time) * 1000
    except Exception:
        return None


def calculate_checksum(data: bytes) -> int:
    """
    Calculate a simple checksum for data verification.
    
    Uses a 16-bit one's complement sum (similar to IP/TCP checksum).
    
    Args:
        data: Bytes to checksum
        
    Returns:
        16-bit checksum value
    """
    if len(data) % 2 == 1:
        data += b'\x00'
    
    checksum = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i + 1]
        checksum += word
        checksum = (checksum & 0xFFFF) + (checksum >> 16)
    
    return ~checksum & 0xFFFF


class SimpleProtocol:
    """
    A simple framing protocol for TCP messages.
    
    Format: [4-byte length][payload]
    """
    
    HEADER_SIZE = 4
    MAX_MESSAGE_SIZE = 1024 * 1024  # 1MB
    
    @staticmethod
    def encode(message: bytes) -> bytes:
        """Encode a message with length prefix."""
        length = len(message)
        if length > SimpleProtocol.MAX_MESSAGE_SIZE:
            raise ValueError(f"Message too large: {length} bytes")
        header = struct.pack(">I", length)
        return header + message
    
    @staticmethod
    def decode_header(header: bytes) -> int:
        """Decode the length from a header."""
        if len(header) != SimpleProtocol.HEADER_SIZE:
            raise ValueError("Invalid header size")
        return struct.unpack(">I", header)[0]
    
    @staticmethod
    def recv_message(sock: socket.socket) -> bytes:
        """Receive a complete framed message."""
        # Read header
        header = b""
        while len(header) < SimpleProtocol.HEADER_SIZE:
            chunk = sock.recv(SimpleProtocol.HEADER_SIZE - len(header))
            if not chunk:
                raise ConnectionError("Connection closed while reading header")
            header += chunk
        
        # Parse length
        length = SimpleProtocol.decode_header(header)
        if length > SimpleProtocol.MAX_MESSAGE_SIZE:
            raise ValueError(f"Message too large: {length} bytes")
        
        # Read payload
        payload = b""
        while len(payload) < length:
            chunk = sock.recv(min(4096, length - len(payload)))
            if not chunk:
                raise ConnectionError("Connection closed while reading payload")
            payload += chunk
        
        return payload
    
    @staticmethod
    def send_message(sock: socket.socket, message: bytes) -> None:
        """Send a complete framed message."""
        sock.sendall(SimpleProtocol.encode(message))


if __name__ == "__main__":
    # Quick self-test
    print("Network Utilities Self-Test")
    print("=" * 40)
    print(f"Local IP: {get_local_ip()}")
    print(f"Port 9090 available: {is_port_available(9090)}")
    
    # Test protocol encoding
    test_msg = b"Hello, Network!"
    encoded = SimpleProtocol.encode(test_msg)
    print(f"Protocol test: {len(test_msg)} bytes → {len(encoded)} bytes framed")
    
    # Test checksum
    checksum = calculate_checksum(test_msg)
    print(f"Checksum: 0x{checksum:04X}")
    
    print("=" * 40)
    print("All tests passed!")
