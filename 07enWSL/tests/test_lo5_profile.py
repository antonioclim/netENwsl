#!/usr/bin/env python3
"""
Test Suite for LO5: Design Custom Firewall Profiles
====================================================
NETWORKING class - ASE, Informatics | Computer Networks Laboratory

This module provides thorough tests for Learning Objective 5:
"Design custom firewall profiles that enforce specific traffic policies"

Tests validate:
    - Profile JSON structure and schema
    - Rule ordering logic (first-match-wins)
    - Profile application correctness
    - Policy inheritance and defaults
    - Conflict detection

Usage:
    pytest tests/test_lo5_profile.py -v
    python3 tests/test_lo5_profile.py --all

Requirements:
    pip install pytest
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# ═══════════════════════════════════════════════════════════════════════════════
# TEST DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ProfileValidationResult:
    """Result of profile validation."""
    valid: bool
    errors: list[str]
    warnings: list[str]
    
    def __bool__(self) -> bool:
        return self.valid


@dataclass
class RuleMatchResult:
    """Result of rule matching simulation."""
    matched: bool
    rule_index: Optional[int]
    action: Optional[str]
    reason: str


# ═══════════════════════════════════════════════════════════════════════════════
# PROFILE SCHEMA VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

PROFILE_SCHEMA = {
    "required_fields": ["name", "description", "rules"],
    "optional_fields": ["forward_policy", "input_policy", "output_policy", "enabled"],
    "rule_required_fields": ["action"],
    "rule_optional_fields": ["chain", "proto", "src", "dst", "sport", "dport", "comment"],
    "valid_actions": ["ACCEPT", "DROP", "REJECT", "LOG"],
    "valid_chains": ["INPUT", "OUTPUT", "FORWARD"],
    "valid_protocols": ["tcp", "udp", "icmp", "all"],
    "valid_policies": ["ACCEPT", "DROP"],
}


def validate_profile_schema(profile: dict[str, Any]) -> ProfileValidationResult:
    """
    Validate a firewall profile against the expected schema.
    
    Args:
        profile: Dictionary containing profile configuration
        
    Returns:
        ProfileValidationResult with validation status and messages
    """
    errors = []
    warnings = []
    
    # Check required fields
    for field in PROFILE_SCHEMA["required_fields"]:
        if field not in profile:
            errors.append(f"Missing required field: {field}")
    
    # Check for unknown fields
    all_known = set(PROFILE_SCHEMA["required_fields"] + PROFILE_SCHEMA["optional_fields"])
    for field in profile:
        if field not in all_known:
            warnings.append(f"Unknown field: {field}")
    
    # Validate rules if present
    if "rules" in profile:
        if not isinstance(profile["rules"], list):
            errors.append("Field 'rules' must be a list")
        else:
            for i, rule in enumerate(profile["rules"]):
                rule_errors = _validate_rule(rule, i)
                errors.extend(rule_errors)
    
    # Validate policies
    for policy_field in ["forward_policy", "input_policy", "output_policy"]:
        if policy_field in profile:
            if profile[policy_field] not in PROFILE_SCHEMA["valid_policies"]:
                errors.append(f"Invalid {policy_field}: {profile[policy_field]}")
    
    return ProfileValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings
    )


def _validate_rule(rule: dict[str, Any], index: int) -> list[str]:
    """Validate a single rule entry."""
    errors = []
    prefix = f"Rule[{index}]"
    
    # Check required fields
    for field in PROFILE_SCHEMA["rule_required_fields"]:
        if field not in rule:
            errors.append(f"{prefix}: Missing required field '{field}'")
    
    # Validate action
    if "action" in rule:
        if rule["action"] not in PROFILE_SCHEMA["valid_actions"]:
            errors.append(f"{prefix}: Invalid action '{rule['action']}'")
    
    # Validate chain
    if "chain" in rule:
        if rule["chain"] not in PROFILE_SCHEMA["valid_chains"]:
            errors.append(f"{prefix}: Invalid chain '{rule['chain']}'")
    
    # Validate protocol
    if "proto" in rule:
        if rule["proto"] not in PROFILE_SCHEMA["valid_protocols"]:
            errors.append(f"{prefix}: Invalid protocol '{rule['proto']}'")
    
    # Validate port numbers
    for port_field in ["sport", "dport"]:
        if port_field in rule:
            port = rule[port_field]
            if isinstance(port, int):
                if not (1 <= port <= 65535):
                    errors.append(f"{prefix}: Invalid {port_field} '{port}' (must be 1-65535)")
            elif isinstance(port, str):
                # Allow port ranges like "8000:8100"
                if ":" in port:
                    try:
                        start, end = port.split(":")
                        if not (1 <= int(start) <= 65535 and 1 <= int(end) <= 65535):
                            errors.append(f"{prefix}: Invalid port range in {port_field}")
                    except ValueError:
                        errors.append(f"{prefix}: Invalid port range format in {port_field}")
    
    return errors


# ═══════════════════════════════════════════════════════════════════════════════
# RULE ORDERING TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def simulate_rule_matching(
    rules: list[dict[str, Any]],
    packet: dict[str, Any]
) -> RuleMatchResult:
    """
    Simulate iptables first-match-wins rule matching.
    
    Args:
        rules: List of firewall rules in order
        packet: Simulated packet attributes
        
    Returns:
        RuleMatchResult indicating which rule matched (if any)
    """
    for i, rule in enumerate(rules):
        if _rule_matches_packet(rule, packet):
            return RuleMatchResult(
                matched=True,
                rule_index=i,
                action=rule.get("action", "ACCEPT"),
                reason=f"Matched rule {i}: {rule.get('comment', 'no comment')}"
            )
    
    return RuleMatchResult(
        matched=False,
        rule_index=None,
        action=None,
        reason="No rule matched - default policy applies"
    )


def _rule_matches_packet(rule: dict[str, Any], packet: dict[str, Any]) -> bool:
    """Check if a rule matches a packet's attributes."""
    # Protocol match
    if "proto" in rule and rule["proto"] != "all":
        if packet.get("proto") != rule["proto"]:
            return False
    
    # Source IP match (simplified - exact match only)
    if "src" in rule:
        if packet.get("src") != rule["src"] and rule["src"] != "0.0.0.0/0":
            return False
    
    # Destination IP match
    if "dst" in rule:
        if packet.get("dst") != rule["dst"] and rule["dst"] != "0.0.0.0/0":
            return False
    
    # Destination port match
    if "dport" in rule:
        if packet.get("dport") != rule["dport"]:
            return False
    
    # Source port match
    if "sport" in rule:
        if packet.get("sport") != rule["sport"]:
            return False
    
    return True


