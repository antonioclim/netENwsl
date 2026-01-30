#!/usr/bin/env python3
"""
Exercise 8.01: Minimal HTTP Server Implementation

This exercise guides you through implementing a basic HTTP/1.1 server
capable of parsing requests, serving static files and handling errors.

Learning Objectives:
- Parse HTTP request format (request line + headers)
- Implement secure path resolution (prevent directory traversal)
- Build valid HTTP responses with proper headers
- Handle different HTTP methods (GET, HEAD)

Estimated Time: 45-60 minutes
Difficulty: Intermediate

Pair Programming Notes:
- Driver: Implement parse_request() and is_safe_path() functions
- Navigator: Review HTTP specification, check for edge cases
- Swap after: Completing Section 2 (path security validation)
- Second Driver: Implement serve_file() and build_response()
- Second Navigator: Test with curl commands, verify security

Author: ing. dr. Antonio Clim
Course: Computer Networks - ASE, CSIE
"""

import socket
import os
import argparse
import urllib.parse
from datetime import datetime
from typing import Optional

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

DEFAULT_PORT = 8081
DEFAULT_DOCROOT = "www"
BUFFER_SIZE = 4096

# MIME type mapping for common file extensions
MIME_TYPES: dict[str, str] = {
    ".html": "text/html; charset=utf-8",
    ".htm": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".txt": "text/plain; charset=utf-8",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".ico": "image/x-icon",
    ".svg": "image/svg+xml",
    ".pdf": "application/pdf",
}

# HTTP status messages
STATUS_MESSAGES: dict[int, str] = {
    200: "OK",
    400: "Bad Request",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    500: "Internal Server Error",
}


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1: HTTP REQUEST PARSING
# ═══════════════════════════════════════════════════════════════════════════════

# 💭 PREDICTION: What character sequence separates HTTP header lines?
#    What encoding should you use to decode HTTP headers?
#    Think about this before implementing...

def parse_request(raw_data: bytes) -> Optional[dict]:
    """
    Parse raw HTTP request bytes into a structured dictionary.
    
    HTTP/1.1 requests have this format:
        METHOD SP REQUEST-TARGET SP HTTP-VERSION CRLF
        Header-Name: Header-Value CRLF
        ...
        CRLF
        [Body]
    
    Args:
        raw_data: Raw bytes received from the socket
        
    Returns:
        Dictionary with keys: method, path, version, headers
        Returns None if parsing fails
        
    Example:
        >>> data = b'GET /index.html HTTP/1.1\\r\\nHost: localhost\\r\\n\\r\\n'
        >>> result = parse_request(data)
        >>> result['method']
        'GET'
        >>> result['path']
        '/index.html'
        >>> result['headers']['host']
        'localhost'
    """
    try:
        text = raw_data.decode("iso-8859-1", errors="replace")
        lines = text.split("\r\n")

        if not lines or not lines[0].strip():
            return None

        # Request line: METHOD SP PATH SP VERSION
        parts = lines[0].split(" ")
        if len(parts) < 3:
            return None

        method, path, version = parts[0].upper(), parts[1], parts[2]

        headers: dict[str, str] = {}
        for line in lines[1:]:
            if line == "":
                break
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            headers[key.strip().lower()] = value.strip()

        return {
            "method": method,
            "path": path,
            "version": version,
            "headers": headers,
        }
    except Exception:
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2: PATH SECURITY VALIDATION  
# ═══════════════════════════════════════════════════════════════════════════════

# 💭 PREDICTION: What happens if a client requests "/../../../etc/passwd"?
#    How can you prevent access to files outside the document root?
#    Think about this before implementing...

