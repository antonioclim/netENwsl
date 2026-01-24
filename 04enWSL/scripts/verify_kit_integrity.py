#!/usr/bin/env python3
"""
Kit Integrity Verification Script — Week 4
==========================================

NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

This script verifies that all claimed artefacts in the kit actually exist,
ensuring consistency between documentation and actual files. Run this before
any commit to prevent hallucination risks and documentation drift.

Usage:
    python scripts/verify_kit_integrity.py
    make verify-integrity

Exit codes:
    0 - All verifications passed
    1 - One or more verifications failed
"""

import sys
import os
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Set

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

PROJECT_ROOT = Path(__file__).parent.parent

# Required files per Learning Objective
REQUIRED_ARTIFACTS: Dict[str, List[str]] = {
    'LO1': [
        'docs/theory_summary.md',
        'docs/glossary.md',
        'docs/concept_analogies.md',
        'README.md',
    ],
    'LO2': [
        'docs/theory_summary.md',
        'docs/misconceptions.md',
        'docs/peer_instruction.md',
        'docs/code_tracing.md',
    ],
    'LO3': [
        'src/exercises/ex_4_01_tcp_proto.py',
        'src/apps/text_proto_server.py',
        'src/apps/text_proto_client.py',
        'tests/test_exercises.py',
        'docs/misconceptions.md',
        'docs/parsons_problems.md',
        'pcap/week04_lo3_text_commands.pcap',
    ],
    'LO4': [
        'src/exercises/ex_4_02_udp_sensor.py',
        'src/apps/binary_proto_server.py',
        'src/apps/binary_proto_client.py',
        'docs/code_tracing.md',
        'docs/misconceptions.md',
        'docs/parsons_problems.md',
        'pcap/week04_lo4_binary_header.pcap',
    ],
    'LO5': [
        'scripts/capture_traffic.py',
        'pcap/README.md',
        'pcap/week04_lo5_tcp_handshake.pcap',
        'pcap/week04_lo5_udp_sensor.pcap',
        'docs/peer_instruction.md',
    ],
    'LO6': [
        'homework/exercises/hw_4_01_enhanced_binary_protocol.py',
        'homework/exercises/hw_4_02_reliable_udp_transfer.py',
        'docs/misconceptions.md',
        'docs/peer_instruction.md',
    ],
}

# Quiz must cover these LOs
QUIZ_LO_COVERAGE: Dict[str, List[str]] = {
    'LO1': ['q01', 'q02', 'q03'],
    'LO2': ['q04', 'q05', 'q06', 'q07'],
    'LO3': ['q08', 'q12'],
    'LO4': ['q09', 'q10', 'q11'],
    'LO5': ['q13', 'q14'],
    'LO6': ['q15'],
}

# PCAP files with minimum size requirements
PCAP_REQUIREMENTS: Dict[str, int] = {
    'pcap/week04_lo3_text_commands.pcap': 1000,      # min 1KB
    'pcap/week04_lo4_binary_header.pcap': 500,       # min 0.5KB
    'pcap/week04_lo5_tcp_handshake.pcap': 500,       # min 0.5KB
    'pcap/week04_lo5_udp_sensor.pcap': 500,          # min 0.5KB
}

# Essential documentation files
ESSENTIAL_DOCS: List[str] = [
    'README.md',
    'docs/learning_objectives.md',
    'docs/troubleshooting.md',
    'docs/misconceptions.md',
    'docs/theory_summary.md',
    'docs/glossary.md',
    'docs/code_tracing.md',
    'docs/parsons_problems.md',
    'docs/peer_instruction.md',
    'docs/concept_analogies.md',
    'docs/commands_cheatsheet.md',
    'docs/expected_outputs.md',
    'docs/further_reading.md',
    'docs/pair_programming_guide.md',
    'formative/quiz.yaml',
    'formative/run_quiz.py',
    'homework/README.md',
]

# Python files that must pass syntax check
PYTHON_FILES_TO_CHECK: List[str] = [
    'src/exercises/*.py',
    'src/apps/*.py',
    'scripts/*.py',
    'tests/*.py',
    'formative/run_quiz.py',
    'setup/*.py',
]


# ═══════════════════════════════════════════════════════════════════════════════
# VERIFICATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def print_header(title: str) -> None:
    """Print a formatted section header."""
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print(f"{'─' * 60}")


