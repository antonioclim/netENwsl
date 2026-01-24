#!/usr/bin/env python3
"""
PATCH FILE: Beginner Mode Additions for ex_13_01_port_scanner.py

Instructions:
1. Add these lines after 'from __future__ import annotations' (line 39)
2. Add explain() calls in tcp_connect_scan() function

This patch adds Beginner Mode functionality to the port scanner.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# ADD AFTER LINE 39 (after 'from __future__ import annotations')
# ═══════════════════════════════════════════════════════════════════════════════

BEGINNER_MODE_CODE = '''
# ═══════════════════════════════════════════════════════════════════════════════
# BEGINNER MODE CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
# Set WEEK13_BEGINNER_MODE=1 environment variable for step-by-step explanations

import os

BEGINNER_MODE = os.environ.get("WEEK13_BEGINNER_MODE", "").lower() in ("1", "true", "yes")


def explain(message: str) -> None:
    """Print explanation only when beginner mode is enabled."""
    if BEGINNER_MODE:
        print(f"\\n💡 EXPLANATION: {message}\\n")
'''

# ═══════════════════════════════════════════════════════════════════════════════
# MODIFY tcp_connect_scan() FUNCTION - Add explain() calls
# ═══════════════════════════════════════════════════════════════════════════════

TCP_CONNECT_SCAN_ADDITIONS = '''
    # Add after creating socket:
    explain(
        f"Creating a TCP socket to scan port {port}. "
        "SOCK_STREAM means TCP (connection-oriented protocol)."
    )
    
    # Add after settimeout():
    explain(
        f"Setting timeout to {timeout} seconds. If the server does not respond "
        "within this time, we assume the port is 'filtered' (firewall DROP)."
    )
    
    # Add before connect_ex():
    explain(
        "Calling connect_ex() which attempts the TCP three-way handshake: "
        "SYN → SYN-ACK → ACK. It returns 0 for success, error code otherwise."
    )
    
    # Add when result.state = "open":
    explain(
        f"Connection succeeded! Port {port} is OPEN. "
        "This means a service is listening and accepted our connection."
    )
    
    # Add when result.state = "closed":
    explain(
        f"Connection refused. Port {port} is CLOSED. "
        "The host responded with RST, meaning no service is listening."
    )
    
    # Add in except socket.timeout:
    explain(
        f"Timeout! No response within {timeout}s. Port {port} is FILTERED. "
        "This usually means a firewall is silently dropping our packets."
    )
'''

# ═══════════════════════════════════════════════════════════════════════════════
# FIX: Colors vs Colours naming inconsistency (line 99-102)
# ═══════════════════════════════════════════════════════════════════════════════

FIX_COLOURS = '''
# ORIGINAL (incorrect):
# if not sys.stdout.isatty():
#     Colors.RED = Colours.GREEN = Colours.YELLOW = ""
#     Colours.BLUE = Colours.CYAN = Colours.RESET = Colours.BOLD = ""

# CORRECTED:
if not sys.stdout.isatty():
    Colours.RED = Colours.GREEN = Colours.YELLOW = ""
    Colours.BLUE = Colours.CYAN = Colours.RESET = Colours.BOLD = ""
'''

print("PATCH FILE: Add these modifications to ex_13_01_port_scanner.py")
print("See BEGINNER_MODE_CODE, TCP_CONNECT_SCAN_ADDITIONS and FIX_COLOURS above.")
