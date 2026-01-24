"""
Formative Assessment Module — Week 8: Transport Layer & HTTP

This module provides interactive quizzes for self-assessment of learning objectives.
Designed through brainstorming with Andrei T. and informed by pedagogical principles
from the DPPD module at Universitatea Politehnica București.

Usage:
    python -m formative.run_quiz
    
Or directly:
    python formative/run_quiz.py

Author: ing. dr. Antonio Clim
Course: Computer Networks - ASE, CSIE
"""

from pathlib import Path

__version__ = "1.0.0"
__author__ = "ing. dr. Antonio Clim"

# Module path for locating quiz files
MODULE_PATH = Path(__file__).parent
DEFAULT_QUIZ = MODULE_PATH / "quiz.yaml"
