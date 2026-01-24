#!/usr/bin/env python3
"""
Parsons Problems Runner — Week 8 Laboratory
============================================

Interactive tool for practising code arrangement with distractors.
Students arrange scrambled code blocks into the correct order
while identifying and excluding distractor blocks.

Usage:
    python formative/parsons/run_parsons.py              # Run all problems
    python formative/parsons/run_parsons.py --lo LO3     # Filter by LO
    python formative/parsons/run_parsons.py --list       # List available problems
    python formative/parsons/run_parsons.py --problem P2 # Run specific problem

Course: Computer Networks — ASE, CSIE
"""

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Optional


PROBLEMS_FILE = Path(__file__).parent / "problems.json"


def load_problems() -> dict:
    """Load problems from JSON file."""
    with open(PROBLEMS_FILE, encoding='utf-8') as f:
        return json.load(f)


def display_problem(problem: dict) -> list[dict]:
    """Display a problem and return shuffled blocks."""
    print("\n" + "═" * 70)
    print(f"🧩 {problem['title']}")
    print(f"   LO: {problem['lo_ref']} | Difficulty: {problem['difficulty']}")
    print("═" * 70)
    
    print(f"\n📋 Instructions:\n{problem['instructions']}")
    print("\n⚠️  Some blocks are DISTRACTORS — do NOT include them in your answer!")
    
    # Shuffle blocks for display
    blocks = problem['blocks'].copy()
    random.shuffle(blocks)
    
    print("\n" + "─" * 70)
    print("CODE BLOCKS (arrange these):")
    print("─" * 70)
    
    for i, block in enumerate(blocks, 1):
        indent = "    " * block.get('indent', 0)
        print(f"\n  [{i:2d}] {indent}{block['code']}")
    
    print("\n" + "─" * 70)
    
    return blocks


def check_answer(user_indices: list[int], blocks: list[dict], correct_order: list[int]) -> tuple[bool, str]:
    """
    Check if the user's answer is correct.
    
    Args:
        user_indices: List of block display indices (1-based) chosen by user
        blocks: The shuffled blocks as displayed
        correct_order: The correct block IDs in order
        
    Returns:
        Tuple of (is_correct, feedback_message)
    """
    # Map user's display indices to block IDs
    try:
        user_block_ids = [blocks[i - 1]['id'] for i in user_indices]
    except IndexError:
        return False, "Invalid block number. Please use numbers from the list."
    
    # Check for distractors
    distractor_ids = {b['id'] for b in blocks if b.get('distractor', False)}
    included_distractors = [bid for bid in user_block_ids if bid in distractor_ids]
    
    if included_distractors:
        distractor_codes = [b['code'][:40] + "..." for b in blocks 
                          if b['id'] in included_distractors]
        return False, f"❌ You included distractor block(s):\n   • " + "\n   • ".join(distractor_codes)
    
    # Check order
    if user_block_ids == correct_order:
        return True, "✅ Correct! All blocks in the right order."
    
    # Provide helpful feedback
    if set(user_block_ids) == set(correct_order):
        return False, "❌ You have the right blocks but in the wrong order."
    
    missing = set(correct_order) - set(user_block_ids)
    extra = set(user_block_ids) - set(correct_order)
    
    feedback = "❌ Incorrect arrangement:\n"
    if missing:
        missing_codes = [b['code'][:40] for b in blocks if b['id'] in missing]
        feedback += f"   Missing: {len(missing)} block(s)\n"
    if extra:
        feedback += f"   Extra: {len(extra)} block(s) that shouldn't be included\n"
    
    return False, feedback


