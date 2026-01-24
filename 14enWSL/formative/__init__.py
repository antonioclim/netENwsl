"""
Formative Assessment Module — Week 14 Lab Kit
NETWORKING class — ASE, CSIE | Computer Networks Laboratory
by ing. dr. Antonio Clim

This module provides formative assessment tools for self-evaluation:
- Interactive quiz runner (run_quiz.py)
- Quiz data in YAML and JSON formats
- Export utilities for LMS integration

Usage:
    from formative import run_quiz
    run_quiz.main()
    
    # Or from command line:
    python -m formative.run_quiz
    python formative/run_quiz.py
    make quiz
"""

__version__ = "1.0.0"
__author__ = "ing. dr. Antonio Clim"
# Contact: Open an issue on GitHub

from pathlib import Path

# Module paths
MODULE_DIR = Path(__file__).parent
QUIZ_YAML = MODULE_DIR / "quiz_week14.yaml"
QUIZ_JSON = MODULE_DIR / "quiz_week14.json"


def get_quiz_path(format: str = "yaml") -> Path:
    """Get path to quiz file in specified format.
    
    Args:
        format: Quiz format - 'yaml' or 'json'
        
    Returns:
        Path to quiz file
        
    Raises:
        ValueError: If format not supported
    """
    if format.lower() == "yaml":
        return QUIZ_YAML
    elif format.lower() == "json":
        return QUIZ_JSON
    else:
        raise ValueError(f"Unsupported format: {format}. Use 'yaml' or 'json'.")


__all__ = [
    "__version__",
    "__author__",
    "get_quiz_path",
    "QUIZ_YAML",
    "QUIZ_JSON",
]
