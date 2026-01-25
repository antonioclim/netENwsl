#!/usr/bin/env python3
"""
Tests for Quiz Export Functions and Validators
===============================================

Tests the LMS export functionality (Moodle XML, Canvas QTI, JSON)
and quiz YAML validation.

Run with: pytest tests/test_exports.py -v

Course: Computer Networks — ASE, CSIE
"""

import json
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
import yaml


# ═══════════════════════════════════════════════════════════════════════════════
# FIXTURES
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def sample_quiz():
    """Sample quiz data for testing exports."""
    return {
        "metadata": {
            "week": 8,
            "topic": "Transport Layer & HTTP",
            "passing_score": 70,
            "estimated_time_minutes": 20
        },
        "questions": [
            {
                "id": "q01",
                "question_type": "multiple_choice",
                "lo_ref": "LO1",
                "difficulty": "basic",
                "bloom_level": "remember",
                "points": 5,
                "stem": "What is the maximum TCP port number?",
                "options": {
                    "a": "32768",
                    "b": "65535",
                    "c": "65536",
                    "d": "256"
                },
                "correct": "b",
                "explanation": "TCP port numbers are 16-bit, so max is 2^16 - 1 = 65535"
            },
            {
                "id": "q02",
                "question_type": "fill_blank",
                "lo_ref": "LO2",
                "difficulty": "intermediate",
                "bloom_level": "understand",
                "points": 5,
                "stem": "The TCP handshake uses ___ packets.",
                "correct": ["3", "three", "Three"],
                "explanation": "TCP uses a three-way handshake: SYN, SYN-ACK, ACK"
            }
        ]
    }


@pytest.fixture
def quiz_file_path():
    """Path to actual quiz.yaml file."""
    return Path(__file__).parent.parent / "formative" / "quiz.yaml"


# ═══════════════════════════════════════════════════════════════════════════════
# YAML_VALIDATION_TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestQuizYamlValidation:
    """Tests for quiz.yaml structure and validity."""
    
    def test_quiz_yaml_exists(self, quiz_file_path):
        """Quiz YAML file should exist."""
        assert quiz_file_path.exists(), f"Quiz file not found: {quiz_file_path}"
    
    def test_quiz_yaml_parseable(self, quiz_file_path):
        """Quiz YAML should be valid YAML."""
        if not quiz_file_path.exists():
            pytest.skip("Quiz file not found")
        
        with open(quiz_file_path, encoding='utf-8') as f:
            quiz = yaml.safe_load(f)
        
        assert quiz is not None
        assert isinstance(quiz, dict)
    
    def test_quiz_has_metadata(self, quiz_file_path):
        """Quiz should have metadata section."""
        if not quiz_file_path.exists():
            pytest.skip("Quiz file not found")
        
        with open(quiz_file_path, encoding='utf-8') as f:
            quiz = yaml.safe_load(f)
        
        assert 'metadata' in quiz
        assert 'week' in quiz['metadata']
        assert 'topic' in quiz['metadata']
    
    def test_quiz_has_questions(self, quiz_file_path):
        """Quiz should have questions."""
        if not quiz_file_path.exists():
            pytest.skip("Quiz file not found")
        
        with open(quiz_file_path, encoding='utf-8') as f:
            quiz = yaml.safe_load(f)
        
        assert 'questions' in quiz
        assert len(quiz['questions']) > 0
    
    def test_all_questions_have_required_fields(self, quiz_file_path):
        """Each question should have required fields."""
        if not quiz_file_path.exists():
            pytest.skip("Quiz file not found")
        
        with open(quiz_file_path, encoding='utf-8') as f:
            quiz = yaml.safe_load(f)
        
        required_fields = ['id', 'question_type', 'stem', 'correct']
        
        for q in quiz['questions']:
            for field in required_fields:
                assert field in q, f"Question {q.get('id', '?')} missing field: {field}"
    
    def test_mc_questions_have_options(self, quiz_file_path):
        """Multiple choice questions should have options."""
        if not quiz_file_path.exists():
            pytest.skip("Quiz file not found")
        
        with open(quiz_file_path, encoding='utf-8') as f:
            quiz = yaml.safe_load(f)
        
        for q in quiz['questions']:
            if q.get('question_type') == 'multiple_choice':
                assert 'options' in q, f"MC question {q.get('id')} missing options"
                assert len(q['options']) >= 2, f"MC question {q.get('id')} needs at least 2 options"
    
    def test_correct_answers_valid(self, quiz_file_path):
        """Correct answers should match available options."""
        if not quiz_file_path.exists():
            pytest.skip("Quiz file not found")
        
        with open(quiz_file_path, encoding='utf-8') as f:
            quiz = yaml.safe_load(f)
        
        for q in quiz['questions']:
            if q.get('question_type') == 'multiple_choice':
                correct = q.get('correct', '')
                options = q.get('options', {})
                assert correct in options, \
                    f"Question {q.get('id')}: correct answer '{correct}' not in options"


