#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# verify_lab_environment.sh
# Complete Laboratory Environment Verification Script
# 
# Computer Networks Course - ASE Bucharest, CSIE
# Repository: https://github.com/antonioclim/netENwsl
# 
# This script verifies all components required for the 14-week laboratory course.
# Run this script in your Ubuntu WSL terminal to ensure proper configuration.
# ═══════════════════════════════════════════════════════════════════════════════

# Colour definitions for output formatting
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
WHITE='\033[1;37m'
NC='\033[0m' # No Colour

# Counters for summary
ERRORS=0
WARNINGS=0
PASSED=0

# ═══════════════════════════════════════════════════════════════════════════════
# Helper Functions
# ═══════════════════════════════════════════════════════════════════════════════

print_header() {
    echo ""
    echo -e "${WHITE}╔═══════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${WHITE}║${CYAN}        COMPUTER NETWORKS LABORATORY — ENVIRONMENT VERIFICATION           ${WHITE}║${NC}"
    echo -e "${WHITE}║${NC}                           by Revolvix                                     ${WHITE}║${NC}"
    echo -e "${WHITE}║${NC}                                                                           ${WHITE}║${NC}"
    echo -e "${WHITE}║${NC}  Repository: https://github.com/antonioclim/netENwsl                      ${WHITE}║${NC}"
    echo -e "${WHITE}║${NC}  Weeks: 1-14 | Networks: 10.0.N.0/24 | Portainer: Port 9000 (RESERVED)   ${WHITE}║${NC}"
    echo -e "${WHITE}╚═══════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_section() {
    echo ""
    echo -e "${BLUE}▶ $1${NC}"
    echo -e "${BLUE}$(printf '─%.0s' {1..75})${NC}"
}

check_required() {
    local description="$1"
    local command="$2"
    local version_info=""
    
    if eval "$command" &>/dev/null; then
        # Try to get version info if available
        if [[ "$description" == *"Python"* ]]; then
            version_info=$(python3 --version 2>/dev/null | cut -d' ' -f2)
        elif [[ "$description" == *"Docker Engine"* ]]; then
            version_info=$(docker --version 2>/dev/null | grep -oP '\d+\.\d+\.\d+' | head -1)
        elif [[ "$description" == *"Docker Compose"* ]]; then
            version_info=$(docker compose version 2>/dev/null | grep -oP '\d+\.\d+\.\d+' | head -1)
        elif [[ "$description" == *"Git"* ]]; then
            version_info=$(git --version 2>/dev/null | grep -oP '\d+\.\d+\.\d+')
        fi
        
        if [[ -n "$version_info" ]]; then
            echo -e "  ${GREEN}✓${NC} $description ${CYAN}(v$version_info)${NC}"
        else
            echo -e "  ${GREEN}✓${NC} $description"
        fi
        ((PASSED++))
        return 0
    else
        echo -e "  ${RED}✗${NC} $description ${RED}[REQUIRED - MISSING]${NC}"
        ((ERRORS++))
        return 1
    fi
}

check_optional() {
    local description="$1"
    local command="$2"
    
    if eval "$command" &>/dev/null; then
        echo -e "  ${GREEN}✓${NC} $description"
        ((PASSED++))
        return 0
    else
        echo -e "  ${YELLOW}○${NC} $description ${YELLOW}(optional - not installed)${NC}"
        ((WARNINGS++))
        return 1
    fi
}

check_python_package() {
    local package="$1"
    local import_name="${2:-$1}"
    local required="${3:-optional}"
    
    if python3 -c "import $import_name" &>/dev/null; then
        local version=$(pip3 show "$package" 2>/dev/null | grep "^Version:" | cut -d' ' -f2)
        if [[ -n "$version" ]]; then
            echo -e "  ${GREEN}✓${NC} $package ${CYAN}(v$version)${NC}"
        else
            echo -e "  ${GREEN}✓${NC} $package"
        fi
        ((PASSED++))
        return 0
    else
        if [[ "$required" == "required" ]]; then
            echo -e "  ${RED}✗${NC} $package ${RED}[REQUIRED - MISSING]${NC}"
            ((ERRORS++))
        else
            echo -e "  ${YELLOW}○${NC} $package ${YELLOW}(optional - not installed)${NC}"
            ((WARNINGS++))
        fi
        return 1
    fi
}

