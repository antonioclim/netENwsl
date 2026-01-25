#!/usr/bin/env python3
"""
LMS Quiz Export Tool — Week 5: IP Addressing and Subnetting
============================================================

Converts quiz.yaml to LMS-compatible formats (Moodle XML, Canvas JSON).

Usage:
    python export_to_lms.py --format moodle --output quiz_moodle.xml
    python export_to_lms.py --format canvas --output quiz_canvas.json
    python export_to_lms.py --format json --output quiz_lms.json

Author: ing. dr. Antonio Clim, ASE-CSIE Bucharest
Version: 1.2.0 (January 2026)
"""

from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)


SCRIPT_DIR = Path(__file__).parent
DEFAULT_QUIZ_PATH = SCRIPT_DIR / "quiz.yaml"


# ═══════════════════════════════════════════════════════════════════════════════
# LOAD_QUIZ
# ═══════════════════════════════════════════════════════════════════════════════
def load_quiz(path: Path) -> Dict[str, Any]:
    """Load quiz from YAML file."""
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


# ═══════════════════════════════════════════════════════════════════════════════
# JSON_EXPORT
# ═══════════════════════════════════════════════════════════════════════════════
def export_to_json(quiz: Dict[str, Any]) -> Dict[str, Any]:
    """Export quiz to generic LMS-compatible JSON format."""
    metadata = quiz.get('metadata', {})
    questions = quiz.get('questions', [])
    
    return {
        "metadata": _build_json_metadata(metadata, quiz),
        "questions": [_convert_question_to_lms(q) for q in questions]
    }


def _build_json_metadata(metadata: Dict[str, Any], quiz: Dict[str, Any]) -> Dict[str, Any]:
    """Build metadata section for JSON export."""
    return {
        "title": f"Week {metadata.get('week', '?')}: {metadata.get('topic', 'Quiz')}",
        "week": metadata.get('week', 0),
        "topic": metadata.get('topic', ''),
        "description": f"Formative assessment covering {metadata.get('topic', 'course topics')}",
        "version": metadata.get('version', '1.0.0'),
        "time_limit_minutes": metadata.get('estimated_time_minutes', 15),
        "passing_score_percent": metadata.get('passing_score', 70),
        "shuffle_questions": False,
        "shuffle_answers": True,
        "exported_at": datetime.now().isoformat(),
        "export_format": "lms_json_v1",
        "learning_objectives": metadata.get('learning_objectives', []),
        "bloom_coverage": metadata.get('bloom_coverage', {}),
        "total_points": quiz.get('scoring', {}).get('total_possible', 0)
    }


