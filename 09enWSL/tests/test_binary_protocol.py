#!/usr/bin/env python3
"""
Binary Protocol Unit Tests — Week 9
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Focused tests for struct operations, CRC validation and endianness handling.
These tests verify the core presentation layer functions work correctly.

Usage:
    python tests/test_binary_protocol.py
    python -m pytest tests/test_binary_protocol.py -v
"""

from __future__ import annotations

import struct
import sys
import zlib
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

# Protocol constants (must match src/utils/net_utils.py)
MAGIC = b"S9PK"
HEADER_FORMAT = ">4sBBII"  # magic(4) + version(1) + flags(1) + length(4) + crc(4)
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)  # 14 bytes


# ═══════════════════════════════════════════════════════════════════════════════
# HEADER_PACK_UNPACK_TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_header_size_calculation():
    """Verify header size matches expected 14 bytes."""
    expected_size = 4 + 1 + 1 + 4 + 4  # magic + version + flags + length + crc
    actual_size = struct.calcsize(HEADER_FORMAT)
    
    assert actual_size == expected_size, f"Header size mismatch: {actual_size} != {expected_size}"
    assert actual_size == 14, "Header should be exactly 14 bytes"
    print("✓ test_header_size_calculation passed")


def test_header_pack_unpack_roundtrip():
    """Test that pack/unpack produces identical values."""
    test_cases = [
        (MAGIC, 1, 0x00, 0, 0),              # Minimal header
        (MAGIC, 1, 0xFF, 1000, 0xDEADBEEF),  # Typical values
        (MAGIC, 255, 0x03, 65535, 0xFFFFFFFF),  # Max values
        (b"TEST", 2, 0x80, 12345, 0x12345678),  # Different magic
    ]
    
    for magic, version, flags, length, crc in test_cases:
        # Pack
        packed = struct.pack(HEADER_FORMAT, magic, version, flags, length, crc)
        assert len(packed) == HEADER_SIZE, f"Packed size wrong for {magic}"
        
        # Unpack
        m, v, f, l, c = struct.unpack(HEADER_FORMAT, packed)
        
        # Verify roundtrip
        assert m == magic, f"Magic mismatch: {m} != {magic}"
        assert v == version, f"Version mismatch: {v} != {version}"
        assert f == flags, f"Flags mismatch: {f} != {flags}"
        assert l == length, f"Length mismatch: {l} != {length}"
        assert c == crc, f"CRC mismatch: {c} != {crc}"
    
    print("✓ test_header_pack_unpack_roundtrip passed")


def test_header_byte_positions():
    """Verify specific bytes are at expected positions."""
    magic = b"S9PK"
    version = 0x01
    flags = 0x03
    length = 0x00000005  # 5 bytes
    crc = 0xF7D18982     # CRC of "Hello"
    
    packed = struct.pack(HEADER_FORMAT, magic, version, flags, length, crc)
    
    # Magic at bytes 0-3
    assert packed[0:4] == b"S9PK", "Magic bytes wrong"
    
    # Version at byte 4
    assert packed[4] == 0x01, "Version byte wrong"
    
    # Flags at byte 5
    assert packed[5] == 0x03, "Flags byte wrong"
    
    # Length at bytes 6-9 (big-endian: 00 00 00 05)
    assert packed[6:10] == b"\x00\x00\x00\x05", "Length bytes wrong"
    
    # CRC at bytes 10-13 (big-endian: F7 D1 89 82)
    assert packed[10:14] == b"\xF7\xD1\x89\x82", "CRC bytes wrong"
    
    print("✓ test_header_byte_positions passed")


# ═══════════════════════════════════════════════════════════════════════════════
# CRC32_VALIDATION_TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_crc32_known_values():
    """Test CRC-32 against known reference values."""
    test_cases = [
        (b"", 0x00000000),           # Empty string
        (b"Hello", 0xF7D18982),      # Standard test
        (b"123456789", 0xCBF43926),  # CRC-32 check value
        (b"\x00", 0xD202EF8D),       # Single null byte
    ]
    
    for data, expected_crc in test_cases:
        computed = zlib.crc32(data) & 0xFFFFFFFF
        assert computed == expected_crc, \
            f"CRC mismatch for {data!r}: 0x{computed:08X} != 0x{expected_crc:08X}"
    
    print("✓ test_crc32_known_values passed")


def test_crc32_detects_corruption():
    """Verify CRC detects single-bit errors."""
    original = b"Transfer $100 to Alice"
    original_crc = zlib.crc32(original) & 0xFFFFFFFF
    
    # Corrupt one bit at various positions
    for pos in [0, 5, 10, len(original) - 1]:
        corrupted = bytearray(original)
        corrupted[pos] ^= 0x01  # Flip lowest bit
        corrupted = bytes(corrupted)
        
        corrupted_crc = zlib.crc32(corrupted) & 0xFFFFFFFF
        assert corrupted_crc != original_crc, \
            f"CRC failed to detect corruption at position {pos}"
    
    print("✓ test_crc32_detects_corruption passed")