check_port_available() {
    local port="$1"
    local service="$2"
    
    if ss -tuln 2>/dev/null | grep -q ":$port "; then
        echo -e "  ${GREEN}✓${NC} Port $port is in use by $service"
        ((PASSED++))
        return 0
    else
        echo -e "  ${YELLOW}○${NC} Port $port is not in use ($service not running)"
        ((WARNINGS++))
        return 1
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
# Main Verification Sections
# ═══════════════════════════════════════════════════════════════════════════════

print_header

# ─────────────────────────────────────────────────────────────────────────────
# Section 1: System Information
# ─────────────────────────────────────────────────────────────────────────────
print_section "SYSTEM INFORMATION"

echo -e "  ${WHITE}Hostname:${NC}      $(hostname)"
echo -e "  ${WHITE}Username:${NC}      $(whoami)"
echo -e "  ${WHITE}Home:${NC}          $HOME"
echo -e "  ${WHITE}Shell:${NC}         $SHELL"

# Check if running in WSL
if grep -qi microsoft /proc/version 2>/dev/null; then
    echo -e "  ${WHITE}Environment:${NC}   ${GREEN}WSL2 (Windows Subsystem for Linux)${NC}"
    WSL_VERSION=$(cat /proc/version | grep -oP 'microsoft-standard-WSL\d*' | head -1)
    echo -e "  ${WHITE}WSL Kernel:${NC}    $WSL_VERSION"
else
    echo -e "  ${WHITE}Environment:${NC}   ${YELLOW}Native Linux (not WSL)${NC}"
fi

# Ubuntu version
if command -v lsb_release &>/dev/null; then
    UBUNTU_VERSION=$(lsb_release -d 2>/dev/null | cut -f2)
    echo -e "  ${WHITE}Distribution:${NC}  $UBUNTU_VERSION"
fi

echo -e "  ${WHITE}Kernel:${NC}        $(uname -r)"
echo -e "  ${WHITE}Architecture:${NC}  $(uname -m)"

# ─────────────────────────────────────────────────────────────────────────────
# Section 2: Core Components
# ─────────────────────────────────────────────────────────────────────────────
print_section "CORE COMPONENTS (Required)"

check_required "Python 3.11+" "python3 --version | grep -qE 'Python 3\.(1[1-9]|[2-9][0-9])'"
check_required "pip3 (Python package manager)" "pip3 --version"
check_required "Git (version control)" "git --version"
check_required "curl (HTTP client)" "curl --version"
check_required "wget (file downloader)" "wget --version"

# ─────────────────────────────────────────────────────────────────────────────
# Section 3: Docker Installation
# ─────────────────────────────────────────────────────────────────────────────
print_section "DOCKER ENVIRONMENT"

check_required "Docker Engine" "docker --version"
check_required "Docker Compose (v2 plugin)" "docker compose version"
check_required "Docker daemon running" "docker info"
check_required "Docker without sudo" "docker ps"

# Check Docker socket permissions
if [[ -S /var/run/docker.sock ]]; then
    if [[ -r /var/run/docker.sock ]] && [[ -w /var/run/docker.sock ]]; then
        echo -e "  ${GREEN}✓${NC} Docker socket accessible"
        ((PASSED++))
    else
        echo -e "  ${YELLOW}○${NC} Docker socket permissions may need adjustment"
        ((WARNINGS++))
    fi
fi

# Check docker group membership
if groups | grep -q docker; then
    echo -e "  ${GREEN}✓${NC} User '$(whoami)' is in docker group"
    ((PASSED++))
else
    echo -e "  ${YELLOW}○${NC} User '$(whoami)' is not in docker group"
    ((WARNINGS++))
fi

# ─────────────────────────────────────────────────────────────────────────────
# Section 4: Portainer (Global Service - Port 9000 RESERVED)
# ─────────────────────────────────────────────────────────────────────────────
print_section "PORTAINER CE (Global Service — Port 9000 RESERVED)"

echo -e "  ${MAGENTA}⚠ IMPORTANT: Port 9000 is ALWAYS reserved for Portainer${NC}"
echo -e "  ${MAGENTA}  Never use port 9000 in weekly laboratory docker-compose files!${NC}"
echo ""

if docker ps 2>/dev/null | grep -q portainer; then
    PORTAINER_STATUS=$(docker ps --filter name=portainer --format "{{.Status}}" 2>/dev/null)
    PORTAINER_PORTS=$(docker ps --filter name=portainer --format "{{.Ports}}" 2>/dev/null)
    echo -e "  ${GREEN}✓${NC} Portainer container is running"
    echo -e "    ${WHITE}Status:${NC} $PORTAINER_STATUS"
    echo -e "    ${WHITE}Ports:${NC}  $PORTAINER_PORTS"
    ((PASSED++))
    
    # Check if port 9000 is accessible
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:9000 2>/dev/null | grep -qE "200|302"; then
        echo -e "  ${GREEN}✓${NC} Portainer web UI accessible at ${CYAN}http://localhost:9000${NC}"
        ((PASSED++))
    else
        echo -e "  ${YELLOW}○${NC} Portainer may not be fully initialised yet"
        ((WARNINGS++))
    fi
else
    echo -e "  ${RED}✗${NC} Portainer container is NOT running"
    echo -e "    ${WHITE}To start Portainer:${NC}"
    echo -e "    docker volume create portainer_data"
    echo -e "    docker run -d -p 9000:9000 --name portainer --restart=always \\"
    echo -e "      -v /var/run/docker.sock:/var/run/docker.sock \\"
    echo -e "      -v portainer_data:/data portainer/portainer-ce:latest"
    ((ERRORS++))
fi

# Check Portainer volume
if docker volume ls 2>/dev/null | grep -q portainer_data; then
    echo -e "  ${GREEN}✓${NC} Portainer data volume exists"
    ((PASSED++))
else
    echo -e "  ${YELLOW}○${NC} Portainer data volume not found"
    ((WARNINGS++))
fi

# ─────────────────────────────────────────────────────────────────────────────
# Section 5: Network Analysis Tools
# ─────────────────────────────────────────────────────────────────────────────
print_section "NETWORK ANALYSIS TOOLS"

check_required "tcpdump (packet capture)" "which tcpdump"
check_required "netcat (nc - network utility)" "which nc"
check_optional "tshark (Wireshark CLI)" "which tshark"
check_optional "nmap (port scanner)" "which nmap"
check_optional "iperf3 (bandwidth testing)" "which iperf3"
check_optional "traceroute" "which traceroute"
check_optional "dig (DNS lookup)" "which dig"
check_optional "host (DNS lookup)" "which host"
check_optional "ss (socket statistics)" "which ss"
check_optional "ip (network config)" "which ip"

# ─────────────────────────────────────────────────────────────────────────────
# Section 6: Python Libraries (Core)
# ─────────────────────────────────────────────────────────────────────────────
print_section "PYTHON LIBRARIES — Core (Required)"

check_python_package "docker" "docker" "required"
check_python_package "requests" "requests" "required"
check_python_package "flask" "flask" "required"
check_python_package "colorama" "colorama" "required"
check_python_package "PyYAML" "yaml" "required"

# ─────────────────────────────────────────────────────────────────────────────
# Section 7: Python Libraries (Network Analysis)
# ─────────────────────────────────────────────────────────────────────────────
print_section "PYTHON LIBRARIES — Network Analysis"

check_python_package "scapy" "scapy.all" "optional"
check_python_package "dpkt" "dpkt" "optional"
check_python_package "netifaces" "netifaces" "optional"
check_python_package "psutil" "psutil" "optional"

# ─────────────────────────────────────────────────────────────────────────────
# Section 8: Python Libraries (Protocol-Specific)
# ─────────────────────────────────────────────────────────────────────────────
print_section "PYTHON LIBRARIES — Protocol Support (Weeks 9-14)"

check_python_package "paramiko" "paramiko" "optional"           # SSH (Week 10-11)
check_python_package "pyftpdlib" "pyftpdlib" "optional"         # FTP (Week 9, 11)
check_python_package "paho-mqtt" "paho.mqtt.client" "optional"  # MQTT (Week 13)
check_python_package "dnspython" "dns.resolver" "optional"      # DNS (Week 10-11)
check_python_package "grpcio" "grpc" "optional"                 # gRPC (Week 12)
check_python_package "grpcio-tools" "grpc_tools" "optional"     # gRPC tools (Week 12)
check_python_package "protobuf" "google.protobuf" "optional"    # Protocol Buffers (Week 12)

# ─────────────────────────────────────────────────────────────────────────────
# Section 9: Running Containers
# ─────────────────────────────────────────────────────────────────────────────
print_section "DOCKER CONTAINERS (Currently Running)"

CONTAINER_COUNT=$(docker ps --format "{{.Names}}" 2>/dev/null | wc -l)

if [[ $CONTAINER_COUNT -gt 0 ]]; then
    echo -e "  ${WHITE}Active containers: $CONTAINER_COUNT${NC}"
    echo ""
    docker ps --format "  {{.Names}}: {{.Status}} ({{.Ports}})" 2>/dev/null | head -10
    if [[ $CONTAINER_COUNT -gt 10 ]]; then
        echo "  ... and $((CONTAINER_COUNT - 10)) more"
    fi
else
    echo -e "  ${YELLOW}○${NC} No containers currently running"
fi

# ─────────────────────────────────────────────────────────────────────────────
# Section 10: Docker Networks
# ─────────────────────────────────────────────────────────────────────────────
print_section "DOCKER NETWORKS"

echo -e "  ${WHITE}Existing networks:${NC}"
docker network ls --format "  {{.Name}}: {{.Driver}}" 2>/dev/null | grep -v "^  host:" | grep -v "^  none:" | head -15

# Check for week-specific networks
echo ""
echo -e "  ${WHITE}Week-specific networks (10.0.N.0/24 pattern):${NC}"
WEEK_NETS=$(docker network ls --format "{{.Name}}" 2>/dev/null | grep -E "^week[0-9]+")
if [[ -n "$WEEK_NETS" ]]; then
    echo "$WEEK_NETS" | while read net; do
        SUBNET=$(docker network inspect "$net" 2>/dev/null | grep -oP '"Subnet": "\K[^"]+' | head -1)
        echo -e "    ${GREEN}✓${NC} $net ${CYAN}($SUBNET)${NC}"
    done
else
    echo -e "    ${YELLOW}○${NC} No week-specific networks found (created when labs start)"
fi

# ─────────────────────────────────────────────────────────────────────────────
# Section 11: Port Availability Check
# ─────────────────────────────────────────────────────────────────────────────
print_section "PORT STATUS (Common Laboratory Ports)"

echo -e "  ${WHITE}Checking key ports:${NC}"

# Port 9000 - MUST be Portainer
if ss -tuln 2>/dev/null | grep -q ":9000 "; then
    if docker ps 2>/dev/null | grep -q portainer; then
        echo -e "  ${GREEN}✓${NC} Port 9000: Portainer ${GREEN}(correct)${NC}"
        ((PASSED++))
    else
        echo -e "  ${RED}✗${NC} Port 9000: In use but NOT by Portainer! ${RED}[CONFLICT]${NC}"
        ((ERRORS++))
    fi
else
    echo -e "  ${YELLOW}○${NC} Port 9000: Available (Portainer not running)"
    ((WARNINGS++))
fi

# Other common ports
declare -A COMMON_PORTS=(
    [8080]="HTTP services"
    [8001]="Backend 1 (Week 14)"
    [8002]="Backend 2 (Week 14)"
    [9090]="TCP Echo (Week 14)"
    [1883]="MQTT plaintext (Week 13)"
    [8883]="MQTT TLS (Week 13)"
    [1025]="SMTP (Week 12)"
    [6200]="JSON-RPC (Week 12)"
)

for port in "${!COMMON_PORTS[@]}"; do
    if ss -tuln 2>/dev/null | grep -q ":$port "; then
        echo -e "  ${CYAN}●${NC} Port $port: In use (${COMMON_PORTS[$port]})"
    fi
done

# ─────────────────────────────────────────────────────────────────────────────
# Section 12: File System Checks
# ─────────────────────────────────────────────────────────────────────────────
print_section "FILE SYSTEM ACCESS"

# Check access to common directories
if [[ -d "/mnt/d/NETWORKING" ]]; then
    echo -e "  ${GREEN}✓${NC} D:\\NETWORKING accessible at /mnt/d/NETWORKING"
    ((PASSED++))
elif [[ -d "/mnt/c/Users" ]]; then
    echo -e "  ${YELLOW}○${NC} Windows C: drive accessible, D:\\NETWORKING not found"
    echo -e "    Consider creating: mkdir -p /mnt/d/NETWORKING"
    ((WARNINGS++))
else
    echo -e "  ${YELLOW}○${NC} Windows drives not mounted (may be native Linux)"
    ((WARNINGS++))
fi

# Check home directory
if [[ -w "$HOME" ]]; then
    echo -e "  ${GREEN}✓${NC} Home directory writable: $HOME"
    ((PASSED++))
else
    echo -e "  ${RED}✗${NC} Home directory not writable!"
    ((ERRORS++))
fi

# ─────────────────────────────────────────────────────────────────────────────
# Section 13: Wireshark Guidance
# ─────────────────────────────────────────────────────────────────────────────
print_section "WIRESHARK GUIDANCE (Windows)"

echo -e "  ${WHITE}Wireshark must be installed on Windows (not in WSL).${NC}"
echo ""
echo -e "  ${WHITE}Installation:${NC}"
echo -e "    1. Download from: https://www.wireshark.org/download.html"
echo -e "    2. Install with Npcap (required for packet capture)"
echo -e "    3. Select interface: ${CYAN}vEthernet (WSL)${NC}"
echo ""
echo -e "  ${WHITE}Common filters for this course:${NC}"
echo -e "    ${CYAN}tcp${NC}                    - All TCP traffic"
echo -e "    ${CYAN}udp${NC}                    - All UDP traffic"
echo -e "    ${CYAN}icmp${NC}                   - Ping packets"
echo -e "    ${CYAN}http${NC}                   - HTTP traffic"
echo -e "    ${CYAN}tcp.port == 9090${NC}       - TCP Echo (Week 14)"
echo -e "    ${CYAN}ip.addr == 10.0.N.x${NC}    - Week N network traffic"
echo -e "    ${CYAN}mqtt${NC}                   - MQTT protocol (Week 13)"

# ═══════════════════════════════════════════════════════════════════════════════
# Summary
# ═══════════════════════════════════════════════════════════════════════════════
echo ""
echo -e "${WHITE}═══════════════════════════════════════════════════════════════════════════${NC}"
echo -e "${WHITE}                            VERIFICATION SUMMARY                            ${NC}"
echo -e "${WHITE}═══════════════════════════════════════════════════════════════════════════${NC}"
echo ""

# Calculate totals
TOTAL=$((PASSED + ERRORS + WARNINGS))

echo -e "  ${GREEN}✓ Passed:${NC}     $PASSED"
echo -e "  ${RED}✗ Errors:${NC}     $ERRORS"
echo -e "  ${YELLOW}○ Warnings:${NC}   $WARNINGS"
echo -e "  ${WHITE}─────────────────────${NC}"
echo -e "  ${WHITE}Total checks:${NC} $TOTAL"
echo ""

if [[ $ERRORS -eq 0 ]]; then
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  ✅ ALL REQUIRED COMPONENTS ARE INSTALLED AND CONFIGURED CORRECTLY!       ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════════════════╝${NC}"
    if [[ $WARNINGS -gt 0 ]]; then
        echo ""
        echo -e "  ${YELLOW}Note: $WARNINGS optional component(s) not installed.${NC}"
        echo -e "  ${YELLOW}These may be needed for specific weeks. Install as required.${NC}"
    fi
else
    echo -e "${RED}╔═══════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║  ❌ $ERRORS REQUIRED COMPONENT(S) MISSING OR MISCONFIGURED                  ║${NC}"
    echo -e "${RED}╚═══════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "  ${WHITE}Please address the errors above before starting laboratory exercises.${NC}"
    echo -e "  ${WHITE}Refer to: https://github.com/antonioclim/netENwsl/blob/main/PrerequisitesEN.md${NC}"
fi

echo ""
echo -e "${WHITE}═══════════════════════════════════════════════════════════════════════════${NC}"
echo -e "  ${WHITE}Standard Credentials:${NC}"
echo -e "    Ubuntu WSL:  ${CYAN}stud / stud${NC}"
echo -e "    Portainer:   ${CYAN}stud / studstudstud${NC} (http://localhost:9000)"
echo ""
echo -e "  ${WHITE}Remember:${NC}"
echo -e "    • Port ${RED}9000${NC} is ${RED}ALWAYS${NC} reserved for Portainer"
echo -e "    • Weekly networks use ${CYAN}10.0.N.0/24${NC} pattern"
echo -e "    • Week 14 TCP Echo uses port ${CYAN}9090${NC} (not 9000)"
echo -e "${WHITE}═══════════════════════════════════════════════════════════════════════════${NC}"
echo ""

# Exit with error count as return code
exit $ERRORS
