#!/usr/bin/env python3
"""
Week 13 Demonstration Runner
NETWORKING class - ASE, Informatics | by Revolvix

Runs automated demonstrations suitable for classroom presentation.
"""

import subprocess
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.logger import setup_logger
from scripts.utils.docker_utils import DockerManager
from scripts.utils.network_utils import ServiceChecker

logger = setup_logger("run_demo")


def run_command(cmd: list, description: str, timeout: int = 60) -> bool:
    """Run a command with logging."""
    logger.info(f"Running: {description}")
    logger.info(f"  Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=False,
            timeout=timeout,
            cwd=str(PROJECT_ROOT)
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        logger.error(f"  Command timed out after {timeout}s")
        return False
    except Exception as e:
        logger.error(f"  Command failed: {e}")
        return False


def demo_full_run():
    """Demo 1: Full automated laboratory run."""
    logger.info("=" * 70)
    logger.info("DEMO 1: Full Automated Laboratory Run")
    logger.info("=" * 70)
    
    artifacts_dir = PROJECT_ROOT / "artifacts"
    artifacts_dir.mkdir(exist_ok=True)
    
    # Start services if needed
    docker = DockerManager(PROJECT_ROOT / "docker")
    logger.info("\nStep 1: Ensuring services are running...")
    docker.compose_up(detach=True)
    time.sleep(5)
    
    # Check service availability
    logger.info("\nStep 2: Verifying service availability...")
    checker = ServiceChecker()
    checker.print_status()
    
    # Run port scan
    logger.info("\nStep 3: Running port scan...")
    run_command([
        sys.executable,
        str(PROJECT_ROOT / "src" / "exercises" / "ex_13_01_port_scanner.py"),
        "--target", "127.0.0.1",
        "--ports", "21,22,80,1883,2121,6200,8080,8883",
        "--json-out", str(artifacts_dir / "demo_scan.json")
    ], "Port Scanner", timeout=120)
    
    # Run MQTT demo
    logger.info("\nStep 4: MQTT plaintext demonstration...")
    run_command([
        sys.executable,
        str(PROJECT_ROOT / "src" / "exercises" / "ex_13_02_mqtt_client.py"),
        "--broker", "127.0.0.1",
        "--port", "1883",
        "--mode", "publish",
        "--topic", "demo/test",
        "--message", '{"demo": "message", "timestamp": "' + datetime.now().isoformat() + '"}',
        "--count", "3"
    ], "MQTT Publish", timeout=30)
    
    # Run vulnerability check
    logger.info("\nStep 5: Vulnerability assessment...")
    run_command([
        sys.executable,
        str(PROJECT_ROOT / "src" / "exercises" / "ex_13_04_vuln_checker.py"),
        "--target", "127.0.0.1",
        "--port", "8080",
        "--service", "http",
        "--json-out", str(artifacts_dir / "demo_vuln.json")
    ], "Vulnerability Checker", timeout=30)
    
    logger.info("\n" + "=" * 70)
    logger.info("DEMO 1 COMPLETE")
    logger.info(f"Artifacts saved to: {artifacts_dir}")
    logger.info("=" * 70)


def demo_traffic_comparison():
    """Demo 2: Plaintext vs TLS traffic comparison."""
    logger.info("=" * 70)
    logger.info("DEMO 2: Plaintext vs TLS Traffic Comparison")
    logger.info("=" * 70)
    
    logger.info("\nThis demo compares observable traffic between plaintext and TLS MQTT.")
    logger.info("")
    
    # Plaintext
    logger.info("Step 1: MQTT Plaintext (port 1883)")
    logger.info("  - All content is visible in packet capture")
    logger.info("  - Topic names, message payloads clearly readable")
    run_command([
        sys.executable,
        str(PROJECT_ROOT / "src" / "exercises" / "ex_13_02_mqtt_client.py"),
        "--broker", "127.0.0.1",
        "--port", "1883",
        "--mode", "publish",
        "--topic", "sensors/temperature",
        "--message", '{"sensor_id": "T001", "value": 23.5, "unit": "celsius"}',
        "--count", "2"
    ], "Plaintext MQTT", timeout=30)
    
    time.sleep(2)
    
    # TLS
    logger.info("\nStep 2: MQTT over TLS (port 8883)")
    logger.info("  - Content encrypted in transit")
    logger.info("  - Only metadata (IPs, ports, timing) visible")
    
    certs_dir = PROJECT_ROOT / "docker" / "configs" / "certs"
    ca_cert = certs_dir / "ca.crt"
    
    if ca_cert.exists():
        run_command([
            sys.executable,
            str(PROJECT_ROOT / "src" / "exercises" / "ex_13_02_mqtt_client.py"),
            "--broker", "127.0.0.1",
            "--port", "8883",
            "--mode", "publish",
            "--topic", "sensors/temperature",
            "--message", '{"sensor_id": "T001", "value": 23.5, "unit": "celsius"}',
            "--count", "2",
            "--tls",
            "--cafile", str(ca_cert)
        ], "TLS MQTT", timeout=30)
    else:
        logger.warning("CA certificate not found. Run setup first.")
    
    logger.info("\n" + "=" * 70)
    logger.info("DEMO 2 COMPLETE")
    logger.info("Capture traffic with Wireshark to observe the differences.")
    logger.info("=" * 70)


def demo_reconnaissance():
    """Demo 3: Reconnaissance pipeline."""
    logger.info("=" * 70)
    logger.info("DEMO 3: Reconnaissance Pipeline")
    logger.info("=" * 70)
    
    artifacts_dir = PROJECT_ROOT / "artifacts"
    artifacts_dir.mkdir(exist_ok=True)
    
    logger.info("\nStep 1: Service Discovery")
    run_command([
        sys.executable,
        str(PROJECT_ROOT / "src" / "exercises" / "ex_13_01_port_scanner.py"),
        "--target", "127.0.0.1",
        "--ports", "1-1024,2121,6200,8080,8883",
        "--json-out", str(artifacts_dir / "recon_ports.json")
    ], "Port Discovery", timeout=180)
    
    logger.info("\nStep 2: Service Fingerprinting")
    
    # HTTP
    run_command([
        sys.executable,
        str(PROJECT_ROOT / "src" / "exercises" / "ex_13_04_vuln_checker.py"),
        "--target", "127.0.0.1",
        "--port", "8080",
        "--service", "http",
        "--json-out", str(artifacts_dir / "recon_http.json")
    ], "HTTP Fingerprint", timeout=30)
    
    # FTP
    run_command([
        sys.executable,
        str(PROJECT_ROOT / "src" / "exercises" / "ex_13_04_vuln_checker.py"),
        "--target", "127.0.0.1",
        "--port", "2121",
        "--service", "ftp",
        "--json-out", str(artifacts_dir / "recon_ftp.json")
    ], "FTP Fingerprint", timeout=30)
    
    # MQTT
    run_command([
        sys.executable,
        str(PROJECT_ROOT / "src" / "exercises" / "ex_13_04_vuln_checker.py"),
        "--target", "127.0.0.1",
        "--port", "1883",
        "--service", "mqtt",
        "--json-out", str(artifacts_dir / "recon_mqtt.json")
    ], "MQTT Check", timeout=30)
    
    logger.info("\nStep 3: Backdoor Detection")
    run_command([
        sys.executable,
        str(PROJECT_ROOT / "src" / "apps" / "ftp_backdoor_check.py"),
        "--target", "127.0.0.1",
        "--ftp-port", "2121",
        "--backdoor-port", "6200"
    ], "Backdoor Check", timeout=30)
    
    logger.info("\n" + "=" * 70)
    logger.info("DEMO 3 COMPLETE")
    logger.info(f"Reports saved to: {artifacts_dir}")
    logger.info("=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Run Week 13 demonstrations"
    )
    parser.add_argument(
        "--demo",
        type=int,
        choices=[1, 2, 3],
        required=True,
        help="Demo number: 1=Full Run, 2=Traffic Comparison, 3=Reconnaissance"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all demos sequentially"
    )
    
    args = parser.parse_args()
    
    demos = {
        1: demo_full_run,
        2: demo_traffic_comparison,
        3: demo_reconnaissance,
    }
    
    if args.all:
        for num, func in demos.items():
            func()
            logger.info("\n" + "-" * 70 + "\n")
            time.sleep(3)
    else:
        demos[args.demo]()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
