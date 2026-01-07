#!/usr/bin/env python3
"""
Homework Assignment 2: Weighted Load Balancer
NETWORKING class - ASE, Informatics | by Revolvix

Implement a weighted round-robin load balancer that distributes
requests proportionally to backend capacity.

Usage:
    # Start backends first (in separate terminals):
    python -m http.server 8001 --directory ../www/
    python -m http.server 8002 --directory ../www/
    python -m http.server 8003 --directory ../www/
    
    # Then start the load balancer:
    python hw_8_02_weighted_balancer.py

Testing:
    # Run multiple requests and observe distribution
    for i in {1..18}; do curl -s http://localhost:8000/ | head -1; done
    
    # Expected distribution (weights 5:3:1):
    # Backend 8001: ~55% (10 requests)
    # Backend 8002: ~33% (6 requests)
    # Backend 8003: ~11% (2 requests)
"""

import socket
import threading
import time
from dataclasses import dataclass
from typing import Optional
from urllib.request import urlopen
from urllib.error import URLError


# Configuration
PROXY_PORT = 8000
PROXY_HOST = "0.0.0.0"

# Backend configuration with weights
# Higher weight = more requests
BACKENDS = {
    "127.0.0.1:8001": 5,  # 5x capacity
    "127.0.0.1:8002": 3,  # 3x capacity
    "127.0.0.1:8003": 1,  # 1x capacity (baseline)
}

# Health check configuration
HEALTH_CHECK_INTERVAL = 10  # seconds
HEALTH_CHECK_TIMEOUT = 2    # seconds


@dataclass
class Backend:
    """Represents a backend server."""
    host: str
    port: int
    weight: int
    healthy: bool = True
    current_weight: int = 0
    
    @property
    def address(self) -> str:
        return f"{self.host}:{self.port}"


