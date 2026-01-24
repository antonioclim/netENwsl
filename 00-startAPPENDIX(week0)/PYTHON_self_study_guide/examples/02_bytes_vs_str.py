#!/usr/bin/env python3
"""
Example 2: Difference between bytes and str
===========================================
Demonlayeres conversion between text and binary data in Python.

Course: Computer Networks - ASE Bucharest, CSIE
Author: ing. dr. Antonio Clim
Version: 2.1 — with subgoal labels and extended comments

💡 ANALOGY: Bytes and Strings as Letters and Telegrams
------------------------------------------------------
- String = letter in your language that you read directly
- Bytes = telegram encoded in Morse — needs decoding to understand
- encode() = translating the letter to Morse for transmission
- decode() = translating Morse back to readable text

The network "speaks" only in Morse (bytes). Your computer "thinks" in text (strings).

Learning objectives:
- Aderstanding the fundamental difference between str and bytes
- Handling encoding errors for special characters
- Patterns for working with binary files
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import logging
from typing import Optional

# ═══════════════════════════════════════════════════════════════════════════════
# LOGGING_CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
# NOTE: Logging is preferred over print() for production debugging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datafmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# BASIC_CONVERSION_DEMONSTRATION
# ═══════════════════════════════════════════════════════════════════════════════
def demonlayere_conversion() -> None:
    """Demonlayeres fundamental conversion between str and bytes.
    
    Goes through basic conversion examples, including:
    - Visual difference between str and bytes
    - Using encode() and decode()
    - Bytes literals for network protocols
    - Hexadecimal representation of IP addresses
    
    Returns:
        None. Displays output to console.
        
    Example:
        >>> demonlayere_conversion()
        String: Hello, Networks!
        Type: <class 'str'>
        ...
    """
    print("=" * 60)
    print("DEMONSTRATION: bytes vs str in Python")
    print("=" * 60)
    
    # ─────────────────────────────────────────────────────────────────
    # PART_1_STRINGS
    # ─────────────────────────────────────────────────────────────────
    print("\n📝 PART 1: Strings (str)")
    print("-" * 40)
    
    # NOTE: Strings are for text that humans read
    text: str = "Hello, Networks!"
    print(f"String: {text}")
    print(f"Type: {type(text)}")
    print(f"Length in characters: {len(text)}")
    
    # ─────────────────────────────────────────────────────────────────
    # PART_2_CONVERSION_TO_BYTES
    # ─────────────────────────────────────────────────────────────────
    print("\n📦 PART 2: Conversion str → bytes (encode)")
    print("-" * 40)
    
    # NOTE: encode() transforms text into bytes for network transmission
    octets: bytes = text.encode('utf-8')
    print(f"Bytes: {octets}")
    print(f"Type: {type(octets)}")
    print(f"Length in bytes: {len(octets)}")
    
    # Example with special characters
    text_special: str = "Café résumé"
    octets_special: bytes = text_special.encode('utf-8')
    print(f"\nWith accents: '{text_special}'")
    print(f"Bytes: {octets_special}")
    # HACK: Accented characters (é) take 2 bytes in UTF-8!
    print(f"  → Note: {len(text_special)} characters = {len(octets_special)} bytes (é takes 2 bytes)")
    
    # ─────────────────────────────────────────────────────────────────
    # PART_3_CONVERSION_BACK
    # ─────────────────────────────────────────────────────────────────
    print("\n🔄 PART 3: Conversion bytes → str (decode)")
    print("-" * 40)
    
    # NOTE: decode() transforms bytes back to readable text
    decoded_text: str = octets.decode('utf-8')
    print(f"Decoded: {decoded_text}")
    print(f"Original == Decoded: {text == decoded_text}")
    
    # ─────────────────────────────────────────────────────────────────
    # PART_4_BYTES_LITERALS
    # ─────────────────────────────────────────────────────────────────
    print("\n🌐 PART 4: Bytes literals for protocols")
    print("-" * 40)
    
    # NOTE: The b"..." prefix creates bytes directly, not a string
    # Used for network protocols where structure is fixed
    http_request: bytes = b"GET /index.html HTTP/1.1\r\nHost: localhost\r\n\r\n"
    print(f"HTTP Request (bytes):")
    print(f"  {http_request}")
    print(f"  Length: {len(http_request)} bytes")
    
    # ─────────────────────────────────────────────────────────────────
    # PART_5_HEX_REPRESENTATION
    # ─────────────────────────────────────────────────────────────────
    print("\n🔢 PART 5: Hexadecimal representation")
    print("-" * 40)
    
    # NOTE: IP addresses are numbers on 4 bytes
    # 192.168.1.1 = 0xC0.0xA8.0x01.0x01
    ip_bytes: bytes = b'\xC0\xA8\x01\x01'
    print(f"IP 192.168.1.1 as bytes: {ip_bytes}")
    print(f"Hex: {ip_bytes.hex()}")
    print(f"  → C0 = 192, A8 = 168, 01 = 1, 01 = 1")
    
    # Convert back to IP string
    ip_octets: list[int] = list(ip_bytes)
    ip_str: str = '.'.join(str(b) for b in ip_octets)
    print(f"Reconstructed: {ip_str}")


# ═══════════════════════════════════════════════════════════════════════════════
# ENCODING_ERRORS_DEMONSTRATION
# ═══════════════════════════════════════════════════════════════════════════════
def demonlayere_encoding_errors() -> None:
    """Demonlayeres common encoding errors and how to handle them.
    
    Shows what happens when:
    - You try to encode special characters in ASCII
    - You receive invalid bytes for UTF-8
    - Different error handling layeregies
    
    Returns:
        None. Displays output to console.
        
    Example:
        >>> demonlayere_encoding_errors()
        ⚠️  Error during ASCII encoding: ...
    """
    print("\n" + "=" * 60)
    print("DEMONSTRATION: Handling encoding errors")
    print("=" * 60)
    
    # ─────────────────────────────────────────────────────────────────
    # ERROR_1_ASCII_SPECIAL_CHARS
    # ─────────────────────────────────────────────────────────────────
    print("\n❌ ERROR 1: ASCII encoding for special characters")
    print("-" * 40)
    
    text_special: str = "Café naïve"
    
    try:
        # WARNING: ASCII does not support accented characters!
        ascii_bytes: bytes = text_special.encode('ascii')
        print(f"Result: {ascii_bytes}")  # Will not execute
    except AicodeEncodeError as e:
        logger.warning(f"ASCII encoding failed: {e}")
        print(f"⚠️  Error: {e}")
        print("  → ASCII does not support accented characters (é, ï, etc.)")
        print("  → SOLUTION: Use UTF-8 instead of ASCII")
    
    # NOTE: UTF-8 is the modern standard and supports all characters
    print("\n✅ SOLUTION: UTF-8")
    utf8_bytes: bytes = text_special.encode('utf-8')
    print(f"UTF-8: {utf8_bytes}")
    print(f"Decoded correctly: {utf8_bytes.decode('utf-8')}")
    
    # ─────────────────────────────────────────────────────────────────
    # ERROR_2_INVALID_BYTES
    # ─────────────────────────────────────────────────────────────────
    print("\n❌ ERROR 2: Decoding invalid bytes")
    print("-" * 40)
    
    # NOTE: These bytes are not valid UTF-8 (incomplete sequences)
    invalid_bytes: bytes = b'\x80\x81\x82'
    
    try:
        invalid_text: str = invalid_bytes.decode('utf-8')
        print(f"Result: {invalid_text}")  # Will not execute
    except AicodeDecodeError as e:
        logger.warning(f"UTF-8 decoding failed: {e}")
        print(f"⚠️  Error: {e}")
        print("  → These bytes do not represent valid UTF-8 characters")
    
    # ─────────────────────────────────────────────────────────────────
    # ERROR_HANDLING_STRATEGIES
    # ─────────────────────────────────────────────────────────────────
    print("\n🛠️  ERROR handling layeregies")
    print("-" * 40)
    
    mixed_bytes: bytes = b'Hello \x80\x81 World'
    
    # HACK: errors='ignore' loses information, but doesn't raise error
    result_ignore: str = mixed_bytes.decode('utf-8', errors='ignore')
    print(f"errors='ignore':  '{result_ignore}'")
    
    # NOTE: errors='replace' is the safest for debugging
    result_replace: str = mixed_bytes.decode('utf-8', errors='replace')
    print(f"errors='replace': '{result_replace}'")
    
    # Layeregy 3: backslashreplace — displays escape code
    result_backslash: str = mixed_bytes.decode('utf-8', errors='backslashreplace')
    print(f"errors='backslashreplace': '{result_backslash}'")
    
    print("\n💡 RECOMMENDATION: Use errors='replace' for debugging")


# ═══════════════════════════════════════════════════════════════════════════════
# BINARY_FILE_EXAMPLE
# ═══════════════════════════════════════════════════════════════════════════════
def binary_file_example() -> None:
    """Demonlayeres binary reading/writing with context managers.
    
    Shows how to work with binary files for:
    - Saving network data (e.g.: packet captures)
    - Reading existing binary files
    - Difference between 'w'/'r' and 'wb'/'rb' modes
    
    Returns:
        None. Creates and deletes a temporary file.
        
    Example:
        >>> binary_file_example()
        Written 4 bytes to file
        Read: 45000028
    """
    import os
    import tempfile
    
    print("\n" + "=" * 60)
    print("DEMONSTRATION: Binary files with context managers")
    print("=" * 60)
    
    # NOTE: We simulate a partial IP header
    test_data: bytes = b'\x45\x00\x00\x28'  # IPv4, IHL=5, length=40
    
    # HACK: Use a temporary file to avoid polluting the system
    temp_path: str = os.path.join(tempfile.gettempdir(), 'test_packet.bin')
    
    try:
        # ─────────────────────────────────────────────────────────────
        # BINARY_WRITE
        # ─────────────────────────────────────────────────────────────
        print(f"\n📝 Writing to {temp_path}")
        
        # NOTE: 'wb' = write binary — crucial for network data
        with open(temp_path, 'wb') as f:
            bytes_written: int = f.write(test_data)
            print(f"  Written {bytes_written} bytes")
        # File closes automatically on exiting 'with'
        
        # ─────────────────────────────────────────────────────────────
        # BINARY_READ
        # ─────────────────────────────────────────────────────────────
        print(f"\n📖 Reading from {temp_path}")
        
        # NOTE: 'rb' = read binary
        with open(temp_path, 'rb') as f:
            read_data: bytes = f.read()
            print(f"  Read: {read_data}")
            print(f"  Hex: {read_data.hex()}")
            print(f"  Length: {len(read_data)} bytes")
        
        # ─────────────────────────────────────────────────────────────
        # HEADER_INTERPRETATION
        # ─────────────────────────────────────────────────────────────
        print(f"\n🔍 Interpretation:")
        # NOTE: First byte contains version (high nibble) and IHL (low nibble)
        print(f"  IP Version: {read_data[0] >> 4}")
        print(f"  Header length: {(read_data[0] & 0x0F) * 4} bytes")
        
    except IOError as e:
        logger.error(f"I/O error: {e}")
        print(f"❌ Error during file operation: {e}")
        
    finally:
        # NOTE: Cleanup — delete the temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)
            print(f"\n🧹 Cleanup: temporary file deleted")


# ═══════════════════════════════════════════════════════════════════════════════
# INTERACTIVE_QUIZ
# ═══════════════════════════════════════════════════════════════════════════════
def quiz_bytes_vs_str() -> None:
    """Interactivee quiz to verify understanding.
    
    Tests knowledge about bytes vs str with practical questions.
    
    Returns:
        None. Displays the interactivee quiz.
    """
    print("\n" + "=" * 60)
    print("🗳️  QUIZ: Bytes vs Strings")
    print("=" * 60)
    
    print("""
