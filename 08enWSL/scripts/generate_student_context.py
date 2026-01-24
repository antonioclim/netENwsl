#!/usr/bin/env python3
"""
Student Context Generator — Week 8 Laboratory
==============================================

Generates unique, deterministic context for each student based on their ID.
This context MUST be used in exercises and submissions.

Purpose:
    - Ensures each student has unique exercise parameters
    - Makes copied/AI-generated solutions detectable
    - Creates accountability through unique identifiers

Usage:
    make init ID=your.student.id
    
    Or directly:
    python scripts/generate_student_context.py "your.student.id"

Output:
    artifacts/student_context.json — Include this in your submission!

Course: Computer Networks — ASE, CSIE
"""

import argparse
import hashlib
import json
import random
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def generate_deterministic_seed(student_id: str) -> int:
    """
    Generate a deterministic seed from student ID.
    
    Same student ID always produces same seed but different
    students get different seeds.
    """
    hash_bytes = hashlib.sha256(student_id.lower().strip().encode()).digest()
    return int.from_bytes(hash_bytes[:4], byteorder='big')


def generate_student_context(student_id: str) -> dict[str, Any]:
    """
    Generate unique exercise context for a student.
    
    All values are deterministic based on student_id so:
    - Same student always gets same values
    - Different students get different values
    - Instructor can verify by regenerating
    
    Args:
        student_id: Student identifier (registration number or similar)
        
    Returns:
        Dictionary containing all unique exercise parameters
    """
    seed = generate_deterministic_seed(student_id)
    rng = random.Random(seed)
    
    # Generate session token (changes daily for freshness verification)
    today = datetime.now().strftime("%Y-%m-%d")
    session_hash = hashlib.sha256(f"{student_id}-{today}".encode()).hexdigest()
    
    # Unique port in safe range (avoiding common ports and Portainer 9000)
    unique_port = 9100 + (seed % 900)  # Range: 9100-9999
    
    # Backend weights for load balancer exercise
    # Ensures non-trivial distribution (not all equal)
    weights_base = [rng.randint(1, 10) for _ in range(3)]
    while len(set(weights_base)) == 1:  # Regenerate if all equal
        weights_base = [rng.randint(1, 10) for _ in range(3)]
    
    # Custom HTTP elements
    header_suffix = hashlib.md5(student_id.encode()).hexdigest()[:8].upper()
    custom_status = rng.choice([418, 451, 503, 507, 509])
    
    # Rate limiting parameters
    rate_limit_requests = rng.randint(5, 20)
    rate_limit_window = rng.randint(30, 120)
    
    # Test paths with student-specific segments
    student_segment = hashlib.md5(student_id.encode()).hexdigest()[:6]
    
    context = {
        # Identification
        "student_id": student_id,
        "student_hash": hashlib.sha256(student_id.encode()).hexdigest()[:16],
        "generated_at": datetime.now().isoformat(),
        "valid_date": today,
        "session_token": session_hash[:12],
        
        # Exercise 1: HTTP Server parameters
        "http_server": {
            "port": unique_port,
            "secret_header_name": "X-Student-Token",
            "secret_header_value": f"STU-{header_suffix}",
            "custom_status_code": custom_status,
            "custom_status_path": "/teapot",
            "custom_status_message": {
                418: "I'm a teapot",
                451: "Unavailable For Legal Reasons", 
                503: "Service Unavailable",
                507: "Insufficient Storage",
                509: "Bandwidth Limit Exceeded"
            }.get(custom_status, "Custom Status"),
        },
        
        # Exercise 2: Load Balancer parameters
        "load_balancer": {
            "weights": {
                "backend1": weights_base[0],
                "backend2": weights_base[1],
                "backend3": weights_base[2],
            },
            "total_weight": sum(weights_base),
            "expected_distribution_18_requests": {
                f"backend{i+1}": round(18 * w / sum(weights_base))
                for i, w in enumerate(weights_base)
            },
        },
        
        # Security exercise parameters
        "security": {
            "rate_limit_requests": rate_limit_requests,
            "rate_limit_window_seconds": rate_limit_window,
            "blocked_user_agents": [
                f"MaliciousBot/{rng.randint(1, 9)}.0",
                f"Scraper-{student_segment}",
            ],
        },
        
        # Test paths for verification
        "test_paths": [
            f"/api/v{rng.randint(1, 3)}/{student_segment}/status",
            f"/data/{rng.choice(['users', 'orders', 'products'])}/{rng.randint(1000, 9999)}",
            f"/health/{student_segment}",
        ],
        
        # Required PCAP captures
        "required_captures": {
            "handshake": {
                "filename": f"pcap/{student_segment}_handshake.pcap",
                "description": "TCP 3-way handshake to YOUR server",
                "min_packets": 3,
                "must_include_port": unique_port,
            },
            "http_exchange": {
                "filename": f"pcap/{student_segment}_http.pcap",
                "description": "Complete HTTP request-response cycle",
                "min_packets": 10,
                "must_include_header": f"STU-{header_suffix}",
            },
            "load_balance": {
                "filename": f"pcap/{student_segment}_loadbalance.pcap",
                "description": "9+ requests showing weight distribution",
                "min_packets": 30,
                "expected_backends": weights_base,
            },
        },
        
        # Verification data (for instructor use)
        "_verification": {
            "seed": seed,
            "regeneration_command": f"python scripts/generate_student_context.py \"{student_id}\"",
        }
    }
    
    return context


