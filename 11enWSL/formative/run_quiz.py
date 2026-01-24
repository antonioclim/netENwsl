#!/usr/bin/env python3
"""
run_quiz.py — Formative Assessment Quiz Runner for Week 11
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Usage:
    python formative/run_quiz.py                  # Run all questions
    python formative/run_quiz.py --level basic    # Run basic questions only
    python formative/run_quiz.py --random         # Randomise question order
    python formative/run_quiz.py --export-json    # Export to LMS format
    python formative/run_quiz.py --review         # Review all answers
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml
except ImportError:
    print("Error: pyyaml not installed. Run: pip install pyyaml")
    sys.exit(1)

QUIZ_YAML_PATH = Path(__file__).parent / "quiz.yaml"
QUIZ_JSON_PATH = Path(__file__).parent / "quiz.json"
DIFFICULTY_LEVELS = ["basic", "intermediate", "advanced"]

COLOURS = {
    "green": "\033[92m", "red": "\033[91m", "yellow": "\033[93m",
    "blue": "\033[94m", "bold": "\033[1m", "reset": "\033[0m",
}


def load_quiz(path: Path = QUIZ_YAML_PATH) -> Dict[str, Any]:
    """Load quiz from YAML or JSON file."""
    if not path.exists():
        raise FileNotFoundError(f"Quiz file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        if path.suffix in [".yaml", ".yml"]:
            return yaml.safe_load(f)
        return json.load(f)


def filter_questions(questions: List[Dict], level: Optional[str] = None,
                     topic: Optional[str] = None) -> List[Dict]:
    """Filter questions by difficulty level and/or topic."""
    filtered = questions
    if level and level != "all":
        filtered = [q for q in filtered if q.get("difficulty") == level]
    if topic:
        topic_lower = topic.lower()
        filtered = [q for q in filtered if topic_lower in q.get("topic", "").lower()]
    return filtered


def display_question(question: Dict, index: int, total: int) -> None:
    """Display a single question."""
    c = COLOURS
    print(f"\n{c['bold']}Question {index}/{total}{c['reset']}")
    print(f"{c['blue']}[{question.get('difficulty', 'unknown')}] {question.get('topic', '')}{c['reset']}")
    print("-" * 60)
    print(f"\n{question.get('stem', '')}\n")
    if question.get("type") == "multiple_choice":
        for key, value in sorted(question.get("options", {}).items()):
            print(f"  {key}) {value}")
    elif question.get("type") == "fill_blank" and question.get("hint"):
        print(f"  {c['yellow']}Hint: {question.get('hint')}{c['reset']}")


def get_user_answer(question: Dict) -> str:
    """Get and validate user answer."""
    if question.get("type") == "multiple_choice":
        valid = list(question.get("options", {}).keys())
        while True:
            answer = input("\nYour answer (a/b/c/d): ").strip().lower()
            if answer in valid:
                return answer
            print(f"Invalid option. Choose from: {', '.join(valid)}")
    return input("\nYour answer: ").strip()


def check_answer(question: Dict, user_answer: str) -> bool:
    """Check if user answer is correct."""
    correct = question.get("correct")
    if question.get("type") == "multiple_choice":
        return user_answer.lower() == correct.lower()
    if isinstance(correct, list):
        return user_answer.lower() in [c.lower() for c in correct]
    return user_answer.lower() == correct.lower()


def display_feedback(question: Dict, is_correct: bool, user_answer: str) -> None:
    """Display feedback for the answered question."""
    c = COLOURS
    if is_correct:
        print(f"\n{c['green']}✓ Correct!{c['reset']}")
    else:
        correct = question.get("correct")
        if isinstance(correct, list):
            correct = correct[0]
        print(f"\n{c['red']}✗ Incorrect. The correct answer is: {correct}{c['reset']}")
    if explanation := question.get("explanation"):
        print(f"\n{c['yellow']}Explanation:{c['reset']} {explanation}")


def run_quiz(quiz: Dict, level: Optional[str] = None, topic: Optional[str] = None,
             randomise: bool = False, limit: Optional[int] = None) -> Dict[str, Any]:
    """Run the interactive quiz."""
    c = COLOURS
    questions = filter_questions(quiz.get("questions", []), level, topic)
    if not questions:
        print(f"{c['red']}No questions match the specified criteria.{c['reset']}")
        return {"score": 0, "total": 0, "percentage": 0}
    if randomise:
        questions = random.sample(questions, len(questions))
    if limit and limit < len(questions):
        questions = questions[:limit]

    metadata = quiz.get("metadata", {})
    print(f"\n{c['bold']}{'='*63}{c['reset']}")
    print(f"{c['bold']}Week {metadata.get('week', '11')} Quiz: {metadata.get('topic', 'Application Protocols')}{c['reset']}")
    print(f"Questions: {len(questions)} | Time: {metadata.get('estimated_time', '10-15 min')}")
    if level and level != "all":
        print(f"Difficulty: {level}")
    print(f"{c['bold']}{'='*63}{c['reset']}")
    input("\nPress Enter to begin...")

    correct_count = 0
    for i, question in enumerate(questions, 1):
        display_question(question, i, len(questions))
        user_answer = get_user_answer(question)
        is_correct = check_answer(question, user_answer)
        if is_correct:
            correct_count += 1
        display_feedback(question, is_correct, user_answer)
        if i < len(questions):
            input("\nPress Enter for next question...")

    percentage = (correct_count / len(questions)) * 100
    print(f"\n{c['bold']}{'='*63}{c['reset']}")
    print(f"{c['bold']}QUIZ COMPLETE{c['reset']}")
    print(f"Score: {correct_count}/{len(questions)} ({percentage:.0f}%)")
    
    passing = quiz.get("metadata", {}).get("passing_score", 70)
    if percentage >= 90:
        print(f"{c['green']}Excellent!{c['reset']}")
    elif percentage >= passing:
        print(f"{c['green']}Good job!{c['reset']}")
    else:
        print(f"{c['yellow']}Review recommended.{c['reset']}")
    print(f"{c['bold']}{'='*63}{c['reset']}")
    return {"score": correct_count, "total": len(questions), "percentage": percentage}


def review_quiz(quiz: Dict, level: Optional[str] = None) -> None:
    """Display all questions with answers."""
    c = COLOURS
    questions = filter_questions(quiz.get("questions", []), level)
    print(f"\n{c['bold']}QUIZ REVIEW — All Answers{c['reset']}\n")
    for i, q in enumerate(questions, 1):
        correct = q.get("correct")
        if isinstance(correct, list):
            correct = correct[0]
        print(f"Q{i} [{q.get('id')}] [{q.get('difficulty')}] {q.get('topic')}")
        print(f"  {c['green']}Answer: {correct}{c['reset']}\n")


def export_to_lms_json(quiz: Dict, output_path: Path = QUIZ_JSON_PATH) -> None:
    """Export quiz to LMS-compatible JSON format."""
    lms_quiz = {
        "metadata": {
            "title": f"Week {quiz.get('metadata', {}).get('week', '11')} Quiz",
            "description": quiz.get("metadata", {}).get("topic", ""),
            "time_limit_minutes": 15,
            "passing_score_percent": quiz.get("metadata", {}).get("passing_score", 70),
            "lms_compatibility": ["Moodle", "Canvas", "Blackboard"],
        },
        "questions": []
    }
    for q in quiz.get("questions", []):
        lms_q = {"id": q.get("id"), "type": q.get("type"), "text": q.get("stem"),
                 "difficulty": q.get("difficulty"), "topic": q.get("topic"), "points": 1}
        if q.get("type") == "multiple_choice":
            lms_q["answers"] = [
                {"text": v, "correct": k == q.get("correct")}
                for k, v in q.get("options", {}).items()
            ]
        else:
            correct = q.get("correct")
            lms_q["correct_answers"] = correct if isinstance(correct, list) else [correct]
        lms_quiz["questions"].append(lms_q)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(lms_quiz, f, indent=2, ensure_ascii=False)
    print(f"Exported {len(lms_quiz['questions'])} questions to: {output_path}")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Week 11 Formative Quiz")
    parser.add_argument("--level", "-l", choices=["basic", "intermediate", "advanced", "all"],
                        default="all", help="Filter by difficulty")
    parser.add_argument("--topic", "-t", type=str, help="Filter by topic")
    parser.add_argument("--random", "-r", action="store_true", help="Randomise order")
    parser.add_argument("--limit", "-n", type=int, help="Limit questions")
    parser.add_argument("--review", action="store_true", help="Review all answers")
    parser.add_argument("--export-json", action="store_true", help="Export to LMS JSON")
    parser.add_argument("--quiz-file", type=Path, default=QUIZ_YAML_PATH)
    args = parser.parse_args()

    try:
        quiz = load_quiz(args.quiz_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return 1

    if args.export_json:
        export_to_lms_json(quiz)
        return 0
    if args.review:
        review_quiz(quiz, args.level if args.level != "all" else None)
        return 0

    level = args.level if args.level != "all" else None
    results = run_quiz(quiz, level=level, topic=args.topic, randomise=args.random, limit=args.limit)
    passing = quiz.get("metadata", {}).get("passing_score", 70)
    return 0 if results["percentage"] >= passing else 1


if __name__ == "__main__":
    sys.exit(main())
