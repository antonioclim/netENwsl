#!/usr/bin/env python3
"""ex_14_03_advanced_challenges.py — Advanced exercises (challenge) for Week 14.

Computer Networks — Week 14 (WSL Environment)
ASE Bucharest, CSIE | by ing. dr. Antonio Clim

Objectives:
- Implement custom binary protocols using struct
- Analyse packet captures programmatically
- Evaluate system performance through benchmarking

Level: Advanced
Estimated time: 45-60 minutes

Pair Programming Notes:
- Driver: Implement protocol encoding/decoding
- Navigator: Verify byte-level correctness, test edge cases
- Swap after: Each challenge completion

Usage:
  python3 ex_14_03_advanced_challenges.py --challenge echo
  python3 ex_14_03_advanced_challenges.py --challenge analyse
  python3 ex_14_03_advanced_challenges.py --challenge benchmark
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import argparse
import json
import socket
import struct
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple


# ═══════════════════════════════════════════════════════════════════════════════
# PREDICTION_PROMPT
# ═══════════════════════════════════════════════════════════════════════════════
def prompt_prediction(challenge: str) -> None:
    """Ask student to predict challenge outcome."""
    predictions = {
        "echo": "What will happen if the client sends a malformed header?",
        "analyse": "What percentage of packets in a typical capture are TCP vs UDP?",
        "benchmark": "How many requests per second can the load balancer handle?"
    }
    question = predictions.get(challenge, "What do you expect to happen?")
    print(f"\n💭 PREDICTION: {question}")
    try:
        prediction = input("   Your answer: ").strip()
        if prediction:
            print(f"   Let's find out!\n")
    except (EOFError, KeyboardInterrupt):
        print("\n")


# ═══════════════════════════════════════════════════════════════════════════════
# CHALLENGE 1: EXTENDED_ECHO_PROTOCOL
# ═══════════════════════════════════════════════════════════════════════════════
def challenge_echo_protocol():
    """
    Challenge: Implement an extended echo protocol.
    
    Protocol:
    - Header: [magic:2][version:1][cmd:1][length:4] = 8 bytes
    - Payload: [length] bytes
    
    Commands:
    - 0x01: ECHO (responds with same payload)
    - 0x02: REVERSE (responds with reversed payload)
    - 0x03: UPPER (responds with payload in uppercase)
    - 0x04: INFO (responds with server info)
    """
    
    MAGIC = b'\xCA\xFE'
    VERSION = 1
    
    CMD_ECHO = 0x01
    CMD_REVERSE = 0x02
    CMD_UPPER = 0x03
    CMD_INFO = 0x04
    
    print("\n" + "=" * 60)
    print("  Challenge: Extended Echo Protocol")
    print("=" * 60)
    print("""
Implement a server and client for the protocol above.

Header structure (8 bytes):
  - magic    (2 bytes): 0xCAFE
  - version  (1 byte):  1
  - cmd      (1 byte):  command type
  - length   (4 bytes): payload length (big-endian)

Available commands:
  0x01 ECHO    - Returns payload unmodified
  0x02 REVERSE - Returns reversed payload
  0x03 UPPER   - Returns payload in uppercase
  0x04 INFO    - Returns server information (JSON)

Example implementation (incomplete):
""")
    
    # Example starter code
    starter_code = '''
def pack_message(cmd: int, payload: bytes) -> bytes:
    """Packs a message according to the protocol."""
    magic = b'\\xCA\\xFE'
    version = struct.pack("B", 1)
    cmd_byte = struct.pack("B", cmd)
    length = struct.pack(">I", len(payload))
    return magic + version + cmd_byte + length + payload

def parse_header(data: bytes) -> Tuple[int, int, int]:
    """Parses the header and returns (version, cmd, length)."""
    if len(data) < 8:
        raise ValueError("Incomplete header")
    if data[:2] != b'\\xCA\\xFE':
        raise ValueError("Invalid magic")
    version = struct.unpack("B", data[2:3])[0]
    cmd = struct.unpack("B", data[3:4])[0]
    length = struct.unpack(">I", data[4:8])[0]
    return version, cmd, length

# TODO: Implement server and client
# Server: listen on port 9090, process commands
# Client: send commands, display responses
'''
    print(starter_code)
    
    print("""
