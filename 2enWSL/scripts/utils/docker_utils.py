#!/usr/bin/env python3
"""
Docker management utilities for Week 2 laboratory scripts.
NETWORKING class - ASE, Informatics | by Revolvix
"""

import subprocess
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
from .logger import setup_logger

logger = setup_logger("docker_utils")


class DockerManager:
    """Docker Compose management wrapper."""
    
    def __init__(self, compose_dir: Path):
        """
        Initialise Docker manager.
        
        Args:
            compose_dir: Directory containing docker-compose.yml
        """
        self.compose_dir = Path(compose_dir)
        self.compose_file = self.compose_dir / "docker-compose.yml"
        
        if not self.compose_file.exists():
            raise FileNotFoundError(f"docker-compose.yml not found in {compose_dir}")
    
    def _run_compose(
        self,
        args: List[str],
        capture: bool = False,
        check: bool = True
    ) -> subprocess.CompletedProcess:
        """Run docker compose command."""
        cmd = ["docker", "compose", "-f", str(self.compose_file)] + args
        
        if capture:
            result = subprocess.run(cmd, capture_output=True, text=True)
        else:
            result = subprocess.run(cmd)
        
        if check and result.returncode != 0:
            error_msg = result.stderr if capture else ""
            logger.error(f"Docker compose failed: {' '.join(args)}")
            if error_msg:
                logger.error(error_msg)
        
        return result
    
    def compose_up(self, detach: bool = True, build: bool = False) -> bool:
        """
        Start services defined in docker-compose.yml.
        
        Args:
            detach: Run in background
            build: Rebuild images before starting
        
        Returns:
            True if successful
        """
        args = ["up"]
        if detach:
            args.append("-d")
        if build:
            args.append("--build")
        
        result = self._run_compose(args)
        return result.returncode == 0
    
    def compose_down(self, volumes: bool = False, dry_run: bool = False) -> bool:
        """
        Stop and remove containers.
        
        Args:
            volumes: Also remove volumes
            dry_run: Only show what would be done
        
        Returns:
            True if successful
        """
        if dry_run:
            logger.info("[DRY RUN] Would run: docker compose down" + 
                       (" -v" if volumes else ""))
            return True
        
        args = ["down"]
        if volumes:
            args.append("-v")
        
        result = self._run_compose(args)
        return result.returncode == 0
    
    def compose_build(self, no_cache: bool = False) -> bool:
        """
        Build images.
        
        Args:
            no_cache: Build without using cache
        
        Returns:
            True if successful
        """
        args = ["build"]
        if no_cache:
            args.append("--no-cache")
        
        result = self._run_compose(args)
        return result.returncode == 0
    
    def compose_logs(self, service: Optional[str] = None, follow: bool = False) -> bool:
        """
        Show logs from containers.
        
        Args:
            service: Specific service name or None for all
            follow: Follow log output
        
        Returns:
            True if successful
        """
        args = ["logs"]
        if follow:
            args.append("-f")
        if service:
            args.append(service)
        
        result = self._run_compose(args)
        return result.returncode == 0
    
    def show_status(self, services: Dict[str, Any]) -> None:
        """Show status of all services."""
        result = self._run_compose(["ps", "--format", "table"], capture=True)
        if result.returncode == 0:
            print(result.stdout)
        else:
            logger.warning("Could not get container status")
    
    def verify_services(self, services: Dict[str, Any]) -> bool:
        """
        Verify all services are running and healthy.
        
        Args:
            services: Dictionary of service definitions with health check info
        
        Returns:
            True if all services are healthy
        """
        all_healthy = True
        
        for name, config in services.items():
            container = config.get("container", name)
            port = config.get("port")
            startup_time = config.get("startup_time", 5)
            
            # Check if container is running
            result = subprocess.run(
                ["docker", "inspect", "-f", "{{.State.Running}}", container],
                capture_output=True,
                text=True
            )
            
            is_running = result.returncode == 0 and result.stdout.strip() == "true"
            
            if is_running:
                logger.info(f"Service {name}: running on port {port}")
            else:
                logger.error(f"Service {name}: not running")
                all_healthy = False
        
        return all_healthy
    
    def remove_by_prefix(self, prefix: str, dry_run: bool = False) -> None:
        """
        Remove containers, networks, and volumes with given prefix.
        
        Args:
            prefix: Name prefix to match
            dry_run: Only show what would be removed
        """
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
                logger.info(f"[DRY RUN] Would remove containers: {containers}")
            else:
                subprocess.run(["docker", "rm", "-f"] + containers)
                logger.info(f"Removed {len(containers)} containers")
        
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
                logger.info(f"[DRY RUN] Would remove networks: {networks}")
            else:
                for net in networks:
                    subprocess.run(["docker", "network", "rm", net])
                logger.info(f"Removed {len(networks)} networks")
    
    def system_prune(self) -> None:
        """Remove unused Docker resources."""
        subprocess.run(["docker", "system", "prune", "-f"])
        logger.info("Docker system pruned")