def test_rule_ordering_specific_before_general() -> tuple[bool, str]:
    """
    Test that specific rules placed before general rules work correctly.
    
    Expected behaviour: TCP port 9090 should be ACCEPTed even when
    a general TCP DROP rule exists, IF the ACCEPT rule comes first.
    """
    rules = [
        {"proto": "tcp", "dport": 9090, "action": "ACCEPT", "comment": "Allow TCP 9090"},
        {"proto": "tcp", "action": "DROP", "comment": "Drop all other TCP"},
    ]
    
    # Test packet to port 9090 - should be accepted
    packet_9090 = {"proto": "tcp", "dport": 9090, "src": "10.0.7.11", "dst": "10.0.7.100"}
    result = simulate_rule_matching(rules, packet_9090)
    
    if not result.matched or result.action != "ACCEPT":
        return False, f"TCP 9090 should be ACCEPT but got: {result}"
    
    # Test packet to port 8080 - should be dropped
    packet_8080 = {"proto": "tcp", "dport": 8080, "src": "10.0.7.11", "dst": "10.0.7.100"}
    result = simulate_rule_matching(rules, packet_8080)
    
    if not result.matched or result.action != "DROP":
        return False, f"TCP 8080 should be DROP but got: {result}"
    
    return True, "Specific-before-general ordering works correctly"


def test_rule_ordering_wrong_order() -> tuple[bool, str]:
    """
    Test that wrong rule ordering causes expected (incorrect) behaviour.
    
    This demonstrates WHY rule order matters - if DROP comes first,
    the specific ACCEPT rule never gets evaluated.
    """
    rules = [
        {"proto": "tcp", "action": "DROP", "comment": "Drop all TCP (wrong position)"},
        {"proto": "tcp", "dport": 9090, "action": "ACCEPT", "comment": "Allow TCP 9090 (unreachable)"},
    ]
    
    # Test packet to port 9090 - SHOULD be dropped due to wrong order
    packet = {"proto": "tcp", "dport": 9090}
    result = simulate_rule_matching(rules, packet)
    
    if result.action == "DROP":
        return True, "Confirmed: Wrong ordering causes DROP of allowed port"
    
    return False, f"Expected DROP due to wrong order, got: {result.action}"


