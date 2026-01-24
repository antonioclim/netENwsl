#!/usr/bin/env python3
"""
Quiz Runner for Week 0 Formative Assessment
============================================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

A command-line tool for running interactive formative quizzes.
Supports multiple question types, Bloom level filtering, review mode
and LMS export (Moodle GIFT, Canvas QTI, JSON).

Usage:
    python run_quiz.py                    # Run full quiz
    python run_quiz.py --random           # Randomise question order
    python run_quiz.py --limit 5          # Run only 5 questions
    python run_quiz.py --bloom apply      # Filter by Bloom level
    python run_quiz.py --show-answers     # Review mode (show answers)
    python run_quiz.py --export json      # Export to JSON for LMS
    python run_quiz.py --export moodle    # Export to Moodle GIFT format
    python run_quiz.py --help             # Show all options

Requirements:
    pip install pyyaml

Version: 1.5.0
Date: 2026-01-24
"""

import yaml
import json
import random
import sys
import argparse
from pathlib import Path
from typing import Optional, Dict, List, Any
from datetime import datetime

__all__ = [
    'load_quiz',
    'run_quiz',
    'export_to_json',
    'export_to_moodle_gift',
    'export_to_qti'
]


def load_quiz(path: Path) -> Dict[str, Any]:
    """Load quiz data from YAML file.
    
    Args:
        path: Path to the quiz YAML file
        
    Returns:
        Parsed quiz dictionary
        
    Raises:
        FileNotFoundError: If quiz file doesn't exist
        yaml.YAMLError: If YAML is malformed
    """
    with open(path, encoding='utf-8') as f:
        return yaml.safe_load(f)


def display_question(
    q: Dict[str, Any], 
    index: int, 
    show_answer: bool = False
) -> Optional[bool]:
    """Display a single question and collect/evaluate answer.
    
    Args:
        q: Question dictionary from quiz
        index: Question number (1-indexed)
        show_answer: If True, show answer immediately (review mode)
        
    Returns:
        True if correct, False if wrong, None if skipped
    """
    bloom_badge = f"[{q.get('bloom_level', '?').upper()}]"
    diff_badge = f"({q.get('difficulty', '?')})"
    lo_badge = f"LO: {q.get('lo_ref', 'N/A')}"
    
    print(f"\n{'─' * 60}")
    print(f"Q{index}. {bloom_badge} {diff_badge} | {lo_badge}")
    print(f"{'─' * 60}")
    print(f"\n{q['stem']}\n")
    
    if q['type'] == 'multiple_choice':
        for key, value in q['options'].items():
            print(f"   {key}) {value}")
        
        if show_answer:
            print(f"\n   ✓ Correct answer: {q['correct']}")
            if 'explanation' in q:
                print(f"   📖 {q['explanation']}")
            return None
            
        answer = input("\nYour answer (a/b/c/d or 's' to skip): ").strip().lower()
        
        if answer == 's':
            print("   ⏭️  Skipped")
            return None
        elif answer == q['correct']:
            print("   ✅ Correct!")
            if 'feedback' in q and 'correct' in q['feedback']:
                print(f"   💬 {q['feedback']['correct']}")
            return True
        else:
            print(f"   ❌ Wrong. Correct answer: {q['correct']}")
            if 'explanation' in q:
                print(f"   📖 {q['explanation']}")
            if 'feedback' in q and 'incorrect' in q['feedback']:
                print(f"   💬 {q['feedback']['incorrect']}")
            return False
            
    elif q['type'] == 'fill_blank':
        if 'hint' in q:
            print(f"   💡 Hint: {q['hint']}")
            
        if show_answer:
            correct_answers = q['correct']
            if isinstance(correct_answers, list):
                print(f"\n   ✓ Accepted answers: {', '.join(correct_answers)}")
            else:
                print(f"\n   ✓ Correct answer: {correct_answers}")
            if 'explanation' in q:
                print(f"   📖 {q['explanation']}")
            return None
            
        answer = input("\nYour answer (or 's' to skip): ").strip()
        
        if answer.lower() == 's':
            print("   ⏭️  Skipped")
            return None
        
        correct_answers = q['correct']
        if isinstance(correct_answers, list):
            is_correct = answer in correct_answers
        else:
            is_correct = answer == correct_answers
            
        if is_correct:
            print("   ✅ Correct!")
            if 'feedback' in q and 'correct' in q['feedback']:
                print(f"   💬 {q['feedback']['correct']}")
            return True
        else:
            if isinstance(correct_answers, list):
                print(f"   ❌ Wrong. Accepted: {', '.join(correct_answers)}")
            else:
                print(f"   ❌ Wrong. Correct: {correct_answers}")
            if 'explanation' in q:
                print(f"   📖 {q['explanation']}")
            if 'feedback' in q and 'incorrect' in q['feedback']:
                print(f"   💬 {q['feedback']['incorrect']}")
            return False
    
    return None


