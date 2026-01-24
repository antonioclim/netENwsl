"""
Docker Management Utilities
NETWORKING class - ASE, Informatics | by Revolvix

Provides Docker Compose orchestration and container management.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import subprocess
import time
from pathlib import Path
from typing import Any, Dict, Optional

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
    

# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
    def _run_compose(
        self,
        args: list,
        capture: bool = False,
        timeout: int = 300
    ) -> subprocess.CompletedProcess:
        """Run a docker compose command."""
        cmd = ["docker", "compose", "-f", str(self.compose_file)] + args
        
        return subprocess.run(
            cmd,
            cwd=self.compose_dir,
            capture_output=capture,
            text=True,
            timeout=timeout
        )
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def compose_up(self, detach: bool = True, build: bool = False) -> bool:
        """
        Start Docker Compose services.
        
        Args:
            detach: Run in detached mode
            build: Force rebuild of images
        
        Returns:
            True if successful
        """
        args = ["up"]
        if detach:
            args.append("-d")
        if build:
            args.append("--build")
        
        logger.info("Starting Docker Compose services...")
        result = self._run_compose(args)
        return result.returncode == 0
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def compose_down(self, volumes: bool = False, dry_run: bool = False) -> bool:
        """
        Stop Docker Compose services.
        
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
            logger.info(f"[DRY RUN] Would run: docker compose {' '.join(args)}")
            return True
        
        logger.info("Stopping Docker Compose services...")
        result = self._run_compose(args)
        return result.returncode == 0
    

# ═══════════════════════════════════════════════════════════════════════════════
# RESOURCE_CREATION
# ═══════════════════════════════════════════════════════════════════════════════
    def compose_build(self) -> bool:
        """Build Docker images."""
        logger.info("Building Docker images...")
        result = self._run_compose(["build"])
        return result.returncode == 0
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def get_status(self) -> Dict[str, Any]:
        """Get status of all services."""
        result = self._run_compose(["ps", "--format", "json"], capture=True)
        
        if result.returncode != 0:
            return {"error": result.stderr}
        
        import json
        try:
            # Docker Compose outputs one JSON object per line
            services = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    services.append(json.loads(line))
            return {"services": services}
        except json.JSONDecodeError:
            return {"raw": result.stdout}
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def show_status(self, services: Dict[str, Any]) -> None:
        """Print formatted status of services."""
        result = self._run_compose(["ps"], capture=True)
        if result.returncode == 0:
            print(result.stdout)
        else:
            print("Unable to retrieve service status")
            print(result.stderr)
    

# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
    def verify_services(self, services: Dict[str, Any]) -> bool:
        """
        Verify all services are healthy.
        
        Args:
            services: Dictionary of service definitions
        
        Returns:
            True if all services are healthy
        """
        all_healthy = True
        
        for name, config in services.items():
            container = config.get("container", name)
            port = config.get("port")
            health_check = config.get("health_check")
            
            # Check container is running
            result = subprocess.run(
                ["docker", "inspect", "-f", "{{.State.Running}}", container],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0 or result.stdout.strip() != "true":
                logger.warning(f"{name}: Container not running")
                all_healthy = False
                continue
            
            logger.info(f"{name}: Running on port {port}")
        
        return all_healthy
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def remove_by_prefix(self, prefix: str, dry_run: bool = False) -> None:
        """Remove Docker resources with a given prefix."""
        # Remove containers
        result = subprocess.run(
            ["docker", "ps", "-a", "--format", "{{.Names}}"],
            capture_output=True,
            text=True
        )
        
        for name in result.stdout.strip().split('\n'):
            if name.startswith(prefix):
                if dry_run:
                    logger.info(f"[DRY RUN] Would remove container: {name}")
                else:
                    subprocess.run(["docker", "rm", "-f", name])
                    logger.info(f"Removed container: {name}")
        
        # Remove networks
        result = subprocess.run(
            ["docker", "network", "ls", "--format", "{{.Name}}"],
            capture_output=True,
            text=True
        )
        
        for name in result.stdout.strip().split('\n'):
            if name.startswith(prefix):
                if dry_run:
                    logger.info(f"[DRY RUN] Would remove network: {name}")
                else:
                    subprocess.run(["docker", "network", "rm", name])
                    logger.info(f"Removed network: {name}")
    

# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
    def system_prune(self) -> None:
        """Prune unused Docker resources."""
        logger.info("Pruning unused Docker resources...")
        subprocess.run(["docker", "system", "prune", "-f"])
    

# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
    def exec_command(self, container: str, command: list) -> subprocess.CompletedProcess:
        """Execute a command in a running container."""
        cmd = ["docker", "exec", container] + command
        return subprocess.run(cmd, capture_output=True, text=True)

if __name__ == "__main__":
    # Module loaded directly - display module info
    print(f"Module {__name__} loaded successfully.")
    print(f"This module provides utility functions for the networking laboratory.")
