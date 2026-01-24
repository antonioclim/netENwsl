#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# MODULE_DOCSTRING
# ═══════════════════════════════════════════════════════════════════════════════
"""
Week 12 Demonstration Scripts
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Automated demonstrations for classroom presentation and student practice.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import subprocess
import sys
import time
import argparse
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Any

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.logger import setup_colour_logger
from scripts.utils.network_utils import (
    SMTPTester,
    JSONRPCTester,
    XMLRPCTester,
    check_port,
)

logger = setup_colour_logger("demo")



# ═══════════════════════════════════════════════════════════════════════════════
# DEMO_SMTP_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def demo_smtp() -> bool:
    """
    Demonstrate SMTP protocol dialogue.
    
    Returns:
        True if successful
    """
    logger.info("=" * 60)
    logger.info("Demo 1: SMTP Protocol")
    logger.info("=" * 60)
    
    if not check_port("127.0.0.1", 1025):
        logger.error("SMTP server not running on port 1025")
        logger.info("Start with: python scripts/start_lab.py --service smtp")
        return False
    
    tester = SMTPTester("127.0.0.1", 1025)
    
    try:
        # Connect and show greeting
        logger.info("\n>>> Connecting to SMTP server...")
        greeting = tester.connect()
        logger.info(f"Server: {greeting.raw.strip()}")
        
        # Send EHLO
        logger.info("\n>>> Sending EHLO command...")
        ehlo = tester.send_command("EHLO demo.client")
        for line in ehlo.raw.strip().split("\r\n"):
            logger.info(f"Server: {line}")
        
        # Start mail transaction
        logger.info("\n>>> Starting mail transaction...")
        
        mail_from = tester.send_command("MAIL FROM:<demo@week12.test>")
        logger.info(f"MAIL FROM: {mail_from.code} {mail_from.message}")
        
        rcpt_to = tester.send_command("RCPT TO:<student@ase.ro>")
        logger.info(f"RCPT TO: {rcpt_to.code} {rcpt_to.message}")
        
        # Send DATA
        logger.info("\n>>> Sending message data...")
        data_start = tester.send_command("DATA")
        logger.info(f"DATA: {data_start.code} {data_start.message}")
        
        message = """Subject: Week 12 SMTP Demo
From: demo@week12.test
To: student@ase.ro

This is a demonstration of the SMTP protocol for Week 12.

The message body can contain multiple lines.
The message is terminated by a single period on its own line.

