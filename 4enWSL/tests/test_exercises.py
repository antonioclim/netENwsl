#!/usr/bin/env python3
"""
Exercise Verification Tests
NETWORKING class - ASE, Informatics | by Revolvix

Verifies that laboratory exercises are working correctly.
"""

import sys
import socket
import struct
import zlib
import time
import threading
import unittest
import argparse
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestTextProtocol(unittest.TestCase):
    """Tests for TEXT protocol implementation."""
    
    HOST = 'localhost'
    PORT = 5400
    
    def send_command(self, command: str) -> str:
        """Send a command and receive response."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        
        try:
            sock.connect((self.HOST, self.PORT))
            
            # Format: length space payload
            payload = command.encode('utf-8')
            message = f"{len(payload)} {command}".encode('utf-8')
            sock.sendall(message)
            
            response = sock.recv(4096).decode('utf-8')
            return response.strip()
        finally:
            sock.close()
    
    def test_ping(self):
        """PING command should return pong."""
        try:
            response = self.send_command("PING")
            self.assertIn("pong", response.lower())
        except ConnectionRefusedError:
            self.skipTest("TEXT server not running")
    
    def test_set_get(self):
        """SET and GET commands should work."""
        try:
            # Set a value
            response = self.send_command("SET testkey testvalue")
            self.assertIn("OK", response)
            
            # Get the value
            response = self.send_command("GET testkey")
            self.assertIn("testvalue", response)
        except ConnectionRefusedError:
            self.skipTest("TEXT server not running")
    
    def test_count(self):
        """COUNT command should return number of keys."""
        try:
            response = self.send_command("COUNT")
            self.assertIn("OK", response)
        except ConnectionRefusedError:
            self.skipTest("TEXT server not running")


class TestBinaryProtocol(unittest.TestCase):
    """Tests for BINARY protocol implementation."""
    
    HOST = 'localhost'
    PORT = 5401
    
    MAGIC = b'NP'
    VERSION = 1
    
    MSG_ECHO_REQ = 1
    MSG_ECHO_RESP = 2
    MSG_PUT_REQ = 3
    MSG_PUT_RESP = 4
    MSG_GET_REQ = 5
    MSG_GET_RESP = 6
    
    def build_message(self, msg_type: int, payload: bytes, seq: int = 1) -> bytes:
        """Build a binary protocol message."""
        # Header: magic(2) + version(1) + type(1) + payload_len(2) + seq(4) + crc(4)
        header_without_crc = struct.pack(
            '>2sBBHI',
            self.MAGIC,
            self.VERSION,
            msg_type,
            len(payload),
            seq
        )
        
        # Calculate CRC over header (without CRC) + payload
        data_for_crc = header_without_crc + payload
        crc = zlib.crc32(data_for_crc) & 0xFFFFFFFF
        
        return header_without_crc + struct.pack('>I', crc) + payload
    
    def send_message(self, msg: bytes) -> bytes:
        """Send a message and receive response."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        
        try:
            sock.connect((self.HOST, self.PORT))
            sock.sendall(msg)
            response = sock.recv(4096)
            return response
        finally:
            sock.close()
    
    def test_connection(self):
        """Should be able to connect to binary server."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((self.HOST, self.PORT))
            sock.close()
        except ConnectionRefusedError:
            self.skipTest("BINARY server not running")


class TestUDPProtocol(unittest.TestCase):
    """Tests for UDP sensor protocol."""
    
    HOST = 'localhost'
    PORT = 5402
    VERSION = 1
    
    def build_datagram(self, sensor_id: int, temperature: float, 
                       location: str, corrupt: bool = False) -> bytes:
        """Build a sensor datagram."""
        location_padded = location[:10].ljust(10).encode('utf-8')
        
        payload = struct.pack(
            '>BIf10s',
            self.VERSION,
            sensor_id,
            temperature,
            location_padded
        )
        
        crc = zlib.crc32(payload) & 0xFFFFFFFF
        
        if corrupt:
            crc ^= 0xDEADBEEF
        
        return payload + struct.pack('>I', crc)
    
    def send_datagram(self, datagram: bytes) -> bool:
        """Send a UDP datagram."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)
        
        try:
            sock.sendto(datagram, (self.HOST, self.PORT))
            return True
        except Exception:
            return False
        finally:
            sock.close()
    
    def test_valid_datagram(self):
        """Valid datagram should be accepted."""
        datagram = self.build_datagram(1001, 22.5, "TestLab")
        result = self.send_datagram(datagram)
        self.assertTrue(result)
    
    def test_datagram_structure(self):
        """Datagram should be exactly 23 bytes."""
        datagram = self.build_datagram(1001, 22.5, "TestLab")
        self.assertEqual(len(datagram), 23)


class TestCRC32(unittest.TestCase):
    """Tests for CRC32 integrity checking."""
    
    def test_crc32_calculation(self):
        """CRC32 should be calculated correctly."""
        data = b"Hello, Network!"
        crc = zlib.crc32(data) & 0xFFFFFFFF
        
        # Verify it's a 32-bit value
        self.assertIsInstance(crc, int)
        self.assertGreaterEqual(crc, 0)
        self.assertLessEqual(crc, 0xFFFFFFFF)
    
    def test_crc32_detects_change(self):
        """CRC32 should detect data changes."""
        data1 = b"Hello, Network!"
        data2 = b"Hello, Networks!"
        
        crc1 = zlib.crc32(data1) & 0xFFFFFFFF
        crc2 = zlib.crc32(data2) & 0xFFFFFFFF
        
        self.assertNotEqual(crc1, crc2)
    
    def test_crc32_consistency(self):
        """CRC32 should be consistent for same data."""
        data = b"Test data for CRC"
        
        crc1 = zlib.crc32(data) & 0xFFFFFFFF
        crc2 = zlib.crc32(data) & 0xFFFFFFFF
        
        self.assertEqual(crc1, crc2)


def run_specific_exercise(exercise_num: int) -> bool:
    """Run tests for a specific exercise."""
    exercise_tests = {
        1: TestTextProtocol,
        2: TestBinaryProtocol,
        3: TestUDPProtocol,
        4: TestCRC32,
    }
    
    if exercise_num not in exercise_tests:
        print(f"Unknown exercise: {exercise_num}")
        return False
    
    suite = unittest.TestLoader().loadTestsFromTestCase(exercise_tests[exercise_num])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


def main():
    parser = argparse.ArgumentParser(
        description="Run exercise verification tests"
    )
    
    parser.add_argument("--exercise", "-e", type=int,
                        help="Run tests for specific exercise (1-4)")
    parser.add_argument("--all", "-a", action="store_true",
                        help="Run all tests")
    
    args = parser.parse_args()
    
    if args.exercise:
        success = run_specific_exercise(args.exercise)
        return 0 if success else 1
    elif args.all or len(sys.argv) == 1:
        # Run all tests
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        
        suite.addTests(loader.loadTestsFromTestCase(TestCRC32))
        suite.addTests(loader.loadTestsFromTestCase(TestTextProtocol))
        suite.addTests(loader.loadTestsFromTestCase(TestBinaryProtocol))
        suite.addTests(loader.loadTestsFromTestCase(TestUDPProtocol))
        
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(main())
