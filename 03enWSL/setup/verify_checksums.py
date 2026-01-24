#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  Checksum Verification — Week 3 Network Programming                          ║
║  NETWORKING class - ASE, CSIE | by ing. dr. Antonio Clim                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

DESCRIPTION:
    Verifies integrity of critical files using SHA-256 checksums.
    Ensures that key educational materials have not been corrupted or
    accidentally modified.

USAGE:
    python setup/verify_checksums.py              # Verify all checksums
    python setup/verify_checksums.py --generate   # Generate new checksums
    python setup/verify_checksums.py --verbose    # Show all files checked
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path


# Files to verify (relative to project root)
CRITICAL_FILES = [
    "formative/quiz.yaml",
    "formative/run_quiz.py",
    "formative/quiz.schema.json",
    "src/exercises/ex_3_01_udp_broadcast.py",
    "src/exercises/ex_3_02_udp_multicast.py",
    "src/exercises/ex_3_03_tcp_tunnel.py",
    "tests/smoke_test.py",
    "docs/learning_objectives_matrix.md",
    "docs/misconceptions.md",
]

CHECKSUMS_FILE = ".checksums.sha256"


class Colours:
    """ANSI colour codes."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def compute_sha256(filepath: Path) -> str:
    """
    Compute SHA-256 hash of a file.
    
    Args:
        filepath: Path to the file
        
    Returns:
        Hexadecimal SHA-256 hash string
    """
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


def find_project_root() -> Path:
    """Find the project root directory."""
    current = Path(__file__).resolve().parent
    
    # Look for project markers
    while current != current.parent:
        if (current / "Makefile").exists() or (current / "README.md").exists():
            return current
        current = current.parent
    
    # Fallback to parent of setup/
    return Path(__file__).resolve().parent.parent


def generate_checksums(root: Path, output_file: Path, verbose: bool = False) -> int:
    """
    Generate checksums for critical files.
    
    Args:
        root: Project root directory
        output_file: Path to write checksums file
        verbose: Whether to print progress
        
    Returns:
        Exit code (0 for success)
    """
    print(f"{Colours.CYAN}Generating checksums...{Colours.RESET}")
    
    checksums = []
    for filepath_str in CRITICAL_FILES:
        filepath = root / filepath_str
        if filepath.exists():
            checksum = compute_sha256(filepath)
            checksums.append(f"{checksum}  {filepath_str}")
            if verbose:
                print(f"  {Colours.GREEN}✓{Colours.RESET} {filepath_str}")
        else:
            print(f"  {Colours.YELLOW}⚠{Colours.RESET} Skipped (not found): {filepath_str}")
    
    output_file.write_text("\n".join(checksums) + "\n", encoding="utf-8")
    print(f"\n{Colours.GREEN}✓ Checksums written to: {output_file}{Colours.RESET}")
    print(f"  Files checksummed: {len(checksums)}")
    
    return 0


def verify_checksums(root: Path, checksums_file: Path, verbose: bool = False) -> int:
    """
    Verify checksums against stored values.
    
    Args:
        root: Project root directory
        checksums_file: Path to checksums file
        verbose: Whether to print all files
        
    Returns:
        Exit code (0 for all valid, 1 for failures)
    """
    if not checksums_file.exists():
        print(f"{Colours.YELLOW}⚠ Checksums file not found: {checksums_file}{Colours.RESET}")
        print("  Run with --generate to create checksums file")
        return 1
    
    print(f"{Colours.CYAN}Verifying checksums...{Colours.RESET}")
    
    # Parse checksums file
    stored_checksums = {}
    for line in checksums_file.read_text(encoding="utf-8").strip().split("\n"):
        if line and "  " in line:
            checksum, filepath = line.split("  ", 1)
            stored_checksums[filepath] = checksum
    
    # Verify each file
    failures = []
    successes = 0
    
    for filepath_str, expected_checksum in stored_checksums.items():
        filepath = root / filepath_str
        
        if not filepath.exists():
            print(f"  {Colours.RED}✗{Colours.RESET} Missing: {filepath_str}")
            failures.append(filepath_str)
            continue
        
        actual_checksum = compute_sha256(filepath)
        
        if actual_checksum == expected_checksum:
            successes += 1
            if verbose:
                print(f"  {Colours.GREEN}✓{Colours.RESET} {filepath_str}")
        else:
            print(f"  {Colours.RED}✗{Colours.RESET} Modified: {filepath_str}")
            failures.append(filepath_str)
    
    # Summary
    print()
    if failures:
        print(f"{Colours.RED}✗ Verification FAILED{Colours.RESET}")
        print(f"  Valid: {successes}, Failed: {len(failures)}")
        print(f"\n  Failed files:")
        for f in failures:
            print(f"    - {f}")
        return 1
    else:
        print(f"{Colours.GREEN}✓ All checksums valid{Colours.RESET}")
        print(f"  Files verified: {successes}")
        return 0


def main(argv: list[str] | None = None) -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Verify or generate SHA-256 checksums for critical files"
    )
    parser.add_argument(
        "--generate", "-g",
        action="store_true",
        help="Generate new checksums file"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show all files being processed"
    )
    parser.add_argument(
        "--checksums-file", "-f",
        type=Path,
        help=f"Checksums file path (default: {CHECKSUMS_FILE})"
    )
    
    args = parser.parse_args(argv)
    
    root = find_project_root()
    checksums_file = args.checksums_file or (root / CHECKSUMS_FILE)
    
    if args.generate:
        return generate_checksums(root, checksums_file, args.verbose)
    else:
        return verify_checksums(root, checksums_file, args.verbose)


if __name__ == "__main__":
    sys.exit(main())
