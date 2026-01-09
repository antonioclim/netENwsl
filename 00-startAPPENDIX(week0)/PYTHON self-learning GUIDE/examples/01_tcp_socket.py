#!/usr/bin/env python3
"""
Example 1: Basic TCP Server and Client
Demonstrates fundamental socket programming concepts.
"""
import socket
import sys

def server(port: int = 8080):
    """Start a simple TCP server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', port))
        s.listen(5)
        print(f"[SERVER] Listening on port {port}...")
        
        while True:
            conn, addr = s.accept()
            print(f"[SERVER] Connection from {addr}")
            with conn:
                data = conn.recv(1024)
                print(f"[SERVER] Received: {data.decode()}")
                response = b"OK: " + data.upper()
                conn.sendall(response)
                print(f"[SERVER] Sent: {response.decode()}")

def client(host: str = '127.0.0.1', port: int = 8080, message: str = 'Test'):
    """Send a message to the server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print(f"[CLIENT] Sending: {message}")
        s.sendall(message.encode())
        response = s.recv(1024)
        print(f"[CLIENT] Response: {response.decode()}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'server':
        server()
    else:
        client(message=' '.join(sys.argv[1:]) if len(sys.argv) > 1 else 'Hello')
