#!/usr/bin/env python3
"""
Week 2 Demonstration Script
NETWORKING class - ASE, CSIE Bucharest | by ing. dr. Antonio Clim

Automated demonstrations showcasing TCP and UDP socket programming.
Suitable for classroom presentation on projector.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import argparse
import subprocess
import sys
import time
import threading
from pathlib import Path
from typing import Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.logger import setup_logger
from scripts.utils.network_utils import NetworkUtils

logger = setup_logger("run_demo")



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class DemoRunner:
    """Orchestrates demonstration scenarios."""
    

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
    def __init__(self, project_root: Path):
        self.root = project_root
        self.src = project_root / "src" / "exercises"
        self.tcp_script = self.src / "ex_2_01_tcp.py"
        self.udp_script = self.src / "ex_2_02_udp.py"
        self.server_proc: Optional[subprocess.Popen] = None
    

# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
    def _run_python(self, script: Path, args: list, background: bool = False):
        """Run a Python script."""
        cmd = [sys.executable, str(script)] + args
        
        if background:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            return proc
        else:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result
    

# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
    def _print_section(self, title: str) -> None:
        """Print section header."""
        print()
        print("─" * 60)
        print(f"  {title}")
        print("─" * 60)
        print()
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def _wait_and_show(self, seconds: float, message: str = "") -> None:
        """Wait with optional message."""
        if message:
            print(f"  ⏳ {message}")
        time.sleep(seconds)
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def demo_tcp_comparison(self) -> bool:
        """
        Demo 1: TCP/UDP Comparison
        Shows the fundamental differences between TCP and UDP.
        """
        self._print_section("Demo 1: TCP vs UDP Comparison")
        
        try:
            # Start TCP server
            print("  [1] Starting TCP server on port 9090...")
            tcp_server = self._run_python(
                self.tcp_script,
                ["server", "--port", "9090", "--mode", "threaded"],
                background=True
            )
            self._wait_and_show(1, "Server initialising...")
            
            # Send TCP messages
            print("\n  [2] Sending TCP messages:")
            for i, msg in enumerate(["Hello", "World", "Test"], 1):
                result = self._run_python(
                    self.tcp_script,
                    ["client", "--host", "127.0.0.1", "--port", "9090", "-m", msg]
                )
                print(f"      Message {i}: {msg}")
                if result.stdout:
                    for line in result.stdout.strip().split('\n'):
                        print(f"        {line}")
                time.sleep(0.3)
            
            # Stop TCP server
            tcp_server.terminate()
            tcp_server.wait(timeout=2)
            
            print("\n  [3] TCP Observations:")
            print("      • Connection established before data transfer")
            print("      • Three-way handshake: SYN → SYN-ACK → ACK")
            print("      • Each message acknowledged by server")
            print("      • Connection closed gracefully: FIN → FIN-ACK → ACK")
            
            self._wait_and_show(2)
            
            # Start UDP server
            print("\n  [4] Starting UDP server on port 9091...")
            udp_server = self._run_python(
                self.udp_script,
                ["server", "--port", "9091"],
                background=True
            )
            self._wait_and_show(1, "Server initialising...")
            
            # Send UDP messages
            print("\n  [5] Sending UDP messages:")
            for cmd in ["ping", "upper:hello", "time"]:
                result = self._run_python(
                    self.udp_script,
                    ["client", "--host", "127.0.0.1", "--port", "9091", "-o", cmd]
                )
                print(f"      Command: {cmd}")
                if result.stdout:
                    for line in result.stdout.strip().split('\n'):
                        print(f"        {line}")
                time.sleep(0.3)
            
            # Stop UDP server
            udp_server.terminate()
            udp_server.wait(timeout=2)
            
            print("\n  [6] UDP Observations:")
            print("      • No connection establishment")
            print("      • Each message is independent (datagram)")
            print("      • No acknowledgements or retransmission")
            print("      • Lower latency, but no delivery guarantee")
            
            self._print_section("Summary: TCP vs UDP")
            print("  ┌────────────────┬──────────────────┬──────────────────┐")
            print("  │ Characteristic │ TCP              │ UDP              │")
            print("  ├────────────────┼──────────────────┼──────────────────┤")
            print("  │ Connection     │ Required         │ Not required     │")
            print("  │ Reliability    │ Guaranteed       │ Best effort      │")
            print("  │ Ordering       │ Preserved        │ Not guaranteed   │")
            print("  │ Overhead       │ 20+ byte header  │ 8 byte header    │")
            print("  │ Use case       │ Web, Email, FTP  │ DNS, VoIP, Games │")
            print("  └────────────────┴──────────────────┴──────────────────┘")
            
            return True
            
        except Exception as e:
            logger.error(f"Demo failed: {e}")
            return False
    

# ═══════════════════════════════════════════════════════════════════════════════
# NETWORK_OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════════
    def demo_concurrent_connections(self) -> bool:
        """
        Demo 2: Concurrent Connection Handling
        Shows how threaded server handles multiple simultaneous connections.
        """
        self._print_section("Demo 2: Concurrent Connection Handling")
        
        try:
            # Start threaded server
            print("  [1] Starting threaded TCP server...")
            server = self._run_python(
                self.tcp_script,
                ["server", "--port", "9090", "--mode", "threaded"],
                background=True
            )
            self._wait_and_show(1)
            
            # Run load test
            print("\n  [2] Launching 10 concurrent clients...")
            result = self._run_python(
                self.tcp_script,
                ["load", "--host", "127.0.0.1", "--port", "9090", 
                 "--clients", "10", "--stagger-ms", "0"]
            )
            
            print("\n  Client results:")
            if result.stdout:
                for line in result.stdout.strip().split('\n')[-5:]:
                    print(f"    {line}")
            
            server.terminate()
            server.wait(timeout=2)
            
            print("\n  [3] Key observations:")
            print("      • Each client gets its own worker thread")
            print("      • Requests processed in parallel, not sequentially")
            print("      • Server remains responsive during load")
            
            self._wait_and_show(2)
            
            # Compare with iterative
            print("\n  [4] Now comparing with iterative (single-threaded) server...")
            server = self._run_python(
                self.tcp_script,
                ["server", "--port", "9090", "--mode", "iterative"],
                background=True
            )
            self._wait_and_show(1)
            
            print("\n  [5] Launching 5 concurrent clients to iterative server...")
            result = self._run_python(
                self.tcp_script,
                ["load", "--host", "127.0.0.1", "--port", "9090",
                 "--clients", "5", "--stagger-ms", "0"]
            )
            
            print("\n  Client results:")
            if result.stdout:
                for line in result.stdout.strip().split('\n')[-5:]:
                    print(f"    {line}")
            
            server.terminate()
            server.wait(timeout=2)
            
            print("\n  [6] Observation:")
            print("      • Iterative server handles one client at a time")
            print("      • Other clients must wait in queue")
            print("      • Total time is sum of individual request times")
            
            return True
            
        except Exception as e:
            logger.error(f"Demo failed: {e}")
            return False



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run Week 2 Demonstrations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available demonstrations:
  1 - TCP vs UDP Comparison
  2 - Concurrent Connection Handling
  
Examples:
  python scripts/run_demo.py --demo 1
  python scripts/run_demo.py --demo 2
  python scripts/run_demo.py --all
        """
    )
    parser.add_argument(
        "--demo", "-d",
        type=int,
        choices=[1, 2],
        help="Run specific demonstration (1 or 2)"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Run all demonstrations"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List available demonstrations"
    )
    
    args = parser.parse_args()
    
    if args.list:
        print("\nAvailable demonstrations:")
        print("  1 - TCP vs UDP Comparison")
        print("      Shows fundamental differences between protocols")
        print("  2 - Concurrent Connection Handling")
        print("      Demonstrates threaded vs iterative servers")
        return 0
    
    if not args.demo and not args.all:
        parser.print_help()
        return 0
    
    runner = DemoRunner(PROJECT_ROOT)
    
    print()
    print("=" * 60)
    print("  Week 2: Socket Programming Demonstrations")
    print("  NETWORKING class - ASE, CSIE Bucharest")
    print("=" * 60)
    
    success = True
    
    if args.all or args.demo == 1:
        success = runner.demo_tcp_comparison() and success
    
    if args.all or args.demo == 2:
        success = runner.demo_concurrent_connections() and success
    
    print()
    print("=" * 60)
    print("  Demonstration complete!")
    print("=" * 60)
    print()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
