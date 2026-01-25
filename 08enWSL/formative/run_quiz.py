#!/usr/bin/env python3
"""
Formative Quiz Runner — Week 8: Transport Layer & HTTP
======================================================

Interactive quiz runner with support for:
- CLI interactive mode with immediate feedback
- LMS export (Moodle XML, Canvas QTI, JSON)
- Progress tracking integration
- Filtering by LO, difficulty and Bloom level

Usage:
    python formative/run_quiz.py                     # Interactive mode
    python formative/run_quiz.py --random            # Randomised order
    python formative/run_quiz.py --lo LO3            # Filter by LO
    python formative/run_quiz.py --difficulty basic  # Filter by difficulty
    python formative/run_quiz.py --export-lms        # Export for LMS (JSON)
    python formative/run_quiz.py --export-moodle     # Export Moodle XML
    python formative/run_quiz.py --export-canvas     # Export Canvas QTI
    python formative/run_quiz.py --review            # Review mode (show answers)

Course: Computer Networks — ASE, CSIE

Implements Brown & Wilson Principle 2 (Peer Instruction) through
immediate feedback and misconception-targeted questions.
"""

import argparse
import json
import random
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import yaml


QUIZ_FILE = Path(__file__).parent / "quiz.yaml"
PROGRESS_FILE = Path(__file__).parent.parent / "artifacts" / "quiz_progress.json"


# ═══════════════════════════════════════════════════════════════════════════════
# DATA_LOADING
# ═══════════════════════════════════════════════════════════════════════════════

def load_quiz(path: Path = QUIZ_FILE) -> dict[str, Any]:
    """Load quiz from YAML file."""
    with open(path, encoding='utf-8') as f:
        return yaml.safe_load(f)


def filter_questions(
    questions: list[dict],
    lo: Optional[str] = None,
    difficulty: Optional[str] = None,
    bloom: Optional[str] = None,
    limit: Optional[int] = None
) -> list[dict]:
    """Filter questions by criteria."""
    filtered = questions.copy()
    
    if lo:
        lo_upper = lo.upper()
        filtered = [q for q in filtered if q.get('lo_ref', '').upper() == lo_upper]
    
    if difficulty:
        filtered = [q for q in filtered if q.get('difficulty', '').lower() == difficulty.lower()]
    
    if bloom:
        filtered = [q for q in filtered if q.get('bloom_level', '').lower() == bloom.lower()]
    
    if limit and limit > 0:
        filtered = filtered[:limit]
    
    return filtered


# ═══════════════════════════════════════════════════════════════════════════════
# QUESTION_ASKING
# ═══════════════════════════════════════════════════════════════════════════════

def _print_question_header(question: dict) -> None:
    """Print question header with metadata."""
    print(f"\n{'─' * 60}")
    print(f"[{question.get('difficulty', '?').upper()}] {question.get('lo_ref', '?')}")
    print(f"{'─' * 60}")
    print(f"\n{question['stem']}")


def ask_multiple_choice(question: dict, show_answer: bool = False) -> bool:
    """Ask a multiple choice question and return if correct."""
    _print_question_header(question)
    
    options = question.get('options', {})
    for key in sorted(options.keys()):
        print(f"   {key}) {options[key]}")
    
    if show_answer:
        print(f"\n📖 Correct answer: {question['correct']}")
        print(f"   {question.get('explanation', '')}")
        return True
    
    answer = input("\nYour answer (a/b/c/d): ").strip().lower()
    correct = question.get('correct', '').lower()
    
    if answer == correct:
        print("✅ Correct!")
        return True
    
    print(f"❌ Wrong. Correct answer: {correct}")
    if 'explanation' in question:
        print(f"\n📖 Explanation:\n{question['explanation']}")
    return False


def ask_fill_blank(question: dict, show_answer: bool = False) -> bool:
    """Ask a fill-in-the-blank question and return if correct."""
    _print_question_header(question)
    
    correct_answers = question.get('correct', [])
    if isinstance(correct_answers, str):
        correct_answers = [correct_answers]
    
    if show_answer:
        print(f"\n📖 Accepted answers: {', '.join(correct_answers)}")
        print(f"   {question.get('explanation', '')}")
        return True
    
    answer = input("\nYour answer: ").strip()
    
    if answer.lower() in [c.lower() for c in correct_answers]:
        print("✅ Correct!")
        return True
    
    print(f"❌ Wrong. Accepted answers: {', '.join(correct_answers)}")
    if 'explanation' in question:
        print(f"\n📖 Explanation:\n{question['explanation']}")
    return False


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ_EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════

