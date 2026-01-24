#!/usr/bin/env python3
"""
Exercise 1.03: Parsing tshark CSV Output
========================================
Computer Networks - Week 1 (WSL Environment)
ASE Bucharest | by ing. dr. Antonio Clim

Objectives:
- Apply CSV parsing techniques to network data
- Analyse packet captures programmatically
- Demonstrate data aggregation with Python collections

Prerequisites:
- Python 3.11+ with csv module (standard library)
- Optional: CSV file exported from tshark

Level: Beginner
Estimated time: 10 minutes

Pair Programming Notes:
- Driver: Write the CSV parsing logic
- Navigator: Predict what protocol numbers mean (hint: 1=ICMP, 6=TCP, 17=UDP)
- Swap after: Parsing complete, before aggregation

If no input is provided, a small built-in sample is analysed.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable, Optional


# ═══════════════════════════════════════════════════════════════════════════════
# SAMPLE_DATA
# ═══════════════════════════════════════════════════════════════════════════════
# Built-in sample for testing without actual capture file
SAMPLE_ROWS = [
    {"frame.number": "1", "ip.src": "10.0.1.11", "ip.dst": "10.0.1.12", "ip.proto": "1"},
    {"frame.number": "2", "ip.src": "10.0.1.11", "ip.dst": "10.0.1.12", "ip.proto": "1"},
    {"frame.number": "3", "ip.src": "10.0.1.12", "ip.dst": "10.0.1.11", "ip.proto": "6"},
]

# Protocol number to name mapping (subset of IANA assignments)
PROTO_NAMES = {
    "1": "ICMP",
    "6": "TCP",
    "17": "UDP",
    "47": "GRE",
    "50": "ESP",
}


# ═══════════════════════════════════════════════════════════════════════════════
# PREDICTION_PROMPT
# ═══════════════════════════════════════════════════════════════════════════════
def prompt_prediction(input_path: Optional[Path]) -> None:
    """
    Ask student to predict CSV analysis results (Brown & Wilson Principle 4).
    """
    print("\n" + "=" * 60)
    print("💭 PREDICTION: CSV ANALYSIS")
    print("=" * 60)
    
    if input_path is None:
        print("Using built-in sample data (3 rows):")
        print("  - 2 packets from 10.0.1.11 → 10.0.1.12 (proto 1)")
        print("  - 1 packet from 10.0.1.12 → 10.0.1.11 (proto 6)")
        print()
        print("Predict:")
        print("  1. What protocol is proto=1? (TCP / UDP / ICMP)")
        print("  2. What protocol is proto=6? (TCP / UDP / ICMP)")
        print("  3. Which IP will be the 'top source'?")
    else:
        print(f"Analysing file: {input_path}")
        print()
        print("Predict:")
        print("  1. How many rows do you expect?")
        print("  2. What protocols do you expect to see?")
    
    print("=" * 60)
    input("Press Enter to continue...")
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# READ_INPUT
# ═══════════════════════════════════════════════════════════════════════════════
def read_rows(path: Optional[Path]) -> Iterable[dict[str, str]]:
    """
    Read packet data from CSV file or return sample data.
    
    Args:
        path: Path to CSV file, or None to use sample data
        
    Returns:
        Iterable of dictionaries (one per row)
    """
    if path is None:
        return SAMPLE_ROWS
    
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


# ═══════════════════════════════════════════════════════════════════════════════
# ANALYSE_DATA
# ═══════════════════════════════════════════════════════════════════════════════
def analyse_packets(rows: list[dict[str, str]]) -> dict:
    """
    Compute statistics from packet data.
    
    Args:
        rows: List of packet metadata dictionaries
        
    Returns:
        Dictionary with analysis results
    """
    if not rows:
        return {"count": 0, "protocols": {}, "top_source": None}
    
    # Count protocols
    proto_counts = Counter(row.get("ip.proto", "?") for row in rows)
    
    # Count source IPs
    src_counts = Counter(row.get("ip.src", "?") for row in rows)
    
    # Identify top source
    top_source = src_counts.most_common(1)[0] if src_counts else (None, 0)
    
    return {
        "count": len(rows),
        "protocols": dict(proto_counts),
        "sources": dict(src_counts),
        "top_source": top_source,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# OUTPUT_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def display_results(analysis: dict) -> None:
    """
    Display analysis results with interpretation.
    """
    print("\n" + "=" * 60)
    print("📊 CSV ANALYSIS RESULTS")
    print("=" * 60)
    
    print(f"  Total packets: {analysis['count']}")
    print()
    
    # Protocol breakdown
    print("  Protocols:")
    for proto, count in sorted(analysis["protocols"].items()):
        name = PROTO_NAMES.get(proto, "Unknown")
        print(f"    {proto} ({name}): {count} packets")
    print()
    
    # Top sources
    print("  Top sources:")
    for src, count in sorted(analysis["sources"].items(), key=lambda x: -x[1])[:3]:
        print(f"    {src}: {count} packets")
    print()
    
    if analysis["top_source"]:
        ip, count = analysis["top_source"]
        print(f"  🏆 Most active source: {ip} ({count} packets)")
    
    print("=" * 60)


# ═══════════════════════════════════════════════════════════════════════════════
# PARSE_ARGUMENTS
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    ap = argparse.ArgumentParser(
        description="Parse a CSV with packet metadata and print basic counts.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 ex_1_03_parse_csv.py
  python3 ex_1_03_parse_csv.py --input artifacts/capture_analysis.csv
  python3 ex_1_03_parse_csv.py --no-predict
        """
    )
    ap.add_argument("--input", type=Path, default=None, 
                    help="Path to a CSV file exported from tshark")
    ap.add_argument("--no-predict", action="store_true",
                    help="Skip prediction prompt")
    return ap.parse_args()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """
    Main entry point.
    
    Returns:
        Exit code (0 for success)
    """
    args = parse_args()
    
    # Prediction prompt
    if not args.no_predict:
        prompt_prediction(args.input)
    
    # Read data
    source = args.input if args.input else "built-in sample"
    print(f"Reading from: {source}")
    rows = list(read_rows(args.input))
    
    if not rows:
        print("CSV rows=0")
        return 0
    
    # Analyse
    analysis = analyse_packets(rows)
    
    # Display
    display_results(analysis)
    
    # Legacy format for test compatibility
    proto_counts = analysis["protocols"]
    top_src = analysis["top_source"][0] if analysis["top_source"] else "?"
    print(f"\nCSV rows={len(rows)} protos={proto_counts} top_src={top_src}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
