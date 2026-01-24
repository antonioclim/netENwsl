#!/usr/bin/env python3
"""
Docker Utility Module
NETWORKING class - ASE, Informatics | by Revolvix

Provides Docker management functions for laboratory environment.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from .logger import get_logger

logger = get_logger("docker_utils")


@dataclass


# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class ServiceConfig:
    """Configuration for a Docker service."""
    container: str
    port: int
    health_check: Optional[str] = None
    startup_time: int = 5



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
            raise FileNotFoundError(f"docker-compose.yml not found in {self.docker_dir}")
    

# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
    def _run_compose(self, *args: str, capture: bool = False) -> subprocess.CompletedProcess:
        """Execute a docker compose command."""
        cmd = ["docker", "compose", "-f", str(self.compose_file)] + list(args)
        logger.debug(f"Executing: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=capture,
                text=True,
                cwd=self.docker_dir,
                timeout=300
            )
            return result
        except subprocess.TimeoutExpired:
            logger.error("Docker command timed out")
            raise
        except FileNotFoundError:
            logger.error("Docker not found. Is Docker Desktop running?")
            raise
    

# ═══════════════════════════════════════════════════════════════════════════════
# RESOURCE_CREATION
# ═══════════════════════════════════════════════════════════════════════════════
    def compose_build(self, no_cache: bool = False) -> bool:
        """
        Build Docker images.
        
        Args:
            no_cache: Force rebuild without cache
        
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
    def compose_up(self, detach: bool = True, build: bool = False) -> bool:
        """
        Start Docker Compose services.
        
        Args:
            detach: Run in detached mode
            build: Build images before starting
        
        Returns:
            True if successful
        """
        logger.info("Starting Docker Compose services...")
        args = ["up"]
        if detach:
            args.append("-d")
        if build:
            args.append("--build")
        
        result = self._run_compose(*args)
        return result.returncode == 0
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def compose_down(self, volumes: bool = False, dry_run: bool = False) -> bool:
        """
        Stop Docker Compose services.
        
        Args:
            volumes: Remove volumes as well
            dry_run: Show what would be done without executing
        
        Returns:
            True if successful
        """
        if dry_run:
            logger.info("[DRY RUN] Would stop services and remove containers")
            if volumes:
                logger.info("[DRY RUN] Would also remove volumes")
            return True
        
        logger.info("Stopping Docker Compose services...")
        args = ["down"]
        if volumes:
            args.extend(["-v", "--remove-orphans"])
        
        result = self._run_compose(*args)
        return result.returncode == 0
    

# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
    def compose_logs(self, service: Optional[str] = None, follow: bool = False, tail: int = 100) -> str:
        """
        Get service logs.
        
        Args:
            service: Specific service name (or all if None)
            follow: Follow log output
            tail: Number of lines to show
        
        Returns:
            Log output as string
        """
        args = ["logs", f"--tail={tail}"]
        if follow:
            args.append("-f")
        if service:
            args.append(service)
        
        result = self._run_compose(*args, capture=True)
        return result.stdout
    

# ═══════════════════════════════════════════════════════════════════════════════
# CONTAINER_MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════
    def get_container_status(self) -> Dict[str, Dict[str, Any]]:
        """
        Get status of all containers.
        
        Returns:
            Dictionary mapping container names to status info
        """
        result = self._run_compose("ps", "--format", "json", capture=True)
        if result.returncode != 0:
            return {}
        
        import json
        status = {}
        
        # Handle both single object and array formats
        try:
            for line in result.stdout.strip().split('\n'):
                if line:
                    data = json.loads(line)
                    name = data.get('Name', data.get('name', ''))
                    status[name] = {
                        'state': data.get('State', data.get('state', 'unknown')),
                        'status': data.get('Status', data.get('status', '')),
                        'ports': data.get('Ports', data.get('ports', ''))
                    }
        except json.JSONDecodeError:
            logger.debug("Could not parse container status as JSON")
        
        return status
    

# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
    def is_container_running(self, container_name: str) -> bool:
        """Check if a specific container is running."""
        result = subprocess.run(
            ["docker", "inspect", "-f", "{{.State.Running}}", container_name],
            capture_output=True,
            text=True
        )
        return result.stdout.strip().lower() == "true"
    

# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
    def verify_services(self, services: Dict[str, ServiceConfig]) -> bool:
        """
        Verify all services are healthy.
        
        Args:
            services: Dictionary of service configurations
        
        Returns:
            True if all services are running
        """
        all_healthy = True
        
        for name, config in services.items():
            if isinstance(config, dict):
                config = ServiceConfig(**config)
            
            container_name = config.container
            is_running = self.is_container_running(container_name)
            
            if is_running:
                logger.info(f"✓ {name} ({container_name}): Running on port {config.port}")
            else:
                logger.error(f"✗ {name} ({container_name}): Not running")
                all_healthy = False
        
        return all_healthy
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def show_status(self, services: Dict[str, ServiceConfig]) -> None:
        """Display status of all services."""
        logger.info("Service Status:")
        logger.info("-" * 50)
        
        container_status = self.get_container_status()
        
        for name, config in services.items():
            if isinstance(config, dict):
                config = ServiceConfig(**config)
            
            status = container_status.get(config.container, {})
            state = status.get('state', 'unknown')
            ports = status.get('ports', '')
            
            if state == 'running':
                logger.info(f"  ✓ {name}: Running")
                if ports:
                    logger.info(f"    Ports: {ports}")
            else:
                logger.warning(f"  ✗ {name}: {state}")
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def remove_by_prefix(self, prefix: str, dry_run: bool = False) -> bool:
        """
        Remove containers, networks and volumes matching a prefix.
        
        Args:
            prefix: Prefix to match (e.g., 'week5')
            dry_run: Show what would be done without executing
        
        Returns:
            True if successful
        """
        # Remove containers
        result = subprocess.run(
            ["docker", "ps", "-a", "--filter", f"name={prefix}", "--format", "{{.Names}}"],
            capture_output=True,
            text=True
        )
        containers = [c for c in result.stdout.strip().split('\n') if c]
        
        for container in containers:
            if dry_run:
                logger.info(f"[DRY RUN] Would remove container: {container}")
            else:
                subprocess.run(["docker", "rm", "-f", container], capture_output=True)
                logger.info(f"Removed container: {container}")
        
        # Remove networks
        result = subprocess.run(
            ["docker", "network", "ls", "--filter", f"name={prefix}", "--format", "{{.Name}}"],
            capture_output=True,
            text=True
        )
        networks = [n for n in result.stdout.strip().split('\n') if n]
        
        for network in networks:
            if dry_run:
                logger.info(f"[DRY RUN] Would remove network: {network}")
            else:
                subprocess.run(["docker", "network", "rm", network], capture_output=True)
                logger.info(f"Removed network: {network}")
        
        return True
    

# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
    def system_prune(self, all_unused: bool = False) -> bool:
        """
        Remove unused Docker resources.
        
        Args:
            all_unused: Remove all unused images, not just dangling
        
        Returns:
            True if successful
        """
        logger.info("Pruning unused Docker resources...")
        cmd = ["docker", "system", "prune", "-f"]
        if all_unused:
            cmd.append("-a")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("Prune completed successfully")
        return result.returncode == 0
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def exec_command(self, container: str, command: List[str], interactive: bool = False) -> subprocess.CompletedProcess:
        """
        Execute a command in a running container.
        
        Args:
            container: Container name
            command: Command to execute
            interactive: Use interactive mode
        
        Returns:
            Completed process result
        """
        cmd = ["docker", "exec"]
        if interactive:
            cmd.append("-it")
        cmd.append(container)
        cmd.extend(command)
        
        return subprocess.run(cmd, capture_output=not interactive, text=True)


if __name__ == "__main__":
    # Quick test
    import sys
    
    if len(sys.argv) > 1:
        docker_dir = Path(sys.argv[1])
    else:
        docker_dir = Path(__file__).parent.parent.parent / "docker"
    
    try:
        dm = DockerManager(docker_dir)
        print(f"Docker manager initialised for: {docker_dir}")
        dm.show_status({})
    except FileNotFoundError as e:
        print(f"Error: {e}")
