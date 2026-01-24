#!/usr/bin/env python3
"""
Exercise 9.04 – FTP Server Demo using pyftpdlib

═══════════════════════════════════════════════════════════════════════════════
OBJECTIVES:
═══════════════════════════════════════════════════════════════════════════════
1. Demonstrate a production-quality FTP server implementation
2. Compare pyftpdlib behaviour with our pseudo-FTP server
3. Understand FTP server configuration: users, permissions, passive ports
4. Observe multi-client session handling

═══════════════════════════════════════════════════════════════════════════════
KEY CONCEPTS:
═══════════════════════════════════════════════════════════════════════════════

1. FTP SERVER ARCHITECTURE
   
   ┌─────────────────────────────────────────────────────────────────────────┐
   │                         FTP Server Components                           │
   ├─────────────────────────────────────────────────────────────────────────┤
   │                                                                         │
   │   Authorizer                Handler                  Server             │
   │   ┌───────────┐            ┌───────────┐           ┌───────────┐       │
   │   │ Users     │────────────│ Protocol  │───────────│ Listener  │       │
   │   │ Passwords │            │ Logic     │           │ Socket    │       │
   │   │ Permissions│           │ Commands  │           │ Port 21   │       │
   │   └───────────┘            └───────────┘           └───────────┘       │
   │                                                                         │
   └─────────────────────────────────────────────────────────────────────────┘

2. FTP PERMISSION CODES
   
   Each letter grants a specific capability:
   
   │ Code │ Permission │ FTP Command │ Description                         │
   │──────│────────────│─────────────│─────────────────────────────────────│
   │  e   │ cwd        │ CWD, CDUP   │ Change working directory            │
   │  l   │ list       │ LIST, NLST  │ List directory contents             │
   │  r   │ retrieve   │ RETR        │ Download files                      │
   │  a   │ append     │ APPE        │ Append to existing files            │
   │  d   │ delete     │ DELE, RMD   │ Delete files and directories        │
   │  f   │ rename     │ RNFR, RNTO  │ Rename files                        │
   │  m   │ mkdir      │ MKD         │ Create directories                  │
   │  w   │ store      │ STOR, STOU  │ Upload files                        │

3. PASSIVE MODE PORTS
   
   Server allocates ports from a configured range for data connections:
   - Control: port 21 (or 2121 in our lab)
   - Data: ports 60000-60100 (passive mode range)
   
   Each concurrent client gets a unique passive port.

═══════════════════════════════════════════════════════════════════════════════
USAGE:
═══════════════════════════════════════════════════════════════════════════════

# Start with defaults
python3 ex_9_04_ftp_server_demo.py

# Custom configuration
python3 ex_9_04_ftp_server_demo.py --host 0.0.0.0 --port 2121 --root ./server-files

# Custom passive port range
python3 ex_9_04_ftp_server_demo.py --passive-ports 60000-60010

Pair Programming Notes:
- Driver: Configure and start the server
- Navigator: Connect with client and verify permissions
- Swap after: Testing LIST and RETR operations
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Tuple


# ═══════════════════════════════════════════════════════════════════════════════
# IMPORT_DEPENDENCIES
# ═══════════════════════════════════════════════════════════════════════════════

try:
    from pyftpdlib.authorizers import DummyAuthorizer
    from pyftpdlib.handlers import FTPHandler
    from pyftpdlib.servers import FTPServer
except ImportError:
    print("Error: pyftpdlib is not installed.")
    print("Install with: pip install pyftpdlib --break-system-packages")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# PREDICTION_PROMPTS
# ═══════════════════════════════════════════════════════════════════════════════

def prompt_prediction(question: str, pause: bool = True) -> None:
    """
    Display a prediction prompt before demonstrating a concept.
    
    This implements Brown & Wilson Principle 4: Predictions.
    Having students predict outcomes before seeing results improves retention.
    
    Args:
        question: The prediction question to display
        pause: Whether to wait for user input
    """
    print(f"\n💭 PREDICTION: {question}")
    if pause:
        input("   Press Enter after making your prediction...")
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# PARSE_ARGUMENTS
# ═══════════════════════════════════════════════════════════════════════════════

def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for FTP server configuration.
    
    Returns:
        Namespace containing all parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="FTP Demo Server — demonstrates FTP server configuration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                    # Default settings
  %(prog)s --port 2121 --user admin          # Custom user
  %(prog)s --passive-ports 60000-60010       # Limited passive range
        """
    )
    parser.add_argument("--host", default="127.0.0.1", help="Bind address")
    parser.add_argument("--port", type=int, default=2121, help="Port (default: 2121)")
    parser.add_argument("--root", default="./server-files", help="Root directory")
    parser.add_argument("--user", default="test", help="Username")
    parser.add_argument("--password", default="12345", help="Password")
    parser.add_argument("--passive-ports", default="60000-60100", 
                        help="Passive port range (default: 60000-60100)")
    parser.add_argument("--predict", action="store_true",
                        help="Enable prediction prompts for learning")
    
    return parser.parse_args()


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_DIRECTORIES
# ═══════════════════════════════════════════════════════════════════════════════