def run_problem(problem: dict, show_solution: bool = False) -> bool:
    """
    Run a single Parsons problem interactively.
    
    Returns:
        True if answered correctly, False otherwise
    """
    blocks = display_problem(problem)
    
    if show_solution:
        print("\n📖 SOLUTION:")
        for bid in problem['correct_order']:
            block = next(b for b in problem['blocks'] if b['id'] == bid)
            indent = "    " * block.get('indent', 0)
            print(f"   {indent}{block['code']}")
        print(f"\n💡 Explanation:\n{problem['explanation']}")
        return True
    
    print("\nEnter the block numbers in order (space-separated).")
    print("Example: 1 3 5 7 2")
    print("Exclude any blocks you think are distractors.\n")
    
    answer = input("Your order: ").strip()
    
    if not answer:
        print("No answer provided.")
        return False
    
    try:
        user_indices = [int(x) for x in answer.split()]
    except ValueError:
        print("❌ Invalid input. Please enter numbers separated by spaces.")
        return False
    
    is_correct, feedback = check_answer(user_indices, blocks, problem['correct_order'])
    print(f"\n{feedback}")
    
    if not is_correct:
        print(f"\n💡 Explanation:\n{problem['explanation']}")
        
        # Show correct solution
        print("\n📖 Correct solution:")
        for bid in problem['correct_order']:
            block = next(b for b in problem['blocks'] if b['id'] == bid)
            indent = "    " * block.get('indent', 0)
            print(f"   {indent}{block['code']}")
    
    return is_correct


def list_problems(data: dict) -> None:
    """List all available problems."""
    problems = data.get('problems', [])
    
    print("\n" + "═" * 60)
    print("📋 AVAILABLE PARSONS PROBLEMS")
    print("═" * 60)
    
    for p in problems:
        print(f"\n  {p['id']}: {p['title']}")
        print(f"      LO: {p['lo_ref']} | Difficulty: {p['difficulty']}")
        distractor_count = sum(1 for b in p['blocks'] if b.get('distractor', False))
        print(f"      Blocks: {len(p['blocks'])} total, {distractor_count} distractors")
    
    print("\n" + "═" * 60)
    print("Run with: python formative/parsons/run_parsons.py --problem P1")
    print("═" * 60 + "\n")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Interactive Parsons problems for code arrangement practice"
    )
    
    parser.add_argument(
        "--problem", "-p",
        type=str,
        help="Run specific problem by ID (e.g., P1)"
    )
    parser.add_argument(
        "--lo",
        type=str,
        help="Filter problems by Learning Objective (e.g., LO3)"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all available problems"
    )
    parser.add_argument(
        "--solution", "-s",
        action="store_true",
        help="Show solutions without asking"
    )
    
    args = parser.parse_args()
    
    if not PROBLEMS_FILE.exists():
        print(f"❌ Problems file not found: {PROBLEMS_FILE}")
        return 1
    
    data = load_problems()
    problems = data.get('problems', [])
    
    if args.list:
        list_problems(data)
        return 0
    
    # Filter by specific problem
    if args.problem:
        problems = [p for p in problems if p['id'].upper() == args.problem.upper()]
        if not problems:
            print(f"❌ Problem '{args.problem}' not found.")
            return 1
    
    # Filter by LO
    if args.lo:
        lo_upper = args.lo.upper()
        problems = [p for p in problems if p['lo_ref'].upper() == lo_upper]
        if not problems:
            print(f"❌ No problems found for {args.lo}")
            return 1
    
    # Run problems
    print("\n" + "═" * 60)
    print("🧩 PARSONS PROBLEMS — Week 8")
    print("═" * 60)
    print(f"Problems to solve: {len(problems)}")
    
    correct = 0
    for p in problems:
        if run_problem(p, show_solution=args.solution):
            correct += 1
        
        if len(problems) > 1:
            input("\nPress Enter for next problem...")
    
    # Summary
    print("\n" + "═" * 60)
    print(f"📊 RESULTS: {correct}/{len(problems)} correct")
    print("═" * 60 + "\n")
    
    return 0 if correct == len(problems) else 1


if __name__ == "__main__":
    sys.exit(main())