def print_status(name: str, passed: bool, message: str = "") -> None:
    """Print test status with color."""
    status = "\033[92m✓\033[0m" if passed else "\033[91m✗\033[0m"
    print(f"  {status} {name}", end="")
    if message:
        print(f" — {message}", end="")
    print()


def verify_file_exists(path: str) -> bool:
    """Check if a file exists relative to project root."""
    return (PROJECT_ROOT / path).exists()


def verify_lo_artifacts() -> Tuple[bool, int, int]:
    """
    Verify all Learning Objective artifacts exist.
    
    Returns:
        Tuple of (all_passed, passed_count, total_count)
    """
    print_header("Learning Objective Artifacts")
    
    all_files: Set[str] = set()
    for lo, files in REQUIRED_ARTIFACTS.items():
        all_files.update(files)
    
    passed = 0
    total = len(all_files)
    
    for lo, files in sorted(REQUIRED_ARTIFACTS.items()):
        print(f"\n  {lo}:")
        for filepath in files:
            exists = verify_file_exists(filepath)
            if exists:
                passed += 1
            print_status(f"    {filepath}", exists)
    
    return passed == total, passed, total


def verify_pcap_samples() -> Tuple[bool, int, int]:
    """
    Verify PCAP samples exist and meet size requirements.
    
    Returns:
        Tuple of (all_passed, passed_count, total_count)
    """
    print_header("PCAP Sample Files")
    
    passed = 0
    total = len(PCAP_REQUIREMENTS)
    
    for filepath, min_size in PCAP_REQUIREMENTS.items():
        full_path = PROJECT_ROOT / filepath
        if full_path.exists():
            size = full_path.stat().st_size
            if size >= min_size:
                passed += 1
                print_status(filepath, True, f"{size} bytes")
            else:
                print_status(filepath, False, f"too small: {size} < {min_size}")
        else:
            print_status(filepath, False, "missing")
    
    return passed == total, passed, total


def verify_quiz_coverage() -> Tuple[bool, int, int]:
    """
    Verify quiz covers all Learning Objectives.
    
    Returns:
        Tuple of (all_passed, passed_count, total_count)
    """
    print_header("Quiz LO Coverage")
    
    quiz_path = PROJECT_ROOT / 'formative' / 'quiz.yaml'
    
    if not quiz_path.exists():
        print_status("formative/quiz.yaml", False, "file not found")
        return False, 0, len(QUIZ_LO_COVERAGE)
    
    try:
        with open(quiz_path, encoding='utf-8') as f:
            quiz = yaml.safe_load(f)
    except Exception as e:
        print_status("Quiz YAML parse", False, str(e))
        return False, 0, len(QUIZ_LO_COVERAGE)
    
    questions = quiz.get('questions', [])
    question_ids = {q.get('id') for q in questions}
    question_los = {q.get('lo_ref') for q in questions}
    
    passed = 0
    total = len(QUIZ_LO_COVERAGE)
    
    for lo, expected_questions in QUIZ_LO_COVERAGE.items():
        found = [q for q in expected_questions if q in question_ids]
        if len(found) == len(expected_questions):
            passed += 1
            print_status(lo, True, f"{len(found)} questions")
        else:
            missing = set(expected_questions) - set(found)
            print_status(lo, False, f"missing: {missing}")
    
    # Also verify LO coverage matches
    print(f"\n  Quiz covers LOs: {sorted(question_los)}")
    
    return passed == total, passed, total


def verify_essential_docs() -> Tuple[bool, int, int]:
    """
    Verify essential documentation files exist.
    
    Returns:
        Tuple of (all_passed, passed_count, total_count)
    """
    print_header("Essential Documentation")
    
    passed = 0
    total = len(ESSENTIAL_DOCS)
    
    for filepath in ESSENTIAL_DOCS:
        exists = verify_file_exists(filepath)
        if exists:
            passed += 1
        print_status(filepath, exists)
    
    return passed == total, passed, total


def verify_python_syntax() -> Tuple[bool, int, int]:
    """
    Verify all Python files have valid syntax.
    
    Returns:
        Tuple of (all_passed, passed_count, total_count)
    """
    print_header("Python Syntax Check")
    
    import py_compile
    import glob
    
    all_files: List[Path] = []
    for pattern in PYTHON_FILES_TO_CHECK:
        all_files.extend(PROJECT_ROOT.glob(pattern))
    
    passed = 0
    total = len(all_files)
    
    for filepath in sorted(all_files):
        try:
            py_compile.compile(str(filepath), doraise=True)
            passed += 1
            rel_path = filepath.relative_to(PROJECT_ROOT)
            print_status(str(rel_path), True)
        except py_compile.PyCompileError as e:
            rel_path = filepath.relative_to(PROJECT_ROOT)
            print_status(str(rel_path), False, f"syntax error")
    
    return passed == total, passed, total


