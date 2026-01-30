#!/usr/bin/env python3
"""
validate_kit.py — Lab Kit Integrity Validator
NETWORKING class — ASE, CSIE | Computer Networks Laboratory
by ing. dr. Antonio Clim

Validates the complete structure and integrity of the Week 14 lab kit.
Checks for required files, validates formats, and ensures pedagogical coverage.

Usage:
    python scripts/validate_kit.py           # Full validation
    python scripts/validate_kit.py --quick   # Quick check (structure only)
    python scripts/validate_kit.py --fix     # Attempt to fix issues
    python scripts/validate_kit.py --json    # Output as JSON
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

class Severity(Enum):
    """Issue severity levels."""
    ERROR = "ERROR"      # Must fix - kit won't work
    WARNING = "WARNING"  # Should fix - affects quality
    INFO = "INFO"        # Nice to have - suggestions


class Category(Enum):
    """Validation categories."""
    STRUCTURE = "Structure"
    PEDAGOGICAL = "Pedagogical"
    CODE_QUALITY = "Code Quality"
    DOCUMENTATION = "Documentation"
    SECURITY = "Security"


# Required files and directories
REQUIRED_STRUCTURE = {
    # Root files
    "README.md": "Main documentation",
    "CHANGELOG.md": "Version history",
    "LICENSE": "License file",
    "SECURITY.md": "Security policy",
    "Makefile": "Build orchestrator",
    "pyproject.toml": "Python project config",
    "ruff.toml": "Linter configuration",
    
    # Docker
    "docker/docker-compose.yml": "Docker services definition",
    "docker/Dockerfile": "Container image definition",
    
    # Documentation
    "docs/theory_summary.md": "Theory content",
    "docs/misconceptions.md": "Common misconceptions",
    "docs/troubleshooting.md": "Troubleshooting guide",
    "docs/learning_objectives.md": "LO traceability matrix",
    "docs/peer_instruction.md": "Peer instruction questions",
    "docs/code_tracing.md": "Code tracing exercises",
    "docs/parsons_problems.md": "Parsons problems",
    
    # Formative assessment
    "formative/quiz.yaml": "Quiz in YAML format",
    "formative/quiz.json": "Quiz in JSON format",
    "formative/run_quiz.py": "Interactive quiz runner",
    "formative/__init__.py": "Package init",
    
    # Tests
    "tests/smoke_test.py": "Smoke tests",
    "tests/expected_outputs.md": "Expected test outputs",
    
    # Setup
    "setup/requirements.txt": "Python dependencies",
    "setup/verify_environment.py": "Environment verification",
}

# Learning objectives to validate
LEARNING_OBJECTIVES = ["LO1", "LO2", "LO3", "LO4", "LO5", "LO6"]

# Minimum requirements
MIN_QUIZ_QUESTIONS = 10
MIN_MISCONCEPTIONS = 10
MIN_PEER_INSTRUCTION_QUESTIONS = 5
MIN_CODE_TRACING_EXERCISES = 5
MIN_PARSONS_PROBLEMS = 5


# ═══════════════════════════════════════════════════════════════════════════════
# DATA CLASSES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ValidationIssue:
    """Single validation issue."""
    severity: Severity
    category: Category
    message: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    fix_suggestion: Optional[str] = None


@dataclass
class ValidationResult:
    """Complete validation result."""
    kit_path: Path
    issues: List[ValidationIssue] = field(default_factory=list)
    checks_passed: int = 0
    checks_failed: int = 0
    checks_warned: int = 0
    
    @property
    def is_valid(self) -> bool:
        """Kit is valid if no errors."""
        return not any(i.severity == Severity.ERROR for i in self.issues)
    
    @property
    def score(self) -> float:
        """Calculate validation score (0-100)."""
        total = self.checks_passed + self.checks_failed + self.checks_warned
        if total == 0:
            return 100.0
        penalties = self.checks_failed * 10 + self.checks_warned * 2
        return max(0, 100 - penalties)
    
    def add_issue(self, issue: ValidationIssue) -> None:
        """Add an issue and update counts."""
        self.issues.append(issue)
        if issue.severity == Severity.ERROR:
            self.checks_failed += 1
        elif issue.severity == Severity.WARNING:
            self.checks_warned += 1
    
    def add_pass(self) -> None:
        """Record a passed check."""
        self.checks_passed += 1


# ═══════════════════════════════════════════════════════════════════════════════
# COLOUR OUTPUT
# ═══════════════════════════════════════════════════════════════════════════════

class Colours:
    """ANSI colour codes."""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    END = '\033[0m'
    
    @classmethod
    def disable(cls) -> None:
        for attr in dir(cls):
            if attr.isupper() and not attr.startswith('_'):
                setattr(cls, attr, '')


def print_header(text: str) -> None:
    """Print section header."""
    print(f"\n{Colours.CYAN}{'═' * 70}{Colours.END}")
    print(f"{Colours.BOLD}  {text}{Colours.END}")
    print(f"{Colours.CYAN}{'═' * 70}{Colours.END}\n")


def print_check(passed: bool, message: str) -> None:
    """Print check result."""
    if passed:
        print(f"  {Colours.GREEN}✓{Colours.END} {message}")
    else:
        print(f"  {Colours.RED}✗{Colours.END} {message}")


def print_issue(issue: ValidationIssue) -> None:
    """Print a validation issue."""
    colour = {
        Severity.ERROR: Colours.RED,
        Severity.WARNING: Colours.YELLOW,
        Severity.INFO: Colours.CYAN,
    }[issue.severity]
    
    prefix = f"[{issue.severity.value}]"
    location = f" ({issue.file_path})" if issue.file_path else ""
    
    print(f"  {colour}{prefix}{Colours.END} {issue.message}{location}")
    
    if issue.fix_suggestion:
        print(f"       {Colours.DIM}Fix: {issue.fix_suggestion}{Colours.END}")


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATORS
# ═══════════════════════════════════════════════════════════════════════════════

def validate_structure(kit_path: Path, result: ValidationResult) -> None:
    """Validate directory structure and required files."""
    print_header("Structure Validation")
    
    for rel_path, description in REQUIRED_STRUCTURE.items():
        full_path = kit_path / rel_path
        exists = full_path.exists()
        
        print_check(exists, f"{rel_path} — {description}")
        
        if exists:
            result.add_pass()
        else:
            result.add_issue(ValidationIssue(
                severity=Severity.ERROR,
                category=Category.STRUCTURE,
                message=f"Missing required file: {rel_path}",
                file_path=rel_path,
                fix_suggestion=f"Create {rel_path}"
            ))


def validate_quiz_yaml(kit_path: Path, result: ValidationResult) -> None:
    """Validate quiz YAML format and content."""
    print_header("Quiz Validation (YAML)")
    
    if not YAML_AVAILABLE:
        result.add_issue(ValidationIssue(
            severity=Severity.WARNING,
            category=Category.PEDAGOGICAL,
            message="PyYAML not installed, skipping YAML validation",
            fix_suggestion="pip install pyyaml"
        ))
        return
    
    quiz_path = kit_path / "formative" / "quiz_week14.yaml"
    
    if not quiz_path.exists():
        return  # Already reported in structure check
    
    try:
        with open(quiz_path, 'r', encoding='utf-8') as f:
            quiz = yaml.safe_load(f)
        
        print_check(True, "YAML syntax valid")
        result.add_pass()
        
        # Check metadata
        if 'metadata' in quiz:
            print_check(True, "Metadata section present")
            result.add_pass()
        else:
            result.add_issue(ValidationIssue(
                severity=Severity.ERROR,
                category=Category.PEDAGOGICAL,
                message="Quiz missing 'metadata' section",
                file_path="formative/quiz.yaml"
            ))
        
        # Check questions
        questions = quiz.get('questions', [])
        q_count = len(questions)
        has_enough = q_count >= MIN_QUIZ_QUESTIONS
        
        print_check(has_enough, f"Question count: {q_count} (min: {MIN_QUIZ_QUESTIONS})")
        
        if has_enough:
            result.add_pass()
        else:
            result.add_issue(ValidationIssue(
                severity=Severity.WARNING,
                category=Category.PEDAGOGICAL,
                message=f"Quiz has only {q_count} questions (recommended: {MIN_QUIZ_QUESTIONS}+)",
                file_path="formative/quiz.yaml"
            ))
        
        # Check LO coverage
        covered_los = set()
        for q in questions:
            lo = q.get('lo_ref')
            if lo:
                covered_los.add(lo)
        
        missing_los = set(LEARNING_OBJECTIVES) - covered_los
        has_all_los = len(missing_los) == 0
        
        print_check(has_all_los, f"LO coverage: {len(covered_los)}/{len(LEARNING_OBJECTIVES)}")
        
        if has_all_los:
            result.add_pass()
        else:
            result.add_issue(ValidationIssue(
                severity=Severity.WARNING,
                category=Category.PEDAGOGICAL,
                message=f"Quiz missing coverage for: {', '.join(missing_los)}",
                file_path="formative/quiz.yaml"
            ))
        
        # Check Bloom coverage
        bloom_levels = set()
        for q in questions:
            bloom = q.get('bloom_level')
            if bloom:
                bloom_levels.add(bloom)
        
        expected_blooms = {"Remember", "Understand", "Apply", "Analyze"}
        missing_blooms = expected_blooms - bloom_levels
        has_bloom_coverage = len(missing_blooms) <= 1
        
        print_check(has_bloom_coverage, f"Bloom levels covered: {len(bloom_levels)}")
        
        if has_bloom_coverage:
            result.add_pass()
        else:
            result.add_issue(ValidationIssue(
                severity=Severity.INFO,
                category=Category.PEDAGOGICAL,
                message=f"Consider adding questions for Bloom levels: {', '.join(missing_blooms)}"
            ))
        
        # Check each question has required fields
        required_fields = ['id', 'type', 'correct', 'stem']
        for i, q in enumerate(questions):
            missing_fields = [f for f in required_fields if f not in q]
            if missing_fields:
                result.add_issue(ValidationIssue(
                    severity=Severity.ERROR,
                    category=Category.PEDAGOGICAL,
                    message=f"Question {i+1} missing fields: {', '.join(missing_fields)}",
                    file_path="formative/quiz.yaml"
                ))
        
    except yaml.YAMLError as e:
        print_check(False, "YAML syntax invalid")
        result.add_issue(ValidationIssue(
            severity=Severity.ERROR,
            category=Category.PEDAGOGICAL,
            message=f"YAML parse error: {e}",
            file_path="formative/quiz.yaml"
        ))


def validate_quiz_json(kit_path: Path, result: ValidationResult) -> None:
    """Validate quiz JSON format."""
    print_header("Quiz Validation (JSON)")
    
    quiz_path = kit_path / "formative" / "quiz_week14.json"
    
    if not quiz_path.exists():
        return
    
    try:
        with open(quiz_path, 'r', encoding='utf-8') as f:
            quiz = json.load(f)
        
        print_check(True, "JSON syntax valid")
        result.add_pass()
        
        # Basic structure check
        has_metadata = 'metadata' in quiz
        has_questions = 'questions' in quiz
        
        print_check(has_metadata, "Metadata section present")
        print_check(has_questions, "Questions section present")
        
        if has_metadata:
            result.add_pass()
        if has_questions:
            result.add_pass()
            
    except json.JSONDecodeError as e:
        print_check(False, "JSON syntax invalid")
        result.add_issue(ValidationIssue(
            severity=Severity.ERROR,
            category=Category.PEDAGOGICAL,
            message=f"JSON parse error: {e}",
            file_path="formative/quiz.json"
        ))


def validate_docker(kit_path: Path, result: ValidationResult) -> None:
    """Validate Docker configuration."""
    print_header("Docker Validation")
    
    compose_path = kit_path / "docker" / "docker-compose.yml"
    
    if not compose_path.exists():
        return
    
    if not YAML_AVAILABLE:
        result.add_issue(ValidationIssue(
            severity=Severity.WARNING,
            category=Category.STRUCTURE,
            message="PyYAML not installed, skipping Docker validation"
        ))
        return
    
    try:
        with open(compose_path, 'r', encoding='utf-8') as f:
            compose = yaml.safe_load(f)
        
        print_check(True, "docker-compose.yml syntax valid")
        result.add_pass()
        
        # Check services
        services = compose.get('services', {})
        required_services = ['app1', 'app2', 'lb']
        
        for svc in required_services:
            # Check with prefix too
            found = svc in services or any(svc in s for s in services.keys())
            print_check(found, f"Service '{svc}' defined")
            if found:
                result.add_pass()
            else:
                result.add_issue(ValidationIssue(
                    severity=Severity.ERROR,
                    category=Category.STRUCTURE,
                    message=f"Missing required service: {svc}",
                    file_path="docker/docker-compose.yml"
                ))
        
        # Check networks
        networks = compose.get('networks', {})
        has_networks = len(networks) >= 2
        print_check(has_networks, f"Networks defined: {len(networks)}")
        
        if has_networks:
            result.add_pass()
        else:
            result.add_issue(ValidationIssue(
                severity=Severity.WARNING,
                category=Category.STRUCTURE,
                message="Expected at least 2 networks for isolation demo"
            ))
        
    except yaml.YAMLError as e:
        print_check(False, "docker-compose.yml syntax invalid")
        result.add_issue(ValidationIssue(
            severity=Severity.ERROR,
            category=Category.STRUCTURE,
            message=f"YAML parse error: {e}",
            file_path="docker/docker-compose.yml"
        ))


def validate_security(kit_path: Path, result: ValidationResult) -> None:
    """Validate security policy and practices."""
    print_header("Security Validation")
    
    security_path = kit_path / "SECURITY.md"
    
    if security_path.exists():
        print_check(True, "SECURITY.md exists")
        result.add_pass()
        
        content = security_path.read_text(encoding='utf-8')
        
        # Check for key sections
        sections = [
            "No Real Credentials",
            "Container Isolation", 
            "Input Validation",
            "Vulnerability Reporting"
        ]
        
        for section in sections:
            has_section = section.lower() in content.lower()
            print_check(has_section, f"Section: {section}")
            if has_section:
                result.add_pass()
            else:
                result.add_issue(ValidationIssue(
                    severity=Severity.INFO,
                    category=Category.SECURITY,
                    message=f"Consider adding section: {section}",
                    file_path="SECURITY.md"
                ))
    
    # Check for hardcoded secrets in Python files
    print(f"\n  {Colours.DIM}Scanning for hardcoded secrets...{Colours.END}")
    
    suspicious_patterns = ['api_key', 'secret_key', 'password', 'token']
    exclusions = ['studstudstud', 'stud', '# lab credential', 'example']
    
    for py_file in kit_path.rglob('*.py'):
        if '__pycache__' in str(py_file):
            continue
        
        try:
            content = py_file.read_text(encoding='utf-8')
            for pattern in suspicious_patterns:
                if pattern in content.lower():
                    # Check if it's an exclusion
                    is_excluded = any(exc in content.lower() for exc in exclusions)
                    if not is_excluded:
                        result.add_issue(ValidationIssue(
                            severity=Severity.WARNING,
                            category=Category.SECURITY,
                            message=f"Potential hardcoded credential: '{pattern}'",
                            file_path=str(py_file.relative_to(kit_path))
                        ))
        except Exception:
            pass
    
    print_check(True, "Secret scan complete")


def validate_code_quality(kit_path: Path, result: ValidationResult) -> None:
    """Validate code quality indicators."""
    print_header("Code Quality Validation")
    
    # Check for pyproject.toml
    pyproject = kit_path / "pyproject.toml"
    if pyproject.exists():
        print_check(True, "pyproject.toml present (modern config)")
        result.add_pass()

        # Basic TOML syntax validation (catches subtle errors early)
        try:
            import tomllib
            with open(pyproject, 'rb') as f:
                tomllib.load(f)
            print_check(True, 'pyproject.toml parses (TOML syntax OK)')
            result.add_pass()
        except Exception as e:
            result.add_issue(ValidationIssue(
                severity=Severity.ERROR,
                category=Category.CODE_QUALITY,
                message=f'pyproject.toml has invalid TOML syntax: {e}',
                file_path='pyproject.toml',
            ))
    else:
        result.add_issue(ValidationIssue(
            severity=Severity.WARNING,
            category=Category.CODE_QUALITY,
            message="Missing pyproject.toml"
        ))
    
    # Check for ruff.toml
    ruff_config = kit_path / "ruff.toml"
    if ruff_config.exists():
        print_check(True, "ruff.toml present (linter config)")
        result.add_pass()
    else:
        result.add_issue(ValidationIssue(
            severity=Severity.WARNING,
            category=Category.CODE_QUALITY,
            message="Missing ruff.toml"
        ))
    
    # Check for pre-commit config
    precommit = kit_path / ".pre-commit-config.yaml"
    if precommit.exists():
        print_check(True, ".pre-commit-config.yaml present")
        result.add_pass()
    else:
        result.add_issue(ValidationIssue(
            severity=Severity.INFO,
            category=Category.CODE_QUALITY,
            message="Missing .pre-commit-config.yaml"
        ))
    
    # Check for CI pipeline
    ci_path = kit_path / ".github" / "workflows" / "ci.yml"
    if ci_path.exists():
        print_check(True, "GitHub Actions CI pipeline present")
        result.add_pass()
    else:
        result.add_issue(ValidationIssue(
            severity=Severity.WARNING,
            category=Category.CODE_QUALITY,
            message="Missing CI pipeline",
            fix_suggestion="Add .github/workflows/ci.yml"
        ))
    
    # Check for type hints in key files
    print(f"\n  {Colours.DIM}Checking type hints...{Colours.END}")
    
    type_hint_files = [
        "formative/run_quiz.py",
        "tests/smoke_test.py",
    ]
    
    for rel_path in type_hint_files:
        file_path = kit_path / rel_path
        if file_path.exists():
            content = file_path.read_text(encoding='utf-8')
            has_type_hints = ' -> ' in content or ': str' in content or ': int' in content
            print_check(has_type_hints, f"Type hints in {rel_path}")
            if has_type_hints:
                result.add_pass()



    # Syntax compilation check for the Python source tree
    print(f"\n  {Colours.DIM}Checking Python syntax (py_compile)...{Colours.END}")
    import py_compile
    compile_errors: List[str] = []
    for folder in ("src", "scripts", "formative", "tests"):
        base = kit_path / folder
        if not base.exists():
            continue
        for py_file in base.rglob("*.py"):
            try:
                py_compile.compile(str(py_file), doraise=True)
            except Exception as e:
                rel = str(py_file.relative_to(kit_path))
                compile_errors.append(f"{rel}: {e}")

    if compile_errors:
        print_check(False, f"Python syntax errors: {len(compile_errors)} file(s)")
        # Report first few errors to keep output readable
        for err in compile_errors[:5]:
            result.add_issue(ValidationIssue(
                severity=Severity.ERROR,
                category=Category.CODE_QUALITY,
                message=f"Python syntax error: {err}",
            ))
    else:
        print_check(True, "Python syntax OK")
        result.add_pass()

def validate_documentation(kit_path: Path, result: ValidationResult) -> None:
    """Validate documentation completeness."""
    print_header("Documentation Validation")
    
    readme = kit_path / "README.md"
    if readme.exists():
        content = readme.read_text(encoding='utf-8')
        
        # Check for key sections
        sections = [
            ("Installation", "install"),
            ("Learning Objectives", "learning"),
            ("Troubleshooting", "troubleshoot"),
            ("Usage", "usage"),
        ]
        
        for name, keyword in sections:
            has_section = keyword in content.lower()
            print_check(has_section, f"README section: {name}")
            if has_section:
                result.add_pass()
            else:
                result.add_issue(ValidationIssue(
                    severity=Severity.INFO,
                    category=Category.DOCUMENTATION,
                    message=f"Consider adding section: {name}",
                    file_path="README.md"
                ))
        
        # Check for badges
        has_badges = '![' in content and '](' in content
        print_check(has_badges, "README has badges")
        if has_badges:
            result.add_pass()
    
    # Check LO traceability matrix
    lo_matrix = kit_path / "docs" / "learning_objectives.md"
    if lo_matrix.exists():
        content = lo_matrix.read_text(encoding='utf-8')
        
        # Check all LOs are documented
        for lo in LEARNING_OBJECTIVES:
            has_lo = lo in content
            print_check(has_lo, f"LO documented: {lo}")
            if has_lo:
                result.add_pass()
            else:
                result.add_issue(ValidationIssue(
                    severity=Severity.WARNING,
                    category=Category.DOCUMENTATION,
                    message=f"Missing LO documentation: {lo}",
                    file_path="docs/learning_objectives.md"
                ))


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN VALIDATION RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

def run_validation(kit_path: Path, quick: bool = False) -> ValidationResult:
    """Run all validations."""
    result = ValidationResult(kit_path=kit_path)
    
    # Always run structure validation
    validate_structure(kit_path, result)
    
    if not quick:
        validate_quiz_yaml(kit_path, result)
        validate_quiz_json(kit_path, result)
        validate_docker(kit_path, result)
        validate_security(kit_path, result)
        validate_code_quality(kit_path, result)
        validate_documentation(kit_path, result)
    
    return result


def print_summary(result: ValidationResult) -> None:
    """Print validation summary."""
    print_header("Validation Summary")
    
    total = result.checks_passed + result.checks_failed + result.checks_warned
    
    print(f"  {Colours.GREEN}Passed:{Colours.END}   {result.checks_passed}")
    print(f"  {Colours.RED}Failed:{Colours.END}   {result.checks_failed}")
    print(f"  {Colours.YELLOW}Warnings:{Colours.END} {result.checks_warned}")
    print(f"  {Colours.BOLD}Total:{Colours.END}    {total}")
    print()
    
    # Score
    score_colour = Colours.GREEN if result.score >= 80 else Colours.YELLOW if result.score >= 60 else Colours.RED
    print(f"  {Colours.BOLD}Score:{Colours.END} {score_colour}{result.score:.1f}/100{Colours.END}")
    
    # Status
    if result.is_valid:
        print(f"\n  {Colours.GREEN}✓ Kit is VALID{Colours.END}")
    else:
        print(f"\n  {Colours.RED}✗ Kit has ERRORS that must be fixed{Colours.END}")
    
    # List errors
    errors = [i for i in result.issues if i.severity == Severity.ERROR]
    if errors:
        print(f"\n  {Colours.RED}Errors to fix:{Colours.END}")
        for issue in errors:
            print_issue(issue)


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate Week 14 Lab Kit integrity"
    )
    parser.add_argument(
        '--path', '-p',
        type=Path,
        default=Path('.'),
        help='Path to kit root (default: current directory)'
    )
    parser.add_argument(
        '--quick', '-q',
        action='store_true',
        help='Quick validation (structure only)'
    )
    parser.add_argument(
        '--json', '-j',
        action='store_true',
        help='Output as JSON'
    )
    parser.add_argument(
        '--no-colour',
        action='store_true',
        help='Disable coloured output'
    )
    
    args = parser.parse_args()
    
    if args.no_colour or args.json:
        Colours.disable()
    
    # Find kit root
    kit_path = args.path.resolve()
    
    # Check if we're in the kit
    if not (kit_path / "README.md").exists():
        # Try parent
        if (kit_path.parent / "README.md").exists():
            kit_path = kit_path.parent
    
    if not args.json:
        print(f"\n{Colours.BOLD}Week 14 Lab Kit Validator{Colours.END}")
        print(f"{Colours.DIM}Path: {kit_path}{Colours.END}")
    
    # Run validation
    result = run_validation(kit_path, quick=args.quick)
    
    # Output
    if args.json:
        output = {
            "kit_path": str(result.kit_path),
            "is_valid": result.is_valid,
            "score": result.score,
            "checks_passed": result.checks_passed,
            "checks_failed": result.checks_failed,
            "checks_warned": result.checks_warned,
            "issues": [
                {
                    "severity": i.severity.value,
                    "category": i.category.value,
                    "message": i.message,
                    "file": i.file_path,
                }
                for i in result.issues
            ]
        }
        print(json.dumps(output, indent=2))
    else:
        print_summary(result)
    
    return 0 if result.is_valid else 1


if __name__ == "__main__":
    sys.exit(main())
