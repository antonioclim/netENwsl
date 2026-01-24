#!/usr/bin/env python3
"""
Ground Truth Validation Script — Week 13: IoT and Security
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

PURPOSE:
    Validates that ground_truth.json matches actual kit contents.
    Ensures AI systems can verify facts about this kit.
    Prevents hallucinations by providing machine-readable verification.

USAGE:
    python tests/validate_ground_truth.py           # Full validation
    python tests/validate_ground_truth.py --quick   # Quick checks only
    python tests/validate_ground_truth.py --json    # Output as JSON

LEARNING OBJECTIVES:
    - Understand the importance of verifiable claims in technical documentation
    - Apply automated testing principles to documentation validation
    - Analyse discrepancies between documented and actual state
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

PROJECT_ROOT = Path(__file__).parent.parent
GROUND_TRUTH_PATH = PROJECT_ROOT / "tests" / "ground_truth.json"

# Tolerance for line count validation (allow 10% variance for minor edits)
LINE_COUNT_TOLERANCE = 0.10


# ═══════════════════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ValidationResult:
    """Result of a single validation check."""

    name: str
    passed: bool
    expected: Any
    actual: Any
    message: str = ""


@dataclass
class ValidationReport:
    """Complete validation report."""

    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    ground_truth_version: str = ""
    total_checks: int = 0
    passed_checks: int = 0
    failed_checks: int = 0
    results: List[ValidationResult] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage."""
        if self.total_checks == 0:
            return 0.0
        return (self.passed_checks / self.total_checks) * 100

    @property
    def all_passed(self) -> bool:
        """Check if all validations passed."""
        return self.failed_checks == 0


# ═══════════════════════════════════════════════════════════════════════════════
# TERMINAL COLOURS
# ═══════════════════════════════════════════════════════════════════════════════

class Colours:
    """ANSI colour codes for terminal output."""

    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


# Disable colours if not TTY
if not sys.stdout.isatty():
    Colours.GREEN = Colours.RED = Colours.YELLOW = ""
    Colours.CYAN = Colours.BOLD = Colours.RESET = ""


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def load_ground_truth() -> Dict[str, Any]:
    """
    Load ground truth from JSON file.

    Returns:
        Dictionary containing ground truth data

    Raises:
        FileNotFoundError: If ground_truth.json does not exist
        json.JSONDecodeError: If JSON is malformed
    """
    if not GROUND_TRUTH_PATH.exists():
        raise FileNotFoundError(f"Ground truth file not found: {GROUND_TRUTH_PATH}")

    with open(GROUND_TRUTH_PATH, encoding="utf-8") as f:
        return json.load(f)


def validate_python_version(gt: Dict[str, Any]) -> ValidationResult:
    """Check Python version meets minimum requirement."""
    major, minor = sys.version_info[:2]
    current = f"{major}.{minor}"

    required = gt["environment"]["python_min_version"]
    req_major, req_minor = map(int, required.split("."))

    passed = (major, minor) >= (req_major, req_minor)

    return ValidationResult(
        name="Python Version",
        passed=passed,
        expected=f">= {required}",
        actual=current,
        message="Python version compatible" if passed else "Python version too old",
    )


def validate_exercise_files(gt: Dict[str, Any]) -> List[ValidationResult]:
    """Verify exercise files exist and have expected line counts."""
    results = []
    exercises_dir = PROJECT_ROOT / "src" / "exercises"

    for ex_id, ex_data in gt["exercises"].items():
        filename = ex_data["filename"]
        expected_lines = ex_data["lines_of_code"]
        filepath = exercises_dir / filename

        if not filepath.exists():
            results.append(
                ValidationResult(
                    name=f"Exercise {ex_id} exists",
                    passed=False,
                    expected=filename,
                    actual="NOT FOUND",
                    message=f"File missing: {filepath}",
                )
            )
            continue

        # Count actual lines
        with open(filepath, encoding="utf-8") as f:
            actual_lines = len(f.readlines())

        # Allow tolerance for minor edits
        tolerance = expected_lines * LINE_COUNT_TOLERANCE
        passed = abs(actual_lines - expected_lines) <= tolerance

        results.append(
            ValidationResult(
                name=f"Exercise {ex_id} line count",
                passed=passed,
                expected=f"{expected_lines} ± {int(tolerance)}",
                actual=actual_lines,
                message="Line count within tolerance" if passed else "Significant line count change",
            )
        )

    return results


