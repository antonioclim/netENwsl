#!/usr/bin/env python3
"""
Unit Tests for LMS Export Functionality
NETWORKING class — ASE, CSIE Bucharest | by ing. dr. Antonio Clim

Tests quiz validation, JSON export and format correctness.
Run with: pytest tests/test_lms_export.py -v
"""

import json
import sys
import tempfile
from pathlib import Path

import pytest
import yaml

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from formative.export_quiz_to_lms import (
    load_quiz_yaml,
    validate_quiz_structure,
    export_to_json,
    format_question_for_export,
)


# ═══════════════════════════════════════════════════════════════════════════════
# FIXTURES
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def sample_quiz_data():
    """Minimal valid quiz structure for testing."""
    return {
        'metadata': {
            'week': 2,
            'topic': 'Test Topic',
            'version': '1.0.0',
            'total_questions': 2,
        },
        'questions': [
            {
                'id': 'q01',
                'type': 'multiple_choice',
                'stem': 'What is 2+2?',
                'options': {'a': '3', 'b': '4', 'c': '5', 'd': '6'},
                'correct': 'b',
                'explanation': 'Basic arithmetic',
            },
            {
                'id': 'q02',
                'type': 'multiple_choice',
                'stem': 'Which protocol is connectionless?',
                'options': {'a': 'TCP', 'b': 'UDP', 'c': 'HTTP', 'd': 'FTP'},
                'correct': 'b',
                'explanation': 'UDP is connectionless',
            },
        ],
    }


@pytest.fixture
def quiz_yaml_file(sample_quiz_data):
    """Create temporary YAML file with quiz data."""
    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.yaml', delete=False
    ) as f:
        yaml.dump(sample_quiz_data, f)
        return Path(f.name)


@pytest.fixture
def real_quiz_path():
    """Path to actual quiz.yaml if it exists."""
    path = PROJECT_ROOT / 'formative' / 'quiz.yaml'
    if path.exists():
        return path
    pytest.skip('quiz.yaml not found')


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATOR TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestQuizValidator:
    """Tests for quiz structure validation."""

    def test_valid_quiz_passes(self, sample_quiz_data):
        """Valid quiz structure should pass validation."""
        errors = validate_quiz_structure(sample_quiz_data)
        assert len(errors) == 0, f"Unexpected errors: {errors}"

    def test_missing_metadata_fails(self, sample_quiz_data):
        """Quiz without metadata should fail."""
        del sample_quiz_data['metadata']
        errors = validate_quiz_structure(sample_quiz_data)
        assert any('metadata' in e.lower() for e in errors)

    def test_missing_questions_fails(self, sample_quiz_data):
        """Quiz without questions should fail."""
        del sample_quiz_data['questions']
        errors = validate_quiz_structure(sample_quiz_data)
        assert any('questions' in e.lower() for e in errors)

    def test_empty_questions_fails(self, sample_quiz_data):
        """Quiz with empty questions list should fail."""
        sample_quiz_data['questions'] = []
        errors = validate_quiz_structure(sample_quiz_data)
        assert any('questions' in e.lower() or 'empty' in e.lower() for e in errors)

    def test_question_missing_id_fails(self, sample_quiz_data):
        """Question without ID should fail."""
        del sample_quiz_data['questions'][0]['id']
        errors = validate_quiz_structure(sample_quiz_data)
        assert len(errors) > 0

    def test_question_missing_correct_fails(self, sample_quiz_data):
        """Question without correct answer should fail."""
        del sample_quiz_data['questions'][0]['correct']
        errors = validate_quiz_structure(sample_quiz_data)
        assert len(errors) > 0

    def test_invalid_correct_option_fails(self, sample_quiz_data):
        """Question with invalid correct option should fail."""
        sample_quiz_data['questions'][0]['correct'] = 'z'  # Not in options
        errors = validate_quiz_structure(sample_quiz_data)
        assert len(errors) > 0


# ═══════════════════════════════════════════════════════════════════════════════
# YAML LOADER TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestYamlLoader:
    """Tests for YAML loading functionality."""

    def test_load_valid_yaml(self, quiz_yaml_file):
        """Should load valid YAML file."""
        data = load_quiz_yaml(quiz_yaml_file)
        assert 'metadata' in data
        assert 'questions' in data

    def test_load_nonexistent_file(self):
        """Should raise error for missing file."""
        with pytest.raises((FileNotFoundError, IOError)):
            load_quiz_yaml(Path('/nonexistent/path.yaml'))

    def test_load_real_quiz(self, real_quiz_path):
        """Should load actual quiz.yaml successfully."""
        data = load_quiz_yaml(real_quiz_path)
        assert 'metadata' in data
        assert 'questions' in data
        assert len(data['questions']) >= 10


