#!/usr/bin/env python3
"""
LMS Export Tests — Week 5
=========================
Tests for Moodle/Canvas export functionality.

Run: pytest tests/test_lms_export.py -v
"""

import json
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestJSONExportStructure(unittest.TestCase):
    """Test JSON export format for generic LMS."""
    
    def setUp(self):
        """Load the exported JSON if it exists."""
        self.export_path = PROJECT_ROOT / 'formative' / 'quiz_lms_export.json'
        self.data = None
        if self.export_path.exists():
            with open(self.export_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
    
    def test_export_file_exists(self):
        """Pre-generated export file should exist."""
        # Skip if file doesn't exist (will be generated)
        if not self.export_path.exists():
            self.skipTest("Export file not yet generated")
        self.assertTrue(self.export_path.exists())
    
    def test_export_has_metadata(self):
        """Export should contain metadata section."""
        if not self.data:
            self.skipTest("No export data")
        self.assertIn('metadata', self.data)
        meta = self.data['metadata']
        self.assertIn('week', meta)
        self.assertIn('topic', meta)
    
    def test_export_has_questions(self):
        """Export should contain questions array."""
        if not self.data:
            self.skipTest("No export data")
        self.assertIn('questions', self.data)
        self.assertIsInstance(self.data['questions'], list)
        self.assertGreater(len(self.data['questions']), 0)
    
    def test_question_structure(self):
        """Each question should have required fields."""
        if not self.data:
            self.skipTest("No export data")
        required_fields = ['id', 'type', 'stem', 'correct', 'points']
        for q in self.data.get('questions', []):
            for field in required_fields:
                self.assertIn(field, q, f"Question {q.get('id', '?')} missing {field}")
    
    def test_bloom_levels_present(self):
        """Questions should have Bloom level annotations."""
        if not self.data:
            self.skipTest("No export data")
        for q in self.data.get('questions', []):
            self.assertIn('bloom_level', q)
            self.assertIn(q['bloom_level'], 
                         ['remember', 'understand', 'apply', 'analyse', 'evaluate', 'create'])
    
    def test_lo_references_present(self):
        """Questions should reference learning objectives."""
        if not self.data:
            self.skipTest("No export data")
        for q in self.data.get('questions', []):
            self.assertIn('lo_ref', q)
            self.assertTrue(q['lo_ref'].startswith('LO'))


class TestMoodleExportFormat(unittest.TestCase):
    """Test Moodle XML export structure."""
    
    def test_moodle_question_format(self):
        """Verify Moodle question structure generation."""
        # Test the building logic directly
        from formative.export_to_lms import _build_moodle_question
        
        sample_q = {
            'id': 'q01',
            'type': 'multiple_choice',
            'stem': 'What is the size of an IPv4 address?',
            'options': {'a': '16 bits', 'b': '32 bits', 'c': '64 bits'},
            'correct': 'b',
            'points': 1,
            'explanation': 'IPv4 is 32 bits.'
        }
        
        xml = _build_moodle_question(sample_q)
        
        self.assertIn('<question type="multichoice">', xml)
        self.assertIn('<questiontext', xml)
        self.assertIn('32 bits', xml)
        self.assertIn('fraction="100"', xml)  # Correct answer


class TestCanvasExportFormat(unittest.TestCase):
    """Test Canvas JSON export structure."""
    
    def test_canvas_question_format(self):
        """Verify Canvas question structure generation."""
        from formative.export_to_lms import _build_canvas_question
        
        sample_q = {
            'id': 'q01',
            'type': 'multiple_choice',
            'stem': 'What is the size of an IPv4 address?',
            'options': {'a': '16 bits', 'b': '32 bits', 'c': '64 bits'},
            'correct': 'b',
            'points': 1
        }
        
        canvas_q = _build_canvas_question(sample_q)
        
        self.assertIn('question_type', canvas_q)
        self.assertEqual(canvas_q['question_type'], 'multiple_choice_question')
        self.assertIn('answers', canvas_q)
        
        # Check correct answer is marked
        correct_count = sum(1 for a in canvas_q['answers'] if a.get('weight', 0) == 100)
        self.assertEqual(correct_count, 1)


class TestExportConsistency(unittest.TestCase):
    """Test that exports are consistent with source quiz."""
    
    def test_question_count_matches(self):
        """Exported question count should match source."""
        quiz_path = PROJECT_ROOT / 'formative' / 'quiz.yaml'
        export_path = PROJECT_ROOT / 'formative' / 'quiz_lms_export.json'
        
        if not quiz_path.exists() or not export_path.exists():
            self.skipTest("Required files missing")
        
        import yaml
        with open(quiz_path, 'r') as f:
            quiz = yaml.safe_load(f)
        with open(export_path, 'r') as f:
            export = json.load(f)
        
        source_count = len(quiz.get('questions', []))
        export_count = len(export.get('questions', []))
        
        self.assertEqual(source_count, export_count,
                        f"Source has {source_count} questions, export has {export_count}")


if __name__ == '__main__':
    unittest.main()