def _print_quiz_header(metadata: dict, questions: list, review_mode: bool) -> None:
    """Print quiz header."""
    print("\n" + "═" * 60)
    print(f"📝 FORMATIVE QUIZ — Week {metadata.get('week', '?')}")
    print(f"   {metadata.get('topic', 'Unknown Topic')}")
    print("═" * 60)
    print(f"Questions: {len(questions)}")
    print(f"Passing score: {metadata.get('passing_score', 70)}%")
    if review_mode:
        print("Mode: REVIEW (answers shown)")
    print("═" * 60)


def _ask_question(q: dict, review_mode: bool) -> Optional[bool]:
    """Ask a single question based on type."""
    qtype = q.get('question_type', 'multiple_choice')
    
    if qtype == 'multiple_choice':
        return ask_multiple_choice(q, show_answer=review_mode)
    elif qtype == 'fill_blank':
        return ask_fill_blank(q, show_answer=review_mode)
    else:
        print(f"⚠️  Unknown question type: {qtype}")
        return None


def _process_questions(questions: list, review_mode: bool) -> dict:
    """Process all questions and collect results."""
    correct_count = 0
    lo_scores: dict[str, dict] = {}
    wrong_questions: list[str] = []
    questions_answered: list[str] = []
    
    for i, q in enumerate(questions, 1):
        print(f"\n📌 Question {i}/{len(questions)}")
        
        lo = q.get('lo_ref', 'Unknown')
        qid = q.get('id', f'q{i}')
        questions_answered.append(qid)
        
        if lo not in lo_scores:
            lo_scores[lo] = {'correct': 0, 'total': 0}
        lo_scores[lo]['total'] += 1
        
        is_correct = _ask_question(q, review_mode)
        
        if is_correct is None:
            continue
        
        if is_correct:
            correct_count += 1
            lo_scores[lo]['correct'] += 1
        else:
            wrong_questions.append(qid)
    
    return {
        'correct_count': correct_count,
        'lo_scores': lo_scores,
        'wrong_questions': wrong_questions,
        'questions_answered': questions_answered
    }


def _print_results(results: dict, total: int, elapsed: float, passing_score: int) -> None:
    """Print quiz results."""
    correct_count = results['correct_count']
    lo_scores = results['lo_scores']
    percentage = (correct_count / total) * 100 if total else 0
    passed = percentage >= passing_score
    
    print("\n" + "═" * 60)
    print("📊 RESULTS")
    print("═" * 60)
    print(f"\nScore: {correct_count}/{total} ({percentage:.1f}%)")
    print(f"Time: {elapsed:.0f} seconds")
    print(f"Status: {'✅ PASSED' if passed else '❌ NEEDS REVIEW'}")
    
    print(f"\n📈 Learning Objective Breakdown:")
    for lo in sorted(lo_scores.keys()):
        data = lo_scores[lo]
        lo_pct = (data['correct'] / data['total']) * 100 if data['total'] > 0 else 0
        filled = int(lo_pct / 10)
        bar = "█" * filled + "░" * (10 - filled)
        status = "✅" if lo_pct >= 70 else "⚠️" if lo_pct >= 50 else "❌"
        print(f"   {lo}: {bar} {lo_pct:.0f}% ({data['correct']}/{data['total']}) {status}")
    
    weak_los = [lo for lo, data in lo_scores.items() 
                if (data['correct'] / data['total']) * 100 < 70]
    if weak_los:
        print(f"\n📚 Recommended review: {', '.join(weak_los)}")
        print("   See: docs/learning_objectives.md for targeted resources")
    
    print("\n" + "═" * 60 + "\n")