class WeightedLoadBalancer:
    """
    Weighted round-robin load balancer with health checking.
    
    TODO: Implement the following methods:
    - select_backend(): Choose next backend based on weights
    - check_health(): Verify backend is responding
    - forward_request(): Proxy request to selected backend
    """
    
    def __init__(self, backend_config: dict):
        """
        Initialise load balancer with backend configuration.
        
        Args:
            backend_config: Dict mapping "host:port" to weight
        """
        self.backends = []
        for address, weight in backend_config.items():
            host, port = address.split(":")
            self.backends.append(Backend(
                host=host,
                port=int(port),
                weight=weight,
                current_weight=0
            ))
        
        self.lock = threading.Lock()
        self.stats = {b.address: 0 for b in self.backends}
    
    def select_backend(self) -> Optional[Backend]:
        """
        TODO: Select next backend using weighted round-robin algorithm
        
        Algorithm (Smooth Weighted Round-Robin):
        1. For each backend, add its weight to current_weight
        2. Select backend with highest current_weight
        3. Subtract total weight from selected backend's current_weight
        4. Return selected backend (only if healthy)
        
        Returns:
            Selected Backend or None if all unhealthy
        
        Example with weights {A: 5, B: 3, C: 1}, total = 9:
            Round 1: A(5), B(3), C(1) → select A → A(-4), B(3), C(1)
            Round 2: A(1), B(6), C(2) → select B → A(1), B(-3), C(2)
            ...
        """
        with self.lock:
            # TODO: Implement weighted selection
            # 
            # healthy_backends = [b for b in self.backends if b.healthy]
            # if not healthy_backends:
            #     return None
            # 
            # total_weight = sum(b.weight for b in healthy_backends)
            # 
            # for backend in healthy_backends:
            #     backend.current_weight += backend.weight
            # 
            # selected = max(healthy_backends, key=lambda b: b.current_weight)
            # selected.current_weight -= total_weight
            # 
            # self.stats[selected.address] += 1
            # return selected
            
            raise NotImplementedError("Implement select_backend()")
    
    def check_health(self, backend: Backend) -> bool:
        """
        TODO: Check if backend is healthy
        
        Args:
            backend: Backend to check
        
        Returns:
            True if backend responds within timeout
        
        Requirements:
        - Send HTTP GET to backend
        - Return True if 2xx response within timeout
        - Return False on timeout or error
        """
        # TODO: Implement health check
        # 
        # try:
        #     url = f"http://{backend.address}/"
        #     with urlopen(url, timeout=HEALTH_CHECK_TIMEOUT) as response:
        #         return 200 <= response.status < 300
        # except (URLError, TimeoutError):
        #     return False
        
        raise NotImplementedError("Implement check_health()")
    
    def run_health_checks(self):
        """
        Background thread to periodically check backend health.
        
        TODO: Implement health check loop
        - Check each backend every HEALTH_CHECK_INTERVAL seconds
        - Update backend.healthy status
        - Log status changes
        """
        print("[Health] Starting health checker...")
        
        while True:
            for backend in self.backends:
                # TODO: Check health and update status
                # was_healthy = backend.healthy
                # backend.healthy = self.check_health(backend)
                # 
                # if was_healthy != backend.healthy:
                #     status = "UP" if backend.healthy else "DOWN"
                #     print(f"[Health] {backend.address} is now {status}")
                pass
            
            time.sleep(HEALTH_CHECK_INTERVAL)
    
    def forward_request(self, client_socket: socket.socket, request: bytes) -> bytes:
        """
        TODO: Forward request to selected backend
        
        Args:
            client_socket: Client connection
            request: Raw HTTP request bytes
        
        Returns:
            Response bytes from backend
        
        Requirements:
        - Select backend using weighted algorithm
        - Connect to backend
        - Forward request
        - Read response
        - Add X-Forwarded-For header
        - Return response or 503 if no backends available
        """
        backend = self.select_backend()
        
        if not backend:
            # No healthy backends
            return b"HTTP/1.1 503 Service Unavailable\r\n\r\nNo backends available"
        
        # TODO: Forward to backend
        # 
        # try:
        #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as backend_socket:
        #         backend_socket.connect((backend.host, backend.port))
        #         
        #         # Add X-Forwarded-For header
        #         client_ip = client_socket.getpeername()[0]
        #         modified_request = self.add_forwarded_header(request, client_ip)
        #         
        #         backend_socket.sendall(modified_request)
        #         
        #         response = b""
        #         while True:
        #             chunk = backend_socket.recv(4096)
        #             if not chunk:
        #                 break
        #             response += chunk
        #         
        #         return response
        # except Exception as e:
        #     print(f"[Proxy] Error forwarding to {backend.address}: {e}")
        #     backend.healthy = False
        #     return b"HTTP/1.1 502 Bad Gateway\r\n\r\nBackend error"
        
        raise NotImplementedError("Implement forward_request()")
    
    def add_forwarded_header(self, request: bytes, client_ip: str) -> bytes:
        """
        Add X-Forwarded-For header to request.
        
        Args:
            request: Original request bytes
            client_ip: Client IP address
        
        Returns:
            Modified request with header added
        """
        request_str = request.decode('utf-8', errors='replace')
        lines = request_str.split('\r\n')
        
        # Insert header after request line
        header = f"X-Forwarded-For: {client_ip}"
        lines.insert(1, header)
        
        return '\r\n'.join(lines).encode('utf-8')
    
    def print_stats(self):
        """Print distribution statistics."""
        total = sum(self.stats.values())
        if total == 0:
            return
        
        print("\n[Stats] Request distribution:")
        for backend in self.backends:
            count = self.stats[backend.address]
            pct = (count / total) * 100
            expected = (backend.weight / sum(b.weight for b in self.backends)) * 100
            print(f"  {backend.address} (weight {backend.weight}): "
                  f"{count} requests ({pct:.1f}%, expected {expected:.1f}%)")


def handle_client(client_socket: socket.socket, address: tuple, balancer: WeightedLoadBalancer):
    """Handle client connection."""
    try:
        request = client_socket.recv(8192)
        if not request:
            return
        
        response = balancer.forward_request(client_socket, request)
        client_socket.sendall(response)
        
    except Exception as e:
        print(f"[Proxy] Client error: {e}")
    finally:
        client_socket.close()


def main():
    """Main entry point."""
    print("=" * 60)
    print("Weighted Load Balancer - Week 8 Homework")
    print("NETWORKING class - ASE, Informatics")
    print("=" * 60)
    print()
    
    balancer = WeightedLoadBalancer(BACKENDS)
    
    print(f"[Proxy] Configured backends:")
    for backend in balancer.backends:
        print(f"  {backend.address} (weight: {backend.weight})")
    print()
    
    # Start health checker thread
    health_thread = threading.Thread(target=balancer.run_health_checks, daemon=True)
    health_thread.start()
    
    # Start proxy server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((PROXY_HOST, PROXY_PORT))
    server.listen(100)
    
    print(f"[Proxy] Listening on {PROXY_HOST}:{PROXY_PORT}")
    print("[Proxy] Press Ctrl+C to stop and see statistics")
    print()
    
    try:
        while True:
            client_socket, address = server.accept()
            thread = threading.Thread(
                target=handle_client,
                args=(client_socket, address, balancer)
            )
            thread.start()
    except KeyboardInterrupt:
        print("\n[Proxy] Shutting down...")
        balancer.print_stats()
    finally:
        server.close()


if __name__ == "__main__":
    main()
