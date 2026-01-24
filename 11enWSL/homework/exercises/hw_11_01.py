#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
  Homework 11.01 – Extended Load Balancer with Active Health Checks
═══════════════════════════════════════════════════════════════════════════════

NETWORKING class - ASE, Informatics | by Revolvix
Week 11: Application Protocols - FTP, DNS, SSH and Load Balancing

LEVEL: Advanced
ESTIMATED TIME: 45-60 minutes

PAIR PROGRAMMING NOTES:
  - Driver: Implement health check logic, test with backends
  - Navigator: Verify timing intervals, check thread safety
  - Swap after: Each major feature (health checks, weighted RR, stats endpoint)

This assignment extends the laboratory load balancer with:
1. Active health checks (periodic HTTP probes)
2. Weighted round-robin distribution
3. Statistics endpoint (/stats)
4. Graceful degradation when all backends fail

PREDICTION PROMPTS:
  💭 Before testing: How quickly will a failed backend be detected with active checks?
  💭 Before weighted test: With weights 3:2:1, what percentage goes to each backend?
  💭 Before stopping all backends: What response will clients receive?

Usage:
    python hw_11_01.py --backends host:port:weight,host:port:weight --listen host:port
    
Example:
    python hw_11_01.py --backends localhost:8081:3,localhost:8082:2,localhost:8083:1 --listen 0.0.0.0:8080
═══════════════════════════════════════════════════════════════════════════════
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import argparse
import socket
import threading
import time
import json
from dataclasses import dataclass, field
from typing import Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION_CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════
HEALTH_CHECK_INTERVAL = 5.0      # Seconds between health checks
HEALTH_CHECK_TIMEOUT = 2.0       # Timeout for health check requests
UNHEALTHY_THRESHOLD = 3          # Consecutive failures to mark unhealthy
HEALTHY_THRESHOLD = 2            # Consecutive successes to mark healthy
SOCKET_TIMEOUT = 5.0             # Timeout for client requests


# ═══════════════════════════════════════════════════════════════════════════════
# DATA_STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Backend:
    """
    Represents a backend server with health tracking.
    
    Attributes:
        host: Backend hostname or IP address
        port: Backend port number
        weight: Distribution weight (higher = more traffic)
        healthy: Current health status
        consecutive_fails: Count of consecutive health check failures
        consecutive_successes: Count of consecutive health check successes
        total_requests: Total requests forwarded to this backend
        active_connections: Current number of active connections
    """
    host: str
    port: int
    weight: int = 1
    healthy: bool = True
    consecutive_fails: int = 0
    consecutive_successes: int = 0
    total_requests: int = 0
    active_connections: int = 0
    
    @property
    def address(self) -> tuple[str, int]:
        """Return (host, port) tuple."""
        return (self.host, self.port)
    
    def __str__(self) -> str:
        status = "UP" if self.healthy else "DOWN"
        return f"{self.host}:{self.port} (w={self.weight}, {status})"


@dataclass
class Statistics:
    """
    Load balancer statistics.
    
    TODO: Add any additional fields you need for tracking.
    """
    total_requests: int = 0
    start_time: float = field(default_factory=time.time)
    
    def to_dict(self) -> dict:
        """Convert statistics to dictionary for JSON serialisation."""
        uptime = time.time() - self.start_time
        return {
            "total_requests": self.total_requests,
            "uptime_seconds": round(uptime, 2),
            "requests_per_second": round(self.total_requests / uptime, 2) if uptime > 0 else 0
        }


# ═══════════════════════════════════════════════════════════════════════════════
# HEALTH_CHECKER_CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class HealthChecker:
    """
    Background health checker that periodically probes backends.
    
    TODO: Implement the health checking logic.
    
    Hints:
    - Use threading.Thread with daemon=True
    - Send HTTP GET to /health or / endpoint
    - Track consecutive failures/successes
    - Update backend.healthy based on thresholds
    """
    
    def __init__(self, backends: list[Backend], interval: float = HEALTH_CHECK_INTERVAL):
        """
        Initialise the health checker.
        
        Args:
            backends: List of Backend objects to monitor
            interval: Seconds between health check rounds
        """
        self.backends = backends
        self.interval = interval
        self.running = False
        self._thread: Optional[threading.Thread] = None
    
    # ─── START_HEALTH_CHECKER ─────────────────────────────────────────────────
    def start(self) -> None:
        """Start the health check background thread."""
        # TODO: Implement this method
        # 1. Set self.running = True
        # 2. Create a daemon thread targeting self._run_checks
        # 3. Start the thread
        pass
    
    # ─── STOP_HEALTH_CHECKER ──────────────────────────────────────────────────
    def stop(self) -> None:
        """Stop the health check thread."""
        self.running = False
        if self._thread:
            self._thread.join(timeout=2.0)
    
    # ─── HEALTH_CHECK_LOOP ────────────────────────────────────────────────────
    def _run_checks(self) -> None:
        """Main health check loop (runs in background thread)."""
        # TODO: Implement this method
        # while self.running:
        #     for backend in self.backends:
        #         self._check_backend(backend)
        #     time.sleep(self.interval)
        pass
    
    # ─── CHECK_SINGLE_BACKEND ─────────────────────────────────────────────────
    def _check_backend(self, backend: Backend) -> None:
        """
        Perform health check on a single backend.
        
        TODO: Implement this method
        
        Steps:
        1. Create socket connection to backend
        2. Send HTTP GET /health request
        3. Check for 200 OK response
        4. Update consecutive_fails or consecutive_successes
        5. Update backend.healthy based on thresholds
        """
        pass


