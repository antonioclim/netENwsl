#!/usr/bin/env python3
"""
Docker Management Utilities
NETWORKING class - ASE, Informatics | by Revolvix

Provides Docker Compose operations and container management functions.
"""

from __future__ import annotations

import subprocess
import time
from pathlib import Path
from typing import Dict, Any, Optional, List

from .logger import get_logger


class DockerManager:
    """Manages Docker Compose operations for the laboratory environment."""
    
    def __init__(self, docker_dir: Path) -> None:
        """
        Initialise Docker manager.
        
        Args:
            docker_dir: Path to directory containing docker-compose.yml
        """
        self.docker_dir = docker_dir
        self.compose_file = docker_dir / "docker-compose.yml"
        self.logger = get_logger("docker_utils")
        
        if not self.compose_file.exists():
            raise FileNotFoundError(f"docker-compose.yml not found in {docker_dir}")
    
    def _run_compose(
        self,
        *args: str,
        capture: bool = False,
        check: bool = True
    ) -> subprocess.CompletedProcess:
        """
        Execute a docker compose command.
        
        Args:
            *args: Command arguments after 'docker compose'
            capture: Whether to capture output
            check: Whether to raise on non-zero exit
        
        Returns:
            CompletedProcess instance
        """
        cmd = ["docker", "compose", "-f", str(self.compose_file)] + list(args)
        self.logger.debug(f"Running: {' '.join(cmd)}")
        
        return subprocess.run(
            cmd,
            capture_output=capture,
            text=True,
            check=check,
            cwd=self.docker_dir.parent
        )
    
    def compose_up(
        self,
        detach: bool = True,
        build: bool = False,
        services: Optional[List[str]] = None
    ) -> bool:
        """
        Start containers with docker compose up.
        
        Args:
            detach: Run in detached mode
            build: Force rebuild before starting
            services: Specific services to start (default: all)
        
        Returns:
            True if successful
        """
        args = ["up"]
        if detach:
            args.append("-d")
        if build:
            args.append("--build")
        if services:
            args.extend(services)
        
        try:
            self._run_compose(*args)
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to start containers: {e}")
            return False
    
    def compose_down(
        self,
        volumes: bool = False,
        remove_orphans: bool = True,
        dry_run: bool = False
    ) -> bool:
        """
        Stop and remove containers.
        
        Args:
            volumes: Also remove volumes
            remove_orphans: Remove containers not defined in compose file
            dry_run: Only show what would be done
        
        Returns:
            True if successful
        """
        if dry_run:
            self.logger.info("[DRY RUN] Would stop and remove containers")
            return True
        
        args = ["down"]
        if volumes:
            args.append("-v")
        if remove_orphans:
            args.append("--remove-orphans")
        
        try:
            self._run_compose(*args)
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to stop containers: {e}")
            return False
    
    def compose_build(self, no_cache: bool = False) -> bool:
        """
        Build container images.
        
        Args:
            no_cache: Build without using cache
        
        Returns:
            True if successful
        """
        args = ["build"]
        if no_cache:
            args.append("--no-cache")
        
        try:
            self._run_compose(*args)
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to build images: {e}")
            return False
    
    def get_container_status(self, container_name: str) -> Optional[str]:
        """
        Get the status of a specific container.
        
        Args:
            container_name: Name of the container
        
        Returns:
            Status string or None if not found
        """
        try:
            result = subprocess.run(
                ["docker", "inspect", "--format", "{{.State.Status}}", container_name],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None
    
    def is_container_running(self, container_name: str) -> bool:
        """Check if a container is running."""
        return self.get_container_status(container_name) == "running"
    
    def wait_for_container(
        self,
        container_name: str,
        timeout: int = 30,
        interval: float = 1.0
    ) -> bool:
        """
        Wait for a container to be running.
        
        Args:
            container_name: Name of the container
            timeout: Maximum seconds to wait
            interval: Check interval in seconds
        
        Returns:
            True if container is running within timeout
        """
        elapsed = 0.0
        while elapsed < timeout:
            if self.is_container_running(container_name):
                return True
            time.sleep(interval)
            elapsed += interval
        return False
    
    def verify_services(self, services: Dict[str, Dict[str, Any]]) -> bool:
        """
        Verify all services are running and healthy.
        
        Args:
            services: Dictionary mapping service names to their configuration
                      Each config should have 'container' key with container name
        
        Returns:
            True if all services are healthy
        """
        all_healthy = True
        
        for name, config in services.items():
            container = config.get("container", f"week1_{name}")
            
            if self.is_container_running(container):
                self.logger.info(f"  {name}: \033[92mrunning\033[0m")
            else:
                self.logger.error(f"  {name}: \033[91mnot running\033[0m")
                all_healthy = False
        
        return all_healthy
    
    def show_status(self, services: Dict[str, Dict[str, Any]]) -> None:
        """
        Display status of all services.
        
        Args:
            services: Dictionary mapping service names to their configuration
        """
        self.logger.info("Service Status:")
        self.logger.info("-" * 40)
        
        for name, config in services.items():
            container = config.get("container", f"week1_{name}")
            port = config.get("port", "N/A")
            status = self.get_container_status(container) or "not found"
            
            if status == "running":
                status_str = f"\033[92m{status}\033[0m"
            else:
                status_str = f"\033[91m{status}\033[0m"
            
            self.logger.info(f"  {name}: {status_str} (port {port})")
    
    def remove_by_prefix(self, prefix: str, dry_run: bool = False) -> None:
        """
        Remove Docker resources matching a prefix.
        
        Args:
            prefix: Prefix to match (e.g., 'week1')
            dry_run: Only show what would be removed
        """
        # Containers
        try:
            result = subprocess.run(
                ["docker", "ps", "-a", "--filter", f"name={prefix}", "--format", "{{.Names}}"],
                capture_output=True,
                text=True
            )
            containers = result.stdout.strip().split("\n")
            containers = [c for c in containers if c]
            
            for container in containers:
                if dry_run:
                    self.logger.info(f"  Would remove container: {container}")
                else:
                    subprocess.run(["docker", "rm", "-f", container], capture_output=True)
                    self.logger.info(f"  Removed container: {container}")
        except subprocess.CalledProcessError:
            pass
        
        # Networks
        try:
            result = subprocess.run(
                ["docker", "network", "ls", "--filter", f"name={prefix}", "--format", "{{.Name}}"],
                capture_output=True,
                text=True
            )
            networks = result.stdout.strip().split("\n")
            networks = [n for n in networks if n and n != "bridge" and n != "host" and n != "none"]
            
            for network in networks:
                if dry_run:
                    self.logger.info(f"  Would remove network: {network}")
                else:
                    subprocess.run(["docker", "network", "rm", network], capture_output=True)
                    self.logger.info(f"  Removed network: {network}")
        except subprocess.CalledProcessError:
            pass
    
    def system_prune(self) -> None:
        """Remove unused Docker resources."""
        try:
            subprocess.run(
                ["docker", "system", "prune", "-f"],
                capture_output=True
            )
            self.logger.info("Pruned unused Docker resources")
        except subprocess.CalledProcessError as e:
            self.logger.warning(f"Failed to prune: {e}")
    
    def exec_command(
        self,
        container_name: str,
        command: List[str],
        interactive: bool = False
    ) -> Optional[str]:
        """
        Execute a command in a running container.
        
        Args:
            container_name: Name of the container
            command: Command and arguments to execute
            interactive: Whether to run interactively
        
        Returns:
            Command output or None if failed
        """
        cmd = ["docker", "exec"]
        if interactive:
            cmd.extend(["-it"])
        cmd.append(container_name)
        cmd.extend(command)
        
        try:
            if interactive:
                subprocess.run(cmd)
                return None
            else:
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                return result.stdout
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Command failed: {e}")
            return None
