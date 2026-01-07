#!/usr/bin/env python3
"""
Week 8 Laboratory Demonstrations
NETWORKING class - ASE, Informatics | by Revolvix

Automated demonstrations for classroom presentation.
"""

import subprocess
import sys
import time
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.logger import setup_logger, print_banner, print_section
from scripts.utils.network_utils import http_get, check_port_open

logger = setup_logger("run_demo")

DEMOS = {
    "docker-nginx": "Docker infrastructure with nginx load balancer",
    "http-server": "HTTP server request/response cycle",
    "handshake": "TCP three-way handshake capture",
    "load-balance": "Load balancing algorithms comparison",
    "headers": "HTTP headers analysis",
}


def demo_docker_nginx():
    """Demonstrate Docker infrastructure with nginx."""
    print_section("Demo: Docker Infrastructure with nginx Load Balancer")
    
    print("\nThis demo shows nginx distributing requests across backend servers.\n")
    
    if not check_port_open("localhost", 8080):
        logger.error("nginx is not running. Start with: python scripts/start_lab.py")
        return False
    
    print("Sending 12 requests through nginx load balancer...\n")
    print("-" * 60)
    
    backend_counts = {}
    
    for i in range(12):
        status, headers, body = http_get("http://localhost:8080/")
        
        if status == 200:
            # Extract backend info from headers
            backend = headers.get("x-backend-id", "unknown")
            backend_name = headers.get("x-backend-name", "Unknown")
            
            backend_counts[backend] = backend_counts.get(backend, 0) + 1
            
            print(f"  Request {i+1:2d}: Backend {backend} ({backend_name})")
        else:
            print(f"  Request {i+1:2d}: Error (status {status})")
        
        time.sleep(0.1)
    
    print("-" * 60)
    print("\nDistribution Summary:")
    for backend, count in sorted(backend_counts.items()):
        bar = "█" * count
        print(f"  Backend {backend}: {bar} ({count} requests)")
    
    print("\nObservations:")
    print("  - Requests are distributed in round-robin order")
    print("  - Each backend receives approximately equal load")
    print("  - X-Backend-ID header identifies the responding server")
    
    return True


def demo_http_server():
    """Demonstrate HTTP server internals."""
    print_section("Demo: HTTP Server Request/Response Cycle")
    
    if not check_port_open("localhost", 8080):
        logger.error("Server not running. Start with: python scripts/start_lab.py")
        return False
    
    print("\nExamining HTTP request/response structure...\n")
    
    # Request 1: GET /
    print("1. GET / (index.html)")
    print("-" * 40)
    
    status, headers, body = http_get("http://localhost:8080/")
    print(f"   Status: {status}")
    print("   Response Headers:")
    for key in ["content-type", "content-length", "server", "x-backend-id"]:
        if key in headers:
            print(f"     {key}: {headers[key]}")
    print(f"   Body: {len(body)} bytes")
    
    # Request 2: GET /hello.txt
    print("\n2. GET /hello.txt")
    print("-" * 40)
    
    status, headers, body = http_get("http://localhost:8080/hello.txt")
    print(f"   Status: {status}")
    print(f"   Content-Type: {headers.get('content-type', 'N/A')}")
    print(f"   Body: {body.decode('utf-8', errors='replace')[:100]}")
    
    # Request 3: GET /not-found
    print("\n3. GET /not-found")
    print("-" * 40)
    
    status, headers, body = http_get("http://localhost:8080/not-found")
    print(f"   Status: {status} (Not Found)")
    
    # Request 4: Different content types
    print("\n4. GET /api/status.json")
    print("-" * 40)
    
    status, headers, body = http_get("http://localhost:8080/api/status.json")
    print(f"   Status: {status}")
    print(f"   Content-Type: {headers.get('content-type', 'N/A')}")
    print(f"   Body: {body.decode('utf-8', errors='replace')}")
    
    print("\nObservations:")
    print("  - Server correctly identifies MIME types by extension")
    print("  - 404 returned for non-existent resources")
    print("  - JSON content served with application/json type")
    
    return True


def demo_handshake():
    """Demonstrate TCP handshake (with capture instruction)."""
    print_section("Demo: TCP Three-Way Handshake")
    
    print("""
This demo shows how to capture and analyse the TCP three-way handshake.

To capture the handshake:

1. Start Wireshark and select the appropriate interface
   (usually 'Loopback' or 'lo' for localhost traffic)

2. Apply filter: tcp.flags.syn == 1

3. Run this command in PowerShell:
   curl http://localhost:8080/

4. In Wireshark, observe:
   - Packet 1: SYN (client → server)
   - Packet 2: SYN-ACK (server → client)  
   - Packet 3: ACK (client → server)

The handshake establishes:
  - Initial Sequence Numbers (ISN) for both directions
  - Window size for flow control
  - TCP options (MSS, SACK, timestamps)
""")
    
    print("Generating a single HTTP request for capture...")
    status, _, _ = http_get("http://localhost:8080/hello.txt")
    print(f"Request complete (status: {status})")
    
    print("\nSuggested Wireshark Filters:")
    print("  tcp.flags.syn == 1            # SYN packets only")
    print("  tcp.flags.syn == 1 && tcp.flags.ack == 0  # Initial SYN only")
    print("  tcp.stream eq 0               # Follow first TCP stream")
    
    return True


