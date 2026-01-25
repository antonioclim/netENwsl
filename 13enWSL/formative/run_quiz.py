#!/usr/bin/env python3
"""
Formative Quiz Runner — Week 13: IoT and Security
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

LEARNING OBJECTIVES:
- Self-assessment of knowledge retention
- Identification of misconceptions
- Bloom taxonomy level awareness

USAGE:
    python formative/run_quiz.py                      # Full quiz
    python formative/run_quiz.py --random --limit 5   # Random 5 questions
    python formative/run_quiz.py --bloom apply        # Only Apply level
    python formative/run_quiz.py --export results.json # Export results
    python formative/run_quiz.py --export-moodle quiz.xml  # Moodle export
    python formative/run_quiz.py --export-canvas quiz.json # Canvas export
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class QuestionResult:
    """Result for a single question."""
    question_id: str
    bloom_level: str
    lo_ref: str
    correct: bool
    time_seconds: float
    user_answer: str
    correct_answer: str


@dataclass
class QuizResult:
    """Complete quiz attempt result."""
    timestamp: str
    total_questions: int
    correct_answers: int
    score_percent: float
    passed: bool
    duration_seconds: float
    by_bloom_level: Dict[str, Dict[str, int]] = field(default_factory=dict)
    by_lo: Dict[str, Dict[str, int]] = field(default_factory=dict)
    question_results: List[QuestionResult] = field(default_factory=list)


# ═══════════════════════════════════════════════════════════════════════════════
# TERMINAL COLOURS
# ═══════════════════════════════════════════════════════════════════════════════

class Clr:
    """ANSI colour codes for terminal output."""
    G = "\033[92m"   # Green
    R = "\033[91m"   # Red
    Y = "\033[93m"   # Yellow
    B = "\033[94m"   # Blue
    C = "\033[96m"   # Cyan
    BD = "\033[1m"   # Bold
    RS = "\033[0m"   # Reset


if not sys.stdout.isatty():
    Clr.G = Clr.R = Clr.Y = Clr.B = Clr.C = Clr.BD = Clr.RS = ""


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ LOADING
# ═══════════════════════════════════════════════════════════════════════════════

def load_quiz(quiz_path: Path) -> Dict[str, Any]:
    """Load quiz from YAML file."""
    with open(quiz_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


# ═══════════════════════════════════════════════════════════════════════════════
# QUESTION HANDLERS — MULTIPLE CHOICE
# ═══════════════════════════════════════════════════════════════════════════════

def display_mcq_options(options: Dict[str, str]) -> None:
    """Display multiple choice options."""
    for key, val in options.items():
        print(f"  {Clr.C}{key}){Clr.RS} {val}")


def get_mcq_answer() -> str:
    """Get multiple choice answer from user."""
    return input(f"\n{Clr.BD}→ Your answer (a/b/c/d):{Clr.RS} ").strip().lower()


def ask_multiple_choice(question: Dict[str, Any]) -> tuple[bool, str, str]:
    """Present multiple choice question and get answer."""
    display_mcq_options(question["options"])
    answer = get_mcq_answer()
    correct = question["correct"].lower()
    return (answer == correct, answer, correct)


# ═══════════════════════════════════════════════════════════════════════════════
# QUESTION HANDLERS — FILL IN BLANK
# ═══════════════════════════════════════════════════════════════════════════════

def check_single_answers(answer: str, correct_list: List[str]) -> bool:
    """Check answer against list of acceptable single answers."""
    return any(
        answer.lower() == a.lower() or answer.lower() in a.lower()
        for a in correct_list
    )


def check_multi_part_answers(answer: str, correct_combos: List[List[str]]) -> bool:
    """Check answer against list of multi-part answer combinations."""
    return any(
        all(part.lower() in answer.lower() for part in combo)
        for combo in correct_combos
    )


def format_correct_display(correct_answers: list) -> str:
    """Format correct answers for display."""
    if isinstance(correct_answers[0], list):
        return " | ".join([", ".join(c) for c in correct_answers])
    return ", ".join(correct_answers)


def ask_fill_blank(question: Dict[str, Any]) -> tuple[bool, str, str]:
    """Present fill-in-the-blank question and get answer."""
    if "hint" in question:
        print(f"  {Clr.Y}💡 Hint: {question['hint']}{Clr.RS}")
    
    answer = input(f"\n{Clr.BD}→ Your answer:{Clr.RS} ").strip()
    correct_answers = question["correct"]
    
    if isinstance(correct_answers[0], list):
        is_correct = check_multi_part_answers(answer, correct_answers)
    else:
        is_correct = check_single_answers(answer, correct_answers)
    
    return (is_correct, answer, format_correct_display(correct_answers))


# ═══════════════════════════════════════════════════════════════════════════════
# QUESTION HANDLERS — SHORT ANSWER
# ═══════════════════════════════════════════════════════════════════════════════

def display_rubric(rubric: List[str]) -> None:
    """Display rubric for self-evaluation."""
    print(f"\n  {Clr.Y}📝 Rubric (self-evaluate):{Clr.RS}")
    for i, criterion in enumerate(rubric, 1):
        print(f"     {i}. {criterion}")


def display_example_answer(example: str) -> None:
    """Display example answer."""
    print(f"\n  {Clr.G}Example answer:{Clr.RS}")
    for line in example.strip().split("\n"):
        print(f"    {line}")


def get_self_score() -> int:
    """Get self-evaluation score from user."""
    try:
        return int(input(f"\n{Clr.BD}→ Self-score (0-3):{Clr.RS} ").strip())
    except ValueError:
        return 0


def ask_short_answer(question: Dict[str, Any]) -> tuple[bool, str, str]:
    """Present short answer question with self-evaluation."""
    display_rubric(question.get("rubric", []))
    
    print(f"\n  {Clr.C}Write your answer below (or type it mentally):{Clr.RS}")
    input("  Press Enter when ready to self-evaluate...")
    
    if "example_answer" in question:
        display_example_answer(question["example_answer"])
    
    score = get_self_score()
    return (score >= 2, f"self-score: {score}", "See rubric above")


# ═══════════════════════════════════════════════════════════════════════════════
# QUESTION FILTERING
# ═══════════════════════════════════════════════════════════════════════════════

def filter_by_bloom(questions: List[Dict], bloom: str) -> List[Dict]:
    """Filter questions by Bloom taxonomy level."""
    return [q for q in questions if q.get("bloom_level", "").lower() == bloom.lower()]


def apply_limit(questions: List[Dict], limit: Optional[int]) -> List[Dict]:
    """Apply question limit."""
    if limit and limit < len(questions):
        return questions[:limit]
    return questions


def prepare_questions(
    questions: List[Dict],
    bloom_filter: Optional[str],
    randomise: bool,
    limit: Optional[int]
) -> List[Dict]:
    """Prepare question list with filters and randomisation."""
    result = questions.copy()
    if bloom_filter:
        result = filter_by_bloom(result, bloom_filter)
    if randomise:
        random.shuffle(result)
    return apply_limit(result, limit)


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ SESSION DISPLAY
# ═══════════════════════════════════════════════════════════════════════════════

def print_quiz_header(metadata: Dict[str, Any], count: int) -> None:
    """Display quiz header."""
    print(f"\n{Clr.BD}{'═' * 64}{Clr.RS}")
    print(f"{Clr.BD}  📝 QUIZ: {metadata.get('topic', 'Unknown')}{Clr.RS}")
    print(f"  Questions: {count} | Passing: {metadata.get('passing_score', 70)}%")
    print(f"{Clr.BD}{'═' * 64}{Clr.RS}")
    input(f"\n{Clr.C}Press Enter to start...{Clr.RS}")


def print_question_header(idx: int, total: int, q: Dict[str, Any]) -> None:
    """Display question header."""
    bloom = q.get("bloom_level", "?")
    lo = q.get("lo_ref", "?")
    diff = q.get("difficulty", "?")
    
    print(f"\n{Clr.BD}{'─' * 64}{Clr.RS}")
    print(f"{Clr.BD}Q{idx}/{total}{Clr.RS} [{Clr.Y}{diff}{Clr.RS}] "
          f"[Bloom: {Clr.B}{bloom.upper()}{Clr.RS}] [{Clr.C}{lo}{Clr.RS}]")
    print(f"{'─' * 64}")
    print(f"\n{q['stem'].strip()}\n")


def print_result_feedback(is_correct: bool, correct_ans: str) -> None:
    """Display result feedback."""
    if is_correct:
        print(f"\n{Clr.G}✅ CORRECT!{Clr.RS}")
    else:
        print(f"\n{Clr.R}❌ Wrong.{Clr.RS} Correct: {Clr.G}{correct_ans}{Clr.RS}")


def print_explanation(explanation: Optional[str]) -> None:
    """Display explanation if available."""
    if explanation:
        print(f"\n{Clr.C}📖 {explanation.strip()}{Clr.RS}")


# ═══════════════════════════════════════════════════════════════════════════════
# STATISTICS TRACKING
# ═══════════════════════════════════════════════════════════════════════════════

def init_stat_entry(stats: Dict, key: str) -> None:
    """Initialise statistics entry if not present."""
    if key not in stats:
        stats[key] = {"total": 0, "correct": 0}


def update_stats(stats: Dict, key: str, is_correct: bool) -> None:
    """Update statistics for a key."""
    init_stat_entry(stats, key)
    stats[key]["total"] += 1
    if is_correct:
        stats[key]["correct"] += 1


def calc_percentage(correct: int, total: int) -> float:
    """Calculate percentage safely."""
    return (correct / total * 100) if total > 0 else 0.0


# ═══════════════════════════════════════════════════════════════════════════════
# RESULTS DISPLAY
# ═══════════════════════════════════════════════════════════════════════════════

def print_bloom_breakdown(stats: Dict[str, Dict[str, int]]) -> None:
    """Print breakdown by Bloom level."""
    print(f"\n  {Clr.BD}By Bloom Level:{Clr.RS}")
    levels = ["remember", "understand", "apply", "analyse", "evaluate", "create"]
    for level in levels:
        if level in stats:
            s = stats[level]
            pct = calc_percentage(s['correct'], s['total'])
            bar = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
            clr = Clr.G if pct >= 70 else Clr.Y if pct >= 50 else Clr.R
            print(f"    {level.capitalize():12s}: {clr}{bar} {s['correct']}/{s['total']} ({pct:.0f}%){Clr.RS}")


def print_lo_breakdown(stats: Dict[str, Dict[str, int]]) -> None:
    """Print breakdown by Learning Objective."""
    print(f"\n  {Clr.BD}By Learning Objective:{Clr.RS}")
    for lo, s in sorted(stats.items()):
        pct = calc_percentage(s['correct'], s['total'])
        icon = "✅" if pct >= 70 else "⚠️" if pct >= 50 else "❌"
        print(f"    {lo}: {icon} {s['correct']}/{s['total']}")


def print_final_results(
    correct: int, total: int, score: float, passed: bool,
    duration: float, bloom_stats: Dict, lo_stats: Dict
) -> None:
    """Print final quiz results."""
    print(f"\n{Clr.BD}{'═' * 64}{Clr.RS}")
    print(f"{Clr.BD}  📊 RESULTS{Clr.RS}")
    print(f"{'═' * 64}")
    print(f"  Score: {Clr.BD}{correct}/{total} ({score:.1f}%){Clr.RS}")
    
    status = f"{Clr.G}✅ PASSED{Clr.RS}" if passed else f"{Clr.R}❌ NEEDS REVIEW{Clr.RS}"
    print(f"  Status: {status}")
    print(f"  Time: {duration:.1f}s ({duration/60:.1f} min)")
    
    print_bloom_breakdown(bloom_stats)
    print_lo_breakdown(lo_stats)
    print(f"{Clr.BD}{'═' * 64}{Clr.RS}\n")


# ═══════════════════════════════════════════════════════════════════════════════
# QUESTION PROCESSING
# ═══════════════════════════════════════════════════════════════════════════════

def process_question(question: Dict[str, Any]) -> tuple[bool, str, str]:
    """Process a single question based on its type."""
    q_type = question["type"]
    if q_type == "multiple_choice":
        return ask_multiple_choice(question)
    elif q_type == "fill_blank":
        return ask_fill_blank(question)
    elif q_type == "short_answer":
        return ask_short_answer(question)
    print(f"{Clr.R}Unknown question type: {q_type}{Clr.RS}")
    return (False, "", "")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN QUIZ RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

def run_interactive_quiz(
    quiz: Dict[str, Any],
    randomise: bool = False,
    limit: Optional[int] = None,
    bloom_filter: Optional[str] = None
) -> QuizResult:
    """Run interactive quiz session."""
    questions = prepare_questions(
        quiz.get("questions", []), bloom_filter, randomise, limit
    )
    metadata = quiz.get("metadata", {})
    
    if not questions:
        print(f"{Clr.R}No questions match the criteria.{Clr.RS}")
        return QuizResult(
            timestamp=datetime.now().isoformat(), total_questions=0,
            correct_answers=0, score_percent=0.0, passed=False, duration_seconds=0.0
        )
    
    print_quiz_header(metadata, len(questions))
    
    start_time = time.time()
    correct = 0
    bloom_stats: Dict[str, Dict[str, int]] = {}
    lo_stats: Dict[str, Dict[str, int]] = {}
    results: List[QuestionResult] = []
    
    for i, q in enumerate(questions, 1):
        q_start = time.time()
        bloom, lo = q.get("bloom_level", "?"), q.get("lo_ref", "?")
        
        print_question_header(i, len(questions), q)
        is_correct, user_ans, correct_ans = process_question(q)
        
        print_result_feedback(is_correct, correct_ans)
        print_explanation(q.get("explanation"))
        
        update_stats(bloom_stats, bloom, is_correct)
        update_stats(lo_stats, lo, is_correct)
        
        if is_correct:
            correct += 1
        
        results.append(QuestionResult(
            question_id=q.get("id", f"q{i}"), bloom_level=bloom, lo_ref=lo,
            correct=is_correct, time_seconds=round(time.time() - q_start, 2),
            user_answer=user_ans, correct_answer=correct_ans
        ))
    
    duration = time.time() - start_time
    score = calc_percentage(correct, len(questions))
    passed = score >= metadata.get("passing_score", 70)
    
    print_final_results(correct, len(questions), score, passed, duration, bloom_stats, lo_stats)
    
    return QuizResult(
        timestamp=datetime.now().isoformat(), total_questions=len(questions),
        correct_answers=correct, score_percent=round(score, 2), passed=passed,
        duration_seconds=round(duration, 2), by_bloom_level=bloom_stats,
        by_lo=lo_stats, question_results=results
    )


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT — JSON RESULTS
# ═══════════════════════════════════════════════════════════════════════════════

def export_results(result: QuizResult, output_path: Path) -> None:
    """Export quiz results to JSON file."""
    data = asdict(result)
    data["question_results"] = [asdict(qr) for qr in result.question_results]
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"{Clr.G}Results exported to: {output_path}{Clr.RS}")


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT — MOODLE XML
# ═══════════════════════════════════════════════════════════════════════════════

def create_moodle_question(root: ET.Element, q: Dict[str, Any]) -> None:
    """Create a single Moodle question element."""
    question = ET.SubElement(root, "question", type="multichoice")
    
    name = ET.SubElement(question, "name")
    ET.SubElement(name, "text").text = q.get("id", "q")
    
    qtext = ET.SubElement(question, "questiontext", format="html")
    ET.SubElement(qtext, "text").text = f"<p>{q['stem']}</p>"
    
    ET.SubElement(question, "defaultgrade").text = str(q.get("points", 1))
    ET.SubElement(question, "single").text = "true"
    ET.SubElement(question, "shuffleanswers").text = "true"
    
    correct_key = q["correct"].lower()
    for key, text in q["options"].items():
        fraction = "100" if key == correct_key else "0"
        ans = ET.SubElement(question, "answer", fraction=fraction)
        ET.SubElement(ans, "text").text = text


def export_moodle_xml(quiz: Dict[str, Any], output_path: Path) -> None:
    """Export quiz to Moodle XML format."""
    root = ET.Element("quiz")
    
    # Category
    cat = ET.SubElement(root, "question", type="category")
    cat_elem = ET.SubElement(cat, "category")
    topic = quiz.get('metadata', {}).get('topic', 'IoT')
    ET.SubElement(cat_elem, "text").text = f"$course$/Week 13 - {topic}"
    
    # Questions
    for q in quiz.get("questions", []):
        if q["type"] == "multiple_choice":
            create_moodle_question(root, q)
    
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    print(f"{Clr.G}Moodle XML exported to: {output_path}{Clr.RS}")


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT — CANVAS JSON
# ═══════════════════════════════════════════════════════════════════════════════

def create_canvas_question(q: Dict[str, Any]) -> Dict[str, Any]:
    """Create a single Canvas question object."""
    correct_key = q["correct"].lower()
    return {
        "question_name": q.get("id", "question"),
        "question_type": "multiple_choice_question",
        "question_text": q["stem"],
        "points_possible": q.get("points", 1),
        "answers": [
            {"answer_text": text, "answer_weight": 100 if key == correct_key else 0}
            for key, text in q["options"].items()
        ]
    }


def export_canvas_json(quiz: Dict[str, Any], output_path: Path) -> None:
    """Export quiz to Canvas-compatible JSON format."""
    metadata = quiz.get("metadata", {})
    canvas_quiz = {
        "title": f"Week {metadata.get('week', 13)} - {metadata.get('topic', 'Quiz')}",
        "quiz_type": "practice_quiz",
        "time_limit": metadata.get("estimated_time_minutes", 20),
        "allowed_attempts": -1,
        "questions": [
            create_canvas_question(q)
            for q in quiz.get("questions", [])
            if q["type"] == "multiple_choice"
        ]
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(canvas_quiz, f, indent=2, ensure_ascii=False)
    
    print(f"{Clr.G}Canvas JSON exported to: {output_path}{Clr.RS}")


# ═══════════════════════════════════════════════════════════════════════════════
# ARGUMENT PARSING
# ═══════════════════════════════════════════════════════════════════════════════

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Formative Quiz Runner — Week 13: IoT and Security",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                            Run full quiz
  %(prog)s --random --limit 5         Random 5 questions
  %(prog)s --bloom apply              Only 'Apply' level questions
  %(prog)s --export results.json      Export results to JSON
  %(prog)s --export-moodle quiz.xml   Export to Moodle XML
  %(prog)s --export-canvas quiz.json  Export to Canvas JSON
        """
    )
    
    parser.add_argument("--quiz", "-q", type=Path, default=Path(__file__).parent / "quiz.yaml")
    parser.add_argument("--random", "-r", action="store_true", help="Randomise question order")
    parser.add_argument("--limit", "-n", type=int, metavar="N", help="Limit to N questions")
    parser.add_argument(
        "--bloom", "-b",
        choices=["remember", "understand", "apply", "analyse", "evaluate", "create"],
        help="Filter by Bloom taxonomy level"
    )
    parser.add_argument("--export", "-e", type=Path, metavar="FILE", help="Export results to JSON")
    parser.add_argument("--export-moodle", type=Path, metavar="FILE", help="Export quiz to Moodle XML")
    parser.add_argument("--export-canvas", type=Path, metavar="FILE", help="Export quiz to Canvas JSON")
    
    return parser.parse_args()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Main entry point."""
    args = parse_arguments()
    
    if not args.quiz.exists():
        print(f"{Clr.R}ERROR: Quiz file not found: {args.quiz}{Clr.RS}")
        return 1
    
    try:
        quiz = load_quiz(args.quiz)
    except yaml.YAMLError as e:
        print(f"{Clr.R}ERROR: Invalid YAML: {e}{Clr.RS}")
        return 1
    
    # Export-only modes
    if args.export_moodle:
        export_moodle_xml(quiz, args.export_moodle)
        return 0
    
    if args.export_canvas:
        export_canvas_json(quiz, args.export_canvas)
        return 0
    
    # Interactive quiz
    result = run_interactive_quiz(quiz, randomise=args.random, limit=args.limit, bloom_filter=args.bloom)
    
    if args.export:
        export_results(result, args.export)
    
    return 0 if result.passed else 1


if __name__ == "__main__":
    sys.exit(main())