def is_safe_path(requested_path: str, docroot: str) -> bool:
    """
    Check if the requested path is safely within the document root.
    
    This prevents directory traversal attacks where attackers try to
    access files outside the web root using sequences like "/../".
    
    Args:
        requested_path: The path from the HTTP request (e.g., "/images/../../../etc/passwd")
        docroot: The document root directory (e.g., "/var/www/html")
        
    Returns:
        True if the resolved path is within docroot, False otherwise
        
    Example:
        >>> is_safe_path('/index.html', '/var/www')
        True
        >>> is_safe_path('/../etc/passwd', '/var/www')
        False
        >>> is_safe_path('/./images/../index.html', '/var/www')
        True
    
    Security Note:
        Always normalise paths BEFORE joining with docroot to prevent
        path traversal. The order of operations matters!
    """
    try:
        # Only consider the path part (ignore query string and fragments)
        parsed = urllib.parse.urlparse(requested_path)
        path = urllib.parse.unquote(parsed.path)

        # Convert to a relative path for joining
        path = path.lstrip("/")

        # Normalise to collapse './' and '../'
        normalised = os.path.normpath(path)

        # If the normalised path escapes upwards, it is unsafe
        if normalised.startswith("..") or os.path.isabs(normalised):
            return False

        docroot_abs = os.path.abspath(docroot)
        full_path = os.path.abspath(os.path.join(docroot_abs, normalised))

        return full_path == docroot_abs or full_path.startswith(docroot_abs + os.sep)
    except Exception:
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3: FILE SERVING
# ═══════════════════════════════════════════════════════════════════════════════

# 💭 PREDICTION: What Content-Type should you return for a .html file?
#    What about a .png file? Why does this matter?
#    Think about this before implementing...

def get_mime_type(filepath: str) -> str:
    """
    Determine the MIME type based on file extension.
    
    Args:
        filepath: Path to the file
        
    Returns:
        MIME type string (e.g., "text/html; charset=utf-8")
        
    Example:
        >>> get_mime_type('/var/www/index.html')
        'text/html; charset=utf-8'
        >>> get_mime_type('/var/www/style.css')
        'text/css; charset=utf-8'
    """
    _, ext = os.path.splitext(filepath)
    return MIME_TYPES.get(ext.lower(), "application/octet-stream")


def serve_file(filepath: str, docroot: str) -> tuple[int, bytes, str]:
    """
    Read and serve a file from the document root.
    
    Args:
        filepath: Requested file path (from HTTP request)
        docroot: Document root directory
        
    Returns:
        Tuple of (status_code, content_bytes, mime_type)
        
    Example:
        >>> status, content, mime = serve_file('/index.html', 'www')
        >>> status
        200
        >>> mime
        'text/html; charset=utf-8'
    """
    try:
        if not is_safe_path(filepath, docroot):
            body = b"Forbidden"
            return 403, body, "text/plain; charset=utf-8"

        parsed = urllib.parse.urlparse(filepath)
        path = urllib.parse.unquote(parsed.path)
        rel = path.lstrip("/")
        rel = os.path.normpath(rel) if rel else ""

        docroot_abs = os.path.abspath(docroot)
        full_path = os.path.join(docroot_abs, rel)

        # Default document
        if os.path.isdir(full_path):
            full_path = os.path.join(full_path, "index.html")

        if not os.path.exists(full_path) or not os.path.isfile(full_path):
            body = b"Not Found"
            return 404, body, "text/plain; charset=utf-8"

        with open(full_path, "rb") as f:
            content = f.read()

        mime = get_mime_type(full_path)
        return 200, content, mime
    except PermissionError:
        body = b"Forbidden"
        return 403, body, "text/plain; charset=utf-8"
    except Exception:
        body = b"Internal Server Error"
        return 500, body, "text/plain; charset=utf-8"


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4: HTTP RESPONSE BUILDING
# ═══════════════════════════════════════════════════════════════════════════════

# 💭 PREDICTION: What must appear between the headers and body in HTTP?
#    What happens if you forget this separator?
#    Think about this before implementing...

def build_response(
    status_code: int,
    headers: dict[str, str],
    body: bytes = b""
) -> bytes:
    """
    Build a complete HTTP response.
    
    HTTP/1.1 responses have this format:
        HTTP-VERSION SP STATUS-CODE SP REASON-PHRASE CRLF
        Header-Name: Header-Value CRLF
        ...
        CRLF
        [Body]
    
    Args:
        status_code: HTTP status code (e.g., 200, 404)
        headers: Dictionary of response headers
        body: Response body as bytes
        
    Returns:
        Complete HTTP response as bytes
        
    Example:
        >>> resp = build_response(200, {'Content-Type': 'text/plain'}, b'Hello')
        >>> resp.startswith(b'HTTP/1.1 200 OK')
        True
    """
    reason = STATUS_MESSAGES.get(status_code, "Unknown")
    status_line = f"HTTP/1.1 {status_code} {reason}\r\n"

    header_lines = "".join(f"{k}: {v}\r\n" for k, v in headers.items())

    head = (status_line + header_lines + "\r\n").encode("iso-8859-1")
    return head + body


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5: REQUEST HANDLING
# ═══════════════════════════════════════════════════════════════════════════════

