#!/usr/bin/env python3
"""
Backend HTTP Server for Load Balancing Demonstration

This server identifies itself in responses, allowing observation
of load balancing behaviour when accessed through a reverse proxy.

Author: ing. dr. Antonio Clim
Course: Computer Networks - ASE, CSIE
"""

import socket
import argparse
import os
from datetime import datetime
from typing import Optional

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

DEFAULT_PORT = 8080
BUFFER_SIZE = 4096

# Server identification (can be set via environment or command line)
BACKEND_ID = os.environ.get("BACKEND_ID", "Unknown")


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1: REQUEST PARSING
# ═══════════════════════════════════════════════════════════════════════════════

def parse_request(raw_data: bytes) -> Optional[dict]:
    """
    Parse HTTP request into structured format.
    
    Args:
        raw_data: Raw bytes from socket
        
    Returns:
        Dictionary with method, path, version, headers
        None if parsing fails
    """
    try:
        text = raw_data.decode('iso-8859-1')
        lines = text.split('\r\n')
        
        # Parse request line
        parts = lines[0].split(' ')
        if len(parts) < 3:
            return None
            
        method, path, version = parts[0], parts[1], parts[2]
        
        # Parse headers
        headers = {}
        for line in lines[1:]:
            if line == '':
                break
            if ': ' in line:
                key, value = line.split(': ', 1)
                headers[key.lower()] = value
        
        return {
            'method': method,
            'path': path,
            'version': version,
            'headers': headers
        }
        
    except Exception:
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2: RESPONSE GENERATION
# ═══════════════════════════════════════════════════════════════════════════════

def build_response(status_code: int, headers: dict, body: bytes = b"") -> bytes:
    """
    Build complete HTTP response.
    
    Args:
        status_code: HTTP status code
        headers: Response headers
        body: Response body
        
    Returns:
        Complete HTTP response as bytes
    """
    status_messages = {
        200: "OK",
        404: "Not Found",
        405: "Method Not Allowed",
    }
    
    status_line = f"HTTP/1.1 {status_code} {status_messages.get(status_code, 'Unknown')}\r\n"
    header_lines = "".join(f"{k}: {v}\r\n" for k, v in headers.items())
    
    response_text = status_line + header_lines + "\r\n"
    return response_text.encode('utf-8') + body


def generate_index_page(backend_id: str, request: dict) -> bytes:
    """
    Generate HTML index page showing backend identification.
    
    Args:
        backend_id: Identifier for this backend server
        request: Parsed request dictionary
        
    Returns:
        HTML content as bytes
    """
    xff = request['headers'].get('x-forwarded-for', 'Direct connection')
    real_ip = request['headers'].get('x-real-ip', 'Not provided')
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Backend {backend_id}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .backend-id {{ font-size: 48px; colour: #2196F3; }}
        .info {{ background: #f5f5f5; padding: 20px; margin: 20px 0; }}
        table {{ border-collapse: collapse; }}
        td, th {{ padding: 8px 16px; border: 1px solid #ddd; }}
    </style>
</head>
<body>
    <h1>Response from <span class="backend-id">Backend {backend_id}</span></h1>
    
    <div class="info">
        <h2>Request Details</h2>
        <table>
            <tr><th>Method</th><td>{request['method']}</td></tr>
            <tr><th>Path</th><td>{request['path']}</td></tr>
            <tr><th>X-Forwarded-For</th><td>{xff}</td></tr>
            <tr><th>X-Real-IP</th><td>{real_ip}</td></tr>
            <tr><th>Timestamp</th><td>{datetime.now().isoformat()}</td></tr>
        </table>
    </div>
    
    <p>This response demonstrates round-robin load balancing.</p>
    <p>Refresh the page to see requests distributed across backends.</p>
</body>
</html>
"""
    return html.encode('utf-8')


def generate_health_response() -> bytes:
    """Generate simple health check response."""
    return b"OK"


def generate_status_json(backend_id: str) -> bytes:
    """Generate JSON status response."""
    import json
    status = {
        "backend_id": backend_id,
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }
    return json.dumps(status, indent=2).encode('utf-8')


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3: REQUEST HANDLING
# ═══════════════════════════════════════════════════════════════════════════════

def handle_request(raw_data: bytes, backend_id: str) -> bytes:
    """
    Process HTTP request and generate response.
    
    Routes:
        /          - Index page with backend identification
        /health    - Health check endpoint
        /api/status - JSON status endpoint
        
    Args:
        raw_data: Raw HTTP request bytes
        backend_id: This server's identifier
        
    Returns:
        Complete HTTP response
    """
    request = parse_request(raw_data)
    
    if request is None:
        return build_response(400, {"Content-Type": "text/plain"}, b"Bad Request")
    
    method = request['method']
    path = request['path']
    
    # Only allow GET and HEAD
    if method not in ('GET', 'HEAD'):
        return build_response(
            405,
            {"Content-Type": "text/plain", "Allow": "GET, HEAD"},
            b"Method Not Allowed"
        )
    
    # Route to appropriate handler
    if path == '/' or path == '/index.html':
        body = generate_index_page(backend_id, request)
        content_type = "text/html; charset=utf-8"
        
    elif path == '/health':
        body = generate_health_response()
        content_type = "text/plain"
        
    elif path == '/api/status' or path == '/api/status.json':
        body = generate_status_json(backend_id)
        content_type = "application/json"
        
    else:
        body = b"Not Found"
        headers = {
            "Content-Type": "text/plain",
            "Content-Length": str(len(body)),
            "X-Backend-ID": backend_id,
        }
        return build_response(404, headers, body if method == 'GET' else b"")
    
    # Build success response
    headers = {
        "Content-Type": content_type,
        "Content-Length": str(len(body)),
        "X-Backend-ID": backend_id,
        "Server": f"PythonBackend/{backend_id}",
        "Date": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
    }
    
    # HEAD requests get headers but no body
    response_body = body if method == 'GET' else b""
    
    return build_response(200, headers, response_body)


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4: SERVER MAIN LOOP
# ═══════════════════════════════════════════════════════════════════════════════

def run_server(host: str, port: int, backend_id: str) -> None:
    """
    Run the backend HTTP server.
    
    Args:
        host: Address to bind to
        port: Port to listen on
        backend_id: Identifier for this backend
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    
    print(f"Backend {backend_id} running on http://{host}:{port}")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            client, addr = server.accept()
            
            try:
                data = client.recv(BUFFER_SIZE)
                if data:
                    # Log request
                    request_line = data.split(b'\r\n')[0].decode('utf-8', errors='ignore')
                    print(f"[{datetime.now().isoformat()}] {addr[0]} -> {request_line}")
                    
                    response = handle_request(data, backend_id)
                    client.sendall(response)
                    
            except Exception as e:
                print(f"Error: {e}")
            finally:
                client.close()
                
    except KeyboardInterrupt:
        print(f"\nBackend {backend_id} shutting down...")
    finally:
        server.close()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Parse arguments and start server."""
    parser = argparse.ArgumentParser(description="Backend HTTP Server")
    parser.add_argument("--host", default="0.0.0.0", help="Bind address")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port")
    parser.add_argument("--id", default=BACKEND_ID, help="Backend identifier")
    
    args = parser.parse_args()
    
    run_server(args.host, args.port, args.id)


if __name__ == "__main__":
    main()
