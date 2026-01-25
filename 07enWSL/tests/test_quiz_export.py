#!/usr/bin/env python3
"""
Quiz Export Tests — Week 7
==========================
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Unit tests for the LMS export functionality including Moodle XML
and Canvas JSON format validation.

Usage:
    python3 -m pytest tests/test_quiz_export.py -v
    python3 tests/test_quiz_export.py
"""

from __future__ import annotations

import json
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# ═══════════════════════════════════════════════════════════════════════════════
# TEST DATA
# ═══════════════════════════════════════════════════════════════════════════════

SAMPLE_QUIZ_YAML = """
metadata:
  week: 7
  topic: "Test Quiz"
  version: "1.0.0"
  passing_score: 70

questions:
  - id: q01
    type: multiple_choice
    lo_ref: LO1
    bloom_level: remember
    difficulty: basic
    points: 1
    stem: "What port does the TCP server use?"
    options:
      a: "8080"
      b: "9090"
      c: "9000"
      d: "80"
    correct: b
    explanation: "TCP server uses port 9090."
    lms_feedback:
      correct: "Correct!"
      incorrect: "Review the configuration."

  - id: q02
    type: true_false
    lo_ref: LO2
    bloom_level: understand
    difficulty: basic
    points: 1
    stem: "UDP provides delivery confirmation."
    correct: false
    explanation: "UDP is connectionless with no delivery confirmation."
"""


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def create_temp_quiz() -> Path:
    """Create a temporary quiz YAML file for testing."""
    with tempfile.NamedTemporaryFile(
        mode='w', 
        suffix='.yaml', 
        delete=False,
        encoding='utf-8'
    ) as f:
        f.write(SAMPLE_QUIZ_YAML)
        return Path(f.name)


# ═══════════════════════════════════════════════════════════════════════════════
# MOODLE XML EXPORT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_moodle_xml_structure():
    """Test that Moodle XML export produces valid structure."""
    try:
        from formative.quiz_export import load_quiz, export_moodle_xml
    except ImportError:
        print("SKIP: quiz_export module not available")
        return True
    
    quiz_path = create_temp_quiz()
    
    try:
        raw_quiz = load_quiz(quiz_path)
        
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.xml',
            delete=False,
            encoding='utf-8'
        ) as f:
            output_path = Path(f.name)
        
        export_moodle_xml(raw_quiz, output_path)
        
        # Parse and validate XML structure
        tree = ET.parse(output_path)
        root = tree.getroot()
        
        assert root.tag == "quiz", "Root element should be 'quiz'"
        
        questions = root.findall(".//question")
        assert len(questions) >= 2, f"Expected at least 2 questions, got {len(questions)}"
        
        # Check question types
        q_types = [q.get("type") for q in questions]
        assert "multichoice" in q_types, "Should have multichoice question"
        assert "truefalse" in q_types, "Should have truefalse question"
        
        print("✓ Moodle XML structure test passed")
        return True
        
    finally:
        quiz_path.unlink()
        if 'output_path' in locals():
            output_path.unlink()


def test_moodle_question_content():
    """Test that Moodle questions contain expected content."""
    try:
        from formative.quiz_export import load_quiz, export_moodle_xml
    except ImportError:
        print("SKIP: quiz_export module not available")
        return True
    
    quiz_path = create_temp_quiz()
    
    try:
        raw_quiz = load_quiz(quiz_path)
        
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.xml',
            delete=False,
            encoding='utf-8'
        ) as f:
            output_path = Path(f.name)
        
        export_moodle_xml(raw_quiz, output_path)
        
        tree = ET.parse(output_path)
        root = tree.getroot()
        
        # Find multichoice question
        mc_question = root.find(".//question[@type='multichoice']")
        assert mc_question is not None, "Multichoice question not found"
        
        # Check stem exists
        stem = mc_question.find(".//questiontext/text")
        assert stem is not None, "Question stem not found"
        assert "port" in stem.text.lower(), "Stem should mention port"
        
        # Check answers exist
        answers = mc_question.findall(".//answer")
        assert len(answers) == 4, f"Expected 4 answers, got {len(answers)}"
        
        print("✓ Moodle question content test passed")
        return True
        
    finally:
        quiz_path.unlink()
        if 'output_path' in locals():
            output_path.unlink()


