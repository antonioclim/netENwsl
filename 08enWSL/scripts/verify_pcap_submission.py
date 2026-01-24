#!/usr/bin/env python3
"""
PCAP Submission Verifier — Week 8 Laboratory
=============================================

Validates that submitted PCAP files:
1. Exist and are recent (within 72 hours)
2. Contain traffic to the student's unique port
3. Show the expected patterns (handshake, HTTP, load balancing)

Usage:
    make verify-pcap
    
    Or directly:
    python scripts/verify_pcap_submission.py

Prerequisites:
    - Student context must be generated first (make init ID=...)
    - tshark (Wireshark CLI) for deep analysis (optional but recommended)

Course: Computer Networks — ASE, CSIE
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


class PcapVerifier:
    """Verifies PCAP submissions against student context."""
    
    def __init__(self, context_path: Path):
        """Initialise with student context."""
        if not context_path.exists():
            raise FileNotFoundError(
                f"Student context not found: {context_path}\n"
                "Run: make init ID=your_student_id"
            )
        
        with open(context_path, encoding='utf-8') as f:
            self.context = json.load(f)
        
        self.student_id = self.context.get("student_id", "unknown")
        self.tshark_available = self._check_tshark()
        self.errors: list[str] = []
        self.warnings: list[str] = []
    
    def _check_tshark(self) -> bool:
        """Check if tshark is available for deep analysis."""
        try:
            result = subprocess.run(
                ["tshark", "--version"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def verify_file_exists(self, pcap_path: Path) -> bool:
        """Check if PCAP file exists."""
        if not pcap_path.exists():
            self.errors.append(f"File not found: {pcap_path}")
            return False
        return True
    
    def verify_file_recent(self, pcap_path: Path, max_hours: int = 72) -> bool:
        """Check if PCAP file was created recently."""
        if not pcap_path.exists():
            return False
        
        mtime = datetime.fromtimestamp(pcap_path.stat().st_mtime)
        age = datetime.now() - mtime
        
        if age > timedelta(hours=max_hours):
            self.errors.append(
                f"PCAP too old: {pcap_path.name}\n"
                f"   Modified: {mtime.strftime('%Y-%m-%d %H:%M')}\n"
                f"   Age: {age.days} days, {age.seconds // 3600} hours\n"
                f"   Required: Within {max_hours} hours of submission"
            )
            return False
        
        return True
    
    def verify_file_size(self, pcap_path: Path, min_bytes: int = 500) -> bool:
        """Check if PCAP file has meaningful content."""
        if not pcap_path.exists():
            return False
        
        size = pcap_path.stat().st_size
        if size < min_bytes:
            self.errors.append(
                f"PCAP too small: {pcap_path.name} ({size} bytes)\n"
                f"   Expected: At least {min_bytes} bytes\n"
                f"   This suggests empty or incomplete capture."
            )
            return False
        
        return True
    
    def verify_contains_port(self, pcap_path: Path, port: int) -> Optional[bool]:
        """Check if PCAP contains traffic to specific port (requires tshark)."""
        if not self.tshark_available:
            self.warnings.append(
                f"Cannot verify port {port} in {pcap_path.name} — tshark not available"
            )
            return None
        
        try:
            result = subprocess.run(
                [
                    "tshark", "-r", str(pcap_path),
                    "-Y", f"tcp.port == {port}",
                    "-T", "fields", "-e", "frame.number"
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            frames = [f for f in result.stdout.strip().split('\n') if f]
            
            if not frames:
                self.errors.append(
                    f"No traffic to port {port} found in {pcap_path.name}\n"
                    f"   Your unique port is {port} — did you capture from the right interface?"
                )
                return False
            
            return True
            
        except subprocess.TimeoutExpired:
            self.warnings.append(f"PCAP analysis timed out: {pcap_path.name}")
            return None
    
    def verify_handshake(self, pcap_path: Path) -> Optional[bool]:
        """Verify PCAP contains TCP handshake (SYN, SYN-ACK, ACK)."""
        if not self.tshark_available:
            self.warnings.append(
                f"Cannot verify handshake in {pcap_path.name} — tshark not available"
            )
            return None
        
        try:
            # Check for SYN packets
            result = subprocess.run(
                [
                    "tshark", "-r", str(pcap_path),
                    "-Y", "tcp.flags.syn == 1 and tcp.flags.ack == 0",
                    "-T", "fields", "-e", "frame.number"
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            syn_count = len([f for f in result.stdout.strip().split('\n') if f])
            
            if syn_count < 1:
                self.errors.append(
                    f"No TCP SYN packets found in {pcap_path.name}\n"
                    f"   A handshake capture must show connection establishment."
                )
                return False
            
            # Check for SYN-ACK packets
            result = subprocess.run(
                [
                    "tshark", "-r", str(pcap_path),
                    "-Y", "tcp.flags.syn == 1 and tcp.flags.ack == 1",
                    "-T", "fields", "-e", "frame.number"
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            synack_count = len([f for f in result.stdout.strip().split('\n') if f])
            
            if synack_count < 1:
                self.errors.append(
                    f"No TCP SYN-ACK packets found in {pcap_path.name}\n"
                    f"   Did the server respond? Check if your server was running."
                )
                return False
            
            return True
            
        except subprocess.TimeoutExpired:
            self.warnings.append(f"Handshake analysis timed out: {pcap_path.name}")
            return None
    
    def verify_http_traffic(self, pcap_path: Path) -> Optional[bool]:
        """Verify PCAP contains HTTP traffic."""
        if not self.tshark_available:
            self.warnings.append(
                f"Cannot verify HTTP traffic in {pcap_path.name} — tshark not available"
            )
            return None
        
        try:
            result = subprocess.run(
                [
                    "tshark", "-r", str(pcap_path),
                    "-Y", "http",
                    "-T", "fields", "-e", "frame.number"
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            frames = [f for f in result.stdout.strip().split('\n') if f]
            
            if len(frames) < 2:  # At least request + response
                self.errors.append(
                    f"Insufficient HTTP traffic in {pcap_path.name}\n"
                    f"   Found: {len(frames)} HTTP frames\n"
                    f"   Expected: At least request + response (2+ frames)"
                )
                return False
            
            return True
            
        except subprocess.TimeoutExpired:
            self.warnings.append(f"HTTP analysis timed out: {pcap_path.name}")
            return None
    
    def verify_all(self) -> bool:
        """Run all verifications for required captures."""
        print("\n" + "=" * 70)
        print(f"🔍 PCAP SUBMISSION VERIFICATION")
        print(f"   Student: {self.student_id}")
        print("=" * 70)
        
        if not self.tshark_available:
            print("\n⚠️  tshark not available — deep analysis will be skipped")
            print("   Install Wireshark for full verification\n")
        
        all_passed = True
        captures = self.context.get("required_captures", {})
        unique_port = self.context.get("http_server", {}).get("port", 8080)
        
        for capture_name, capture_info in captures.items():
            print(f"\n📁 Verifying: {capture_name}")
            print(f"   File: {capture_info['filename']}")
            
            pcap_path = Path(capture_info['filename'])
            capture_passed = True
            
            # Basic checks
            if not self.verify_file_exists(pcap_path):
                capture_passed = False
            elif not self.verify_file_recent(pcap_path):
                capture_passed = False
            elif not self.verify_file_size(pcap_path):
                capture_passed = False
            else:
                # Deep analysis based on capture type
                if capture_name == "handshake":
                    port_result = self.verify_contains_port(pcap_path, unique_port)
                    hs_result = self.verify_handshake(pcap_path)
                    if port_result is False or hs_result is False:
                        capture_passed = False
                
                elif capture_name == "http_exchange":
                    http_result = self.verify_http_traffic(pcap_path)
                    if http_result is False:
                        capture_passed = False
                
                elif capture_name == "load_balance":
                    # For load balance just check it has substantial content
                    min_packets = capture_info.get("min_packets", 30)
                    if not self.verify_file_size(pcap_path, min_bytes=min_packets * 100):
                        capture_passed = False
            
            if capture_passed:
                print(f"   ✅ PASSED")
            else:
                print(f"   ❌ FAILED")
                all_passed = False
        
        # Print summary
        print("\n" + "=" * 70)
        
        if self.errors:
            print("\n❌ ERRORS:")
            for err in self.errors:
                for line in err.split('\n'):
                    print(f"   {line}")
        
        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for warn in self.warnings:
                print(f"   {warn}")
        
        print("\n" + "=" * 70)
        if all_passed and not self.errors:
            print("✅ ALL PCAP VERIFICATIONS PASSED")
            print("   Your captures are ready for submission.")
        else:
            print("❌ SOME VERIFICATIONS FAILED")
            print("   Fix the issues above before submitting.")
        print("=" * 70 + "\n")
        
        return all_passed and not self.errors


def main() -> int:
    """Main entry point."""
    context_path = Path("artifacts/student_context.json")
    
    try:
        verifier = PcapVerifier(context_path)
        success = verifier.verify_all()
        return 0 if success else 1
    
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\nRun this first:")
        print("  make init ID=your_student_id\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
