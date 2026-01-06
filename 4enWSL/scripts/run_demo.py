#!/usr/bin/env python3
"""
Automated Demonstration Script
NETWORKING class - ASE, Informatics | by Revolvix

Runs automated demonstrations of Week 4 protocol implementations.
"""

import subprocess
import sys
import time
import threading
import argparse
from pathlib import Path
from queue import Queue

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.logger import setup_logger
from scripts.utils.network_utils import NetworkUtils

logger = setup_logger("demo")


def run_with_output(cmd: list, label: str, output_queue: Queue = None) -> int:
    """
    Run a command and optionally capture output.
    
    Args:
        cmd: Command to run
        label: Label for output
        output_queue: Optional queue for capturing output
    
    Returns:
        Return code
    """
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        for line in process.stdout:
            line = line.rstrip()
            if output_queue:
                output_queue.put((label, line))
            else:
                logger.info(f"[{label}] {line}")
        
        process.wait()
        return process.returncode
    except Exception as e:
        logger.error(f"[{label}] Error: {e}")
        return 1


def demo_text_protocol():
    """Demonstrate TEXT protocol communication."""
    logger.info("")
    logger.info("=" * 60)
    logger.info("Demo 1: TEXT Protocol over TCP")
    logger.info("=" * 60)
    logger.info("")
    
    src_dir = PROJECT_ROOT / "src" / "apps"
    server_script = src_dir / "text_proto_server.py"
    client_script = src_dir / "text_proto_client.py"
    
    if not server_script.exists():
        logger.error(f"Server script not found: {server_script}")
        return False
    
    # Start server in background
    logger.info("Starting TEXT protocol server on port 5400...")
    server_proc = subprocess.Popen(
        [sys.executable, str(server_script), "--port", "5400"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    time.sleep(2)
    
    # Wait for server to be ready
    if not NetworkUtils.wait_for_port("localhost", 5400, timeout=10):
        logger.error("Server failed to start")
        server_proc.terminate()
        return False
    
    logger.info("Server ready!")
    logger.info("")
    
    # Run client commands
    commands = [
        "PING",
        "SET name Alice",
        "SET city Bucharest",
        "SET course Networks",
        "GET name",
        "GET city",
        "COUNT",
        "KEYS",
        "DEL city",
        "COUNT",
        "QUIT"
    ]
    
    logger.info("Executing client commands:")
    logger.info("-" * 40)
    
    for cmd in commands:
        logger.info(f"  >>> {cmd}")
        
        if client_script.exists():
            result = subprocess.run(
                [sys.executable, str(client_script), 
                 "--host", "localhost", "--port", "5400",
                 "-c", cmd],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.stdout.strip():
                for line in result.stdout.strip().split("\n"):
                    if line.strip():
                        logger.info(f"  <<< {line.strip()}")
        
        time.sleep(0.5)
    
    logger.info("-" * 40)
    logger.info("")
    
    # Stop server
    server_proc.terminate()
    server_proc.wait()
    
    logger.info("TEXT protocol demo complete!")
    return True


def demo_binary_protocol():
    """Demonstrate BINARY protocol communication."""
    logger.info("")
    logger.info("=" * 60)
    logger.info("Demo 2: BINARY Protocol over TCP")
    logger.info("=" * 60)
    logger.info("")
    
    src_dir = PROJECT_ROOT / "src" / "apps"
    server_script = src_dir / "binary_proto_server.py"
    client_script = src_dir / "binary_proto_client.py"
    
    if not server_script.exists():
        logger.error(f"Server script not found: {server_script}")
        return False
    
    # Start server
    logger.info("Starting BINARY protocol server on port 5401...")
    server_proc = subprocess.Popen(
        [sys.executable, str(server_script), "--port", "5401"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    time.sleep(2)
    
    if not NetworkUtils.wait_for_port("localhost", 5401, timeout=10):
        logger.error("Server failed to start")
        server_proc.terminate()
        return False
    
    logger.info("Server ready!")
    logger.info("")
    
    # Run client commands
    commands = [
        ("echo", "Hello Binary World!"),
        ("put", "username admin"),
        ("put", "password secret123"),
        ("get", "username"),
        ("count", ""),
        ("keys", ""),
    ]
    
    logger.info("Executing binary protocol commands:")
    logger.info("-" * 40)
    
    for cmd, arg in commands:
        full_cmd = f"{cmd} {arg}".strip()
        logger.info(f"  >>> {full_cmd}")
        
        if client_script.exists():
            result = subprocess.run(
                [sys.executable, str(client_script),
                 "--host", "localhost", "--port", "5401",
                 "-c", full_cmd],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.stdout.strip():
                for line in result.stdout.strip().split("\n"):
                    if line.strip() and not line.startswith("["):
                        logger.info(f"  <<< {line.strip()}")
        
        time.sleep(0.5)
    
    logger.info("-" * 40)
    logger.info("")
    
    server_proc.terminate()
    server_proc.wait()
    
    logger.info("BINARY protocol demo complete!")
    return True


def demo_udp_sensor():
    """Demonstrate UDP sensor protocol."""
    logger.info("")
    logger.info("=" * 60)
    logger.info("Demo 3: UDP Sensor Protocol")
    logger.info("=" * 60)
    logger.info("")
    
    src_dir = PROJECT_ROOT / "src" / "apps"
    server_script = src_dir / "udp_sensor_server.py"
    client_script = src_dir / "udp_sensor_client.py"
    
    if not server_script.exists():
        logger.error(f"Server script not found: {server_script}")
        return False
    
    # Start server
    logger.info("Starting UDP sensor server on port 5402...")
    server_proc = subprocess.Popen(
        [sys.executable, str(server_script), "--port", "5402"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    time.sleep(2)
    logger.info("Server ready!")
    logger.info("")
    
    # Simulate sensor readings
    sensors = [
        (1001, 22.5, "Lab_A"),
        (1002, 23.1, "Lab_B"),
        (1003, 21.8, "Office"),
        (1001, 22.7, "Lab_A"),
        (1002, 23.3, "Lab_B"),
        (2001, 18.5, "Exterior"),
    ]
    
    logger.info("Simulating sensor readings:")
    logger.info("-" * 40)
    
    for sensor_id, temp, location in sensors:
        logger.info(f"  Sensor {sensor_id} @ {location}: {temp}°C")
        
        if client_script.exists():
            subprocess.run(
                [sys.executable, str(client_script),
                 "--host", "localhost", "--port", "5402",
                 "--sensor-id", str(sensor_id),
                 "--temp", str(temp),
                 "--location", location],
                capture_output=True,
                timeout=5
            )
        
        time.sleep(0.3)
    
    logger.info("-" * 40)
    logger.info("")
    
    # Test corrupt packet
    logger.info("Testing CRC validation with corrupt packet...")
    if client_script.exists():
        result = subprocess.run(
            [sys.executable, str(client_script),
             "--host", "localhost", "--port", "5402",
             "--sensor-id", "9999",
             "--temp", "0.0",
             "--location", "TEST",
             "--corrupt"],
            capture_output=True,
            text=True,
            timeout=5
        )
        logger.info("  Corrupt packet sent (should be rejected by server)")
    
    time.sleep(1)
    
    server_proc.terminate()
    server_proc.wait()
    
    logger.info("")
    logger.info("UDP sensor demo complete!")
    return True


def demo_error_detection():
    """Demonstrate CRC32 error detection."""
    logger.info("")
    logger.info("=" * 60)
    logger.info("Demo 4: CRC32 Error Detection")
    logger.info("=" * 60)
    logger.info("")
    
    import struct
    import zlib
    
    # Create sample packet
    data = b"Hello, Network!"
    
    # Calculate CRC32
    crc = zlib.crc32(data) & 0xFFFFFFFF
    
    logger.info("Original data: " + repr(data))
    logger.info(f"CRC32: {crc:08X}")
    logger.info("")
    
    # Verify intact packet
    packet = data + struct.pack(">I", crc)
    received_crc = struct.unpack(">I", packet[-4:])[0]
    calculated_crc = zlib.crc32(packet[:-4]) & 0xFFFFFFFF
    
    logger.info("Verification of intact packet:")
    logger.info(f"  Received CRC:   {received_crc:08X}")
    logger.info(f"  Calculated CRC: {calculated_crc:08X}")
    logger.info(f"  Match: {received_crc == calculated_crc}")
    logger.info("")
    
    # Corrupt packet (flip one bit)
    corrupted = bytearray(data)
    corrupted[0] ^= 0x01  # Flip one bit
    corrupted = bytes(corrupted)
    
    corrupted_packet = corrupted + struct.pack(">I", crc)  # Keep original CRC
    received_crc = struct.unpack(">I", corrupted_packet[-4:])[0]
    calculated_crc = zlib.crc32(corrupted_packet[:-4]) & 0xFFFFFFFF
    
    logger.info("Verification of corrupted packet:")
    logger.info(f"  Corrupted data: " + repr(corrupted))
    logger.info(f"  Received CRC:   {received_crc:08X}")
    logger.info(f"  Calculated CRC: {calculated_crc:08X}")
    logger.info(f"  Match: {received_crc == calculated_crc}")
    logger.info("")
    
    logger.info("CRC32 error detection demo complete!")
    return True


DEMOS = {
    1: ("Complete Protocol Showcase", demo_text_protocol),
    2: ("Binary Protocol Demo", demo_binary_protocol),
    3: ("UDP Sensor Demo", demo_udp_sensor),
    4: ("CRC32 Error Detection", demo_error_detection),
}


def main():
    parser = argparse.ArgumentParser(
        description="Run Week 4 Laboratory Demonstrations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available Demos:
  1 - TEXT Protocol over TCP
  2 - BINARY Protocol over TCP  
  3 - UDP Sensor Protocol
  4 - CRC32 Error Detection

Examples:
  python run_demo.py --demo 1    # Run TEXT protocol demo
  python run_demo.py --demo all  # Run all demos
  python run_demo.py --list      # List available demos
        """
    )
    
    parser.add_argument("--demo", "-d", type=str, default="all",
                        help="Demo number to run (1-4) or 'all'")
    parser.add_argument("--list", "-l", action="store_true",
                        help="List available demonstrations")
    
    args = parser.parse_args()
    
    if args.list:
        logger.info("")
        logger.info("Available demonstrations:")
        for num, (name, _) in DEMOS.items():
            logger.info(f"  {num}. {name}")
        logger.info("")
        return 0
    
    logger.info("")
    logger.info("╔════════════════════════════════════════════════════════════╗")
    logger.info("║         Week 4 Laboratory Demonstrations                   ║")
    logger.info("║         NETWORKING class - ASE, Informatics                ║")
    logger.info("╚════════════════════════════════════════════════════════════╝")
    
    if args.demo == "all":
        demos_to_run = list(DEMOS.values())
    else:
        try:
            demo_num = int(args.demo)
            if demo_num not in DEMOS:
                logger.error(f"Invalid demo number: {demo_num}")
                return 1
            demos_to_run = [DEMOS[demo_num]]
        except ValueError:
            logger.error(f"Invalid demo selection: {args.demo}")
            return 1
    
    success = True
    for name, demo_func in demos_to_run:
        try:
            if not demo_func():
                success = False
        except Exception as e:
            logger.error(f"Demo failed: {e}")
            success = False
    
    logger.info("")
    logger.info("=" * 60)
    if success:
        logger.info("All demonstrations completed successfully!")
    else:
        logger.warning("Some demonstrations encountered issues")
    logger.info("=" * 60)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
