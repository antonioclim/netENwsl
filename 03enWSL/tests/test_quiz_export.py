#!/usr/bin/env python3
"""
Unit Tests for Quiz Validation and LMS Export
NETWORKING class - ASE, CSIE | by ing. dr. Antonio Clim

Run with: pytest tests/test_quiz_export.py -v
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path
import pytest

# Adjust path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from formative.run_quiz import (
    load_quiz,
    validate_quiz,
    export_moodle,
    export_json,
)


# ═══════════════════════════════════════════════════════════════════════════════
# TEST FIXTURES
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def valid_quiz() -> dict:
    """Minimal valid quiz structure."""
    return {
        'metadata': {
            'title': 'Test Quiz',
            'week': 3,
            'passing_score': 70
        },
        'questions': [
            {
                'id': 'q01',
                'lo_ref': 'LO1',
                'bloom_level': 'remember',
                'type': 'multiple_choice',
                'stem': 'What is 2+2?',
                'options': {'a': '3', 'b': '4', 'c': '5'},
                'correct': 'b'
            },
            {
                'id': 'q02',
                'lo_ref': 'LO2',
                'bloom_level': 'understand',
                'type': 'fill_blank',
                'stem': 'The capital of France is ___',
                'correct': ['Paris', 'paris']
            }
        ]
    }


@pytest.fixture
def invalid_quiz_missing_metadata() -> dict:
    """Quiz missing metadata section."""
    return {
        'questions': [
            {'id': 'q01', 'stem': 'Test?', 'correct': 'a'}
        ]
    }


@pytest.fixture
def invalid_quiz_missing_fields() -> dict:
    """Quiz with questions missing required fields."""
    return {
        'metadata': {'title': 'Test'},
        'questions': [
            {
                'id': 'q01',
                'stem': 'What?'
                # Missing: lo_ref, bloom_level, type, correct
            }
        ]
    }


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestQuizValidation:
    """Tests for quiz structure validation."""
    
    def test_valid_quiz_passes(self, valid_quiz: dict) -> None:
        """Valid quiz should return empty error list."""
        errors = validate_quiz(valid_quiz)
        assert errors == []
    
    def test_missing_metadata_detected(
        self, invalid_quiz_missing_metadata: dict
    ) -> None:
        """Missing metadata should be detected."""
        errors = validate_quiz(invalid_quiz_missing_metadata)
        assert any('metadata' in e.lower() for e in errors)
    
    def test_missing_question_fields_detected(
        self, invalid_quiz_missing_fields: dict
    ) -> None:
        """Missing required fields in questions should be detected."""
        errors = validate_quiz(invalid_quiz_missing_fields)
        # Should detect missing lo_ref, bloom_level, type, correct
        assert len(errors) >= 4
        assert any('lo_ref' in e for e in errors)
        assert any('bloom_level' in e for e in errors)
    
    def test_empty_quiz_detected(self) -> None:
        """Empty quiz should be detected."""
        errors = validate_quiz({})
        assert len(errors) >= 2  # Missing metadata and questions


# ═══════════════════════════════════════════════════════════════════════════════
# MOODLE EXPORT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestMoodleExport:
    """Tests for Moodle GIFT format export."""
    
    def test_moodle_export_creates_file(self, valid_quiz: dict) -> None:
        """Export should create a file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'quiz.gift'
            export_moodle(valid_quiz, output)
            assert output.exists()
    
    def test_moodle_export_contains_questions(self, valid_quiz: dict) -> None:
        """Export should contain question IDs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'quiz.gift'
            export_moodle(valid_quiz, output)
            content = output.read_text(encoding='utf-8')
            assert 'q01' in content
            # q02 is fill_blank, may not be exported
    
    def test_moodle_export_correct_answer_marked(
        self, valid_quiz: dict
    ) -> None:
        """Correct answer should be marked with = prefix."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'quiz.gift'
            export_moodle(valid_quiz, output)
            content = output.read_text(encoding='utf-8')
            # Option b (value '4') is correct
            assert '=4' in content
    
    def test_moodle_export_wrong_answers_marked(
        self, valid_quiz: dict
    ) -> None:
        """Wrong answers should be marked with ~ prefix."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'quiz.gift'
            export_moodle(valid_quiz, output)
            content = output.read_text(encoding='utf-8')
            # Options a and c are wrong
            assert '~3' in content
            assert '~5' in content


# ═══════════════════════════════════════════════════════════════════════════════
# JSON/CANVAS EXPORT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestJsonExport:
    """Tests for JSON/Canvas format export."""
    
    def test_json_export_creates_file(self, valid_quiz: dict) -> None:
        """Export should create a valid JSON file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'quiz.json'
            export_json(valid_quiz, output)
            assert output.exists()
    
    def test_json_export_is_valid_json(self, valid_quiz: dict) -> None:
        """Export should be parseable as JSON."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'quiz.json'
            export_json(valid_quiz, output)
            content = output.read_text(encoding='utf-8')
            data = json.loads(content)  # Should not raise
            assert isinstance(data, dict)
    
    def test_json_export_contains_metadata(self, valid_quiz: dict) -> None:
        """Export should contain metadata section."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'quiz.json'
            export_json(valid_quiz, output)
            data = json.loads(output.read_text(encoding='utf-8'))
            assert 'metadata' in data
            assert data['metadata']['title'] == 'Test Quiz'
    
    def test_json_export_contains_questions(self, valid_quiz: dict) -> None:
        """Export should contain all questions."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'quiz.json'
            export_json(valid_quiz, output)
            data = json.loads(output.read_text(encoding='utf-8'))
            assert 'questions' in data
            assert len(data['questions']) == 2
    
    def test_json_export_has_timestamp(self, valid_quiz: dict) -> None:
        """Export should include export timestamp."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'quiz.json'
            export_json(valid_quiz, output)
            data = json.loads(output.read_text(encoding='utf-8'))
            assert 'exported' in data


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ FILE LOADING TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestQuizLoading:
    """Tests for quiz file loading."""
    
    def test_load_actual_quiz_file(self) -> None:
        """Should be able to load the actual quiz.yaml file."""
        quiz_path = Path(__file__).parent.parent / 'formative' / 'quiz.yaml'
        if quiz_path.exists():
            quiz = load_quiz(quiz_path)
            assert 'metadata' in quiz
            assert 'questions' in quiz
            assert len(quiz['questions']) >= 10


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