def run_quiz(
    quiz: dict[str, Any],
    randomise: bool = False,
    lo_filter: Optional[str] = None,
    difficulty_filter: Optional[str] = None,
    limit: Optional[int] = None,
    review_mode: bool = False
) -> dict[str, Any]:
    """
    Run the interactive quiz.
    
    Returns:
        Dictionary with results for progress tracking
    """
    metadata = quiz.get('metadata', {})
    questions = quiz.get('questions', [])
    
    questions = filter_questions(
        questions,
        lo=lo_filter,
        difficulty=difficulty_filter,
        limit=limit
    )
    
    if not questions:
        print("❌ No questions match your filters.")
        return {}
    
    if randomise:
        random.shuffle(questions)
    
    _print_quiz_header(metadata, questions, review_mode)
    
    start_time = time.time()
    results = _process_questions(questions, review_mode)
    elapsed = time.time() - start_time
    
    passing_score = metadata.get('passing_score', 70)
    _print_results(results, len(questions), elapsed, passing_score)
    
    percentage = (results['correct_count'] / len(questions)) * 100 if questions else 0
    
    return {
        "score": results['correct_count'],
        "total": len(questions),
        "percentage": percentage,
        "lo_scores": {lo: (d['correct'] / d['total']) * 100 for lo, d in results['lo_scores'].items()},
        "wrong_questions": results['wrong_questions'],
        "questions_answered": results['questions_answered'],
        "time_spent_seconds": elapsed,
        "passed": percentage >= passing_score
    }


def record_progress(results: dict[str, Any]) -> None:
    """Record quiz results to progress file."""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, encoding='utf-8') as f:
            progress = json.load(f)
    else:
        progress = {"attempts": []}
    
    progress["attempts"].append({
        "timestamp": datetime.now().isoformat(),
        **results
    })
    
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2)


# ═══════════════════════════════════════════════════════════════════════════════
# LMS_EXPORT_JSON
# ═══════════════════════════════════════════════════════════════════════════════

def _build_lms_question(q: dict) -> dict:
    """Build a single LMS-compatible question."""
    lms_q = {
        "id": q.get('id'),
        "type": "multiple_choice" if q.get('question_type') == 'multiple_choice' else "short_answer",
        "points": q.get('points', 5),
        "text": q.get('stem', '').strip(),
        "category": q.get('lo_ref', 'General'),
        "difficulty": q.get('difficulty', 'intermediate'),
    }
    
    if q.get('question_type') == 'multiple_choice':
        lms_q["answers"] = [
            {"text": v, "correct": k == q.get('correct')}
            for k, v in q.get('options', {}).items()
        ]
    else:
        correct = q.get('correct', [])
        if isinstance(correct, str):
            correct = [correct]
        lms_q["correct_answers"] = correct
    
    if 'explanation' in q:
        lms_q["feedback"] = q['explanation'].strip()
    
    return lms_q


