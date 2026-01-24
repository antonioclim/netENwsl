#!/usr/bin/env python3
"""
Week 10 - SSH Client Demo
NETWORKING class - ASE, Informatics | by Revolvix

Demonstrates SSH connection using Paramiko library.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# IMPORT_DEPENDENCIES
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations
from typing import Optional, List, Dict, Tuple, Any

import sys
import argparse



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
try:
    import paramiko
except ImportError:
    print("Error: paramiko not installed. Run: pip install paramiko")
    sys.exit(1)




# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    parser = argparse.ArgumentParser(description="SSH Client Demo")
    parser.add_argument("--host", default="127.0.0.1", help="SSH server host")
    parser.add_argument("--port", type=int, default=2222, help="SSH server port")
    parser.add_argument("--user", default="labuser", help="Username")
    parser.add_argument("--password", default="labpass", help="Password")
    parser.add_argument("--command", "-c", default="hostname", help="Command to execute")
    args = parser.parse_args()

    print("[INFO] Week 10 SSH Client Demo")
    print(f"[INFO] Connecting to {args.host}:{args.port} as {args.user}")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(
            hostname=args.host,
            port=args.port,
            username=args.user,
            password=args.password,
            timeout=10,
        )
        print("[OK] Connected successfully")
        print()

        # Execute command
        print(f"[CMD] {args.command}")
        stdin, stdout, stderr = client.exec_command(args.command)
        
        output = stdout.read().decode().strip()
        errors = stderr.read().decode().strip()

        if output:
            print(f"[OUT] {output}")
        if errors:
            print(f"[ERR] {errors}")

        print()
        print("[OK] Command executed successfully")
        return 0

    except paramiko.AuthenticationException:
        print("[ERROR] Authentication failed")
        return 1
    except paramiko.SSHException as e:
        print(f"[ERROR] SSH error: {e}")
        return 1
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        return 1
    finally:
        client.close()




# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    sys.exit(main())
