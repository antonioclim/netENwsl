#!/usr/bin/env python3
"""Week 10 - SSH client using Paramiko.

Demonstrates programmatic SSH access to the lab SSH server.

NETWORKING class - ASE, Informatics | by Revolvix
"""

from __future__ import annotations

import sys
import time
import paramiko


def main() -> int:
    host = "ssh-server"
    port = 22
    username = "labuser"
    password = "labpass"

    print("[INFO] Week 10 Paramiko SSH Client")
    print(f"[INFO] Connecting to {host}:{port} as {username}")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(
            hostname=host,
            port=port,
            username=username,
            password=password,
            timeout=10,
        )
        print("[OK] Connected successfully")

        # Execute commands
        commands = [
            "hostname",
            "whoami",
            "uname -a",
            "date",
        ]

        for cmd in commands:
            print(f"\n[CMD] {cmd}")
            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.read().decode().strip()
            errors = stderr.read().decode().strip()
            
            if output:
                print(f"  {output}")
            if errors:
                print(f"  [ERR] {errors}")

        print("\n[OK] All commands executed successfully")
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


if __name__ == "__main__":
    sys.exit(main())