def validate_ports_in_compose(gt: Dict[str, Any]) -> List[ValidationResult]:
    """Check docker-compose.yml uses correct ports."""
    results = []
    compose_path = PROJECT_ROOT / "docker" / "docker-compose.yml"

    if not compose_path.exists():
        results.append(
            ValidationResult(
                name="docker-compose.yml exists",
                passed=False,
                expected="docker/docker-compose.yml",
                actual="NOT FOUND",
            )
        )
        return results

    with open(compose_path, encoding="utf-8") as f:
        content = f.read()

    for port_name, port_data in gt["ports"].items():
        # Skip reserved ports (not in compose)
        if "reserved" in port_name:
            continue

        port_num = port_data["number"]
        found = str(port_num) in content

        results.append(
            ValidationResult(
                name=f"Port {port_name}",
                passed=found,
                expected=port_num,
                actual="found" if found else "NOT FOUND",
                message=f"Port {port_num} configured" if found else f"Port {port_num} missing from compose",
            )
        )

    return results


def validate_documentation_files(gt: Dict[str, Any]) -> List[ValidationResult]:
    """Verify key documentation files exist."""
    results = []

    for doc_path in gt["documentation"]["key_documents"]:
        full_path = PROJECT_ROOT / doc_path

        passed = full_path.exists()
        results.append(
            ValidationResult(
                name=f"Doc: {doc_path}",
                passed=passed,
                expected="exists",
                actual="exists" if passed else "NOT FOUND",
            )
        )

    return results


def validate_quiz_structure(gt: Dict[str, Any]) -> List[ValidationResult]:
    """Verify quiz file exists and has expected structure."""
    results = []
    quiz_path = PROJECT_ROOT / gt["quiz"]["file"]

    if not quiz_path.exists():
        results.append(
            ValidationResult(
                name="Quiz file exists",
                passed=False,
                expected=gt["quiz"]["file"],
                actual="NOT FOUND",
            )
        )
        return results

    # Try to load and validate structure
    try:
        import yaml

        with open(quiz_path, encoding="utf-8") as f:
            quiz_data = yaml.safe_load(f)

        # Check question count
        actual_questions = len(quiz_data.get("questions", []))
        expected_questions = gt["quiz"]["total_questions"]
        passed = actual_questions >= expected_questions

        results.append(
            ValidationResult(
                name="Quiz question count",
                passed=passed,
                expected=f">= {expected_questions}",
                actual=actual_questions,
            )
        )

    except ImportError:
        results.append(
            ValidationResult(
                name="Quiz structure",
                passed=False,
                expected="PyYAML installed",
                actual="PyYAML not available",
                message="Install with: pip install pyyaml",
            )
        )
    except Exception as e:
        results.append(
            ValidationResult(
                name="Quiz structure",
                passed=False,
                expected="valid YAML",
                actual=str(e),
            )
        )

    return results


def validate_lo_coverage(gt: Dict[str, Any]) -> List[ValidationResult]:
    """Verify all Learning Objectives have documented artifacts."""
    results = []

    for lo_id, lo_data in gt["learning_objectives"].items():
        artifacts = lo_data.get("artifacts", [])
        passed = len(artifacts) >= 3  # Minimum: theory, exercise, assessment

        results.append(
            ValidationResult(
                name=f"{lo_id} artifact coverage",
                passed=passed,
                expected=">= 3 artifacts",
                actual=len(artifacts),
                message=f"{lo_id}: {lo_data['description'][:50]}...",
            )
        )

    return results


