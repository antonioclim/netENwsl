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
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

    # Load certificate and private key
    context.load_cert_chain(certfile=str(CERT_FILE), keyfile=str(KEY_FILE))

    # Enforce a sensible minimum TLS version
    context.minimum_version = ssl.TLSVersion.TLSv1_2

    # Use default secure settings, keep compatibility with OpenSSL defaults
    context.options |= ssl.OP_NO_COMPRESSION
    return context


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
        request_data = client_socket.recv(8192)
        if not request_data:
            return

        try:
            request_text = request_data.decode("iso-8859-1", errors="replace")
        except Exception:
            request_text = ""

        request_line = request_text.split("\r\n", 1)[0]
        parts = request_line.split()
        if len(parts) < 3:
            client_socket.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")
            return

        method, path, _version = parts[0].upper(), parts[1], parts[2]
        if method not in {"GET", "HEAD"}:
            client_socket.sendall(b"HTTP/1.1 405 Method Not Allowed\r\nAllow: GET, HEAD\r\n\r\n")
            return

        # Map path
        if path == "/":
            path = "/index.html"
        safe_path = (path.split("?", 1)[0]).lstrip("/")
        full_path = (DOCUMENT_ROOT / safe_path).resolve()
        doc_root = DOCUMENT_ROOT.resolve()
        if not str(full_path).startswith(str(doc_root)):
            client_socket.sendall(b"HTTP/1.1 403 Forbidden\r\n\r\n")
            return

        if full_path.is_dir():
            full_path = full_path / "index.html"

        if not full_path.exists() or not full_path.is_file():
            body = b"Not Found"
            headers = (
                "HTTP/1.1 404 Not Found\r\n"
                f"X-Protocol: {protocol}\r\n"
                "Content-Type: text/plain; charset=utf-8\r\n"
                f"Content-Length: {len(body)}\r\n"
                "Connection: close\r\n\r\n"
            ).encode("iso-8859-1")
            client_socket.sendall(headers + (body if method == "GET" else b""))
            return

        content = full_path.read_bytes()
        mime = "text/html; charset=utf-8" if full_path.suffix.lower() in {".html", ".htm"} else "application/octet-stream"
        headers = (
            "HTTP/1.1 200 OK\r\n"
            f"X-Protocol: {protocol}\r\n"
            f"Content-Type: {mime}\r\n"
            f"Content-Length: {len(content)}\r\n"
            "Connection: close\r\n\r\n"
        ).encode("iso-8859-1")
        client_socket.sendall(headers + (content if method == "GET" else b""))
        
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
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, HTTP_PORT))
    server_socket.listen(50)

    try:
        while True:
            client_socket, address = server_socket.accept()
            thread = threading.Thread(
                target=handle_request,
                args=(client_socket, address, False),
                daemon=True,
            )
            thread.start()
    finally:
        server_socket.close()


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
    
    context = create_ssl_context()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, HTTPS_PORT))
    server_socket.listen(50)

    try:
        while True:
            client_socket, address = server_socket.accept()
            try:
                ssl_socket = context.wrap_socket(client_socket, server_side=True)
            except ssl.SSLError as e:
                print(f"[HTTPS] TLS handshake failed: {e}")
                client_socket.close()
                continue

            thread = threading.Thread(
                target=handle_request,
                args=(ssl_socket, address, True),
                daemon=True,
            )
            thread.start()
    finally:
        server_socket.close()


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
