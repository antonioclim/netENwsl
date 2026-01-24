#!/usr/bin/env python3
"""
Week 10 Formative Assessment Quiz Runner
========================================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

Interactive quiz runner for self-assessment with LMS export capabilities.

Usage:
    python formative/run_quiz.py                    # Run all questions
    python formative/run_quiz.py --random           # Shuffle questions
    python formative/run_quiz.py --limit 5          # First 5 questions
    python formative/run_quiz.py --lo LO1           # Filter by Learning Objective
    python formative/run_quiz.py --difficulty basic # Filter by difficulty
    python formative/run_quiz.py --review           # Review mode (show answers)
    python formative/run_quiz.py --live-only        # Only live verification questions
    python formative/run_quiz.py --export-moodle    # Export to Moodle XML
    python formative/run_quiz.py --export-canvas    # Export to Canvas QTI
    python formative/run_quiz.py --export-json      # Export to JSON (generic LMS)

Prerequisites:
    pip install pyyaml
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import json
import random
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from xml.dom import minidom

try:
    import yaml
except ImportError:
    print("[ERROR] PyYAML is required: pip install pyyaml")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
SCRIPT_DIR = Path(__file__).parent
DEFAULT_QUIZ = SCRIPT_DIR / "quiz.yaml"
PROGRESS_FILE = Path.home() / ".week10_quiz_progress.json"

# ANSI colour codes for terminal output
COLOURS = {
    "green": "\033[92m",
    "red": "\033[91m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "cyan": "\033[96m",
    "bold": "\033[1m",
    "reset": "\033[0m",
}


# ═══════════════════════════════════════════════════════════════════════════════
# PROGRESS_TRACKER
# ═══════════════════════════════════════════════════════════════════════════════
class ProgressTracker:
    """Tracks quiz attempts and progress over time."""
    
    def __init__(self) -> None:
        self.data = self._load()
    
    def _load(self) -> Dict[str, Any]:
        """Load progress from file."""
        if PROGRESS_FILE.exists():
            try:
                with open(PROGRESS_FILE, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        return {
            'first_attempt': datetime.now().isoformat(),
            'attempts': [],
            'best_score': 0,
            'total_attempts': 0,
            'lo_scores': {}
        }
    
    def _save(self) -> None:
        """Save progress to file."""
        try:
            with open(PROGRESS_FILE, 'w') as f:
                json.dump(self.data, f, indent=2)
        except IOError:
            pass  # Silently fail if cannot save
    
    def record_attempt(self, score: float, total: int, lo_scores: Dict[str, float]) -> None:
        """Record a quiz attempt."""
        self.data['attempts'].append({
            'timestamp': datetime.now().isoformat(),
            'score': score,
            'total': total,
            'percentage': (score / total * 100) if total > 0 else 0
        })
        
        self.data['total_attempts'] += 1
        
        percentage = (score / total * 100) if total > 0 else 0
        if percentage > self.data['best_score']:
            self.data['best_score'] = percentage
        
        # Update LO scores
        for lo, lo_score in lo_scores.items():
            if lo not in self.data['lo_scores']:
                self.data['lo_scores'][lo] = []
            self.data['lo_scores'][lo].append(lo_score)
        
        self._save()
    
    def get_summary(self) -> str:
        """Get a summary of progress."""
        if self.data['total_attempts'] == 0:
            return "No quiz attempts yet."
        
        recent = self.data['attempts'][-5:]
        recent_scores = [a['percentage'] for a in recent]
        avg_recent = sum(recent_scores) / len(recent_scores)
        
        return f"""
