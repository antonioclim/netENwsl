#!/usr/bin/env python3
"""
Progress Tracker — Week 8 Formative Assessment
==============================================

Tracks student progress across multiple quiz attempts enabling:
- Spaced repetition recommendations
- Identification of persistent weak spots
- Progress visualisation over time

Usage:
    python formative/progress_tracker.py              # Show progress report
    python formative/progress_tracker.py --reset      # Clear all progress
    python formative/progress_tracker.py --export     # Export to CSV

Data stored in: artifacts/quiz_progress.json

Course: Computer Networks — ASE, CSIE

Implements Brown & Wilson Principle 9 (novice support) through
adaptive recommendations based on demonstrated understanding.
"""

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


PROGRESS_FILE = Path(__file__).parent.parent / "artifacts" / "quiz_progress.json"


# ═══════════════════════════════════════════════════════════════════════════════
# DATA_PERSISTENCE
# ═══════════════════════════════════════════════════════════════════════════════

def load_progress() -> dict[str, Any]:
    """Load existing progress or create new tracking file."""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, encoding='utf-8') as f:
            return json.load(f)
    
    return {
        "created": datetime.now().isoformat(),
        "attempts": [],
        "lo_history": {},
        "question_history": {},
    }


def save_progress(progress: dict[str, Any]) -> None:
    """Save progress to JSON file."""
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    progress["last_updated"] = datetime.now().isoformat()
    
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)


# ═══════════════════════════════════════════════════════════════════════════════
# ATTEMPT_RECORDING
# ═══════════════════════════════════════════════════════════════════════════════

def _build_attempt_record(results: dict[str, Any]) -> dict[str, Any]:
    """Build an attempt record from quiz results."""
    return {
        "timestamp": datetime.now().isoformat(),
        "score": results.get("score", 0),
        "total": results.get("total", 0),
        "percentage": results.get("percentage", 0),
        "lo_scores": results.get("lo_scores", {}),
        "wrong_questions": results.get("wrong_questions", []),
        "time_spent_seconds": results.get("time_spent_seconds"),
    }


def _update_lo_history(progress: dict, attempt: dict, results: dict) -> None:
    """Update LO history for trend analysis."""
    for lo, score in results.get("lo_scores", {}).items():
        if lo not in progress["lo_history"]:
            progress["lo_history"][lo] = []
        progress["lo_history"][lo].append({
            "timestamp": attempt["timestamp"],
            "score": score
        })


def _update_question_history(progress: dict, results: dict) -> None:
    """Update question history for difficulty tracking."""
    for qid in results.get("questions_answered", []):
        if qid not in progress["question_history"]:
            progress["question_history"][qid] = {"attempts": 0, "correct": 0}
        progress["question_history"][qid]["attempts"] += 1
        if qid not in results.get("wrong_questions", []):
            progress["question_history"][qid]["correct"] += 1


def record_attempt(results: dict[str, Any]) -> None:
    """
    Record a quiz attempt.
    
    Args:
        results: Dictionary containing score, total, percentage,
                 lo_scores, wrong_questions, questions_answered
    """
    progress = load_progress()
    attempt = _build_attempt_record(results)
    
    progress["attempts"].append(attempt)
    _update_lo_history(progress, attempt, results)
    _update_question_history(progress, results)
    
    save_progress(progress)


# ═══════════════════════════════════════════════════════════════════════════════
# ANALYSIS_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def get_weak_spots(min_attempts: int = 2, threshold: float = 70.0) -> list[str]:
    """
    Identify LOs that consistently score below threshold.
    
    Args:
        min_attempts: Minimum attempts before flagging as weak
        threshold: Score percentage below which LO is considered weak
        
    Returns:
        List of weak LO identifiers
    """
    progress = load_progress()
    weak = []
    
    for lo, history in progress.get("lo_history", {}).items():
        if len(history) >= min_attempts:
            recent = history[-3:]
            avg = sum(h["score"] for h in recent) / len(recent)
            if avg < threshold:
                weak.append(lo)
    
    return weak


