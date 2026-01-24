#!/usr/bin/env python3
"""
Unit Tests for Protocol Functions
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Tests individual functions without requiring running servers.
These tests verify the core protocol logic in isolation.

Usage:
    python tests/test_unit_functions.py
    python -m pytest tests/test_unit_functions.py -v
"""


# ═══════════════════════════════════════════════════════════════════════════════
# IMPORT_DEPENDENCIES
# ═══════════════════════════════════════════════════════════════════════════════

import sys
import struct
import zlib
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_LENGTH_PREFIX_FRAMING
# ═══════════════════════════════════════════════════════════════════════════════

class TestLengthPrefixFraming(unittest.TestCase):
    """Tests for length-prefix framing functions."""
    
    def test_frame_empty_payload(self):
        """Empty payload should have length 0."""
        payload = b''
        length_bytes = len(payload).to_bytes(2, 'big')
        frame = length_bytes + payload
        self.assertEqual(frame, b'\x00\x00')
        self.assertEqual(len(frame), 2)
    
    def test_frame_hello(self):
        """Frame 'hello' correctly with 2-byte big-endian length."""
        payload = b'hello'
        length_bytes = len(payload).to_bytes(2, 'big')
        frame = length_bytes + payload
        self.assertEqual(frame, b'\x00\x05hello')
        self.assertEqual(len(frame), 7)
    
    def test_frame_set_command(self):
        """Frame 'SET key value' (13 bytes)."""
        payload = b'SET key value'
        length_bytes = len(payload).to_bytes(2, 'big')
        frame = length_bytes + payload
        # 13 = 0x000D
        self.assertEqual(frame[:2], b'\x00\x0d')
        self.assertEqual(len(frame), 15)
    
    def test_frame_unicode(self):
        """UTF-8 encoding for 'café' produces 5 bytes."""
        payload = 'café'.encode('utf-8')  # c, a, f, é (2 bytes)
        self.assertEqual(len(payload), 5)
        length_bytes = len(payload).to_bytes(2, 'big')
        frame = length_bytes + payload
        self.assertEqual(frame[:2], b'\x00\x05')
    
    def test_parse_frame_hello(self):
        """Parse framed 'hello' correctly."""
        frame = b'\x00\x05hello'
        length = int.from_bytes(frame[:2], 'big')
        payload = frame[2:2+length]
        self.assertEqual(length, 5)
        self.assertEqual(payload, b'hello')
    
    def test_max_payload_length(self):
        """Maximum payload length with 2-byte field is 65535."""
        max_len = 65535
        length_bytes = max_len.to_bytes(2, 'big')
        self.assertEqual(length_bytes, b'\xff\xff')


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_BINARY_HEADER
# ═══════════════════════════════════════════════════════════════════════════════

class TestBinaryHeader(unittest.TestCase):
    """Tests for binary protocol header construction."""
    
    MAGIC = b'NP'
    VERSION = 1
    
    def test_header_size_without_crc(self):
        """Header without CRC should be 10 bytes."""
        header = struct.pack('>2sBBHI', 
                            self.MAGIC, self.VERSION, 1, 0, 0)
        self.assertEqual(len(header), 10)
    
    def test_header_size_with_crc(self):
        """Complete header with CRC should be 14 bytes."""
        header = struct.pack('>2sBBHII', 
                            self.MAGIC, self.VERSION, 1, 0, 0, 0)
        self.assertEqual(len(header), 14)
    
    def test_magic_bytes(self):
        """Magic should be 'NP' = 0x4E50."""
        header = struct.pack('>2sBBHII', 
                            self.MAGIC, self.VERSION, 1, 0, 0, 0)
        self.assertEqual(header[:2], b'NP')
        self.assertEqual(header[:2].hex(), '4e50')
    
    def test_version_byte(self):
        """Version 1 should be at offset 2."""
        header = struct.pack('>2sBBHII', 
                            self.MAGIC, self.VERSION, 1, 0, 0, 0)
        self.assertEqual(header[2], 1)
    
    def test_type_byte(self):
        """Message type should be at offset 3."""
        msg_type = 5
        header = struct.pack('>2sBBHII', 
                            self.MAGIC, self.VERSION, msg_type, 0, 0, 0)
        self.assertEqual(header[3], 5)
    
    def test_payload_length_field(self):
        """Payload length (2 bytes) at offset 4-5."""
        payload_len = 100
        header = struct.pack('>2sBBHII', 
                            self.MAGIC, self.VERSION, 1, payload_len, 0, 0)
        extracted_len = struct.unpack('>H', header[4:6])[0]
        self.assertEqual(extracted_len, 100)
    
    def test_sequence_number_field(self):
        """Sequence number (4 bytes) at offset 6-9."""
        seq = 12345678
        header = struct.pack('>2sBBHII', 
                            self.MAGIC, self.VERSION, 1, 0, seq, 0)
        extracted_seq = struct.unpack('>I', header[6:10])[0]
        self.assertEqual(extracted_seq, 12345678)
    
    def test_crc_calculation(self):
        """CRC should be calculated over header + payload."""
        header_no_crc = struct.pack('>2sBBHI', 
                                    self.MAGIC, self.VERSION, 1, 2, 42)
        payload = b'Hi'
        crc = zlib.crc32(header_no_crc + payload) & 0xFFFFFFFF
        self.assertIsInstance(crc, int)
        self.assertGreaterEqual(crc, 0)
        self.assertLessEqual(crc, 0xFFFFFFFF)
    
    def test_header_roundtrip(self):
        """Pack and unpack header should preserve values."""
        magic = b'NP'
        version = 1
        msg_type = 3
        payload_len = 50
        seq = 999
        crc = 0xDEADBEEF
        
        header = struct.pack('>2sBBHII', 
                            magic, version, msg_type, payload_len, seq, crc)
        
        unpacked = struct.unpack('>2sBBHII', header)
        self.assertEqual(unpacked[0], magic)
        self.assertEqual(unpacked[1], version)
        self.assertEqual(unpacked[2], msg_type)
        self.assertEqual(unpacked[3], payload_len)
        self.assertEqual(unpacked[4], seq)
        self.assertEqual(unpacked[5], crc)


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_ENDIANNESS
# ═══════════════════════════════════════════════════════════════════════════════