# 💭 PREDICTION: How should HEAD requests differ from GET requests?
#    Should HEAD return Content-Length? Should it return a body?
#    Think about this before implementing...

def handle_request(raw_data: bytes, docroot: str) -> bytes:
    """
    Process an HTTP request and generate appropriate response.
    
    Supported methods:
    - GET: Return headers and body
    - HEAD: Return headers only (no body)
    
    Args:
        raw_data: Raw HTTP request bytes
        docroot: Document root directory
        
    Returns:
        Complete HTTP response as bytes
        
    Example:
        >>> req = b'GET /index.html HTTP/1.1\\r\\nHost: localhost\\r\\n\\r\\n'
        >>> resp = handle_request(req, 'www')
        >>> b'200 OK' in resp
        True
    """
    request = parse_request(raw_data)

    if request is None:
        body = b"Bad Request"
        headers = {
            "Content-Type": "text/plain; charset=utf-8",
            "Content-Length": str(len(body)),
            "Connection": "close",
        }
        return build_response(400, headers, body)

    method = request.get("method", "")
    path = request.get("path", "/")

    if method not in {"GET", "HEAD"}:
        body = b"Method Not Allowed"
        headers = {
            "Content-Type": "text/plain; charset=utf-8",
            "Content-Length": str(len(body)),
            "Allow": "GET, HEAD",
            "Connection": "close",
        }
        return build_response(405, headers, body if method == "GET" else b"")

    status_code, content, mime = serve_file(path, docroot)

    date_hdr = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    headers = {
        "Date": date_hdr,
        "Server": "Week8HTTP/1.0",
        "Content-Type": mime,
        "Content-Length": str(len(content)),
        "Connection": "close",
    }

    response_body = content if method == "GET" else b""
    return build_response(status_code, headers, response_body)


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 6: SERVER MAIN LOOP
# ═══════════════════════════════════════════════════════════════════════════════

def run_server(host: str, port: int, docroot: str) -> None:
    """
    Run the HTTP server main loop.
    
    This function:
    1. Creates a TCP socket
    2. Binds to the specified address
    3. Listens for connections
    4. Accepts clients and handles requests
    
    Args:
        host: Host address to bind to
        port: Port number to listen on
        docroot: Document root directory
    """
    # Create TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow address reuse (avoid "Address already in use" errors)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind and listen
    server_socket.bind((host, port))
    server_socket.listen(5)
    
    print(f"HTTP Server running on http://{host}:{port}")
    print(f"Document root: {os.path.abspath(docroot)}")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            # Accept client connection
            client_socket, client_addr = server_socket.accept()
            print(f"\n[{datetime.now().isoformat()}] Connection from {client_addr}")
            
            try:
                # Receive request
                raw_data = client_socket.recv(BUFFER_SIZE)
                
                if raw_data:
                    # Handle request and send response
                    response = handle_request(raw_data, docroot)
                    client_socket.sendall(response)
                    
            except Exception as e:
                print(f"Error handling request: {e}")
                # Send 500 Internal Server Error
                error_response = build_response(
                    500,
                    {"Content-Type": "text/plain"},
                    b"Internal Server Error"
                )
                client_socket.sendall(error_response)
                
            finally:
                client_socket.close()
                
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        server_socket.close()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Parse arguments and start the server."""
    parser = argparse.ArgumentParser(
        description="Minimal HTTP/1.1 Server - Week 8 Exercise"
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
        "--docroot",
        default=DEFAULT_DOCROOT,
        help=f"Document root directory (default: {DEFAULT_DOCROOT})"
    )
    
    args = parser.parse_args()
    
    # Verify document root exists
    if not os.path.isdir(args.docroot):
        print(f"Error: Document root '{args.docroot}' does not exist")
        return 1
    
    run_server(args.host, args.port, args.docroot)
    return 0


if __name__ == "__main__":
    exit(main())
