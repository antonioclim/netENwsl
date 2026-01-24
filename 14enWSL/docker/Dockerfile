# =============================================================================
# Dockerfile - Week 14 Laboratory Environment
# NETWORKING class - ASE, Informatics | by Revolvix
# =============================================================================
#
# This container provides a complete environment for networking exercises:
#   - Python 3.11 runtime for applications
#   - Network analysis tools (tcpdump, tshark, curl, netcat)
#   - Development utilities
#
# =============================================================================

FROM python:3.11-slim-bookworm

LABEL maintainer="NETWORKING class - ASE, Informatics"
LABEL description="Week 14 Laboratory Environment"
LABEL version="1.0"
LABEL week="14"

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Bucharest

# Update and install required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Networking tools
    iputils-ping \
    iproute2 \
    net-tools \
    netcat-openbsd \
    curl \
    wget \
    dnsutils \
    traceroute \
    # Packet analysis
    tcpdump \
    tshark \
    # Development utilities
    vim-tiny \
    nano \
    jq \
    # Process management
    procps \
    # Build essentials (for some Python packages)
    gcc \
    libc-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Configure tshark for non-root capture (optional in container context)
RUN setcap cap_net_raw,cap_net_admin+eip /usr/bin/dumpcap 2>/dev/null || true

# Set working directory
WORKDIR /app

# Copy and install Python requirements first (for layer caching)
COPY setup/requirements.txt /app/setup/
RUN pip install --no-cache-dir -r /app/setup/requirements.txt || true

# Copy application source code
COPY src/ /app/src/
COPY scripts/ /app/scripts/
COPY docs/ /app/docs/

# Create directories for artifacts and captures
RUN mkdir -p /app/artifacts /app/pcap

# Set executable permissions on scripts
RUN find /app/scripts -name "*.py" -exec chmod +x {} \; 2>/dev/null || true
RUN find /app/src -name "*.py" -exec chmod +x {} \; 2>/dev/null || true

# Environment configuration
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

# Expose common ports
# Backend servers
EXPOSE 8001 8002
# Load balancer
EXPOSE 8080
# TCP echo server
EXPOSE 9000

# Volume mount points for persistent data
VOLUME ["/app/artifacts", "/app/pcap"]

# Default command
CMD ["bash"]

# =============================================================================
# BUILD AND RUN EXAMPLES
# =============================================================================
#
# Build image:
#   docker build -t week14-lab:latest -f docker/Dockerfile .
#
# Run interactive shell:
#   docker run -it --rm week14-lab:latest
#
# Run backend server:
#   docker run -d -p 8001:8001 week14-lab:latest \
#       python3 /app/src/apps/backend_server.py --port 8001 --id backend1
#
# Run with volume for artifacts:
#   docker run -it --rm -v $(pwd)/artifacts:/app/artifacts week14-lab:latest
#
# =============================================================================
