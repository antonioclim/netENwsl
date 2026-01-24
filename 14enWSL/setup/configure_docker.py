#!/usr/bin/env python3
"""
Docker Desktop Configuration Helper
NETWORKING class - ASE, Informatics | by Revolvix

Provides guidance and automated configuration assistance for Docker Desktop
with WSL2 backend, optimised for the Week 14 laboratory environment.

This script:
- Validates current Docker configuration
- Suggests best settings for the laboratory
- Helps troubleshoot common Docker issues
- Configures Docker daemon settings where possible
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════
import subprocess
import sys
import json
import platform
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import argparse


# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY_UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════
class Colours:
    """ANSI colour codes for terminal output."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str) -> None:
    """Print a formatted header."""
    print(f"\n{Colours.HEADER}{Colours.BOLD}{'=' * 60}{Colours.ENDC}")
    print(f"{Colours.HEADER}{Colours.BOLD}{text}{Colours.ENDC}")
    print(f"{Colours.HEADER}{Colours.BOLD}{'=' * 60}{Colours.ENDC}\n")


def print_success(text: str) -> None:
    print(f"{Colours.GREEN}[✓] {text}{Colours.ENDC}")


def print_warning(text: str) -> None:
    print(f"{Colours.YELLOW}[!] {text}{Colours.ENDC}")


def print_error(text: str) -> None:
    print(f"{Colours.RED}[✗] {text}{Colours.ENDC}")


def print_info(text: str) -> None:
    print(f"{Colours.CYAN}[i] {text}{Colours.ENDC}")


