#!/usr/bin/env python3
"""
Exercise 1.04: PCAP Statistics
==============================
Computer Networks - Week 1 (WSL Environment)
ASE Bucharest | by ing. dr. Antonio Clim

Objectives:
- Apply programmatic PCAP analysis using Python
- Analyse captured traffic to identify protocols
- Demonstrate packet counting and statistics

Prerequisites:
- Python 3.11+ with scapy or dpkt installed
- A PCAP file from previous capture exercises

Level: Intermediate
Estimated time: 15 minutes

Pair Programming Notes:
- Driver: Write the packet parsing logic
- Navigator: Predict protocol distribution based on the capture scenario
- Swap after: Parsing complete, before displaying results

This script supports two backends:
- scapy (preferred, if installed)
- dpkt (fallback)

Examples
--------
python3 src/exercises/ex_1_04_pcap_stats.py --pcap pcap/ex4_capture.pcap
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Optional


# ═══════════════════════════════════════════════════════════════════════════════
# PREDICTION_PROMPT
# ═══════════════════════════════════════════════════════════════════════════════
def prompt_prediction(pcap_path: Path) -> None:
    """
    Ask student to predict PCAP statistics (Brown & Wilson Principle 4).
    """
    print("\n" + "=" * 60)
    print("💭 PREDICTION: PCAP ANALYSIS")
    print("=" * 60)
    print(f"You are about to analyse: {pcap_path}")
    print()
    print("Before running, predict:")
    print("  1. How many packets do you expect?")
    print("  2. What protocols do you expect? (TCP / UDP / ICMP)")
    print("  3. If you captured a TCP connection, what's the minimum")
    print("     packet count? (Hint: handshake + data + teardown)")
    print()
    print("Protocol reminder:")
    print("  - TCP handshake = 3 packets (SYN, SYN-ACK, ACK)")
    print("  - TCP teardown = 4 packets (FIN-ACK x2)")
    print("  - ICMP ping = 2 packets per request (echo + reply)")
    print("=" * 60)
    input("Press Enter to continue...")
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# SCAPY_BACKEND
# ═══════════════════════════════════════════════════════════════════════════════
def stats_with_scapy(path: Path) -> dict[str, Any]:
    """
    Parse PCAP using Scapy library.
    
    Scapy provides high-level packet dissection with easy
    layer access via haslayer() method.
    
    Args:
        path: Path to PCAP file
        
    Returns:
        Dictionary with packets, bytes and protocol counts
    """
    from scapy.all import rdpcap  # type: ignore

    pkts = rdpcap(str(path))
    proto = Counter()
    total_bytes = 0

    for p in pkts:
        total_bytes += len(p)
        if p.haslayer("ICMP"):
            proto["ICMP"] += 1
        elif p.haslayer("TCP"):
            proto["TCP"] += 1
        elif p.haslayer("UDP"):
            proto["UDP"] += 1
        else:
            proto["OTHER"] += 1

    return {"packets": len(pkts), "bytes": total_bytes, "protocols": dict(proto)}


# ═══════════════════════════════════════════════════════════════════════════════
# DPKT_BACKEND
# ═══════════════════════════════════════════════════════════════════════════════
def stats_with_dpkt(path: Path) -> dict[str, Any]:
    """
    Parse PCAP using dpkt library (fallback).
    
    dpkt is lower-level but doesn't require libpcap.
    
    Args:
        path: Path to PCAP file
        
    Returns:
        Dictionary with packets, bytes and protocol counts
    """
    import dpkt  # type: ignore

    proto = Counter()
    total_bytes = 0
    packets = 0

    with path.open("rb") as f:
        pcap = dpkt.pcap.Reader(f)
        for _ts, buf in pcap:
            packets += 1
            total_bytes += len(buf)
            try:
                eth = dpkt.ethernet.Ethernet(buf)
                ip = eth.data
                if isinstance(ip, dpkt.ip.IP):
                    if ip.p == dpkt.ip.IP_PROTO_ICMP:
                        proto["ICMP"] += 1
                    elif ip.p == dpkt.ip.IP_PROTO_TCP:
                        proto["TCP"] += 1
                    elif ip.p == dpkt.ip.IP_PROTO_UDP:
                        proto["UDP"] += 1
                    else:
                        proto["IP_OTHER"] += 1
                else:
                    proto["NON_IP"] += 1
            except Exception:
                proto["PARSE_ERROR"] += 1

    return {"packets": packets, "bytes": total_bytes, "protocols": dict(proto)}


# ═══════════════════════════════════════════════════════════════════════════════
# OUTPUT_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def display_results(stats: dict[str, Any], backend: str) -> None:
    """
    Display PCAP statistics with interpretation.
    """
    print("\n" + "=" * 60)
    print("📊 PCAP ANALYSIS RESULTS")
    print("=" * 60)
    print(f"  Backend used: {backend}")
    print(f"  Total packets: {stats['packets']}")
    print(f"  Total bytes: {stats['bytes']}")
    print()
    
    # Protocol breakdown
    print("  Protocol distribution:")
    total_proto = sum(stats['protocols'].values())
    for proto, count in sorted(stats['protocols'].items(), key=lambda x: -x[1]):
        pct = 100 * count / total_proto if total_proto > 0 else 0
        bar = "█" * int(pct / 5)
        print(f"    {proto:10s}: {count:4d} ({pct:5.1f}%) {bar}")
    print()
    
    # Interpretation hints
    if stats['packets'] > 0:
        avg_size = stats['bytes'] / stats['packets']
        print(f"  📏 Average packet size: {avg_size:.1f} bytes")
        
        if 'TCP' in stats['protocols']:
            tcp_count = stats['protocols']['TCP']
            if tcp_count >= 7:
                print("  💡 Enough TCP packets for a complete connection (3 handshake + data + 4 teardown)")
            elif tcp_count >= 3:
                print("  💡 TCP packets present - likely includes handshake")
    
    print("=" * 60)


# ═══════════════════════════════════════════════════════════════════════════════
# PARSE_ARGUMENTS
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    ap = argparse.ArgumentParser(
        description="Compute basic statistics from a PCAP file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 ex_1_04_pcap_stats.py --pcap pcap/ex4_capture.pcap
  python3 ex_1_04_pcap_stats.py --pcap demo.pcap --backend scapy
  python3 ex_1_04_pcap_stats.py --pcap demo.pcap --no-predict
        """
    )
    ap.add_argument("--pcap", type=Path, required=True, 
                    help="Path to a PCAP file")
    ap.add_argument("--backend", choices=["auto", "scapy", "dpkt"], default="auto", 
                    help="Parser backend (default: auto)")
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
        Exit code (0 for success, 1 for failure)
    """
    args = parse_args()

    # Verify file exists
    if not args.pcap.exists():
        print(f"❌ PCAP file not found: {args.pcap}")
        return 1
    
    # Prediction prompt
    if not args.no_predict:
        prompt_prediction(args.pcap)

    # Select backend
    backend = args.backend
    if backend == "auto":
        try:
            import scapy  # type: ignore  # noqa: F401
            backend = "scapy"
        except ImportError:
            backend = "dpkt"
    
    print(f"Analysing {args.pcap} with {backend}...")
    
    # Parse and analyse
    try:
        if backend == "scapy":
            stats = stats_with_scapy(args.pcap)
        else:
            stats = stats_with_dpkt(args.pcap)
    except ImportError as e:
        print(f"❌ Required library not installed: {e}")
        print("Install with: pip install scapy --break-system-packages")
        return 1
    
    # Display results
    display_results(stats, backend)
    
    # Legacy format for test compatibility
    print(f"\nPCAP packets={stats['packets']} bytes={stats['bytes']} protocols={stats['protocols']}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