def get_feedback(score: float, scoring_config: Dict[str, Any]) -> str:
    """Get appropriate feedback based on score.
    
    Args:
        score: Percentage score (0-100)
        scoring_config: Scoring configuration from quiz
        
    Returns:
        Feedback string for the score level
    """
    levels = scoring_config.get('levels', [])
    for level in levels:
        range_min, range_max = level['range']
        if range_min <= score <= range_max:
            return f"{level['label']}: {level['feedback']}"
    return "No feedback available for this score range."


def run_quiz(
    quiz: Dict[str, Any], 
    randomise: bool = False, 
    limit: Optional[int] = None,
    bloom_filter: Optional[str] = None,
    show_answers: bool = False
) -> Dict[str, Any]:
    """Run the interactive quiz.
    
    Args:
        quiz: Loaded quiz dictionary
        randomise: Shuffle question order
        limit: Maximum questions to ask
        bloom_filter: Filter by Bloom level
        show_answers: Review mode
        
    Returns:
        Results dictionary with score and details
    """
    questions = list(quiz.get('questions', []))
    
    # Apply Bloom level filter
    if bloom_filter:
        bloom_filter = bloom_filter.lower()
        questions = [q for q in questions if q.get('bloom_level', '').lower() == bloom_filter]
        if not questions:
            print(f"No questions found for Bloom level: {bloom_filter}")
            print("Available levels: remember, understand, apply, analyse, evaluate, create")
            return {'score': 0, 'total': 0, 'passed': False}
    
    # Randomise if requested
    if randomise:
        random.shuffle(questions)
        
    # Apply limit
    if limit and limit > 0:
        questions = questions[:limit]
    
    if not questions:
        print("No questions available.")
        return {'score': 0, 'total': 0, 'passed': False}
    
    # Get metadata
    meta = quiz.get('metadata', {})
    
    # Display header
    _display_quiz_header(meta, len(questions), bloom_filter, show_answers)
    
    input("\nPress Enter to start...")
    
    # Run questions
    correct = 0
    answered = 0
    skipped = 0
    
    for i, q in enumerate(questions, 1):
        result = display_question(q, i, show_answers)
        if result is True:
            correct += 1
            answered += 1
        elif result is False:
            answered += 1
        else:
            skipped += 1
    
    # Calculate score
    if answered > 0:
        score = (correct / answered) * 100
    else:
        score = 0.0
        
    passing_score = meta.get('passing_score', 70)
    passed = score >= passing_score
    
    # Display results
    _display_quiz_results(correct, answered, skipped, score, passing_score, passed, quiz.get('scoring', {}))
    
    return {
        'score': score,
        'correct': correct,
        'answered': answered,
        'skipped': skipped,
        'total': len(questions),
        'passed': passed
    }


def _display_quiz_header(
    meta: Dict[str, Any], 
    num_questions: int, 
    bloom_filter: Optional[str], 
    show_answers: bool
) -> None:
    """Display quiz header with metadata."""
    print("\n" + "═" * 60)
    print(f"  📝 QUIZ: {meta.get('topic', 'Formative Assessment')}")
    print("═" * 60)
    print(f"  Questions: {num_questions}")
    print(f"  Passing score: {meta.get('passing_score', 70)}%")
    print(f"  Estimated time: {meta.get('estimated_time', '15 minutes')}")
    if bloom_filter:
        print(f"  Bloom filter: {bloom_filter.upper()}")
    if show_answers:
        print("  Mode: 📖 REVIEW (answers shown)")
    print("═" * 60)


