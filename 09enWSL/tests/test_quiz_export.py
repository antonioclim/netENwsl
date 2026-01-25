#!/usr/bin/env python3
"""
Quiz Export Validation Tests — Week 9
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Tests for validating formative quiz YAML structure and LMS JSON export.
Ensures compatibility with Canvas and Moodle import formats.

Usage:
    python tests/test_quiz_export.py
    python -m pytest tests/test_quiz_export.py -v
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

# When run from improved archive, tests should still work against original
# PROJECT_ROOT points to the merged directory (original + improved)
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# For testing during development, allow override
import os
if os.environ.get("QUIZ_TEST_ROOT"):
    PROJECT_ROOT = Path(os.environ["QUIZ_TEST_ROOT"])

# Try to import yaml, provide helpful error if missing
try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

QUIZ_YAML_PATH = PROJECT_ROOT / "formative" / "quiz.yaml"
QUIZ_JSON_PATH = PROJECT_ROOT / "formative" / "quiz_lms.json"

REQUIRED_METADATA_FIELDS = [
    "week", "title", "version", "author",
    "estimated_time_minutes", "passing_score_percent", "total_questions"
]

REQUIRED_QUESTION_FIELDS = [
    "id", "lo_ref", "stem", "correct"
]

VALID_BLOOM_LEVELS = [
    "remember", "understand", "apply", "analyse", "evaluate", "create"
]

VALID_LO_REFS = ["LO1", "LO2", "LO3", "LO4", "LO5", "LO6"]


# ═══════════════════════════════════════════════════════════════════════════════
# YAML_SCHEMA_TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_quiz_yaml_exists():
    """Verify quiz.yaml file exists."""
    assert QUIZ_YAML_PATH.exists(), f"Quiz YAML not found: {QUIZ_YAML_PATH}"
    print("✓ test_quiz_yaml_exists passed")


def test_quiz_yaml_parseable():
    """Verify quiz.yaml is valid YAML."""
    with open(QUIZ_YAML_PATH, 'r', encoding='utf-8') as f:
        quiz = yaml.safe_load(f)
    
    assert quiz is not None, "Quiz YAML parsed to None"
    assert isinstance(quiz, dict), "Quiz YAML should be a dictionary"
    print("✓ test_quiz_yaml_parseable passed")
    return quiz


def test_quiz_yaml_metadata():
    """Verify quiz metadata contains required fields."""
    with open(QUIZ_YAML_PATH, 'r', encoding='utf-8') as f:
        quiz = yaml.safe_load(f)
    
    assert "metadata" in quiz, "Missing 'metadata' section"
    metadata = quiz["metadata"]
    
    for field in REQUIRED_METADATA_FIELDS:
        assert field in metadata, f"Missing metadata field: {field}"
    
    # Type checks
    assert isinstance(metadata["week"], int), "week should be integer"
    assert isinstance(metadata["total_questions"], int), "total_questions should be integer"
    assert metadata["week"] == 9, "Week should be 9"
    
    print("✓ test_quiz_yaml_metadata passed")


def test_quiz_yaml_questions_structure():
    """Verify each question has required fields."""
    with open(QUIZ_YAML_PATH, 'r', encoding='utf-8') as f:
        quiz = yaml.safe_load(f)
    
    assert "questions" in quiz, "Missing 'questions' section"
    questions = quiz["questions"]
    
    assert isinstance(questions, list), "questions should be a list"
    assert len(questions) >= 10, f"Expected 10+ questions, found {len(questions)}"
    
    # Fields required for all questions
    base_required = ["id", "lo_ref", "stem"]
    
    for i, q in enumerate(questions):
        for field in base_required:
            assert field in q, f"Question {i+1} missing field: {field}"
        
        # Validate LO reference
        assert q["lo_ref"] in VALID_LO_REFS, \
            f"Question {i+1} has invalid lo_ref: {q['lo_ref']}"
        
        # Validate Bloom level if present
        if "bloom_level" in q:
            assert q["bloom_level"] in VALID_BLOOM_LEVELS, \
                f"Question {i+1} has invalid bloom_level: {q['bloom_level']}"
        
        # Type-specific validation
        qtype = q.get("type", "multiple_choice")
        if qtype == "open_response":
            # Open response needs rubric instead of correct answer
            assert "rubric" in q or "sample_answer" in q, \
                f"Question {i+1} (open_response) needs rubric or sample_answer"
        elif qtype not in ["fill_blank", "code_trace"]:
            # Multiple choice needs correct answer
            assert "correct" in q, f"Question {i+1} missing 'correct' field"
    
    print(f"✓ test_quiz_yaml_questions_structure passed ({len(questions)} questions)")


def test_quiz_yaml_question_ids_unique():
    """Verify all question IDs are unique."""
    with open(QUIZ_YAML_PATH, 'r', encoding='utf-8') as f:
        quiz = yaml.safe_load(f)
    
    ids = [q["id"] for q in quiz["questions"]]
    unique_ids = set(ids)
    
    assert len(ids) == len(unique_ids), \
        f"Duplicate question IDs found: {len(ids)} total, {len(unique_ids)} unique"
    
    print("✓ test_quiz_yaml_question_ids_unique passed")


def test_quiz_yaml_lo_coverage():
    """Verify all Learning Objectives are covered."""
    with open(QUIZ_YAML_PATH, 'r', encoding='utf-8') as f:
        quiz = yaml.safe_load(f)
    
    covered_los = set(q["lo_ref"] for q in quiz["questions"])
    
    for lo in VALID_LO_REFS:
        assert lo in covered_los, f"Learning Objective {lo} not covered by any question"
    
    print(f"✓ test_quiz_yaml_lo_coverage passed (all 6 LOs covered)")


def test_quiz_yaml_answers_valid():
    """Verify answer options and correct answers are valid."""
    with open(QUIZ_YAML_PATH, 'r', encoding='utf-8') as f:
        quiz = yaml.safe_load(f)
    
    for i, q in enumerate(quiz["questions"]):
        qid = q.get("id", f"question_{i+1}")
        qtype = q.get("type", "multiple_choice")
        
        # Skip validation for open_response and code_trace types
        if qtype in ["open_response", "code_trace"]:
            continue
        
        # Skip if no correct answer (some types may not have one)
        if "correct" not in q:
            continue
        
        correct = q["correct"]
        
        # fill_blank can have list of correct answers
        if qtype == "fill_blank":
            assert isinstance(correct, (str, list)), \
                f"{qid}: fill_blank correct should be string or list"
            continue
        
        # For multiple choice: single letter answer
        assert isinstance(correct, str) and len(correct) == 1, \
            f"{qid}: correct answer should be single letter"
        assert correct.lower() in "abcde", \
            f"{qid}: correct answer '{correct}' not in a-e range"
        
        # If options present, verify correct answer exists
        if "options" in q:
            options = q["options"]
            assert correct.lower() in options or correct.upper() in options, \
                f"{qid}: correct answer '{correct}' not in options"
    
    print("✓ test_quiz_yaml_answers_valid passed")


# ═══════════════════════════════════════════════════════════════════════════════
# LMS_JSON_EXPORT_TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_quiz_lms_json_exists():
    """Verify quiz_lms.json file exists."""
    assert QUIZ_JSON_PATH.exists(), f"LMS JSON not found: {QUIZ_JSON_PATH}"
    print("✓ test_quiz_lms_json_exists passed")


def test_quiz_lms_json_parseable():
    """Verify quiz_lms.json is valid JSON."""
    with open(QUIZ_JSON_PATH, 'r', encoding='utf-8') as f:
        lms_data = json.load(f)
    
    assert lms_data is not None, "LMS JSON parsed to None"
    assert isinstance(lms_data, dict), "LMS JSON should be a dictionary"
    print("✓ test_quiz_lms_json_parseable passed")
    return lms_data


def test_quiz_lms_json_structure():
    """Verify LMS JSON has Canvas/Moodle compatible structure."""
    with open(QUIZ_JSON_PATH, 'r', encoding='utf-8') as f:
        lms_data = json.load(f)
    
    # Check top-level structure
    assert "quiz" in lms_data or "questions" in lms_data, \
        "LMS JSON should have 'quiz' or 'questions' key"
    
    # Get questions array (handle different structures)
    if "quiz" in lms_data:
        questions = lms_data["quiz"].get("questions", [])
    else:
        questions = lms_data.get("questions", [])
    
    assert len(questions) >= 10, f"Expected 10+ questions in LMS export"
    
    # Verify each question has required LMS fields
    for i, q in enumerate(questions):
        assert "question_text" in q or "stem" in q or "text" in q, \
            f"Question {i+1} missing question text field"
        
        qtype = q.get("type", "multiple_choice")
        # open_response can have rubric instead of answers
        if qtype == "open_response":
            assert "rubric" in q or "answers" in q or "options" in q or "choices" in q, \
                f"Question {i+1} (open_response) missing rubric or answers"
        else:
            assert "answers" in q or "options" in q or "choices" in q or "correct_answer" in q, \
                f"Question {i+1} missing answers field"
    
    print(f"✓ test_quiz_lms_json_structure passed ({len(questions)} questions)")


def test_quiz_lms_json_no_email_addresses():
    """Verify LMS export contains no email addresses."""
    with open(QUIZ_JSON_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple email pattern check
    import re
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    matches = re.findall(email_pattern, content)
    
    assert len(matches) == 0, f"Found email addresses in LMS export: {matches}"
    print("✓ test_quiz_lms_json_no_email_addresses passed")


def test_quiz_lms_json_matches_yaml_count():
    """Verify LMS JSON has same number of questions as YAML."""
    with open(QUIZ_YAML_PATH, 'r', encoding='utf-8') as f:
        yaml_quiz = yaml.safe_load(f)
    
    with open(QUIZ_JSON_PATH, 'r', encoding='utf-8') as f:
        json_quiz = json.load(f)
    
    yaml_count = len(yaml_quiz["questions"])
    
    # Handle different JSON structures
    if "quiz" in json_quiz:
        json_count = len(json_quiz["quiz"].get("questions", []))
    else:
        json_count = len(json_quiz.get("questions", []))
    
    assert yaml_count == json_count, \
        f"Question count mismatch: YAML={yaml_count}, JSON={json_count}"
    
    print(f"✓ test_quiz_lms_json_matches_yaml_count passed ({yaml_count} questions)")


# ═══════════════════════════════════════════════════════════════════════════════
# CANVAS_MOODLE_COMPATIBILITY_TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_canvas_import_compatibility():
    """Verify JSON structure is Canvas-compatible."""
    with open(QUIZ_JSON_PATH, 'r', encoding='utf-8') as f:
        lms_data = json.load(f)
    
    # Canvas expects specific field names
    # This is a basic compatibility check
    
    if "quiz" in lms_data:
        quiz = lms_data["quiz"]
        
        # Canvas quiz metadata
        if "title" in quiz:
            assert isinstance(quiz["title"], str), "title should be string"
        
        if "questions" in quiz:
            for q in quiz["questions"]:
                # Canvas question structure
                if "question_type" in q:
                    valid_types = [
                        "multiple_choice_question",
                        "true_false_question",
                        "short_answer_question",
                        "essay_question"
                    ]
                    # Don't fail, just warn
                    if q["question_type"] not in valid_types:
                        print(f"  Warning: Non-standard question type: {q['question_type']}")
    
    print("✓ test_canvas_import_compatibility passed")


def test_moodle_gift_convertible():
    """Verify questions can be converted to Moodle GIFT format."""
    with open(QUIZ_YAML_PATH, 'r', encoding='utf-8') as f:
        quiz = yaml.safe_load(f)
    
    # Check that each question has the fields needed for GIFT conversion
    for i, q in enumerate(quiz["questions"]):
        qtype = q.get("type", "multiple_choice")
        
        # GIFT needs: stem for all types
        assert "stem" in q, f"Question {i+1} needs 'stem' for GIFT"
        
        # For open_response/essay types, GIFT uses {} for essay
        if qtype == "open_response":
            # Essay questions don't need 'correct' in GIFT
            continue
        
        # Multiple choice and fill_blank need correct answer
        if qtype in ["multiple_choice", "fill_blank"]:
            assert "correct" in q, f"Question {i+1} needs 'correct' for GIFT"
        
        # Options should be present for multiple choice
        if "options" in q and qtype == "multiple_choice":
            assert isinstance(q["options"], dict), \
                f"Question {i+1} options should be a dictionary"
    
    print("✓ test_moodle_gift_convertible passed")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════

def run_all_tests() -> int:
    """Run all tests and return exit code."""
    tests = [
        # YAML tests
        test_quiz_yaml_exists,
        test_quiz_yaml_parseable,
        test_quiz_yaml_metadata,
        test_quiz_yaml_questions_structure,
        test_quiz_yaml_question_ids_unique,
        test_quiz_yaml_lo_coverage,
        test_quiz_yaml_answers_valid,
        # JSON tests
        test_quiz_lms_json_exists,
        test_quiz_lms_json_parseable,
        test_quiz_lms_json_structure,
        test_quiz_lms_json_no_email_addresses,
        test_quiz_lms_json_matches_yaml_count,
        # Compatibility tests
        test_canvas_import_compatibility,
        test_moodle_gift_convertible,
    ]
    
    print("=" * 60)
    print("  Quiz Export Validation Tests — Week 9")
    print("=" * 60)
    print()
    
    passed = 0
    failed = 0
    skipped = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except FileNotFoundError as e:
            print(f"⊘ {test.__name__} SKIPPED: {e}")
            skipped += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} ERROR: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"  Results: {passed} passed, {failed} failed, {skipped} skipped")
    print("=" * 60)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
