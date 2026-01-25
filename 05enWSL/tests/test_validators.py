#!/usr/bin/env python3
"""
Validator Tests — Week 5
========================
Tests for quiz schema and Parsons problems validation.

Run: pytest tests/test_validators.py -v
"""

import json
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


class TestQuizYAMLSchema(unittest.TestCase):
    """Validate quiz.yaml structure and content."""
    
    @unittest.skipUnless(YAML_AVAILABLE, "PyYAML not installed")
    def setUp(self):
        """Load quiz YAML."""
        quiz_path = PROJECT_ROOT / 'formative' / 'quiz.yaml'
        if quiz_path.exists():
            with open(quiz_path, 'r', encoding='utf-8') as f:
                self.quiz = yaml.safe_load(f)
        else:
            self.quiz = None
    
    def test_quiz_file_exists(self):
        """Quiz YAML file should exist."""
        quiz_path = PROJECT_ROOT / 'formative' / 'quiz.yaml'
        self.assertTrue(quiz_path.exists(), "formative/quiz.yaml not found")
    
    def test_has_metadata_section(self):
        """Quiz should have metadata section."""
        if not self.quiz:
            self.skipTest("Quiz not loaded")
        self.assertIn('metadata', self.quiz)
    
    def test_metadata_fields(self):
        """Metadata should have required fields."""
        if not self.quiz:
            self.skipTest("Quiz not loaded")
        meta = self.quiz.get('metadata', {})
        required = ['week', 'topic', 'passing_score', 'learning_objectives']
        for field in required:
            self.assertIn(field, meta, f"Metadata missing: {field}")
    
    def test_has_questions(self):
        """Quiz should have questions list."""
        if not self.quiz:
            self.skipTest("Quiz not loaded")
        self.assertIn('questions', self.quiz)
        self.assertIsInstance(self.quiz['questions'], list)
    
    def test_question_required_fields(self):
        """Each question must have required fields."""
        if not self.quiz:
            self.skipTest("Quiz not loaded")
        required = ['id', 'type', 'stem', 'correct', 'points', 'bloom_level', 'lo_ref']
        for q in self.quiz.get('questions', []):
            for field in required:
                self.assertIn(field, q, f"Question {q.get('id', '?')} missing: {field}")
    
    def test_bloom_coverage(self):
        """Quiz should cover multiple Bloom levels."""
        if not self.quiz:
            self.skipTest("Quiz not loaded")
        levels = set()
        for q in self.quiz.get('questions', []):
            levels.add(q.get('bloom_level', ''))
        
        # Should have at least 4 different levels
        self.assertGreaterEqual(len(levels), 4, 
            f"Only {len(levels)} Bloom levels covered: {levels}")
    
    def test_lo_coverage(self):
        """Quiz should reference all learning objectives."""
        if not self.quiz:
            self.skipTest("Quiz not loaded")
        
        # Get defined LOs
        defined_los = set()
        for lo in self.quiz.get('metadata', {}).get('learning_objectives', []):
            defined_los.add(lo.get('id', ''))
        
        # Get referenced LOs
        referenced_los = set()
        for q in self.quiz.get('questions', []):
            referenced_los.add(q.get('lo_ref', ''))
        
        # All defined LOs should be referenced
        missing = defined_los - referenced_los
        self.assertEqual(len(missing), 0, 
            f"LOs defined but not referenced: {missing}")
    
    def test_no_oxford_commas(self):
        """Quiz text should not contain Oxford commas."""
        if not self.quiz:
            self.skipTest("Quiz not loaded")
        
        import re
        pattern = re.compile(r',\s+and\s+')
        
        violations = []
        for q in self.quiz.get('questions', []):
            stem = q.get('stem', '')
            if pattern.search(stem):
                violations.append(q.get('id', '?'))
        
        self.assertEqual(len(violations), 0, 
            f"Oxford commas found in questions: {violations}")
    
    def test_points_positive(self):
        """All questions should have positive points."""
        if not self.quiz:
            self.skipTest("Quiz not loaded")
        for q in self.quiz.get('questions', []):
            self.assertGreater(q.get('points', 0), 0,
                f"Question {q.get('id', '?')} has non-positive points")


class TestParsonsJSONSchema(unittest.TestCase):
    """Validate Parsons problems JSON structure."""
    
    def setUp(self):
        """Load Parsons problems JSON."""
        parsons_path = PROJECT_ROOT / 'formative' / 'parsons' / 'problems.json'
        if parsons_path.exists():
            with open(parsons_path, 'r', encoding='utf-8') as f:
                self.problems = json.load(f)
        else:
            self.problems = None
    
    def test_parsons_file_exists(self):
        """Parsons JSON file should exist."""
        parsons_path = PROJECT_ROOT / 'formative' / 'parsons' / 'problems.json'
        self.assertTrue(parsons_path.exists(), 
            "formative/parsons/problems.json not found")
    
    def test_has_problems_list(self):
        """JSON should contain problems array."""
        if not self.problems:
            self.skipTest("Problems not loaded")
        self.assertIn('problems', self.problems)
        self.assertIsInstance(self.problems['problems'], list)
    
    def test_problem_structure(self):
        """Each problem should have required fields."""
        if not self.problems:
            self.skipTest("Problems not loaded")
        required = ['id', 'title', 'blocks', 'solution']
        for p in self.problems.get('problems', []):
            for field in required:
                self.assertIn(field, p, 
                    f"Problem {p.get('id', '?')} missing: {field}")
    
    def test_has_distractors(self):
        """Problems should include distractor blocks."""
        if not self.problems:
            self.skipTest("Problems not loaded")
        
        problems_with_distractors = 0
        for p in self.problems.get('problems', []):
            blocks = p.get('blocks', [])
            distractors = [b for b in blocks if b.get('distractor', False)]
            if distractors:
                problems_with_distractors += 1
        
        # At least half should have distractors
        total = len(self.problems.get('problems', []))
        self.assertGreaterEqual(problems_with_distractors, total // 2,
            "Most problems should include distractor blocks")
    
    def test_solution_uses_valid_blocks(self):
        """Solution should only reference valid block IDs."""
        if not self.problems:
            self.skipTest("Problems not loaded")
        
        for p in self.problems.get('problems', []):
            block_ids = {b.get('id') for b in p.get('blocks', [])}
            solution_ids = set(p.get('solution', []))
            
            invalid = solution_ids - block_ids
            self.assertEqual(len(invalid), 0,
                f"Problem {p.get('id', '?')} solution references invalid blocks: {invalid}")


class TestMisconceptionAnchors(unittest.TestCase):
    """Validate misconception document anchors."""
    
    def test_misconceptions_file_exists(self):
        """Misconceptions markdown should exist."""
        path = PROJECT_ROOT / 'docs' / 'misconceptions.md'
        self.assertTrue(path.exists())
    
    def test_anchor_format(self):
        """Misconceptions should have valid anchor IDs."""
        path = PROJECT_ROOT / 'docs' / 'misconceptions.md'
        if not path.exists():
            self.skipTest("File not found")
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        import re
        anchors = re.findall(r'\{#(misconception-\d+)\}', content)
        
        # Should have numbered anchors
        self.assertGreater(len(anchors), 5, 
            f"Expected at least 6 misconception anchors, found {len(anchors)}")
        
        # Check sequential numbering
        for i, anchor in enumerate(anchors):
            expected = f"misconception-{i}"
            self.assertEqual(anchor, expected,
                f"Anchor {i} should be {expected}, got {anchor}")


if __name__ == '__main__':
    unittest.main()
