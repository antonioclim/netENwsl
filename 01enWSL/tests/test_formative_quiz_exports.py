#!/usr/bin/env python3
"""
Tests for Formative Quiz Exports and Validation
================================================
Computer Networks - Week 1 (WSL Environment)
ASE Bucharest | by ing. dr. Antonio Clim

Tests cover:
- Quiz YAML validation
- Canvas JSON export structure
- Moodle XML export structure
- LMS JSON roundtrip
- Bloom level coverage
- Learning Objective coverage
"""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent

# Import the quiz runner as a module
from formative.run_quiz import (
    load_quiz,
    validate_quiz,
    export_to_canvas_json,
    export_to_moodle_xml,
    iter_questions,
    save_quiz_json,
    build_question_index,
)


def _quiz_path() -> Path:
    return PROJECT_ROOT / "formative" / "quiz.yaml"


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_quiz_yaml_validates() -> None:
    """Quiz YAML file passes structural validation."""
    quiz = load_quiz(_quiz_path())
    ok, errors = validate_quiz(quiz)
    assert ok, f"Validation errors: {errors}"


def test_quiz_has_required_top_level_keys() -> None:
    """Quiz contains metadata, sections and questions."""
    quiz = load_quiz(_quiz_path())
    assert "metadata" in quiz, "Missing metadata"
    assert "sections" in quiz, "Missing sections"
    assert "questions" in quiz, "Missing questions"


def test_all_questions_have_correct_answer() -> None:
    """Every question has a correct answer defined."""
    quiz = load_quiz(_quiz_path())
    missing = []
    for sec_id, q in iter_questions(quiz):
        qid = q.get("id", "unknown")
        qtype = str(q.get("type") or "").strip()
        has_correct = "correct" in q or "answer" in q
        if qtype in {"multiple_choice", "mcq", "true_false", "fill_blank", "numeric"}:
            if not has_correct:
                missing.append(f"{sec_id}/{qid}")
    assert not missing, f"Questions missing correct answer: {missing}"


def test_all_questions_have_bloom_level() -> None:
    """Every question specifies a Bloom taxonomy level."""
    quiz = load_quiz(_quiz_path())
    valid_levels = {"remember", "understand", "apply", "analyse", "evaluate", "create"}
    missing = []
    invalid = []
    for sec_id, q in iter_questions(quiz):
        qid = q.get("id", "unknown")
        level = str(q.get("bloom_level") or "").strip().lower()
        if not level:
            missing.append(f"{sec_id}/{qid}")
        elif level not in valid_levels:
            invalid.append(f"{sec_id}/{qid}: {level}")
    assert not missing, f"Questions missing bloom_level: {missing}"
    assert not invalid, f"Questions with invalid bloom_level: {invalid}"


def test_all_questions_have_lo_reference() -> None:
    """Every question references a Learning Objective."""
    quiz = load_quiz(_quiz_path())
    missing = []
    for sec_id, q in iter_questions(quiz):
        qid = q.get("id", "unknown")
        lo = q.get("lo_ref")
        if not lo:
            missing.append(f"{sec_id}/{qid}")
    assert not missing, f"Questions missing lo_ref: {missing}"


# ═══════════════════════════════════════════════════════════════════════════════
# BLOOM LEVEL COVERAGE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_bloom_levels_have_minimum_coverage() -> None:
    """Quiz covers at least 3 different Bloom levels."""
    quiz = load_quiz(_quiz_path())
    levels = set()
    for _, q in iter_questions(quiz):
        level = str(q.get("bloom_level") or "").strip().lower()
        if level:
            levels.add(level)
    assert len(levels) >= 3, f"Only {len(levels)} Bloom levels covered: {levels}"


def test_bloom_distribution_is_reasonable() -> None:
    """Lower levels (remember/understand) don't dominate excessively."""
    quiz = load_quiz(_quiz_path())
    counts = {"remember": 0, "understand": 0, "apply": 0, "analyse": 0}
    total = 0
    for _, q in iter_questions(quiz):
        level = str(q.get("bloom_level") or "").strip().lower()
        if level in counts:
            counts[level] += 1
        total += 1
    
    lower = counts["remember"] + counts["understand"]
    higher = counts["apply"] + counts["analyse"]
    
    # Lower levels should not exceed 70% of total
    if total > 0:
        lower_pct = (lower / total) * 100
        assert lower_pct <= 75, f"Lower Bloom levels too dominant: {lower_pct:.1f}%"


# ═══════════════════════════════════════════════════════════════════════════════
# CANVAS EXPORT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_canvas_export_has_expected_shape(tmp_path: Path) -> None:
    """Canvas export contains title and questions list."""
    quiz = load_quiz(_quiz_path())
    out = tmp_path / "quiz_canvas.json"
    export_to_canvas_json(quiz, out)

    payload = json.loads(out.read_text(encoding="utf-8"))
    assert "title" in payload, "Missing title"
    assert isinstance(payload["questions"], list), "questions must be a list"

    expected = 0
    for _, q in iter_questions(quiz):
        t = str(q.get("type") or "").strip()
        if t in {"multiple_choice", "mcq", "true_false"}:
            expected += 1

    assert len(payload["questions"]) == expected


def test_canvas_export_questions_have_required_fields(tmp_path: Path) -> None:
    """Each Canvas question has stem, options and correct answer."""
    quiz = load_quiz(_quiz_path())
    out = tmp_path / "quiz_canvas.json"
    export_to_canvas_json(quiz, out)

    payload = json.loads(out.read_text(encoding="utf-8"))
    for i, q in enumerate(payload["questions"]):
        assert "stem" in q, f"Question {i} missing stem"
        assert "options" in q, f"Question {i} missing options"
        assert "correct" in q, f"Question {i} missing correct"


