#!/usr/bin/env python3
"""
Week 10 - FTP Client Demo
NETWORKING class - ASE, Informatics | by Revolvix

Demonstrates FTP connection using Python ftplib.
"""

from __future__ import annotations

import sys
import argparse
from ftplib import FTP


def main() -> int:
    parser = argparse.ArgumentParser(description="FTP Client Demo")
    parser.add_argument("--host", default="127.0.0.1", help="FTP server host")
    parser.add_argument("--port", type=int, default=2121, help="FTP server port")
    parser.add_argument("--user", default="labftp", help="Username")
    parser.add_argument("--password", default="labftp", help="Password")
    args = parser.parse_args()

    print("[INFO] Week 10 FTP Client Demo")
    print(f"[INFO] Connecting to {args.host}:{args.port} as {args.user}")

    try:
        ftp = FTP()
        ftp.connect(args.host, args.port, timeout=10)
        ftp.login(args.user, args.password)
        
        print(f"[OK] Connected successfully")
        print(f"[BANNER] {ftp.getwelcome()}")
        print()

        # List directory
        print("[CMD] LIST")
        files = []
        ftp.retrlines("LIST", files.append)
        
        if files:
            print("[DIR] Directory listing:")
            for f in files:
                print(f"      {f}")
        else:
            print("[DIR] Empty directory")

        # Get current directory
        print()
        print(f"[PWD] Current directory: {ftp.pwd()}")

        # System info
        try:
            print(f"[SYS] {ftp.sendcmd('SYST')}")
        except Exception:
            pass

        ftp.quit()
        print()
        print("[OK] FTP demo completed successfully")
        return 0

    except Exception as e:
        print(f"[ERROR] FTP error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