def get_difficult_questions(min_attempts: int = 2, threshold: float = 0.5) -> list[str]:
    """
    Identify questions that are frequently answered incorrectly.
    
    Args:
        min_attempts: Minimum attempts before flagging
        threshold: Correct rate below which question is flagged
        
    Returns:
        List of difficult question IDs
    """
    progress = load_progress()
    difficult = []
    
    for qid, stats in progress.get("question_history", {}).items():
        if stats["attempts"] >= min_attempts:
            correct_rate = stats["correct"] / stats["attempts"]
            if correct_rate < threshold:
                difficult.append(qid)
    
    return difficult


def calculate_improvement() -> Optional[float]:
    """Calculate improvement from first to last attempt."""
    progress = load_progress()
    attempts = progress.get("attempts", [])
    
    if len(attempts) < 2:
        return None
    
    return attempts[-1]["percentage"] - attempts[0]["percentage"]


def get_streak() -> int:
    """Get current streak of passing scores (>=70%)."""
    progress = load_progress()
    attempts = progress.get("attempts", [])
    
    streak = 0
    for attempt in reversed(attempts):
        if attempt["percentage"] >= 70:
            streak += 1
        else:
            break
    
    return streak


def get_recommended_review() -> list[str]:
    """Get recommended LOs to review based on weak spots and recency."""
    weak = get_weak_spots()
    progress = load_progress()
    lo_history = progress.get("lo_history", {})
    
    all_los = {"LO1", "LO2", "LO3", "LO4", "LO5", "LO6"}
    never_attempted = all_los - set(lo_history.keys())
    
    recommendations = list(never_attempted) + weak
    return sorted(set(recommendations))


# ═══════════════════════════════════════════════════════════════════════════════
# REPORT_DISPLAY
# ═══════════════════════════════════════════════════════════════════════════════

def _print_report_header(attempts: list) -> None:
    """Print the report header with overview stats."""
    print("\n" + "═" * 70)
    print("📊 QUIZ PROGRESS REPORT — Week 8")
    print("═" * 70)
    
    if not attempts:
        print("\n📝 No quiz attempts recorded yet.")
        print("   Start with: make quiz")
        print("═" * 70 + "\n")
        return
    
    print(f"\n📈 Overview")
    print(f"   Total attempts: {len(attempts)}")
    print(f"   First attempt:  {attempts[0]['timestamp'][:10]}")
    print(f"   Last attempt:   {attempts[-1]['timestamp'][:10]}")


def _print_score_trend(attempts: list) -> None:
    """Print score trend visualisation."""
    scores = [a["percentage"] for a in attempts]
    
    print(f"\n📉 Score Trend")
    recent_scores = scores[-5:]
    trend_visual = " → ".join(f"{s:.0f}%" for s in recent_scores)
    print(f"   Recent: {trend_visual}")
    
    improvement = calculate_improvement()
    if improvement is not None:
        direction = "📈" if improvement > 0 else "📉" if improvement < 0 else "➡️"
        print(f"   Change: {direction} {improvement:+.1f}% (first to last)")
    
    streak = get_streak()
    if streak > 0:
        print(f"   🔥 Current passing streak: {streak} attempts")


def _print_lo_breakdown(lo_history: dict) -> None:
    """Print LO breakdown with visual bars."""
    print(f"\n🎯 Learning Objective Breakdown")
    
    for lo in sorted(lo_history.keys()):
        history = lo_history[lo]
        if history:
            latest = history[-1]["score"]
            filled = int(latest / 10)
            bar = "█" * filled + "░" * (10 - filled)
            status = "✅" if latest >= 70 else "⚠️" if latest >= 50 else "❌"
            print(f"   {lo}: {bar} {latest:.0f}% {status}")


