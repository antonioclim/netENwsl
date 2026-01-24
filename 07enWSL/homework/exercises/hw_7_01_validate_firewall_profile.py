#!/usr/bin/env python3
"""
Homework Exercise 7.01: Custom Firewall Profile Design
======================================================
Computer Networks - Week 7 (WSL Environment)
ASE Bucharest, CSIE | by ing. dr. Antonio Clim

Objective:
Design and implement a custom firewall profile that demonstrates understanding
of packet filtering semantics and the behavioural distinction between REJECT
and DROP actions.

Requirements:
1. Create a new profile in configs/firewall_profiles.json
2. The profile must include at least 3 rules
3. At least one rule must use REJECT action
4. At least one rule must use DROP action
5. Document the reasoning for each rule

Deliverables:
- Modified firewall_profiles.json with your custom profile
- A written analysis (500-750 words) explaining:
  - Your profile's purpose and threat model
  - Why you chose REJECT vs DROP for each rule
  - Expected observable behaviour in Wireshark captures
  - Trade-offs between security and usability in your design

Level: Intermediate
Estimated time: 60-90 minutes

Pair Programming Notes:
- Driver: Edit JSON file and run validation
- Navigator: Review rule logic and check documentation
- Swap after: Profile creation, before testing
"""

from __future__ import annotations

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import json
from pathlib import Path
from typing import List, Dict, Any


# ═══════════════════════════════════════════════════════════════════════════════
# PROFILE_TEMPLATE
# ═══════════════════════════════════════════════════════════════════════════════
# Template for a custom firewall profile
# Copy this structure into firewall_profiles.json and customise
CUSTOM_PROFILE_TEMPLATE: Dict[str, Any] = {
    "name": "hw_custom_profile",
    "description": "Student-designed firewall profile for homework 7.01",
    "rules": [
        {
            "protocol": "tcp",
            "port": 0,        # Replace with your chosen port
            "action": "REJECT",
            "comment": "Explain why REJECT is appropriate here"
        },
        {
            "protocol": "udp",
            "port": 0,        # Replace with your chosen port
            "action": "DROP",
            "comment": "Explain why DROP is appropriate here"
        },
        {
            "protocol": "tcp",
            "port": 0,        # Replace with your chosen port
            "action": "ACCEPT",
            "comment": "Explain why this traffic should be allowed"
        }
    ]
}


