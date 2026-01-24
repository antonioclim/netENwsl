#!/usr/bin/env python3
"""
Session Token Generator — Week 6: NAT/PAT & SDN
================================================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

Generates a unique session token for the laboratory session.
This token MUST be included in all submissions to prove authenticity.

The token is based on:
- Your username
- Current timestamp
- Machine hostname

This makes each token unique and impossible to predict or generate by AI.

Usage:
    python scripts/generate_session_token.py
    python scripts/generate_session_token.py --username "FirstnameLastname"
    python scripts/generate_session_token.py --save

Contact: Issues: Open an issue in GitHub
"""

from __future__ import annotations

import argparse
import hashlib
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

VERSION = "1.0.0"
WEEK_NUMBER = 6


# ═══════════════════════════════════════════════════════════════════════════════
# TOKEN GENERATION
# ═══════════════════════════════════════════════════════════════════════════════

def generate_token(username: Optional[str] = None) -> str:
    """
    Generate unique session token.
    
    Args:
        username: Optional username override. If None, uses system username.
        
    Returns:
        Unique token string in format: W6-{HASH}-{TIMESTAMP}
    """
    if username is None:
        username = os.environ.get("USER", os.environ.get("USERNAME", "student"))
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    
    try:
        hostname = os.uname().nodename[:8]
    except AttributeError:
        # Windows compatibility
        import socket
        hostname = socket.gethostname()[:8]
    
    # Create deterministic but unique token
    seed = f"{username}_{timestamp}_{hostname}_{os.getpid()}"
    token_hash = hashlib.sha256(seed.encode()).hexdigest()[:12].upper()
    
    return f"W{WEEK_NUMBER}-{token_hash}-{timestamp}"


def get_token_info(token: str) -> dict:
    """
    Parse token to extract information.
    
    Args:
        token: Token string to parse
        
    Returns:
        Dictionary with token components
    """
    parts = token.split("-")
    if len(parts) >= 3:
        date_time = parts[2] if len(parts) > 2 else ""
        return {
            "week": parts[0],
            "hash": parts[1],
            "date": date_time.split("_")[0] if "_" in date_time else date_time,
            "time": date_time.split("_")[1] if "_" in date_time else "unknown",
        }
    return {"raw": token}


# ═══════════════════════════════════════════════════════════════════════════════
# TOKEN STORAGE
# ═══════════════════════════════════════════════════════════════════════════════

def save_token(token: str, base_path: Optional[Path] = None) -> Path:
    """
    Save token to artefacts directory.
    
    Args:
        token: Token string to save
        base_path: Optional base path override
        
    Returns:
        Path where token was saved
    """
    if base_path is None:
        base_path = Path(__file__).parent.parent
    
    artefacts_dir = base_path / "artefacts"
    artefacts_dir.mkdir(exist_ok=True)
    
    token_file = artefacts_dir / ".session_token"
    token_file.write_text(f"{token}\n")
    
    return token_file


def load_token(base_path: Optional[Path] = None) -> Optional[str]:
    """
    Load existing token from artefacts directory.
    
    Args:
        base_path: Optional base path override
        
    Returns:
        Token string if found, None otherwise
    """
    if base_path is None:
        base_path = Path(__file__).parent.parent
    
    token_file = base_path / "artefacts" / ".session_token"
    
    if token_file.exists():
        return token_file.read_text().strip()
    return None


# ═══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

def print_banner(token: str, saved_path: Optional[Path] = None) -> None:
    """Print formatted token information."""
    info = get_token_info(token)
    
    print()
    print("═" * 64)
    print("  🔑 SESSION TOKEN GENERATED")
    print("═" * 64)
    print()
    print(f"  Token:     {token}")
    print(f"  Generated: {info.get('date', 'N/A')} at {info.get('time', 'N/A')}")
    print()
    print("  ┌────────────────────────────────────────────────────────────┐")
    print("  │  ⚠️  IMPORTANT: Include this token in ALL submissions:     │")
    print("  │                                                            │")
    print("  │  • Screenshot filenames (e.g., nat_capture_W6-ABC123.png) │")
    print("  │  • PCAP file comments                                      │")
    print("  │  • Homework answer headers                                 │")
    print("  │  • Lab report footer                                       │")
    print("  │                                                            │")
    print("  │  This token proves YOU ran the lab — AI cannot generate   │")
    print("  │  these values because they depend on your specific        │")
    print("  │  system and timestamp.                                     │")
    print("  └────────────────────────────────────────────────────────────┘")
    print()
    
    if saved_path:
        print(f"  Token saved to: {saved_path}")
        print()
    
    print("═" * 64)
    print()


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate unique session token for Week 6 laboratory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python scripts/generate_session_token.py
    python scripts/generate_session_token.py --username "IonPopescu"
    python scripts/generate_session_token.py --save
    python scripts/generate_session_token.py --check

Contact: Issues: Open an issue in GitHub
        """
    )
    parser.add_argument(
        "--username", "-u",
        help="Your name (FirstnameLastname, no spaces)"
    )
    parser.add_argument(
        "--save", "-s",
        action="store_true",
        help="Save token to artefacts/.session_token"
    )
    parser.add_argument(
        "--check", "-c",
        action="store_true",
        help="Check for existing saved token"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Only output the token (for scripting)"
    )
    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"Session Token Generator v{VERSION}"
    )
    
    args = parser.parse_args()
    
    # Check for existing token
    if args.check:
        existing = load_token()
        if existing:
            if args.quiet:
                print(existing)
            else:
                print(f"Existing token found: {existing}")
            return 0
        else:
            if not args.quiet:
                print("No existing token found. Run without --check to generate one.")
            return 1
    
    # Generate new token
    token = generate_token(args.username)
    
    # Save if requested
    saved_path = None
    if args.save:
        saved_path = save_token(token)
    
    # Output
    if args.quiet:
        print(token)
    else:
        print_banner(token, saved_path)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
