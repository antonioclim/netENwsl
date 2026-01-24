# ==============================================================================
# Dockerfile - Week 4 WSL Starter Kit
# Custom TCP/UDP Protocol Development Environment
# ==============================================================================
# NETWORKING class - ASE, Informatics | by Revolvix
#
# Purpose:
# - Provide a minimal, reproducible container for protocol development
# - Support TEXT, BINARY TCP, and UDP sensor protocol servers
# - Enable packet capture and analysis within the container
#
# Usage:
#   docker build -t week4_lab .
#   docker run -p 5400:5400 -p 5401:5401 -p 5402:5402/udp week4_lab
# ==============================================================================

FROM python:3.11-slim

# Labels
LABEL maintainer="ASE CSIE - Computer Networks"
LABEL description="Week 4 Laboratory - Custom Protocol Development"
LABEL version="1.0.0"

# Set working directory
WORKDIR /app

# Install minimal runtime tools for networking introspection
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       iproute2 \
       iputils-ping \
       netcat-openbsd \
       procps \
       tcpdump \
       tshark \
       curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy application code
COPY src/ /app/src/
COPY scripts/ /app/scripts/
COPY tests/ /app/tests/

# Ensure scripts are executable
RUN chmod +x /app/scripts/*.py /app/tests/*.py 2>/dev/null || true

# Create non-root user for safer defaults
RUN useradd -m -u 1000 -s /bin/bash netuser \
    && mkdir -p /app/artifacts /app/pcap \
    && chown -R netuser:netuser /app

# Allow non-root packet capture (requires container capabilities)
RUN setcap cap_net_raw,cap_net_admin+eip /usr/bin/tcpdump 2>/dev/null || true

# Switch to non-root user
USER netuser

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/home/netuser/.local/bin:${PATH}"

# Week 4 default ports
EXPOSE 5400/tcp
EXPOSE 5401/tcp
EXPOSE 5402/udp

# Health check - verify TEXT server is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import socket; s=socket.socket(); s.settimeout(2); s.connect(('localhost',5400)); s.close()" || exit 1

# Default command - start TEXT protocol server
CMD ["python3", "-u", "src/apps/text_proto_server.py", "--port", "5400"]
