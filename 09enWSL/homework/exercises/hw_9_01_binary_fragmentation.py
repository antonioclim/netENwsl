#!/usr/bin/env python3
"""
Homework Assignment 1: Multi-Format Protocol
Week 9: Session Layer (L5) and Presentation Layer (L6)

NETWORKING class - ASE, Informatics | by Revolvix

Student: <Your Name>
ID: <Student ID>
Date: <Submission Date>

Assignment:
-----------
Implement a binary protocol supporting multiple data formats (TEXT, INTEGER, BLOB)
with proper headers, checksums and serialisation.

Protocol Format:
----------------
+--------+--------+--------+--------+--------+--------+
| MAGIC  | VER    | TYPE   | LENGTH          | CRC    |
| 4B     | 1B     | 1B     | 4B              | 4B     |
+--------+--------+--------+--------+--------+--------+
| PAYLOAD (variable length)                           |
+----------------------------------------------------+

Message Types:
- TEXT (0x01): UTF-8 encoded string
- INTEGER (0x02): 32-bit signed integer
- BLOB (0x03): Raw binary data

Requirements:
- Magic bytes: b'MFMT'
- Version: 1
- Network byte order (big-endian) for all multi-byte fields
- CRC-32 calculated over type + length + payload
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import struct
import zlib
from enum import IntEnum
from typing import Tuple, Optional


# =============================================================================
# Constants
# =============================================================================

MAGIC = b'MFMT'
VERSION = 1
HEADER_FORMAT = ">4sBBII"  # magic(4), version(1), type(1), length(4), crc(4)
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class MessageType(IntEnum):
    """Protocol message types."""
    TEXT = 0x01
    INTEGER = 0x02
    BLOB = 0x03


# =============================================================================
# TODO: Implement these functions
# =============================================================================


# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def encode_message(msg_type: int, payload: bytes) -> bytes:
    """
    Encode a message with the protocol header.
    
    Args:
        msg_type: Message type (TEXT, INTEGER, or BLOB)
        payload: Raw payload bytes
        
    Returns:
        Complete message with header and payload
        
    Raises:
        ValueError: If msg_type is invalid
        
    Example:
        >>> data = encode_message(MessageType.TEXT, b"Hello")
        >>> len(data) == HEADER_SIZE + 5
        True
    """
    # TODO: Implement this function
    # 1. Validate message type
    # 2. Calculate payload length
    # 3. Calculate CRC-32 over (type + length + payload)
    # 4. Pack header using struct
    # 5. Return header + payload
    
    raise NotImplementedError("Implement encode_message()")



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def decode_message(data: bytes) -> Tuple[int, bytes]:
    """
    Decode a message and extract the payload.
    
    Args:
        data: Complete message bytes (header + payload)
        
    Returns:
        Tuple of (message_type, payload)
        
    Raises:
        ValueError: If magic bytes are incorrect
        ValueError: If version is unsupported
        ValueError: If CRC check fails
        ValueError: If data is truncated
        
    Example:
        >>> msg = encode_message(MessageType.TEXT, b"Hello")
        >>> msg_type, payload = decode_message(msg)
        >>> payload
        b'Hello'
    """
    # TODO: Implement this function
    # 1. Verify data length >= HEADER_SIZE
    # 2. Unpack header
    # 3. Verify magic bytes
    # 4. Verify version
    # 5. Extract payload
    # 6. Verify CRC
    # 7. Return (type, payload)
    
    raise NotImplementedError("Implement decode_message()")



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def verify_checksum(data: bytes) -> bool:
    """
    Verify the CRC-32 checksum of a message.
    
    Args:
        data: Complete message bytes (header + payload)
        
    Returns:
        True if checksum is valid, False otherwise
        
    Example:
        >>> msg = encode_message(MessageType.INTEGER, struct.pack(">i", 42))
        >>> verify_checksum(msg)
        True
    """
    # TODO: Implement this function
    # 1. Extract stored CRC from header
    # 2. Calculate CRC over (type + length + payload)
    # 3. Compare and return result
    
    raise NotImplementedError("Implement verify_checksum()")


# =============================================================================
# Helper functions for specific types
# =============================================================================


# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def encode_text(text: str) -> bytes:
    """
    Encode a text string as a TEXT message.
    
    Args:
        text: String to encode
        
    Returns:
        Complete message bytes
    """
    payload = text.encode('utf-8')
    return encode_message(MessageType.TEXT, payload)



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def decode_text(data: bytes) -> str:
    """
    Decode a TEXT message to a string.
    
    Args:
        data: Complete message bytes
        
    Returns:
        Decoded string
        
    Raises:
        ValueError: If message type is not TEXT
    """
    msg_type, payload = decode_message(data)
    if msg_type != MessageType.TEXT:
        raise ValueError(f"Expected TEXT, got {msg_type}")
    return payload.decode('utf-8')



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def encode_integer(value: int) -> bytes:
    """
    Encode an integer as an INTEGER message.
    
    Args:
        value: 32-bit signed integer
        
    Returns:
        Complete message bytes
    """
    payload = struct.pack(">i", value)
    return encode_message(MessageType.INTEGER, payload)



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def decode_integer(data: bytes) -> int:
    """
    Decode an INTEGER message to an int.
    
    Args:
        data: Complete message bytes
        
    Returns:
        Decoded integer
        
    Raises:
        ValueError: If message type is not INTEGER
    """
    msg_type, payload = decode_message(data)
    if msg_type != MessageType.INTEGER:
        raise ValueError(f"Expected INTEGER, got {msg_type}")
    return struct.unpack(">i", payload)[0]



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def encode_blob(data: bytes) -> bytes:
    """
    Encode raw bytes as a BLOB message.
    
    Args:
        data: Raw binary data
        
    Returns:
        Complete message bytes
    """
    return encode_message(MessageType.BLOB, data)



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def decode_blob(data: bytes) -> bytes:
    """
    Decode a BLOB message to raw bytes.
    
    Args:
        data: Complete message bytes
        
    Returns:
        Decoded binary data
        
    Raises:
        ValueError: If message type is not BLOB
    """
    msg_type, payload = decode_message(data)
    if msg_type != MessageType.BLOB:
        raise ValueError(f"Expected BLOB, got {msg_type}")
    return payload


# =============================================================================
# Test cases
# =============================================================================


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def test_all():
    """Run all test cases."""
    print("Testing Multi-Format Protocol Implementation")
    print("=" * 50)
    
    tests = [
        test_encode_decode_text,
        test_encode_decode_integer,
        test_encode_decode_blob,
        test_empty_payload,
        test_large_payload,
        test_checksum_verification,
        test_invalid_magic,
        test_corrupted_data,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            print(f"  [PASS] {test.__name__}")
            passed += 1
        except NotImplementedError as e:
            print(f"  [SKIP] {test.__name__}: {e}")
        except AssertionError as e:
            print(f"  [FAIL] {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"  [ERROR] {test.__name__}: {type(e).__name__}: {e}")
            failed += 1
    
    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    return failed == 0



# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def test_encode_decode_text():
    """Test TEXT message encoding and decoding."""
    original = "Hello, World! Привіт! 你好!"
    encoded = encode_text(original)
    decoded = decode_text(encoded)
    assert decoded == original, f"Text mismatch: {decoded} != {original}"



# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def test_encode_decode_integer():
    """Test INTEGER message encoding and decoding."""
    for value in [0, 1, -1, 2147483647, -2147483648, 42, -12345]:
        encoded = encode_integer(value)
        decoded = decode_integer(encoded)
        assert decoded == value, f"Integer mismatch: {decoded} != {value}"



# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def test_encode_decode_blob():
    """Test BLOB message encoding and decoding."""
    original = bytes(range(256))
    encoded = encode_blob(original)
    decoded = decode_blob(encoded)
    assert decoded == original, "Blob mismatch"



# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def test_empty_payload():
    """Test handling of empty payloads."""
    for msg_type in MessageType:
        encoded = encode_message(msg_type, b"")
        decoded_type, payload = decode_message(encoded)
        assert decoded_type == msg_type
        assert payload == b""



# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def test_large_payload():
    """Test handling of large payloads."""
    large_data = b"X" * 100000
    encoded = encode_blob(large_data)
    decoded = decode_blob(encoded)
    assert decoded == large_data



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def test_checksum_verification():
    """Test CRC-32 checksum verification."""
    encoded = encode_text("Test message")
    assert verify_checksum(encoded), "Valid checksum should verify"
    
    # Corrupt the payload
    corrupted = bytearray(encoded)
    corrupted[-1] ^= 0xFF  # Flip bits in last byte
    assert not verify_checksum(bytes(corrupted)), "Corrupted data should fail verification"



# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def test_invalid_magic():
    """Test rejection of invalid magic bytes."""
    encoded = encode_text("Test")
    invalid = b"XXXX" + encoded[4:]
    try:
        decode_message(invalid)
        assert False, "Should raise ValueError for invalid magic"
    except ValueError:
        pass



# ═══════════════════════════════════════════════════════════════════════════════
# TEST_VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════
def test_corrupted_data():
    """Test handling of corrupted/truncated data."""
    # Truncated header
    try:
        decode_message(b"MFM")
        assert False, "Should raise ValueError for truncated header"
    except ValueError:
        pass
    
    # Truncated payload
    encoded = encode_text("Hello")
    truncated = encoded[:-3]
    try:
        decode_message(truncated)
        assert False, "Should raise ValueError for truncated payload"
    except ValueError:
        pass


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    # Run tests
    success = test_all()
    
    if success:
        print("\nAll tests passed! Your implementation is complete.")
    else:
        print("\nSome tests failed. Review your implementation.")
    
    # Interactive demo (uncomment to use)
    # print("\n--- Interactive Demo ---")
    # while True:
    #     text = input("Enter text to encode (or 'quit'): ")
    #     if text.lower() == 'quit':
    #         break
    #     encoded = encode_text(text)
    #     print(f"Encoded ({len(encoded)} bytes): {encoded.hex()}")
    #     decoded = decode_text(encoded)
    #     print(f"Decoded: {decoded}")
