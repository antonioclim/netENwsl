#!/usr/bin/env python3
"""
Exercise 9.03 – FTP Client Demo using ftplib (Python Standard Library)

═══════════════════════════════════════════════════════════════════════════════
OBJECTIVES:
═══════════════════════════════════════════════════════════════════════════════
1. Demonstrate FTP client operations using Python's standard ftplib
2. Compare standard FTP client behaviour with our pseudo-FTP implementation
3. Observe active vs passive mode differences
4. Understand the dual-channel architecture in practice

═══════════════════════════════════════════════════════════════════════════════
KEY CONCEPTS:
═══════════════════════════════════════════════════════════════════════════════

1. FTP DUAL-CHANNEL ARCHITECTURE
   
   Control Channel (port 21/2121):
   ┌────────────────────────────────────────────────────────────────────────┐
   │ USER test → 331 Password required                                      │
   │ PASS ***** → 230 Login successful                                      │
   │ PASV       → 227 Entering Passive Mode (h1,h2,h3,h4,p1,p2)            │
   │ RETR file  → 150 Opening data connection                              │
   │ QUIT       → 221 Goodbye                                              │
   └────────────────────────────────────────────────────────────────────────┘
   
   Data Channel (dynamic port):
   ┌────────────────────────────────────────────────────────────────────────┐
   │ [Binary file contents transferred here]                                │
   │ Connection closed after transfer completes                             │
   └────────────────────────────────────────────────────────────────────────┘

2. PASSIVE vs ACTIVE MODE
   
   Passive (PASV): Client connects TO server's data port — NAT-friendly
   Active (PORT):  Server connects TO client's data port — blocked by NAT

═══════════════════════════════════════════════════════════════════════════════
USAGE:
═══════════════════════════════════════════════════════════════════════════════

# List files on FTP server
python3 ex_9_03_ftp_client_demo.py --host 127.0.0.1 --port 2121 --user test --password 12345 list

# Download a file
python3 ex_9_03_ftp_client_demo.py ... get hello.txt

# Upload a file
python3 ex_9_03_ftp_client_demo.py ... put myfile.txt

# Show current directory
python3 ex_9_03_ftp_client_demo.py ... pwd

Pair Programming Notes:
- Driver: Execute commands and observe Wireshark capture
- Navigator: Predict response codes and verify dual-channel behaviour
- Swap after: Completing LIST and GET operations
"""

from __future__ import annotations

