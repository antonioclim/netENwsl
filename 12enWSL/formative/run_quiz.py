#!/usr/bin/env python3
"""
Formative Quiz Runner — Week 12
================================
Computer Networks - ASE, CSIE | by ing. dr. Antonio Clim

Interactive quiz for self-assessment of learning objectives.

Usage:
    python formative/run_quiz.py                    # Run full quiz
    python formative/run_quiz.py --random           # Randomise questions
    python formative/run_quiz.py --limit 5          # Run only 5 questions
    python formative/run_quiz.py --lo LO1 LO5       # Filter by LO
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ_LOADER
# ═══════════════════════════════════════════════════════════════════════════════
def load_quiz(path: Path) -> Dict[str, Any]:
    """
    Load quiz from YAML file.
    
    Args:
        path: Path to quiz YAML file
        
    Returns:
        Quiz dictionary with metadata and questions
    """
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ_RUNNER
# ═══════════════════════════════════════════════════════════════════════════════
def run_quiz(
    quiz: Dict[str, Any],
    randomise: bool = False,
    limit: Optional[int] = None,
    lo_filter: Optional[List[str]] = None
) -> float:
    """
    Run interactive quiz and return score percentage.
    
    Args:
        quiz: Loaded quiz dictionary
        randomise: Shuffle question order
        limit: Maximum questions to ask
        lo_filter: Only include questions for these LOs
    
    Returns:
        Score as percentage (0-100)
    """
    questions = list(quiz.get("questions", []))
    
    # Filter by LO if specified
    if lo_filter:
        questions = [q for q in questions if q.get("lo_ref") in lo_filter]
    
    if randomise:
        random.shuffle(questions)
    
    if limit and limit > 0:
        questions = questions[:limit]
    
    if not questions:
        print("No questions match the specified criteria.")
        return 0.0
    
    metadata = quiz.get("metadata", {})
    correct = 0
    total = len(questions)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # DISPLAY_HEADER
    # ═══════════════════════════════════════════════════════════════════════════
    print("\n" + "═" * 70)
    print(f"  QUIZ: {metadata.get('topic', 'Week 12')}")
    print(f"  Questions: {total} | Passing: {metadata.get('passing_score', 70)}%")
    print(f"  Time estimate: {metadata.get('estimated_time', '15 minutes')}")
    print("═" * 70)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # RUN_QUESTIONS
    # ═══════════════════════════════════════════════════════════════════════════
    for i, q in enumerate(questions, 1):
        print(f"\n{'─' * 60}")
        difficulty = q.get("difficulty", "?").upper()
        lo_ref = q.get("lo_ref", "?")
        print(f"Q{i}/{total} [{difficulty}] [LO: {lo_ref}]")
        print(f"\n    {q['stem']}\n")
        
        if q["type"] == "multiple_choice":
            # Display options
            for key, val in q.get("options", {}).items():
                print(f"    {key}) {val}")
            
            # Get answer
            while True:
                answer = input("\n    Your answer (a/b/c/d): ").strip().lower()
                if answer in ["a", "b", "c", "d"]:
                    break
                print("    Please enter a, b, c or d.")
            
            # Check answer
            if answer == q["correct"]:
                print("    ✅ Correct!")
                correct += 1
            else:
                print(f"    ❌ Incorrect. Correct answer: {q['correct']}")
                if "explanation" in q:
                    print(f"\n    📖 {q['explanation']}")
                if "misconception_ref" in q:
                    print(f"    📚 See: {q['misconception_ref']}")
        
        elif q["type"] == "fill_blank":
            # Get answer
            answer = input("\n    Your answer: ").strip()
            
            # Check answer (case-insensitive for fill-blank)
            correct_answers = [str(a).lower() for a in q.get("correct", [])]
            if answer.lower() in correct_answers:
                print("    ✅ Correct!")
                correct += 1
            else:
                acceptable = ", ".join(str(a) for a in q.get("correct", []))
                print(f"    ❌ Incorrect. Accepted answers: {acceptable}")
                if "hint" in q:
                    print(f"    💡 Hint: {q['hint']}")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # DISPLAY_RESULTS
    # ═══════════════════════════════════════════════════════════════════════════
    score = (correct / total) * 100 if total > 0 else 0
    passing = metadata.get("passing_score", 70)
    passed = score >= passing
    
    print("\n" + "═" * 70)
    print(f"  RESULTS: {correct}/{total} correct ({score:.1f}%)")
    print(f"  STATUS:  {'✅ PASSED' if passed else '❌ NEEDS REVIEW'}")
    print("═" * 70)
    
    # Display feedback
    feedback = quiz.get("feedback", {})
    if score >= 90:
        msg = feedback.get("excellent", "Excellent work!")
    elif score >= passing:
        msg = feedback.get("good", "Good job!")
    else:
        msg = feedback.get("needs_review", "Keep practising!")
    
    print(f"\n  {msg}\n")
    
    return score


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(
        description="Week 12 Formative Quiz Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python formative/run_quiz.py                  # Full quiz
  python formative/run_quiz.py --random         # Randomised order
  python formative/run_quiz.py --limit 5        # Only 5 questions
  python formative/run_quiz.py --lo LO1 LO5     # Filter by LO
        """
    )
    parser.add_argument(
        "--quiz", "-q",
        type=Path,
        default=None,
        help="Path to quiz YAML file (default: formative/quiz.yaml)"
    )
    parser.add_argument(
        "--random", "-r",
        action="store_true",
        help="Randomise question order"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        default=None,
        help="Maximum number of questions to ask"
    )
    parser.add_argument(
        "--lo",
        nargs="+",
        metavar="LOx",
        help="Filter by Learning Objectives (e.g., --lo LO1 LO5)"
    )
    
    args = parser.parse_args()
    
    # Determine quiz path
    if args.quiz:
        quiz_path = args.quiz
    else:
        # Try relative to script location first
        script_dir = Path(__file__).parent
        quiz_path = script_dir / "quiz.yaml"
        if not quiz_path.exists():
            # Try current directory
            quiz_path = Path("formative/quiz.yaml")
    
    if not quiz_path.exists():
        print(f"Error: Quiz file not found: {quiz_path}")
        print("Run this script from the 12enWSL directory or specify --quiz path")
        return 1
    
    # Load and run quiz
    try:
        quiz = load_quiz(quiz_path)
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML in quiz file: {e}")
        return 1
    except Exception as e:
        print(f"Error loading quiz: {e}")
        return 1
    
    passing_score = quiz.get("metadata", {}).get("passing_score", 70)
    score = run_quiz(
        quiz,
        randomise=args.random,
        limit=args.limit,
        lo_filter=args.lo
    )
    
    return 0 if score >= passing_score else 1


# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    sys.exit(main())
