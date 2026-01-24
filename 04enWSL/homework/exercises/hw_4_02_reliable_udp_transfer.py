#!/usr/bin/env python3
"""
Week 4 Homework Assignment 2: Reliable UDP Protocol
====================================================
Computer Networks - Week 4 (WSL Environment)
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Student: <Your Name>
Group: <Your Group>
Date: <Submission Date>

Description:
    Design and implement a reliable data transfer protocol over UDP,
    featuring sequence numbers, acknowledgments, retransmission,
    and sliding window flow control.

Requirements:
    - Implement Stop-and-Wait or Go-Back-N reliability
    - Add sequence numbers and acknowledgments
    - Implement timeout-based retransmission
    - Transfer files with integrity verification

Level: Advanced
Estimated time: 120-150 minutes

Pair Programming Notes:
- Driver: Implement Packet.to_bytes() and Packet.from_bytes()
- Navigator: Verify header format and checksum calculation
- Swap after: Packet serialisation passes tests
- Second round - Driver: Implement RTT estimation
- Second round - Navigator: Check edge cases (timeout too short/long)
- Third round - Driver: Implement send_data() with window management
- Third round - Navigator: Track window state and retransmissions
"""

import socket
import struct
import threading
import hashlib
import time
import random
from dataclasses import dataclass
from enum import IntEnum
from typing import Optional, BinaryIO
from collections import deque


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════════

DEFAULT_PORT = 5420
WINDOW_SIZE = 4              # Sliding window size
INITIAL_TIMEOUT = 1.0        # Initial timeout in seconds
MAX_RETRIES = 5              # Maximum retransmission attempts
CHUNK_SIZE = 1024            # Payload size per packet
ALPHA = 0.125                # EWMA coefficient for RTT estimation


# ═══════════════════════════════════════════════════════════════════════════════
# PACKET_LOSS_SIMULATION
# ═══════════════════════════════════════════════════════════════════════════════ (for testing)
# ═══════════════════════════════════════════════════════════════════════════════

class PacketLossSimulator:
    """Simulate packet loss for testing reliability."""
    
    def __init__(self, loss_rate: float = 0.0):
        self.loss_rate = loss_rate
        self.packets_sent = 0
        self.packets_dropped = 0
    
    def should_drop(self) -> bool:
        """Determine if a packet should be dropped."""
        self.packets_sent += 1
        if random.random() < self.loss_rate:
            self.packets_dropped += 1
            return True
        return False
    
    def get_stats(self) -> dict:
        """Get loss statistics."""
        return {
            "sent": self.packets_sent,
            "dropped": self.packets_dropped,
            "actual_loss_rate": self.packets_dropped / max(1, self.packets_sent)
        }


# Global simulator (set loss_rate > 0 for testing)
loss_simulator = PacketLossSimulator(loss_rate=0.0)


# ═══════════════════════════════════════════════════════════════════════════════
# PROTOCOL_FLAGS
# ═══════════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════════

class Flags(IntEnum):
    """Packet flags."""
    DATA = 0x01      # Contains data
    ACK = 0x02       # Acknowledgment
    SYN = 0x04       # Synchronise (connection start)
    FIN = 0x08       # Finish (connection end)


# ═══════════════════════════════════════════════════════════════════════════════
# PACKET_STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════════

# Header format:
# Offset  Size  Field
# 0       4     Sequence Number
# 4       4     Acknowledgment Number
# 8       1     Flags
# 9       2     Window Size
# 11      2     Payload Length
# 13      4     Checksum (CRC32)
# Total: 17 bytes

HEADER_FORMAT = '!IIBHHI'
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)