def save_context(context: dict[str, Any], output_path: Path) -> None:
    """Save context to JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(context, f, indent=2, ensure_ascii=False)


def print_summary(context: dict[str, Any]) -> None:
    """Print human-readable summary of generated context."""
    print("\n" + "=" * 70)
    print("🎯 STUDENT CONTEXT GENERATED SUCCESSFULLY")
    print("=" * 70)
    
    print(f"\n📋 Student: {context['student_id']}")
    print(f"   Session: {context['session_token']}")
    print(f"   Valid for: {context['valid_date']}")
    
    print(f"\n🔧 Exercise 1 — HTTP Server:")
    hs = context['http_server']
    print(f"   • Your unique port: {hs['port']}")
    print(f"   • Secret header: {hs['secret_header_name']}: {hs['secret_header_value']}")
    print(f"   • Custom status: {hs['custom_status_code']} at {hs['custom_status_path']}")
    
    print(f"\n⚖️  Exercise 2 — Load Balancer:")
    lb = context['load_balancer']
    print(f"   • Backend weights: {lb['weights']}")
    print(f"   • For 18 requests expect: {lb['expected_distribution_18_requests']}")
    
    print(f"\n🔒 Security Parameters:")
    sec = context['security']
    print(f"   • Rate limit: {sec['rate_limit_requests']} requests / {sec['rate_limit_window_seconds']}s")
    
    print(f"\n📁 Required PCAP Submissions:")
    for name, cap in context['required_captures'].items():
        print(f"   • {cap['filename']}")
        print(f"     ({cap['description']})")
    
    print("\n" + "=" * 70)
    print("⚠️  IMPORTANT: Include artifacts/student_context.json in your submission!")
    print("    Your exercises MUST use these unique parameters.")
    print("    Generic solutions will NOT pass verification.")
    print("=" * 70 + "\n")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate unique student context for Week 8 exercises",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python scripts/generate_student_context.py "12345ABC"
    python scripts/generate_student_context.py "student_id" --output my_context.json
    
This script generates deterministic unique exercise parameters for each student.
The same student ID always generates the same parameters allowing instructors
to verify submissions by regenerating the expected context.

For issues: Open an issue in GitHub
        """
    )
    
    parser.add_argument(
        "student_id",
        help="Your student identifier (registration number or similar)"
    )
    parser.add_argument(
        "--output", "-o",
        default="artifacts/student_context.json",
        help="Output file path (default: artifacts/student_context.json)"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress summary output"
    )
    
    args = parser.parse_args()
    
    # Validate student ID
    if len(args.student_id.strip()) < 3:
        print("❌ Error: Student ID must be at least 3 characters")
        return 1
    
    # Generate context
    context = generate_student_context(args.student_id)
    
    # Save to file
    output_path = Path(args.output)
    save_context(context, output_path)
    
    # Print summary
    if not args.quiet:
        print_summary(context)
        print(f"✅ Context saved to: {output_path}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
