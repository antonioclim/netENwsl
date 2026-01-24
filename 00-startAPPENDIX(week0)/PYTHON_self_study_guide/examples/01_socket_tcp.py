#!/usr/bin/env python3
"""
Example 1: Basic TCP Server and Client
======================================
Demonstrates fundamental socket programming concepts.

Course: Computer Networks - ASE Bucharest, CSIE
Author: ing. dr. Antonio Clim
Version: 2.1 — with subgoal labels and extended comments

💡 ANALOGY: Socket as a Landline Telephone
------------------------------------------
| Socket Operation | Telephone Equivalent                  |
|------------------|---------------------------------------|
| socket()         | You buy a new telephone               |
| bind()           | You get assigned a phone number (port)|
| listen()         | You plug in the phone, wait for calls |
| accept()         | You pick up the receiver when it rings|
| connect()        | You dial someone's number             |
| send()/recv()    | You speak / You listen                |
| close()          | You hang up the phone                 |

Learning objectives:
- Understanding the client-server model
- Proper handling of network errors
- Context manager pattern for resources
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import socket
import sys
import logging
from typing import Optional

__all__ = ['server', 'client', 'DEFAULT_HOST', 'DEFAULT_PORT', 'BUFFER_SIZE']

# ═══════════════════════════════════════════════════════════════════════════════
# LOGGING_CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
# NOTE: Logging is preferred over print() for production debugging
# because you can control the level (DEBUG/INFO/WARNING) and format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION_CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════
DEFAULT_HOST: str = '0.0.0.0'  # Listen on all interfaces
DEFAULT_PORT: int = 8080
BUFFER_SIZE: int = 1024  # Buffer size for recv()
SOCKET_TIMEOUT: float = 30.0  # Timeout in seconds
MAX_CONNECTIONS: int = 5  # Backlog for listen()


# ═══════════════════════════════════════════════════════════════════════════════
# SERVER_IMPLEMENTATION
# ═══════════════════════════════════════════════════════════════════════════════
def server(port: int = DEFAULT_PORT) -> None:
    """Start a simple TCP server that echoes messages.
    
    The server listens on all interfaces (0.0.0.0) and responds
    with the uppercase version of the received message.
    
    Args:
        port: The port to listen on (default 8080)
        
    Returns:
        None. Runs indefinitely until Ctrl+C.
        
    Raises:
        OSError: If the port is already in use or unavailable
        
    Example:
        >>> server(8080)
        [SERVER] Listening on port 8080...
        
    Note:
        - Handles one client at a time (for simplicity)
        - For multi-client, see threading examples
        
    See Also:
        - client(): The complementary client function
        - https://docs.python.org/3/library/socket.html
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # ───────────────────────────────────────────────────────────
            # SOCKET_OPTIONS_CONFIGURATION
            # ───────────────────────────────────────────────────────────
            # HACK: SO_REUSEADDR allows quick rebind after restart.
            # Without it, you must wait ~60s (TIME_WAIT) after stopping.
            # WARNING: In production, evaluate the security implications!
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # ───────────────────────────────────────────────────────────
            # BIND_AND_LISTEN
            # ───────────────────────────────────────────────────────────
            # NOTE: 0.0.0.0 = listen on ALL interfaces (localhost + LAN)
            # For local only, change to 127.0.0.1
            s.bind((DEFAULT_HOST, port))
            s.listen(MAX_CONNECTIONS)
            
            logger.info(f"Server started on port {port}")
            print(f"[SERVER] Listening on port {port}...")
            print(f"[SERVER] Stop with Ctrl+C")
            
            # ───────────────────────────────────────────────────────────
            # ACCEPT_CONNECTIONS_LOOP
            # ───────────────────────────────────────────────────────────
            # TODO: Add support for multiple simultaneous connections (threading)
            while True:
                try:
                    conn, addr = s.accept()
                    logger.info(f"New connection from {addr}")
                    print(f"[SERVER] Connection from {addr}")
                    
                    with conn:
                        # HACK: Set timeout to avoid indefinite blocking
                        # if client doesn't send data
                        conn.settimeout(SOCKET_TIMEOUT)
                        
                        try:
                            # ───────────────────────────────────────────
                            # RECEIVE_DATA
                            # ───────────────────────────────────────────
                            data: bytes = conn.recv(BUFFER_SIZE)
                            
                            if not data:
                                # NOTE: Empty data = client closed connection
                                logger.warning(f"Client {addr} sent empty data")
                                continue
                            
                            # ───────────────────────────────────────────
                            # PROCESS_MESSAGE
                            # ───────────────────────────────────────────
                            # NOTE: errors='replace' replaces invalid
                            # characters with � instead of raising exception
                            decoded_message: str = data.decode('utf-8', errors='replace')
                            print(f"[SERVER] Received: {decoded_message}")
                            logger.info(f"Received from {addr}: {decoded_message[:50]}...")
                            
                            # ───────────────────────────────────────────
                            # SEND_RESPONSE
                            # ───────────────────────────────────────────
                            # NOTE: sendall() guarantees complete sending,
                            # unlike send() which may send partially
                            response: bytes = b"OK: " + data.upper()
                            conn.sendall(response)
                            print(f"[SERVER] Sent: {response.decode('utf-8', errors='replace')}")
                            
                        except socket.timeout:
                            logger.warning(f"Timeout reading from {addr}")
                            print(f"[SERVER] Timeout - client {addr} did not send data")
                            
                        except AicodeDecodeError as e:
                            # NOTE: Rarely happens with errors='replace',
                            # but kept for safety
                            logger.error(f"Decode error from {addr}: {e}")
                            print(f"[SERVER] Decode error: {e}")
                            conn.sendall(b"ERROR: Invalid encoding")
                            
                except ConnectionResetError:
                    # NOTE: Client abruptly closed connection (e.g.: Ctrl+C)
                    logger.warning(f"Client disconnected abruptly")
                    print("[SERVER] Client disconnected abruptly (connection reset)")
                    
                except ConnectionAbortedError:
                    logger.warning("Connection aborted")
                    print("[SERVER] Connection aborted")
                    
    except OSError as e:
        # ───────────────────────────────────────────────────────────────
        # STARTUP_ERROR_HANDLING
        # ───────────────────────────────────────────────────────────────
        logger.error(f"Cannot start server: {e}")
        print(f"[ERROR] Cannot start server: {e}")
        
        # NOTE: Provide concrete solutions for the most common error
        if "Address already in use" in str(e):
            print("  → The port is already in use!")
            print("  → Solutions:")
            print("    1. Wait ~60 seconds and try again")
            print("    2. Use a different port: python script.py server 8081")
            print("    3. Check what's using the port: ss -tlnp | grep 8080")
        sys.exit(1)
        
    except KeyboardInterrupt:
        # NOTE: Ctrl+C is the normal way to stop
        logger.info("Server stopped by user")
        print("\n[SERVER] Stopped at user's request (Ctrl+C)")