@dataclass
class Packet:
    """Reliable UDP packet structure."""
    seq_num: int
    ack_num: int
    flags: int
    window: int
    payload: bytes
    
    def to_bytes(self) -> bytes:
        """Serialize packet to bytes."""
        # TODO: Implement serialization
        # 1. Calculate CRC32 of header (excluding checksum) + payload
        # 2. Pack header with checksum
        # 3. Append payload
        raise NotImplementedError("Implement packet serialization")
    
    @classmethod
    def from_bytes(cls, data: bytes) -> Optional['Packet']:
        """
        Deserialize packet from bytes.
        
        Returns:
            Packet object if valid, None if checksum fails
        """
        # TODO: Implement deserialization
        # 1. Unpack header
        # 2. Extract payload
        # 3. Verify checksum
        # 4. Return Packet or None
        raise NotImplementedError("Implement packet deserialization")
    
    def is_data(self) -> bool:
        return bool(self.flags & Flags.DATA)
    
    def is_ack(self) -> bool:
        return bool(self.flags & Flags.ACK)
    
    def is_syn(self) -> bool:
        return bool(self.flags & Flags.SYN)
    
    def is_fin(self) -> bool:
        return bool(self.flags & Flags.FIN)


def calculate_checksum(data: bytes) -> int:
    """Calculate CRC32 checksum."""
    import binascii
    return binascii.crc32(data) & 0xFFFFFFFF


# ═══════════════════════════════════════════════════════════════════════════════
# RTT_ESTIMATION
# ═══════════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════════

class RTTEstimator:
    """
    Estimate round-trip time using Exponential Weighted Moving Average.
    """
    
    def __init__(self, initial_rtt: float = INITIAL_TIMEOUT):
        self.estimated_rtt = initial_rtt
        self.dev_rtt = initial_rtt / 4  # RTT deviation
        self.alpha = ALPHA
        self.beta = 0.25
    
    def update(self, sample_rtt: float):
        """Update RTT estimate with new sample."""
        # TODO: Implement EWMA RTT estimation
        # estimated_rtt = (1 - alpha) * estimated_rtt + alpha * sample_rtt
        # dev_rtt = (1 - beta) * dev_rtt + beta * |sample_rtt - estimated_rtt|
        raise NotImplementedError("Implement RTT estimation")
    
    def get_timeout(self) -> float:
        """Calculate timeout based on current estimates."""
        # TODO: Return timeout value
        # timeout = estimated_rtt + 4 * dev_rtt
        raise NotImplementedError("Implement timeout calculation")


# ═══════════════════════════════════════════════════════════════════════════════
# RELIABLE_SENDER
# ═══════════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════════

