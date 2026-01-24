#!/usr/bin/env python3
"""
Homework Assignment 2: Weighted Round-Robin Load Balancer
NETWORKING class - ASE, Informatics | by Revolvix

Week 14 - Computer Networks Laboratory

OBJECTIVE:
Extend the load balancer to support weighted round-robin distribution
and implement additional load balancing algorithms.

REQUIREMENTS:
1. Implement weighted round-robin algorithm
2. Add support for least-connections algorithm
3. Implement backend weight configuration via API
4. Add real-time statistics endpoint
5. Support dynamic backend addition/removal

LOAD BALANCING ALGORITHMS TO IMPLEMENT:

1. WEIGHTED ROUND-ROBIN
   - Each backend has a weight (1-10)
   - Higher weight = more requests
   - Example: app1(weight=3), app2(weight=1) -> app1 gets 75% of requests
   
2. LEAST CONNECTIONS
   - Route to backend with fewest active connections
   - Track connection count per backend
   - Useful for long-lived connections

3. RANDOM
   - Randomly select a healthy backend
   - Simplest algorithm
   - Good for testing

API ENDPOINTS TO IMPLEMENT:

GET /status
    Returns: Current backend status, algorithm, statistics

GET /backends
    Returns: List of all backends with weights and health

POST /backends
    Body: {"host": "app3", "port": 8001, "weight": 2}
    Action: Add new backend

DELETE /backends/<host>
    Action: Remove backend from pool

PUT /backends/<host>/weight
    Body: {"weight": 5}
    Action: Update backend weight

GET /algorithm
    Returns: Current algorithm name

PUT /algorithm
    Body: {"algorithm": "weighted-round-robin"}
    Action: Switch algorithm

GET /stats
    Returns: Request counts, latencies, error rates per backend

EVALUATION CRITERIA:
- Algorithm correctness (30%)
- API implementation (25%)
- Statistics accuracy (20%)
- Code quality (15%)
- Testing thoroughness (10%)

HINTS:
- Use a generator for weighted round-robin cycling
- Track connection counts with thread-safe counters
- Consider using asyncio for better concurrency
- Test with different weight distributions
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import socket
import threading
import json
import time
import random
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable, Any
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import re


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
LISTEN_HOST = '0.0.0.0'
LISTEN_PORT = 8081  # Different from lab LB


# ═══════════════════════════════════════════════════════════════════════════════
# PREDICTION_PROMPT
# ═══════════════════════════════════════════════════════════════════════════════
def prompt_prediction() -> None:
    """Ask student to predict load balancer behaviour."""
    print("\n💭 PREDICTION: With weights 3:1, how many of 100 requests go to backend 1?")
    print("   Options: a) 50  b) 75  c) 30  d) Depends on algorithm")
    try:
        prediction = input("   Your answer (a/b/c/d): ").strip()
        if prediction:
            print(f"   Let's implement and measure!\n")
    except (EOFError, KeyboardInterrupt):
        print("\n")


# ═══════════════════════════════════════════════════════════════════════════════
# DATA_MODELS
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class Backend:
    """Represents a backend server."""
    host: str
    port: int
    weight: int = 1
    healthy: bool = True
    active_connections: int = 0
    total_requests: int = 0
    total_errors: int = 0
    total_latency_ms: float = 0.0
    
    @property
    def address(self) -> str:
        return f"{self.host}:{self.port}"
    
    @property
    def avg_latency_ms(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return self.total_latency_ms / self.total_requests
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'host': self.host,
            'port': self.port,
            'weight': self.weight,
            'healthy': self.healthy,
            'active_connections': self.active_connections,
            'total_requests': self.total_requests,
            'total_errors': self.total_errors,
            'avg_latency_ms': round(self.avg_latency_ms, 2)
        }


@dataclass
class LoadBalancerStats:
    """Statistics for the load balancer."""
    start_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        uptime = (datetime.now(timezone.utc) - self.start_time).total_seconds()
        return {
            'uptime_seconds': round(uptime, 2),
            'total_requests': self.total_requests,
            'successful_requests': self.successful_requests,
            'failed_requests': self.failed_requests,
            'success_rate': round(
                self.successful_requests / max(1, self.total_requests) * 100, 2
            )
        }


# ═══════════════════════════════════════════════════════════════════════════════
# LOAD_BALANCING_ALGORITHMS
# ═══════════════════════════════════════════════════════════════════════════════
class LoadBalancerAlgorithm:
    """Base class for load balancing algorithms."""
    
    name: str = "base"
    
    def __init__(self, backends: List[Backend]):
        self.backends = backends
    
    def select(self) -> Optional[Backend]:
        """Select a backend to handle the request."""
        raise NotImplementedError
    
    def healthy_backends(self) -> List[Backend]:
        """Get list of healthy backends."""
        return [b for b in self.backends if b.healthy]


class RoundRobinAlgorithm(LoadBalancerAlgorithm):
    """Simple round-robin algorithm."""
    
    name = "round-robin"
    
    def __init__(self, backends: List[Backend]):
        super().__init__(backends)
        self.index = 0
        self.lock = threading.Lock()
    
    def select(self) -> Optional[Backend]:
        """Select next backend in rotation."""
        healthy = self.healthy_backends()
        if not healthy:
            return None
        
        with self.lock:
            # TODO: Implement round-robin selection
            # Return backends in order, cycling through the list
            pass


class WeightedRoundRobinAlgorithm(LoadBalancerAlgorithm):
    """Weighted round-robin algorithm."""
    
    name = "weighted-round-robin"
    
    def __init__(self, backends: List[Backend]):
        super().__init__(backends)
        self.lock = threading.Lock()
        self._build_sequence()
    
    def _build_sequence(self) -> None:
        """
        Build the weighted selection sequence.
        
        For backends with weights [3, 1], the sequence would be:
        [backend1, backend1, backend1, backend2]
        
        This ensures requests are distributed according to weights.
        """
        # TODO: Implement weighted sequence building
        # Create a list where each backend appears 'weight' times
        self.sequence = []
        self.index = 0
    
    def select(self) -> Optional[Backend]:
        """Select backend based on weighted rotation."""
        # TODO: Implement weighted round-robin selection
        # 1. Filter for healthy backends
        # 2. Rebuild sequence if needed
        # 3. Return next in sequence
        pass


class LeastConnectionsAlgorithm(LoadBalancerAlgorithm):
    """Least connections algorithm."""
    
    name = "least-connections"
    
    def select(self) -> Optional[Backend]:
        """Select backend with fewest active connections."""
        # TODO: Implement least-connections selection
        # Return the healthy backend with minimum active_connections
        pass


class RandomAlgorithm(LoadBalancerAlgorithm):
    """Random selection algorithm."""
    
    name = "random"
    
    def select(self) -> Optional[Backend]:
        """Randomly select a healthy backend."""
        healthy = self.healthy_backends()
        if not healthy:
            return None
        return random.choice(healthy)


# ═══════════════════════════════════════════════════════════════════════════════
# LOAD_BALANCER_CORE
# ═══════════════════════════════════════════════════════════════════════════════
class WeightedLoadBalancer:
    """
    Weighted Load Balancer implementation.
    
    TODO: Complete the implementation.
    """
    
    ALGORITHMS = {
        'round-robin': RoundRobinAlgorithm,
        'weighted-round-robin': WeightedRoundRobinAlgorithm,
        'least-connections': LeastConnectionsAlgorithm,
        'random': RandomAlgorithm,
    }
    
    def __init__(self, config: Dict[str, Any]):
        """Initialise load balancer from configuration."""
        self.backends: List[Backend] = []
        self.stats = LoadBalancerStats()
        self.running = True
        
        # Load backends from config
        for backend_config in config.get('backends', []):
            backend = Backend(
                host=backend_config['host'],
                port=backend_config['port'],
                weight=backend_config.get('weight', 1)
            )
            self.backends.append(backend)
        
        # Set algorithm
        algorithm_name = config.get('algorithm', 'round-robin')
        self.set_algorithm(algorithm_name)
        
        # Health check settings
        self.health_check_interval = config.get('health_check_interval', 5)
        self.health_check_path = config.get('health_check_path', '/health')
        
        # Start health check thread
        self.health_thread = threading.Thread(target=self._health_check_loop, daemon=True)
    
    def set_algorithm(self, name: str) -> bool:
        """Set the load balancing algorithm."""
        if name not in self.ALGORITHMS:
            return False
        self.algorithm = self.ALGORITHMS[name](self.backends)
        return True
    
    def get_backend(self) -> Optional[Backend]:
        """Get next backend using current algorithm."""
        return self.algorithm.select()
    
    def add_backend(self, host: str, port: int, weight: int = 1) -> Backend:
        """Add a new backend."""
        backend = Backend(host=host, port=port, weight=weight)
        self.backends.append(backend)
        # Rebuild algorithm with new backend list
        self.algorithm = type(self.algorithm)(self.backends)
        return backend
    
    def remove_backend(self, host: str) -> bool:
        """Remove a backend by hostname."""
        for i, backend in enumerate(self.backends):
            if backend.host == host:
                self.backends.pop(i)
                self.algorithm = type(self.algorithm)(self.backends)
                return True
        return False
    
    def update_weight(self, host: str, weight: int) -> bool:
        """Update backend weight."""
        # TODO: Implement weight update
        pass
    
    def _health_check_loop(self) -> None:
        """Background thread for health checks."""
        while self.running:
            self._perform_health_checks()
            time.sleep(self.health_check_interval)
    
    def _perform_health_checks(self) -> None:
        """Check health of all backends."""
        # TODO: Implement health checking
        pass
    
    def proxy_request(self, method: str, path: str, headers: Dict, body: bytes) -> tuple:
        """Proxy an HTTP request to a backend."""
        backend = self.get_backend()
        if not backend:
            return (503, {}, b'Service Unavailable: No healthy backends')
        
        # TODO: Implement request proxying
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """Get current load balancer status."""
        return {
            'algorithm': self.algorithm.name,
            'backends': [b.to_dict() for b in self.backends],
            'stats': self.stats.to_dict()
        }
    
    def start(self) -> None:
        """Start the load balancer."""
        self.health_thread.start()
    
    def stop(self) -> None:
        """Stop the load balancer."""
        self.running = False


# ═══════════════════════════════════════════════════════════════════════════════
# HTTP_HANDLER
# ═══════════════════════════════════════════════════════════════════════════════
class LoadBalancerHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the load balancer."""
    
    lb: WeightedLoadBalancer = None  # Set by server
    
    def log_message(self, format: str, *args) -> None:
        """Custom log format."""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")
    
    def do_GET(self) -> None:
        """Handle GET requests."""
        parsed = urlparse(self.path)
        path = parsed.path
        
        # Management endpoints
        if path == '/status':
            self._send_json(self.lb.get_status())
        elif path == '/backends':
            self._send_json([b.to_dict() for b in self.lb.backends])
        elif path == '/algorithm':
            self._send_json({'algorithm': self.lb.algorithm.name})
        elif path == '/stats':
            self._send_json(self.lb.stats.to_dict())
        else:
            # Proxy to backend
            self._proxy_request()
    
    def _send_json(self, data: Any, status: int = 200) -> None:
        """Send JSON response."""
        body = json.dumps(data, indent=2).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    
    def _proxy_request(self) -> None:
        """Proxy request to backend."""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else b''
        
        headers = dict(self.headers)
        status, response_headers, response_body = self.lb.proxy_request(
            self.command, self.path, headers, body
        )
        
        self.send_response(status)
        for key, value in response_headers.items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(response_body)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    """Main entry point."""
    print("=" * 50)
    print("Weighted Load Balancer - Homework Assignment 2")
    print("NETWORKING class - ASE, Informatics")
    print("=" * 50)
    print()
    
    prompt_prediction()
    
    # Default configuration
    config = {
        'algorithm': 'weighted-round-robin',
        'backends': [
            {'host': 'app1', 'port': 8001, 'weight': 3},
            {'host': 'app2', 'port': 8001, 'weight': 1},
        ],
        'health_check_interval': 5,
        'health_check_path': '/health'
    }
    
    # Create load balancer
    lb = WeightedLoadBalancer(config)
    lb.start()
    
    # Set up HTTP server
    LoadBalancerHandler.lb = lb
    server = HTTPServer((LISTEN_HOST, LISTEN_PORT), LoadBalancerHandler)
    
    print(f"Starting load balancer on {LISTEN_HOST}:{LISTEN_PORT}")
    print(f"Algorithm: {lb.algorithm.name}")
    print(f"Backends: {len(lb.backends)}")
    print()
    print("Management endpoints:")
    print(f"  GET  http://localhost:{LISTEN_PORT}/status")
    print(f"  GET  http://localhost:{LISTEN_PORT}/backends")
    print(f"  POST http://localhost:{LISTEN_PORT}/backends")
    print(f"  PUT  http://localhost:{LISTEN_PORT}/algorithm")
    print()
    print("Press Ctrl+C to stop")
    print()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down...")
        lb.stop()
        server.shutdown()


if __name__ == "__main__":
    main()
