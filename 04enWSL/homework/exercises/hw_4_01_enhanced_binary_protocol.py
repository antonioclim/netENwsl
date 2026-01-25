#!/usr/bin/env python3
"""
Week 4 Homework Assignment 1: Enhanced Binary Protocol
======================================================
Computer Networks - Week 4 (WSL Environment)
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Student: <Your Name>
Group: <Your Group>
Date: <Submission Date>

Description:
    Extend the BINARY protocol to support batch operations,
    subscriptions and additional header flags.

Requirements:
    - Implement MSG_BATCH, MSG_SUBSCRIBE, MSG_NOTIFY message types
    - Add flags field with compression and encryption support
    - Implement proper error handling

Level: Advanced
Estimated time: 90-120 minutes

Pair Programming Notes:
- Driver: Implement Message.to_bytes() and Message.from_bytes() first
- Navigator: Verify header format matches specification exactly
- Swap after: Message serialisation works correctly
- Second round - Driver: Implement batch operations
- Second round - Navigator: Track state changes in key-value store
"""

import socket
import struct
import threading
import zlib
from dataclasses import dataclass
from enum import IntEnum
from typing import Optional, Callable


# ═══════════════════════════════════════════════════════════════════════════════
# PROTOCOL_CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════════

MAGIC = b'NP'
VERSION = 1
DEFAULT_PORT = 5410  # Different port from lab exercise

# Original message types (from lab)
class MsgType(IntEnum):
    PING = 0x01
    PONG = 0x02
    SET = 0x03
    GET = 0x04
    DEL = 0x05
    RESPONSE = 0x06
    ERROR = 0x07
    # TODO: Add new message types
    # MSG_BATCH = 0x10
    # MSG_SUBSCRIBE = 0x11
    # MSG_NOTIFY = 0x12


# Protocol flags
class Flags(IntEnum):
    NONE = 0x00
    COMPRESSED = 0x01      # Bit 0: payload compressed with zlib
    ENCRYPTED = 0x02       # Bit 1: payload encrypted (XOR)
    # Add more flags as needed


# Error codes
class ErrorCode(IntEnum):
    OK = 0
    INVALID_MESSAGE = 1
    KEY_NOT_FOUND = 2
    INVALID_TYPE = 3
    COMPRESSION_ERROR = 4
    ENCRYPTION_ERROR = 5
    TIMEOUT = 6
    # TODO: Add more error codes as needed


# ═══════════════════════════════════════════════════════════════════════════════
# HEADER_STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════════

# Extended header format:
# Offset  Size  Field
# 0       2     Magic ('NP')
# 2       1     Version
# 3       1     Flags (NEW!)
# 4       1     Message Type
# 5       2     Payload Length
# 7       4     Sequence Number
# 11      4     CRC32
# Total: 15 bytes

HEADER_FORMAT = '!2sBBBHII'  # Network byte order
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)


@dataclass
class Message:
    """Protocol message structure."""
    version: int
    flags: int
    msg_type: int
    sequence: int
    payload: bytes
    
    def to_bytes(self) -> bytes:
        """Serialize message to bytes."""
        # TODO: Implement serialization
        # 1. Apply compression if COMPRESSED flag is set
        # 2. Apply encryption if ENCRYPTED flag is set
        # 3. Calculate CRC32
        # 4. Pack header and payload
        raise NotImplementedError("Implement message serialization")
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'Message':
        """Deserialize message from bytes."""
        # TODO: Implement deserialization
        # 1. Unpack header
        # 2. Verify CRC32
        # 3. Decrypt if ENCRYPTED flag is set
        # 4. Decompress if COMPRESSED flag is set
        raise NotImplementedError("Implement message deserialization")


# ═══════════════════════════════════════════════════════════════════════════════
# ENCRYPTION_HELPERS
# ═══════════════════════════════════════════════════════════════════════════════ (Simple XOR - for demonstration only!)
# ═══════════════════════════════════════════════════════════════════════════════

XOR_KEY = b'WEEK4SECRET'  # In real applications, use proper encryption!

def xor_encrypt(data: bytes) -> bytes:
    """Simple XOR encryption/decryption."""
    # TODO: Implement XOR encryption
    # Hint: XOR each byte with corresponding key byte (cycling)
    raise NotImplementedError("Implement XOR encryption")


