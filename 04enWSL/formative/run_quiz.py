#!/usr/bin/env python3
"""
Formative Quiz Runner — Week 4
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Interactive quiz runner with support for filtering by Learning Objective
and Bloom taxonomy level.

Usage:
    python formative/run_quiz.py                    # Run full quiz
    python formative/run_quiz.py --random           # Randomise order
    python formative/run_quiz.py --limit 5          # Only 5 questions
    python formative/run_quiz.py --lo LO3 LO4       # Filter by LO
    python formative/run_quiz.py --bloom apply      # Filter by Bloom level
"""


# ═══════════════════════════════════════════════════════════════════════════════
# IMPORT_DEPENDENCIES
# ═══════════════════════════════════════════════════════════════════════════════

import yaml
import random
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ_LOADER
# ═══════════════════════════════════════════════════════════════════════════════

def load_quiz(path: Path) -> Dict[str, Any]:
    """
    Load quiz from YAML file.
    
    Args:
        path: Path to the quiz YAML file
        
    Returns:
        Dictionary containing quiz metadata and questions
    """
    with open(path, encoding='utf-8') as f:
        return yaml.safe_load(f)


# ═══════════════════════════════════════════════════════════════════════════════
# QUESTION_FILTER
# ═══════════════════════════════════════════════════════════════════════════════

def filter_questions(
    questions: List[Dict],
    lo_filter: Optional[List[str]] = None,
    bloom_filter: Optional[str] = None,
    difficulty_filter: Optional[str] = None
) -> List[Dict]:
    """
    Filter questions by Learning Objective, Bloom level, or difficulty.
    
    Args:
        questions: List of question dictionaries
        lo_filter: List of LO identifiers to include (e.g., ['LO1', 'LO2'])
        bloom_filter: Bloom level to include (e.g., 'apply')
        difficulty_filter: Difficulty level to include (e.g., 'intermediate')
        
    Returns:
        Filtered list of questions
    """
    result = questions
    
    if lo_filter:
        result = [q for q in result if q.get('lo_ref') in lo_filter]
    
    if bloom_filter:
        result = [q for q in result if q.get('bloom_level') == bloom_filter]
    
    if difficulty_filter:
        result = [q for q in result if q.get('difficulty') == difficulty_filter]
    
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# QUESTION_PRESENTER
# ═══════════════════════════════════════════════════════════════════════════════

def present_question(q: Dict, index: int, total: int) -> Optional[str]:
    """
    Present a question to the user and collect their answer.
    
    Args:
        q: Question dictionary
        index: Current question number (1-based)
        total: Total number of questions
        
    Returns:
        User's answer as a string, or None if skipped
    """
    print(f"\n{'─'*60}")
    bloom = q.get('bloom_level', '?').upper()
    lo = q.get('lo_ref', '?')
    difficulty = q.get('difficulty', '?')
    print(f"Question {index}/{total} [{bloom}] [{lo}] [{difficulty}]")
    print(f"{'─'*60}")
    print(f"\n{q['stem']}\n")
    
    q_type = q['type']
    
    if q_type == 'multiple_choice':
        for key, val in q['options'].items():
            print(f"  {key}) {val}")
        answer = input("\nYour answer (a/b/c/d): ").strip().lower()
        
    elif q_type == 'true_false':
        print("  Enter: true or false")
        answer = input("\nYour answer: ").strip().lower()
        
    elif q_type in ('fill_blank', 'code_output', 'short_answer'):
        if 'hint' in q:
            print(f"  💡 Hint: {q['hint']}")
        answer = input("\nYour answer: ").strip()
        
    else:
        answer = input("\nYour answer: ").strip()
    
    return answer


# ═══════════════════════════════════════════════════════════════════════════════
# ANSWER_CHECKER
# ═══════════════════════════════════════════════════════════════════════════════

def check_answer(q: Dict, answer: str) -> bool:
    """
    Check if the user's answer is correct.
    
    Args:
        q: Question dictionary containing correct answer
        answer: User's answer
        
    Returns:
        True if correct, False otherwise
    """
    q_type = q['type']
    correct = q['correct']
    
    if q_type == 'multiple_choice':
        return answer == correct
    
    elif q_type == 'true_false':
        user_true = answer in ('true', 't', 'yes', 'y', '1')
        user_false = answer in ('false', 'f', 'no', 'n', '0')
        if correct:
            return user_true
        else:
            return user_false
    
    elif q_type in ('fill_blank', 'code_output', 'short_answer'):
        # Accept any of the correct answers (case-insensitive)
        correct_list = correct if isinstance(correct, list) else [correct]
        return answer.lower() in [c.lower() for c in correct_list]
    
    return False


# ═══════════════════════════════════════════════════════════════════════════════
# FEEDBACK_DISPLAY
# ═══════════════════════════════════════════════════════════════════════════════

def show_feedback(q: Dict, is_correct: bool) -> None:
    """
    Display feedback for the user's answer.
    
    Args:
        q: Question dictionary
        is_correct: Whether the answer was correct
    """
    if is_correct:
        print("\n✅ Correct!")
    else:
        correct = q['correct']
        if isinstance(correct, list):
            correct = correct[0]
        print(f"\n❌ Incorrect. Correct answer: {correct}")
    
    if 'explanation' in q:
        print(f"📖 {q['explanation']}")
    
    if q.get('misconception_ref'):
        print(f"📚 Related misconception: {q['misconception_ref']}")


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ_RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

