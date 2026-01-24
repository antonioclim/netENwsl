#!/usr/bin/env python3
"""
Progress Tracker — Learning Objectives Progress Tracking
=========================================================
Computer Networks — ASE, CSIE | by ing. dr. Antonio Clim

Tracks student progress through the laboratory exercises and learning objectives.
Progress is stored locally and can be viewed or reset.

Usage:
    python formative/progress_tracker.py              # Show current progress
    python formative/progress_tracker.py --reset      # Reset all progress
    python formative/progress_tracker.py --export     # Export to JSON
    python formative/progress_tracker.py --lo LO1     # Show LO1 details

The tracker monitors:
    - Exercise completions
    - Quiz attempts and scores
    - Learning Objective coverage
    - Time spent (estimated)
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
PROGRESS_FILE = Path.home() / ".week10_progress.json"

LEARNING_OBJECTIVES = {
    "LO1": {
        "description": "Explain the role of TLS certificates in HTTPS communication",
        "bloom_level": "Understand",
        "required_activities": ["ex_10_01", "quiz_lo1"],
        "optional_activities": ["hw_10_01"]
    },
    "LO2": {
        "description": "Compare REST API designs across Richardson Maturity Model levels",
        "bloom_level": "Analyse",
        "required_activities": ["ex_10_02", "quiz_lo2"],
        "optional_activities": ["hw_10_02"]
    },
    "LO3": {
        "description": "Analyse DNS query and response structure",
        "bloom_level": "Analyse",
        "required_activities": ["ex_10_03", "quiz_lo3"],
        "optional_activities": ["hw_10_03"]
    },
    "LO4": {
        "description": "Implement basic clients for HTTP, DNS, SSH and FTP protocols",
        "bloom_level": "Apply",
        "required_activities": ["ex_10_04", "quiz_lo4"],
        "optional_activities": []
    },
    "LO5": {
        "description": "Evaluate security differences between encrypted and unencrypted protocols",
        "bloom_level": "Evaluate",
        "required_activities": ["quiz_lo5"],
        "optional_activities": ["hw_10_01"]
    }
}


# ═══════════════════════════════════════════════════════════════════════════════
# DATA_CLASSES
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass
class ActivityRecord:
    """Record of a completed activity."""
    activity_id: str
    completed_at: str
    duration_minutes: Optional[int] = None
    score: Optional[float] = None
    notes: Optional[str] = None


@dataclass 
class ProgressData:
    """Complete progress data structure."""
    student_id: Optional[str] = None
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_activity: Optional[str] = None
    exercises: Dict[str, ActivityRecord] = field(default_factory=dict)
    quiz_attempts: List[Dict[str, Any]] = field(default_factory=list)
    lo_progress: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    total_time_minutes: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialisation."""
        return {
            "student_id": self.student_id,
            "started_at": self.started_at,
            "last_activity": self.last_activity,
            "exercises": {
                k: {
                    "activity_id": v.activity_id,
                    "completed_at": v.completed_at,
                    "duration_minutes": v.duration_minutes,
                    "score": v.score,
                    "notes": v.notes
                }
                for k, v in self.exercises.items()
            },
            "quiz_attempts": self.quiz_attempts,
            "lo_progress": self.lo_progress,
            "total_time_minutes": self.total_time_minutes
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProgressData":
        """Create from dictionary."""
        progress = cls(
            student_id=data.get("student_id"),
            started_at=data.get("started_at", datetime.now().isoformat()),
            last_activity=data.get("last_activity"),
            quiz_attempts=data.get("quiz_attempts", []),
            lo_progress=data.get("lo_progress", {}),
            total_time_minutes=data.get("total_time_minutes", 0)
        )
        
        for ex_id, ex_data in data.get("exercises", {}).items():
            progress.exercises[ex_id] = ActivityRecord(
                activity_id=ex_data.get("activity_id", ex_id),
                completed_at=ex_data.get("completed_at", ""),
                duration_minutes=ex_data.get("duration_minutes"),
                score=ex_data.get("score"),
                notes=ex_data.get("notes")
            )
        
        return progress


# ═══════════════════════════════════════════════════════════════════════════════
# PROGRESS_TRACKER
# ═══════════════════════════════════════════════════════════════════════════════
class ProgressTracker:
    """
    Tracks learning progress through Week 10 laboratory.
    
    Monitors exercise completions, quiz scores and learning objective coverage.
    Progress is persisted to a local JSON file.
    """
    
    def __init__(self, progress_file: Path = PROGRESS_FILE):
        """
        Initialise the progress tracker.
        
        Args:
            progress_file: Path to the progress JSON file
        """
        self.progress_file = progress_file
        self.data = self._load()
    
    def _load(self) -> ProgressData:
        """Load progress from file or create new."""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    return ProgressData.from_dict(json.load(f))
            except (json.JSONDecodeError, IOError, KeyError):
                pass
        
        return ProgressData()
    
    def _save(self) -> None:
        """Save progress to file."""
        self.data.last_activity = datetime.now().isoformat()
        
        try:
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(self.data.to_dict(), f, indent=2)
        except IOError as e:
            print(f"[WARNING] Could not save progress: {e}")
    
    def set_student_id(self, student_id: str) -> None:
        """Set the student identifier."""
        self.data.student_id = student_id
        self._save()
    
    def mark_exercise_complete(
        self,
        exercise_id: str,
        lo_refs: List[str],
        duration_minutes: Optional[int] = None,
        score: Optional[float] = None
    ) -> None:
        """
        Mark an exercise as completed.
        
        Args:
            exercise_id: Identifier for the exercise (e.g. "ex_10_01")
            lo_refs: Learning objectives covered by this exercise
            duration_minutes: Time spent on the exercise
            score: Score achieved (0-100)
        """
        self.data.exercises[exercise_id] = ActivityRecord(
            activity_id=exercise_id,
            completed_at=datetime.now().isoformat(),
            duration_minutes=duration_minutes,
            score=score
        )
        
        if duration_minutes:
            self.data.total_time_minutes += duration_minutes
        
        # Update LO progress
        for lo in lo_refs:
            if lo not in self.data.lo_progress:
                self.data.lo_progress[lo] = {
                    "completed_activities": [],
                    "quiz_scores": []
                }
            
            if exercise_id not in self.data.lo_progress[lo]["completed_activities"]:
                self.data.lo_progress[lo]["completed_activities"].append(exercise_id)
        
        self._save()
    
    def record_quiz_attempt(
        self,
        score: float,
        total_questions: int,
        lo_scores: Dict[str, float]
    ) -> None:
        """
        Record a quiz attempt.
        
        Args:
            score: Points earned
            total_questions: Total questions answered
            lo_scores: Scores per learning objective
        """
        attempt = {
            "timestamp": datetime.now().isoformat(),
            "score": score,
            "total": total_questions,
            "percentage": (score / total_questions * 100) if total_questions > 0 else 0,
            "lo_scores": lo_scores
        }
        
        self.data.quiz_attempts.append(attempt)
        
        # Update LO progress with quiz scores
        for lo, lo_score in lo_scores.items():
            if lo not in self.data.lo_progress:
                self.data.lo_progress[lo] = {
                    "completed_activities": [],
                    "quiz_scores": []
                }
            
            self.data.lo_progress[lo]["quiz_scores"].append(lo_score)
            
            # Mark quiz activity as complete if score >= 70%
            quiz_activity = f"quiz_{lo.lower()}"
            if lo_score >= 70 and quiz_activity not in self.data.lo_progress[lo]["completed_activities"]:
                self.data.lo_progress[lo]["completed_activities"].append(quiz_activity)
        
        self._save()
    
    def get_lo_status(self, lo_id: str) -> Dict[str, Any]:
        """
        Get the status of a specific learning objective.
        
        Args:
            lo_id: Learning objective identifier (e.g. "LO1")
            
        Returns:
            Dictionary with LO status details
        """
        lo_def = LEARNING_OBJECTIVES.get(lo_id, {})
        lo_progress = self.data.lo_progress.get(lo_id, {
            "completed_activities": [],
            "quiz_scores": []
        })
        
        required = set(lo_def.get("required_activities", []))
        completed = set(lo_progress.get("completed_activities", []))
        
        required_done = required & completed
        required_missing = required - completed
        
        quiz_scores = lo_progress.get("quiz_scores", [])
        best_quiz = max(quiz_scores) if quiz_scores else 0
        
        is_complete = len(required_missing) == 0
        
        return {
            "id": lo_id,
            "description": lo_def.get("description", ""),
            "bloom_level": lo_def.get("bloom_level", ""),
            "is_complete": is_complete,
            "required_done": list(required_done),
            "required_missing": list(required_missing),
            "optional_done": list(completed - required),
            "quiz_attempts": len(quiz_scores),
            "best_quiz_score": best_quiz
        }
    
    def get_overall_progress(self) -> Dict[str, Any]:
        """
        Get overall progress summary.
        
        Returns:
            Dictionary with overall progress statistics
        """
        lo_statuses = [self.get_lo_status(lo) for lo in LEARNING_OBJECTIVES]
        
        complete_count = sum(1 for s in lo_statuses if s["is_complete"])
        total_los = len(LEARNING_OBJECTIVES)
        
        exercise_count = len(self.data.exercises)
        quiz_count = len(self.data.quiz_attempts)
        
        best_quiz = max(
            (a["percentage"] for a in self.data.quiz_attempts),
            default=0
        )
        
        return {
            "student_id": self.data.student_id,
            "started_at": self.data.started_at,
            "last_activity": self.data.last_activity,
            "los_complete": complete_count,
            "los_total": total_los,
            "completion_percentage": (complete_count / total_los * 100) if total_los > 0 else 0,
            "exercises_completed": exercise_count,
            "quiz_attempts": quiz_count,
            "best_quiz_score": best_quiz,
            "total_time_minutes": self.data.total_time_minutes,
            "lo_details": lo_statuses
        }
    
    def reset(self) -> None:
        """Reset all progress data."""
        self.data = ProgressData()
        self._save()
        print("[OK] Progress reset")
    
    def export_json(self, output_path: Path) -> None:
        """Export progress to a JSON file."""
        progress = self.get_overall_progress()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(progress, f, indent=2)
        
        print(f"[OK] Progress exported to: {output_path}")
    
    def print_summary(self) -> None:
        """Print a formatted progress summary."""
        progress = self.get_overall_progress()
        
        # Header
        print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  WEEK 10 PROGRESS TRACKER                                                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Student ID:     {(progress['student_id'] or 'Not set'):<59} ║
║  Started:        {progress['started_at'][:19]:<59} ║
║  Total Time:     {progress['total_time_minutes']} minutes                                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  OVERALL PROGRESS                                                             ║
║                                                                              ║""")
        
        # Progress bar
        pct = progress['completion_percentage']
        bar_filled = int(pct / 5)
        bar = "█" * bar_filled + "░" * (20 - bar_filled)
        print(f"║    [{bar}] {pct:.0f}%                        ║")
        
        print(f"""║                                                                              ║
║    Learning Objectives: {progress['los_complete']}/{progress['los_total']} complete                                      ║
║    Exercises Completed: {progress['exercises_completed']:<52} ║
║    Quiz Attempts:       {progress['quiz_attempts']:<52} ║
║    Best Quiz Score:     {progress['best_quiz_score']:.1f}%                                             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  LEARNING OBJECTIVES                                                          ║
║                                                                              ║""")
        
        # LO details
        for lo in progress['lo_details']:
            status = "✅" if lo['is_complete'] else "🔄"
            quiz_info = f"Quiz: {lo['best_quiz_score']:.0f}%" if lo['quiz_attempts'] > 0 else "No quiz"
            
            desc = lo['description'][:45] + "..." if len(lo['description']) > 45 else lo['description']
            print(f"║    {status} {lo['id']}: {desc:<48} ║")
            print(f"║         {quiz_info:<64} ║")
            
            if lo['required_missing']:
                missing = ", ".join(lo['required_missing'][:3])
                print(f"║         Missing: {missing:<55} ║")
        
        print("""║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")


# ═══════════════════════════════════════════════════════════════════════════════
# COMMAND_LINE_INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Week 10 Progress Tracker",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("--reset", action="store_true",
                       help="Reset all progress")
    parser.add_argument("--export", type=Path, default=None,
                       metavar="FILE", help="Export progress to JSON file")
    parser.add_argument("--lo", type=str, default=None,
                       help="Show details for specific LO (e.g. LO1)")
    parser.add_argument("--student-id", type=str, default=None,
                       help="Set student ID")
    parser.add_argument("--mark-complete", type=str, default=None,
                       metavar="EXERCISE", help="Mark an exercise as complete")
    parser.add_argument("--lo-refs", type=str, default=None,
                       help="LO references for marked exercise (comma-separated)")
    
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point."""
    args = parse_args(argv)
    tracker = ProgressTracker()
    
    if args.reset:
        confirm = input("Reset all progress? (yes/no): ")
        if confirm.lower() == "yes":
            tracker.reset()
        else:
            print("[CANCELLED] Progress not reset")
        return 0
    
    if args.student_id:
        tracker.set_student_id(args.student_id)
        print(f"[OK] Student ID set to: {args.student_id}")
    
    if args.mark_complete:
        lo_refs = args.lo_refs.split(",") if args.lo_refs else []
        tracker.mark_exercise_complete(args.mark_complete, lo_refs)
        print(f"[OK] Marked {args.mark_complete} as complete")
        return 0
    
    if args.export:
        tracker.export_json(args.export)
        return 0
    
    if args.lo:
        status = tracker.get_lo_status(args.lo.upper())
        print(f"\n{args.lo.upper()}: {status['description']}")
        print(f"Bloom Level: {status['bloom_level']}")
        print(f"Status: {'Complete ✅' if status['is_complete'] else 'In Progress 🔄'}")
        print(f"Required Done: {', '.join(status['required_done']) or 'None'}")
        print(f"Required Missing: {', '.join(status['required_missing']) or 'None'}")
        print(f"Best Quiz Score: {status['best_quiz_score']:.1f}%")
        return 0
    
    # Default: show summary
    tracker.print_summary()
    return 0


if __name__ == "__main__":
    sys.exit(main())