class ReliableSender:
    """
    Reliable UDP sender with sliding window.
    """
    
    def __init__(self, dest_host: str, dest_port: int = DEFAULT_PORT):
        self.dest_host = dest_host
        self.dest_port = dest_port
        self.socket: Optional[socket.socket] = None
        
        # Sliding window state
        self.base = 0              # Oldest unacknowledged sequence number
        self.next_seq = 0          # Next sequence number to use
        self.window_size = WINDOW_SIZE
        
        # Buffer for unacknowledged packets
        self.send_buffer: dict[int, tuple[Packet, float]] = {}  # seq -> (packet, send_time)
        self.buffer_lock = threading.Lock()
        
        # RTT estimation
        self.rtt_estimator = RTTEstimator()
        
        # Statistics
        self.stats = {
            "packets_sent": 0,
            "retransmissions": 0,
            "bytes_sent": 0,
            "acks_received": 0,
            "duplicate_acks": 0
        }
        
        # Receiver thread for ACKs
        self.running = False
        self.ack_thread: Optional[threading.Thread] = None
    
    def connect(self):
        """Initialise UDP socket and start ACK receiver."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(0.1)  # Non-blocking for receiver thread
        
        # Start ACK receiver thread
        self.running = True
        self.ack_thread = threading.Thread(target=self._ack_receiver)
        self.ack_thread.daemon = True
        self.ack_thread.start()
        
        # Send SYN to initiate connection
        # TODO: Implement connection establishment
        print(f"Connected to {self.dest_host}:{self.dest_port}")
    
    def disconnect(self):
        """Close connection."""
        # TODO: Send FIN and wait for ACK
        self.running = False
        if self.ack_thread:
            self.ack_thread.join(timeout=2.0)
        if self.socket:
            self.socket.close()
    
    def _ack_receiver(self):
        """Background thread to receive ACKs."""
        while self.running:
            try:
                data, addr = self.socket.recvfrom(HEADER_SIZE + 100)
                packet = Packet.from_bytes(data)
                
                if packet and packet.is_ack():
                    self._process_ack(packet)
                    
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"ACK receiver error: {e}")
    
    def _process_ack(self, ack_packet: Packet):
        """Process received ACK."""
        # TODO: Implement ACK processing
        # 1. Update RTT estimate if this ACK is for a timed packet
        # 2. Remove acknowledged packets from buffer
        # 3. Slide window forward
        # 4. Detect duplicate ACKs for fast retransmit
        raise NotImplementedError("Implement ACK processing")
    
    def _send_packet(self, packet: Packet, retransmit: bool = False):
        """Send a packet (possibly retransmission)."""
        # Apply packet loss simulation
        if loss_simulator.should_drop():
            print(f"[SIM] Dropped packet seq={packet.seq_num}")
            return
        
        data = packet.to_bytes()
        self.socket.sendto(data, (self.dest_host, self.dest_port))
        
        # Update statistics
        self.stats["packets_sent"] += 1
        if retransmit:
            self.stats["retransmissions"] += 1
        else:
            self.stats["bytes_sent"] += len(packet.payload)
    
    def _check_timeouts(self):
        """Check for timed-out packets and retransmit."""
        # TODO: Implement timeout checking
        # 1. Get current timeout value from RTT estimator
        # 2. Check each packet in send buffer
        # 3. Retransmit if timed out
        # 4. Update retry count
        raise NotImplementedError("Implement timeout checking")
    
    def send_data(self, data: bytes):
        """
        Send data reliably.
        
        This is the main sending interface.
        """
        # TODO: Implement reliable sending
        # 1. Split data into chunks
        # 2. Create packets with sequence numbers
        # 3. Send within window limit
        # 4. Wait for ACKs / handle retransmissions
        raise NotImplementedError("Implement reliable send")
    
    def send_file(self, filepath: str) -> dict:
        """
        Send a file reliably.
        
        Returns:
            Transfer statistics including SHA-256 hash
        """
        # TODO: Implement file transfer
        # 1. Read file in chunks
        # 2. Calculate SHA-256 hash
        # 3. Send file size and hash in first packet
        # 4. Send file data
        # 5. Return statistics
        raise NotImplementedError("Implement file transfer")
    
    def get_stats(self) -> dict:
        """Get transfer statistics."""
        return {
            **self.stats,
            "loss_simulation": loss_simulator.get_stats()
        }


# ═══════════════════════════════════════════════════════════════════════════════
# RELIABLE_RECEIVER
# ═══════════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════════

class ReliableReceiver:
    """
    Reliable UDP receiver.
    """
    
    def __init__(self, port: int = DEFAULT_PORT):
        self.port = port
        self.socket: Optional[socket.socket] = None
        
        # Receiver state
        self.expected_seq = 0      # Next expected sequence number
        self.recv_window = WINDOW_SIZE
        
        # Buffer for out-of-order packets
        self.recv_buffer: dict[int, Packet] = {}
        
        # Received data
        self.received_data = bytearray()
        
        # Statistics
        self.stats = {
            "packets_received": 0,
            "bytes_received": 0,
            "acks_sent": 0,
            "out_of_order": 0,
            "duplicates": 0
        }
        
        self.running = False
    
    def start(self):
        """Start receiver."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('0.0.0.0', self.port))
        self.running = True
        
        print(f"Receiver listening on port {self.port}")
    
    def stop(self):
        """Stop receiver."""
        self.running = False
        if self.socket:
            self.socket.close()
    
    def _send_ack(self, ack_num: int, dest_addr: tuple):
        """Send ACK for received packet."""
        # Apply packet loss simulation to ACKs too
        if loss_simulator.should_drop():
            print(f"[SIM] Dropped ACK for seq={ack_num}")
            return
        
        ack_packet = Packet(
            seq_num=0,
            ack_num=ack_num,
            flags=Flags.ACK,
            window=self.recv_window,
            payload=b''
        )
        
        self.socket.sendto(ack_packet.to_bytes(), dest_addr)
        self.stats["acks_sent"] += 1
    
    def receive_data(self, timeout: float = 30.0) -> bytes:
        """
        Receive data reliably.
        
        Returns:
            Complete received data
        """
        # TODO: Implement reliable receiving
        # 1. Receive packets
        # 2. Check sequence numbers
        # 3. Buffer out-of-order packets
        # 4. Deliver in-order data
        # 5. Send ACKs
        raise NotImplementedError("Implement reliable receive")
    
    def receive_file(self, output_path: str, timeout: float = 60.0) -> dict:
        """
        Receive a file reliably.
        
        Returns:
            Transfer statistics including verification result
        """
        # TODO: Implement file reception
        # 1. Receive file metadata (size, hash)
        # 2. Receive file data
        # 3. Write to output file
        # 4. Verify SHA-256 hash
        # 5. Return statistics
        raise NotImplementedError("Implement file reception")
    
    def get_stats(self) -> dict:
        """Get reception statistics."""
        return self.stats


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════════