def xor_decrypt(data: bytes) -> bytes:
    """XOR decryption (same as encryption for XOR)."""
    return xor_encrypt(data)


# ═══════════════════════════════════════════════════════════════════════════════
# CRC32_CALCULATION
# ═══════════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════════

def calculate_crc32(data: bytes) -> int:
    """Calculate CRC32 checksum."""
    import binascii
    return binascii.crc32(data) & 0xFFFFFFFF


# ═══════════════════════════════════════════════════════════════════════════════
# SERVER_IMPLEMENTATION
# ═══════════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════════

class EnhancedBinaryServer:
    """
    Enhanced binary protocol server with batch operations and subscriptions.
    """
    
    def __init__(self, host: str = '0.0.0.0', port: int = DEFAULT_PORT):
        self.host = host
        self.port = port
        self.socket: Optional[socket.socket] = None
        self.running = False
        
        # Key-value store
        self.store: dict[str, bytes] = {}
        self.store_lock = threading.Lock()
        
        # Subscriptions: key -> list of (client_addr, callback_socket)
        self.subscriptions: dict[str, list] = {}
        self.subscriptions_lock = threading.Lock()
        
        # Sequence number for server-initiated messages
        self.sequence = 0
        self.sequence_lock = threading.Lock()
    
    def get_next_sequence(self) -> int:
        """Get next sequence number (thread-safe)."""
        with self.sequence_lock:
            seq = self.sequence
            self.sequence = (self.sequence + 1) % (2**32)
            return seq
    
    def start(self):
        """Start the server."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        self.running = True
        
        print(f"Enhanced Binary Server listening on {self.host}:{self.port}")
        
        while self.running:
            try:
                client_socket, client_addr = self.socket.accept()
                print(f"Connection from {client_addr}")
                
                # Handle client in separate thread
                thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_addr)
                )
                thread.daemon = True
                thread.start()
                
            except socket.error:
                if self.running:
                    raise
    
    def handle_client(self, client_socket: socket.socket, client_addr: tuple):
        """Handle a single client connection."""
        try:
            while self.running:
                # TODO: Implement message handling
                # 1. Receive header (HEADER_SIZE bytes)
                # 2. Parse header to get payload length
                # 3. Receive payload
                # 4. Deserialize complete message
                # 5. Process based on message type
                # 6. Send response
                pass
                
        except Exception as e:
            print(f"Error handling client {client_addr}: {e}")
        finally:
            client_socket.close()
    
    def handle_batch(self, payload: bytes) -> tuple[ErrorCode, bytes]:
        """
        Handle MSG_BATCH message.
        
        Batch payload format:
            - 2 bytes: operation count
            - For each operation:
                - 1 byte: operation type (SET=0x03, GET=0x04, DEL=0x05)
                - 2 bytes: key length
                - N bytes: key
                - 2 bytes: value length (for SET only)
                - M bytes: value (for SET only)
        
        Returns:
            Tuple of (error_code, response_payload)
        """
        # TODO: Implement batch processing
        raise NotImplementedError("Implement batch message handling")
    
    def handle_subscribe(self, client_socket: socket.socket, 
                        payload: bytes) -> tuple[ErrorCode, bytes]:
        """
        Handle MSG_SUBSCRIBE message.
        
        Subscribe payload format:
            - 2 bytes: key length
            - N bytes: key
        
        Server should:
            1. Add client to subscription list for the key
            2. Send MSG_NOTIFY when key changes
        """
        # TODO: Implement subscription handling
        raise NotImplementedError("Implement subscription handling")
    
    def notify_subscribers(self, key: str, value: bytes):
        """Notify all subscribers when a key changes."""
        # TODO: Implement notification
        # 1. Get list of subscribers for key
        # 2. Build MSG_NOTIFY message
        # 3. Send to each subscriber
        raise NotImplementedError("Implement subscriber notification")
    
    def stop(self):
        """Stop the server."""
        self.running = False
        if self.socket:
            self.socket.close()


# ═══════════════════════════════════════════════════════════════════════════════
# CLIENT_IMPLEMENTATION
# ═══════════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════════

class EnhancedBinaryClient:
    """
    Enhanced binary protocol client.
    """
    
    def __init__(self, host: str = 'localhost', port: int = DEFAULT_PORT):
        self.host = host
        self.port = port
        self.socket: Optional[socket.socket] = None
        self.sequence = 0
        self.use_compression = False
        self.use_encryption = False
    
    def connect(self):
        """Connect to the server."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        print(f"Connected to {self.host}:{self.port}")
    
    def disconnect(self):
        """Disconnect from the server."""
        if self.socket:
            self.socket.close()
            self.socket = None
    
    def enable_compression(self, enabled: bool = True):
        """Enable or disable compression for subsequent messages."""
        self.use_compression = enabled
    
    def enable_encryption(self, enabled: bool = True):
        """Enable or disable encryption for subsequent messages."""
        self.use_encryption = enabled
    
    def get_next_sequence(self) -> int:
        """Get next sequence number."""
        seq = self.sequence
        self.sequence = (self.sequence + 1) % (2**32)
        return seq
    
    def send_message(self, msg_type: int, payload: bytes = b'') -> Message:
        """Send a message and wait for response."""
        # TODO: Implement send with flags
        # 1. Determine flags based on compression/encryption settings
        # 2. Build message
        # 3. Serialize and send
        # 4. Receive and deserialize response
        raise NotImplementedError("Implement message sending")
    
    def batch_operations(self, operations: list[tuple]) -> list:
        """
        Execute batch operations.
        
        Args:
            operations: List of (operation_type, key, value) tuples
                       value is None for GET and DEL
        
        Returns:
            List of results for each operation
        """
        # TODO: Implement batch client
        raise NotImplementedError("Implement batch operations")
    
    def subscribe(self, key: str, callback: Callable[[str, bytes], None]):
        """
        Subscribe to key changes.
        
        Args:
            key: Key to subscribe to
            callback: Function called with (key, new_value) when key changes
        """
        # TODO: Implement subscription client
        # Consider using a background thread to receive notifications
        raise NotImplementedError("Implement subscription")


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════════