def _print_weak_spots_and_difficult(progress: dict) -> None:
    """Print weak spots and frequently missed questions."""
    weak = get_weak_spots()
    if weak:
        print(f"\n⚠️  Persistent Weak Spots")
        for lo in weak:
            print(f"   • {lo} — Review: docs/learning_objectives.md#{lo.lower()}")
    
    difficult = get_difficult_questions()
    if difficult:
        print(f"\n🔴 Frequently Missed Questions")
        for qid in difficult[:5]:
            stats = progress["question_history"][qid]
            rate = stats["correct"] / stats["attempts"] * 100
            print(f"   • {qid}: {rate:.0f}% correct ({stats['attempts']} attempts)")


def _print_recommendations(scores: list) -> None:
    """Print next steps recommendations."""
    recommendations = get_recommended_review()
    if recommendations:
        print(f"\n📚 Recommended Review")
        for lo in recommendations[:3]:
            print(f"   • {lo}: make quiz-lo LO={lo[-1]}")
    
    print(f"\n📌 Next Steps")
    latest_score = scores[-1] if scores else 0
    
    if latest_score >= 90:
        print("   🌟 Excellent! Ready for homework and advanced exercises.")
        print("   Consider: make quiz-advanced")
    elif latest_score >= 70:
        print("   👍 Good progress! Focus on weak LOs before homework.")
        weak = get_weak_spots()
        if weak:
            print(f"   Try: make quiz-lo LO={weak[0][-1]}")
    else:
        print("   📖 Review theory and try basic questions first.")
        print("   Start with: make quiz-basic")
    
    print("\n" + "═" * 70 + "\n")


def show_progress_report() -> None:
    """Display full progress summary."""
    progress = load_progress()
    attempts = progress.get("attempts", [])
    
    _print_report_header(attempts)
    
    if not attempts:
        return
    
    _print_score_trend(attempts)
    _print_lo_breakdown(progress.get("lo_history", {}))
    _print_weak_spots_and_difficult(progress)
    _print_recommendations([a["percentage"] for a in attempts])


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def export_to_csv(output_path: Path) -> None:
    """Export progress to CSV for external analysis."""
    progress = load_progress()
    attempts = progress.get("attempts", [])
    
    if not attempts:
        print("No data to export.")
        return
    
    all_los = sorted(set(
        lo for a in attempts 
        for lo in a.get("lo_scores", {}).keys()
    ))
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        header = ["timestamp", "score", "total", "percentage"] + all_los
        writer.writerow(header)
        
        for attempt in attempts:
            row = [
                attempt["timestamp"],
                attempt["score"],
                attempt["total"],
                attempt["percentage"],
            ]
            for lo in all_los:
                row.append(attempt.get("lo_scores", {}).get(lo, ""))
            writer.writerow(row)
    
    print(f"✅ Exported {len(attempts)} attempts to {output_path}")


def reset_progress() -> None:
    """Clear all progress data."""
    if PROGRESS_FILE.exists():
        PROGRESS_FILE.unlink()
        print("✅ Progress data cleared.")
    else:
        print("No progress data to clear.")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Main entry point for progress tracker."""
    parser = argparse.ArgumentParser(
        description="Track and analyse quiz progress"
    )
    
    parser.add_argument(
        "--reset", action="store_true",
        help="Clear all progress data"
    )
    parser.add_argument(
        "--export", type=Path, metavar="FILE",
        help="Export progress to CSV file"
    )
    parser.add_argument(
        "--weak", action="store_true",
        help="Show only weak spots"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output raw JSON data"
    )
    
    args = parser.parse_args()
    
    if args.reset:
        confirm = input("⚠️  This will delete all progress. Continue? [y/N]: ")
        if confirm.lower() == 'y':
            reset_progress()
        else:
            print("Cancelled.")
        return 0
    
    if args.export:
        export_to_csv(args.export)
        return 0
    
    if args.weak:
        weak = get_weak_spots()
        if weak:
            print("Weak spots:", ", ".join(weak))
        else:
            print("No weak spots identified (need 2+ attempts)")
        return 0
    
    if args.json:
        progress = load_progress()
        print(json.dumps(progress, indent=2))
        return 0
    
    show_progress_report()
    return 0


if __name__ == "__main__":
    sys.exit(main())