# ═══════════════════════════════════════════════════════════════════════════════
# PREDICTION_PROMPT
# ═══════════════════════════════════════════════════════════════════════════════
def prompt_prediction() -> None:
    """
    Display prediction prompts before validation.
    
    Implements Brown & Wilson Principle 4: Predictions.
    """
    print()
    print("💭 PREDICTION: Before running the validator, consider:")
    print("   1. Does your profile have at least 3 rules?")
    print("   2. Do you have at least one REJECT and one DROP action?")
    print("   3. Does each rule have a descriptive comment (10+ characters)?")
    print()
    input("   Press Enter after reviewing your profile...")
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# FILE_OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════════
def load_profiles(path: Path) -> Dict[str, Any]:
    """
    Load existing firewall profiles from JSON file.
    
    Args:
        path: Path to firewall_profiles.json
        
    Returns:
        Dictionary containing all profiles
        
    Raises:
        FileNotFoundError: If file does not exist
        json.JSONDecodeError: If file is invalid JSON
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATION_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def validate_profile(profile: Dict[str, Any]) -> List[str]:
    """
    Validate a firewall profile against homework requirements.
    
    Requirements checked:
    - Must have 'name', 'description' and 'rules' fields
    - Must have at least 3 rules
    - Must have at least one REJECT action
    - Must have at least one DROP action
    - Each rule must have protocol, port, action and comment fields
    - Comments must be at least 10 characters (meaningful)
    
    Args:
        profile: Dictionary containing profile definition
        
    Returns:
        List of validation issues (empty if valid)
    """
    issues: List[str] = []
    
    # ═══════════════════════════════════════════════════════════════════════════
    # CHECK_REQUIRED_FIELDS
    # ═══════════════════════════════════════════════════════════════════════════
    if "name" not in profile:
        issues.append("Profile missing 'name' field")
    if "description" not in profile:
        issues.append("Profile missing 'description' field")
    if "rules" not in profile:
        issues.append("Profile missing 'rules' field")
        return issues  # Can't continue without rules
    
    rules = profile.get("rules", [])
    
    # ═══════════════════════════════════════════════════════════════════════════
    # CHECK_RULE_COUNT
    # ═══════════════════════════════════════════════════════════════════════════
    if len(rules) < 3:
        issues.append(f"Profile has {len(rules)} rules, minimum is 3")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # CHECK_ACTION_VARIETY
    # ═══════════════════════════════════════════════════════════════════════════
    actions = [r.get("action", "").upper() for r in rules]
    
    if "REJECT" not in actions:
        issues.append("Profile must include at least one REJECT rule")
    if "DROP" not in actions:
        issues.append("Profile must include at least one DROP rule")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # CHECK_INDIVIDUAL_RULES
    # ═══════════════════════════════════════════════════════════════════════════
    for i, rule in enumerate(rules):
        rule_num = i + 1
        
        if "protocol" not in rule:
            issues.append(f"Rule {rule_num} missing 'protocol' field")
        elif rule["protocol"] not in ("tcp", "udp", "icmp"):
            issues.append(f"Rule {rule_num} has invalid protocol: {rule['protocol']}")
            
        if "port" not in rule:
            issues.append(f"Rule {rule_num} missing 'port' field")
        elif not isinstance(rule["port"], int) or rule["port"] < 0:
            issues.append(f"Rule {rule_num} has invalid port: {rule['port']}")
            
        if "action" not in rule:
            issues.append(f"Rule {rule_num} missing 'action' field")
        elif rule["action"].upper() not in ("ACCEPT", "REJECT", "DROP"):
            issues.append(f"Rule {rule_num} has invalid action: {rule['action']}")
            
        if "comment" not in rule:
            issues.append(f"Rule {rule_num} missing 'comment' field")
        elif len(rule.get("comment", "")) < 10:
            issues.append(f"Rule {rule_num} needs a more descriptive comment (min 10 chars)")
    
    return issues


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """
    Main entry point for homework validator.
    
    Returns:
        Exit code (0 = valid profile found, 1 = error or no profile)
    """
    # ═══════════════════════════════════════════════════════════════════════════
    # DISPLAY_HEADER
    # ═══════════════════════════════════════════════════════════════════════════
    print("=" * 70)
    print("Homework 7.01: Custom Firewall Profile Validator")
    print("Computer Networks - Week 7 | ASE Bucharest, CSIE")
    print("=" * 70)
    print()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # LOCATE_PROFILES_FILE
    # ═══════════════════════════════════════════════════════════════════════════
    project_root = Path(__file__).parent.parent.parent
    profiles_path = project_root / "docker" / "configs" / "firewall_profiles.json"
    
    if not profiles_path.exists():
        print(f"❌ ERROR: Profiles file not found: {profiles_path}")
        print()
        print("Make sure you are running this from the correct directory.")
        return 1
    
    # ═══════════════════════════════════════════════════════════════════════════
    # LOAD_AND_SEARCH_PROFILES
    # ═══════════════════════════════════════════════════════════════════════════
    try:
        profiles = load_profiles(profiles_path)
    except json.JSONDecodeError as e:
        print(f"❌ ERROR: Invalid JSON in profiles file: {e}")
        return 1
    
    # Look for the student's custom profile
    custom_profile = None
    for profile in profiles.get("profiles", []):
        if profile.get("name", "").startswith("hw_"):
            custom_profile = profile
            break
    
    # ═══════════════════════════════════════════════════════════════════════════
    # HANDLE_NO_PROFILE
    # ═══════════════════════════════════════════════════════════════════════════
    if custom_profile is None:
        print("ℹ️  No custom profile found (name starting with 'hw_')")
        print()
        print("To complete this homework:")
        print("  1. Open docker/configs/firewall_profiles.json")
        print("  2. Add a new profile with name starting with 'hw_'")
        print("  3. Include at least 3 rules with REJECT and DROP actions")
        print("  4. Run this script again to validate")
        print()
        print("Template structure:")
        print("-" * 50)
        print(json.dumps(CUSTOM_PROFILE_TEMPLATE, indent=2))
        print("-" * 50)
        return 0
    
    # ═══════════════════════════════════════════════════════════════════════════
    # VALIDATE_PROFILE
    # ═══════════════════════════════════════════════════════════════════════════
    print(f"Found custom profile: {custom_profile.get('name')}")
    print()
    
    prompt_prediction()
    
    issues = validate_profile(custom_profile)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # DISPLAY_RESULTS
    # ═══════════════════════════════════════════════════════════════════════════
    if issues:
        print("❌ VALIDATION FAILED")
        print()
        print("Issues found:")
        for issue in issues:
            print(f"  • {issue}")
        print()
        print("Please fix these issues and run the validator again.")
        return 1
    else:
        print("✅ VALIDATION PASSED")
        print()
        print("Your profile structure is valid. Next steps:")
        print("  1. Test your profile:")
        print("     python scripts/run_demo.py --demo custom")
        print("  2. Capture traffic during testing")
        print("  3. Analyse the captures in Wireshark")
        print("  4. Write your analysis document")
        print()
        print("Questions to address in your analysis:")
        print("  • Why did you choose REJECT for some rules and DROP for others?")
        print("  • What differences do you observe in Wireshark for each action?")
        print("  • What are the debugging implications of your choices?")
        return 0


if __name__ == "__main__":
    exit(main())
