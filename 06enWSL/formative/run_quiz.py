#!/usr/bin/env python3
"""
Formative Quiz Runner — Week 6: NAT/PAT & SDN
=============================================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

Interactive CLI quiz for self-assessment with LMS export capabilities.

Usage:
    python formative/run_quiz.py                    # Run full quiz
    python formative/run_quiz.py --random           # Randomise question order
    python formative/run_quiz.py --limit 5          # Limit to 5 questions
    python formative/run_quiz.py --lo LO1 LO2       # Filter by Learning Objectives
    python formative/run_quiz.py --difficulty basic # Filter by difficulty
    python formative/run_quiz.py --review           # Review mode (show answers)
    python formative/run_quiz.py --export json      # Export to LMS-compatible JSON
    python formative/run_quiz.py --export moodle    # Export to Moodle GIFT format
    python formative/run_quiz.py --export canvas    # Export to Canvas QTI format

Requirements:
    pip install pyyaml --break-system-packages

Contact:
    Issues: Open an issue in GitHub
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union
from xml.dom import minidom


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

DEFAULT_QUIZ_PATH = Path(__file__).parent / "quiz.yaml"
PASSING_SCORE = 70  # percent
VERSION = "1.2.0"


# ═══════════════════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Question:
    """Represents a single quiz question."""
    id: str
    type: str
    lo_ref: str
    bloom_level: str
    difficulty: str
    stem: str
    correct: Any
    explanation: str
    points: int = 1
    options: Optional[Dict[str, str]] = None
    hint: Optional[str] = None
    misconception_ref: Optional[str] = None
    feedback: Optional[Dict[str, str]] = None
    anti_ai_note: Optional[str] = None


@dataclass
class QuizResult:
    """Stores quiz attempt results."""
    timestamp: str
    total_questions: int
    correct_answers: int
    score_percent: float
    points_earned: int
    total_points: int
    passed: bool
    time_taken_seconds: float
    questions_answered: List[Dict[str, Any]] = field(default_factory=list)
    lo_performance: Dict[str, Dict[str, int]] = field(default_factory=dict)


# ═══════════════════════════════════════════════════════════════════════════════
# YAML LOADING
# ═══════════════════════════════════════════════════════════════════════════════

def load_quiz(path: Path) -> Dict[str, Any]:
    """
    Load quiz from YAML file.
    
    Args:
        path: Path to quiz YAML file
        
    Returns:
        Parsed quiz dictionary
        
    Raises:
        FileNotFoundError: If quiz file does not exist
        yaml.YAMLError: If YAML parsing fails
    """
    try:
        import yaml
    except ImportError:
        print("Error: PyYAML not installed.")
        print("Install with: pip install pyyaml --break-system-packages")
        sys.exit(1)
    
    if not path.exists():
        raise FileNotFoundError(f"Quiz file not found: {path}")
    
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def parse_questions(quiz_data: Dict[str, Any]) -> List[Question]:
    """Parse questions from quiz data into Question objects."""
    questions = []
    for q in quiz_data.get("questions", []):
        questions.append(Question(
            id=q.get("id", "unknown"),
            type=q.get("type", "multiple_choice"),
            lo_ref=q.get("lo_ref", ""),
            bloom_level=q.get("bloom_level", ""),
            difficulty=q.get("difficulty", "intermediate"),
            stem=q.get("stem", ""),
            correct=q.get("correct"),
            explanation=q.get("explanation", ""),
            points=q.get("points", 1),
            options=q.get("options"),
            hint=q.get("hint"),
            misconception_ref=q.get("misconception_ref"),
            feedback=q.get("feedback"),
            anti_ai_note=q.get("anti_ai_note"),
        ))
    return questions


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

def run_interactive_quiz(
    questions: List[Question],
    metadata: Dict[str, Any],
    randomise: bool = False,
    limit: Optional[int] = None,
    review_mode: bool = False,
) -> QuizResult:
    """
    Run interactive quiz session.
    
    Args:
        questions: List of Question objects
        metadata: Quiz metadata
        randomise: Whether to shuffle question order
        limit: Maximum number of questions to ask
        review_mode: If True, show correct answers immediately
        
    Returns:
        QuizResult with session statistics
    """
    if randomise:
        questions = questions.copy()
        random.shuffle(questions)
    
    if limit:
        questions = questions[:limit]
    
    correct = 0
    points_earned = 0
    total_points = sum(q.points for q in questions)
    answered = []
    lo_perf: Dict[str, Dict[str, int]] = {}
    
    start_time = time.time()
    
    print()
    print("═" * 64)
    print(f"  {metadata.get('topic', 'Quiz')}")
    print("═" * 64)
    print(f"  Questions: {len(questions)} | Passing: {metadata.get('passing_score', 70)}%")
    print(f"  Total Points: {total_points}")
    if review_mode:
        print("  Mode: REVIEW (answers shown after each question)")
    print("═" * 64)
    print()
    
    for i, q in enumerate(questions, 1):
        # Track LO performance
        if q.lo_ref not in lo_perf:
            lo_perf[q.lo_ref] = {"correct": 0, "total": 0, "points": 0}
        lo_perf[q.lo_ref]["total"] += 1
        
        # Display question
        print(f"\n{'─' * 64}")
        print(f"Q{i}. [{q.difficulty.upper()}] [{q.lo_ref}] [{q.bloom_level}] ({q.points} pt)")
        print(f"{'─' * 64}")
        print(f"\n{q.stem.strip()}\n")
        
        is_correct = False
        user_answer = ""
        
        if q.type == "multiple_choice" and q.options:
            # Display options
            for key, val in q.options.items():
                print(f"   {key}) {val}")
            print()
            
            # Get answer
            user_answer = input("Your answer (a/b/c/d): ").strip().lower()
            is_correct = user_answer == q.correct
            
            if is_correct:
                print("\n✅ Correct!")
                correct += 1
                points_earned += q.points
                lo_perf[q.lo_ref]["correct"] += 1
                lo_perf[q.lo_ref]["points"] += q.points
            else:
                print(f"\n❌ Incorrect. Correct answer: {q.correct}")
                if q.feedback and user_answer in q.feedback:
                    print(f"   💡 {q.feedback[user_answer]}")
            
            if review_mode or not is_correct:
                print(f"\n📖 Explanation: {q.explanation}")
                if q.misconception_ref:
                    print(f"   📚 See: {q.misconception_ref}")
        
        elif q.type == "fill_blank":
            if q.hint:
                print(f"   💡 Hint: {q.hint}")
            print()
            
            user_answer = input("Your answer: ").strip().lower()
            acceptable = [a.lower() for a in q.correct] if isinstance(q.correct, list) else [q.correct.lower()]
            is_correct = user_answer in acceptable
            
            if is_correct:
                print("\n✅ Correct!")
                correct += 1
                points_earned += q.points
                lo_perf[q.lo_ref]["correct"] += 1
                lo_perf[q.lo_ref]["points"] += q.points
            else:
                print(f"\n❌ Incorrect. Accepted answers: {', '.join(q.correct) if isinstance(q.correct, list) else q.correct}")
            
            if review_mode or not is_correct:
                print(f"\n📖 Explanation: {q.explanation}")
        
        elif q.type == "open_response":
            if q.anti_ai_note:
                print(f"   ⚠️  {q.anti_ai_note}")
            if q.hint:
                print(f"   💡 Hint: {q.hint}")
            print()
            
            user_answer = input("Your answer: ").strip()
            print("\n📝 Response recorded (requires manual verification)")
            print(f"📖 {q.explanation}")
            # Give partial credit for attempting live questions
            points_earned += q.points // 2
            lo_perf[q.lo_ref]["points"] += q.points // 2
        
        answered.append({
            "question_id": q.id,
            "user_answer": user_answer,
            "correct_answer": q.correct,
            "is_correct": is_correct,
            "points": q.points if is_correct else 0,
            "lo_ref": q.lo_ref,
        })
    
    elapsed = time.time() - start_time
    score_pct = (points_earned / total_points * 100) if total_points > 0 else 0
    passed = score_pct >= metadata.get("passing_score", 70)
    
    # Results summary
    print()
    print("═" * 64)
    print("  RESULTS")
    print("═" * 64)
    print(f"  Score: {points_earned}/{total_points} points ({score_pct:.1f}%)")
    print(f"  Questions: {correct}/{len(questions)} correct")
    print(f"  Time: {elapsed:.0f} seconds")
    print(f"  Status: {'✅ PASSED' if passed else '❌ NEEDS REVIEW'}")
    print()
    
    # LO breakdown
    print("  Performance by Learning Objective:")
    for lo, stats in sorted(lo_perf.items()):
        lo_pct = (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
        status = "✅" if lo_pct >= 70 else "⚠️" if lo_pct >= 50 else "❌"
        print(f"    {lo}: {stats['correct']}/{stats['total']} ({lo_pct:.0f}%) {status}")
    
    print("═" * 64)
    print()
    
    # Post-quiz guidance
    post_quiz = metadata.get("post_quiz", {})
    if passed and "if_above_passing" in post_quiz:
        print("💡 " + post_quiz["if_above_passing"].strip())
    elif not passed and "if_below_passing" in post_quiz:
        print("📚 " + post_quiz["if_below_passing"].strip())
    
    return QuizResult(
        timestamp=datetime.now().isoformat(),
        total_questions=len(questions),
        correct_answers=correct,
        score_percent=score_pct,
        points_earned=points_earned,
        total_points=total_points,
        passed=passed,
        time_taken_seconds=elapsed,
        questions_answered=answered,
        lo_performance=lo_perf,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# LMS EXPORT FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def export_to_json(quiz_data: Dict[str, Any], output_path: Path) -> None:
    """Export quiz to LMS-compatible JSON format."""
    # Load and transform to standard LMS JSON
    json_path = Path(__file__).parent / "quiz_lms.json"
    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as f:
            lms_data = json.load(f)
    else:
        # Generate from YAML data
        lms_data = {
            "metadata": quiz_data.get("metadata", {}),
            "questions": [],
        }
        for q in quiz_data.get("questions", []):
            lms_q = {
                "id": q.get("id"),
                "type": q.get("type"),
                "learning_objective": q.get("lo_ref"),
                "difficulty": q.get("difficulty"),
                "points": q.get("points", 1),
                "question_text": q.get("stem", "").strip(),
            }
            if q.get("options"):
                lms_q["answers"] = [
                    {"id": k, "text": v, "correct": k == q.get("correct")}
                    for k, v in q.get("options", {}).items()
                ]
            lms_data["questions"].append(lms_q)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(lms_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Exported to JSON: {output_path}")


def export_to_moodle_gift(quiz_data: Dict[str, Any], output_path: Path) -> None:
    """Export quiz to Moodle GIFT format."""
    lines = []
    lines.append("// Week 6: NAT/PAT & SDN - Moodle GIFT Format")
    lines.append("// Generated by run_quiz.py")
    lines.append(f"// {datetime.now().isoformat()}")
    lines.append("")
    lines.append("$CATEGORY: Week 6 - NAT/PAT & SDN")
    lines.append("")
    
    for q in quiz_data.get("questions", []):
        q_id = q.get("id", "q")
        stem = q.get("stem", "").strip().replace("\n", " ").replace("{", "\\{").replace("}", "\\}")
        
        if q.get("type") == "multiple_choice" and q.get("options"):
            lines.append(f"// {q_id} - {q.get('lo_ref', '')} - {q.get('difficulty', '')}")
            lines.append(f"::{q_id}::{stem} {{")
            for key, val in q.get("options", {}).items():
                val_escaped = val.replace("{", "\\{").replace("}", "\\}")
                if key == q.get("correct"):
                    lines.append(f"  ={val_escaped}")
                else:
                    feedback = q.get("feedback", {}).get(key, "")
                    if feedback:
                        lines.append(f"  ~{val_escaped}#{feedback}")
                    else:
                        lines.append(f"  ~{val_escaped}")
            lines.append("}")
            lines.append("")
        
        elif q.get("type") == "fill_blank":
            lines.append(f"// {q_id} - {q.get('lo_ref', '')} - {q.get('difficulty', '')}")
            correct = q.get("correct", [])
            if isinstance(correct, list):
                answers = " ".join(f"={a}" for a in correct)
            else:
                answers = f"={correct}"
            lines.append(f"::{q_id}::{stem} {{{answers}}}")
            lines.append("")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    
    print(f"✅ Exported to Moodle GIFT: {output_path}")


def export_to_moodle_xml(quiz_data: Dict[str, Any], output_path: Path) -> None:
    """Export quiz to Moodle XML format."""
    root = ET.Element("quiz")
    
    # Category
    cat = ET.SubElement(root, "question", type="category")
    cat_text = ET.SubElement(cat, "category")
    ET.SubElement(cat_text, "text").text = "$course$/Week 6 - NAT/PAT & SDN"
    
    for q in quiz_data.get("questions", []):
        q_type = q.get("type", "multiple_choice")
        
        if q_type == "multiple_choice":
            question = ET.SubElement(root, "question", type="multichoice")
        elif q_type == "fill_blank":
            question = ET.SubElement(root, "question", type="shortanswer")
        else:
            question = ET.SubElement(root, "question", type="essay")
        
        # Name
        name = ET.SubElement(question, "name")
        ET.SubElement(name, "text").text = q.get("id", "Question")
        
        # Question text
        qtext = ET.SubElement(question, "questiontext", format="html")
        ET.SubElement(qtext, "text").text = f"<![CDATA[<p>{q.get('stem', '').strip()}</p>]]>"
        
        # General feedback
        gfb = ET.SubElement(question, "generalfeedback", format="html")
        ET.SubElement(gfb, "text").text = f"<![CDATA[<p>{q.get('explanation', '')}</p>]]>"
        
        # Default grade
        ET.SubElement(question, "defaultgrade").text = str(q.get("points", 1))
        
        # Answers
        if q_type == "multiple_choice" and q.get("options"):
            ET.SubElement(question, "single").text = "true"
            ET.SubElement(question, "shuffleanswers").text = "true"
            
            for key, val in q.get("options", {}).items():
                fraction = "100" if key == q.get("correct") else "0"
                answer = ET.SubElement(question, "answer", fraction=fraction, format="html")
                ET.SubElement(answer, "text").text = f"<![CDATA[<p>{val}</p>]]>"
                fb = q.get("feedback", {}).get(key, "")
                afb = ET.SubElement(answer, "feedback", format="html")
                ET.SubElement(afb, "text").text = f"<![CDATA[<p>{fb}</p>]]>" if fb else ""
        
        elif q_type == "fill_blank":
            ET.SubElement(question, "usecase").text = "0"
            correct = q.get("correct", [])
            if not isinstance(correct, list):
                correct = [correct]
            for ans in correct:
                answer = ET.SubElement(question, "answer", fraction="100", format="plain_text")
                ET.SubElement(answer, "text").text = ans
    
    # Pretty print
    xml_str = ET.tostring(root, encoding="unicode")
    dom = minidom.parseString(xml_str)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(dom.toprettyxml(indent="  "))
    
    print(f"✅ Exported to Moodle XML: {output_path}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Week 6 Formative Quiz Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run_quiz.py                     # Full quiz
    python run_quiz.py --random --limit 5  # 5 random questions
    python run_quiz.py --lo LO1 LO2        # Only LO1 and LO2
    python run_quiz.py --export json       # Export to JSON
    python run_quiz.py --export moodle     # Export to Moodle GIFT
    python run_quiz.py --export moodle-xml # Export to Moodle XML

Contact: Issues: Open an issue in GitHub
        """
    )
    parser.add_argument(
        "--quiz", "-q",
        type=Path,
        default=DEFAULT_QUIZ_PATH,
        help="Path to quiz YAML file"
    )
    parser.add_argument(
        "--random", "-r",
        action="store_true",
        help="Randomise question order"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        help="Limit number of questions"
    )
    parser.add_argument(
        "--lo",
        nargs="+",
        help="Filter by Learning Objectives (e.g., --lo LO1 LO2)"
    )
    parser.add_argument(
        "--difficulty", "-d",
        choices=["basic", "intermediate", "advanced"],
        help="Filter by difficulty"
    )
    parser.add_argument(
        "--review",
        action="store_true",
        help="Review mode: show answers after each question"
    )
    parser.add_argument(
        "--export", "-e",
        choices=["json", "moodle", "moodle-xml", "gift"],
        help="Export quiz to LMS format"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output file for export (default: auto-generated)"
    )
    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"Quiz Runner v{VERSION}"
    )
    
    args = parser.parse_args()
    
    try:
        quiz_data = load_quiz(args.quiz)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Error loading quiz: {e}")
        return 1
    
    # Handle exports
    if args.export:
        base_name = args.quiz.stem
        
        if args.export == "json":
            output = args.output or Path(f"{base_name}_export.json")
            export_to_json(quiz_data, output)
        elif args.export in ("moodle", "gift"):
            output = args.output or Path(f"{base_name}_moodle.gift")
            export_to_moodle_gift(quiz_data, output)
        elif args.export == "moodle-xml":
            output = args.output or Path(f"{base_name}_moodle.xml")
            export_to_moodle_xml(quiz_data, output)
        
        return 0
    
    # Parse questions
    questions = parse_questions(quiz_data)
    
    # Apply filters
    if args.lo:
        lo_set = set(args.lo)
        questions = [q for q in questions if q.lo_ref in lo_set]
    
    if args.difficulty:
        questions = [q for q in questions if q.difficulty == args.difficulty]
    
    if not questions:
        print("No questions match the specified filters.")
        return 1
    
    # Run quiz
    result = run_interactive_quiz(
        questions=questions,
        metadata=quiz_data.get("metadata", {}),
        randomise=args.random,
        limit=args.limit,
        review_mode=args.review,
    )
    
    return 0 if result.passed else 1


if __name__ == "__main__":
    sys.exit(main())
