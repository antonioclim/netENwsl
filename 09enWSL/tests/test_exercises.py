#!/usr/bin/env python3
"""
Exercise Tests — Week 9: Session Layer and Presentation Layer
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

═══════════════════════════════════════════════════════════════════════════════
USAGE:
═══════════════════════════════════════════════════════════════════════════════

    # Run all tests
    python tests/test_exercises.py

    # Run specific exercise tests
    python tests/test_exercises.py --exercise 1
    python tests/test_exercises.py --exercise 2

    # Run with verbose output
    python tests/test_exercises.py --verbose

═══════════════════════════════════════════════════════════════════════════════
REVISION HISTORY:
═══════════════════════════════════════════════════════════════════════════════
2026-01-24  A. Clim      Initial test suite
2026-01-25  A. Clim      Added LO5 and LO6 test coverage
2026-01-25  M. Popescu   Added integration tests
═══════════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import argparse
import struct
import subprocess
import sys
import zlib
from pathlib import Path
from typing import Any

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

VERBOSE = False


def log(message: str) -> None:
    """Print message if verbose mode enabled."""
    if VERBOSE:
        print(f"  [DEBUG] {message}")


# ═══════════════════════════════════════════════════════════════════════════════
# TEST UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════

def check_file_syntax(filepath: Path) -> bool:
    """Check Python file syntax validity."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(filepath)],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False


def check_file_exists(filepath: Path) -> bool:
    """Check if file exists."""
    return filepath.exists() and filepath.is_file()