def _display_quiz_results(
    correct: int, 
    answered: int, 
    skipped: int, 
    score: float, 
    passing_score: int, 
    passed: bool, 
    scoring: Dict[str, Any]
) -> None:
    """Display quiz results with feedback."""
    print("\n" + "═" * 60)
    print("  📊 RESULTS")
    print("═" * 60)
    print(f"  Correct: {correct}/{answered}")
    if skipped > 0:
        print(f"  Skipped: {skipped}")
    print(f"  Score: {score:.1f}%")
    print(f"  Passing: {passing_score}%")
    print(f"  Status: {'✅ PASSED' if passed else '❌ NEEDS REVIEW'}")
    
    if scoring:
        feedback = get_feedback(score, scoring)
        print(f"\n  💬 {feedback}")
    
    print("═" * 60 + "\n")


def export_to_json(quiz: Dict[str, Any], output_path: Path) -> None:
    """Export quiz to JSON format for LMS import.
    
    Args:
        quiz: Loaded quiz dictionary
        output_path: Path for output JSON file
    """
    # Transform to LMS-friendly format
    export_data = {
        "metadata": {
            "title": f"Week {quiz['metadata'].get('week', 0)}: {quiz['metadata'].get('topic', 'Quiz')}",
            "description": "Formative assessment for Computer Networks prerequisites",
            "version": quiz['metadata'].get('version', '1.0'),
            "date": datetime.now().isoformat(),
            "total_questions": len(quiz.get('questions', [])),
            "passing_score": quiz['metadata'].get('passing_score', 70)
        },
        "questions": []
    }
    
    for q in quiz.get('questions', []):
        question_data = {
            "id": q.get('id'),
            "type": q.get('type'),
            "bloom_level": q.get('bloom_level'),
            "learning_objective": q.get('lo_ref'),
            "stem": q.get('stem'),
            "points": q.get('points', 1)
        }
        
        if q['type'] == 'multiple_choice':
            question_data['options'] = [
                {"key": k, "text": v, "correct": k == q['correct']}
                for k, v in q['options'].items()
            ]
        elif q['type'] == 'fill_blank':
            question_data['correct_answers'] = q['correct'] if isinstance(q['correct'], list) else [q['correct']]
        
        if 'explanation' in q:
            question_data['explanation'] = q['explanation']
        if 'feedback' in q:
            question_data['feedback'] = q['feedback']
            
        export_data['questions'].append(question_data)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Exported to JSON: {output_path}")


def export_to_moodle_gift(quiz: Dict[str, Any], output_path: Path) -> None:
    """Export quiz to Moodle GIFT format.
    
    Args:
        quiz: Loaded quiz dictionary
        output_path: Path for output GIFT file
    """
    lines = [
        f"// Week {quiz['metadata'].get('week', 0)} Quiz - Moodle GIFT Format",
        f"// Generated: {datetime.now().isoformat()}",
        ""
    ]
    
    for q in quiz.get('questions', []):
        # Category
        lines.append(f"$CATEGORY: Week{quiz['metadata'].get('week', 0)}/{q.get('lo_ref', 'General')}")
        lines.append("")
        
        # Question title
        title = f"[{q.get('id', 'Q')}] {q.get('lo_ref', '')}"
        
        if q['type'] == 'multiple_choice':
            stem = q['stem'].replace(':', '\\:').replace('~', '\\~').replace('=', '\\=')
            lines.append(f"::{title}::{stem} {{")
            
            for key, value in q['options'].items():
                value_escaped = value.replace('~', '\\~').replace('=', '\\=')
                if key == q['correct']:
                    lines.append(f"  ={value_escaped}")
                else:
                    lines.append(f"  ~{value_escaped}")
            
            lines.append("}")
            
        elif q['type'] == 'fill_blank':
            stem = q['stem'].replace('___', '{')
            correct_answers = q['correct'] if isinstance(q['correct'], list) else [q['correct']]
            answers = ' '.join(f"={ans}" for ans in correct_answers)
            lines.append(f"::{title}::{stem}{answers}}}")
        
        lines.append("")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✅ Exported to Moodle GIFT: {output_path}")


