#!/usr/bin/env python3
"""
Homework Assignment 1: HTTPS Server with TLS
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Extend the basic HTTP server to support HTTPS connections.

Learning Objectives:
- Understand TLS handshake process
- Apply socket wrapping with ssl module
- Configure certificate-based security

Pair Programming Notes (if working with a partner):
- Driver: Implement create_ssl_context() and certificate loading
- Navigator: Verify TLS version settings, check OpenSSL documentation
- Swap after: SSL context is working
- Second Driver: Implement dual-port server logic
- Second Navigator: Test with curl and openssl s_client

Certificate Generation (run once):
    openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes \\
        -subj "/C=RO/ST=Bucharest/L=Bucharest/O=ASE/CN=localhost"

Usage:
    python hw_8_01_https_server.py

Testing:
    curl http://localhost:8080/           # HTTP
    curl -k https://localhost:8443/       # HTTPS (self-signed)
"""

import socket
import ssl
import threading
from pathlib import Path
from typing import Optional

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

HTTP_PORT = 8080
HTTPS_PORT = 8443
HOST = "0.0.0.0"
DOCUMENT_ROOT = Path(__file__).parent.parent.parent / "www"
CERT_FILE = Path(__file__).parent / "cert.pem"
KEY_FILE = Path(__file__).parent / "key.pem"


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1: SSL CONTEXT CREATION
# ═══════════════════════════════════════════════════════════════════════════════

# 💭 PREDICTION: What TLS version should be the minimum for security?
#    What happens if the client only supports TLS 1.0?
#    Think about this before implementing...

def create_ssl_context() -> ssl.SSLContext:
    """
    Create and configure SSL context for TLS 1.2+
    
    Requirements:
    - Use TLS 1.2 minimum version
    - Load certificate and private key
    - Set appropriate ciphers
    
    Returns:
        Configured SSLContext
    
    Hints:
    - Use ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    - Call load_cert_chain() with cert and key files
    - Set minimum_version to ssl.TLSVersion.TLSv1_2
    """
    # YOUR CODE HERE
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    
    # TODO: Load certificate chain
    # context.load_cert_chain(certfile=..., keyfile=...)
    
    # TODO: Set minimum TLS version
    # context.minimum_version = ...
    
    raise NotImplementedError("Implement create_ssl_context()")


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2: REQUEST HANDLING
# ═══════════════════════════════════════════════════════════════════════════════

# 💭 PREDICTION: How will you know if a connection is HTTP or HTTPS?
#    Should the response differ based on protocol?
#    Think about this before implementing...

def handle_request(client_socket: socket.socket, address: tuple, is_https: bool) -> None:
    """
    Handle HTTP/HTTPS request.
    
    Args:
        client_socket: Connected client socket
        address: Client address tuple (ip, port)
        is_https: True if this is an HTTPS connection
    
    Requirements:
    - Read HTTP request from socket
    - Parse request line (method, path, version)
    - Serve file from DOCUMENT_ROOT or return 404
    - Add appropriate headers including protocol indicator
    """
    protocol = "HTTPS" if is_https else "HTTP"
    print(f"[{protocol}] Connection from {address[0]}:{address[1]}")
    
    try:
        # TODO: Receive request data
        # request_data = client_socket.recv(...)
        
        # TODO: Parse request line
        # method, path, version = ...
        
        # TODO: Build and send response
        # response = build_response(...)
        # client_socket.sendall(response)
        
        raise NotImplementedError("Implement handle_request()")
        
    except Exception as e:
        print(f"[{protocol}] Error: {e}")
    finally:
        client_socket.close()


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3: HTTP SERVER
# ═══════════════════════════════════════════════════════════════════════════════

# 💭 PREDICTION: Why do we need separate servers for HTTP and HTTPS?
#    Could we use the same port for both?
#    Think about this before implementing...

def start_http_server() -> None:
    """
    Start HTTP server on HTTP_PORT.
    
    Requirements:
    - Create TCP socket
    - Bind to HOST:HTTP_PORT
    - Accept connections in a loop
    - Spawn thread for each connection
    """
    print(f"[HTTP] Starting server on {HOST}:{HTTP_PORT}")
    
    # TODO: Create and configure socket
    # server_socket = socket.socket(...)
    # server_socket.setsockopt(...)
    # server_socket.bind(...)
    # server_socket.listen(...)
    
    # TODO: Accept loop
    # while True:
    #     client_socket, address = server_socket.accept()
    #     thread = threading.Thread(target=handle_request, args=(...))
    #     thread.start()
    
    raise NotImplementedError("Implement start_http_server()")


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4: HTTPS SERVER
# ═══════════════════════════════════════════════════════════════════════════════

# 💭 PREDICTION: At what point do you wrap the socket with SSL?
#    Before or after accept()? Why does it matter?
#    Think about this before implementing...

def start_https_server() -> None:
    """
    Start HTTPS server on HTTPS_PORT.
    
    Requirements:
    - Create TCP socket
    - Wrap with SSL context
    - Bind to HOST:HTTPS_PORT
    - Accept connections in a loop
    - Spawn thread for each connection
    
    Hints:
    - Create SSL context first
    - Wrap socket AFTER accept() for client connections
    - Handle ssl.SSLError for TLS handshake failures
    """
    print(f"[HTTPS] Starting server on {HOST}:{HTTPS_PORT}")
    
    # TODO: Check certificate files exist
    if not CERT_FILE.exists() or not KEY_FILE.exists():
        print("[HTTPS] Certificate files not found!")
        print("Generate with:")
        print('  openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes')
        return
    
    # TODO: Create SSL context
    # context = create_ssl_context()
    
    # TODO: Create and configure socket
    # server_socket = socket.socket(...)
    
    # TODO: Accept loop with SSL wrapping
    # while True:
    #     client_socket, address = server_socket.accept()
    #     try:
    #         ssl_socket = context.wrap_socket(client_socket, server_side=True)
    #         thread = threading.Thread(target=handle_request, args=(..., True))
    #         thread.start()
    #     except ssl.SSLError as e:
    #         print(f"[HTTPS] TLS handshake failed: {e}")
    
    raise NotImplementedError("Implement start_https_server()")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Main entry point - start both servers."""
    print("=" * 60)
    print("HTTPS Server - Week 8 Homework")
    print("NETWORKING class - ASE, Informatics")
    print("by ing. dr. Antonio Clim")
    print("=" * 60)
    print()
    
    # Start HTTP server in separate thread
    http_thread = threading.Thread(target=start_http_server, daemon=True)
    http_thread.start()
    
    # Start HTTPS server in main thread
    start_https_server()
    
    return 0


if __name__ == "__main__":
    exit(main())
