"""
Anti-Cheat System for Week 10 Laboratory
=========================================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

This module provides environment-bound validation to ensure students
interact with the real laboratory environment rather than using AI
to generate answers.

Components:
    - challenge_generator: Creates unique per-session challenges
    - submission_validator: Validates student submissions
    - fingerprint: Generates environment fingerprints
"""

from .challenge_generator import SessionChallenge
from .submission_validator import SubmissionValidator
from .fingerprint import get_environment_fingerprint

__all__ = [
    'SessionChallenge',
    'SubmissionValidator',
    'get_environment_fingerprint',
]

__version__ = '1.0.0'
