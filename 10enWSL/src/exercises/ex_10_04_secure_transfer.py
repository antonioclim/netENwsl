#!/usr/bin/env python3
"""
Week 10 - Exercise 4: Secure Shell and File Transfer Protocols
=================================================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

This exercise demonstrates SSH and FTP client operations using Python
libraries (paramiko for SSH, ftplib for FTP).

Objectives:
- Connect to SSH servers and execute remote commands
- Understand SSH authentication methods (password, key-based)
- Use FTP for file transfers (active vs passive mode)
- Compare encrypted (SSH/SFTP) vs unencrypted (FTP) protocols

Prerequisites:
- Python 3.11+
- paramiko library (pip install paramiko)
- Lab SSH and FTP containers running

Pair Programming Notes:
- Driver: Establish SSH connection and run commands
- Navigator: Monitor connections in Wireshark
- Swap after: Successful SSH session, before FTP testing

Security note
-------------
FTP transmits credentials in plaintext. Use SFTP (SSH File Transfer Protocol)
for production file transfers.

Common Errors
-------------
1. "Connection refused" → SSH/FTP container not running; docker ps
2. "Authentication failed" → Wrong credentials; SSH: labuser/labpass, FTP: labftp/labftp
3. "Host key verification failed" → First connection; use AutoAddPolicy or accept key
4. "paramiko not found" → pip install paramiko --break-system-packages
5. "Passive mode failed" → FTP ports 30000-30009 not mapped; check docker-compose
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import ftplib
import io
import sys
from typing import Optional

try:
    import paramiko
except ImportError:
    print("[WARNING] paramiko not installed, SSH features unavailable")
    paramiko = None  # type: ignore


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
DEFAULT_SSH_HOST = "localhost"
DEFAULT_SSH_PORT = 2222
DEFAULT_SSH_USER = "labuser"
DEFAULT_SSH_PASS = "labpass"

DEFAULT_FTP_HOST = "localhost"
DEFAULT_FTP_PORT = 2121
DEFAULT_FTP_USER = "labftp"
DEFAULT_FTP_PASS = "labftp"


# ═══════════════════════════════════════════════════════════════════════════════
# SSH_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def ssh_connect(
    host: str = DEFAULT_SSH_HOST,
    port: int = DEFAULT_SSH_PORT,
    username: str = DEFAULT_SSH_USER,
    password: str = DEFAULT_SSH_PASS,
) -> Optional[paramiko.SSHClient]:
    """
    Establish an SSH connection.
    
    💭 PREDICTION: What security warning might appear on first connection?
    Why is it important to verify host keys?
    
    Args:
        host: SSH server hostname
        port: SSH server port
        username: SSH username
        password: SSH password
    
    Returns:
        Connected SSHClient or None on failure
    """
    if paramiko is None:
        print("[ERROR] paramiko is required for SSH: pip install paramiko")
        return None
    
    try:
        client = paramiko.SSHClient()
        # AutoAddPolicy for lab use only! In production, verify host keys.
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        print(f"[SSH] Connecting to {host}:{port} as {username}...")
        client.connect(
            hostname=host,
            port=port,
            username=username,
            password=password,
            timeout=10,
            allow_agent=False,
            look_for_keys=False,
        )
        print("[SSH] Connected successfully")
        return client
    except paramiko.AuthenticationException:
        print("[ERROR] SSH authentication failed")
        return None
    except paramiko.SSHException as exc:
        print(f"[ERROR] SSH error: {exc}")
        return None
    except Exception as exc:
        print(f"[ERROR] Connection failed: {exc}")
        return None


def ssh_execute(client: paramiko.SSHClient, command: str) -> tuple[str, str, int]:
    """
    Execute a command over SSH.
    
    💭 PREDICTION: How does SSH ensure the command output is encrypted?
    
    Args:
        client: Connected SSHClient
        command: Command to execute
    
    Returns:
        Tuple of (stdout, stderr, exit_code)
    """
    print(f"[SSH] Executing: {command}")
    stdin, stdout, stderr = client.exec_command(command)
    
    exit_code = stdout.channel.recv_exit_status()
    stdout_text = stdout.read().decode("utf-8")
    stderr_text = stderr.read().decode("utf-8")
    
    return stdout_text, stderr_text, exit_code


def demo_ssh(host: str, port: int, username: str, password: str) -> None:
    """
    Demonstrate SSH operations.
    
    💭 PREDICTION: What system information will these commands reveal?
    """
    print("\n" + "#" * 60)
    print("# DEMO: SSH Remote Command Execution")
    print("#" * 60)
    
    client = ssh_connect(host, port, username, password)
    if client is None:
        return
    
    try:
        commands = [
            "hostname",
            "whoami",
            "uname -a",
            "date",
            "pwd",
        ]
        
        for cmd in commands:
            stdout, stderr, code = ssh_execute(client, cmd)
            print(f"\n$ {cmd}")
            if stdout.strip():
                print(f"  {stdout.strip()}")
            if stderr.strip():
                print(f"  [stderr] {stderr.strip()}")
            print(f"  [exit code: {code}]")
    finally:
        client.close()
        print("\n[SSH] Connection closed")


# ═══════════════════════════════════════════════════════════════════════════════
# FTP_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def ftp_connect(
    host: str = DEFAULT_FTP_HOST,
    port: int = DEFAULT_FTP_PORT,
    username: str = DEFAULT_FTP_USER,
    password: str = DEFAULT_FTP_PASS,
    passive: bool = True,
) -> Optional[ftplib.FTP]:
    """
    Establish an FTP connection.
    
    💭 PREDICTION: How many TCP connections will FTP establish?
    What's the difference between active and passive mode?
    
    Args:
        host: FTP server hostname
        port: FTP server port
        username: FTP username
        password: FTP password
        passive: Use passive mode (recommended for NAT)
    
    Returns:
        Connected FTP object or None on failure
    """
    try:
        print(f"[FTP] Connecting to {host}:{port} as {username}...")
        ftp = ftplib.FTP()
        ftp.connect(host, port, timeout=10)
        ftp.login(username, password)
        ftp.set_pasv(passive)
        
        mode = "passive" if passive else "active"
        print(f"[FTP] Connected successfully ({mode} mode)")
        print(f"[FTP] Server: {ftp.getwelcome()}")
        return ftp
    except ftplib.error_perm as exc:
        print(f"[ERROR] FTP permission error: {exc}")
        return None
    except Exception as exc:
        print(f"[ERROR] FTP connection failed: {exc}")
        return None


def ftp_list_directory(ftp: ftplib.FTP, path: str = ".") -> list[str]:
    """
    List directory contents.
    
    Args:
        ftp: Connected FTP object
        path: Directory path
    
    Returns:
        List of directory entries
    """
    print(f"[FTP] Listing directory: {path}")
    entries = []
    ftp.retrlines(f"LIST {path}", entries.append)
    return entries


def ftp_download_file(ftp: ftplib.FTP, remote_path: str) -> Optional[bytes]:
    """
    Download a file from FTP server.
    
    💭 PREDICTION: Which FTP command initiates the data transfer?
    
    Args:
        ftp: Connected FTP object
        remote_path: Path to remote file
    
    Returns:
        File contents as bytes or None on failure
    """
    print(f"[FTP] Downloading: {remote_path}")
    try:
        buffer = io.BytesIO()
        ftp.retrbinary(f"RETR {remote_path}", buffer.write)
        data = buffer.getvalue()
        print(f"[FTP] Downloaded {len(data)} bytes")
        return data
    except ftplib.error_perm as exc:
        print(f"[ERROR] Download failed: {exc}")
        return None


def ftp_upload_file(ftp: ftplib.FTP, remote_path: str, data: bytes) -> bool:
    """
    Upload a file to FTP server.
    
    Args:
        ftp: Connected FTP object
        remote_path: Path on remote server
        data: File contents as bytes
    
    Returns:
        True if upload succeeded
    """
    print(f"[FTP] Uploading to: {remote_path} ({len(data)} bytes)")
    try:
        buffer = io.BytesIO(data)
        ftp.storbinary(f"STOR {remote_path}", buffer)
        print("[FTP] Upload complete")
        return True
    except ftplib.error_perm as exc:
        print(f"[ERROR] Upload failed: {exc}")
        return False


def demo_ftp(host: str, port: int, username: str, password: str) -> None:
    """
    Demonstrate FTP operations.
    
    💭 PREDICTION: Can you see FTP credentials in Wireshark? Why?
    """
    print("\n" + "#" * 60)
    print("# DEMO: FTP File Transfer")
    print("#" * 60)
    
    ftp = ftp_connect(host, port, username, password)
    if ftp is None:
        return
    
    try:
        # Show current directory
        print(f"\n[FTP] Current directory: {ftp.pwd()}")
        
        # List directory
        print("\n[FTP] Directory listing:")
        entries = ftp_list_directory(ftp)
        for entry in entries:
            print(f"  {entry}")
        
        # Try to create and upload a test file
        test_data = b"Hello from Week 10 FTP exercise!\n"
        if ftp_upload_file(ftp, "test_upload.txt", test_data):
            # Download it back
            downloaded = ftp_download_file(ftp, "test_upload.txt")
            if downloaded:
                print(f"[FTP] Downloaded content: {downloaded.decode('utf-8').strip()}")
            
            # Delete test file
            try:
                ftp.delete("test_upload.txt")
                print("[FTP] Test file deleted")
            except ftplib.error_perm:
                print("[FTP] Could not delete test file")
    finally:
        ftp.quit()
        print("\n[FTP] Connection closed")


# ═══════════════════════════════════════════════════════════════════════════════
# PROTOCOL_COMPARISON
# ═══════════════════════════════════════════════════════════════════════════════
def compare_protocols() -> None:
    """Print a comparison of SSH/SFTP vs FTP."""
    print("\n" + "#" * 60)
    print("# Protocol Comparison: SSH/SFTP vs FTP")
    print("#" * 60)
    
    print("""
