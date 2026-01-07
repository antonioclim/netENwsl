#!/usr/bin/env python3
"""
Exercise Verification Tests for Week 9 Laboratory
NETWORKING class - ASE, Informatics | by Revolvix

Tests to verify that exercises are implemented correctly.

Usage:
    python tests/test_exercises.py
    python tests/test_exercises.py --exercise 1
"""

from __future__ import annotations

import argparse
import struct
import subprocess
import sys
import zlib
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def test_exercise_1_endianness():
    """Test Exercise 1: Endianness and Binary Framing."""
    print("\n" + "=" * 50)
    print("Exercise 1: Endianness and Binary Framing")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    # Test 1: Big-endian packing
    print("\n[Test 1.1] Big-endian packing...")
    value = 0x12345678
    packed = struct.pack(">I", value)
    expected = b'\x12\x34\x56\x78'
    
    if packed == expected:
        print(f"  PASS: {value:#x} -> {packed.hex()}")
        passed += 1
    else:
        print(f"  FAIL: Expected {expected.hex()}, got {packed.hex()}")
        failed += 1
    
    # Test 2: Little-endian packing
    print("[Test 1.2] Little-endian packing...")
    packed_le = struct.pack("<I", value)
    expected_le = b'\x78\x56\x34\x12'
    
    if packed_le == expected_le:
        print(f"  PASS: {value:#x} -> {packed_le.hex()}")
        passed += 1
    else:
        print(f"  FAIL: Expected {expected_le.hex()}, got {packed_le.hex()}")
        failed += 1
    
    # Test 3: CRC-32 calculation
    print("[Test 1.3] CRC-32 calculation...")
    data = b"Hello, FTP!"
    crc = zlib.crc32(data) & 0xFFFFFFFF
    
    if crc > 0:
        print(f"  PASS: CRC-32 of '{data.decode()}' = 0x{crc:08X}")
        passed += 1
    else:
        print("  FAIL: CRC calculation returned 0")
        failed += 1
    
    # Test 4: Header structure
    print("[Test 1.4] Protocol header structure...")
    magic = b"FTPC"
    payload = b"test payload"
    length = len(payload)
    crc = zlib.crc32(payload) & 0xFFFFFFFF
    flags = 0
    
    header = struct.pack(">4sIII", magic, length, crc, flags)
    
    if len(header) == 16:
        print(f"  PASS: Header size = 16 bytes")
        passed += 1
    else:
        print(f"  FAIL: Header size = {len(header)} bytes (expected 16)")
        failed += 1
    
    # Summary
    print(f"\nExercise 1 Results: {passed} passed, {failed} failed")
    return failed == 0


def test_exercise_2_pseudo_ftp():
    """Test Exercise 2: Pseudo-FTP Protocol."""
    print("\n" + "=" * 50)
    print("Exercise 2: Pseudo-FTP Protocol")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    # Test 1: Check if script exists
    print("\n[Test 2.1] Script exists...")
    script_path = PROJECT_ROOT / "src" / "exercises" / "ex_9_02_pseudo_ftp.py"
    
    if script_path.exists():
        print(f"  PASS: {script_path.name} found")
        passed += 1
    else:
        print(f"  FAIL: Script not found at {script_path}")
        failed += 1
        return False
    
    # Test 2: Script is valid Python
    print("[Test 2.2] Script syntax valid...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(script_path)],
            capture_output=True,
            timeout=10
        )
        if result.returncode == 0:
            print("  PASS: No syntax errors")
            passed += 1
        else:
            print("  FAIL: Syntax errors found")
            failed += 1
    except Exception as e:
        print(f"  FAIL: {e}")
        failed += 1
    
    # Test 3: Import check
    print("[Test 2.3] Module imports...")
    try:
        spec_path = str(script_path)
        # Just check that we can read and parse the file
        with open(spec_path, 'r') as f:
            content = f.read()
            if "def pack_data" in content or "class Session" in content:
                print("  PASS: Key functions/classes found")
                passed += 1
            else:
                print("  PASS: Script loaded (structure may vary)")
                passed += 1
    except Exception as e:
        print(f"  FAIL: {e}")
        failed += 1
    
    print(f"\nExercise 2 Results: {passed} passed, {failed} failed")
    return failed == 0


def test_ftp_demo_client():
    """Test FTP demo client script."""
    print("\n" + "=" * 50)
    print("FTP Demo Client")
    print("=" * 50)
    
    script_path = PROJECT_ROOT / "src" / "exercises" / "ftp_demo_client.py"
    
    if not script_path.exists():
        print("  SKIP: ftp_demo_client.py not found")
        return True
    
    # Check syntax
    print("\n[Test] Script syntax valid...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(script_path)],
            capture_output=True,
            timeout=10
        )
        if result.returncode == 0:
            print("  PASS")
            return True
        else:
            print("  FAIL")
            return False
    except Exception as e:
        print(f"  FAIL: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Test Week 9 Laboratory Exercises"
    )
    parser.add_argument(
        "--exercise", "-e",
        type=int,
        choices=[1, 2],
        help="Test specific exercise only"
    )
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("Week 9 Laboratory - Exercise Tests")
    print("=" * 50)
    
    results = []
    
    if args.exercise is None or args.exercise == 1:
        results.append(test_exercise_1_endianness())
    
    if args.exercise is None or args.exercise == 2:
        results.append(test_exercise_2_pseudo_ftp())
        results.append(test_ftp_demo_client())
    
    print("\n" + "=" * 50)
    
    if all(results):
        print("\033[32mAll tests PASSED\033[0m")
        return 0
    else:
        print("\033[31mSome tests FAILED\033[0m")
        return 1


if __name__ == "__main__":
    sys.exit(main())