def test_packet_serialization():
    """Test packet serialization and deserialization."""
    packet = Packet(
        seq_num=12345,
        ack_num=0,
        flags=Flags.DATA,
        window=WINDOW_SIZE,
        payload=b"Hello, reliable UDP!"
    )
    
    data = packet.to_bytes()
    recovered = Packet.from_bytes(data)
    
    assert recovered is not None, "Deserialization returned None"
    assert recovered.seq_num == packet.seq_num
    assert recovered.ack_num == packet.ack_num
    assert recovered.flags == packet.flags
    assert recovered.payload == packet.payload
    
    print("Packet serialization test passed!")


def test_checksum_corruption():
    """Test that corrupted packets are detected."""
    packet = Packet(
        seq_num=1,
        ack_num=0,
        flags=Flags.DATA,
        window=4,
        payload=b"Test data"
    )
    
    data = bytearray(packet.to_bytes())
    
    # Corrupt one byte
    data[5] ^= 0xFF
    
    recovered = Packet.from_bytes(bytes(data))
    assert recovered is None, "Corrupted packet should return None"
    
    print("Checksum corruption test passed!")


def test_rtt_estimation():
    """Test RTT estimation."""
    estimator = RTTEstimator(initial_rtt=1.0)
    
    # Simulate some RTT samples
    samples = [0.8, 0.9, 1.1, 0.95, 1.0]
    
    for sample in samples:
        estimator.update(sample)
        timeout = estimator.get_timeout()
        print(f"  Sample: {sample:.2f}s -> Timeout: {timeout:.2f}s")
    
    # Timeout should be reasonable (not too high or low)
    final_timeout = estimator.get_timeout()
    assert 0.5 < final_timeout < 5.0, f"Timeout {final_timeout} seems unreasonable"
    
    print("RTT estimation test passed!")


def test_local_transfer():
    """Test local transfer (requires running receiver)."""
    print("\nStarting local transfer test...")
    print("Note: Start receiver first: python hw_4_02.py receiver")
    
    sender = ReliableSender('localhost')
    sender.connect()
    
    try:
        test_data = b"Hello, this is a test of reliable UDP transfer! " * 100
        print(f"Sending {len(test_data)} bytes...")
        
        sender.send_data(test_data)
        
        print("Transfer complete!")
        print(f"Statistics: {sender.get_stats()}")
        
    finally:
        sender.disconnect()


