#!/usr/bin/env python3
"""
Docker Management Utilities
NETWORKING class - ASE, Informatics | by Revolvix

Provides Docker Compose and container management functionality.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import subprocess
import time
import socket
from pathlib import Path
from typing import Dict, List, Optional, Any
from .logger import setup_logger

logger = setup_logger("docker_utils")



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class DockerManager:
    """Manages Docker Compose operations for the laboratory."""
    

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
    def __init__(self, docker_dir: Path):
        """
        Initialise Docker manager.
        
        Args:
            docker_dir: Path to directory containing docker-compose.yml
        """
        self.docker_dir = Path(docker_dir)
        self.compose_file = self.docker_dir / "docker-compose.yml"
        
        if not self.compose_file.exists():
            raise FileNotFoundError(f"Docker Compose file not found: {self.compose_file}")
    

# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
    def _run_compose(self, *args, capture: bool = False) -> subprocess.CompletedProcess:
        """Run a docker compose command."""
        cmd = ["docker", "compose", "-f", str(self.compose_file)] + list(args)
        
        if capture:
            return subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(self.docker_dir)
            )
        else:
            return subprocess.run(
                cmd,
                cwd=str(self.docker_dir)
            )
    

# ═══════════════════════════════════════════════════════════════════════════════
# RESOURCE_CREATION
# ═══════════════════════════════════════════════════════════════════════════════
    def compose_build(self, no_cache: bool = False) -> bool:
        """
        Build Docker images.
        
        Args:
            no_cache: If True, build without cache
        
        Returns:
            True if successful
        """
        logger.info("Building Docker images...")
        args = ["build"]
        if no_cache:
            args.append("--no-cache")
        
        result = self._run_compose(*args)
        return result.returncode == 0
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def compose_up(self, detach: bool = True, services: Optional[List[str]] = None) -> bool:
        """
        Start Docker Compose services.
        
        Args:
            detach: Run in detached mode
            services: Optional list of specific services to start
        
        Returns:
            True if successful
        """
        logger.info("Starting Docker Compose services...")
        args = ["up"]
        if detach:
            args.append("-d")
        if services:
            args.extend(services)
        
        result = self._run_compose(*args)
        return result.returncode == 0
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def compose_down(self, volumes: bool = False, dry_run: bool = False) -> bool:
        """
        Stop Docker Compose services.
        
        Args:
            volumes: Also remove volumes
            dry_run: Show what would be done
        
        Returns:
            True if successful
        """
        if dry_run:
            logger.info("[DRY RUN] Would stop Docker Compose services")
            return True
        
        logger.info("Stopping Docker Compose services...")
        args = ["down"]
        if volumes:
            args.append("-v")
        
        result = self._run_compose(*args)
        return result.returncode == 0
    

# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
    def compose_logs(self, service: Optional[str] = None, follow: bool = False, 
                     tail: int = 100) -> None:
        """Show service logs."""
        args = ["logs", f"--tail={tail}"]
        if follow:
            args.append("-f")
        if service:
            args.append(service)
        
        self._run_compose(*args)
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def compose_ps(self) -> str:
        """Get running services status."""
        result = self._run_compose("ps", capture=True)
        return result.stdout
    

# ═══════════════════════════════════════════════════════════════════════════════
# CONTAINER_MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════
    def get_container_status(self, container_name: str) -> Dict[str, Any]:
        """
        Get detailed status of a container.
        
        Args:
            container_name: Name of the container
        
        Returns:
            Dictionary with container status information
        """
        try:
            result = subprocess.run(
                ["docker", "inspect", container_name, "--format",
                 "{{.State.Status}}|{{.State.Running}}|{{.State.Health.Status}}"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                parts = result.stdout.strip().split("|")
                return {
                    "status": parts[0] if len(parts) > 0 else "unknown",
                    "running": parts[1].lower() == "true" if len(parts) > 1 else False,
                    "health": parts[2] if len(parts) > 2 else "none"
                }
        except Exception as e:
            logger.debug(f"Failed to get container status: {e}")
        
        return {"status": "not_found", "running": False, "health": "none"}
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def wait_for_service(self, host: str, port: int, timeout: int = 30, 
                         protocol: str = "tcp") -> bool:
        """
        Wait for a service to become available.
        
        Args:
            host: Service hostname
            port: Service port
            timeout: Maximum wait time in seconds
            protocol: "tcp" or "udp"
        
        Returns:
            True if service is available
        """
        sock_type = socket.SOCK_STREAM if protocol == "tcp" else socket.SOCK_DGRAM
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                sock = socket.socket(socket.AF_INET, sock_type)
                sock.settimeout(2)
                sock.connect((host, port))
                sock.close()
                return True
            except (socket.error, socket.timeout):
                time.sleep(1)
        
        return False
    

# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
    def verify_services(self, services: Dict[str, Dict[str, Any]]) -> bool:
        """
        Verify all services are running and healthy.
        
        Args:
            services: Dictionary mapping service names to their configurations
                     Expected keys: container, port, health_check, startup_time
        
        Returns:
            True if all services are healthy
        """
        all_healthy = True
        
        for name, config in services.items():
            container = config.get("container", name)
            port = config.get("port")
            startup_time = config.get("startup_time", 5)
            
            logger.info(f"Checking {name}...")
            
            # Wait for startup
            time.sleep(startup_time)
            
            # Check container status
            status = self.get_container_status(container)
            
            if not status["running"]:
                logger.error(f"  Container {container} is not running")
                all_healthy = False
                continue
            
            # Check port availability
            if port:
                protocol = "udp" if "udp" in str(port) else "tcp"
                port_num = int(str(port).replace("/udp", ""))
                
                if self.wait_for_service("localhost", port_num, timeout=10, protocol=protocol):
                    logger.info(f"  {name} is ready on port {port}")
                else:
                    logger.error(f"  {name} port {port} not responding")
                    all_healthy = False
            else:
                logger.info(f"  {name} container is running")
        
        return all_healthy
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def show_status(self, services: Dict[str, Dict[str, Any]]) -> None:
        """Display formatted status of all services."""
        print("\n" + "=" * 60)
        print("Service Status")
        print("=" * 60)
        
        for name, config in services.items():
            container = config.get("container", name)
            port = config.get("port")
            
            status = self.get_container_status(container)
            
            if status["running"]:
                status_str = "\033[92m●\033[0m Running"
                if status["health"] == "healthy":
                    status_str += " (healthy)"
            else:
                status_str = "\033[91m○\033[0m Stopped"
            
            port_str = f":{port}" if port else ""
            print(f"  {name:20} {status_str:30} {port_str}")
        
        print("=" * 60 + "\n")
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def remove_by_prefix(self, prefix: str, dry_run: bool = False) -> None:
        """
        Remove containers, networks and volumes with given prefix.
        
        Args:
            prefix: Prefix to match (e.g., "week4")
            dry_run: If True, only show what would be removed
        """
        # Containers
        result = subprocess.run(
            ["docker", "ps", "-a", "--filter", f"name={prefix}", "-q"],
            capture_output=True,
            text=True
        )
        containers = result.stdout.strip().split()
        
        if containers and containers[0]:
            if dry_run:
                logger.info(f"[DRY RUN] Would remove containers: {containers}")
            else:
                subprocess.run(["docker", "rm", "-f"] + containers)
        
        # Networks
        result = subprocess.run(
            ["docker", "network", "ls", "--filter", f"name={prefix}", "-q"],
            capture_output=True,
            text=True
        )
        networks = result.stdout.strip().split()
        
        if networks and networks[0]:
            if dry_run:
                logger.info(f"[DRY RUN] Would remove networks: {networks}")
            else:
                for network in networks:
                    subprocess.run(["docker", "network", "rm", network])
        
        # Volumes
        result = subprocess.run(
            ["docker", "volume", "ls", "--filter", f"name={prefix}", "-q"],
            capture_output=True,
            text=True
        )
        volumes = result.stdout.strip().split()
        
        if volumes and volumes[0]:
            if dry_run:
                logger.info(f"[DRY RUN] Would remove volumes: {volumes}")
            else:
                subprocess.run(["docker", "volume", "rm"] + volumes)
    

# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
    def system_prune(self) -> None:
        """Prune unused Docker resources."""
        logger.info("Pruning unused Docker resources...")
        subprocess.run(
            ["docker", "system", "prune", "-f"],
            capture_output=True
        )

if __name__ == "__main__":
    # Module loaded directly - display module info
    print(f"Module {__name__} loaded successfully.")
    print(f"This module provides utility functions for the networking laboratory.")
