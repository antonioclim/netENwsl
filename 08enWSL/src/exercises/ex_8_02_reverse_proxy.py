#!/usr/bin/env python3
"""
Exercise 8.02: Reverse Proxy with Round-Robin Load Balancing

This exercise guides you through implementing a reverse proxy that
distributes incoming requests across multiple backend servers using
the round-robin algorithm.

Learning Objectives:
- Understand reverse proxy architecture and purpose
- Implement round-robin load balancing with thread safety
- Forward HTTP requests while preserving headers
- Add proxy-specific headers (X-Forwarded-For)

Estimated Time: 40-50 minutes
Difficulty: Advanced

Pair Programming Notes:
- Driver: Implement RoundRobinBalancer class (Section 1)
- Navigator: Verify thread safety, check modulo arithmetic
- Swap after: Completing RoundRobinBalancer.next_backend()
- Second Driver: Implement add_proxy_headers() and forward_request()
- Second Navigator: Test with multiple concurrent requests

Author: ing. dr. Antonio Clim
Course: Computer Networks - ASE, CSIE
"""

import socket
import threading
import argparse
from datetime import datetime
from typing import Optional

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

DEFAULT_PORT = 8888
BUFFER_SIZE = 8192
CONNECTION_TIMEOUT = 10  # seconds


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1: ROUND-ROBIN LOAD BALANCER
# ═══════════════════════════════════════════════════════════════════════════════

# 💭 PREDICTION: If you have 3 backends and send 9 requests, how many
#    requests will each backend receive with round-robin?
#    What mathematical operation ensures the index wraps around?
#    Think about this before implementing...

class RoundRobinBalancer:
    """
    Thread-safe round-robin load balancer for selecting backend servers.
    
    Round-robin distributes requests sequentially across available backends:
    Request 1 → Backend A
    Request 2 → Backend B
    Request 3 → Backend C
    Request 4 → Backend A (cycle repeats)
    
    Thread safety is essential because multiple client connections
    may be processed concurrently.
    
    Example:
        >>> balancer = RoundRobinBalancer([('127.0.0.1', 9001), ('127.0.0.1', 9002)])
        >>> balancer.next_backend()
        ('127.0.0.1', 9001)
        >>> balancer.next_backend()
        ('127.0.0.1', 9002)
        >>> balancer.next_backend()
        ('127.0.0.1', 9001)
    """
    
    def __init__(self, backends: list[tuple[str, int]]) -> None:
        """
        Initialise the load balancer with a list of backend servers.
        
        Args:
            backends: List of (host, port) tuples for backend servers
            
        Example:
            >>> backends = [('localhost', 9001), ('localhost', 9002), ('localhost', 9003)]
            >>> balancer = RoundRobinBalancer(backends)
        """
        # TODO: Implement initialisation
        #
        # Steps:
        # 1. Store the backends list
        # 2. Initialise index to 0
        # 3. Create a threading.Lock for thread safety
        #
        # Why a lock? Multiple threads may call next_backend() simultaneously.
        # Without a lock, two threads could get the same backend.
        
        pass  # Replace with your implementation
    
    def next_backend(self) -> Optional[tuple[str, int]]:
        """
        Get the next backend server using round-robin selection.
        
        Returns:
            Tuple of (host, port) for the selected backend
            Returns None if no backends are available
            
        Thread Safety:
            This method is thread-safe. Multiple threads can call it
            simultaneously without race conditions.
        """
        # TODO: Implement round-robin selection
        #
        # Steps:
        # 1. Acquire the lock (use 'with self.lock:')
        # 2. Check if backends list is empty - return None if so
        # 3. Get the backend at current index
        # 4. Increment index with wraparound: (index + 1) % len(backends)
        # 5. Return the selected backend
        #
        # KEY INSIGHT: The modulo operation (%) makes the index wrap around:
        #   0 → 1 → 2 → 0 → 1 → 2 → ... (with 3 backends)
        
        pass  # Replace with your implementation
    
    def add_backend(self, host: str, port: int) -> None:
        """Add a new backend server to the pool."""
        # TODO: Implement backend addition (thread-safe)
        pass
    
    def remove_backend(self, host: str, port: int) -> bool:
        """Remove a backend server from the pool. Returns True if found."""
        # TODO: Implement backend removal (thread-safe)
        pass


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2: PROXY HEADER MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════

# 💭 PREDICTION: What header tells the backend server the original client IP?
#    What if the request already has this header (from another proxy)?
#    Think about this before implementing...

