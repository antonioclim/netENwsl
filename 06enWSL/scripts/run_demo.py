#!/usr/bin/env python3
"""
Week 6 Demonstration Runner
NETWORKING class - ASE, Informatics | by Revolvix

Runs automated demonstrations for NAT/PAT and SDN exercises.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.logger import setup_logger

logger = setup_logger("run_demo")

DEMOS = {
    "nat": {
        "description": "NAT/PAT topology with MASQUERADE translation",
        "topology": "topo_nat.py",
        "mode": "cli"
    },
    "nat-test": {
        "description": "NAT topology automated smoke test",
        "topology": "topo_nat.py",
        "mode": "test"
    },
    "sdn": {
        "description": "SDN topology with OpenFlow policies",
        "topology": "topo_sdn.py",
        "mode": "cli",
        "extra_args": ["--install-flows"]
    },
    "sdn-test": {
        "description": "SDN topology automated smoke test",
        "topology": "topo_sdn.py",
        "mode": "test",
        "extra_args": ["--install-flows"]
    },
    "nat-visual": {
        "description": "NAT translation visualisation (automated)",
        "script": "nat_visual_demo"
    },
    "sdn-flows": {
        "description": "SDN flow installation demonstration",
        "script": "sdn_flow_demo"
    },
}



# ═══════════════════════════════════════════════════════════════════════════════
# VERIFY_PREREQUISITES
# ═══════════════════════════════════════════════════════════════════════════════
def check_mininet() -> bool:
    """Check if Mininet is available."""
    try:
        result = subprocess.run(
            ["mn", "--version"],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False



# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
def run_topology_demo(
    topology: str,
    mode: str,
    extra_args: Optional[list[str]] = None
) -> int:
    """
    Run a Mininet topology demonstration.
    
    Args:
        topology: Topology filename
        mode: Either 'cli' or 'test'
        extra_args: Additional arguments to pass
        
    Returns:
        Exit code
    """
    # Locate topology file
    topo_paths = [
        PROJECT_ROOT / "src" / "exercises" / topology,
        PROJECT_ROOT / "mininet" / "topologies" / topology,
    ]
    
    topo_file = None
    for path in topo_paths:
        if path.exists():
            topo_file = path
            break
    
    if topo_file is None:
        logger.error(f"Topology file not found: {topology}")
        logger.info(f"Searched in: {[str(p) for p in topo_paths]}")
        return 1
    
    # Build command
    cmd = ["sudo", "python3", str(topo_file)]
    
    if mode == "cli":
        cmd.append("--cli")
    elif mode == "test":
        cmd.append("--test")
    
    if extra_args:
        cmd.extend(extra_args)
    
    logger.info(f"Running: {' '.join(cmd)}")
    print()
    
    try:
        result = subprocess.run(cmd)
        return result.returncode
    except KeyboardInterrupt:
        print("\nDemo interrupted")
        return 130



# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
def run_nat_visual_demo() -> int:
    """
    Run NAT visualisation demo showing PAT in action.
    """
    logger.info("NAT Translation Visualisation Demo")
    logger.info("=" * 60)
    print()
    print("This demo will:")
    print("  1. Start the NAT topology")
    print("  2. Launch NAT observer on h3")
    print("  3. Generate connections from h1 and h2")
    print("  4. Display translation observations")
    print()
    
    # This would normally run a multi-step automated demo
    # For now, we'll guide the user to the interactive version
    logger.info("Starting interactive NAT demo...")
    return run_topology_demo("topo_nat.py", "cli")



# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTE_OPERATION
# ═══════════════════════════════════════════════════════════════════════════════
def run_sdn_flow_demo() -> int:
    """
    Run SDN flow installation demonstration.
    """
    logger.info("SDN Flow Installation Demo")
    logger.info("=" * 60)
    print()
    print("This demo will:")
    print("  1. Start the SDN topology with static flows")
    print("  2. Show initial flow table")
    print("  3. Demonstrate permitted traffic (h1 ↔ h2)")
    print("  4. Demonstrate blocked traffic (h1 → h3)")
    print("  5. Show updated flow table with statistics")
    print()
    
    logger.info("Starting interactive SDN demo...")
    return run_topology_demo("topo_sdn.py", "cli", ["--install-flows"])



# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
def list_demos() -> None:
    """Print available demonstrations."""
    print()
    print("Available Demonstrations:")
    print("=" * 60)
    
    for name, info in DEMOS.items():
        desc = info.get("description", "No description")
        print(f"  {name:<15} - {desc}")
    
    print()
    print("Usage: python scripts/run_demo.py --demo <name>")
    print()



# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ENTRY_POINT
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run Week 6 Laboratory Demonstrations"
    )
    parser.add_argument(
        "--demo", "-d",
        choices=list(DEMOS.keys()),
        help="Demo to run"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List available demos"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    args = parser.parse_args()
    
    if args.verbose:
        from scripts.utils.logger import set_verbose
        set_verbose(logger, True)
    
    if args.list or not args.demo:
        list_demos()
        return 0
    
    # Check prerequisites
    if not check_mininet():
        logger.error("Mininet is not available")
        logger.info("Please run demos inside the Docker container:")
        logger.info("  docker exec -it week6_lab bash")
        logger.info("  make <demo-name>")
        return 1
    
    demo_info = DEMOS.get(args.demo)
    if not demo_info:
        logger.error(f"Unknown demo: {args.demo}")
        list_demos()
        return 1
    
    print()
    logger.info("=" * 60)
    logger.info(f"Demo: {demo_info.get('description', args.demo)}")
    logger.info("=" * 60)
    print()
    
    # Run the demo
    if "script" in demo_info:
        # Custom script demo
        script = demo_info["script"]
        if script == "nat_visual_demo":
            return run_nat_visual_demo()
        elif script == "sdn_flow_demo":
            return run_sdn_flow_demo()
        else:
            logger.error(f"Unknown script: {script}")
            return 1
    else:
        # Topology-based demo
        return run_topology_demo(
            demo_info["topology"],
            demo_info.get("mode", "cli"),
            demo_info.get("extra_args")
        )


if __name__ == "__main__":
    sys.exit(main())
