#!/usr/bin/env python3
"""
Homework 2.1: Multi-Protocol Calculator Server
NETWORKING class - ASE, Informatics | by Revolvix

Implement a calculator server supporting both TCP and UDP clients.

Requirements:
- TCP server on port 9100
- UDP server on port 9101
- Operations: add, sub, mul, div, pow
- Concurrent TCP handling via threading
- Comprehensive error handling and logging

Example protocol:
    add:5:3  → 8
    mul:6:7  → 42
    div:15:3 → 5.0

Usage:
    python hw_2_01.py server          # Start the server
    python hw_2_01.py test            # Run self-tests
"""

from __future__ import annotations

import argparse
import logging
import socket
import sys
import threading
from datetime import datetime
from typing import Callable

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Configuration
TCP_PORT = 9100
UDP_PORT = 9101
BUFFER_SIZE = 1024


# =============================================================================
# TODO: Implement the calculator operations
# =============================================================================

OPERATIONS: dict[str, Callable[[float, float], float]] = {
    # TODO: Add operation functions
    # 'add': lambda a, b: a + b,
    # 'sub': ...,
    # 'mul': ...,
    # 'div': ...,
    # 'pow': ...,
}


def parse_request(data: str) -> tuple[str, float, float]:
    """
    Parse a calculator request string.
    
    Args:
        data: Request in format "operation:operand1:operand2"
    
    Returns:
        Tuple of (operation_name, operand1, operand2)
    
    Raises:
        ValueError: If format is invalid
    """
    # TODO: Implement parsing
    # Expected format: "add:5:3"
    # Return tuple: ("add", 5.0, 3.0)
    raise NotImplementedError("Implement parse_request()")


def calculate(operation: str, a: float, b: float) -> str:
    """
    Perform the calculation and return result string.
    
    Args:
        operation: Operation name (add, sub, mul, div, pow)
        a: First operand
        b: Second operand
    
    Returns:
        Result as string, or error message
    """
    # TODO: Implement calculation with error handling
    # - Check for unknown operations
    # - Handle division by zero
    # - Return formatted result
    raise NotImplementedError("Implement calculate()")


# =============================================================================
# TODO: Implement TCP server
# =============================================================================

def handle_tcp_client(conn: socket.socket, addr: tuple[str, int]) -> None:
    """
    Handle a single TCP client connection.
    
    Args:
        conn: Connected socket
        addr: Client address tuple (ip, port)
    """
    # TODO: Implement TCP client handler
    # - Receive data
    # - Parse and calculate
    # - Send response
    # - Log the interaction
    # - Handle errors gracefully
    raise NotImplementedError("Implement handle_tcp_client()")


def run_tcp_server() -> None:
    """
    Run the TCP server (blocking).
    
    Creates a listening socket and spawns threads for each client.
    """
    # TODO: Implement TCP server
    # - Create socket with SO_REUSEADDR
    # - Bind to TCP_PORT
    # - Listen for connections
    # - Accept and spawn thread for each client
    raise NotImplementedError("Implement run_tcp_server()")


# =============================================================================
# TODO: Implement UDP server
# =============================================================================

def run_udp_server() -> None:
    """
    Run the UDP server (blocking).
    
    Receives datagrams and responds to each.
    """
    # TODO: Implement UDP server
    # - Create UDP socket
    # - Bind to UDP_PORT
    # - Receive datagrams in loop
    # - Parse, calculate, respond
    # - Log interactions
    raise NotImplementedError("Implement run_udp_server()")


# =============================================================================
# TODO: Implement dual-protocol server
# =============================================================================

def run_server() -> None:
    """
    Run both TCP and UDP servers simultaneously.
    
    Hint: Use threading to run both servers concurrently.
    """
    # TODO: Start both servers
    # Option 1: Two threads (one TCP, one UDP)
    # Option 2: Use select() for I/O multiplexing
    raise NotImplementedError("Implement run_server()")


# =============================================================================
# Self-tests
# =============================================================================

def run_tests() -> None:
    """Run basic self-tests."""
    print("Running self-tests...")
    
    # Test parsing
    try:
        op, a, b = parse_request("add:5:3")
        assert op == "add" and a == 5.0 and b == 3.0, "Parse test failed"
        print("✓ Parse test passed")
    except NotImplementedError:
        print("✗ parse_request() not implemented")
    except AssertionError as e:
        print(f"✗ {e}")
    
    # Test calculation
    try:
        result = calculate("add", 5, 3)
        assert result == "8" or result == "8.0", f"Expected 8, got {result}"
        print("✓ Add test passed")
        
        result = calculate("div", 10, 0)
        assert "ERROR" in result, "Division by zero should return error"
        print("✓ Division by zero test passed")
    except NotImplementedError:
        print("✗ calculate() not implemented")
    except AssertionError as e:
        print(f"✗ {e}")
    
    print("\nImplement the TODOs and run tests again!")


# =============================================================================
# Main entry point
# =============================================================================

def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Multi-Protocol Calculator Server"
    )
    parser.add_argument(
        "command",
        choices=["server", "test"],
        help="Command to run"
    )
    
    args = parser.parse_args()
    
    if args.command == "server":
        logger.info(f"Starting calculator server (TCP:{TCP_PORT}, UDP:{UDP_PORT})")
        try:
            run_server()
        except NotImplementedError as e:
            logger.error(f"Not implemented: {e}")
            return 1
        except KeyboardInterrupt:
            logger.info("Server stopped")
            return 0
    
    elif args.command == "test":
        run_tests()
        return 0
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