# ═══════════════════════════════════════════════════════════════════════════════
# JSON EXPORT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestJsonExport:
    """Tests for JSON export functionality."""

    def test_export_produces_valid_json(self, sample_quiz_data):
        """Export should produce valid JSON structure."""
        result = export_to_json(sample_quiz_data)
        # Should be serialisable
        json_str = json.dumps(result)
        assert len(json_str) > 0
        # Should be deserialisable
        parsed = json.loads(json_str)
        assert 'questions' in parsed

    def test_export_preserves_question_count(self, sample_quiz_data):
        """Export should preserve number of questions."""
        result = export_to_json(sample_quiz_data)
        assert len(result['questions']) == len(sample_quiz_data['questions'])

    def test_export_includes_metadata(self, sample_quiz_data):
        """Export should include metadata."""
        result = export_to_json(sample_quiz_data)
        assert 'metadata' in result or 'week' in result

    def test_export_question_has_required_fields(self, sample_quiz_data):
        """Exported questions should have required LMS fields."""
        result = export_to_json(sample_quiz_data)
        for q in result['questions']:
            assert 'id' in q or 'question_id' in q
            assert 'stem' in q or 'question_text' in q or 'text' in q
            assert 'options' in q or 'answers' in q or 'choices' in q

    def test_export_idempotency(self, sample_quiz_data):
        """Exporting twice should produce identical results."""
        result1 = export_to_json(sample_quiz_data)
        result2 = export_to_json(sample_quiz_data)
        assert json.dumps(result1, sort_keys=True) == json.dumps(result2, sort_keys=True)


# ═══════════════════════════════════════════════════════════════════════════════
# QUESTION FORMATTING TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestQuestionFormatting:
    """Tests for individual question formatting."""

    def test_format_multiple_choice(self, sample_quiz_data):
        """Should format multiple choice question correctly."""
        q = sample_quiz_data['questions'][0]
        formatted = format_question_for_export(q)
        assert formatted is not None
        # Should preserve essential info
        assert 'q01' in str(formatted) or formatted.get('id') == 'q01'

    def test_format_preserves_options(self, sample_quiz_data):
        """Should preserve all answer options."""
        q = sample_quiz_data['questions'][0]
        formatted = format_question_for_export(q)
        # Check options are present (format may vary)
        formatted_str = json.dumps(formatted)
        for option_text in q['options'].values():
            assert option_text in formatted_str

    def test_format_marks_correct_answer(self, sample_quiz_data):
        """Should indicate which answer is correct."""
        q = sample_quiz_data['questions'][0]
        formatted = format_question_for_export(q)
        # Correct answer should be identifiable
        formatted_str = json.dumps(formatted)
        # Either explicit 'correct' field or marked in options
        assert 'correct' in formatted_str.lower() or 'true' in formatted_str.lower()


# ═══════════════════════════════════════════════════════════════════════════════
# INTEGRATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestIntegration:
    """End-to-end integration tests."""

    def test_full_pipeline_with_temp_file(self, quiz_yaml_file):
        """Test complete load → validate → export pipeline."""
        # Load
        data = load_quiz_yaml(quiz_yaml_file)
        assert data is not None

        # Validate
        errors = validate_quiz_structure(data)
        assert len(errors) == 0

        # Export
        result = export_to_json(data)
        assert len(result['questions']) > 0

        # Verify JSON serialisation
        json_str = json.dumps(result, indent=2)
        assert len(json_str) > 100  # Not trivially small

    def test_real_quiz_export(self, real_quiz_path):
        """Test export with actual quiz.yaml."""
        data = load_quiz_yaml(real_quiz_path)
        errors = validate_quiz_structure(data)
        
        # Real quiz should be valid
        assert len(errors) == 0, f"Validation errors: {errors}"

        result = export_to_json(data)
        
        # Should have substantial content
        assert len(result['questions']) >= 10
        
        # Each question should be well-formed
        for q in result['questions']:
            assert q is not None


# ═══════════════════════════════════════════════════════════════════════════════
# CANVAS/MOODLE FORMAT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestLMSFormats:
    """Tests for specific LMS format requirements."""

    def test_canvas_format_compatibility(self, sample_quiz_data):
        """Export should be compatible with Canvas QTI import."""
        result = export_to_json(sample_quiz_data)
        # Canvas expects specific structure
        assert 'questions' in result
        for q in result['questions']:
            # Canvas needs question text
            has_text = any(k in q for k in ['stem', 'text', 'question_text'])
            assert has_text, "Question missing text field for Canvas"

    def test_moodle_format_compatibility(self, sample_quiz_data):
        """Export should be compatible with Moodle import."""
        result = export_to_json(sample_quiz_data)
        # Moodle expects certain fields
        assert 'questions' in result
        for q in result['questions']:
            # Moodle needs answer options
            has_options = any(k in q for k in ['options', 'answers', 'choices'])
            assert has_options, "Question missing options for Moodle"


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
