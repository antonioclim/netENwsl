#!/usr/bin/env python3
"""
Firewall Profile Validator Tests — Week 7
==========================================
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Unit tests for firewall profile validation including schema checking
and rule ordering verification.

Usage:
    python3 -m pytest tests/test_validator.py -v
    python3 tests/test_validator.py
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# ═══════════════════════════════════════════════════════════════════════════════
# TEST DATA
# ═══════════════════════════════════════════════════════════════════════════════

VALID_PROFILE = {
    "baseline": {
        "description": "Allow all traffic",
        "forward_policy": "ACCEPT",
        "rules": []
    },
    "block_tcp_9090": {
        "description": "Block TCP port 9090",
        "forward_policy": "ACCEPT",
        "rules": [
            {"chain": "FORWARD", "proto": "tcp", "dport": 9090, "action": "DROP"}
        ]
    }
}

INVALID_PROFILE_MISSING_ACTION = {
    "broken": {
        "rules": [
            {"chain": "FORWARD", "proto": "tcp", "dport": 9090}
        ]
    }
}

SHADOWED_RULES_PROFILE = {
    "shadowed": {
        "description": "Rules where specific is after general",
        "forward_policy": "ACCEPT",
        "rules": [
            {"chain": "FORWARD", "proto": "tcp", "action": "DROP"},
            {"chain": "FORWARD", "proto": "tcp", "dport": 9090, "action": "ACCEPT"}
        ]
    }
}


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def validate_rule_schema(rule: dict) -> list[str]:
    """
    Validate a single firewall rule against expected schema.
    
    Args:
        rule: Dictionary containing rule specification
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    # Check required action field
    if "action" not in rule:
        errors.append("Rule missing required 'action' field")
    elif rule["action"] not in {"ACCEPT", "DROP", "REJECT", "LOG"}:
        errors.append(f"Invalid action: {rule['action']}")
    
    # Check chain if present
    if "chain" in rule and rule["chain"] not in {"INPUT", "OUTPUT", "FORWARD"}:
        errors.append(f"Invalid chain: {rule['chain']}")
    
    # Check protocol if present
    if "proto" in rule and rule["proto"] not in {"tcp", "udp", "icmp", "all"}:
        errors.append(f"Invalid protocol: {rule['proto']}")
    
    # Check port is numeric if present
    if "dport" in rule:
        if not isinstance(rule["dport"], int) or rule["dport"] < 1 or rule["dport"] > 65535:
            errors.append(f"Invalid port: {rule['dport']}")
    
    return errors


def validate_profile_schema(profile: dict) -> list[str]:
    """
    Validate a firewall profile against expected schema.
    
    Args:
        profile: Profile dictionary with rules and policy
        
    Returns:
        List of validation error messages
    """
    errors = []
    
    # Check forward_policy if present
    if "forward_policy" in profile:
        if profile["forward_policy"] not in {"ACCEPT", "DROP", "REJECT"}:
            errors.append(f"Invalid forward_policy: {profile['forward_policy']}")
    
    # Validate each rule
    for i, rule in enumerate(profile.get("rules", [])):
        rule_errors = validate_rule_schema(rule)
        for err in rule_errors:
            errors.append(f"Rule {i}: {err}")
    
    return errors


def check_rule_shadowing(rules: list[dict]) -> list[str]:
    """
    Check if any rules are shadowed by earlier rules.
    
    A rule is shadowed if a more general rule appears before it
    and would match the same traffic.
    
    Args:
        rules: List of rule dictionaries
        
    Returns:
        List of warning messages about shadowed rules
    """
    warnings = []
    
    for i, rule in enumerate(rules):
        for j, earlier in enumerate(rules[:i]):
            if rule_is_shadowed_by(rule, earlier):
                warnings.append(
                    f"Rule {i} may be shadowed by rule {j}: "
                    f"specific rule after general rule"
                )
    
    return warnings