def run_quiz(
    quiz: Dict,
    randomise: bool = False,
    limit: Optional[int] = None,
    lo_filter: Optional[List[str]] = None,
    bloom_filter: Optional[str] = None
) -> Dict[str, Any]:
    """
    Run the quiz interactively.
    
    Args:
        quiz: Quiz dictionary with metadata and questions
        randomise: Whether to randomise question order
        limit: Maximum number of questions to present
        lo_filter: List of LO identifiers to include
        bloom_filter: Bloom level to include
        
    Returns:
        Results dictionary with scores and breakdowns
    """
    questions = quiz.get('questions', [])
    questions = filter_questions(questions, lo_filter, bloom_filter)
    
    if randomise:
        questions = questions.copy()
        random.shuffle(questions)
    
    if limit:
        questions = questions[:limit]
    
    if not questions:
        print("\n⚠️  No questions match the specified filters.")
        return {'score': 0, 'total': 0, 'percentage': 0, 'passed': False}
    
    metadata = quiz.get('metadata', {})
    
    # Display header
    print("\n" + "═"*60)
    print(f"  📝 QUIZ: {metadata.get('topic', 'Week 4')}")
    print(f"  Questions: {len(questions)} | Passing: {metadata.get('passing_score', 70)}%")
    print("═"*60)
    
    correct_count = 0
    results_by_lo: Dict[str, Dict[str, int]] = {}
    results_by_bloom: Dict[str, Dict[str, int]] = {}
    
    for i, q in enumerate(questions, 1):
        answer = present_question(q, i, len(questions))
        is_correct = check_answer(q, answer)
        show_feedback(q, is_correct)
        
        if is_correct:
            correct_count += 1
        
        # Track results by Learning Objective
        lo = q.get('lo_ref', 'Unknown')
        if lo not in results_by_lo:
            results_by_lo[lo] = {'correct': 0, 'total': 0}
        results_by_lo[lo]['total'] += 1
        if is_correct:
            results_by_lo[lo]['correct'] += 1
        
        # Track results by Bloom level
        bloom = q.get('bloom_level', 'unknown')
        if bloom not in results_by_bloom:
            results_by_bloom[bloom] = {'correct': 0, 'total': 0}
        results_by_bloom[bloom]['total'] += 1
        if is_correct:
            results_by_bloom[bloom]['correct'] += 1
        
        input("\nPress Enter to continue...")
    
    # Calculate final score
    total = len(questions)
    percentage = (correct_count / total * 100) if total > 0 else 0
    passing = metadata.get('passing_score', 70)
    passed = percentage >= passing
    
    # Display summary
    print("\n" + "═"*60)
    print("  📊 RESULTS SUMMARY")
    print("═"*60)
    print(f"\n  Score: {correct_count}/{total} ({percentage:.1f}%)")
    print(f"  Status: {'✅ PASSED' if passed else '❌ NEEDS REVIEW'}")
    
    # Results by Learning Objective
    print("\n  By Learning Objective:")
    for lo, data in sorted(results_by_lo.items()):
        pct = data['correct'] / data['total'] * 100 if data['total'] > 0 else 0
        status = '✅' if pct >= 70 else '⚠️' if pct >= 50 else '❌'
        print(f"    {status} {lo}: {data['correct']}/{data['total']} ({pct:.0f}%)")
    
    # Results by Bloom level
    print("\n  By Bloom Level:")
    bloom_order = ['remember', 'understand', 'apply', 'analyse', 'evaluate']
    for bloom in bloom_order:
        if bloom in results_by_bloom:
            data = results_by_bloom[bloom]
            pct = data['correct'] / data['total'] * 100 if data['total'] > 0 else 0
            print(f"    {bloom.capitalize()}: {data['correct']}/{data['total']} ({pct:.0f}%)")
    
    print("\n" + "═"*60)
    
    # Recommendations based on weak areas
    weak_los = [lo for lo, data in results_by_lo.items() 
                if data['correct'] / data['total'] < 0.7]
    if weak_los:
        print("\n  📚 Recommended Review:")
        for lo in weak_los:
            print(f"    • Review materials for {lo}")
        print()
    
    return {
        'score': correct_count,
        'total': total,
        'percentage': percentage,
        'passed': passed,
        'by_lo': results_by_lo,
        'by_bloom': results_by_bloom
    }


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """
    Main entry point for the quiz runner.
    
    Returns:
        Exit code (0 if passed, 1 if failed)
    """
    parser = argparse.ArgumentParser(
        description="Run formative quiz for Week 4",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_quiz.py                    # Full quiz
  python run_quiz.py --random --limit 5 # Random 5 questions
  python run_quiz.py --lo LO3 LO4       # Only LO3 and LO4
  python run_quiz.py --bloom apply      # Only 'apply' level
        """
    )
    
    parser.add_argument(
        '--quiz', '-q', 
        type=Path, 
        default=Path(__file__).parent / 'quiz.yaml',
        help='Path to quiz YAML file'
    )
    parser.add_argument(
        '--random', '-r', 
        action='store_true',
        help='Randomise question order'
    )
    parser.add_argument(
        '--limit', '-l', 
        type=int,
        help='Limit number of questions'
    )
    parser.add_argument(
        '--lo', 
        nargs='+',
        help='Filter by Learning Objectives (e.g., LO1 LO2)'
    )
    parser.add_argument(
        '--bloom', 
        choices=['remember', 'understand', 'apply', 'analyse', 'evaluate'],
        help='Filter by Bloom level'
    )
    
    args = parser.parse_args()
    
    # Validate quiz file exists
    if not args.quiz.exists():
        print(f"Error: Quiz file not found: {args.quiz}")
        return 1
    
    # Load and run quiz
    try:
        quiz = load_quiz(args.quiz)
    except yaml.YAMLError as e:
        print(f"Error parsing quiz file: {e}")
        return 1
    
    results = run_quiz(
        quiz,
        randomise=args.random,
        limit=args.limit,
        lo_filter=args.lo,
        bloom_filter=args.bloom
    )
    
    return 0 if results['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