class TestEndianness(unittest.TestCase):
    """Tests for byte order handling."""
    
    def test_big_endian_1000(self):
        """1000 in big-endian should be 03e8."""
        packed = struct.pack('>H', 1000)
        self.assertEqual(packed.hex(), '03e8')
        self.assertEqual(packed, b'\x03\xe8')
    
    def test_little_endian_1000(self):
        """1000 in little-endian should be e803."""
        packed = struct.pack('<H', 1000)
        self.assertEqual(packed.hex(), 'e803')
        self.assertEqual(packed, b'\xe8\x03')
    
    def test_wrong_endian_interpretation(self):
        """Reading little-endian as big-endian gives wrong value."""
        little = struct.pack('<H', 1000)
        wrong_value = struct.unpack('>H', little)[0]
        self.assertEqual(wrong_value, 59395)  # 0xE803
    
    def test_network_byte_order(self):
        """Network byte order (!) should be same as big-endian (>)."""
        value = 12345
        big = struct.pack('>I', value)
        network = struct.pack('!I', value)
        self.assertEqual(big, network)
    
    def test_4byte_big_endian(self):
        """4-byte integer 0x12345678 in big-endian."""
        packed = struct.pack('>I', 0x12345678)
        self.assertEqual(packed, b'\x12\x34\x56\x78')
    
    def test_4byte_little_endian(self):
        """4-byte integer 0x12345678 in little-endian."""
        packed = struct.pack('<I', 0x12345678)
        self.assertEqual(packed, b'\x78\x56\x34\x12')


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_CRC32
# ═══════════════════════════════════════════════════════════════════════════════

class TestCRC32Functions(unittest.TestCase):
    """Tests for CRC32 integrity checking."""
    
    def test_crc32_returns_int(self):
        """CRC32 should return an integer."""
        data = b"Hello, Network!"
        crc = zlib.crc32(data)
        self.assertIsInstance(crc, int)
    
    def test_crc32_masked_range(self):
        """Masked CRC32 should be in valid 32-bit range."""
        data = b"Test data"
        crc = zlib.crc32(data) & 0xFFFFFFFF
        self.assertGreaterEqual(crc, 0)
        self.assertLessEqual(crc, 0xFFFFFFFF)
    
    def test_crc32_consistency(self):
        """CRC32 should be consistent for same data."""
        data = b"Test data for CRC"
        crc1 = zlib.crc32(data) & 0xFFFFFFFF
        crc2 = zlib.crc32(data) & 0xFFFFFFFF
        self.assertEqual(crc1, crc2)
    
    def test_crc32_detects_single_bit_change(self):
        """CRC32 should detect single bit change."""
        data1 = b"Hello, Network!"
        data2 = b"Hello, Network?"  # Last char changed
        crc1 = zlib.crc32(data1) & 0xFFFFFFFF
        crc2 = zlib.crc32(data2) & 0xFFFFFFFF
        self.assertNotEqual(crc1, crc2)
    
    def test_crc32_detects_byte_swap(self):
        """CRC32 should detect byte swap (unlike simple checksum)."""
        data1 = b"Hello"
        data2 = b"eHllo"  # 'H' and 'e' swapped
        crc1 = zlib.crc32(data1) & 0xFFFFFFFF
        crc2 = zlib.crc32(data2) & 0xFFFFFFFF
        self.assertNotEqual(crc1, crc2)
    
    def test_crc32_incremental(self):
        """Incremental CRC calculation should match full calculation."""
        data_full = b"Hello, World!"
        crc_full = zlib.crc32(data_full) & 0xFFFFFFFF
        
        # Calculate incrementally
        crc_part1 = zlib.crc32(b"Hello")
        crc_incremental = zlib.crc32(b", World!", crc_part1) & 0xFFFFFFFF
        
        self.assertEqual(crc_full, crc_incremental)
    
    def test_crc32_empty_data(self):
        """CRC32 of empty data should be 0."""
        crc = zlib.crc32(b'') & 0xFFFFFFFF
        self.assertEqual(crc, 0)


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_UDP_DATAGRAM
# ═══════════════════════════════════════════════════════════════════════════════