# ═══════════════════════════════════════════════════════════════════════════════
# CLIENT_IMPLEMENTATION
# ═══════════════════════════════════════════════════════════════════════════════
def client(host: str = '127.0.0.1', port: int = DEFAULT_PORT, 
           message: str = 'Test') -> Optional[str]:
    """Send a message to the server and return the response.
    
    Creates a TCP connection, sends the message, waits for response,
    then closes the connection.
    
    Args:
        host: Server IP address or hostname
        port: Server port (default 8080)
        message: Message to send (default 'Test')
        
    Returns:
        Server response as string, or None if failed
        
    Raises:
        Does not raise exceptions — handles them internally and returns None
        
    Example:
        >>> response = client('127.0.0.1', 8080, 'Hello')
        >>> print(response)
        'OK: HELLO'
        
    Note:
        The function does not raise exceptions to simplify integration.
        Check if the result is None to detect errors.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # ───────────────────────────────────────────────────────────
            # TIMEOUT_CONFIGURATION
            # ───────────────────────────────────────────────────────────
            # NOTE: Timeout for connect() — avoids blocking if server
            # doesn't respond (firewall, wrong address, etc.)
            s.settimeout(10.0)
            
            # ───────────────────────────────────────────────────────────
            # CONNECT_TO_SERVER
            # ───────────────────────────────────────────────────────────
            logger.info(f"Connecting to {host}:{port}")
            s.connect((host, port))
            
            print(f"[CLIENT] Connected to {host}:{port}")
            print(f"[CLIENT] Sending: {message}")
            
            # ───────────────────────────────────────────────────────────
            # SEND_MESSAGE
            # ───────────────────────────────────────────────────────────
            # NOTE: encode() converts str → bytes (required for socket)
            s.sendall(message.encode('utf-8'))
            
            # ───────────────────────────────────────────────────────────
            # RECEIVE_RESPONSE
            # ───────────────────────────────────────────────────────────
            response: bytes = s.recv(BUFFER_SIZE)
            
            if not response:
                logger.warning("Server closed connection without response")
                print("[CLIENT] Server did not send a response")
                return None
                
            response_str: str = response.decode('utf-8', errors='replace')
            print(f"[CLIENT] Response: {response_str}")
            logger.info(f"Response received: {response_str[:50]}...")
            
            return response_str
            
    except socket.timeout:
        logger.error(f"Timeout connecting to {host}:{port}")
        print(f"[ERROR] Timeout - server not responding within 10 seconds")
        print("  → Check if the server is running")
        return None
        
    except ConnectionRefusedError:
        logger.error(f"Connection refused by {host}:{port}")
        print(f"[ERROR] Connection refused by {host}:{port}")
        print("  → Server is not running or port is wrong")
        print("  → Start the server: python 01_socket_tcp.py server")
        return None
        
    except socket.gaierror as e:
        # NOTE: gaierror = "getaddrinfo error" = DNS problem
        logger.error(f"DNS error for {host}: {e}")
        print(f"[ERROR] Cannot resolve address '{host}': {e}")
        return None
        
    except OSError as e:
        logger.error(f"Network error: {e}")
        print(f"[ERROR] Network problem: {e}")
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# USER_INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════
def print_usage() -> None:
    """Display usage instructions."""
    print("""
