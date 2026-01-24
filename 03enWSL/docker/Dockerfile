# ============================================================================
# Dockerfile — Week 3 Laboratory Container
# NETWORKING class - ASE, Informatics | by Revolvix
# ============================================================================
#
# Build:
#   docker build -t week3-lab .
#
# Run (interactive):
#   docker run -it --rm --privileged week3-lab
#
# ============================================================================

FROM ubuntu:22.04

LABEL maintainer="ASE-CSIE Computer Networks"
LABEL description="Week 3: Network Programming (UDP broadcast/multicast, TCP tunnel)"
LABEL version="1.0"

# ─── Environment Variables ────────────────────────────────────────────────

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV TZ=Europe/Bucharest

# ─── System Packages ──────────────────────────────────────────────────────

RUN apt-get update && apt-get install -y --no-install-recommends \
    # Python
    python3 \
    python3-pip \
    python3-venv \
    # Network tools
    iproute2 \
    iputils-ping \
    tcpdump \
    tshark \
    netcat-openbsd \
    iperf3 \
    traceroute \
    dnsutils \
    net-tools \
    nmap \
    # Utilities
    vim \
    nano \
    less \
    curl \
    wget \
    ca-certificates \
    procps \
    && rm -rf /var/lib/apt/lists/*

# ─── Python Packages ──────────────────────────────────────────────────────

RUN pip3 install --no-cache-dir \
    scapy \
    && rm -rf /root/.cache

# ─── Wireshark/tshark Configuration ───────────────────────────────────────

RUN echo "wireshark-common wireshark-common/install-setuid boolean true" | \
    debconf-set-selections

# ─── Working Directory ────────────────────────────────────────────────────

WORKDIR /app

# ─── Exposed Ports ────────────────────────────────────────────────────────
# Common ports used in Week 3 exercises

EXPOSE 5007/udp
EXPOSE 5008/udp
EXPOSE 8080/tcp
EXPOSE 9090/tcp

# ─── Default Command ──────────────────────────────────────────────────────

CMD ["bash", "-c", "echo 'Week 3 Lab Container Ready'; exec bash"]