# ═══════════════════════════════════════════════════════════════════════════════
# COMMAND_UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════
def run_command(cmd: list, timeout: int = 30) -> Tuple[bool, str, str]:
    """Execute a command and return results."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return (result.returncode == 0, result.stdout, result.stderr)
    except subprocess.TimeoutExpired:
        return (False, "", "Command timed out")
    except FileNotFoundError:
        return (False, "", f"Command not found: {cmd[0]}")
    except Exception as e:
        return (False, "", str(e))


# ═══════════════════════════════════════════════════════════════════════════════
# DOCKER_INFO_RETRIEVAL
# ═══════════════════════════════════════════════════════════════════════════════
def get_docker_info() -> Optional[Dict[str, Any]]:
    """Get Docker system information."""
    success, stdout, _ = run_command(['docker', 'info', '--format', '{{json .}}'])
    if success and stdout:
        try:
            return json.loads(stdout)
        except json.JSONDecodeError:
            return None
    return None


def get_docker_version() -> Optional[Dict[str, Any]]:
    """Get Docker version information."""
    success, stdout, _ = run_command(['docker', 'version', '--format', '{{json .}}'])
    if success and stdout:
        try:
            return json.loads(stdout)
        except json.JSONDecodeError:
            return None
    return None


def check_docker_running() -> bool:
    """Check if Docker daemon is running."""
    success, _, _ = run_command(['docker', 'info'], timeout=15)
    return success


# ═══════════════════════════════════════════════════════════════════════════════
# WSL_INTEGRATION_CHECKS
# ═══════════════════════════════════════════════════════════════════════════════
def check_wsl2_integration() -> Dict[str, Any]:
    """Check WSL2 integration status."""
    result = {
        'wsl2_backend': False,
        'distros': [],
        'default_distro': None
    }
    
    # Get Docker info
    info = get_docker_info()
    if info:
        # Check if using WSL2 backend
        os_type = info.get('OSType', '')
        kernel_version = info.get('KernelVersion', '')
        if 'wsl' in kernel_version.lower() or os_type == 'linux':
            result['wsl2_backend'] = True
    
    # List WSL distros
    if platform.system() == 'Windows':
        success, stdout, _ = run_command(['wsl', '-l', '-v'], timeout=10)
        if success:
            lines = stdout.strip().split('\n')[1:]  # Skip header
            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 3:
                    name = parts[0].replace('*', '').strip()
                    version = parts[-1]
                    is_default = '*' in line
                    result['distros'].append({
                        'name': name,
                        'version': version,
                        'default': is_default
                    })
                    if is_default:
                        result['default_distro'] = name
    
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# RESOURCE_CHECKS
# ═══════════════════════════════════════════════════════════════════════════════
def get_docker_resources() -> Dict[str, Any]:
    """Get Docker resource allocation."""
    info = get_docker_info()
    resources = {
        'cpus': 0,
        'memory_gb': 0,
        'storage_driver': 'unknown'
    }
    
    if info:
        resources['cpus'] = info.get('NCPU', 0)
        mem_bytes = info.get('MemTotal', 0)
        resources['memory_gb'] = round(mem_bytes / (1024**3), 1)
        resources['storage_driver'] = info.get('Driver', 'unknown')
    
    return resources


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION_VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════
def validate_configuration() -> Dict[str, bool]:
    """Validate Docker configuration for Week 14 lab."""
    checks = {
        'docker_running': False,
        'sufficient_memory': False,
        'sufficient_cpus': False,
        'compose_available': False,
        'networks_configurable': False,
        'wsl2_backend': False
    }
    
    # Check Docker running
    if check_docker_running():
        checks['docker_running'] = True
        
        # Get resources
        resources = get_docker_resources()
        checks['sufficient_memory'] = resources['memory_gb'] >= 4
        checks['sufficient_cpus'] = resources['cpus'] >= 2
        
        # Check Compose
        success, _, _ = run_command(['docker', 'compose', 'version'])
        checks['compose_available'] = success
        
        # Check network creation capability
        success, _, _ = run_command([
            'docker', 'network', 'create', '--driver', 'bridge', 
            'week14_test_net'
        ])
        if success:
            run_command(['docker', 'network', 'rm', 'week14_test_net'])
            checks['networks_configurable'] = True
        
        # Check WSL2
        wsl_info = check_wsl2_integration()
        checks['wsl2_backend'] = wsl_info['wsl2_backend']
    
    return checks


# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def display_current_configuration() -> None:
    """Display current Docker configuration."""
    print_header("Current Docker Configuration")
    
    if not check_docker_running():
        print_error("Docker is not running")
        print_info("Start Docker Desktop and run this script again")
        return
    
    # Version info
    version = get_docker_version()
    if version:
        client_ver = version.get('Client', {}).get('Version', 'unknown')
        server_ver = version.get('Server', {}).get('Version', 'unknown')
        print(f"Docker Client: {client_ver}")
        print(f"Docker Server: {server_ver}")
    
    # Resource info
    resources = get_docker_resources()
    print(f"\n{Colours.BOLD}Resources:{Colours.ENDC}")
    print(f"  CPUs: {resources['cpus']}")
    print(f"  Memory: {resources['memory_gb']} GB")
    print(f"  Storage Driver: {resources['storage_driver']}")
    
    # WSL2 info
    wsl_info = check_wsl2_integration()
    print(f"\n{Colours.BOLD}WSL2 Integration:{Colours.ENDC}")
    print(f"  WSL2 Backend: {'Yes' if wsl_info['wsl2_backend'] else 'No'}")
    if wsl_info['distros']:
        print(f"  Available Distros:")
        for distro in wsl_info['distros']:
            default = " (default)" if distro['default'] else ""
            print(f"    - {distro['name']} v{distro['version']}{default}")
    
    # Docker info
    info = get_docker_info()
    if info:
        print(f"\n{Colours.BOLD}System Info:{Colours.ENDC}")
        print(f"  OS: {info.get('OperatingSystem', 'unknown')}")
        print(f"  Architecture: {info.get('Architecture', 'unknown')}")
        print(f"  Containers: {info.get('Containers', 0)} "
              f"(Running: {info.get('ContainersRunning', 0)})")
        print(f"  Images: {info.get('Images', 0)}")


def display_recommendations() -> None:
    """Display configuration recommendations."""
    print_header("Configuration Recommendations")
    
    checks = validate_configuration()
    resources = get_docker_resources()
    
    # Memory recommendation
    if not checks['sufficient_memory']:
        print_warning(f"Memory: {resources['memory_gb']} GB (4+ GB recommended)")
        print_info("  Increase Docker Desktop memory allocation:")
        print_info("  Settings > Resources > Advanced > Memory")
    else:
        print_success(f"Memory: {resources['memory_gb']} GB ✓")
    
    # CPU recommendation
    if not checks['sufficient_cpus']:
        print_warning(f"CPUs: {resources['cpus']} (2+ recommended)")
        print_info("  Increase Docker Desktop CPU allocation:")
        print_info("  Settings > Resources > Advanced > CPUs")
    else:
        print_success(f"CPUs: {resources['cpus']} ✓")
    
    # WSL2 recommendation
    if platform.system() == 'Windows':
        if not checks['wsl2_backend']:
            print_warning("WSL2 backend not detected")
            print_info("  Enable WSL2 backend:")
            print_info("  Settings > General > Use the WSL 2 based engine")
        else:
            print_success("WSL2 backend enabled ✓")
    
    # Week 14 specific settings
    print(f"\n{Colours.BOLD}Week 14 Specific Settings:{Colours.ENDC}")
    
    lab_config = {
        'containers': 5,
        'networks': 2,
        'ports': [8080, 8001, 8002, 9090, 9000],
        'estimated_memory': 1.5  # GB
    }
    
    print(f"  Containers required: {lab_config['containers']}")
    print(f"  Networks required: {lab_config['networks']}")
    print(f"  Ports used: {', '.join(map(str, lab_config['ports']))}")
    print(f"  Estimated memory usage: ~{lab_config['estimated_memory']} GB")
    
    if resources['memory_gb'] < lab_config['estimated_memory'] + 2:
        print_warning(f"  Consider allocating at least "
                     f"{lab_config['estimated_memory'] + 2} GB to Docker")


# ═══════════════════════════════════════════════════════════════════════════════
# TROUBLESHOOTING
# ═══════════════════════════════════════════════════════════════════════════════
def troubleshoot_common_issues() -> None:
    """Provide troubleshooting for common Docker issues."""
    print_header("Troubleshooting Common Issues")
    
    issues = [
        {
            "problem": "Docker daemon not responding",
            "symptoms": ["docker info hangs", "Cannot connect to Docker daemon"],
            "solutions": [
                "Restart Docker Desktop",
                "Check Docker Desktop is running in system tray",
                "On Windows: Restart WSL: wsl --shutdown",
                "Check Windows Services for 'Docker Desktop Service'"
            ]
        },
        {
            "problem": "Port already in use",
            "symptoms": ["bind: address already in use", "port is already allocated"],
            "solutions": [
                "Find process: netstat -ano | findstr :<PORT>",
                "Stop conflicting service or change port in docker-compose.yml",
                "Run: docker compose down to stop previous containers"
            ]
        },
        {
            "problem": "Network creation fails",
            "symptoms": ["network with name already exists", "failed to create network"],
            "solutions": [
                "Remove existing network: docker network rm <n>",
                "Run cleanup: python scripts/cleanup.py --full",
                "Restart Docker Desktop"
            ]
        }
    ]
    
    for i, issue in enumerate(issues, 1):
        print(f"{Colours.BOLD}{i}. {issue['problem']}{Colours.ENDC}")
        print(f"   {Colours.YELLOW}Symptoms:{Colours.ENDC}")
        for symptom in issue['symptoms']:
            print(f"     - {symptom}")
        print(f"   {Colours.GREEN}Solutions:{Colours.ENDC}")
        for solution in issue['solutions']:
            print(f"     → {solution}")
        print()


# ═══════════════════════════════════════════════════════════════════════════════
# DIAGNOSTICS
# ═══════════════════════════════════════════════════════════════════════════════
def run_diagnostics() -> int:
    """Run full Docker diagnostics."""
    print_header("Docker Diagnostics")
    
    checks = validate_configuration()
    all_passed = True
    
    for check, passed in checks.items():
        check_name = check.replace('_', ' ').title()
        if passed:
            print_success(check_name)
        else:
            print_error(check_name)
            all_passed = False
    
    print()
    if all_passed:
        print_success("All diagnostics passed! Ready for Week 14 laboratory.")
        return 0
    else:
        print_warning("Some checks failed. Review recommendations above.")
        return 1


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Docker Desktop Configuration Helper - Week 14",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="NETWORKING class - ASE, Informatics | by Revolvix"
    )
    
    parser.add_argument('--diagnose', '-d', action='store_true', help='Run full diagnostics')
    parser.add_argument('--config', '-c', action='store_true', help='Show current configuration')
    parser.add_argument('--recommend', '-r', action='store_true', help='Show recommendations')
    parser.add_argument('--troubleshoot', '-t', action='store_true', help='Show troubleshooting guide')
    parser.add_argument('--all', '-a', action='store_true', help='Show all information')
    
    args = parser.parse_args()
    
    # If no arguments, show all
    if not any([args.diagnose, args.config, args.recommend, args.troubleshoot, args.all]):
        args.all = True
    
    print_header("Docker Configuration Helper - Week 14")
    print("NETWORKING class - ASE, Informatics | by Revolvix")
    
    exit_code = 0
    
    if args.config or args.all:
        display_current_configuration()
    
    if args.diagnose or args.all:
        exit_code = run_diagnostics()
    
    if args.recommend or args.all:
        display_recommendations()
    
    if args.troubleshoot or args.all:
        troubleshoot_common_issues()
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