╔═══════════════════════════════════════════════════════════════════════╗
║  01_socket_tcp.py - TCP Server/Client Example                         ║
╠═══════════════════════════════════════════════════════════════════════╣
║  USAGE:                                                               ║
║    Server:  python 01_socket_tcp.py server [port]                     ║
║    Client:  python 01_socket_tcp.py [message]                         ║
║    Client:  python 01_socket_tcp.py client [host] [port] [message]    ║
║                                                                       ║
║  EXAMPLES:                                                            ║
║    python 01_socket_tcp.py server              # Server on 8080       ║
║    python 01_socket_tcp.py server 9000         # Server on 9000       ║
║    python 01_socket_tcp.py "Hello world"       # Client to 8080       ║
║    python 01_socket_tcp.py client 192.168.1.5 8080 "Test"             ║
║                                                                       ║
║  DEBUGGING:                                                           ║
║    - Check port: ss -tlnp | grep 8080                                 ║
║    - Enable debug: export LOG_LEVEL=DEBUG                             ║
╚═══════════════════════════════════════════════════════════════════════╝
""")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point — parses arguments and executes.
    
    Returns:
        Exit code: 0 for success, 1 for error
    """
    if len(sys.argv) < 2:
        print_usage()
        return 0
        
    if sys.argv[1] == 'server':
        port: int = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_PORT
        server(port)
        return 0
        
    elif sys.argv[1] == 'client':
        # Format: client [host] [port] [message]
        host: str = sys.argv[2] if len(sys.argv) > 2 else '127.0.0.1'
        port: int = int(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_PORT
        msg: str = ' '.join(sys.argv[4:]) if len(sys.argv) > 4 else 'Hello'
        result = client(host, port, msg)
        return 0 if result else 1
        
    elif sys.argv[1] in ['-h', '--help', 'help']:
        print_usage()
        return 0
        
    else:
        # Treat arguments as message for client
        message: str = ' '.join(sys.argv[1:])
        result = client(message=message)
        return 0 if result else 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        sys.exit(1)
