#!/usr/bin/env python3
"""
Formative Quiz Runner - Week 3: Network Programming
NETWORKING class - ASE, CSIE | by ing. dr. Antonio Clim

Usage:
    python run_quiz.py              # Interactive quiz
    python run_quiz.py --validate   # Validate structure
    python run_quiz.py --export-lms moodle  # Export to Moodle
"""
from __future__ import annotations
import argparse
import json
import random
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pip install pyyaml")
    sys.exit(1)

QUIZ_FILE = Path(__file__).parent / "quiz.yaml"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    END = '\033[0m'

def load_quiz(path: Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def validate_quiz(quiz: dict) -> list[str]:
    errors = []
    if 'metadata' not in quiz:
        errors.append("Missing metadata")
    if 'questions' not in quiz:
        errors.append("Missing questions")
    for q in quiz.get('questions', []):
        for field in ['id', 'lo_ref', 'bloom_level', 'type', 'stem', 'correct']:
            if field not in q:
                errors.append(f"Question {q.get('id','?')}: missing {field}")
    return errors

def run_quiz(quiz: dict, randomise: bool = False, limit: int | None = None) -> dict:
    questions = quiz['questions'].copy()
    if randomise:
        random.shuffle(questions)
    if limit:
        questions = questions[:limit]
    
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}  {quiz['metadata']['title']}{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"  Questions: {len(questions)} | Passing: {quiz['metadata'].get('passing_score', 70)}%\n")
    
    results = {'correct': 0, 'total': len(questions), 'answers': []}
    
    for i, q in enumerate(questions, 1):
        print(f"\n{Colors.CYAN}Q{i}/{len(questions)}{Colors.END} [{q['bloom_level']}] [{q['lo_ref']}]")
        print(q['stem'].strip())
        
        if q['type'] == 'multiple_choice':
            for k, v in sorted(q.get('options', {}).items()):
                print(f"  {Colors.YELLOW}{k}){Colors.END} {v}")
            answer = input(f"\n{Colors.GREEN}Answer: {Colors.END}").strip().lower()
            correct = answer == q['correct'].lower()
        else:
            answer = input(f"\n{Colors.GREEN}Answer: {Colors.END}").strip()
            correct_answers = q['correct'] if isinstance(q['correct'], list) else [q['correct']]
            correct = answer in correct_answers
        
        if correct:
            print(f"{Colors.GREEN}✓ Correct!{Colors.END}")
            results['correct'] += 1
        else:
            print(f"{Colors.RED}✗ Incorrect. Answer: {q['correct']}{Colors.END}")
        
        if 'explanation' in q:
            print(f"{Colors.CYAN}Explanation:{Colors.END} {q['explanation'][:200]}...")
        
        results['answers'].append({'id': q['id'], 'correct': correct})
    
    pct = round(results['correct'] / results['total'] * 100, 1) if results['total'] else 0
    passed = pct >= quiz['metadata'].get('passing_score', 70)
    
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"  Score: {results['correct']}/{results['total']} ({pct}%)")
    print(f"  Status: {Colors.GREEN if passed else Colors.RED}{'PASSED' if passed else 'NEEDS REVIEW'}{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")
    
    return results

def export_moodle(quiz: dict, output: Path) -> None:
    lines = [f"// {quiz['metadata']['title']}", "$CATEGORY: Week3_NetworkProgramming", ""]
    for q in quiz['questions']:
        if q['type'] == 'multiple_choice':
            stem = q['stem'].replace('\n', ' ').replace('{', '\\{')
            lines.append(f"::{q['id']}::{stem} {{")
            for k, v in sorted(q.get('options', {}).items()):
                prefix = "=" if k == q['correct'] else "~"
                lines.append(f"  {prefix}{v}")
            lines.append("}")
            lines.append("")
    output.write_text('\n'.join(lines), encoding='utf-8')
    print(f"{Colors.GREEN}✓ Exported to Moodle GIFT: {output}{Colors.END}")

def export_json(quiz: dict, output: Path) -> None:
    data = {'metadata': quiz['metadata'], 'questions': quiz['questions'], 'exported': datetime.now().isoformat()}
    output.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"{Colors.GREEN}✓ Exported to JSON: {output}{Colors.END}")

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Quiz runner with LMS export")
    parser.add_argument('--quiz', type=Path, default=QUIZ_FILE)
    parser.add_argument('--random', action='store_true')
    parser.add_argument('--limit', type=int)
    parser.add_argument('--validate', action='store_true')
    parser.add_argument('--export-lms', choices=['moodle', 'canvas', 'json'])
    args = parser.parse_args(argv)
    
    quiz = load_quiz(args.quiz)
    
    if args.validate:
        errors = validate_quiz(quiz)
        if errors:
            print(f"{Colors.RED}Errors: {errors}{Colors.END}")
            return 1
        print(f"{Colors.GREEN}✓ Quiz structure is valid{Colors.END}")
        print(f"  Questions: {len(quiz['questions'])}")
        return 0
    
    if args.export_lms:
        out_dir = args.quiz.parent
        if args.export_lms == 'moodle':
            export_moodle(quiz, out_dir / 'quiz_moodle.gift')
        elif args.export_lms == 'json' or args.export_lms == 'canvas':
            export_json(quiz, out_dir / f'quiz_{args.export_lms}.json')
        return 0
    
    results = run_quiz(quiz, args.random, args.limit)
    return 0 if results['correct'] / results['total'] >= 0.7 else 1

if __name__ == "__main__":
    sys.exit(main())