Best regards,
Week 12 Demo Script"""
        
        data_end = tester.send_data(message)
        logger.info(f"Message accepted: {data_end.code} {data_end.message}")
        
        # Show LIST (non-standard)
        logger.info("\n>>> Using LIST command (non-standard, educational)...")
        list_result = tester.send_command("LIST")
        for line in list_result.raw.strip().split("\r\n"):
            logger.info(f"Server: {line}")
        
        # Quit
        logger.info("\n>>> Closing connection...")
        quit_result = tester.send_command("QUIT")
        logger.info(f"Server: {quit_result.code} {quit_result.message}")
        
        tester.close()
        
        logger.info("\n✓ SMTP demo completed successfully")
        return True
    
    except Exception as e:
        logger.error(f"SMTP demo failed: {e}")
        tester.close()
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# DEMO_JSONRPC_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def demo_jsonrpc() -> bool:
    """
    Demonstrate JSON-RPC 2.0 protocol.
    
    Returns:
        True if successful
    """
    logger.info("=" * 60)
    logger.info("Demo 2: JSON-RPC 2.0 Protocol")
    logger.info("=" * 60)
    
    if not check_port("127.0.0.1", 6200):
        logger.error("JSON-RPC server not running on port 6200")
        return False
    
    tester = JSONRPCTester("http://127.0.0.1:6200")
    
    try:
        # Basic arithmetic
        logger.info("\n>>> Basic arithmetic operations:")
        
        for method, params, expected in [
            ("add", [10, 32], 42),
            ("subtract", [100, 58], 42),
            ("multiply", [6, 7], 42),
            ("divide", [84, 2], 42),
        ]:
            result = tester.call(method, params)
            status = "✓" if result.success and result.result == expected else "✗"
            logger.info(f"  {status} {method}{tuple(params)} = {result.result}")
        
        # Error handling
        logger.info("\n>>> Error handling:")
        error_result = tester.call("divide", [1, 0])
        logger.info(f"  divide(1, 0) → Error: {error_result.error}")
        
        nonexistent = tester.call("nonexistent_method")
        logger.info(f"  nonexistent_method() → Error: {nonexistent.error}")
        
        # Batch request
        logger.info("\n>>> Batch request (3 operations in 1 HTTP request):")
        batch_results = tester.batch_call([
            ("add", [1, 2]),
            ("multiply", [3, 4]),
            ("subtract", [10, 5]),
        ])
        for i, r in enumerate(batch_results):
            logger.info(f"  Result {i+1}: {r.result}")
        
        # Server info
        logger.info("\n>>> Server introspection:")
        info = tester.call("get_server_info")
        logger.info(f"  Server: {info.result}")
        
        stats = tester.call("get_stats")
        logger.info(f"  Stats: {stats.result}")
        
        logger.info("\n✓ JSON-RPC demo completed successfully")
        return True
    
    except Exception as e:
        logger.error(f"JSON-RPC demo failed: {e}")
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# DEMO_XMLRPC_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def demo_xmlrpc() -> bool:
    """
    Demonstrate XML-RPC protocol.
    
    Returns:
        True if successful
    """
    logger.info("=" * 60)
    logger.info("Demo 3: XML-RPC Protocol")
    logger.info("=" * 60)
    
    if not check_port("127.0.0.1", 6201):
        logger.error("XML-RPC server not running on port 6201")
        return False
    
    tester = XMLRPCTester("http://127.0.0.1:6201")
    
    try:
        # Basic arithmetic
        logger.info("\n>>> Basic arithmetic operations:")
        
        for method, args, expected in [
            ("add", (10, 32), 42),
            ("subtract", (100, 58), 42),
            ("multiply", (6, 7), 42),
            ("divide", (84, 2), 42),
        ]:
            result = tester.call(method, *args)
            status = "✓" if result.success and result.result == expected else "✗"
            logger.info(f"  {status} {method}{args} = {result.result}")
        
        # Introspection
        logger.info("\n>>> XML-RPC Introspection:")
        methods = tester.call("system.listMethods")
        logger.info(f"  Available methods: {', '.join(methods.result[:5])}...")
        
        # Server info
        logger.info("\n>>> Server info:")
        info = tester.call("get_server_info")
        logger.info(f"  {info.result}")
        
        logger.info("\n✓ XML-RPC demo completed successfully")
        return True
    
    except Exception as e:
        logger.error(f"XML-RPC demo failed: {e}")
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# DEMO_RPC_COMPARE_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def demo_rpc_compare() -> bool:
    """
    Compare JSON-RPC and XML-RPC side by side.
    
    Returns:
        True if successful
    """
    logger.info("=" * 60)
    logger.info("Demo 4: RPC Protocol Comparison")
    logger.info("=" * 60)
    
    import json
    import urllib.request
    
    # JSON-RPC request
    logger.info("\n>>> JSON-RPC request/response:")
    json_request = {
        "jsonrpc": "2.0",
        "method": "add",
        "params": [10, 32],
        "id": 1
    }
    logger.info(f"Request ({len(json.dumps(json_request))} bytes):")
    logger.info(f"  {json.dumps(json_request)}")
    
    try:
        req = urllib.request.Request(
            "http://127.0.0.1:6200",
            data=json.dumps(json_request).encode(),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            json_response = resp.read().decode()
            logger.info(f"Response ({len(json_response)} bytes):")
            logger.info(f"  {json_response}")
    except Exception as e:
        logger.error(f"JSON-RPC failed: {e}")
    
    # XML-RPC request (approximate, for comparison)
    logger.info("\n>>> XML-RPC equivalent request/response:")
    xml_request = """<?xml version="1.0"?>
<methodCall>
  <methodName>add</methodName>
  <params>
    <param><value><int>10</int></value></param>
    <param><value><int>32</int></value></param>
  </params>