Tasks:
1. Complete the functions above
2. Implement the server (hint: socket.socket, bind, listen, accept)
3. Implement the client (hint: socket.socket, connect, send, recv)
4. Test all 4 commands
5. Add error handling (timeout, connection refused, etc.)

Bonus:
- Add support for multiple connections (threading or select)
- Implement a new command (e.g.: HASH - returns SHA256)
- Add logging with timestamp for each command
""")
    
    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# CHALLENGE 2: PCAP_ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
def challenge_analyse_pcap():
    """
    Challenge: Implement a simple pcap analyser.
    """
    
    print("\n" + "=" * 60)
    print("  Challenge: PCAP Analysis")
    print("=" * 60)
    print("""
Implement a Python script that analyses a pcap file
and extracts useful statistics.

Requirements:
1. Parse the global pcap header (24 bytes)
2. Parse each packet header + data
3. Extract and count:
   - Packets per protocol (TCP/UDP/ICMP)
   - Top 5 source IP addresses
   - Top 5 destination ports
   - Unique TCP conversations (src_ip:src_port -> dst_ip:dst_port)

PCAP structure:
  Global Header (24 bytes):
    - magic_number (4 bytes): 0xa1b2c3d4 or 0xd4c3b2a1
    - version_major (2 bytes)
    - version_minor (2 bytes)
    - thiszone (4 bytes)
    - sigfigs (4 bytes)
    - snaplen (4 bytes)
    - network (4 bytes): 1 = Ethernet

  Per-Packet Header (16 bytes):
    - ts_sec (4 bytes)
    - ts_usec (4 bytes)
    - incl_len (4 bytes): bytes captured
    - orig_len (4 bytes): original length

  Ethernet Header (14 bytes):
    - dst_mac (6 bytes)
    - src_mac (6 bytes)
    - ethertype (2 bytes): 0x0800 = IPv4

  IP Header (20+ bytes):
    - version_ihl (1 byte): version=4, ihl=header_length/4
    - ...
    - protocol (1 byte, offset 9): 6=TCP, 17=UDP, 1=ICMP
    - src_ip (4 bytes, offset 12)
    - dst_ip (4 bytes, offset 16)

Example starter code:
""")
    
    starter_code = '''
import struct
from collections import Counter

def analyse_pcap(filepath: str) -> Dict[str, Any]:
    """Analyses a pcap file and returns statistics."""
    
    stats = {
        "packets": 0,
        "protocols": Counter(),
        "src_ips": Counter(),
        "dst_ports": Counter(),
        "conversations": set(),
    }
    
    with open(filepath, "rb") as f:
        # Read global header (24 bytes)
        global_header = f.read(24)
        magic = struct.unpack("<I", global_header[:4])[0]
        
        # Check endianness
        if magic == 0xa1b2c3d4:
            endian = "<"  # little-endian
        elif magic == 0xd4c3b2a1:
            endian = ">"  # big-endian
        else:
            raise ValueError("Invalid pcap magic")
        
        while True:
            # Read packet header (16 bytes)
            pkt_header = f.read(16)
            if len(pkt_header) < 16:
                break
            
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack(
                f"{endian}IIII", pkt_header
            )
            
            # Read packet data
            pkt_data = f.read(incl_len)
            if len(pkt_data) < incl_len:
                break
            
            stats["packets"] += 1
            
            # TODO: Parse Ethernet header
            # TODO: Parse IP header
            # TODO: Extract protocol, IPs, ports
            # TODO: Update statistics
    
    return stats
'''
    print(starter_code)
    
    print("""
Tasks:
1. Complete the analyse_pcap() function
2. Implement Ethernet and IP header parsing
3. Extract and count protocols
4. Identify TCP conversations
5. Display a formatted report

Testing:
  python3 ex_14_03.py --challenge analyse --pcap artifacts/demo.pcap

