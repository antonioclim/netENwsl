#!/usr/bin/env python3
"""
Docker Management Utilities
NETWORKING class - ASE, Informatics | by ing. dr. Antonio Clim

Provides utilities for managing Docker containers and networks.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import subprocess
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
from .logger import get_logger



# ═══════════════════════════════════════════════════════════════════════════════
# CLASS_DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════
class DockerManager:
    """Manages Docker operations for the laboratory environment."""
    

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
    def __init__(self, docker_dir: Path):
        """
        Initialise the Docker manager.
        
        Args:
            docker_dir: Path to the directory containing docker-compose.yml
        """
        self.docker_dir = docker_dir
        self.compose_file = docker_dir / "docker-compose.yml"
        self.logger = get_logger("docker")
        
        if not self.compose_file.exists():
            raise FileNotFoundError(f"docker-compose.yml not found in {docker_dir}")
    

# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
    def _run_compose(
        self, 
        args: List[str], 
        capture: bool = False,
        check: bool = True
    ) -> subprocess.CompletedProcess:
        """Run a docker compose command."""
        cmd = ["docker", "compose", "-f", str(self.compose_file)] + args
        
        if capture:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.docker_dir.parent
            )
        else:
            result = subprocess.run(
                cmd,
                cwd=self.docker_dir.parent
            )
        
        if check and result.returncode != 0:
            raise RuntimeError(f"Docker compose command failed: {' '.join(args)}")
        
        return result
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def compose_up(
        self, 
        detach: bool = True, 
        build: bool = False,
        extra_args: Optional[List[str]] = None
    ) -> bool:
        """
        Start containers with docker compose up.
        
        Args:
            detach: Run in detached mode
            build: Build images before starting
            extra_args: Additional arguments to pass
            
        Returns:
            True on success, False on failure
        """
        args = ["up"]
        if detach:
            args.append("-d")
        if build:
            args.append("--build")
        if extra_args:
            args.extend(extra_args)
        
        self.logger.info("Starting containers...")
        try:
            self._run_compose(args)
            return True
        except RuntimeError:
            return False
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def compose_down(self, volumes: bool = False, dry_run: bool = False) -> None:
        """Stop and remove containers."""
        args = ["down"]
        if volumes:
            args.append("-v")
        
        if dry_run:
            self.logger.info(f"[DRY RUN] Would run: docker compose {' '.join(args)}")
            return
        
        self.logger.info("Stopping containers...")
        self._run_compose(args)
    

# ═══════════════════════════════════════════════════════════════════════════════
# RESOURCE_CREATION
# ═══════════════════════════════════════════════════════════════════════════════
    def compose_build(self, no_cache: bool = False) -> bool:
        """
        Build Docker images.
        
        Args:
            no_cache: Build without using cache
            
        Returns:
            True on success, False on failure
        """
        args = ["build"]
        if no_cache:
            args.append("--no-cache")
        
        self.logger.info("Building images...")
        try:
            self._run_compose(args)
            return True
        except RuntimeError:
            return False
    

# ═══════════════════════════════════════════════════════════════════════════════
# LOG_RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
    def compose_logs(self, follow: bool = False, tail: int = 100) -> None:
        """Show container logs."""
        args = ["logs", f"--tail={tail}"]
        if follow:
            args.append("-f")
        self._run_compose(args)
    

# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
    def get_running_containers(self) -> List[str]:
        """Get list of running container names."""
        result = self._run_compose(["ps", "-q"], capture=True, check=False)
        if result.returncode != 0:
            return []
        
        container_ids = result.stdout.strip().split('\n')
        return [c for c in container_ids if c]
    

# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
    def is_container_running(self, container_name: str) -> bool:
        """Check if a specific container is running."""
        try:
            result = subprocess.run(
                ["docker", "inspect", "-f", "{{.State.Running}}", container_name],
                capture_output=True,
                text=True
            )
            return result.stdout.strip() == "true"
        except Exception:
            return False
    

# ═══════════════════════════════════════════════════════════════════════════════
# CONTAINER_MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════
    def wait_for_container(
        self, 
        container_name: str, 
        timeout: int = 30,
        check_interval: float = 1.0
    ) -> bool:
        """Wait for a container to be running."""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if self.is_container_running(container_name):
                return True
            time.sleep(check_interval)
        
        return False
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def exec_command(
        self, 
        container: str, 
        command: List[str],
        capture: bool = False
    ) -> subprocess.CompletedProcess:
        """Execute a command in a container."""
        cmd = ["docker", "exec", container] + command
        
        if capture:
            return subprocess.run(cmd, capture_output=True, text=True)
        else:
            return subprocess.run(cmd)
    

# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
    def verify_services(self, services: Dict[str, Any]) -> bool:
        """
        Verify that all services are running and healthy.
        
        Args:
            services: Dictionary mapping service names to their configuration
                     including 'container', 'port' and optional 'health_check'
        
        Returns:
            True if all services are verified, False otherwise
        """
        all_healthy = True
        
        for name, config in services.items():
            container = config.get('container')
            port = config.get('port')
            
            self.logger.info(f"Checking {name}...")
            
            # Check container is running
            if not self.is_container_running(container):
                self.logger.error(f"  Container {container} is not running")
                all_healthy = False
                continue
            
            self.logger.info(f"  Container running: {container}")
            
            # Check port if specified
            if port:
                result = subprocess.run(
                    ["docker", "exec", container, "nc", "-z", "localhost", str(port)],
                    capture_output=True
                )
                if result.returncode == 0:
                    self.logger.info(f"  Port {port} is listening")
                else:
                    self.logger.warning(f"  Port {port} not yet available")
        
        return all_healthy
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def show_status(self, services: Optional[Dict[str, Any]] = None) -> None:
        """Display the status of containers."""
        self.logger.info("Container Status:")
        self._run_compose(["ps"])
        
        if services:
            print("\nService Details:")
            for name, config in services.items():
                container = config.get('container')
                port = config.get('port')
                running = "✓" if self.is_container_running(container) else "✗"
                print(f"  {running} {name}: {container}:{port}")
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def remove_by_prefix(self, prefix: str, dry_run: bool = False) -> None:
        """Remove containers, networks and volumes matching a prefix."""
        # Remove containers
        result = subprocess.run(
            ["docker", "ps", "-a", "-q", "--filter", f"name={prefix}"],
            capture_output=True,
            text=True
        )
        containers = result.stdout.strip().split('\n')
        containers = [c for c in containers if c]
        
        if containers:
            if dry_run:
                self.logger.info(f"[DRY RUN] Would remove containers: {containers}")
            else:
                subprocess.run(["docker", "rm", "-f"] + containers)
                self.logger.info(f"Removed {len(containers)} containers")
        
        # Remove networks
        result = subprocess.run(
            ["docker", "network", "ls", "-q", "--filter", f"name={prefix}"],
            capture_output=True,
            text=True
        )
        networks = result.stdout.strip().split('\n')
        networks = [n for n in networks if n]
        
        if networks:
            if dry_run:
                self.logger.info(f"[DRY RUN] Would remove networks: {networks}")
            else:
                for net in networks:
                    subprocess.run(["docker", "network", "rm", net], capture_output=True)
                self.logger.info(f"Removed {len(networks)} networks")
    

# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
    def system_prune(self) -> None:
        """Prune unused Docker resources."""
        self.logger.info("Pruning unused Docker resources...")
        subprocess.run(["docker", "system", "prune", "-f"])

if __name__ == "__main__":
    # Module loaded directly - display module info
    print(f"Module {__name__} loaded successfully.")
    print(f"This module provides utility functions for the networking laboratory.")