╔══════════════════════════════════════════════════════════════════╗
║  QUIZ PROGRESS SUMMARY                                           ║
╠══════════════════════════════════════════════════════════════════╣
║  Total Attempts:    {self.data['total_attempts']:<44} ║
║  Best Score:        {self.data['best_score']:.1f}%                                          ║
║  Recent Average:    {avg_recent:.1f}% (last {len(recent)} attempts)                        ║
╚══════════════════════════════════════════════════════════════════╝
"""


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ_LOADER
# ═══════════════════════════════════════════════════════════════════════════════
def load_quiz(path: Path) -> Dict[str, Any]:
    """Load quiz from YAML file."""
    if not path.exists():
        raise FileNotFoundError(f"Quiz file not found: {path}")
    
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def filter_questions(
    questions: List[Dict[str, Any]],
    lo_filter: Optional[str] = None,
    difficulty_filter: Optional[str] = None,
    live_only: bool = False,
    standard_only: bool = False,
) -> List[Dict[str, Any]]:
    """Filter questions by various criteria."""
    filtered = questions
    
    if lo_filter:
        filtered = [q for q in filtered if q.get("lo_ref") == lo_filter.upper()]
    
    if difficulty_filter:
        filtered = [q for q in filtered if q.get("difficulty") == difficulty_filter.lower()]
    
    if live_only:
        filtered = [q for q in filtered if q.get("type") == "live_verification"]
    
    if standard_only:
        filtered = [q for q in filtered if q.get("type") != "live_verification"]
    
    return filtered


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ_DISPLAY
# ═══════════════════════════════════════════════════════════════════════════════
def colour(text: str, colour_name: str) -> str:
    """Apply ANSI colour to text."""
    return f"{COLOURS.get(colour_name, '')}{text}{COLOURS['reset']}"


def display_question(q: Dict[str, Any], index: int, total: int) -> None:
    """Display a single question."""
    print(f"\n{'─' * 70}")
    print(colour(f"Question {index}/{total}", "bold"), end="")
    print(f"  [{q.get('lo_ref', '?')}] [{q.get('difficulty', '?')}] [{q.get('bloom_level', '?')}]")
    
    if q.get('type') == 'live_verification':
        print(colour("  🔬 LIVE VERIFICATION — Requires lab environment", "cyan"))
    
    print(f"{'─' * 70}")
    
    # Display stem (may be multiline)
    stem = q.get("stem", "").strip()
    print(f"\n{stem}\n")
    
    # Display options for multiple choice
    if q.get("type") in ["multiple_choice", None]:
        options = q.get("options", {})
        for key in sorted(options.keys()):
            print(f"  {key}) {options[key]}")


def get_answer(q: Dict[str, Any]) -> str:
    """Get user's answer for a question."""
    q_type = q.get("type", "multiple_choice")
    
    if q_type == "multiple_choice":
        while True:
            answer = input("\nYour answer (a/b/c/d): ").strip().lower()
            if answer in ['a', 'b', 'c', 'd']:
                return answer
            print(colour("Please enter a, b, c or d", "yellow"))
    
    elif q_type == "live_verification":
        print(colour("\n[Run the command shown above and enter the result]", "cyan"))
        return input("Your answer: ").strip()
    
    else:
        return input("\nYour answer: ").strip()


def check_answer(q: Dict[str, Any], answer: str) -> bool:
    """Check if the answer is correct."""
    q_type = q.get("type", "multiple_choice")
    correct = q.get("correct", "")
    
    if q_type == "multiple_choice":
        return answer.lower() == str(correct).lower()
    
    elif q_type == "live_verification":
        # For live questions, check against pattern or exact match
        import re
        pattern = q.get("expected_pattern", "")
        
        if pattern:
            return bool(re.match(pattern, answer))
        
        # Dynamic answers are always "correct" if non-empty
        if correct in ["dynamic", "dynamically_generated", "varies"]:
            return bool(answer.strip())
        
        return answer.strip() == str(correct).strip()
    
    return answer.lower() == str(correct).lower()


