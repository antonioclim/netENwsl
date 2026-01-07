#!/usr/bin/env python3
"""
Docker Management Utilities
NETWORKING class - ASE, Informatics | by Revolvix

Provides helper functions for Docker Compose operations in the Week 12 lab.
"""

import subprocess
import time
import socket
from pathlib import Path
from typing import Any, Optional

from .logger import setup_logger


class DockerManager:
    """Manages Docker Compose operations for the laboratory."""
    
    def __init__(self, docker_dir: Path):
        """
        Initialise the Docker manager.
        
        Args:
            docker_dir: Path to directory containing docker-compose.yml
        """
        self.docker_dir = docker_dir
        self.compose_file = docker_dir / "docker-compose.yml"
        self.logger = setup_logger("docker_manager")
        
        if not self.compose_file.exists():
            raise FileNotFoundError(f"Docker Compose file not found: {self.compose_file}")
    
    def _run_compose(self, args: list[str], check: bool = True) -> subprocess.CompletedProcess:
        """
        Run a docker compose command.
        
        Args:
            args: Arguments to pass to docker compose
            check: Whether to raise on non-zero exit
        
        Returns:
            Completed process result
        """
        cmd = ["docker", "compose", "-f", str(self.compose_file)] + args
        self.logger.debug(f"Running: {' '.join(cmd)}")
        
        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=self.docker_dir,
            check=check
        )
    
    def compose_build(self, no_cache: bool = False) -> bool:
        """
        Build Docker images.
        
        Args:
            no_cache: Whether to build without cache
        
        Returns:
            True if successful
        """
        self.logger.info("Building Docker images...")
        args = ["build"]
        if no_cache:
            args.append("--no-cache")
        
        try:
            result = self._run_compose(args)
            if result.returncode == 0:
                self.logger.info("Build completed successfully")
                return True
            else:
                self.logger.error(f"Build failed: {result.stderr}")
                return False
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Build error: {e}")
            return False
    
    def compose_up(self, detach: bool = True, build: bool = False) -> bool:
        """
        Start containers with docker compose up.
        
        Args:
            detach: Run in detached mode
            build: Build images before starting
        
        Returns:
            True if successful
        """
        self.logger.info("Starting containers...")
        args = ["up"]
        if detach:
            args.append("-d")
        if build:
            args.append("--build")
        
        try:
            result = self._run_compose(args)
            if result.returncode == 0:
                self.logger.info("Containers started successfully")
                return True
            else:
                self.logger.error(f"Start failed: {result.stderr}")
                return False
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Start error: {e}")
            return False
    
    def compose_down(self, volumes: bool = False, dry_run: bool = False) -> bool:
        """
        Stop and remove containers.
        
        Args:
            volumes: Also remove volumes
            dry_run: Only show what would be done
        
        Returns:
            True if successful
        """
        args = ["down"]
        if volumes:
            args.append("-v")
        
        if dry_run:
            self.logger.info(f"[DRY RUN] Would run: docker compose {' '.join(args)}")
            return True
        
        self.logger.info("Stopping containers...")
        try:
            result = self._run_compose(args)
            if result.returncode == 0:
                self.logger.info("Containers stopped successfully")
                return True
            else:
                self.logger.error(f"Stop failed: {result.stderr}")
                return False
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Stop error: {e}")
            return False
    
    def compose_logs(self, follow: bool = False, tail: Optional[int] = None) -> str:
        """
        Get container logs.
        
        Args:
            follow: Follow log output (blocking)
            tail: Number of lines to show
        
        Returns:
            Log output as string
        """
        args = ["logs"]
        if follow:
            args.append("-f")
        if tail:
            args.extend(["--tail", str(tail)])
        
        result = self._run_compose(args, check=False)
        return result.stdout
    
    def get_container_status(self) -> dict[str, str]:
        """
        Get status of all containers.
        
        Returns:
            Dict mapping container name to status
        """
        result = self._run_compose(["ps", "--format", "json"], check=False)
        
        # Parse container statuses
        status = {}
        if result.returncode == 0 and result.stdout:
            import json
            for line in result.stdout.strip().split("\n"):
                if line:
                    try:
                        container = json.loads(line)
                        name = container.get("Name", "unknown")
                        state = container.get("State", "unknown")
                        status[name] = state
                    except json.JSONDecodeError:
                        continue
        
        return status
    
    def verify_services(self, services: dict[str, dict[str, Any]]) -> bool:
        """
        Verify that services are responding on their configured ports.
        
        Args:
            services: Dict mapping service name to config with 'port' and optional 'startup_time'
        
        Returns:
            True if all services are healthy
        """
        all_healthy = True
        
        for name, config in services.items():
            port = config.get("port")
            startup_time = config.get("startup_time", 5)
            
            self.logger.info(f"Checking {name} on port {port}...")
            time.sleep(startup_time)
            
            if self._check_port(port):
                self.logger.info(f"  [{name}] OK - responding on port {port}")
            else:
                self.logger.error(f"  [{name}] FAIL - not responding on port {port}")
                all_healthy = False
        
        return all_healthy
    
    def _check_port(self, port: int, host: str = "127.0.0.1", timeout: float = 2.0) -> bool:
        """Check if a port is accepting connections."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                result = s.connect_ex((host, port))
                return result == 0
        except Exception:
            return False
    
    def show_status(self, services: dict[str, dict[str, Any]]) -> None:
        """Display current status of all services."""
        print("\nWeek 12 Laboratory Status")
        print("=" * 50)
        
        container_status = self.get_container_status()
        
        for name, config in services.items():
            port = config.get("port")
            container = config.get("container", f"week12_{name}")
            
            # Container status
            c_status = container_status.get(container, "not found")
            
            # Port status
            p_status = "listening" if self._check_port(port) else "not listening"
            
            print(f"  {name}:")
            print(f"    Container: {c_status}")
            print(f"    Port {port}: {p_status}")
        
        print("=" * 50)
    
    def remove_by_prefix(self, prefix: str, dry_run: bool = False) -> bool:
        """
        Remove Docker resources matching a prefix.
        
        Args:
            prefix: Prefix to match (e.g., 'week12')
            dry_run: Only show what would be done
        
        Returns:
            True if successful
        """
        resources_to_remove = []
        
        # Find containers
        result = subprocess.run(
            ["docker", "ps", "-a", "--format", "{{.Names}}", "--filter", f"name={prefix}"],
            capture_output=True,
            text=True
        )
        containers = [c.strip() for c in result.stdout.split("\n") if c.strip()]
        resources_to_remove.extend(("container", c) for c in containers)
        
        # Find networks
        result = subprocess.run(
            ["docker", "network", "ls", "--format", "{{.Name}}", "--filter", f"name={prefix}"],
            capture_output=True,
            text=True
        )
        networks = [n.strip() for n in result.stdout.split("\n") if n.strip()]
        resources_to_remove.extend(("network", n) for n in networks)
        
        # Find volumes
        result = subprocess.run(
            ["docker", "volume", "ls", "--format", "{{.Name}}", "--filter", f"name={prefix}"],
            capture_output=True,
            text=True
        )
        volumes = [v.strip() for v in result.stdout.split("\n") if v.strip()]
        resources_to_remove.extend(("volume", v) for v in volumes)
        
        if dry_run:
            for rtype, rname in resources_to_remove:
                self.logger.info(f"[DRY RUN] Would remove {rtype}: {rname}")
            return True
        
        success = True
        for rtype, rname in resources_to_remove:
            cmd = ["docker", rtype, "rm", "-f", rname]
            result = subprocess.run(cmd, capture_output=True)
            if result.returncode == 0:
                self.logger.info(f"Removed {rtype}: {rname}")
            else:
                self.logger.warning(f"Failed to remove {rtype}: {rname}")
                success = False
        
        return success
    
    def system_prune(self) -> bool:
        """Run docker system prune to clean unused resources."""
        self.logger.info("Pruning unused Docker resources...")
        result = subprocess.run(
            ["docker", "system", "prune", "-f"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            self.logger.info("Prune completed")
            self.logger.info(result.stdout)
            return True
        else:
            self.logger.error(f"Prune failed: {result.stderr}")
            return False
