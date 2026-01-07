# ============================================================================
# Dockerfile - Container environment for Week 6 (NAT/PAT & SDN)
# NETWORKING class - ASE, Informatics | by Revolvix
#
# Provides a complete environment with Mininet, Open vSwitch, and OS-Ken
# for NAT/PAT and SDN laboratory exercises.
# ============================================================================

FROM ubuntu:22.04

LABEL maintainer="Revolvix"
LABEL description="Environment for Week 6 Laboratory - NAT/PAT & SDN"
LABEL version="1.0"

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Bucharest

# Install base system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Python environment
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    # Network utilities
    net-tools \
    iproute2 \
    iptables \
    iputils-ping \
    iputils-arping \
    traceroute \
    dnsutils \
    netcat-openbsd \
    curl \
    wget \
    # Packet capture and analysis
    tcpdump \
    tshark \
    # System utilities
    conntrack \
    bridge-utils \
    procps \
    psmisc \
    sudo \
    vim \
    nano \
    less \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Mininet and Open vSwitch
RUN apt-get update && apt-get install -y --no-install-recommends \
    mininet \
    openvswitch-switch \
    openvswitch-common \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip3 install --no-cache-dir --break-system-packages \
    # SDN Controller framework
    os-ken>=2.4.0 \
    # Packet crafting
    scapy>=2.5.0 \
    # HTTP client
    requests>=2.28.0 \
    # YAML parsing
    pyyaml>=6.0 \
    # Docker API
    docker>=6.0.0

# Create non-root user for development
RUN useradd -m -s /bin/bash -G sudo student && \
    echo "student ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Create working directories
RUN mkdir -p /home/student/week6/{src,scripts,pcap,artifacts,configs} && \
    chown -R student:student /home/student/week6

# Copy project files
WORKDIR /home/student/week6
COPY --chown=student:student . .

# Make scripts executable
RUN find . -type f -name "*.sh" -exec chmod +x {} \; 2>/dev/null || true
RUN find . -type f -name "*.py" -exec chmod +x {} \; 2>/dev/null || true

# Configure Open vSwitch directories
RUN mkdir -p /var/run/openvswitch /var/log/openvswitch

# Create startup script
COPY --chown=root:root <<'EOF' /usr/local/bin/start-week6.sh
#!/bin/bash
# Week 6 Laboratory Startup Script

echo "=========================================="
echo "  Week 6: NAT/PAT & SDN Laboratory"
echo "  NETWORKING class - ASE, Informatics"
echo "=========================================="
echo ""

# Start Open vSwitch
echo "[*] Starting Open vSwitch..."
service openvswitch-switch start 2>/dev/null || ovs-ctl start 2>/dev/null || true
sleep 2

# Verify OVS is running
if ovs-vsctl show >/dev/null 2>&1; then
    echo "[✓] Open vSwitch is running"
else
    echo "[!] Open vSwitch failed to start (some features may not work)"
fi

echo ""
echo "Useful commands:"
echo "  make check      - Verify dependencies"
echo "  make nat-demo   - Start NAT topology"
echo "  make sdn-demo   - Start SDN topology"
echo "  make clean      - Cleanup Mininet"
echo ""

# Execute the passed command or start shell
exec "$@"
EOF

RUN chmod +x /usr/local/bin/start-week6.sh

# Expose OpenFlow controller ports
EXPOSE 6633 6653

# Persistent volumes
VOLUME ["/home/student/week6/pcap", "/home/student/week6/artifacts"]

# Entry point
ENTRYPOINT ["/usr/local/bin/start-week6.sh"]
CMD ["/bin/bash"]

# ============================================================================
# Build:
#   docker build -t week6-networking:latest .
#
# Run interactive:
#   docker run -it --privileged --net=host week6-networking:latest
#
# Run with mounted volumes:
#   docker run -it --privileged --net=host \
#     -v $(pwd)/pcap:/home/student/week6/pcap \
#     week6-networking:latest
# ============================================================================
