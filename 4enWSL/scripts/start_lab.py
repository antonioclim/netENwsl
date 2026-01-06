#!/usr/bin/env python3
"""
Week 4 Laboratory Launcher
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
from scripts.utils.network_utils import NetworkUtils
from scripts.utils.logger import setup_logger

logger = setup_logger("start_lab")

# Service configurations
SERVICES = {
    "text_server": {
        "container": "week4_demo",
        "port": 5400,
        "health_check": "tcp",
        "startup_time": 3,
        "description": "TEXT Protocol Server"
    },
    "binary_server": {
        "container": "week4_demo",
        "port": 5401,
        "health_check": "tcp",
        "startup_time": 3,
        "description": "BINARY Protocol Server"
    },
    "udp_server": {
        "container": "week4_demo",
        "port": 5402,
        "health_check": "udp",
        "startup_time": 3,
        "description": "UDP Sensor Server"
    },
    "portainer": {
        "container": "week4_portainer",
        "port": 9443,
        "health_check": "tcp",
        "startup_time": 10,
        "description": "Portainer Management"
    }
}


def start_native_servers(port_text: int = 5400, port_binary: int = 5401, 
                         port_udp: int = 5402) -> list:
    """
    Start servers natively (without Docker) for development.
    
    Returns:
        List of subprocess.Popen objects
    """
    processes = []
    src_dir = PROJECT_ROOT / "src" / "apps"
    
    servers = [
        (src_dir / "text_proto_server.py", ["--port", str(port_text)]),
        (src_dir / "binary_proto_server.py", ["--port", str(port_binary)]),
        (src_dir / "udp_sensor_server.py", ["--port", str(port_udp)]),
    ]
    
    for script, args in servers:
        if script.exists():
            proc = subprocess.Popen(
                [sys.executable, str(script)] + args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            processes.append(proc)
            logger.info(f"Started {script.name} (PID: {proc.pid})")
    
    return processes


def check_docker_available() -> bool:
    """Check if Docker is available and running."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except Exception:
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Start Week 4 Laboratory Environment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python start_lab.py              # Start all services
  python start_lab.py --status     # Check current status
  python start_lab.py --native     # Run servers without Docker
  python start_lab.py --service text  # Start only TEXT server

Services:
  text    - TEXT Protocol Server (TCP 5400)
  binary  - BINARY Protocol Server (TCP 5401)
  udp     - UDP Sensor Server (UDP 5402)
  all     - All services (default)
        """
    )
    
    parser.add_argument("--status", action="store_true",
                        help="Check status only, don't start services")
    parser.add_argument("--rebuild", action="store_true",
                        help="Force rebuild Docker images")
    parser.add_argument("--native", action="store_true",
                        help="Run servers natively without Docker")
    parser.add_argument("--service", "-s", type=str, default="all",
                        choices=["text", "binary", "udp", "all"],
                        help="Specific service to start")
    parser.add_argument("--detach", "-d", action="store_true", default=True,
                        help="Run in detached mode (default)")
    parser.add_argument("--logs", "-l", action="store_true",
                        help="Show service logs after starting")
    
    args = parser.parse_args()
    
    docker_dir = PROJECT_ROOT / "docker"
    
    # Status check mode
    if args.status:
        if check_docker_available():
            try:
                docker = DockerManager(docker_dir)
                docker.show_status(SERVICES)
            except FileNotFoundError:
                logger.error("Docker Compose file not found")
        else:
            logger.warning("Docker not available. Checking native processes...")
            
            # Check for native processes
            for name, config in SERVICES.items():
                port = config["port"]
                if NetworkUtils.check_port("localhost", port):
                    logger.info(f"  {name}: Running on port {port}")
                else:
                    logger.info(f"  {name}: Not running")
        return 0
    
    # Native mode (without Docker)
    if args.native:
        logger.info("=" * 60)
        logger.info("Starting Week 4 Laboratory (Native Mode)")
        logger.info("=" * 60)
        
        processes = start_native_servers()
        
        if not processes:
            logger.error("No servers could be started. Check src/apps/ directory.")
            return 1
        
        logger.info("")
        logger.info("Waiting for servers to initialise...")
        time.sleep(3)
        
        # Verify servers
        all_running = True
        for name, config in [("TEXT", 5400), ("BINARY", 5401), ("UDP", 5402)]:
            if NetworkUtils.check_port("localhost", config):
                logger.info(f"  {name} server: Ready on port {config}")
            else:
                logger.warning(f"  {name} server: Not responding on port {config}")
                all_running = False
        
        if all_running:
            logger.info("")
            logger.info("=" * 60)
            logger.info("Laboratory environment is ready!")
            logger.info("")
            logger.info("Press Ctrl+C to stop all servers")
            logger.info("=" * 60)
            
            try:
                for proc in processes:
                    proc.wait()
            except KeyboardInterrupt:
                logger.info("\nStopping servers...")
                for proc in processes:
                    proc.terminate()
        
        return 0 if all_running else 1
    
    # Docker mode
    logger.info("=" * 60)
    logger.info("Starting Week 4 Laboratory Environment")
    logger.info("=" * 60)
    
    if not check_docker_available():
        logger.error("Docker is not available. Please start Docker Desktop.")
        logger.info("Alternatively, use --native flag to run without Docker.")
        return 1
    
    try:
        docker = DockerManager(docker_dir)
        
        # Build if requested
        if args.rebuild:
            logger.info("Building Docker images...")
            if not docker.compose_build():
                logger.error("Failed to build images")
                return 1
        
        # Start services
        logger.info("Starting Docker Compose services...")
        services_to_start = None
        if args.service != "all":
            service_map = {
                "text": "week4-lab",
                "binary": "week4-lab",
                "udp": "week4-lab"
            }
            services_to_start = [service_map.get(args.service, "week4-lab")]
        
        if not docker.compose_up(detach=args.detach, services=services_to_start):
            logger.error("Failed to start services")
            return 1
        
        # Wait for services
        logger.info("")
        logger.info("Waiting for services to initialise...")
        time.sleep(5)
        
        # Verify services
        all_healthy = True
        for name, config in SERVICES.items():
            port = config["port"]
            desc = config["description"]
            
            if NetworkUtils.wait_for_port("localhost", port, timeout=15):
                logger.info(f"  ✓ {desc}: Ready on port {port}")
            else:
                logger.error(f"  ✗ {desc}: Not responding on port {port}")
                all_healthy = False
        
        if all_healthy:
            logger.info("")
            logger.info("=" * 60)
            logger.info("Laboratory environment is ready!")
            logger.info("")
            logger.info("Access points:")
            logger.info("  Portainer:      https://localhost:9443")
            logger.info("  TEXT Server:    localhost:5400")
            logger.info("  BINARY Server:  localhost:5401")
            logger.info("  UDP Server:     localhost:5402")
            logger.info("=" * 60)
            
            # Show logs if requested
            if args.logs:
                logger.info("\nService logs:")
                docker.compose_logs(follow=False, tail=20)
            
            return 0
        else:
            logger.error("")
            logger.error("Some services failed to start. Check logs:")
            docker.compose_logs(follow=False, tail=50)
            return 1
    
    except FileNotFoundError as e:
        logger.error(f"Configuration error: {e}")
        return 1
    except Exception as e:
        logger.error(f"Failed to start laboratory: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