def verify_docker_config() -> Tuple[bool, int, int]:
    """
    Verify Docker configuration files exist and are valid.
    
    Returns:
        Tuple of (all_passed, passed_count, total_count)
    """
    print_header("Docker Configuration")
    
    docker_files = [
        'docker/docker-compose.yml',
        'docker/Dockerfile',
    ]
    
    passed = 0
    total = len(docker_files)
    
    for filepath in docker_files:
        exists = verify_file_exists(filepath)
        if exists:
            passed += 1
        print_status(filepath, exists)
    
    return passed == total, passed, total


def verify_makefile_targets() -> Tuple[bool, int, int]:
    """
    Verify Makefile contains required targets.
    
    Returns:
        Tuple of (all_passed, passed_count, total_count)
    """
    print_header("Makefile Targets")
    
    required_targets = [
        'help', 'test', 'quiz', 'lint', 'verify', 'verify-integrity',
        'docker-up', 'docker-down', 'clean', 'start', 'stop',
    ]
    
    makefile_path = PROJECT_ROOT / 'Makefile'
    
    if not makefile_path.exists():
        print_status("Makefile", False, "not found")
        return False, 0, len(required_targets)
    
    with open(makefile_path, encoding='utf-8') as f:
        content = f.read()
    
    passed = 0
    total = len(required_targets)
    
    for target in required_targets:
        # Look for target definition (target:)
        if f'\n{target}:' in content or content.startswith(f'{target}:'):
            passed += 1
            print_status(f"make {target}", True)
        else:
            print_status(f"make {target}", False, "not found")
    
    return passed == total, passed, total


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """
    Run all verification checks.
    
    Returns:
        Exit code (0 if all passed, 1 if any failed)
    """
    print()
    print("═" * 60)
    print("  Week 4 Kit Integrity Verification")
    print("  NETWORKING class - ASE, Informatics")
    print("═" * 60)
    
    results: List[Tuple[str, bool, int, int]] = []
    
    # Run all verifications
    checks = [
        ("LO Artifacts", verify_lo_artifacts),
        ("PCAP Samples", verify_pcap_samples),
        ("Quiz Coverage", verify_quiz_coverage),
        ("Essential Docs", verify_essential_docs),
        ("Python Syntax", verify_python_syntax),
        ("Docker Config", verify_docker_config),
        ("Makefile Targets", verify_makefile_targets),
    ]
    
    for name, check_func in checks:
        try:
            passed, count, total = check_func()
            results.append((name, passed, count, total))
        except Exception as e:
            print(f"\n  \033[91m✗\033[0m Error in {name}: {e}")
            results.append((name, False, 0, 1))
    
    # Summary
    print()
    print("═" * 60)
    print("  SUMMARY")
    print("═" * 60)
    
    total_passed = 0
    total_checks = 0
    all_sections_passed = True
    
    for name, passed, count, total in results:
        total_passed += count
        total_checks += total
        status = "\033[92m✓ PASS\033[0m" if passed else "\033[91m✗ FAIL\033[0m"
        print(f"  {name}: {status} ({count}/{total})")
        if not passed:
            all_sections_passed = False
    
    print()
    print(f"  Total: {total_passed}/{total_checks} checks passed")
    
    if all_sections_passed:
        print()
        print("  \033[92m╔════════════════════════════════════════╗\033[0m")
        print("  \033[92m║  ✓ Kit integrity verification PASSED  ║\033[0m")
        print("  \033[92m╚════════════════════════════════════════╝\033[0m")
        print()
        return 0
    else:
        print()
        print("  \033[91m╔════════════════════════════════════════╗\033[0m")
        print("  \033[91m║  ✗ Kit integrity verification FAILED  ║\033[0m")
        print("  \033[91m╚════════════════════════════════════════╝\033[0m")
        print()
        print("  Fix the issues above before committing.")
        print()
        return 1


if __name__ == '__main__':
    sys.exit(main())
