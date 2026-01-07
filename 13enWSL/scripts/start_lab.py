#!/usr/bin/env python3
"""
Week 13 Laboratory Launcher
NETWORKING class - ASE, Informatics | by Revolvix

This script starts all Docker containers and verifies the laboratory environment.
"""

import subprocess
import sys
import time
import argparse
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_logger

logger = setup_logger("start_lab")

# Service definitions with health check configuration
SERVICES = {
    "mosquitto": {
        "container": "week13_mosquitto",
        "port": 1883,
        "health_check": None,
        "startup_time": 5
    },
    "dvwa": {
        "container": "week13_dvwa",
        "port": 8080,
        "health_check": "http://localhost:8080/",
        "startup_time": 15
    },
    "vsftpd": {
        "container": "week13_vsftpd",
        "port": 2121,
        "health_check": None,
        "startup_time": 5
    }
}


def ensure_env_file(docker_dir: Path) -> None:
    """Ensure .env file exists with default values."""
    env_file = docker_dir / ".env"
    if not env_file.exists():
        logger.info("Creating default .env file...")
        env_content = """# Week 13 Docker Environment
MQTT_PLAIN_PORT=1883
MQTT_TLS_PORT=8883
DVWA_HOST_PORT=8080
VSFTPD_HOST_PORT=2121
VSFTPD_BACKDOOR_HOST_PORT=6200
"""
        env_file.write_text(env_content)


def ensure_certificates(docker_dir: Path) -> bool:
    """Ensure TLS certificates exist."""
    certs_dir = docker_dir / "configs" / "certs"
    ca_crt = certs_dir / "ca.crt"
    server_crt = certs_dir / "server.crt"
    
    if ca_crt.exists() and server_crt.exists():
        return True
    
    logger.info("Generating TLS certificates...")
    try:
        # Run the configure_docker script
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "setup" / "configure_docker.py")],
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode == 0
    except Exception as e:
        logger.error(f"Failed to generate certificates: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Start Week 13 Laboratory")
    parser.add_argument("--status", action="store_true", help="Check status only")
    parser.add_argument("--rebuild", action="store_true", help="Force rebuild images")
    parser.add_argument("--detach", "-d", action="store_true", default=True,
                        help="Run in detached mode (default)")
    parser.add_argument("--no-detach", action="store_true",
                        help="Run in foreground (interactive)")
    args = parser.parse_args()
    
    docker_dir = PROJECT_ROOT / "docker"
    docker = DockerManager(docker_dir)
    
    if args.status:
        docker.show_status(SERVICES)
        return 0
    
    logger.info("=" * 60)
    logger.info("Starting Week 13 Laboratory Environment")
    logger.info("IoT and Security in Computer Networks")
    logger.info("=" * 60)
    
    try:
        # Ensure prerequisites
        ensure_env_file(docker_dir)
        
        if not ensure_certificates(docker_dir):
            logger.warning("Certificate generation had issues - TLS may not work")
        
        # Create artifacts directory
        artifacts_dir = PROJECT_ROOT / "artifacts"
        artifacts_dir.mkdir(exist_ok=True)
        
        # Build images if requested
        if args.rebuild:
            logger.info("Building Docker images...")
            if not docker.compose_build():
                logger.error("Failed to build images")
                return 1
        
        # Start containers
        logger.info("Starting Docker containers...")
        detach = not args.no_detach
        if not docker.compose_up(detach=detach, build=False):
            logger.error("Failed to start containers")
            return 1
        
        # Wait for services to initialise
        logger.info("Waiting for services to initialise...")
        time.sleep(8)
        
        # Verify services
        logger.info("Verifying services...")
        all_healthy = docker.verify_services(SERVICES)
        
        if all_healthy:
            logger.info("=" * 60)
            logger.info("Laboratory environment is ready!")
            logger.info("")
            logger.info("Access points:")
            logger.info("  Portainer:      https://localhost:9443 (if installed)")
            logger.info("  DVWA:           http://localhost:8080")
            logger.info("  MQTT Plain:     localhost:1883")
            logger.info("  MQTT TLS:       localhost:8883")
            logger.info("  FTP:            localhost:2121")
            logger.info("  Backdoor Stub:  localhost:6200")
            logger.info("=" * 60)
            logger.info("")
            logger.info("Quick start commands:")
            logger.info("  python src/exercises/ex_13_01_port_scanner.py --target 127.0.0.1 --ports 1-1024")
            logger.info("  python src/exercises/ex_13_02_mqtt_client.py --broker 127.0.0.1 --port 1883 --mode publish --topic test --message hello")
            logger.info("")
            return 0
        else:
            logger.warning("Some services may not be fully ready")
            logger.info("Check logs with: docker compose -f docker/docker-compose.yml logs")
            return 1
    
    except KeyboardInterrupt:
        logger.info("\nInterrupted by user")
        return 130
    
    except Exception as e:
        logger.error(f"Failed to start laboratory: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