def test_canvas_export_is_valid_json(tmp_path: Path) -> None:
    """Canvas export produces valid JSON."""
    quiz = load_quiz(_quiz_path())
    out = tmp_path / "quiz_canvas.json"
    export_to_canvas_json(quiz, out)
    
    # Should not raise
    content = out.read_text(encoding="utf-8")
    parsed = json.loads(content)
    assert isinstance(parsed, dict)


# ═══════════════════════════════════════════════════════════════════════════════
# MOODLE EXPORT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_moodle_export_contains_questions(tmp_path: Path) -> None:
    """Moodle XML export contains expected number of questions."""
    quiz = load_quiz(_quiz_path())
    out = tmp_path / "quiz_moodle.xml"
    export_to_moodle_xml(quiz, out)

    tree = ET.parse(out)
    root = tree.getroot()
    assert root.tag == "quiz"

    exported = 0
    for _, q in iter_questions(quiz):
        t = str(q.get("type") or "").strip()
        if t in {"multiple_choice", "mcq", "true_false", "fill_blank"}:
            exported += 1

    questions = root.findall("question")
    assert len(questions) == exported


def test_moodle_export_has_valid_question_types(tmp_path: Path) -> None:
    """Moodle questions have valid type attributes."""
    quiz = load_quiz(_quiz_path())
    out = tmp_path / "quiz_moodle.xml"
    export_to_moodle_xml(quiz, out)

    tree = ET.parse(out)
    root = tree.getroot()
    
    valid_types = {"multichoice", "truefalse", "shortanswer"}
    for q in root.findall("question"):
        qtype = q.get("type")
        assert qtype in valid_types, f"Invalid Moodle question type: {qtype}"


def test_moodle_multichoice_has_answers(tmp_path: Path) -> None:
    """Moodle multichoice questions have answer elements."""
    quiz = load_quiz(_quiz_path())
    out = tmp_path / "quiz_moodle.xml"
    export_to_moodle_xml(quiz, out)

    tree = ET.parse(out)
    root = tree.getroot()
    
    for q in root.findall("question[@type='multichoice']"):
        answers = q.findall("answer")
        assert len(answers) >= 2, "Multichoice needs at least 2 answers"
        
        # Exactly one should have fraction="100"
        correct = [a for a in answers if a.get("fraction") == "100"]
        assert len(correct) == 1, "Exactly one answer should be correct"


def test_moodle_export_is_valid_xml(tmp_path: Path) -> None:
    """Moodle export produces well-formed XML."""
    quiz = load_quiz(_quiz_path())
    out = tmp_path / "quiz_moodle.xml"
    export_to_moodle_xml(quiz, out)
    
    # Should not raise
    tree = ET.parse(out)
    assert tree.getroot() is not None


# ═══════════════════════════════════════════════════════════════════════════════
# LMS JSON EXPORT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_lms_json_export_roundtrips(tmp_path: Path) -> None:
    """LMS JSON export can be loaded back."""
    quiz = load_quiz(_quiz_path())
    out = tmp_path / "quiz_lms_export.json"
    save_quiz_json(quiz, out)

    payload = json.loads(out.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    assert "questions" in payload
    assert "sections" in payload

    # Questions are expected to be a list of dicts with an id
    assert isinstance(payload["questions"], list)
    assert all(isinstance(q, dict) and q.get("id") for q in payload["questions"])

    # Sections should reference question ids rather than duplicating full objects
    assert isinstance(payload["sections"], list)
    for sec in payload["sections"]:
        assert isinstance(sec, dict)
        assert sec.get("id")
        qids = sec.get("questions")
        assert isinstance(qids, list)
        assert all(isinstance(x, str) for x in qids)


def test_lms_json_preserves_question_count(tmp_path: Path) -> None:
    """LMS JSON has same question count as source."""
    quiz = load_quiz(_quiz_path())
    out = tmp_path / "quiz_lms_export.json"
    save_quiz_json(quiz, out)

    payload = json.loads(out.read_text(encoding="utf-8"))
    
    original_count = len(build_question_index(quiz))
    exported_count = len(payload["questions"])
    
    assert exported_count == original_count


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATOR EDGE CASES
# ═══════════════════════════════════════════════════════════════════════════════

def test_validator_rejects_empty_quiz() -> None:
    """Validator rejects quiz without required keys."""
    empty_quiz: dict = {}
    ok, errors = validate_quiz(empty_quiz)
    assert not ok
    assert any("metadata" in e for e in errors)


def test_validator_rejects_invalid_mcq() -> None:
    """Validator catches MCQ without correct answer in options."""
    bad_quiz = {
        "metadata": {"week": 1},
        "sections": [
            {"id": "test", "questions": ["q1"]}
        ],
        "questions": [
            {
                "id": "q1",
                "type": "multiple_choice",
                "stem": "Test?",
                "options": {"a": "A", "b": "B"},
                "correct": "z"  # Not in options
            }
        ]
    }
    ok, errors = validate_quiz(bad_quiz)
    assert not ok
    assert any("correct" in e.lower() or "option" in e.lower() for e in errors)


def test_validator_accepts_minimal_valid_quiz() -> None:
    """Validator accepts minimal but valid quiz structure."""
    minimal = {
        "metadata": {"week": 1},
        "sections": [
            {"id": "s1", "questions": ["q1"]}
        ],
        "questions": [
            {
                "id": "q1",
                "type": "true_false",
                "stem": "Is this a test?",
                "correct": True
            }
        ]
    }
    ok, errors = validate_quiz(minimal)
    assert ok, f"Validation failed: {errors}"