def test_compression():
    """Test compression functionality."""
    original = b"Hello, this is a test message that should be compressed!"
    compressed = zlib.compress(original)
    decompressed = zlib.decompress(compressed)
    
    assert decompressed == original, "Compression/decompression failed"
    print(f"Compression test passed!")
    print(f"  Original size: {len(original)} bytes")
    print(f"  Compressed size: {len(compressed)} bytes")
    print(f"  Ratio: {len(compressed)/len(original):.2%}")


def test_encryption():
    """Test XOR encryption functionality."""
    original = b"Secret message to encrypt"
    encrypted = xor_encrypt(original)
    decrypted = xor_decrypt(encrypted)
    
    assert decrypted == original, "Encryption/decryption failed"
    assert encrypted != original, "Encryption should modify data"
    print("Encryption test passed!")


def test_message_serialization():
    """Test message serialization."""
    msg = Message(
        version=VERSION,
        flags=Flags.NONE,
        msg_type=MsgType.PING,
        sequence=1,
        payload=b''
    )
    
    data = msg.to_bytes()
    recovered = Message.from_bytes(data)
    
    assert recovered.version == msg.version
    assert recovered.flags == msg.flags
    assert recovered.msg_type == msg.msg_type
    assert recovered.sequence == msg.sequence
    assert recovered.payload == msg.payload
    print("Message serialization test passed!")


def test_batch_operations():
    """Test batch operations (requires running server)."""
    client = EnhancedBinaryClient()
    client.connect()
    
    try:
        operations = [
            (MsgType.SET, "key1", b"value1"),
            (MsgType.SET, "key2", b"value2"),
            (MsgType.GET, "key1", None),
            (MsgType.DEL, "key2", None),
        ]
        
        results = client.batch_operations(operations)
        print(f"Batch operations completed: {results}")
        
    finally:
        client.disconnect()


def main():
    """Main entry point for testing."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python hw_4_01.py <server|client|test>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "server":
        server = EnhancedBinaryServer()
        try:
            server.start()
        except KeyboardInterrupt:
            server.stop()
            print("\nServer stopped.")
    
    elif command == "client":
        # Interactive client mode
        client = EnhancedBinaryClient()
        client.connect()
        try:
            # TODO: Add interactive commands
            print("Interactive client mode - implement commands")
        finally:
            client.disconnect()
    
    elif command == "test":
        print("Running tests...")
        print("-" * 40)
        
        # These tests don't require server
        test_compression()
        test_encryption()
        # test_message_serialization()  # Uncomment after implementing
        
        print("-" * 40)
        print("Basic tests completed!")
        print("Note: Implement the TODO sections to run full tests.")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