def display_feedback(q: Dict[str, Any], correct: bool, user_answer: str) -> None:
    """Display feedback after answering."""
    if correct:
        print(colour("\n✅ Correct!", "green"))
    else:
        print(colour("\n❌ Incorrect", "red"))
        
        if q.get("type") != "live_verification":
            print(f"   Correct answer: {q.get('correct', '?')}")
    
    # Show explanation
    explanation = q.get("explanation", "").strip()
    if explanation:
        print(colour("\n📖 Explanation:", "blue"))
        for line in explanation.split('\n'):
            print(f"   {line.strip()}")
    
    # Show misconception reference
    if "misconception_ref" in q:
        print(colour(f"\n📚 See also: {q['misconception_ref']}", "yellow"))


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ_RUNNER
# ═══════════════════════════════════════════════════════════════════════════════
def run_quiz(
    quiz: Dict[str, Any],
    questions: List[Dict[str, Any]],
    review_mode: bool = False,
    track_progress: bool = True
) -> float:
    """Run the interactive quiz."""
    metadata = quiz.get("metadata", {})
    
    print(f"\n{'═' * 70}")
    print(colour(f"  {metadata.get('topic', 'Quiz')}", "bold"))
    print(f"  Week {metadata.get('week', '?')} — {len(questions)} questions")
    print(f"  Passing score: {metadata.get('passing_score', 70)}%")
    print(f"{'═' * 70}")
    
    if review_mode:
        print(colour("\n  📖 REVIEW MODE — Answers will be shown immediately", "yellow"))
    
    correct_count = 0
    total_points = 0
    earned_points = 0
    lo_correct: Dict[str, int] = {}
    lo_total: Dict[str, int] = {}
    
    for i, q in enumerate(questions, 1):
        display_question(q, i, len(questions))
        
        lo = q.get("lo_ref", "Unknown")
        points = q.get("points", 1)
        total_points += points
        
        if lo not in lo_total:
            lo_total[lo] = 0
            lo_correct[lo] = 0
        lo_total[lo] += points
        
        if review_mode:
            # Show answer immediately in review mode
            correct_answer = q.get("correct", "?")
            print(colour(f"\n📝 Answer: {correct_answer}", "green"))
            
            explanation = q.get("explanation", "").strip()
            if explanation:
                print(colour("\n📖 Explanation:", "blue"))
                for line in explanation.split('\n'):
                    print(f"   {line.strip()}")
            
            input("\nPress Enter to continue...")
        else:
            # Interactive mode
            answer = get_answer(q)
            is_correct = check_answer(q, answer)
            
            if is_correct:
                correct_count += 1
                earned_points += points
                lo_correct[lo] = lo_correct.get(lo, 0) + points
            
            display_feedback(q, is_correct, answer)
            
            if i < len(questions):
                input("\nPress Enter for next question...")
    
    # Calculate final score
    score_percent = (earned_points / total_points * 100) if total_points > 0 else 0
    passing = metadata.get("passing_score", 70)
    passed = score_percent >= passing
    
    # Display results
    print(f"\n{'═' * 70}")
    print(colour("  RESULTS", "bold"))
    print(f"{'═' * 70}")
    
    if not review_mode:
        status_colour = "green" if passed else "red"
        status_text = "PASSED ✅" if passed else "NEEDS REVIEW ❌"
        
        print(f"\n  Score: {earned_points}/{total_points} points ({score_percent:.1f}%)")
        print(f"  Status: {colour(status_text, status_colour)}")
        
        print("\n  Performance by Learning Objective:")
        for lo in sorted(lo_total.keys()):
            lo_pct = (lo_correct.get(lo, 0) / lo_total[lo] * 100) if lo_total[lo] > 0 else 0
            bar = "█" * int(lo_pct / 10) + "░" * (10 - int(lo_pct / 10))
            lo_colour = "green" if lo_pct >= 70 else "yellow" if lo_pct >= 50 else "red"
            print(f"    {lo}: {colour(bar, lo_colour)} {lo_pct:.0f}%")
        
        # Track progress
        if track_progress:
            tracker = ProgressTracker()
            lo_scores = {lo: (lo_correct.get(lo, 0) / lo_total[lo] * 100) 
                        for lo in lo_total if lo_total[lo] > 0}
            tracker.record_attempt(earned_points, total_points, lo_scores)
    
    print(f"\n{'═' * 70}\n")
    
    return score_percent


