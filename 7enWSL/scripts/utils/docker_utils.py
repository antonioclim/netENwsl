#!/usr/bin/env python3
"""
Docker Management Utilities
NETWORKING class - ASE, Informatics | by Revolvix

Provides Docker Compose and container management functionality
for the Week 7 laboratory scripts.
"""

from __future__ import annotations

import subprocess
import time
from pathlib import Path
from typing import Dict, Any, Optional, List

from .logger import get_logger


class DockerManager:
    """Manages Docker Compose operations for the laboratory environment."""
    
    def __init__(self, compose_dir: Path) -> None:
        """
        Initialise the Docker manager.
        
        Args:
            compose_dir: Directory containing docker-compose.yml
        """
        self.compose_dir = compose_dir
        self.compose_file = compose_dir / "docker-compose.yml"
        self.logger = get_logger("docker")
        
        if not self.compose_file.exists():
            raise FileNotFoundError(f"docker-compose.yml not found in {compose_dir}")
    
    def _run_compose(
        self,
        args: List[str],
        check: bool = True,
        capture: bool = False,
        timeout: int = 120
    ) -> subprocess.CompletedProcess:
        """Run a docker compose command."""
        cmd = ["docker", "compose", "-f", str(self.compose_file)] + args
        self.logger.debug(f"Running: {' '.join(cmd)}")
        
        return subprocess.run(
            cmd,
            check=check,
            capture_output=capture,
            text=True,
            timeout=timeout,
            cwd=self.compose_dir
        )
    
    def _run_docker(
        self,
        args: List[str],
        check: bool = True,
        capture: bool = True,
        timeout: int = 60
    ) -> subprocess.CompletedProcess:
        """Run a docker command."""
        cmd = ["docker"] + args
        self.logger.debug(f"Running: {' '.join(cmd)}")
        
        return subprocess.run(
            cmd,
            check=check,
            capture_output=capture,
            text=True,
            timeout=timeout
        )
    
    def compose_up(
        self,
        services: Optional[List[str]] = None,
        detach: bool = True,
        build: bool = False,
        profiles: Optional[List[str]] = None
    ) -> None:
        """
        Start services with docker compose up.
        
        Args:
            services: Specific services to start (default: all)
            detach: Run in detached mode
            build: Build images before starting
            profiles: Docker Compose profiles to enable
        """
        args = []
        
        if profiles:
            for profile in profiles:
                args.extend(["--profile", profile])
        
        args.append("up")
        
        if detach:
            args.append("-d")
        if build:
            args.append("--build")
        
        if services:
            args.extend(services)
        
        self.logger.info("Starting services...")
        self._run_compose(args)
    
    def compose_down(
        self,
        volumes: bool = False,
        remove_orphans: bool = True,
        dry_run: bool = False
    ) -> None:
        """
        Stop and remove containers.
        
        Args:
            volumes: Also remove volumes
            remove_orphans: Remove orphaned containers
            dry_run: Only print what would be done
        """
        if dry_run:
            self.logger.info("[DRY RUN] Would stop and remove containers")
            return
        
        args = ["down"]
        if volumes:
            args.append("-v")
        if remove_orphans:
            args.append("--remove-orphans")
        
        self.logger.info("Stopping services...")
        self._run_compose(args, check=False)
    
    def compose_build(self, services: Optional[List[str]] = None) -> None:
        """Build or rebuild services."""
        args = ["build"]
        if services:
            args.extend(services)
        
        self.logger.info("Building images...")
        self._run_compose(args)
    
    def compose_logs(
        self,
        services: Optional[List[str]] = None,
        follow: bool = False,
        tail: int = 100
    ) -> str:
        """
        Get logs from services.
        
        Args:
            services: Specific services (default: all)
            follow: Follow log output
            tail: Number of lines to show
            
        Returns:
            Log output as string
        """
        args = ["logs", f"--tail={tail}"]
        if follow:
            args.append("-f")
        if services:
            args.extend(services)
        
        result = self._run_compose(args, capture=True, check=False)
        return result.stdout
    
    def compose_ps(self) -> str:
        """Get status of services."""
        result = self._run_compose(["ps"], capture=True, check=False)
        return result.stdout
    
    def show_status(self, services: Dict[str, Any]) -> None:
        """
        Show status of defined services.
        
        Args:
            services: Dictionary of service definitions
        """
        self.logger.info("Service Status:")
        self.logger.info("-" * 50)
        
        ps_output = self.compose_ps()
        print(ps_output)
        
        for name, svc in services.items():
            container = svc.get("container", f"week7_{name}")
            port = svc.get("port", "N/A")
            
            # Check if container is running
            result = self._run_docker(
                ["inspect", "-f", "{{.State.Status}}", container],
                check=False,
                capture=True
            )
            status = result.stdout.strip() if result.returncode == 0 else "not found"
            
            self.logger.info(f"  {name}: {status} (port {port})")
    
    def verify_services(
        self,
        services: Dict[str, Any],
        timeout: int = 30
    ) -> bool:
        """
        Verify all services are healthy.
        
        Args:
            services: Dictionary of service definitions
            timeout: Maximum wait time in seconds
            
        Returns:
            True if all services are healthy
        """
        self.logger.info("Verifying services...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            all_healthy = True
            
            for name, svc in services.items():
                container = svc.get("container", f"week7_{name}")
                
                result = self._run_docker(
                    ["inspect", "-f", "{{.State.Running}}", container],
                    check=False,
                    capture=True
                )
                
                if result.returncode != 0 or result.stdout.strip() != "true":
                    all_healthy = False
                    break
            
            if all_healthy:
                self.logger.info("All services are running")
                return True
            
            time.sleep(2)
        
        self.logger.warning("Some services failed to start within timeout")
        return False
    
    def remove_by_prefix(self, prefix: str, dry_run: bool = False) -> None:
        """
        Remove containers, networks, and volumes by prefix.
        
        Args:
            prefix: Resource name prefix
            dry_run: Only print what would be done
        """
        # Remove containers
        result = self._run_docker(
            ["ps", "-aq", "--filter", f"name={prefix}"],
            check=False
        )
        containers = result.stdout.strip().split()
        
        if containers and containers[0]:
            if dry_run:
                self.logger.info(f"[DRY RUN] Would remove containers: {containers}")
            else:
                self.logger.info(f"Removing containers: {containers}")
                self._run_docker(["rm", "-f"] + containers, check=False)
        
        # Remove networks
        result = self._run_docker(
            ["network", "ls", "-q", "--filter", f"name={prefix}"],
            check=False
        )
        networks = result.stdout.strip().split()
        
        if networks and networks[0]:
            if dry_run:
                self.logger.info(f"[DRY RUN] Would remove networks: {networks}")
            else:
                self.logger.info(f"Removing networks: {networks}")
                for net in networks:
                    self._run_docker(["network", "rm", net], check=False)
        
        # Remove volumes
        result = self._run_docker(
            ["volume", "ls", "-q", "--filter", f"name={prefix}"],
            check=False
        )
        volumes = result.stdout.strip().split()
        
        if volumes and volumes[0]:
            if dry_run:
                self.logger.info(f"[DRY RUN] Would remove volumes: {volumes}")
            else:
                self.logger.info(f"Removing volumes: {volumes}")
                self._run_docker(["volume", "rm"] + volumes, check=False)
    
    def system_prune(self) -> None:
        """Prune unused Docker resources."""
        self.logger.info("Pruning unused Docker resources...")
        self._run_docker(["system", "prune", "-f"], check=False)