def test_crc32_mask_required():
    """Verify the 0xFFFFFFFF mask handles signed results."""
    # Some Python versions may return signed values
    data = b"test data for mask verification"
    
    masked = zlib.crc32(data) & 0xFFFFFFFF
    
    # Result must be positive and fit in 32 bits
    assert masked >= 0, "Masked CRC should be non-negative"
    assert masked <= 0xFFFFFFFF, "Masked CRC should fit in 32 bits"
    
    print("✓ test_crc32_mask_required passed")


# ═══════════════════════════════════════════════════════════════════════════════
# ENDIANNESS_CONVERSION_TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_endianness_big_vs_little():
    """Verify big-endian and little-endian produce different bytes."""
    value = 0x12345678
    
    big_endian = struct.pack(">I", value)
    little_endian = struct.pack("<I", value)
    
    # They should be different
    assert big_endian != little_endian, "BE and LE should differ"
    
    # Big-endian: MSB first
    assert big_endian == b"\x12\x34\x56\x78", "Big-endian bytes wrong"
    
    # Little-endian: LSB first
    assert little_endian == b"\x78\x56\x34\x12", "Little-endian bytes wrong"
    
    print("✓ test_endianness_big_vs_little passed")


def test_network_byte_order_is_big_endian():
    """Verify '!' format specifier equals '>' (network = big-endian)."""
    value = 0xCAFEBABE
    
    network_order = struct.pack("!I", value)
    big_endian = struct.pack(">I", value)
    
    assert network_order == big_endian, \
        "Network byte order should equal big-endian"
    
    print("✓ test_network_byte_order_is_big_endian passed")


def test_wrong_endianness_produces_wrong_value():
    """Demonstrate that mismatched endianness corrupts data."""
    original_value = 0x12345678
    
    # Pack as big-endian (network order)
    packed = struct.pack(">I", original_value)
    
    # Unpack as little-endian (wrong!)
    wrong_value = struct.unpack("<I", packed)[0]
    
    # Values should be completely different
    assert wrong_value != original_value, \
        "Mismatched endianness should produce different value"
    assert wrong_value == 0x78563412, \
        f"Expected 0x78563412, got 0x{wrong_value:08X}"
    
    print("✓ test_wrong_endianness_produces_wrong_value passed")


def test_multi_field_header_endianness():
    """Test endianness across multiple fields in a header."""
    # Simulate a protocol header: magic + length + checksum
    fmt_be = ">4sII"  # Big-endian
    fmt_le = "<4sII"  # Little-endian
    
    magic = b"TEST"
    length = 256    # 0x00000100
    checksum = 0xAABBCCDD
    
    packed_be = struct.pack(fmt_be, magic, length, checksum)
    packed_le = struct.pack(fmt_le, magic, length, checksum)
    
    # Magic is same (single bytes)
    assert packed_be[:4] == packed_le[:4] == b"TEST"
    
    # But numeric fields differ
    assert packed_be[4:8] != packed_le[4:8], "Length bytes should differ"
    assert packed_be[8:12] != packed_le[8:12], "Checksum bytes should differ"
    
    # Verify BE length bytes
    assert packed_be[4:8] == b"\x00\x00\x01\x00", "BE length wrong"
    
    # Verify LE length bytes
    assert packed_le[4:8] == b"\x00\x01\x00\x00", "LE length wrong"
    
    print("✓ test_multi_field_header_endianness passed")


# ═══════════════════════════════════════════════════════════════════════════════
# INTEGRATION_TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_full_message_pack_unpack():
    """Test packing and unpacking a complete message with header and payload."""
    payload = b"Hello, Week 9!"
    version = 1
    flags = 0x00
    
    # Calculate CRC of payload
    crc = zlib.crc32(payload) & 0xFFFFFFFF
    length = len(payload)
    
    # Pack header
    header = struct.pack(HEADER_FORMAT, MAGIC, version, flags, length, crc)
    
    # Combine header + payload
    message = header + payload
    
    # Unpack and verify
    h_magic, h_version, h_flags, h_length, h_crc = struct.unpack(
        HEADER_FORMAT, message[:HEADER_SIZE]
    )
    h_payload = message[HEADER_SIZE:HEADER_SIZE + h_length]
    
    assert h_magic == MAGIC, "Magic mismatch"
    assert h_version == version, "Version mismatch"
    assert h_flags == flags, "Flags mismatch"
    assert h_length == len(payload), "Length mismatch"
    assert h_crc == crc, "CRC mismatch"
    assert h_payload == payload, "Payload mismatch"
    
    # Verify CRC
    computed_crc = zlib.crc32(h_payload) & 0xFFFFFFFF
    assert computed_crc == h_crc, "CRC verification failed"
    
    print("✓ test_full_message_pack_unpack passed")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════

def run_all_tests() -> int:
    """Run all tests and return exit code."""
    tests = [
        test_header_size_calculation,
        test_header_pack_unpack_roundtrip,
        test_header_byte_positions,
        test_crc32_known_values,
        test_crc32_detects_corruption,
        test_crc32_mask_required,
        test_endianness_big_vs_little,
        test_network_byte_order_is_big_endian,
        test_wrong_endianness_produces_wrong_value,
        test_multi_field_header_endianness,
        test_full_message_pack_unpack,
    ]
    
    print("=" * 60)
    print("  Binary Protocol Unit Tests — Week 9")
    print("=" * 60)
    print()
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} ERROR: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"  Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