# ═══════════════════════════════════════════════════════════════════════════════
# LMS_EXPORT
# ═══════════════════════════════════════════════════════════════════════════════
def export_moodle_xml(quiz: Dict[str, Any], output_path: Path) -> None:
    """Export quiz to Moodle XML format."""
    questions = quiz.get("questions", [])
    metadata = quiz.get("metadata", {})
    
    # Create root element
    root = ET.Element("quiz")
    
    # Add category question
    category = ET.SubElement(root, "question")
    category.set("type", "category")
    cat_elem = ET.SubElement(category, "category")
    cat_text = ET.SubElement(cat_elem, "text")
    cat_text.text = f"$course$/Week {metadata.get('week', '10')}/Formative Assessment"
    
    # Add each question
    for q in questions:
        if q.get("type") == "live_verification":
            continue  # Skip live questions for LMS
        
        question = ET.SubElement(root, "question")
        question.set("type", "multichoice")
        
        # Name
        name = ET.SubElement(question, "name")
        name_text = ET.SubElement(name, "text")
        name_text.text = f"{q.get('id', 'q')} - {q.get('lo_ref', 'LO')}"
        
        # Question text
        qtext = ET.SubElement(question, "questiontext")
        qtext.set("format", "html")
        qtext_text = ET.SubElement(qtext, "text")
        qtext_text.text = f"<![CDATA[<p>{q.get('stem', '').strip()}</p>]]>"
        
        # General feedback
        feedback = ET.SubElement(question, "generalfeedback")
        feedback.set("format", "html")
        fb_text = ET.SubElement(feedback, "text")
        fb_text.text = f"<![CDATA[<p>{q.get('explanation', '').strip()}</p>]]>"
        
        # Default grade
        grade = ET.SubElement(question, "defaultgrade")
        grade.text = str(q.get("points", 1))
        
        # Shuffle answers
        shuffle = ET.SubElement(question, "shuffleanswers")
        shuffle.text = "1"
        
        # Single answer
        single = ET.SubElement(question, "single")
        single.text = "true"
        
        # Add answers
        correct = q.get("correct", "")
        for key, value in q.get("options", {}).items():
            answer = ET.SubElement(question, "answer")
            answer.set("fraction", "100" if key == correct else "0")
            answer.set("format", "html")
            
            ans_text = ET.SubElement(answer, "text")
            ans_text.text = f"<![CDATA[<p>{value}</p>]]>"
    
    # Pretty print
    xml_str = ET.tostring(root, encoding="unicode")
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent="  ")
    
    # Remove extra blank lines
    lines = [line for line in pretty_xml.split('\n') if line.strip()]
    pretty_xml = '\n'.join(lines)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(pretty_xml)
    
    print(f"[OK] Exported {len(questions)} questions to Moodle XML: {output_path}")


def export_canvas_qti(quiz: Dict[str, Any], output_path: Path) -> None:
    """Export quiz to Canvas QTI format."""
    questions = quiz.get("questions", [])
    metadata = quiz.get("metadata", {})
    
    # Create QTI structure
    root = ET.Element("questestinterop")
    root.set("xmlns", "http://www.imsglobal.org/xsd/ims_qtiasiv1p2")
    
    assessment = ET.SubElement(root, "assessment")
    assessment.set("ident", f"week{metadata.get('week', '10')}_formative")
    assessment.set("title", f"Week {metadata.get('week', '10')} Formative Assessment")
    
    section = ET.SubElement(assessment, "section")
    section.set("ident", "root_section")
    
    for q in questions:
        if q.get("type") == "live_verification":
            continue
        
        item = ET.SubElement(section, "item")
        item.set("ident", q.get("id", "q"))
        item.set("title", f"{q.get('lo_ref', 'LO')} - {q.get('bloom_level', 'apply')}")
        
        # Add item metadata and content (simplified)
        presentation = ET.SubElement(item, "presentation")
        material = ET.SubElement(presentation, "material")
        mattext = ET.SubElement(material, "mattext")
        mattext.set("texttype", "text/html")
        mattext.text = q.get("stem", "")
    
    xml_str = ET.tostring(root, encoding="unicode")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(xml_str)
    
    print(f"[OK] Exported to Canvas QTI: {output_path}")