def _convert_question_to_lms(q: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a single question to LMS format."""
    q_type = q.get('type', 'multiple_choice')
    
    lms_q = {
        "id": q.get('id', ''),
        "type": _map_question_type(q_type),
        "bloom_level": q.get('bloom_level', 'remember'),
        "difficulty": q.get('difficulty', 'intermediate'),
        "points": q.get('points', 1),
        "lo_ref": q.get('lo_ref', ''),
        "stem": q.get('stem', '').strip(),
        "correct": q.get('correct', ''),
        "feedback": {
            "general": q.get('explanation', '').strip() if q.get('explanation') else ''
        }
    }
    
    if q_type == 'multiple_choice':
        lms_q["answers"] = _build_mc_answers(q)
    elif q_type == 'fill_blank':
        lms_q["answers"] = _build_fill_blank_answers(q)
        lms_q["hint"] = q.get('hint', '')
    elif q_type == 'open_response':
        lms_q["rubric"] = q.get('rubric', [])
        lms_q["sample_answer"] = q.get('sample_answer', '')
        lms_q["manual_grading"] = True
    
    return lms_q


def _build_mc_answers(q: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Build answers list for multiple choice question."""
    options = q.get('options', {})
    correct = q.get('correct', '')
    answers = []
    for key, value in sorted(options.items()):
        answers.append({
            "id": key,
            "text": value,
            "is_correct": key == correct,
            "weight": 100 if key == correct else 0
        })
    return answers


def _build_fill_blank_answers(q: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Build answers list for fill-in-the-blank question."""
    correct_answers = q.get('correct', [])
    if isinstance(correct_answers, str):
        correct_answers = [correct_answers]
    return [{"text": ans, "is_correct": True} for ans in correct_answers]


def _map_question_type(q_type: str) -> str:
    """Map internal question type to LMS standard type."""
    mapping = {
        'multiple_choice': 'multiple_choice',
        'fill_blank': 'short_answer',
        'open_response': 'essay'
    }
    return mapping.get(q_type, 'multiple_choice')


# ═══════════════════════════════════════════════════════════════════════════════
# MOODLE_EXPORT
# ═══════════════════════════════════════════════════════════════════════════════
def export_to_moodle_xml(quiz: Dict[str, Any]) -> str:
    """Export quiz to Moodle XML format."""
    root = ET.Element('quiz')
    
    # Add category
    _add_moodle_category(root, quiz.get('metadata', {}))
    
    # Add questions
    for q in quiz.get('questions', []):
        q_elem = _build_moodle_question(q)
        root.append(q_elem)
    
    return ET.tostring(root, encoding='unicode', method='xml')


def _add_moodle_category(root: ET.Element, metadata: Dict[str, Any]) -> None:
    """Add category element to Moodle XML."""
    category = ET.SubElement(root, 'question')
    category.set('type', 'category')
    cat_elem = ET.SubElement(category, 'category')
    cat_text = ET.SubElement(cat_elem, 'text')
    cat_text.text = f"$course$/Week {metadata.get('week', '?')}: {metadata.get('topic', 'Quiz')}"


def _build_moodle_question(q: Dict[str, Any]) -> ET.Element:
    """Create a Moodle XML question element."""
    q_type = q.get('type', 'multiple_choice')
    moodle_type = {
        'multiple_choice': 'multichoice', 
        'fill_blank': 'shortanswer', 
        'open_response': 'essay'
    }.get(q_type, 'multichoice')
    
    question = ET.Element('question')
    question.set('type', moodle_type)
    
    # Name
    name = ET.SubElement(question, 'name')
    name_text = ET.SubElement(name, 'text')
    name_text.text = q.get('id', 'Question')
    
    # Question text
    qtext = ET.SubElement(question, 'questiontext')
    qtext.set('format', 'html')
    qtext_text = ET.SubElement(qtext, 'text')
    qtext_text.text = q.get('stem', '').strip()
    
    # Grade
    grade = ET.SubElement(question, 'defaultgrade')
    grade.text = str(q.get('points', 1))
    
    # Answers for MC
    if q_type == 'multiple_choice':
        _add_moodle_mc_answers(question, q)
    
    # Feedback
    if q.get('explanation'):
        feedback = ET.SubElement(question, 'generalfeedback')
        feedback.set('format', 'html')
        fb_text = ET.SubElement(feedback, 'text')
        fb_text.text = q.get('explanation', '').strip()
    
    return question


def _add_moodle_mc_answers(question: ET.Element, q: Dict[str, Any]) -> None:
    """Add answer elements for multiple choice question."""
    correct = q.get('correct', '')
    for key, value in sorted(q.get('options', {}).items()):
        answer = ET.SubElement(question, 'answer')
        answer.set('fraction', '100' if key == correct else '0')
        ans_text = ET.SubElement(answer, 'text')
        ans_text.text = value


# ═══════════════════════════════════════════════════════════════════════════════
# CANVAS_EXPORT
# ═══════════════════════════════════════════════════════════════════════════════
def export_to_canvas_json(quiz: Dict[str, Any]) -> Dict[str, Any]:
    """Export quiz to Canvas-compatible JSON format."""
    metadata = quiz.get('metadata', {})
    return {
        "quiz": {
            "title": f"Week {metadata.get('week', '?')}: {metadata.get('topic', 'Quiz')}",
            "quiz_type": "assignment",
            "time_limit": metadata.get('estimated_time_minutes', 15),
            "shuffle_answers": True,
            "points_possible": quiz.get('scoring', {}).get('total_possible', 0),
            "questions": [_build_canvas_question(q) for q in quiz.get('questions', [])]
        }
    }


def _build_canvas_question(q: Dict[str, Any]) -> Dict[str, Any]:
    """Build a Canvas-format question."""
    q_type = q.get('type', 'multiple_choice')
    
    canvas_type = {
        'multiple_choice': 'multiple_choice_question',
        'fill_blank': 'short_answer_question',
        'open_response': 'essay_question'
    }.get(q_type, 'multiple_choice_question')
    
    canvas_q = {
        "question_name": q.get('id', 'Question'),
        "question_type": canvas_type,
        "question_text": q.get('stem', '').strip(),
        "points_possible": q.get('points', 1),
        "answers": []
    }
    
    if q_type == 'multiple_choice':
        canvas_q["answers"] = _build_canvas_mc_answers(q)
    elif q_type == 'fill_blank':
        canvas_q["answers"] = _build_canvas_fill_answers(q)
    
    return canvas_q


def _build_canvas_mc_answers(q: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Build Canvas-format MC answers."""
    correct = q.get('correct', '')
    answers = []
    for key, value in sorted(q.get('options', {}).items()):
        answers.append({
            "answer_text": value,
            "weight": 100 if key == correct else 0
        })
    return answers


def _build_canvas_fill_answers(q: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Build Canvas-format fill-blank answers."""
    correct_answers = q.get('correct', [])
    if isinstance(correct_answers, str):
        correct_answers = [correct_answers]
    return [{"answer_text": ans, "weight": 100} for ans in correct_answers]


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Export quiz.yaml to LMS-compatible formats"
    )
    parser.add_argument(
        '--quiz', '-q', type=Path, 
        default=DEFAULT_QUIZ_PATH, 
        help='Path to quiz YAML file'
    )
    parser.add_argument(
        '--format', '-f', 
        choices=['json', 'moodle', 'canvas'], 
        default='json', 
        help='Export format'
    )
    parser.add_argument(
        '--output', '-o', type=Path, 
        help='Output file path'
    )
    parser.add_argument(
        '--pretty', action='store_true', 
        help='Pretty-print JSON output'
    )
    
    args = parser.parse_args(argv)
    
    try:
        quiz = load_quiz(args.quiz)
        print(f"Loaded quiz: {args.quiz}")
        print(f"  Questions: {len(quiz.get('questions', []))}")
    except FileNotFoundError:
        print(f"Error: Quiz file not found: {args.quiz}")
        return 1
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return 1
    
    if args.output:
        output_path = args.output
    else:
        suffix = '.xml' if args.format == 'moodle' else '.json'
        output_path = SCRIPT_DIR / f"quiz_lms_export{suffix}"
    
    try:
        if args.format == 'json':
            result = export_to_json(quiz)
            content = json.dumps(result, indent=2 if args.pretty else None, ensure_ascii=False)
        elif args.format == 'moodle':
            content = export_to_moodle_xml(quiz)
        elif args.format == 'canvas':
            result = export_to_canvas_json(quiz)
            content = json.dumps(result, indent=2 if args.pretty else None, ensure_ascii=False)
        else:
            return 1
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\nExported to: {output_path}")
        print(f"Format: {args.format.upper()}")
        return 0
        
    except IOError as e:
        print(f"Error writing output: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