┌─────────────────┬───────────────────────┬───────────────────────┐
│ Aspect          │ SSH/SFTP              │ FTP                   │
├─────────────────┼───────────────────────┼───────────────────────┤
│ Encryption      │ Yes (always)          │ No (plaintext)        │
│ Port            │ 22                    │ 21 (control), 20/high │
│ Connections     │ Single multiplexed    │ Separate ctrl + data  │
│ Authentication  │ Password, keys, etc.  │ Password (plaintext)  │
│ NAT friendly    │ Yes                   │ Needs passive mode    │
│ Firewall        │ Single port           │ Multiple ports        │
│ Modern use      │ Recommended           │ Legacy only           │
└─────────────────┴───────────────────────┴───────────────────────┘

Security implications:
- FTP credentials are visible in network captures
- FTP file contents are transmitted in plaintext
- SSH encrypts everything: credentials, commands, data
- Always prefer SFTP over FTP for file transfers
""")


# ═══════════════════════════════════════════════════════════════════════════════
# ARGUMENT_PARSING
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="SSH and FTP Exercise")
    
    sub = parser.add_subparsers(dest="cmd", required=True)
    
    # SSH demo
    p_ssh = sub.add_parser("ssh", help="SSH demonstration")
    p_ssh.add_argument("--host", default=DEFAULT_SSH_HOST)
    p_ssh.add_argument("--port", type=int, default=DEFAULT_SSH_PORT)
    p_ssh.add_argument("--user", default=DEFAULT_SSH_USER)
    p_ssh.add_argument("--password", default=DEFAULT_SSH_PASS)
    
    # FTP demo
    p_ftp = sub.add_parser("ftp", help="FTP demonstration")
    p_ftp.add_argument("--host", default=DEFAULT_FTP_HOST)
    p_ftp.add_argument("--port", type=int, default=DEFAULT_FTP_PORT)
    p_ftp.add_argument("--user", default=DEFAULT_FTP_USER)
    p_ftp.add_argument("--password", default=DEFAULT_FTP_PASS)
    
    # Compare protocols
    sub.add_parser("compare", help="Compare SSH/SFTP vs FTP")
    
    # Run all demos
    sub.add_parser("demo", help="Run all demonstrations")
    
    return parser.parse_args(argv)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main(argv: list[str]) -> int:
    """Main entry point."""
    args = parse_args(argv)
    
    if args.cmd == "ssh":
        demo_ssh(args.host, args.port, args.user, args.password)
        return 0
    
    if args.cmd == "ftp":
        demo_ftp(args.host, args.port, args.user, args.password)
        return 0
    
    if args.cmd == "compare":
        compare_protocols()
        return 0
    
    if args.cmd == "demo":
        compare_protocols()
        demo_ssh(DEFAULT_SSH_HOST, DEFAULT_SSH_PORT, DEFAULT_SSH_USER, DEFAULT_SSH_PASS)
        demo_ftp(DEFAULT_FTP_HOST, DEFAULT_FTP_PORT, DEFAULT_FTP_USER, DEFAULT_FTP_PASS)
        return 0
    
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