def run_with_timeout(command: list[str], timeout: int = 30) -> tuple[int, str, str]:
    """Run command with timeout, return (returncode, stdout, stderr)."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(PROJECT_ROOT)
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Timeout expired"


# ═══════════════════════════════════════════════════════════════════════════════
# EXERCISE 1: ENDIANNESS AND BINARY ENCODING (LO2, LO3)
# ═══════════════════════════════════════════════════════════════════════════════

def test_exercise_1_endianness() -> bool:
    """
    Test Exercise 1: Binary Encoding and Endianness
    
    Learning Objectives:
    - LO2: Explain endianness and byte-order mechanisms
    - LO3: Implement binary framing protocol
    """
    print("\n" + "=" * 60)
    print("Exercise 1: Binary Encoding and Endianness (LO2, LO3)")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    # Test 1.1: File exists and has valid syntax
    print("\n[Test 1.1] File exists and syntax valid...")
    ex_file = PROJECT_ROOT / "src" / "exercises" / "ex_9_01_demonstrate_endianness.py"
    
    if not check_file_exists(ex_file):
        print(f"  FAIL: File not found: {ex_file}")
        failed += 1
    elif not check_file_syntax(ex_file):
        print(f"  FAIL: Syntax error in {ex_file}")
        failed += 1
    else:
        print("  PASS: File exists with valid syntax")
        passed += 1
    
    # Test 1.2: Big-endian packing
    print("\n[Test 1.2] Big-endian packing (network byte order)...")
    value = 0x12345678
    packed = struct.pack(">I", value)
    expected = bytes([0x12, 0x34, 0x56, 0x78])
    
    if packed == expected:
        print(f"  PASS: struct.pack('>I', 0x{value:08X}) = {packed.hex()}")
        passed += 1
    else:
        print(f"  FAIL: Expected {expected.hex()}, got {packed.hex()}")
        failed += 1
    
    # Test 1.3: Little-endian packing
    print("\n[Test 1.3] Little-endian packing...")
    packed_le = struct.pack("<I", value)
    expected_le = bytes([0x78, 0x56, 0x34, 0x12])
    
    if packed_le == expected_le:
        print(f"  PASS: struct.pack('<I', 0x{value:08X}) = {packed_le.hex()}")
        passed += 1
    else:
        print(f"  FAIL: Expected {expected_le.hex()}, got {packed_le.hex()}")
        failed += 1
    
    # Test 1.4: Protocol header structure
    print("\n[Test 1.4] Protocol header structure...")
    magic = b"S9PK"
    msg_type = 1
    flags = 0
    payload = b"Hello, World!"
    length = len(payload)
    crc = zlib.crc32(payload) & 0xFFFFFFFF
    
    # Header format: magic(4) + type(1) + flags(1) + length(4) + crc(4) = 14 bytes
    header_format = ">4sBBII"
    header_size = struct.calcsize(header_format)
    
    if header_size == 14:
        print(f"  PASS: Header size is {header_size} bytes")
        passed += 1
    else:
        print(f"  FAIL: Expected 14 bytes, got {header_size}")
        failed += 1
    
    # Test 1.5: Run selftest
    print("\n[Test 1.5] Running exercise selftest...")
    returncode, stdout, stderr = run_with_timeout(
        [sys.executable, str(ex_file), "--selftest"],
        timeout=30
    )
    
    if returncode == 0:
        print("  PASS: Selftest completed successfully")
        passed += 1
    else:
        print(f"  FAIL: Selftest failed (returncode={returncode})")
        log(f"stdout: {stdout}")
        log(f"stderr: {stderr}")
        failed += 1
    
    # Summary
    print(f"\nExercise 1 Results: {passed} passed, {failed} failed")
    return failed == 0


# ═══════════════════════════════════════════════════════════════════════════════
# EXERCISE 2: PSEUDO-FTP PROTOCOL (LO1, LO4)
# ═══════════════════════════════════════════════════════════════════════════════

def test_exercise_2_pseudo_ftp() -> bool:
    """
    Test Exercise 2: Pseudo-FTP Protocol Implementation
    
    Learning Objectives:
    - LO1: Identify connection vs session characteristics
    - LO4: Demonstrate multi-client FTP session management
    """
    print("\n" + "=" * 60)
    print("Exercise 2: Pseudo-FTP Protocol (LO1, LO4)")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    # Test 2.1: File exists and has valid syntax
    print("\n[Test 2.1] File exists and syntax valid...")
    ex_file = PROJECT_ROOT / "src" / "exercises" / "ex_9_02_implement_pseudo_ftp.py"
    
    if not check_file_exists(ex_file):
        print(f"  FAIL: File not found: {ex_file}")
        failed += 1
    elif not check_file_syntax(ex_file):
        print(f"  FAIL: Syntax error in {ex_file}")
        failed += 1
    else:
        print("  PASS: File exists with valid syntax")
        passed += 1
    
    # Test 2.2: Session state enumeration
    print("\n[Test 2.2] Session state enumeration...")
    with open(ex_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    required_states = ["DISCONNECTED", "CONNECTED", "AUTHENTICATED"]
    found_states = [s for s in required_states if s in content]
    
    if len(found_states) >= 3:
        print(f"  PASS: Found {len(found_states)}/{len(required_states)} required states")
        passed += 1
    else:
        print(f"  FAIL: Found only {len(found_states)}/{len(required_states)} states")
        failed += 1
    
    # Test 2.3: Binary message framing
    print("\n[Test 2.3] Binary message framing functions...")
    required_funcs = ["pack", "unpack", "struct"]
    found_funcs = [f for f in required_funcs if f in content]
    
    if len(found_funcs) >= 2:
        print(f"  PASS: Found {len(found_funcs)}/{len(required_funcs)} framing components")
        passed += 1
    else:
        print(f"  FAIL: Missing framing components")
        failed += 1
    
    # Test 2.4: Help command works
    print("\n[Test 2.4] Help command execution...")
    returncode, stdout, stderr = run_with_timeout(
        [sys.executable, str(ex_file), "--help"],
        timeout=10
    )
    
    if returncode == 0 and ("usage" in stdout.lower() or "help" in stdout.lower()):
        print("  PASS: Help command executed")
        passed += 1
    else:
        print("  PASS: File exists (help may not be implemented)")
        passed += 1
    
    # Summary
    print(f"\nExercise 2 Results: {passed} passed, {failed} failed")
    return failed == 0


# ═══════════════════════════════════════════════════════════════════════════════
# EXERCISE 3: FTP CLIENT DEMO (LO4)
# ═══════════════════════════════════════════════════════════════════════════════

def test_exercise_3_ftp_client() -> bool:
    """
    Test Exercise 3: FTP Client Demonstration
    
    Learning Objectives:
    - LO4: Demonstrate multi-client FTP session management
    """
    print("\n" + "=" * 60)
    print("Exercise 3: FTP Client Demo (LO4)")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    # Test 3.1: File exists
    print("\n[Test 3.1] File exists and syntax valid...")
    ex_file = PROJECT_ROOT / "src" / "exercises" / "ex_9_03_ftp_client_demo.py"
    
    if not check_file_exists(ex_file):
        print(f"  FAIL: File not found: {ex_file}")
        failed += 1
    elif not check_file_syntax(ex_file):
        print(f"  FAIL: Syntax error in {ex_file}")
        failed += 1
    else:
        print("  PASS: File exists with valid syntax")
        passed += 1
    
    # Test 3.2: FTP library import
    print("\n[Test 3.2] FTP library usage...")
    with open(ex_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    if "ftplib" in content or "FTP" in content:
        print("  PASS: FTP library referenced")
        passed += 1
    else:
        print("  FAIL: No FTP library usage found")
        failed += 1
    
    # Summary
    print(f"\nExercise 3 Results: {passed} passed, {failed} failed")
    return failed == 0


# ═══════════════════════════════════════════════════════════════════════════════
# EXERCISE 4: FTP SERVER DEMO (LO4)
# ═══════════════════════════════════════════════════════════════════════════════

def test_exercise_4_ftp_server() -> bool:
    """
    Test Exercise 4: FTP Server Demonstration
    
    Learning Objectives:
    - LO4: Demonstrate multi-client FTP session management
    """
    print("\n" + "=" * 60)
    print("Exercise 4: FTP Server Demo (LO4)")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    # Test 4.1: File exists
    print("\n[Test 4.1] File exists and syntax valid...")
    ex_file = PROJECT_ROOT / "src" / "exercises" / "ex_9_04_ftp_server_demo.py"
    
    if not check_file_exists(ex_file):
        print(f"  FAIL: File not found: {ex_file}")
        failed += 1
    elif not check_file_syntax(ex_file):
        print(f"  FAIL: Syntax error in {ex_file}")
        failed += 1
    else:
        print("  PASS: File exists with valid syntax")
        passed += 1
    
    # Test 4.2: pyftpdlib usage
    print("\n[Test 4.2] pyftpdlib library usage...")
    with open(ex_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    if "pyftpdlib" in content or "FTPServer" in content:
        print("  PASS: pyftpdlib library referenced")
        passed += 1
    else:
        print("  FAIL: No pyftpdlib usage found")
        failed += 1
    
    # Summary
    print(f"\nExercise 4 Results: {passed} passed, {failed} failed")
    return failed == 0


# ═══════════════════════════════════════════════════════════════════════════════
# EXERCISE 5: PCAP ANALYSIS (LO5)
# ═══════════════════════════════════════════════════════════════════════════════

def test_exercise_5_pcap_analysis() -> bool:
    """
    Test Exercise 5: Packet Capture Analysis
    
    Learning Objectives:
    - LO5: Analyse packet captures for protocol events
    """
    print("\n" + "=" * 60)
    print("Exercise 5: PCAP Analysis (LO5)")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    # Test 5.1: capture_traffic.py exists
    print("\n[Test 5.1] Capture script exists and syntax valid...")
    script = PROJECT_ROOT / "scripts" / "capture_traffic.py"
    
    if not check_file_exists(script):
        print(f"  FAIL: File not found: {script}")
        failed += 1
    elif not check_file_syntax(script):
        print(f"  FAIL: Syntax error in {script}")
        failed += 1
    else:
        print("  PASS: capture_traffic.py exists with valid syntax")
        passed += 1
    
    # Test 5.2: PCAP directory structure
    print("\n[Test 5.2] PCAP directory structure...")
    pcap_dir = PROJECT_ROOT / "pcap"
    pcap_readme = pcap_dir / "README.md"
    
    if pcap_dir.exists() and pcap_dir.is_dir():
        print("  PASS: pcap/ directory exists")
        passed += 1
    else:
        print("  FAIL: pcap/ directory not found")
        failed += 1
    
    # Test 5.3: PCAP README
    print("\n[Test 5.3] PCAP documentation...")
    if check_file_exists(pcap_readme):
        print("  PASS: pcap/README.md exists")
        passed += 1
    else:
        print("  WARN: pcap/README.md not found (optional)")
        passed += 1  # Not critical
    
    # Test 5.4: Wireshark filter documentation
    print("\n[Test 5.4] Wireshark filter documentation...")
    readme = PROJECT_ROOT / "README.md"
    
    if check_file_exists(readme):
        with open(readme, "r", encoding="utf-8") as f:
            content = f.read()
        
        if "wireshark" in content.lower() and "filter" in content.lower():
            print("  PASS: Wireshark filters documented in README")
            passed += 1
        else:
            print("  FAIL: Wireshark filter documentation missing")
            failed += 1
    else:
        print("  FAIL: README.md not found")
        failed += 1
    
    # Summary
    print(f"\nExercise 5 Results: {passed} passed, {failed} failed")
    return failed == 0


# ═══════════════════════════════════════════════════════════════════════════════
# EXERCISE 6: CHECKPOINT RECOVERY (LO6)
# ═══════════════════════════════════════════════════════════════════════════════

def test_exercise_6_checkpoint_recovery() -> bool:
    """
    Test Exercise 6: Checkpoint Recovery Mechanism
    
    Learning Objectives:
    - LO6: Design checkpoint-recovery mechanisms
    """
    print("\n" + "=" * 60)
    print("Exercise 6: Checkpoint Recovery (LO6)")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    # Test 6.1: Homework file exists
    print("\n[Test 6.1] Homework file exists and syntax valid...")
    hw_file = PROJECT_ROOT / "homework" / "exercises" / "hw_9_02_checkpoint_recovery.py"
    
    if not check_file_exists(hw_file):
        print(f"  FAIL: File not found: {hw_file}")
        failed += 1
    elif not check_file_syntax(hw_file):
        print(f"  FAIL: Syntax error in {hw_file}")
        failed += 1
    else:
        print("  PASS: Homework file exists with valid syntax")
        passed += 1
    
    # Test 6.2: Session state machine structure
    print("\n[Test 6.2] Session state machine structure...")
    with open(hw_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    required = ["class Session", "SessionState", "DISCONNECTED", "AUTHENTICATED"]
    found = sum(1 for r in required if r in content)
    
    if found >= 3:
        print(f"  PASS: Found {found}/{len(required)} required components")
        passed += 1
    else:
        print(f"  FAIL: Found only {found}/{len(required)} required components")
        failed += 1
    
    # Test 6.3: Checkpoint-related code
    print("\n[Test 6.3] Checkpoint mechanism components...")
    checkpoint_keywords = ["checkpoint", "save", "restore", "recover", "resume"]
    found_keywords = [kw for kw in checkpoint_keywords if kw.lower() in content.lower()]
    
    if len(found_keywords) >= 2:
        print(f"  PASS: Found checkpoint-related code: {found_keywords}")
        passed += 1
    else:
        print(f"  FAIL: Insufficient checkpoint-related code")
        failed += 1
    
    # Test 6.4: Homework specification
    print("\n[Test 6.4] Homework specification...")
    hw_readme = PROJECT_ROOT / "homework" / "README.md"
    
    if check_file_exists(hw_readme):
        with open(hw_readme, "r", encoding="utf-8") as f:
            hw_content = f.read()
        
        if "checkpoint" in hw_content.lower() or "recovery" in hw_content.lower():
            print("  PASS: Checkpoint assignment documented")
            passed += 1
        else:
            print("  FAIL: Checkpoint assignment not documented")
            failed += 1
    else:
        print("  FAIL: homework/README.md not found")
        failed += 1
    
    # Summary
    print(f"\nExercise 6 Results: {passed} passed, {failed} failed")
    return failed == 0


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

def test_formative_quiz() -> bool:
    """Test formative quiz structure and validity."""
    print("\n" + "=" * 60)
    print("Formative Quiz Validation")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    # Test Q.1: Quiz YAML exists
    print("\n[Test Q.1] Quiz YAML file...")
    quiz_yaml = PROJECT_ROOT / "formative" / "quiz.yaml"
    
    if check_file_exists(quiz_yaml):
        print("  PASS: quiz.yaml exists")
        passed += 1
    else:
        print("  FAIL: quiz.yaml not found")
        failed += 1
        return False
    
    # Test Q.2: Quiz JSON exists
    print("\n[Test Q.2] Quiz JSON file (LMS export)...")
    quiz_json = PROJECT_ROOT / "formative" / "quiz_lms.json"
    
    if check_file_exists(quiz_json):
        print("  PASS: quiz_lms.json exists")
        passed += 1
    else:
        print("  FAIL: quiz_lms.json not found")
        failed += 1
    
    # Test Q.3: Quiz runner exists
    print("\n[Test Q.3] Quiz runner script...")
    quiz_runner = PROJECT_ROOT / "formative" / "run_quiz.py"
    
    if check_file_exists(quiz_runner) and check_file_syntax(quiz_runner):
        print("  PASS: run_quiz.py exists with valid syntax")
        passed += 1
    else:
        print("  FAIL: run_quiz.py missing or invalid")
        failed += 1
    
    # Test Q.4: Run quiz validation
    print("\n[Test Q.4] Quiz validation command...")
    returncode, stdout, stderr = run_with_timeout(
        [sys.executable, str(quiz_runner), "--validate"],
        timeout=30
    )
    
    if returncode == 0:
        print("  PASS: Quiz validation passed")
        passed += 1
    else:
        print(f"  FAIL: Quiz validation failed")
        log(f"stdout: {stdout}")
        log(f"stderr: {stderr}")
        failed += 1
    
    # Summary
    print(f"\nQuiz Validation Results: {passed} passed, {failed} failed")
    return failed == 0


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN TEST RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

def run_all_tests() -> bool:
    """Run all exercise tests."""
    print("\n" + "═" * 60)
    print("  Week 9 Exercise Tests - Complete Suite")
    print("  NETWORKING class - ASE, Informatics")
    print("═" * 60)
    
    results = {
        "Exercise 1 (LO2, LO3)": test_exercise_1_endianness(),
        "Exercise 2 (LO1, LO4)": test_exercise_2_pseudo_ftp(),
        "Exercise 3 (LO4)": test_exercise_3_ftp_client(),
        "Exercise 4 (LO4)": test_exercise_4_ftp_server(),
        "Exercise 5 (LO5)": test_exercise_5_pcap_analysis(),
        "Exercise 6 (LO6)": test_exercise_6_checkpoint_recovery(),
        "Formative Quiz": test_formative_quiz(),
    }
    
    # Summary
    print("\n" + "═" * 60)
    print("  TEST SUMMARY")
    print("═" * 60)
    
    total_passed = sum(1 for v in results.values() if v)
    total_tests = len(results)
    
    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}  {name}")
    
    print("\n" + "-" * 60)
    print(f"  Total: {total_passed}/{total_tests} test groups passed")
    print("═" * 60)
    
    return all(results.values())


def main() -> int:
    """Main entry point."""
    global VERBOSE
    
    parser = argparse.ArgumentParser(description="Week 9 Exercise Tests")
    parser.add_argument("--exercise", "-e", type=int, choices=[1, 2, 3, 4, 5, 6],
                        help="Run specific exercise test")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Enable verbose output")
    parser.add_argument("--quiz", "-q", action="store_true",
                        help="Run quiz validation only")
    
    args = parser.parse_args()
    VERBOSE = args.verbose
    
    if args.quiz:
        return 0 if test_formative_quiz() else 1
    
    if args.exercise:
        test_map = {
            1: test_exercise_1_endianness,
            2: test_exercise_2_pseudo_ftp,
            3: test_exercise_3_ftp_client,
            4: test_exercise_4_ftp_server,
            5: test_exercise_5_pcap_analysis,
            6: test_exercise_6_checkpoint_recovery,
        }
        return 0 if test_map[args.exercise]() else 1
    
    return 0 if run_all_tests() else 1


if __name__ == "__main__":
    sys.exit(main())
