#!/usr/bin/env python3
"""
run_quiz.py — Interactive Quiz Runner for Week 14
NETWORKING class — ASE, CSIE | Computer Networks Laboratory
by ing. dr. Antonio Clim

Runs formative assessment quizzes from YAML format with:
- Interactive CLI interface
- Immediate feedback per question
- Score tracking and LO coverage analysis
- Export capabilities (JSON, Moodle XML)

Usage:
    python formative/run_quiz.py                    # Interactive mode
    python formative/run_quiz.py --random           # Randomize question order
    python formative/run_quiz.py --limit 5          # Limit to N questions
    python formative/run_quiz.py --lo LO1 LO2       # Filter by Learning Objectives
    python formative/run_quiz.py --export json      # Export to JSON
    python formative/run_quiz.py --help             # Show all options
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import json
import random
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml
except ImportError:
    print("Error: PyYAML required. Install with: pip install pyyaml")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY_UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════
class Colours:
    """ANSI colour codes for terminal output."""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ENDC = '\033[0m'

    @classmethod
    def disable(cls) -> None:
        """Disable colours for non-terminal output."""
        for attr in dir(cls):
            if not attr.startswith('_') and attr.isupper():
                setattr(cls, attr, '')


def print_banner(text: str, char: str = "═", width: int = 70) -> None:
    """Print a banner with decorative borders."""
    print(f"\n{Colours.CYAN}{char * width}{Colours.ENDC}")
    print(f"{Colours.BOLD}  {text}{Colours.ENDC}")
    print(f"{Colours.CYAN}{char * width}{Colours.ENDC}\n")


def print_box(lines: List[str], title: str = "") -> None:
    """Print content in a box."""
    width = max(len(line) for line in lines) + 4
    width = max(width, len(title) + 4)
    
    print(f"╔{'═' * width}╗")
    if title:
        print(f"║ {Colours.BOLD}{title}{Colours.ENDC}{' ' * (width - len(title) - 1)}║")
        print(f"╠{'═' * width}╣")
    for line in lines:
        print(f"║ {line}{' ' * (width - len(line) - 1)}║")
    print(f"╚{'═' * width}╝")


# ═══════════════════════════════════════════════════════════════════════════════
# DATA_MODELS
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class QuestionResult:
    """Result of answering a single question."""
    question_id: str
    lo_ref: str
    bloom_level: str
    points_possible: int
    points_earned: int
    correct: bool
    user_answer: str
    correct_answer: str
    time_taken_seconds: float = 0.0


@dataclass
class QuizResult:
    """Complete quiz session result."""
    quiz_title: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    results: List[QuestionResult] = field(default_factory=list)
    prediction: Optional[int] = None
    
    @property
    def total_questions(self) -> int:
        return len(self.results)
    
    @property
    def correct_count(self) -> int:
        return sum(1 for r in self.results if r.correct)
    
    @property
    def total_points(self) -> int:
        return sum(r.points_possible for r in self.results)
    
    @property
    def earned_points(self) -> int:
        return sum(r.points_earned for r in self.results)
    
    @property
    def percentage(self) -> float:
        if self.total_points == 0:
            return 0.0
        return (self.earned_points / self.total_points) * 100
    
    @property
    def lo_scores(self) -> Dict[str, Dict[str, int]]:
        """Calculate scores per Learning Objective."""
        scores: Dict[str, Dict[str, int]] = {}
        for r in self.results:
            if r.lo_ref not in scores:
                scores[r.lo_ref] = {"earned": 0, "possible": 0, "correct": 0, "total": 0}
            scores[r.lo_ref]["earned"] += r.points_earned
            scores[r.lo_ref]["possible"] += r.points_possible
            scores[r.lo_ref]["total"] += 1
            if r.correct:
                scores[r.lo_ref]["correct"] += 1
        return scores


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ_LOADER
# ═══════════════════════════════════════════════════════════════════════════════
def load_quiz(path: Path) -> Dict[str, Any]:
    """Load quiz from YAML file."""
    if not path.exists():
        raise FileNotFoundError(f"Quiz file not found: {path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        quiz = yaml.safe_load(f)
    
    # Validate basic structure
    if 'metadata' not in quiz:
        raise ValueError("Quiz missing 'metadata' section")
    if 'questions' not in quiz:
        raise ValueError("Quiz missing 'questions' section")
    
    return quiz


def filter_questions(
    questions: List[Dict], 
    lo_filter: Optional[List[str]] = None,
    bloom_filter: Optional[List[str]] = None,
    difficulty_filter: Optional[List[str]] = None
) -> List[Dict]:
    """Filter questions by criteria."""
    filtered = questions
    
    if lo_filter:
        filtered = [q for q in filtered if q.get('lo_ref') in lo_filter]
    
    if bloom_filter:
        filtered = [q for q in filtered if q.get('bloom_level') in bloom_filter]
    
    if difficulty_filter:
        filtered = [q for q in filtered if q.get('difficulty') in difficulty_filter]
    
    return filtered


# ═══════════════════════════════════════════════════════════════════════════════
# QUESTION_HANDLERS
# ═══════════════════════════════════════════════════════════════════════════════
def ask_multiple_choice(question: Dict, index: int, total: int) -> QuestionResult:
    """Handle multiple choice question."""
    q_id = question.get('id', f'q{index}')
    lo_ref = question.get('lo_ref', 'Unknown')
    bloom = question.get('bloom_level', 'Unknown')
    points = question.get('points', 1)
    stem = question.get('stem', '').strip()
    options = question.get('options', {})
    correct = question.get('correct', '').lower()
    explanation = question.get('explanation', '')
    hint = question.get('hint', '')
    
    # Display question
    print(f"\n{Colours.BOLD}Question {index}/{total}{Colours.ENDC} "
          f"{Colours.DIM}[{bloom}] [{lo_ref}] [{points} pt]{Colours.ENDC}")
    print(f"\n{stem}\n")
    
    # Display options
    for key, value in sorted(options.items()):
        print(f"  {Colours.CYAN}{key.upper()}){Colours.ENDC} {value}")
    
    # Show hint if available
    if hint:
        print(f"\n  {Colours.DIM}💡 Hint: {hint}{Colours.ENDC}")
    
    # Get user input
    valid_options = [k.lower() for k in options.keys()]
    user_answer = ""
    
    while True:
        try:
            user_input = input(f"\n{Colours.YELLOW}Your answer ({'/'.join(valid_options)}, or 'skip'): {Colours.ENDC}").strip().lower()
            
            if user_input == 'skip':
                user_answer = ""
                break
            elif user_input in valid_options:
                user_answer = user_input
                break
            else:
                print(f"  {Colours.RED}Invalid option. Try again.{Colours.ENDC}")
        except (EOFError, KeyboardInterrupt):
            print("\n")
            user_answer = ""
            break
    
    # Check answer
    is_correct = user_answer == correct
    points_earned = points if is_correct else 0
    
    # Display feedback
    if is_correct:
        print(f"\n  {Colours.GREEN}✓ Correct!{Colours.ENDC}")
    else:
        correct_text = options.get(correct, correct)
        print(f"\n  {Colours.RED}✗ Incorrect.{Colours.ENDC}")
        print(f"  {Colours.CYAN}Correct answer: {correct.upper()}) {correct_text}{Colours.ENDC}")
    
    # Show explanation
    if explanation:
        print(f"\n  {Colours.DIM}📖 Explanation:{Colours.ENDC}")
        for line in explanation.strip().split('\n'):
            print(f"     {line}")
    
    return QuestionResult(
        question_id=q_id,
        lo_ref=lo_ref,
        bloom_level=bloom,
        points_possible=points,
        points_earned=points_earned,
        correct=is_correct,
        user_answer=user_answer,
        correct_answer=correct
    )


def ask_fill_blank(question: Dict, index: int, total: int) -> QuestionResult:
    """Handle fill-in-the-blank question."""
    q_id = question.get('id', f'q{index}')
    lo_ref = question.get('lo_ref', 'Unknown')
    bloom = question.get('bloom_level', 'Unknown')
    points = question.get('points', 1)
    stem = question.get('stem', '').strip()
    correct_answers = question.get('correct', [])
    case_sensitive = question.get('case_sensitive', False)
    explanation = question.get('explanation', '')
    hint = question.get('hint', '')
    
    if isinstance(correct_answers, str):
        correct_answers = [correct_answers]
    
    # Display question
    print(f"\n{Colours.BOLD}Question {index}/{total}{Colours.ENDC} "
          f"{Colours.DIM}[{bloom}] [{lo_ref}] [{points} pt]{Colours.ENDC}")
    print(f"\n{stem}\n")
    
    # Show hint
    if hint:
        print(f"  {Colours.DIM}💡 Hint: {hint}{Colours.ENDC}")
    
    # Get user input
    try:
        user_answer = input(f"\n{Colours.YELLOW}Your answer (or 'skip'): {Colours.ENDC}").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n")
        user_answer = ""
    
    if user_answer.lower() == 'skip':
        user_answer = ""
    
    # Check answer
    if case_sensitive:
        is_correct = user_answer in correct_answers
    else:
        is_correct = user_answer.lower() in [a.lower() for a in correct_answers]
    
    points_earned = points if is_correct else 0
    
    # Display feedback
    if is_correct:
        print(f"\n  {Colours.GREEN}✓ Correct!{Colours.ENDC}")
    else:
        print(f"\n  {Colours.RED}✗ Incorrect.{Colours.ENDC}")
        print(f"  {Colours.CYAN}Accepted answers: {', '.join(correct_answers)}{Colours.ENDC}")
    
    # Show explanation
    if explanation:
        print(f"\n  {Colours.DIM}📖 Explanation:{Colours.ENDC}")
        for line in explanation.strip().split('\n'):
            print(f"     {line}")
    
    return QuestionResult(
        question_id=q_id,
        lo_ref=lo_ref,
        bloom_level=bloom,
        points_possible=points,
        points_earned=points_earned,
        correct=is_correct,
        user_answer=user_answer,
        correct_answer=correct_answers[0] if correct_answers else ""
    )


def ask_question(question: Dict, index: int, total: int) -> QuestionResult:
    """Route question to appropriate handler."""
    q_type = question.get('type', 'multiple_choice')
    
    if q_type == 'multiple_choice':
        return ask_multiple_choice(question, index, total)
    elif q_type == 'fill_blank':
        return ask_fill_blank(question, index, total)
    else:
        print(f"  {Colours.YELLOW}Unknown question type: {q_type}, treating as multiple choice{Colours.ENDC}")
        return ask_multiple_choice(question, index, total)


# ═══════════════════════════════════════════════════════════════════════════════
# PREDICTION_PROMPT
# ═══════════════════════════════════════════════════════════════════════════════
def prompt_prediction(total_questions: int, total_points: int) -> Optional[int]:
    """Ask student to predict their score before starting."""
    print(f"\n{Colours.MAGENTA}💭 PREDICTION{Colours.ENDC}")
    print(f"Before starting, predict how many points you'll score out of {total_points}.")
    print("(This helps with metacognitive awareness - no penalty for being wrong!)")
    
    try:
        prediction_str = input(f"\n{Colours.YELLOW}Your prediction (0-{total_points}, or Enter to skip): {Colours.ENDC}").strip()
        if prediction_str:
            prediction = int(prediction_str)
            if 0 <= prediction <= total_points:
                print(f"\n  You predicted: {prediction}/{total_points} points. Let's see how you do!\n")
                return prediction
    except (ValueError, EOFError, KeyboardInterrupt):
        pass
    
    print("\n  Skipping prediction. Starting quiz...\n")
    return None


# ═══════════════════════════════════════════════════════════════════════════════
# RESULT_DISPLAY
# ═══════════════════════════════════════════════════════════════════════════════
def display_results(result: QuizResult, quiz: Dict) -> None:
    """Display comprehensive quiz results."""
    scoring = quiz.get('scoring', {})
    feedback = quiz.get('feedback', {})
    passing_threshold = scoring.get('passing_threshold', 70)
    
    passed = result.earned_points >= passing_threshold
    
    print_banner(f"Quiz Complete: {result.quiz_title}")
    
    # Score summary
    score_colour = Colours.GREEN if passed else Colours.RED
    print(f"  {Colours.BOLD}Final Score:{Colours.ENDC} {score_colour}{result.earned_points}/{result.total_points} "
          f"({result.percentage:.1f}%){Colours.ENDC}")
    print(f"  {Colours.BOLD}Questions:{Colours.ENDC} {result.correct_count}/{result.total_questions} correct")
    print(f"  {Colours.BOLD}Status:{Colours.ENDC} {score_colour}{'PASSED ✓' if passed else 'NEEDS REVIEW ✗'}{Colours.ENDC}")
    
    # Prediction comparison
    if result.prediction is not None:
        diff = result.earned_points - result.prediction
        diff_str = f"+{diff}" if diff > 0 else str(diff)
        print(f"\n  {Colours.MAGENTA}💭 Prediction comparison:{Colours.ENDC}")
        print(f"     Predicted: {result.prediction} | Actual: {result.earned_points} | Diff: {diff_str}")
        
        if abs(diff) <= 2:
            print(f"     {Colours.GREEN}Excellent self-assessment!{Colours.ENDC}")
        elif diff > 0:
            print(f"     {Colours.CYAN}You did better than expected!{Colours.ENDC}")
        else:
            print(f"     {Colours.YELLOW}Room for improvement in self-assessment.{Colours.ENDC}")
    
    # LO breakdown
    print(f"\n  {Colours.BOLD}Learning Objective Breakdown:{Colours.ENDC}")
    lo_scores = result.lo_scores
    for lo, scores in sorted(lo_scores.items()):
        pct = (scores['earned'] / scores['possible'] * 100) if scores['possible'] > 0 else 0
        lo_colour = Colours.GREEN if pct >= 70 else Colours.YELLOW if pct >= 50 else Colours.RED
        print(f"     {lo}: {lo_colour}{scores['earned']}/{scores['possible']} ({pct:.0f}%){Colours.ENDC} "
              f"[{scores['correct']}/{scores['total']} questions]")
    
    # Grade
    grade_boundaries = scoring.get('grade_boundaries', {})
    grade = "F"
    for g, info in sorted(grade_boundaries.items(), key=lambda x: x[1].get('min_points', 0), reverse=True):
        if result.earned_points >= info.get('min_points', 0):
            grade = g
            break
    
    print(f"\n  {Colours.BOLD}Grade:{Colours.ENDC} {Colours.CYAN}{grade}{Colours.ENDC}")
    
    # Feedback
    if passed:
        on_pass = feedback.get('on_pass', '')
        if on_pass:
            print(f"\n{Colours.GREEN}{on_pass}{Colours.ENDC}")
    else:
        on_fail = feedback.get('on_fail', '')
        if on_fail:
            print(f"\n{Colours.YELLOW}{on_fail}{Colours.ENDC}")
        
        # Per-LO feedback for weak areas
        per_lo = feedback.get('per_lo_feedback', {})
        weak_los = [lo for lo, scores in lo_scores.items() 
                   if scores['possible'] > 0 and (scores['earned'] / scores['possible']) < 0.7]
        
        if weak_los and per_lo:
            print(f"\n  {Colours.BOLD}Recommended review for weak areas:{Colours.ENDC}")
            for lo in weak_los:
                if lo in per_lo:
                    print(f"\n  {Colours.CYAN}{lo}:{Colours.ENDC}")
                    for line in per_lo[lo].strip().split('\n'):
                        print(f"     {line}")
    
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def export_to_json(quiz: Dict, output_path: Path) -> None:
    """Export quiz to JSON format."""
    export_config = quiz.get('export', {}).get('json', {})
    include_explanations = export_config.get('include_explanations', True)
    include_verification = export_config.get('include_verification', False)
    
    export_data = {
        "metadata": quiz.get('metadata', {}),
        "questions": []
    }
    
    for q in quiz.get('questions', []):
        q_export = {
            "id": q.get('id'),
            "type": q.get('type'),
            "bloom_level": q.get('bloom_level'),
            "lo_ref": q.get('lo_ref'),
            "difficulty": q.get('difficulty'),
            "points": q.get('points'),
            "stem": q.get('stem'),
            "correct": q.get('correct')
        }
        
        if q.get('type') == 'multiple_choice':
            q_export['options'] = q.get('options')
        
        if include_explanations:
            q_export['explanation'] = q.get('explanation')
            q_export['hint'] = q.get('hint')
        
        if include_verification:
            q_export['verification'] = q.get('verification')
        
        export_data['questions'].append(q_export)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    print(f"Quiz exported to: {output_path}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_QUIZ_RUNNER
# ═══════════════════════════════════════════════════════════════════════════════
def run_quiz(
    quiz: Dict,
    randomize: bool = False,
    limit: Optional[int] = None,
    lo_filter: Optional[List[str]] = None,
    show_prediction: bool = True
) -> QuizResult:
    """Run interactive quiz session."""
    metadata = quiz.get('metadata', {})
    questions = quiz.get('questions', [])
    
    # Apply filters
    questions = filter_questions(questions, lo_filter=lo_filter)
    
    # Randomize if requested
    if randomize:
        questions = questions.copy()
        random.shuffle(questions)
    
    # Limit questions if requested
    if limit and limit < len(questions):
        questions = questions[:limit]
    
    total_points = sum(q.get('points', 1) for q in questions)
    
    # Start quiz
    title = f"Week {metadata.get('week', '?')}: {metadata.get('topic', 'Quiz')}"
    print_banner(title)
    
    print(f"  {Colours.BOLD}Questions:{Colours.ENDC} {len(questions)}")
    print(f"  {Colours.BOLD}Total Points:{Colours.ENDC} {total_points}")
    print(f"  {Colours.BOLD}Passing Score:{Colours.ENDC} {metadata.get('passing_score_percent', 70)}%")
    print(f"  {Colours.BOLD}Estimated Time:{Colours.ENDC} {metadata.get('estimated_time_minutes', 15)} minutes")
    
    # Prediction
    prediction = None
    if show_prediction:
        prediction = prompt_prediction(len(questions), total_points)
    
    # Initialize result
    result = QuizResult(
        quiz_title=title,
        started_at=datetime.now(),
        prediction=prediction
    )
    
    # Run questions
    for i, question in enumerate(questions, 1):
        q_result = ask_question(question, i, len(questions))
        result.results.append(q_result)
        
        # Progress indicator
        progress = i / len(questions)
        bar_width = 30
        filled = int(bar_width * progress)
        bar = f"[{'█' * filled}{'░' * (bar_width - filled)}]"
        print(f"\n  {Colours.DIM}Progress: {bar} {i}/{len(questions)}{Colours.ENDC}")
    
    result.ended_at = datetime.now()
    
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# PARSE_ARGUMENTS
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Interactive Quiz Runner for Week 14 Lab Kit",
        epilog="NETWORKING class — ASE, CSIE | by ing. dr. Antonio Clim"
    )
    
    parser.add_argument(
        '--quiz', '-q',
        type=Path,
        default=Path(__file__).parent / 'quiz_week14.yaml',
        help='Path to quiz YAML file (default: quiz_week14.yaml)'
    )
    
    parser.add_argument(
        '--random', '-r',
        action='store_true',
        help='Randomize question order'
    )
    
    parser.add_argument(
        '--limit', '-l',
        type=int,
        help='Limit number of questions'
    )
    
    parser.add_argument(
        '--lo',
        nargs='+',
        help='Filter by Learning Objectives (e.g., --lo LO1 LO2)'
    )
    
    parser.add_argument(
        '--no-prediction',
        action='store_true',
        help='Skip prediction prompt'
    )
    
    parser.add_argument(
        '--export',
        choices=['json'],
        help='Export quiz to format instead of running'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=Path,
        help='Output path for export'
    )
    
    parser.add_argument(
        '--no-colour',
        action='store_true',
        help='Disable coloured output'
    )
    
    return parser.parse_args()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point."""
    args = parse_args()
    
    # Disable colours if requested
    if args.no_colour:
        Colours.disable()
    
    # Load quiz
    try:
        quiz = load_quiz(args.quiz)
    except (FileNotFoundError, ValueError) as e:
        print(f"{Colours.RED}Error: {e}{Colours.ENDC}")
        return 1
    
    # Export mode
    if args.export:
        output_path = args.output or Path(f"quiz_export.{args.export}")
        if args.export == 'json':
            export_to_json(quiz, output_path)
        return 0
    
    # Interactive mode
    try:
        result = run_quiz(
            quiz,
            randomize=args.random,
            limit=args.limit,
            lo_filter=args.lo,
            show_prediction=not args.no_prediction
        )
        
        display_results(result, quiz)
        
        # Return appropriate exit code
        scoring = quiz.get('scoring', {})
        passing = scoring.get('passing_threshold', 70)
        return 0 if result.earned_points >= passing else 1
        
    except KeyboardInterrupt:
        print(f"\n\n{Colours.YELLOW}Quiz interrupted. Progress not saved.{Colours.ENDC}")
        return 130


if __name__ == "__main__":
    sys.exit(main())