class TestUDPDatagram(unittest.TestCase):
    """Tests for UDP sensor datagram structure."""
    
    VERSION = 1
    
    def test_datagram_size(self):
        """Datagram should be exactly 23 bytes."""
        # version(1) + sensor_id(4) + temp(4) + location(10) + crc(4) = 23
        location_padded = 'TestLab'.ljust(10).encode('utf-8')[:10]
        payload = struct.pack('>BIf10s', 
                             self.VERSION, 1001, 22.5, location_padded)
        crc = zlib.crc32(payload) & 0xFFFFFFFF
        datagram = payload + struct.pack('>I', crc)
        self.assertEqual(len(datagram), 23)
    
    def test_location_padding_short(self):
        """Short location should be padded to 10 bytes."""
        short_loc = 'Lab'.ljust(10).encode('utf-8')[:10]
        self.assertEqual(len(short_loc), 10)
        self.assertEqual(short_loc, b'Lab       ')
    
    def test_location_truncation_long(self):
        """Long location should be truncated to 10 bytes."""
        long_loc = 'VeryLongLocationName'.ljust(10).encode('utf-8')[:10]
        self.assertEqual(len(long_loc), 10)
        self.assertEqual(long_loc, b'VeryLongLo')
    
    def test_temperature_float(self):
        """Temperature should be packed as 4-byte float."""
        temp = 23.5
        packed = struct.pack('>f', temp)
        self.assertEqual(len(packed), 4)
        unpacked = struct.unpack('>f', packed)[0]
        self.assertAlmostEqual(unpacked, 23.5, places=1)
    
    def test_sensor_id_range(self):
        """Sensor ID should support full 32-bit range."""
        sensor_id = 0xFFFFFFFF
        packed = struct.pack('>I', sensor_id)
        self.assertEqual(len(packed), 4)
        unpacked = struct.unpack('>I', packed)[0]
        self.assertEqual(unpacked, 0xFFFFFFFF)
    
    def test_datagram_parsing(self):
        """Datagram should parse back to original values."""
        version = 1
        sensor_id = 42
        temp = 25.5
        location = 'Room101'
        
        location_padded = location.ljust(10).encode('utf-8')[:10]
        payload = struct.pack('>BIf10s', version, sensor_id, temp, location_padded)
        crc = zlib.crc32(payload) & 0xFFFFFFFF
        datagram = payload + struct.pack('>I', crc)
        
        # Parse
        parsed = struct.unpack('>BIf10sI', datagram)
        self.assertEqual(parsed[0], version)
        self.assertEqual(parsed[1], sensor_id)
        self.assertAlmostEqual(parsed[2], temp, places=1)
        self.assertEqual(parsed[3].rstrip(b' ').decode('utf-8'), location)


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_TEXT_PROTOCOL_COMMANDS
# ═══════════════════════════════════════════════════════════════════════════════

class TestTextProtocolCommands(unittest.TestCase):
    """Tests for TEXT protocol command parsing."""
    
    VALID_COMMANDS = {'PING', 'SET', 'GET', 'DEL', 'COUNT', 'KEYS', 'QUIT'}
    
    def test_valid_commands(self):
        """All valid commands should be recognised."""
        for cmd in self.VALID_COMMANDS:
            self.assertIn(cmd.upper(), self.VALID_COMMANDS)
    
    def test_ping_no_payload(self):
        """PING command has no payload."""
        cmd = "PING"
        parts = cmd.split(' ', 1)
        self.assertEqual(parts[0], 'PING')
        self.assertEqual(len(parts), 1)
    
    def test_set_parsing(self):
        """SET command should parse key and value."""
        cmd = "SET mykey myvalue"
        parts = cmd.split(' ', 2)
        self.assertEqual(parts[0], 'SET')
        self.assertEqual(parts[1], 'mykey')
        self.assertEqual(parts[2], 'myvalue')
    
    def test_get_parsing(self):
        """GET command should parse key."""
        cmd = "GET mykey"
        parts = cmd.split(' ', 1)
        self.assertEqual(parts[0], 'GET')
        self.assertEqual(parts[1], 'mykey')
    
    def test_case_insensitive_command(self):
        """Commands should be case-insensitive."""
        for variant in ['ping', 'PING', 'Ping', 'pInG']:
            self.assertIn(variant.upper(), self.VALID_COMMANDS)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("="*60)
    print("Week 4 Unit Tests — Protocol Functions")
    print("NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim")
    print("="*60)
    print()
    
    unittest.main(verbosity=2)