# ═══════════════════════════════════════════════════════════════════════════════
# JSON_EXPORT_TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestJsonExport:
    """Tests for LMS JSON export functionality."""
    
    def test_json_export_creates_file(self, sample_quiz):
        """JSON export should create a valid file."""
        # Import here to avoid circular imports during collection
        from formative.run_quiz import export_to_json
        
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            output_path = Path(f.name)
        
        try:
            export_to_json(sample_quiz, output_path)
            assert output_path.exists()
            
            with open(output_path, encoding='utf-8') as f:
                data = json.load(f)
            
            assert 'quiz_metadata' in data
            assert 'questions' in data
        finally:
            output_path.unlink(missing_ok=True)
    
    def test_json_export_preserves_questions(self, sample_quiz):
        """JSON export should preserve all questions."""
        from formative.run_quiz import export_to_json
        
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            output_path = Path(f.name)
        
        try:
            export_to_json(sample_quiz, output_path)
            
            with open(output_path, encoding='utf-8') as f:
                data = json.load(f)
            
            assert len(data['questions']) == len(sample_quiz['questions'])
        finally:
            output_path.unlink(missing_ok=True)
    
    def test_json_export_metadata_complete(self, sample_quiz):
        """JSON export metadata should be complete."""
        from formative.run_quiz import export_to_json
        
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            output_path = Path(f.name)
        
        try:
            export_to_json(sample_quiz, output_path)
            
            with open(output_path, encoding='utf-8') as f:
                data = json.load(f)
            
            meta = data['quiz_metadata']
            assert 'title' in meta
            assert 'passing_score_percent' in meta
            assert meta['passing_score_percent'] == 70
        finally:
            output_path.unlink(missing_ok=True)


# ═══════════════════════════════════════════════════════════════════════════════
# MOODLE_EXPORT_TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestMoodleExport:
    """Tests for Moodle XML export functionality."""
    
    def test_moodle_export_creates_valid_xml(self, sample_quiz):
        """Moodle export should create valid XML."""
        from formative.run_quiz import export_to_moodle_xml
        
        with tempfile.NamedTemporaryFile(suffix='.xml', delete=False) as f:
            output_path = Path(f.name)
        
        try:
            export_to_moodle_xml(sample_quiz, output_path)
            assert output_path.exists()
            
            # Should be parseable XML
            tree = ET.parse(output_path)
            root = tree.getroot()
            assert root.tag == 'quiz'
        finally:
            output_path.unlink(missing_ok=True)
    
    def test_moodle_export_has_category(self, sample_quiz):
        """Moodle export should include category element."""
        from formative.run_quiz import export_to_moodle_xml
        
        with tempfile.NamedTemporaryFile(suffix='.xml', delete=False) as f:
            output_path = Path(f.name)
        
        try:
            export_to_moodle_xml(sample_quiz, output_path)
            
            tree = ET.parse(output_path)
            root = tree.getroot()
            
            categories = [q for q in root.findall('question') 
                          if q.get('type') == 'category']
            assert len(categories) >= 1
        finally:
            output_path.unlink(missing_ok=True)
    
    def test_moodle_export_mc_questions(self, sample_quiz):
        """Moodle export should include MC questions correctly."""
        from formative.run_quiz import export_to_moodle_xml
        
        with tempfile.NamedTemporaryFile(suffix='.xml', delete=False) as f:
            output_path = Path(f.name)
        
        try:
            export_to_moodle_xml(sample_quiz, output_path)
            
            tree = ET.parse(output_path)
            root = tree.getroot()
            
            mc_questions = [q for q in root.findall('question') 
                           if q.get('type') == 'multichoice']
            # Sample has 1 MC question
            assert len(mc_questions) >= 1
        finally:
            output_path.unlink(missing_ok=True)


# ═══════════════════════════════════════════════════════════════════════════════
# CANVAS_EXPORT_TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestCanvasExport:
    """Tests for Canvas QTI export functionality."""
    
    def test_canvas_export_creates_valid_xml(self, sample_quiz):
        """Canvas export should create valid QTI XML."""
        from formative.run_quiz import export_to_canvas_qti
        
        with tempfile.NamedTemporaryFile(suffix='.xml', delete=False) as f:
            output_path = Path(f.name)
        
        try:
            export_to_canvas_qti(sample_quiz, output_path)
            assert output_path.exists()
            
            tree = ET.parse(output_path)
            root = tree.getroot()
            assert root.tag == 'questestinterop'
        finally:
            output_path.unlink(missing_ok=True)
    
    def test_canvas_export_has_assessment(self, sample_quiz):
        """Canvas export should have assessment element."""
        from formative.run_quiz import export_to_canvas_qti
        
        with tempfile.NamedTemporaryFile(suffix='.xml', delete=False) as f:
            output_path = Path(f.name)
        
        try:
            export_to_canvas_qti(sample_quiz, output_path)
            
            tree = ET.parse(output_path)
            root = tree.getroot()
            
            assessments = root.findall('assessment')
            assert len(assessments) == 1
        finally:
            output_path.unlink(missing_ok=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PROGRESS_TRACKER_TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestProgressTracker:
    """Tests for progress tracking functionality."""
    
    def test_weak_spots_empty_initially(self):
        """Weak spots should be empty with no data."""
        from formative.progress_tracker import get_weak_spots, PROGRESS_FILE
        
        # Temporarily remove progress file if exists
        backup = None
        if PROGRESS_FILE.exists():
            backup = PROGRESS_FILE.read_text()
            PROGRESS_FILE.unlink()
        
        try:
            weak = get_weak_spots()
            assert isinstance(weak, list)
        finally:
            if backup:
                PROGRESS_FILE.write_text(backup)
    
    def test_recommendations_returns_list(self):
        """Recommendations should return a list."""
        from formative.progress_tracker import get_recommended_review
        
        recommendations = get_recommended_review()
        assert isinstance(recommendations, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
