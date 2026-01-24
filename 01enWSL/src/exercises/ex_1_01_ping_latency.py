#!/usr/bin/env python3
"""
Exercise 1.01: Measuring Latency with Ping
==========================================
Computer Networks - Week 1 (WSL Environment)
ASE Bucharest | by ing. dr. Antonio Clim

Objectives:
- Recall the purpose of ICMP echo requests (ping)
- Explain the difference between latency and bandwidth
- Demonstrate RTT measurement using the ping command

Prerequisites:
- Network connectivity (loopback always available)
- ping command available (standard on Linux)

Level: Beginner
Estimated time: 10 minutes

Pair Programming Notes:
- Driver: Write the ping command and observe output
- Navigator: Predict RTT values before execution
- Swap after: Running ping on different hosts

Examples
--------
python3 src/exercises/ex_1_01_ping_latency.py --host 127.0.0.1 --count 3
python3 src/exercises/ex_1_01_ping_latency.py --host 8.8.8.8 --count 5
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════════
# DATA_STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class PingResult:
    """
    Immutable container for ping statistics.
    
    Attributes:
        host: Target hostname or IP address
        transmitted: Number of ICMP echo requests sent
        received: Number of ICMP echo replies received
        avg_rtt_ms: Average round-trip time in milliseconds (None if no replies)
    """
    host: str
    transmitted: int
    received: int
    avg_rtt_ms: Optional[float]


# ═══════════════════════════════════════════════════════════════════════════════
# PREDICTION_PROMPT
# ═══════════════════════════════════════════════════════════════════════════════
def prompt_prediction(host: str, count: int) -> None:
    """
    Ask student to predict outcome before execution (Brown & Wilson Principle 4).
    
    This helps build intuition about network behaviour.
    """
    print("\n" + "=" * 60)
    print("💭 PREDICTION TIME")
    print("=" * 60)
    print(f"You are about to ping {host} with {count} packets.")
    print()
    print("Before running, predict:")
    print(f"  1. Will all {count} packets be received? (yes/no)")
    print("  2. What RTT do you expect? (e.g., <1ms, 10-50ms, >100ms)")
    print()
    
    if host in ("127.0.0.1", "localhost"):
        print("Hint: This is the loopback address (your own machine).")
    elif host.startswith("172.") or host.startswith("192.168.") or host.startswith("10."):
        print("Hint: This is a private/local network address.")
    else:
        print("Hint: This appears to be an external address.")
    
    print("=" * 60)
    input("Press Enter to continue...")
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_PING
# ═══════════════════════════════════════════════════════════════════════════════
def run_ping(host: str, count: int, timeout_s: int) -> str:
    """
    Execute the ping command and capture output.
    
    Args:
        host: Target hostname or IP address
        count: Number of ICMP echo requests to send
        timeout_s: Timeout in seconds for each packet
        
    Returns:
        Combined stdout and stderr from ping command
    """
    cmd = ["ping", "-n", "-c", str(count), "-W", str(timeout_s), host]
    proc = subprocess.run(cmd, text=True, capture_output=True)
    return proc.stdout + proc.stderr


# ═══════════════════════════════════════════════════════════════════════════════
# PARSE_OUTPUT
# ═══════════════════════════════════════════════════════════════════════════════
def parse_ping(output: str, host: str, count: int) -> PingResult:
    """
    Parse ping output to extract statistics.
    
    Handles the standard Linux ping output format:
    "X packets transmitted, Y received, Z% packet loss"
    "rtt min/avg/max/mdev = A/B/C/D ms"
    
    Args:
        output: Raw ping command output
        host: Original target (for result object)
        count: Original count (fallback if parsing fails)
        
    Returns:
        PingResult with extracted statistics
    """
    transmitted = count
    received = 0
    avg = None

    # Extract packet counts
    m = re.search(r"(\d+) packets transmitted, (\d+) received", output)
    if m:
        transmitted = int(m.group(1))
        received = int(m.group(2))

    # Extract average RTT (second value in min/avg/max/mdev)
    m = re.search(r"rtt min/avg/max/mdev = [^/]+/([^/]+)/", output)
    if m:
        try:
            avg = float(m.group(1))
        except ValueError:
            avg = None

    return PingResult(host=host, transmitted=transmitted, received=received, avg_rtt_ms=avg)


# ═══════════════════════════════════════════════════════════════════════════════
# OUTPUT_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def display_results(result: PingResult) -> None:
    """
    Display ping results with interpretation.
    
    Args:
        result: Parsed ping statistics
    """
    avg_txt = f"{result.avg_rtt_ms:.3f} ms" if result.avg_rtt_ms is not None else "n/a"
    loss_pct = 100 * (1 - result.received / result.transmitted) if result.transmitted > 0 else 100
    
    print(f"PING host={result.host} tx={result.transmitted} rx={result.received} avg_rtt={avg_txt}")
    print()
    
    # Interpretation
    print("📊 INTERPRETATION:")
    if result.received == 0:
        print("  ❌ No replies received - host may be unreachable or blocking ICMP")
    elif result.received < result.transmitted:
        print(f"  ⚠️  Packet loss detected: {loss_pct:.1f}%")
    else:
        print("  ✅ All packets received successfully")
    
    if result.avg_rtt_ms is not None:
        if result.avg_rtt_ms < 1:
            print("  ⚡ Very low latency - likely local/loopback connection")
        elif result.avg_rtt_ms < 50:
            print("  🟢 Good latency - typical for local network or nearby servers")
        elif result.avg_rtt_ms < 150:
            print("  🟡 Moderate latency - typical for distant servers")
        else:
            print("  🔴 High latency - may indicate network congestion or distant server")


# ═══════════════════════════════════════════════════════════════════════════════
# PARSE_ARGUMENTS
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    ap = argparse.ArgumentParser(
        description="Run ping and report basic latency statistics.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 ex_1_01_ping_latency.py --host 127.0.0.1 --count 5
  python3 ex_1_01_ping_latency.py --host 8.8.8.8 --count 3
  python3 ex_1_01_ping_latency.py --host google.com --no-predict
        """
    )
    ap.add_argument("--host", default="127.0.0.1", 
                    help="Target host or IP address (default: 127.0.0.1)")
    ap.add_argument("--count", type=int, default=4, 
                    help="Number of ICMP echo requests (default: 4)")
    ap.add_argument("--timeout-s", type=int, default=2, 
                    help="Per-packet timeout in seconds (default: 2)")
    ap.add_argument("--no-predict", action="store_true",
                    help="Skip the prediction prompt")
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
    
    # Prediction prompt (pedagogical feature)
    if not args.no_predict:
        prompt_prediction(args.host, args.count)
    
    # Execute ping
    print(f"Running: ping -c {args.count} {args.host}")
    print("-" * 40)
    output = run_ping(args.host, args.count, args.timeout_s)
    
    # Parse and display results
    result = parse_ping(output, args.host, args.count)
    display_results(result)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
