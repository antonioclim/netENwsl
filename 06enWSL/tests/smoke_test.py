#!/usr/bin/env python3
"""
Smoke Test for Week 6 Laboratory Materials
===========================================
Computer Networks - Week 6 (WSL Environment)
ASE Bucharest | by ing. dr. Antonio Clim

Verifies that all required files exist and basic syntax is correct.

Usage:
    python3 smoke_test.py
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import List, Tuple


# ═══════════════════════════════════════════════════════════════════════════════
# REQUIRED_FILES
# ═══════════════════════════════════════════════════════════════════════════════

REQUIRED_FILES = [
    # Documentation
    "README.md",
    "docs/theory_summary.md",
    "docs/commands_cheatsheet.md",
    "docs/troubleshooting.md",
    "docs/further_reading.md",
    "docs/peer_instruction.md",
    "docs/pair_programming_guide.md",
    "docs/misconceptions.md",
    "docs/glossary.md",
    "docs/code_tracing.md",
    "docs/parsons_problems.md",
    "docs/concept_analogies.md",
    # Source code
    "src/exercises/ex_6_01_nat_topology.py",
    "src/exercises/ex_6_02_sdn_topology.py",
    "src/apps/nat_observer.py",
    "src/apps/sdn_policy_controller.py",
    "src/apps/tcp_echo.py",
    "src/apps/udp_echo.py",
    # Homework
    "homework/README.md",
]


def check_files(base_path: Path) -> Tuple[List[str], List[str]]:
    """Check for required files."""
    found = []
    missing = []
    
    for file_path in REQUIRED_FILES:
        full_path = base_path / file_path
        if full_path.exists():
            found.append(file_path)
        else:
            missing.append(file_path)
    
    return found, missing


def check_python_syntax(base_path: Path) -> Tuple[List[str], List[Tuple[str, str]]]:
    """Check Python syntax for all .py files."""
    valid = []
    errors = []
    
    for py_file in base_path.rglob("*.py"):
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                compile(f.read(), py_file, "exec")
            valid.append(str(py_file.relative_to(base_path)))
        except SyntaxError as e:
            errors.append((str(py_file.relative_to(base_path)), str(e)))
    
    return valid, errors


def main() -> int:
    """Run smoke tests."""
    base_path = Path(__file__).parent.parent
    
    print("=" * 60)
    print("  WEEK 6 SMOKE TEST")
    print("=" * 60)
    print()
    
    # Check files
    print("Checking required files...")
    found, missing = check_files(base_path)
    
    print(f"  Found: {len(found)}/{len(REQUIRED_FILES)}")
    
    if missing:
        print(f"  Missing files:")
        for f in missing:
            print(f"    ✗ {f}")
    else:
        print("  ✓ All required files present")
    
    print()
    
    # Check Python syntax
    print("Checking Python syntax...")
    valid, errors = check_python_syntax(base_path)
    
    print(f"  Valid: {len(valid)}")
    
    if errors:
        print(f"  Syntax errors:")
        for f, e in errors:
            print(f"    ✗ {f}: {e}")
    else:
        print("  ✓ All Python files have valid syntax")
    
    print()
    print("=" * 60)
    
    if missing or errors:
        print("  SMOKE TEST FAILED")
        return 1
    else:
        print("  SMOKE TEST PASSED")
        return 0


if __name__ == "__main__":
    sys.exit(main())
