#!/usr/bin/env python3
"""
Exercise Verification Tests
NETWORKING class - ASE, Informatics | by Revolvix

Tests to verify laboratory exercises complete successfully.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import subprocess
import sys
import time
import unittest
import argparse
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))



# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
def run_in_container(container: str, command: str, timeout: int = 30) -> subprocess.CompletedProcess:
    """Execute a command in a Docker container."""
    return subprocess.run(
        ["docker", "exec", container, "bash", "-c", command],
        capture_output=True,
        text=True,
        timeout=timeout
    )



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class TestExercise1Broadcast(unittest.TestCase):
    """Test Exercise 1: UDP Broadcast."""


# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_broadcast_sender_runs(self):
        """Broadcast sender should execute without errors."""
        result = run_in_container(
            "week3_client",
            "python3 /app/src/exercises/ex_3_01_udp_broadcast.py send "
            "--dst 255.255.255.255 --port 5007 --count 1"
        )
        self.assertEqual(
            result.returncode, 0,
            f"Broadcast sender failed: {result.stderr}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_broadcast_receiver_help(self):
        """Broadcast receiver should show help without errors."""
        result = run_in_container(
            "week3_client",
            "python3 /app/src/exercises/ex_3_01_udp_broadcast.py recv --help"
        )
        self.assertEqual(
            result.returncode, 0,
            f"Broadcast receiver help failed: {result.stderr}"
        )



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class TestExercise2Multicast(unittest.TestCase):
    """Test Exercise 2: UDP Multicast."""


# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_multicast_sender_runs(self):
        """Multicast sender should execute without errors."""
        result = run_in_container(
            "week3_client",
            "python3 /app/src/exercises/ex_3_02_udp_multicast.py send "
            "--group 239.1.1.1 --port 5008 --count 1"
        )
        self.assertEqual(
            result.returncode, 0,
            f"Multicast sender failed: {result.stderr}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_multicast_receiver_help(self):
        """Multicast receiver should show help without errors."""
        result = run_in_container(
            "week3_client",
            "python3 /app/src/exercises/ex_3_02_udp_multicast.py recv --help"
        )
        self.assertEqual(
            result.returncode, 0,
            f"Multicast receiver help failed: {result.stderr}"
        )



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class TestExercise3TcpTunnel(unittest.TestCase):
    """Test Exercise 3: TCP Tunnel."""


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_tunnel_help(self):
        """TCP tunnel should show help without errors."""
        result = run_in_container(
            "week3_client",
            "python3 /app/src/exercises/ex_3_03_tcp_tunnel.py --help"
        )
        self.assertEqual(
            result.returncode, 0,
            f"TCP tunnel help failed: {result.stderr}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_echo_through_tunnel(self):
        """Echo should work through the tunnel."""
        result = run_in_container(
            "week3_client",
            "echo 'TUNNEL_TEST' | nc -w 2 router 9090"
        )
        self.assertEqual(
            result.returncode, 0,
            f"Echo through tunnel failed: {result.stderr}"
        )
        self.assertIn(
            "TUNNEL_TEST",
            result.stdout,
            "Expected echo response not received"
        )


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
    def test_direct_echo(self):
        """Echo should work directly to server."""
        result = run_in_container(
            "week3_client",
            "echo 'DIRECT_TEST' | nc -w 2 server 8080"
        )
        self.assertEqual(
            result.returncode, 0,
            f"Direct echo failed: {result.stderr}"
        )
        self.assertIn(
            "DIRECT_TEST",
            result.stdout,
            "Expected echo response not received"
        )



# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
def run_specific_exercise(exercise_num: int) -> bool:
    """Run tests for a specific exercise."""
    test_classes = {
        1: TestExercise1Broadcast,
        2: TestExercise2Multicast,
        3: TestExercise3TcpTunnel,
    }
    
    if exercise_num not in test_classes:
        print(f"Unknown exercise: {exercise_num}")
        return False
    
    suite = unittest.TestLoader().loadTestsFromTestCase(test_classes[exercise_num])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run exercise verification tests"
    )
    parser.add_argument(
        "--exercise", "-e", type=int, choices=[1, 2, 3],
        help="Run tests for specific exercise only"
    )
    args = parser.parse_args()

    if args.exercise:
        success = run_specific_exercise(args.exercise)
        return 0 if success else 1
    else:
        # Run all tests
        loader = unittest.TestLoader()
        suite = loader.discover(
            start_dir=str(Path(__file__).parent),
            pattern="test_exercises.py"
        )
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