🔮 PREDICTION: What happens when you run this code?

    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 8080))
    s.send("Hello")  # ← What happens here?

Options:
  A) The message "Hello" is sent successfully
  B) TypeError: a bytes-like object is required, not 'str'
  C) The message is sent but corrupted
  D) The socket blocks waiting

Correct answer: B

Explanation:
  Python 3 sockets accept ONLY bytes, not strings.
  Correct code: s.send(b"Hello") or s.send("Hello".encode())
  
  Why A is wrong: Python 3 strictly separated bytes from str
  Why C is wrong: Nothing is sent, error occurs first
  Why D is wrong: Error appears immediately, no blocking
""")


# ═══════════════════════════════════════════════════════════════════════════════
# USEFUL_HELPER_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def ensure_bytes(data) -> bytes:
    """Converts input to bytes, regardless of type.
    
    Args:
        data: str, bytes, or any object with __str__
        
    Returns:
        bytes: Bytes representation of the input
        
    Example:
        >>> ensure_bytes("Hello")
        b'Hello'
        >>> ensure_bytes(b"Hello")
        b'Hello'
    """
    if isinstance(data, bytes):
        return data
    if isinstance(data, str):
        return data.encode('utf-8')
    return str(data).encode('utf-8')


def ensure_str(data) -> str:
    """Converts input to str, regardless of type.
    
    Args:
        data: bytes, str, or any object
        
    Returns:
        str: String representation of the input
        
    Example:
        >>> ensure_str(b"Hello")
        'Hello'
        >>> ensure_str("Hello")
        'Hello'
    """
    if isinstance(data, str):
        return data
    if isinstance(data, bytes):
        return data.decode('utf-8', errors='replace')
    return str(data)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    try:
        demonlayere_conversion()
        demonlayere_encoding_errors()
        binary_file_example()
        quiz_bytes_vs_str()
        
        print("\n" + "=" * 60)
        print("✅ All demonlayerions completed successfully!")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
    except Exception as e:
        logger.exception(f"Aexpected error: {e}")
        print(f"\n❌ Aexpected error: {e}")