def export_json(quiz: Dict[str, Any], output_path: Path) -> None:
    """Export quiz to generic JSON format for LMS import."""
    questions = quiz.get("questions", [])
    metadata = quiz.get("metadata", {})
    
    export_data = {
        "metadata": {
            "title": f"Week {metadata.get('week', '10')} Formative Assessment",
            "topic": metadata.get("topic", ""),
            "passing_score": metadata.get("passing_score", 70),
            "total_questions": len([q for q in questions if q.get("type") != "live_verification"]),
            "exported_at": datetime.now().isoformat(),
            "format_version": "1.0"
        },
        "questions": []
    }
    
    for q in questions:
        if q.get("type") == "live_verification":
            continue
        
        q_export = {
            "id": q.get("id"),
            "type": "multiple_choice",
            "learning_objective": q.get("lo_ref"),
            "bloom_level": q.get("bloom_level"),
            "difficulty": q.get("difficulty"),
            "points": q.get("points", 1),
            "stem": q.get("stem", "").strip(),
            "options": q.get("options", {}),
            "correct_answer": q.get("correct"),
            "explanation": q.get("explanation", "").strip()
        }
        
        export_data["questions"].append(q_export)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    print(f"[OK] Exported {len(export_data['questions'])} questions to JSON: {output_path}")


# ═══════════════════════════════════════════════════════════════════════════════
# COMMAND_LINE_INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Week 10 Formative Assessment Quiz Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python formative/run_quiz.py                    # Run full quiz
    python formative/run_quiz.py --random --limit 5 # Random 5 questions
    python formative/run_quiz.py --lo LO1           # Only LO1 questions
    python formative/run_quiz.py --live-only        # Only live verification
    python formative/run_quiz.py --export-moodle    # Export for Moodle
    python formative/run_quiz.py --progress         # Show progress summary
"""
    )
    
    # Quiz options
    parser.add_argument("--quiz", "-q", type=Path, default=DEFAULT_QUIZ,
                       help="Path to quiz YAML file")
    parser.add_argument("--random", "-r", action="store_true",
                       help="Shuffle questions")
    parser.add_argument("--limit", "-l", type=int, default=None,
                       help="Limit number of questions")
    parser.add_argument("--lo", type=str, default=None,
                       help="Filter by Learning Objective (e.g. LO1)")
    parser.add_argument("--difficulty", "-d", type=str, default=None,
                       choices=["basic", "intermediate", "advanced", "procedural"],
                       help="Filter by difficulty")
    parser.add_argument("--review", action="store_true",
                       help="Review mode (show answers immediately)")
    
    # Question type filters
    parser.add_argument("--live-only", action="store_true",
                       help="Only live verification questions")
    parser.add_argument("--standard-only", action="store_true",
                       help="Only standard questions (exclude live)")
    
    # Export options
    parser.add_argument("--export-moodle", type=Path, default=None,
                       metavar="FILE", help="Export to Moodle XML format")
    parser.add_argument("--export-canvas", type=Path, default=None,
                       metavar="FILE", help="Export to Canvas QTI format")
    parser.add_argument("--export-json", type=Path, default=None,
                       metavar="FILE", help="Export to generic JSON format")
    
    # Progress tracking
    parser.add_argument("--progress", action="store_true",
                       help="Show progress summary and exit")
    parser.add_argument("--no-track", action="store_true",
                       help="Do not track this attempt")
    
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point."""
    args = parse_args(argv)
    
    # Show progress summary
    if args.progress:
        tracker = ProgressTracker()
        print(tracker.get_summary())
        return 0
    
    try:
        quiz = load_quiz(args.quiz)
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        return 1
    
    # Handle exports
    if args.export_moodle:
        export_moodle_xml(quiz, args.export_moodle)
        return 0
    
    if args.export_canvas:
        export_canvas_qti(quiz, args.export_canvas)
        return 0
    
    if args.export_json:
        export_json(quiz, args.export_json)
        return 0
    
    # Filter questions
    questions = quiz.get("questions", [])
    questions = filter_questions(
        questions,
        lo_filter=args.lo,
        difficulty_filter=args.difficulty,
        live_only=args.live_only,
        standard_only=args.standard_only
    )
    
    if not questions:
        print("[WARNING] No questions match the specified filters")
        return 1
    
    # Shuffle if requested
    if args.random:
        random.shuffle(questions)
    
    # Limit if requested
    if args.limit:
        questions = questions[:args.limit]
    
    # Run quiz
    score = run_quiz(
        quiz,
        questions,
        review_mode=args.review,
        track_progress=not args.no_track
    )
    
    # Return 0 if passed, 1 if failed
    passing = quiz.get("metadata", {}).get("passing_score", 70)
    return 0 if score >= passing else 1


if __name__ == "__main__":
    sys.exit(main())