def test_with_loss(loss_rate: float = 0.1):
    """Test transfer with simulated packet loss."""
    global loss_simulator
    loss_simulator = PacketLossSimulator(loss_rate=loss_rate)
    
    print(f"\nTesting with {loss_rate*100:.0f}% packet loss...")
    test_local_transfer()
    
    print(f"\nLoss simulation stats: {loss_simulator.get_stats()}")


# ═══════════════════════════════════════════════════════════════════════════════
# PERFORMANCE_ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════════

def analyze_performance(results: list[dict]) -> None:
    """
    Analyse and display performance results.
    
    Args:
        results: List of test results with different loss rates
    """
    print("\n" + "=" * 60)
    print("Performance Analysis")
    print("=" * 60)
    
    print(f"{'Loss Rate':>12} {'Throughput':>12} {'Retrans':>12} {'Time':>12}")
    print("-" * 60)
    
    for r in results:
        print(f"{r['loss_rate']*100:>10.0f}% "
              f"{r['throughput']:>10.2f} KB/s "
              f"{r['retransmissions']:>10} "
              f"{r['time']:>10.2f}s")
    
    print("=" * 60)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Main entry point."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python hw_4_02.py <sender|receiver|test|benchmark>")
        print("")
        print("Commands:")
        print("  sender [host] [file]  - Send data/file to receiver")
        print("  receiver [output]     - Receive data/file")
        print("  test                  - Run unit tests")
        print("  benchmark             - Run performance benchmark")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "sender":
        host = sys.argv[2] if len(sys.argv) > 2 else 'localhost'
        filepath = sys.argv[3] if len(sys.argv) > 3 else None
        
        sender = ReliableSender(host)
        sender.connect()
        
        try:
            if filepath:
                print(f"Sending file: {filepath}")
                stats = sender.send_file(filepath)
                print(f"File transfer statistics: {stats}")
            else:
                # Interactive mode
                print("Enter data to send (Ctrl+D to finish):")
                data = sys.stdin.buffer.read()
                sender.send_data(data)
                print(f"Statistics: {sender.get_stats()}")
        finally:
            sender.disconnect()
    
    elif command == "receiver":
        output_path = sys.argv[2] if len(sys.argv) > 2 else None
        
        receiver = ReliableReceiver()
        receiver.start()
        
        try:
            if output_path:
                print(f"Receiving file to: {output_path}")
                stats = receiver.receive_file(output_path)
                print(f"File reception statistics: {stats}")
            else:
                print("Receiving data...")
                data = receiver.receive_data()
                print(f"Received {len(data)} bytes")
                print(f"Statistics: {receiver.get_stats()}")
        except KeyboardInterrupt:
            print("\nReceiver stopped.")
        finally:
            receiver.stop()
    
    elif command == "test":
        print("Running unit tests...")
        print("-" * 40)
        
        # Tests that don't require network
        # test_packet_serialization()  # Uncomment after implementing
        # test_checksum_corruption()   # Uncomment after implementing
        # test_rtt_estimation()        # Uncomment after implementing
        
        print("-" * 40)
        print("Note: Implement the TODO sections to run all tests.")
        print("For network tests, start receiver first.")
    
    elif command == "benchmark":
        print("Running performance benchmark...")
        print("Note: Start receiver first: python hw_4_02.py receiver")
        
        results = []
        
        for loss_rate in [0.0, 0.05, 0.10, 0.20, 0.30]:
            global loss_simulator
            loss_simulator = PacketLossSimulator(loss_rate=loss_rate)
            
            # TODO: Implement actual benchmark
            # Run transfer and collect statistics
            print(f"Testing with {loss_rate*100:.0f}% loss...")
        
        analyze_performance(results)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
