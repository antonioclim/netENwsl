#!/usr/bin/env python3
"""Session token generator (Week 6).

The session token is a short identifier that students include in submissions.
It is not, by itself, a proof of learning or a proof of execution. For graded work,
pair it with the Week 6 anti-AI artefacts (challenge, evidence and PCAP capture).

Usage
    python scripts/generate_session_token.py
    python scripts/generate_session_token.py --username "FirstnameLastname"
    python scripts/generate_session_token.py --save
    python scripts/generate_session_token.py --check

Output
    W6-<HASH>-<YYYYMMDD_HHMM>

Storage
- Preferred: artifacts/.session_token
- Compatibility: artefacts/.session_token (legacy misspelling)
"""

from __future__ import annotations

import argparse
import hashlib
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


VERSION = "1.1.0"
WEEK_NUMBER = 6


def generate_token(username: Optional[str] = None) -> str:
    """Generate a per-run token.

    The token is derived from:
    - user name
    - local timestamp (minute granularity)
    - hostname fragment
    - process id

    It is intended for traceability rather than cryptographic security.
    """
    if username is None:
        username = os.environ.get("USER", os.environ.get("USERNAME", "student"))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")

    try:
        hostname = os.uname().nodename[:8]
    except AttributeError:
        import socket

        hostname = socket.gethostname()[:8]

    seed = f"{username}_{timestamp}_{hostname}_{os.getpid()}"
    token_hash = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:12].upper()

    return f"W{WEEK_NUMBER}-{token_hash}-{timestamp}"


def get_token_info(token: str) -> dict:
    parts = token.split("-")
    if len(parts) >= 3:
        date_time = parts[2]
        return {
            "week": parts[0],
            "hash": parts[1],
            "date": date_time.split("_")[0] if "_" in date_time else date_time,
            "time": date_time.split("_")[1] if "_" in date_time else "unknown",
        }
    return {"raw": token}


def _preferred_artifacts_dir(base_path: Path) -> Path:
    return base_path / "artifacts"


def _legacy_artefacts_dir(base_path: Path) -> Path:
    return base_path / "artefacts"


def save_token(token: str, base_path: Optional[Path] = None, output: Optional[Path] = None) -> Path:
    """Save token to disk.

    If output is not provided the token is saved to artifacts/.session_token.
    """
    if base_path is None:
        base_path = Path(__file__).parent.parent

    if output is None:
        artifacts_dir = _preferred_artifacts_dir(base_path)
        artifacts_dir.mkdir(exist_ok=True)
        output = artifacts_dir / ".session_token"
    else:
        output.parent.mkdir(parents=True, exist_ok=True)

    output.write_text(f"{token}\n", encoding="utf-8")
    return output


def load_token(base_path: Optional[Path] = None) -> Optional[str]:
    """Load a previously saved token.

    Prefers artifacts/.session_token and falls back to the legacy artefacts path.
    """
    if base_path is None:
        base_path = Path(__file__).parent.parent

    preferred = _preferred_artifacts_dir(base_path) / ".session_token"
    legacy = _legacy_artefacts_dir(base_path) / ".session_token"

    for p in (preferred, legacy):
        if p.exists():
            return p.read_text(encoding="utf-8", errors="replace").strip()
    return None


def print_banner(token: str, saved_path: Optional[Path] = None) -> None:
    info = get_token_info(token)

    print()
    print("=" * 64)
    print("  SESSION TOKEN GENERATED")
    print("=" * 64)
    print()
    print(f"  Token:     {token}")
    print(f"  Generated: {info.get('date', 'N/A')} at {info.get('time', 'N/A')}")
    print()
    print("Include this token in your submission (for example, in a report header)")
    print("and in filenames where appropriate.")
    print()
    if saved_path:
        print(f"Token saved to: {saved_path}")
        print()
    print("=" * 64)
    print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a Week 6 session token",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--username", "-u", help="Name (FirstnameLastname, no spaces)")
    parser.add_argument("--save", "-s", action="store_true", help="Save token to artifacts/.session_token")
    parser.add_argument("--output", help="Optional output path for --save")
    parser.add_argument("--check", "-c", action="store_true", help="Print existing token if available")
    parser.add_argument("--quiet", "-q", action="store_true", help="Only output the token")
    parser.add_argument("--version", "-v", action="version", version=f"Session Token Generator v{VERSION}")

    args = parser.parse_args()

    if args.check:
        existing = load_token()
        if existing:
            print(existing if args.quiet else f"Existing token: {existing}")
            return 0
        if not args.quiet:
            print("No existing token found. Run without --check to generate one.")
        return 1

    token = generate_token(args.username)

    saved_path = None
    if args.save:
        out = Path(args.output) if args.output else None
        saved_path = save_token(token, output=out)

    if args.quiet:
        print(token)
    else:
        print_banner(token, saved_path)

    return 0


if __name__ == "__main__":
    sys.exit(main())