import argparse
import sys
from ftplib import FTP
from pathlib import Path
from typing import Optional


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
    Parse command-line arguments for FTP client configuration.
    
    Returns:
        Namespace containing all parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="FTP Demo Client — demonstrates standard FTP operations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --host localhost --port 2121 --user test --password 12345 list
  %(prog)s --port 2121 get document.pdf
  %(prog)s --port 2121 put local_file.txt
        """
    )
    parser.add_argument("--host", default="127.0.0.1", help="Server address")
    parser.add_argument("--port", type=int, default=2121, help="Port")
    parser.add_argument("--user", default="test", help="Username")
    parser.add_argument("--password", default="12345", help="Password")
    parser.add_argument("--local-dir", default="./client-files", help="Local directory")
    parser.add_argument("--passive", action="store_true", default=True, 
                        help="Passive mode (default)")
    parser.add_argument("--active", action="store_true", help="Active mode")
    parser.add_argument("--predict", action="store_true", 
                        help="Enable prediction prompts for learning")
    parser.add_argument("command", help="Command: list, get, put, pwd")
    parser.add_argument("argument", nargs="?", help="Argument for command")
    
    return parser.parse_args()


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_LOCAL_DIRECTORY
# ═══════════════════════════════════════════════════════════════════════════════

def setup_local_directory(local_dir: str) -> Path:
    """
    Ensure local directory exists for file transfers.
    
    Args:
        local_dir: Path to local directory (relative or absolute)
        
    Returns:
        Resolved Path object to the local directory
    """
    local_path = Path(local_dir).resolve()
    local_path.mkdir(parents=True, exist_ok=True)
    return local_path


# ═══════════════════════════════════════════════════════════════════════════════
# CONNECT_TO_SERVER
# ═══════════════════════════════════════════════════════════════════════════════

def connect_to_server(host: str, port: int, passive: bool) -> FTP:
    """
    Establish TCP connection to FTP server (control channel).
    
    This creates the control channel connection on the specified port.
    The data channel will be established separately for each transfer.
    
    Args:
        host: Server hostname or IP address
        port: Server port (typically 21, here 2121)
        passive: True for passive mode, False for active mode
        
    Returns:
        Connected FTP object (not yet authenticated)
    """
    ftp = FTP()
    ftp.connect(host, port)
    print(f"[CLIENT] Connected to {host}:{port}")
    
    # Set transfer mode
    ftp.set_pasv(passive)
    mode_name = "Passive" if passive else "Active"
    print(f"[CLIENT] {mode_name} mode enabled")
    
    return ftp


# ═══════════════════════════════════════════════════════════════════════════════
# AUTHENTICATE
# ═══════════════════════════════════════════════════════════════════════════════

def authenticate(ftp: FTP, user: str, password: str) -> bool:
    """
    Authenticate with FTP server using USER and PASS commands.
    
    FTP authentication sequence:
    1. USER <username> → 331 Password required
    2. PASS <password> → 230 Login successful (or 530 Login incorrect)
    
    Args:
        ftp: Connected FTP object
        user: Username for authentication
        password: Password for authentication
        
    Returns:
        True if authentication successful, False otherwise
    """
    try:
        response = ftp.login(user, password)
        print(f"[CLIENT] Login: {response}")
        return True
    except Exception as e:
        print(f"[CLIENT] Authentication failed: {e}")
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_COMMAND
# ═══════════════════════════════════════════════════════════════════════════════

def execute_command(ftp: FTP, command: str, argument: Optional[str], 
                    local_dir: Path) -> int:
    """
    Execute the requested FTP command.
    
    Supported commands:
    - list/ls: List directory contents (uses LIST command)
    - pwd: Print working directory
    - get: Download file (uses RETR command)
    - put: Upload file (uses STOR command)
    
    Args:
        ftp: Authenticated FTP object
        command: Command to execute (list, get, put, pwd)
        argument: Optional argument (filename for get/put)
        local_dir: Local directory for file operations
        
    Returns:
        0 on success, 1 on error
    """
    cmd = command.lower()
    
    # ─── LIST DIRECTORY ───
    if cmd in ("list", "ls"):
        print("[CLIENT] === Directory listing ===")
        ftp.retrlines("LIST")
        return 0
    
    # ─── PRINT WORKING DIRECTORY ───
    elif cmd == "pwd":
        print(f"[CLIENT] Current directory: {ftp.pwd()}")
        return 0
    
    # ─── DOWNLOAD FILE (RETR) ───
    elif cmd == "get":
        if not argument:
            print("Usage: get <filename>")
            return 1
        
        local_path = local_dir / argument
        print(f"[CLIENT] Downloading: {argument} -> {local_path}")
        
        with open(local_path, "wb") as f:
            ftp.retrbinary(f"RETR {argument}", f.write)
        
        print(f"[CLIENT] ✓ Saved: {local_path} ({local_path.stat().st_size} bytes)")
        return 0
    
    # ─── UPLOAD FILE (STOR) ───
    elif cmd == "put":
        if not argument:
            print("Usage: put <filename>")
            return 1
        
        local_path = local_dir / argument
        if not local_path.is_file():
            print(f"File does not exist: {local_path}")
            return 1
        
        print(f"[CLIENT] Uploading: {local_path}")
        
        with open(local_path, "rb") as f:
            ftp.storbinary(f"STOR {argument}", f)
        
        print(f"[CLIENT] ✓ Uploaded: {argument}")
        return 0
    
    else:
        print(f"Unknown command: {cmd}")
        print("Available commands: list, pwd, get, put")
        return 1


# ═══════════════════════════════════════════════════════════════════════════════
# CLEANUP
# ═══════════════════════════════════════════════════════════════════════════════

def cleanup(ftp: FTP) -> None:
    """
    Gracefully close FTP connection using QUIT command.
    
    The QUIT command closes both control and any active data channels.
    Server responds with 221 Goodbye.
    """
    try:
        ftp.quit()
        print("[CLIENT] Disconnected")
    except Exception:
        # Connection may already be closed
        pass


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """
    Main entry point for FTP client demonstration.
    
    Workflow:
    1. Parse command-line arguments
    2. Setup local directory for file transfers
    3. Connect to FTP server (control channel)
    4. Authenticate with USER/PASS
    5. Execute requested command
    6. Cleanup and disconnect
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    # ─── PARSE ARGUMENTS ───
    args = parse_arguments()
    
    # ─── SETUP LOCAL DIRECTORY ───
    local_dir = setup_local_directory(args.local_dir)
    
    # ─── PREDICTION PROMPT (if enabled) ───
    if args.predict:
        prompt_prediction(
            "How many TCP connections will be used for this FTP session?\n"
            "   (a) 1 — single connection for everything\n"
            "   (b) 2 — control channel + data channel\n"
            "   (c) 3 — authentication + commands + data"
        )
    
    try:
        # ─── CONNECT TO SERVER ───
        passive_mode = not args.active
        ftp = connect_to_server(args.host, args.port, passive_mode)
        
        # ─── AUTHENTICATE ───
        if not authenticate(ftp, args.user, args.password):
            return 1
        
        # ─── EXECUTE COMMAND ───
        result = execute_command(ftp, args.command, args.argument, local_dir)
        
        # ─── CLEANUP ───
        cleanup(ftp)
        
        return result
        
    except Exception as e:
        print(f"[CLIENT] Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
