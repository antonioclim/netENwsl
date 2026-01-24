#!/usr/bin/env python3
"""
Homework 3.3: TCP Tunnel with Logging and Metrics
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

Student: <Your Name>
Student ID: <Your ID>
Date: <Submission Date>

Description:
Enhance the basic TCP tunnel to provide detailed logging, traffic metrics,
and optional features like connection limits and timeout handling.

Requirements:
- Detailed logging (connections, data transfer, errors)
- Traffic metrics (bytes transferred, connection duration, throughput)
- Maximum connections limit
- Idle connection timeout
- Status display on demand
- Log levels (DEBUG, INFO, WARNING, ERROR)

Usage:
    python hw_3_03.py --listen-port PORT --target-host HOST --target-port PORT
                      [--max-connections N] [--timeout SECONDS] [--log-file FILE]

Example:
    python hw_3_03.py --listen-port 9090 --target-host 172.20.0.10 --target-port 8080
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import socket
import threading
import signal
import sys
import time
import logging
import argparse
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple
from dataclasses import dataclass, field
from collections import defaultdict

# Configuration
DEFAULT_BUFFER_SIZE = 4096
DEFAULT_MAX_CONNECTIONS = 100
DEFAULT_TIMEOUT = 300  # 5 minutes


@dataclass


# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class ConnectionStats:
    """Statistics for a single connection."""
    connection_id: str
    source_addr: Tuple[str, int]
    target_addr: Tuple[str, int]
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    bytes_sent: int = 0      # client -> server
    bytes_received: int = 0  # server -> client
    last_activity: float = field(default_factory=time.time)
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def get_duration(self) -> float:
        """Calculate connection duration in seconds."""
        end = self.end_time or time.time()
        return end - self.start_time
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def get_throughput(self) -> float:
        """Calculate average throughput in bytes/second.
        
        TODO: Implement this method
        """
        # YOUR CODE HERE
        return 0.0
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def update_activity(self) -> None:
        """Update last activity timestamp."""
        self.last_activity = time.time()
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def is_idle(self, timeout: float) -> bool:
        """Check if connection has been idle too long.
        
        TODO: Implement this method
        """
        # YOUR CODE HERE
        return False
    

# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
    def to_log_string(self) -> str:
        """Format connection stats for logging.
        
        TODO: Implement this method
        """
        # YOUR CODE HERE
        return ""


@dataclass


# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class TunnelStats:
    """Aggregate statistics for the tunnel."""
    start_time: float = field(default_factory=time.time)
    total_connections: int = 0
    active_connections: int = 0
    peak_connections: int = 0
    total_bytes_sent: int = 0
    total_bytes_received: int = 0
    connections: Dict[str, ConnectionStats] = field(default_factory=dict)
    

# ═══════════════════════════════════════════════════════════════════════════════
# NETWORK_OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════════
    def add_connection(self, conn_stats: ConnectionStats) -> None:
        """Register a new connection.
        
        TODO: Implement this method
        - Add to connections dict
        - Update counters
        - Update peak if needed
        """
        # YOUR CODE HERE
        pass
    

# ═══════════════════════════════════════════════════════════════════════════════
# NETWORK_OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════════
    def remove_connection(self, connection_id: str) -> None:
        """Remove a connection and update totals.
        
        TODO: Implement this method
        - Get final stats
        - Update total bytes
        - Remove from active
        - Update active count
        """
        # YOUR CODE HERE
        pass
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def get_uptime(self) -> timedelta:
        """Calculate tunnel uptime."""
        return timedelta(seconds=time.time() - self.start_time)
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def get_average_duration(self) -> float:
        """Calculate average connection duration.
        
        TODO: Implement this method
        """
        # YOUR CODE HERE
        return 0.0
    

# ═══════════════════════════════════════════════════════════════════════════════
# OUTPUT_FORMATTING
# ═══════════════════════════════════════════════════════════════════════════════
    def format_summary(self) -> str:
        """Format complete statistics summary.
        
        TODO: Implement this method
        See homework README for expected format
        """
        # YOUR CODE HERE
        return "Statistics summary not implemented"



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class TunnelLogger:
    """Custom logger with connection context."""
    

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
    def __init__(self, name: str, log_file: Optional[str] = None,
                 level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Console handler
        console = logging.StreamHandler()
        console.setLevel(level)
        console.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)-5s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        self.logger.addHandler(console)
        
        # File handler (if specified)
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)-5s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            ))
            self.logger.addHandler(file_handler)
    

# ═══════════════════════════════════════════════════════════════════════════════
# NETWORK_OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════════
    def connection(self, conn_id: str, message: str, level: int = logging.INFO):
        """Log with connection context."""
        self.logger.log(level, f"[{conn_id}] {message}")
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def info(self, message: str):
        self.logger.info(message)
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def debug(self, message: str):
        self.logger.debug(message)
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def warning(self, message: str):
        self.logger.warning(message)
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def error(self, message: str):
        self.logger.error(message)



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class TCPTunnelWithMetrics:
    """Enhanced TCP Tunnel with thorough logging and metrics."""
    

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
    def __init__(self, listen_port: int, target_host: str, target_port: int,
                 max_connections: int = DEFAULT_MAX_CONNECTIONS,
                 timeout: int = DEFAULT_TIMEOUT,
                 log_file: Optional[str] = None,
                 debug: bool = False):
        self.listen_port = listen_port
        self.target_host = target_host
        self.target_port = target_port
        self.max_connections = max_connections
        self.timeout = timeout
        
        self.running = False
        self.connection_counter = 0
        self.lock = threading.Lock()
        
        self.stats = TunnelStats()
        self.logger = TunnelLogger(
            'tunnel',
            log_file=log_file,
            level=logging.DEBUG if debug else logging.INFO
        )
        
        self.server_socket: Optional[socket.socket] = None
        
        # Signal handlers
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)
        # SIGUSR1 for status display (Unix only)
        if hasattr(signal, 'SIGUSR1'):
            signal.signal(signal.SIGUSR1, self._handle_status)
    

# ═══════════════════════════════════════════════════════════════════════════════
# CLEANUP_RESOURCES
# ═══════════════════════════════════════════════════════════════════════════════
    def _handle_shutdown(self, signum, frame):
        """Handle graceful shutdown."""
        self.logger.info("Shutdown signal received")
        self.running = False
        if self.server_socket:
            self.server_socket.close()
    

# ═══════════════════════════════════════════════════════════════════════════════
# DATA_PROCESSING
# ═══════════════════════════════════════════════════════════════════════════════
    def _handle_status(self, signum, frame):
        """Handle status display request (SIGUSR1)."""
        print("\n" + self.stats.format_summary())
    

# ═══════════════════════════════════════════════════════════════════════════════
# NETWORK_OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════════
    def _generate_connection_id(self) -> str:
        """Generate unique connection ID.
        
        TODO: Implement this method
        Format: conn-XXX where XXX is zero-padded counter
        """
        # YOUR CODE HERE
        return "conn-000"
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def _relay_data(self, source: socket.socket, destination: socket.socket,
                    conn_stats: ConnectionStats, direction: str) -> None:
        """Relay data between sockets with statistics.
        
        TODO: Implement this method
        - Read from source
        - Write to destination
        - Update bytes_sent or bytes_received in conn_stats
        - Update last_activity
        - Log data transfer at DEBUG level
        - Handle errors gracefully
        
        Args:
            source: Socket to read from
            destination: Socket to write to
            conn_stats: Connection statistics object
            direction: Either 'client->server' or 'server->client'
        """
        # YOUR CODE HERE
        pass
    

# ═══════════════════════════════════════════════════════════════════════════════
# NETWORK_OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════════
    def _handle_connection(self, client_socket: socket.socket,
                          client_address: Tuple[str, int]) -> None:
        """Handle a single client connection.
        
        TODO: Implement this method
        - Check max connections limit
        - Generate connection ID
        - Create ConnectionStats
        - Connect to target server
        - Log connection events
        - Start relay threads
        - Wait for completion
        - Update statistics
        - Clean up
        """
        # YOUR CODE HERE
        pass
    

# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
    def _check_idle_connections(self) -> None:
        """Check for and close idle connections.
        
        TODO: Implement this method
        - Iterate through active connections
        - Close those exceeding timeout
        - Log warnings for closed connections
        """
        # YOUR CODE HERE
        pass
    

# ═══════════════════════════════════════════════════════════════════════════════
# NETWORK_OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════════
    def _create_server_socket(self) -> socket.socket:
        """Create and configure the listening socket.
        
        TODO: Implement this method
        - Create TCP socket
        - Set SO_REUSEADDR
        - Bind to listen_port
        - Start listening
        """
        # YOUR CODE HERE
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return sock
    

# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
    def run(self) -> None:
        """Main tunnel loop.
        
        TODO: Implement this method
        - Create server socket
        - Log startup info
        - Accept connections in loop
        - Handle each in separate thread
        - Periodically check idle connections
        """
        self.logger.info("=" * 60)
        self.logger.info("TCP Tunnel with Metrics")
        self.logger.info(f"Listening on port {self.listen_port}")
        self.logger.info(f"Forwarding to {self.target_host}:{self.target_port}")
        self.logger.info(f"Max connections: {self.max_connections}")
        self.logger.info(f"Idle timeout: {self.timeout}s")
        self.logger.info("=" * 60)
        
        # YOUR CODE HERE
        
        # Print final statistics
        self.logger.info("Tunnel stopped")
        print(self.stats.format_summary())



# ═══════════════════════════════════════════════════════════════════════════════
# PARSE_ARGUMENTS
# ═══════════════════════════════════════════════════════════════════════════════
def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="TCP Tunnel with Logging and Metrics"
    )
    parser.add_argument(
        '--listen-port', '-l',
        type=int,
        required=True,
        help="Port to listen on for incoming connections"
    )
    parser.add_argument(
        '--target-host', '-H',
        type=str,
        required=True,
        help="Target host to forward connections to"
    )
    parser.add_argument(
        '--target-port', '-P',
        type=int,
        required=True,
        help="Target port to forward connections to"
    )
    parser.add_argument(
        '--max-connections', '-m',
        type=int,
        default=DEFAULT_MAX_CONNECTIONS,
        help=f"Maximum concurrent connections (default: {DEFAULT_MAX_CONNECTIONS})"
    )
    parser.add_argument(
        '--timeout', '-t',
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"Idle connection timeout in seconds (default: {DEFAULT_TIMEOUT})"
    )
    parser.add_argument(
        '--log-file', '-f',
        type=str,
        default=None,
        help="Log file path (optional, logs to console only if not specified)"
    )
    parser.add_argument(
        '--debug', '-d',
        action='store_true',
        help="Enable debug logging"
    )
    return parser.parse_args()



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    """Main entry point."""
    args = parse_arguments()
    
    tunnel = TCPTunnelWithMetrics(
        listen_port=args.listen_port,
        target_host=args.target_host,
        target_port=args.target_port,
        max_connections=args.max_connections,
        timeout=args.timeout,
        log_file=args.log_file,
        debug=args.debug
    )
    
    try:
        tunnel.run()
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
