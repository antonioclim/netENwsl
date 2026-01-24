# =============================================================================
# Dockerfile — Week 12: Email Protocols and RPC
# NETWORKING class - ASE, Informatics | by Revolvix
# =============================================================================
#
# This image provides a complete Python environment for the Week 12 laboratory,
# including all dependencies for SMTP, JSON-RPC, XML-RPC, and gRPC.
#
# =============================================================================

FROM python:3.12-slim

LABEL maintainer="by Revolvix"
LABEL description="Week 12 Laboratory: Email Protocols and RPC"

WORKDIR /app

# Install system tools for networking and debugging
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    netcat-openbsd \
    tcpdump \
    tshark \
    iputils-ping \
    dnsutils \
    net-tools \
    procps \
    vim-tiny \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for layer caching
COPY setup/requirements.txt /app/setup/requirements.txt

# Install Python dependencies
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/setup/requirements.txt

# Create directories for runtime data
RUN mkdir -p /app/spool /app/logs /app/pcap /app/artifacts

# Copy application code
COPY . /app

# Expose service ports
EXPOSE 1025 6200 6201 6251

# Default command keeps container running
CMD ["bash", "-c", "tail -f /dev/null"]