Bonus:
- Add support for IPv6
- Calculate total capture duration
- Identify possible port scans
""")
    
    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# CHALLENGE 3: HTTP_BENCHMARK
# ═══════════════════════════════════════════════════════════════════════════════
def challenge_benchmark():
    """
    Challenge: Implement a simple HTTP benchmark.
    """
    
    print("\n" + "=" * 60)
    print("  Challenge: HTTP Benchmark")
    print("=" * 60)
    print("""
Implement an HTTP benchmark tool similar to Apache Bench (ab).

Requirements:
1. Accept parameters: URL, number of requests, concurrency
2. Send HTTP GET requests
3. Measure and report:
   - Total time
   - Requests per second
   - Time per request (mean)
   - Time per request (across all concurrent)
   - Transfer rate
   - Connection times (min, mean, max)
   - Percentile latencies (50%, 90%, 99%)

Example starter code:
""")
    
    starter_code = '''
import threading
import time
from queue import Queue
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

def http_worker(url: str, results: Queue, timeout: float = 5.0):
    """Worker thread for HTTP requests."""
    try:
        start = time.time()
        req = Request(url, method="GET")
        with urlopen(req, timeout=timeout) as response:
            data = response.read()
            latency = time.time() - start
            results.put({
                "success": True,
                "status": response.status,
                "latency": latency,
                "bytes": len(data),
            })
    except Exception as e:
        latency = time.time() - start
        results.put({
            "success": False,
            "error": str(e),
            "latency": latency,
        })

def run_benchmark(url: str, n_requests: int, concurrency: int) -> Dict:
    """Runs the benchmark."""
    results = Queue()
    threads = []
    
    start_time = time.time()
    
    # TODO: Implement concurrency logic
    # - Start `concurrency` threads
    # - Distribute `n_requests` requests among them
    # - Collect results
    
    total_time = time.time() - start_time
    
    # TODO: Calculate and return statistics
    return {
        "total_time": total_time,
        "requests": n_requests,
        "concurrency": concurrency,
        # ... other statistics
    }
'''
    print(starter_code)
    
    print("""
Tasks:
1. Complete the concurrency logic with threads
2. Implement statistics calculation
3. Display a report similar to `ab`
4. Add progress indicator

Desired usage:
  python3 ex_14_03.py --challenge benchmark \\
    --url http://10.0.14.10:8080/ \\
    --requests 100 \\
    --concurrency 10

Expected output:
  Server Hostname:        10.0.14.10
  Server Port:            8080
  Document Path:          /
  Concurrency Level:      10
  Time taken for tests:   1.234 seconds
  Complete requests:      100
  Failed requests:        0
  Requests per second:    81.04 [#/sec]
  Time per request:       123.4 [ms] (mean)
  
  Connection Times (ms)
                min   mean    max
  Connect:        1     5     15
  Processing:    10    50    200
  Total:         11    55    215
  
  Percentage of requests served within a certain time (ms)
    50%     45
    90%    120
    99%    200

Bonus:
- Add support for POST with payload
- Implement keep-alive connections
- Add results export in JSON/CSV
""")
    
    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# PARSE_ARGUMENTS
# ═══════════════════════════════════════════════════════════════════════════════
def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Advanced exercises W14")
    parser.add_argument(
        "--challenge",
        choices=["echo", "analyse", "benchmark"],
        required=True,
        help="Choose the challenge"
    )
    parser.add_argument("--pcap", help="pcap file for analyse")
    parser.add_argument("--url", help="URL for benchmark")
    parser.add_argument("--requests", type=int, default=100, help="Number of requests")
    parser.add_argument("--concurrency", type=int, default=10, help="Concurrency")
    parser.add_argument("--predict", "-p", action="store_true",
                        help="Enable prediction prompt")
    return parser.parse_args()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point."""
    args = parse_args()
    
    if args.predict:
        prompt_prediction(args.challenge)
    
    if args.challenge == "echo":
        return challenge_echo_protocol()
    elif args.challenge == "analyse":
        return challenge_analyse_pcap()
    elif args.challenge == "benchmark":
        return challenge_benchmark()
    else:
        print(f"Unknown challenge: {args.challenge}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
