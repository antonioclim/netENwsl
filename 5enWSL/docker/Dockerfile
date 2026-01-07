# Dockerfile — Week 5 WSL Kit
# NETWORKING class - ASE, Informatics | by Revolvix
# =====================================
# Container for Python IP addressing exercises
#
# Build:   docker build -t week5-wslkit docker/
# Run:     docker run --rm -it week5-wslkit

FROM python:3.11-slim

LABEL maintainer="NETWORKING class - ASE, Informatics"
LABEL description="Week 5 WSL Kit - Network Layer: IP Addressing"
LABEL version="1.0"

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TERM=xterm-256color
ENV PYTHONPATH=/app

# Install networking tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    iputils-ping \
    iproute2 \
    net-tools \
    tcpdump \
    traceroute \
    dnsutils \
    netcat-openbsd \
    curl \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Create directory structure
RUN mkdir -p /app/src /app/docs /app/pcap /app/artifacts

# Set permissions
RUN chmod 755 /app

# Verification at build time
RUN python3 -c "import ipaddress; print('Python networking modules: OK')"

# Default entrypoint
ENTRYPOINT ["/bin/bash"]

# Default command (displays help)
CMD ["-c", "echo 'Week 5 WSL Kit - IP Addressing Laboratory'; echo 'Run: python src/exercises/ex_5_01_cidr_flsm.py --help'; exec bash"]
