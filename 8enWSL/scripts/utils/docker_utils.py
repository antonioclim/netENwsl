#!/usr/bin/env python3
"""
Docker Utilities
NETWORKING class - ASE, Informatics | by Revolvix

Provides Docker management functions for laboratory scripts.
"""

import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
import json

from .logger import setup_logger

logger = setup_logger("docker_utils")


class DockerManager:
    """Manages Docker containers for the laboratory environment."""
    
    def __init__(self, compose_dir: Path):
        """
        Initialise Docker manager.
        
        Args:
            compose_dir: Directory containing docker-compose.yml
        """
        self.compose_dir = Path(compose_dir)
        self.compose_file = self.compose_dir / "docker-compose.yml"
        
        if not self.compose_file.exists():
            raise FileNotFoundError(f"Compose file not found: {self.compose_file}")
    
    def _run_compose(
        self,
        *args: str,
        capture: bool = False,
        check: bool = True
    ) -> subprocess.CompletedProcess:
        """Run a docker compose command."""
        cmd = ["docker", "compose", "-f", str(self.compose_file)] + list(args)
        
        return subprocess.run(
            cmd,
            cwd=self.compose_dir,
            capture_output=capture,
            text=True,
            check=check
        )
    
    def _run_docker(
        self,
        *args: str,
        capture: bool = False,
        check: bool = True
    ) -> subprocess.CompletedProcess:
        """Run a docker command."""
        cmd = ["docker"] + list(args)
        
        return subprocess.run(
            cmd,
            capture_output=capture,
            text=True,
            check=check
        )
    
    def compose_up(self, detach: bool = True, build: bool = False) -> bool:
        """
        Start containers using docker compose.
        
        Args:
            detach: Run in detached mode
            build: Build images before starting
        
        Returns:
            True if successful
        """
        args = ["up"]
        if detach:
            args.append("-d")
        if build:
            args.append("--build")
        
        try:
            self._run_compose(*args)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to start containers: {e}")
            return False
    
    def compose_down(self, volumes: bool = False, dry_run: bool = False) -> bool:
        """
        Stop containers using docker compose.
        
        Args:
            volumes: Also remove volumes
            dry_run: Only show what would be done
        
        Returns:
            True if successful
        """
        if dry_run:
            logger.info("[DRY RUN] Would execute: docker compose down" +
                       (" -v" if volumes else ""))
            return True
        
        args = ["down"]
        if volumes:
            args.append("-v")
        
        try:
            self._run_compose(*args)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to stop containers: {e}")
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
            logger.error(f"Failed to build images: {e}")
            return False
    
    def get_container_status(self) -> Dict[str, Dict[str, Any]]:
        """
        Get status of all compose containers.
        
        Returns:
            Dictionary mapping container names to status info
        """
        try:
            result = self._run_compose("ps", "--format", "json", capture=True)
            containers = {}
            
            for line in result.stdout.strip().split("\n"):
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    name = data.get("Name", data.get("name", "unknown"))
                    containers[name] = {
                        "state": data.get("State", data.get("state", "unknown")),
                        "status": data.get("Status", data.get("status", "")),
                        "ports": data.get("Ports", data.get("ports", "")),
                    }
                except json.JSONDecodeError:
                    continue
            
            return containers
        except subprocess.CalledProcessError:
            return {}
    
    def verify_services(self, services: Dict[str, Dict[str, Any]]) -> bool:
        """
        Verify all services are running and healthy.
        
        Args:
            services: Dictionary mapping service names to their expected config
        
        Returns:
            True if all services are healthy
        """
        status = self.get_container_status()
        all_healthy = True
        
        for name, config in services.items():
            container_name = config.get("container", name)
            container_status = status.get(container_name, {})
            state = container_status.get("state", "unknown")
            
            if state == "running":
                logger.info(f"  ✓ {name}: running")
            else:
                logger.error(f"  ✗ {name}: {state}")
                all_healthy = False
        
        return all_healthy
    
    def show_status(self, services: Dict[str, Dict[str, Any]]):
        """Display status of services."""
        print("\n" + "=" * 50)
        print("Service Status")
        print("=" * 50 + "\n")
        
        status = self.get_container_status()
        
        if not status:
            print("  No containers are running.")
            return
        
        for name, info in status.items():
            state = info.get("state", "unknown")
            status_text = info.get("status", "")
            ports = info.get("ports", "")
            
            if state == "running":
                state_colour = "\033[92m"  # Green
            elif state == "exited":
                state_colour = "\033[91m"  # Red
            else:
                state_colour = "\033[93m"  # Yellow
            
            print(f"  {name}:")
            print(f"    State:  {state_colour}{state}\033[0m")
            if status_text:
                print(f"    Status: {status_text}")
            if ports:
                print(f"    Ports:  {ports}")
            print()
    
    def get_logs(self, service: Optional[str] = None, tail: int = 100) -> str:
        """
        Get container logs.
        
        Args:
            service: Specific service name (None for all)
            tail: Number of lines to retrieve
        
        Returns:
            Log output as string
        """
        args = ["logs", "--tail", str(tail)]
        if service:
            args.append(service)
        
        try:
            result = self._run_compose(*args, capture=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error getting logs: {e}"
    
    def remove_by_prefix(self, prefix: str, dry_run: bool = False):
        """
        Remove Docker resources matching a prefix.
        
        Args:
            prefix: Resource name prefix
            dry_run: Only show what would be done
        """
        # Remove containers
        try:
            result = self._run_docker(
                "ps", "-a", "--format", "{{.Names}}",
                capture=True, check=False
            )
            for name in result.stdout.strip().split("\n"):
                if name and name.startswith(prefix):
                    if dry_run:
                        logger.info(f"[DRY RUN] Would remove container: {name}")
                    else:
                        logger.info(f"Removing container: {name}")
                        self._run_docker("rm", "-f", name, check=False)
        except Exception as e:
            logger.warning(f"Error removing containers: {e}")
        
        # Remove networks
        try:
            result = self._run_docker(
                "network", "ls", "--format", "{{.Name}}",
                capture=True, check=False
            )
            for name in result.stdout.strip().split("\n"):
                if name and prefix in name:
                    if dry_run:
                        logger.info(f"[DRY RUN] Would remove network: {name}")
                    else:
                        logger.info(f"Removing network: {name}")
                        self._run_docker("network", "rm", name, check=False)
        except Exception as e:
            logger.warning(f"Error removing networks: {e}")
        
        # Remove volumes
        try:
            result = self._run_docker(
                "volume", "ls", "--format", "{{.Name}}",
                capture=True, check=False
            )
            for name in result.stdout.strip().split("\n"):
                if name and prefix in name:
                    if dry_run:
                        logger.info(f"[DRY RUN] Would remove volume: {name}")
                    else:
                        logger.info(f"Removing volume: {name}")
                        self._run_docker("volume", "rm", name, check=False)
        except Exception as e:
            logger.warning(f"Error removing volumes: {e}")
    
    def system_prune(self, all_unused: bool = False):
        """
        Prune unused Docker resources.
        
        Args:
            all_unused: Remove all unused images, not just dangling
        """
        args = ["system", "prune", "-f"]
        if all_unused:
            args.append("-a")
        
        try:
            self._run_docker(*args)
        except subprocess.CalledProcessError as e:
            logger.warning(f"Error during prune: {e}")