# ═══════════════════════════════════════════════════════════════════════════════
# LOAD_BALANCER_CLASS
# ═══════════════════════════════════════════════════════════════════════════════

class WeightedLoadBalancer:
    """
    Load balancer with weighted round-robin and health checking.
    
    TODO: Complete the implementation.
    """
    
    def __init__(self, backends: list[Backend], listen_host: str, listen_port: int):
        """
        Initialise the load balancer.
        
        Args:
            backends: List of Backend objects
            listen_host: Host to listen on
            listen_port: Port to listen on
        """
        self.backends = backends
        self.listen_host = listen_host
        self.listen_port = listen_port
        self.stats = Statistics()
        self.health_checker = HealthChecker(backends)
        
        # Weighted round-robin state
        self._weighted_list: list[Backend] = []
        self._current_index = 0
        self._rebuild_weighted_list()
        
        # Lock for thread-safe operations
        self._lock = threading.Lock()
    
    # ─── BUILD_WEIGHTED_LIST ──────────────────────────────────────────────────
    def _rebuild_weighted_list(self) -> None:
        """
        Build weighted list for round-robin selection.
        
        Each backend appears 'weight' times in the list.
        Example: backend with weight=3 appears 3 times.
        """
        # TODO: Implement this method
        # self._weighted_list = []
        # for backend in self.backends:
        #     self._weighted_list.extend([backend] * backend.weight)
        pass
    
    # ─── GET_HEALTHY_BACKENDS ─────────────────────────────────────────────────
    def get_healthy_backends(self) -> list[Backend]:
        """Return list of currently healthy backends."""
        return [b for b in self.backends if b.healthy]
    
    # ─── SELECT_BACKEND ───────────────────────────────────────────────────────
    def select_backend(self) -> Optional[Backend]:
        """
        Select next backend using weighted round-robin.
        
        TODO: Implement this method
        
        Returns:
            Backend object or None if all backends are unhealthy
        
        Hints:
        - Filter weighted list to only healthy backends
        - Use self._current_index for rotation
        - Increment index with modulo
        """
        pass
    
    # ─── HANDLE_STATS_ENDPOINT ────────────────────────────────────────────────
    def handle_stats_request(self, client_socket: socket.socket) -> None:
        """
        Handle /stats endpoint request.
        
        TODO: Implement this method
        
        Should return JSON with:
        - total_requests
        - requests_per_backend: {backend_addr: count}
        - backend_health: {backend_addr: healthy}
        - active_connections: {backend_addr: count}
        """
        # TODO: Build stats dictionary
        stats_data = self.stats.to_dict()
        stats_data["backends"] = {}
        
        for backend in self.backends:
            key = f"{backend.host}:{backend.port}"
            stats_data["backends"][key] = {
                "healthy": backend.healthy,
                "total_requests": backend.total_requests,
                "active_connections": backend.active_connections,
                "weight": backend.weight
            }
        
        # Send JSON response
        response_body = json.dumps(stats_data, indent=2)
        response = (
            f"HTTP/1.1 200 OK\r\n"
            f"Content-Type: application/json\r\n"
            f"Content-Length: {len(response_body)}\r\n"
            f"\r\n"
            f"{response_body}"
        )
        client_socket.sendall(response.encode())
    
    # ─── HANDLE_SERVICE_UNAVAILABLE ───────────────────────────────────────────
    def handle_service_unavailable(self, client_socket: socket.socket) -> None:
        """Send 503 Service Unavailable response."""
        response = (
            "HTTP/1.1 503 Service Unavailable\r\n"
            "Content-Type: text/plain\r\n"
            "Content-Length: 19\r\n"
            "\r\n"
            "Service Unavailable"
        )
        client_socket.sendall(response.encode())
    
    # ─── FORWARD_REQUEST_TO_BACKEND ───────────────────────────────────────────
    def forward_request(self, client_socket: socket.socket, request: bytes, backend: Backend) -> bool:
        """
        Forward client request to selected backend.
        
        TODO: Implement this method
        
        Steps:
        1. Increment backend.active_connections
        2. Connect to backend
        3. Send request
        4. Receive response
        5. Forward response to client
        6. Decrement backend.active_connections
        7. Increment backend.total_requests
        
        Returns:
            True if successful, False if backend failed
        """
        pass
    
    # ─── HANDLE_CLIENT_CONNECTION ─────────────────────────────────────────────
    def handle_client(self, client_socket: socket.socket, client_addr: tuple) -> None:
        """
        Handle incoming client connection.
        
        TODO: Complete this method
        """
        try:
            client_socket.settimeout(SOCKET_TIMEOUT)
            request = client_socket.recv(8192)
            
            if not request:
                return
            
            # Parse request line to check for /stats endpoint
            request_line = request.decode('utf-8', errors='ignore').split('\r\n')[0]
            method, path, *_ = request_line.split(' ')
            
            # Handle stats endpoint
            if path == '/stats':
                self.handle_stats_request(client_socket)
                return
            
            # TODO: Select backend and forward request
            # backend = self.select_backend()
            # if backend is None:
            #     self.handle_service_unavailable(client_socket)
            #     return
            # self.forward_request(client_socket, request, backend)
            
            with self._lock:
                self.stats.total_requests += 1
            
        except Exception as e:
            logger.error(f"Error handling client {client_addr}: {e}")
        finally:
            client_socket.close()
    
    # ─── RUN_SERVER ───────────────────────────────────────────────────────────
    def run(self) -> None:
        """Start the load balancer."""
        # Start health checker
        self.health_checker.start()
        
        # Create listening socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.listen_host, self.listen_port))
        server.listen(128)
        
        logger.info(f"Load balancer listening on {self.listen_host}:{self.listen_port}")
        logger.info(f"Backends: {', '.join(str(b) for b in self.backends)}")
        logger.info(f"Health check interval: {HEALTH_CHECK_INTERVAL}s")
        logger.info("Press Ctrl+C to stop")
        
        try:
            while True:
                client_socket, client_addr = server.accept()
                # Handle each client in a separate thread
                thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_addr)
                )
                thread.start()
        except KeyboardInterrupt:
            logger.info("Shutting down...")
        finally:
            self.health_checker.stop()
            server.close()


