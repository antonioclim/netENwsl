#!/usr/bin/env python3
"""
Homework Exercise 7.01: Custom Firewall Profile Design
NETWORKING class - ASE, Informatics | by Revolvix

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

Starter Code:
Below is a template for your custom profile. Modify the firewall_profiles.json
file and add your profile following this structure.
"""

from __future__ import annotations

import json
from pathlib import Path

# Template for a custom firewall profile
CUSTOM_PROFILE_TEMPLATE = {
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


def load_profiles(path: Path) -> dict:
    """Load existing firewall profiles from JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_profile(profile: dict) -> list[str]:
    """
    Validate a firewall profile and return a list of issues.
    
    Requirements:
    - Must have 'name', 'description', and 'rules' fields
    - Must have at least 3 rules
    - Must have at least one REJECT action
    - Must have at least one DROP action
    """
    issues = []
    
    if "name" not in profile:
        issues.append("Profile missing 'name' field")
    if "description" not in profile:
        issues.append("Profile missing 'description' field")
    if "rules" not in profile:
        issues.append("Profile missing 'rules' field")
        return issues
    
    rules = profile.get("rules", [])
    
    if len(rules) < 3:
        issues.append(f"Profile has {len(rules)} rules, minimum is 3")
    
    actions = [r.get("action", "").upper() for r in rules]
    
    if "REJECT" not in actions:
        issues.append("Profile must include at least one REJECT rule")
    if "DROP" not in actions:
        issues.append("Profile must include at least one DROP rule")
    
    for i, rule in enumerate(rules):
        if "protocol" not in rule:
            issues.append(f"Rule {i+1} missing 'protocol' field")
        if "port" not in rule:
            issues.append(f"Rule {i+1} missing 'port' field")
        if "action" not in rule:
            issues.append(f"Rule {i+1} missing 'action' field")
        if "comment" not in rule or len(rule.get("comment", "")) < 10:
            issues.append(f"Rule {i+1} needs a descriptive comment")
    
    return issues


def main():
    """Validate student's custom firewall profile."""
    print("=" * 60)
    print("Homework 7.01: Custom Firewall Profile Validator")
    print("NETWORKING class - ASE, Informatics")
    print("=" * 60)
    print()
    
    project_root = Path(__file__).parent.parent.parent
    profiles_path = project_root / "docker" / "configs" / "firewall_profiles.json"
    
    if not profiles_path.exists():
        print(f"[ERROR] Profiles file not found: {profiles_path}")
        return 1
    
    profiles = load_profiles(profiles_path)
    
    # Look for the student's custom profile
    custom_profile = None
    for profile in profiles.get("profiles", []):
        if profile.get("name", "").startswith("hw_"):
            custom_profile = profile
            break
    
    if custom_profile is None:
        print("[INFO] No custom profile found (name starting with 'hw_')")
        print()
        print("To complete this homework:")
        print("1. Open docker/configs/firewall_profiles.json")
        print("2. Add a new profile with name starting with 'hw_'")
        print("3. Include at least 3 rules with REJECT and DROP actions")
        print("4. Run this script again to validate")
        print()
        print("Template structure:")
        print(json.dumps(CUSTOM_PROFILE_TEMPLATE, indent=2))
        return 0
    
    print(f"Found custom profile: {custom_profile.get('name')}")
    print()
    
    issues = validate_profile(custom_profile)
    
    if issues:
        print("[VALIDATION FAILED]")
        for issue in issues:
            print(f"  - {issue}")
        return 1
    else:
        print("[VALIDATION PASSED]")
        print()
        print("Profile structure is valid. Next steps:")
        print("1. Test your profile: python scripts/run_demo.py --demo custom")
        print("2. Capture traffic and analyse in Wireshark")
        print("3. Write your analysis document")
        return 0


if __name__ == "__main__":
    exit(main())