def add_proxy_headers(request_str: str, client_ip: str) -> str:
    """
    Add or update proxy-related headers in the HTTP request.
    
    Headers added:
    - X-Forwarded-For: Chain of client IPs through proxies
    - X-Real-IP: Original client IP (for simple cases)
    
    If X-Forwarded-For already exists, append the new IP to the chain.
    This creates a trail showing all proxies the request passed through.
    
    Args:
        request_str: Original HTTP request as string
        client_ip: IP address of the connecting client
        
    Returns:
        Modified HTTP request with proxy headers
        
    Example:
        >>> req = "GET / HTTP/1.1\\r\\nHost: backend\\r\\n\\r\\n"
        >>> modified = add_proxy_headers(req, "192.168.1.100")
        >>> "X-Forwarded-For: 192.168.1.100" in modified
        True
        
        # With existing X-Forwarded-For:
        >>> req = "GET / HTTP/1.1\\r\\nX-Forwarded-For: 10.0.0.1\\r\\n\\r\\n"
        >>> modified = add_proxy_headers(req, "192.168.1.100")
        >>> "X-Forwarded-For: 10.0.0.1, 192.168.1.100" in modified
        True
    """
    # TODO: Implement proxy header injection
    #
    # Steps:
    # 1. Split request into lines on '\r\n'
    # 2. Find if X-Forwarded-For header exists
    # 3. If exists: append client_ip to existing value
    # 4. If not exists: insert new X-Forwarded-For header
    # 5. Also add X-Real-IP header with client_ip
    # 6. Rejoin lines with '\r\n'
    #
    # IMPORTANT: Insert headers BEFORE the blank line that ends headers!
    
    pass  # Replace with your implementation


def modify_host_header(request_str: str, backend_host: str, backend_port: int) -> str:
    """
    Update the Host header to match the backend server.
    
    Some backend servers validate the Host header and reject requests
    where Host doesn't match their expected hostname.
    
    Args:
        request_str: Original HTTP request as string
        backend_host: Backend server hostname
        backend_port: Backend server port
        
    Returns:
        Request with modified Host header
    """
    # TODO: Implement Host header modification
    #
    # Steps:
    # 1. Find the Host header line
    # 2. Replace its value with backend_host:backend_port
    # 3. Return modified request
    
    pass  # Replace with your implementation


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3: REQUEST FORWARDING
# ═══════════════════════════════════════════════════════════════════════════════

# 💭 PREDICTION: What happens if a backend server takes too long to respond?
#    How do you ensure you receive the COMPLETE response?
#    Think about this before implementing...

def forward_request(
    request: bytes,
    backend_host: str,
    backend_port: int,
    client_ip: str
) -> bytes:
    """
    Forward an HTTP request to a backend server and return the response.
    
    This function:
    1. Connects to the backend server
    2. Adds proxy headers to the request
    3. Sends the modified request
    4. Receives and returns the complete response
    
    Args:
        request: Original HTTP request bytes from client
        backend_host: Backend server hostname
        backend_port: Backend server port
        client_ip: Original client IP address
        
    Returns:
        Complete HTTP response from backend as bytes
        
    Raises:
        ConnectionError: If unable to connect to backend
        TimeoutError: If backend doesn't respond in time
    """
    # TODO: Implement request forwarding
    #
    # Steps:
    # 1. Create a new TCP socket for backend connection
    # 2. Set socket timeout to CONNECTION_TIMEOUT
    # 3. Connect to (backend_host, backend_port)
    # 4. Decode request bytes to string
    # 5. Add proxy headers with add_proxy_headers()
    # 6. Optionally modify Host header
    # 7. Encode back to bytes and send to backend
    # 8. Receive response in a loop until no more data
    # 9. Close the backend socket
    # 10. Return the complete response
    #
    # IMPORTANT: Use a loop for recv() because responses may be larger
    # than BUFFER_SIZE and arrive in multiple chunks!
    
    pass  # Replace with your implementation


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4: BACKEND HEALTH CHECKING
# ═══════════════════════════════════════════════════════════════════════════════

# 💭 PREDICTION: How can you quickly test if a backend is alive?
#    What timeout is appropriate for a health check?
#    Think about this before implementing...

def check_backend_health(host: str, port: int, timeout: float = 2.0) -> bool:
    """
    Check if a backend server is alive and accepting connections.
    
    This performs a simple TCP connection test. For more thorough
    health checks, you could send an HTTP HEAD request to a /health
    endpoint.
    
    Args:
        host: Backend hostname
        port: Backend port
        timeout: Connection timeout in seconds
        
    Returns:
        True if backend is reachable, False otherwise
        
    Example:
        >>> check_backend_health('localhost', 9001)
        True
        >>> check_backend_health('localhost', 9999)  # Nothing running
        False
    """
    # TODO: Implement health check
    #
    # Steps:
    # 1. Create a TCP socket
    # 2. Set timeout
    # 3. Try to connect
    # 4. If successful, close socket and return True
    # 5. If any exception, return False
    #
    # NOTE: A more complete health check would:
    # - Send "HEAD /health HTTP/1.1\r\n..."
    # - Check for 200 OK response
    # - This ensures the HTTP server is working, not just TCP
    
    pass  # Replace with your implementation


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5: CLIENT CONNECTION HANDLER
# ═══════════════════════════════════════════════════════════════════════════════

