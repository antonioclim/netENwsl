"""
Formative Assessment Tools — Week 12
====================================
Computer Networks - ASE, CSIE | by ing. dr. Antonio Clim

This package provides self-assessment tools for Week 12:
- Interactive quiz runner (run_quiz.py)
- LMS export functionality (export_lms.py)
- Quiz data in YAML and JSON formats

Usage:
    python -m formative.run_quiz
    python -m formative.export_lms --format moodle
    make quiz
"""

__all__ = ["run_quiz", "export_lms"]
__version__ = "2.0.0"
__author__ = "ing. dr. Antonio Clim"