def export_to_json(quiz: dict[str, Any], output_path: Path) -> None:
    """Export quiz to JSON format (LMS compatible)."""
    metadata = quiz.get('metadata', {})
    questions = quiz.get('questions', [])
    
    lms_export = {
        "quiz_metadata": {
            "title": f"Week {metadata.get('week', '?')}: {metadata.get('topic', 'Quiz')}",
            "description": f"Formative assessment for Week {metadata.get('week', '?')}",
            "time_limit_minutes": metadata.get('estimated_time_minutes', 20),
            "passing_score_percent": metadata.get('passing_score', 70),
            "shuffle_answers": True,
            "show_correct_answers": True,
            "allow_multiple_attempts": True,
        },
        "questions": [_build_lms_question(q) for q in questions]
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(lms_export, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Exported {len(questions)} questions to {output_path}")
    print("   This JSON can be imported into most LMS systems.")


# ═══════════════════════════════════════════════════════════════════════════════
# MOODLE_EXPORT
# ═══════════════════════════════════════════════════════════════════════════════

def _add_moodle_category(root: ET.Element, metadata: dict) -> None:
    """Add category element to Moodle XML."""
    category = ET.SubElement(root, 'question')
    category.set('type', 'category')
    cat_text = ET.SubElement(category, 'category')
    cat_text_inner = ET.SubElement(cat_text, 'text')
    cat_text_inner.text = f"$course$/Week{metadata.get('week', '8')}_Transport_HTTP"


def _add_moodle_question(root: ET.Element, q: dict) -> None:
    """Add a question element to Moodle XML."""
    question = ET.SubElement(root, 'question')
    question.set('type', 'multichoice')
    
    name = ET.SubElement(question, 'name')
    name_text = ET.SubElement(name, 'text')
    name_text.text = q.get('id', 'Q')
    
    qtext = ET.SubElement(question, 'questiontext')
    qtext.set('format', 'html')
    qtext_text = ET.SubElement(qtext, 'text')
    qtext_text.text = f"<![CDATA[<p>{q.get('stem', '').strip()}</p>]]>"
    
    if 'explanation' in q:
        feedback = ET.SubElement(question, 'generalfeedback')
        feedback.set('format', 'html')
        fb_text = ET.SubElement(feedback, 'text')
        fb_text.text = f"<![CDATA[<p>{q['explanation'].strip()}</p>]]>"
    
    grade = ET.SubElement(question, 'defaultgrade')
    grade.text = str(q.get('points', 5))
    
    shuffle = ET.SubElement(question, 'shuffleanswers')
    shuffle.text = '1'
    
    single = ET.SubElement(question, 'single')
    single.text = 'true'
    
    correct_key = q.get('correct', '')
    for key, value in q.get('options', {}).items():
        answer = ET.SubElement(question, 'answer')
        answer.set('fraction', '100' if key == correct_key else '0')
        answer.set('format', 'html')
        ans_text = ET.SubElement(answer, 'text')
        ans_text.text = f"<![CDATA[<p>{value}</p>]]>"


def export_to_moodle_xml(quiz: dict[str, Any], output_path: Path) -> None:
    """Export quiz to Moodle XML format."""
    metadata = quiz.get('metadata', {})
    questions = quiz.get('questions', [])
    
    root = ET.Element('quiz')
    _add_moodle_category(root, metadata)
    
    mc_count = 0
    for q in questions:
        if q.get('question_type') == 'multiple_choice':
            _add_moodle_question(root, q)
            mc_count += 1
    
    tree = ET.ElementTree(root)
    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    
    print(f"✅ Exported {mc_count} questions to {output_path}")
    print("   Import in Moodle: Course → Question Bank → Import → Moodle XML")


# ═══════════════════════════════════════════════════════════════════════════════
# CANVAS_EXPORT
# ═══════════════════════════════════════════════════════════════════════════════

def export_to_canvas_qti(quiz: dict[str, Any], output_path: Path) -> None:
    """Export quiz to Canvas QTI format."""
    metadata = quiz.get('metadata', {})
    questions = quiz.get('questions', [])
    
    # Canvas QTI 1.2 format
    root = ET.Element('questestinterop')
    root.set('xmlns', 'http://www.imsglobal.org/xsd/ims_qtiasiv1p2')
    
    assessment = ET.SubElement(root, 'assessment')
    assessment.set('ident', f"week{metadata.get('week', '8')}_quiz")
    assessment.set('title', f"Week {metadata.get('week', '8')}: {metadata.get('topic', 'Quiz')}")
    
    section = ET.SubElement(assessment, 'section')
    section.set('ident', 'root_section')
    
    for q in questions:
        if q.get('question_type') != 'multiple_choice':
            continue
        
        item = ET.SubElement(section, 'item')
        item.set('ident', q.get('id', 'q'))
        item.set('title', q.get('id', 'Question'))
        
        # Presentation
        presentation = ET.SubElement(item, 'presentation')
        material = ET.SubElement(presentation, 'material')
        mattext = ET.SubElement(material, 'mattext')
        mattext.set('texttype', 'text/html')
        mattext.text = q.get('stem', '')
        
        # Response
        response = ET.SubElement(presentation, 'response_lid')
        response.set('ident', 'response1')
        response.set('rcardinality', 'Single')
        
        render = ET.SubElement(response, 'render_choice')
        for key, value in q.get('options', {}).items():
            label = ET.SubElement(render, 'response_label')
            label.set('ident', key)
            mat = ET.SubElement(label, 'material')
            txt = ET.SubElement(mat, 'mattext')
            txt.set('texttype', 'text/plain')
            txt.text = value
        
        # Processing
        resprocessing = ET.SubElement(item, 'resprocessing')
        outcomes = ET.SubElement(resprocessing, 'outcomes')
        decvar = ET.SubElement(outcomes, 'decvar')
        decvar.set('maxvalue', str(q.get('points', 5)))
        decvar.set('minvalue', '0')
        decvar.set('varname', 'SCORE')
        decvar.set('vartype', 'Decimal')
        
        # Correct answer
        respcondition = ET.SubElement(resprocessing, 'respcondition')
        respcondition.set('continue', 'No')
        conditionvar = ET.SubElement(respcondition, 'conditionvar')
        varequal = ET.SubElement(conditionvar, 'varequal')
        varequal.set('respident', 'response1')
        varequal.text = q.get('correct', '')
        setvar = ET.SubElement(respcondition, 'setvar')
        setvar.set('action', 'Set')
        setvar.set('varname', 'SCORE')
        setvar.text = str(q.get('points', 5))
    
    tree = ET.ElementTree(root)
    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    
    mc_count = sum(1 for q in questions if q.get('question_type') == 'multiple_choice')
    print(f"✅ Exported {mc_count} questions to {output_path}")
    print("   Import in Canvas: Course → Settings → Import → QTI")


# ═══════════════════════════════════════════════════════════════════════════════
# LISTING
# ═══════════════════════════════════════════════════════════════════════════════

def list_questions(quiz: dict[str, Any]) -> None:
    """List all questions with metadata."""
    questions = quiz.get('questions', [])
    
    print("\n" + "═" * 70)
    print("📋 QUIZ QUESTIONS")
    print("═" * 70)
    
    for q in questions:
        qid = q.get('id', '?')
        lo = q.get('lo_ref', '?')
        diff = q.get('difficulty', '?')
        bloom = q.get('bloom_level', '?')
        qtype = q.get('question_type', '?')
        stem = q.get('stem', '')
        stem_short = stem[:50] + "..." if len(stem) > 50 else stem
        
        print(f"\n{qid}: [{lo}] [{diff}] [{bloom}] ({qtype})")
        print(f"    {stem_short}")
    
    print("\n" + "═" * 70 + "\n")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Main entry point for quiz runner."""
    parser = argparse.ArgumentParser(
        description="Run formative assessment quiz",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument("--random", "-r", action="store_true",
                        help="Randomise question order")
    parser.add_argument("--lo", type=str,
                        help="Filter by Learning Objective (e.g., LO3)")
    parser.add_argument("--difficulty", "-d",
                        choices=["basic", "intermediate", "advanced"],
                        help="Filter by difficulty")
    parser.add_argument("--limit", "-n", type=int,
                        help="Limit number of questions")
    parser.add_argument("--review", action="store_true",
                        help="Review mode — show all answers")
    parser.add_argument("--list-questions", action="store_true",
                        help="List all questions without running quiz")
    parser.add_argument("--export-lms", type=Path, metavar="FILE",
                        help="Export to LMS-compatible JSON")
    parser.add_argument("--export-moodle", type=Path, metavar="FILE",
                        help="Export to Moodle XML format")
    parser.add_argument("--export-canvas", type=Path, metavar="FILE",
                        help="Export to Canvas QTI format")
    parser.add_argument("--no-progress", action="store_true",
                        help="Do not record progress")
    
    args = parser.parse_args()
    
    if not QUIZ_FILE.exists():
        print(f"❌ Quiz file not found: {QUIZ_FILE}")
        return 1
    
    quiz = load_quiz()
    
    if args.export_lms:
        export_to_json(quiz, args.export_lms)
        return 0
    
    if args.export_moodle:
        export_to_moodle_xml(quiz, args.export_moodle)
        return 0
    
    if args.export_canvas:
        export_to_canvas_qti(quiz, args.export_canvas)
        return 0
    
    if args.list_questions:
        list_questions(quiz)
        return 0
    
    results = run_quiz(
        quiz,
        randomise=args.random,
        lo_filter=args.lo,
        difficulty_filter=args.difficulty,
        limit=args.limit,
        review_mode=args.review,
    )
    
    if results and not args.no_progress and not args.review:
        record_progress(results)
    
    return 0 if results.get('passed', False) else 1


if __name__ == "__main__":
    sys.exit(main())