# ═══════════════════════════════════════════════════════════════════════════════
# PARSE_ARGUMENTS
# ═══════════════════════════════════════════════════════════════════════════════

def parse_backends(backends_str: str) -> list[Backend]:
    """
    Parse backends string into list of Backend objects.
    
    Format: host:port:weight,host:port:weight,...
    Weight is optional (default: 1)
    
    Examples:
        "localhost:8081:3,localhost:8082:2"
        "localhost:8081,localhost:8082"  # weight=1 for both
    """
    backends = []
    for part in backends_str.split(','):
        parts = part.strip().split(':')
        if len(parts) == 2:
            host, port = parts
            weight = 1
        elif len(parts) == 3:
            host, port, weight = parts
            weight = int(weight)
        else:
            raise ValueError(f"Invalid backend format: {part}")
        
        backends.append(Backend(host=host, port=int(port), weight=weight))
    
    return backends


def build_argument_parser() -> argparse.ArgumentParser:
    """Build command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Week 11 Homework: Extended Load Balancer with Health Checks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python hw_11_01.py --backends localhost:8081:3,localhost:8082:2,localhost:8083:1
  python hw_11_01.py --backends localhost:8081,localhost:8082 --listen 0.0.0.0:9000
        """
    )
    
    parser.add_argument(
        '--backends', '-b',
        required=True,
        help='Backend servers (format: host:port:weight,...)'
    )
    parser.add_argument(
        '--listen', '-l',
        default='0.0.0.0:8080',
        help='Listen address (default: 0.0.0.0:8080)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    return parser


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Entry point for extended load balancer homework."""
    parser = build_argument_parser()
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Parse listen address
    listen_parts = args.listen.split(':')
    listen_host = listen_parts[0]
    listen_port = int(listen_parts[1])
    
    # Parse backends
    backends = parse_backends(args.backends)
    
    if not backends:
        logger.error("No backends specified")
        return 1
    
    # Create and run load balancer
    lb = WeightedLoadBalancer(backends, listen_host, listen_port)
    lb.run()
    
    return 0


if __name__ == '__main__':
    exit(main())
