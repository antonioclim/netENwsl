#!/usr/bin/env python3
"""
Backend HTTP Server for Docker Containers
NETWORKING class - ASE, Informatics | by Revolvix

Simple HTTP server that identifies itself via headers.
Used as backend servers for nginx reverse proxy demonstrations.
"""

import socket
import os
import sys
import argparse
import threading
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple, Optional

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from utils.net_utils import (
        parse_http_request,
        build_response,
        safe_map_target_to_path,
        guess_content_type,
        HTTP_STATUS_CODES,
    )
except ImportError:
    # Inline minimal implementations if imports fail
    def parse_http_request(raw):
        lines = raw.decode("iso-8859-1").split("\r\n")
        request_line = lines[0].split(" ")
        method = request_line[0] if request_line else "GET"
        target = request_line[1] if len(request_line) > 1 else "/"
        headers = {}
        for line in lines[1:]:
            if ":" in line:
                k, v = line.split(":", 1)
                headers[k.strip().lower()] = v.strip()
        return type("Req", (), {"method": method, "target": target, "headers": headers})()
    
    def build_response(status, body=b"", content_type="text/plain", extra_headers=None):
        reason = {200: "OK", 404: "Not Found", 500: "Error"}.get(status, "Unknown")
        headers = [
            f"HTTP/1.1 {status} {reason}",
            f"Content-Type: {content_type}",
            f"Content-Length: {len(body)}",
        ]
        if extra_headers:
            for k, v in extra_headers.items():
                headers.append(f"{k}: {v}")
        return ("\r\n".join(headers) + "\r\n\r\n").encode() + body


class BackendServer:
    """Simple HTTP backend server with identification headers."""
    
    def __init__(
        self,
        host: str = "0.0.0.0",
        port: int = 8080,
        www_root: str = "/var/www",
        backend_id: str = "0",
        backend_name: str = "Backend"
    ):
        self.host = host
        self.port = port
        self.www_root = Path(www_root).resolve()
        self.backend_id = backend_id
        self.backend_name = backend_name
        self.request_count = 0
        self.running = False
        
        # Ensure www_root exists
        self.www_root.mkdir(parents=True, exist_ok=True)
    
    def log(self, message: str):
        """Log with timestamp and backend ID."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [Backend-{self.backend_id}] {message}")
    
    def handle_request(self, client_socket: socket.socket, client_addr: Tuple[str, int]):
        """Handle a single HTTP request."""
        try:
            # Receive request
            raw_request = client_socket.recv(8192)
            if not raw_request:
                return
            
            self.request_count += 1
            
            # Parse request
            req = parse_http_request(raw_request)
            self.log(f"{req.method} {req.target} from {client_addr[0]}")
            
            # Add backend identification headers
            extra_headers = {
                "X-Backend-ID": self.backend_id,
                "X-Backend-Name": self.backend_name,
                "X-Request-Count": str(self.request_count),
                "X-Served-By": f"Backend-{self.backend_id}",
                "Server": f"ASE-Backend-{self.backend_id}/1.0",
            }
            
            # Handle special endpoints
            if req.target == "/health":
                response = build_response(
                    200,
                    b"OK",
                    "text/plain",
                    extra_headers
                )
            elif req.target == "/api/info":
                info = {
                    "backend_id": self.backend_id,
                    "backend_name": self.backend_name,
                    "request_count": self.request_count,
                    "www_root": str(self.www_root),
                }
                response = build_response(
                    200,
                    json.dumps(info, indent=2).encode(),
                    "application/json",
                    extra_headers
                )
            else:
                # Serve static file
                response = self.serve_file(req.target, extra_headers)
            
            client_socket.sendall(response)
            
        except Exception as e:
            self.log(f"Error: {e}")
            try:
                error_response = build_response(
                    500,
                    f"Internal Server Error: {e}".encode(),
                    "text/plain"
                )
                client_socket.sendall(error_response)
            except Exception:
                pass
        finally:
            client_socket.close()
    
    def serve_file(self, target: str, extra_headers: Dict[str, str]) -> bytes:
        """Serve a static file."""
        # Normalise path
        path = target.lstrip("/")
        if not path or path == "/":
            path = "index.html"
        
        # Security: prevent directory traversal
        try:
            full_path = (self.www_root / path).resolve()
            if not str(full_path).startswith(str(self.www_root)):
                return build_response(403, b"Forbidden", "text/plain", extra_headers)
        except Exception:
            return build_response(403, b"Forbidden", "text/plain", extra_headers)
        
        # Check if file exists
        if not full_path.exists() or not full_path.is_file():
            return build_response(
                404,
                f"Not Found: {target}".encode(),
                "text/plain",
                extra_headers
            )
        
        # Read and serve file
        try:
            content = full_path.read_bytes()
            content_type = self.guess_mime_type(full_path)
            return build_response(200, content, content_type, extra_headers)
        except Exception as e:
            return build_response(
                500,
                f"Error reading file: {e}".encode(),
                "text/plain",
                extra_headers
            )
    
    def guess_mime_type(self, path: Path) -> str:
        """Guess MIME type from file extension."""
        mime_types = {
            ".html": "text/html; charset=utf-8",
            ".htm": "text/html; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".js": "application/javascript",
            ".json": "application/json",
            ".txt": "text/plain; charset=utf-8",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".svg": "image/svg+xml",
            ".ico": "image/x-icon",
        }
        return mime_types.get(path.suffix.lower(), "application/octet-stream")
    
    def run(self):
        """Start the server."""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen(64)
            self.running = True
            
            self.log(f"Server started on http://{self.host}:{self.port}/")
            self.log(f"Document root: {self.www_root}")
            self.log(f"Backend ID: {self.backend_id}, Name: {self.backend_name}")
            
            while self.running:
                try:
                    client_socket, client_addr = server_socket.accept()
                    # Handle in a new thread
                    thread = threading.Thread(
                        target=self.handle_request,
                        args=(client_socket, client_addr),
                        daemon=True
                    )
                    thread.start()
                except OSError:
                    break
                    
        except KeyboardInterrupt:
            self.log("Shutting down...")
        finally:
            self.running = False
            server_socket.close()


def main():
    parser = argparse.ArgumentParser(
        description="Backend HTTP Server for nginx proxy"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Bind address (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=int(os.environ.get("HTTP_PORT", 8080)),
        help="Port number (default: 8080 or HTTP_PORT env)"
    )
    parser.add_argument(
        "--www", "-w",
        default=os.environ.get("WWW_DIR", "/var/www"),
        help="Document root (default: /var/www or WWW_DIR env)"
    )
    parser.add_argument(
        "--id",
        default=os.environ.get("BACKEND_ID", "0"),
        help="Backend ID (default: 0 or BACKEND_ID env)"
    )
    parser.add_argument(
        "--name", "-n",
        default=os.environ.get("BACKEND_NAME", "Backend"),
        help="Backend name (default: Backend or BACKEND_NAME env)"
    )
    
    args = parser.parse_args()
    
    server = BackendServer(
        host=args.host,
        port=args.port,
        www_root=args.www,
        backend_id=args.id,
        backend_name=args.name
    )
    server.run()


if __name__ == "__main__":
    main()