def setup_directories(root: str) -> Path:
    """
    Ensure the FTP root directory exists.
    
    Args:
        root: Path to FTP root directory
        
    Returns:
        Resolved Path object to the root directory
    """
    root_path = Path(root).resolve()
    root_path.mkdir(parents=True, exist_ok=True)
    return root_path


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURE_AUTHORISATION
# ═══════════════════════════════════════════════════════════════════════════════

def configure_authorisation(user: str, password: str, root_path: Path) -> DummyAuthorizer:
    """
    Configure FTP user authentication and permissions.
    
    Permission codes:
    - e: change directory (CWD, CDUP)
    - l: list files (LIST, NLST)
    - r: retrieve/download files (RETR)
    - a: append to files (APPE)
    - d: delete files/directories (DELE, RMD)
    - f: rename files (RNFR, RNTO)
    - m: create directories (MKD)
    - w: store/upload files (STOR, STOU)
    
    Args:
        user: Username for authentication
        password: Password for authentication
        root_path: FTP root directory for this user
        
    Returns:
        Configured DummyAuthorizer instance
    """
    authorizer = DummyAuthorizer()
    
    # Add user with full permissions
    # perm="elradfmw" grants all standard FTP operations
    authorizer.add_user(
        username=user,
        password=password,
        homedir=str(root_path),
        perm="elradfmw"  # e=cwd, l=list, r=retr, a=appe, d=delete, f=rename, m=mkdir, w=stor
    )
    
    return authorizer


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURE_HANDLER
# ═══════════════════════════════════════════════════════════════════════════════

def configure_handler(authorizer: DummyAuthorizer, 
                      passive_ports: str) -> type:
    """
    Configure FTP protocol handler with authorisation and passive ports.
    
    The handler processes FTP commands and manages data connections.
    Passive ports are used when clients request PASV mode.
    
    Args:
        authorizer: Configured user authorisation
        passive_ports: Port range string (e.g., "60000-60100")
        
    Returns:
        Configured FTPHandler class (not instance)
    """
    # Parse passive port range
    start_port, end_port = parse_port_range(passive_ports)
    
    # Configure handler class
    handler = FTPHandler
    handler.authorizer = authorizer
    handler.banner = "Week 9 FTP Demo Server (pyftpdlib)"
    handler.passive_ports = range(start_port, end_port + 1)
    
    return handler


def parse_port_range(port_range: str) -> Tuple[int, int]:
    """
    Parse a port range string into start and end integers.
    
    Args:
        port_range: String like "60000-60100"
        
    Returns:
        Tuple of (start_port, end_port)
        
    Raises:
        ValueError: If format is invalid
    """
    try:
        start, end = map(int, port_range.split("-"))
        return start, end
    except ValueError:
        raise ValueError(f"Invalid port range format: {port_range}. Expected: START-END")


# ═══════════════════════════════════════════════════════════════════════════════
# START_SERVER
# ═══════════════════════════════════════════════════════════════════════════════

def start_server(host: str, port: int, handler: type, 
                 root_path: Path, user: str, passive_ports: str) -> None:
    """
    Create and start the FTP server.
    
    Server listens on the specified address and handles connections
    using the configured handler. Runs until Ctrl+C is pressed.
    
    Args:
        host: IP address to bind to
        port: Port number to listen on
        handler: Configured FTPHandler class
        root_path: FTP root directory
        user: Username (for display)
        passive_ports: Passive port range (for display)
    """
    # Create server instance
    address = (host, port)
    server = FTPServer(address, handler)
    
    # Configure connection limits
    server.max_cons = 256           # Maximum simultaneous connections
    server.max_cons_per_ip = 5      # Maximum connections per IP address
    
    # Display server information
    print("=" * 60)
    print("  FTP SERVER STARTED")
    print("=" * 60)
    print(f"  Address:       {host}:{port}")
    print(f"  Root:          {root_path}")
    print(f"  User:          {user}")
    print(f"  Passive ports: {passive_ports}")
    print(f"  Max clients:   {server.max_cons}")
    print("=" * 60)
    print("  Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    # Run server (blocking)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[FTP SERVER] Stopping...")
        server.close_all()
        print("[FTP SERVER] Stopped")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """
    Main entry point for FTP server demonstration.
    
    Workflow:
    1. Parse command-line arguments
    2. Setup root directory
    3. Configure user authorisation
    4. Configure protocol handler
    5. Start server (runs until Ctrl+C)
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    # ─── PARSE ARGUMENTS ───
    args = parse_arguments()
    
    # ─── PREDICTION PROMPT (if enabled) ───
    if args.predict:
        prompt_prediction(
            "When a client connects in passive mode, which component\n"
            "   allocates the data channel port?\n"
            "   (a) The client chooses a port\n"
            "   (b) The server allocates from passive_ports range\n"
            "   (c) The operating system assigns randomly"
        )
    
    try:
        # ─── SETUP DIRECTORIES ───
        root_path = setup_directories(args.root)
        
        # ─── CONFIGURE AUTHORISATION ───
        authorizer = configure_authorisation(args.user, args.password, root_path)
        
        # ─── CONFIGURE HANDLER ───
        handler = configure_handler(authorizer, args.passive_ports)
        
        # ─── START SERVER ───
        start_server(
            host=args.host,
            port=args.port,
            handler=handler,
            root_path=root_path,
            user=args.user,
            passive_ports=args.passive_ports
        )
        
        return 0
        
    except Exception as e:
        print(f"[FTP SERVER] Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
