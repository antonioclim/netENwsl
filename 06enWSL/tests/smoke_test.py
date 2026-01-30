#!/usr/bin/env python3
"""
Smoke Tests — Week 6: NAT/PAT & SDN
===================================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

Quick sanity checks to verify the laboratory kit is properly set up.

Usage:
    python tests/smoke_test.py
    make smoke

Contact: Issues: Open an issue in GitHub
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

PROJECT_ROOT = Path(__file__).parent.parent

# Required files for the laboratory to function
REQUIRED_FILES = [
    "README.md",
    "Makefile",
    "pyproject.toml",
    "formative/quiz.yaml",
    "formative/run_quiz.py",
    "docs/theory_summary.md",
    "docs/troubleshooting.md",
    "docs/misconceptions.md",
    "docs/glossary.md",
    "docs/learning_objectives.md",
    "docs/peer_instruction.md",
    "src/exercises/ex_6_01_nat_topology.py",
    "src/exercises/ex_6_02_sdn_topology.py",
    "src/apps/nat_observer.py",
    "src/apps/tcp_echo.py",
    "src/apps/udp_echo.py",
    "homework/README.md",
    "setup/requirements.txt",
    "scripts/generate_session_token.py",
"scripts/run_demo.py",
"anti_ai/__init__.py",
"anti_ai/challenge.py",
"anti_ai/challenge_generator.py",
"anti_ai/evidence_collector.py",
"anti_ai/fingerprint.py",
"anti_ai/pcap_tools.py",
"anti_ai/submission_validator.py",
]


# ═══════════════════════════════════════════════════════════════════════════════
# TEST FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def check_required_files() -> Tuple[int, int, List[str]]:
    """
    Check that all required files exist.
    
    Returns:
        Tuple of (found_count, total_count, missing_files)
    """
    missing = []
    found = 0
    
    for file_path in REQUIRED_FILES:
        full_path = PROJECT_ROOT / file_path
        if full_path.exists():
            found += 1
        else:
            missing.append(file_path)
    
    return found, len(REQUIRED_FILES), missing


def check_python_syntax() -> Tuple[int, List[Tuple[str, str]]]:
    """
    Check all Python files for syntax errors.
    
    Returns:
        Tuple of (valid_count, list of (file, error) for invalid files)
    """
    errors = []
    valid = 0
    
    # Find all Python files
    python_files = list(PROJECT_ROOT.glob("**/*.py"))
    python_files = [
        f for f in python_files 
        if "__pycache__" not in str(f) and ".git" not in str(f)
    ]
    
    for py_file in python_files:
        try:
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(py_file)],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                valid += 1
            else:
                rel_path = py_file.relative_to(PROJECT_ROOT)
                errors.append((str(rel_path), result.stderr.strip()))
        except subprocess.TimeoutExpired:
            rel_path = py_file.relative_to(PROJECT_ROOT)
            errors.append((str(rel_path), "Timeout"))
        except Exception as e:
            rel_path = py_file.relative_to(PROJECT_ROOT)
            errors.append((str(rel_path), str(e)))
    
    return valid, errors


def check_yaml_valid() -> Tuple[bool, str]:
    """
    Check that quiz YAML is valid.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        import yaml
    except ImportError:
        return False, "PyYAML not installed"
    
    quiz_path = PROJECT_ROOT / "formative" / "quiz.yaml"
    
    if not quiz_path.exists():
        return False, "Quiz file not found"
    
    try:
        with open(quiz_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        
        # Basic validation
        if "metadata" not in data:
            return False, "Missing metadata section"
        if "questions" not in data:
            return False, "Missing questions section"
        
        return True, f"Valid ({len(data['questions'])} questions)"
    except yaml.YAMLError as e:
        return False, f"YAML parse error: {e}"
    except Exception as e:
        return False, str(e)


def check_quiz_json() -> Tuple[bool, str]:
    """
    Check that quiz JSON (LMS export) is valid if present.
    
    Returns:
        Tuple of (is_valid, message)
    """
    import json
    
    json_path = PROJECT_ROOT / "formative" / "quiz_lms.json"
    
    if not json_path.exists():
        return True, "Not present (optional)"
    
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        q_count = len(data.get("questions", []))
        return True, f"Valid ({q_count} questions)"
    except json.JSONDecodeError as e:
        return False, f"JSON parse error: {e}"
    except Exception as e:
        return False, str(e)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Run smoke tests."""
    print()
    print("=" * 60)
    print("  WEEK 6 SMOKE TEST")
    print("=" * 60)
    print()
    
    all_passed = True
    
    # Check required files
    print("Checking required files...")
    found, total, missing = check_required_files()
    print(f"  Found: {found}/{total}")
    
    if missing:
        print("  Missing files:")
        for f in missing[:5]:  # Show first 5 missing
            print(f"    ✗ {f}")
        if len(missing) > 5:
            print(f"    ... and {len(missing) - 5} more")
        all_passed = False
    else:
        print("  ✓ All required files present")
    
    print()
    
    # Check Python syntax
    print("Checking Python syntax...")
    valid, errors = check_python_syntax()
    print(f"  Valid: {valid}")
    
    if errors:
        print("  Syntax errors:")
        for file, error in errors[:3]:  # Show first 3 errors
            # Extract line number from error message
            error_short = error.split("\n")[0] if error else "Unknown error"
            print(f"    ✗ {file}: {error_short}")
        if len(errors) > 3:
            print(f"    ... and {len(errors) - 3} more")
        all_passed = False
    else:
        print("  ✓ All Python files have valid syntax")
    
    print()
    
    # Check YAML
    print("Checking quiz YAML...")
    yaml_valid, yaml_msg = check_yaml_valid()
    if yaml_valid:
        print(f"  ✓ {yaml_msg}")
    else:
        print(f"  ✗ {yaml_msg}")
        all_passed = False
    
    # Check JSON
    print("Checking quiz JSON (LMS)...")
    json_valid, json_msg = check_quiz_json()
    if json_valid:
        print(f"  ✓ {json_msg}")
    else:
        print(f"  ✗ {json_msg}")
        all_passed = False
    
    print()
    print("=" * 60)
    if all_passed:
        print("  SMOKE TEST PASSED")
    else:
        print("  SMOKE TEST FAILED")
    print("=" * 60)
    print()
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