def rule_is_shadowed_by(specific: dict, general: dict) -> bool:
    """
    Check if a specific rule would be shadowed by a general rule.
    
    Args:
        specific: The potentially shadowed rule
        general: The earlier, potentially shadowing rule
        
    Returns:
        True if specific would be shadowed
    """
    # Same chain required
    if specific.get("chain", "FORWARD") != general.get("chain", "FORWARD"):
        return False
    
    # Same protocol or general catches all
    spec_proto = specific.get("proto")
    gen_proto = general.get("proto")
    
    if gen_proto and spec_proto and gen_proto != spec_proto:
        return False
    
    # If general has no port but specific does, general shadows specific
    if "dport" not in general and "dport" in specific:
        if gen_proto is None or gen_proto == spec_proto:
            return True
    
    return False


# ═══════════════════════════════════════════════════════════════════════════════
# TEST FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def test_valid_profile_passes():
    """Test that valid profiles pass validation."""
    for name, profile in VALID_PROFILE.items():
        errors = validate_profile_schema(profile)
        assert len(errors) == 0, f"Profile '{name}' should be valid: {errors}"
    
    print("✓ Valid profile test passed")
    return True


def test_missing_action_detected():
    """Test that missing action field is detected."""
    for name, profile in INVALID_PROFILE_MISSING_ACTION.items():
        errors = validate_profile_schema(profile)
        assert len(errors) > 0, f"Profile '{name}' should have errors"
        assert any("action" in e.lower() for e in errors), "Should detect missing action"
    
    print("✓ Missing action detection test passed")
    return True


def test_shadowed_rules_detected():
    """Test that shadowed rules are detected."""
    profile = SHADOWED_RULES_PROFILE["shadowed"]
    warnings = check_rule_shadowing(profile["rules"])
    
    assert len(warnings) > 0, "Should detect shadowed rule"
    assert any("shadowed" in w.lower() for w in warnings), "Should mention shadowing"
    
    print("✓ Shadowed rules detection test passed")
    return True


def test_invalid_port_detected():
    """Test that invalid port numbers are detected."""
    rule = {"chain": "FORWARD", "proto": "tcp", "dport": 99999, "action": "DROP"}
    errors = validate_rule_schema(rule)
    
    assert len(errors) > 0, "Should detect invalid port"
    assert any("port" in e.lower() for e in errors), "Should mention port"
    
    print("✓ Invalid port detection test passed")
    return True


def test_invalid_protocol_detected():
    """Test that invalid protocols are detected."""
    rule = {"chain": "FORWARD", "proto": "invalid", "action": "DROP"}
    errors = validate_rule_schema(rule)
    
    assert len(errors) > 0, "Should detect invalid protocol"
    assert any("protocol" in e.lower() for e in errors), "Should mention protocol"
    
    print("✓ Invalid protocol detection test passed")
    return True


def test_profile_file_loading():
    """Test loading and validating profile from file."""
    # Create temp file with valid profile
    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.json',
        delete=False,
        encoding='utf-8'
    ) as f:
        json.dump(VALID_PROFILE, f)
        temp_path = Path(f.name)
    
    try:
        # Load and validate
        with open(temp_path, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
        
        for name, profile in loaded.items():
            errors = validate_profile_schema(profile)
            assert len(errors) == 0, f"Loaded profile '{name}' should be valid"
        
        print("✓ Profile file loading test passed")
        return True
        
    finally:
        temp_path.unlink()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def run_all_tests() -> int:
    """Run all validator tests."""
    tests = [
        test_valid_profile_passes,
        test_missing_action_detected,
        test_shadowed_rules_detected,
        test_invalid_port_detected,
        test_invalid_protocol_detected,
        test_profile_file_loading,
    ]
    
    print("=" * 60)
    print("Firewall Profile Validator Tests — Week 7")
    print("=" * 60)
    print()
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            result = test()
            if result:
                passed += 1
            else:
                failed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__}: {e}")
            failed += 1
    
    print()
    print("-" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