def demo_load_balance():
    """Compare load balancing algorithms."""
    print_section("Demo: Load Balancing Algorithms Comparison")
    
    if not check_port_open("localhost", 8080):
        logger.error("nginx not running. Start with: python scripts/start_lab.py")
        return False
    
    algorithms = {
        "Round-Robin": "http://localhost:8080/",
        "Weighted": "http://localhost:8080/weighted/",
        "Least Conn": "http://localhost:8080/least-conn/",
        "IP Hash": "http://localhost:8080/sticky/",
    }
    
    print("\nComparing different load balancing algorithms...\n")
    
    for algo_name, url in algorithms.items():
        print(f"{algo_name}:")
        print("-" * 40)
        
        backends = []
        for i in range(6):
            status, headers, _ = http_get(url)
            if status == 200:
                backend = headers.get("x-backend-id", "?")
                backends.append(backend)
        
        print(f"  Sequence: {' → '.join(backends)}")
        
        # Analyse pattern
        if algo_name == "Round-Robin":
            print("  Pattern: Cycles through backends equally")
        elif algo_name == "Weighted":
            print("  Pattern: Proportional distribution (5:3:1)")
        elif algo_name == "Least Conn":
            print("  Pattern: Routes to least loaded backend")
        elif algo_name == "IP Hash":
            unique = set(backends)
            if len(unique) == 1:
                print(f"  Pattern: All requests to same backend (sticky)")
            else:
                print("  Pattern: Consistent per-client routing")
        print()
    
    return True


def demo_headers():
    """Analyse HTTP headers in detail."""
    print_section("Demo: HTTP Headers Analysis")
    
    if not check_port_open("localhost", 8080):
        logger.error("Server not running")
        return False
    
    print("\nExamining HTTP headers in detail...\n")
    
    # Use curl for verbose output
    print("curl -v http://localhost:8080/ 2>&1 | grep -E '^[<>]'")
    print("-" * 60)
    
    result = subprocess.run(
        ["curl", "-v", "-s", "http://localhost:8080/"],
        capture_output=True,
        text=True
    )
    
    # Parse and display headers
    for line in result.stderr.split("\n"):
        if line.startswith(">"):
            print(f"  \033[92mRequest:\033[0m {line[2:]}")
        elif line.startswith("<"):
            print(f"  \033[94mResponse:\033[0m {line[2:]}")
    
    print("\nKey Headers Explained:")
    print("  Host:           Target server (required in HTTP/1.1)")
    print("  User-Agent:     Client identification")
    print("  Accept:         Preferred content types")
    print("  X-Forwarded-For: Original client IP (added by proxy)")
    print("  X-Backend-ID:   Backend server identifier")
    print("  Connection:     Connection management (keep-alive/close)")
    
    return True


def list_demos():
    """List available demonstrations."""
    print("\nAvailable Demonstrations:")
    print("-" * 60)
    for name, description in DEMOS.items():
        print(f"  {name:15s} {description}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Run Week 8 Laboratory Demonstrations"
    )
    parser.add_argument(
        "--demo", "-d",
        choices=list(DEMOS.keys()),
        help="Specific demo to run"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List available demonstrations"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Run all demonstrations"
    )
    
    args = parser.parse_args()
    
    print_banner(
        "Week 8 Laboratory Demonstrations",
        "Transport Layer: HTTP Server and Reverse Proxies"
    )
    
    if args.list:
        list_demos()
        return 0
    
    demo_functions = {
        "docker-nginx": demo_docker_nginx,
        "http-server": demo_http_server,
        "handshake": demo_handshake,
        "load-balance": demo_load_balance,
        "headers": demo_headers,
    }
    
    if args.all:
        for name, func in demo_functions.items():
            print(f"\n{'='*60}")
            print(f"Running: {name}")
            print("=" * 60)
            func()
            time.sleep(1)
        return 0
    
    if args.demo:
        func = demo_functions.get(args.demo)
        if func:
            return 0 if func() else 1
        else:
            logger.error(f"Unknown demo: {args.demo}")
            return 1
    
    # Default: show menu
    list_demos()
    print("Usage: python scripts/run_demo.py --demo <name>")
    return 0


if __name__ == "__main__":
    sys.exit(main())
