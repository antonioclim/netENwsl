# ============================================================
# Dockerfile - Week 2 WSL Starter Kit
# Socket Programming: TCP and UDP
# NETWORKING class - ASE, Informatics | by Revolvix
# ============================================================
# 
# Lightweight container with Python and network tools for
# TCP/UDP socket programming exercises.
#
# Build: docker build -t week2_lab -f docker/Dockerfile .
# Run:   docker run -it --rm week2_lab
#
# ============================================================

FROM python:3.11-slim-bookworm

LABEL maintainer="ASE CSIE - Computer Networks"
LABEL description="Week 2 Socket Programming Laboratory Environment"
LABEL version="1.0.0"
LABEL week="2"

# Environment configuration
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    TERM=xterm-256color

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Network diagnostic tools
    netcat-openbsd \
    net-tools \
    iproute2 \
    iputils-ping \
    iputils-tracepath \
    dnsutils \
    # Packet capture and analysis
    tcpdump \
    tshark \
    # Utilities
    curl \
    wget \
    procps \
    less \
    vim-tiny \
    tree \
    # Build tools (for any pip packages needing compilation)
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create application user (non-root for security)
RUN useradd -m -s /bin/bash -u 1000 student \
    && mkdir -p /app /app/pcap /app/artifacts /app/logs \
    && chown -R student:student /app

# Set working directory
WORKDIR /app

# Copy and install Python requirements
COPY setup/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt

# Copy source code
COPY --chown=student:student src/ /app/src/
COPY --chown=student:student scripts/ /app/scripts/

# Make scripts executable
RUN chmod +x /app/scripts/*.py 2>/dev/null || true

# Create convenient aliases
RUN echo 'alias ll="ls -la"' >> /home/student/.bashrc \
    && echo 'alias tcp-server="python3 /app/src/exercises/ex_2_01_tcp.py server"' >> /home/student/.bashrc \
    && echo 'alias tcp-client="python3 /app/src/exercises/ex_2_01_tcp.py client"' >> /home/student/.bashrc \
    && echo 'alias udp-server="python3 /app/src/exercises/ex_2_02_udp.py server"' >> /home/student/.bashrc \
    && echo 'alias udp-client="python3 /app/src/exercises/ex_2_02_udp.py client"' >> /home/student/.bashrc \
    && echo 'export PS1="\[\033[1;32m\]week2-lab\[\033[0m\]:\[\033[1;34m\]\w\[\033[0m\]\$ "' >> /home/student/.bashrc

# Switch to non-root user
USER student

# Expose ports for TCP and UDP applications
EXPOSE 9090/tcp 9091/udp 8080/tcp

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python3 -c "import socket; s=socket.socket(); s.close(); print('OK')" || exit 1

# Default command - interactive shell
CMD ["/bin/bash"]