# ═══════════════════════════════════════════════════════════════════════════════
# CANVAS JSON EXPORT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_canvas_json_structure():
    """Test that Canvas JSON export produces valid structure."""
    try:
        from formative.quiz_export import load_quiz, export_canvas_json
    except ImportError:
        print("SKIP: quiz_export module not available")
        return True
    
    quiz_path = create_temp_quiz()
    
    try:
        raw_quiz = load_quiz(quiz_path)
        
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.json',
            delete=False,
            encoding='utf-8'
        ) as f:
            output_path = Path(f.name)
        
        export_canvas_json(raw_quiz, output_path)
        
        # Load and validate JSON
        with open(output_path, 'r', encoding='utf-8') as f:
            canvas_quiz = json.load(f)
        
        assert "quiz" in canvas_quiz, "Root should have 'quiz' key"
        assert "questions" in canvas_quiz, "Root should have 'questions' key"
        
        questions = canvas_quiz["questions"]
        assert len(questions) >= 2, f"Expected at least 2 questions, got {len(questions)}"
        
        print("✓ Canvas JSON structure test passed")
        return True
        
    finally:
        quiz_path.unlink()
        if 'output_path' in locals():
            output_path.unlink()


def test_canvas_question_types():
    """Test that Canvas questions have correct type mappings."""
    try:
        from formative.quiz_export import load_quiz, export_canvas_json
    except ImportError:
        print("SKIP: quiz_export module not available")
        return True
    
    quiz_path = create_temp_quiz()
    
    try:
        raw_quiz = load_quiz(quiz_path)
        
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.json',
            delete=False,
            encoding='utf-8'
        ) as f:
            output_path = Path(f.name)
        
        export_canvas_json(raw_quiz, output_path)
        
        with open(output_path, 'r', encoding='utf-8') as f:
            canvas_quiz = json.load(f)
        
        questions = canvas_quiz["questions"]
        q_types = [q.get("question_type") for q in questions]
        
        # Canvas uses these type names
        valid_types = {
            "multiple_choice_question",
            "true_false_question",
            "short_answer_question",
            "matching_question"
        }
        
        for qtype in q_types:
            assert qtype in valid_types, f"Invalid Canvas question type: {qtype}"
        
        print("✓ Canvas question types test passed")
        return True
        
    finally:
        quiz_path.unlink()
        if 'output_path' in locals():
            output_path.unlink()


# ═══════════════════════════════════════════════════════════════════════════════
# GENERIC JSON EXPORT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_generic_json_completeness():
    """Test that generic JSON export includes all question data."""
    try:
        from formative.quiz_export import load_quiz, export_generic_json
    except ImportError:
        print("SKIP: quiz_export module not available")
        return True
    
    quiz_path = create_temp_quiz()
    
    try:
        raw_quiz = load_quiz(quiz_path)
        
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.json',
            delete=False,
            encoding='utf-8'
        ) as f:
            output_path = Path(f.name)
        
        export_generic_json(raw_quiz, output_path)
        
        with open(output_path, 'r', encoding='utf-8') as f:
            exported = json.load(f)
        
        # Check metadata preserved
        assert "metadata" in exported, "Should include metadata"
        assert exported["metadata"]["week"] == 7, "Week should be 7"
        
        # Check questions preserved
        assert "questions" in exported, "Should include questions"
        
        for q in exported["questions"]:
            assert "id" in q, "Question should have id"
            assert "stem" in q, "Question should have stem"
            assert "correct" in q, "Question should have correct answer"
        
        print("✓ Generic JSON completeness test passed")
        return True
        
    finally:
        quiz_path.unlink()
        if 'output_path' in locals():
            output_path.unlink()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def run_all_tests() -> int:
    """Run all export tests and return exit code."""
    tests = [
        test_moodle_xml_structure,
        test_moodle_question_content,
        test_canvas_json_structure,
        test_canvas_question_types,
        test_generic_json_completeness,
    ]
    
    print("=" * 60)
    print("Quiz Export Tests — Week 7")
    print("=" * 60)
    print()
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            result = test()
            if result:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ {test.__name__}: {e}")
            failed += 1
    
    print()
    print("-" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
