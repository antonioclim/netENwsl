#!/bin/bash
# verify_lab_environment.sh
# Script de verificare completă a mediului de laborator

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

ERRORS=0
WARNINGS=0

echo ""
echo "╔═══════════════════════════════════════════════════════════════════════════╗"
echo "║        VERIFICARE MEDIU LABORATOR REȚELE DE CALCULATOARE                  ║"
echo "║                         by Revolvix                                        ║"
echo "╚═══════════════════════════════════════════════════════════════════════════╝"
echo ""

check_required() {
    if eval "$2" &>/dev/null; then
        echo -e "  ${GREEN}✓${NC} $1"
    else
        echo -e "  ${RED}✗${NC} $1"
        ((ERRORS++))
    fi
}

check_optional() {
    if eval "$2" &>/dev/null; then
        echo -e "  ${GREEN}✓${NC} $1"
    else
        echo -e "  ${YELLOW}○${NC} $1 (opțional)"
        ((WARNINGS++))
    fi
}

echo -e "${BLUE}▶ INFORMAȚII SISTEM${NC}"
echo "  Hostname: $(hostname)"
echo "  Ubuntu: $(lsb_release -d 2>/dev/null | cut -f2)"
echo "  Kernel: $(uname -r)"
echo "  User: $(whoami)"
echo ""

echo -e "${BLUE}▶ COMPONENTE PRINCIPALE${NC}"
check_required "Python 3.11+" "python3 --version | grep -E 'Python 3\.(1[1-9]|[2-9][0-9])'"
check_required "pip3" "pip3 --version"
check_required "Git" "git --version"
check_required "curl" "curl --version"
check_required "wget" "wget --version"
echo ""

echo -e "${BLUE}▶ DOCKER${NC}"
check_required "Docker Engine" "docker --version"
check_required "Docker Compose" "docker compose version"
check_required "Docker daemon activ" "docker info"
check_required "Docker fără sudo" "docker ps"
echo ""

echo -e "${BLUE}▶ PORTAINER (Port 9000)${NC}"
if docker ps | grep -q portainer; then
    echo -e "  ${GREEN}✓${NC} Portainer rulează pe portul 9000"
else
    echo -e "  ${YELLOW}○${NC} Portainer nu rulează (porniți manual dacă e necesar)"
    ((WARNINGS++))
fi
echo ""

echo -e "${BLUE}▶ CONTAINERE ACTIVE${NC}"
docker ps --format "  {{.Names}}: {{.Status}}" 2>/dev/null || echo "  (niciun container activ)"
echo ""

echo -e "${BLUE}▶ INSTRUMENTE REȚEA${NC}"
check_required "tcpdump" "which tcpdump"
check_optional "tshark" "which tshark"
check_required "netcat" "which nc"
check_optional "nmap" "which nmap"
check_optional "iperf3" "which iperf3"
echo ""

echo -e "${BLUE}▶ BIBLIOTECI PYTHON${NC}"
check_required "docker" "python3 -c 'import docker'"
check_required "scapy" "python3 -c 'import scapy.all'"
check_required "dpkt" "python3 -c 'import dpkt'"
check_required "requests" "python3 -c 'import requests'"
check_required "flask" "python3 -c 'import flask'"
check_optional "paramiko" "python3 -c 'import paramiko'"
check_optional "pyftpdlib" "python3 -c 'import pyftpdlib'"
check_optional "paho-mqtt" "python3 -c 'import paho.mqtt.client'"
check_optional "dnspython" "python3 -c 'import dns.resolver'"
check_optional "grpcio" "python3 -c 'import grpc'"
echo ""

echo "═══════════════════════════════════════════════════════════════════════════"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ TOATE COMPONENTELE NECESARE SUNT INSTALATE CORECT!${NC}"
    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}   ($WARNINGS componente opționale lipsesc)${NC}"
    fi
else
    echo -e "${RED}❌ $ERRORS COMPONENTĂ(E) NECESARĂ(E) LIPSEȘTE/LIPSESC${NC}"
fi
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""

exit $ERRORS