def validate_network_config(gt: Dict[str, Any]) -> ValidationResult:
    """Verify network configuration is consistent."""
    env = gt["environment"]

    # Check subnet format is valid
    subnet = env["network_subnet"]
    try:
        import ipaddress

        network = ipaddress.ip_network(subnet)
        passed = True
        message = f"Valid network: {network.num_addresses} addresses"
    except (ImportError, ValueError) as e:
        passed = False
        message = str(e)

    return ValidationResult(
        name="Network configuration",
        passed=passed,
        expected=subnet,
        actual="valid" if passed else "invalid",
        message=message,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# REPORT GENERATION
# ═══════════════════════════════════════════════════════════════════════════════

def run_all_validations(gt: Dict[str, Any], quick: bool = False) -> ValidationReport:
    """
    Run all validation checks.

    Args:
        gt: Ground truth data
        quick: If True, skip slow checks

    Returns:
        Complete validation report
    """
    report = ValidationReport()
    report.ground_truth_version = gt["_meta"]["version"]

    # Collect all results
    all_results: List[ValidationResult] = []

    # Quick checks (always run)
    all_results.append(validate_python_version(gt))
    all_results.append(validate_network_config(gt))

    # Standard checks
    all_results.extend(validate_documentation_files(gt))
    all_results.extend(validate_quiz_structure(gt))
    all_results.extend(validate_lo_coverage(gt))

    # Slower checks (skip if quick mode)
    if not quick:
        all_results.extend(validate_exercise_files(gt))
        all_results.extend(validate_ports_in_compose(gt))

    # Compile report
    report.results = all_results
    report.total_checks = len(all_results)
    report.passed_checks = sum(1 for r in all_results if r.passed)
    report.failed_checks = report.total_checks - report.passed_checks

    return report


def print_report(report: ValidationReport) -> None:
    """Print validation report to terminal."""
    print()
    print(f"{Colours.CYAN}{'═' * 70}{Colours.RESET}")
    print(f"{Colours.BOLD}  Ground Truth Validation Report{Colours.RESET}")
    print(f"{Colours.CYAN}{'═' * 70}{Colours.RESET}")
    print()
    print(f"  Timestamp: {report.timestamp}")
    print(f"  Ground Truth Version: {report.ground_truth_version}")
    print()

    # Print each result
    for result in report.results:
        if result.passed:
            status = f"{Colours.GREEN}✅ PASS{Colours.RESET}"
        else:
            status = f"{Colours.RED}❌ FAIL{Colours.RESET}"

        print(f"  {status}  {result.name}")
        print(f"         Expected: {result.expected}")
        print(f"         Actual:   {result.actual}")
        if result.message:
            print(f"         Note:     {result.message}")
        print()

    # Summary
    print(f"{Colours.CYAN}{'─' * 70}{Colours.RESET}")
    print()
    print(f"  {Colours.BOLD}Summary:{Colours.RESET}")
    print(f"    Total Checks:  {report.total_checks}")
    print(f"    Passed:        {Colours.GREEN}{report.passed_checks}{Colours.RESET}")
    print(f"    Failed:        {Colours.RED}{report.failed_checks}{Colours.RESET}")
    print(f"    Success Rate:  {report.success_rate:.1f}%")
    print()

    if report.all_passed:
        print(f"  {Colours.GREEN}{Colours.BOLD}✅ ALL VALIDATIONS PASSED{Colours.RESET}")
    else:
        print(f"  {Colours.RED}{Colours.BOLD}❌ SOME VALIDATIONS FAILED{Colours.RESET}")

    print()
    print(f"{Colours.CYAN}{'═' * 70}{Colours.RESET}")
    print()


def export_json_report(report: ValidationReport, output_path: Path) -> None:
    """Export validation report as JSON."""
    data = {
        "timestamp": report.timestamp,
        "ground_truth_version": report.ground_truth_version,
        "summary": {
            "total_checks": report.total_checks,
            "passed_checks": report.passed_checks,
            "failed_checks": report.failed_checks,
            "success_rate": report.success_rate,
            "all_passed": report.all_passed,
        },
        "results": [
            {
                "name": r.name,
                "passed": r.passed,
                "expected": str(r.expected),
                "actual": str(r.actual),
                "message": r.message,
            }
            for r in report.results
        ],
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Report exported to: {output_path}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """
    Main entry point for ground truth validation.

    Returns:
        0 if all validations passed, 1 otherwise
    """
    parser = argparse.ArgumentParser(
        description="Validate ground truth against actual kit contents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Full validation
  %(prog)s --quick            # Quick checks only
  %(prog)s --json             # Output as JSON
  %(prog)s --output report.json  # Save JSON report
        """,
    )
    parser.add_argument(
        "--quick", "-q",
        action="store_true",
        help="Skip slow checks (file line counts, Docker compose)",
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output report as JSON to stdout",
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Save JSON report to file",
    )

    args = parser.parse_args()

    try:
        gt = load_ground_truth()
    except FileNotFoundError as e:
        print(f"{Colours.RED}Error: {e}{Colours.RESET}")
        return 1
    except json.JSONDecodeError as e:
        print(f"{Colours.RED}Error parsing ground truth: {e}{Colours.RESET}")
        return 1

    report = run_all_validations(gt, quick=args.quick)

    if args.json:
        # Output JSON to stdout
        import json as json_module

        data = {
            "all_passed": report.all_passed,
            "success_rate": report.success_rate,
            "failed": [r.name for r in report.results if not r.passed],
        }
        print(json_module.dumps(data, indent=2))
    else:
        print_report(report)

    if args.output:
        export_json_report(report, args.output)

    return 0 if report.all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