def test_protocol_specific_matching() -> tuple[bool, str]:
    """Test that protocol-specific rules only match correct protocols."""
    rules = [
        {"proto": "tcp", "dport": 9090, "action": "ACCEPT"},
        {"proto": "udp", "dport": 9091, "action": "ACCEPT"},
        {"action": "DROP", "comment": "Default drop"},
    ]
    
    # TCP to 9090 - should accept
    tcp_packet = {"proto": "tcp", "dport": 9090}
    tcp_result = simulate_rule_matching(rules, tcp_packet)
    
    # UDP to 9090 - should drop (no UDP rule for 9090)
    udp_wrong = {"proto": "udp", "dport": 9090}
    udp_result = simulate_rule_matching(rules, udp_wrong)
    
    # UDP to 9091 - should accept
    udp_right = {"proto": "udp", "dport": 9091}
    udp_right_result = simulate_rule_matching(rules, udp_right)
    
    if tcp_result.action != "ACCEPT":
        return False, f"TCP 9090 should ACCEPT: {tcp_result}"
    
    if udp_result.action != "DROP":
        return False, f"UDP 9090 should DROP: {udp_result}"
    
    if udp_right_result.action != "ACCEPT":
        return False, f"UDP 9091 should ACCEPT: {udp_right_result}"
    
    return True, "Protocol-specific matching works correctly"


# ═══════════════════════════════════════════════════════════════════════════════
# PROFILE FILE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_load_profile_file() -> tuple[bool, str]:
    """Test loading the actual firewall_profiles.json file."""
    profile_path = PROJECT_ROOT / "docker" / "configs" / "firewall_profiles.json"
    
    if not profile_path.exists():
        return False, f"Profile file not found: {profile_path}"
    
    try:
        with open(profile_path) as f:
            profiles = json.load(f)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    
    if not isinstance(profiles, dict):
        return False, "Profiles should be a dictionary"
    
    # Validate each profile
    errors = []
    for name, profile in profiles.items():
        result = validate_profile_schema(profile)
        if not result.valid:
            errors.extend([f"{name}: {e}" for e in result.errors])
    
    if errors:
        return False, f"Profile validation errors: {errors}"
    
    return True, f"Loaded and validated {len(profiles)} profiles"


def test_profile_has_required_profiles() -> tuple[bool, str]:
    """Test that required profiles exist for laboratory exercises."""
    profile_path = PROJECT_ROOT / "docker" / "configs" / "firewall_profiles.json"
    
    if not profile_path.exists():
        return False, f"Profile file not found"
    
    with open(profile_path) as f:
        profiles = json.load(f)
    
    required = ["allow_all", "block_tcp_9090", "block_udp_9091"]
    missing = [p for p in required if p not in profiles]
    
    if missing:
        return False, f"Missing required profiles: {missing}"
    
    return True, f"All required profiles present: {required}"


# ═══════════════════════════════════════════════════════════════════════════════
# CONFLICT DETECTION
# ═══════════════════════════════════════════════════════════════════════════════

def detect_rule_conflicts(rules: list[dict[str, Any]]) -> list[str]:
    """
    Detect potential conflicts or redundancies in rule set.
    
    Conflicts include:
        - Unreachable rules (shadowed by earlier rules)
        - Redundant rules (same effect as earlier rules)
        - Contradictory rules (different actions for same traffic)
    """
    conflicts = []
    
    for i, rule_a in enumerate(rules):
        for j, rule_b in enumerate(rules[i+1:], start=i+1):
            # Check if rule_a shadows rule_b
            if _rule_shadows(rule_a, rule_b):
                conflicts.append(
                    f"Rule {i} shadows Rule {j}: "
                    f"{rule_a.get('comment', 'no comment')} shadows "
                    f"{rule_b.get('comment', 'no comment')}"
                )
    
    return conflicts


def _rule_shadows(rule_a: dict, rule_b: dict) -> bool:
    """Check if rule_a completely shadows rule_b."""
    # A general rule shadows a more specific rule if:
    # - A has fewer constraints than B
    # - All of A's constraints are also in B
    
    constraint_fields = ["proto", "src", "dst", "sport", "dport"]
    
    a_constraints = {f: rule_a.get(f) for f in constraint_fields if f in rule_a}
    b_constraints = {f: rule_b.get(f) for f in constraint_fields if f in rule_b}
    
    # If A has no constraints, it shadows everything
    if not a_constraints and b_constraints:
        return True
    
    # If A's constraints are a subset of B's
    for field, value in a_constraints.items():
        if field in b_constraints:
            if b_constraints[field] != value:
                return False
        # A has a constraint B doesn't - A is more specific
        else:
            return False
    
    return True


def test_conflict_detection() -> tuple[bool, str]:
    """Test the conflict detection mechanism."""
    rules_with_conflict = [
        {"action": "DROP", "comment": "Drop everything"},
        {"proto": "tcp", "dport": 9090, "action": "ACCEPT", "comment": "Unreachable!"},
    ]
    
    conflicts = detect_rule_conflicts(rules_with_conflict)
    
    if not conflicts:
        return False, "Should detect that rule 0 shadows rule 1"
    
    return True, f"Conflict detection working: {conflicts[0]}"


# ═══════════════════════════════════════════════════════════════════════════════
# HOMEWORK VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