def handle_client(
    client_socket: socket.socket,
    client_addr: tuple,
    balancer: RoundRobinBalancer
) -> None:
    """
    Handle a single client connection.
    
    This function runs in a separate thread for each client.
    
    Args:
        client_socket: Socket connected to the client
        client_addr: Client's (ip, port) tuple
        balancer: Round-robin balancer for backend selection
    """
    client_ip = client_addr[0]
    
    try:
        # Receive request from client
        request = client_socket.recv(BUFFER_SIZE)
        
        if not request:
            return
        
        # Log the request
        request_line = request.split(b'\r\n')[0].decode('utf-8', errors='ignore')
        print(f"[{datetime.now().isoformat()}] {client_ip} -> {request_line}")
        
        # Select backend
        backend = balancer.next_backend()
        
        if backend is None:
            # No backends available
            error_response = (
                b"HTTP/1.1 503 Service Unavailable\r\n"
                b"Content-Type: text/plain\r\n"
                b"Content-Length: 23\r\n"
                b"\r\n"
                b"No backends available\r\n"
            )
            client_socket.sendall(error_response)
            return
        
        backend_host, backend_port = backend
        print(f"    -> Forwarding to {backend_host}:{backend_port}")
        
        # Forward request to backend
        try:
            response = forward_request(request, backend_host, backend_port, client_ip)
            client_socket.sendall(response)
            
        except (ConnectionError, TimeoutError) as e:
            print(f"    -> Backend error: {e}")
            error_response = (
                b"HTTP/1.1 502 Bad Gateway\r\n"
                b"Content-Type: text/plain\r\n"
                b"Content-Length: 15\r\n"
                b"\r\n"
                b"Backend error\r\n"
            )
            client_socket.sendall(error_response)
            
    except Exception as e:
        print(f"Error handling client {client_ip}: {e}")
        
    finally:
        client_socket.close()


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 6: PROXY SERVER MAIN LOOP
# ═══════════════════════════════════════════════════════════════════════════════

def run_proxy(host: str, port: int, backends: list[tuple[str, int]]) -> None:
    """
    Run the reverse proxy server.
    
    Args:
        host: Address to bind the proxy to
        port: Port to listen on
        backends: List of (host, port) tuples for backend servers
    """
    # Create load balancer
    balancer = RoundRobinBalancer(backends)
    
    # Create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(10)
    
    print(f"Reverse Proxy running on http://{host}:{port}")
    print(f"Backends: {backends}")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            # Accept client connection
            client_socket, client_addr = server_socket.accept()
            
            # Handle in separate thread
            thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_addr, balancer)
            )
            thread.daemon = True
            thread.start()
            
    except KeyboardInterrupt:
        print("\nShutting down proxy...")
    finally:
        server_socket.close()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def parse_backends(backend_str: str) -> list[tuple[str, int]]:
    """
    Parse backend specification string into list of (host, port) tuples.
    
    Args:
        backend_str: Comma-separated list like "host1:port1,host2:port2"
        
    Returns:
        List of (host, port) tuples
        
    Example:
        >>> parse_backends("localhost:9001,localhost:9002")
        [('localhost', 9001), ('localhost', 9002)]
    """
    backends = []
    for spec in backend_str.split(','):
        spec = spec.strip()
        if ':' in spec:
            host, port = spec.rsplit(':', 1)
            backends.append((host, int(port)))
    return backends


def main() -> int:
    """Parse arguments and start the proxy."""
    parser = argparse.ArgumentParser(
        description="Reverse Proxy with Round-Robin Load Balancing - Week 8 Exercise"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host address to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Port to listen on (default: {DEFAULT_PORT})"
    )
    parser.add_argument(
        "--backends",
        required=True,
        help="Comma-separated backend servers (e.g., localhost:9001,localhost:9002)"
    )
    
    args = parser.parse_args()
    
    backends = parse_backends(args.backends)
    
    if not backends:
        print("Error: No valid backends specified")
        return 1
    
    run_proxy(args.host, args.port, backends)
    return 0


if __name__ == "__main__":
    exit(main())