</methodCall>"""
    logger.info(f"Request ({len(xml_request)} bytes):")
    for line in xml_request.strip().split("\n"):
        logger.info(f"  {line}")
    
    # Comparison summary
    logger.info("\n>>> Size comparison:")
    logger.info(f"  JSON-RPC request: ~{len(json.dumps(json_request))} bytes")
    logger.info(f"  XML-RPC request:  ~{len(xml_request)} bytes")
    logger.info(f"  XML overhead: ~{len(xml_request) - len(json.dumps(json_request))} bytes ({100 * (len(xml_request) / len(json.dumps(json_request)) - 1):.0f}% larger)")
    
    logger.info("\n✓ RPC comparison demo completed")
    return True



# ═══════════════════════════════════════════════════════════════════════════════
# DEMO_BENCHMARK_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def demo_benchmark() -> bool:
    """
    Run RPC benchmark comparison.
    
    Returns:
        True if successful
    """
    logger.info("=" * 60)
    logger.info("Demo 5: RPC Performance Benchmark")
    logger.info("=" * 60)
    
    benchmark_script = PROJECT_ROOT / "src" / "apps" / "rpc" / "benchmark_rpc.py"
    
    if benchmark_script.exists():
        logger.info("Running benchmark script...")
        result = subprocess.run(
            [sys.executable, str(benchmark_script)],
            capture_output=False,
            cwd=PROJECT_ROOT
        )
        return result.returncode == 0
    else:
        logger.warning("Benchmark script not found, running inline benchmark...")
        
        import time
        
        json_tester = JSONRPCTester("http://127.0.0.1:6200")
        xml_tester = XMLRPCTester("http://127.0.0.1:6201")
        
        iterations = 100
        
        # JSON-RPC benchmark
        logger.info(f"\n>>> JSON-RPC: {iterations} calls to add(10, 32)...")
        start = time.perf_counter()
        for _ in range(iterations):
            json_tester.call("add", [10, 32])
        json_duration = time.perf_counter() - start
        json_rps = iterations / json_duration
        
        # XML-RPC benchmark
        logger.info(f">>> XML-RPC: {iterations} calls to add(10, 32)...")
        start = time.perf_counter()
        for _ in range(iterations):
            xml_tester.call("add", 10, 32)
        xml_duration = time.perf_counter() - start
        xml_rps = iterations / xml_duration
        
        # Results
        logger.info("\n>>> Results:")
        logger.info(f"  JSON-RPC: {json_rps:.1f} requests/sec ({json_duration*1000/iterations:.1f} ms/req)")
        logger.info(f"  XML-RPC:  {xml_rps:.1f} requests/sec ({xml_duration*1000/iterations:.1f} ms/req)")
        
        if json_rps > xml_rps:
            factor = json_rps / xml_rps
            logger.info(f"\n  JSON-RPC is {factor:.1f}x faster in this test")
        else:
            factor = xml_rps / json_rps
            logger.info(f"\n  XML-RPC is {factor:.1f}x faster in this test")
        
        logger.info("\n✓ Benchmark completed")
        return True


DEMOS = {
    "smtp": ("SMTP Protocol Dialogue", demo_smtp),
    "jsonrpc": ("JSON-RPC 2.0 Operations", demo_jsonrpc),
    "xmlrpc": ("XML-RPC Operations", demo_xmlrpc),
    "rpc-compare": ("RPC Protocol Comparison", demo_rpc_compare),
    "benchmark": ("RPC Performance Benchmark", demo_benchmark),
    "all": ("All Demonstrations", None),
}



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run Week 12 demonstrations"
    )
    parser.add_argument(
        "--demo", "-d",
        choices=list(DEMOS.keys()),
        default="all",
        help="Demonstration to run (default: all)"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List available demonstrations"
    )
    
    args = parser.parse_args()
    
    if args.list:
        print("\nAvailable demonstrations:")
        for name, (desc, _) in DEMOS.items():
            print(f"  {name:15} - {desc}")
        return 0
    
    if args.demo == "all":
        demos_to_run = ["smtp", "jsonrpc", "xmlrpc", "rpc-compare"]
    else:
        demos_to_run = [args.demo]
    
    results = []
    for demo_name in demos_to_run:
        _, demo_func = DEMOS[demo_name]
        if demo_func:
            success = demo_func()
            results.append((demo_name, success))
            time.sleep(1)  # Brief pause between demos
    
    # Summary
    print("\n" + "=" * 60)
    print("Demo Summary:")
    all_passed = True
    for name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"  {status}: {name}")
        if not success:
            all_passed = False
    print("=" * 60)
    
    return 0 if all_passed else 1



# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    sys.exit(main())