def export_to_qti(quiz: Dict[str, Any], output_path: Path) -> None:
    """Export quiz to QTI 1.2 format (Canvas compatible).
    
    Args:
        quiz: Loaded quiz dictionary
        output_path: Path for output QTI XML file
    """
    # Simplified QTI export - full implementation would be more complex
    print(f"⚠️  QTI export is a simplified version. For full Canvas import, use quiz.json")
    
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2">',
        f'  <assessment title="Week {quiz["metadata"].get("week", 0)} Quiz">',
        '    <section>'
    ]
    
    for q in quiz.get('questions', []):
        xml_lines.append(f'      <item title="{q.get("id", "Q")}">')
        xml_lines.append(f'        <presentation><material><mattext>{q["stem"]}</mattext></material></presentation>')
        xml_lines.append('      </item>')
    
    xml_lines.extend([
        '    </section>',
        '  </assessment>',
        '</questestinterop>'
    ])
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml_lines))
    
    print(f"✅ Exported to QTI: {output_path}")


def main() -> int:
    """Main entry point.
    
    Returns:
        Exit code: 0 if passed or review mode, 1 if failed
    """
    parser = argparse.ArgumentParser(
        description='Run Week 0 formative quiz for Computer Networks',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_quiz.py                    # Run full quiz
  python run_quiz.py --random           # Randomise questions
  python run_quiz.py --limit 5          # Only 5 questions
  python run_quiz.py --bloom apply      # Only 'apply' level
  python run_quiz.py --show-answers     # Review mode
  python run_quiz.py --export json      # Export to JSON
  python run_quiz.py --export moodle    # Export to Moodle GIFT
        """
    )
    parser.add_argument(
        '--quiz', '-q',
        type=Path,
        default=Path(__file__).parent / 'quiz.yaml',
        help='Path to quiz YAML file (default: ./quiz.yaml)'
    )
    parser.add_argument(
        '--random', '-r',
        action='store_true',
        help='Randomise question order'
    )
    parser.add_argument(
        '--limit', '-l',
        type=int,
        metavar='N',
        help='Limit to N questions'
    )
    parser.add_argument(
        '--bloom', '-b',
        choices=['remember', 'understand', 'apply', 'analyse', 'evaluate', 'create'],
        metavar='LEVEL',
        help='Filter by Bloom taxonomy level'
    )
    parser.add_argument(
        '--show-answers', '-a',
        action='store_true',
        help='Review mode: show answers without testing'
    )
    parser.add_argument(
        '--export', '-e',
        choices=['json', 'moodle', 'qti'],
        metavar='FORMAT',
        help='Export quiz to specified format (json, moodle, qti)'
    )
    parser.add_argument(
        '--output', '-o',
        type=Path,
        help='Output path for export (default: auto-generated)'
    )
    
    args = parser.parse_args()
    
    # Check quiz file exists
    if not args.quiz.exists():
        print(f"Error: Quiz file not found: {args.quiz}")
        print("\nMake sure quiz.yaml exists in the formative/ directory.")
        print("Expected location: formative/quiz.yaml")
        return 1
    
    # Load quiz
    try:
        quiz = load_quiz(args.quiz)
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML in quiz file")
        print(f"Details: {e}")
        return 1
    except Exception as e:
        print(f"Error loading quiz: {e}")
        return 1
    
    # Handle export mode
    if args.export:
        output_path = args.output
        if not output_path:
            base = args.quiz.stem
            if args.export == 'json':
                output_path = args.quiz.parent / f"{base}_export.json"
            elif args.export == 'moodle':
                output_path = args.quiz.parent / f"{base}_moodle.gift"
            elif args.export == 'qti':
                output_path = args.quiz.parent / f"{base}_qti.xml"
        
        if args.export == 'json':
            export_to_json(quiz, output_path)
        elif args.export == 'moodle':
            export_to_moodle_gift(quiz, output_path)
        elif args.export == 'qti':
            export_to_qti(quiz, output_path)
        
        return 0
    
    # Run quiz
    try:
        results = run_quiz(
            quiz,
            randomise=args.random,
            limit=args.limit,
            bloom_filter=args.bloom,
            show_answers=args.show_answers
        )
    except KeyboardInterrupt:
        print("\n\n👋 Quiz interrupted by user.")
        return 0
    
    # Return appropriate exit code
    if args.show_answers:
        return 0  # Review mode always succeeds
    return 0 if results.get('passed', False) else 1


if __name__ == "__main__":
    sys.exit(main())