def validate_homework_profile(profile_path: Path) -> ProfileValidationResult:
    """
    Validate a student-submitted homework profile.
    
    This function is used by the homework grading system to check
    that submitted profiles meet the requirements.
    
    Args:
        profile_path: Path to student's JSON profile file
        
    Returns:
        ProfileValidationResult with detailed feedback
    """
    errors = []
    warnings = []
    
    # Check file exists
    if not profile_path.exists():
        return ProfileValidationResult(
            valid=False,
            errors=[f"File not found: {profile_path}"],
            warnings=[]
        )
    
    # Load and parse JSON
    try:
        with open(profile_path) as f:
            profile = json.load(f)
    except json.JSONDecodeError as e:
        return ProfileValidationResult(
            valid=False,
            errors=[f"Invalid JSON syntax: {e}"],
            warnings=[]
        )
    
    # Validate schema
    schema_result = validate_profile_schema(profile)
    errors.extend(schema_result.errors)
    warnings.extend(schema_result.warnings)
    
    # Additional homework-specific checks
    if "rules" in profile:
        if len(profile["rules"]) < 3:
            warnings.append("Homework requires at least 3 rules")
        
        # Check for variety in actions
        actions_used = set(r.get("action") for r in profile["rules"])
        if len(actions_used) < 2:
            warnings.append("Consider using multiple action types")
    
    # Check for documentation
    if "description" in profile:
        if len(profile["description"]) < 20:
            warnings.append("Description should be more detailed")
    
    return ProfileValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings
    )


# ═══════════════════════════════════════════════════════════════════════════════
# TEST RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

ALL_TESTS = [
    ("Schema: Validate profile structure", lambda: test_load_profile_file()),
    ("Schema: Required profiles exist", lambda: test_profile_has_required_profiles()),
    ("Ordering: Specific before general", lambda: test_rule_ordering_specific_before_general()),
    ("Ordering: Wrong order demonstration", lambda: test_rule_ordering_wrong_order()),
    ("Matching: Protocol-specific rules", lambda: test_protocol_specific_matching()),
    ("Conflict: Detection mechanism", lambda: test_conflict_detection()),
]


def run_all_tests(verbose: bool = True) -> tuple[int, int]:
    """
    Run all LO5 tests.
    
    Args:
        verbose: Print detailed output
        
    Returns:
        Tuple of (passed_count, total_count)
    """
    passed = 0
    total = len(ALL_TESTS)
    
    if verbose:
        print("=" * 70)
        print("LO5 Tests: Design Custom Firewall Profiles")
        print("=" * 70)
        print()
    
    for name, test_func in ALL_TESTS:
        try:
            success, message = test_func()
            if success:
                passed += 1
                status = "✓ PASS"
            else:
                status = "✗ FAIL"
            
            if verbose:
                print(f"{status}: {name}")
                print(f"       {message}")
                print()
        except Exception as e:
            if verbose:
                print(f"✗ ERROR: {name}")
                print(f"       Exception: {e}")
                print()
    
    if verbose:
        print("=" * 70)
        print(f"Results: {passed}/{total} tests passed")
        print("=" * 70)
    
    return passed, total


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="LO5 Profile Tests")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--quiet", "-q", action="store_true", help="Minimal output")
    parser.add_argument("--validate", type=Path, help="Validate a homework profile")
    args = parser.parse_args()
    
    if args.validate:
        result = validate_homework_profile(args.validate)
        print(f"Valid: {result.valid}")
        if result.errors:
            print(f"Errors: {result.errors}")
        if result.warnings:
            print(f"Warnings: {result.warnings}")
        return 0 if result.valid else 1
    
    passed, total = run_all_tests(verbose=not args.quiet)
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())


# ═══════════════════════════════════════════════════════════════════════════════
# PYTEST INTEGRATION
# ═══════════════════════════════════════════════════════════════════════════════

import pytest


@pytest.mark.lo5
class TestProfileSchema:
    """Pytest class for profile schema tests."""
    
    def test_load_profile_file(self):
        success, msg = test_load_profile_file()
        assert success, msg
    
    def test_required_profiles_exist(self):
        success, msg = test_profile_has_required_profiles()
        assert success, msg


@pytest.mark.lo5
class TestRuleOrdering:
    """Pytest class for rule ordering tests."""
    
    def test_specific_before_general(self):
        success, msg = test_rule_ordering_specific_before_general()
        assert success, msg
    
    def test_wrong_order_demonstration(self):
        success, msg = test_rule_ordering_wrong_order()
        assert success, msg
    
    def test_protocol_specific_matching(self):
        success, msg = test_protocol_specific_matching()
        assert success, msg


@pytest.mark.lo5
class TestConflictDetection:
    """Pytest class for conflict detection tests."""
    
    def test_conflict_detection_works(self):
        success, msg = test_conflict_detection()
        assert success, msg
